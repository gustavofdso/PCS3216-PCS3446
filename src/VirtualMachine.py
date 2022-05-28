from src.Assembler import Assembler
from src.Loader import Loader
from src.Dumper import Dumper
from src.Linker import Linker

class VirtualMachine:
    def __init__(self):
        self.assembler = Assembler()
        self.loader = Loader()
        self.dumper = Dumper()
        self.linker = Linker()