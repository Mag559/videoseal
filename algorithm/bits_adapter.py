

BIT_COUNT: int = 256
BYTE_COUNT: int = BIT_COUNT // 8



def bytes_to_bits(bytes_list: bytearray | bytes) -> list[int]:
    bits_list = []
    for byte_idx in range(BYTE_COUNT):
        if byte_idx < len(bytes_list):
            bits_in_byte = [(bytes_list[byte_idx] >> (7 - i)) & 0b1 for i in range(8)]
            bits_list.extend(bits_in_byte)
        else:
            bits_list.extend([0 for _ in range(8)])
    return bits_list


def bits_to_bytes(bits_list: list[int]) -> bytearray:
    bytes_list: bytearray = bytearray()
    for byte_idx in range(BYTE_COUNT):
        byte: int = 0
        for i in range(8):
            byte += bits_list[byte_idx * 8 + i] << (7 - i)
        bytes_list.append(byte)
    return bytes_list


def int_to_bits(number: int) -> list[int]:
    bytes_list = number.to_bytes(BYTE_COUNT, byteorder='big')
    return bytes_to_bits(bytes_list)


def bits_to_int(bits_list: list[int]) -> int:
    return int.from_bytes(bits_to_bytes(bits_list), byteorder='big')


def str_to_bits(string: str) -> list[int]:
    bytes_list = bytearray(BYTE_COUNT)
    encoded_string = string.encode('utf-8', errors='replace')[:BYTE_COUNT]
    bytes_list[:len(encoded_string)] = encoded_string
    return bytes_to_bits(bytes_list)


def bits_to_str(bits_list: list[int]) -> str:
    bytes_list = bits_to_bytes(bits_list)
    return bytes_list.decode('utf-8', errors='replace')