import sys
import sqlite3
from add_book import Add_book
from edit_book import Edit_book
# from new_auth import New_auth
# from client_add import Clients
# from give_book import Give_book
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/manager_form.ui', self)  # Загружаем дизайн

        self.id_books = []
        self.type_table = 0

        self.book_add = Add_book(self)

        self.books_view()
        self.client_view()
        self.journal()

        self.btn_add_book.clicked.connect(self.add_book)
        self.btn_add_reader.clicked.connect(self.add_reader)
        self.btn_add_journal.clicked.connect(self.add_journal)

        self.btn_edit_book.clicked.connect(self.edit_book)

        self.btn_del_book.clicked.connect(self.delete_book)

        # self.btn_del.clicked.connect(self.delete)

        # self.tw_books.itemChanged.connect(self.edit)
        # self.tw_books.itemChanged.connect(self.edit)

        # self.btn_search.clicked.connect(self.search)

    def search(self):
        if self.type_table == 0:
            self.books_view(self.input_search.text())
        elif self.type_table == 1:
            self.journal(self.input_search.text())
        elif self.type_table == 2:
            self.author_view(self.input_search.text())
        elif self.type_table == 3:
            self.client_view(self.input_search.text())

    def books_view(self, search=''):
        self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        books = cursor.execute(
            f"SELECT id_book, name_book, id_book, id_book, year_book, location_book, inventory_number, id_pub_house, comm_book "
            f"FROM books_in_library "
            f"WHERE name_book "
            f"LIKE '%{search}%'").fetchall()
        self.tw_books.setColumnCount(9)
        # скрытие столбца с ID книг
        self.tw_books.setColumnHidden(0, True)
        self.tw_books.setHorizontalHeaderLabels(
            ['ID', 'Наименование', 'Авторы', 'Жанр', 'Год', 'Местоположение', 'Инвертарный номер', 'Издатель',
             'Комментарий'])
        self.tw_books.setRowCount(len(books))
        # запрет на редактирование содержимого таблицы
        self.tw_books.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # выделение всей строки при нажатии на айтем
        self.tw_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_books.currentRow()
        self.tw_books.selectRow(row_num)
        # убираем не нужные номера строк
        self.tw_books.verticalHeader().setVisible(False)
        # установка адаптивно заполняющего размера ячеек
        self.tw_books.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по вертикали
        self.tw_books.verticalHeader().setDefaultSectionSize(50)
        # self.tw_books.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по горизонтали
        self.tw_books.horizontalHeader().setDefaultSectionSize(150)
        # фиксированный размер 3 столбца
        # self.tw_books.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        self.tw_books.horizontalHeader().setDefaultSectionSize(100)
        # фиксированный размер 3 столбца
        # self.tw_books.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        # self.tw_books.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for i, elem in enumerate(books):
            for j, val in enumerate(elem):
                if j == 2:
                    self.id_books.append(val)
                    authors = cursor.execute("""
                            SELECT a.name_author 
                            FROM author_book ab, authors a
                            WHERE ab.id_author = a.id_author and ab.id_book = ?""", (val,)).fetchall()
                    self.tw_books.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in authors])))
                elif j == 3:
                    genre = cursor.execute("""
                            SELECT a.name_genre
                            FROM genre_book ab, genre a
                            WHERE ab.id_genre = a.id_genre and ab.id_book = ?""", (val,)).fetchall()
                    self.tw_books.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in genre])))
                elif j == 7:
                    genre = cursor.execute("""
                            SELECT name_pub_house
                            FROM pub_houses
                            WHERE id_pub_house = ?""", (val,)).fetchall()
                    self.tw_books.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in genre])))
                else:
                    self.tw_books.setItem(i, j, QTableWidgetItem(str(val)))

    def tab_clear(self):
        # Удаление содержимого таблицы
        self.tw_books.clear()
        # Удаление сетки таблицы
        self.tw_books.setRowCount(0)
        self.tw_books.setColumnCount(0)

    def journal(self, search=''):
        self.type_table = 1
        # self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        # ticket = f"SELECT cb.id_clients_books, cb.id_client, cb.id_book, cb.date, cb.count_book, cb.id_book " + \
        #      f"FROM clients_books cb, clients c " + \
        #      f"WHERE cb.id_client = c.id_client AND c.name_client " + \
        #      f"LIKE '%{search}%'"
        ticket = f"SELECT rt.id_reader_ticket, rt.id_reader, rt.id_book, rt.id_user, rt.date_give, rt.date_return, rt.return_check " + \
                 f"FROM readers_ticket rt, readers r " + \
                 f"WHERE rt.id_reader = r.id_reader AND r.name_reader " + \
                 f"LIKE '%{search}%'"
        journal = cursor.execute(ticket).fetchall()
        self.tw_journal.setColumnCount(7)
        self.tw_journal.setColumnHidden(0, True)
        # self.tw_journal.setColumnHidden(5, True)
        self.tw_journal.setHorizontalHeaderLabels(
            ['ID', 'Читатель', 'Книга', 'Выдал', 'Дата выдачи', 'Дата возврата', 'Возвращена'])
        self.tw_journal.setRowCount(len(journal))
        self.tw_journal.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_journal.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_journal.currentRow()
        self.tw_journal.selectRow(row_num)
        self.tw_journal.verticalHeader().setVisible(False)
        self.tw_journal.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_journal.verticalHeader().setDefaultSectionSize(50)
        for i, elem in enumerate(journal):
            for j, val in enumerate(elem):
                if j == 1:
                    self.id_books.append(val)
                    reader = cursor.execute("""
                            SELECT name_reader
                            FROM readers
                            WHERE id_reader = ?""", (val,)).fetchall()
                    self.tw_journal.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in reader])))
                elif j == 2:
                    book = cursor.execute("""
                            SELECT name_book
                            FROM books_in_library
                            WHERE id_book = ?""", (val,)).fetchall()
                    self.tw_journal.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in book])))
                elif j == 3:
                    user = cursor.execute("""
                            SELECT name_user
                            FROM users
                            WHERE id_user = ?""", (val,)).fetchall()
                    self.tw_journal.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in user])))
                else:
                    self.tw_journal.setItem(i, j, QTableWidgetItem(str(val)))

    def author_view(self, search=''):
        self.type_table = 2
        # self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        auth = cursor.execute(f"SELECT id_author, name_author "
                              f"FROM authors "
                              f"WHERE name_author "
                              f"LIKE '%{search}%'").fetchall()
        self.tw_books.setColumnCount(2)
        self.tw_books.setColumnHidden(0, True)
        self.tw_books.setHorizontalHeaderLabels(
            ['ID', 'Авторы'])
        self.tw_books.setRowCount(len(auth))
        self.tw_books.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_books.currentRow()
        self.tw_books.selectRow(row_num)
        self.tw_books.verticalHeader().setVisible(False)
        self.tw_books.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_books.verticalHeader().setDefaultSectionSize(70)
        for i, elem in enumerate(auth):
            for j, val in enumerate(elem):
                self.tw_books.setItem(i, j, QTableWidgetItem(str(val)))

    def client_view(self, search=''):
        self.type_table = 3
        # self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        auth = cursor.execute(f"SELECT id_reader, name_reader, id_group, phone_reader, address_reader "
                              f"FROM readers "
                              f"WHERE name_reader "
                              f"LIKE '%{search}%'"
                              ).fetchall()
        self.tw_readers.setColumnCount(5)
        self.tw_readers.setColumnHidden(0, True)
        self.tw_readers.setHorizontalHeaderLabels(
            ['ID', 'ФИО', 'Группа', 'Номер', 'Адрес'])
        self.tw_readers.setRowCount(len(auth))
        self.tw_readers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_readers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_readers.currentRow()
        self.tw_readers.selectRow(row_num)
        self.tw_readers.verticalHeader().setVisible(False)
        self.tw_readers.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_readers.verticalHeader().setDefaultSectionSize(50)
        for i, elem in enumerate(auth):
            for j, val in enumerate(elem):
                if j == 2:
                    self.id_books.append(val)
                    reader = cursor.execute("""
                            SELECT name_group 
                            FROM groups
                            WHERE id_group = ?""", (val,)).fetchall()
                    self.tw_readers.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in reader])))
                else:
                    self.tw_readers.setItem(i, j, QTableWidgetItem(str(val)))

    def add_book(self):
        self.book_add.show()

    def add_reader(self):
        pass

    def add_journal(self):
        pass

    def edit_book(self):
        id_book = self.check()
        self.book_edit = Edit_book(self, id_book)
        self.book_edit.show()

    def delete_book(self):
        index_rows = list(set(i.row() for i in self.tw_books.selectedItems()))
        if index_rows:
            choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить книгу?',
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                for elem in index_rows:
                    ids = self.tw_books.item(elem, 0).text()
                    cursor = self.connection.cursor()
                    m = f'DELETE FROM books_in_library WHERE id_book = {str(ids)}'
                    cursor.execute(m)
                    self.connection.commit()

                    n = f'DELETE FROM author_book WHERE id_book = {str(ids)}'
                    cursor.execute(n)
                    self.connection.commit()

                    c = f'DELETE FROM genre_book WHERE id_book = {str(ids)}'
                    cursor.execute(c)
                    self.connection.commit()

                    self.books_view()
            elif choice == QMessageBox.No:
                pass

    def check(self):
        # Получение номера строки
        rows = list(set([i.row() for i in self.tw_books.selectedItems()]))
        if rows:
            # Получение ID в строке (0-ой столбец)
            ids = self.tw_books.item(rows[0], 0).text()
            return ids
        else:
            return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Manager()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
