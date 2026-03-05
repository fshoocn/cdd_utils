"""解码状态机 — 管理解码游标"""
from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List


@dataclass
class DecodeState:
    """解码状态机
    
    管理解码过程中的源数据和游标位置。
    
    Attributes:
        source: 源字节数据
        cursor_bit: 当前游标的比特位置
        journal: 解码操作日志（调试用）
        length_keys: 动态长度参数
    """
    source: bytes = b''
    cursor_bit: int = 0
    journal: List[Dict[str, Any]] = field(default_factory=list)
    length_keys: Dict[str, int] = field(default_factory=dict)

    @property
    def cursor_byte(self) -> int:
        """当前游标的字节位置"""
        return self.cursor_bit // 8

    @property
    def remaining_bits(self) -> int:
        """剩余可读比特数"""
        return len(self.source) * 8 - self.cursor_bit

    def read_bits(self, bit_length: int, byte_order: str = "21") -> int:
        """读取指定位数的值
        
        Args:
            bit_length: 位长度
            byte_order: 字节序 ("21"=大端, "12"=小端)
            
        Returns:
            读取的数值
        """
        if bit_length <= 0:
            return 0

        value = 0
        for i in range(bit_length):
            byte_idx = (self.cursor_bit + i) // 8
            bit_idx = 7 - ((self.cursor_bit + i) % 8)
            if byte_idx < len(self.source):
                bit = (self.source[byte_idx] >> bit_idx) & 1
                value = (value << 1) | bit
            else:
                value = value << 1

        self.journal.append({
            'action': 'read',
            'value': value,
            'bit_length': bit_length,
            'bit_offset': self.cursor_bit,
        })
        self.cursor_bit += bit_length

        if byte_order == "12" and bit_length > 8:  # 小端需要反转字节
            num_bytes = (bit_length + 7) // 8
            value_bytes = value.to_bytes(num_bytes, byteorder='big')
            value = int.from_bytes(value_bytes, byteorder='little')

        return value

    def read_bytes(self, num_bytes: int) -> bytes:
        """读取完整字节"""
        value = self.read_bits(num_bytes * 8)
        return value.to_bytes(num_bytes, byteorder='big')

    def reset(self) -> None:
        """重置游标"""
        self.cursor_bit = 0
        self.journal.clear()
        self.length_keys.clear()
