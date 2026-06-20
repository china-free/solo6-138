import codec

MARKER_CHARS = (' ', '\t')


def read_lines(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        return f.readlines()


def write_lines(file_path: str, lines: list[str]) -> None:
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.writelines(lines)


def _split_line_endings(line: str) -> tuple[str, str]:
    cleaned = line.rstrip('\r\n')
    newline = ''
    if line.endswith('\r\n'):
        newline = '\r\n'
    elif line.endswith('\n'):
        newline = '\n'
    elif line.endswith('\r'):
        newline = '\r'
    return cleaned, newline


def _extract_trailing_whitespace(line_content: str) -> str:
    trailing = ''
    for ch in reversed(line_content):
        if ch in MARKER_CHARS:
            trailing = ch + trailing
        else:
            break
    return trailing


def distribute_bits(whitespace_payload: str, lines: list[str]) -> list[str]:
    total = len(whitespace_payload)
    num_lines = len(lines)
    if total == 0 or num_lines == 0:
        return lines.copy()
    avg = total // num_lines
    remainder = total % num_lines
    result = []
    idx = 0
    for i, line in enumerate(lines):
        count = avg + (1 if i < remainder else 0)
        chunk = whitespace_payload[idx:idx + count]
        idx += count
        cleaned, newline = _split_line_endings(line)
        result.append(cleaned + chunk + newline)
    return result


def extract_trailing_whitespace(lines: list[str]) -> str:
    collected = []
    for line in lines:
        content, _ = _split_line_endings(line)
        trailing = _extract_trailing_whitespace(content)
        collected.append(trailing)
    return ''.join(collected)


def encode_into_document(input_path: str, output_path: str, secret: str) -> None:
    lines = read_lines(input_path)
    encoded = codec.encode_message(secret)
    new_lines = distribute_bits(encoded, lines)
    write_lines(output_path, new_lines)


def decode_from_document(input_path: str) -> str:
    lines = read_lines(input_path)
    whitespace = extract_trailing_whitespace(lines)
    return codec.decode_message(whitespace)
