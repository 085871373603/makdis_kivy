"""Tes logika non-UI (tidak membutuhkan Kivy):  python -m unittest -v"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maxdis import config  # noqa: E402


class PasswordTests(unittest.TestCase):
    def test_benar_tanpa_peduli_huruf_besar_kecil(self):
        for typed in ("1JD7", "1jd7", "1Jd7"):
            self.assertTrue(config.password_matches(typed), typed)

    def test_spasi_di_pinggir_diabaikan(self):
        self.assertTrue(config.password_matches("  1jd7  "))

    def test_salah_atau_kosong(self):
        for typed in ("", "   ", "1JD", "1JD77", "abcd"):
            self.assertFalse(config.password_matches(typed), repr(typed))


class MenuTests(unittest.TestCase):
    def test_jumlah_dan_urutan_menu(self):
        self.assertEqual(
            [m.key for m in config.MENUS],
            ["timer", "juklak", "sob", "pps", "rak", "shelftalker"],
        )

    def test_menu_yang_dikunci(self):
        locked = {m.key for m in config.MENUS if m.locked}
        self.assertEqual(locked, {"sob", "pps", "rak"})

    def test_key_unik(self):
        keys = [m.key for m in config.MENUS]
        self.assertEqual(len(keys), len(set(keys)))

    def test_rak_membuka_url(self):
        rak = next(m for m in config.MENUS if m.key == "rak")
        self.assertEqual(rak.action, "url")
        self.assertEqual(rak.url, "https://rak-nu.vercel.app")

    def test_shelftalker_mode_desktop_tanpa_password(self):
        item = next(m for m in config.MENUS if m.key == "shelftalker")
        self.assertEqual(item.action, "desktop")
        self.assertFalse(item.locked)
        self.assertEqual(item.target_route, "home")

    def test_tombol_home_menuju_timer(self):
        self.assertIn(config.HOME_ROUTE, [m.target_route for m in config.MENUS])

    def test_warna_hex_valid(self):
        for m in config.MENUS:
            self.assertRegex(m.bg, r"^#[0-9a-fA-F]{6}$")

    def test_title_for_route(self):
        self.assertEqual(config.title_for_route("home"), "Generator Shelftalker")
        self.assertEqual(config.title_for_route("tidak_ada"), "Tidak Ada")


if __name__ == "__main__":
    unittest.main()
