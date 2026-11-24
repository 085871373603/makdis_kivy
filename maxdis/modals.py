"""Dialog (ModalView). Tampilannya didefinisikan di ``kv/modals.kv``."""

from __future__ import annotations

from typing import Callable

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.modalview import ModalView

from . import theme
from .config import ACCESS_PASSWORD, password_matches


class BaseModal(ModalView):
    """Dasar semua dialog: latar gelap + kartu bersudut membulat (dari KV).

    ``ModalView`` menggambar kotak latar sendiri. Di sini dibuat transparan
    supaya hanya ``ModalCard`` yang terlihat. Nama properti overlay berbeda
    antar versi Kivy, maka dicek dulu.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.auto_dismiss = True          # klik di luar dialog = tutup
        self.background = ""
        if self.property("overlay_color", quiet=True) is not None:
            self.overlay_color = theme.OVERLAY
            self.background_color = (0, 0, 0, 0)
        else:  # Kivy lama: background_color dipakai sebagai overlay
            self.background_color = theme.OVERLAY


class PasswordModal(BaseModal):
    """Padanan #passwordModal + verifyPassword()."""

    error_text = StringProperty("")

    def __init__(
        self,
        on_success: Callable[[], None],
        expected: str = ACCESS_PASSWORD,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._on_success = on_success
        self._expected = expected

    def on_open(self) -> None:
        # setTimeout(() => input.focus(), 150)
        Clock.schedule_once(self._focus_input, 0.15)

    def _focus_input(self, _dt) -> None:
        self.ids.pw.focus = True

    def clear_error(self) -> None:
        if self.error_text:
            self.error_text = ""

    def verify(self) -> None:
        if password_matches(self.ids.pw.text, self._expected):
            callback = self._on_success
            self.dismiss()
            callback()
            return

        # Password salah: kosongkan input dulu, baru tampilkan pesan
        # (mengosongkan teks akan memicu clear_error()).
        self.ids.pw.text = ""
        self.error_text = "Password salah! Silakan coba lagi."
        self.ids.pw.focus = True


class InfoModal(BaseModal):
    """Dialog informasi satu tombol (padanan #devModal dan alert())."""

    glyph = StringProperty("cross")
    title_text = StringProperty("")
    body_text = StringProperty("")
    button_text = StringProperty("Mengerti")


class DesktopModal(BaseModal):
    """Padanan #desktopModal: konfirmasi beralih ke tampilan desktop."""

    def __init__(self, on_confirm: Callable[[], None], **kwargs):
        super().__init__(**kwargs)
        self._on_confirm = on_confirm

    def confirm(self) -> None:
        callback = self._on_confirm
        self.dismiss()
        callback()
