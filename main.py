from src.VirtualMachine import VirtualMachine

virtualmachine = VirtualMachine()
virtualmachine.assemble('soma')
virtualmachine.load('soma')
virtualmachine.run()