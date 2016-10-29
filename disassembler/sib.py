from byte_helper import getBitArray


class Sib(object):

    def __init__(self, byte):
        self.byte = byte

        bits = getBitArray(byte)
        self.scale = bits[:2]
        self.index = bits[2:5]
        self.base  = bits[5:]
