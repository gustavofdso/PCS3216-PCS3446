import os
import pandas as pd
from ctypes import c_uint8, c_uint16, c_int8

class AssemblyError(Exception): pass

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
        with open('./source/' + filename + '.asm', 'r') as f:
            file_lines = f.readlines()
            f.close()

        # Separating commands from comments
        # TODO: tratar os > para serem o label seguinte
        lines = pd.DataFrame(columns = ['label', 'command', 'operator'])
        for line in file_lines:
            content = line.split(';', maxsplit = 1)[0].strip().split()
            if len(content) == 0: continue
            if len(content) > 3: raise AssemblyError('Too many symbols: ' + content)

            label, command, operator = '', '', ''

            # Separating labels, commands and operators
            if content[0] in self.mnemonic_table['mnemonic'].to_list() or content[0] in ['@', '$', 'K']:
                if len(content) >= 1: command = content[0]
                if len(content) == 2: operator = content[1]
            else:
                if len(content) >= 1: label = content[0]
                if len(content) >= 2: command = content[1]
                if len(content) == 3: operator = content[2]

            if operator != '':
                if operator[0] == '=': operator = int(operator[1:], 10)
                elif operator[0] == '#': operator = int(operator[1:], 2)
                elif operator[0] == '/': operator = int(operator[1:], 16)

            lines.loc[lines.shape[0]] = [label, command, operator]

        labels = pd.DataFrame(columns = ['label', 'adress'])

        if not '@' in lines['command'].to_list(): raise AssemblyError('Program must have an start adress')

        start_adress = lines[lines['command'] == '@']['operator'].iloc[-1]

        # First assembly step - building label table
        instruction_counter = 0
        for i in lines.index:
            label, command, operator = lines.at[i, 'label'], lines.at[i, 'command'], lines.at[i, 'operator']

            if label == '': continue

            # Getting label adress
            adress = start_adress + instruction_counter
            if command == '$': instruction_counter += operator + operator % 2
            else: instruction_counter += 2

            labels.loc[labels.shape[0]] = [label, adress]

        # Second assembly step - assembling instructions
        obj_code = ''
        for i in lines.index:
            label, command, operator = lines.at[i, 'label'], lines.at[i, 'command'], lines.at[i, 'operator']
            if operator in labels['label'].to_list(): operator = labels.set_index('label').at[operator, 'adress']
            
            # Pseudo-instructions
            if command == '@': pass

            # Reserving memory space with zero
            elif command == '$':
                for i in range(operator):
                    concat = ''.zfill(16)
                    obj_code += concat + '\n'

            # Reserving byte with value
            elif command == 'K':
                concat = '{0:b}'.format(operator).zfill(16) + '\n'
                obj_code += concat

            # Regular instruction
            elif command in self.mnemonic_table['mnemonic'].to_list():
                opcode = self.mnemonic_table.set_index('mnemonic').at[command, 'opcode']
                concat = '{0:b}'.format(opcode).zfill(4) + '{0:b}'.format(operator).zfill(12) + '\n'
                obj_code += concat

            # If not valid instruction, assembly error
            else: raise AssemblyError('Bad instruction: ' + command)

        # Saving binary to object file
        with open('./object/' + filename + '.obj', 'w') as f:
            f.write(obj_code)
            f.close()