"""编解码工具函数"""
from typing import Optional


def bcd_encode(value: int) -> bytes:
    """BCD 编码"""
    s = str(value)
    if len(s) % 2:
        s = '0' + s
    result = bytearray()
    for i in range(0, len(s), 2):
        high = int(s[i])
        low = int(s[i + 1])
        result.append((high << 4) | low)
    return bytes(result)


def bcd_decode(data: bytes) -> int:
    """BCD 解码"""
    result = 0
    for byte in data:
        high = (byte >> 4) & 0x0F
        low = byte & 0x0F
        result = result * 100 + high * 10 + low
    return result


def twos_complement(value: int, bit_length: int) -> int:
    """二进制补码转换（有符号数）"""
    if value & (1 << (bit_length - 1)):
        return value - (1 << bit_length)
    return value


def sign_extend(value: int, bit_length: int, target_bits: int = 32) -> int:
    """符号扩展"""
    if value & (1 << (bit_length - 1)):
        mask = ((1 << target_bits) - 1) ^ ((1 << bit_length) - 1)
        return value | mask
    return value


def parse_textmap_s(s) -> int:
    """将 textmap 的 s/e 值解析为整数。

    支持两种格式:
    - 普通整数/字符串: '31' → 31
    - 元组字符串: '(31,0,0)' → 0x1F0000  (各字节拼接为大端整数)
    """
    if s is None:
        return 0
    if isinstance(s, (int, float)):
        return int(s)
    s_str = str(s).strip()
    if s_str.startswith('(') and s_str.endswith(')'):
        parts = [int(x.strip()) for x in s_str[1:-1].split(',') if x.strip()]
        val = 0
        for b in parts:
            val = (val << 8) | (b & 0xFF)
        return val
    return int(s_str)


def format_textmap_s(s) -> str:
    """将 textmap 的 s 值格式化为十六进制显示字符串。

    - 普通整数: 31 → '0x1F'
    - 元组字符串: '(31,0,0)' → '0x1F 0x00 0x00'
    """
    if s is None:
        return '?'
    s_str = str(s).strip()
    if s_str.startswith('(') and s_str.endswith(')'):
        parts = [int(x.strip()) for x in s_str[1:-1].split(',') if x.strip()]
        return ' '.join(f'0x{b & 0xFF:02X}' for b in parts)
    try:
        return f'0x{int(s_str):02X}'
    except (TypeError, ValueError):
        return str(s)
