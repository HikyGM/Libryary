import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from add_group import Add_group


class Add_group_reader(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_group_reader_form.ui', self)
        self.ex = ex
        self.groups_view()
        self.new_group = Add_group(self)

        self.btn_add.clicked.connect(self.add_group)
        self.btn_add_new_group.clicked.connect(self.add_new_group)
        self.btn_cancel.clicked.connect(self.close)

    def groups_view(self, search=''):
        self.tab_clear(self.tw_groups)
        if not search:
            search = ''
        cursor = self.connection.cursor()

        public_house = cursor.execute(f"SELECT id_group, name_group "
                                      f"FROM groups "
                                      f"WHERE name_group "
                                      f"LIKE '%{search}%'"
                                      ).fetchall()
        self.tw_groups.setColumnCount(2)
        self.tw_groups.setColumnHidden(0, True)
        self.tw_groups.setHorizontalHeaderLabels(
            ['ID', 'Наименование'])
        self.tw_groups.setRowCount(len(public_house))
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
        for i, elem in enumerate(public_house):
            for j, val in enumerate(elem):
                self.tw_groups.setItem(i, j, QTableWidgetItem(str(val)))

    def add_group(self):
        id_group = self.check(self.tw_groups)
        self.ex.name_group = id_group
        self.ex.view_group()
        self.close()

    def add_new_group(self):
        self.new_group.show()

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
