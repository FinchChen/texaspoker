import newfunc

a = newfunc.dealer(2)

while True:

    print 'Hold1: '
    inputs = raw_input()
    holds = []
    holds.append(int(a.r_convert(inputs)))
    print 'Hold2: '
    inputs = raw_input()
    holds.append(int(a.r_convert(inputs)))
    print 'Borads Number: '
    inputs = raw_input()
    borads = []
    if inputs != 0:
        for i in range(int(inputs)):
            print 'Borad' + str(i+1) + ': '
            tmp = raw_input()
            borads.append(int(a.r_convert(tmp)))
    print 'Bets: '
    inputs = raw_input()
    bets = float(inputs)
    print 'Pots: '
    inputs = raw_input()
    pots = float(inputs)
    print "Opponents: "
    inputs = raw_input()
    oppo = int(inputs)

    a.decision(holds,borads,bets,pots,oppo)