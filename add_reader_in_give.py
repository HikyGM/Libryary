import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Add_reader_in_give(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_reader_in_give_form.ui', self)  # Загружаем дизайн

        self.btn_add.clicked.connect(self.add_reader)
        self.btn_cancel.clicked.connect(self.close)

        self.ex = ex
        self.readers_view()

    def readers_view(self, search=''):
        self.tab_clear(self.tw_readers)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        public_house = cursor.execute(f"SELECT id_reader, name_reader, id_group "
                                      f"FROM readers "
                                      f"WHERE name_reader "
                                      f"LIKE '%{search}%'"
                                      ).fetchall()
        self.tw_readers.setColumnCount(3)
        # self.tw_readers.setColumnHidden(0, True)
        self.tw_readers.setHorizontalHeaderLabels(
            ['ID', 'ФИО', 'Группа'])
        self.tw_readers.setRowCount(len(public_house))
        self.tw_readers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_readers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_readers.currentRow()
        self.tw_readers.selectRow(row_num)
        self.tw_readers.verticalHeader().setVisible(False)
        self.tw_readers.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_readers.verticalHeader().setDefaultSectionSize(50)
        self.tw_readers.horizontalHeader().setDefaultSectionSize(150)
        self.tw_readers.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tw_readers.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(public_house):
            for j, val in enumerate(elem):
                if j == 2:
                    reader = cursor.execute("""
                            SELECT name_group
                            FROM groups
                            WHERE id_group = ?""", (val,)).fetchall()
                    self.tw_readers.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in reader])))
                else:
                    self.tw_readers.setItem(i, j, QTableWidgetItem(str(val)))

    def add_reader(self):
        id_reader = self.check(self.tw_readers)
        self.ex.name_reader = id_reader
        self.ex.view_reader()
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
