# MAXDIS Store Application (Kivy)

Versi Kivy dari halaman **Menu Utama** (HTML). Tata letak, warna, alur password,
dialog mode desktop, dan indikator offline mengikuti versi HTML.

## Struktur

```
maxdis_kivy/
├── main.py              # titik masuk
├── buildozer.spec       # konfigurasi build APK
├── requirements.txt
├── assets/              # taruh semua PNG di sini
├── kv/
│   ├── widgets.kv       # tombol, kartu menu, header, input, banner offline
│   ├── modals.kv        # dialog password / info / mode desktop
│   └── screens.kv       # Menu Utama + placeholder halaman
├── maxdis/
│   ├── config.py        # daftar MENUS, password, konstanta (tanpa Kivy)
│   ├── theme.py         # warna (setara :root CSS)
│   ├── app.py           # navigasi, dialog, mode desktop, offline
│   ├── screens.py       # MenuScreen, PageScreen, register_screen()
│   ├── modals.py        # PasswordModal, InfoModal, DesktopModal
│   ├── widgets.py       # widget kustom
│   └── utils.py         # aset, buka URL, orientasi, status bar, koneksi
└── tests/test_config.py
```

## Menjalankan

```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v              # tes logika (tanpa Kivy)
```

## Build APK (Linux / WSL)

```bash
pip install buildozer cython
buildozer android debug          # hasil: bin/*.apk
buildozer android debug deploy run logcat
```

Aktifkan `icon.filename` di `buildozer.spec` setelah `assets/logo-192.png` ada.

## Padanan HTML → Kivy

| HTML / JavaScript                         | Kivy                                              |
|-------------------------------------------|---------------------------------------------------|
| `goHome()` (tombol ×) → `index.html`      | `MaxdisApp.go_home()` → layar `timer`             |
| `openPasswordModal()` / `verifyPassword()`| `PasswordModal` (trim + huruf besar, Enter, Batal)|
| `openDesktopModal()` / `switchToDesktop()`| `DesktopModal` → landscape/lebar → layar `home` setelah 0,3 dtk |
| `openDevModal()`                          | `show_development_notice()` (`action="dev"`)      |
| `updateOnlineStatus()`                    | `OfflineBanner` + cek koneksi tiap 5 detik        |
| `<meta theme-color>`                      | `utils.set_status_bar_color()` (Android)          |
| `onerror` ikon Timer                      | `MenuItem.icon_fallback`                          |
| Service Worker / `manifest.json`          | tidak dipakai (aplikasi native)                   |

## Menghubungkan halaman asli

Menu membuka layar sesuai `route`. Sebelum layar asli dibuat, tampil placeholder.

```python
# maxdis/screens.py (atau modul baru yang di-import di app.py)
@register_screen("timer")
class TimerScreen(Screen):
    ...
```

Route: `timer`, `juklak`, `sob`, `pps`, `home` (Shelftalker). Menu **Kebersihan Rak**
membuka `https://rak-nu.vercel.app` di browser perangkat.

## Mengubah menu

Edit `MENUS` di `maxdis/config.py`. Tidak perlu menyentuh KV.
Untuk menu yang belum siap: `action="dev"`. Untuk password: `locked=True`.
Password diubah lewat `ACCESS_PASSWORD`.

> Catatan keamanan: seperti di HTML, password tersimpan di dalam kode sehingga
> hanya cocok sebagai pembatas akses ringan, bukan pengamanan data.
