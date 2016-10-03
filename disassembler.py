from portable_executable import PortableExecutable
from opcodes import OPCODES
from disassembler_exception import DisassemblerException

class Disassembler(object):

    def disassembleByteStream(self, byteStream):
        pass

    def disassemble(self, codeSection):
        bytes = codeSection.rawData
        i = 0
        while i < len(bytes):
            opcode = bytes[i]
            if opcode not in OPCODES:
                raise DisassemblerException("Unknown opcode: " + opcode.decode('utf8'))
            i += 1

            






if __name__ == '__main__':
    parser = PortableExecutable("main.exe")

    section = parser.sections[".text"]

    
    print("Name:", section.name)
    print("Data size:", section.sizeRawData)
    print("Data offset:", section.pointerRawData)

    Disassembler().disassemble(section)

