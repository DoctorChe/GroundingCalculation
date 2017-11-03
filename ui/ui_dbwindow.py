# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dbwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DBWindow(object):
    def setupUi(self, DBWindow):
        DBWindow.setObjectName("DBWindow")
        DBWindow.resize(829, 408)
        DBWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        DBWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DBWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(DBWindow)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_equipment = QtWidgets.QComboBox(DBWindow)
        self.comboBox_equipment.setObjectName("comboBox_equipment")
        self.horizontalLayout.addWidget(self.comboBox_equipment)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtWidgets.QTableView(DBWindow)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.pushButton_close = QtWidgets.QPushButton(DBWindow)
        self.pushButton_close.setObjectName("pushButton_close")
        self.verticalLayout.addWidget(self.pushButton_close, 0, QtCore.Qt.AlignRight)

        self.retranslateUi(DBWindow)
        self.comboBox_equipment.currentTextChanged['QString'].connect(DBWindow.show_equipment_table)
        self.pushButton_close.clicked.connect(DBWindow.close)
        QtCore.QMetaObject.connectSlotsByName(DBWindow)

    def retranslateUi(self, DBWindow):
        _translate = QtCore.QCoreApplication.translate
        DBWindow.setWindowTitle(_translate("DBWindow", "База данных"))
        self.label.setText(_translate("DBWindow", "Выберите необходимую таблицу из списка"))
        self.pushButton_close.setText(_translate("DBWindow", "Закрыть"))

