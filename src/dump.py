def DumpError(Exception): pass

def dump(self, filename, size, start_adress, bank):
    start_adress = self.process_operator(start_adress)
    bank = self.process_operator(bank)
    size = self.process_operator(size)

    obj_code = '{:04b}'.format(bank) + '{:012b}'.format(start_adress) + '\n'
    for relative_adress in range(size):
        if start_adress + relative_adress >= len(self.memory[bank]): raise(DumpError("Memory overflow on dump!"))
        obj_code += '{:08b}'.format(self.memory[bank][start_adress + relative_adress].value) + '\n'

    # Opening the file and dumping the memory lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

def hex_dump(self, size, start_adress, bank):
    start_adress = self.process_operator(start_adress)
    bank = self.process_operator(bank)
    size = self.process_operator(size)
    
    print('Memory bank: {:02d}'.format(bank))
    for relative_adress in range(size):
        if start_adress + relative_adress >= len(self.memory[bank]): raise(DumpError("Memory overflow on dump!"))
        print(
            '{:03X}'.format(start_adress + relative_adress),
            '=>',
            '{:02X}'.format(self.memory[bank][start_adress + relative_adress].value)
        )
