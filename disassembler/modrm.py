
class ModRM(object):
    REG_MNEMONICS = {(0, 0, 0): "eax",
                     (0, 0, 1): "ecx",
                     (0, 1, 0): "edx",
                     (0, 1, 1): "ebx",
                     (1, 0, 0): "esp",
                     (1, 0, 1): "ebp",
                     (1, 1, 0): "esi",
                     (1, 1, 1): "edi"}

    def __init__(self, byte):
        self.byte = byte
        bits = self.getBitArray(byte)
        self.mod = bits[:2]
        self.reg = bits[2:5]
        self.rm  = bits[5:]

        self.hasSib = False
        if self.mod != [1, 1]:
            if self.rm == [1, 0, 0]:
                self.hasSib = True

        if self.mod == [0, 1]:
            self.displacementSize = 8 // 8
        elif self.mod == [1, 0]:
            self.displacementSize = 32 // 8
        elif self.mod == [0, 0] and self.rm == [1, 0, 1]:
            self.displacementSize = 32 // 8
        else:
            self.displacementSize = 0

        self.hasDisplacement = self.displacementSize

    def getMnemonic(self, sibMnemonic="SIB"):
        mne = "{reg}, {rm}"
        mne = mne.format(reg=self.REG_MNEMONICS[tuple(self.reg)],
                         rm="{rm}")

        rmMne = self.REG_MNEMONICS[tuple(self.rm)]
        if self.mod == [1, 1]:
            mne = mne.format(rm=rmMne)
        else:
            mne = mne.format(rm="[{register}{displacement}]")

            if self.hasSib:
                reg = sibMnemonic
            else:
                reg = self.REG_MNEMONICS[tuple(self.rm)]

            mne = mne.format(register=reg,
                             displacement="{displacement}")
            if self.hasDisplacement:
                dispString = " + " + str(self.displacementSize)
                mne = mne.format(displacement=dispString,
                                 register="{register}")
            else:
                mne = mne.format(displacement="",
                                 register="{register}")

        return mne

    def getBitArray(self, num):
        bitString = bin(num)[2:]
        bits = [int(i) for i in bitString]

        return (8 - len(bits)) * [0] + bits

    def parse(self):
        pass
