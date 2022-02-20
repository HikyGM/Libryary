import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from add_group_reader import Add_group_reader


class Add_reader(QMainWindow):
    def __init__(self, ex):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_reader_form.ui', self)  # Загружаем дизайн

        self.btn_add.clicked.connect(self.check_lines)
        self.btn_cancel.clicked.connect(self.close)

        self.ex = ex
        self.name_group = ''
        self.group_add = Add_group_reader(self)

        self.btn_add_tab_group.clicked.connect(self.add_group)

    def check_lines(self):
        if not self.line_name.text():
            self.label_info.setText('Заполните ФИО')
        elif not self.line_year.text():
            self.label_info.setText('Заполните дату рождения')
        elif not self.line_address.text():
            self.label_info.setText('Заполните адрес')
        elif not self.line_phone.text():
            self.label_info.setText('Заполните номер телефона')
        elif not self.line_group.text():
            self.label_info.setText('Заполните группу')
        else:
            self.add()

    def add(self):
        cursor = self.connection.cursor()
        add = f'INSERT INTO readers(name_reader, address_reader, phone_reader, id_group, year_reader)' + \
              f'VALUES ("{self.line_name.text()}", "{self.line_address.text()}", ' + \
              f'"{self.line_phone.text()}", "{self.name_group[0]}", "{self.line_year.text()}")'
        cursor.execute(add)
        self.connection.commit()
        self.ex.client_view()
        self.name_group = ''
        self.line_name.clear()
        self.line_year.clear()
        self.line_address.clear()
        self.line_phone.clear()
        self.line_group.clear()
        self.close()

    def add_group(self):
        self.group_add.show()

    def view_group(self):
        self.line_group.setText(str(self.name_group[1]))

    def cancel(self):
        self.name_group = ''
        self.line_name.clear()
        self.line_year.clear()
        self.line_address.clear()
        self.line_phone.clear()
        self.line_group.clear()
        self.close()
