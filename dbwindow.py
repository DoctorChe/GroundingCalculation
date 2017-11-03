#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Окно редактирования базы данных"""
from PyQt5 import QtWidgets, QtCore, QtSql

import dboperations
from ui.ui_dbwindow import Ui_DBWindow

rus = {
    'table_8_4': {
        'a_to_l': 'Отношение расстояний между вертикальными электродами к их длине',
        'n': 'Число вертикальных электродов',
        'k_i_min': 'Кивзм min',
        'k_i_max': 'Кивзм max', },
    'table_8_5': {
        'a_to_l': 'Отношение расстояний между вертикальными электродами к их длине',
        'n': 'Число вертикальных электродов',
        'k_i_min': 'Кивзм min',
        'k_i_max': 'Кивзм max', },
    'table_8_6': {
        'a_to_l': 'Отношение расстояний между вертикальными электродами к их длине',
        'n': 'Число вертикальных электродов в ряду',
        'k_i': 'Кигзм', },
    'table_8_7': {
        'a_to_l': 'Отношение расстояний между вертикальными электродами к их длине',
        'n': 'Число вертикальных электродов в ряду',
        'k_i': 'Кигзм', },
}


class DBWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent,
                                   flags=QtCore.Qt.Window)
        self.ui = Ui_DBWindow()
        self.ui.setupUi(self)

        # Установить список таблиц в comboBox_equipment (из базы данных)
        table_list = [""]
        table_list.extend(list(dboperations.find_tables()))
        table_list.sort()
        self.ui.comboBox_equipment.insertItems(0, table_list)

        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName("db/database.db")
        self.con.open()

        self.model = None

    @QtCore.pyqtSlot(str)
    def show_equipment_table(self, equipment):
        """Вывод таблицы оборудования"""
        # self.model = QtSql.QSqlQueryModel(parent=self)
        self.model = QtSql.QSqlTableModel(parent=self)
        self.model.setTable(equipment)
        self.model.setSort(0, QtCore.Qt.AscendingOrder)
        self.model.select()

        field_count = self.model.columnCount()
        for field_index in range(0, field_count):
            field = self.model.record(field_index).fieldName(field_index)
            self.model.setHeaderData(field_index, QtCore.Qt.Horizontal, rus[equipment][field])

        self.ui.tableView.setModel(self.model)
        # self.ui.tableView.hideColumn(0)
        self.ui.tableView.setColumnWidth(0, 430)
        self.ui.tableView.setColumnWidth(1, 200)
        self.ui.tableView.setColumnWidth(2, 75)


    def closeEvent(self, e):
        """Обработка события закрытия программы"""
        self.con.close()
        e.accept()
