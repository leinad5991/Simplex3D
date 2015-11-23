import matplotlib
matplotlib.use('TkAgg')

import sys, types, pprint
import numpy as np
from matplotlib import pyplot as pl
from matplotlib import animation

class Kepler:
	"""
	solves the Kepler problem
	"""
	def __init__(self, t0 = 0.0):
		self.t = t0
		self.dt = 0.00002

		self.X = np.array([0.25,0.0]) # initial position
		self.V = np.array([0.0,0.45]) # initial velocity

		#self.scheme = self.euler
		self.scheme = self.midpoint
		#self.scheme = self.leapfrog


		# attributes used for dynamic plotting
		self.x_line = None
		self.y_line = None

	def f(self,X):
		x,y = X
		d3 = (x**2+y**2)**1.5 # ||x||^3
		M = .5
		return np.array([-M*x/d3,-M*y/d3])

	def timestep(self, Nsteps = 1):
		for i in xrange(Nsteps):
			self.scheme()
		self.t += self.dt * Nsteps

	def euler(self):
		Xold = self.X
		self.X = Xold + self.dt*self.V
		self.V = self.V + self.dt*self.f(Xold)

	def midpoint(self):
		Xmid = self.X + 0.5*self.dt*self.V
		Vmid = self.V + 0.5*self.dt*self.f(self.X)
		self.X = self.X + self.dt*Vmid
		self.V = self.V + self.dt*self.f(Xmid)

	def leapfrog(self):
		X = self.X + 0.5*self.dt*self.V
		self.V += self.dt*self.f(X)
		self.X = X + 0.5*self.dt*self.V

odes = Kepler()

Nsteps = 100
t_max = 50 # final start time
frames = int(t_max / float(Nsteps * odes.dt))

xhist,yhist = odes.X

######################################################################
# Set up plot
fig = pl.figure()
ax = pl.axes(xlim=(-0.1,0.3), ylim=(-0.1, 0.1))
line, = ax.plot([], [],lw=2,marker='.',markerfacecolor='red', markersize=12)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
#ax.legend(prop=dict(size=14))
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

######################################################################
# Animate plot
def init():
    line.set_data([], [])
    time_text.set_text('')
    return (line, time_text)

def integrate(i):
	#global xhist,yhist
	odes.timestep(Nsteps)
	x,y = odes.X
	xhist=np.append(xhist,x)
	yhist=np.append(yhist,y)
	line.set_data(xhist,yhist)
	time_text.set_text('time = %.2f' % odes.t)
	return (line, time_text)

anim = animation.FuncAnimation(fig, integrate, init_func=init, frames=frames,
                               interval=0, blit=True,repeat=False)

pl.show()
