import argparse
import document_parser


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
        document_parser.encode_into_document(args.input, args.output, args.message)
        print(f'Success! Secret message encoded into {args.output}')
    elif args.command == 'decode':
        message = document_parser.decode_from_document(args.input)
        if message:
            print(f'Decoded message: {message}')
        else:
            print('No hidden message found.')


if __name__ == '__main__':
    main()
