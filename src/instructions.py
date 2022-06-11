# Inconditional jump to addresss
def _jump(self):
    operand = self.instruction_register & 0xFFF
    self.program_counter = operand

# Jump to addresss if accumulator is zero
def _jump_if_zero(self):
    if self.accumulator == 0: self._jump()

# Jump to addresss if accumulator is negative
def _jump_if_negative(self):
    if self.accumulator < 0: self._jump()
    
# Load value to accumulator
def _load_value(self):
    operand = self.instruction_register & 0x0FF
    self.accumulator = operand
    
# Add value from memory to accumulator
def _add(self):
    operand = self.instruction_register & 0xFFF
    self.accumulator += self.get_from_memory(operand)

# Subtract value from memory from accumulator
def _subtract(self):
    operand = self.instruction_register & 0xFFF
    self.accumulator -= self.get_from_memory(operand)

# Multiply value from memory by accumulator
def _multiply(self):
    operand = self.instruction_register & 0xFFF
    self.accumulator *= self.get_from_memory(operand)
    
# Divide accumulator by value from memory
def _divide(self):
    operand = self.instruction_register & 0xFFF
    self.accumulator //= self.get_from_memory(operand)

# Load accumulator with value from memory
def _load(self):
    operand = self.instruction_register & 0xFFF
    self.accumulator = self.get_from_memory(operand)

# Move accumulator to memory
def _move_to_memory(self):
    pass

def _subroutine_call(self):
    pass
    
def _return_from_subroutine(self):
    pass
    
def _halt_machine(self):
    pass

def _get_data(self):
    pass

def _put_data(self):
    pass
    
def _operating_system(self):
    pass