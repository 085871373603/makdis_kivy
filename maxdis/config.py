"""Konfigurasi aplikasi & daftar menu.

Modul ini sengaja TIDAK meng-import Kivy supaya mudah diuji.

Setiap ``MenuItem`` menggantikan satu ``<a class="menu-item">`` di HTML:

* ``action="screen"``  -> buka layar internal (``route``; default = ``key``)
* ``action="url"``     -> buka tautan eksternal di browser (``url``)
* ``action="desktop"`` -> tampilkan dialog "Beralih ke Tampilan Desktop",
                          lalu buka ``route`` dalam mode desktop
* ``action="dev"``     -> tampilkan dialog "masih dalam tahap development"
* ``locked=True``      -> minta password lebih dulu (``openPasswordModal``)
"""

from __future__ import annotations

from dataclasses import dataclass

APP_TITLE = "Menu Utama "
APP_VERSION = "App Toko V2.5.6"
APP_COPYRIGHT = "ARNX © 2026"

# Sama dengan HTML: password dibandingkan setelah trim() + toUpperCase().
ACCESS_PASSWORD = "1JD7"

SCREEN_MENU = "menu"
# Tombol "×" di header pada HTML menuju ./index.html (= Timer Makdis).
HOME_ROUTE = "timer"

STATUS_BAR_COLOR = "#e51b23"  # <meta name="theme-color">
DESKTOP_WIDTH = 1024          # viewport width=1024 pada switchToDesktop()
DESKTOP_DELAY = 0.3           # setTimeout(..., 300)


@dataclass(frozen=True)
class MenuItem:
    key: str
    title: str
    description: str
    icon: str
    bg: str
    icon_fallback: str = ""
    locked: bool = False
    action: str = "screen"
    route: str = ""
    url: str = ""

    @property
    def target_route(self) -> str:
        return self.route or self.key


MENUS: tuple[MenuItem, ...] = (
    # ./index.html
    MenuItem(
        key="timer",
        title="Timer Makdis",
        description="Aplikasi Timer",
        icon="icon-192lama.png",
        icon_fallback="logo-192.png",
        bg="#fff0f0",
    ),
    # ./juklak.html
    MenuItem(
        key="juklak",
        title="Juklak Menu",
        description="RTD/RTE/IHB & BnS.",
        icon="logo_juklak.png",
        bg="#fff8e6",
    ),
    # ./so.html  (password)
    MenuItem(
        key="sob",
        title="SOB",
        description="SO BSPOT.",
        icon="so.png",
        bg="#eaf3ff",
        locked=True,
    ),
    # ./pps.html  (password)
    MenuItem(
        key="pps",
        title="Laporan PPS",
        description="-.",
        icon="pps.png",
        bg="#eaf8ed",
        locked=True,
    ),
    # https://rak-nu.vercel.app  (password)
    MenuItem(
        key="rak",
        title="PIC RAK",
        description="Manajemen dan monitoring kebersihan rak.",
        icon="rak.png",
        bg="#f3ecff",
        locked=True,
        action="url",
        url="https://rak-nu.vercel.app",
    ),
    # ./home.html  (dialog mode desktop)
    MenuItem(
        key="shelftalker",
        title="Generator Shelftalker",
        description=".",
        icon="label.png",
        bg="#eaf0ff",
        action="desktop",
        route="home",
    ),
)


def title_for_route(route: str) -> str:
    """Judul layar untuk sebuah route (dipakai layar placeholder)."""
    for item in MENUS:
        if item.target_route == route:
            return item.title
    return route.replace("_", " ").title()


def password_matches(typed: str, expected: str = ACCESS_PASSWORD) -> bool:
    """Padanan ``input.trim().toUpperCase() === "1JD7"``."""
    return typed.strip().upper() == expected.upper()
