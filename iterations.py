#import matplotlib.pyplot as plt
from math import exp

EPS = 0.000001
X0_for_SI = 2 
X0_for_Newton = -5
X0_for_Newton_mod = -5

def dfdx(x):
    return 2*x - exp(-x-1) + 2

def f(x):
    return exp(-x-1) + x*x + 2*x - 1

def g(x):
    return -(exp(-x-1) + x*x - 1)/2

def SimpleIterationMethod(x0, func):
    """
    Works if |f'| < 1

    """
    m = 1
    x = x0
    x1 = func(x)
    while abs(x1 - x) > EPS:
        temp = x1
        x1 = func(x1)
        x = temp
        m += 1
        if m>=40:
            return 'Use other x0 for simple iteration method'
        # print(x1)
    return (x1, m)

def NewtonMethod(x0, func, dfunc):
    x = x0
    x1 = x - func(x)/dfunc(x)
    m = 1
    while abs(x1 - x) > EPS:
        temp = x1
        x1 = x1 - func(x1)/dfunc(x1)
        x = temp
        m += 1
        if m >= 40:
            if dfunc(x) == dfunc(x0):
                return 'Use other x0 for Newton modified method'
            else:
                return 'Use other x0 for Newton method'
       # print(x)
    return (x1, m)

def NewtonModifyMethod(x0, func, dfunc):
    return NewtonMethod(x0, func, lambda x: dfunc(x0))

def main():
    # |f'| < 1 if -0.648266 < x < 1.0635
    res = SimpleIterationMethod(X0_for_SI, g)

    res2 = NewtonMethod(X0_for_Newton, f, dfdx)

    res3 = NewtonModifyMethod(X0_for_Newton_mod, f, dfdx)

    print(res, res2, res3, sep = '\n')

if __name__ == '__main__':
    main()
# TODO : counter, table output, fix main (all 3 methods use, etc.), exit counter