from src.VirtualMachine import VirtualMachine

virtualmachine = VirtualMachine()
virtualmachine.assemble('somador')
virtualmachine.load('somador')
virtualmachine.assemble('soma')
virtualmachine.load('soma')
#virtualmachine.run_code(start_adress = '0', bank = '0', step = False)
virtualmachine.run()