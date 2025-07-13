import cv2

class CameraStream:
    def __init__(self, cam_index=0, width=640, height=480):
        self.cam_index = cam_index
        self.width = width
        self.height = height
        self.cap = None

    def start_stream(self):
        try:
            self.cap = cv2.VideoCapture(self.cam_index)
            if not self.cap.isOpened():
                raise RuntimeError(f"Kamera {self.cam_index} konnte nicht geöffnet werden.")
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            print("Stream gestartet. Drücke 'q' zum Beenden.")
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Kein Frame erhalten, beende Stream.")
                    break

                cv2.imshow("Kamera Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Stream beendet vom Nutzer.")
                    break

        except Exception as e:
            print(f"Fehler im Stream: {e}")

        finally:
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()