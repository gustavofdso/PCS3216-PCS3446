import os
import pandas as pd
from ctypes import c_uint8, c_uint16, c_int8

class AssemblyError(Exception):
    pass

class Assembler:
    
    def __init__(self):


        self.pseudoinstrucions_list = ['@', '#', '$', 'K', '&', '>', '<']

    def assemble(self, filename):

        # Opening the file and reading lines
        with open(filename, 'r') as f:
            file_lines = f.readlines()

        # Separating commands from comments
        lines = pd.DataFrame(columns = ['instruction', 'comment'])
        for line in file_lines:
            if ';' in line:
                instruction = line.split(';', maxsplit = 1)[0].strip()
                comment = line.split(';', maxsplit = 1)[1].strip()
            else:
                instruction = line.strip()
                comment = ''

            lines.loc[lines.shape[0]] = [instruction, comment]

        # Executing assembly steps
        for step in [1, 2]:
            instruction_counter = 0

            for i in lines.index:
                binary = self.binary_from_instruction(instruction)
                instruction_counter += 1

        save_path = '\\object\\' + '.'.join(filename.split('.')[:-1]) + 'obj'

    def binary_from_instruction(self, instruction):
        splited_instruction = instruction.split()
        if len(splited_instruction) == 0: return ''

        if splited_instruction[0] == 'JP':

        elif splited_instruction[0] == 'JZ':

        elif splited_instruction[0] == 'JN':

        elif splited_instruction[0] == 'LV':

        elif splited_instruction[0] == '+':

        elif splited_instruction[0] == '-':

        elif splited_instruction[0] == '*':

        elif splited_instruction[0] == '/':

        elif splited_instruction[0] == 'LD':

        elif splited_instruction[0] == 'MM':

        elif splited_instruction[0] == 'SC':

        elif splited_instruction[0] == 'RS':
            
        elif splited_instruction[0] == 'HM':

        elif splited_instruction[0] == 'GD':

        elif splited_instruction[0] == 'PD':

        elif splited_instruction[0] == 'OS':
