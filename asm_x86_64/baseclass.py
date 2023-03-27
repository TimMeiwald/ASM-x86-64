from abc import ABC
from .binary import Binary


class Base(ABC):
    @staticmethod
    def nmodrm(mod: int, r: int, m: int) -> Binary:
        """Intel Volume 2A 2-6

        r changes row
        m changes column
        Not sure which way it's meant to be as long as you're consistent works."""
        if r > 7:
            r -= 8
        if m > 7:
            m -= 8
        mod = mod * 2 ** 6
        m = m * 2 ** 3
        return Binary(mod + r + m, 1, 1)
    
    @staticmethod
    def modrm(mod: int, r: int, m: int) -> Binary:
        # Deprecated use nmodrm
        """Intel Volume 2A 2-6

        r changes row
        m changes column
        Not sure which way it's meant to be as long as you're consistent works."""
        if r > 7:
            r -= 8
        if m > 7:
            m -= 8
        mod = mod * 2 ** 6
        m = m * 2 ** 3
        return mod + r + m

    @staticmethod
    def calculate_prefix(*, reg1: int = 0, reg2: int = 0) -> int:
        # Deprecated for calculate_rex
        """Calculates the prefix byte required when 32 bit uses a register
        greater than Register 7. Aka the registers added in x86-64 instead of just the ones
        used in x86."""
        upper_64_prefix = Binary(0, 0, 0)
        if reg1 >= 8:
            upper_64_prefix = Binary(0x41, 1, 1)
        if reg2 >= 8:
            upper_64_prefix = Binary(0x44, 1, 1)
        if reg1 >= 8 and reg2 >= 8:
            upper_64_prefix = Binary(0x45, 1, 1)
        return upper_64_prefix
    
    @staticmethod
    def calculate_rex_prefix(*, reg1: int = 0, reg2: int = 0) -> Binary:
        """Calculates the prefix byte required when 32 bit uses a register
        greater than Register 7. Aka the registers added in x86-64 instead of just the ones
        used in x86."""
        upper_64_prefix = Binary(0, 0, 0)
        if reg1 >= 8:
            upper_64_prefix = Binary(0x41, 1, 1)
        if reg2 >= 8:
            upper_64_prefix = Binary(0x44, 1, 1)
        if reg1 >= 8 and reg2 >= 8:
            upper_64_prefix = Binary(0x45, 1, 1)
        if(len(upper_64_prefix) == 0):
            return None
        return upper_64_prefix

    @staticmethod
    def construct_instruction(
        *,
        instr_prefix: list[Binary] = None,
        rex_prefix: Binary = None,
        opcode: Binary = None,
        modrm: Binary = None,
        sib: Binary = None,
        displacement: Binary = None,
        immediate: Binary = None,
    ) -> Binary:

        # Size Checks as per Chapter 2 Volume 2 Intel Manual
        if(opcode != None):
            opcode_length = len(opcode)
            if opcode_length > 3 or opcode_length < 1:
                raise TypeError(
                    f"Opcode must be 1, 2 or 3 bytes long. Currently {opcode_length}"
                )
        if(rex_prefix != None):
            rex_prefix_length = len(rex_prefix)
            if rex_prefix_length != 1:
                raise TypeError(
                    f"rex byte must be 1 byte long. Currently {rex_prefix_length}"
                )
        if(modrm != None):
            modrm_length = len(modrm)
            if modrm_length != 1:
                raise TypeError(f"modrm byte must be 1 byte long. Currently {modrm_length}")
        if(sib != None):
            sib_length = len(sib)
            if sib != 1:
                raise TypeError(f"sib byte must be 1 byte long. Currently {sib_length}")
        if(displacement != None):
            displacement_length = len(displacement)
            if displacement_length not in [1, 2, 4]:
                raise TypeError(
                    f"displacement must be 1, 2 or 4 bytes long. Currently {displacement_length}"
                )
        if(immediate != None):
            immediate_length = len(immediate)
            if immediate_length not in [1, 2, 4]:
                raise TypeError(
                    f"displacement must be 1, 2 or 4 bytes long. Currently {immediate_length}"
                )

        # Add everything that is not None

        instruction = Binary(0, 0, 0)
        if instr_prefix != None:
            prefixes = Binary(0, 0, 0)
            for prefix in instr_prefix:
                if(prefix != None):
                    prefix_length = len(prefix)
                    if prefix_length != 1:
                        raise TypeError(
                            f"prefixes must be 1 byte. Currently {prefix_length}"
                        )
                    prefixes += prefix
            instruction += prefixes

        # rex must directly precede opcode, and is used for lots of 64 bit extensions hence seperated
        if rex_prefix != None:
            instruction += rex_prefix

        # opcode is required
        if opcode == None:
            raise TypeError("An instruction must have an opcode!")
        instruction += opcode

        if modrm != None:
            instruction += modrm
        if sib != None:
            instruction += modrm
        if displacement != None:
            instruction += displacement
        if immediate != None:
            instruction += immediate
        return instruction
