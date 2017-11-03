#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Программа для расчёта заземляющих устройств"""

import sys
# Импортируем наш интерфейс из файла
from ui.ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow, QSystemTrayIcon, QStyle, QAction, \
    QMenu, qApp
from PyQt5 import QtCore
# from PyQt5 import QtWidgets
# from PyQt5 import QtGui
from grounding_arrangement_calculation import GroundingArrangement
# import dboperations
# import addcabledialog
# import addbuswaydialog
import dbwindow

from mailmerge import MailMerge
from appy.pod.renderer import Renderer


# tr_connection_windings_list = ["Y/Yн-0", "Yн/Y-0", "Y/Δ-11", "Yн/Δ-11", "Y/Zн-11", "Δ/Yн-11", "Δ/Δ-0", "1/1н"]


class MainWindow(QMainWindow):
    """Основной класс программы"""

    # Объявление чекбокса и иконки системного трея
    check_box = None
    tray_icon = None

    def __init__(self, iniFile, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dbwindow = None
        self.iniFile = iniFile
        self.settings = QtCore.QSettings(iniFile, QtCore.QSettings.IniFormat)

        # # Установить список производителей трансформаторов в comboBox_tr_manufacturer (из базы данных)
        # manufactures_list = [""]
        # manufactures_list.extend(list(dboperations.find_manufacturers()))
        # manufactures_list.sort()
        # self.ui.comboBox_tr_manufacturer.insertItems(0, manufactures_list)

        # Чтение настроек
        self.read_settings()

        if self.ui.radioButton.isChecked():
            self.ui.radioButton_2.click()
            self.ui.radioButton.click()
        else:
            self.ui.radioButton.click()
            self.ui.radioButton_2.click()

        self.ui.tab_calc_results.setEnabled(self.ui.radioButton.isChecked())
        self.ui.tab_check_results.setEnabled(self.ui.radioButton_2.isChecked())

        # if not self.ui.comboBox_contoured.currentIndex():
        #     self.ui.doubleSpinBox_grounding_contour_width.setEnabled(False)
        self.on_clicked_comboBox_contoured(self.ui.comboBox_contoured.currentIndex())

        # Событие
        # self.ui.action_db.triggered.connect(self.show_db_window)

        # Здесь прописываем событие нажатия на кнопку
        # self.ui.pushButton.clicked.connect(self.start_calculation)

        # self.ui.comboBox_tr_manufacturer.activated[str].connect(self.on_clicked_comboBox_tr_manufacturer)
        self.ui.radioButton.clicked[bool].connect(self.on_clicked_radioButton)
        self.ui.radioButton_2.clicked[bool].connect(self.on_clicked_radioButton_2)
        self.minimize_to_tray()

        self.ga = GroundingArrangement()

    def on_clicked_radioButton(self, checked):
        self.ui.tab_calc_results.setEnabled(checked)
        self.ui.tab_check_results.setEnabled(not checked)

    def on_clicked_radioButton_2(self, checked):
        self.ui.tab_calc_results.setEnabled(not checked)
        self.ui.tab_check_results.setEnabled(checked)

    def save_and_quit(self):
        # print("save_and_quit")
        # self.settings = QtCore.QSettings(self.iniFile, QtCore.QSettings.IniFormat)
        # self.settings.setIniCodec("utf-8")
        # self.save_settings()
        qApp.quit()

    def minimize_to_tray(self):
        """
            Объявим и добавим действия для работы с иконкой системного трея
            show - показать окно
            hide - скрыть окно
            exit - выход из программы
        """

        # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Показать", self)
        hide_action = QAction("Скрыть", self)
        quit_action = QAction("Выход", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        # quit_action.triggered.connect(qApp.quit)
        quit_action.triggered.connect(self.save_and_quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, e):
        """Обработка события закрытия программы"""
        # Переопределение метода closeEvent, для перехвата события закрытия окна
        # Окно будет закрываться только в том случае, если нет галочки в чекбоксе
        # if self.ui.action_minimize_to_tray.isChecked():
        #     e.ignore()
        #     self.hide()
        #     self.tray_icon.showMessage(
        #         "Программный трей",
        #         "Приложение было минимизированно в трей",
        #         QSystemTrayIcon.Information,
        #         2000
        #     )
        # else:
        #     # Write data to config file
        #     self.settings = QtCore.QSettings(self.iniFile, QtCore.QSettings.IniFormat)
        #     self.save_settings()
        #     e.accept()

        # Write data to config file
        self.settings = QtCore.QSettings(self.iniFile, QtCore.QSettings.IniFormat)
        self.save_settings()
        e.accept()

    # @QtCore.pyqtSlot(int)
    # def on_clicked_comboBox_tr_regime(self, index):
    #     """Переключение режима трасформатора"""
    #     if not index:
    #         self.ui.comboBox_tr_regime_value.hide()
    #         self.ui.lineEdit_tr_regime_value.show()
    #     else:
    #         self.ui.comboBox_tr_regime_value.show()
    #         self.ui.lineEdit_tr_regime_value.hide()

    # @QtCore.pyqtSlot()
    # def update_comboBox_tr_manufacturer(self):
    #     """
    #     Поиск заводов-производителей трансформаторов в базе
    #     Добавление их в comboBox_tr_manufacturer
    #     """
    #     models = dboperations.find_manufacturers()
    #     self.ui.comboBox_tr_manufacturer.clear()
    #     if len(models) > 1:
    #         self.ui.comboBox_tr_manufacturer.insertItems(0, ['', ])
    #     self.ui.comboBox_tr_manufacturer.insertItems(1, models)
    #     self.clean_calc_data_tr()

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_permissible_resistance(self, value):
        """Предача значения из comboBox в doubleSpinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.doubleSpinBox_permissible_resistance.setValue(float(value_last))
        except ValueError:
            self.ui.doubleSpinBox_permissible_resistance.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_soil_resistivity_high(self, value):
        """Предача значения из comboBox в spinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.spinBox_soil_resistivity_high.setValue(int(value_last))
        except ValueError:
            self.ui.spinBox_soil_resistivity_high.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_soil_resistivity_low(self, value):
        """Предача значения из comboBox в spinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.spinBox_soil_resistivity_low.setValue(int(value_last))
        except ValueError:
            self.ui.spinBox_soil_resistivity_low.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_ground_electrode_vertical_length(self, value):
        """Предача значения из comboBox в doubleSpinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.doubleSpinBox_ground_electrode_vertical_length.setValue(float(value_last))
        except ValueError:
            self.ui.doubleSpinBox_ground_electrode_vertical_length.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_ground_electrode_vertical_diameter(self, value):
        """Предача значения из comboBox в spinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.spinBox_ground_electrode_vertical_diameter.setValue(int(value_last))
        except ValueError:
            self.ui.spinBox_ground_electrode_vertical_diameter.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_ground_electrode_vertical_climat_coeff(self, value):
        """Предача значения из comboBox в doubleSpinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.doubleSpinBox_ground_electrode_vertical_climat_coeff.setValue(float(value_last))
        except ValueError:
            self.ui.doubleSpinBox_ground_electrode_vertical_climat_coeff.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_ground_electrode_horizontal_width(self, value):
        """Предача значения из comboBox в spinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.spinBox_ground_electrode_horizontal_width.setValue(int(value_last))
        except ValueError:
            self.ui.spinBox_ground_electrode_horizontal_width.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_ground_electrode_horizontal_depth(self, value):
        """Предача значения из comboBox в doubleSpinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.doubleSpinBox_ground_electrode_horizontal_depth.setValue(float(value_last))
        except ValueError:
            self.ui.doubleSpinBox_ground_electrode_horizontal_depth.setValue(0)

    @QtCore.pyqtSlot(str)
    def on_clicked_comboBox_ground_electrode_horizontal_climat_coeff(self, value):
        """Предача значения из comboBox в doubleSpinBox"""
        value_last = value.split(' ')[-1]
        try:
            self.ui.doubleSpinBox_ground_electrode_horizontal_climat_coeff.setValue(float(value_last))
        except ValueError:
            self.ui.doubleSpinBox_ground_electrode_horizontal_climat_coeff.setValue(0)

    @QtCore.pyqtSlot(int)
    def on_clicked_comboBox_contoured(self, contoured):
        """Предача значения из comboBox в doubleSpinBox"""
        self.ui.doubleSpinBox_grounding_contour_width.setEnabled(contoured)

    # @QtCore.pyqtSlot(str)
    # def on_clicked_comboBox_tr_manufacturer(self, manufacturer):
    #     """
    #     Поиск моделей трансформаторов в базе
    #     Добавление их в comboBox_tr_model
    #     """
    #     models = dboperations.find_models(manufacturer)
    #     self.ui.comboBox_tr_model.clear()
    #     if len(models) > 1:
    #         self.ui.comboBox_tr_model.insertItems(0, ['', ])
    #     self.ui.comboBox_tr_model.insertItems(1, models)
    #     self.clean_calc_data_tr()

    # @QtCore.pyqtSlot(str)
    # def on_clicked_comboBox_tr_short_circuit_loss(self, short_circuit_loss):
    #     """
    #     Поиск напряжений короткого замыкания трансформаторов в базе
    #     Добавление их в comboBox_tr_impedance_voltage
    #     """
    #     manufacturer = self.ui.comboBox_tr_manufacturer.currentText()
    #     model = self.ui.comboBox_tr_model.currentText()
    #     full_rated_capacity = self.ui.comboBox_tr_full_rated_capacity.currentText()
    #     nominal_voltage_HV = self.ui.comboBox_U_sr_VN.currentText()
    #     nominal_voltage_LV = self.ui.comboBox_U_sr_NN.currentText()
    #     connection_windings = self.ui.comboBox_tr_connection_windings.currentText()
    #     impedance_voltage = dboperations.find_impedance_voltage(manufacturer, model, full_rated_capacity,
    #                                                             nominal_voltage_HV, nominal_voltage_LV,
    #                                                             connection_windings, short_circuit_loss)
    #     self.ui.comboBox_tr_impedance_voltage.clear()
    #     if len(impedance_voltage) > 1:
    #         self.ui.comboBox_tr_impedance_voltage.insertItems(0, ['', ])
    #     self.ui.comboBox_tr_impedance_voltage.insertItems(1, impedance_voltage)

    #     msg = "Данные трансформатора введены успешно."
    #     self.statusBar().showMessage(msg)

    #     self.clean_calc_data_tr()

    # def calc_tr_data(self):
    #     # Считывание данных трансформатора
    #     try:
    #         # Параметры трансформатора
    #         St_nom = 1
    #         U_NN_nom = 0
    #         Pk_nom = 0
    #         u_k = 0
    #         R0t = 0
    #         X0t = 0
    #         St_nom = float(self.ui.comboBox_tr_full_rated_capacity.currentText())
    #         U_NN_nom = float(self.ui.comboBox_U_sr_NN.currentText())
    #         Pk_nom = float(self.ui.comboBox_tr_short_circuit_loss.currentText())
    #         u_k = float(self.ui.comboBox_tr_impedance_voltage.currentText())
    #         # R0t = float(self.ui.lineEdit_R0t.text())
    #         # X0t = float(self.ui.lineEdit_X0t.text())
    #     except ValueError:
    #         msg = ("Исходные данные трансформатора введены не корректно. " +
    #                "Сопротивление трансформатора в расчётах не учитывается.")
    #         self.statusBar().showMessage(msg)
    #     else:
    #         # Pk_nom, U_NN_nom, St_nom, u_k, R0t, X0t,  # Трансформатор
    #         R1t = gac.calc_Rt(Pk_nom, U_NN_nom * 1000, St_nom)
    #         X1t = gac.calc_Xt(Pk_nom, U_NN_nom * 1000, St_nom, u_k)
    #         # print(R1t, X1t)
    #         self.ui.lineEdit_Rt.setText("{:.2f}".format(R1t))
    #         self.ui.lineEdit_Xt.setText("{:.2f}".format(X1t))
    #         if self.ui.comboBox_tr_connection_windings.currentText() == "Δ/Yн-11":
    #             R0t = R1t
    #             X0t = X1t
    #             self.ui.lineEdit_R0t.setText("{:.2f}".format(R0t))
    #             self.ui.lineEdit_X0t.setText("{:.2f}".format(X0t))
    #             msg = "Расчетные данные трансформатора вычислены успешно."
    #             self.statusBar().showMessage(msg)
    #         else:
    #             self.ui.lineEdit_R0t.setText("")
    #             self.ui.lineEdit_X0t.setText("")
    #             msg = "Введите сопротивление нулевой последовательности трансформатора вручную."
    #             self.statusBar().showMessage(msg)

    # def clean_calc_data_tr(self):
    #     self.ui.lineEdit_Rt.clear()
    #     self.ui.lineEdit_Xt.clear()
    #     self.ui.lineEdit_R0t.clear()
    #     self.ui.lineEdit_X0t.clear()

    def checked_action_minimize_to_tray(self):
        # print("action_minimize_to_tray Checked=" + str(self.ui.action_minimize_to_tray.isChecked()))
        pass

    def clean_form(self):
        """Полная очистка формы"""
        self.ui.radioButton.click()
        self.ui.comboBox_permissible_resistance.setCurrentIndex(0)
        self.ui.doubleSpinBox_natural_grounding_resistance.setValue(0)
        self.ui.doubleSpinBox_soil_high_level_depth.setValue(0)
        self.ui.comboBox_soil_resistivity_high.setCurrentIndex(0)
        self.ui.comboBox_soil_resistivity_low.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_vertical_length.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_vertical_type.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_vertical_diameter.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_vertical_climat_coeff.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_horizontal_width.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_horizontal_depth.setCurrentIndex(0)
        self.ui.comboBox_ground_electrode_horizontal_climat_coeff.setCurrentIndex(0)
        self.ui.comboBox_contoured.setCurrentIndex(0)
        self.ui.spinBox_a_div_l.setValue(1)
        self.ui.spinBox_ground_electrode_vertical_number.setValue(1)
        self.ui.doubleSpinBox_ground_electrode_horizontal_length.setValue(0)
        self.ui.doubleSpinBox_grounding_contour_width.setValue(0)

        self.clear_results()  # Очистить данные предыдущих вычислений

        self.ui.tabWidget.setCurrentWidget(self.ui.tab_init_data)

        msg = "Форма очищена."
        self.statusBar().showMessage(msg)

    def read_settings(self):
        """Чтение настроек"""
        self.settings.beginGroup("Common")
        check_state_minimize_to_tray = self.settings.value("minimize_to_tray", False, type=bool)
        self.ui.action_minimize_to_tray.setChecked(check_state_minimize_to_tray)
        self.settings.endGroup()

        self.settings.beginGroup("Initial_data")
        mode = self.settings.value("mode", False, type=bool)
        self.ui.radioButton.setChecked(mode)
        self.ui.radioButton_2.setChecked(not mode)
        self.ui.comboBox_permissible_resistance.setCurrentIndex(
            int(self.settings.value("comboBox_permissible_resistance", 0)))
        self.ui.doubleSpinBox_permissible_resistance.setValue(
            float(self.settings.value("doubleSpinBox_permissible_resistance", 0)))
        self.ui.doubleSpinBox_natural_grounding_resistance.setValue(
            float(self.settings.value("doubleSpinBox_natural_grounding_resistance", 0)))
        self.settings.endGroup()

        self.settings.beginGroup("Soil")
        self.ui.doubleSpinBox_soil_high_level_depth.setValue(
            float(self.settings.value("doubleSpinBox_soil_high_level_depth", 0)))
        self.ui.comboBox_soil_resistivity_high.setCurrentIndex(
            int(self.settings.value("comboBox_soil_resistivity_high", 0)))
        self.ui.spinBox_soil_resistivity_high.setValue(
            float(self.settings.value("spinBox_soil_resistivity_high", 0)))
        self.ui.comboBox_soil_resistivity_low.setCurrentIndex(
            int(self.settings.value("comboBox_soil_resistivity_low", 0)))
        self.ui.spinBox_soil_resistivity_low.setValue(
            float(self.settings.value("spinBox_soil_resistivity_low", 0)))
        self.settings.endGroup()

        self.settings.beginGroup("Vertical_electrode")
        self.ui.comboBox_ground_electrode_vertical_length.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_vertical_length", 0)))
        self.ui.doubleSpinBox_ground_electrode_vertical_length.setValue(
            float(self.settings.value("doubleSpinBox_ground_electrode_vertical_length", 0)))
        self.ui.comboBox_ground_electrode_vertical_type.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_vertical_type", 0)))
        self.ui.comboBox_ground_electrode_vertical_diameter.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_vertical_diameter", 0)))
        self.ui.spinBox_ground_electrode_vertical_diameter.setValue(
            float(self.settings.value("spinBox_ground_electrode_vertical_diameter", 0)))
        self.ui.comboBox_ground_electrode_vertical_climat_coeff.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_vertical_climat_coeff", 0)))
        self.ui.doubleSpinBox_ground_electrode_vertical_climat_coeff.setValue(
            float(self.settings.value("doubleSpinBox_ground_electrode_vertical_climat_coeff", 0)))
        self.settings.endGroup()

        self.settings.beginGroup("Horizontal_electrode")
        self.ui.comboBox_ground_electrode_horizontal_width.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_horizontal_width", 0)))
        self.ui.spinBox_ground_electrode_horizontal_width.setValue(
            float(self.settings.value("spinBox_ground_electrode_horizontal_width", 0)))
        self.ui.comboBox_ground_electrode_horizontal_depth.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_horizontal_depth", 0)))
        self.ui.doubleSpinBox_ground_electrode_horizontal_depth.setValue(
            float(self.settings.value("doubleSpinBox_ground_electrode_horizontal_depth", 0)))
        self.ui.comboBox_ground_electrode_horizontal_climat_coeff.setCurrentIndex(
            int(self.settings.value("comboBox_ground_electrode_horizontal_climat_coeff", 0)))
        self.ui.doubleSpinBox_ground_electrode_horizontal_climat_coeff.setValue(
            float(self.settings.value("doubleSpinBox_ground_electrode_horizontal_climat_coeff", 0)))
        self.settings.endGroup()

        self.settings.beginGroup("Contour")
        self.ui.comboBox_contoured.setCurrentIndex(
            int(self.settings.value("comboBox_contoured", 0)))
        self.ui.spinBox_a_div_l.setValue(
            float(self.settings.value("spinBox_a_div_l", 0)))
        self.ui.spinBox_ground_electrode_vertical_number.setValue(
            float(self.settings.value("spinBox_ground_electrode_vertical_number", 1)))
        self.ui.doubleSpinBox_ground_electrode_horizontal_length.setValue(
            float(self.settings.value("doubleSpinBox_ground_electrode_horizontal_length", 0)))
        self.ui.doubleSpinBox_grounding_contour_width.setValue(
            float(self.settings.value("doubleSpinBox_grounding_contour_width", 0)))
        self.settings.endGroup()

        msg = "Загружены данные предыдущего расчёта."
        self.statusBar().showMessage(msg)

    def save_settings(self):
        """Сохранение настроек"""
        self.settings.setIniCodec("utf-8")

        self.settings.beginGroup("Common")
        self.settings.setValue("minimize_to_tray", self.ui.action_minimize_to_tray.isChecked())
        self.settings.endGroup()

        self.settings.beginGroup("Initial_data")
        self.settings.setValue("mode", self.ui.radioButton.isChecked())
        self.settings.setValue("doubleSpinBox_permissible_resistance",
                               self.ui.doubleSpinBox_permissible_resistance.valueFromText(
                                   self.ui.doubleSpinBox_permissible_resistance.text()
                               ))
        self.settings.setValue('comboBox_permissible_resistance',
                               self.ui.comboBox_permissible_resistance.currentIndex())
        self.settings.setValue("doubleSpinBox_natural_grounding_resistance",
                               self.ui.doubleSpinBox_natural_grounding_resistance.valueFromText(
                                   self.ui.doubleSpinBox_natural_grounding_resistance.text()
                               ))
        self.settings.endGroup()

        self.settings.beginGroup("Soil")
        self.settings.setValue("doubleSpinBox_soil_high_level_depth",
                               self.ui.doubleSpinBox_soil_high_level_depth.valueFromText(
                                   self.ui.doubleSpinBox_soil_high_level_depth.text()
                               ))
        self.settings.setValue("spinBox_soil_resistivity_high",
                               self.ui.spinBox_soil_resistivity_high.valueFromText(
                                   self.ui.spinBox_soil_resistivity_high.text()
                               ))
        self.settings.setValue('comboBox_soil_resistivity_high', self.ui.comboBox_soil_resistivity_high.currentIndex())
        self.settings.setValue("spinBox_soil_resistivity_low",
                               self.ui.spinBox_soil_resistivity_low.valueFromText(
                                   self.ui.spinBox_soil_resistivity_low.text()
                               ))
        self.settings.setValue('comboBox_soil_resistivity_low', self.ui.comboBox_soil_resistivity_low.currentIndex())
        self.settings.endGroup()
        #
        self.settings.beginGroup("Vertical_electrode")
        self.settings.setValue("doubleSpinBox_ground_electrode_vertical_length",
                               self.ui.doubleSpinBox_ground_electrode_vertical_length.valueFromText(
                                   self.ui.doubleSpinBox_ground_electrode_vertical_length.text()
                               ))
        self.settings.setValue('comboBox_ground_electrode_vertical_length',
                               self.ui.comboBox_ground_electrode_vertical_length.currentIndex())
        self.settings.setValue("comboBox_ground_electrode_vertical_type",
                               self.ui.comboBox_ground_electrode_vertical_type.currentIndex())
        self.settings.setValue("spinBox_ground_electrode_vertical_diameter",
                               self.ui.spinBox_ground_electrode_vertical_diameter.valueFromText(
                                   self.ui.spinBox_ground_electrode_vertical_diameter.text()
                               ))
        self.settings.setValue('comboBox_ground_electrode_vertical_diameter',
                               self.ui.comboBox_ground_electrode_vertical_diameter.currentIndex())
        self.settings.setValue("doubleSpinBox_ground_electrode_vertical_climat_coeff",
                               self.ui.doubleSpinBox_ground_electrode_vertical_climat_coeff.valueFromText(
                                   self.ui.doubleSpinBox_ground_electrode_vertical_climat_coeff.text()
                               ))
        self.settings.setValue('comboBox_ground_electrode_vertical_climat_coeff',
                               self.ui.comboBox_ground_electrode_vertical_climat_coeff.currentIndex())
        self.settings.endGroup()

        self.settings.beginGroup("Horizontal_electrode")
        self.settings.setValue("spinBox_ground_electrode_horizontal_width",
                               self.ui.spinBox_ground_electrode_horizontal_width.valueFromText(
                                   self.ui.spinBox_ground_electrode_horizontal_width.text()
                               ))
        self.settings.setValue('comboBox_ground_electrode_horizontal_width',
                               self.ui.comboBox_ground_electrode_horizontal_width.currentIndex())
        self.settings.setValue("doubleSpinBox_ground_electrode_horizontal_depth",
                               self.ui.doubleSpinBox_ground_electrode_horizontal_depth.valueFromText(
                                   self.ui.doubleSpinBox_ground_electrode_horizontal_depth.text()
                               ))
        self.settings.setValue('comboBox_ground_electrode_horizontal_depth',
                               self.ui.comboBox_ground_electrode_horizontal_depth.currentIndex())
        self.settings.setValue("doubleSpinBox_ground_electrode_horizontal_climat_coeff",
                               self.ui.doubleSpinBox_ground_electrode_horizontal_climat_coeff.valueFromText(
                                   self.ui.doubleSpinBox_ground_electrode_horizontal_climat_coeff.text()
                               ))
        self.settings.setValue('comboBox_ground_electrode_horizontal_climat_coeff',
                               self.ui.comboBox_ground_electrode_horizontal_climat_coeff.currentIndex())
        self.settings.endGroup()

        self.settings.beginGroup("Contour")
        self.settings.setValue("comboBox_contoured", self.ui.comboBox_contoured.currentIndex())
        self.settings.setValue('spinBox_a_div_l',
                               self.ui.spinBox_a_div_l.valueFromText(
                                   self.ui.spinBox_a_div_l.text()
                               ))
        self.settings.setValue('spinBox_ground_electrode_vertical_number',
                               self.ui.spinBox_ground_electrode_vertical_number.valueFromText(
                                   self.ui.spinBox_ground_electrode_vertical_number.text()
                               ))
        self.settings.setValue('doubleSpinBox_ground_electrode_horizontal_length',
                               self.ui.doubleSpinBox_ground_electrode_horizontal_length.valueFromText(
                                   self.ui.doubleSpinBox_ground_electrode_horizontal_length.text()
                               ))
        self.settings.setValue("doubleSpinBox_grounding_contour_width",
                               self.ui.doubleSpinBox_grounding_contour_width.valueFromText(
                                   self.ui.doubleSpinBox_grounding_contour_width.text()
                               ))
        self.settings.endGroup()

        msg = "Данные расчёта сохранены."
        self.statusBar().showMessage(msg)

    def read_form_data(self):
        """Считывание данных с формы"""

        # Режим вычислений
        self.ga.mode = self.ui.radioButton.isChecked()

        # Нормируемое сопротивление растеканию тока в землю (допустимое при данном грунте)
        try:
            self.ga.rдопзм = float(self.ui.doubleSpinBox_permissible_resistance.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Сопротивление естественного заземлятеля (Rе)
        try:
            self.ga.Rе = float(self.ui.doubleSpinBox_natural_grounding_resistance.value())
        except ValueError:
            msg = "Исходные данные сопротивления естественного заземлятеля введены не корректно."
            self.statusBar().showMessage(msg)

        # Толщина верхнего слоя грунта (H1)
        try:
            self.ga.H1 = float(self.ui.doubleSpinBox_soil_high_level_depth.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Удельное сопротивление верхнего слоя грунта (ρ1)
        try:
            # self.soil_resistivity_high = int(self.ui.spinBox_soil_resistivity_high.value())
            self.ga.ρ1 = int(self.ui.spinBox_soil_resistivity_high.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Удельное сопротивление нижнего слоя грунта (ρ2)
        try:
            self.ga.ρ2 = int(self.ui.spinBox_soil_resistivity_low.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Длина вертикального заземлителя (L=2-5 м)
        try:
            self.ga.Lв = float(self.ui.doubleSpinBox_ground_electrode_vertical_length.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Тип вертикального заземлителя
        try:
            self.ga.ground_electrode_vertical_type = self.ui.comboBox_ground_electrode_vertical_type.currentIndex()
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Диаметр стержня (ширина полки уголка dв)
        try:
            self.ga.dв = int(
                self.ui.spinBox_ground_electrode_vertical_diameter.value()) / 1000
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Климатический коэффициент для вертикальных электродов
        try:
            self.ga.Kв = float(self.ui.doubleSpinBox_ground_electrode_vertical_climat_coeff.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Ширина соединительной полосы (dг)
        try:
            self.ga.dг = int(
                self.ui.spinBox_ground_electrode_horizontal_width.value()) / 1000
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Глубина заложения горизонтального заземлителя (t=0,5-0,8 м) (T)
        try:
            self.ga.T = float(
                self.ui.doubleSpinBox_ground_electrode_horizontal_depth.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Климатический коэффициент для горизонтальной полосы (Kг)
        try:
            self.ga.Kг = float(self.ui.doubleSpinBox_ground_electrode_horizontal_climat_coeff.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Расположение вертикальных заземлителей
        try:
            self.ga.contoured = self.ui.comboBox_contoured.currentIndex()
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)
            self.ga.contoured = 0

        try:
            self.ga.k_Lг_to_Lв = self.ui.spinBox_a_div_l.value()
        except ValueError:
            msg = "Исходные данные отношения расстояния между вертикальными электродами к длине электрода (a/l) " \
                  "введены не корректно. "
            self.statusBar().showMessage(msg)

        try:
            self.ga.n_уточн = self.ui.spinBox_ground_electrode_vertical_number.value()
        except AttributeError:
            msg = "Исходные данные количества вертекальных электродов введены не корректно."
            self.statusBar().showMessage(msg)

        # Длина горизонтального заземлителя (A, длина контура заземления)
        try:
            self.ga.Lг_A = float(self.ui.doubleSpinBox_ground_electrode_horizontal_length.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

        # Ширина контура заземления (B, только для контурного)
        try:
            self.ga.Lг_B = float(self.ui.doubleSpinBox_grounding_contour_width.value())
        except ValueError:
            msg = "Исходные данные нормируемого значения введены не корректно."
            self.statusBar().showMessage(msg)

    def start_calculation(self):
        """Основная функция программы"""
        self.clear_results()  # Очистить данные предыдущих вычислений
        self.read_form_data()  # Считать данные с формы

        if not self.ga.rдопзм:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте нормируемое сопротивление растекания тока в землю",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        elif not self.ga.Lв:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте высоту вертикального электрода",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        elif not self.ga.dв:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте диаметр (или ширину) вертикального электрода",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        elif not self.ga.ρ1:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте удельное сопротивление верхнего слоя грунта",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        elif not self.ga.dг:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте диаметр (или ширину) горизонтального электрода",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        elif not self.ga.T:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте глубину расположения горизонтального электрода",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        elif not self.ga.Lг_A and not self.ga.Lг_B:
            self.statusBar().showMessage('Введите исходные данные.')
            dialog = QMessageBox(QMessageBox.Warning,
                                 "Сообщение",
                                 "Задайте длину горизонтального заземлителя (длину контура заземления)",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
            dialog.exec()
        else:
            try:
                self.ga.calc_R()
                if self.ga.mode:
                    self.show_results_calc()
                else:
                    self.show_results_check()

            except ValueError:
                self.statusBar().showMessage('Введите исходные данные.')
            # except Exception:
            # Заглушка для всех ошибок
            #            print('Это что ещё такое?')
            else:
                msg = "Расчёт закончен успешно."
                self.statusBar().showMessage(msg)
            finally:
                # Выбирается вкладка "Результаты"
                if self.ui.radioButton.isChecked():
                    self.ui.tabWidget.setCurrentWidget(self.ui.tab_calc_results)
                else:
                    self.ui.tabWidget.setCurrentWidget(self.ui.tab_check_results)

    def show_results_calc(self):
        try:
            self.ui.label_Ki_v_pr.setText("{:.2f}".format(self.ga.Kивзмпр))
            # self.ui.label_ground_electrode_vertical_climat_coeff.setText("{:.2f}".format(self.ga.Kг))
            self.ui.label_R_artificial.setText("{:.2f}".format(self.ga.Rи))
            self.ui.label_ro.setText("{:.2f}".format(self.ga.ρэкв))
            self.ui.label_t.setText("{:.2f}".format(self.ga.t))
            self.ui.label_R_vo.setText("{:.2f}".format(self.ga.Rво))
            self.ui.label_n_pr.setText("{0:d}".format(self.ga.nпр))
            # self.ui.label_ground_electrode_vertical_sum_resistance.setText("{:.2f}".format(self.ga.Rзв))
            self.ui.label_k_Lh_to_Lv.setText("{0:d}".format(self.ga.k_Lг_to_Lв))
            self.ui.label_h.setText("{:.1f}".format(self.ga.k_Lг_to_Lв * self.ga.Lв))
            self.ui.label_L_h.setText("{:.2f}".format(self.ga.Lг))
            self.ui.label_R_h.setText("{:.2f}".format(self.ga.Rг))
            self.ui.label_R_v.setText("{:.2f}".format(self.ga.Rв_уточн))
            self.ui.label_Ki_h.setText("{:.2f}".format(self.ga.Kигзм))
            self.ui.label_Ki_v.setText("{:.2f}".format(self.ga.Kивзм))
            self.ui.label_n.setText("{:d}".format(self.ga.n_уточн))
            self.ui.label_Rfull.setText("{:.2f}".format(self.ga.Rз))
            if self.ga.k_Lг_to_Lв >= 1:
                self.ui.label_a_div_l.setText("Выполняется")
            else:
                self.ui.label_a_div_l.setText("Не выполняется")
        except AttributeError:
            msg = 'Запустите расчёт заземляющего устройства'
            self.statusBar().showMessage(msg)

    def show_results_check(self):
        try:
            self.ui.label_R_artificial_check.setText("{:.2f}".format(self.ga.Rи))
            self.ui.label_ro_check.setText("{:.2f}".format(self.ga.ρэкв))
            self.ui.label_t_check.setText("{:.2f}".format(self.ga.t))
            self.ui.label_R_vo_check.setText("{:.2f}".format(self.ga.Rво))
            self.ui.label_Ki_v_check.setText("{:.2f}".format(self.ga.Kивзм))
            self.ui.label_R_v_check.setText("{:.2f}".format(self.ga.Rв_уточн))
            self.ui.label_k_Lh_to_Lv_check.setText("{0:d}".format(self.ga.k_Lг_to_Lв))
            self.ui.label_h_check.setText("{:.1f}".format(self.ga.k_Lг_to_Lв * self.ga.Lв))
            self.ui.label_L_h_check.setText("{:.2f}".format(self.ga.Lг))
            self.ui.label_Ki_h_check.setText("{:.2f}".format(self.ga.Kигзм))
            self.ui.label_R_h_check.setText("{:.2f}".format(self.ga.Rг))
            self.ui.label_Rfull_check.setText("{:.2f}".format(self.ga.Rз))
            if self.ga.k_Lг_to_Lв >= 1:
                self.ui.label_a_div_l_check.setText("Выполняется")
            else:
                self.ui.label_a_div_l_check.setText("Не выполняется")
            self.ui.label_result_check.setText(self.ga.result)
        except AttributeError:
            msg = 'Запустите расчёт заземляющего устройства'
            self.statusBar().showMessage(msg)

    def clear_results(self):
        """Очистка результатов вычислений"""
        self.ui.label_Ki_v_pr.setText("-")
        self.ui.label_R_artificial.setText("-")
        self.ui.label_ro.setText("-")
        self.ui.label_t.setText("-")
        self.ui.label_R_vo.setText("-")
        self.ui.label_n_pr.setText("-")
        self.ui.label_k_Lh_to_Lv.setText("-")
        self.ui.label_h.setText("-")
        self.ui.label_L_h.setText("-")
        self.ui.label_R_h.setText("-")
        self.ui.label_R_v.setText("-")
        self.ui.label_Ki_h.setText("-")
        self.ui.label_Ki_v.setText("-")
        self.ui.label_n.setText("-")
        self.ui.label_Rfull.setText("-")
        self.ui.label_a_div_l.setText("-")
        self.ui.label_R_artificial_check.setText("-")
        self.ui.label_ro_check.setText("-")
        self.ui.label_t_check.setText("-")
        self.ui.label_R_vo_check.setText("-")
        self.ui.label_Ki_v_check.setText("-")
        self.ui.label_R_v_check.setText("-")
        self.ui.label_k_Lh_to_Lv_check.setText("-")
        self.ui.label_h_check.setText("-")
        self.ui.label_L_h_check.setText("-")
        self.ui.label_Ki_h_check.setText("-")
        self.ui.label_R_h_check.setText("-")
        self.ui.label_Rfull_check.setText("-")
        self.ui.label_a_div_l_check.setText("-")
        self.ui.label_result_check.setText("-")

    def save_report_odt(self):
        """Сохранение отчёта в файл ODT"""
        self.start_calculation()

        template = "./template/А4_Приложение.odt"
        # Ip0_3ph_max_exp = str(self.Ip0_3ph_max)
        # if not self.Ip0_3ph_max:
        #     print("Нет данных для отчёта")
        # else:
        context = dict()
        # context["Ip0_1ph_max_exp"] = "{:.2f}".format(self.Ip0_1ph_max)
        result = './report/result.odt'
        renderer = Renderer(template, context, result, overwriteExisting=True)
        renderer.run()

        msg = f"Отчёт сохранён в файле '{result}'."
        self.statusBar().showMessage(msg)

    def save_report_docx(self):
        """Сохранение отчёта в файл DOCX"""
        self.start_calculation()

        if self.ga.mode:
            template = "./template/form1_calc.docx"
        else:
            template = "./template/form2_check.docx"

        document = MailMerge(template)
        document.merge(
            ro1="{:d}".format(self.ga.ρ1),
            ro2="{:d}".format(self.ga.ρ2),
            ro="{:.0f}".format(self.ga.ρэкв),
            L_v="{:.1f}".format(self.ga.Lв),
            L_h="{:.1f}".format(self.ga.Lг),
            H1="{:.2f}".format(self.ga.H1),
            T="{:.2f}".format(self.ga.T),
            t="{:.2f}".format(self.ga.t),
            d_v="{:.1f}".format(self.ga.dв * 1000),
            b_h="{:.0f}".format(self.ga.dг * 1000),
            R_i="{:.2f}".format(self.ga.Rи),
            R_vo="{:.2f}".format(self.ga.Rво),
            R_v="{:.2f}".format(self.ga.Rв_уточн),
            R_h="{:.2f}".format(self.ga.Rг),
            # R_v="{:.2f}".format(self.ga.Rв_уточн),
            Ki_v="{:.2f}".format(self.ga.Kивзм),
            Ki_h="{:.2f}".format(self.ga.Kигзм),
            k1="{:.2f}".format(self.ga.Kв),
            k2="{:.2f}".format(self.ga.Kг),
            n_pr="{:d}".format(self.ga.nпр),
            n="{:d}".format(self.ga.n_уточн),
            h="{:.2f}".format(self.ga.k_Lг_to_Lв * self.ga.Lв),
            result=self.ga.result,
        )
        result = './report/result.docx'
        document.write(result)

        msg = f"Отчёт сохранён в файле '{result}'."
        self.statusBar().showMessage(msg)

    @QtCore.pyqtSlot()
    def open_file_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Считать данные из файла", "",
                                                  "INI Files (*.ini)", options=options)
        if fileName:
            self.settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
            self.settings.setIniCodec("utf-8")
            self.read_settings()

    @QtCore.pyqtSlot()
    def save_file_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить файл с текущими данными", "",
                                                  "INI Files (*.ini)", options=options)
        if fileName:
            self.settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
            self.save_settings()

    @QtCore.pyqtSlot()
    def show_about_window(self):
        """Отображение окна сведений о программе"""
        return QMessageBox.about(self,
                                 "О программе",
                                 "Программа для расчёта заземляющих устройств\n" \
                                 "Версия 1.0")

    @QtCore.pyqtSlot()
    def show_aboutqt_window(self):
        """Отображение окна сведений о библиотеке Qt"""
        return QMessageBox.aboutQt(self)

    @QtCore.pyqtSlot()
    def show_db_window(self):
        self.dbwindow = dbwindow.DBWindow()
        self.dbwindow.show()


if __name__ == "__main__":
    # QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)  # pylint: disable=invalid-name
    myapp = MainWindow("last_values.ini")
    myapp.show()
    sys.exit(app.exec_())

# TODO Добавить чертёж ЗУ на форму
# TODO Добавить проверку на электродинамическую стойкость
