"""编码状态机 — 管理编码游标和字节缓冲区

对标 odxtools EncodeState，但简化了重叠检测（used_mask）。
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class EncodeState:
    """编码状态机
    
    管理编码过程中的字节缓冲区和游标位置。
    
    Attributes:
        buffer: 字节缓冲区 (bytearray)
        cursor_bit: 当前游标的比特位置
        journal: 编码操作日志（调试用）
        length_keys: 动态长度参数
    """
    buffer: bytearray = field(default_factory=bytearray)
    cursor_bit: int = 0
    journal: List[Dict[str, Any]] = field(default_factory=list)
    length_keys: Dict[str, int] = field(default_factory=dict)

    @property
    def cursor_byte(self) -> int:
        """当前游标的字节位置"""
        return self.cursor_bit // 8

    def write_bits(self, value: int, bit_length: int, byte_order: str = "21") -> None:
        """写入指定位数的值
        
        Args:
            value: 要写入的数值
            bit_length: 位长度
            byte_order: 字节序 ("21"=大端, "12"=小端)
        """
        if bit_length <= 0:
            return

        # 确保缓冲区足够大
        needed_bytes = (self.cursor_bit + bit_length + 7) // 8
        if len(self.buffer) < needed_bytes:
            self.buffer.extend(b'\x00' * (needed_bytes - len(self.buffer)))

        # 小端序：先将 value 按小端字节序排列，再统一按位写入
        if byte_order == "12" and bit_length > 8:  # 小端
            num_bytes = (bit_length + 7) // 8
            le_bytes = value.to_bytes(num_bytes, byteorder='little')
            value = int.from_bytes(le_bytes, byteorder='big')

        # 按位写入（MSB first）
        for i in range(bit_length):
            bit = (value >> (bit_length - 1 - i)) & 1
            byte_idx = (self.cursor_bit + i) // 8
            bit_idx = 7 - ((self.cursor_bit + i) % 8)
            if bit:
                self.buffer[byte_idx] |= (1 << bit_idx)
            else:
                self.buffer[byte_idx] &= ~(1 << bit_idx)

        self.journal.append({
            'action': 'write',
            'value': value,
            'bit_length': bit_length,
            'bit_offset': self.cursor_bit,
        })
        self.cursor_bit += bit_length

    def write_bytes(self, data: bytes) -> None:
        """写入完整字节"""
        self.write_bits(int.from_bytes(data, 'big'), len(data) * 8)

    def get_bytes(self) -> bytes:
        """获取编码结果"""
        return bytes(self.buffer)

    def reset(self) -> None:
        """重置状态"""
        self.buffer = bytearray()
        self.cursor_bit = 0
        self.journal.clear()
        self.length_keys.clear()
