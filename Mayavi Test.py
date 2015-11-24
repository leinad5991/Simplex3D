
from mayavi.mlab import *
from tvtk.tools import visual
import numpy as np
import SimplexDownhill as sd
# Create a figure

f = figure(size=(1000,1000))

# Tell visual to use this as the viewer.
@show
@animate(delay=5000)
def anim(nn):
    #coord=[[0,0,0],[1,0,0],[0,0,1],[0,1,0]]
    coord=nn[0]
    #Colors
    red=(1,0,0)

    print(1)
    visual.set_viewer(f)
    b=[]
    l=[]

    #Initialize Points as balls
    for i in coord:
        b.append(visual.sphere(pos=i,radius=0.05,color=red))
        yield


    for i in coord:
        for j in coord:
            if i != j:
                l.append(plot3d([i[0], (i[0] + j[0]) / 2., j[0]], [i[1], (i[1] + j[1]) / 2., j[1]],
                                     [i[2], (i[2] + j[2]) / 2., j[2]], tube_radius=0.01, color=red))

    #offset
    o=15-5


    
    for i in nn:
        #Update points
        for j in range(4):

            b[j].x=i[j][0]+o
            b[j].y=i[j][1]+o
            b[j].z=i[j][2]+o
            #Color in progress
            '''
            d=sd.square_sum([i[j][0],i[j][1],i[j][2]])/100.
            print(d)
            b[j].color=(np.sin(d)**2,0,np.cos(d)**2)
            b[j].radius=d/10.
            '''

        print("")
        p=0

        #Update lines
        for a in i:
            for c in i:
                if(a!=c):
                    l[p].mlab_source.set(x=[a[0]+o, (a[0]+c[0])/2.+o ,c[0]+o])
                    l[p].mlab_source.set(y=[a[1]+o, (a[1]+c[1])/2.+o ,c[1]+o])
                    l[p].mlab_source.set(z=[a[2]+o, (a[2]+c[2])/2.+o ,c[2]+o])
                    p+=1

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

    obj = contour3d(scalars, contours=[scalars.min() + 0.001 * scalars.ptp()], transparent=True, opacity=1.0)
    obj2 = contour3d(scalars, contours=[scalars.min() + 0.01 * scalars.ptp()], transparent=True, opacity=0.9)
    obj3 = contour3d(scalars, contours=[scalars.min() + 0.1 * scalars.ptp()], transparent=True, opacity=0.8)
    obj4 = contour3d(scalars, contours=[scalars.min() + 0.3 * scalars.ptp()], transparent=True, opacity=0.7)
    obj5 = contour3d(scalars, contours=[scalars.min() + 0.5 * scalars.ptp()], transparent=True, opacity=0.6)

    axes(ranges=[-10, 10, -10, 10, -10, 10], nb_labels=11)

    return obj, obj2, obj3, obj4, obj5


def rosenbrock():
    x, y, z = np.ogrid[-5:5:64j, -5:5:64j, -10:10:64j]

    scalars = 100 * (y - x ** 2) ** 2 + (x - 1) ** 2 + 100 * (z - y ** 2) ** 2 + (y - 1) ** 2

    obj = contour3d(scalars, contours=[scalars.min() + 0.0001 * scalars.ptp()], transparent=True, opacity=1.0)
    obj2 = contour3d(scalars, contours=[scalars.min() + 0.001 * scalars.ptp()], transparent=True, opacity=0.9)
    obj3 = contour3d(scalars, contours=[scalars.min() + 0.01 * scalars.ptp()], transparent=True, opacity=0.8)
    obj4 = contour3d(scalars, contours=[scalars.min() + 0.03 * scalars.ptp()], transparent=True, opacity=0.7)
    obj5 = contour3d(scalars, contours=[scalars.min() + 0.1 * scalars.ptp()], transparent=True, opacity=0.6)
    obj6 = contour3d(scalars, contours=[scalars.min() + 0.3 * scalars.ptp()], transparent=True, opacity=0.5)

    axes(ranges=[-5, 5, -5, 5, -10, 10], nb_labels=11)

    return obj, obj2, obj3, obj4, obj5, obj6


def styb_tang():
    x, y, z = np.ogrid[-10:10:64j, -10:10:64j, -10:10:64j]

    scalars = (x ** 4 - 16.0 * x ** 2 + 5.0 * x) * 0.5 + (y ** 4 - 16.0 * y ** 2 + 5.0 * y) * 0.5 + (
                                                                                                    z ** 4 - 16.0 * z ** 2 + 5.0 * z) * 0.5

    obj = contour3d(scalars, contours=[scalars.min() + 0.0001 * scalars.ptp()], transparent=True, opacity=1.0)
    obj2 = contour3d(scalars, contours=[scalars.min() + 0.001 * scalars.ptp()], transparent=True, opacity=0.9)
    obj3 = contour3d(scalars, contours=[scalars.min() + 0.01 * scalars.ptp()], transparent=True, opacity=0.8)
    obj4 = contour3d(scalars, contours=[scalars.min() + 0.03 * scalars.ptp()], transparent=True, opacity=0.7)
    obj5 = contour3d(scalars, contours=[scalars.min() + 0.1 * scalars.ptp()], transparent=True, opacity=0.6)
    obj6 = contour3d(scalars, contours=[scalars.min() + 0.3 * scalars.ptp()], transparent=True, opacity=0.5)

    axes(ranges=[-5, 5, -5, 5, -10, 10], nb_labels=11)

    return obj, obj2, obj3, obj4, obj5, obj6


# scalar3()
# print(100)
# initialize()
# demoanim()
n = 6
#start = n * np.random.rand(4, 3) - n/2
start = np.array([[-15.0, 20.0, -15.0], [-5.0, -8.0, -2.0], [5.0, -20.0, 6.0], [10.0, -5.0, 3.0]])
nn=np.array(sd.solver(sd.styb_tang, start, 10 ** (-10), 10000)).tolist()

anim(nn)

#square_sum()
# rosenbrock()
# styb_tang()
