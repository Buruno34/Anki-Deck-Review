from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo
from PyQt6.QtWidgets import QApplication
from aqt.qt import *
from pathlib import Path
from aqt.webview import AnkiWebView, AnkiWebViewKind
from aqt.sound import av_player, play_clicked_audio


class ReviewWidget(QDialog):
    def __init__(self, card_ids, parent=mw):
        super().__init__(parent)

        self.card_ids = card_ids
        self.index = 0

        # Load QSS
        app = QApplication.instance()
        ADDON_PATH = Path(__file__).parent
        QSS_PATH = ADDON_PATH / "estilo.qss"

        with open(Path(QSS_PATH), "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

        self.setWindowTitle("Quick Review")
        self.resize(900, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)

        # Pregunta
        self.question = AnkiWebView(parent=self, kind=AnkiWebViewKind.CARD_LAYOUT)
        self.question.setProperty("darkMode", False)  # optional; match your theme
        self.question.set_bridge_command(self._on_bridge_cmd, self)
        #self.question.setMinimumHeight(400)
        self.question.setObjectName("preguntas")
        


        self.web = AnkiWebView(parent=self, kind=AnkiWebViewKind.CARD_LAYOUT)
        self.web.setProperty("darkMode", False)  # optional; match your theme
        self.web.set_bridge_command(self._on_bridge_cmd, self)
        self.web.setMinimumHeight(400)   # ajusta a gusto

        layout.addWidget(self.question, stretch=1)
        layout.addWidget(self.web, stretch=1)

        self.showButton = QPushButton("Show Answer")
        self.showButton.clicked.connect(self.show_answer)
        layout.addWidget(self.showButton)

        self.buttonsLayout = QHBoxLayout()

        self.again = QPushButton("I Dont know")
        self.again.setShortcut("1")
        self.review = QPushButton("I know it well but i want to review in 2 to 3 months")
        self.review.setShortcut("2")
        self.good = QPushButton("I Abolutley know this")
        self.good.setShortcut("3")

        for btn in (self.again, self.review, self.good):
            btn.hide()
            self.buttonsLayout.addWidget(btn)

        layout.addLayout(self.buttonsLayout)

        self.load_card()
        self.button_action()

    def button_action(self):
        self.again.clicked.connect(self.again_funct)
        self.review.clicked.connect(self.review_funct)
        self.good.clicked.connect(self.good_funct)

    def again_funct(self):
        self.next_card()

    def review_funct(self):
        mw.col.sched.set_due_date([self.card.id], "30-90")
        mw.col.save()
        self.next_card()

    def good_funct(self):
        mw.col.sched.set_due_date([self.card.id], "150-200")
        #mw.col.sched.suspend_cards([self.card.id])
        mw.col.save()
        self.next_card()

    def _on_bridge_cmd(self, cmd: str):
       
        if cmd.startswith("play:"):
            play_clicked_audio(cmd, self.card)

    def _render_web(self, html):
        
        html = mw.prepare_card_text_for_display(html)
        
        self.web.stdHtml(
            html,
            css=["css/reviewer.css"],
            js=[
                "js/mathjax.js",
                "js/vendor/mathjax/tex-chtml-full.js",
                "js/reviewer.js",
            ],
            context=self,
        )

    def _render_question(self, html):
        html = mw.prepare_card_text_for_display(html)
        self.question.stdHtml(
            html,
            css=["css/reviewer.css"],
            js=[
                "js/mathjax.js",
                "js/vendor/mathjax/tex-chtml-full.js",
                "js/reviewer.js",
            ],
            context=self,
        )

    def load_card(self):
        # corta cualquier audio que siga sonando de la tarjeta anterior
        av_player.stop_and_clear_queue()

        if self.index >= len(self.card_ids):
            self.accept()
            return

        self.card = mw.col.get_card(self.card_ids[self.index])

        self._render_question(self.card.question())
        #self.question.setText(self.card.question())
        self._render_web(self.card.answer())

        self.web.hide()
        self.question.show()
        self.showButton.show()

        for b in (self.again, self.review, self.good):
            b.hide()

        # reproduce el audio de la pregunta (si la carta tiene autoplay)
        if self.card.autoplay():
            self.question.setPlaybackRequiresGesture(False)
            self.web.setPlaybackRequiresGesture(False)
            av_player.play_tags(self.card.question_av_tags())
        else:
            self.web.setPlaybackRequiresGesture(True)
            self.question.setPlaybackRequiresGesture(True)

    def show_answer(self):
        self.question.hide()
        self.web.show()
        self.showButton.hide()

        for b in (self.again, self.review, self.good):
            b.show()

        # reproduce el audio de la respuesta
        av_player.stop_and_clear_queue()
        if self.card.autoplay():
            av_player.play_tags(self.card.answer_av_tags())

    def next_card(self):
        av_player.stop_and_clear_queue()
        self.index += 1
        self.load_card()

    def reject(self):
        av_player.stop_and_clear_queue()
        super().reject()

    def accept(self):
        av_player.stop_and_clear_queue()
        super().accept()