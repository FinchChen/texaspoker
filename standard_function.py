from __future__ import division
import random

class robot(object):

    def __init__(self,name,money,minbet):

        self.name = name
        self.money = money
        self.minbet = minbet
        self.pot = 0
        self.hand = []
        self.boradCards = []
        self.isRaise = False
        self.betAmount = 0
        self.MAPPING = {'A':12,'K':11,'Q':10,'J':9,'10':8,'9':7,'8':6,'7':5,'6':4,'5':3,'4':2,'3':1,'2':0}
        self.R_MAPPING = {'12':'A','11':'K','10':'Q','9':'J','8':'10','7':'9','6':'8','5':'7','4':'6','3':'5','2':'4','1':'3','0':'2'}
        self.Type_MAPPING = {'High card':0,'One pair':1,'Two pairs':2,'Trips':3,'Straight':4,'Full house':5,'Quads':6}
        self.R_Type_MAPPING = {'0':'High card','1':'One pair','2':'Two pairs','3':'Trips','4':'Straight','5':'Full house','6':'Quads'}

        return

    def clean(self):

        self.pot = 0
        self.boradCards = []
        self.isRaise = False
        self.betAmount = 0
    
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

    def raiseDecision(self,totalBET,totalPOT):

        # need update

        self.pot = totalPOT
        self.previousBet = self.betAmount
        self.needToBet = totalBET - self.previousBet
        self.betAmount = self.needToBet
        self.potodds = self.needToBet / totalPOT
        if self.potodds <= 0.5:
            self.decision = 'call'
        else:
            self.decision = 'fold'

        print self.name,self.convert(self.hand),self.decision,self.betAmount,self.pot,self.money

        return self.decision

    def addPosition(self,position):

        self.oppoentNumber = position[1]-1
        

        pos = float(position[0]+1) / float(position[1])

        if pos <= 1.0/3.0:

            self.position = 'Front'
        
        elif pos <= 2.0/3.0:

            self.position = 'Middle'

        else:

            self.position = 'Back'
        
        return

    def startHand(self): # Start Hand Chart

        ###if self.position == 'Utg':
        ###   self.decision = 'call'
        ###   return self.decision

        if self.hand == [12,12] or self.hand == [11,11]: # AA and KK
            self.decision = 'raise'
        elif self.hand == [10,10]:
            self.decision = 'raise'
        elif self.hand == [12,11]:
            self.decision = 'raise'
        elif self.hand == [9,9] or self.hand == [8,8] or self.hand == [7,7]:
            self.decision = 'raise'
        elif self.hand[0] == self.hand[1] and self.hand[0] <= 6:
            self.decision = 'call'
        elif self.hand[0] == 12 and self.hand[1] >= 8:
            self.decision = 'call'
        elif self.hand[0] == 12:
            self.decision = 'call'
        elif self.hand[0] <= 11 and self.hand[0] >= 10 and self.hand[1] <= 10 and self.hand >= 9:
            self.decision = 'call'
        elif self.hand[0] - self.hand[1] == 1 and self.hand[1] >= 4:
            self.decision = 'call'
        else:
            self.decision = 'fold'

        if self.decision == 'call':
            self.betAmount = self.minbet
            if self.position == 'Utg':
                self.betAmount = 0
        elif self.decision == 'raise':
            self.betAmount = 3 * self.minbet
        elif self.decision == 'fold':
            self.betAmount = 0
            if self.position == 'Utg':
                self.decision = 'call'
        
        self.money -= self.betAmount
        
        print self.name,self.convert(self.hand),self.decision,self.betAmount,'pot:',self.pot,'money:',self.money

        return self.decision

    def makeDecision(self):

        # standard robot, decided by position, if back and no raise then raise(bluff)
        # if got one pair or above then raise 1/2 pot

        self.decision = 'call'
        self.betAmount = self.minbet
        self.money -= self.betAmount

        print self.name,self.convert(self.hand),self.decision,self.betAmount,'pot:',self.pot,'money:',self.money

        return self.decision

    def calpotodds(self,bet,pot):

        return bet/(bet+pot)

    def returnrate(self,winrate,potodds):

        return winrate/potodds

    def simulation_outside(self,circles,opponents):

        win = 0
        total = 0

        for i in range(circles):

            tmp_deck = [0,1,2,3,4,5,6,7,8,9,10,11,12] * 4
            random.shuffle(tmp_deck)

            for x in (self.hand+self.boradCards):
                tmp_deck.remove(int(x))

            my_holds = self.hand

            tmp = 5-len(self.boradCards)
            final_borad = self.boradCards + tmp_deck[:tmp]
            del tmp_deck[:tmp]
            opp_holds = []
            for i in range(opponents):
                opp_holds.append(tmp_deck[:2])
                del tmp_deck[:2]
           
            counter = 0
            for i in opp_holds:
                if self.find_my_best(my_holds + final_borad) > self.find_my_best(i + final_borad):
                    counter += 1
                
            if counter == opponents:
                win += 1

            total += 1

        return win/total

    def decisionAI(self,opponents):

        winrate = self.simulation_outside(1000,opponents)
        print 'Hand simulation_outside: ' + format(winrate,'0.2%')
        tmpbet = self.minbet if not self.isRaise else self.betAmount
        potodds = self.calpotodds(tmpbet,self.pot)
        print 'Pot odds: '+ format(potodds,'0.2%')
        returnrate = self.returnrate(float(winrate),float(potodds))
        print 'Rate of Return: ' + format(returnrate,'0.2%')
        

        tmp = random.randint(0,99)
        if returnrate < 0.8:
            if tmp <= 4:
                print 'Raise (Bluff)'
            else:
                print 'Fold'
        elif returnrate < 1:
            if tmp <= 14:
                print 'Raise (Bluff)'
            elif tmp <= 20:
                print 'Call'
            else:
                print 'Fold'
        elif returnrate < 1.3:
            if tmp <= 59:
                print 'Call'
            else:
                print 'Raise (Dangerous)'
        else:
            if tmp <= 29:
                print 'Call (Hide)'
            else:
                print 'Raise'
        
        print ''

    def getHandStrength(self):

        best,self.types,strength = self.find_my_best(self.hand+self.boradCards)

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
                        types = 4 # trips
                        break
                    elif len(keys) >= 2:
                        types = 6 # full house
                        break
                    else:
                        print 'jesus'

            for i in tmp_list:
                if cards.count(i) == 4:
                    types = 7 # quads
                    key6 = i
                    break
            
            if len(keys) == 3:
                types = 3 # two pairs
            
        elif unique == length - 2:
            types = 6666
            for i in tmp_list:
                if cards.count(i) == 2:
                    types = 3 # two pairs
                    break
                elif cards.count(i) == 3:
                    types = 4 # trips
                    break
            if unique == 5 and tmp_list[0] - tmp_list[4] == 4:
                types = 5 # straight
                cards = tmp_list
        elif length - unique <= 1 :
            types = 2 # one pair
            for i in range(unique-4):
                if tmp_list[i] - tmp_list[i+4] == 4:
                    types = 5 # straight
                    del tmp_list[:i]
                    break
                elif length == unique:
                    types = 1 # high card
                    #break
                elif length - unique == 1:
                    types = 2 # one pair
                    #break
        else:
            types = 2 # one pair

        best = []

        if types == 7:
            tmp_list.remove(key6)
            best = [key6,key6,key6,key6,tmp_list[0]]
        elif types == 6:
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
        elif types == 5:
            best = tmp_list[:5]
        elif types == 4:
            tmp_list.remove(keys[0])
            best = keys * 3 + tmp_list[:2]
        elif types == 3:
            keys.sort(reverse=True)
            for i in keys[:2]:
                best.append(i)
                best.append(i)
            best.append(tmp_list[0])
        elif types == 2:
            tmp_list.remove(keys[0])
            best = keys * 2 + tmp_list[:3]
        elif types == 1:
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
        
        strength = hex(types * 16 ** 5 + cards[0] * 16 ** 4 + cards[1] * 16 ** 3 + cards[2] * 16 **2 + cards[3] * 16 + cards[4])
        # print hex(cards[0] * 16 ** 4 + cards[1] * 16 ** 3 + cards[2] * 16 **2 + cards[3] * 16 + cards[4])
        return strength


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