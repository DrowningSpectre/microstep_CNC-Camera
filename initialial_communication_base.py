import serial
import serial.tools.list_ports
import cv2
import subprocess
import re
import platform
import os

class InitialCommunication:
    def __init__(self,
                 cnc_cmds=None,
                 cnc_baudrate=115200,
                 cnc_timeout=3,
                 max_cam_index=3,
                 ffmpeg_path=r"C:\\Users\\Chris\\Documents\\Projekt\\Libs\\ffmpeg_build\\bin\\ffmpeg.exe",
                 debug=False):
        self.cnc_cmds = cnc_cmds or ['G28']
        self.cnc_baudrate = cnc_baudrate
        self.cnc_timeout = cnc_timeout
        self.max_cam_index = max_cam_index
        self.ffmpeg_exe = ffmpeg_path
        self.debug = debug

    def log(self, msg):
        if self.debug:
            print(msg)

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
        except Exception as e:
            self.log(f"CNC detection error on {port}: {e}")
        return False

    # --- Cameras via OpenCV + FFmpeg ---

    def get_camera_names_windows(self):
        if platform.system() != "Windows":
            return {}

        if not os.path.isfile(self.ffmpeg_exe):
            self.log(f"FFmpeg not found at: {self.ffmpeg_exe}")
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
            self.log(f"Camera listing error: {e}")
            return {}

    def find_cameras(self):
        camera_names = self.get_camera_names_windows()
        available_cams = []
        for i in range(self.max_cam_index):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    name = camera_names.get(i, f"Camera {i}")
                    available_cams.append((i, name))
                cap.release()
        return available_cams