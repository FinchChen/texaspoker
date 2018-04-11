import CallRobot
import Dealer
import FoldRobot
import StandardRobot
import xlsxwriter
import time


class test(object):

    def __init__(self):

        self.data = [[],[],[]]

        self.minbet = 100
        self.ante = 50
        self.initStack = 10000
        self.robot1 = CallRobot.robot('robot1', self.initStack, self.minbet)
        self.robot2 = CallRobot.robot('robot2', self.initStack, self.minbet)
        self.robot3 = CallRobot.robot('robot3', self.initStack, self.minbet)
        self.robot4 = StandardRobot.robot(
            '4 standard robot', self.initStack, self.minbet)
        self.robot5 = FoldRobot.robot('5 fold robot', self.initStack, self.minbet)
        self.robot6 = CallRobot.robot('robot6', self.initStack, self.minbet)
        self.robot7 = CallRobot.robot('robot7', self.initStack, self.minbet)
        self.robot8 = CallRobot.robot('robot8', self.initStack, self.minbet)
        self.robot9 = CallRobot.robot('robot9', self.initStack, self.minbet)
        self.initial_game_list = [
            self.robot1, self.robot2, self.robot3, self.robot4, self.robot5,self.robot6,self.robot7,self.robot8,self.robot9]
        self.fixed_game_list = [self.robot1, self.robot2,
                                self.robot3, self.robot4, self.robot5,self.robot6,self.robot7,self.robot8,self.robot9]
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

                dec = p.raiseDecision(self.BET, self.POT)
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

                dec = p.raiseDecision(self.BET, self.POT)
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

        for i in range(len(self.move_list)):

            obj = self.move_list[i]
            obj.addPosition([i, len(self.move_list)])
            obj.pot = self.POT
            obj.boradCards = self.boradCards
            deci = obj.makeDecision()

            if not self.test1(deci, obj):
                break

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
            
            if i.name == 'robot1':
                self.data[0].append(i.money)
            elif i.name == '4 standard robot':
                self.data[1].append(i.money)
            elif i.name == '5 fold robot':
                self.data[2].append(i.money)

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
        elif playerCount <= 3:
            self.ante = 1000
            self.minbet = 2500
        elif playerCount <= 5:
            self.ante = 500
            self.minbet = 1250
        elif playerCount <= 7:
            self.ante = 100
            self.minbet = 250

        for i in self.in_game_list:
            i.clean()

        print "Next Round.\n\n"

    def gameOver(self):

        print "GAME OVER"

        for i in self.initial_game_list:
            print i.name, i.money
        
        print self.data

        print 'Press enter to Exit.'
        raw_input()

        return

    def start(self):

        while not self.GameEnd:

            #print 'Press enter to start.'
            #raw_input()
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
                deci = i.startHand()
                if not self.test1(deci, i):
                    break

            self.utg.pot = self.POT
            if not self.israised:
                utgdeci = self.utg.startHand()

                self.test1(utgdeci, self.utg)

            if len(self.in_game_list) == 1:

                self.in_game_list[0].money += self.POT
                self.POT = 0
                print 'winner ??'
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
        col = 0

        for i in self.data:
            for y in i:
                worksheet.write(row,col,y)
                col += 1
            col = 0
            row += 1

        workbook.close()
        print 'success'


def main():
    tmp = test()
    tmp.start()


main()
