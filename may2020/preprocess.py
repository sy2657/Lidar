# load data 

# determine the extreme values of points 
import csv

trajfile = "2019-9-10-12-0-0-BF1-CL1-Traj(0-18000frames).csv"

with open(trajfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count ==0:
            line_count = line_count+1
            continue
        # init 
        if line_count==1:
            xmax = float(row[6])
            xmin = float(row[6])
            ymax = float(row[7])
            ymin = float(row[7])
        # x, y vals 
        xval = float(row[6])
        yval = float(row[7])
        if xval > xmax:
            xmax = xval
        if xval < xmin:
            xmin = xval
        if yval > ymax:
            ymax = yval
        if yval < ymin:
            ymin = yval
            
        line_count = line_count+1
import numpy as np
xmax = np.ceil(float(xmax))
ymax = np.ceil(float(ymax))

xmin = np.floor(float(xmin))
ymin = np.floor(float(ymin))

ymax = ymax+1
xmax = xmax+1

# december step 1

dcmap1 = {}
ind= 0

for ix in range(int(xmin), int(xmax)):
    for iy in range(int(ymin), int(ymax)):
        myvec=[]
        myvec.append(ix)
        myvec.append(iy)
        dcmap1[ind]=myvec
        ind=ind+1
# initialize 

# combine steps 

# december step 2 
dlookupdict={}
dinvlookupdict={}

for i in range(36712):
    dlookupdict[i] = dcmap1[i]
    p1 = dcmap1[i][0]
    p2 = dcmap1[i][1]
    dinvlookupdict[(p1,p2)]=i

# december step 3

dtrajcount={}
# xmin, xmax, ymin, ymax

# change range to -10, 10
range1 = 10 

for i in range(36712):
    p = dlookupdict[i]
    px = p[0]
    py = p[1]
    if i==24000:
        print(24000)
    # calculate x between i.x - 5, i.x+5
    for j in range(-range1, range1+ 1):
        jx = px+j
        if jx>xmax-1 or jx<xmin: # check if pts in range
            continue
        # calculate y between i.y-5, i.y+5 
        for k in range(-range1, range1+1):
            jy = py+k
            # check if pts are in range
            if jy>ymax-1 or jy<ymin:
                continue
            # inv dict lookup
            p2 = dinvlookupdict[(jx, jy)]
            # save trajcount1[(i, p2)]
            dtrajcount[(i, p2)]=0

# train with trajectory

# dec step 3.b
listoutliers = []
rangeoutliers = {}
doutlier = {}
listoutliers2 = {}

# step 4 

#tfile = "dec2019/Ramp/2019-9-9-15-0-0-BF1-CL1-Traj(0-18000frames)Ramp.csv"
tfile =  "2019-9-10-12-0-0-BF1-CL1-Traj(0-18000frames).csv"

import math
import csv

trajnum = 0 
obnum = 1

irow =0

outlier =0


with open(tfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        irow=irow+1
        trajnum = row[0]
        frameindex = row[17]
        #print("frame:",frameindex)
        if line_count==0:
            line_count=line_count+1
            continue
        if line_count==1:
            line_count=line_count+1
            prevrow = row
            prevx = float(prevrow[6])
            prevy = float(prevrow[7])
            # use round instead of floor
            pfx = round(prevx)
            pfy = round(prevy)
            continue
        # skip if timestamp is 0
        #timest = float(row[2])
        #if timest==0:
        #    continue
        currx =float(row[6])
        curry =float(row[7])
        # instead of floor, use round
        fx = round(currx)
        fy = round(curry)
        if pfx==fx and pfy==fy:
            prevframe=frameindex
            line_count = line_count + 1
            continue
        if obnum != trajnum:
            pfx = fx
            pfy= fy
            obnum = trajnum
            prevtrajnum = trajnum
            prevframe=frameindex
            line_count = line_count+1
            continue
        # now save to the map(i,j)
        # debug
        
        fromi = dinvlookupdict[(pfx,pfy)]
        #topt = []
        toi = dinvlookupdict[(fx,fy)]
        #check if in range 
        if abs(pfx - fx) >10 or abs(pfy - fy) > 10:
            xr1 = fx - pfx
            yr1 = fy - pfy
            if [pfx, pfy] in listoutliers:
                # get the list of points + their counts
                #listptcount = doutlier[fromi]
                arrayptcount = listoutliers2[fromi]
                if [fx, fy] in arrayptcount:
                    doutlier[fromi, toi] = doutlier[fromi, toi]+1
                else:
                    arrayptcount.append([fx,fy])
                    listoutliers2[fromi] = arrayptcount 
                    doutlier[fromi, toi] = 1 
            #add to outliers 
            else:
                if len(listoutliers) ==0 :
                    #print("hi 0")
                    listoutliers = [[pfx, pfy]]
                    listoutliers2[fromi] = [[fx, fy]]
                    doutlier[fromi, toi] = 1
                    continue
                print("hi 1")
                listoutliers.append([pfx, pfy])
                listoutliers2[fromi] = [[fx, fy]]
                doutlier[fromi, toi] = 1 
            # print to keep track 
            #print("pfx, pfy", pfx, pfy)
            #print("fx, fy", fx, fy)
            line_count = line_count + 1
            # skip normal step
            continue

        mcount = dtrajcount[(fromi,toi)]
        if mcount >20:
            print("mcount", mcount)
        dtrajcount[(fromi, toi)] = mcount+1
        # set previous
        pfx = fx
        pfy = fy
        prevframe = frameindex
        prevtrajnum= trajnum
        line_count=line_count+1
