"""Helper lintas-platform: aset, browser, mode desktop, status bar, koneksi."""

from __future__ import annotations

import os
import socket
import threading
from typing import Callable

from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
KV_DIR = os.path.join(BASE_DIR, "kv")

if platform == "android":
    from android.runnable import run_on_ui_thread  # type: ignore
else:

    def run_on_ui_thread(func):  # type: ignore
        return func


# --------------------------------------------------------------------------
# Aset
# --------------------------------------------------------------------------
def asset_path(*names: str) -> str:
    """Path absolut gambar pertama yang ditemukan, atau '' bila tidak ada.

    Dicari di ``assets/`` lalu di folder proyek (mirip struktur file HTML).
    Ini setara dengan ``onerror="this.src='./logo-192.png'"``: berikan nama
    fallback sebagai argumen berikutnya.
    """
    for name in names:
        if not name:
            continue
        for folder in (ASSETS_DIR, BASE_DIR):
            candidate = os.path.join(folder, name)
            if os.path.isfile(candidate):
                return candidate
    return ""


# --------------------------------------------------------------------------
# Browser
# --------------------------------------------------------------------------
def open_url(url: str) -> bool:
    """Buka URL di browser bawaan perangkat."""
    try:
        if platform == "android":
            from jnius import autoclass  # type: ignore

            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")
            activity = autoclass("org.kivy.android.PythonActivity").mActivity
            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(url))
            activity.startActivity(intent)
            return True

        import webbrowser

        return bool(webbrowser.open(url))
    except Exception as exc:  # pragma: no cover - tergantung perangkat
        Logger.error("MAXDIS: gagal membuka URL %s (%s)", url, exc)
        return False


# --------------------------------------------------------------------------
# Mode desktop  (padanan viewport width=1024 pada switchToDesktop())
# --------------------------------------------------------------------------
_SCREEN_ORIENTATION_PORTRAIT = 1
_SCREEN_ORIENTATION_SENSOR_LANDSCAPE = 6

_display = {"desktop": False, "saved_size": None}


@run_on_ui_thread
def _android_set_orientation(value: int) -> None:  # pragma: no cover
    try:
        from jnius import autoclass  # type: ignore

        activity = autoclass("org.kivy.android.PythonActivity").mActivity
        activity.setRequestedOrientation(value)
    except Exception as exc:
        Logger.error("MAXDIS: gagal mengubah orientasi (%s)", exc)


def is_desktop_mode() -> bool:
    return bool(_display["desktop"])


def enter_desktop_mode(width: int = 1024, height: int = 720) -> None:
    """Android/iOS: paksa landscape. Desktop OS: lebarkan jendela."""
    if _display["desktop"]:
        return
    _display["desktop"] = True

    if platform == "android":
        _android_set_orientation(_SCREEN_ORIENTATION_SENSOR_LANDSCAPE)
    elif platform != "ios":
        from kivy.core.window import Window

        _display["saved_size"] = tuple(Window.size)
        Window.size = (width, height)


def leave_desktop_mode() -> None:
    """Kembali ke tampilan portrait semula."""
    if not _display["desktop"]:
        return
    _display["desktop"] = False

    if platform == "android":
        _android_set_orientation(_SCREEN_ORIENTATION_PORTRAIT)
    elif platform != "ios":
        from kivy.core.window import Window

        saved = _display.get("saved_size")
        if saved:
            Window.size = saved
        _display["saved_size"] = None


# --------------------------------------------------------------------------
# Status bar  (padanan <meta name="theme-color">)
# --------------------------------------------------------------------------
@run_on_ui_thread
def _android_status_bar(color_hex: str) -> None:  # pragma: no cover
    try:
        from jnius import autoclass  # type: ignore

        Color = autoclass("android.graphics.Color")
        LayoutParams = autoclass("android.view.WindowManager$LayoutParams")
        activity = autoclass("org.kivy.android.PythonActivity").mActivity
        window = activity.getWindow()
        window.clearFlags(LayoutParams.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(Color.parseColor(color_hex))
    except Exception as exc:
        Logger.warning("MAXDIS: gagal mengubah warna status bar (%s)", exc)


def set_status_bar_color(color_hex: str) -> None:
    if platform == "android":
        _android_status_bar(color_hex)


# --------------------------------------------------------------------------
# Koneksi  (padanan navigator.onLine + event online/offline)
# --------------------------------------------------------------------------
def check_connection(
    callback: Callable[[bool], None],
    host: str = "1.1.1.1",
    port: int = 53,
    timeout: float = 2.0,
) -> None:
    """Cek koneksi di thread terpisah; ``callback(bool)`` dipanggil di UI thread."""

    def worker() -> None:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                online = True
        except OSError:
            online = False
        Clock.schedule_once(lambda _dt: callback(online), 0)

    threading.Thread(target=worker, daemon=True).start()
