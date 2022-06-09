from dis import Instruction
import os
from numpy import insert
import pandas as pd
from ctypes import c_uint8, c_uint16, c_int8

class AssemblyError(Exception):
    pass

class Assembler:
    
    def __init__(self):
        self.mnemonic_table = pd.DataFrame(
            (
                ('JP', 0x0),
                ('JZ', 0x1),
                ('JN', 0x2),
                ('LV', 0x3),
                ('+' , 0x4),
                ('-' , 0x5),
                ('*' , 0x6),
                ('/' , 0x7),
                ('LD', 0x8),
                ('MM', 0x9),
                ('SC', 0xA),
                ('RS', 0xB),
                ('HM', 0xC),
                ('GD', 0xD),
                ('PD', 0xE),
                ('OS', 0xF)
            ), columns = ['mnemonic', 'opcode']
        )

    def assemble(self, filename):

        # Opening the file and reading lines
        with open(filename, 'r') as f: file_lines = f.readlines()

        # Separating commands from comments
        lines = pd.DataFrame(columns = ['label', 'command', 'operator', 'comment'])
        for line in file_lines:
            # Separating comments
            if ';' in line:
                content = line.split(';', maxsplit = 1)[0].strip()
                comment = line.split(';', maxsplit = 1)[1].strip()
            else:
                content = line.strip()
                comment = ''

            # Separating labels, commands and operators
            if len(content.split()) == 2:
                label = ''
                command = content.split()[0]
                operator = content.split()[1]
            elif len(content.split()) == 3:
                label = content.split()[0]
                command = content.split()[1]
                operator = content.split()[2]
            else: raise AssemblyError('Too many mnemonics: ' + content)
            
            lines.loc[lines.shape[0]] = [label, command, operator, comment]

        labels = pd.DataFrame(columns = ['label', 'address'])

        # First assembly step
        instruction_counter = 0
        for i in lines.index:

            instruction_counter += 1

        # Second assembly step

        save_path = r'\\object\\' + '.'.join(filename.split('.')[:-1]) + '.obj'

    def binary_from_instruction(self, command, operator = None):
        splited_command = command.split()