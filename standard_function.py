class robot(object):

    def __init__(self,name,money,minbet):

        self.name = name
        self.money = money
        self.minbet = minbet
        self.MAPPING = {'A':12,'K':11,'Q':10,'J':9,'10':8,'9':7,'8':6,'7':5,'6':4,'5':3,'4':2,'3':1,'2':0}
        self.R_MAPPING = {'12':'A','11':'K','10':'Q','9':'J','8':'10','7':'9','6':'8','5':'7','4':'6','3':'5','2':'4','1':'3','0':'2'}
        self.Type_MAPPING = {'High card':0,'One pair':1,'Two pairs':2,'Trips':3,'Straight':4,'Full house':5,'Quads':6}
        self.R_Type_MAPPING = {'0':'High card','1':'One pair','2':'Two pairs','3':'Trips','4':'Straight','5':'Full house','6':'Quads'}

        return

    def r_convert(self,cards_vision): # array in list eg.['A','9']

        cards_vision.sort(reverse=True)
        inner = []

        for i in cards_vision:
            
            tmp = self.MAPPING[i]
            inner.append(tmp)

        return inner
    
    def convert(self,cards): # int in list eg.[11,2]

        cards.sort(reverse=True)
        vision = []

        for i in cards:
            
            tmp = self.R_MAPPING[str(i)]
            vision.append(tmp)
        
        return vision

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
            else:
                strength = 'Weak'
        elif cards[0] == 10:
            if cards[1] >= 8:
                strength = 'Opportunity'
            else:
                strength = 'Weak'
        elif cards[0]-cards[1] == 1 and cards[1] >= 6:
            strength = 'Opportunity'
        else:
            strength = 'Weak'

        return strength

    def addHand(self,hand):

        self.hand = hand

        return

    def addPosition(self,position):

        self.oppoentNumber = position[1]-1

        if position[0] == 0:

            self.position = 'Button'

            return

        pos = float(position[0]+1) / float(position[1])

        if pos <= 1.0/3.0:

            self.position = 'Front'
        
        elif pos <= 2.0/3.0:

            self.position = 'Middle'

        else:

            self.position = 'Back'
        
        return

    def addPot(self,pot):
        
        self.pot = pot

        return

    def addMoney(self,money):

        self.money += money

        return
    
    def getMoney(self):

        return self.money

    def setBorad(self,boradCards):

        self.boradCards = boradCards

        return

    def startHand(self): # Start Hand Chart

        self.decision = 'call'
        self.betAmount = self.minbet
        self.money -= self.betAmount

        print self.name,self.convert(self.hand),self.decision,self.betAmount,self.pot,self.money

        return self.decision

    def makeDecision(self):

        

        #

        self.decision = 'raise'
        self.betAmount = self.minbet
        self.money -= self.betAmount

        print self.name,self.convert(self.hand),self.decision,self.betAmount,self.pot,self.money

        return self.decision

    def getBetAmount(self):

        return self.betAmount

    def getName(self):

        return self.name

    def getHandStrength(self):

        best,types,strength = self.find_my_best(self.hand+self.boradCards)

        return strength

    def find_my_best(self,cards):

        cards.sort(reverse=True)
        unique = len(set(cards))
        length = len(cards)
        keys = []
        tmp_list = list(set(cards))
        tmp_list.sort(reverse=True)
        types = 999

        for i in tmp_list:
            if cards.count(i) >= 2:
                keys.append(i)

        if length - unique >= 3:
            types = 666

            for i in tmp_list:
                if cards.count(i) >= 5:
                    print 'OOOOOOut of range!!!'
                elif cards.count(i) == 3:
                    if len(keys) == 1:
                        types = 3
                        break
                    elif len(keys) >= 2:
                        types = 5
                        break
                    else:
                        print 'jesus'

            for i in tmp_list:
                if cards.count(i) == 4:
                    types = 6
                    key6 = i
                    break
            
            if len(keys) == 3:
                types = 2
            
        elif unique == length - 2:
            types = 6666
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
            types = 1
            for i in range(unique-4):
                if tmp_list[i] - tmp_list[i+4] == 4:
                    types = 4
                    del tmp_list[:i]
                    break
                elif length == unique:
                    types = 0
                    break
                elif length - unique == 1:
                    types = 1
                    break
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
            if key2 == []:
                for i in tmp_list:
                    if cards.count(i) == 3:
                        key2.append(i)
                key2.sort(reverse=True)
                try:
                    best = [key2[0],key2[0],key2[0],key2[1],key2[1]]
                except:
                    print cards, types, key2, tmp_list, length, unique
            else:
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
        '''
        time.sleep(0.1)
        print types
        '''
        if types == 666:
            print cards, best
        strength = self.calaulate_hand_strength(best,types)

        return best,types,strength

    def calaulate_hand_strength(self,cards,types):
        '''
        time.sleep(0.1)
        print cards
        '''
        try:
            strength = hex(types * 16 ** 5 + cards[0] * 16 ** 4 + cards[1] * 16 ** 3 + cards[2] * 16 **2 + cards[3] * 16 + cards[4])
        except:
            print cards, types

        return strength

    def test(self):

        print self.name,self.position,self.oppoentNumber,self.hand

        return


class dealer(object):

    def __init__(self):

        import random

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