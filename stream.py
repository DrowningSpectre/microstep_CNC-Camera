import cv2

class CameraStream:
    def __init__(self, cam_index=0, width=640, height=480):
        self.cam_index = cam_index
        self.width = width
        self.height = height
        self.cap = None

    def start_stream(self):
        """Start the camera stream and display live video."""
        try:
            self.cap = cv2.VideoCapture(self.cam_index)
            if not self.cap.isOpened():
                raise RuntimeError(f"Camera {self.cam_index} could not be opened.")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            print("Stream started. Press 'q' to quit.")
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("No frame received. Exiting stream.")
                    break

                cv2.imshow("Camera Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Stream stopped by user.")
                    break

        except Exception as e:
            print(f"Stream error: {e}")

        finally:
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()