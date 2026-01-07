import datetime
from models import Transaction


def test_to_dict():
    test_tr = Transaction(
        amount=500,
        category='Кафе',
        date='2026-01-05',
        description='Кофе и пирожное',
        transaction_type='expense'
    )
    tr_dict = test_tr.to_dict()
    assert tr_dict['amount'] == 500.0
    assert tr_dict['category'] == 'Кафе'
    assert tr_dict['date'] == datetime.datetime.strptime('2026-01-05', '%Y-%m-%d')
    assert tr_dict['description'] == 'Кофе и пирожное'
    assert tr_dict['transaction_type'] == 'expense'