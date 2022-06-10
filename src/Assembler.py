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

        self.pseudoinstructions = ['@', '#', '$', 'K', '&', '>', '<']

    def assemble(self, filename):
        # Opening the file and reading lines
        with open(filename, 'r') as f: file_lines = f.readlines()

        # Separating commands from comments
        # TODO: tratar os > para serem o label seguinte
        lines = pd.DataFrame(columns = ['label', 'command', 'operator'])
        for line in file_lines:
            content = line.split(';', maxsplit = 1)[0].strip().split()
            if len(content) == 0: continue
            if len(content) > 3: raise AssemblyError('Too many symbols: ' + content)

            label, command, operator = '', '', ''

            # Separating labels, commands and operators
            if content[0] in self.mnemonic_table['mnemonic'].to_list() or content[0] in self.pseudoinstructions:
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

        labels = pd.DataFrame(columns = ['label', 'isRelocable', 'isExternal', 'address'])

        if not ('@' in lines['command'].to_list()) ^ ('&' in lines['command'].to_list()): raise AssemblyError('Program must be either absolute or relocable')

        if '@' in lines['command'].to_list(): start_adress = lines[lines['command'] == '@']['operator'].iloc[-1]
        elif '&' in lines['command'].to_list(): start_adress = lines[lines['command'] == '&']['operator'].iloc[-1]

        # First assembly step - building label table
        relative_adress = 0
        for i in lines.index:
            label = lines.at[i, 'label']
            command = lines.at[i, 'command']
            operator = lines.at[i, 'operator']

            if label == '': continue

            if command == '<':
                isRelocable = False
                isExternal = True
                adress = '?'
            else:
                if '@' in lines['command'].to_list(): isRelocable = False
                elif '&' in lines['command'].to_list(): isRelocable = True
                isExternal = False
                adress = start_adress + relative_adress
                relative_adress += 2

            labels.loc[labels.shape[0]] = [label, isRelocable, isExternal, adress]
        
        print(lines, labels)

        # Second assembly step - building instructions
        instruction_counter = 0
        for i in lines.index:
            label = lines.at[i, 'label']
            command = lines.at[i, 'command']
            operator = lines.at[i, 'operator']

            instruction_counter += 1

        save_path = r'./object/' + '.'.join(filename.split('.')[:-1]) + 'obj'