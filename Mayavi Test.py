from mayavi.mlab import *
from tvtk.tools import visual
import numpy as np
import SimplexDownhill as sd

"""
ToDo:
1. **!DONE! Make the different coordinate systems work together
2. Add more collors to points
3. (almost done)rewrite scalar functions
4. clean up code
5. **!DONE! implement Schwefel function
6. add more commentary

Changelog:
    
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
@animate(delay=5000)
def anim(nn):
    # coord=[[0,0,0],[1,0,0],[0,0,1],[0,1,0]]
    coord = nn[0]
    # Colors
    red = (1, 0, 0)

    print(1)
    visual.set_viewer(f)
    b = []
    l = []

    # Initialize Points as balls
    for i in coord:
        b.append(visual.sphere(pos=i, radius=0.40, color=red, extent=box))
        yield

    # Initialize lines between points
    for i in coord:
        for j in coord:
            if i != j:
                l.append(plot3d([i[0], (i[0] + j[0]) / 2., j[0]], [i[1], (i[1] + j[1]) / 2., j[1]],
                                [i[2], (i[2] + j[2]) / 2., j[2]], tube_radius=0.08, color=red))

    # offset
    o = 0

    for i in nn:
        # Update points
        for j in range(4):
            b[j].x = i[j][0] + o
            b[j].y = i[j][1] + o
            b[j].z = i[j][2] + o
            # Color in progress
            '''
            d=sd.square_sum([i[j][0],i[j][1],i[j][2]])/100.
            print(d)
            b[j].color=(np.sin(d)**2,0,np.cos(d)**2)
            b[j].radius=d/10.
            '''

        print("")
        p = 0

        # Update lines
        for a in i:
            for c in i:
                if (a != c):
                    l[p].mlab_source.set(x=[a[0] + o, (a[0] + c[0]) / 2. + o, c[0] + o])
                    l[p].mlab_source.set(y=[a[1] + o, (a[1] + c[1]) / 2. + o, c[1] + o])
                    l[p].mlab_source.set(z=[a[2] + o, (a[2] + c[2]) / 2. + o, c[2] + o])
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


def scalar3():
    s = 64
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]

    data = x * y * z

    grid = pipeline.scalar_field(data)
    grid.spacing = [1.0, 1.0, 2.0]

    contours = pipeline.contour_surface(grid,
                                        contours=np.logspace(1, 10, base=2).tolist(), transparent=True)
    show()


def scalar2():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    s = np.sin(x * y * z) / (x * y * z)
    src = pipeline.volume(pipeline.scalar_field(s), vmin=0, vmax=0.1)
    # outline()
    show()


def scalar1():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    # s = 2*x**2+y**2+z**2
    s = np.sin(x * y * z) / (x * y * z)
    # pipeline.volume(pipeline.scalar_field(s))
    src = pipeline.volume(pipeline.scalar_field(s), vmin=0, vmax=0.8)
    pipeline.iso_surface(src, contours=[s.min() + 0.1 * s.ptp(), ], opacity=0.1)  # ptp is the range
    pipeline.iso_surface(src, contours=[s.max() - 0.1 * s.ptp(), ], )
    pipeline.image_plane_widget(src,
                                plane_orientation='z_axes',
                                slice_index=10)

    show()


def square_sum():
    x, y, z = np.ogrid[-10:10:64j, -10:10:64j, -10:10:64j]
    scalars = x ** 2 + y ** 2 + z ** 2
    levels = [scalars.min() + 0.001, scalars.min() + 0.01 * scalars.ptp(), scalars.min() + 0.1 * scalars.ptp(),
              scalars.min() + 0.3 * scalars.ptp(), scalars.min() + 0.5 * scalars.ptp()]

    obj = contour3d(scalars, contours=levels, transparent=True, opacity=0.6, extent=box)
    axes(ranges=[-10, 10, -10, 10, -10, 10], nb_labels=11)

    return obj


def rosenbrock():
    x, y, z = np.ogrid[-10:10:64j, -10:10:64j, -10:10:64j]
    scalars = 100 * (y - x ** 2) ** 2 + (x - 1) ** 2 + 100 * (z - y ** 2) ** 2 + (y - 1) ** 2
    levels = [scalars.min() + 0.0001 * scalars.ptp(), scalars.min() + 0.001, scalars.min() + 0.01 * scalars.ptp(),
              scalars.min() + 0.03 * scalars.ptp(), scalars.min() + 0.1 * scalars.ptp(),
              scalars.min() + 0.3 * scalars.ptp()]

    obj = contour3d(scalars, contours=levels, transparent=True, opacity=0.6, extent=box)
    axes(ranges=[-10, 10, -10, 10, -10, 10], nb_labels=11)

    return obj


def styb_tang():
    x, y, z = np.ogrid[-10:10:64j, -10:10:64j, -10:10:64j]
    scalars = (x ** 4 - 16.0 * x ** 2 + 5.0 * x) * 0.5 + (y ** 4 - 16.0 * y ** 2 + 5.0 * y) * 0.5 + (
                                                                                                        z ** 4 - 16.0 * z ** 2 + 5.0 * z) * 0.5
    levels = [scalars.min() + 0.0001 * scalars.ptp(), scalars.min() + 0.001, scalars.min() + 0.01 * scalars.ptp(),
              scalars.min() + 0.03 * scalars.ptp(), scalars.min() + 0.1 * scalars.ptp(),
              scalars.min() + 0.3 * scalars.ptp()]

    obj = contour3d(scalars, contours=levels, transparent=True, opacity=0.6, extent=box)
    axes(ranges=[-10, 10, -10, 10, -10, 10], nb_labels=11)

    return obj


def schwefel():
    x, y, z = np.ogrid[-500:500:128j, -500:500:128j, -500:500:128j]
    scalars = 418.9829 * 3 - x * np.sin(np.sqrt(abs(x))) - y * np.sin(np.sqrt(abs(y))) - z * np.sin(np.sqrt(abs(z)))
    levels = [scalars.min() + 0.05 * scalars.ptp(), scalars.min() + 0.1 * scalars.ptp(),
              scalars.min() + 0.2 * scalars.ptp(), scalars.min() + 0.3 * scalars.ptp()]

    obj = contour3d(scalars, contours=levels, transparent=True, opacity=0.6, extent=box)
    axes(ranges=[-10, 10, -10, 10, -10, 10], nb_labels=11)

    return obj


n = 6
# start = n * np.random.rand(4, 3) - n/2
start = np.array([[-5.0, 2.0, -1.0], [-5.0, -8.0, -2.0], [5.0, -2.0, 6.0], [10.0, -5.0, 3.0]])
nn = np.array(sd.solver(sd.square_sum, start, 10 ** (-10), 10000)).tolist()

anim(nn)

square_sum()
# rosenbrock()
# styb_tang()
# schwefel()
