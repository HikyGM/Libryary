import sys
import sqlite3
from add_user import Add_user
from add_group import Add_group
from edit_user import Edit_user
from edit_group import Edit_group
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/admin_form.ui', self)  # Загружаем дизайн

        self.user_add = Add_user(self)
        self.group_add = Add_group(self)

        self.id_users = []
        self.type_table = 0

        self.users_view()
        self.groups_view()
        self.journal()
        # self.journal()

        # self.btn_add_user.clicked.connect(self.add_book)
        self.btn_add_user.clicked.connect(self.add_users)
        self.btn_edit_user.clicked.connect(self.edit_users)

        self.btn_add_group.clicked.connect(self.add_groups)
        self.btn_edit_group.clicked.connect(self.edit_group)

        self.btn_search_user.clicked.connect(self.search)

        # self.btn_add_reader.clicked.connect(self.add_reader)
        # self.btn_add_journal.clicked.connect(self.add_journal)

        # self.btn_del.clicked.connect(self.delete)

        # self.tw_users.itemChanged.connect(self.edit)
        # self.tw_users.itemChanged.connect(self.edit)

        # self.btn_search.clicked.connect(self.search)

    def search(self):
        self.users_view(self.input_search_user.text())

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

    def users_view(self, search=''):
        self.tab_clear(self.tw_users)
        if not search:
            search = ''
        cursor = self.connection.cursor()
        users = cursor.execute(
            f"SELECT id_user, login_user, name_user, type_user, address_user, phone_user "
            f"FROM users "
            f"WHERE name_user "
            f"LIKE '%{search}%'").fetchall()
        self.tw_users.setColumnCount(6)
        # скрытие столбца с ID книг
        # self.tw_users.setColumnHidden(0, True)
        self.tw_users.setHorizontalHeaderLabels(
            ['ID', 'Логин', 'Имя', 'Тип', 'Адрес', 'Телефон'])
        self.tw_users.setRowCount(len(users))
        # запрет на редактирование содержимого таблицы
        self.tw_users.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # выделение всей строки при нажатии на айтем
        self.tw_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_users.currentRow()
        self.tw_users.selectRow(row_num)
        # убираем не нужные номера строк
        self.tw_users.verticalHeader().setVisible(False)
        # установка адаптивно заполняющего размера ячеек
        self.tw_users.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по вертикали
        self.tw_users.verticalHeader().setDefaultSectionSize(50)
        # self.tw_users.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по горизонтали
        self.tw_users.horizontalHeader().setDefaultSectionSize(150)
        # фиксированный размер 3 столбца
        self.tw_users.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        self.tw_users.horizontalHeader().setDefaultSectionSize(20)
        # фиксированный размер 3 столбца
        # self.tw_users.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        # self.tw_users.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for i, elem in enumerate(users):
            for j, val in enumerate(elem):
                if j == 3:
                    type_user = cursor.execute("""
                    SELECT name_type_user
                    FROM type_users
                    WHERE id_type_user = ?""", (val,)).fetchall()
                    self.tw_users.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in type_user])))
                else:
                    self.tw_users.setItem(i, j, QTableWidgetItem(str(val)))

    def journal(self, search=''):
        self.tab_clear(self.tw_auth_journal)
        if not search:
            search = ''
        cursor = self.connection.cursor()
        users = cursor.execute(
            f"SELECT id_journal, id_user, data_time "
            f"FROM journal ORDER BY id_journal DESC").fetchall()
        self.tw_auth_journal.setColumnCount(3)
        # скрытие столбца с ID книг
        # self.tw_users.setColumnHidden(0, True)
        self.tw_auth_journal.setHorizontalHeaderLabels(
            ['ID', 'Имя пользователя', 'Дата авторизации'])
        self.tw_auth_journal.setRowCount(len(users))
        # запрет на редактирование содержимого таблицы
        self.tw_auth_journal.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # выделение всей строки при нажатии на айтем
        self.tw_auth_journal.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_auth_journal.currentRow()
        self.tw_auth_journal.selectRow(row_num)
        # убираем не нужные номера строк
        self.tw_auth_journal.verticalHeader().setVisible(False)
        # установка адаптивно заполняющего размера ячеек
        self.tw_auth_journal.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по вертикали
        self.tw_auth_journal.verticalHeader().setDefaultSectionSize(50)
        # self.tw_users.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по горизонтали
        self.tw_auth_journal.horizontalHeader().setDefaultSectionSize(150)
        # фиксированный размер 3 столбца
        self.tw_auth_journal.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        self.tw_auth_journal.horizontalHeader().setDefaultSectionSize(20)
        # фиксированный размер 3 столбца
        # self.tw_users.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        # self.tw_users.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for i, elem in enumerate(users):
            for j, val in enumerate(elem):
                if j == 1:
                    type_user = cursor.execute("""
                           SELECT name_user
                           FROM users
                           WHERE id_user = ?""", (val,)).fetchall()
                    self.tw_auth_journal.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in type_user])))
                else:
                    self.tw_auth_journal.setItem(i, j, QTableWidgetItem(str(val)))

    def groups_view(self, search=''):
        self.tab_clear(self.tw_groups)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        groups = cursor.execute(f"SELECT id_group, name_group "
                                f"FROM groups "
                                f"WHERE name_group "
                                f"LIKE '%{search}%'"
                                ).fetchall()
        self.tw_groups.setColumnCount(2)
        # self.tw_groups.setColumnHidden(0, True)
        self.tw_groups.setHorizontalHeaderLabels(
            ['ID', 'Группа'])
        self.tw_groups.setRowCount(len(groups))
        self.tw_groups.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_groups.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_groups.currentRow()
        self.tw_groups.selectRow(row_num)
        self.tw_groups.verticalHeader().setVisible(False)
        self.tw_groups.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_groups.verticalHeader().setDefaultSectionSize(50)
        self.tw_groups.horizontalHeader().setDefaultSectionSize(150)
        self.tw_groups.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tw_groups.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(groups):
            for j, val in enumerate(elem):
                self.tw_groups.setItem(i, j, QTableWidgetItem(str(val)))

    def add_users(self):
        self.user_add.show()

    def edit_users(self):
        id_user = self.check(self.tw_users)
        self.user_edit = Edit_user(self, id_user)
        self.user_edit.show()

    def add_groups(self):
        self.group_add.show()

    def edit_group(self):
        id_group = self.check(self.tw_groups)
        self.group_edit = Edit_group(self, id_group)
        self.group_edit.show()

    def add_journal(self):
        pass

    def delete(self):
        if self.type_table == 0:
            index_rows = list(set(i.row() for i in self.tw_users.selectedItems()))
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить книгу?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        ids = self.tw_users.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM books WHERE id_book = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                        self.users_view()
                elif choice == QMessageBox.No:
                    pass
        elif self.type_table == 1:
            index_rows = list(set(i.row() for i in self.tw_users.selectedItems()))
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить запись??',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        idk = self.tw_users.item(elem, 4).text()
                        idb = self.tw_users.item(elem, 5).text()
                        cursor = self.connection.cursor()
                        give = f'UPDATE books ' + \
                               f'SET count_books = count_books + {int(idk)} ' + \
                               f'WHERE id_book = {idb}'
                        cursor.execute(give)
                        self.connection.commit()

                        ids = self.tw_users.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM clients_books WHERE id_clients_books = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                    self.journal()
                elif choice == QMessageBox.No:
                    pass
        elif self.type_table == 2:
            index_rows = list([i.row() for i in self.tw_users.selectedItems()])
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить автора?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        ids = self.tw_users.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM authors WHERE id_author = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                        cursor = self.connection.cursor()
                        n = f'DELETE FROM authors_books WHERE id_author = {str(ids)}'
                        cursor.execute(n)
                        self.connection.commit()
                    self.author_view()
                elif choice == QMessageBox.No:
                    pass
        elif self.type_table == 3:
            index_rows = list([i.row() for i in self.tw_users.selectedItems()])
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить клиента?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        ids = self.tw_users.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM clients WHERE id_client = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                        cursor = self.connection.cursor()
                        n = f'DELETE FROM clients_books WHERE id_client = {str(ids)}'
                        cursor.execute(n)
                        self.connection.commit()
                    self.groups_view()
                elif choice == QMessageBox.No:
                    pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Admin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
