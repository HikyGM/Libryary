import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class View_reader(QMainWindow):
    def __init__(self, ex, id_reader):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/view_reader_form.ui', self)  # Загружаем дизайн

        self.ex = ex
        self.id_reader = id_reader
        self.name_group = ''
        self.btn_cancel.clicked.connect(self.close)

        # заполнение форм
        cursor = self.connection.cursor()
        res = cursor.execute(
            """SELECT name_reader, address_reader, phone_reader, id_group, year_reader 
            FROM readers 
            WHERE id_reader = ?""",
            (self.id_reader,)).fetchall()
        all_info = res[0]
        name, address, phone, group, year = all_info

        self.label_name.setText(str(name))
        self.label_address.setText(str(address))
        self.label_phone.setText(str(phone))
        self.label_year.setText(str(year))

        # добавление группы
        res = cursor.execute(
            """SELECT id_group, name_group FROM groups WHERE id_group = ?""",
            (group,)).fetchall()
        self.name_group = res[0]

        self.label_group.setText(str(self.name_group[1]))
