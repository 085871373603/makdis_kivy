"""MAXDIS Store Application — titik masuk.

Jalankan di komputer :  python main.py
Build APK            :  buildozer android debug
"""

from kivy.config import Config
from kivy.utils import platform

# Config HARUS diatur sebelum jendela Kivy dibuat (sebelum import maxdis.app).
Config.set("kivy", "exit_on_escape", "0")  # ESC dipakai untuk "kembali"
if platform not in ("android", "ios"):
    Config.set("graphics", "width", "420")   # ukuran ponsel saat dev di PC
    Config.set("graphics", "height", "820")
    Config.set("input", "mouse", "mouse,disable_multitouch")

from maxdis.app import MaxdisApp  # noqa: E402


def main() -> None:
    MaxdisApp().run()


if __name__ == "__main__":
    main()
