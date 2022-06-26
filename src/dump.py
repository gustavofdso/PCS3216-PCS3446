class DumpError(Exception): pass

# Absolute dumper
def dump(self, filename, size, start_adress, bank):
    start_adress = self.process_operator(start_adress)
    bank = self.process_operator(bank)
    size = self.process_operator(size)

    if start_adress + size > len(self.memory[bank]): raise DumpError("Data too large!")

    # Dumping bank and memory adress
    obj_code = '{:04b}'.format(bank) + '{:012b}'.format(start_adress) + '\n'

    # Dumping the code
    for relative_adress in range(size):
        obj_code += '{:08b}'.format(self.memory[bank][start_adress + relative_adress].value) + '\n'

    # Opening the file writing lines
    with open('./object/' + filename + '.obj', 'w') as f:
        f.write(obj_code)
        f.close()

# Hexadecimal dumper
def hex_dump(self, size, start_adress, bank):
    start_adress = self.process_operator(start_adress)
    bank = self.process_operator(bank)
    size = self.process_operator(size)
    
    if start_adress + size > len(self.memory[bank]): raise DumpError("Data too large!")

    # Showing bank
    print('Memory bank: {:02d}'.format(bank))
    
    # Dumping the code
    for relative_adress in range(size):
        print(
            '{:03X}'.format(start_adress + relative_adress),
            '=>',
            '{:02X}'.format(self.memory[bank][start_adress + relative_adress].value)
        )
