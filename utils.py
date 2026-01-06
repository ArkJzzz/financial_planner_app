# utils.py
import re
from datetime import datetime


def validate_amount(amount_str: str) -> float:
    """Проверяет и преобразует строковое представление суммы в число.

    Функция нормализует входную строку, заменяя десятичные запятые на точки,
    проверяет соответствие формату числа и гарантирует, что значение положительно.

    Args:
        amount_str (str): Строка, содержащая сумму (например, "100", "100.50", "100,50").

    Returns:
        float: Сумма в виде числа с плавающей запятой.

    Raises:
        ValueError: Если входные данные не являются строкой.
        ValueError: Если строка пуста или содержит недопустимые символы.
        ValueError: Если итоговое число меньше или равно нулю.

    Examples:
        >>> validate_amount("100,50")
        100.5
        >>> validate_amount(" 50.0 ")
        50.0
    """
    if not isinstance(amount_str, str):
        raise ValueError("Сумма должна быть строкой")
    
    amount_str = amount_str.strip()
    if not amount_str:
        raise ValueError("Сумма не может быть пустой")
    
    # Заменяем запятую на точку (для русскоязычных пользователей)
    amount_str = amount_str.replace(',', '.')
    
    # Регулярное выражение: число, возможно с десятичной частью
    if not re.fullmatch(r"^\d+(\.\d+)?$", amount_str):
        raise ValueError("Неверный формат суммы. Используйте цифры и, при необходимости, точку или запятую.")
    
    amount = float(amount_str)
    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")
    return amount


def validate_date(date_str: str) -> str:
    """Проверяет корректность строкового представления даты.

    Функция выполняет комплексную проверку: на соответствие типу данных, 
    соблюдение формата ГГГГ-ММ-ДД и валидность самой календарной даты.

    Args:
        date_str (str): Строка с датой для проверки. Ожидаемый формат: 'YYYY-MM-DD'.

    Returns:
        str: Очищенная от пробелов строка даты, если все проверки пройдены успешно.

    Raises:
        ValueError: Если входной параметр не является строкой или строка пуста.
        ValueError: Если строка не соответствует шаблону ГГГГ-ММ-ДД.
        ValueError: Если указанная дата календарно не существует (например, 2026-02-30).

    Examples:
        >>> validate_date(" 2026-01-06 ")
        '2026-01-06'
        >>> validate_date("2026-13-01")
        Traceback (most recent call last):
            ...
        ValueError: Дата введена некорректно или несуществующая
    """
    if not isinstance(date_str, str):
        raise ValueError("Дата должна быть строкой")
    
    date_str = date_str.strip()
    if not date_str:
        raise ValueError("Дата не может быть пустой")
    
    # Регулярное выражение: 4 цифры, дефис, 2 цифры, дефис, 2 цифры
    if not re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД (например, 2025-12-23)")
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Дата введена некорректно или несуществующая")
    
    return date_str


def validate_category(category_str: str) -> str:
    """Проверяет корректность названия категории и очищает его.

    Функция гарантирует, что категория не является пустой и содержит только 
    допустимые символы. Строка очищается от начальных и конечных пробелов.

    Args:
        category_str (str): Название категории для проверки.

    Returns:
        str: Очищенная строка категории (без лишних пробелов по краям).

    Raises:
        ValueError: Если входной аргумент не является строкой.
        ValueError: Если после удаления пробелов строка оказалась пустой.
        ValueError: Если строка содержит спецсимволы (разрешены только буквы, 
            цифры, пробелы и дефисы).

    Examples:
        >>> validate_category(" Продукты-2026 ")
        'Продукты-2026'
        >>> validate_category("Зарплата!")
        Traceback (most recent call last):
            ...
        ValueError: Категория может содержать только буквы, цифры, пробелы и дефисы
    """
    if not isinstance(category_str, str):
        raise ValueError("Категория должна быть строкой")
    
    category_str = category_str.strip()
    if not category_str:
        raise ValueError("Категория не может быть пустой")

    # Поиск любых символов, кроме букв, цифр, пробелов и дефисов
    if re.search(r"[^а-яА-Яa-zA-Z0-9\s\-]", category_str):
        raise ValueError("Категория может содержать только буквы, цифры, пробелы и дефисы")
    
    return category_str