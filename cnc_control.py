import serial
import time

class CNCController:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        """Establish serial connection to the CNC device."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Wait for initialization
            if self.ser.is_open:
                print(f"CNC connected on {self.port}")
        except serial.SerialException as e:
            print(f"Error while connecting to CNC: {e}")
            self.ser = None

    def send_command(self, cmd):
        """Send a G-code or M-code command to the CNC and optionally read the response."""
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + '\n').encode('utf-8'))
            print(f"Command sent: {cmd}")
            response = self.ser.readline().decode('utf-8').strip()
            print(f"Response: {response}")
            return response
        else:
            print("Serial connection not open.")
            return None

    def disconnect(self):
        """Close the serial connection to the CNC device."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("CNC connection closed.")