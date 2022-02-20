import sqlite3
from add_new_public_house import Add_new_public_house
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Add_public_house(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_public_house_form.ui', self)
        self.ex = ex
        self.public_house_view()
        self.new_public_house = Add_new_public_house(self)
        self.btn_add.clicked.connect(self.add_public_house)
        self.btn_add_new_public_house.clicked.connect(self.add_new_public_house)
        self.btn_cancel.clicked.connect(self.close)

    def public_house_view(self, search=''):
        self.tab_clear(self.tw_public_house)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        public_house = cursor.execute(f"SELECT id_pub_house, name_pub_house "
                                      f"FROM pub_houses "
                                      f"WHERE name_pub_house "
                                      f"LIKE '%{search}%'"
                                      ).fetchall()
        self.tw_public_house.setColumnCount(2)
        # self.tw_public_house.setColumnHidden(0, True)
        self.tw_public_house.setHorizontalHeaderLabels(
            ['ID', 'Наименование'])
        self.tw_public_house.setRowCount(len(public_house))
        self.tw_public_house.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_public_house.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.tw_public_house.currentRow()
        self.tw_public_house.selectRow(row_num)
        self.tw_public_house.verticalHeader().setVisible(False)
        self.tw_public_house.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tw_public_house.verticalHeader().setDefaultSectionSize(50)
        self.tw_public_house.horizontalHeader().setDefaultSectionSize(150)
        self.tw_public_house.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tw_public_house.horizontalHeader().setDefaultSectionSize(20)
        for i, elem in enumerate(public_house):
            for j, val in enumerate(elem):
                self.tw_public_house.setItem(i, j, QTableWidgetItem(str(val)))

    def add_public_house(self):
        id_public_house = self.check(self.tw_public_house)
        self.ex.name_public_house = id_public_house
        self.ex.view_public_house()
        self.close()

    def add_new_public_house(self):
        self.new_public_house.show()

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
