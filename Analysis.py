import os
import json

class Analysis:
    gazeCollection = []
    wordOrder = []
    folderPath = None

    def __init__(self):
        self.gazeCollection = []
        if self.folderPath is None:
            self.folderPath = os.path.join(os.environ['APPDATA'], 'EyeTracker')

        if not os.path.exists(self.folderPath):
            os.makedirs(self.folderPath)

    def addToCollection(self, gaze):
        self.gazeCollection.append(gaze)

    def addWordToWordOrder(self, word):
        self.wordOrder.append(word)

        path = os.path.join(self.folderPath, "level1.json")

        with open(path, 'w') as fp:
            json.dump(self.wordOrder, fp)

    def printWordOrder(self):
        print(self.wordOrder)

    def print(self):
        print(self.gazeCollection)

