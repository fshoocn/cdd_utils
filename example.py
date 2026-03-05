from cdd_v2 import loadfile 
from pathlib import Path

def format_hex(data: bytes) -> str:
    """格式化字节为 hex 字符串"""
    if not data:
        return "(empty)"
    return ' '.join(f'{b:02X}' for b in data)

if __name__ == "__main__":
    cdd_path = Path(__file__).resolve().parent / "testfile" / "XIAOPENG_CMS019-A1.cdd"
    db = loadfile.load_cdd(cdd_path, strict=False)
    print(db.services.Vehicle_Manufacturer_FOTA_Special_Part_Number_Write.positive_responses.encode_default())  # 按索引访问
    req_hex = db.services.Vehicle_Manufacturer_FOTA_Special_Part_Number_Write.request.encode_default()
    print(f"  请求 Hex: {format_hex(req_hex)}")