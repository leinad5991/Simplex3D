
from mayavi import mlab
from tvtk.tools import visual
import numpy as np
# Create a figure


f = mlab.figure(size=(1000,1000))
print(10)
t=np.arange(1,100,0.1)
nn=[]
for j in t: nn.append([[0.,np.sin(j/10.),np.sin(j/10.)],[np.sin(j/10.),0.,0.],[0.,0.,np.sin(j/10.)],[0.,np.sin(j/10.),0.]])
# Tell visual to use this as the viewer.
@mlab.show
@mlab.animate(delay=50)
def initialize():
    coord=[[0,0,0],[1,0,0],[0,0,1],[0,1,0]]
    #Colors
    red=(1,0,0)

    print(1)
    visual.set_viewer(f)
    b=[]
    l=[]

    for i in coord:
        b.append(visual.sphere(pos=i,radius=0.05))


    for i in coord:
        for j in coord:
            if i!=j:
                l.append(mlab.plot3d( [i[0],(i[0]+j[0])/2.,j[0]] ,[i[1],(i[1]+j[1])/2.,j[1]] ,[i[2],(i[2]+j[2])/2.,j[2]] ,tube_radius=0.01,color=red))





    
    for i in nn:
        for j in range(4):

            b[j].x=i[j][0]
            b[j].y=i[j][1]
            b[j].z=i[j][2]
        p=0
        for a in i:
            for c in i:
                if(a!=c):
                    l[p].mlab_source.set(x=[a[0], (a[0]+c[0])/2. ,c[0]])
                    l[p].mlab_source.set(y=[a[1], (a[1]+c[1])/2. ,c[1]])
                    l[p].mlab_source.set(z=[a[2], (a[2]+c[2])/2. ,c[2]])
                    p+=1

        yield
@mlab.show
@mlab.animate(delay=50)
def demoanim():
    visual.set_viewer(f)

    a=np.arange(-4,4,0.1)
    x = a
    y = np.sin(a)
    z = a*0
    s = mlab.plot3d(x,y,z)
    # Even sillier animation.
    b1 = visual.sphere()
    b2 = visual.box(x=4, color=visual.color.red)
    b3 = visual.box(x=-4, color=visual.color.red)


    i=0
    while True:
        s.mlab_source.set(y=np.sin(a+i/10.))
        i+=1
        f.scene.camera.azimuth(0.5)
        b1.x=2*np.sin(i/10.)
        yield

def anim(coords,obj):
    visual.set_viewer(f)
    print(2)
    b=obj[0]
    l=obj[1]
    print(1)
    for c in coords:
        for i in b:

            i.mlab_source.set(x=c[0],y=c[1],z=c[2])
            yield
def scalar3():

    s=64
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]

    data = x*y*z

    grid = mlab.pipeline.scalar_field(data)
    grid.spacing = [1.0, 1.0, 2.0]

    contours = mlab.pipeline.contour_surface(grid,
                             contours=np.logspace(1,10,base=2).tolist(), transparent=True)
    mlab.show()

def scalar2():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    s= np.sin(x*y*z)/(x*y*z)
    src=mlab.pipeline.volume(mlab.pipeline.scalar_field(s),vmin=0, vmax=0.8)
    #mlab.outline()
    mlab.show()

def scalar1():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    #s = 2*x**2+y**2+z**2
    s= np.sin(x*y*z)/(x*y*z)
    #mlab.pipeline.volume(mlab.pipeline.scalar_field(s))
    src=mlab.pipeline.volume(mlab.pipeline.scalar_field(s),vmin=0, vmax=0.8)
    mlab.pipeline.iso_surface(src, contours=[s.min()+0.1*s.ptp(), ], opacity=0.1)  # ptp is the range
    mlab.pipeline.iso_surface(src, contours=[s.max()-0.1*s.ptp(), ],)
    mlab.pipeline.image_plane_widget(src,
                                 plane_orientation='z_axes',
                                 slice_index=10)


    mlab.show()

scalar3()
print(100)
#initialize()
#demoanim()
