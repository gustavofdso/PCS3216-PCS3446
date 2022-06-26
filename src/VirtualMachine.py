import argparse
import pandas as pd
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

        # Initializing instructions table
        self.mnemonic_table = pd.DataFrame(
            (
                ('JP', 0x0, self._jump),
                ('JZ', 0x1, self._jump_if_zero),
                ('JN', 0x2, self._jump_if_negative),
                ('LV', 0x3, self._load_value),
                ('+' , 0x4, self._add),
                ('-' , 0x5, self._subtract),
                ('*' , 0x6, self._multiply),
                ('/' , 0x7, self._divide),
                ('LD', 0x8, self._load),
                ('MM', 0x9, self._move_to_memory),
                ('SC', 0xA, self._subroutine_call),
                ('RS', 0xB, self._return_from_subroutine),
                ('HM', 0xC, self._halt_machine),
                ('GD', 0xD, self._get_data),
                ('PD', 0xE, self._put_data),
                ('OS', 0xF, self._operating_system)
            ), columns = ['mnemonic', 'opcode', 'instruction']
        )

        # Initializing labels for program linking
        self.linker_labels = pd.DataFrame(columns = ['label', 'adress'])

    # Defining machine instructions
    from src.instructions import (
        _jump, _jump_if_zero, _jump_if_negative, _load_value,
        _add, _subtract, _multiply, _divide,
        _load, _move_to_memory, _subroutine_call, _return_from_subroutine,
        _halt_machine, _get_data, _put_data, _operating_system
    )

    # Defining machine system programs
    from src.load import load
    from src.dump import dump, hex_dump
    from src.assemble import assemble

    # Defining machine utils
    from src.utils import get_target_adress, process_operator, show_status, show_files

    # Defining machine execution algorithm
    from src.execute import fetch_instruction, execute_instruction, run_code

    # Defining command interpreter
    def run(self):
        print('Enter a command! Type HELP to see possible commands.')
        while True:
            msg = input('$ ').split()
            if len(msg) == 0: continue
            command = msg[0].upper()
            parser = argparse.ArgumentParser()
            try:
                # HELP command
                if command == 'HELP':
                    print(
"""
* HELP          - Briefs the commands.
    usage: $ HELP
* DIR           - Lists available files.
    usage: $ DIR
* STA           - Shows the current status for the virtual machine's registers.
    usage: $ STA
* ASM           - Assembles a source code file.
    usage: $ ASM FILENAME
* LOAD          - Loads a file into memory.
    usage: $ LOAD FILENAME
* DUMP          - Dumps a file from memory.
    usage: $ DUMP FILENAME [-s SIZE] [-a ADRESS] [-b BANK] [--hex]

    options:
        -s      Selects the size for the code in bytes. Default 16.
        -a      Selects the start adress for the code. Default 0x0.
        -b      Selects the memory bank for the code. Default 0.
        --hex   Selects if the dump should be binary to file or hexadecimal to screen. Default False.
* RUN       - Run code.
    usage: $ RUN [-a ADRESS] [-b BANK] [--step]

    options:
        -a      Selects the start adress for the code. Default 0x0.
        -b      Selects the memory bank for the code. Default 0.
        --step  Selects if the code should be run step by step. Default False.
* EXIT      - Stops the command interpreter.
    usage: $ EXIT
"""
                    )

                # DIR command
                if command == 'DIR':
                    self.show_files()

                # STA command
                elif command == 'STA':
                    self.show_status()

                # ASM command
                elif command == 'ASM':
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    self.assemble(args[1])

                # LOAD command
                elif command == 'LOAD':
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    self.load(args[1])

                # DUMP command
                elif command == 'DUMP':
                    parser.add_argument('-s', default = '16', type = str)
                    parser.add_argument('-a', default = '0', type = str)
                    parser.add_argument('-b', default = '0', type = str)
                    parser.add_argument('--hex', action = "store_true")
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    if kwargs['hex']: self.hex_dump(kwargs['s'], kwargs['a'], kwargs['b'])
                    else: self.dump(args[1], kwargs['s'],  kwargs['a'], kwargs['b'])

                # RUN command
                elif command == 'RUN':
                    parser.add_argument('-a', default = '0', type = str)
                    parser.add_argument('-b', default = '0', type = str)
                    parser.add_argument('--step', action = "store_true")
                    kwargs, args = parser.parse_known_args(msg)
                    kwargs = vars(kwargs)
                    self.run_code(kwargs['a'], kwargs['b'], step = kwargs['step'])

                # EXIT command
                elif command == 'EXIT':
                    print('Exiting command interpreter!')
                    break

                else:
                    print("Invalid command! Type HELP to see possible commands.")
            
            except IndexError: print("Incorrect usage for this command! Type HELP to see possible commands.")
            except Exception as e: print(e.__class__.__name__ + ': ' + str(e) + "\nType HELP to see possible commands.")