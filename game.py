import AllInRobot
import CallRobot
#import FoldRobot
#import RandomRobot
import StandardRobot
#import AI_V1
# import AI_V2
#import RealPlayer
import Dealer
import random

Stack = 10000
Minbet = 100
Ante = 50
GameEnd = False

all_in_robot = AllInRobot.robot('1 All-in robot',Stack,Minbet)
call_robot = CallRobot.robot('2 Call station',Stack,Minbet)
#fold_robot = FoldRobot.robot('fold robot',Stack,Minbet)
#random_robot = RandomRobot.robot('random robot',Stack,Minbet)
standard_Robot = StandardRobot.robot('3 standard robot',Stack,Minbet)
#AI1 = AI_V1.robot('AI V1',Stack,Minbet)
#player1 = RealPlayer.player('real player 1',Stack,Minbet)

initial_game_list = [all_in_robot,call_robot,standard_Robot]
#tmp_list = initial_game_list
#random.shuffle(tmp_list)
#initial_game_list = tmp_list

def allin():

    return

while not GameEnd:

    print 'Press enter to start.'
    raw_input()
    print "Initial the game..."

    dealer = Dealer.dealer()

    initial_game_list.append(initial_game_list.pop(0))
    in_game_list = []
    in_game_list.extend(initial_game_list)
    move_list = []
    move_list.extend(in_game_list)

    POT = 0
    RaiseAmount = 0
    IsRaised = False
    IsAllIn = False

    print "Game started.\n\nPre-flop stage:"

    for i in move_list:
        i.clean()
        i.hand = dealer.dealHandCards()
        i.money -= Ante
        POT += Ante

    utg = move_list[0]
    utg.position = 'Utg'
    utg.betAmount = Minbet
    utg.money -= utg.betAmount
    POT += utg.betAmount
    print utg.name,utg.convert(utg.hand),'bet',utg.betAmount,'pot:',utg.pot,'money:',utg.money
       
    for i in move_list[1:]:
        i.addPosition([move_list.index(i),len(move_list)])
        i.pot = POT
        deci = i.startHand()

        if deci == 'fold':
            in_game_list.remove(i)
            move_list.remove(i)
        elif deci == 'call':
            BET = i.betAmount
            POT += BET
        elif deci == 'raise':
            RaiseAmount = i.betAmount
            POT += RaiseAmount
            i.isRaise = True
            IsRaised = True
        elif deci == 'All-in':
            IsAllIn = True
        
        if i.isRaise:

            for p in move_list[move_list.index(i)+1:]:
                
                dec = p.raiseDecision(RaiseAmount,POT)
                if dec == 'fold':
                    in_game_list.remove(p)
                    move_list.remove(p)
                elif dec == 'call':
                    POT += p.needToBet
                    p.money -= p.needToBet
                elif dec == 're-raise':
                    print 'xxx'
                elif dec == 'All-in':
                    print 'yyy'


            for p in move_list[:move_list.index(i)]:
                
                dec = p.raiseDecision(RaiseAmount,POT)
                if dec == 'fold':
                    in_game_list.remove(p)
                    move_list.remove(p)
                elif dec == 'call':
                    POT += p.needToBet
                    p.money -= p.needToBet
                elif dec == 're-raise':
                    print 'xxx'
                elif dec == 'All-in':
                    print 'yyy'
            
            i.isRaise = False
            break

    utg.pot = POT

    if not IsRaised:

        utgdeci = utg.startHand()

        if utgdeci == 'fold':
            in_game_list.remove(utg)
            move_list.remove(utg)
        elif utgdeci == 'raise' or utgdeci == 'All-in':
            BET = utg.betAmount
            POT += BET

            for p in move_list[move_list.index(utg)+1:]:
                    
                dec = p.raiseDecision(BET,POT)
                if dec == 'fold':
                    in_game_list.remove(p)
                elif dec == 'call':
                    POT += p.needToBet
                    p.money -= p.needToBet
                elif dec == 're-raise':
                    print 'xxx'
                elif dec == 'All-in':
                    print 'yyy'

            for p in move_list[:move_list.index(utg)]:
                    
                dec = p.raiseDecision(BET,POT)
                if dec == 'fold':
                    in_game_list.remove(p)
                elif dec == 'call':
                    POT += p.needToBet
                    p.money -= p.needToBet
                elif dec == 're-raise':
                    print 'xxx'
                elif dec == 'All-in':
                    print 'yyy'
    
    if len(in_game_list) == 1:

        in_game_list[0].money += POT
        POT = 0
        print 'change here'
        continue
    
    if IsAllIn:

        allin()
        print 'change here'
        continue
    
    RaiseAmount = 0
    IsRaised = False
    BoradCards = dealer.dealBoradCards()
    move_list = []
    move_list.extend(in_game_list)
    for i in in_game_list:
        i.clean()

    print "\nTurn stage:\nThe borad cards are: %s,%s,%s" % (standard_Robot.convert(BoradCards)[0],standard_Robot.convert(BoradCards)[1],standard_Robot.convert(BoradCards)[2])

    for i in range(len(move_list)):

        obj = move_list[i]
        obj.addPosition([i,len(move_list)])
        obj.pot += POT
        obj.BoradCards = BoradCards
        obj.raiseAmount = RaiseAmount
        deci = obj.makeDecision()

        if deci == 'fold':
            in_game_list.remove(obj)
            move_list.remove(obj)
        elif deci == 'call':
            POT += obj.betAmount
        elif deci == 'raise':
            POT += obj.betAmount
            RaiseAmount = obj.betAmount
    
    RaiseAmount = 0
    IsRaised = False
    BoradCards += dealer.dealTwoMoreCards()
    move_list = []
    move_list.extend(in_game_list)
    for i in in_game_list:
        i.clean()

    print "\nRiver stage:\nThe borad cards are: %s,%s,%s,%s,%s" % (standard_Robot.convert(BoradCards)[0],standard_Robot.convert(BoradCards)[1],standard_Robot.convert(BoradCards)[2],standard_Robot.convert(BoradCards)[3],standard_Robot.convert(BoradCards)[4])

    for i in range(len(move_list)):

        obj = move_list[i]
        obj.addPosition([i,len(move_list)])
        obj.pot = POT
        obj.boradCards = BoradCards
        deci = obj.makeDecision()

        if deci == 'fold':
            in_game_list.remove(obj)
            move_list.remove(obj)
        elif deci == 'call':
            POT += obj.betAmount
        elif deci == 'raise':
            POT += obj.betAmount
            RaiseAmount = obj.betAmount
    
    print "Result:"

    minstrength = 0
    winner = ''
    for i in in_game_list:
        
        if i.getHandStrength() > minstrength:
            minstrength = i.getHandStrength()
            winner = i.name
    
    print "Winner is " + winner

    for i in initial_game_list:
        print i.name,i.money

    for i in in_game_list:
        i.clean()
    
    playerCount = len(initial_game_list)
    if playerCount== 4:
        ante = 100
        minbet = 250
    elif playerCount == 3:
        ante = 500
        minbet = 750
    elif playerCount == 2:
        ante = 2000
        minbet = 1000
    elif playerCount == 1:
        GameEnd = True

    print "Next Round.\n\n"

print "GAME FINISHED"
for i in initial_game_list:
    print i.name,i.money
print 'Press enter to Exit.'
raw_input()