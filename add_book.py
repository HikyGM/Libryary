import sqlite3
from add_author import Add_author
from add_genre import Add_genre
from add_public_house import Add_public_house
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Add_book(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_book_form.ui', self)
        self.ex = ex
        self.list_authors = []
        self.list_genre = []

        # [0] - id [1] - название издателя
        self.name_public_house = ''

        # объекты классов
        self.authors_view = Add_author(self)
        self.genre_view = Add_genre(self)
        self.public_house_view = Add_public_house(self)

        # события кнопок
        self.btn_add.clicked.connect(self.check_lines)
        self.btn_add_tab_auth.clicked.connect(self.add_authors)
        self.btn_add_tab_genre.clicked.connect(self.add_genre)
        self.btn_add_tab_public_house.clicked.connect(self.add_public_house)
        self.btn_cancel.clicked.connect(self.cancel)

    def view_author(self):
        self.table_authors.setColumnCount(2)
        # self.tw_authors.setColumnHidden(0, True)
        self.table_authors.setHorizontalHeaderLabels(
            ['ID', 'Автор'])
        self.table_authors.setRowCount(len(self.list_authors))
        self.table_authors.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_authors.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.table_authors.currentRow()
        self.table_authors.selectRow(row_num)
        self.table_authors.verticalHeader().setVisible(False)
        self.table_authors.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_authors.verticalHeader().setDefaultSectionSize(50)
        self.table_authors.horizontalHeader().setDefaultSectionSize(150)
        self.table_authors.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.table_authors.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(self.list_authors):
            for j, val in enumerate(elem):
                self.table_authors.setItem(i, j, QTableWidgetItem(str(val)))

    def view_genre(self):
        self.table_genre.setColumnCount(2)
        # self.tw_authors.setColumnHidden(0, True)
        self.table_genre.setHorizontalHeaderLabels(
            ['ID', 'Автор'])
        self.table_genre.setRowCount(len(self.list_genre))
        self.table_genre.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_genre.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.table_genre.currentRow()
        self.table_genre.selectRow(row_num)
        self.table_genre.verticalHeader().setVisible(False)
        self.table_genre.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_genre.verticalHeader().setDefaultSectionSize(50)
        self.table_genre.horizontalHeader().setDefaultSectionSize(150)
        self.table_genre.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.table_genre.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(self.list_genre):
            for j, val in enumerate(elem):
                self.table_genre.setItem(i, j, QTableWidgetItem(str(val)))

    def view_public_house(self):
        self.line_pub_houses.setText(str(self.name_public_house[1]))

    def cancel(self):
        self.list_authors = []
        self.list_genre = []
        self.name_public_house = ''
        self.tab_clear(self.table_authors)
        self.tab_clear(self.table_genre)
        self.line_pub_houses.clear()
        self.close()

    def tab_clear(self, table):
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(0)

    def check_lines(self):
        if not self.line_name.text():
            self.label_info.setText('Заполните название')
        elif not self.line_year.text():
            self.label_info.setText('Заполните год')
        elif not self.line_inv_numb.text():
            self.label_info.setText('Заполните инвертарный номер')
        elif not self.line_way.text():
            self.label_info.setText('Заполните местоположение')
        elif not self.line_pub_houses.text():
            self.label_info.setText('Заполните издателя')
        elif not self.table_authors.rowCount():
            self.label_info.setText('Добавьте автора книги')
        elif not self.table_genre.rowCount():
            self.label_info.setText('Добавьте автора книги')
        else:
            self.add()

    def add_authors(self):
        self.authors_view.show()

    def add_genre(self):
        self.genre_view.show()

    def add_public_house(self):
        self.public_house_view.show()

    def add(self):
        # добавление в базу книги
        cursor = self.connection.cursor()
        add = f'INSERT INTO books_in_library(name_book, year_book, id_pub_house, location_book, inventory_number, comm_book)' + \
              f'VALUES ("{self.line_name.text()}", "{self.line_year.text()}", ' + \
              f'"{self.name_public_house[0]}", "{self.line_way.text()}", "{self.line_inv_numb.text()}", ' \
              f'"{self.text_comm.toPlainText()}")'
        cursor.execute(add)
        self.connection.commit()

        # добавление в базу авторов книги
        cursor = self.connection.cursor()
        ids = cursor.execute(f'SELECT id_book FROM books_in_library ORDER BY id_book DESC LIMIT 1').fetchone()
        id_authors = list(set([self.table_authors.item(i, 0).text() for i in range(self.table_authors.rowCount())]))
        for num in range(len(id_authors)):
            cursor.execute(f'INSERT INTO author_book(id_author, id_book) VALUES ({id_authors[num]}, {ids[0]})')
            self.connection.commit()

        # добавление в базу жанров книги
        cursor = self.connection.cursor()
        id_genres = list(set([self.table_genre.item(i, 0).text() for i in range(self.table_genre.rowCount())]))
        for num in range(len(id_genres)):
            cursor.execute(f'INSERT INTO genre_book(id_genre, id_book) VALUES ({id_genres[num]}, {ids[0]})')
            self.connection.commit()

        # очистка всех полей после добавления
        self.list_authors = []
        self.list_genre = []
        self.name_public_house = ''
        self.tab_clear(self.table_authors)
        self.tab_clear(self.table_genre)
        self.line_pub_houses.setText(str(self.name_public_house))
        self.ex.books_view()
        self.line_name.clear()
        self.line_year.clear()
        self.line_inv_numb.clear()
        self.line_way.clear()
        self.line_pub_houses.clear()
        self.text_comm.clear()
        # закрытие формы
        self.close()
