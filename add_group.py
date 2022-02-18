import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Add_group(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_group_form.ui', self)  # Загружаем дизайн
        self.btn_add.clicked.connect(self.check_lines)
        self.btn_cancel.clicked.connect(self.close)
        self.ex = ex

    def check_lines(self):
        if not self.line_group.text():
            self.label_info.setText('Заполните логин')
        else:
            self.add()

    def add(self):
        cursor = self.connection.cursor()
        add = f'INSERT INTO groups(name_group)' + \
              f'VALUES ("{self.line_group.text()}")'
        cursor.execute(add)
        self.connection.commit()
        self.ex.groups_view()
        self.close()
