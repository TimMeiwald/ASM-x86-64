from .baseclass import Base
from .binary import Binary


class JE(Base):
    @classmethod
    def je32(address: int):
        opcode = Binary(0x0F, 1, 1)
        opcode += Binary(0x84, 1, 1)
        address = Binary(address, 4, 4)
        binary = opcode + address
        return binary
