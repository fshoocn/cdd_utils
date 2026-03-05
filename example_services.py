"""
CDD V2 — 打印所有服务及其参数 + 默认 Hex 数据
================================================

遍历所有诊断服务，展示：
- 请求/正响应/负响应 的元素结构
- 每个元素的类型、编码属性、默认值
- 请求报文的默认 Hex 编码（常量不变，自由参数填最小值/第一个有效值）

运行方式：
    python Backend/example_services.py
    python Backend/example_services.py Backend/testfile/GAC_A20_SBM.cdd
"""
import math
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.WARNING)

# ━━━ 兼容 import ━━━
try:
    from Backend.cdd_v2 import load_cdd
    from Backend.cdd_v2.models.base import (
        CodedElement, IdentifiableElement, ByteOrder, Encoding, Quantity,
    )
    from Backend.cdd_v2.models.elements import (
        ConstElement, TextTableElement, LinCompElement, PlaceholderElement,
    )
    from Backend.cdd_v2.models.containers import (
        StructElement, MultiplexedElement, NumIterElement, DidElement,
    )
except ModuleNotFoundError:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from Backend.cdd_v2 import load_cdd
    from Backend.cdd_v2.models.base import (
        CodedElement, IdentifiableElement, ByteOrder, Encoding, Quantity,
    )
    from Backend.cdd_v2.models.elements import (
        ConstElement, TextTableElement, LinCompElement, PlaceholderElement,
    )
    from Backend.cdd_v2.models.containers import (
        StructElement, MultiplexedElement, NumIterElement, DidElement,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  编码工具
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_element_name(elem) -> str:
    """获取元素的显示名称"""
    if elem.qualifier:
        return elem.qualifier
    if hasattr(elem, 'name') and elem.name and elem.name.tuv:
        return elem.name.tuv[0].value
    return elem.id or "?"


def get_element_type_tag(elem) -> str:
    """获取元素类型简写"""
    if isinstance(elem, ConstElement):
        return "CONST"
    if isinstance(elem, TextTableElement):
        return "TEXT"
    if isinstance(elem, LinCompElement):
        return "LIN"
    if isinstance(elem, PlaceholderElement):
        return "GAP"
    if isinstance(elem, StructElement):
        return "STRUCT"
    if isinstance(elem, MultiplexedElement):
        return "MUX"
    if isinstance(elem, NumIterElement):
        return "NUMITER"
    if isinstance(elem, DidElement):
        return "DID"
    if isinstance(elem, CodedElement):
        return "CODED"
    return type(elem).__name__


def get_default_value(elem) -> int:
    """获取元素的默认填充值：常量→constvalue，文本表→第一个有效s值，
    线性→comp.s（起始值），否则→0"""
    if isinstance(elem, CodedElement) and elem.constvalue is not None:
        return elem.constvalue

    if isinstance(elem, TextTableElement) and elem.textmap:
        for tm in elem.textmap:
            if tm.s is not None:
                return int(tm.s)
        return 0

    if isinstance(elem, LinCompElement) and elem.comp:
        if elem.comp.s is not None:
            return int(elem.comp.s)
        return 0

    return 0


def get_default_display(elem) -> str:
    """获取默认值的人类可读描述"""
    val = get_default_value(elem)
    bl = getattr(elem, 'bit_length', None) or 0

    if isinstance(elem, ConstElement):
        return f"= 0x{val:02X}" if bl <= 8 else f"= 0x{val:0{math.ceil(bl/4)}X}"

    if isinstance(elem, TextTableElement) and elem.textmap:
        for tm in elem.textmap:
            if int(tm.s) == val:
                text_str = ""
                if tm.text and tm.text.tuv:
                    text_str = tm.text.tuv[0].value
                return f"→ {val} ({text_str})" if text_str else f"→ {val}"
        return f"→ {val}"

    if isinstance(elem, LinCompElement) and elem.comp:
        f_val = elem.comp.f or 1
        o_val = elem.comp.o or 0
        phys = val * f_val + o_val
        unit = ""
        return f"→ raw={val} phys={phys}{unit}"

    if isinstance(elem, PlaceholderElement):
        return f"= 0x{0:02X} (padding)"

    if bl > 0:
        return f"→ 0x{val:0{max(2, math.ceil(bl/4))}X}"
    return f"→ {val}"


def encode_message(msg) -> bytes:
    """编码整个消息为字节流（优先使用模型内置编码）。"""
    if msg is None:
        return b''
    if hasattr(msg, 'encode_default'):
        return msg.encode_default()
    return b''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  打印工具
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def format_hex(data: bytes) -> str:
    """格式化字节为 hex 字符串"""
    if not data:
        return "(empty)"
    return ' '.join(f'{b:02X}' for b in data)


def print_element(elem, indent: int = 4, prefix: str = ""):
    """打印单个元素信息"""
    pad = ' ' * indent
    name = get_element_name(elem)
    tag = get_element_type_tag(elem)
    bl = getattr(elem, 'bit_length', None)
    spec = getattr(elem, 'spec', None)
    qty = getattr(elem, 'quantity', None)
    minsz = getattr(elem, 'minsz', None)
    maxsz = getattr(elem, 'maxsz', None)

    # 位长/字节长信息
    bl_str = ""
    if bl:
        if qty == Quantity.FIELD or str(qty) == 'field':
            total_bits = bl * (minsz or 1)
            total_bytes = math.ceil(total_bits / 8)
            if minsz == maxsz:
                bl_str = f"  {total_bytes}B (field bl={bl}×{minsz})"
            else:
                max_bits = bl * (maxsz or minsz or 1)
                max_bytes = math.ceil(max_bits / 8)
                bl_str = f"  {total_bytes}~{max_bytes}B (field bl={bl}×{minsz}~{maxsz})"
        else:
            bl_str = f"  bl={bl}"

    spec_str = f"  spec={spec}" if spec else ""
    default_str = ""
    if isinstance(elem, CodedElement):
        default_str = f"  {get_default_display(elem)}"

    # 容器重复次数（EOSITERCOMP / StructElement with variable count）
    repeat_str = ""
    if isinstance(elem, StructElement):
        lo = getattr(elem, 'min_num_of_items', 1) or 0
        hi = getattr(elem, 'max_num_of_items', None)
        if hi is None or hi != lo:
            hi_s = str(hi) if hi is not None else "∞"
            repeat_str = f"  repeat={lo}..{hi_s}"

    must_str = ""
    if hasattr(elem, 'must') and elem.must is not None:
        must_str = "  [必选]" if elem.must else "  [可选]"

    print(f"{pad}{prefix}[{tag:7s}] {name:<45s}{bl_str}{spec_str}{default_str}{repeat_str}{must_str}")

    # TextTableElement: 显示所有 NRC / TextMap 条目
    if isinstance(elem, TextTableElement) and elem.textmap:
        tm_pad = ' ' * (indent + 10)
        for tm in elem.textmap:
            text_str = ""
            if tm.text and tm.text.tuv:
                text_str = tm.text.tuv[0].value
            s_hex = f"0x{int(tm.s):02X}" if tm.s is not None else "?"
            print(f"{tm_pad}{s_hex}: {text_str}")

    # 容器类型递归打印子元素
    children = getattr(elem, 'children', ())
    if children:
        for i, child in enumerate(children):
            print_element(child, indent + 6, prefix=f"{i+1}. ")

    # MUX 打印分支
    if isinstance(elem, MultiplexedElement):
        if elem.cases:
            for case in elem.cases:
                case_pad = ' ' * (indent + 6)
                text = ""
                if elem.ref_textmap and isinstance(elem.ref_textmap, TextTableElement):
                    for tm in elem.ref_textmap.textmap:
                        if tm.s is not None and int(tm.s) == case.s and tm.text and tm.text.tuv:
                            text = f" ({tm.text.tuv[0].value})"
                            break
                print(f"{case_pad}CASE {case.s}-{case.e}{text}:")
                if case.structure:
                    for i, child in enumerate(case.structure.children):
                        print_element(child, indent + 12, prefix=f"{i+1}. ")


def print_message(msg, label: str, indent: int = 2):
    """打印消息及其编码的 Hex"""
    if msg is None:
        print(f"{'':>{indent}}{label}: (无)")
        return
    data = encode_message(msg)
    print(f"{'':>{indent}}{label} ({len(msg.elements)} 元素)  Hex: {format_hex(data)}")
    for elem in msg.elements:
        print_element(elem, indent + 2)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  主程序
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    if len(sys.argv) > 1:
        cdd_path = Path(sys.argv[1])
    else:
        cdd_path = Path(__file__).parent / "testfile" / "XIAOPENG_CMS019-A1.cdd"

    if not cdd_path.exists():
        print(f"CDD 文件不存在: {cdd_path}")
        sys.exit(1)

    db = load_cdd(cdd_path, strict=False)

    print("=" * 90)
    print(f"  CDD: {cdd_path.name}")
    print(f"  ECU: {db.ecu.name.tuv[0].value}  (DTD {db.model.dtdvers})")
    print(f"  服务总数: {len(db.services)}    警告: {len(db.warnings)}")
    print("=" * 90)
    print()

    for idx, svc in enumerate(db.services):
        if not svc.is_used:
            continue

        svc_name = svc.qualifier or "(unnamed)"
        protocol = ""
        if svc.protocol_svc_name and svc.protocol_svc_name.tuv:
            protocol = svc.protocol_svc_name.tuv[0].value

        # 编码请求
        req_hex = encode_message(svc.request)

        addr_mode = []
        if svc.func:
            addr_mode.append("func")
        if svc.phys:
            addr_mode.append("phys")

        print(f"━━━ [{idx:3d}] {svc_name} ━━━")
        print(f"  协议: {protocol}  寻址: {','.join(addr_mode) or '?'}")
        print(f"  请求 Hex: {format_hex(req_hex)}")
        print()

        # 请求
        print_message(svc.request, "请求 (Request)")
        print()

        # 正响应
        print_message(svc.positive_responses, "正响应 (Positive Response)")
        print()

        # 负响应
        print_message(svc.negative_responses, "负响应 (Negative Response)")

        print()
        print()


if __name__ == "__main__":
    main()
