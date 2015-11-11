
from mayavi import mlab
from tvtk.tools import visual
import numpy as np
# Create a figure
f = mlab.figure(size=(500,500))

# Tell visual to use this as the viewer.
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
b1.v = 5.0

@mlab.show
@mlab.animate(delay=20)
def anim():
    i=0
    while True:
        s.mlab_source.set(y=np.sin(a+i/10.))
        i+=1
        f.scene.camera.azimuth(0.5)
        b1.x=2*np.sin(i/10.)
        yield

# Run the animation.
anim()