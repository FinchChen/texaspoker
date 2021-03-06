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
        self.preStack = 0
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

        self.pot = totalPOT
        self.previousBet = self.betAmount
        self.needToBet = totalBET - self.previousBet
        self.betAmount = self.needToBet
        self.decision = 'call'
        if self.betAmount < self.minbet and self.previousBet == 0:
            self.betAmount = self.minbet
        if self.money < self.minbet * 4 or self.needToBet > self.money:
            self.decision = 'All-in'
            self.betAmount = self.money
            self.money = 0
        else:
            self.money -= self.betAmount

        print self.name,self.convert(self.hand),self.decision,self.betAmount,self.pot,self.money

        return self.decision
    
    def reRaiseDecision(self):

        self.decision = 'fold'

        print self.name,self.convert(self.hand),self.decision,self.betAmount,'pot:',self.pot,'money:',self.money

        return self.decision


    def addPosition(self,position):

        self.position = ''
        
        return

    def startHand(self):

        self.decision = 'call'
        self.betAmount = self.minbet

        if self.position == 'Utg':
            self.betAmount = 0

        if self.money < self.minbet * 4:
            self.decision = 'All-in'
            self.betAmount = self.money
            self.money = 0
        else:
            self.money -= self.betAmount
        
        print self.name,self.convert(self.hand),self.decision,self.betAmount,'pot:',self.pot,'money:',self.money

        return self.decision

    def makeDecision(self):

        # standard robot, decided by position, if back and no raise then raise(bluff)
        # if got one pair or above then raise 1/2 pot

        self.decision = 'check'
        self.betAmount = 0

        if self.money < self.minbet * 4:
            self.decision = 'All-in'
            self.betAmount = self.money
            self.money = 0

        print self.name,self.convert(self.hand),self.decision,self.betAmount,'pot:',self.pot,'money:',self.money

        return self.decision

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

        if types == 666:
            print cards, best
        strength = self.calaulate_hand_strength(best,types)

        return best,types,strength

    def calaulate_hand_strength(self,cards,types):
        
        strength = hex(types * 16 ** 5 + cards[0] * 16 ** 4 + cards[1] * 16 ** 3 + cards[2] * 16 **2 + cards[3] * 16 + cards[4])
        # print hex(cards[0] * 16 ** 4 + cards[1] * 16 ** 3 + cards[2] * 16 **2 + cards[3] * 16 + cards[4])
        return strength
