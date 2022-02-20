import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Add_new_public_house(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_new_public_house_form.ui', self)
        self.ex = ex
        self.btn_add.clicked.connect(self.check_lines)
        self.btn_cancel.clicked.connect(self.close)

    def check_lines(self):
        if not self.line_name.text():
            self.label_info.setText('Заполните наименование')
        else:
            self.add()

    def add(self):
        cursor = self.connection.cursor()
        add = f'INSERT INTO pub_houses(name_pub_house)' + \
              f'VALUES ("{self.line_name.text()}")'
        cursor.execute(add)
        self.connection.commit()
        self.ex.groups_view()
        self.close()
