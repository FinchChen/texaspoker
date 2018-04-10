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
        self.Type_MAPPING = {'High card':1,'One pair':2,'Two pairs':3,'Trips':4,'Straight':5,'Full house':6,'Quads':7}
        self.R_Type_MAPPING = {'1':'High card','2':'One pair','3':'Two pairs','4':'Trips','5':'Straight','6':'Full house','7':'Quads'}

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
