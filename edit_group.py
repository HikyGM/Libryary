import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Edit_group(QMainWindow):
    def __init__(self, ex, id):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_group_form.ui', self)  # Загружаем дизайн
        self.btn_add.clicked.connect(self.check_lines)
        self.ex = ex
        self.id = id
        self.btn_add.setText('Изменить')
        cursor = self.connection.cursor()
        res = cursor.execute(
            """SELECT name_group FROM groups WHERE id_group = ?""",
            (self.id,)).fetchall()
        all_info = res[0]
        name = all_info[0]
        self.line_group.setText(str(name))

    def check_lines(self):
        if not self.line_group.text():
            self.label_info.setText('Заполните логин')
        else:
            self.update()

    def update(self):
        cursor = self.connection.cursor()
        res = f'UPDATE groups ' + \
              f'SET name_group = "{self.line_group.text()}" ' + \
              f'WHERE id_group = {self.id}'
        cursor.execute(res)
        self.connection.commit()
        self.ex.groups_view()
        self.close()
