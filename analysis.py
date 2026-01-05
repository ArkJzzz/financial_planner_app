import pandas as pd
import matplotlib.pyplot as plt

def transactions_to_df(transactions: list) -> pd.DataFrame:
    """Преобразование операций в DataFrame"""
    df = pd.DataFrame([op.to_dict() for op in transactions])
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

def group_by_category(df: pd.DataFrame, transaction_type: str) -> pd.Series:
    """Группировка по категории для заданного типа операций"""
    filtered = df[df["transaction_type"] == transaction_type]
    return filtered.groupby("category")["amount"].sum()

def plot_pie_by_category(df: pd.DataFrame, transaction_type: str):
    """Круговая диаграмма расходов или доходов"""
    data = group_by_category(df, transaction_type)
    if data.empty:
        print(f"Нет данных для {transaction_type}")
        return
    data.plot(kind="pie", autopct="%1.1f%%", figsize=(6,6), title=f"{transaction_type.capitalize()} по категориям")
    plt.ylabel("")
    plt.show()

def plot_income_expence_over_time(df: pd.DataFrame):
    """Линейный график доходов и расходов по датам"""
    if df.empty:
        print("Нет данных для графика")
        return
    df_grouped = df.groupby(["date", "transaction_type"])["amount"].sum().unstack(fill_value=0)
    df_grouped.plot(figsize=(8,5), marker="o", title="Доходы и расходы по времени")
    plt.xlabel("Дата")
    plt.ylabel("Сумма")
    plt.grid(True)
    plt.show()