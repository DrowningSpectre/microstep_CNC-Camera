# Initial Communication Module

**This project is currently in draft/early development stage.**

This Python module is part of an early-stage project aiming to develop a **microscope camera system integrated with CNC control**.  
The goal is to enable synchronized image capture and precise CNC hardware manipulation for advanced prototyping, analysis, and automation tasks.

Currently, the stable version does not utilize WMI for camera detection (Windows only), but this is planned.  
Future development will add support for both Windows and Linux platforms and include a graphical user interface (GUI).  
Further enhancements will include image analysis and AI-assisted functionalities to enhance system capabilities.

## Features

- Detects available serial ports and identifies CNC devices by sending configurable commands.
- Lists connected cameras with friendly names using FFmpeg and Windows WMI (planned).
- Provides a user-friendly console interface to select CNC serial port and camera.
- Supports integration with OpenCV for camera streaming.
- Planned: cross-platform support (Windows and Linux).
- Planned: GUI for easier device selection and control.

## Requirements

- Python 3.7+
- `pyserial`
- `opencv-python`
- `wmi` (Windows only, planned)
- FFmpeg binary accessible (configured via path in code)

## Installation

1. Clone the repository or copy the files.
2. Install dependencies:

```bash
pip install -r requirements.txt