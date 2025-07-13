from initialial_communication_base import InitialCommunication
from cnc_control import CNCController
from stream import CameraStream

def main():
    initializer = InitialCommunication()
    cnc_port, cam_index = initializer.select_devices()

    if cnc_port:
        print(f"Selected CNC: {cnc_port}")
        cnc = CNCController(port=cnc_port)
        cnc.connect()
        cnc.send_command('G28')
        cnc.disconnect()
    else:
        print("No CNC selected.")

    if cam_index is not None:
        print(f"Selected camera: {cam_index}")
        cam_stream = CameraStream(cam_index=cam_index)
        cam_stream.start_stream()
    else:
        print("No camera selected.")

if __name__ == "__main__":
    main()