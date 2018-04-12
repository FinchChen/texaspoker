import CallRobot
import Dealer
import FoldRobot
import StandardRobot
import RandomRobot
import AI_V1
import xlsxwriter
import time


class test(object):

    def __init__(self):

        self.data = [[],[],[],[],[],[],[],[]]
        self.counter = 0

        self.minbet = 100
        self.ante = 50
        self.initStack = 20000
        self.robot1 = CallRobot.robot('1 call robot', self.initStack, self.minbet)
        self.robot2 = StandardRobot.robot(
            '2 standard robot', self.initStack, self.minbet)
        self.robot3 = AI_V1.robot('3 AI V1', self.initStack, self.minbet)
        self.robot4 = StandardRobot.robot(
            '4 standard robot', self.initStack, self.minbet)
        self.robot5 = AI_V1.robot('5 AI V1', self.initStack, self.minbet)
        self.robot6 = StandardRobot.robot(
            '6 standard robot', self.initStack, self.minbet)
        self.robot7 = AI_V1.robot('7 AI V1', self.initStack, self.minbet)
        self.initial_game_list = [
            self.robot1, self.robot2, self.robot3,self.robot4,self.robot5,self.robot6,self.robot7]
        self.fixed_game_list = [self.robot1, self.robot2,self.robot3,self.robot4,self.robot5,self.robot6,self.robot7]
        self.GameEnd = False

    def test2(self, i):

        self.raiseAmount = i.betAmount
        self.BET = self.raiseAmount
        self.POT += self.BET
        self.israised = True
        for p in self.move_list[self.move_list.index(i)+1:]:

            dec = p.reRaiseDecision()
            if dec == 'fold':
                self.in_game_list.remove(p)
                self.move_list.remove(p)
                return False

        for p in self.move_list[:self.move_list.index(i)]:

            dec = p.reRaiseDecision()
            if dec == 'fold':
                self.in_game_list.remove(p)
                self.move_list.remove(p)
                return False


    def test1(self, deci, i):

        if deci == 'check':
            self.BET = 0
        elif deci == 'fold':
            self.in_game_list.remove(i)
            self.move_list.remove(i)
        elif deci == 'call':
            self.BET = i.betAmount
            self.POT += self.BET
        elif deci == 'raise':
            self.BET = i.betAmount
            self.raiseAmount = i.betAmount
            self.POT += self.BET
            i.isRaise = True
            self.israised = True
        elif deci == 'All-in':
            self.raiseAmount = i.betAmount - i.previousBet
            self.BET = i.betAmount
            self.POT += self.raiseAmount
            i.isRaise = True
            self.israised = True

        if i.isRaise:

            for p in self.move_list[self.move_list.index(i)+1:]:

                if p.name != '3 AI V1' and p.name != '5 AI V1' and p.name != '7 AI V1':
                    dec = p.raiseDecision(self.BET, self.POT)
                else:
                    dec = p.raiseDecision(self.BET, self.POT, len(self.move_list)-1)
                
                if dec == 'fold':
                    self.in_game_list.remove(p)
                    self.move_list.remove(p)
                elif dec == 'call':
                    self.POT += p.needToBet
                    # p.money -= p.needToBet # REMEMBER THIS BUG!!!
                elif dec == 're-raise':
                    print 'xxx'
                elif dec == 'All-in':
                    self.test2(p)
                    i.isRaise = False
                    return False

            for p in self.move_list[:self.move_list.index(i)]:

                if p.name != '3 AI V1' and p.name != '5 AI V1' and p.name != '7 AI V1':
                    dec = p.raiseDecision(self.BET, self.POT)
                else:
                    dec = p.raiseDecision(self.BET, self.POT, len(self.move_list)-1)
                
                if dec == 'fold':
                    self.in_game_list.remove(p)
                    self.move_list.remove(p)
                elif dec == 'call':
                    self.POT += p.needToBet
                elif dec == 're-raise':
                    print 'xxx'
                elif dec == 'All-in':
                    self.test2(p)
                    i.isRaise = False
                    return False

            i.isRaise = False

            return False

        return True

    def initialGame(self):

        self.dealer = Dealer.dealer()
        self.initial_game_list.append(self.initial_game_list.pop(0))
        self.in_game_list = []
        self.in_game_list.extend(self.initial_game_list)
        self.move_list = []
        self.move_list.extend(self.in_game_list)
        self.POT = 0
        self.raiseAmount = 0
        self.israised = False

        return

    def roundReset(self):

        for i in self.move_list:
            i.clean()
            i.preStack = i.money
            i.minbet = self.minbet
            i.hand = self.dealer.dealHandCards()
            i.money -= self.ante
            self.POT += self.ante

        return

    def preflopOver(self):

        self.israised = False
        self.boradCards = self.dealer.dealBoradCards()
        #self.move_list = []
        # self.move_list.extend(self.in_game_list)

        for i in self.in_game_list:
            i.clean()
            if i.decision == 'All-in':
                self.move_list.remove(i)

        return

    def turnStart(self):

        for i in self.in_game_list:
            i.boradCards = self.boradCards

        return

    def turnOver(self):

        self.raiseAmount = 0
        #self.move_list = []
        # self.move_list.extend(self.in_game_list)
        self.boradCards += self.dealer.dealTwoMoreCards()

        for i in self.in_game_list:
            i.clean()
            if i.decision == 'All-in':
                if i in self.move_list:
                    self.move_list.remove(i)

        return

    def riverStage(self):

        tmp = len(self.move_list)

        for i in range(len(self.move_list)):

            if i < len(self.move_list):
                obj = self.move_list[i]
                obj.addPosition([i, len(self.move_list)])
                obj.pot = self.POT
                obj.boradCards = self.boradCards
                
                if obj.name != '3 AI V1' and obj.name != '5 AI V1' and obj.name != '7 AI V1':
                    deci = obj.makeDecision()
                else:
                    deci = obj.makeDecision(len(self.move_list)-1)
                
                if not self.test1(deci, obj):
                    break
                '''
                if len(self.move_list) != tmp:
                    obj = self.move_list[i-1]
                    obj.addPosition([i, len(self.move_list)])
                    obj.pot = self.POT
                    obj.boradCards = self.boradCards
                    
                    if obj.name != 'AI V1':
                        deci = obj.makeDecision()
                    else:
                        deci = obj.makeDecision(len(self.move_list))

                    if not self.test1(deci, obj):
                        break
                '''   

        return

    def result(self):

        minstrength = 0
        self.winner = ''
        for i in self.in_game_list:

            if i.getHandStrength() > minstrength:
                minstrength = i.getHandStrength()
                self.winner = i.name
            # print i.getHandStrength()

        print "Winner is " + self.winner

        for i in self.fixed_game_list:
            if i.name == self.winner:
                i.money += self.POT
            if i.money <= 0:
                if i in self.initial_game_list:
                    self.initial_game_list.remove(i)
            
        
        for i in range(len(self.fixed_game_list)):
            obj = self.fixed_game_list[i]
            self.data[i+1].append(obj.money)
        

        


        tmp1 = 0
        tmp2 = 0
        for i in self.fixed_game_list:
            tmp1 += i.money
            tmp2 += i.money-i.preStack
            print i.name, i.money, i.money-i.preStack
            if i.money == 0:
                i.preStack = 0
        if tmp2 != 0:
            print self.POT
        print tmp1, tmp2  # fix the allin problem
        tmp1 = 0
        tmp2 = 0

        playerCount = len(self.initial_game_list)
        
        if playerCount == 1:
            self.GameEnd = True
        '''
        elif playerCount <= 4:
            self.ante = 150
            self.minbet = 300
        
        elif playerCount <= 5:
            self.ante = 500
            self.minbet = 1250
        elif playerCount <= 7:
            self.ante = 100
            self.minbet = 250
        '''

        if playerCount <= 3:
            for i in self.in_game_list:
                if i.name[2:] != 'AI V1':
                    self.GameEnd = False
                    break
                else:
                    self.GameEnd = True

        for i in self.in_game_list:
            i.clean()

        print "Next Round.\n\n"

    def gameOver(self):

        print "GAME OVER"

        for i in self.initial_game_list:
            print i.name, i.money

        
        

        print 'Press enter to Exit.'
        raw_input()

        return

    def start(self):

        while not self.GameEnd:

            #print 'Press enter to start.'
            #raw_input()
            self.counter += 1
            if self.counter >= 2000:
                self.GameEnd = True

            print "Initial the game..."
            self.initialGame()
            print "Game started.\n\nPre-flop stage:"
            self.roundReset()

            self.utg = self.move_list[0]
            self.utg.position = 'Utg'
            self.utg.betAmount = self.minbet
            self.utg.previousBet = self.utg.betAmount
            self.utg.money -= self.utg.betAmount
            self.utg.pot = self.POT
            self.POT += self.utg.betAmount

            print self.utg.name, self.utg.convert(
                self.utg.hand), 'bet', self.utg.betAmount, 'pot:', self.utg.pot, 'money:', self.utg.money

            for i in self.move_list[1:]:
                i.addPosition([self.move_list.index(i), len(self.move_list)])
                i.pot = self.POT
                if i.name != '3 AI V1' and i.name != '5 AI V1' and i.name != '7 AI V1':
                    deci = i.startHand()
                else:
                    deci = i.startHand(len(self.move_list)-1)
                if not self.test1(deci, i):
                    break

            self.utg.pot = self.POT
            if not self.israised:
                if self.utg.name != '3 AI V1' and self.utg.name != '5 AI V1'and self.utg.name != '7 AI V1' :
                    utgdeci = self.utg.startHand()
                else:
                    utgdeci = self.utg.startHand(len(self.move_list)-1)
                self.test1(utgdeci, self.utg)

            if len(self.in_game_list) == 1:

                self.in_game_list[0].money += self.POT
                self.POT = 0
                #print 'winner ??'
                continue

            self.preflopOver()

            print "\nTurn stage:\nThe borad cards are: %s,%s,%s" % (self.robot1.convert(
                self.boradCards)[0], self.robot1.convert(self.boradCards)[1], self.robot1.convert(self.boradCards)[2])

            self.turnStart()

            self.riverStage()

            self.turnOver()

            print "\nRiver stage:\nThe borad cards are: %s,%s,%s,%s,%s" % (self.robot1.convert(self.boradCards)[0], self.robot1.convert(
                self.boradCards)[1], self.robot1.convert(self.boradCards)[2], self.robot1.convert(self.boradCards)[3], self.robot1.convert(self.boradCards)[4])

            self.turnStart()

            self.riverStage()

            print "Result:"

            self.result()

        self.gameOver()

        self.printData()
    
    def printData(self):

        #print 'filename?:'
        #input1 = raw_input()
        name = str(time.localtime().tm_mon)+'.'+str(time.localtime().tm_mday)+'.'+str(time.localtime().tm_hour)+'.'+str(time.localtime().tm_min)
        workbook = xlsxwriter.Workbook(name+'.xlsx')
        worksheet = workbook.add_worksheet('sheet')

        row = 0
        col = 1

        for i in self.data[1:]:
            for y in i:
                worksheet.write(row,col,y)
                col += 1
                if y <= 0:
                    break
            col = 1
            row += 1
        
        for k in range(len(self.fixed_game_list)):
            worksheet.write(k,0,self.fixed_game_list[k].name)

        workbook.close()
        print name


