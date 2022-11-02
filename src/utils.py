import os

# Get adress for memory acess
def get_target_adress(self, adress):
    if self.indirect_mode:
        adress = self.memory[self.current_bank.value][adress].value << 8 | self.memory[self.current_bank.value][adress + 1].value
        adress &= 0x0FFF
    self.indirect_mode = False
    return adress

# Defining string to number conversion
def process_operator(self, number):
    if number[0] == '=': number = int(number[1:], 10)
    elif number[0] == '#': number = int(number[1:], 2)
    elif number[0] == '/': number = int(number[1:], 16)
    else:
        try: number = int(number, 10)
        except Exception: pass
    return number

# Showing machine status
def show_status(self):
    print('Machine status:')
    print('\tACC => {0:03d}, 0b{0:08b}, 0x{0:04X}'.format(self.accumulator.value))
    print('\tPC  => 0x{:04X}'.format(self.program_counter.value))
    print('\tRI  => 0x{:04X}'.format(self.instruction_register.value))
    print('\tLR  => 0x{:04X}'.format(self.link_register.value))

# Showing available files for ASM, LOAD and JOB
def show_files(self):
    # Showing ASM files
    print('Available files for ASM:')
    for filename in os.listdir('./source/'):
        if '.s' in filename.lower(): print('\t' + filename.lower().replace('.s', ''))
    
    # Showing LOAD files
    print('\nAvailable files for LOAD:')
    for filename in os.listdir('./object/'):
        if '.o' in filename.lower(): print('\t' + filename.lower().replace('.o', ''))

    # Showing JOB files
    print('\nAvailable files for JOB:')
    for filename in os.listdir('./jobs/'):
        if '.csv' in filename.lower(): print('\t' + filename.lower().replace('.csv', ''))