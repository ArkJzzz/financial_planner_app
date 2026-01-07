import datetime
import pytest
import pandas as pd
from models import Transaction
from analysis import transactions_to_df, group_by_category, plot_pie_by_category, plot_income_expence_over_time


@pytest.fixture
def sample_transactions():
    """Создает список из 5 транзакций для тестов."""
    return [
        Transaction(100.0, "Еда", "2026-01-01", "Кофе", "expense"),
        Transaction(5000.0, "Зарплата", "2026-01-05", "Аванс", "income"),
        Transaction(1500.0, "Транспорт", "2026-01-02", "Проездной", "expense"),
        Transaction(200.0, "Еда", "2026-01-04", "Обед", "expense"),
        Transaction(300.0, "Зарплата", "2026-01-06", "Бонус", "income")
    ]

@pytest.fixture
def sample_df(sample_transactions):
    """Преобразует фикстуру транзакций в DataFrame."""
    return transactions_to_df(sample_transactions)


def test_transactions_to_df(sample_transactions):
    """Проверка корректности создания DataFrame из списка объектов."""
    df = transactions_to_df(sample_transactions)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert list(df.columns) == ['amount', 'category', 'date', 'description', 'transaction_type']
    assert pd.api.types.is_datetime64_any_dtype(df['date'])

def test_group_by_category_logic(sample_df):
    """Проверка правильности группировки и суммирования."""
    # Проверяем расходы (expense): Еда (100+200) и Транспорт (1500)
    expenses = group_by_category(sample_df, "expense")
    assert expenses["Еда"] == 300.0
    assert expenses["Транспорт"] == 1500.0
    
    # Проверяем доходы (income): Зарплата (5000+300)
    income = group_by_category(sample_df, "income")
    assert income["Зарплата"] == 5300.0

def test_dataframe_types(sample_df):
    """Проверка типов колонок после преобразования."""
    assert sample_df['amount'].dtype == 'float64'
    assert sample_df['category'].dtype == 'object'
