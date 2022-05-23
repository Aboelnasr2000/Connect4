import math


class Node:
    def __init__(self, parent, score, max_or_min):

        self.max_or_min = max_or_min
        self.parent = parent
        self.score = score
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):

        return self.children

    def printTree(self, indentation_number):  # function to print the minimax tree
        if self.score == -9223372036854775807:
            return
        else:
            if self.max_or_min:
                my_string = "MAX"
            else:
                my_string = "MIN"
            print(indentation_number * '\t', my_string, " Score: ", self.score)
        for child in self.children:
            child.printTree(indentation_number + 1)
