from ctypes import c_int8

# Inconditional jump to addresss
def _jump(self):
    operand = self.instruction_register.value & 0x0FFF
    self.program_counter.value = operand

# Jump to addresss if accumulator is zero
def _jump_if_zero(self):
    if self.accumulator.value == 0: self._jump()

# Jump to addresss if accumulator is negative
def _jump_if_negative(self):
    if self.accumulator.value < 0: self._jump()
    
# Load value to accumulator
def _load_value(self):
    operand = self.instruction_register.value & 0x00FF
    self.accumulator.value = operand
    
# Add value from memory to accumulator
def _add(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.accumulator.value += self.memory[self.current_bank.value][adress].value

# Subtract value from memory from accumulator
def _subtract(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.accumulator.value -= self.memory[self.current_bank.value][adress].value

# Multiply value from memory by accumulator
def _multiply(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.accumulator.value *= self.memory[self.current_bank.value][adress].value
    
# Divide accumulator by value from memory
def _divide(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.accumulator.value //= self.memory[self.current_bank.value][adress].value

# Load accumulator with value from memory
def _load(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.accumulator = self.memory[self.current_bank.value][adress]

# Move accumulator to memory
def _move_to_memory(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.memory[self.current_bank.value][adress] = self.accumulator

# Enter a subroutine
def _subroutine_call(self):
    operand = self.instruction_register.value & 0x0FFF
    next_instr = self.program_counter.value

    self.memory[self.current_bank.value][operand].value = next_instr >> 8
    self.memory[self.current_bank.value][operand + 1].value = next_instr & 0x00FF

    self.program_counter.value = operand + 2

# Return from a subroutine
def _return_from_subroutine(self):
    # TODO: fazer essa func
    pass
    
# Halt the machine or turn on/off the memory indirect mode
def _halt_machine(self):
    operand = (self.instruction_register.value & 0x0F00) >> 8

    if operand == 0b0000:
        print('Machine halted! Press ^C to interrupt execution!')
        while True:
            try: pass
            except KeyboardInterrupt: self.running = False

    elif operand == 0b0001: self.indirect_mode = True
    elif operand == 0b0010: self.indirect_mode = False

# Get a value into the accumulator
def _get_data(self):
    self.accumulator = c_int8(input('Enter ACC => '))

# Put a value from the accumulator
def _put_data(self):
    print('ACC => {:04d}'.format(self.accumulator.value))
    
# Make an OS call
def _operating_system(self):
    operand = (self.instruction_register.value & 0x0F00) >> 8

    # Print current state
    if operand == 0b0000:
        print(
            'Internal registers:\n'
            '\tACC => {:d}\n'.format(self.accumulator.value),
            '\tPC  => {:#05X}\n'.format(self.program_counter.value),
            '\tRI  => {:#05X}\n'.format(self.instruction_register.value)
        )

    # Finish execution
    elif operand == 0b1111:
        self.running = False