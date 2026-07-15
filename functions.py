from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo
from .ui import ReviewWidget

def on_deck_options_menu(menu: QMenu, deck_id: int) -> None:
    action = QAction("Review (quick pass)", mw)
    action.triggered.connect(lambda: start_quick_review(deck_id))
    menu.addAction(action)
    
def start_quick_review(deck_id: int) -> None:
    deck = mw.col.decks.get(deck_id)
    deck_name = deck["name"]
    card_ids = mw.col.find_cards(f'deck:"{deck_name}" is:new -is:suspended')
    if not card_ids:
        showInfo("There are no new cards to review")
        return
    dialog = ReviewWidget(card_ids)
    dialog.exec()

def on_deck_options_menu(menu: QMenu, deck_id: int) -> None:
    action = QAction("Review (quick pass)", mw)
    action.triggered.connect(lambda: start_quick_review(deck_id))
    menu.addAction(action)
