from PyQt5.QtWidgets import QWidget, QLabel


class UITestSentence(QWidget):
    wordMapping = {
        (387, 484): "Dolg",
        (503, 658): "stavek,",
        (674, 725): "na",
        (742, 922): "katerem",
        (941, 1036): "bom",
        (1054, 1253): "poizkušal",
        (1269, 1418): "zaznati",
        (1437, 1536): "skok"
    }

    def __init__(self, parent=None):
        super(UITestSentence, self).__init__(parent)

        self.testSentence = QLabel("Dolg stavek, na katerem bom poizkušal zaznati skok")
        self.testSentence.setStyleSheet("font-size: 50px")


