import standard_function

minbet = 100
ante = 10
robot1 = standard_function.robot('robot1',10000,minbet)
robot2 = standard_function.robot('robot2',10000,minbet)
robot3 = standard_function.robot('robot3',10000,minbet)
robot4 = standard_function.robot('robot4',10000,minbet)
robot5 = standard_function.robot('robot5',10000,minbet)
initial_game_list = [robot1,robot2,robot3,robot4,robot5]
fixed_game_list = [robot1,robot2,robot3,robot4,robot5]

while True:

    print 'Press enter to start.'
    
    raw_input()

    print "Initial the game..."

    dealer = standard_function.dealer()

    initial_game_list.append(initial_game_list.pop(0))
    in_game_list = []
    in_game_list.extend(initial_game_list)
    move_list = []
    move_list.extend(in_game_list)

    POT = 0
    raiseAmount = 0

    print "Game started.\n\nPre-flop stage:"

    for i in move_list:
        i.hand = dealer.dealHandCards()
        i.money -= ante
        POT += ante

    utg = move_list[0]
    utg.position = 'Utg'
    utg.betAmount = minbet
    utg.money -= utg.betAmount
    POT += utg.betAmount
    print utg.name,utg.convert(utg.hand),utg.betAmount,utg.pot,utg.money
    
    for i in move_list[1:]: # other normal player

        #i.hand = dealer.dealHandCards()
        #i.addHand(dealer.dealHandCards())
        i.addPosition([move_list.index(i),len(move_list)])
        #i.addPot(pot)
        i.pot = POT
        
        deci = i.startHand()

        if deci == 'fold':
            in_game_list.remove(i)
        elif deci == 'call':
            BET = i.betAmount
            POT += BET
        elif deci == 'raise':
            BET = i.betAmount
            POT += BET
            i.isRaise = True
        
        
        if i.isRaise:

            for p in move_list[move_list.index(i)+1:]:
                
                dec = p.raiseDecision(BET,POT)
                if dec == 'fold':
                    in_game_list.remove(p)
                elif dec == 'call':
                    POT += p.needToBet
                    p.money -= p.needToBet
                elif dec == 're-raise':
                    print 'xxx'


            for p in move_list[:move_list.index(i)]:
                
                dec = p.raiseDecision(BET,POT)
                if dec == 'fold':
                    in_game_list.remove(p)
                elif dec == 'call':
                    POT += p.needToBet
                    p.money -= p.needToBet
                elif dec == 're-raise':
                    print 'xxx'
            
            i.isRaise = False
            break
    
    if utg.startHand() == 'fold':
        in_game_list.remove(utg)

    utg.pot = POT
    print utg.name,utg.convert(utg.hand),utg.decision,"0",utg.pot,utg.money

    if len(in_game_list) == 1:

        in_game_list[0].money += POT
        POT = 0
        continue

    boradCards = dealer.dealBoradCards() 

    move_list = []
    move_list.extend(in_game_list)

    for i in in_game_list:
        i.clean()

    print "\nTurn stage:\nThe borad cards are: %s,%s,%s" % (robot1.convert(boradCards)[0],robot1.convert(boradCards)[1],robot1.convert(boradCards)[2])
        
    for i in range(len(move_list)):

        obj = move_list[i]

        obj.addPosition([i,len(move_list)])
        obj.pot += POT
        #obj.setBorad(boradCards)
        obj.boradCards = boradCards
        #obj.addRaise(raiseAmount)
        obj.raiseAmount = raiseAmount

        deci = obj.makeDecision()

        if deci == 'fold':
            in_game_list.remove(obj.name)
        elif deci == 'call':
            POT += obj.betAmount
        elif deci == 'raise':
            POT += obj.betAmount
            raiseAmount = obj.betAmount

        #move_list[i].test()

    raiseAmount = 0

    move_list = []
    move_list.extend(in_game_list)

    boradCards += dealer.dealTwoMoreCards() 

    for i in in_game_list:
        i.clean()
    
    print "\nRiver stage:\nThe borad cards are: %s,%s,%s,%s,%s" % (robot1.convert(boradCards)[0],robot1.convert(boradCards)[1],robot1.convert(boradCards)[2],robot1.convert(boradCards)[3],robot1.convert(boradCards)[4])

    for i in range(len(move_list)):

        obj = move_list[i]

        obj.addPosition([i,len(move_list)])
        obj.pot = POT
        #obj.setBorad(boradCards)
        obj.boradCards = boradCards

        deci = obj.makeDecision()

        if deci == 'fold':
            in_game_list.remove(obj.name)
        else:
            POT += obj.betAmount
    
    print "Result:"

    minstrength = 0
    winner = ''
    for i in in_game_list:
        
        if i.getHandStrength() > minstrength:
            minstrength = i.getHandStrength()
            winner = i.name
        # print i.getHandStrength()

    print "Winner is " + winner

    for i in initial_game_list:
        if i.name == winner:
            # print "type: "
            i.money += POT
    
    

    for i in fixed_game_list:
        print i.name,i.money

    for i in in_game_list:
        i.clean()

    print "Next Round.\n\n"





