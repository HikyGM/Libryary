import sys
import sqlite3
from add_book import Add_book
from edit_book import Edit_book
from add_reader import Add_reader
from edit_reader import Edit_reader
from view_reader import View_reader
from add_give_books import Add_give_books
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Librarian(QMainWindow):
    def __init__(self, id_user):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/librarian_form.ui', self)  # Загружаем дизайн

        self.type_table = 0
        self.id_user = id_user

        self.book_add = Add_book(self)
        self.reader_add = Add_reader(self)

        self.books_view()
        self.client_view()
        self.journal()

        self.btn_view_reader.clicked.connect(self.view_reader)

        self.btn_search_books.clicked.connect(self.search_books)
        self.btn_search_readers.clicked.connect(self.search_reader)
        self.btn_search_journal.clicked.connect(self.search_journal)

        # self.btn_add_book.clicked.connect(self.add_book)
        self.btn_add_reader.clicked.connect(self.add_reader)
        self.btn_add_journal.clicked.connect(self.add_journal)

        # self.btn_edit_book.clicked.connect(self.edit_book)
        self.btn_edit_reader.clicked.connect(self.edit_reader)

        # self.btn_del_book.clicked.connect(self.delete_book)
        self.btn_del_reader.clicked.connect(self.delete_reader)
        self.btn_del_journal.clicked.connect(self.delete_journal)

    def search_books(self):
        self.books_view(self.line_search_books.text())

    def search_reader(self):
        self.client_view(self.line_search_readers.text())

    def search_journal(self):
        self.journal(self.line_search_journal.text())

    def books_view(self, search=''):
        self.tab_clear(self.tw_books)
        if not search:
            search = ''
        cursor = self.connection.cursor()
        res_give_book = cursor.execute(
            f"SELECT id_book "
            f"FROM readers_ticket "
        ).fetchall()
        id_give_book = [int(elem[0]) for elem in res_give_book]
        cursor = self.connection.cursor()
        books = cursor.execute(
            f"SELECT id_book, name_book, id_book, id_book, year_book, location_book, inventory_number, id_pub_house, comm_book "
            f"FROM books_in_library "
            f"WHERE name_book "
            f"LIKE '%{search}%'").fetchall()
        self.tw_books.setColumnCount(9)
        self.tw_books.setColumnHidden(0, True)
        self.tw_books.setHorizontalHeaderLabels(
            ['ID', 'Наименование', 'Авторы', 'Жанр', 'Год', 'Местоположение', 'Инвертарный номер', 'Издатель',
             'Комментарий'])
        self.tw_books.setRowCount(len(books) - len(id_give_book))
        self.tw_books.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_books.currentRow()
        self.tw_books.selectRow(row_num)
        self.tw_books.verticalHeader().setVisible(False)
        self.tw_books.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_books.verticalHeader().setDefaultSectionSize(50)
        self.tw_books.horizontalHeader().setDefaultSectionSize(150)
        self.tw_books.horizontalHeader().setDefaultSectionSize(100)
        count_rows = 0
        for i, elem in enumerate(books):
            if elem[0] in id_give_book:
                continue
            for j, val in enumerate(elem):
                if j == 2:
                    authors = cursor.execute("""
                            SELECT a.name_author 
                            FROM author_book ab, authors a
                            WHERE ab.id_author = a.id_author and ab.id_book = ?""", (val,)).fetchall()
                    self.tw_books.setItem(count_rows, j, QTableWidgetItem(", ".join([b[0] for b in authors])))
                elif j == 3:
                    genre = cursor.execute("""
                            SELECT a.name_genre
                            FROM genre_book ab, genre a
                            WHERE ab.id_genre = a.id_genre and ab.id_book = ?""", (val,)).fetchall()
                    self.tw_books.setItem(count_rows, j, QTableWidgetItem(", ".join([b[0] for b in genre])))
                elif j == 7:
                    pub_house = cursor.execute("""
                            SELECT name_pub_house
                            FROM pub_houses
                            WHERE id_pub_house = ?""", (val,)).fetchall()
                    self.tw_books.setItem(count_rows, j, QTableWidgetItem(", ".join([b[0] for b in pub_house])))
                else:
                    self.tw_books.setItem(count_rows, j, QTableWidgetItem(str(val)))
            count_rows += 1

    def journal(self, search=''):
        self.tab_clear(self.tw_journal)
        if not search:
            search = ''
        cursor = self.connection.cursor()
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

    def client_view(self, search=''):
        self.tab_clear(self.tw_readers)
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
                    reader = cursor.execute("""
                            SELECT name_group 
                            FROM groups
                            WHERE id_group = ?""", (val,)).fetchall()
                    self.tw_readers.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in reader])))
                else:
                    self.tw_readers.setItem(i, j, QTableWidgetItem(str(val)))

    def view_reader(self):
        id_reader = self.check(self.tw_readers)
        self.reader_view = View_reader(self, id_reader)
        self.reader_view.show()

    # def add_book(self):
    #     self.book_add.show()

    def add_reader(self):
        self.reader_add.show()

    def add_journal(self):
        self.give_books_add = Add_give_books(self, self.id_user)
        self.give_books_add.show()

    # def edit_book(self):
    #     id_book = self.check(self.tw_books)
    #     self.book_edit = Edit_book(self, id_book)
    #     self.book_edit.show()

    def edit_reader(self):
        id_reader = self.check(self.tw_readers)
        self.reader_edit = Edit_reader(self, id_reader)
        self.reader_edit.show()

    def edit_journal(self):
        pass

    # def delete_book(self):
    #     index_rows = list(set(i.row() for i in self.tw_books.selectedItems()))
    #     if index_rows:
    #         choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить книгу?',
    #                                       QMessageBox.Yes | QMessageBox.No)
    #         if choice == QMessageBox.Yes:
    #             for elem in index_rows:
    #                 ids = self.tw_books.item(elem, 0).text()
    #                 cursor = self.connection.cursor()
    #                 m = f'DELETE FROM books_in_library WHERE id_book = {str(ids)}'
    #                 cursor.execute(m)
    #                 self.connection.commit()
    #
    #                 n = f'DELETE FROM author_book WHERE id_book = {str(ids)}'
    #                 cursor.execute(n)
    #                 self.connection.commit()
    #
    #                 c = f'DELETE FROM genre_book WHERE id_book = {str(ids)}'
    #                 cursor.execute(c)
    #                 self.connection.commit()
    #
    #                 self.books_view()
    #         elif choice == QMessageBox.No:
    #             pass

    def delete_reader(self):
        index_rows = list(set(i.row() for i in self.tw_readers.selectedItems()))
        if index_rows:
            choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить читателя?',
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                for elem in index_rows:
                    ids = self.tw_readers.item(elem, 0).text()
                    cursor = self.connection.cursor()
                    m = f'DELETE FROM readers WHERE id_reader = {str(ids)}'
                    cursor.execute(m)
                    self.connection.commit()

                    n = f'DELETE FROM readers_ticket WHERE id_reader = {str(ids)}'
                    cursor.execute(n)
                    self.connection.commit()

                    self.client_view()
                    self.journal()
            elif choice == QMessageBox.No:
                pass

    def delete_journal(self):
        index_rows = list(set(i.row() for i in self.tw_journal.selectedItems()))
        if index_rows:
            choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить запись?',
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                for elem in index_rows:
                    ids = self.tw_journal.item(elem, 0).text()
                    cursor = self.connection.cursor()
                    m = f'DELETE FROM readers_ticket WHERE id_reader_ticket = {str(ids)}'
                    cursor.execute(m)
                    self.connection.commit()

                    self.journal()
                    self.books_view()
            elif choice == QMessageBox.No:
                pass

    def check(self, table):
        # Получение номера строки
        rows = list(set([i.row() for i in table.selectedItems()]))
        if rows:
            # Получение ID в строке (0-ой столбец)
            ids = table.item(rows[0], 0).text()
            return ids
        else:
            return False

    def tab_clear(self, table):
        # Удаление содержимого таблицы
        table.clear()
        # Удаление сетки таблицы
        table.setRowCount(0)
        table.setColumnCount(0)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Manager()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
