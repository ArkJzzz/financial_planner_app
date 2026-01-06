import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from models import Transaction
from storage import save_transactions, load_transactions
from utils import validate_amount, validate_date, validate_category
from analysis import transactions_to_df, plot_pie_by_category, plot_income_expence_over_time


class FinancialPlannerApp:
    """Управляющий класс графического интерфейса «Финансовый Планер».

    Класс инкапсулирует логику визуализации данных через Tkinter, обработку 
    пользовательского ввода, хранение текущего состояния транзакций и вызов 
    функций аналитического анализа (Pandas/Matplotlib).

    Attributes:
        root (tk.Tk): Главное окно приложения.
        transactions (list[Transaction]): Список объектов транзакций, 
            загруженных из хранилища.
        amount_var (tk.StringVar): Буфер для ввода суммы операции.
        category_var (tk.StringVar): Буфер для ввода категории.
        date_var (tk.StringVar): Буфер для ввода даты (формат YYYY-MM-DD).
        desc_var (tk.StringVar): Буфер для ввода описания.
        type_var (tk.StringVar): Переключатель типа операции ('expense'/'income').
        tree (ttk.Treeview): Виджет таблицы для отображения истории транзакций.
    """

    def __init__(self, root):
        """Инициализирует приложение, настраивает главное окно и загружает данные.

        При создании объекта происходит автоматическая загрузка истории из 
        файла через :func:`load_transactions` и первичная отрисовка всех 
        компонентов интерфейса.

        Args:
            root (tk.Tk): Корневой объект окна Tkinter, в котором будет 
                развернуто приложение.
        """
        self.root = root
        self.root.title('Финансовый Планер')
        self.root.geometry('800x600')
        self.root.minsize(700, 500)

        # Загружаем существующие операции
        self.transactions = load_transactions()

        # Создаём виджеты
        self.create_widgets()
        self.refresh_transaction_table()

    def create_widgets(self):
        """Создает и размещает все элементы пользовательского интерфейса.

        Метод выполняет визуальную компоновку приложения, разделенную на три логических блока:
        1. Форма ввода (LabelFrame): сбор данных о сумме, категории, дате и описании.
        2. Таблица истории (Treeview): интерактивный список всех транзакций с прокруткой.
        3. Панель аналитики (LabelFrame): кнопки вызова графических отчетов.

        В процессе выполнения инициализируются связанные переменные Tkinter 
        (`amount_var`, `category_var` и др.), необходимые для реактивного 
        взаимодействия с пользователем.

        Note:
            Использует менеджеры геометрии `pack` для основных контейнеров 
            и `grid` для элементов внутри форм ввода и аналитики.
        """

        # === Верхняя панель: форма ввода ===
        input_frame = ttk.LabelFrame(self.root, text=' ➕ Новая операция ', padding=(10, 10))
        input_frame.pack(fill='x', padx=10, pady=(10, 5))

        # Сумма
        ttk.Label(input_frame, text='Сумма (RUB):').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=15)
        amount_entry.grid(row=0, column=1, sticky='w')

        # Категория
        ttk.Label(input_frame, text='Категория:').grid(row=0, column=2, sticky='w', padx=(20, 10))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(input_frame, textvariable=self.category_var, width=20)
        category_entry.grid(row=0, column=3, sticky='w')

        # Дата
        _timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        ttk.Label(input_frame, text='Дата (ГГГГ-ММ-ДД):').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.date_var = tk.StringVar(value=_timestamp)
        date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=1, column=1, sticky='w', pady=(10, 0))

        # Описание
        ttk.Label(input_frame, text='Описание:').grid(row=1, column=2, sticky='w', padx=(20, 10), pady=(10, 0))
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(input_frame, textvariable=self.desc_var, width=30)
        desc_entry.grid(row=1, column=3, sticky='w', pady=(10, 0))

        # Тип операции
        ttk.Label(input_frame, text='Тип:').grid(row=2, column=0, sticky='w', pady=(10, 0))
        self.type_var = tk.StringVar(value='expense')
        expense_rb = ttk.Radiobutton(input_frame, text='Расход', variable=self.type_var, value='expense')
        income_rb = ttk.Radiobutton(input_frame, text='Доход', variable=self.type_var, value='income')
        expense_rb.grid(row=2, column=1, sticky='w', pady=(10, 0))
        income_rb.grid(row=2, column=1, sticky='w', padx=(80, 0), pady=(10, 0))

        # Кнопка 'Добавить'
        add_btn = ttk.Button(input_frame, text=' Добавить операцию', command=self.add_transaction)
        add_btn.grid(row=3, column=0, columnspan=4, pady=(15, 0))

        # === Таблица операций ===
        table_frame = ttk.LabelFrame(self.root, text=' 📜 История операций ', padding=(10, 10))
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Создаём Treeview (таблицу)
        columns = ('type', 'amount', 'category', 'date', 'description')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        # Заголовки
        self.tree.heading('type', text='Тип')
        self.tree.heading('amount', text='Сумма (RUB)')
        self.tree.heading('category', text='Категория')
        self.tree.heading('date', text='Дата')
        self.tree.heading('description', text='Описание')

        # Ширина колонок
        self.tree.column('type', width=80, anchor='center')
        self.tree.column('amount', width=100, anchor='e')
        self.tree.column('category', width=150)
        self.tree.column('date', width=100, anchor='center')
        self.tree.column('description', width=250)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Размещение
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # === Нижняя панель: аналитика ===
        analyze_frame = ttk.LabelFrame(self.root, text=' 📊 Аналитика', padding=(10, 10))
        analyze_frame.pack(fill='x', padx=10, pady=(10, 5))

        # Кнопка 'Расходы'
        expense_btn = ttk.Button(analyze_frame, text=' Расходы', command=self.expense_dia)
        expense_btn.grid(row=0, column=0, padx=10)

        # Кнопка 'Доходы'
        income_btn = ttk.Button(analyze_frame, text=' Доходы', command=self.income_dia)
        income_btn.grid(row=0, column=1, padx=10)

        # Кнопка 'Динамика'
        trends_btn = ttk.Button(analyze_frame, text=' Динамика', command=self.cashflow_trends)
        trends_btn.grid(row=0, column=2, padx=10)


    def add_transaction(self):
        """Обрабатывает добавление новой транзакции через интерфейс.

        Метод выполняет последовательность действий:
        1. Извлекает значения из строковых переменных Tkinter (`StringVar`).
        2. Вызывает функции внешней валидации: :func:`validate_amount`, 
           :func:`validate_category` и :func:`validate_date`.
        3. При успешной проверке создает объект :class:`Transaction`.
        4. Инициирует сохранение в CSV-файл и обновляет локальный список.
        5. Перерисовывает таблицу в интерфейсе и очищает поля ввода.

        В случае любой ошибки валидации или записи процесс прерывается, 
        и пользователю выводится модальное окно с описанием проблемы.

        Raises:
            Exception: Перехватывает все исключения (ValueError, IOError и др.), 
                возникающие в процессе валидации или сохранения, и отображает 
                их через `messagebox.showerror`.
        """
        try:
            # 1. Получаем и валидируем данные
            amount = validate_amount(self.amount_var.get())
            category = validate_category(self.category_var.get())
            date = validate_date(self.date_var.get())
            description = self.desc_var.get().strip()
            trans_type = self.type_var.get()

            # 2. Создаём объект
            transaction = Transaction(
                amount=amount,
                category=category,
                date=date,
                description=description,
                transaction_type=trans_type
            )

            # 3. Сохраняем
            save_transactions([transaction])
            self.transactions.append(transaction)

            # 4. Обновляем интерфейс
            self.refresh_transaction_table()
            self.clear_input_fields()

            messagebox.showinfo('Успех', 'Операция добавлена')

        except Exception as e:
            messagebox.showerror('Ошибка ввода', f'Не удалось добавить операцию:\n{e}')

    def clear_input_fields(self):
        """Сбрасывает значения в текстовых полях формы ввода.

        Метод очищает переменные `amount_var`, `category_var` и `desc_var`, 
        что приводит к визуальному удалению текста из соответствующих 
        виджетов `ttk.Entry`.
        """
        self.amount_var.set('')
        self.category_var.set('')
        self.desc_var.set('')

    def refresh_transaction_table(self):
        """Синхронизирует виджет таблицы с актуальным списком транзакций.

        Метод полностью очищает текущие записи в графическом виджете `Treeview` 
        и заново заполняет его данными из атрибута `self.transactions`. 
        В процессе выполняется форматирование данных: преобразование типов 
        в человекочитаемый вид (например, 'income' в 'Доход') и округление сумм.

        После обновления таблицы выполняется автоматическая прокрутка к 
        последней (самой новой) записи.
        """
        # Очищаем текущие строки
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавляем все операции
        for t in self.transactions:
            row_type = 'Доход' if t.transaction_type == 'income' else 'Расход'
            self.tree.insert('', 'end', values=(
                row_type,
                f'{t.amount:.2f}',
                t.category,
                t.date,
                t.description
            ))

        # Скролл вниз (к новой операции)
        self.tree.yview_moveto(1.0)

    def expense_dia(self):
        """Обработчик события: генерирует и отображает круговую диаграмму расходов.

        Метод подготавливает данные, конвертируя текущий список транзакций 
        в формат DataFrame, и инициирует построение графика распределения 
        расходов по категориям.
        """
        df = transactions_to_df(self.transactions)

        # Круговая диаграмма расходов
        plot_pie_by_category(df, 'expense')

    def income_dia(self):
        """Обработчик события: генерирует и отображает круговую диаграмму доходов.

        Метод подготавливает данные, конвертируя текущий список транзакций 
        в формат DataFrame, и инициирует построение графика распределения 
        доходов по категориям.
        """
        df = transactions_to_df(self.transactions)

        # Круговая диаграмма доходов
        plot_pie_by_category(df, 'income')

    def cashflow_trends(self):
        """Обработчик события: формирует и отображает график динамики денежных потоков.

        Метод преобразует текущую историю транзакций в формат временного ряда 
        и визуализирует тренды доходов и расходов. Это позволяет пользователю 
        проанализировать финансовую активность в хронологическом порядке.
        """
        df = transactions_to_df(self.transactions)

        # Динамика доходов и расходов по времени
        plot_income_expence_over_time(df)


# === Точка входа для запуска GUI ===
if __name__ == '__main__':
    root = tk.Tk()
    app = FinancialPlannerApp(root)
    root.mainloop()