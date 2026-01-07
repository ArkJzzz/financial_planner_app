import pytest
from utils import validate_amount, validate_date, validate_category


def test_validate_amount_valid_amounts():
    """Успешная валидация корректных значений."""
    assert validate_amount("100") == 100.0
    assert validate_amount("100.50") == 100.50
    assert validate_amount("123456.789") == 123456.789
    assert validate_amount("100,50") == 100.50  # Запятая как разделитель
    assert validate_amount("  100.50  ") == 100.50  # Пробельные символы

def test_validate_amount_wrong_type():
    """Ошибка, если передана не строка (например, число или None)."""
    with pytest.raises(ValueError, match="Сумма должна быть строкой"):
        validate_amount(100)
    with pytest.raises(ValueError, match="Сумма должна быть строкой"):
        validate_amount(100.50)

def test_validate_amount_empty():
    """Ошибка на пустые строки."""
    with pytest.raises(ValueError, match="Сумма не может быть пустой"):
        validate_amount("")
    with pytest.raises(ValueError, match="Сумма не может быть пустой"):
        validate_amount("   ")
    with pytest.raises(ValueError, match="Сумма не может быть пустой"):
        validate_amount("\t\n")
    with pytest.raises(ValueError, match="Сумма должна быть строкой"):
        validate_amount(None)

def test_validate_amount_invalid_characters():
    """Ошибка при наличии букв или спецсимволов."""
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("100abc")
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("100$")
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("100.50.20")  # Две точки
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("abc123")

def test_validate_amount_negative_or_zero():
    """Ошибка при отрицательных значениях или нуле."""
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("-100")
    with pytest.raises(ValueError, match="Сумма должна быть больше нуля"):
        validate_amount("0")
    with pytest.raises(ValueError, match="Сумма должна быть больше нуля"):
        validate_amount("0.0")
    with pytest.raises(ValueError, match="Сумма должна быть строкой"):
        validate_amount(0)

def test_validate_amount_edge_cases():
    """Тесты граничных случаев."""
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount(".50")  # Начинается с точки
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("50.")  # Заканчивается на точку
    with pytest.raises(ValueError, match="Неверный формат суммы"):
        validate_amount("..50")  # Две точки подряд

def test_validate_date_valid_dates():
    """Успешная валидация корректных дат."""
    assert validate_date("2026-01-06") == "2026-01-06"
    assert validate_date("2026-12-31") == "2026-12-31"
    assert validate_date("2026-07-15") == "2026-07-15"
    assert validate_date("2026-02-28") == "2026-02-28"  # Обычный февраль
    assert validate_date(" 2026-01-06 ") == "2026-01-06"  # Пробельные символы

def test_validate_date_leap_years():
    """Тесты високосных лет."""
    # Високосные годы: делятся на 4, но не на 100, или делятся на 400
    assert validate_date("2026-02-28") == "2026-02-28"  # Не високосный
    assert validate_date("2024-02-29") == "2024-02-29"  # Високосный
    assert validate_date("2000-02-29") == "2000-02-29"  # Високосный
    assert validate_date("2028-02-29") == "2028-02-29"  # Високосный
    assert validate_date("1600-02-29") == "1600-02-29"  # Високосный

def test_validate_date_month_boundaries():
    """Тесты граничных значений месяцев."""
    # Январь
    assert validate_date("2026-01-01") == "2026-01-01"
    assert validate_date("2026-01-31") == "2026-01-31"
    
    # Февраль (обычный год)
    assert validate_date("2026-02-01") == "2026-02-01"
    assert validate_date("2026-02-28") == "2026-02-28"
    
    # Март
    assert validate_date("2026-03-01") == "2026-03-01"
    assert validate_date("2026-03-31") == "2026-03-31"
    
    # Апрель
    assert validate_date("2026-04-01") == "2026-04-01"
    assert validate_date("2026-04-30") == "2026-04-30"
    
    # Май
    assert validate_date("2026-05-01") == "2026-05-01"
    assert validate_date("2026-05-31") == "2026-05-31"
    
    # Июнь
    assert validate_date("2026-06-01") == "2026-06-01"
    assert validate_date("2026-06-30") == "2026-06-30"
    
    # Июль
    assert validate_date("2026-07-01") == "2026-07-01"
    assert validate_date("2026-07-31") == "2026-07-31"
    
    # Август
    assert validate_date("2026-08-01") == "2026-08-01"
    assert validate_date("2026-08-31") == "2026-08-31"
    
    # Сентябрь
    assert validate_date("2026-09-01") == "2026-09-01"
    assert validate_date("2026-09-30") == "2026-09-30"
    
    # Октябрь
    assert validate_date("2026-10-01") == "2026-10-01"
    assert validate_date("2026-10-31") == "2026-10-31"
    
    # Ноябрь
    assert validate_date("2026-11-01") == "2026-11-01"
    assert validate_date("2026-11-30") == "2026-11-30"
    
    # Декабрь
    assert validate_date("2026-12-01") == "2026-12-01"
    assert validate_date("2026-12-31") == "2026-12-31"

