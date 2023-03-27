from asm_x86_64.MOV import MOV


def test_mov():
    x = MOV.load_c32_to_r_displacement_only(0, 100)
    assert x.__repr__() == "b8 64 00 00 00"

def test_mov2():
    x = MOV.load_m32_to_r_displacement_only(0, 0x100)
    assert x.__repr__() == "8b 04 25 00 01 00 00"