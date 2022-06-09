import os
from ctypes import c_uint8, c_uint16, c_int8

class AssemblyError(Exception):
    pass

class Assembler:
    
    def __init__(self):
        self.mnemonics_table = {
            "JP": 0x0,
            "JZ": 0x1,
            "JN": 0x2,
            "LV": 0x3,
            "+" : 0x4,
            "-" : 0x5,
            "*" : 0x6,
            "/" : 0x7,
            "LD": 0x8,
            "MM": 0x9,
            "SC": 0xA,
            "RS": 0xB,
            "HM": 0xC,
            "GD": 0xD,
            "PD": 0xE,
            "OS": 0xF,
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

        save_path = '\\object\\' + '.'.join(filename.split('.')[:-1]) + 'obj'