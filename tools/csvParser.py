import csv

path = 'data/sample.csv'

def get_csv_data(path: str) -> str:
    # Try utf-8, fallback to latin1 if needed
    try:
        with open(path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = ""
            for row in reader:
                data += str(row) + "\n"
            return data
    except UnicodeDecodeError:
        with open(path, mode='r', encoding='latin1') as file:
            reader = csv.DictReader(file)
            data = ""
            for row in reader:
                data += str(row) + "\n"
            return data
