import sqlite3
from add_author import Add_author
from add_genre import Add_genre
from add_public_house import Add_public_house
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Edit_book(QMainWindow):
    def __init__(self, ex, id_book):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_book_form.ui', self)
        self.ex = ex
        self.id_book = id_book
        self.list_authors = []
        self.list_genre = []
        self.count_author = 0
        self.count_genre = 0
        # [0] - id [1] - название издателя
        # self.name_public_house = ''

        # объекты классов
        self.authors_view = Add_author(self)
        self.genre_view = Add_genre(self)
        self.public_house_view = Add_public_house(self)

        # заполнение форм
        cursor = self.connection.cursor()
        res = cursor.execute(
            """SELECT name_book, year_book, id_pub_house, location_book, inventory_number, comm_book 
            FROM books_in_library 
            WHERE id_book = ?""",
            (self.id_book,)).fetchall()
        all_info = res[0]
        name, year, pub_house, location, inventory_number, comm = all_info
        self.line_name.setText(str(name))
        self.line_year.setText(str(year))
        self.line_inv_numb.setText(str(inventory_number))
        self.line_way.setText(str(location))
        # добавление издателя
        res = cursor.execute(
            """SELECT id_pub_house, name_pub_house FROM pub_houses WHERE id_pub_house = ?""",
            (pub_house,)).fetchall()
        self.name_public_house = res[0]
        self.view_public_house()
        self.text_comm.setText(str(comm))
        # добавление авторов
        cursor = self.connection.cursor()
        id_author = list(
            cursor.execute(f'SELECT id_author FROM author_book WHERE id_book = {self.id_book}').fetchall())
        for i in id_author:
            rowPosition = self.table_authors.rowCount()
            self.table_authors.insertRow(rowPosition)
            cursor = self.connection.cursor()
            nb = cursor.execute(f'SELECT name_author FROM authors WHERE id_author = {i[0]}').fetchone()
            for j in nb:
                self.list_authors.append((i[0], j))
        self.view_author()
        self.cr = [self.table_authors.item(i, 0).text() for i in range(self.table_authors.rowCount())]
        # добавление жанров
        cursor = self.connection.cursor()
        id_genre = list(
            cursor.execute(f'SELECT id_genre FROM genre_book WHERE id_book = {self.id_book}').fetchall())
        for i in id_genre:
            rowPosition = self.table_genre.rowCount()
            self.table_genre.insertRow(rowPosition)
            cursor = self.connection.cursor()
            gb = cursor.execute(f'SELECT name_genre FROM genre WHERE id_genre = {i[0]}').fetchone()
            for j in gb:
                self.list_genre.append((i[0], j))
        self.view_genre()
        self.gr = [self.table_genre.item(i, 0).text() for i in range(self.table_genre.rowCount())]

        # события кнопок
        self.btn_add.clicked.connect(self.check_lines)
        self.btn_add_tab_auth.clicked.connect(self.add_authors)
        self.btn_add_tab_genre.clicked.connect(self.add_genre)
        self.btn_add_tab_public_house.clicked.connect(self.add_public_house)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_del_auth_tab.clicked.connect(self.delete_author)
        self.btn_del_genre_tab.clicked.connect(self.delete_genre)

    def view_author(self):
        self.table_authors.setColumnCount(2)
        self.table_authors.setColumnHidden(0, True)
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
            self.update()

    def add_authors(self):
        self.authors_view.show()

    def add_genre(self):
        self.genre_view.show()

    def add_public_house(self):
        self.public_house_view.show()

    def delete_author(self):
        index_rows_author = list([i.row() for i in self.table_authors.selectedItems()])
        del self.list_authors[index_rows_author[0]]
        self.view_author()

    def delete_genre(self):
        index_rows_genre = list([i.row() for i in self.table_genre.selectedItems()])
        del self.list_genre[index_rows_genre[0]]
        self.view_genre()

    def update(self):
        cursor = self.connection.cursor()
        res = f'UPDATE books_in_library ' + \
              f'SET name_book = "{self.line_name.text()}", year_book = "{self.line_year.text()}", ' + \
              f'id_pub_house= "{self.name_public_house[0]}", location_book = "{self.line_way.text()}", ' + \
              f'inventory_number = "{self.line_inv_numb.text()}", comm_book = "{self.text_comm.toPlainText()}" ' + \
              f'WHERE id_book = {self.id_book}'
        cursor.execute(res)
        self.connection.commit()

        # обновление авторов
        for i in range(len(self.cr)):
            cursor = self.connection.cursor()
            tabres = f'DELETE FROM author_book WHERE id_book = {self.id_book} AND id_author = {self.cr[i]}'
            cursor.execute(tabres)
            self.connection.commit()
        cursor = self.connection.cursor()
        ida = list(set([self.table_authors.item(i, 0).text() for i in range(self.table_authors.rowCount())]))
        for num in range(len(ida)):
            cursor.execute(f'INSERT INTO author_book(id_book, id_author) VALUES ({self.id_book}, {ida[num]})')
            self.connection.commit()

        # обновление жанров
        for i in range(len(self.gr)):
            cursor = self.connection.cursor()
            tabgen = f'DELETE FROM genre_book WHERE id_book = {self.id_book} AND id_genre = {self.gr[i]}'
            cursor.execute(tabgen)
            self.connection.commit()
        cursor = self.connection.cursor()
        idge = list(set([self.table_genre.item(i, 0).text() for i in range(self.table_genre.rowCount())]))
        for num in range(len(idge)):
            cursor.execute(f'INSERT INTO genre_book(id_book, id_genre) VALUES ({self.id_book}, {idge[num]})')
            self.connection.commit()

        # очистка всех полей после добавления
        self.list_authors = []
        self.list_genre = []
        self.name_public_house = ''
        self.tab_clear(self.table_authors)
        self.tab_clear(self.table_genre)
        self.line_pub_houses.setText(str(self.name_public_house))
        self.line_name.clear()
        self.line_year.clear()
        self.line_inv_numb.clear()
        self.line_way.clear()
        self.line_pub_houses.clear()
        self.text_comm.clear()
        self.ex.books_view()
        # закрытие формы
        self.close()
