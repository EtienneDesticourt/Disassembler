from portable_executable import PortableExecutable

class Disassembler(object):

    def disassembleByteStream(self, byteStream):
        pass

    def disassemble(self, codeSection):
        pass






if __name__ == '__main__':
    parser = PortableExecutable("main.exe")

    section = parser.sections[".text"]

    if section:
        print("Name:", section.name)
        print("Data size:", section.sizeRawData)
        print("Data offset:", section.pointerRawData)

