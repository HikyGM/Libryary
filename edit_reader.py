import sqlite3
from add_group_reader import Add_group_reader
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class Edit_reader(QMainWindow):
    def __init__(self, ex, id_reader):
        super().__init__()
        self.connection = sqlite3.connect("db/library.db")
        uic.loadUi('forms/add_reader_form.ui', self)
        self.ex = ex
        self.id_reader = id_reader
        print('id', self.id_reader)
        # [0] - id [1] - название издателя
        self.name_group = ''

        # объекты классов
        self.group_view = Add_group_reader(self)

        # заполнение форм
        cursor = self.connection.cursor()
        res = cursor.execute(
            """SELECT name_reader, address_reader, phone_reader, id_group, year_reader 
            FROM readers 
            WHERE id_reader = ?""",
            (self.id_reader,)).fetchall()
        all_info = res[0]
        name, address, phone, group, year = all_info
        self.line_name.setText(str(name))
        self.line_year.setText(str(year))
        self.line_address.setText(str(address))
        self.line_phone.setText(str(phone))
        # добавление группы
        res = cursor.execute(
            """SELECT id_group, name_group FROM groups WHERE id_group = ?""",
            (group,)).fetchall()
        self.name_group = res[0]
        self.view_group()

        # события кнопок
        self.btn_add.clicked.connect(self.check_lines)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_add_tab_group.clicked.connect(self.add_group)

    def view_group(self):
        self.line_group.setText(str(self.name_group[1]))

    def cancel(self):
        self.name_group = ''
        self.line_group.clear()
        self.close()

    def tab_clear(self, table):
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(0)

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
            self.update()

    def add_group(self):
        self.group_view.show()

    def update(self):
        cursor = self.connection.cursor()
        res = f'UPDATE readers ' + \
              f'SET name_reader = "{self.line_name.text()}", address_reader = "{self.line_address.text()}", ' + \
              f'phone_reader= "{self.line_phone.text()}", id_group = "{self.name_group[0]}", ' + \
              f'year_reader = "{self.line_year.text()}" ' + \
              f'WHERE id_reader = {self.id_reader}'
        cursor.execute(res)
        self.connection.commit()
        self.ex.client_view()

        # очистка всех полей после добавления


        self.name_group = ''
        self.line_name.clear()
        self.line_year.clear()
        self.line_address.clear()
        self.line_phone.clear()
        self.line_group.clear()
        self.close()
