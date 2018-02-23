from __future__ import division

class dealer(object):

    # Constants
    PLAYER = 0
    initDECK = [0,1,2,3,4,5,6,7,8,9,10,11,12] * 4
    MAPPING = {'A':12,'K':11,'Q':10,'J':9,'10':8,'9':7,'8':6,'7':5,'6':4,'5':3,'4':2,'3':1,'2':0}
    R_MAPPING = {'12':'A','11':'K','10':'Q','9':'J','8':'10','7':'9','6':'8','5':'7','4':'6','3':'5','2':'4','1':'3','0':'2'}
    Type_MAPPING = {'High card':0,'One pair':1,'Two pairs':2,'Trips':3,'Straight':4,'Full house':5,'Quads':6}
    R_Type_MAPPING = {'0':'High card','1':'One pair','2':'Two pairs','3':'Trips','4':'Straight','5':'Full house','6':'Quads'}
    
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
        self.Hand1.sort(reverse=True)
        del self.Deck[:2]
        self.Boradcards = self.Deck[:3]
        del self.Deck[:3]
        self.Boradcards.sort(reverse=True)

    def convert(self,cards):

        cards.sort(reverse=True)
        vision = []

        for i in cards:
            
            tmp = self.R_MAPPING[str(i)]
            vision.append(tmp)
        
        return vision
    
    def pr(self):
        
        print self.convert(self.Hand1)
        print self.convert(self.Boradcards)

    def calaulate_hold_strength(self,cards):

        strength = '??'

        if cards[0] == cards[1]:
            if cards[0] >= 10:
                strength = 'Super Strong'
            elif cards[0] >= 8:
                strength = 'Strong'
            else:
                strength = 'Opportunity'
        elif cards[0] == 12:
            if cards[1] >= 10:
                strength = 'Super Strong'
            elif cards[1] >= 8:
                strength = 'Strong'
            else:
                strength = 'Dangerous'
        elif cards[0] == 11:
            if cards[1] >= 10:
                strength = 'Strong'
            elif cards[1] >= 8:
                strength = 'Dangerous'
        elif cards[0] == 10:
            if cards[1] >= 8:
                strength = 'Opportunity'
        elif cards[0]-cards[1] == 1 and cards[1] >= 6:
            strength = 'Opportunity'
        else:
            strength = 'Weak'

        return strength

    def print_expectation(self):

        print 'Expectation:'

        for i in range(13):
            print '         ' + self.R_MAPPING[str(i)] + ': ' + format(self.Deck.count(i)/len(self.Deck),'0.2%')

    def calaulate_hand_strength(self,cards,types):

        strength = hex(types * 16 ** 5 + cards[0] * 16 ** 4 + cards[1] * 16 ** 3 + cards[2] * 16 **2 + cards[3] * 16 + cards[4])


        return strength

    def find_my_best(self,cards):

        cards.sort(reverse=True)
        unique = len(set(cards))
        length = len(cards)
        keys = []
        tmp_list = list(set(cards))
        tmp_list.sort(reverse=True)
        types = 0

        for i in tmp_list:
            if cards.count(i) >= 2:
                keys.append(i)

        if length - unique >= 3:
            for i in tmp_list:
                if cards.count(i) == 2 or cards.count(i) == 3:
                    types = 5
                    break
                elif cards.count(i) == 4:
                    types = 6
                    key6 = i
                    break
        elif unique == length - 2:
            for i in tmp_list:
                if cards.count(i) == 2:
                    types = 2
                    break
                elif cards.count(i) == 3:
                    types = 3
                    break
            if unique == 5 and tmp_list[0] - tmp_list[4] == 4:
                types = 4
                cards = tmp_list
        elif length - unique <= 1 :
            for i in range(unique-4):
                if tmp_list[i] - tmp_list[i+4] == 4:
                    types = 4
                    del tmp_list[:i]
                    break
                elif length == unique:
                    types = 0
        else:
            types = 1

        best = []

        if types == 6:
            tmp_list.remove(key6)
            best = [key6,key6,key6,key6,tmp_list[0]]
        elif types == 5:
            key2 = []
            key3 = 999
            for i in tmp_list:
                if cards.count(i) == 2:
                    key2.append(i)
                elif cards.count(i) == 3:
                    key3 = i
            key2.sort(reverse=True)
            best = [key3,key3,key3,key2[0],key2[0]]
        elif types == 4:
            best = tmp_list[:5]
        elif types == 3:
            tmp_list.remove(keys[0])
            best = keys * 3 + tmp_list[:2]
        elif types == 2:
            keys.sort(reverse=True)
            for i in keys[:2]:
                best.append(i)
                best.append(i)
            best.append(tmp_list[0])
        elif types == 1:
            tmp_list.remove(keys[0])
            best = keys * 2 + tmp_list[:3]
        elif types == 0:
            best = cards[:5]
        
        strength = self.calaulate_hand_strength(best,types)

        return best,types,strength

    def simulation(self,holds,borads):

        import random

        tmp_deck = self.Deck
        random.shuffle(tmp_deck)
        my_holds = holds
        final_borad = borads + tmp_deck[:2]
        opp_holds = tmp_deck[2:4]
        print self.find_my_best(my_holds + final_borad)
        print opp_holds , final_borad , my_holds
        print self.find_my_best(opp_holds + final_borad)
        

    
    def start(self):

        print 'Game start '

        print '\nPre-flop round'
        hand = self.convert(self.Hand1)
        print 'My hold cards: ' + hand[0] + ' ' + hand[1]
        print 'Hand strength: ' + self.calaulate_hold_strength(self.Hand1)

        print '\nFlop round'
        Boradcards = self.convert(self.Boradcards)
        print 'Community cards: ' + Boradcards[0] + ' ' + Boradcards[1] + ' ' + Boradcards[2]
        hand1 = self.convert(self.Hand1 + self.Boradcards)
        print 'My hand: ' + hand1[0] + ' ' + hand1[1] + ' ' + hand1[2] + ' ' + hand1[3] + ' ' + hand1[4]
        print 'Hand type: ' + self.R_Type_MAPPING[str(self.find_my_best(self.Hand1 + self.Boradcards)[1])]
        
        self.simulation(self.Hand1,self.Boradcards)
        
        #print 'Hand strength: '
        #print 'Hand strength: '
        #print self.calaulate_hand_strength(self.Hand1 + self.Boradcards)
        #self.print_expectation()


        #print '\nTurn round'

        #print '\nRiver round'



    
