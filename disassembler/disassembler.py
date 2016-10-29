from portable_executable import PortableExecutable
from opcodes import OPCODES
from disassembler_exception import DisassemblerException
from instruction import Instruction
import instruction_part
from prefix import Prefix


class Disassembler(object):

    def parse_stream(self, bytes):
        instructions = []

        previous_part = None

        for b in bytes:
            if not previous_part:
                instruction = Instruction()

            if previous_part == None or previous_part == instruction_part.PREFIX:
                if Prefix.is_prefix(b):
                    current_part = Prefix(b)
                    previous_part = instruction_part.PREFIX
                else:
                    current_part = Opcode(b)
                    previous_part = instruction_part.OPCODE

            if previous_part == instruction_part.OPCODE:  # We only support 1 byte opcodes for now

            instruction.add_part(current_part)

        return instructions

    def get_bit_array(self, num):
        bitString = bin(num)[2:]
        bits = [int(i) for i in bitString]
        return (8 - len(bits)) * [0] + bits

    def disassemble(self, bytes):
        instructions = []
        k = 0
        while k < len(bytes):
            first_byteIndex = k

            #b = bytes[k]
            #k += 1

            # if b not in OPCODES:
            #    break
            #raise DisassemblerException("Unknown opcode: " + hex(opcode))

            # Handle prefixes modifiers or required
            prefixGroup = 1
            while prefixGroup:
                b = bytes[k]
                mnemonics, numArgs, prefixGroup = OPCODES[b]
                k += 1

            # Handle escape sequence if any
            b = bytes[k]
            k += 1
            if b == 0x0F:
                b = bytes[k]
                k += 1
                if b == 0x38 or b == 0x3A:
                    b = bytes[k]
                    k += 1

            # Handle opcode and potential extensions
            opcode = b
            mnemonics, numArgs, prefixGroup = OPCODES[opcode]
            if prefixGroup:
                raise DisassemblerException(
                    "Misplaced prefix. Parsing has gone haywire.")

            # Handle Modrm
            if numArgs > 0:
                b = bytes[k]
                k += 1
                modRM = self.getBitArray(b)  # [::-1]
                mod = modRM[:2]
                reg1 = modRM[2:5]
                reg2 = modRM[5:]

                # Handle SIB
                if mod != [1, 1] and reg1 == [1, 0, 0]:
                    b = bytes[k]
                    k += 1

                # Handle displacement
                if mod == [0, 1]:
                    dispSize = 8 / 8
                    k += dispSize
                if mod == [1, 0]:
                    dispSize = 32 / 8
                    k += dispSize

            instruction = Instruction(bytes[firstByteIndex:k], firstByteIndex)
            print(instruction.bytes)
            instructions.append(instruction)
            #k += numArgs

        return instructions


if __name__ == '__main__':
    parser = PortableExecutable("main.exe")

    section = parser.sections[".text"]

    print("Name:", section.name)
    print("Data size:", section.sizeRawData)
    print("Data offset:", section.pointerRawData)

    ep = parser.rawEntryPoint
    bytes = section.rawData[ep - section.pointerRawData:]
    # instructions = Disassembler().disassemble(bytes)
    # print(len(instructions))
    # for i in instructions:
    #     print(i.disassembly)
