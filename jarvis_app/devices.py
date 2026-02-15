from __future__ import annotations

import platform
import subprocess
from dataclasses import dataclass


@dataclass
class DeviceStatus:
    camera_available: bool
    projector_available: bool
    details: str


def detect_projector() -> tuple[bool, str]:
    system = platform.system().lower()
    if system == "linux":
        try:
            result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True, check=False)
            connected = [ln for ln in result.stdout.splitlines() if " connected" in ln]
            projector = any(tok in ln for ln in connected for tok in ["HDMI", "DP", "VGA"])
            return projector, f"Connected displays: {len(connected)}"
        except FileNotFoundError:
            return False, "xrandr not found"
    if system == "windows":
        try:
            from screeninfo import get_monitors

            monitors = get_monitors()
            projector = len(monitors) > 1
            return projector, f"Detected monitors: {len(monitors)}"
        except Exception as exc:
            return False, f"Monitor detection error: {exc}"
    return False, "Projector detection unsupported on this OS"


def detect_camera() -> tuple[bool, str]:
    try:
        import cv2

        cap = cv2.VideoCapture(0)
        ok = bool(cap.isOpened())
        cap.release()
        return ok, "Camera index 0 reachable" if ok else "Camera not reachable"
    except Exception as exc:
        return False, f"OpenCV unavailable: {exc}"


def detect_all() -> DeviceStatus:
    cam, cam_msg = detect_camera()
    proj, proj_msg = detect_projector()
    return DeviceStatus(camera_available=cam, projector_available=proj, details=f"{cam_msg}; {proj_msg}")
