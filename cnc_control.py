import serial
import time

class CNCController:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Warte auf Initialisierung
            if self.ser.is_open:
                print(f"CNC verbunden auf {self.port}")
        except serial.SerialException as e:
            print(f"Fehler beim Verbinden mit CNC: {e}")
            self.ser = None

    def send_command(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + '\n').encode('utf-8'))
            print(f"Befehl gesendet: {cmd}")
            # Optional Antwort lesen
            response = self.ser.readline().decode('utf-8').strip()
            print(f"Antwort: {response}")
            return response
        else:
            print("Serielle Verbindung nicht geöffnet.")
            return None

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("CNC Verbindung geschlossen.")