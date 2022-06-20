from ctypes import c_int8

# Inconditional jump to addresss
def _jump(self):
    operand = self.instruction_register.value & 0xFFF
    self.program_counter.value = operand

# Jump to addresss if accumulator is zero
def _jump_if_zero(self):
    if self.accumulator == 0: self._jump()

# Jump to addresss if accumulator is negative
def _jump_if_negative(self):
    if self.accumulator < 0: self._jump()
    
# Load value to accumulator
def _load_value(self):
    operand = self.instruction_register.value & 0xFF
    self.accumulator = operand
    
# Add value from memory to accumulator
def _add(self):
    operand = self.instruction_register.value & 0xFFF
    self.accumulator += self.get_from_memory(operand)

# Subtract value from memory from accumulator
def _subtract(self):
    operand = self.instruction_register.value & 0xFFF
    self.accumulator -= self.get_from_memory(operand)

# Multiply value from memory by accumulator
def _multiply(self):
    operand = self.instruction_register.value & 0xFFF
    self.accumulator *= self.get_from_memory(operand)
    
# Divide accumulator by value from memory
def _divide(self):
    operand = self.instruction_register.value & 0xFFF
    self.accumulator //= self.get_from_memory(operand)

# Load accumulator with value from memory
def _load(self):
    operand = self.instruction_register.value & 0xFFF
    self.accumulator = self.get_from_memory(operand)

# Move accumulator to memory
def _move_to_memory(self):
    operand = self.instruction_register.value & 0xFFF

    if self.indirect_mode:
        addr = self.memory[self.current_bank.value][operand].value << 8 | self.memory[self.current_bank.value][operand + 1].value
        bank = addr >> 12
        addr &= 0xFFF
    else:
        bank = self.current_bank.value
        addr = operand

    self.indirect_mode = False

    self.memory[bank][addr].value = self.accumulator

def _subroutine_call(self):
    operand = self.instruction_register.value & 0xFFF
    next_instr = self.program_counter.value

    self.memory[self.current_bank.value][operand].value = next_instr >> 8
    self.memory[self.current_bank.value][operand + 1].value = next_instr & 0xFF

    self.program_counter.value = operand + 2
    
def _return_from_subroutine(self):
    # TODO: fazer essa func
    pass
    
def _halt_machine(self):
    operand = (self.instruction_register.value & 0x0F00) >> 8

    if operand == 0b00:
        print('Machine halted! ^C to interrupt execution!')
        while True:
            try: pass
            except KeyboardInterrupt: self.running = False

    elif operand == 0b01: self.indirect_mode = True
    elif operand == 0b10: self.indirect_mode = False

def _get_data(self):
    self.accumulator = c_int8(input('Enter data: '))

def _put_data(self):
    print('ACC => {1:04d}'.format(self.accumulator.value))
    
def _operating_system(self):
    operand = (self.instruction_register.value & 0x0F00) >> 8

    # Dump current state to stdout
    if operand == 0b0000:
        print('-- Current VM State')
        print('ACC => {0: 04d}'.format(self.accumulator.value))
        print('PC  => {0: #05x}'.format(self.program_counter.value.value))
        print('RI  => {0: #05x}'.format(self.instruction_register.value))

    # Finish execution
    elif operand == 0b1111:
        self.running = False