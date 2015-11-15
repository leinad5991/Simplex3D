__author__ = 'Philipp Warzecha'

# Donwhill Simplex Verfahren in 3D

"""
Version 0.1

ToDo:
1. implement stop criteria
2. wrap everthing nicely together
3. more test functions
4. randoom starting points?
5. graphics, etc..
"""

import numpy as np
from matplotlib import pyplot as pl


# 2 testfunctions, 1 global minimum, no local minimum each.
# x is list of vectors. 4x3 numpy array
def square_sum(x):
    return x[0] ** 2 + x[1] ** 2 + x[2] ** 2


def rosenbrock(x):
    return abs(100 * (x[1] - x[0] ** 2) ** 2 + (x[0] - 1) ** 2 + 100 * (x[2] - x[1] ** 2) ** 2 + (x[1] - 1) ** 2)


# search algorithm, ugly but works fine. x is again 4x3 numpy array
def reflect(x, testfn):
    last = len(x) - 1
    x_centroid = 1 / last * np.array([x[0] + x[1] + x[2]])
    x_reflect = np.array([2 * x_centroid[0] - x[last]])
    x_contract = np.array([(x_centroid[0] + x[last]) / 2])
    if testfn(x[last]) >= testfn(x_reflect[0]) > testfn(x[0]):
        x[last] = x_reflect[0]
    elif testfn(x_reflect[0]) < testfn(x[0]):
        x_expand = np.array(3 * [x_centroid[0] - 2 * x[last]])
        if testfn(x_expand[0]) < testfn(x[0]):
            x[last] = x_expand[0]
        else:
            x[last] = x_reflect[0]
    elif testfn(x_contract[0]) < testfn(x[last]):
        x[last] = x_contract[0]
    else:
        x[:] = (x[0] + x[:]) * 0.5


# start points
points = np.array([[-15.0, 20.0, -150.0], [-5.0, -8.0, -2.0], [5.0, -20.0, 6.0], [10.0, -51.0, 3.0]])

print("Punkte: \n", points)
# loop through the algorithm
# strange behaviour in print("Funktionswerte:..."), therefor a bit clumsy coding
for i in range(1000):
    print("Funktionswerte: ",
          np.array([square_sum(points[0]), square_sum(points[1]), square_sum(points[2]), square_sum(points[3])]))
    points = np.asarray(sorted(points, key=square_sum))
    reflect(points, square_sum)
    print("Punkte: \n", points)
