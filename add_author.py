import sqlite3
from add_new_author import Add_new_author
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Add_author(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_author_form.ui', self)
        self.ex = ex
        self.author_view()
        self.new_author = Add_new_author(self)
        self.btn_add.clicked.connect(self.add_author)
        self.btn_add_new_auth.clicked.connect(self.add_new_author)
        self.btn_cancel.clicked.connect(self.close)

    def author_view(self, search=''):
        self.tab_clear(self.tw_authors)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        authors = cursor.execute(f"SELECT id_author, name_author "
                                 f"FROM authors "
                                 f"WHERE name_author "
                                 f"LIKE '%{search}%'"
                                 ).fetchall()
        self.tw_authors.setColumnCount(2)
        # self.tw_authors.setColumnHidden(0, True)
        self.tw_authors.setHorizontalHeaderLabels(
            ['ID', 'Автор'])
        self.tw_authors.setRowCount(len(authors))
        self.tw_authors.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_authors.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_authors.currentRow()
        self.tw_authors.selectRow(row_num)
        self.tw_authors.verticalHeader().setVisible(False)
        self.tw_authors.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_authors.verticalHeader().setDefaultSectionSize(50)
        self.tw_authors.horizontalHeader().setDefaultSectionSize(150)
        self.tw_authors.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tw_authors.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(authors):
            for j, val in enumerate(elem):
                self.tw_authors.setItem(i, j, QTableWidgetItem(str(val)))

    def add_author(self):
        id_author = self.check(self.tw_authors)
        self.ex.list_authors.append(id_author)
        self.ex.view_author()
        self.close()
        print(self.ex.list_authors)

    def add_new_author(self):
        self.new_author.show()

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
