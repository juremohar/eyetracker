

# def calculateWordCoordinates(wordWidth, wordHeight, x, y):
#     coordinates = []
#
#     # top Left
#     coordinates.append((x, y))
#
#     xTopRight = x + wordWidth
#     # top right
#     coordinates.append((xTopRight, y))
#
#     yBottomLeft = y + wordHeight
#     # bottom Left
#     coordinates.append((x, yBottomLeft))
#
#     xBottomRight = x + wordWidth
#     yBottomRight = y + wordHeight
#     # bottom right
#     coordinates.append((xBottomRight, yBottomRight))
#
#     return coordinates

def calculateWordCoordinates(wordWidth, wordHeight, x, y):
    x1 = x
    x2 = int(x) + int(wordWidth)
    y1 = y
    y2 = int(y) + int(wordHeight)

    return {
        "x1": x1,
        "x2": x2,
        "y1": y1,
        "y2": y2
    }

def isGazeOnWord(wordCoordinates, gazeX, gazeY):
    return (int(wordCoordinates["x1"]) <= int(gazeX) <= int(wordCoordinates["x2"])) and (int(wordCoordinates["y1"]) <= int(gazeY) <= int(wordCoordinates["y2"]))

def gazeOnWord(sentenceMapping, gazeX, gazeY):
    for tuple in sentenceMapping.keys():
        if tuple[0] >= gazeX and gazeX <= tuple[1]:
            return sentenceMapping[tuple]
    return None





