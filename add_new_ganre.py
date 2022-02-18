import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Add_new_genre(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_new_genre_form.ui', self)
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
        add = f'INSERT INTO genre(name_genre)' + \
              f'VALUES ("{self.line_name.text()}")'
        cursor.execute(add)
        self.connection.commit()
        self.ex.genre_view()
        self.close()
