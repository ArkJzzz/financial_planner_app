import os
import csv
import datetime
from models import Transaction


# Пути к файлам с данными
_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
_base_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_base_dir, 'data')
CSV_FILE = os.path.join(DATA_DIR, f'transactions_{_timestamp}.csv')


def ensure_data_dir():
    '''Создает директорию, если ее не существует'''
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_transaction(transactions):
    '''Сохраняет транзакции'''
    if not transactions:
        return  # Ничего не делаем

    ensure_data_dir()   # Создаем папку
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = ['amount', 'category', 'date', 'description', 'transaction_type']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for t in transactions:
                writer.writerow(t.to_dict())

    except Exception as e:
        print(f'Ошибка при сохранении данных: {e}')

def load_transactions():
    '''Выгружает транзакции из файла'''
    transactions = []
    
    if not os.path.exists(DATA_DIR):
        return transactions     # Возвращаем пустой список, если файла нет

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                t = Transaction(
                        amount=float(row['amount']),
                        category=row['category'],
                        date=row['date'],
                        description=row.get('description', ''),
                        transaction_type=row['transaction_type']
                    )
                transactions.append(t)
    
    except Exception as e:
        print(f'Ошибка при загрузке данных: {e}')
        return []

    return transactions