
class Analysis:
    gazeCollection = []

    def __init__(self):
        self.gazeCollection = []

    def addToCollection(self, gaze):
        self.gazeCollection.append(gaze)

    def print(self):
        print(self.gazeCollection)

