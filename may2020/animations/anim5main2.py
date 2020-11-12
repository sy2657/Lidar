import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv

# input : arrays holding the x,y coordinates
grandx = []
grandy = []

lengths = []

labs = [1,2,3,4,5,6,7,8,9,10]

# frame 467, 468 and pframe440c10f+str(i)

#  show all vehicles, all points, 30 sec

totx1 = []
toty1 = []

for i in range(0, 4):
    fname1 = "pframe100/pframe100c1f"+str(i)+".csv"
    axframe1 = []
    ayframe1 = []
    with open(fname1) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        rowind = 0
        for row in csv_reader:
            axframe1.append(float(row[0]))
            ayframe1.append(float(row[1]))
            rowind = rowind+1
            if rowind>=20: # 10 
                break
    totx1.append(axframe1)
    toty1.append(ayframe1)

for i1 in range(4, 48):
    axframe1 = 20*[np.nan]
    ayframe1 = 20*[np.nan]
    totx1.append(axframe1)
    toty1.append(ayframe1)
    
    
totx2 = []
toty2 = []
# frame 70
for i in range(0, 48):
    fname = "pframe100/pframe100c2f"+str(i)+".csv"
    axframe1 = []
    ayframe1 = []
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        rowind = 0
        for row in csv_reader:
            axframe1.append(float(row[0]))
            ayframe1.append(float(row[1]))
            rowind=rowind+1
            if rowind>=20:
                break
    totx2.append(axframe1)
    toty2.append(ayframe1)

totx3 = []
toty3 = []
for i in range(0, 4):
    fname = "pframe100/pframe100c5f"+str(i)+".csv"
    axframe1 = []
    ayframe1 = []
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        rowind = 0
        for row in csv_reader:
            axframe1.append(float(row[0]))
            ayframe1.append(float(row[1]))
            rowind=rowind+1
            if rowind>=20:
                break
    totx3.append(axframe1)
    toty3.append(ayframe1)

for i1 in range(4, 48):
    axframe1 = 20*[np.nan]
    ayframe1 = 20*[np.nan]
    totx3.append(axframe1)
    toty3.append(ayframe1)

# combine totx2 and totx3
totx4 = []
toty4 = []

for j in range(0,48):
    xlen1 = len(totx1[j])
    xlen2 = len(totx2[j])
    xlen3 = len(totx3[j])
    ylen1 = len(toty1[j])
    ylen2 = len(toty2[j])
    ylen3 = len(toty3[j])
    tx1 = totx1[j]
    tx2 = totx2[j]
    tx3 = totx3[j]
    ty1 = toty1[j]
    ty2 = toty2[j]
    ty3 = toty3[j]
    if xlen1 <20:
        e = totx1[j][0]
        for i in range(xlen1, 20):
            tx1.append(e)
    if xlen2 <20:
        e = totx2[j][0]
        for i in range(xlen2, 20):
            tx2.append(e)
    if xlen3 <20:
        e = totx3[j][0]
        for i in range(xlen3, 20):
            tx3.append(e)
    if ylen1 <20:
        e = toty1[j][0]
        for i in range(ylen1, 20):
            ty1.append(e)
    if ylen2 <20:
        e = toty2[j][0]
        for i in range(ylen2, 20):
            ty2.append(e)
    if ylen3 <20:
        e = toty3[j][0]
        for i in range(ylen3, 20):
            ty3.append(e)
    cx = tx1 + tx2 + tx3
    cy = ty1 + ty2 + ty3
    totx4.append(cx)
    toty4.append(cy)



# read following frame
followarrayx=[]
followarrayy=[]
followframe = 'frame480points.csv'
followframe = 'frame467points.csv'
followframe = 'frame101points.csv'
followframe = 'frame149points.csv'

