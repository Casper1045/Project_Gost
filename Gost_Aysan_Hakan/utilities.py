def bytearray_to_64bits_block(byte_array):
    # Block de 64 bits | 8 bytes
    block_array = []
    offsets = [56, 48, 40, 32, 24, 16, 8, 0]
    offset_num = 0
    block64bit = 0
    for byte in byte_array:
        block64bit |= byte << offsets[offset_num]
        offset_num += 1
        if offset_num > 7:
            block_array.append(block64bit)
            block64bit = 0
            offset_num = 0

    # If the byte_array is not a multiple of 8 bits, save the last block completed by 0 bits
    if block64bit != 0:
        block_array.append(block64bit)

    return block_array


def _64bits_block_to_bytearray(blocks):
    byte_array = []
    mask = 255
    offsets = [56, 48, 40, 32, 24, 16, 8, 0]

    for block in blocks:
        for offset in offsets:
            value = block >> offset & mask
            byte_array.append(value)

    return bytearray(byte_array)


def save_to_bin(filename, byte_array):
    file = open(filename, "wb")
    file.write(byte_array)
    file.close()


def load_from_bin(filename):
    file = open(filename, "rb")
    byte = file.read()
    file.close()
    return byte


def load_txt_file(name):
    file = open(name, encoding="UTF-8")
    return file.readline()


def save_txt_file(name, txt):
    file = open(name, mode='w', encoding="UTF-8")
    file.write(txt)