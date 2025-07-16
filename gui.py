import sys
import cv2

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtGui import QImage, QPixmap

from GUILayout import Ui_MainWindow  # Passe ggf. den Import an, je nach Dateiname deiner .ui-Python-Datei

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.comm = InitialCommunication(debug=False)
        self.cnc_controller = None
        self.cap = None
        self.reader_thread = None
        self.available_cams = []
        self.available_ports = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.setup_connections()
        self.populate_device_lists()

    def setup_connections(self):
        self.ui.connect_button.clicked.connect(self.handle_device_selection)
        self.ui.stop_button.clicked.connect(self.stop_camera)

        self.ui.cnc_button.clicked.connect(self.send_home_command)
        self.ui.btn_x_pos.clicked.connect(lambda: self.move_axis('X', 1))
        self.ui.btn_x_neg.clicked.connect(lambda: self.move_axis('X', -1))
        self.ui.btn_y_pos.clicked.connect(lambda: self.move_axis('Y', 1))
        self.ui.btn_y_neg.clicked.connect(lambda: self.move_axis('Y', -1))
        self.ui.btn_z_pos.clicked.connect(lambda: self.move_axis('Z', 1))
        self.ui.btn_z_neg.clicked.connect(lambda: self.move_axis('Z', -1))

        self.ui.btn_send.clicked.connect(self.send_custom_command)

    def populate_device_lists(self):
        serial_ports_info = self.comm.get_serial_port_info()
        self.available_ports = [info[0] for info in serial_ports_info]
        self.ui.port_dropdown.clear()
        for port, desc, vidpid in serial_ports_info:
            self.ui.port_dropdown.addItem(f"{port} - {desc} (VID:PID={vidpid})")

        cam_infos = self.comm.find_cameras()
        self.available_cams = [i for i, _ in cam_infos]
        self.ui.cam_dropdown.clear()
        for i, name in cam_infos:
            self.ui.cam_dropdown.addItem(f"{i}: {name}")

    def handle_device_selection(self):
        self.stop_camera()

        if self.cnc_controller:
            self.cnc_controller.disconnect()
            self.cnc_controller = None

        self.ui.cnc_button.setEnabled(False)

        cam_index = self.ui.cam_dropdown.currentIndex()
        if 0 <= cam_index < len(self.available_cams):
            self.cap = cv2.VideoCapture(self.available_cams[cam_index])
            if not self.cap.isOpened():
                self.ui.response_box.append("Could not open selected camera.")
                return
            self.timer.start(30)
            self.ui.stop_button.setEnabled(True)
        else:
            self.cap = None

        port_index = self.ui.port_dropdown.currentIndex()
        if 0 <= port_index < len(self.available_ports):
            port = self.available_ports[port_index]
            self.cnc_controller = CNCController(port)
            self.cnc_controller.connect()

            if self.cnc_controller.ser and self.cnc_controller.ser.is_open:
                self.reader_thread = InitReaderThread(self.cnc_controller.ser)
                self.reader_thread.new_line.connect(self.ui.response_box.append)
                self.reader_thread.start()
                self.ui.response_box.append(f"CNC connected on {port}. Awaiting initialization response from device...")
                self.ui.cnc_button.setEnabled(True)
            else:
                self.ui.response_box.append(f"Port {port} could not be opened.")
                self.cnc_controller = None
        else:
            self.cnc_controller = None

    def move_axis(self, axis, direction):
        if not self.cnc_controller:
            self.ui.response_box.append("No CNC controller connected.")
            return

        try:
            step_size = float(self.ui.step_input.text())
        except ValueError:
            self.ui.response_box.append("Step size must be a valid number.")
            return

        distance = step_size * direction
        self.cnc_controller.send_command("G91")
        cmd = f"G1 {axis}{distance:.3f} F3000"
        response = self.cnc_controller.send_command(cmd)
        self.cnc_controller.send_command("G90")
        self.ui.response_box.append(f"Move {axis} {distance}mm   Status: {response or 'No response.'}")

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.ui.video_label.setPixmap(pixmap)

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.timer.stop()
        self.ui.video_label.clear()
        self.ui.stop_button.setEnabled(False)

    def send_home_command(self):
        if self.cnc_controller:
            response = self.cnc_controller.send_command("G28")
            self.ui.response_box.append(f"CNC Response: {response or 'No response.'}")
        else:
            self.ui.response_box.append("No CNC controller connected.")

    def send_custom_command(self):
        if self.cnc_controller:
            cmd = self.ui.command_input.text().strip()
            if cmd:
                response = self.cnc_controller.send_command(cmd)
                self.ui.response_box.append(f"> {cmd}\n{response or 'No response.'}")
        else:
            self.ui.response_box.append("No CNC controller connected.")

    def closeEvent(self, event):
        self.stop_camera()
        if self.reader_thread:
            self.reader_thread.stop()
        if self.cnc_controller:
            self.cnc_controller.disconnect()
        event.accept()
