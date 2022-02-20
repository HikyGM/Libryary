import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class View_reader(QMainWindow):
    def __init__(self, ex, id_reader):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/view_reader_form.ui', self)  # Загружаем дизайн

        self.ex = ex
        self.id_reader = id_reader
        self.name_group = ''
        self.btn_cancel.clicked.connect(self.close)

        # заполнение форм
        cursor = self.connection.cursor()
        res = cursor.execute(
            """SELECT name_reader, address_reader, phone_reader, id_group, year_reader 
            FROM readers 
            WHERE id_reader = ?""",
            (self.id_reader,)).fetchall()
        all_info = res[0]
        name, address, phone, group, year = all_info

        self.label_name.setText(str(name))
        self.label_address.setText(str(address))
        self.label_phone.setText(str(phone))
        self.label_year.setText(str(year))

        # добавление группы
        res = cursor.execute(
            """SELECT id_group, name_group FROM groups WHERE id_group = ?""",
            (group,)).fetchall()
        self.name_group = res[0]

        self.label_group.setText(str(self.name_group[1]))

        cursor = self.connection.cursor()
        books = cursor.execute(
            """SELECT id_book, date_give, return_check 
            FROM readers_ticket 
            WHERE id_reader = ?""",
            (self.id_reader,)).fetchall()
        self.tw_view_books.setColumnCount(3)
        self.tw_view_books.setHorizontalHeaderLabels(
            ['Книга', 'Дата выдачи', 'Возврат'])
        self.tw_view_books.setRowCount(len(books))
        self.tw_view_books.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_view_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_view_books.currentRow()
        self.tw_view_books.selectRow(row_num)
        self.tw_view_books.verticalHeader().setVisible(False)
        self.tw_view_books.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_view_books.verticalHeader().setDefaultSectionSize(50)
        self.tw_view_books.horizontalHeader().setDefaultSectionSize(150)
        self.tw_view_books.horizontalHeader().setDefaultSectionSize(100)
        for i, elem in enumerate(books):
            for j, val in enumerate(elem):
                if j == 0:
                    authors = cursor.execute("""
                                    SELECT name_book 
                                    FROM books_in_library
                                    WHERE id_book = ?""", (val,)).fetchall()
                    self.tw_view_books.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in authors])))
                else:
                    self.tw_view_books.setItem(i, j, QTableWidgetItem(str(val)))
