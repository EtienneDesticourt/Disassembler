from opcodes import OPCODES

class Instruction(object):
    """Represents an intel instruction. \n
        Takes up 1 to 15 bytes and is composed of 6 parts.\n
        Prefixes: 0-4 bytes\n
        Opcode: 1-3 bytes\n
        ModR/M: 1 byte\n
        SIB: 1 byte\n
        Displacement: 1 byte or word\n
        Immediate: 1 byte or word\n"""
    def __init__(self, bytes, position):
        self.bytes = bytes
        self.disassembly = ""
        for b in bytes:
            if b in OPCODES:
                self.disassembly += OPCODES[b][0]
            else:
                self.disassembly += hex(b)
            self.disassembly += " "
        self.position = position

