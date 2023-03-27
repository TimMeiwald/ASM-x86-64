from .baseclass import Base
from .binary import Binary


class IDIV(Base):
    @classmethod
    def idiv_register_one_with_register_two(cls, reg: int) -> tuple[Binary, str]:
        """Unsigned Quotient in EAX, Remainder in EDX"""
        opcode = Binary(0xF7, 1, 1)
        upper_64_prefix = cls.calculate_prefix(reg1=reg)
        register_pair = cls.modrm(3, reg, 7)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary
