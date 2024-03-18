import pandas as pd
import math

def average(list):
    return sum(list)/len(list)

def sim1(user1, user2, mean1, mean2):

    p = pd.merge(user1, user2, on='movieId')

    num=0
    den1=0
    den2=0
    
    for i, item in p.iterrows():
        
        r1 = user1.loc[user1["movieId"]==item["movieId"]]["rating"].values[0]
        r2 = user2.loc[user2["movieId"]==item["movieId"]]["rating"].values[0]
        
        num += (r1-mean1)*(r2-mean2)
        den1 += ((r1-mean1)**2)
        den2 += ((r2-mean2)**2)
        
    if den1==0 or den2==0:
        return -1
    
    return num/(math.sqrt(den1)*math.sqrt(den2))

def sim2(user1, user2, length):
    p = pd.merge(user1, user2, on='movieId')
    
    sim=0
    
    for i, item in p.iterrows():
        sim+=(item["rating_x"]-item["rating_y"])**2
        
    if len(p)==0:
        return 0
    
    return len(p)/math.sqrt(sim)
    

def pred(movie, mean ,sim, users, rMeans): 
    num=0
    den=0
    
    for i in sim:
        u=i[0]
        if movie in users[u]["movieId"].values:
            r2 = users[u].loc[users[u]["movieId"]==movie]["rating"].values[0]
            num += i[1]*(r2-rMeans[u])
        
            den += i[1]
    if(den==0):
        return 0    
    return mean+(num/den)

def racc(userId):
    
    s={}

    users={}

    rMeans={}

    ratings = pd.read_csv("ml-latest-small/ratings.csv")

    movies = pd.read_csv("ml-latest-small/movies.csv")

    rat = [ r for i, r in ratings.iterrows() if r["userId"]== userId]

    rat = pd.DataFrame(rat)[["movieId","rating"]]

    mean= average(rat["rating"])
    
    items = pd.merge(movies, rat, on="movieId", how='left', indicator=True)

    items = items[items['_merge'] == 'left_only']

    items.drop(columns=['_merge'], inplace=True)

    score={}

    l=len(rat)
        
    for j, r in ratings.iterrows():
        if r["userId"] in users:
            users[r["userId"]].append(r)
        else:
            users[r["userId"]]=[r]
        

    for i in range (1,610):
        
        if i!=userId:
        
            user = pd.DataFrame(users[i])[["movieId","rating"]]
        
            users[i]= user
        
            meansu = average(user["rating"])
    
            rMeans[i]= meansu
    
            s[i]=sim2(rat, user,l)

    sortedSim = sorted(s.items(), key=lambda x: x[1], reverse=True)[:30]
    
    print("similar user"+str(sortedSim[:10]))

    for movieId in items["movieId"]:
        score[movieId]=(pred(movieId, mean, sortedSim, users, rMeans))
    
    
    sortedScore = sorted(score.items(), key=lambda x: x[1],  reverse=True)[:10]

    return sortedScore

print(racc(610))