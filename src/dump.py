def dump(self, filename, size, start_adress, bank):
    start_adress = self.string_to_number(start_adress)
    bank = self.string_to_number(bank)
    size = self.string_to_number(size)

    obj_code = '{:b}'.format(bank).zfill(4) + '{:b}'.format(start_adress).zfill(12) + '\n'
    for i in range(size):
        if start_adress + i >= len(self.memory[bank]): break
        obj_code += '{:b}'.format(self.memory[bank][start_adress + i].value).zfill(8) + '\n'

    # Opening the file and dumping the memory lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

def hex_dump(self, size, start_adress, bank):
    start_adress = self.string_to_number(start_adress)
    bank = self.string_to_number(bank)
    size = self.string_to_number(size)

    print('Memory bank: {:d}'.format(bank))
    for i in range(size):
        if start_adress + i >= len(self.memory[bank]): break
        print(
            '{:X}'.format(start_adress + i).zfill(2),
            '=>',
            '{:X}'.format(self.memory[bank][start_adress + i].value).zfill(2)
        )