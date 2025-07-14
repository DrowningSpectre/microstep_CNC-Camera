import serial
import time

class CNCController:
    def __init__(self, port, baudrate=115200, timeout=3):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.step_size = 1.0  # Default step size in mm

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

    def set_step_size(self, step):
        """Set the step size in millimeters for axis movements."""
        if step > 0:
            self.step_size = float(step)
            print(f"Step size set to {self.step_size} mm")
        else:
            print("Step size must be a positive number.")

    def home(self, cmd ="G28\n"):
        """Move home"""
        return self.send_command(cmd)

    def move_x(self, direction=1):
        """Move the X axis by step_size in the specified direction (+1 or -1)."""
        distance = direction * self.step_size
        cmd = f"G91\nG0 X{distance}\nG90"
        return self.send_command(cmd)

    def move_y(self, direction=1):
        """Move the Y axis by step_size in the specified direction (+1 or -1)."""
        distance = direction * self.step_size
        cmd = f"G91\nG0 Y{distance}\nG90"
        return self.send_command(cmd)

    def move_z(self, direction=1):
        """Move the Z axis by step_size in the specified direction (+1 or -1)."""
        distance = direction * self.step_size
        cmd = f"G91\nG0 Z{distance}\nG90"
        return self.send_command(cmd)