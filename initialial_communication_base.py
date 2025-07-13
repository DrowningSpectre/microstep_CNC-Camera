import serial
import serial.tools.list_ports
import cv2
import subprocess
import re
import platform
import os

class InitialCommunication:
    def __init__(self, cnc_cmds=None, cnc_baudrate=115200, cnc_timeout=0.1, max_cam_index=3,ffmpeg_path=r"C:\\Users\\Chris\\Documents\\Projekt\\Libs\\ffmpeg_build\\bin\\ffmpeg.exe"):
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
    # Kameras mit Namen (nur Windows / ffmpeg)
    # -----------------------------------------------
    def get_camera_names_windows(self):
        if platform.system() != "Windows":
            return {}
        
        if not os.path.isfile(self.ffmpeg_exe):
            print(f"FFmpeg nicht gefunden unter: {self.ffmpeg_exe}")
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
            print(f"Fehler beim Abrufen der Kameranamen: {e}")
            return {}

    def find_cameras(self):
        available_cams = []
        camera_names = self.get_camera_names_windows()

        for i in range(self.max_cam_index):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    name = camera_names.get(i, f"Unbekanntes Gerät {i}")
                    available_cams.append((i, name))
                cap.release()
        return available_cams

    # -----------------------------------------------
    # Auswahl
    # -----------------------------------------------
    def user_select(self, options, prompt, allow_none=False):
        if allow_none:
            options = ['Keines'] + options

        if not options:
            print("Keine Optionen gefunden.")
            return None

        print(prompt)
        for idx, option in enumerate(options):
            print(f"{idx}: {option}")
        while True:
            selection = input(f"Wähle eine Zahl (0-{len(options)-1}): ")
            if selection.isdigit():
                selection = int(selection)
                if 0 <= selection < len(options):
                    if allow_none and selection == 0:
                        return None
                    return options[selection]
            print("Ungültige Eingabe, versuche es erneut.")

    # -----------------------------------------------
    # Hauptfunktion zur Gerätesuche & Auswahl
    # -----------------------------------------------
    def select_devices(self):
        # CNC-Port Auswahl
        serial_ports = self.find_serial_ports()
        selected_cnc = None
        if serial_ports:
            selected_port = self.user_select(serial_ports, "Verfügbare serielle Ports:", allow_none=True)
            if selected_port:
                print(f"Prüfe, ob Port {selected_port} eine CNC ist...")
                if self.is_cnc_port(selected_port):
                    print(f"Port {selected_port} ist eine CNC.")
                    selected_cnc = selected_port
                else:
                    print(f"Port {selected_port} ist keine CNC oder antwortet nicht.")
            else:
                print("Keine CNC ausgewählt.")
        else:
            print("Keine seriellen Ports gefunden.")

        # Kameraauswahl
        camera_options = self.find_cameras()
        selected_cam_index = None
        if camera_options:
            display_options = [f"{i}: {name}" for i, name in camera_options]
            user_choice = self.user_select(display_options, "Verfügbare Kameras:")
            if user_choice:
                selected_cam_index = int(user_choice.split(":")[0])
        else:
            print("Keine Kameras gefunden.")

        return selected_cnc, selected_cam_index