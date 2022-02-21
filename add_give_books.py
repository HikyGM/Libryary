import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from datetime import datetime, timedelta
from add_give_book import Add_give_book
from add_reader_in_give import Add_reader_in_give


class Add_give_books(QMainWindow):
    def __init__(self, ex, id_user):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_give_books_form.ui', self)  # Загружаем дизайн

        self.btn_add_reader.clicked.connect(self.add_reader)
        self.btn_add_tab_books.clicked.connect(self.add_book)

        self.btn_add.clicked.connect(self.check_lines)
        self.btn_cancel.clicked.connect(self.close)

        self.ex = ex
        self.name_reader = ''
        self.list_books = []
        self.id_user = id_user

        self.give_book_add = Add_give_book(self)
        self.reader_in_give_add = Add_reader_in_give(self)

    def view_books(self):
        self.table_books.setColumnCount(2)
        self.table_books.setColumnHidden(0, True)
        self.table_books.setHorizontalHeaderLabels(
            ['ID', 'Название книги'])
        self.table_books.setRowCount(len(self.list_books))
        self.table_books.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.table_books.currentRow()
        self.table_books.selectRow(row_num)
        self.table_books.verticalHeader().setVisible(False)
        self.table_books.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_books.verticalHeader().setDefaultSectionSize(50)
        self.table_books.horizontalHeader().setDefaultSectionSize(150)
        self.table_books.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.table_books.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(self.list_books):
            for j, val in enumerate(elem):
                self.table_books.setItem(i, j, QTableWidgetItem(str(val)))

    def view_reader(self):
        self.line_reader.setText(str(self.name_reader[1]))

    def add_book(self):
        self.give_book_add.show()

    def add_reader(self):
        self.reader_in_give_add.show()

    def check_lines(self):
        if not self.line_reader.text():
            self.label_info.setText('Добавьте читателя')
        elif not self.table_books.rowCount():
            self.label_info.setText('Добавьте книгу')
        else:
            self.add()

    def add(self):
        # добавление в базу книги
        id_books = list(set([self.table_books.item(i, 0).text() for i in range(self.table_books.rowCount())]))
        for num in range(len(id_books)):
            cursor = self.connection.cursor()
            add = f'INSERT INTO readers_ticket(id_reader, id_book, id_user, date_give, date_return, return_check)' + \
                  f'VALUES ("{self.name_reader[0]}", "{id_books[num]}", ' + \
                  f'"{self.id_user}", "{datetime.now().strftime("%d.%m.%Y")}", "{(datetime.now() + timedelta(days=7)).strftime("%d.%m.%Y")}", "НЕТ")'
            cursor.execute(add)
            self.connection.commit()

        # очистка всех полей после добавления
        self.list_books = []
        self.name_reader = ''
        self.tab_clear(self.table_books)
        self.line_reader.clear()

        self.ex.journal()
        self.ex.books_view()
        # закрытие формы
        self.close()

    def cancel(self):
        # очистка всех полей после добавления
        self.list_books = []
        self.name_reader = ''
        self.tab_clear(self.table_books)
        self.line_reader.clear()

        self.ex.journal()
        # закрытие формы
        self.close()

    def tab_clear(self, table):
        # Удаление содержимого таблицы
        table.clear()
        # Удаление сетки таблицы
        table.setRowCount(0)
        table.setColumnCount(0)
