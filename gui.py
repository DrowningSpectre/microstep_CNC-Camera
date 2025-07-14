from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout,
    QComboBox, QGroupBox, QFormLayout, QLineEdit, QTextEdit,
    
    # QApplication,QMessageBox 

)
from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtGui import QImage, QPixmap

# import sys
# import time

import cv2

#from archive.stream import CameraStream

from initialial_communication_base import InitialCommunication
from cnc_control import CNCController


class InitReaderThread(QThread):
    new_line = Signal(str)

    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.running = True

    def run(self):
        while self.running and self.ser and self.ser.is_open:
            if self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    self.new_line.emit(line)
            else:
                self.msleep(50)

    def stop(self):
        self.running = False
        self.wait()


class MicroscopeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microstep Control")
        self.setGeometry(100, 100, 800, 750)

        self.comm = InitialCommunication(debug=False)
        self.cnc_controller = None
        self.cap = None
        self.reader_thread = None

        self.available_cams = []
        self.available_ports = []

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.populate_device_lists()

    def init_ui(self):
        layout = QVBoxLayout()

        device_group = QGroupBox("Device Selection")
        device_form = QFormLayout()

        self.cam_dropdown = QComboBox()
        self.port_dropdown = QComboBox()

        device_form.addRow("Camera:", self.cam_dropdown)
        device_form.addRow("CNC Port:", self.port_dropdown)

        device_group.setLayout(device_form)
        layout.addWidget(device_group)

        self.video_label = QLabel("Camera preview will appear here")
        self.video_label.setFixedHeight(480)
        layout.addWidget(self.video_label)

        self.response_box = QTextEdit()
        self.response_box.setReadOnly(True)
        self.response_box.setFixedHeight(80)
        layout.addWidget(self.response_box)

        button_layout = QHBoxLayout()
        self.connect_button = QPushButton("Connect Devices")
        self.connect_button.clicked.connect(self.handle_device_selection)

        self.cnc_button = QPushButton("Home")
        self.cnc_button.clicked.connect(self.send_cnc_command)
        self.cnc_button.setEnabled(False)

        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        self.stop_button.setEnabled(False)

        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.cnc_button)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        cnc_move_group = QGroupBox("CNC Movement Controls")
        cnc_move_layout = QVBoxLayout()

        step_layout = QHBoxLayout()
        step_label = QLabel("Step size (mm):")
        self.step_input = QLineEdit("1.0")
        step_layout.addWidget(step_label)
        step_layout.addWidget(self.step_input)
        cnc_move_layout.addLayout(step_layout)

        xyz_button_layout = QHBoxLayout()

        x_layout = QVBoxLayout()
        self.btn_x_pos = QPushButton("X+")
        self.btn_x_neg = QPushButton("X-")
        x_layout.addWidget(self.btn_x_pos)
        x_layout.addWidget(self.btn_x_neg)
        xyz_button_layout.addLayout(x_layout)

        y_layout = QVBoxLayout()
        self.btn_y_pos = QPushButton("Y+")
        self.btn_y_neg = QPushButton("Y-")
        y_layout.addWidget(self.btn_y_pos)
        y_layout.addWidget(self.btn_y_neg)
        xyz_button_layout.addLayout(y_layout)

        z_layout = QVBoxLayout()
        self.btn_z_pos = QPushButton("Z+")
        self.btn_z_neg = QPushButton("Z-")
        z_layout.addWidget(self.btn_z_pos)
        z_layout.addWidget(self.btn_z_neg)
        xyz_button_layout.addLayout(z_layout)

        cnc_move_layout.addLayout(xyz_button_layout)
        cnc_move_group.setLayout(cnc_move_layout)
        layout.addWidget(cnc_move_group)

        self.btn_x_pos.clicked.connect(lambda: self.move_axis('X', 1))
        self.btn_x_neg.clicked.connect(lambda: self.move_axis('X', -1))
        self.btn_y_pos.clicked.connect(lambda: self.move_axis('Y', 1))
        self.btn_y_neg.clicked.connect(lambda: self.move_axis('Y', -1))
        self.btn_z_pos.clicked.connect(lambda: self.move_axis('Z', 1))
        self.btn_z_neg.clicked.connect(lambda: self.move_axis('Z', -1))

        self.setLayout(layout)

    def populate_device_lists(self):
        serial_ports_info = self.comm.get_serial_port_info()
        self.available_ports = [info[0] for info in serial_ports_info]
        self.port_dropdown.clear()
        for port, desc, vidpid in serial_ports_info:
            self.port_dropdown.addItem(f"{port} - {desc} (VID:PID={vidpid})")

        cam_infos = self.comm.find_cameras()
        self.available_cams = [i for i, _ in cam_infos]
        self.cam_dropdown.clear()
        for i, name in cam_infos:
            self.cam_dropdown.addItem(f"{i}: {name}")

    def handle_device_selection(self):
        self.stop_camera()
        if self.cnc_controller:
            self.cnc_controller.disconnect()
            self.cnc_controller = None
        self.cnc_button.setEnabled(False)

        cam_index = self.cam_dropdown.currentIndex()
        if cam_index >= 0 and cam_index < len(self.available_cams):
            self.cap = cv2.VideoCapture(self.available_cams[cam_index])
            if not self.cap.isOpened():
                self.response_box.append("Could not open selected camera.")
                return
            self.timer.start(30)
            self.stop_button.setEnabled(True)
        else:
            self.cap = None

        port_index = self.port_dropdown.currentIndex()
        if port_index >= 0 and port_index < len(self.available_ports):
            port = self.available_ports[port_index]
            self.cnc_controller = CNCController(port)
            self.cnc_controller.connect()
            if self.cnc_controller.ser and self.cnc_controller.ser.is_open:
                self.reader_thread = InitReaderThread(self.cnc_controller.ser)
                self.reader_thread.new_line.connect(self.response_box.append)
                self.reader_thread.start()
                self.response_box.append(f"CNC connected on {port}. Awaiting initialization response from device...")
                self.cnc_button.setEnabled(True)
            else:
                self.response_box.append(f"Port {port} could not be opened.")
                self.cnc_controller = None
        else:
            self.cnc_controller = None

    def move_axis(self, axis, direction):
        if not self.cnc_controller:
            self.response_box.append("No CNC controller connected.")
            return

        try:
            step_size = float(self.step_input.text())
        except ValueError:
            self.response_box.append("Step size must be a valid number.")
            return

        distance = step_size * direction
        self.cnc_controller.send_command("G91")
        cmd = f"G1 {axis}{distance:.3f} F3000"
        response = self.cnc_controller.send_command(cmd)
        self.cnc_controller.send_command("G90")
        self.response_box.append(f"Move {axis}  {distance}mm   Status: {response or 'No response.'}")

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.video_label.setPixmap(pixmap)

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.timer.stop()
        self.video_label.clear()
        self.stop_button.setEnabled(False)

    def send_cnc_command(self):
        if self.cnc_controller:
            response = self.cnc_controller.send_command("G28")
            self.response_box.append(f"CNC Response: {response or 'No response.'}")
        else:
            self.response_box.append("No CNC controller connected.")

    def closeEvent(self, event):
        self.stop_camera()
        if self.reader_thread:
            self.reader_thread.stop()
        if self.cnc_controller:
            self.cnc_controller.disconnect()
        event.accept()