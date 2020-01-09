def predict1(x, P):
    x = np.dot(F, x) + np.dot(B, u)
    P = np.dot(F, np.dot(P, F.transpose())) + Q
    return x, P

def update1(x, P, z):
    y = z - np.dot(H,x)
    S = np.dot(H, np.dot(P, H.transpose()))
    K = np.dot(P, np.dot(H.transpose(), inv(S)))
    #print("k",K)
    #print("y", y)
    x = x+ np.dot(K,y)
    P = P - np.dot(K, np.dot(H, P))
    xs.append(x)
    cov.append(P)
    return x, P

def update2(x, P,z):
    S = np.dot(np.dot(H, P), H.transpose()) + R
    K = np.dot(np.dot(P, H.transpose()), inv(S))
    z = matrix([z])
    y = z.transpose() - np.dot(H, x)
    x = x + np.dot(K, y)
    P = P - np.dot(np.dot(K,H), P)
    return x, P
 
 # PART B STEP 2 
# determine initial pos and velocity

#  (1) determine average speed
# determine based on traj file

# (2) determine average x velocity and y velocity (break into sep components)
tfile ="april2019/2019-02-27-12-19-36_Velodyne-HDL-32-Data-BF1-CL1-Traj.csv"

import math
import csv

trajnum = 0 
obnum = 1

irow =0

settimestamp= []
setx =[]
sety =[]

every5 =0

arrayvel = []

arrayvelx = []
arrayvely = []

with open(tfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        irow=irow+1
        
        frameindex = row[17]  
        # check first row
        if line_count==0:
            line_count=line_count+1
            continue
        if line_count==1:
            line_count=line_count+1
            prevrow = row
            prevx = float(prevrow[6])
            prevy = float(prevrow[7])
            # change floor to round
            #pfx = round(prevx)
            #pfy = round(prevy)
            pts = float(prevrow[2])*0.000001
            continue 
        vehped = row[1]
        if vehped ==2:
            continue
            
        trajnum= float(row[0])
        currx = float(row[6])
        curry = float(row[7])
        timestamp = float(row[2])
        # ts should be between 0.05 and 0.15 ~ 0.1 sec 
        ts = timestamp*0.000001
        
        # test for 0 timestamp
        if timestamp==0:
            pts=0
            prevx = currx
            prevy=curry
            continue
        if pts==0:
            pts = ts
            prevx =currx
            prevy= curry
            continue
        
        if irow == 875:
            print("timestamp", ts)
            print("prev timestamp", pts)
        # every 5 
        every5= every5+1
        if every5==1:
            pts =ts 
            prevx = currx
            prevy= curry 
        if every5==5:
            # calculate diff
            #print("row", irow)
            diff = ts - pts 
            # calculate distance
            xdist = currx - prevx
            ydist = curry - prevy
            xdist2 = pow(xdist,2)
            ydist2 = pow(ydist,2)
            dist = pow(xdist2+ydist2, 0.5)
            v = dist/float(diff)
            vx = xdist/float(diff)
            vy = ydist/float(diff)
            if dist!=0:
                arrayvel.append(v)
                arrayvelx.append(vx)
                arrayvely.append(vy)
            every5=0
        else:
            continue
        if trajnum!= obnum:
            # reset 
            prevx = float(row[6])
            prevy= float(row[7])
            pts = ts
            obnum=trajnum
            
 # set values of initial velocity
avx = np.mean(arrayvelx)
avy = np.mean(arrayvely)

avy1 = 0.1*avy
avx1 = 0.1*avx

# PART B STEP 2 B 
# determine average speed based on frames data
from numpy import dot, array, sqrt

import numpy as np

path = "april2019/2019-02-27-12-19-36_Velodyne-HDL-32-Data-BF1-CL1-Cluster_csv"

dpath = "dec2019/Ramp/2019-9-9-15-0-0-BF1-CL1(0-18000frames)-Cluster_csv"

import csv

# determine initial position 

# initial cluster to track 
initialcluster = 3

initialframe = 100
initialframe = 391

name = "Cluster_Frame"
name = name+str(initialframe)
name = name+".csv"
    #print(name)
 
 # dec: change to dpath
pathname = dpath+"/"+name
    
firstrow=0


arrayx = []
arrayy = []

# average over the cluster 

with open(pathname) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        if firstrow==0:
            firstrow=1
            continue
        clusterid = float(row[0])
        vehped = float(row[1])
        if clusterid==initialcluster and vehped==1:
            xpoint = float(row[2])
            ypoint = float(row[3])
            arrayx.append(xpoint)
            arrayy.append(ypoint)

# initial position

px0 = np.mean(arrayx)
py0 = np.mean(arrayy)



   