def main():

    #tmp = test()
    t = time.time()
    circle = 1
    list1 = []
    
    for i in range(circle):
        list1.append([])
        tmp = test()
        tmp.start()
        list1[i].append(tmp.data)
        for i in tmp.fixed_game_list:
            tmp.data[0].append(i.name)
    
    '''
    name = str(time.localtime().tm_mon)+'.'+str(time.localtime().tm_mday)+'.'+str(time.localtime().tm_hour)+'.'+str(time.localtime().tm_min)
    callbook = xlsxwriter.Workbook('call'+name+'.xlsx')
    callsheet = callbook.add_worksheet('sheet')
    standardbook = xlsxwriter.Workbook('standard'+name+'.xlsx')
    standardsheet = standardbook.add_worksheet('sheet')

    print name

    row1 = 0
    col1 = 0
    row2 = 0
    col2 = 0

    for k in list1:
        for c in range(len(k[0])-1):

            if k[0][0][c] == 'AI V1':
                for i in k[0][c+1]:
                    callsheet.write(row1,col1,i)
                    col1 += 1
                    if col1 >= 2000:
                        break
                    if i <= 0:
                        break

            elif k[0][0][c] == 'standard robot':
                for i in k[0][c+1]:
                    standardsheet.write(row2,col2,i)
                    col2 += 1
                    if col2 >= 2000:
                        break
                    if i <= 0:
                        break
        col1 = col2 = 0
        row1 += 1
        row2 += 1


    callbook.close()
    standardbook.close()

    '''    

    print time.time() - t
        

main()
