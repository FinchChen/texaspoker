from __future__ import division
import AI_V1


tmp = AI_V1.robot('s',100,100)
tmp.hand = [12,7]
tmp.boradCards = [11,10,5,3,0]
tmp2 =  tmp.simulation_outside(1000,4)
print float(tmp2)