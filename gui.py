from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPixmap
import sys
import os
from tree import draw
from main import get_tokens, set_tokens

# global tokens
combo_box_options = ["SEMICOLON", "IF", "THEN", "END", "REPEAT", "UNTIL", "IDENTIFIER", "ASSIGN", "READ", "WRITE",
                     "ELSE", "LESSTHAN", "EQUAL", "PLUS", "MINUS", "MULT", "DIV", "OPENBRACKET", "CLOSEDBRACKET", "NUMBER"]

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('mainwindow.ui', self) # Load the .ui file

        # edit view inside the mainwindow
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # connect buttons with functions
        self.runButton.clicked.connect(self.run)
        self.addTokenButton.clicked.connect(self.addToken)
        self.actionLoad.triggered.connect(self.open_file)
        self.actionClear.triggered.connect(self.clear_text)
        self.actionQuit.triggered.connect(self.close_program)

        self.show()  # Show the GUI

    # implement buttons functions
    def run(self):
        try:
            self.store_tokens()
            draw()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Syntax Error', f"{e}", QtWidgets.QMessageBox.Ok)

    def addToken(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

        combo = QtWidgets.QComboBox()
        for t in combo_box_options:
            combo.addItem(t)
        self.tableWidget.setCellWidget(rowPosition, 1, combo)

    def fill_table(self, file):
        global token_values
        global token_types
        with open(file, 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                split_array = line.split(',')
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)

                item1 = QtWidgets.QTableWidgetItem(split_array[0].strip())
                self.tableWidget.setItem(rowPosition, 0, item1)
                combo = QtWidgets.QComboBox()
                for t in combo_box_options:
                    combo.addItem(t)
                self.tableWidget.setCellWidget(rowPosition, 1, combo)
                index = combo.findText(split_array[1].strip(), QtCore.Qt.MatchFixedString)
                combo.setCurrentIndex(index)

    def store_tokens(self):
        tokens = get_tokens()
        tokens = []
        rowPosition = self.tableWidget.rowCount()
        for i in range(rowPosition):
            if self.tableWidget.item(i, 0):
                x = (self.tableWidget.item(i, 0).text(), self.tableWidget.cellWidget(i, 1).currentText())
                tokens.append(x)
        set_tokens(tokens)

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', os.getenv('HOME'))
        if filename[0]:
            self.fill_table(filename[0])

    def clear_text(self):
        self.tableWidget.setRowCount(0)

    @staticmethod
    def close_program():
        sys.exit()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
