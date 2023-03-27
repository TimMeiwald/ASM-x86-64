from .baseclass import Base
from .binary import Binary


class ADD(Base):
    @classmethod
    def r1_with_r2(cls, reg1: int, reg2: int) -> tuple[Binary, str]:
        opcode = Binary(1, 1, 1)
        upper_64_prefix = cls.calculate_prefix(reg1=reg1, reg2=reg2)
        register_pair = cls.modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary
