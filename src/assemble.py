import pandas as pd

class AssemblyError(Exception): pass

def assemble(self, filename):
    # Opening the file and reading lines
    with open('./source/' + filename + '.asm', 'r') as f:
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

    lines.dropna(subset = 'command', inplace = True)
    lines['operator'].fillna(0, inplace = True)
    
    # Getting bank and memory adress for the code
    if not '@' in lines['command'].to_list(): raise AssemblyError('Program must have an start adress (missing @)')
    if not '#' in lines['command'].to_list(): raise AssemblyError('Program must have a physical end (missing #)')

    adress_line = lines[lines['command'] == '@']['operator'].iloc[-1]
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
            if label not in self.linker_labels['label'].to_list(): raise AssemblyError('Unkown external reference: ' + label)
            labels = pd.concat([labels, self.linker_labels[self.linker_labels['label'] == label]])
            continue

        # Entry point
        elif command == '>':
            continue

        # Program start adress
        elif command == '@':
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
        elif command in self.mnemonic_table['mnemonic'].to_list():
            instruction_counter += 2

        # If not valid instruction, assembly error
        else: raise AssemblyError('Bad instruction: ' + command)

        if label is None: continue

        # Checking if a label has been defined twice
        if label in labels['label'].to_list(): raise AssemblyError('Multiple definition: ' + label)
        
        labels.loc[labels.shape[0]] = [label, label_adress]

    # Second assembly step - assembling instructions
    obj_code = '{:b}'.format(bank).zfill(4) + '{:b}'.format(start_adress).zfill(12) + '\n'
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
            self.linker_labels = pd.concat([self.linker_labels, labels[labels['label'] == label]])
            continue

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
        elif command in self.mnemonic_table['mnemonic'].to_list():
            opcode = self.mnemonic_table.set_index('mnemonic').at[command, 'opcode']
            obj_code +='{:b}'.format(opcode).zfill(4) + '{:b}'.format(operator).zfill(12) + '\n'

        # If not valid instruction, assembly error
        else: raise AssemblyError('Bad instruction: ' + command)

    self.linker_labels.dropna(inplace = True)
    self.linker_labels.drop_duplicates('label', inplace = True, keep = 'last')

    # Saving binary to object file
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()