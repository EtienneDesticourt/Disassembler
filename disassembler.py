from portable_executable import PortableExecutable
from opcodes import OPCODES
from disassembler_exception import DisassemblerException
from instruction import Instruction

class Disassembler(object):

    def parsePrefix(self, byte):
        pass

    def parseOpcode(self, byte):
        pass


    def getBitArray(self, num):
        bitString = bin(num)[2:]
        bits = [int(i) for i in bitString]
        return (8 - len(bits))*[0] + bits

    def disassembleByteStream(self, byteStream):
        pass

    def disassemble(self, bytes):
        instructions = []
        k = 0
        while k < len(bytes):
            firstByteIndex = k

            b = bytes[k]
            k += 1

            if opcode not in OPCODES:
                break
                #raise DisassemblerException("Unknown opcode: " + hex(opcode))

            #Handle prefixes modifiers or required
            prefixGroup = 1
            while prefixGroup:
                b = bytes[k]
                mnemonics, numArgs, prefixGroup = OPCODES[opcode]
                k += 1

            #Handle escape sequence if any
            b = bytes[k]
            k += 1
            if b == 0x0F:
                b = bytes[k]
                k += 1
                if b == 0x38 or b == 0x3A:
                    b = bytes[k]
                    k += 1

            #Handle opcode and potential extensions
            opcode = b
            mnemonics, numArgs, prefixGroup = OPCODES[opcode]
            if prefixGroup:
                raise DisassemblerException("Misplaced prefix. Parsing has gone haywire.")

            #Handle Modrm
            if numArgs > 0:
                b = bytes[k]
                k += 1
                modRM = self.getBitArray(byte)
                mod = modRM[:2]
                reg1 = modRM[2:5]
                reg2 = modRM[5:]

                #Handle SIB
                if mod != [1,1] and reg1 == [1, 0, 0]:
                    b = bytes[k]
                    k += 1

                #Handle displacement
                if mod == [0,1]:
                    dispSize = 8 / 8
                if mod == [1,0]:
                    dispSize = 32 / 8












            instruction = Instruction(bytes[firstByteIndex:k + numArgs], firstByteIndex)
            instructions.append(instruction)
            k += numArgs

        return instructions


if __name__ == '__main__':
    parser = PortableExecutable("main.exe")

    section = parser.sections[".text"]


    print("Name:", section.name)
    print("Data size:", section.sizeRawData)
    print("Data offset:", section.pointerRawData)

    ep = parser.rawEntryPoint
    bytes = section.rawData[ep - section.pointerRawData:]
    instructions = Disassembler().disassemble(bytes)
    print(len(instructions))
    for i in instructions:
        print(i.disassembly)

