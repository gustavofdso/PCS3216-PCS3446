from src.VirtualMachine import VirtualMachine

virtualmachine = VirtualMachine()
virtualmachine.assemble('hello')
virtualmachine.load('hello')
virtualmachine.run_code(start_adress = '0', bank = '0', step = False)
#virtualmachine.run()