from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo
from PyQt6.QtWidgets import QApplication
from aqt.qt import *
from pathlib import Path


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
        self.question = QLabel()
        self.question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question.setWordWrap(True)
        self.question.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
        """)

      


        # Respuesta
        self.answer = QLabel()
        self.answer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer.setWordWrap(True)
        self.answer.hide()
        self.answer.setStyleSheet("""
            font-size: 22px;
            color: #4CAF50;
        """)

        layout.addStretch()
        layout.addWidget(self.question)
        layout.addSpacing(25)
        layout.addWidget(self.answer)
        layout.addStretch()

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
        mw.col.sched.set_due_date([self.card.id], "90-150")
        mw.col.save()
        self.next_card()
    
    def good_funct(self):
        mw.col.sched.suspend_cards([self.card.id])
        mw.col.save()
        self.next_card()



    def load_card(self):
        if self.index >= len(self.card_ids):
            self.accept()
            return

        self.card = mw.col.get_card(self.card_ids[self.index])

        self.question.setText(self.card.question())
        self.answer.setText(self.card.answer())

        self.answer.hide()
        self.showButton.show()

        for b in (self.again, self.review, self.good):
            b.hide()

    def show_answer(self):
        self.answer.show()
        self.showButton.hide()

        for b in (self.again, self.review, self.good):
            b.show()

    def next_card(self):
        self.index += 1
        self.load_card()

