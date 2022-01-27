import sys
import sqlite3
# from add_book import Add_book
# from new_auth import New_auth
# from client_add import Clients
# from give_book import Give_book
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Librarian(QMainWindow):
    def __init__(self):
        super().__init__()
        pass
        # self.connection = sqlite3.connect("db/library.db")
        # uic.loadUi('forms/main_wid.ui', self)  # Загружаем дизайн
        # self.id_books = []
        # self.type_table = 0
        # self.books_view()
        # self.btn_books.clicked.connect(self.books_view)
        # self.btn_journal.clicked.connect(self.journal)
        # self.btn_author.clicked.connect(self.author_view)
        # self.btn_clients.clicked.connect(self.client_view)
        # self.btn_add.clicked.connect(self.add)
        # self.btn_edit.clicked.connect(self.edit)
        # self.btn_del.clicked.connect(self.delete)
        # # self.main_table.itemChanged.connect(self.edit)
        # self.btn_search.clicked.connect(self.search)
