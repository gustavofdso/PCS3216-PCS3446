from ctypes import c_uint8

def load(self, filename):
    # Opening the file and reading lines
    with open('./object/' + filename + '.obj', 'r') as f:
        file_lines = f.readlines()
        f.close()

    obj_code = ''.join(file_lines)
    adress = int(obj_code[0:7], 2)
    i = 0
    while True:
        if 8*i + 7 >= len(obj_code): break
        line = obj_code[8*i: 8*i + 7]
        self.memory[self.current_bank][adress + i] = c_uint8(line)
        i += 1