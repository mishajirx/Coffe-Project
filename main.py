import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.open_second_form)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffee WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            for key in self.modified.keys():
                que += "'{}'='{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def open_second_form(self):
        self.second_form = SecondForm(self)
        self.second_form.show()


class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.con = sqlite3.connect("coffee.sqlite")

    def initUI(self, args):
        self.setGeometry(400, 300, 500, 300)
        self.setWindowTitle('Добавление вкусняшки')

        self.name_lbl1 = QLabel(self)
        self.name_lbl1.setText("Введите название сорта: ")
        self.name_lbl1.move(15, 20)

        self.name_te1 = QLineEdit(self)
        self.name_te1.move(160, 20)

        self.name_lbl2 = QLabel(self)
        self.name_lbl2.setText("Введите степень обжарки: ")
        self.name_lbl2.move(15, 50)

        self.name_te2 = QLineEdit(self)
        self.name_te2.move(160, 50)

        self.name_lbl3 = QLabel(self)
        self.name_lbl3.setText("Молотый/в зёрнах: ")
        self.name_lbl3.move(15, 80)

        self.name_te3 = QLineEdit(self)
        self.name_te3.move(160, 80)

        self.name_lbl4 = QLabel(self)
        self.name_lbl4.setText("Введите описание вкуса: ")
        self.name_lbl4.move(15, 110)

        self.name_te4 = QLineEdit(self)
        self.name_te4.move(160, 110)

        self.name_lbl5 = QLabel(self)
        self.name_lbl5.setText("Введите объём упаковки: ")
        self.name_lbl5.move(15, 140)

        self.name_te5 = QLineEdit(self)
        self.name_te5.move(160, 140)

        self.name_lbl6 = QLabel(self)
        self.name_lbl6.setText("Введите цену: ")
        self.name_lbl6.move(15, 170)

        self.name_te6 = QLineEdit(self)
        self.name_te6.move(160, 170)

        self.btn = QPushButton('Добавить', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(350, 100)
        self.btn.resize(80, 50)
        self.btn.clicked.connect(self.hello)

    def hello(self):
        self.sort_name = self.name_te1.text()
        self.stepen = self.name_te2.text()
        self.molotiy = self.name_te3.text()
        self.vkus = self.name_te4.text()
        self.upakovka = self.name_te5.text()
        self.price = self.name_te6.text()
        cur = self.con.cursor()

        sql = "INSERT INTO coffee('{}', '{}', '{}', '{}', '{}', '{}') VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(
            'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
            'объем упаковки', self.sort_name, self.stepen, self.molotiy, self.vkus, self.price,
            self.upakovka)
        cur.execute(sql)
        self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
