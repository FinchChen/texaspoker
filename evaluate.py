import standard_function

minbet = 100
robot1 = standard_function.robot('robot1',10000,minbet)
robot2 = standard_function.robot('robot2',10000,minbet)
robot3 = standard_function.robot('robot3',10000,minbet)

while True:

    print 'Press enter to start.'
    
    raw_input()

    print "Initial the game..."

    dealer = standard_function.dealer()

    initial_game_list = [robot1,robot2,robot3]
    in_game_list = initial_game_list
    move_list = in_game_list

    pot = 0
    raiseAmount = 0

    print "Game started.\n\nPre-flop stage:"

    for i in initial_game_list:

        i.addHand(dealer.dealHandCards())
        i.addPosition([initial_game_list.index(i),len(initial_game_list)])
        i.addPot(pot)
        deci = i.startHand()

        if deci == 'fold':
            in_game_list.remove(i.getName())
        else:
            pot += i.getBetAmount()

    boradCards = dealer.dealBoradCards() 

    print "\nTurn stage:\nThe borad cards are: %s,%s,%s" % (robot1.convert(boradCards)[0],robot1.convert(boradCards)[1],robot1.convert(boradCards)[2])
        
    for i in range(len(move_list)):

        obj = move_list[i]
        obj.addPosition([i,len(move_list)])
        obj.addPot(pot)
        obj.setBorad(boradCards)
        if raiseAmount != 0:
            obj.addRaise(raiseAmount)
        deci = obj.makeDecision()

        if deci == 'fold':
            in_game_list.remove(obj.getName())
        elif deci == 'call':
            pot += obj.getBetAmount()
        elif deci == 'raise':
            pot += obj.getBetAmount()
            raiseAmount = obj.getBetAmount()

        #move_list[i].test()

    move_list = in_game_list # update list

    boradCards += dealer.dealTwoMoreCards() 
    
    print "\nRiver stage:\nThe borad cards are: %s,%s,%s,%s,%s" % (robot1.convert(boradCards)[0],robot1.convert(boradCards)[1],robot1.convert(boradCards)[2],robot1.convert(boradCards)[3],robot1.convert(boradCards)[4])

    for i in range(len(move_list)):

        obj = move_list[i]

        obj.addPosition([i,len(move_list)])
        obj.addPot(pot)
        obj.setBorad(boradCards)
        deci = obj.makeDecision()

        if deci == 'fold':
            in_game_list.remove(obj.getName())
        else:
            pot += obj.getBetAmount()
    
    print "Result:"

    minstrength = 0
    for i in in_game_list:

        if i.getHandStrength() > minstrength:
            minstrength = i.getHandStrength()
            winner = i.getName()

    print "Winner is " + winner

    for i in initial_game_list:
        if i.getName() == winner:
            i.addMoney(pot)

    print "Next Round."





