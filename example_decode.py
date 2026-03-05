"""
CDD V2 — 解码示例（DiagnosticMessage.decode_values）
=====================================================

演示内容：
1) 按模型默认值编码，再解码（round-trip）
2) 给定 Hex 字节串，按消息结构解码

运行方式：
    python Backend/example_decode.py
    python Backend/example_decode.py Backend/testfile/1.cdd ReadAllIdentified request
    python Backend/example_decode.py Backend/testfile/1.cdd ReadAllIdentified positive "59 02 00 00 00 00 00"
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.WARNING)

try:
    from Backend.cdd import load_cdd
except ModuleNotFoundError:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from Backend.cdd import load_cdd


def normalize_hex_to_bytes(text: str) -> bytes:
    clean = text.replace("0x", "").replace(" ", "").replace("_", "")
    if len(clean) % 2 != 0:
        clean = "0" + clean
    return bytes.fromhex(clean)


def format_hex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data) if data else "(empty)"


def pick_message(service, msg_kind: str):
    kind = msg_kind.lower()
    if kind in ("req", "request"):
        return service.request, "Request"
    if kind in ("pos", "positive"):
        return service.positive_responses, "Positive Response"
    if kind in ("neg", "negative"):
        return service.negative_responses, "Negative Response"
    raise ValueError(f"不支持的消息类型: {msg_kind}，可选 request/positive/negative")


def main():
    cdd_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Backend/testfile/1.cdd")
    svc_qual = sys.argv[2] if len(sys.argv) > 2 else "EraseMemory_Start"
    msg_kind = sys.argv[3] if len(sys.argv) > 3 else "request"
    input_hex = sys.argv[4] if len(sys.argv) > 4 else "31 01 FF 00 22 11 22 33 44 55 66 77 88"

    if not cdd_path.exists():
        print(f"CDD 文件不存在: {cdd_path}")
        sys.exit(1)

    db = load_cdd(cdd_path, strict=False)

    service = next((s for s in db.services if s.qualifier == svc_qual), None)
    if service is None:
        print(f"未找到服务: {svc_qual}")
        print("可选服务示例:")
        for s in db.services[:20]:
            if s.qualifier:
                print(f"  - {s.qualifier}")
        sys.exit(1)

    message, title = pick_message(service, msg_kind)
    if message is None:
        print(f"服务 {svc_qual} 没有 {title}")
        sys.exit(1)

    print("=" * 88)
    print(f"CDD: {cdd_path.name}")
    print(f"Service: {service.qualifier}")
    print(f"Message: {title}")
    print("=" * 88)

    # 1) round-trip: encode_default -> decode_values
    encoded = message.encode_default()
    decoded_from_model = message.decode_values(encoded)

    print("\n[1] 模型默认编码 -> 解码")
    print(f"Encoded Hex: {format_hex(encoded)}")
    print("Decoded JSON:")
    print(json.dumps(decoded_from_model, ensure_ascii=False, indent=2))

    # 2) 外部 Hex 解码（可选）
    if input_hex:
        raw = normalize_hex_to_bytes(input_hex)
        decoded_from_hex = message.decode_values(raw)
        print("\n[2] 外部 Hex -> 解码")
        print(f"Input Hex : {format_hex(raw)}")
        print("Decoded JSON:")
        print(json.dumps(decoded_from_hex, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
