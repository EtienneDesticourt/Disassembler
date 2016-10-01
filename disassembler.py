from disassembler_exception import DisassemblerException
import binascii, struct

#DATA
SHORT = 2
LONG = 4

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
PE_OPT_SIGNATURE        = b'\x0B\x01'
PE_OPT_SIGNATURE_LENGTH = SHORT
LINKER_VERSION_LENGTH   = LONG #major + minor
SIZE_CODE_LENGTH        = LONG


class PEExecutable(object):
	def __init__(self):
		pass

	def parse(self, bytes):
		print(len(bytes))
		#CHECK DOES HEADER INTEGRITY
		dosSignature = bytes[DOS_SIGNATURE_SLICE]
		if dosSignature != DOS_SIGNATURE:
			raise DisassemblerException("Corrupted executable file. Wrong DOS signature.")


		#CHECK PE HEADER INTEGRITY
		peOffset = bytes[PE_OFFSET_LOCATION]
		peSignature = bytes[peOffset:peOffset + PE_SIGNATURE_LENGTH]
		if peSignature != PE_SIGNATURE:
			raise DisassemblerException("Corrupted executable file. Wrong PE signature.")

		currentOffset = peOffset + PE_SIGNATURE_LENGTH
		machine = bytes[currentOffset:currentOffset + MACHINE_LENGTH]
		if machine != INTEL_MACHINE:
			raise DisassemblerException("Wrong compilation. Only INTEL machine supported.")

		currentOffset += MACHINE_LENGTH
		numSections = bytes[currentOffset:currentOffset + NUM_SECTIONS_LENGTH]

		currentOffset += NUM_SECTIONS_LENGTH + TIMEDATE_LENGTH
		#We save it to get the size of the optional header later
		#which should be here if no deprecated values are present
		timedateEndOffset = currentOffset

		#GET START OF PE OPT HEADER
		#Check if deprecated values present
		currentOffset += SIZE_OPT_HEADER_LENGTH + CHARAC_LENGTH
		peOptSignature = bytes[currentOffset:currentOffset + PE_OPT_SIGNATURE_LENGTH]
		if peOptSignature != PE_OPT_SIGNATURE:
			#Deprecated values (pointer to symbol table and num of symb. table) might be present, we must look further for signature
			currentOffset += SYMB_TABLE_LENGTH + NUM_SYMB_TABLE_LENGTH
			peOptSignature = bytes[currentOffset:currentOffset + PE_OPT_SIGNATURE_LENGTH]
			if peOptSignature != PE_OPT_SIGNATURE:
				raise DisassemblerException("Corrupted executable file. Wrong PE opt signature.")
			sizeOptHeaderOffset = timedateEndOffset + SYMB_TABLE_LENGTH + NUM_SYMB_TABLE_LENGTH
			sizeOptHeader = bytes[sizeOptHeaderOffset:sizeOptHeaderOffset + SIZE_OPT_HEADER_LENGTH]
		else:
			sizeOptHeader = bytes[timeDateEndOffset:timeDateEndOffset + SIZE_OPT_HEADER_LENGTH]
		sizeOptHeader = int.from_bytes(sizeOptHeader, byteorder='little')


		#GET START OF SECTIONS
		name = bytes[currentOffset + sizeOptHeader:currentOffset + sizeOptHeader+16]
		print(name)






		#stores section
		#get .text section
		#find x86 opcodes
		#translate to assembly



if __name__ == '__main__':
	with open("main.exe", "rb") as f:
	    data = f.read()

	parser = PEExecutable()
	parser.parse(data)
