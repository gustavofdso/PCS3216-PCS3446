def dump(self, start_position, size, filename):
    start_position = self.string_to_number(start_position)
    size = self.string_to_number(size)

    obj_code = '{:b}'.format(start_position).zfill(16)
    for i in range(size):
        obj_code += '{:b}'.format(self.memory[self.current_bank.value][start_position + i].value).zfill(8) + '\n'

    # Opening the file and dumping the memory lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

def hex_dump(self, start_position, size):
    start_position = self.string_to_number(start_position)
    size = self.string_to_number(size)

    for i in range(size):
        print(
            '{:X}'.format(start_position + i).zfill(2),
            '=>',
            '{:X}'.format(self.memory[self.current_bank.value][start_position + i].value).zfill(2)
        )