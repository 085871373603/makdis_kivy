"""Design tokens — setara dengan variabel ``:root`` pada CSS versi HTML."""

from kivy.utils import get_color_from_hex as hx

# Brand
PRIMARY = hx("#e51b23")
PRIMARY_DARK = hx("#c9151d")
PRIMARY_LIGHT = hx("#fff0f0")
PRIMARY_GLOW = (229 / 255, 27 / 255, 35 / 255, 0.12)
HEADER_START = hx("#ed2028")
HEADER_END = hx("#d9151e")

# Surface
BACKGROUND = hx("#f4f6f9")
SURFACE = hx("#ffffff")
SURFACE_DOWN = hx("#fafbfc")
WHITE = (1, 1, 1, 1)

# Text
TEXT = hx("#202631")
TEXT_SECONDARY = hx("#64748b")
TEXT_MUTED = hx("#94a3b8")
PLACEHOLDER = hx("#aab2be")

# Border & misc
BORDER = hx("#e8ebf0")
BORDER_DOWN = hx("#f5c5c7")
ARROW_BG = hx("#f6f7f9")
DIVIDER = hx("#e1e5eb")

# Input
INPUT_BG = hx("#f9fafb")
INPUT_BORDER = hx("#dfe3e8")

# Buttons
BTN_CANCEL_BG = hx("#f0f2f5")
BTN_CANCEL_BG_DOWN = hx("#e2e6eb")
BTN_CANCEL_TEXT = hx("#475569")
BLUE = hx("#005eaa")
BLUE_DARK = hx("#004c89")
BLUE_LIGHT = hx("#eaf3ff")

# Overlay / toast
OVERLAY = (15 / 255, 23 / 255, 42 / 255, 0.65)
TOAST_BG = (30 / 255, 41 / 255, 59 / 255, 0.94)
