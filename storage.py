import os
import csv
import datetime
import pandas as pd
from models import Transaction


# Пути к файлам с данными
_base_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_base_dir, 'data')
CSV_FILE = os.path.join(DATA_DIR, f'transactions.csv')


def ensure_data_dir():
    """Проверяет наличие директории для хранения данных и создает её при отсутствии.

    Функция использует путь, указанный в глобальной переменной `DATA_DIR`. 
    Если целевая папка (и все промежуточные директории) отсутствует в файловой 
    системе, она будет создана автоматически.

    Note:
        Функция опирается на внешнюю константу `DATA_DIR`, которая должна быть 
        определена в модуле.

    Raises:
        OSError: Если создание директории невозможно из-за ограничений прав 
            доступа или системных ошибок.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_transactions(transactions):
    """Сохраняет список транзакций в CSV-файл.

    Функция выполняет дозапись (append) данных в файл. 
    Если файл не существует, он создается вместе с заголовками столбцов. 
    При пустом входном списке запись не производится.

    Args:
        transactions (list[Transaction]): Список объектов транзакций для сохранения.
            Каждый объект должен иметь метод `to_dict()`.

    Note:
        - Использует глобальную константу `CSV_FILE` для определения пути к файлу.
        - Автоматически вызывает `ensure_data_dir()` перед началом записи.
        - Данные сохраняются в кодировке UTF-8.

    Raises:
        Exception: Если возникает ошибка при открытии файла или процессе записи 
            (ошибка перехватывается внутри функции и выводится в консоль).

    Example:
        >>> tx = Transaction(100.0, "Еда", "2026-01-06", "Хлеб", "expense")
        >>> save_transactions([tx])
    """
    if not transactions:
        return  # Ничего не делаем

    ensure_data_dir()   # Создаем папку
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = ['amount', 'category', 'date', 'description', 'transaction_type']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Если файл новый, записываем заголовки
            if not file_exists:
                writer.writeheader()

            for t in transactions:
                writer.writerow(t.to_dict())

    except Exception as e:
        print(f'Ошибка при сохранении данных: {e}')

def load_transactions():
    """Загружает список транзакций из CSV-файла и преобразует их в объекты Transaction.

    Функция считывает данные из хранилища, выполняет десериализацию каждой строки 
    и восстанавливает объекты класса :class:`Transaction`. Если директория данных 
    или сам файл отсутствуют, возвращается пустой список.

    Returns:
        list[Transaction]: Список восстановленных объектов транзакций. 
        В случае отсутствия файла или возникновения ошибки чтения возвращается 
        пустой список `[]`.

    Note:
        - Опирается на глобальные константы `DATA_DIR` и `CSV_FILE`.
        - Предполагает, что CSV-файл имеет корректные заголовки: 
          'amount', 'category', 'date', 'description', 'transaction_type'.

    Raises:
        Exception: Если возникает ошибка при чтении файла или парсинге данных 
            (например, поврежден формат CSV). Ошибка перехватывается, выводится 
            в консоль, и функция возвращает пустой список.
    """
    transactions = []
    
    if not os.path.exists(DATA_DIR):
        return transactions     # Возвращаем пустой список, если файла нет

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Создаем объект Transaction, преобразуя данные из строк
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

