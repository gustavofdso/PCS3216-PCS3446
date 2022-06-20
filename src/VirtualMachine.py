import pandas as pd
from ctypes import c_uint8, c_uint16, c_int8

class VirtualMachineError(Exception): pass

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
        self.accumulator = c_int8(0)
    
        self.instruction_decoder = pd.DataFrame(
            (
                (0x0, self._jump),
                (0x1, self._jump_if_zero),
                (0x2, self._jump_if_negative),
                (0x3, self._load_value),
                (0x4, self._add),
                (0x5, self._subtract),
                (0x6, self._multiply),
                (0x7, self._divide),
                (0x8, self._load),
                (0x9, self._move_to_memory),
                (0xA, self._subroutine_call),
                (0xB, self._return_from_subroutine),
                (0xC, self._halt_machine),
                (0xD, self._get_data),
                (0xE, self._put_data),
                (0xF, self._operating_system)
            ), columns = ['opcode', 'instruction']
        )

    # Defining machine system programs
    from src.assemble import assemble
    from src.load import load
    from src.dump import dump, hex_dump

    # Get data from memory
    def get_from_memory(self, adress):
        if self.indirect_mode:
            addr = self.memory[self.current_bank][adress].value << 8 | self.memory[self.current_bank][adress + 1].value
            addr &= 0xFFF
        else:
            addr = adress

        self.indirect_mode = False

        return self.memory[self.current_bank][addr].value

    # Defining machine instructions
    from src.instructions import (
        _jump, _jump_if_zero, _jump_if_negative, _load_value,
        _add, _subtract, _multiply, _divide,
        _load, _move_to_memory, _subroutine_call, _return_from_subroutine,
        _halt_machine, _get_data, _put_data, _operating_system
    )

    # Defining execution algorithm 
    def fetch_instruction(self):
        # TODO: debug
        self.instruction_register = self.memory[self.current_bank.value][self.program_counter.value].value << 8 | self.memory[self.current_bank.value][self.program_counter.value + 1].value
        self.program_counter.value += 2

    def execute_instruction(self):
        # TODO: talvez isso de bug
        opcode = (self.program_counter >> 12).value

        if opcode not in self.instruction_decoder['opcode']:
            raise VirtualMachineError('Bad instruction @ 0x{:01X}{:03X}'.format(self.current_bank, self.program_counter))
        self.instruction_decoder.set_index(opcode).at[opcode, 'instruction']()

    def run_code(self, step = True):
        self.program_counter = c_uint16(0x20)
        self.running = True
        while self.running:
            self.fetch_instruction()
            self.execute_instruction()
            if step: input()

    def run(self):
        print('Please enter a command!')
        while True:
            msg = input('\n').split()
            command = msg[0].upper()
            try:
                if command == 'HELP':
                    print(
"""
Help!
Valid commands are:

* HELP      - Briefs the commands.
* ASM       - Assembles a source code file
    Type 'ASM source' with a source.asm file within the source directory
* LOAD      - Loads a file into memory
    Type 'LOAD <object>' with a object.obj file within the object directory
* DUMP      - Dumps a file from memory
    Type 'DUMP <position> <size> <object>' to dump a file within the object directory
* RUN       - Run code starting from memory position 0x0
    Type 'RUN' or 'RUN STEP' to start running code
* EXIT      - Stops the command interpreter
"""
                    )
                elif command == 'ASM':
                    source = msg[1]
                    self.assemble(source)
                elif command == 'LOAD':
                    source = msg[1]
                    self.load(source)
                elif command == 'DUMP':
                    position, size, source = int(msg[1]), int(msg[2]), msg[3]
                    self.dump(position, size, source)
                elif command == 'RUN':
                    if len(msg) == 1:
                        self.run_code(step = False)
                    else:
                        step = msg[1].upper()
                        if step == 'STEP': self.run_code(step = True)
                        else: print("Type 'RUN' or 'RUN STEP' to start running code")
                elif command == 'EXIT':
                    print('Exiting command interpreter!')
                    break
                else:
                    print("Invalid command! Type 'HELP'!")
            except Exception as e: print("Error!\n" + e.with_traceback + "\n Type 'HELP'!")