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

    Version 0.4:
        - improved visuals of scalar functions

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
# Create array for coordinate reference.
box = [10, -10, 10, -10, 10, -10]


@show
@animate(delay=2000)
def anim(data, info):
    
    visual.set_viewer(f)
    
    #Text
    txt = text(0.1, 0.9, info[0], figure=f)
    txt.property.bold = 1

    
    # Colors
    red, black = (1, 0, 0), (0, 0, 0)
    
    #Iteration
    it=1
    
    #Balls and Lines
    b = []
    l = []
    
    #First coordinate
    coord = data[0]
    
    # Initialize Points as balls
    for i in coord:
        b.append(visual.sphere(pos=i, radius=0.25, color=black, extent=box))

    # Initialize lines between points
    for i in coord:
        for j in coord:
            if i != j:
                l.append(plot3d([i[0], (i[0] + j[0]) / 2., j[0]], [i[1], (i[1] + j[1]) / 2., j[1]],
                                [i[2], (i[2] + j[2]) / 2., j[2]], tube_radius=0.05))
    yield
    for i in data[1:]:

        txt.text = info[it]
        it += 1
        
        # Update points
        for j in range(4):
            b[j].x = i[j][0]
            b[j].y = i[j][1]
            b[j].z = i[j][2]

        #Ball color
        b[0].color = black
        b[1].color = black
        b[2].color = black
        b[3].color = red

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

    points = np.arange(-4, 4, 0.1)
    x = points
    y = np.sin(points)
    z = points * 0
    #Line Plot
    plot = plot3d(x, y, z)
    
    #Ball Plot
    ball = visual.sphere()

    i = 0
    while True:
        #Plot Update
        plot.mlab_source.set(y=np.sin(points + i / 10.))
        
        #Ball Update
        ball.x = 2 * np.sin(i / 10.)
        
        i += 1
        yield


def scalar(lev, func, size):
    global box
    d = size
    x, y, z = np.ogrid[-d:d:128j, -d:d:128j, -d:d:128j]
    scalars = func([x, y, z])
    levels = []
    for i in lev:
        levels.append(scalars.min() + i * scalars.ptp() * f.scene.magnification)
    obj = contour3d(scalars, contours=levels, transparent=True, extent=box)
    obj.actor.property.set(representation='p')
    obj.actor.property.backface_culling = True

    axes(ranges=[-d, d, -d, d, -d, d], nb_labels=11)
    return obj


def square_sum():
    iso = scalar([0.001, 0.01, 0.1, 0.3, 0.5], sd.square_sum, 10)
    iso.module_manager.scalar_lut_manager.lut.scale = "linear"
    iso.module_manager.scalar_lut_manager.data_range = [0.0, 170.0]


def rosenbrock():
    iso = scalar([0.0001, 0.001, 0.01, 0.03, 0.1, 0.3], sd.rosenbrock, 10)
    iso.module_manager.scalar_lut_manager.lut.scale = "log10"
    iso.module_manager.scalar_lut_manager.data_range = [1000.0, 4000000.0]


def styb_tang():
    iso = scalar([0.0003, 0.003, 0.01, 0.03, 0.1, 0.3], sd.styb_tang, 10)
    iso.module_manager.scalar_lut_manager.lut.scale = "log10"
    iso.module_manager.scalar_lut_manager.data_range = [0.0, 12000.0]


def schwefel():
    iso = scalar([0.05, 0.01, 0.2, 0.3, 0.33], sd.schwefel, 600)
    iso.module_manager.scalar_lut_manager.lut.scale = "linear"
    iso.module_manager.scalar_lut_manager.data_range = [0.0, 1500.0]


n = 20
start = n * np.random.rand(4, 3) - n/2
#start = np.array([[-5.0, 2.0, -1.0], [-9, -8.0, -2.0], [5.0, -2.0, 6.0], [9, 9, 9]])

info, data = sd.solver(sd.styb_tang, start, 10 ** (-10), 10000)



#square_sum()
#rosenbrock()
styb_tang()
#schwefel()
#demoanim()
anim(data,info)
