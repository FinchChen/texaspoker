from __future__ import division
import time
import random

class dealer(object):

    # Constants
    PLAYER = 0
    initDECK = []
    MAPPING = {}
    R_MAPPING = {}
    Type_MAPPING = {}
    R_Type_MAPPING = {}
    
    # Variables
    Deck = []
    Hand1 = []
    Boradcards = []

    def __init__(self,player_num):
            
        import random

        self.initDECK = [0,1,2,3,4,5,6,7,8,9,10,11,12] * 4
        self.MAPPING = {'A':12,'K':11,'Q':10,'J':9,'10':8,'9':7,'8':6,'7':5,'6':4,'5':3,'4':2,'3':1,'2':0}
        self.R_MAPPING = {'12':'A','11':'K','10':'Q','9':'J','8':'10','7':'9','6':'8','5':'7','4':'6','3':'5','2':'4','1':'3','0':'2'}
        self.Type_MAPPING = {'High card':0,'One pair':1,'Two pairs':2,'Trips':3,'Straight':4,'Full house':5,'Quads':6}
        self.R_Type_MAPPING = {'0':'High card','1':'One pair','2':'Two pairs','3':'Trips','4':'Straight','5':'Full house','6':'Quads'}

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

    def r_convert(self,cards_vision):
            
        return  self.MAPPING[cards_vision]


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

    def print_expectation(self):

        print 'Expectation:'

        for i in range(13):
            print '         ' + self.R_MAPPING[str(i)] + ': ' + format(self.Deck.count(i)/len(self.Deck),'0.2%')

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

    def simulation(self,holds,borads,circles):

        import random

        win = 0
        total = 0

        for i in range(circles):

            tmp_deck = self.Deck
            random.shuffle(tmp_deck)
            my_holds = holds

            tmp = 5-len(borads)
            final_borad = borads + tmp_deck[:tmp]
            opp_holds = tmp_deck[tmp:tmp+2]

            '''
            print 'Community Cards: ' + str(final_borad)
            print 'My holds: ' + str(my_holds)
            print 'Opponent holds: ' + str(opp_holds)
            print self.find_my_best(my_holds + final_borad)
            print self.find_my_best(opp_holds + final_borad)
            '''
            if self.find_my_best(my_holds + final_borad) > self.find_my_best(opp_holds + final_borad):
                win += 1
            
            total += 1

        return win/total

    def start(self):

        print 'Game start '

        print '\nPre-flop round'
        hand = self.convert(self.Hand1)
        print 'My hold cards: ' + hand[0] + ' ' + hand[1]
        print 'Hand strength: ' + self.calaulate_hold_strength(self.Hand1)
        print 'Hand simulation: ' + format(self.simulation(self.Hand1,[],10000),'0.2%')

        print '\nFlop round'
        Boradcards = self.convert(self.Boradcards)
        print 'Community cards: ' + Boradcards[0] + ' ' + Boradcards[1] + ' ' + Boradcards[2]
        hand1 = self.convert(self.Hand1 + self.Boradcards)
        print 'My hand: ' + hand1[0] + ' ' + hand1[1] + ' ' + hand1[2] + ' ' + hand1[3] + ' ' + hand1[4]
        print 'Hand type: ' + self.R_Type_MAPPING[str(self.find_my_best(self.Hand1 + self.Boradcards)[1])]
        
        print 'Hand simulation: ' + format(self.simulation(self.Hand1,self.Boradcards,10000),'0.2%')

        #print 'Hand strength: '
        #print 'Hand strength: '
        #print self.calaulate_hand_strength(self.Hand1 + self.Boradcards)
        #self.print_expectation()


        #print '\nTurn round'

        #print '\nRiver round'

    def decision(self,holds,borads,bet,pot,opponents):
        winrate = self.simulation_outside(holds,borads,10000,opponents)
        print 'Hand simulation_outside: ' + format(winrate,'0.2%')
        potodds = self.potodds(bet,pot)
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
                print 'Raise'
        else:
            if tmp <= 29:
                print 'Call'
            else:
                print 'Raise'

    def potodds(self,bet,pot):

        return bet/(bet+pot)

    def returnrate(self,winrate,potodds):

        return winrate/potodds

    def simulation_outside(self,holds,borads,circles,opponents):

        win = 0
        total = 0

        for i in range(circles):

            tmp_deck = [0,1,2,3,4,5,6,7,8,9,10,11,12] * 4
            random.shuffle(tmp_deck)

            for x in (holds+borads):
                tmp_deck.remove(int(x))

            my_holds = holds

            tmp = 5-len(borads)
            final_borad = borads + tmp_deck[:tmp]
            del tmp_deck[:tmp]
            opp_holds = []
            for i in range(opponents):
                opp_holds.append(tmp_deck[:2])
                del tmp_deck[:2]

            '''
            print 'Community Cards: ' + str(final_borad)
            print 'My holds: ' + str(my_holds)
            print 'Opponent holds: ' + str(opp_holds)
            print self.find_my_best(my_holds + final_borad)
            print self.find_my_best(opp_holds + final_borad)
            '''

            counter = 0
            for i in opp_holds:
                if self.find_my_best(my_holds + final_borad) > self.find_my_best(i + final_borad):
                    counter += 1
                
            if counter == opponents:
                win += 1

            total += 1

        return win/total


    
