import logging
import argparse
import json
import dataclasses
from pathlib import Path
from xsdata.formats.dataclass.parsers import XmlParser
from enum import Enum

# 假设 main.py 在 Backend 根目录下运行
from cdd.models.candela import Candela
from cdd.cdd_parser import CddParser
from cdd.utils.exceptions import CddException, ErrorFormatter

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

def setup_logging(debug: bool = False, log_file: str = "app.log"):
    # 确保日志文件目录存在
    log_path = Path(log_file)
    if log_path.parent != Path('.'):
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # 配置 handlers
    # 控制台：默认 INFO，如果开启 debug 则是 DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)

    # 文件：始终 DEBUG
    file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
    file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,  # 根 Logger 必须设为 DEBUG，否则 DEBUG 消息会被过滤，无法到达 file_handler
        format="%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            console_handler,
            file_handler
        ],
        force=True
    )

def main():
    parser = argparse.ArgumentParser(description="CDD 解析工具")
    parser.add_argument("cdd_file", nargs="?", default=r"Backend\testfile\GAC_A20_SBM.cdd", help="CDD 文件路径")
    parser.add_argument("--strict", action="store_true", default=True, help="是否开启严格模式")
    parser.add_argument("--debug", action="store_true", default=False, help="是否开启调试模式（显示详细堆栈）")
    
    args = parser.parse_args()
    
    file_path = Path(args.cdd_file)
    if not file_path.exists():
        # 尝试相对于当前工作目录查找
        file_path = Path.cwd() / args.cdd_file
        if not file_path.exists():
            print(f"错误: 文件未找到 {args.cdd_file}")
            return

    setup_logging(debug=args.debug)
    logger = logging.getLogger(__name__)
    logger.info(f"正在解析文件: {file_path}")

    try:
        candela = XmlParser().from_path(file_path, Candela)
        cdd_parser = CddParser(candela, strict=args.strict)
        
        # 这里可以添加打印结果或其他逻辑
        if cdd_parser.ecu_model:
            logger.info(f"解析成功! ECU ID: {cdd_parser.ecu_model.ecu.id if hasattr(cdd_parser.ecu_model.ecu, 'id') else 'Unknown'}")
            
            # 导出到 JSON 文件
            output_file = Path("parsed_data.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cdd_parser.ecu_model, f, cls=EnhancedJSONEncoder, ensure_ascii=False, indent=2)
            logger.info(f"数据已导出到: {output_file.absolute()}")
        
    except CddException as e:
        # 使用美观的错误格式化
        error_msg = e.format_error(show_traceback=args.debug)
        print(error_msg.encode('utf-8', errors='replace').decode('utf-8'))
    except Exception as e:
        # 非 CDD 异常，使用通用格式化器
        formatter = ErrorFormatter()
        error_msg = formatter.format_exception(e, show_traceback=args.debug)
        print(error_msg.encode('utf-8', errors='replace').decode('utf-8'))

if __name__ == "__main__":
    main()




