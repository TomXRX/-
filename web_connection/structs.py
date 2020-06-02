import struct
def spliter(format, buffer):
    data = buffer[:struct.calcsize(format)]
    buffer = buffer[struct.calcsize(format):]
    ret = struct.unpack(format, data)
    if len(ret) == 1: ret = ret[0]
    return ret, buffer