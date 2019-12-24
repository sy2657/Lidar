# combine the measurements and the kalman filter
# average the previous cluster for single pt 
# measure the min dist from cluster

# PART B STEP 3

# KF setup 

dt = 1
# p_x, p_y, v_x, v_y
x1 = array(([[px0], [py0], [avx1], [avy1]])) 

# extra change p_x, extra change p_y, change v_x, change v_y 
u = array(([[4.0], [12.0], [0], [0]]))

P = array([[10, 0, 0 , 0], [0, 10, 0, 0], [0, 0, 100, 0], [0, 0, 0, 100]])

F = array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])

#H = array([[1,0,0,0], [0,1,0,0], [0,0,0,0], [0,0,0,0]])
H = array([[1,0,0,0], [0,1,0,0]])
           
# meas noise
R = array([[0.1,0], [0,0.1]])

# extract measurements from the closest dist clusters frame by frame

# compare the prediction with

# 1. use prediction to choose the next cluster depending on closest distance
# 2. update measurements with this cluster data

# average over the distances 

path = "april2019/2019-02-27-12-19-36_Velodyne-HDL-32-Data-BF1-CL1-Cluster_csv"

from collections import defaultdict

import matplotlib.pyplot as plt
import csv


# array to be plotted
arrayx = []

arrayy = []
# set tarray values as the frame number to track the evolution
tarray = []


# parameters of step 5

firstrow=0

firstrowfirstfile= 0

obnum =0

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

# initial cluster to track 
initialcluster = 3


# must intialize matchfreq
mf = defaultdict(list)

mx = 11

for j in range(0, mx):
    mf[j]=0 

matchfreq= mf

initialframe = 100
n = 175 # ending frame 

# initialize distances map 
mapdistances = defaultdict(list)

totxvalues = defaultdict(list)
totyvalues = defaultdict(list)

f = 1000 # default value

for j in range(0, mx):
    mapdistances[j]=[]
    totxvalues[j] = []
    totyvalues[j] = []

currentdistances = []


# do not need to process initial frame     
for i in range(initialframe+1, n):
    #print("i is ",i)
    name = "Cluster_Frame"
    name = name+str(i)
    name = name+".csv"
    #print(name)
    pathname = path+"/"+name
    
    firstrow=0
    
    row1 = 0
    
    # clear map
    for j in range(0, mx):
        mapdistances[j] =[]
        totxvalues[j] =[]
        totyvalues[j]=[]

    # PREDICT STEP 
    x1, P = predict1(x1, P)
    
    with open(pathname) as csv_file:
        
            
        m = f
        
        currentmap= {}
            
        
        
        csv_reader = csv.reader(csv_file, delimiter=",")
        
                    
            
        for row in csv_reader:
            
            row1 = row1+ 1
            
            # must skip first row again
            if firstrow==0:
                firstrow=1
                continue
            
            vehped = float(row[1])
            
            if vehped == 2: 
                continue # only track vehicles
            
            clusterid = float(row[0]) # current cluster id 
            
            if clusterid != obnum:
                   
                
                numo1 = float(obnum)
                
                
                # append to dictionary of maps
                #totalmap[numo1] = currentmap
                
                mapdistances[numo1] = currentdistances
                totxvalues[numo1] = xvalues
                totyvalues[numo1] = yvalues
                
                
                if obnum==11:
                    print("11 row", row1)
                    print("11 row vehped",vehped)
                
                # instead of checking matchfreq[numo1]>f , calculate min dist.s at end of file
                #if matchfreq[numo1] > f:
                    #f = matchfreq[numo1]
                    #print("f is", f)
                    #ky = numo1
                    #print("ky is",ky)
                    #hxvalues = xvalues
                    #hyvalues = yvalues 
                    
                
                # new comparisons 
                obnum = clusterid
                
                currentdistances=[]
                #currentmap= {}
                
                xvalues =[]
                yvalues =[]
                
                continue
            #clustertype = row[1]
            xpoint = float(row[2])
            ypoint = float(row[3])
            xvalues.append(xpoint) # save to array 
            yvalues.append(ypoint)
            # calc distance
            
            # INSTEAD, CALCULATE DIST FROM PREDICTED PT x1 
            dx1 = x1[0] - xpoint #avx - xpoint
            dy1 = x1[1] - ypoint #avy - ypoint
            d1 = pow(dx1, 2) + pow(dy1, 2)
            dist = math.sqrt(d1)
            # save to indices
            
            
            currentdistances.append(dist) 
        
        # find min 
        for j in range(0, mx):
            meandistances = np.mean(mapdistances[j])
            if meandistances < m:
                m = meandistances
                ky = j 
                
        #print("min meandist", m)
        finalarray.append(ky)
        hxvalues = totxvalues[ky]
        hyvalues = totyvalues[ky]
        
        avx = np.mean(hxvalues)
        avy = np.mean(hyvalues)
        
        # this is the measurement to be input into update step
        
        # CHANGE: add this to measurements
        #measurements.append([avx, avy])
        
        z1 = [avx, avy]
        # UPDATE STEP
        x1, P = update2(x1, P, z1)
        
        plt.scatter(hxvalues, hyvalues)
        #plt.scatter(x1[0], x1[1])
        
        #plt.scatter(np.asscalar(x1[0]), np.asscalar(x1[1]))
        
        # print mean
        #print("mean x,",np.mean(hxvalues))
        #print("mean y,",np.mean(hyvalues))
        
        # reset hxvalues and hyvalues (don't need )
        hxvalues =[]
        hyvalues =[]
        
        # set prevmap to the one 
        #prevmap = totalmap[ky]
        
#plt.legend(['file1', 'file2', 'file3', 'file4', 'file5', 'file6', 'file7', 'file8'], loc='upper left')

plt.show()


# which method?
# precomputing the coord with traj file
# or
# this method: updating after each frame's measurement

