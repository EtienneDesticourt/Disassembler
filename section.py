from type_length import SHORT, LONG, DOUBLE

NAME_LENGTH 					= DOUBLE
VIRTUAL_SIZE_LENGTH 			= LONG
VIRTUAL_ADDRESS_LENGTH 			= LONG
SIZE_OF_RAW_DATA_LENGTH 		= LONG
POINTER_TO_RAW_DATA_LENGTH 		= LONG
POINTER_TO_RELOCATIONS_LENGTH 	= LONG
POINTER_TO_LINE_NUMBERS_LENGTH	= LONG
NUMBER_OF_RELOCATIONS_LENGTH 	= SHORT
NUMBER_OF_LINE_NUMBERS_LENGTH 	= SHORT
CHARACTERISTICS_LENGTH 			= LONG

SECTION_LENGTH = NAME_LENGTH + VIRTUAL_SIZE_LENGTH + VIRTUAL_ADDRESS_LENGTH + SIZE_OF_RAW_DATA_LENGTH + POINTER_TO_RELOCATIONS_LENGTH + POINTER_TO_RAW_DATA_LENGTH \
               + POINTER_TO_LINE_NUMBERS_LENGTH + NUMBER_OF_RELOCATIONS_LENGTH + NUMBER_OF_LINE_NUMBERS_LENGTH + CHARACTERISTICS_LENGTH

class Section(object):
	def parse(self, sectionTable):
		currentOffset = 0
		self.name = sectionTable[:NAME_LENGTH]
		currentOffset += NAME_LENGTH

		self.virtualSize = sectionTable[currentOffset: currentOffset + VIRTUAL_SIZE_LENGTH]
		currentOffset += VIRTUAL_SIZE_LENGTH

		self.virtualAddress = sectionTable[currentOffset: currentOffset + VIRTUAL_ADDRESS_LENGTH]
		currentOffset += VIRTUAL_ADDRESS_LENGTH

		self.sizeRawData = sectionTable[currentOffset: currentOffset + SIZE_OF_RAW_DATA_LENGTH]
		currentOffset += SIZE_OF_RAW_DATA_LENGTH

		self.pointerRawData = sectionTable[currentOffset: currentOffset + POINTER_TO_RAW_DATA_LENGTH]
		currentOffset += POINTER_TO_RAW_DATA_LENGTH

		self.pointerReloc = sectionTable[currentOffset: currentOffset + POINTER_TO_RELOCATIONS_LENGTH]
		currentOffset += POINTER_TO_RELOCATIONS_LENGTH

		self.pointerLineNum = sectionTable[currentOffset: currentOffset + POINTER_TO_LINE_NUMBERS_LENGTH]
		currentOffset += POINTER_TO_LINE_NUMBERS_LENGTH

		self.numReloc = sectionTable[currentOffset: currentOffset + NUMBER_OF_RELOCATIONS_LENGTH]
		currentOffset += NUMBER_OF_RELOCATIONS_LENGTH

		self.numLineNum = sectionTable[currentOffset: currentOffset + NUMBER_OF_LINE_NUMBERS_LENGTH]
		currentOffset += NUMBER_OF_LINE_NUMBERS_LENGTH

		self.charac = sectionTable[currentOffset: currentOffset + CHARACTERISTICS_LENGTH]

