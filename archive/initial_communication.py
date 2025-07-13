import serial
import serial.tools.list_ports
import cv2
import subprocess
import re
import platform
import os

try:
    import wmi
except ImportError:
    wmi = None

class InitialCommunication:
    def __init__(self,
                 cnc_cmds=None,
                 cnc_baudrate=115200,
                 cnc_timeout=0.1,
                 max_cam_index=3,
                 ffmpeg_path=r"C:\\Users\\Chris\\Documents\\Projekt\\Libs\\ffmpeg_build\\bin\\ffmpeg.exe"):
        self.cnc_cmds = cnc_cmds or ['M115']
        self.cnc_baudrate = cnc_baudrate
        self.cnc_timeout = cnc_timeout
        self.max_cam_index = max_cam_index
        self.ffmpeg_exe = ffmpeg_path

    # --- CNC ---

    def get_serial_port_info(self):
        ports = serial.tools.list_ports.comports()
        result = []
        for p in ports:
            vid_pid = f"{p.vid:04X}:{p.pid:04X}" if p.vid and p.pid else "Unknown"
            result.append((p.device, p.description, vid_pid))
        return result

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

    # --- Cameras via FFmpeg ---

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
            print(f"Error retrieving camera names: {e}")
            return {}

    # --- Cameras via WMI (Windows) ---

    def get_cameras_wmi(self):
        if platform.system() != "Windows" or wmi is None:
            return []

        c = wmi.WMI()
        cams = []
        for device in c.Win32_PnPEntity():
            if device.Name and ("camera" in device.Name.lower() or "webcam" in device.Name.lower()):
                cams.append({
                    "Name": device.Name,
                    "DeviceID": device.DeviceID
                })
        return cams

    # --- Combine OpenCV and WMI camera names ---

    def find_cameras_with_wmi_names(self):
        wmi_cams = self.get_cameras_wmi()
        wmi_names = [cam['Name'] for cam in wmi_cams]

        available_cams = []
        for i in range(self.max_cam_index):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    if i < len(wmi_names):
                        name = wmi_names[i]
                    else:
                        name = f"{i} (ID unknown): Unknown device {i}"
                    available_cams.append((i, name))
                cap.release()
        return available_cams

    # --- User selection ---

    def user_select(self, options, prompt, allow_none=False):
        if allow_none:
            options = ['None'] + options

        if not options:
            print("No options found.")
            return None

        print(prompt)
        for idx, option in enumerate(options):
            print(f"{idx}: {option}")
        while True:
            selection = input(f"Select a number (0-{len(options)-1}): ")
            if selection.isdigit():
                selection = int(selection)
                if 0 <= selection < len(options):
                    if allow_none and selection == 0:
                        return None
                    return options[selection]
            print("Invalid input, please try again.")

    # --- Main device selection ---

    def select_devices(self):
        # Show available serial ports
        serial_ports_info = self.get_serial_port_info()
        serial_port_options = [f"{port} - {desc} (VID:PID={vidpid})" for port, desc, vidpid in serial_ports_info]

        selected_cnc = None
        if serial_port_options:
            selected_port = self.user_select(serial_port_options, "Available serial ports:", allow_none=True)
            if selected_port:
                port = selected_port.split()[0]
                print(f"Checking if port {port} is a CNC device...")
                if self.is_cnc_port(port):
                    print(f"Port {port} is a CNC device.")
                    selected_cnc = port
                else:
                    print(f"Port {port} is not a CNC device or not responding.")
            else:
                print("No CNC device selected.")
        else:
            print("No serial ports found.")

        # Camera selection with WMI names
        camera_options = self.find_cameras_with_wmi_names()
        camera_option_strings = [f"{idx}: {name}" for idx, name in camera_options]

        selected_cam_index = None
        if camera_option_strings:
            user_choice = self.user_select(camera_option_strings, "Available cameras:", allow_none=True)
            if user_choice:
                selected_cam_index = int(user_choice.split(":")[0])
        else:
            print("No cameras found.")

        return selected_cnc, selected_cam_index