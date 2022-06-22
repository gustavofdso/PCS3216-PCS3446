import pandas as pd

class AssemblyError(Exception): pass

def assemble(self, filename):
    mnemonic_table = pd.DataFrame(
        (
            ('JP', 0x0), ('JZ', 0x1), ('JN', 0x2), ('LV', 0x3),
            ('+' , 0x4), ('-' , 0x5), ('*' , 0x6), ('/' , 0x7),
            ('LD', 0x8), ('MM', 0x9), ('SC', 0xA), ('RS', 0xB),
            ('HM', 0xC), ('GD', 0xD), ('PD', 0xE), ('OS', 0xF)
        ), columns = ['mnemonic', 'opcode']
    )

    # Opening the file and reading lines
    with open('./source/' + filename + '.asm', 'r') as f:
        file_lines = f.readlines()
        f.close()

    # Separating commands from comments
    lines = pd.DataFrame(columns = ['label', 'command', 'operator'])
    for line in file_lines:
        content = line.split(';', maxsplit = 1)[0].strip().split()
        if len(content) == 0: continue
        if len(content) > 3: raise AssemblyError('Too many symbols: ' + content)

        label, command, operator = '', '', ''

        # Separating labels, commands and operators
        try:
            if content[0] in mnemonic_table['mnemonic'].to_list() or content[0] in ['@', '$', 'K', '#']:
                command = content[0]
                operator = content[1]
            else:
                label = content[0]
                command = content[1]
                operator = content[2]
        except Exception: pass

        if operator != '': operator = self.string_to_number(operator)

        lines.loc[lines.shape[0]] = [label, command, operator]

    if not '@' in lines['command'].to_list(): raise AssemblyError('Program must have an start adress')
    if not '#' in lines['command'].to_list(): raise AssemblyError('Program must have an end adress')
    start_adress = lines[lines['command'] == '@']['operator'].iloc[-1]

    # First assembly step - building label table
    labels = pd.DataFrame(columns = ['label', 'adress'])
    instruction_counter = start_adress
    for i in lines.index:
        label, command, operator = lines.at[i, 'label'], lines.at[i, 'command'], lines.at[i, 'operator']

        # Getting label adress
        adress = start_adress + instruction_counter

        # Pseudo-instructions

        # Program start adress
        if command == '@':
            pass
        
        # Reserving memory space with zeros
        elif command == '$':
            instruction_counter += operator

        # Reserving byte with value
        elif command == 'K':
            instruction_counter += 1

        # Finish assembly
        elif command == '#':
            break
        
        # Regular instruction
        elif command in mnemonic_table['mnemonic'].to_list():
            instruction_counter += 2

        # If not valid instruction, assembly error
        else: raise AssemblyError('Bad instruction: ' + command)

        if label == '': continue

        labels.loc[labels.shape[0]] = [label, adress]
    
    # Second assembly step - assembling instructions
    obj_code = '{:b}'.format(start_adress).zfill(16) + '\n'
    for i in lines.index:
        label, command, operator = lines.at[i, 'label'], lines.at[i, 'command'], lines.at[i, 'operator']
        if operator in labels['label'].to_list(): operator = labels.set_index('label').at[operator, 'adress']
        
        # Pseudo-instructions

        # Program start adress
        if command == '@':
            pass

        # Reserving memory space with zeros
        elif command == '$':
            for i in range(operator):
                obj_code += ''.zfill(8) + '\n'

        # Reserving byte with value
        elif command == 'K':
            obj_code +='{:b}'.format(operator).zfill(8) + '\n'

        # Finish assembly
        elif command == '#':
            obj_code += '1111111100000000'
            break

        # Regular instruction
        elif command in mnemonic_table['mnemonic'].to_list():
            opcode = mnemonic_table.set_index('mnemonic').at[command, 'opcode']
            obj_code +='{:b}'.format(opcode).zfill(4) + '{:b}'.format(operator).zfill(12) + '\n'

        # If not valid instruction, assembly error
        else: raise AssemblyError('Bad instruction: ' + command)

    # Saving binary to object file
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()