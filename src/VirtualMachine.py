import argparse
from ctypes import c_uint8, c_uint16, c_int8

class VirtualMachine:
    def __init__(self, banks = 16, bank_size = 4096):
        # Initializing system memory
        self.indirect_mode = False
        self.current_bank = c_uint8(0)
        self.memory = [[c_uint8(0) for i in range(bank_size)] for j in range(banks)]
        
        # Initializing system registers
        self.program_counter = c_uint16(0)
        self.link_register = c_uint16(0)
        self.instruction_register = c_uint16(0)
        self.accumulator = c_int8(0)

    # Defining machine system programs
    from src.assemble import assemble
    from src.load import load
    from src.dump import dump, hex_dump

    # Get adress for memory acess
    def get_indirect_adress(self, adress):
        if self.indirect_mode:
            adress = self.memory[self.current_bank][adress].value << 8 | self.memory[self.current_bank][adress + 1].value
            adress &= 0xFFF
        self.indirect_mode = False

        return adress

    # Defining string to number conversion
    def string_to_number(self, number):
        if number[0] == '=': number = int(number[1:], 10)
        elif number[0] == '#': number = int(number[1:], 2)
        elif number[0] == '/': number = int(number[1:], 16)
        else:
            try: number = int(number, 10)
            except Exception: pass

        return number

    # Defining machine instructions
    from src.instructions import (
        _jump, _jump_if_zero, _jump_if_negative, _load_value,
        _add, _subtract, _multiply, _divide,
        _load, _move_to_memory, _subroutine_call, _return_from_subroutine,
        _halt_machine, _get_data, _put_data, _operating_system
    )

    # Defining execution algorithm 
    def fetch_instruction(self):
        # Fetching instruction and updating program counter
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

    def run_code(self, start_adress, bank, step = False):
        self.program_counter.value = self.string_to_number(start_adress)
        self.current_bank.value = self.string_to_number(bank)

        # Running sequential instructions
        self.running = True
        while self.running:
            self.fetch_instruction()
            self.execute_instruction()
            if step:
                input()
                print(
                    'Machine status:\n'
                    '\tACC => {:d}\n'.format(self.accumulator.value),
                    '\tPC  => {:#05X}\n'.format(self.program_counter.value),
                    '\tRI  => {:#05X}'.format(self.instruction_register.value)
                )

    def run(self):
        print('Enter a command!')
        while True:
            msg = input('$ ').split()
            if len(msg) == 0: continue
            command = msg[0].upper()
            parser = argparse.ArgumentParser()
            try:
                if command == 'HELP':
                    print(
"""
* HELP          - Briefs the commands.
    usage: HELP
* ASM           - Assembles a source code file.
    usage: ASM FILENAME
* LOAD          - Loads a file into memory.
    usage: LOAD FILENAME
* DUMP          - Dumps a file from memory.
    usage: DUMP FILENAME [-s SIZE] [-a ADRESS] [-b BANK] [--hex]

    options:
        -s      Selects the size for the code in bytes. Default 16.
        -a      Selects the start adress for the code. Default 0x0.
        -b      Selects the memory bank for the code. Default 0.
        --hex   Selects if the dump should be binary to file or hexadecimal to screen. Default False.
* RUN       - Run code.
    usage: RUN [-a ADRESS] [-b BANK] [--step]

    options:
        -a      Selects the start adress for the code. Default 0x0.
        -b      Selects the memory bank for the code. Default 0.
        --step  Selects if the code should be run step by step. Default False.
* EXIT      - Stops the command interpreter.
    usage: EXIT
"""
                    )

                elif command == 'ASM':
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    self.assemble(args[1])

                elif command == 'LOAD':
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    self.load(args[1])

                elif command == 'DUMP':
                    parser.add_argument('-s', default = '16', type = str)
                    parser.add_argument('-a', default = '0', type = str)
                    parser.add_argument('-b', default = '0', type = str)
                    parser.add_argument('--hex', action = "store_true")
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    if kwargs['hex']:
                        self.hex_dump(kwargs['s'], kwargs['a'], kwargs['b'])
                    else:
                        self.dump(args[1], kwargs['s'],  kwargs['a'], kwargs['b'])

                elif command == 'RUN':
                    parser.add_argument('-a', default = '0', type = str)
                    parser.add_argument('-b', default = '0', type = str)
                    parser.add_argument('--step', action = "store_true")
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    self.run_code(kwargs['a'], kwargs['b'], step = kwargs['step'])

                elif command == 'EXIT':
                    print('Exiting command interpreter!')
                    break

                else:
                    print("Invalid command! Type HELP!")
            
            except IndexError: print("Incorrect usage for this command! Type 'HELP'!")
            except Exception as e: print(e.__class__.__name__ + ': ' + str(e) + "\n\nType 'HELP'!")