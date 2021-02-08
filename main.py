import sys
import sqlite3
from PyQt5.QtGui import QPainter, QColor
from UI.ui_main import Ui_Form
from UI.addEditCoffeeForm import Ui_Form1
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QTableWidget
from random import randrange


class Example(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/coffee.db')

        self.update()

    def update(self):
        cur = self.con.cursor()

        result = cur.execute("""Select * from coffee""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(len(result[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))
        # con.close()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)

    def add(self):
        self.win = NewWindow()
        self.win.show()

    def edit(self):
        try:
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                b = self.tableWidget.model().index(currentQTableWidgetItem.row(), 1).data()
                a = int(self.tableWidget.model().index(currentQTableWidgetItem.row(), 0).data())
                c = int(self.tableWidget.model().index(currentQTableWidgetItem.row(), 2).data())
                e = self.tableWidget.model().index(currentQTableWidgetItem.row(), 4).data()
                d = self.tableWidget.model().index(currentQTableWidgetItem.row(), 3).data()
                f = int(self.tableWidget.model().index(currentQTableWidgetItem.row(), 5).data())
                g = int(self.tableWidget.model().index(currentQTableWidgetItem.row(), 6).data())
            self.win = NewWindow(a, b, c, d, e, f, g)
            self.win.show()
        except Exception:
            pass


class NewWindow(QWidget, Ui_Form1):
    def __init__(self, a=0, b=0, c=0, d=0, e=0, f=0, g=0):
        super().__init__()
        self.setupUi(self)
        self.flag = True
        self.id = a

        if a != b != c != d != e != f != e != 0:
            self.flag = False
            self.lineEdit.setText(b)
            # index = self.comboBox.findText(c, QtCore.Qt.MatchFixedString)
            index = self.comboBox.findText(str(c))
            if index >= 0:
                self.comboBox.setCurrentIndex(index)
            index = self.comboBox.findText(d, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.comboBox_2.setCurrentIndex(index)
            self.lineEdit_2.setText(e)
            self.spinBox.setValue(f)
            self.spinBox_2.setValue(g)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        try:
            self.con = sqlite3.connect('data/coffee.db')
            cur = self.con.cursor()
            self.name = self.lineEdit.text()
            self.taste = self.lineEdit_2.text()
            self.price = self.spinBox.value()
            self.v = self.spinBox_2.value()
            self.combo1 = self.comboBox.currentText()
            self.combo2 = self.comboBox_2.currentText()
            if not self.flag:
                cur.execute("""UPDATE coffee
                SET Name = ?, degree = ?, ground = ?, taste = ?, price = ?, volume = ? 
                WHERE ID = ?""",
                        (self.name, self.combo1, self.combo2, self.taste, int(self.price), int(self.v), self.id))
            else:
                cur.execute("""INSERT INTO coffee (Name, degree, ground, taste, price, volume) 
                           VALUES (?,?,?,?,?,?) """,
                        (self.name, self.combo1, self.combo2, self.taste, int(self.price), int(self.v)))

            self.con.commit()
            self.con.close()
            ex.update()
            self.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
