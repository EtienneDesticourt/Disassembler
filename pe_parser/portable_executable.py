import struct
from datetime import datetime
from disassembler_exception import PEParsingException
from section import Section, SECTION_LENGTH

#DOS HEADER
DOS_SIGNATURE       = b'MZ' #Mike Zbikowski
DOS_SIGNATURE_SLICE = slice(0,2)
PE_OFFSET_LOCATION  = 0x3C
SIZE_DOS_HEADER     = 0x40

#COFF HEADER
PE_SIGNATURE      = b'PE\0\0'
INTEL_MACHINE     = b'\x4C\x01'
PE_SIGN_FORMAT    = "4s"
MACHINE_FORMAT    = "2s"
NUM_SEC_FORMAT    = "h"
TIMEDATE_FORMAT   = "l"
POINT_SYMB_FORMAT = "l"
NUM_SYMB_FORMAT   = "l"
SIZE_OPT_FORMAT   = "h"
CHARAC_FORMAT     = "h"
SIZE_PE_HEADER    = 0x18

#PE OPT HEADER
OPT_MAGIC        = b'\x0B\x01'
OPT_MAGIC_FORMAT = "2s"
LINKER_FORMAT    = "bb"
SIZE_CODE_FORMAT = "l"
SIZE_INIT_FORMAT = "l"
SIZE_UNIN_FORMAT = "l"
ADDRESS_ENTRY_FORMAT = "l"
SIZE_PARSED_OPT_HEADER = 0x0C #We only care about the 12 first bytes

FORMATS = [PE_SIGN_FORMAT, MACHINE_FORMAT, NUM_SEC_FORMAT, TIMEDATE_FORMAT, POINT_SYMB_FORMAT, NUM_SYMB_FORMAT,
           SIZE_OPT_FORMAT, CHARAC_FORMAT, OPT_MAGIC_FORMAT, LINKER_FORMAT, SIZE_CODE_FORMAT, SIZE_INIT_FORMAT,
           SIZE_UNIN_FORMAT, ADDRESS_ENTRY_FORMAT]

PE_FORMAT = '<' + ''.join(FORMATS)

#SECTIONS
TEXT_SECTION_NAME = ".text"

class PortableExecutable(object):
    def __init__(self, filePath):
        self.sections = {}
        with open(filePath, 'rb') as f:
            bytes = f.read()
        self.parse(bytes)

    def calcRawEntryPoint(self):
        text = self.sections[TEXT_SECTION_NAME]
        va = text.virtualAddress
        pointRaw = text.pointerRawData
        return pointRaw + (self.addressEntry - va)

    def calcSectionOffset(self):
        return SIZE_PE_HEADER + self.coffOffset + self.sizeOptHeader

    def parse(self, bytes):
        if len(bytes) < SIZE_DOS_HEADER + SIZE_PE_HEADER + SIZE_PARSED_OPT_HEADER:
            raise PEParsingException("Byte stream too short. PE file either truncated or corrupted.")

        if bytes[DOS_SIGNATURE_SLICE] != DOS_SIGNATURE:
            raise PEParsingException("Corrupted executable file. Wrong DOS signature.")

        self.coffOffset = bytes[PE_OFFSET_LOCATION]
        fields = struct.unpack_from(PE_FORMAT, bytes, self.coffOffset)

        #COFF HEADER
        self.signature      = fields[0]
        self.machine        = fields[1]
        self.numSections    = fields[2]
        self.timedateStamp  = fields[3]
        self.pointSymbols   = fields[4]
        self.numSymbols     = fields[5]
        self.sizeOptHeader  = fields[6]
        self.characs        = fields[7]
        #OPT HEADER
        self.optMagic       = fields[8]
        self.majLinker      = fields[9]
        self.minLinker      = fields[10]
        self.sizeCode       = fields[11]
        self.sizeInitData   = fields[12]
        self.sizeUninitData = fields[13]
        self.addressEntry   = fields[14]

        if self.signature != PE_SIGNATURE:
            raise PEParsingException("Corrupted executable file. Wrong PE signature.")

        if self.optMagic != OPT_MAGIC:
            raise PEParsingException("Corrupted executable file. Wrong opt header magic. ")

        sectionOffset = self.calcSectionOffset()
        sectionTable = bytes[sectionOffset:]
        for i in range(self.numSections):
            offset = i * SECTION_LENGTH
            sectionHeader = sectionTable[offset:offset + SECTION_LENGTH]
            s = Section(sectionHeader, bytes)
            self.sections[s.name] = s

        self.rawEntryPoint = self.calcRawEntryPoint()


        #get .text section
        #find x86 opcodes
        #translate to assembly

