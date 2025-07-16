# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUILayoutnnTekk.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1177, 881)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.device_group = QGroupBox(self.widget)
        self.device_group.setObjectName(u"device_group")
        self.device_group.setGeometry(QRect(850, 0, 301, 131))
        self.formLayoutWidget = QWidget(self.device_group)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 20, 281, 62))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.port_dropdown = QComboBox(self.formLayoutWidget)
        self.port_dropdown.setObjectName(u"port_dropdown")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.port_dropdown)

        self.cam_dropdown = QComboBox(self.formLayoutWidget)
        self.cam_dropdown.setObjectName(u"cam_dropdown")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cam_dropdown)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.connect_button = QPushButton(self.device_group)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setGeometry(QRect(10, 90, 131, 31))
        self.stop_button = QPushButton(self.device_group)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(160, 90, 131, 31))
        self.cnc_move_group = QGroupBox(self.widget)
        self.cnc_move_group.setObjectName(u"cnc_move_group")
        self.cnc_move_group.setGeometry(QRect(850, 130, 301, 401))
        self.btn_x_pos = QPushButton(self.cnc_move_group)
        self.btn_x_pos.setObjectName(u"btn_x_pos")
        self.btn_x_pos.setGeometry(QRect(30, 170, 61, 61))
        self.cnc_button = QPushButton(self.cnc_move_group)
        self.cnc_button.setObjectName(u"cnc_button")
        self.cnc_button.setGeometry(QRect(110, 160, 81, 81))
        self.btn_x_neg = QPushButton(self.cnc_move_group)
        self.btn_x_neg.setObjectName(u"btn_x_neg")
        self.btn_x_neg.setGeometry(QRect(210, 170, 61, 61))
        self.btn_y_pos = QPushButton(self.cnc_move_group)
        self.btn_y_pos.setObjectName(u"btn_y_pos")
        self.btn_y_pos.setGeometry(QRect(120, 80, 61, 61))
        self.btn_y_neg = QPushButton(self.cnc_move_group)
        self.btn_y_neg.setObjectName(u"btn_y_neg")
        self.btn_y_neg.setGeometry(QRect(120, 260, 61, 61))
        self.btn_z_pos = QPushButton(self.cnc_move_group)
        self.btn_z_pos.setObjectName(u"btn_z_pos")
        self.btn_z_pos.setGeometry(QRect(220, 80, 61, 61))
        self.btn_z_neg = QPushButton(self.cnc_move_group)
        self.btn_z_neg.setObjectName(u"btn_z_neg")
        self.btn_z_neg.setGeometry(QRect(220, 260, 61, 61))
        self.btn_focus_pos = QPushButton(self.cnc_move_group)
        self.btn_focus_pos.setObjectName(u"btn_focus_pos")
        self.btn_focus_pos.setGeometry(QRect(60, 350, 75, 41))
        self.btn_focus_neg = QPushButton(self.cnc_move_group)
        self.btn_focus_neg.setObjectName(u"btn_focus_neg")
        self.btn_focus_neg.setGeometry(QRect(170, 350, 75, 41))
        self.horizontalLayoutWidget = QWidget(self.cnc_move_group)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 20, 281, 51))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.step_label = QLabel(self.horizontalLayoutWidget)
        self.step_label.setObjectName(u"step_label")

        self.horizontalLayout.addWidget(self.step_label)

        self.step_input = QLineEdit(self.horizontalLayoutWidget)
        self.step_input.setObjectName(u"step_input")

        self.horizontalLayout.addWidget(self.step_input)

        self.serial_terminal = QGroupBox(self.widget)
        self.serial_terminal.setObjectName(u"serial_terminal")
        self.serial_terminal.setGeometry(QRect(0, 530, 1151, 271))
        self.response_box = QTextEdit(self.serial_terminal)
        self.response_box.setObjectName(u"response_box")
        self.response_box.setGeometry(QRect(10, 20, 1131, 181))
        self.horizontalLayoutWidget_2 = QWidget(self.serial_terminal)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 200, 401, 71))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.command_label = QLabel(self.horizontalLayoutWidget_2)
        self.command_label.setObjectName(u"command_label")

        self.horizontalLayout_2.addWidget(self.command_label)

        self.command_input = QLineEdit(self.horizontalLayoutWidget_2)
        self.command_input.setObjectName(u"command_input")
        self.command_input.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.command_input)

        self.btn_send = QPushButton(self.horizontalLayoutWidget_2)
        self.btn_send.setObjectName(u"btn_send")

        self.horizontalLayout_2.addWidget(self.btn_send)

        self.video_stream = QGroupBox(self.widget)
        self.video_stream.setObjectName(u"video_stream")
        self.video_stream.setGeometry(QRect(0, 0, 841, 531))
        self.video_label = QLabel(self.video_stream)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(20, 29, 800, 480))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1177, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.device_group.setTitle(QCoreApplication.translate("MainWindow", u"Device Selection", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Camera :", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"CNC Port :", None))
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop Camera", None))
        self.cnc_move_group.setTitle(QCoreApplication.translate("MainWindow", u"Control", None))
        self.btn_x_pos.setText(QCoreApplication.translate("MainWindow", u"+X", None))
        self.cnc_button.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_x_neg.setText(QCoreApplication.translate("MainWindow", u"-X", None))
        self.btn_y_pos.setText(QCoreApplication.translate("MainWindow", u"+Y", None))
        self.btn_y_neg.setText(QCoreApplication.translate("MainWindow", u"-Y", None))
        self.btn_z_pos.setText(QCoreApplication.translate("MainWindow", u"UP", None))
        self.btn_z_neg.setText(QCoreApplication.translate("MainWindow", u"Down", None))
        self.btn_focus_pos.setText(QCoreApplication.translate("MainWindow", u"+Focus", None))
        self.btn_focus_neg.setText(QCoreApplication.translate("MainWindow", u"-Focus", None))
        self.step_label.setText(QCoreApplication.translate("MainWindow", u"Distance (mm)", None))
        self.serial_terminal.setTitle(QCoreApplication.translate("MainWindow", u"Serial Terminal", None))
        self.command_label.setText(QCoreApplication.translate("MainWindow", u"Bash", None))
        self.btn_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.video_stream.setTitle(QCoreApplication.translate("MainWindow", u"Video Stream", None))
        self.video_label.setText(QCoreApplication.translate("MainWindow", u"                                                                                                                   Video Output", None))
    # retranslateUi

