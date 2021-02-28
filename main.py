from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QTableWidgetItem


class Uishka(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(825, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 821, 73))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setObjectName("layout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 800, 475))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class Example(QMainWindow, Uishka):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("cofffee.sqlite")
        self.initUI()
        self.select_data("А")

    def initUI(self):
        super().setupUi(self)
        self.setWindowTitle('Алфавитный указатель')

    def select_data(self, char):
        res = []
        raw = self.connection.cursor().execute('SELECT * FROM Films').fetchall()
        self.tableWidget.clearContents()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название', 'Год', 'Жанр', 'длительность'])
        self.tableWidget.setColumnWidth(1, 350)
        for i in raw:
            if i[1][0].upper() == char:
                res.append(i)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        if not res:
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(0, 1, QTableWidgetItem('Фильмов нет'))

    def f(self):
        self.select_data(self.sender().text())

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
