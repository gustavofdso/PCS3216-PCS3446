import pandas as pd
from ctypes import c_uint8, c_uint16, c_int8

class VirtualMachineError(Exception): pass

class VirtualMachine:
    def __init__(self, banks = 16, bank_size = 4096):
        # Initializing system memory
        self.indirect_mode = False
        self.current_bank = c_uint8(0)
        self.memory = [[c_uint8(0) for i in range(bank_size)] for j in range(banks)]
        
        # Initializing system registers
        self.program_counter = c_uint16(0)
        self.instruction_register = c_uint16(0)
        self.accumulator = c_int8(0)

    # Defining machine system programs
    from src.assemble import assemble
    from src.load import load
    from src.dump import dump, hex_dump

    # Get data from memory
    def get_indirect_adress(self, adress):
        if self.indirect_mode:
            adress = self.memory[self.current_bank][adress].value << 8 | self.memory[self.current_bank][adress + 1].value
            adress &= 0xFFF
        self.indirect_mode = False

        return adress

    # Defining machine instructions
    from src.instructions import (
        _jump, _jump_if_zero, _jump_if_negative, _load_value,
        _add, _subtract, _multiply, _divide,
        _load, _move_to_memory, _subroutine_call, _return_from_subroutine,
        _halt_machine, _get_data, _put_data, _operating_system
    )

    # Defining execution algorithm 
    def fetch_instruction(self):
        self.instruction_register.value = self.memory[self.current_bank.value][self.program_counter.value].value << 8 | self.memory[self.current_bank.value][self.program_counter.value + 1].value
        self.program_counter.value += 2

    def execute_instruction(self):
        # Getting opcode and executing instruction
        opcode = (self.instruction_register.value & 0xF000) >> 12
        if   opcode == 0x0: self._jump()
        elif opcode == 0x1: self._jump_if_zero()
        elif opcode == 0x2: self._jump_if_negative()
        elif opcode == 0x3: self._load_value()
        elif opcode == 0x4: self._add()
        elif opcode == 0x5: self._subtract()
        elif opcode == 0x6: self._multiply()
        elif opcode == 0x7: self._divide()
        elif opcode == 0x8: self._load()
        elif opcode == 0x9: self._move_to_memory()
        elif opcode == 0xA: self._subroutine_call()
        elif opcode == 0xB: self._return_from_subroutine()
        elif opcode == 0xC: self._halt_machine()
        elif opcode == 0xD: self._get_data()
        elif opcode == 0xE: self._put_data()
        elif opcode == 0xF: self._operating_system()

    def run_code(self, step = True):
        self.program_counter = c_uint16(0x0)
        self.running = True
        while self.running:
            self.fetch_instruction()
            self.execute_instruction()
            if step: input()

    def run(self):
        print('Enter a command!')
        while True:
            msg = input('$').split()
            command = msg[0].upper()
            try:
                # TODO: fazer pyparsing com flags
                if command == 'HELP':
                    print(
"""
Help!
Valid commands are:

* HELP      - Briefs the commands.
* ASM       - Assembles a source code file
    Type 'ASM <source>' with a source.asm file within the source directory
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
                    source, position, size = msg[1:4]
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
            except Exception as e: print(e.__class__.__name__ + ': ' + str(e), "\n\nType 'HELP'!")