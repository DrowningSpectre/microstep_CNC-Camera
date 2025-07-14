# Microstep Control

**Status:** Draft · Early Development

**Microstep Control** is an experimental Python-based microscope camera and CNC control interface. It combines image streaming, serial CNC communication, and precise positioning into a unified GUI application. The goal is to build a flexible foundation for advanced analysis, prototyping, and automation workflows.

---

## 🔧 Project Goals

- Integrate a microscope camera with a CNC motion system
- Provide a real-time image preview using OpenCV
- Enable axis movement via GUI buttons (X/Y/Z with step size)
- Display CNC responses live without interruptive dialogs
- Prepare for AI-based image processing and control
- Cross-platform compatibility (Windows now, Linux planned)
- Future-proof modular design with serial abstraction and pluggable components

---

## 🖼️ Features (Current Stage)

- Detect connected serial ports and identify CNC boards
- Discover video capture devices using FFmpeg (Windows only for now)
- Connect and stream from selected camera using OpenCV
- Send CNC commands over serial (e.g., G28, G1, G91/G90)
- Live response feedback via console-style text box
- Step-based control for X/Y/Z axis via GUI buttons
- Adjustable step size in mm
- Modular backend design: `initial_communication_base.py`, `cnc_control.py`, `stream.py`

---

## 📦 Requirements

- Python 3.8+
- `PySide6`
- `pyserial`
- `opencv-python`
- `ffmpeg` (binary must be present and configured in code path)

**Optional (planned):**

- `wmi` (Windows-only, camera info via WMI)
- `numpy`, `pillow`, `tensorflow` (for AI and image analysis, future)

---

## 📥 Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/microstep_v.0.001.git
cd microstep_v.0.001