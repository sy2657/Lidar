# run algorithm 
# do not initialize countmap, but check if val = countmap.get() is none

# run algorithm on input

# test initializing

import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


# december highest 
# step 4 b 


class frequency_grid(object):
    
    def __init__(self): # initialize forward and back map outside of init
        #self.numpoints = numpoints
        self.time_elapsed= 0 # 0
        self.numcells = 160000
        
        self.xmin =-200
        self.xmax = 200
        self.ymin =-200
        self.ymax =200
        
        self.forwardmap = {}  # dcmap1
        self.backmap = {}
        
        ind_temp = 0
        for ix in range(int(xmin), int(xmax)):
            for iy in range(int(ymin), int(ymax)):
                myvec = []
                myvec.append(ix)
                myvec.append(iy)
                self.forwardmap[ind_temp] = myvec
                self.backmap[(ix, iy)]= ind_temp
                ind_temp=ind_temp+1
                
        self.countmap = {}
        
        self.current_position = []
        self.prevmap = {} # set to current map at end of frame 
        self.currentmap = {}
        
        self.tracking_list = {} # list of objects that are tracked 
        
        self.range = 10
        
        # initialize grid count map
        self.countmap = {}
    
        
    # set up based on trajectories file : training method 
    def setup_grid(self): 
        
        fileind = 1
        for filename in os.listdir('24hrdata'):
            fname = '24hrdata/'+filename
            fileind =fileind+1
            #irow=0
            obnum=1
            with open(fname) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    trajectory_num = row[0]
                    if line_count==0:
                        line_count = line_count+1 # skip header
                        continue
                    if line_count==1:
                        prevrow = row
                        prevx = float(prevrow[6])
                        prevy = float(prevrow[7])
                        pfx = round(prevx)
                        pfy = round(prevy)
                        continue
                    currentx = float(row[6])
                    currenty = float(row[7])
                    fx = round(currentx)
                    fy = round(currenty)
                    if pfx == fx and pfy ==fy:
                        #prevframe = frameindex
                        continue
                    if obnum != trajectory_num:
                        pfx = fx
                        pfy = fy
                        obnum = trajectory_num
                        continue
                    #save
                    fromi = self.backmap[(pfx, pfy)]
                    toi = self.backmap[(fx, fy)]
                    if abs(pfx - fx)>10 or abs(pfy - fy)>10:
                        continue
                    # check if it is none 
                    val = self.countmap.get((fromi, toi))
                    if val == None:
                        self.countmap[(fromi, toi)] = 1
                    else:
                        mcount = self.countmap[(fromi, toi)]
                        self.countmap[(fromi, toi)] = mcount+1
                        # check by printing
                        if mcount > 500:
                            print("over 500 from i: ", fromi, " toi:", toi)
                    pfx=fx
                    pfy=fy
    
    def highestfreq(fromi):
        highest = 0
        indexhighest = fromi
        (px, py) = self.forwardmap[fromi]
        for j in range(-10, 11):
            jx = px+j
            if jx>xmax-1 or jx<xmin: # check if pts in range
                continue
            for k in range(-10, 11):
                jy = py+k
                # check if pts are in range
                if jy>ymax-1 or jy<ymin:
                    continue
                toi = self.backmap[(jx, jy)]
                # check if value is none 
                val = self.countmap.get((fromi, toi))
                if val == None:
                    t = 0
                else:
                    t = self.countmap[(fromi, toi)]
                #if t>0:
                    #print(t)
                if t > highest:
                    highest=t
                    indexhighest=toi
        return highest, indexhighest
