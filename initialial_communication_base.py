import serial
import serial.tools.list_ports
import cv2
import subprocess
import re
import platform
import os


FFMPEG_PATH = r"C:\\Users\\Chris\\Documents\\Projekt\\Libs\\ffmpeg_build\\bin\\ffmpeg.exe"


class InitialCommunication:
    def __init__(self, cnc_cmds=None, cnc_baudrate=115200, cnc_timeout=0.1, max_cam_index=3, ffmpeg_path=FFMPEG_PATH):
        self.cnc_cmds = cnc_cmds or ['M115']
        self.cnc_baudrate = cnc_baudrate
        self.cnc_timeout = cnc_timeout
        self.max_cam_index = max_cam_index
        self.ffmpeg_exe = ffmpeg_path

    # -----------------------------------------------
    # CNC
    # -----------------------------------------------
    def find_serial_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def is_cnc_port(self, port):
        try:
            with serial.Serial(port, self.cnc_baudrate, timeout=self.cnc_timeout) as ser:
                for cmd in self.cnc_cmds:
                    ser.write((cmd + '\n').encode('utf-8'))
                    response = ser.readline().decode('utf-8').strip().lower()
                    if response and "ok" in response:
                        return True
        except Exception:
            return False
        return False

    # -----------------------------------------------
    # Camera detection with names (Windows / FFmpeg only)
    # -----------------------------------------------
    def get_camera_names_windows(self):
        if platform.system() != "Windows":
            return {}

        if not os.path.isfile(self.ffmpeg_exe):
            print(f"FFmpeg not found at: {self.ffmpeg_exe}")
            return {}

        try:
            result = subprocess.run(
                [self.ffmpeg_exe, '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stderr
            pattern = r'\[dshow @ .*\]  "(.*?)"\s+\(video\)'
            matches = re.findall(pattern, output)
            return {i: name for i, name in enumerate(matches)}
        except Exception as e:
            print(f"Error while listing devices: {e}")
            return {}

    def find_cameras(self):
        available_cams = []
        camera_names = self.get_camera_names_windows()

        for i in range(self.max_cam_index):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    name = camera_names.get(i, f"Unknown device {i}")
                    available_cams.append((i, name))
                cap.release()
        return available_cams

    # -----------------------------------------------
    # Selection interface
    # -----------------------------------------------
    def user_select(self, options, prompt, allow_none=False):
        if allow_none:
            options = ['NONE'] + options

        if not options:
            print("No options found.")
            return None

        print(prompt)
        for idx, option in enumerate(options):
            print(f"{idx}: {option}")
        while True:
            selection = input(f"Select a number (0-{len(options) - 1}): ")
            if selection.isdigit():
                selection = int(selection)
                if 0 <= selection < len(options):
                    if allow_none and selection == 0:
                        return None
                    return options[selection]
            print("Invalid input. Please try again.")

    # -----------------------------------------------
    # Main entry: device scan and selection
    # -----------------------------------------------
    def select_devices(self):
        # CNC port selection
        serial_ports = self.find_serial_ports()
        selected_cnc = None
        if serial_ports:
            selected_port = self.user_select(serial_ports, "Available serial ports:", allow_none=True)
            if selected_port:
                print(f"Checking if port {selected_port} is a CNC device...")
                if self.is_cnc_port(selected_port):
                    print(f"Port {selected_port} is a CNC device.")
                    selected_cnc = selected_port
                else:
                    print(f"Port {selected_port} is not a CNC device or not responding.")
            else:
                print("No CNC device selected.")
        else:
            print("No serial ports available.")

        # Camera selection
        camera_options = self.find_cameras()
        selected_cam_index = None
        if camera_options:
            display_options = [f"{i}: {name}" for i, name in camera_options]
            user_choice = self.user_select(display_options, "Available cameras:")
            if user_choice:
                selected_cam_index = int(user_choice.split(":")[0])
        else:
            print("No cameras found.")

        return selected_cnc, selected_cam_index