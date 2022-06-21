def dump(self, start_position, size, filename):
    if start_position[0] == '=': start_position = int(start_position[1:], 10)
    elif start_position[0] == '#': start_position = int(start_position[1:], 2)
    elif start_position[0] == '/': start_position = int(start_position[1:], 16)
    else: start_position = int(start_position, 10)

    if size[0] == '=': size = int(size[1:], 10)
    elif size[0] == '#': size = int(size[1:], 2)
    elif size[0] == '/': size = int(size[1:], 16)
    else: size = int(size, 10)

    obj_code = ''
    for i in range(size):
        obj_code += '{0:b}'.format(self.memory[self.current_bank.value][start_position + i].value).zfill(8) + '\n'

    # Opening the file and dumping the memory lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

def hex_dump(self, start_position, size):
    for i in range(size):
        print(
            '{0:X}'.format(start_position + i).zfill(2),
            '->',
            '{0:X}'.format(self.memory[self.current_bank.value][start_position + i].value).zfill(2)
        )