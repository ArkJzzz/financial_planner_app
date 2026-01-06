import datetime


class Transaction:
    """Класс, представляющий отдельную финансовую операцию.

    Используется для учета поступлений (income) или расходов (expense)
    денежных средств с валидацией даты и очисткой строковых данных.

    Attributes:
        amount (float): Сумма денежных средств.
        category (str): Категория операции (например, продукты, бензин, зарплата).
        date (datetime.datetime): Объект даты операции.
        description (str): Дополнительное описание транзакции.
        transaction_type (str): Тип операции ('expense' или 'income').
    """
    def __init__(
            self,
            amount: float,
            category: str,
            date: str,
            description: str = '',
            transaction_type: str = 'expense'
            ):
        """Инициализирует объект транзакции.

        Args:
            amount (float): Сумма операции.
            category (str): Категория операции. Строка очищается от пробелов.
            date (str): Дата в строковом формате 'YYYY-MM-DD'.
            description (str, optional): Описание операции. По умолчанию ''.
            transaction_type (str, optional): Тип операции: 'expense' (расход) 
                или 'income' (доход). По умолчанию 'expense'.

        Raises:
            ValueError: Если формат даты `date` не соответствует 'YYYY-MM-DD'.
        """
        self.amount = amount
        self.category = category.strip()
        # Преобразование строки в объект datetime согласно формату
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d')
        self.description = description.strip()
        self.transaction_type = transaction_type.strip()


    def to_dict(self):
        """Возвращает данные транзакции в виде словаря.

        Returns:
            dict: Словарь, содержащий ключи 'amount', 'category', 'date', 
                'description' и 'transaction_type'. 
        """
        return {
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
            'transaction_type': self.transaction_type
        }