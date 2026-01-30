import copy
import logging as pylogging
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import validate_call
from xsdata.formats.dataclass.parsers import XmlParser

from .models.cdd_model import CddModel
from .utils.exceptions import (
    DuplicateIdError,
    IdNotFoundError,
    ParserExecutionError,
    CddParseError,
)
from .utils.logging import logging
from .parsers.factory import ParserFactory

from .models.candela import Candela

@logging
class CddParser:
    @validate_call
    def __init__(self, candela: Candela, strict: bool = True):
        """初始化解析器并建立原始对象索引"""
        self.candela = candela
        self.strict = strict
        self._parser_factory = ParserFactory()

        # 索引：所有带 id 的原始对象
        self.raw_data: Dict[str, Any] = {}
        # 索引：已解析过的对象（可直接复用）
        self.analyzed_data: Dict[str, Any] = {}

        # 启动时先建立 ID 索引，便于后续按需解析
        self._index_raw_data(self.candela)
        # 解析主入口
        self.ecu_model = self._parser()
        
    def _register_obj_id(self, obj: Any) -> None:
        """注册对象 ID，处理冲突策略"""
        obj_id = getattr(obj, 'id', None)
        # 如果 id 不存在或是空字符串，尝试使用 oid
        if not obj_id:
            obj_id = getattr(obj, 'oid', None)
            
        if obj_id is None:
            return

        if obj_id in self.raw_data:
            if self.strict:
                self._logger.error(f'发现重复ID: {obj_id} 对象: {obj}')
                raise DuplicateIdError(
                    obj_id=obj_id,
                    existing_obj=self.raw_data[obj_id],
                    new_obj=obj
                )
            else:
                self._logger.warning(f'发现重复ID (跳过): {obj_id} 对象: {obj}')
                return  # 兼容模式：保留旧值，跳过新值
        self.raw_data[obj_id] = obj

    # 遍历 Candela对象下面所有带ID的原始对象，然后存入 raw_data 索引
    def _index_raw_data(self, obj: Any, seen: Optional[set] = None):
        """递归遍历对象图并建立 raw_data 索引"""
        if obj is None:
            return
        if seen is None:
            seen = set()
        obj_identity = id(obj)
        if obj_identity in seen:
            return
        seen.add(obj_identity)
        
        # 1. 如果对象有 id 字段，则尝试注册索引,假如不存在id,但是存在oid，也注册索引
        if hasattr(obj, 'id') or hasattr(obj, 'oid'):
            self._register_obj_id(obj)
            
        # 2. 展开对象内容（支持 dict/list/tuple/set/对象字段/slots）
        if isinstance(obj, dict):
            for v in obj.values():
                self._index_raw_data(v, seen)
        elif isinstance(obj, (list, tuple, set)):
            for item in obj:
                self._index_raw_data(item, seen)
        elif hasattr(obj, '__dict__'):
            for v in obj.__dict__.values():
                self._index_raw_data(v, seen)
        elif hasattr(obj, '__slots__'):
            for slot in obj.__slots__:
                self._index_raw_data(getattr(obj, slot, None), seen)

    def get_analyzed_data_from_id(self, ref_id: str) -> Any:
        """根据 ref_id 获取对应的已解析对象
        
        如果对象已解析则直接返回缓存；否则调用 ParserFactory 进行实时解析并缓存。
        
        Raises:
            IdNotFoundError: 当 ref_id 为空或在索引中未找到时抛出
            ParserExecutionError: 当解析过程中发生错误时抛出（仅 strict 模式）
        """
        if ref_id is None:
            self._logger.error('引用ID为空')
            raise IdNotFoundError(ref_id="None", context="引用ID为空")
        
        # 优先走缓存
        if ref_id in self.analyzed_data:
            self._logger.debug(f'命中缓存 ID: {ref_id}')
            # 深拷贝以防止外部修改已解析对象
            element = copy.deepcopy(self.analyzed_data[ref_id])
            return element

        # 假如不在已解析索引中，则从原始数据索引中获取
        if ref_id not in self.raw_data:
            self._logger.error(f'引用ID未找到: {ref_id}')
            raise IdNotFoundError(ref_id=ref_id, context="ID 不在原始数据索引中")

        # 命中原始索引
        raw_obj = self.raw_data[ref_id]
        
        # 调用工厂进行解析，并传入自身作为回调以便递归处理引用
        try:
            self._logger.debug(f'开始解析对象 ID: {ref_id}')
            analyzed_obj = self._parser_factory.parse(
                raw_obj, 
                get_data_from_id=self.get_analyzed_data_from_id,
                raw_data_map=self.raw_data,
                strict=self.strict
            )
        except CddParseError:
            # 自定义异常直接向上传播
            if self.strict:
                raise
            else:
                self._logger.warning(f"解析对象 {ref_id} 失败, 将返回 None.")
                analyzed_obj = None
        except Exception as e:
            # 其他未预期的异常包装为 ParserExecutionError
            if self.strict:
                self._logger.error(f"解析对象出错 {ref_id}: {e}")
                raise ParserExecutionError(
                    parser_name="Unknown",
                    obj_id=ref_id,
                    original_error=e
                ) from e
            else:
                self._logger.warning(f"解析对象 {ref_id} 时发生未知错误, 将返回 None. 错误信息: {e}")
                analyzed_obj = None
                
        # 缓存解析结果（包括 None，用于避免重复报错）
        self.analyzed_data[ref_id] = analyzed_obj
        if analyzed_obj is None:
            self._logger.debug(f'解析对象 ID: {ref_id} 结果为 None')
            return None
        else:
            self._logger.debug(f'完成解析对象 ID: {ref_id}')
            element = copy.deepcopy(analyzed_obj)
            return element

    def _parser(self) -> CddModel:
        """解析 Candela 对象的主入口，返回 CddModel"""
        self._logger.info('开始解析 Candela 对象')
        cdd_model = CddModel()
        # 解析版本号
        cdd_model.dtdvers = self.candela.dtdvers
        self._logger.info(f'解析 dtdvers: {cdd_model.dtdvers}')
        # 解析 ecu
        cdd_model.ecu = self.get_analyzed_data_from_id(self.candela.ecudoc.ecu.id)
        # self._logger.info(f'解析 ecu: {cdd_model.ecu}')
        # 打印解析到的diag个数
        diag_count = cdd_model.ecu.diag_list.__len__()
        diag_Name_list = []
        for diag in cdd_model.ecu.diag_list:
            diag_Name_list.append(diag.service_name.tuv[0].value if hasattr(diag, 'service_name') else diag.name.tuv[0].value)
        self._logger.info(f'解析 diagnostics 数量: {diag_count}，Names: {diag_Name_list}')
        self._logger.info('完成解析 Candela 对象')
        return cdd_model
    

if __name__ == "__main__":
    # pylogging.basicConfig(
    #     level=pylogging.INFO,
    #     format="%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s",
    # )
    candela = XmlParser().from_path(Path(r"Backend\testfile\1.cdd"), Candela)
    parser = CddParser(candela, strict=True)
    pass

# python -m Backend.cdd.cdd_parser