from __future__ import division
import numpy as np

__author__ = 'Philipp Warzecha'


# Donwhill Simplex in 3D


"""
ToDo:
1. **!DONE! implement stop criteria
2. **!DONE! wrap everything nicely together
3. more test functions
4. **!DONE! random starting points?
5. make compatible with maya vi (!!important!!)
6. port to 2.7 without future

Changelog:

    Version 0.3:
        - added random starting points, not really sure if thats better
        - restructured solver method a bit, still needs work
        - added two test functions. Styblinski Tang is doable, only one global minimum.
          Schwefel is harder and has many local minima
        - corrected small errors

    Version 0.2.1:
        - corrected error in while loop in solver method, difference barley noticeable

    Version 0.2:
        -ported to Python 2.7 (still with future import)
        -implemented stop criteria
        -wraped everything into solver method

    Version 0.1:
        -Simplex algorithm done. Finds minima and runs smoothly

"""


# x is list of vectors. 4x3 numpy array
# Minimum: square_sum(0,0,0) = 0, only global minimum
def square_sum(x):
    return x[0] ** 2 + x[1] ** 2 + x[2] ** 2


# Minimum: rosenbrock(1,1,1) = 0, only global minimum
def rosenbrock(x):
    return abs(100 * (x[1] - x[0] ** 2) ** 2 + (x[0] - 1) ** 2 + 100 * (x[2] - x[1] ** 2) ** 2 + (x[1] - 1) ** 2)


# Minimum: sytblinski_tang(-2.903534,-2.903534,-2.903534) = -117,49797, only global minimum
# points remain within a distance higher than 10^-9
def styb_tang(x):
    return sum(x ** 4 - 16.0 * x ** 2 + 5.0 * x) * 0.5


# Minimum: schwefel(420.9687,420.9687,420.9687= = 0, many local minima
def schwefel(x):
    return 418.9829 * 3 - sum(x * np.sin(np.sqrt(abs(x))))


# search algorithm, ugly but works fine. x is again 4x3 numpy array.
# Looks better now, still a mess
def simplex(x, testfn):
    last = len(x) - 1.0
    x_centroid = 1 / last * np.array([x[0] + x[1] + x[2]])
    x_reflect = np.array([2 * x_centroid[0] - x[last]])
    x_contract = np.array([(x_centroid[0] + x[last]) * 0.5])
    f_x0 = testfn(x[0])
    f_xreflect = testfn(x_reflect[0])
    f_xworst = testfn(x[last])
    # reflected value is better than worst but not better than best value
    if f_xworst >= f_xreflect > f_x0:
        x[last] = x_reflect[0]
    # reflected value is better than former best, check if expanded value is even better
    elif f_xreflect < f_x0:
        x_expand = np.array(3 * [x_centroid[0] - 2 * x[last]])
        if testfn(x_expand[0]) < f_x0:
            x[last] = x_expand[0]
        else:
            x[last] = x_reflect[0]
    # contracted value is better than worst value
    elif testfn(x_contract[0]) < f_xworst:
        x[last] = x_contract[0]
    # contract every point but the best towards the best point
    else:
        x[:] = (x[0] + x[:]) * 0.5


"""solver uses the simplex downhill algorithm. func is the function to search through for the optimum.
   points is a list of starting points(NxM numpy array).
   stop_value ist the distance between the worst and the best point.
   failure is the number of maximum iterations before the algorithm stops
"""
def solver(func, points, stop_value, failure):
    i = 0
    while abs(points[-1, 0] - points[0, 0]) > stop_value or abs(points[-1, 1] - points[0, 1]) > stop_value \
            or abs(points[-1, 1] - points[0, 1]) > stop_value:
        points = np.asarray(sorted(points, key=func))
        simplex(points, func)
        i += 1
        if i >= failure: break
    if i < failure:
        print "Miminum gefunden bei: \n", points
        print "\nFunktionswerte: ", np.array([func(points[0]), func(points[1]), func(points[2]), func(points[3])])
        print "\nAnzhal Schritte: ", i
    else:
        print "Abbruch nach", i, "Schritten:"
        print "Punkte: \n", points
        print "Funktionswerte: ", np.array([func(points[0]), func(points[1]), func(points[2]), func(points[3])])

# start points
start = np.random.rand(4, 3)
# start = np.array([[-15.0, 20.0, -15.0], [-5.0, -8.0, -2.0], [5.0, -20.0, 6.0], [10.0, -5.0, 3.0]])
solver(styb_tang, start, 10 ** (-8), 10000)
