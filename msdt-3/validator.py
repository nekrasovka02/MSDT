import re
import csv
import sys
from checksum import calculate_checksum, serialize_result

# ------------------------------------------------------------------
# Замените эти регулярные выражения на свои (10 штук)
# Ключи должны точно совпадать с заголовками столбцов в CSV
# ------------------------------------------------------------------

regex_patterns = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'http_status_message': r'^\d{3} [A-Za-z ]+$',
    'inn': r'^\d{12}$',
    'passport': r'^\d{2} \d{2} \d{6}$',
    'ip_v4': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    'latitude': r"^(-?(90(\.0{1,6})?|([0-9]|[1-8]\d)(\.\d{1,6})?))$",
    'hex_color': r'^#[0-9a-fA-F]{6}$',
    'isbn': r'^(?!000)\d{3}-\d-\d{5}-\d{3}-\d$|^\d-\d{5}-\d{3}-[\dX]$',
    # если учесть что isbn может (нет) начинаться с 000 
    # 'isbn': r'^\d{3}-\d-\d{5}-\d{3}-\d$|^\d-\d{5}-\d{3}-[\dX]$',
    'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    'time': r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d{1,6})?$',
}

def validate_row(row: dict) -> bool:
    for column, value in row.items():
        raw = value.strip().strip('"')
        pattern = regex_patterns.get(column)
        if not pattern or not re.fullmatch(pattern, raw):
            return False
    return True

def main(csv_filename: str) -> list:
    invalid = []
    for enc in ('utf-16', 'utf-8'):
        try:
            with open(csv_filename, 'r', encoding=enc) as f:
                sample = f.readline()
                delim = ';' if ';' in sample else ','
                f.seek(0)
                reader = csv.DictReader(f, delimiter=delim)
                for idx, row in enumerate(reader):
                    if not validate_row(row):
                        invalid.append(idx)
            return invalid
        except UnicodeDecodeError:
            continue
    raise ValueError("Не удалось прочитать файл. Проверьте кодировку (utf-8 или utf-16).")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python validator.py <csv_file>")
        sys.exit(1)

    VARIANT = 37   # замените на свой номер
    invalid_rows = main(sys.argv[1])
    checksum = calculate_checksum(invalid_rows)
    serialize_result(VARIANT, checksum)
    print(f"Invalid rows: {len(invalid_rows)}")
    print(f"Checksum: {checksum}")
    print("Result saved to result.json")