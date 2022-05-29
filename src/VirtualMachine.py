from src.CPU import CPU

from src.Assembler import Assembler
from src.Linker import Linker

class VirtualMachine:
    def __init__(self):
        # Initializing CPU
        self.CPU = CPU()

        # Initializing system programms
        self.assembler = Assembler()
        self.linker = Linker()

    def load(self):
        pass

    def dump(self):
        pass

    def hex_dump(self):
        pass

    def run(self):
        pass