import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


# december highest 
# step 4 b 


class frequency_grid(object):
    
    def __init__(self, numpoints=3):
        self.numpoints = numpoints
        self.time_elapsed= 0 # 0
        self.numcells = 160000
        
        self.xmin =-200
        self.xmax = 200
        self.ymin =-200
        self.ymax =200
        
        self.forwardmap = {}  # dcmap1
        self.backmap = {}
        self.countmap = {}
        
        self.current_position = []
        self.prevmap = {} # set to current map at end of frame 
        self.currentmap = {}
        
        self.tracking_list = {} # list of objects that are tracked 
        
        # step 1
        ind_temp = 0
        for ix in range(int(self.xmin), int(self.xmax)):
            for iy in range(int(self.ymin), int(self.ymax)):
                myvec = []
                myvec.append(ix)
                myvec.append(iy)
                self.forwardmap[ind_temp] = myvec
                self.backmap[(ix, iy)]= ind_temp
                ind_temp=ind_temp+1
        
        self.range = 10
        # initialize grid count map
        for i in range(self.numcells):
            p = self.forwardmap[i]
            px = p[0]
            py = p[1]
            for j in range(-self.range, self.range+1):
                jx = px+j
                if jx > self.xmax-1 or jx < self.xmin:
                    continue
                for k in range(-self.range, self.range+1):
                    jy = py +k
                    if jy > self.ymax-1 or jy<self.ymin:
                        continue
                    p2 = self.backmap[(jx, jy)]
                    self.countmap[(i, p2)] = 0 # dtrajcount
    
        
    # set up based on trajectories file : training method 
    def setup_grid(): 
        
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
                    mcount = self.countmap[(fromi, toi)]
                    self.countmap[(fromi, toi)] = mcount+1
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
                t = self.countmap[(fromi, toi)]
                #if t>0:
                    #print(t)
                if t > highest:
                    highest=t
                    indexhighest=toi
        return highest, indexhighest
                    
    def predict(self, next_frame): # predict next
        
        mf = defaultdict(list)
        
        mx = 20
        for j in range(0, mx):
            mf[j] = 0
            
        matchfreq = mf
        
        f= 0
        
        currentmap = {} # temporary currentmap
        currentmap_freq = {} # holds freq scores
        
        for j,next_key in enumerate(next_frame.keys()):
            pos_next = next_frame[next_key].position
            x_next = pos_next[0]
            y_next = pos_next[1]
            xr = round(xpoint)
            yr = round(ypoint)
            fromi = self.backmap[(xr, yr)]
            h1, i1 = self.highestfreq(fromi)
            
            # save to map
            currentmap[i1] = 1
            currentmap_freq[i1] = h1 
            val = self.prevmap.get(fromi)
            if val ==None:
                pass
            else:
                matchfreq[next_key] = matchfreq[next_key] +1
            
            
        # version with multiple points in pos_next
        for j,next_key in enumerate(next_frame.keys()):
            pos_next = next_frame[next_key].position
            
            for pos in pos_next:
                x_next = pos[0]
                y_next = pos[1]
                xr = round(xpoint)
                yr = round(ypoint)
                fromi = self.backmap[(xr, yr)]
                h1, i1 = self.highestfreq(fromi)
                currentmap[i1] = 1
                currentmap_freq[i1] = h1
                val = self.prevmap.get(fromi)
                if val ==None:
                    pass
                else:
                    matchfreq[pos] = matchfreq[pos]+1
                
        '''
        next_x = next_detection_position[0]
        next_y = next_detection_position[1]
        array_points= next_detection_position
        
        xvalues= []
        yvalues =[]
        prevmap={}
        hxvalues =[]
        hyvalues=[]
        '''
        
        
        # cycle through the different points
        for point in array_points:
            xpoint = float(point[0])
            ypoint = float(point[1])
            xr = round(xpoint)
            yr = round(ypoint)
            fromi = self.backmap[(xr, yr)]
            h1, i1 = self.highestfreq(fromi)
            # save to map
            self.currentmap[i1] = 1
            val = self.prevmap.get(fromi) # from i from previous point
            if val == None:
                pass
            else:
                matchfreq[point] = matchfreq[point]+1
                
