import pandas as pd
import math

from raccomandation import racc

users=[610,22,547]

rac=[]

for u in users:
    rac.append(racc(u))
 

def averageAgg(list):
    scoreA={}
    for key in item.keys():
        s = sum(item[key])/3
        scoreA[key]=s
    return scoreA
        
    
def leastMiseryAgg(list):
    scoreL={}
    for key in item.keys():
        s = min(item[key])/(4-len(item[key]))  #explain whi you divide
        scoreL[key]=s
    return scoreL

item={}

for list in rac:
    for i in list:
        if i[0] in item.keys():
            item[i[0]].append(i[1])
        else:
            item[i[0]]=[i[1]]

av=averageAgg(item)

sortedAv = sorted(av.items(), key=lambda x: x[1], reverse=True)[:10]

lm=leastMiseryAgg(item)

sortedLm = sorted(lm.items(), key=lambda x: x[1], reverse=True)[:10]

print(sortedAv,sortedLm)

