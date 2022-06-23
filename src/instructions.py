# Inconditional jump to addresss
from py import process


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
    self.accumulator.value = self.memory[self.current_bank.value][adress].value

# Move accumulator to memory
def _move_to_memory(self):
    operand = self.instruction_register.value & 0x0FFF
    adress = self.get_indirect_adress(operand)
    self.memory[self.current_bank.value][adress].value = self.accumulator.value

# Enter a subroutine
def _subroutine_call(self):
    self.link_register.value = self.program_counter.value
    self._jump()

# Return from a subroutine
def _return_from_subroutine(self):
    self.program_counter.value = self.link_register.value
    
# Halt the machine or turn on/off the memory indirect mode
def _halt_machine(self):
    operand = self.instruction_register.value & 0x000F

    if operand == 0b0000:
        print('Machine halted! Press ^C to interrupt execution!')
        while True:
            try: pass
            except KeyboardInterrupt:
                self.running = False
                break

    elif operand == 0b0001: self.indirect_mode = True
    elif operand == 0b0010: self.indirect_mode = False

# Get a value into the accumulator
def _get_data(self):
    self.accumulator.value = self.process_operator(input('Enter ACC => ')) & 0x00FF

# Put a value from the accumulator
def _put_data(self):
    operand = self.instruction_register.value & 0x000F

    # Decimal form
    if operand == 0b0000:
        print('ACC => {:03d}'.format(self.accumulator.value))

    # Binary form
    elif operand == 0b0001:
        print('ACC => {:08b}'.format(self.accumulator.value))

    # Hexadecimal form
    elif operand == 0b0010:
        print('ACC => {:02X}'.format(self.accumulator.value))

    # Character form
    elif operand == 0b0011:
        print('ACC => {:c}'.format(self.accumulator.value))
    
# Make an OS call
def _operating_system(self):
    operand = self.instruction_register.value & 0x000F

    # Print current state
    if operand == 0b0000:
        print('OS Call! Machine status:')
        print('\tACC => {:03d}'.format(self.accumulator.value))
        print('\tPC  => {:02X}'.format(self.program_counter.value))
        print('\tRI  => {:02X}'.format(self.instruction_register.value))

    # Finish execution
    elif operand == 0b1111:
        self.running = False