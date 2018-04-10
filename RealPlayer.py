class player(object):

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