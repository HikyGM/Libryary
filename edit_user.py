import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Edit_user(QMainWindow):
    def __init__(self, ex, id):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_user_form.ui', self)  # Загружаем дизайн
        self.btn_add.clicked.connect(self.check_lines)
        self.btn_cancel.clicked.connect(self.close)

        self.ex = ex
        self.id = id
        self.btn_add.setText('Изменить')
        cursor = self.connection.cursor()
        res = cursor.execute(
            """SELECT login_user, password_user, name_user, address_user, phone_user, type_user FROM users WHERE id_user = ?""",
            (self.id,)).fetchall()
        all_info = res[0]
        login, password, name, address, phone, type = all_info
        self.line_login.setText(str(login))
        self.line_password.setText(str(password))
        self.line_fio.setText(str(name))
        self.line_address.setText(str(address))
        self.line_phone.setText(str(phone))
        # self.combo_type.setText(type)

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
            self.update()

    def update(self):
        cursor = self.connection.cursor()
        res = f'UPDATE users ' + \
              f'SET login_user = "{self.line_login.text()}", password_user = "{self.line_password.text()}", ' + \
              f'name_user = "{self.line_fio.text()}", address_user = "{self.line_address.text()}", ' + \
              f'phone_user = "{self.line_phone.text()}", type_user = "{self.line_phone.text()}" ' + \
              f'WHERE id_user = {self.id}'
        cursor.execute(res)
        self.connection.commit()
        self.ex.users_view()
        self.close()
