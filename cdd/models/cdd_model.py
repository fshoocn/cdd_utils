from dataclasses import field
from typing import Optional, List, Union
from pydantic.dataclasses import dataclass as pyd_dataclass
from enum import Enum

from .candela import Comp, Name, Desc, Excl, Textmap, Tuv, Diagclass as DiagClass

class ByteOrder(str, Enum):
    BIG_ENDIAN = "21"
    LITTLE_ENDIAN = "12"

class DisplayFormat(str, Enum):
    HEX = "hex"
    DECIMAL = "dec"
    TEXT = "text"
    BINARY = "bin"
    FLOAT = "flt"

class Encoding(str, Enum):
    UNSIGNED = "uns"
    ASCII = "asc"
    UTF8 = "utf"
    BCD = "bcd"
    FLOAT = "flt"
    DOUBLE = "dbl"

class Quantity(str, Enum):
    ATOM = "atom"
    FIELD = "field"

    

@pyd_dataclass(config={"validate_assignment": True})
class DiagnosticElement():
    """
    诊断数据的基础元素定义。

    描述诊断报文中一个数据元素的通用属性（名称、描述、编码、长度等），
    作为所有具体元素类型的父类。

    Attributes:
        id (Optional[str]): 元素唯一标识。
        name (Name): 元素名称。
        description (Optional[Desc]): 元素描述（可多语言）。
        qualifier (Optional[str]): 限定符/别名。
        spec (Optional[str]): 语义规范/角色，该数据扮演什么角色。
        must (int): 是否必须存在 (1=必须, 0=可选)。

        constvalue (int): 常量的固定值。
        response_suppress_bit (Optional[int]): 响应抑制位 (respsupbit)，仅在 spec='sub' 时有效。
        bit_length (int): 基础长度（bit），在 ATOM 下用于确定元素长度。
        display_format (DisplayFormat): 展示数据格式（仅影响显示层）。
        encoding (Encoding): 编码格式（实际数据的语义/物理编码）。
        byte_order (ByteOrder): 字节序。
        sig (int): 精度/线性映射偏移（依据具体编码或线性映射解释）。
        quantity (Quantity): 数量类型。(atom（此时bl决定长度），field(此时bl和minsz、maxsz决定长度)
        minsz (int): 最小长度（与 FIELD 配合使用）。
        maxsz (int): 最大长度（与 FIELD 配合使用）。
        excl (Optional[Excl]): 排除数据定义（当值落在排除集合时视为无效）。
        ref_id (Optional[str]): 引用ID，用于关联请求与响应中的相同数据。
    """

    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    spec: Optional[str] = None
    must: Optional[int] = None

    constvalue: Optional[int] = None
    response_suppress_bit: Optional[int] = None
    
    bit_length: int = 0
    display_format: DisplayFormat = DisplayFormat.HEX
    encoding: Encoding = Encoding.UNSIGNED
    byte_order: ByteOrder = ByteOrder.BIG_ENDIAN
    sig : Optional[int] = None
    quantity: Quantity = Quantity.ATOM
    minsz: int = 1
    maxsz: int = 1

    excl : List[Excl] = field(default_factory=list)

    ref_id: Optional[str] = None

@pyd_dataclass(config={"validate_assignment": True})
class NumIterElement(DiagnosticElement):
    """
    数字迭代器元素，表示由计数器确定次数的可重复数据块。

    NUMITERCOMP (Number Iterator Component) 用于描述通过一个计数器组件确定重复次数的数据结构。
    selref 引用一个组件（通常是一个字节），其值决定了迭代次数。
    例如 DTC 计数器为 3，则后续的 DTC 数据块会重复 3 次。

    Attributes:
        must (int): 是否必须存在 (1=必须, 0=可选)。
        selref (Optional[str]): 选择器引用 ID，指向计数器组件。
        selbm (Optional[int]): 选择器位掩码 (selector bit mask)。
        children (List[DiagnosticElement]): 每次迭代包含的子元素列表。
    """
    must: int = 1
    selref: Optional[str] = None
    selbm: Optional[int] = None
    children: List["DiagnosticElement"] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class TextTableElement(DiagnosticElement):
    """
    文本映射元素，通过 `textmap` 将原始值映射为文本。

    Attributes:
        textmap (Optional[Textmap]): 文本映射数据。
    """
    textmap : List[Textmap] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class LinCompElement(DiagnosticElement):
    """
    线性转换元素，通过 `comp` 将原始值映射为物理值。

    Attributes:
        comp (Optional[Comp]): 线性转换参数。
    """
    comp : Optional[Comp] = None

