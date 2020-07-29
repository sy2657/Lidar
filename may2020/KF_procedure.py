# PART B STEP 2 
# determine initial pos and velocity

#  (1) determine average speed
# determine based on traj file

# (2) determine average x velocity and y velocity (break into sep components)
#tfile ="april2019/2019-02-27-12-19-36_Velodyne-HDL-32-Data-BF1-CL1-Traj.csv"

trajfile = "2019-9-10-12-0-0-BF1-CL1-Traj(0-18000frames).csv"

#tfile =  "2019-9-10-12-0-0-BF1-CL1-Traj(0-18000frames).csv"


import math
import csv

trajnum = 0
obnum=1
irow=0
settimestamp=[]
setx = []
sety = []
every5 = 0

arrayvel=[]
arrayvelx =[]
arrayvely=[]

with open(trajfile) as csv_file:
    csv_reader= csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count ==0:
            line_count=1
            continue
        if line_count==1:
            line_count=2
            prevrow = row
            prevx = float(row[6])
            prevy = float(row[7])
            pts = float(row[2])*0.000001
        xval = float(row[6])
        yval = float(row[7])
        trajnum = float(row[0])
        timestamp = float(row[2])
        ts = timestamp*0.000001
        # test for 0 timestamp
        if timestamp==0:
            prevx = xval
            prevy = yval
            pts = 0
            continue
        if pts ==0:
            pts = ts
            prevx = xval
            prevy = yval
            continue
        every5 = every5+1
        if every5 == 1:
            pts = ts
            prevx = xval
            prevy = yval 
            
        if every5 == 5:
            diff = ts - pts
            if diff==0:
                continue
            xdist = xval - prevx
            ydist = yval - prevy
            xdist2 = pow(xdist, 2)
            ydist2 = pow(ydist, 2)
            dist = pow(xdist2+ydist2, 0.5)
            v = dist/float(diff)
            vx = xdist/float(diff)
            vy = ydist/float(diff)
            if dist!=0:
                arrayvel.append(v)
                arrayvelx.append(vx)
                arrayvely.append(vy)
            every5= 0
        else:
            continue
        if trajnum != obnum:
            prevx = xval
            prevy = yval
            pts =ts
            obnum = trajnum
            
import numpy as np
avx= np.mean(arrayvelx)
avy= np.mean(arrayvely)

# determine initial position based on init. cluster and frame

initialcluster = 1
initialframe= 1

firstrow = 0
pathname = "file_out"+str(initialframe)+".csv"

arrayx = []
arrayy = []

with open(pathname) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        if firstrow==0:
            firstrow=1
            continue
        clusterid = float(row[0])
        if clusterid == initialcluster:
            xpoint = float(row[1])
            ypoint = float(row[2])
            arrayx.append(xpoint)
            arrayy.append(ypoint)
            
# initial position
px0 = np.mean(arrayx)
py0 = np.mean(arrayy)

# combine the measurements and the kalman filter
# average the previous cluster for single pt 
# measure the min dist from cluster
from numpy import array

dt = 1
# p_x, p_y, v_x, v_y
x1 = array(([[px0], [py0], [avx], [avy]])) 

# extra change p_x, extra change p_y, change v_x, change v_y 
u = array(([[4.0], [12.0], [0], [0]]))

P = array([[10, 0, 0 , 0], [0, 10, 0, 0], [0, 0, 100, 0], [0, 0, 0, 100]])

F = array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])

#H = array([[1,0,0,0], [0,1,0,0], [0,0,0,0], [0,0,0,0]])
H = array([[1,0,0,0], [0,1,0,0]])
           
# meas noise
R = array([[0.1,0], [0,0.1]])

B = np.eye(4)

Q = np.eye(4)
            
    
from numpy.linalg import inv
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
 
from numpy import *

# main procedure

# KF step 7  (one cluster)

### input parameters
initialframe = 1
n = 10 # ending frame 
 
initialcluster = 2

###
from collections import defaultdict

import matplotlib.pyplot as plt
import csv

