class dealer(object):

    # Constants
    PLAYER = 0

    # Variables
    Deck = []
    Hand1 = []
    Boradcards = []
    Type = 'High Cards'

    def __init__(self,player_num):
    
        import random

        self.PLAYER = player_num

        tmp_deck = []

        for x in range(1,14):
            for y in range(1,5):
                tmp_deck.append([x,y])

        random.shuffle(tmp_deck)
        self.Deck = tmp_deck

        self.Hand1 = self.Deck[:2]
        del self.Deck[:2]
        self.Boradcards = self.Deck[:3]
    
    def printBoradcards(self):

        print self.Boradcards
    
    def printGame(self):

        print self.convert(self.Hand1)
        print self.convert(self.Boradcards)
        print ''

    def convert(self,cards):

        vision = []

        for i in cards:

            if i[0] == 1:
                tmp = 'A'
            elif i[0] == 10:
                tmp = 'T'
            elif i[0] == 11:
                tmp = 'J'
            elif i[0] == 12:
                tmp = 'Q'
            elif i[0] == 13:
                tmp = 'K'
            else:
                tmp = str(i[0])

            if i[1] == 1:
                suit = 's'
            elif i[1] == 2:
                suit = 'h'
            elif i[1] == 3:
                suit = 'd'
            elif i[1] == 4:
                suit = 'c'
            
            vision.append(tmp+suit)
        
        return vision

    def getMyHand(self):
        return self.Hand1

    def getBorad(self):
        return self.Boradcards

    def calculateMyHand(self):

        tmp = self.Hand1+self.Boradcards

        suit = [0,0,0,0]
        number = []

        for i in tmp:
            suit[i[1]-1] += 1
            number.append(i[0])
        
        number.sort()

        for i in suit:
            if i >= 5:
                self.Type = 'flush'

        print self.Type

        return
'''
    def findRepeat(self,List):

        tmp = set(List)
        for i in tmp:
            if List.count(i) >= 2:
'''
