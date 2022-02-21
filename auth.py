import sys
import sqlite3
from datetime import datetime
from manager import Manager
from admin import Admin
from librarian import Librarian
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Login(QMainWindow):
    def __init__(self):
        super().__init__()


        self.admin = Admin()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/auth_form.ui', self)  # Загружаем дизайн
        self.btn_chek_auth.clicked.connect(self.chek_user)

    def chek_user(self):
        cursor = self.connection.cursor()
        if self.login_input.text():
            check = cursor.execute("""SELECT password_user, type_user, id_user FROM users WHERE login_user = ?""",
                                   (self.login_input.text(),)).fetchone()
            if check[0] == self.password_input.text():
                cursor = self.connection.cursor()
                now = datetime.now()
                add = f'INSERT INTO journal(id_user, data_time)' + \
                      f'VALUES ("{check[2]}", "{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}")'
                cursor.execute(add)
                self.connection.commit()
                ex.hide()
                if check[1] == '1':
                    self.admin.show()
                elif check[1] == '2':
                    self.manager = Manager(check[2])
                    self.manager.show()
                elif check[1] == '3':
                    self.librarian = Librarian(check[2])
                    self.librarian.show()
            else:
                self.error_label.setText('Неверный логин или пароль')
        else:
            self.error_label.setText('Введите логин')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