@pyd_dataclass(config={"validate_assignment": True})
class StructElement(DiagnosticElement):
    """
    结构体元素，包含一组有序的子元素。

    Attributes:
        min_num_of_items (int): 最小重复次数。
        max_num_of_items (Optional[int]): 最大重复次数 (None 表示不限制)。
        struct (List[DiagnosticElement]): 子元素列表。
    """
    min_num_of_items: int = 0
    max_num_of_items: Optional[int] = None
    struct : List[DiagnosticElement] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class RecordElement(StructElement):
    """
    记录型结构体元素，带有记录序号。

    Attributes:
        record_number (int): 记录序号。
    """
    record_number: int = 0


@pyd_dataclass(config={"validate_assignment": True})
class DidElement(DiagnosticElement):
    """
    记录DID元素

    Attributes:
        did (int): DID 编号。
        struct (List[DiagnosticElement]): 子元素列表。
    """
    did: int = 0
    struct : List[DiagnosticElement] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class MuxCase:
    """
    多路复用分支定义
    
    Attributes:
        s (int): 分支对应的起始值 (Selector Value)。
        e (int): 分支对应的结束值。
        structure (StructElement): 该分支对应的数据结构。
    """
    s: int
    e: int
    structure: StructElement

    def __post_init__(self):
        if self.s > self.e:
            raise ValueError("MuxCase.s must be <= MuxCase.e")

@pyd_dataclass(config={"validate_assignment": True})
class MultiplexedElement(DiagnosticElement):
    """
    多路复用元素，根据选择器值进入不同分支结构。

    Attributes:
        ref_textmap (Optional[TextTableElement]): 选择器文本映射。
        cases (List[MuxCase]): 复用分支集合。
        structure (Optional[StructElement]): 默认分支对应的数据结构。
    """

    ref_textmap: Optional[TextTableElement] = None 
    cases: List[MuxCase] = field(default_factory=list)
    structure: Optional[StructElement] = None

@pyd_dataclass(config={"validate_assignment": True})
class PlaceholderElement(DiagnosticElement):
    """
    占位数据类型，用于填充信号中的保留位或未使用位，常见于19服务DTC故障状态信息中。
    """
    description: Desc = field(
        default_factory=lambda: Desc(
            tuv=[
                Tuv(lang="en-US", value="Placeholder for reserved or unused bits in the signal."),
                Tuv(lang="zh-CN", value="信号中保留位或未使用位的占位符。"),
            ]
        )
    )
    spec: str = "no"

@pyd_dataclass(config={"validate_assignment": True})
class StateGroup():
    """
    状态组定义，用于描述服务可执行条件与状态转换。

    Attributes:
        name (Name): 状态组名称。
        qualifier (Optional[str]): 限定符/别名。
        spec (str): 语义规范/角色。
        state (List[Name]): 状态列表。
    """
    name: Name
    qualifier: Optional[str] = None
    spec: str = ""
    state: List[Name] = field(default_factory=list)