velx= avx/10
vely=avy/10


# array to be plotted
arrayx = []

arrayy = []
# set tarray values as the frame number to track the evolution
tarray = []


# parameters of step 5

firstrow=0

firstrowfirstfile= 0

obnum =2 

previndices=[]

currentindices=[]

totalmap = {}

arrayofarrays = []

# rename current dict to totaldict?
currentdict = {}

arrayofdicts=[]

finalarray=[]

xvalues = []
yvalues = []

hxvalues =[]
hyvalues= []

prevmap={}



# must intialize matchfreq
mf = defaultdict(list)

mx = 11

for j in range(0, mx):
    mf[j]=0 

matchfreq= mf



# initialize distances map 
mapdistances = defaultdict(list)

totxvalues = defaultdict(list)
totyvalues = defaultdict(list)


currentcluster = 0
clusters = defaultdict(list)

f = 1000 # default value

for j in range(0, mx):
    mapdistances[j]=[]
    totxvalues[j] = []
    totyvalues[j] = []
    clusters[j] = []

currentdistances = []


outputclusters = []
outputclusters.append(initialcluster)

    
pathname = "file_out"+str(initialframe)+".csv"
firstrow=0
    
xvalues1= []
yvalues1 = []

with open(pathname) as csv_file:
    m = f
    currentmap={}
    csv_reader = csv.reader(csv_file, delimiter=",")

    for row in csv_reader:
        # don't skip first row
        clusterid = float(row[0])
        xpoint = float(row[1])
        ypoint = float(row[2])
        if clusterid == initialcluster:
            xvalues1.append(xpoint)
            yvalues1.append(ypoint)
# find x1 based on icluster 
avx1 = np.mean(xvalues1)
avy1 = np.mean(yvalues1)

print("start point x", avx1)
print("start point y", avy1)

x1 = array(([[avx1], [avy1], [velx], [vely]])) 


for i in range(initialframe+1, n): # not need to process initial frame
    pathname = "file_out"+str(i)+".csv"
    firstrow=0
    for j in range(0, mx):
        mapdistances[j]= []
        totxvalues[j]= []
        totyvalues[j]= []
        clusters[j] = []
    # predict
    x1, P = predict1(x1, P)
    
    with open(pathname) as csv_file:
        m = f
        currentmap={}
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        for row in csv_reader:
            # don't skip first row
            clusterid = float(row[0])
            
            if clusterid != obnum:
                numo1 = float(obnum)
                mapdistances[numo1] = currentdistances
                totxvalues[numo1] = xvalues
                totyvalues[numo1] = yvalues
                clusters[numo1] = currentcluster
                obnum = clusterid
                currentdistances=[]
                xvalues=[]
                yvalues=[]
                continue
            
            xpoint = float(row[1])
            ypoint = float(row[2])
            xvalues.append(xpoint)
            yvalues.append(ypoint)
            currentcluster = clusterid
            
            print("x1", x1)
            print("x1[0]", x1[0])
            
            # distance from predicted point x1
            dx1 = x1[0] - xpoint
            dy1 = x1[1] - ypoint
            d1 = pow(dx1,2)+pow(dy1,2)
            dist = math.sqrt(d1)
            # save
            currentdistances.append(dist)
        # find min
        for j in range(0, mx):
            meandistances = np.mean(mapdistances[j])
            if meandistances <m:
                m = meandistances
                ky =j
                print("cluster", clusters[ky])
                
        outputclusters.append(clusters[ky])
        hxvalues = totxvalues[ky]
        hyvalues = totyvalues[ky]
        
        avx = np.mean(hxvalues)
        avy = np.mean(hyvalues)
        
        #print("avx is", avx)
        #print("avy is", avy)
        
        # measurement, update
        z1 = [avx, avy]
        
        x1, P = update2(x1, P, z1)
        
        #plt.scatter(hxvalues, hyvalues)
        plt.scatter(avx, avy)
        hxvalues=[]
        hyvalues=[]
plt.show()
            
            
        

            
            
        


 
