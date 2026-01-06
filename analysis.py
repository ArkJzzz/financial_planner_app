import pandas as pd
import matplotlib.pyplot as plt

def transactions_to_df(transactions: list) -> pd.DataFrame:
    """Преобразует список объектов транзакций в объект pandas DataFrame.

    Функция собирает данные из объектов транзакций и выполняет постобработку:
    преобразует строковые даты в объекты `datetime64`, что позволяет в дальнейшем
    проводить временной анализ (группировку по месяцам, расчет трендов и т.д.).

    Args:
        transactions (list[Transaction]): Список экземпляров класса :class:`Transaction`.

    Returns:
        pd.DataFrame: Таблица данных с колонками, соответствующими полям транзакции.
        Если список пуст, возвращается пустой DataFrame. Колонки результата:
        'amount', 'category', 'date', 'description', 'transaction_type'.

    Note:
        Столбец 'date' автоматически конвертируется в формат :obj:`pandas.Timestamp`
        только в том случае, если DataFrame не пуст.

    Example:
        >>> transactions = [Transaction(100.0, "Еда", "2026-01-06")]
        >>> df = transactions_to_df(transactions)
        >>> print(df['date'].dtype)
        datetime64[ns]
    """
    df = pd.DataFrame([tr.to_dict() for tr in transactions])
    if not df.empty:
        # Приведение к формату datetime для корректной работы с временными рядами
        df["date"] = pd.to_datetime(df["date"])
    return df

def group_by_category(df: pd.DataFrame, transaction_type: str) -> pd.Series:
    """Группирует данные по категориям и вычисляет суммарный объем средств.

    Функция фильтрует входной DataFrame по указанному типу транзакций (доход или расход)
    и суммирует значения в столбце 'amount' для каждой уникальной категории.

    Args:
        df (pd.DataFrame): Таблица данных, содержащая столбцы 'transaction_type', 
            'category' и 'amount'.
        transaction_type (str): Тип операции для фильтрации (например, 'expense' 
            или 'income').

    Returns:
        pd.Series: Объект Series, где индексами являются названия категорий, 
        а значениями — общие суммы по каждой категории.

    Example:
        >>> # Получение суммы расходов по категориям
        >>> expenses_by_cat = group_by_category(df, 'expense')
        >>> print(expenses_by_cat['Еда'])
        5000.0
    """
    filtered = df[df["transaction_type"] == transaction_type]
    return filtered.groupby("category")["amount"].sum()

def plot_pie_by_category(df: pd.DataFrame, transaction_type: str):
    """Строит круговую диаграмму распределения финансов по категориям.

    Функция агрегирует данные для выбранного типа операций (доходы или расходы)
    и визуализирует процентное соотношение каждой категории в общем объеме.
    Если данные для указанного типа отсутствуют, график не строится.

    Args:
        df (pd.DataFrame): Таблица данных, содержащая как минимум колонки 
            'transaction_type', 'category' и 'amount'.
        transaction_type (str): Тип операций для отображения: 'expense' (расходы) 
            или 'income' (доходы).

    Note:
        - Функция использует метод `plt.show()` для отображения графика, что 
          может блокировать выполнение кода в зависимости от настроек бэкенда Matplotlib.
        - Для корректного отображения меток категорий на русском языке убедитесь, 
          что в Matplotlib настроены шрифты с поддержкой кириллицы.

    Returns:
        None: Функция отображает интерактивное окно с графиком через `plt.show()`.
    """
    data = group_by_category(df, transaction_type)
    if data.empty:
        print(f"Нет данных для {transaction_type}")
        return

    # Построение диаграммы с настройками размера и отображением процентов
    data.plot(
            kind="pie", 
            autopct="%1.1f%%", 
            figsize=(6,6), 
            title=f"{transaction_type.capitalize()} по категориям"
        )
    plt.ylabel("") # Скрываем стандартную подпись оси Y (название Series)
    plt.show()

def plot_income_expence_over_time(df: pd.DataFrame):
    """Визуализирует динамику доходов и расходов во времени.

    Функция группирует транзакции по датам и типам, вычисляет ежедневные суммы
    и строит линейный график. Позволяет наглядно сравнить притоки и оттоки
    денежных средств на временной шкале.

    Args:
        df (pd.DataFrame): Таблица данных. Должна содержать колонки 'date',
            'transaction_type' и 'amount'. Колонка 'date' должна иметь
            тип datetime64.

    Note:
        - Если в определенную дату отсутствует один из типов операций (например, 
          только расходы), функция подставит 0 для корректного отображения графика.
        - Для корректной работы функции рекомендуется предварительно обработать 
          DataFrame функцией :func:`transactions_to_df`.

    Returns:
        None: Функция отображает интерактивное окно с графиком через `plt.show()`.

    Raises:
        KeyError: Если в DataFrame отсутствуют необходимые колонки.
    """
    if df.empty:
        print("Нет данных для графика")
        return
    # Группировка по дате и типу, затем разворачивание типов в отдельные колонки
    df_grouped = df.groupby(["date", "transaction_type"])["amount"].sum().unstack(fill_value=0)
    # Построение графика с маркерами на каждой точке данных
    df_grouped.plot(
            figsize=(8,5), 
            marker="o", 
            title="Доходы и расходы по времени"
        )
    plt.xlabel("Дата")
    plt.ylabel("Сумма")
    plt.grid(True)
    plt.show()