from disassembler_exception import PEParsingException
from type_length import SHORT, LONG
from section import Section, SECTION_LENGTH

#DOS HEADER
DOS_SIGNATURE       = b'MZ' #Mike Zbikowski
DOS_SIGNATURE_SLICE = slice(0,2)
PE_OFFSET_LOCATION  = 0x3C

#PE HEADER
PE_SIGNATURE            = b'PE\0\0'
PE_SIGNATURE_LENGTH     = LONG
INTEL_MACHINE     	    = b'\x4C\x01'
MACHINE_LENGTH          = SHORT
NUM_SECTIONS_LENGTH     = SHORT
TIMEDATE_LENGTH         = LONG
SYMB_TABLE_LENGTH       = LONG #deprecated
NUM_SYMB_TABLE_LENGTH   = LONG #deprecated
SIZE_OPT_HEADER_LENGTH  = SHORT
CHARAC_LENGTH           = SHORT

#PE OPT HEADER
PE_OPT_OFFSET           = PE_SIGNATURE_LENGTH + MACHINE_LENGTH + NUM_SECTIONS_LENGTH + TIMEDATE_LENGTH + SIZE_OPT_HEADER_LENGTH + CHARAC_LENGTH
DEPR_PE_OPT_OFFSET      = PE_OPT_OFFSET + SYMB_TABLE_LENGTH + NUM_SYMB_TABLE_LENGTH
PE_OPT_SIGNATURE        = b'\x0B\x01'
PE_OPT_SIGNATURE_LENGTH = SHORT
LINKER_VERSION_LENGTH   = LONG #major + minor
SIZE_CODE_LENGTH        = LONG



class PortableExecutable(object):
	def __init__(self):
		self.sections = []

	def getSection(self, name):
		for section in self.sections:
			if section.name == name:
				return section

	def checkFileCorrectness(self, bytes):
		#CHECK DOES HEADER INTEGRITY
		dosSignature = bytes[DOS_SIGNATURE_SLICE]
		if dosSignature != DOS_SIGNATURE:
			raise PEParsingException("Corrupted executable file. Wrong DOS signature.")

		#CHECK PE HEADER INTEGRITY
		peOffset = bytes[PE_OFFSET_LOCATION]
		peSignature = bytes[peOffset:peOffset + PE_SIGNATURE_LENGTH]
		if peSignature != PE_SIGNATURE:
			raise PEParsingException("Corrupted executable file. Wrong PE signature.")

		#CHECK CORRECT MACHINE COMPILATION
		currentOffset = peOffset + PE_SIGNATURE_LENGTH
		machine = bytes[currentOffset:currentOffset + MACHINE_LENGTH]
		if machine != INTEL_MACHINE:
			raise PEParsingException("Wrong compilation. Only INTEL machine supported.")

	def getNumSections(self, bytes):
		peOffset = bytes[PE_OFFSET_LOCATION]
		numSectionOffset = peOffset + PE_SIGNATURE_LENGTH + MACHINE_LENGTH
		numSections = bytes[numSectionOffset:numSectionOffset + NUM_SECTIONS_LENGTH]
		return int.from_bytes(numSections, byteorder='little')

	def getSectionOffset(self, bytes):
		#GET START OF PE OPT HEADER
		peOffset = bytes[PE_OFFSET_LOCATION]

		#Look for optional pe header offset, and check whether it's at deprecated location
		peOptOffset = peOffset + PE_OPT_OFFSET
		signature = bytes[peOptOffset: peOptOffset + PE_OPT_SIGNATURE_LENGTH]
		if signature != PE_OPT_SIGNATURE:
			peOptOffset = peOffset + DEPR_PE_OPT_OFFSET
			signature = bytes[peOptOffset: peOptOffset + PE_OPT_SIGNATURE_LENGTH]
			if signature != PE_OPT_SIGNATURE:
				raise PEParsingException("Corrupted executable file. Wrong PE opt signature.")

		#Find the size of the optional header, stored in the PE header
		sizeOptHeaderOffset = peOptOffset - CHARAC_LENGTH - SIZE_OPT_HEADER_LENGTH
		sizeOptHeader = bytes[sizeOptHeaderOffset: sizeOptHeaderOffset + SIZE_OPT_HEADER_LENGTH]

		return peOptOffset + int.from_bytes(sizeOptHeader, byteorder='little')

	def parse(self, bytes):
		self.checkFileCorrectness(bytes)

		print("File shows no signs of corruption.")

		#Parse all sections
		self.sections = []
		sectionOffset = self.getSectionOffset(bytes)
		sectionTable = bytes[sectionOffset:]
		numSections = self.getNumSections(bytes)

		print("Found " + str(numSections) + " sections.\n")

		for i in range(numSections):
			s = Section()
			s.parse(sectionTable[i * SECTION_LENGTH:], bytes)
			self.sections.append(s)

		#get .text section
		#find x86 opcodes
		#translate to assembly

