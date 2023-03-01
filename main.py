import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main()

    def main(self):
        uic.loadUi('UI/UI.ui', self)
        self.app.clicked.connect(self.open_update_win)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM coffee')
        result = cursor.fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setDisabled(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["id", "Name coffe", "Roast", "Description", "Ground", "Price", "Volume"])
        self.tableWidget.cellDoubleClicked.connect(self.expandShipments)
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(f'{result[i][0]}'))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(f'{result[i][1]}'))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f'{result[i][2]}'))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(f'{result[i][3]}'))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(f'{result[i][4]}'))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(f'{result[i][5]}'))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(f'{result[i][6]}'))
        self.tableWidget.resizeColumnsToContents()
        conn.close()

    def open_update_win(self, arg=False):
        uic.loadUi('UI/addEditCoffeeForm.ui', self)
        self.pushButton_2.clicked.connect(self.main)
        if arg:
            self.pushButton_3.show()
            self.pushButton.setText('update')
            self.name_coffe_lineEdit.setText(arg[1])
            self.roast_lineEdit.setText(arg[2])
            self.ground_lineEdit.setText(arg[3])
            self.textEdit.setText(arg[4])
            self.price_lineEdit.setText(str(arg[5]))
            self.lineEdit_5.setText(str(arg[6]))
            self.pushButton.clicked.connect(self.save)
            self.pushButton_3.clicked.connect(lambda: self.save(de=True))
        else:
            self.pushButton_3.hide()
            self.pushButton.setText('create')
            self.pushButton.clicked.connect(lambda: self.save(True))

    def expandShipments(self, row, column):
        item = self.tableWidget.item(row, 0)
        # print(item.text())
        self.id = item.text()
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM coffee WHERE id == {self.id}')
        result = cursor.fetchall()[0]
        conn.close()
        self.open_update_win(arg=result)

    def save(self, new=False, de=False):
        con = sqlite3.connect('data/coffee.sqlite')
        cursor = con.cursor()
        if de:
            cursor.execute(f"""DELETE FROM coffee WHERE id == {self.id}""")
        elif new:
            # print(self.name_coffe_lineEdit.text(), self.roast_lineEdit.text(), self.ground_lineEdit.text())
            # print(self.textEdit.toPlainText(), int(self.price_lineEdit.text()), int(self.lineEdit_5.text()))
            last_id = cursor.execute(f"""SELECT id FROM coffee""").fetchall()[-1][0]
            cursor.execute(f'''INSERT INTO coffee(id, name, roast, ground, description, price, volume)
                            VALUES ({last_id + 1}, '{self.name_coffe_lineEdit.text()}', '{self.roast_lineEdit.text()}',
                            '{self.ground_lineEdit.text()}', '{self.textEdit.toPlainText()}',
                            {float(self.price_lineEdit.text())}, {int(self.lineEdit_5.text())})''')
        else:
            cursor.execute(f"""UPDATE coffee SET 
                               name == '{self.name_coffe_lineEdit.text()}',
                               roast == '{self.roast_lineEdit.text()}',
                               ground == '{self.ground_lineEdit.text()}',
                               description == '{self.textEdit.toPlainText()}',
                               price == {float(self.price_lineEdit.text())},
                               volume == {int(self.lineEdit_5.text())}
                               WHERE id == {self.id}""")

        con.commit()
        con.close()
        self.main()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
