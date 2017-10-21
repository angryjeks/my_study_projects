#import matplotlib.pyplot as plt
from math import exp
from math import log
from matplotlib import pyplot as plt
from matplotlib import animation
import seaborn
import scipy
import numpy as np

EPS = 10**(-6)
q1 = 0.388453
q2 = 0.36269
n_si = 14




X0_for_SI = 0.25
X0_for_Newton = 0.25
X0_for_Newton_mod = -5
n_nm=4
xv, yv = [], []

fig, ax = plt.subplots()
ln, = ax.plot([], [], 'b')


def output(string, listi, prove):
    if not prove:
        print(string)
        print(' | n|Xn             ||f(Xn)|        ||f(Xn)-f(Xn-1)|||Xn-Xn-1|      |EPS        ')
        l = listi[0]
        print('{0:s}|{1:2d}|{2:1.9e}|{3:1.9e}|{4:s}|{5:s}|{6:1.3e}'.format(l[0], l[1], l[2], l[3], l[4], l[5], l[6]))
        for j in range(1, len(listi)):
            print('{0:s}|{1:2d}|{2:1.9e}|{3:1.9e}|{4:1.9e}|{5:1.9e}|{6:1.3e}'.format(listi[j][0], listi[j][1], listi[j][2], listi[j][3], listi[j][4], listi[j][5], listi[j][6]))
    else:
        print(string)
        print(' n|Xn             ||f(Xn)|        ||f(Xn)-f(Xn-1)|||Xn-Xn-1|      |EPS        ')
        l = listi[0]
        print('{0:2d}|{1:1.9e}|{2:1.9e}|{3:s}|{4:s}|{5:1.3e}'.format(l[0], l[1], l[2], l[3], l[4], l[5]))
        for j in range(1, len(listi)):
            print('{0:2d}|{1:1.9e}|{2:1.9e}|{3:1.9e}|{4:1.9e}|{5:1.3e}'.format(listi[j][0], listi[j][1], listi[j][2], listi[j][3], listi[j][4], listi[j][5]))

    #for i in listi:



def init():
    #n_nm = int(log(2, (log(0.5/EPS)/log(1/q2)+1))) + 1
    #n_si = int(log((0.5)/((1-q1)*EPS))/log(1/q1)) + 1
    ax.set_xlim(0, 5)
    ax.set_ylim(-5, 10)
    for x in np.linspace(-2, 2.4, 1000):
        xv.append(x)
        yv.append(g(x))
    ln.set_data(xv, yv)
    return ln,

def animate(frame):
    xv.append(frame)
    yv.append(f(frame))
    ln.set_data(xv, yv)
    return ln,


def dfdx(x):
    return 2*x - exp(-x-1) + 2

def f(x):
    return exp(-x-1) + x*x + 2*x - 1

def g(x):
    return -0.5*(exp(-x-1)+x*x-1)

def SimpleIterationMethod(x0, func):
    """
    Works if |f'| < 1

    """
    #print(n_si)
    booli = ' '
    listi = []
    plt.plot([0, 10], [0, 10], c = 'orange')
    x_si = []
    y_si = []
    m = 0
    x = x0
    x1 = func(x)
    listi.append([' ',m, x, x1, '---------------', '---------------', EPS] )
    x_si.append(x)
    y_si.append(x1)
    #while (q1/(1-q1))*abs(x1 - x) > EPS:
    #while abs(x1 - x) > EPS:
    for i in range(n_si):
        booli = ' '
        temp = x1
        x1 = func(x1)
        x = temp
        m += 1
        if ((q1/(1-q1))*abs(x1 - x) < EPS):
            booli = '*'
        listi.append([booli,m, x1, func(x1), abs(func(x) - func(x1)), abs(x - x1),  EPS])
        x_si.append(x1)
        y_si.append(func(x1))
        if m>=40:
            return 'Use other x0 for simple iteration method'
        plt.scatter(x_si, y_si, s = 10, c = 'red')
        # print(x1)
    output('Simple Iteration: ',listi, False)
    #print(listi)
    return (x1, m)

def NewtonMethod(x0, func, dfunc):
    #print(n_nm)
    booli = ' '
    listi = []
    x = x0
    x1 = x - func(x)/dfunc(x)
    m = 0
    listi.append([booli,m, x, x1, '---------------', '---------------', EPS])
    #while abs(x1 - x) > EPS or abs(func(x1))>EPS:
    for i in range(n_nm):
        booli = ' '
        temp = x1
        x1 = x1 - func(x1)/dfunc(x1)
        x = temp
        m += 1
        if abs(x1 - x) < EPS and abs(func(x1))<EPS:
            booli = '*'
        listi.append([booli, m, x, func(x1), abs(func(x) - func(x1)), abs(x - x1),  EPS])
        if m >= 40:
            if dfunc(x) == dfunc(x0):
                return 'Use other x0 for Newton modified method'
            else:
                return 'Use other x0 for Newton method'
        #output(listi)
       # print(x)
    output('Newton method: ', listi, False)
    return (x1, m)
def SichnihMethod(x0, x1, func):
    listi = []
    x = x1
    x01 = x0
    xn1 = 10
    m = 0
    listi.append([m, x01, x1, '---------------', '---------------', EPS])
    while abs(xn1 - x01) > EPS or abs(func(xn1)) > EPS:
        xn1 = x - ((x - x01)*func(x))/(func(x) - func(x01))
        temp1, temp2, temp3 = x01, x, xn1
        x01 = temp2
        x = temp3
        m += 1
        listi.append([m, x01, abs(func(x01)), abs(func(xn1) - func(x01)), abs(xn1 - x01),  EPS])
        #print(m)
        """if m >= 40:
            if dfunc(x) == dfunc(x0):
                return 'Use other x0 for Newton modified method'
            else:
                return 'Use other x0 for Newton method'"""
        #print(xn1)
    output('Sichnih:', listi, True)
    return (xn1, m)

def NewtonModifyMethod(x0, func, dfunc):
    return NewtonMethod(x0, func, lambda x: dfunc(x0))

def main():
    # |f'| < 1 if -0.648266 < x < 1.0635
    res = SimpleIterationMethod(X0_for_SI, g)

    res2 = NewtonMethod(X0_for_Newton, f, dfdx)

    res3 = SichnihMethod(0, 0.5, f)

    print(res, res2, res3, sep = '\n')
    input()

if __name__ == '__main__':
    main()
# TODO : counter, table output, fix main (all 3 methods use, etc.), exit counter
