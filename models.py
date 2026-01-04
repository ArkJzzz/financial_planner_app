import datetime


class Transaction:
    '''
    Финансовая операция (поступление или расход денежных стредств)
        amount: сумма
        category: категогия (продукты, бензин, заработная плата и т.п.)
        date: дата операции
        description: описание
        transaction_type: тип операции - "expense" (расходы) или "income" (поступления)
    '''
    def __init__(
            self,
            amount: float,
            category: str,
            date: str,
            description: str = '',
            transaction_type: str = 'expense'
            ):

        if transaction_type not in ('expense', 'income'):
            raise ValueError('Тип транзакции должен быть только "expense" или "income"')

        if amount <= 0:
            raise ValueError('Сумма транзакции должна быть положительной')

        self.amount = amount
        self.category = category.strip()
        self.date = self._validate_date(date)
        self.description = description.strip()
        self.transaction_type = transaction_type.strip()

    @staticmethod
    def _validate_date(date_str: str) -> str:
        '''Принимает дату в формате YYYY-MM-DD'''
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_str # Дата соответствует шаблону
        except ValueError:
            raise ValueError('Дата записывается в формате YYYY-MM-DD')

    def to_dict(self):
        '''Возвращает транзакцию в виде словаря'''
        return {
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
            'transaction_type': self.transaction_type
        }