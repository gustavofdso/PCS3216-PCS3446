import pandas as pd

class AssemblyError(Exception): pass

# Absolute assembler
def assemble(self, filename):
    # Opening the file and reading lines
    with open('./source/' + filename + '.s', 'r') as f:
        file_lines = f.readlines()
        f.close()

    # Separating commands from comments
    lines = pd.DataFrame(columns = ['label', 'command', 'operator'])
    for line in file_lines:
        content = line.split(';', maxsplit = 1)[0].strip().split()
        if len(content) == 0: continue
        if len(content) > 3: raise AssemblyError('Too many symbols in line: ' + content)

        label, command, operator = None, None, None

        # Separating labels, commands and operators
        try:
            if content[0] in self.mnemonic_table['mnemonic'].to_list() or content[0] in ['<', '>', '@', '$', 'K', '#']:
                command = content[0]
                operator = content[1]
            else:
                label = content[0]
                command = content[1]
                operator = content[2]
        except Exception: pass

        if operator is not None: operator = self.process_operator(operator)

        lines.loc[lines.shape[0]] = [label, command, operator]

    # Ignoring lines with no command and filling operators with zero
    lines.dropna(subset = 'command', inplace = True)
    lines['operator'].fillna(0, inplace = True)

    # Getting bank and memory adress
    adress_lines = lines[lines['command'] == '@']['operator'].to_list()
    if len(adress_lines) == 0: raise AssemblyError('Program must have an start adress (missing @).')
    elif len(adress_lines) >= 2: raise AssemblyError('Program must have only one start adress (multiple @).')
    adress_line = adress_lines[0]
    bank = (adress_line & 0xF000) >> 12
    start_adress = adress_line & 0x0FFF

    # First assembly step - building label table
    labels = pd.DataFrame(columns = ['label', 'adress'])
    instruction_counter = 0
    for i in lines.index:
        label, command, operator = lines.at[i, 'label'], lines.at[i, 'command'], lines.at[i, 'operator']

        # Getting label adress
        label_adress = start_adress + instruction_counter
        
        # Pseudo-instructions

        # External label reference
        if command == '<':
            if label not in self.linker['label'].to_list(): raise AssemblyError('Unkown external reference: ' + label)
            labels = pd.concat([labels, self.linker[self.linker['label'] == label]])
            continue

        # Entry point
        elif command == '>':
            continue

        # Program start adress
        elif command == '@':
            continue
        
        # Reserving memory space with zeros
        elif command == '$':
            instruction_counter += operator

        # Reserving byte with value
        elif command == 'K':
            instruction_counter += 1

        # Finish assembly
        elif command == '#':
            pass
        
        # Regular instruction
        elif command in self.mnemonic_table['mnemonic'].to_list():
            instruction_counter += 2

        # If not valid instruction, assembly error
        else: raise AssemblyError('Bad instruction: ' + command)

        if label is None:
            continue

        # Checking if a label has been defined twice
        if label in labels['label'].to_list(): raise AssemblyError('Multiple definition of ' + label)
        
        labels.loc[labels.shape[0]] = [label, label_adress]

    # Second assembly step - assembling instructions

    # Dumping bank and memory adress
    obj_code = '{:04b}'.format(bank) + '{:012b}'.format(start_adress) + '\n'

    # Filling the assembled lines
    for i in lines.index:
        label, command, operator = lines.at[i, 'label'], lines.at[i, 'command'], lines.at[i, 'operator']
        if operator in labels['label'].to_list(): operator = labels.set_index('label').at[operator, 'adress']
        
        # Pseudo-instructions

        # External label reference
        if command == '<':
            continue

        # Entry point
        if command == '>':
            if label not in labels['label'].to_list(): raise AssemblyError('Unkown entry point: ' + label)
            self.linker = pd.concat([self.linker, labels[labels['label'] == label]])
            continue

        # Program start adress
        if command == '@':
            continue

        # Reserving memory space with zeros
        elif command == '$':
            for i in range(operator):
                obj_code += '00000000' + '\n'

        # Reserving byte with value
        elif command == 'K':
            operator &= 0xFF
            obj_code +='{:08b}'.format(operator) + '\n'

        # Finish assembly
        elif command == '#':
            obj_code += '1111000000001111'

        # Regular instruction
        elif command in self.mnemonic_table['mnemonic'].to_list():
            opcode = self.mnemonic_table.set_index('mnemonic').at[command, 'opcode']
            operator &= 0x0FFF
            obj_code +='{:04b}'.format(opcode) + '{:012b}'.format(operator) + '\n'

        # If not valid instruction, assembly error
        else: raise AssemblyError('Bad instruction: ' + command)

    # Updating external adresses table
    self.linker.dropna(inplace = True)
    self.linker.drop_duplicates('label', inplace = True, keep = 'last')

    # Saving binary to object file
    with open('./object/' + filename + '.o', 'w') as f:
        f.write(obj_code)
        f.close()