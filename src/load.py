class LoadError(Exception): pass

# Absolute loader
def load(self, filename):
    # Opening the file and reading lines
    with open('./object/' + filename + '.o', 'r') as f:
        file_lines = f.read()
        f.close()
    obj_code = ''.join(file_lines.replace('\n', ''))
    splitted_code = [obj_code[i: i + 8] for i in range(0, len(obj_code), 8)]
    
    # Getting bank and memory adress
    bank = int(splitted_code[0][:3], 2)
    start_adress = int(splitted_code[0][4:] + splitted_code[1], 2)
    
    # Checking if data size is too large
    if start_adress + len(splitted_code[2:]) > len(self.memory[bank]): raise LoadError("Data too large!")

    # Loading the code
    relative_adress = 0
    for i in splitted_code[2:]:
        self.memory[bank][start_adress + relative_adress].value = int(i, 2)
        relative_adress += 1