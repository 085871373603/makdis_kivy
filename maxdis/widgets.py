"""Widget kustom. Tampilannya didefinisikan di ``kv/widgets.kv``."""

from __future__ import annotations

from kivy.animation import Animation
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from . import theme


def horizontal_gradient(start, end) -> Texture:
    """Tekstur gradien 2-piksel (kiri -> kanan) untuk header."""
    texture = Texture.create(size=(2, 1), colorfmt="rgba")
    data = bytes(
        [int(c * 255) for c in start[:3]] + [255]
        + [int(c * 255) for c in end[:3]] + [255]
    )
    texture.blit_buffer(data, colorfmt="rgba", bufferfmt="ubyte")
    texture.mag_filter = "linear"
    texture.min_filter = "linear"
    return texture


# --------------------------------------------------------------------------
# Teks & tombol
# --------------------------------------------------------------------------
class WrapLabel(Label):
    """Label yang membungkus teks dan tingginya mengikuti isi."""


class PillLabel(Label):
    """Label berbentuk pil (badge "6 MENU")."""


class FlatButton(ButtonBehavior, Label):
    """Tombol datar bersudut membulat (.btn-modal)."""

    bg_color = ColorProperty(theme.PRIMARY)
    bg_down_color = ColorProperty(theme.PRIMARY_DARK)
    fg_color = ColorProperty(theme.WHITE)


class GhostButton(ButtonBehavior, Label):
    """Tombol transparan di header (.btn-close)."""


class ArrowBadge(Widget):
    """Kotak kecil berisi chevron di kanan kartu (.menu-arrow)."""

    pressed = BooleanProperty(False)


# --------------------------------------------------------------------------
# Kartu menu
# --------------------------------------------------------------------------
class MenuIcon(FloatLayout):
    """Kotak ikon berwarna; menampilkan inisial bila gambar tidak ada."""

    source = StringProperty("")
    letter = StringProperty("")
    bg_color = ColorProperty(theme.PRIMARY_LIGHT)


class MenuCard(ButtonBehavior, BoxLayout):
    """Satu baris menu (.menu-item)."""

    title = StringProperty("")
    description = StringProperty("")
    icon_source = StringProperty("")
    icon_bg = ColorProperty(theme.PRIMARY_LIGHT)
    item = ObjectProperty(None, allownone=True)
    compact = BooleanProperty(False)  # layar < 400dp
    wide = BooleanProperty(False)     # layar >= 700dp


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
class AppHeader(BoxLayout):
    logo = StringProperty("")
    gradient = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gradient = horizontal_gradient(theme.HEADER_START, theme.HEADER_END)


# --------------------------------------------------------------------------
# Dialog
# --------------------------------------------------------------------------
class ModalCard(BoxLayout):
    """Kartu putih bersudut membulat di dalam dialog (.modal-content)."""


class RoundedInput(TextInput):
    """Input password bergaya .input-password."""


class IconBubble(Widget):
    """Ikon besar di dalam dialog, digambar dengan canvas.

    Font bawaan Kivy tidak memuat emoji, sehingga 🔒 / ❌ / 🖥️ digambar manual.
    ``glyph``: ``lock`` | ``cross`` | ``desktop``.
    """

    glyph = StringProperty("lock")
    bg_color = ColorProperty(theme.PRIMARY_LIGHT)
    fg_color = ColorProperty(theme.PRIMARY)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for prop in ("pos", "size", "glyph", "bg_color", "fg_color"):
            self.bind(**{prop: self._redraw})
        self._redraw()

    def _redraw(self, *_args) -> None:
        u = dp(1)
        cx, cy = self.center
        self.canvas.clear()
        with self.canvas:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(19)])
            Color(*self.fg_color)

            if self.glyph == "lock":
                cy -= 2 * u
                # gembok: lengkung di atas, badan di bawah menutup separuhnya
                Line(
                    rounded_rectangle=(cx - 7 * u, cy - 2 * u, 14 * u, 18 * u, 7 * u),
                    width=2.2 * u,
                )
                RoundedRectangle(
                    pos=(cx - 11 * u, cy - 13 * u),
                    size=(22 * u, 16 * u),
                    radius=[3 * u],
                )
            elif self.glyph == "desktop":
                Line(
                    rounded_rectangle=(cx - 13 * u, cy - 6 * u, 26 * u, 18 * u, 3 * u),
                    width=2 * u,
                )
                Line(points=[cx, cy - 6 * u, cx, cy - 10 * u], width=2 * u)
                Line(
                    points=[cx - 6 * u, cy - 10 * u, cx + 6 * u, cy - 10 * u],
                    width=2 * u,
                    cap="round",
                )
            else:  # cross
                Line(
                    points=[cx - 8 * u, cy - 8 * u, cx + 8 * u, cy + 8 * u],
                    width=3 * u,
                    cap="round",
                )
                Line(
                    points=[cx - 8 * u, cy + 8 * u, cx + 8 * u, cy - 8 * u],
                    width=3 * u,
                    cap="round",
                )


# --------------------------------------------------------------------------
# Indikator offline
# --------------------------------------------------------------------------
class OfflineBanner(Label):
    """Pil "OFFLINE MODE" di bawah layar (.offline-indicator)."""

    shown = BooleanProperty(False)

    def on_shown(self, _instance, value: bool) -> None:
        Animation.cancel_all(self, "opacity")
        Animation(opacity=1 if value else 0, d=0.25).start(self)
