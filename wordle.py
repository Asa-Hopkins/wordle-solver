import pickle
import os

def process():
    x = open("wordle.txt","r")
    w = x.readlines()
    a = []
    words = 0
    for i in w:
        if len(i)!=6 or i!=i.lower() or i.__contains__("'") or i.__contains__("é") or i.__contains__("Å"):
            pass
        else:
            a.append(i[:-1])
            words+=1
    return a

def convert(rel):
    temp = 0
    for i in rel:
        temp = temp*3 + i
    return temp

if os.path.exists("relations"):
    f = open("relations","rb")
    words, match_dict = pickle.load(f)
else:
    match_dict = {}
    words = {}
    f.close()
if os.path.exists("first"):
    f = open("first","rb")
    aesir, roate = pickle.load(f)
    f.close()
else:
    aesir, roate = 0

def match(word,guess, rel = 0, use_dict = 1):
    if use_dict:
        return rel*243 + match_dict[words[guess]*2315+words[word]]
    l = len(word)
    count = {}
    green = [False]*l
    orange = [False]*l
    for i in guess:
        count[i] = word.count(i)
    for a in range(0,l):
        green[a] = guess[a]==word[a]
        count[guess[a]] -= green[a]
    for a in range(0,l):
        if green[a]:
            continue
        orange[a] = count[guess[a]] > 0
        count[guess[a]] -= 1
    for a in range(0,l):
        rel = rel*3 + green[a]*2 + orange[a]
    return rel

if len(match_dict)==0: #Calculate lookup
    a = 0
    for j in open("answers.txt","r").read().split(","):
        if j not in words:
            words[j] = a
            a+=1
    for j in open("answers.txt","r").read().split(","):
        for i in process():
            if i not in words:
                words[i] = a
                a+=1
            match_dict[words[i]*2315+words[j]] = match(j,i, use_dict=0)
    
def table(word = False, fw = False, fwr = None, answers = False):
    wordlist = process()
    if answers==False:
        answers = open("wordleAnswers.txt","r").read().split(",")
    #wordlist = open("nerdle.txt","r").read().split(",")
    #answers = wordlist[:]
    if fw == ["aesir"] and aesir!=0:
        return aesir[fwr]
    if fw == ["roate"] and roate!=0:
        return roate[fwr]
    if fw:
        b = []
        lookup = {}
        number = {}
        count = 0
        for j in answers:
            rel = 0
            for i in fw:
                rel = match(j,i, rel)
            if fwr == rel:
                b.append(j)
            if fwr==None:
                if number.get(rel)==None:
                    number[rel] = count
                    count += 1
                lookup[j] = number[rel]
    if fwr!=None:
        answers = b
    if len(answers) == 1:
        return [[answers]*2]+[answers]
    if len(answers)==0:
        return [0]
    c = 0
    l = len(answers)
    minimax = ["",1e9]
    average = ["",1e9]
    for i in ([word] if word else wordlist):
        m = 0
        avg = 0
        bins = {}
        for j in answers:
            rel = (lookup[j] if (fw and fwr==None) else 0)
            rel = match(j,i,rel)
            if bins.get(rel) == None:
                bins[rel] = 0
            avg += 2*bins[rel] + 1
            bins[rel] += 1
            m += bins[rel] > m
            
            if avg > average[1]*l and m > minimax[1]:
                break
        if minimax[1] > m or (minimax[1] == m and avg/l < average[1]):
            minimax = [i,m,avg/l]
        if avg/l < average[1]:
            average = [i, avg/l, m]
        if avg/l == average[1] and m == minimax[1] and i in answers:
            average = [i,avg/l,m]
            minimax = [i,m,avg/l]
        c=c+1
    #    if c%100 == 0:
    #        print(i, minimax, average)
    #print(minimax, average)
    #if len(answers) < 10:
    #    print(answers)
    return [minimax, average], answers

def solve(word, alg = 0):
    guesses = 1
    rel = 0
    guess = ["aesir","roate"][alg]
    rel = match(word,guess)
    ans = False
    while guess!=word:
        guess, ans = table(fw = [guess], fwr = rel, answers = ans)
        guess = guess[alg][0]
        rel = match(word,guess)
        #print(guess, len(ans))
        guesses +=1
    return guesses

def test(l,alg = 0):
    s = []
    for word in l:
        s.append(solve(word,alg=alg))
    print(sum(s)/len(s), max(s))

 
#x = table()

#Best words
# ['slate', 221, 71.57278617710583]
# ['aesir', 168, 69.8829373650108]
# ['roate', 195, 60.42462203023758]
# ['serai', 168, 72.92138228941684]

#['58-46=12', 101, 32.38938103029961]
#['48-32=16', 111, 31.110026519212322]
