from .baseclass import Base
from .binary import Binary


class JMP(Base):
    @classmethod
    def jump_relative_near(const: int):
        """Relative to RIP, So 32 bit const offset from RIP"""
        opcode = Binary(0xE9, 1, 1)
        const = Binary(const, 4, 4)
        binary = opcode + const
        return binary

    @classmethod
    def jump_near_absolute_indirect_m(address: int):
        """Relative to RIP, So 32 bit offset from RIP"""
        opcode = Binary(0xFF, 1, 1)
        opcode += Binary(0x24, 1, 1)
        opcode += Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = opcode + address
        return binary