def test_validate_date_wrong_type():
    """Ошибка, если передана не строка (например, число или None)."""
    with pytest.raises(ValueError, match="Дата должна быть строкой"):
        validate_date(2026)
    with pytest.raises(ValueError, match="Дата должна быть строкой"):
        validate_date(None)
    with pytest.raises(ValueError, match="Дата должна быть строкой"):
        validate_date([])

def test_validate_date_edge_cases():
    """Тесты граничных случаев."""
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-02-29")  # Не високосный год
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("1900-02-29")  # 1900 не високосный год (делится на 100, но не на 4)

def test_validate_date_empty():
    """Ошибка на пустые строки."""
    with pytest.raises(ValueError, match="Дата не может быть пустой"):
        validate_date("")
    with pytest.raises(ValueError, match="Дата не может быть пустой"):
        validate_date("   ")
    with pytest.raises(ValueError, match="Дата не может быть пустой"):
        validate_date("\t\n")
    with pytest.raises(ValueError, match="Дата не может быть пустой"):
        validate_date(" \t \n ")

def test_validate_date_invalid_format():
    """Ошибка при неверном формате даты."""
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("2026/01/06")
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("26-01-06")
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("2026.01.06")
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("2026-1-06")
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("2026-01-6")
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("2026--01-06")
    with pytest.raises(ValueError, match="Дата должна быть в формате ГГГГ-ММ-ДД"):
        validate_date("2026-01-06-01")

def test_validate_date_invalid_dates():
    """Ошибка при несуществующих датах."""
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-02-30")  # Февраль не имеет 30 дней
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-04-31")  # Апрель не имеет 31 дня
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-13-01")  # Месяц 13 не существует
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-00-01")  # Месяц 0 не существует
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-01-00")  # День 0 не существует
    with pytest.raises(ValueError, match="Дата введена некорректно или несуществующая"):
        validate_date("2026-12-32")  # Декабрь не имеет 32 дней


def test_validate_category_valid_characters():
    """Успешная валидация допустимых символов."""
    assert validate_category("Продукты") == "Продукты"
    assert validate_category("Зарплата-2026") == "Зарплата-2026"
    assert validate_category("Категория 123") == "Категория 123"
    assert validate_category("Категория-123") == "Категория-123"
    assert validate_category("Категория-123-456") == "Категория-123-456"
    assert validate_category("Категория 123 456") == "Категория 123 456"
    assert validate_category("  Продукты 2026  ") == "Продукты 2026"

def test_validate_category_mixed_case():
    """Тесты с разным регистром."""
    assert validate_category("продукты") == "продукты"
    assert validate_category("ПРОДУКТЫ") == "ПРОДУКТЫ"
    assert validate_category("ПродУкТы") == "ПродУкТы"

def test_validate_category_numbers():
    """Тесты с числами."""
    assert validate_category("123") == "123"
    assert validate_category("Категория123") == "Категория123"
    assert validate_category("Категория-123") == "Категория-123"
    assert validate_category("123-456") == "123-456"

def test_validate_category_wrong_type():
    """Ошибка, если передана не строка (например, число или None)."""
    with pytest.raises(ValueError, match="Категория должна быть строкой"):
        validate_category(123)
    with pytest.raises(ValueError, match="Категория должна быть строкой"):
        validate_category(None)
    with pytest.raises(ValueError, match="Категория должна быть строкой"):
        validate_category([])

def test_validate_category_empty_or_whitespace():
    """Ошибка на пустые строки."""
    with pytest.raises(ValueError, match="Категория не может быть пустой"):
        validate_category("")
    with pytest.raises(ValueError, match="Категория не может быть пустой"):
        validate_category("   ")
    with pytest.raises(ValueError, match="Категория не может быть пустой"):
        validate_category("\t\n")
    with pytest.raises(ValueError, match="Категория не может быть пустой"):
        validate_category(" \t \n ")

def test_validate_category_invalid_characters():
    """Ошибка при наличии недопустимых символов."""
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Продукты!")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Зарплата@")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория#123")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория$")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория%")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория&")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория*")
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория_123")  # Подчеркивание не разрешено
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория.123")  # Точка не разрешена
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория,123")  # Запятая не разрешена
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория;123")  # Точка с запятой не разрешена
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория:123")  # Двоеточие не разрешено
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория?123")  # Вопросительный знак не разрешен
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория/123")  # Слэш не разрешен
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория\\123")  # Обратный слэш не разрешен
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория\"123")  # Кавычки не разрешены
    with pytest.raises(ValueError, match="Категория может содержать только буквы, цифры, пробелы и дефисы"):
        validate_category("Категория'123")  # Апостроф не разрешен
