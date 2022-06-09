
from ctypes import c_uint8, c_uint16, c_int8

class AssemblyError(Exception):
    pass

class Assembler:
    
    def __init__(self):
        self.mnemonics_table = {
            "JP": (0x0, 2),
            "JZ": (0x1, 2),
            "JN": (0x2, 2),
            "LV": (0x3, 1),
            "+" : (0x4, 2), 
            "-" : (0x5, 2), 
            "*" : (0x6, 2), 
            "/" : (0x7, 2),
            "LD": (0x8, 2),
            "MM": (0x9, 2),
            "SC": (0xA, 2),
            "RS": (0xB, 1),
            "HM": (0xC, 1),
            "GD": (0xD, 1),
            "PD": (0xE, 1),
            "OS": (0xF, 1),
        }

        self.pseudoinstrucions = ['@', '#', '$', 'K', '&', '>', '<']

    def assemble(self, filename):
        with open(filename, 'r') as f:
            file_lines = f.readlines()

        label_table = {}
        object_code = []
        instruction_counter = 0
        initial_address = 0
        current_object_file = 0

        lines = []
        for i, line in enumerate(file_lines):
            instruction = line.split(';', maxsplit = 1)[0].strip()
            comment = ''.join(line.split(';', maxsplit = 1)[1:]).strip()
            if instruction == '': continue
            
            lines.append((i, instruction, comment))