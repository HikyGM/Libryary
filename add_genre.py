import sqlite3
from add_new_ganre import Add_new_genre
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Add_genre(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_genre_form.ui', self)
        self.ex = ex
        self.genre_view()
        self.new_genre = Add_new_genre(self)
        self.btn_add.clicked.connect(self.add_genre)
        self.btn_add_new_genre.clicked.connect(self.add_new_genre)
        self.btn_cancel.clicked.connect(self.close)

    def genre_view(self, search=''):
        self.tab_clear(self.tw_genre)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        genres = cursor.execute(f"SELECT id_genre, name_genre "
                                f"FROM genre "
                                f"WHERE name_genre "
                                f"LIKE '%{search}%'"
                                ).fetchall()
        self.tw_genre.setColumnCount(2)
        # self.tw_genre.setColumnHidden(0, True)
        self.tw_genre.setHorizontalHeaderLabels(
            ['ID', 'Наименование'])
        self.tw_genre.setRowCount(len(genres))
        self.tw_genre.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_genre.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_genre.currentRow()
        self.tw_genre.selectRow(row_num)
        self.tw_genre.verticalHeader().setVisible(False)
        self.tw_genre.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_genre.verticalHeader().setDefaultSectionSize(50)
        self.tw_genre.horizontalHeader().setDefaultSectionSize(150)
        self.tw_genre.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tw_genre.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(genres):
            for j, val in enumerate(elem):
                self.tw_genre.setItem(i, j, QTableWidgetItem(str(val)))

    def add_genre(self):
        id_genre = self.check(self.tw_genre)
        self.ex.list_genre.append(id_genre)
        self.ex.view_genre()
        self.close()

    def add_new_genre(self):
        self.new_genre.show()

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
