import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv

# input : arrays holding the x,y coordinates
grandx = []
grandy = []

lengths = []

nend=10
for i in range(1, nend):
    arrayx =[]
    arrayy =[]
    csv_file_name = 'p'+str(440)+'ave'+str(i)+'.csv'
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter =",")
        for row in csv_reader:
            arrayx.append(float(row[0]))
            arrayy.append(float(row[1]))
    grandx.append(arrayx)
    grandy.append(arrayy)
    len1 = len(arrayx)
    lengths.append(len1)
    
mlen = max(lengths)

cdatax = []
cdatay = []

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
        


class AnimatedScatter(object):
    
    def __init__(self, numpoints=9):
        self.numpoints = numpoints
        self.time_elapsed= 0
        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        #self.stream = self.data_stream()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1000, 
                                           init_func=self.setup_plot, blit=True)
    
    def setup_plot(self):
        self.time_elapsed = int(self.time_elapsed+1)
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
        self.ax.axis([-50, 50, -50, 50])
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
        coorddata3 = np.array([1,2,3,4,5,6,7,8,9])
        coorddata4 = np.array([5,5,5,5,5,5,5,5,5])
        coorddata1 = cdatax
        coorddata2 = cdatay
        #coorddata1 = np.array([[1,2],[2,1],[3,1],[4,1],[5,1],[6,2],[7,2],[8,3],[9,1],[10,1],[11,1],[12,1],[13,2],[14,1],[15,1]])
        #coorddata2 = np.array([[1,1],[2,1],[3,2],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,2],[11,3],[12,1],[13,1],[14,1],[15,2]])
        
        self.scat = self.ax.scatter(coorddata1[self.time_elapsed], coorddata2[self.time_elapsed], c = coorddata3, s=coorddata4, animated=True)

        return self.scat,
    
    def show(self):
        plt.show()
        
if __name__ == '__main__':
    a= AnimatedScatter()
    a.show()
