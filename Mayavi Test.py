from mayavi.mlab import *
from tvtk.tools import visual
import numpy as np
import SimplexDownhill as sd

reload(sd)

"""
ToDo:
1. **!DONE! Make the different coordinate systems work together
2. **!DONE!Add more collors to points
3. **!DONE!rewrite scalar functions
4. clean up code
5. **!DONE! implement Schwefel function
6. add more commentary
Changelog:

    Version 0.3:
        - colored points
        - better code for scalar functions

    Version 0.2:
        - added Schwefel function
        - resolved problem between different coordinate systems
        - rewrote the scalar functions
    Version 0.1:
        - basic animation and scalar fields work, but not together
"""
# Create a figure. Tell visual to use this as the viewer.
f = figure(size=(1000, 1000))
# Create box item for coordinate reference.
box = [10, -10, 10, -10, 10, -10]


@show
@animate(delay=2000)
def anim(nn, info):
    txt = text(0.1, 0.9, "hola", line_width=200, figure=f)

    # coord=[[0,0,0],[1,0,0],[0,0,1],[0,1,0]]
    coord = nn[0]
    # Colors
    red = (1, 0, 0)
    deb = 0
    visual.set_viewer(f)
    b = []
    l = []

    # Initialize Points as balls
    for i in coord:
        b.append(visual.sphere(pos=i, radius=0.40, color=red, extent=box))

    # Initialize lines between points
    for i in coord:
        for j in coord:
            if i != j:
                l.append(plot3d([i[0], (i[0] + j[0]) / 2., j[0]], [i[1], (i[1] + j[1]) / 2., j[1]],
                                [i[2], (i[2] + j[2]) / 2., j[2]], tube_radius=0.08))

    for i in nn:

        txt.text = info[deb]
        deb += 1
        # Update points
        for j in range(4):
            b[j].x = i[j][0]
            b[j].y = i[j][1]
            b[j].z = i[j][2]
            # Color in progress

            # b[j].radius=np.sqrt(d)

        b[0].color = (0, 0, 0)
        b[1].color = (0, 0, 0)
        b[2].color = (0, 0, 0)
        b[3].color = (1, 0, 0)

        p = 0

        # Update lines
        for a in i:
            for c in i:
                if (a != c):
                    l[p].mlab_source.set(x=[a[0], (a[0] + c[0]) / 2., c[0]])
                    l[p].mlab_source.set(y=[a[1], (a[1] + c[1]) / 2., c[1]])
                    l[p].mlab_source.set(z=[a[2], (a[2] + c[2]) / 2., c[2]])
                    p += 1

        yield


@show
@animate(delay=50)
def demoanim():
    visual.set_viewer(f)

    a = np.arange(-4, 4, 0.1)
    x = a
    y = np.sin(a)
    z = a * 0
    s = plot3d(x, y, z)
    # Even sillier animation.
    b1 = visual.sphere()
    b2 = visual.box(x=4, color=visual.color.red)
    b3 = visual.box(x=-4, color=visual.color.red)

    i = 0
    while True:
        s.mlab_source.set(y=np.sin(a + i / 10.))
        i += 1
        f.scene.camera.azimuth(0.5)
        b1.x = 2 * np.sin(i / 10.)
        yield


def scalar(lev, func):
    global box
    x, y, z = np.ogrid[-10:10:128j, -10:10:128j, -10:10:128j]
    scalars = func([x, y, z])
    levels = []
    for i in lev:
        levels.append(scalars.min() + i * scalars.ptp())
    obj = contour3d(scalars, contours=levels, transparent=True, extent=box)
    obj.actor.property.set(representation='p')
    obj.actor.property.backface_culling = True

    axes(ranges=[-10, 10, -10, 10, -10, 10], nb_labels=11)
    return obj


def square_sum():
    return scalar([0.001, 0.01, 0.1, 0.3, 0.5], sd.square_sum)


def rosenbrock():
    return scalar([0.0001, 0.001, 0.01, 0.03, 0.1, 0.3], sd.rosenbrock)


def styb_tang():
    return scalar([0.0001, 0.001, 0.01, 0.03, 0.1, 0.3], sd.styb_tang)


def schwefel():
    return scalar([0.05, 0.01, 0.2, 0.3, 0.33], sd.schwefel)


n = 6
# start = n * np.random.rand(4, 3) - n/2
start = np.array([[-5.0, 2.0, -1.0], [-9, -8.0, -2.0], [5.0, -2.0, 6.0], [9, 9, 9]])
info, nn = sd.solver(sd.square_sum, start, 10 ** (-10), 10000)

# scalar([0.001,0.01,0.1,0.3,0.5],sd.square_sum)
square_sum()
# rosenbrock()
# styb_tang()
# schwefel()

anim(nn, info)
