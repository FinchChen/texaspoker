import random

class dealer(object):

    def __init__(self):

        self.initDECK = [0,1,2,3,4,5,6,7,8,9,10,11,12] * 4

        tmp_deck = self.initDECK
        random.shuffle(tmp_deck)
        self.Deck = tmp_deck

        return

    def dealHandCards(self):

        Hand1 = self.Deck[:2]
        Hand1.sort(reverse=True)
        del self.Deck[:2]

        return Hand1

    def dealBoradCards(self):

        Boradcards = self.Deck[:3]
        del self.Deck[:3]
        Boradcards.sort(reverse=True)

        return Boradcards
    
    def dealTwoMoreCards(self):

        cards = self.Deck[:2]
        cards.sort(reverse=True)
        del self.Deck[:2]

        return cards