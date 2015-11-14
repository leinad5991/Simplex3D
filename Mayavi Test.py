
from mayavi import mlab
from tvtk.tools import visual
import numpy as np
# Create a figure

f = mlab.figure(size=(1000,1000))

# Tell visual to use this as the viewer.
@mlab.show
@mlab.animate(delay=20)
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
def anim():
    #Colors
    red=(1,0,0)


    visual.set_viewer(f)
    coord=[[0,0,0],[1,0,0],[0,0,1],[0,1,0]]
    b=[]
    l=[]
    for i in coord: b.append(visual.sphere(pos=i,radius=0.1))

    for i in coord:
        for j in coord:
            if i!=j:
                l.append(mlab.plot3d( [i[0],(i[0]+j[0])/2.,j[0]] ,[i[1],(i[1]+j[1])/2.,j[1]] ,[i[2],(i[2]+j[2])/2.,j[2]] ,tube_radius=0.01,color=red))

    mlab.show()



def scalar():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    #s = 2*x**2+y**2+z**2
    s= np.sin(x*y*z)/(x*y*z)
    #mlab.pipeline.volume(mlab.pipeline.scalar_field(s))
    mlab.pipeline.volume(mlab.pipeline.scalar_field(s),vmin=0, vmax=0.8)
    mlab.show()

#scalar()
anim()
