import algo1
import random as rd




max = 0
for i in range (100): 
    M1 = rd.randint(1,10)*rd.random()
    M2 = rd.randint(1,10)*rd.random()
    M3 = rd.randint(1,10)*rd.random()
    nb_countries = algo1.algo(M1,M2,M3)
    if nb_countries > max:
        max = nb_countries
        bestM = (M1,M2,M3)
    

print (bestM)

