

class Prefix(object):
    GROUPS = [['0xF0', '0xF2', '0xF3'],
              ['0x2E', '0x36', '0x3E', '0x26', '0x64', '0x65', '0x2E', '0x3E'],
              ['0x66'],
              ['0x67']]

    def __init__(self, byte):
        self.byte = byte

    def is_prefix(byte):
        for group in self.GROUPS:
            if byte in group:
                return True
        return False
