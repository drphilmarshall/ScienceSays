# ============================================================================

import numpy as np
import pylab as plt
import matplotlib.animation as animation
# JSAnimation import available at https://github.com/jakevdp/JSAnimation
# Documentation at http://nbviewer.ipython.org/github/jakevdp/JSAnimation/blob/master/animation_example.ipynb
from JSAnimation import IPython_display as display

# ============================================================================

swarm_params = { 'Npart' : 100 , 'Noverdense' : 0, 'Nunderdense': 0}
color_dict = { 'particle' : 'k.', 'overdense' : 'r.', 'underdense' : 'b.'}
collapseParam = 2

fig = plt.figure()
ax = plt.axes(xlim=(-100, 100), ylim=(-100, 100))
line, = ax.plot([], [], 'b.', ms=10)

# ============================================================================

class agent():

    def __init__(self,id_number,pars):
        self.name = id_number
        self.xpos = pars['x_init']
        self.ypos = pars['y_init']
        self.cat = pars['cat']
        self.direction = 2*np.math.pi*np.random.rand(1)
        return None
    
    def update_position(self, newx, newy):
        self.xpos = newx
        self.ypos = newy
        return None
    
    def changeDirection(self, newdir):
        self.direction = newdir
        return None

# ============================================================================
# PJM: this could maybe be built into agent as a __subtr__ method, to overload
# the '-' operator!
    
def agentSep(agent1,agent2):
    return np.sqrt((agent1.xpos-agent2.xpos)**2+(agent1.ypos-agent2.ypos)**2)

# ============================================================================

class swarm():
    
    def __init__(self, pars):
        
        self.members = []
        
        for i in np.arange(pars['Npart']):
            temp = agent(i,{'x_init':0, 'y_init':0, 'cat': 'particle'})
            self.members.append(temp)
    
    def timeEvolveBeforeDecoupling(self, N):
        counter = 0
        while counter < N:
            for member in self.members:
                member.update_position(member.xpos+np.cos(member.direction),member.ypos+np.sin(member.direction))
            counter += 1
        
    def timeEvolveAfterDecoupling(self,N):
        counter = 0
        while counter < N:
            for member in self.members:
                minDist = 10000
                ydiff = 1000
                xdiff = 1000
                for other in self.members:
                    if agentSep(member,other) < minDist and other.name != member.name:
                        minDist = agentSep(member,other)
                        xdiff = other.xpos - member.xpos
                        ydiff = other.ypos - member.ypos
                #member.changeDirection(np.arctan2(ydiff,xdiff))
                if agentSep(member,other) != 0:
                    member.update_position(member.xpos+collapseParam*xdiff/agentSep(member,other),member.ypos+collapseParam*ydiff/agentSep(member,other))
            counter += 1
                
    def showCurrentState(self):
        plt.figure()
        plt.grid(b=True, which='major', color='0.65',linestyle='-')
        for member in self.members:
            plt.plot(member.xpos,member.ypos,'b.')
        
    def animInit(self):
        line.set_data([], [])
        return line,
    
    def makeAnim(self,i):
        if i < 50:
            self.timeEvolveBeforeDecoupling(1)
        else: 
            self.timeEvolveAfterDecoupling(1)
        xvec = []
        yvec = []
        for member in self.members:
            xvec.append(member.xpos)
            yvec.append(member.ypos)
        line.set_data(np.array(xvec),np.array(yvec))
        return line
        
    def play(self):
        movie = animation.FuncAnimation(fig, self.makeAnim, init_func=self.animInit,
                        frames=100, interval=20, blit=True)
        return movie                        

# ============================================================================

