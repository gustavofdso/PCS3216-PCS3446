from src.Assembler import Assembler
from src.Linker import Linker

from ctypes import c_uint8, c_uint16, c_int8

class VirtualMachineError(Exception):
    pass

class VirtualMachine:
    def __init__(self, banks = 16, bank_size = 4096):
        # Initializing system memory
        self.current_bank = c_uint8(0)
        self.indirect_mode = False
        self.running = True
        self.memory = [[c_uint8(0) for i in range(bank_size)] for j in range(banks)]
        
        # Initializing system registers
        self.program_counter = c_uint16(0)
        self.instruction_register = c_uint16(0)
        self.instruction_counter = c_uint16(0)
        self.accumulator = c_int8(0)

        # Initializing system programms
        self.assembler = Assembler()
        self.linker = Linker()

    # Defining machine basic funcionalities
    def load(self, file):
        pass

    def dump(self, file):
        pass

    def hex_dump(self, start_position, end_position):
        pass

    # Get data from memory
    def get_from_memory(self, adress):
        pass

    # Defining machine instructions

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
    def _sub(self):
        operand = self.instruction_register & 0xFFF
        self.accumulator -= self.get_from_memory(operand)

    # Multiply value from memory by accumulator
    def _multiply(self):
        operand = self.instruction_register & 0xFFF
        self.accumulator *= self.get_from_memory(operand)
        
    # Divide value from memory from accumulator
    def _divide(self):
        operand = self.instruction_register & 0xFFF
        self.accumulator //= self.get_from_memory(operand)

    def _load(self):
        operand = self.instruction_register & 0xFFF
        self.accumulator = self.get_from_memory(operand)

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

    # Defining execution algorithm 
    def fetch_instruction(self):
        pass

    def run(self):
        pass