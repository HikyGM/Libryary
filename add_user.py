import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Add_user(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_user_form.ui', self)  # Загружаем дизайн
        self.btn_add.clicked.connect(self.check_lines)
        self.ex = ex

    def check_lines(self):
        if not self.line_login.text():
            self.label_info.setText('Заполните логин')
        elif not self.line_password.text():
            self.label_info.setText('Заполните пароль')
        elif not self.line_fio.text():
            self.label_info.setText('Заполните ФИО')
        elif not self.line_address.text():
            self.label_info.setText('Заполните адрес')
        elif not self.line_phone.text().isnumeric():
            self.label_info.setText('Заполните номер телефона')
        else:
            self.add()

    def add(self):
        cursor = self.connection.cursor()
        add = f'INSERT INTO users(login_user, password_user, name_user, address_user, phone_user, type_user)' + \
              f'VALUES ("{self.line_login.text()}", "{self.line_password.text()}", ' + \
              f'"{self.line_fio.text()}", "{self.line_address.text()}", "{self.line_phone.text()}", ' \
              f'"{self.line_phone.text()}")'
        cursor.execute(add)
        self.connection.commit()
        self.ex.users_view()
        self.close()
