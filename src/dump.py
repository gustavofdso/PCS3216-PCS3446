def dump(self, filename, size, start_adress, bank):
    start_adress = self.process_operator(start_adress)
    bank = self.process_operator(bank)
    size = self.process_operator(size)

    obj_code = '{:b}'.format(bank).zfill(4) + '{:b}'.format(start_adress).zfill(12) + '\n'
    for relative_adress in range(size):
        if start_adress + relative_adress >= len(self.memory[bank]): break
        obj_code += '{:b}'.format(self.memory[bank][start_adress + relative_adress].value).zfill(8) + '\n'

    # Opening the file and dumping the memory lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

def hex_dump(self, size, start_adress, bank):
    start_adress = self.process_operator(start_adress)
    bank = self.process_operator(bank)
    size = self.process_operator(size)

    print('Memory bank: {:d}'.format(bank))
    for relative_adress in range(size):
        if start_adress + relative_adress >= len(self.memory[bank]): break
        print(
            '{:X}'.format(start_adress + relative_adress).zfill(2),
            '=>',
            '{:X}'.format(self.memory[bank][start_adress + relative_adress].value).zfill(2)
        )