# Fetching next instruction
def fetch_instruction(self):
    # Fetching instruction and updating program counter
    self.instruction_register.value = self.memory[self.current_bank.value][self.program_counter.value].value << 8 | self.memory[self.current_bank.value][self.program_counter.value + 1].value
    self.program_counter.value += 2

# Executing current instruction
def execute_instruction(self):
    # Getting opcode and executing instruction
    opcode = (self.instruction_register.value & 0xF000) >> 12
    self.mnemonic_table.set_index('opcode').at[opcode, 'instruction']()

# Running code on memory
def run_code(self, start_adress, bank, step = False):
    self.program_counter.value = self.process_operator(start_adress)
    self.current_bank.value = self.process_operator(bank)

    # Running sequential instructions
    self.running = True
    while self.running:
        self.fetch_instruction()
        self.execute_instruction()
        # If the code is to be run on step, wait for user entry and show status
        if step:
            input()
            print('Step!')
            self.show_status()