
from mayavi import mlab
from tvtk.tools import visual
import numpy as np
# Create a figure

f = mlab.figure(size=(1000,1000))

# Tell visual to use this as the viewer.
@mlab.show
@mlab.animate(delay=20)





def initialize():
    coord=[[0,0,0],[1,0,0],[0,0,1],[0,1,0]]
    #Colors
    red=(1,0,0)

    print(1)
    visual.set_viewer(f)
    b=[]
    l=[]
    yield
    for i in coord:
        b.append(visual.sphere(pos=i,radius=0.05))
        yield
    '''
    for i in coord:
        for j in coord:
            if i!=j:
                l.append(mlab.plot3d( [i[0],(i[0]+j[0])/2.,j[0]] ,[i[1],(i[1]+j[1])/2.,j[1]] ,[i[2],(i[2]+j[2])/2.,j[2]] ,tube_radius=0.01,color=red))
                yield

'''
    print("a")
    t=np.arange(1,1000,0.1)
    nn=[]
    for j in t: nn.append([[0.,np.sin(j/10.),np.sin(j/10.)],[np.sin(j/10.),0.,0.],[0.,0.,np.sin(j/10.)],[0.,np.sin(j/10.),0.]])

    
    for i in nn:
        for j in range(4):
            print(i[0][1])
            b[j].x=i[j][0]
            b[j].y=i[j][1]
            b[j].z=i[j][2]
            yield

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

def scalar():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    #s = 2*x**2+y**2+z**2
    s= np.sin(x*y*z)/(x*y*z)
    #mlab.pipeline.volume(mlab.pipeline.scalar_field(s))
    mlab.pipeline.volume(mlab.pipeline.scalar_field(s),vmin=0, vmax=0.8)
    mlab.show()

#scalar()
print(100)
initialize()
#demoanim()
