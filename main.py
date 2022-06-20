from src.VirtualMachine import VirtualMachine

virtualmachine = VirtualMachine()
virtualmachine.load('soma')
# virtualmachine.dump(0, 10, 'somadump')
virtualmachine.hex_dump(0, 25)
virtualmachine.run()