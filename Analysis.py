
class Analysis:
    gazeCollection = []
    wordOrder = []

    def __init__(self):
        self.gazeCollection = []

    def addToCollection(self, gaze):
        self.gazeCollection.append(gaze)

    def addWordToWordOrder(self, word):
        self.wordOrder.append(word)

    def printWordOrder(self):
        print(self.wordOrder)

    def print(self):
        print(self.gazeCollection)

