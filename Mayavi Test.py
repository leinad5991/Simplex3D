
from mayavi import mlab
from tvtk.tools import visual
import numpy as np
# Create a figure

f = mlab.figure(size=(1000,1000))

# Tell visual to use this as the viewer.
@mlab.show
@mlab.animate(delay=20)
def anim():
    visual.set_viewer(f)

    a=np.arange(-4,4,0.1)
    x = a
    y = np.sin(a)
    z = a*0
    s = mlab.plot3d(x,y,z)
    # Even sillier animation.
    b1 = visual.sphere()
    b2 = visual.box(x=4., color=visual.color.red)
    b3 = visual.box(x=-4, color=visual.color.red)


    i=0
    while True:
        s.mlab_source.set(y=np.sin(a+i/10.))
        i+=1
        f.scene.camera.azimuth(0.5)
        b1.x=2*np.sin(i/10.)
        yield

def scalar():
    x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    s = 2*x**2+y**2+z**2

    mlab.pipeline.volume(mlab.pipeline.scalar_field(s))

scalar()
#anim()
