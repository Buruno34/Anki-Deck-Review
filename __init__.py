from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo
from .ui import ReviewWidget
from .functions import on_deck_options_menu



gui_hooks.deck_browser_will_show_options_menu.append(on_deck_options_menu)