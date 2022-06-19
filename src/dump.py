def dump(self, start_position, end_position, filename):
    obj_code = ''
    for i in range(start_position, end_position):
        obj_code += self.memory[self.current_bank][i]

    # Opening the file and dumping the memory lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

def hex_dump(self, start_position, end_position):
    for i in range(start_position, end_position):
        print(i, '-', self.memory[self.current_bank][i])