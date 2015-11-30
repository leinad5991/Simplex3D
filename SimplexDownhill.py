from __future__ import division
import numpy as np

# Downhill Simplex in 3D
"""
ToDo:
1. **!DONE! implement stop criteria
2. **!DONE! wrap everything nicely together
3. **!DONE! more test functions
4. **!DONE! random starting points?
5. **!DONE! make compatible with maya vi (!!important!!)
6. **!DONE! port to 2.7 without future

Changelog:

    Version 1.0:
        - removed unnecessary code
        - enough test functions
        - import from future removed except division

    Version 0.4:
        - rewrote stop criteria
        - solver method returns points for MayaVi(as a python array)
        - different starting point generation

    Version 0.3:
        - added random starting points, not really sure if thats better
        - restructured solver method a bit, still needs work
        - added two test functions. Styblinski Tang is doable, but has local minima.
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
    return sum(i**2 for i in x)


# Minimum: rosenbrock(1,1,1) = 0, only global minimum
def rosenbrock(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (x[0] - 1) ** 2 + 100 * (x[2] - x[1] ** 2) ** 2 + (x[1] - 1) ** 2


# Minimum: sytblinski_tang(-2.903534,-2.903534,-2.903534) = -117,49797, global minimum, some local minima
# points remain within a distance higher than 10^-9
def styb_tang(x):
    return sum(i ** 4 - 16.0 * i ** 2 + 5.0 * i for i in x) * 0.5


# Minimum: schwefel(420.9687,420.9687,420.9687) = 0, many local minima
def schwefel(x):
    return 418.9829 * 3 - sum(i * np.sin(np.sqrt(abs(i))) for i in x)


# search algorithm, ugly but works fine. x is again 4x3 numpy array.
# Looks better now, still a mess
def simplex(x, testfn):
    last = len(x) - 1.0
    x_centroid = 1 / last * (x[0] + x[1] + x[2])
    x_reflect = (2 * x_centroid - x[last])
    x_contract = (x_centroid + x[last]) * 0.5

    f_x0 = testfn(x[0])
    f_xreflect = testfn(x_reflect)
    f_xworst = testfn(x[last])

    # reflected value is better than worst but not better than best value
    if f_xworst >= f_xreflect > f_x0:
        x[last] = x_reflect[0]
        return "Reflect"
    # reflected value is better than former best, check if expanded value is even better
    elif f_xreflect < f_x0:
        x_expand = 3*x_centroid[0] - 2 * x[last]
        if testfn(x_expand) < f_x0:
            x[last] = x_expand
            return "2xReflect"
        else:
            x[last] = x_reflect
            return "Reflect"
    # contracted value is better than worst value
    elif testfn(x_contract) < f_xworst:
        x[last] = x_contract
        return "1/2xReflect"
    # contract every point but the best towards the best point
    else:
        x[:] = (x[0] + x[:]) * 0.5
        return "Contract"


"""
   solver uses the simplex downhill algorithm. func is the function to search through for the optimum.
   points is a list of starting points(NxM numpy array).
   stop_value ist the distance between the function value of the worst and the best point.
   failure is the number of maximum iterations before the algorithm stops
   maya_points is an array of all points through the search
"""
def solver(func, points, stop_value, failure):
    maya_points = []
    info=[]
    i = 0

    while abs(func(points[-1]) - func(points[0])) > stop_value:
        
        points = np.asarray(sorted(points, key=func))
        info.append(simplex(points, func))
        maya_points.append(points)
        i += 1
        if i >= failure:
            print "Abbruch!"
            break
    if i< failure : print "Minimum gefunden"
    print "bei:\n",points, "\nFunktionswert: ", sum(func(points[:]))/4
    print "\nAnzhal Schritte: ", i
    return info,np.array(maya_points).tolist()