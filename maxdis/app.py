"""Kelas aplikasi: navigasi, dialog, mode desktop, dan indikator offline.

Padanan fungsi JavaScript pada versi HTML
-----------------------------------------
goHome()              -> MaxdisApp.go_home()
openPasswordModal()   -> MaxdisApp.on_menu_selected()  (item.locked)
verifyPassword()      -> PasswordModal.verify()
openDesktopModal()    -> MaxdisApp.on_menu_selected()  (item.action == "desktop")
switchToDesktop()     -> MaxdisApp.switch_to_desktop()
openDevModal()        -> MaxdisApp.show_development_notice()
updateOnlineStatus()  -> MaxdisApp._set_online()
"""

from __future__ import annotations

import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.utils import platform

from . import theme, utils
from .config import (
    APP_TITLE,
    DESKTOP_DELAY,
    DESKTOP_WIDTH,
    HOME_ROUTE,
    MENUS,
    SCREEN_MENU,
    STATUS_BAR_COLOR,
    MenuItem,
    title_for_route,
)
from .modals import DesktopModal, InfoModal, PasswordModal
from .screens import SCREEN_REGISTRY, MenuScreen, PageScreen
from .widgets import OfflineBanner

# Urutan penting: widgets.kv mendefinisikan widget yang dipakai file lain.
KV_FILES = ("widgets.kv", "modals.kv", "screens.kv")
CONNECTION_POLL_SECONDS = 5


class MaxdisApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = APP_TITLE
        self.history: list[str] = []
        self._desktop_route = ""

    # ------------------------------------------------------------------
    # Siklus hidup
    # ------------------------------------------------------------------
    def build(self):
        for name in KV_FILES:
            Builder.load_file(os.path.join(utils.KV_DIR, name))

        Window.clearcolor = theme.BACKGROUND
        Window.softinput_mode = "below_target"  # keyboard tidak menutupi input

        icon = utils.asset_path("logo-192.png")
        if icon and platform not in ("android", "ios"):
            self.icon = icon

        self.sm = ScreenManager(transition=SlideTransition(duration=0.2))
        self.sm.bind(current=self._on_screen_changed)

        self.menu_screen = MenuScreen(name=SCREEN_MENU)
        self.menu_screen.populate(MENUS, self.on_menu_selected)
        self.sm.add_widget(self.menu_screen)

        self.banner = OfflineBanner()

        root = FloatLayout()
        root.add_widget(self.sm)
        root.add_widget(self.banner)

        Window.bind(on_keyboard=self._on_keyboard)
        return root

    def on_start(self) -> None:
        utils.set_status_bar_color(STATUS_BAR_COLOR)
        self._poll_connection()
        Clock.schedule_interval(self._poll_connection, CONNECTION_POLL_SECONDS)

    def on_stop(self) -> None:
        Clock.unschedule(self._poll_connection)

    def on_pause(self) -> bool:
        return True  # izinkan aplikasi dijeda di Android

    # ------------------------------------------------------------------
    # Navigasi
    # ------------------------------------------------------------------
    def _ensure_screen(self, route: str) -> None:
        if self.sm.has_screen(route):
            return
        screen_cls = SCREEN_REGISTRY.get(route)
        if screen_cls is not None:
            screen = screen_cls(name=route)
        else:
            screen = PageScreen(name=route, title=title_for_route(route))
        self.sm.add_widget(screen)

    def navigate(self, route: str) -> None:
        """Buka layar ``route`` (padanan ``window.location.href = ...``)."""
        if route == self.sm.current:
            return
        self._ensure_screen(route)
        self.history.append(self.sm.current)
        self.sm.transition.direction = "left"
        self.sm.current = route

    def go_back(self) -> bool:
        """Kembali ke layar sebelumnya (padanan tombol Back browser)."""
        if not self.history:
            return False
        previous = self.history.pop()
        self.sm.transition.direction = "right"
        self.sm.current = previous
        return True

    def go_home(self) -> None:
        """Tombol "×" di header -> ``./index.html`` (Timer Makdis)."""
        self.navigate(HOME_ROUTE)

    def _on_keyboard(self, _window, key, *_args) -> bool:
        # 27 = ESC di desktop / tombol Back di Android.
        # Dialog yang sedang terbuka menutup dirinya lebih dulu (ModalView).
        if key != 27:
            return False
        if any(isinstance(child, ModalView) for child in Window.children):
            return False  # biarkan dialog menutup dirinya sendiri
        if self.go_back():
            return True
        if platform == "android":
            self.stop()
        return True

    def _on_screen_changed(self, _manager, current: str) -> None:
        # Mode desktop hanya berlaku selama layar desktop terbuka.
        if utils.is_desktop_mode() and current != self._desktop_route:
            utils.leave_desktop_mode()

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------
    def on_menu_selected(self, item: MenuItem) -> None:
        if item.action == "desktop":
            DesktopModal(on_confirm=lambda: self.switch_to_desktop(item)).open()
        elif item.action == "dev":
            self.show_development_notice()
        elif item.locked:
            PasswordModal(on_success=lambda: self.open_item(item)).open()
        else:
            self.open_item(item)

    def open_item(self, item: MenuItem) -> None:
        if item.action == "url":
            if not item.url:
                self.show_message("Tujuan menu tidak ditemukan.")
            elif not utils.open_url(item.url):
                self.show_message("Tautan tidak dapat dibuka di perangkat ini.")
            return
        self.navigate(item.target_route)

    def switch_to_desktop(self, item: MenuItem) -> None:
        utils.enter_desktop_mode(DESKTOP_WIDTH)
        self._desktop_route = item.target_route
        Clock.schedule_once(
            lambda _dt: self.navigate(item.target_route), DESKTOP_DELAY
        )

    # ------------------------------------------------------------------
    # Dialog informasi
    # ------------------------------------------------------------------
    def show_development_notice(self) -> None:
        InfoModal(
            glyph="cross",
            title_text="Hmmm...",
            body_text=(
                "Menu ini masih dalam tahap [b]development[/b] dan belum "
                "dapat diakses saat ini."
            ),
        ).open()

    def show_message(self, message: str, title: str = "Perhatian") -> None:
        InfoModal(glyph="cross", title_text=title, body_text=message).open()

    # ------------------------------------------------------------------
    # Status koneksi
    # ------------------------------------------------------------------
    def _poll_connection(self, *_args) -> None:
        utils.check_connection(self._set_online)

    def _set_online(self, online: bool) -> None:
        if self.banner.shown == (not online):
            return
        Logger.info("MAXDIS: koneksi %s", "online" if online else "offline")
        self.banner.shown = not online
