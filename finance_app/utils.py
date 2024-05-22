import csv
from io import BytesIO, StringIO


def int_to_money(cents: int):
    return "$" + str(cents / 100)


def make_csv_file(data: list[dict]) -> BytesIO:
    if len(data) < 1:
        return BytesIO()

    # Write dictionary to string
    with StringIO() as string_file:
        csv_writer = csv.DictWriter(string_file, data[0].keys())
        csv_writer.writerows(data)
        string_file.seek(0)
        csv_str = string_file.read()

    # Create in-memory file using csv string
    return BytesIO(csv_str.encode("utf-8"))
