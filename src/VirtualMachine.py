from src.Assembler import Assembler
from src.Linker import Linker

from ctypes import c_uint8, c_uint16, c_int8

class VirtualMachine:
    def __init__(self, banks = 16, bank_size = 4096):
        # Initializing system memory
        self.current_bank = c_uint8(0)
        self.indirect_mode = False
        self.running = True
        self.memory = [[c_uint8(0) for i in range(bank_size)] for j in range(banks)]
        
        # Initializing system registers
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

    # Defining machine instructions
    def _jump(self, instruction):
        pass

    def _jump_if_zero(self, instruction):
        pass

    def _jump_if_negative(self, instruction):
        pass
        
    def _load_value(self, instruction):
        pass
        
    def _add(self, instruction):
        pass

    def _sub(self, instruction):
        pass

    def _multiply(self, instruction):
        pass
        
    def _divide(self, instruction):
        pass

    def _load(self, instruction):
        pass

    def _move_to_memory(self, instruction):
        pass

    def _subroutine_call(self, instruction):
        pass
        
    def _return_from_subroutine(self, instruction):
        pass
        
    def _halt_machine(self, instruction):
        pass

    def _get_data(self, instruction):
        pass

    def _put_data(self, instruction):
        pass
        
    def _operating_system(self, instruction):
        pass

    # Defining execution algorithm 
    def run(self):
        pass