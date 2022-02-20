import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Add_give_book(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_give_book_form.ui', self)  # Загружаем дизайн

        self.btn_add.clicked.connect(self.add_book)
        self.btn_cancel.clicked.connect(self.close)

        self.ex = ex
        self.name_book = ''

        self.view_books()

    def view_books(self, search=''):
        self.tab_clear(self.tw_books)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        genres = cursor.execute(f"SELECT id_book, name_book, location_book, inventory_number "
                                f"FROM books_in_library "
                                f"WHERE name_book "
                                f"LIKE '%{search}%'"
                                ).fetchall()
        self.tw_books.setColumnCount(4)
        # self.tw_authors.setColumnHidden(0, True)
        self.tw_books.setHorizontalHeaderLabels(
            ['ID', 'Название книги', 'Местоположение', 'N'])
        self.tw_books.setRowCount(len(genres))
        self.tw_books.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_books.currentRow()
        self.tw_books.selectRow(row_num)
        self.tw_books.verticalHeader().setVisible(False)
        self.tw_books.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_books.verticalHeader().setDefaultSectionSize(50)
        self.tw_books.horizontalHeader().setDefaultSectionSize(150)
        self.tw_books.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tw_books.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(genres):
            for j, val in enumerate(elem):
                self.tw_books.setItem(i, j, QTableWidgetItem(str(val)))

    def add_book(self):
        id_book = self.check(self.tw_books)
        self.ex.list_books.append(id_book)
        self.ex.view_books()
        self.close()

    def check(self, table):
        # Получение номера строки
        rows = list(set([i.row() for i in table.selectedItems()]))
        if rows:
            # Получение ID в строке (0-ой столбец)
            ids = table.item(rows[0], 0).text()
            names = table.item(rows[0], 1).text()
            return ids, names
        else:
            return False

    def tab_clear(self, table):
        # Удаление содержимого таблицы
        table.clear()
        # Удаление сетки таблицы
        table.setRowCount(0)
        table.setColumnCount(0)