LENGTH_HEADER_BITS = 32
ZERO_CHAR = ' '
ONE_CHAR = '\t'


def string_to_binary(text: str) -> str:
    data = text.encode('utf-8')
    return ''.join(format(byte, '08b') for byte in data)


def binary_to_string(binary: str) -> str:
    padding = len(binary) % 8
    if padding != 0:
        binary = binary[:-padding]
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    byte_array = bytearray()
    for b in chars:
        if len(b) == 8:
            byte_array.append(int(b, 2))
    return byte_array.decode('utf-8')


def binary_to_whitespace(binary: str) -> str:
    return ''.join(ONE_CHAR if bit == '1' else ZERO_CHAR for bit in binary)


def whitespace_to_binary(whitespace: str) -> str:
    return ''.join(
        '1' if ch == ONE_CHAR else '0'
        for ch in whitespace
        if ch in (ZERO_CHAR, ONE_CHAR)
    )


def encode_message(text: str) -> str:
    binary_payload = string_to_binary(text)
    length_header = format(len(binary_payload), f'0{LENGTH_HEADER_BITS}b')
    full_binary = length_header + binary_payload
    return binary_to_whitespace(full_binary)


def decode_message(whitespace: str) -> str:
    binary = whitespace_to_binary(whitespace)
    if len(binary) < LENGTH_HEADER_BITS:
        return ''
    length_bits = binary[:LENGTH_HEADER_BITS]
    payload_length = int(length_bits, 2)
    total_needed = LENGTH_HEADER_BITS + payload_length
    if len(binary) < total_needed:
        return binary_to_string(binary[LENGTH_HEADER_BITS:])
    return binary_to_string(binary[LENGTH_HEADER_BITS:total_needed])
