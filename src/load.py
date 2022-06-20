from ctypes import c_uint8

def load(self, filename):
    # Opening the file and reading lines
    with open('./object/' + filename + '.obj', 'r') as f:
        file_lines = f.read()
        f.close()

    obj_code = ''.join(file_lines.replace('\n', ''))
    splitted_code = [obj_code[i: i + 8] for i in range(0, len(obj_code), 8)]
    
    adress = int(splitted_code[0], 2)
    relative_adress = 0
    for i in splitted_code[1:]:
        # Saving byte to memory
        self.memory[self.current_bank.value][adress + relative_adress] = c_uint8(int(i, 2))
        relative_adress += 1