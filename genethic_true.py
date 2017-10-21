import numpy as np
from math import exp, sin
import matplotlib.pyplot as plt
import random

PROB_MUT = 0.3
PROB_OF_SEX = 0.8
ELITE = 0.1
POOL_SIZE = 500
EPS = 0.000001

"""def coupling(lis):
    for i in range(0, len(lis), 2 ):
        r = random.choice([1,0])
        if r == 0:
            a = random.uniform(lis[i].pos, lis[i+1].pos)
            b = random.uniform(lis[i].pos, lis[i+1].pos)
        else:
            a = random.uniform(lis[i].pos, lis[i-1].pos)
            b = random.uniform(lis[i].pos, lis[i-1].pos)
        c = Gen(a, abs(f(a)))
        d = Gen(b, abs(f(b)))
        lis[i+1], lis[i] = c.comp(d)
    return lis
"""
def coupling(lis):
    prob = PROB_MUT
    new_lis = lis
    for i in range(int(ELITE*POOL_SIZE)):
        if random.uniform(0, 1) < prob:
            lucker = random.choice(lis)
            lucker.pos += random.choice([-1, 1])*0.5
            lucker.abso = abs(f(lucker.pos))
            continue
        a, b = random.choice(lis), random.choice(lis)
        r = random.uniform(a.pos, b.pos)
        new_lis.append(Gen(r, abs(f(r))))


    return new_lis

def gen():
    m = 0
    gens = []
    for i in range(POOL_SIZE):
        g = random.uniform(-20, 20)
        gens.append(Gen(g, abs(f(g))))
    
    gens.sort(key = lambda gen: gen.abso)
    while gens[0].abso > EPS:
        #for gen1 in gens:
            #print(gen1.pos, gen1.abso)
        #input()
        print(gens[0].pos, gens[0].abso)
        gens = coupling(gens[:int(ELITE*POOL_SIZE)])
        gens.sort(key = lambda gen: gen.abso)
        m += 1
        print(m)
        #input()
    return (gens, m)

def sort(x):
    for i in range(len(x)-1):
        for j in range(i, len(x)-1):
            if x[j] >= x[j+1]:
                temp = x[j]
                x[j] = x[j+1]
                x[j+1] = temp
    return x

class Gen:
    def __init__(self, pos, abso):
        self.pos, self.abso = pos, abso

    def comp(self, other):
        if self.abso >= other.abso:
            return (self, other)
        else:
            return (other, self)
    


def f(x):
    return x + sin(x) - 1



def main():
    p, m = gen()
    for gen1 in p:
        print(gen1.pos, gen1.abso)
    print("Vot skol'ko shagov - " , m)
    """x_v = np.linspace(-4, 4, num = 1000)
    y_v = []
    
    for x in x_v:
        y_v.append(f(x))
    plt.plot(x_v, y_v)
    plt.plot([-4, 4], [0, 0])



    plt.show()"""


if __name__ == '__main__':
    main()
