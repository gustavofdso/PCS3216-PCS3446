from dis import Instruction
import os
from numpy import insert
import pandas as pd
from ctypes import c_uint8, c_uint16, c_int8

class AssemblyError(Exception):
    pass

class Assembler:
    
    def __init__(self):
        pass

    def assemble(self, filename):

        # Opening the file and reading lines
        with open(filename, 'r') as f: file_lines = f.readlines()

        # Separating commands from comments
        lines = pd.DataFrame(columns = ['command', 'comment'])
        for line in file_lines:
            if ';' in line:
                command = line.split(';', maxsplit = 1)[0].strip()
                comment = line.split(';', maxsplit = 1)[1].strip()
            else:
                command = line.strip()
                comment = ''

            lines.loc[lines.shape[0]] = [command, comment]

        labels = pd.DataFrame(columns = ['label', 'address'])

        # First assembly step
        instruction_counter = 0
        for i in lines.index:
            command = lines.at[i, 'command']
            splited_command = command.split()

            instruction_counter += 1

        # Second assembly step

        save_path = r'\\object\\' + '.'.join(filename.split('.')[:-1]) + '.obj'

    def binary_from_instruction(self, command, operator = None):
        splited_command = command.split()

        # No code
        if len(splited_command) == 0: return ''

        if splited_command[0] == 'JP':

        elif splited_command[0] == 'JZ':

        elif splited_command[0] == 'JN':

        elif splited_command[0] == 'LV':

        elif splited_command[0] == '+':

        elif splited_command[0] == '-':

        elif splited_command[0] == '*':

        elif splited_command[0] == '/':

        elif splited_command[0] == 'LD':

        elif splited_command[0] == 'MM':

        elif splited_command[0] == 'SC':

        elif splited_command[0] == 'RS':

        elif splited_command[0] == 'HM':

        elif splited_command[0] == 'GD':

        elif splited_command[0] == 'PD':

        elif splited_command[0] == 'OS':

        else: raise AssemblyError('Unknown command: ' + command)