# ---------
@pyd_dataclass(config={"validate_assignment": True})
class DiagnosticMessage:
    """
    诊断报文定义，包含报文级元信息与元素列表。

    Attributes:
        id (Optional[str]): 报文唯一标识。
        name (Name): 报文名称。
        description (Optional[Desc]): 报文描述（可多语言）。
        qualifier (Optional[str]): 限定符/别名。
        elements (List[DiagnosticElement]): 报文元素列表。
    """
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    elements: List[DiagnosticElement] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class DiagnosticService:
    """
    诊断服务定义，描述服务的请求/响应与执行条件。

    Attributes:
        id (Optional[str]): 服务唯一标识。
        service_name (Name): 服务名称。
        protocol_svc_name (Name): 协议服务名称。
        description (Optional[Desc]): 服务描述（可多语言）。
        qualifier (Optional[str]): 限定符/别名。
        is_used (bool): 服务是否被使用。
        func (bool): 是否支持功能寻址。
        phys (bool): 是否支持物理寻址。
        resp_on_phys (bool): 物理寻址是否响应。
        resp_on_func (bool): 功能寻址是否响应。
        respsupbit (bool): 是否支持响应抑制位。
        request (Optional[DiagnosticMessage]): 请求报文。
        positive_responses (Optional[DiagnosticMessage]): 正响应报文。
        negative_responses (Optional[DiagnosticMessage]): 负响应报文。
        mayBeExec (List[int]): 可执行条件，记录 StateGroups 下标。
        trans (List[int]): 状态转换，记录 StateGroups 下标。
    """
    service_name: Name
    protocol_svc_name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    
    is_used: bool = False
    func: bool = False
    phys: bool = False
    resp_on_phys: bool = False
    resp_on_func: bool = False
    respsupbit: bool = False

    request: Optional[DiagnosticMessage] = None
    positive_responses: Optional[DiagnosticMessage] = None
    negative_responses: Optional[DiagnosticMessage] = None
    mayBeExec: List[int] = field(default_factory=list)
    trans: List[int] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class DiagnosticInstance:
    """
    诊断实例，用于组织多个服务。

    Attributes:
        id (Optional[str]): 分组唯一标识。
        name (Name): 分组名称。
        description (Optional[Desc]): 分组描述（可多语言）。
        qualifier (Optional[str]): 限定符/别名。
        services (List[DiagnosticService]): 服务列表。
    """
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None

    services: List[DiagnosticService] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class DiagnosticGroup:
    """
    诊断服务分组，用于组织多个诊断实例。

    Attributes:
        id (Optional[str]): 分组唯一标识。
        name (Name): 分组名称。
        description (Optional[Desc]): 分组描述（可多语言）。
        qualifier (Optional[str]): 限定符/别名。
        diagInst (List[DiagnosticInstance]): 诊断实例列表。
    """
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None

    diagInst: List[DiagnosticInstance] = field(default_factory=list)


@pyd_dataclass(config={"validate_assignment": True})
class EcuAttributes:
    """
    ECU 诊断信息

    Attributes:
        request_can_id (Optional[int]): 物理请求 CAN ID。
        response_can_id (Optional[int]): 物理响应 CAN ID。
        functional_request_can_id (Optional[int]): 功能请求 CAN ID。
        p2_client (Optional[int]): 客户端 P2 定时参数。
        p2_server (Optional[int]): 服务端 P2 定时参数。
        p2_star_client (Optional[int]): 客户端 P2* 定时参数。
        p2_star_server (Optional[int]): 服务端 P2* 定时参数。
        st_min (Optional[int]): TP 发送最小间隔（STmin）。
        block_size (Optional[int]): TP 块大小（Block Size）。
    """
    request_can_id: Optional[int] = None
    response_can_id: Optional[int] = None
    functional_request_can_id: Optional[int] = None
    
    p2_client: Optional[int] = None
    p2_server: Optional[int] = None
    p2_star_client: Optional[int] = None
    p2_star_server: Optional[int] = None
    
    st_min: Optional[int] = None
    block_size: Optional[int] = None

@pyd_dataclass(config={"validate_assignment": True})
class EcuModel:
    id: str
    name: Name
    qualifier: Optional[str] = None

    diag_list: List[Union[DiagnosticInstance, DiagnosticGroup]] = field(default_factory=list)

@pyd_dataclass(config={"validate_assignment": True})
class CddModel:
    dtdvers: Optional[str] = None
    state_groups: List[StateGroup] = field(default_factory=list)
    ecu: Optional[EcuModel] = None
