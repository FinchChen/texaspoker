class dealer(object):

    # Constants
    PLAYER = 0
    initDECK = [0,1,2,3,4,5,6,7,8,9,10,11,12] * 4

    # Variables
    Deck = []
    Hand1 = []
    Boradcards = []

    def __init__(self,player_num):
            
        import random

        self.PLAYER = player_num

        '''
        for i in range(52):
            self.initDECK.append(i)   
        '''     
        tmp_deck = self.initDECK
        random.shuffle(tmp_deck)
        self.Deck = tmp_deck

        self.Hand1 = self.Deck[:2]
        del self.Deck[:2]
        self.Boradcards = self.Deck[:3]

        print self.Hand1
        print self.Boradcards
    
