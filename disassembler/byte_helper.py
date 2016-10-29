

def getBitArray(byte):
    if isinstance(byte, bytes):
        num = int.from_bytes(byte, byteorder='little')
    else:
        num = byte
    bitString = bin(num)[2:]
    bits = [int(i) for i in bitString]
    return (8 - len(bits))*[0] + bits