frows = 0
with open(followframe) as followfile:
    csv_follow = csv.reader(followfile, delimiter=",")
    for row in csv_follow:
        followarrayx.append(float(row[0]))
        followarrayy.append(float(row[1]))
        frows=frows+1
        
# set color
followcolor = frows*[9]

    
#mlen = max(lengths)

cdatax = []
cdatay = []
'''
for j in range(0, mlen):
    elemjx = []
    elemjy = []
    for i in range(0, nend-1):
        xa = grandx[i]
        ya = grandy[i]
        if j >= lengths[i]:
            exa = np.nan
            eya = np.nan
        else:
            exa = xa[j]
            eya = ya[j]
        elemjx.append(exa)
        elemjy.append(eya)
    cdatax.append(elemjx)
    cdatay.append(elemjy)
'''
#print("cdatax", cdatax)

class AnimatedScatter(object):
    
    def __init__(self, numpoints=3):
        self.numpoints = numpoints
        self.time_elapsed= 0
        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        #self.stream = self.data_stream()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1000, 
                                           init_func=self.setup_plot, blit=True)
    
    def setup_plot(self):
        #self.time_elapsed = int(self.time_elapsed+1)
        print("time", self.time_elapsed)
        coorddata1 = np.random.random((1, self.numpoints))
        coorddata2 = np.random.random((1, self.numpoints))
        coorddata3 = np.random.random((1, self.numpoints))
        #coorddata1 = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        #coorddata2 = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        coorddata4 = np.random.random((1, self.numpoints))
        #coorddata4 = np.array([5])
        #x,y,s,c = next(self.stream)
        #self.scat = self.ax.scatter(coorddata1, coorddata2, c=coorddata3, s=coorddata4, animated= True)
        #self.scat = self.ax.scatter(np.array(arrayx[self.time_elapsed]),np.array(arrayy[self.time_elapsed]), c=coorddata3, s=coorddata4, animated=True)
        self.scat = self.ax.scatter(coorddata1, coorddata2, c = coorddata3, s=coorddata4, animated=True)
        self.ax.axis([-120, 120, -120, 120])
        return self.scat,
    
    def update(self, i):
        dt =1 
        self.time_elapsed += dt
        self.time_elapsed = int(self.time_elapsed)
        #x1 = arrayx[self.time_elapsed]
        #y1 = arrayy[self.time_elapsed]
        cdata = 10*np.random.random((self.numpoints, 2))
        col = np.random.random((self.numpoints))
        #data = next(self.stream)
        # set x and y data
        self.scat.set_offsets(cdata)
        #self.scat.set_offsets(data[:2, :])
        self.scat.set_array(col)
        # set size
        #self.scat._sizes = 2
        # colors
        #self.scat.set_array([2,3])
        
        # each has 5 pts 
        coorddata3 = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]) # 10 or 20 numbers
        coorddata4 = np.array([5,5,5,5,5,5,5,5,5])
        
        coorddata1 = totx4 # totx , cdatax
        coorddata2 = toty4 # toty, cdatay
        #coorddata1 = np.array([[1,2],[2,1],[3,1],[4,1],[5,1],[6,2],[7,2],[8,3],[9,1],[10,1],[11,1],[12,1],[13,2],[14,1],[15,1]])
        #coorddata2 = np.array([[1,1],[2,1],[3,2],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,2],[11,3],[12,1],[13,1],[14,1],[15,2]])
        if self.time_elapsed > 47:
            # plot frame after
            self.scat = self.ax.scatter(followarrayx, followarrayy, c = followcolor, animated= True)
            return self.scat,
        
        #print("size of x", len(coorddata1[self.time_elapsed]))
        print("time elaps", self.time_elapsed)
        self.scat = self.ax.scatter(coorddata1[self.time_elapsed], coorddata2[self.time_elapsed], c = coorddata3, animated=True)
        

        return self.scat,
    
    def show(self):
        plt.show()
        
if __name__ == '__main__':
    a= AnimatedScatter()
    a.show()
