import sys
import argparse


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
    return ''.join('\t' if bit == '1' else ' ' for bit in binary)


def whitespace_to_binary(whitespace: str) -> str:
    return ''.join('1' if ch == '\t' else '0' for ch in whitespace if ch in (' ', '\t'))


def encode_message(text: str) -> str:
    binary = string_to_binary(text)
    length_bin = format(len(binary), '032b')
    return binary_to_whitespace(length_bin + binary)


def decode_message(whitespace: str) -> str:
    binary = whitespace_to_binary(whitespace)
    if len(binary) < 32:
        return ''
    length_bits = binary[:32]
    msg_length = int(length_bits, 2)
    if len(binary) < 32 + msg_length:
        return binary_to_string(binary[32:])
    return binary_to_string(binary[32:32 + msg_length])


def distribute_bits(bits_whitespace: str, lines: list[str]) -> list[str]:
    total = len(bits_whitespace)
    num_lines = len(lines)
    if total == 0:
        return lines.copy()
    avg = total // num_lines
    remainder = total % num_lines
    result = []
    idx = 0
    for i, line in enumerate(lines):
        count = avg + (1 if i < remainder else 0)
        chunk = bits_whitespace[idx:idx + count]
        idx += count
        cleaned = line.rstrip('\r\n')
        newline = ''
        if line.endswith('\r\n'):
            newline = '\r\n'
        elif line.endswith('\n'):
            newline = '\n'
        elif line.endswith('\r'):
            newline = '\r'
        result.append(cleaned + chunk + newline)
    return result


def extract_trailing_whitespace(lines: list[str]) -> str:
    collected = []
    for line in lines:
        stripped = line.rstrip('\r\n')
        trailing = ''
        for ch in reversed(stripped):
            if ch in (' ', '\t'):
                trailing = ch + trailing
            else:
                break
        collected.append(trailing)
    return ''.join(collected)


def encode_file(input_path: str, output_path: str, secret: str) -> None:
    with open(input_path, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()
    encoded = encode_message(secret)
    new_lines = distribute_bits(encoded, lines)
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.writelines(new_lines)


def decode_file(input_path: str) -> str:
    with open(input_path, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()
    whitespace = extract_trailing_whitespace(lines)
    return decode_message(whitespace)


def main():
    parser = argparse.ArgumentParser(
        description='Markdown Steganography - Hide messages in line-ending whitespace'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    encode_parser = subparsers.add_parser('encode', help='Encode a secret message into a Markdown file')
    encode_parser.add_argument('-i', '--input', required=True, help='Input Markdown file path')
    encode_parser.add_argument('-o', '--output', required=True, help='Output Markdown file path')
    encode_parser.add_argument('-m', '--message', required=True, help='Secret message to hide')

    decode_parser = subparsers.add_parser('decode', help='Decode a hidden message from a Markdown file')
    decode_parser.add_argument('-i', '--input', required=True, help='Input Markdown file path')

    args = parser.parse_args()

    if args.command == 'encode':
        encode_file(args.input, args.output, args.message)
        print(f'Success! Secret message encoded into {args.output}')
    elif args.command == 'decode':
        message = decode_file(args.input)
        if message:
            print(f'Decoded message: {message}')
        else:
            print('No hidden message found.')


if __name__ == '__main__':
    main()
