import struct

#SECTION TABLE
NAME_FORMAT                     = "8s"
VIRTUAL_SIZE_FORMAT             = "l"
VIRTUAL_ADDRESS_FORMAT          = "l"
SIZE_OF_RAW_DATA_FORMAT         = "l"
POINTER_TO_RAW_DATA_FORMAT      = "l"
POINTER_TO_RELOCATIONS_FORMAT   = "l"
POINTER_TO_LINE_NUMBERS_FORMAT  = "l"
NUMBER_OF_RELOCATIONS_FORMAT    = "h"
NUMBER_OF_LINE_NUMBERS_FORMAT   = "h"
CHARACTERISTICS_FORMAT          = "l"
SECTION_LENGTH                  = 0x28

FORMATS = [NAME_FORMAT, VIRTUAL_SIZE_FORMAT, VIRTUAL_ADDRESS_FORMAT, SIZE_OF_RAW_DATA_FORMAT, POINTER_TO_RELOCATIONS_FORMAT, POINTER_TO_RAW_DATA_FORMAT,
           POINTER_TO_LINE_NUMBERS_FORMAT, NUMBER_OF_RELOCATIONS_FORMAT, NUMBER_OF_LINE_NUMBERS_FORMAT, CHARACTERISTICS_FORMAT]

SECTION_FORMAT = '<' + ''.join(FORMATS)

class Section(object):
    def __init__(self, sectionBytes, bytes):
        self.parse(sectionBytes, bytes)

    def parse(self, sectionBytes, bytes):
        fields = struct.unpack(SECTION_FORMAT, sectionBytes)
        print(fields[0])
        self.name           = fields[0].decode('utf8').rstrip('\0')
        self.virtualSize    = fields[1]
        self.virtualAddress = fields[2]
        self.sizeRawData    = fields[3]
        self.pointerRawData = fields[4]
        self.pointerReloc   = fields[5]
        self.pointerLineNum = fields[6]
        self.numReloc       = fields[7]
        self.numLineNum     = fields[8]
        self.charac         = fields[9]
        self.rawData        = bytes[self.pointerRawData:self.pointerRawData + self.sizeRawData]
