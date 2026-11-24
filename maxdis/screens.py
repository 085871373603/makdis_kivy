"""Layar aplikasi.

Menambah layar baru
-------------------
Setiap menu membuka layar yang namanya sama dengan ``route`` pada ``MENUS``.
Selama belum ada layar asli, ``PageScreen`` (placeholder) dipakai. Untuk
menghubungkan layar asli cukup daftarkan dengan decorator:

    from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
    from maxdis.screens import register_screen

    @register_screen("timer")
    class TimerScreen(Screen):
        ...
"""

from __future__ import annotations

from typing import Callable

from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen

from .config import APP_COPYRIGHT, APP_VERSION, MenuItem
from .utils import asset_path
from .widgets import MenuCard

SCREEN_REGISTRY: dict[str, type[Screen]] = {}


def register_screen(route: str):
    """Decorator: daftarkan kelas Screen untuk sebuah route."""

    def decorator(cls: type[Screen]) -> type[Screen]:
        SCREEN_REGISTRY[route] = cls
        return cls

    return decorator


class MenuScreen(Screen):
    """Halaman "Menu Utama"."""

    logo = StringProperty("")
    item_count = NumericProperty(0)
    app_version = StringProperty(APP_VERSION)
    app_copyright = StringProperty(APP_COPYRIGHT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logo = asset_path("logo-192.png")

    def populate(self, items, on_select: Callable[[MenuItem], None]) -> None:
        box = self.ids.cards
        box.clear_widgets()
        for item in items:
            card = MenuCard(
                title=item.title,
                description=item.description,
                icon_source=asset_path(item.icon, item.icon_fallback),
                icon_bg=get_color_from_hex(item.bg),
                item=item,
            )
            card.bind(on_release=lambda widget: on_select(widget.item))
            box.add_widget(card)
        self.item_count = len(items)


class PageScreen(Screen):
    """Placeholder untuk halaman yang belum dihubungkan."""

    title = StringProperty("")
    message = StringProperty(
        "Halaman ini belum dihubungkan.\n"
        "Daftarkan layar aslinya dengan @register_screen di maxdis/screens.py."
    )
