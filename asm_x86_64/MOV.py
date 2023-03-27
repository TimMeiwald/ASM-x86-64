from .baseclass import Base
from .binary import Binary


class MOV(Base):

    # TODO: Transparently add SIB bytes for non direct addressing
    @classmethod
    def load_c32_to_r_displacement_only(cls, register: int, constant: int) -> Binary:
        rex = cls.calculate_rex_prefix(reg1=register)
        # In this specific case modrm also encodes the instruction, so assign to opcode since otherwise construct_instruction complains
        modrm = cls.nmodrm(2, register, 7)
        displacement = Binary(constant, 4, 4)
        binary = cls.construct_instruction(rex_prefix=rex, opcode=modrm, displacement=displacement)
        return binary

    @classmethod
    def load_m32_to_r_displacement_only(cls, register: int, address: int) -> Binary:
        pre_prefix = cls.calculate_prefix(reg1=register)
        prefix = Binary(0x8B, 1, 1)
        value = cls.modrm(0, 4, register)
        reg = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = pre_prefix + prefix + reg + suffix + address
        return binary

    @classmethod
    def load_r_to_m32_displacement_only(cls, register: int, address: int) -> Binary:
        pre_prefix = cls.calculate_prefix(reg1=register)
        prefix = Binary(0x89, 1, 1)
        value = cls.modrm(0, 4, register)
        reg = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = pre_prefix + prefix + reg + suffix + address
        return binary
