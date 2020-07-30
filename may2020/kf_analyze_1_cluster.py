# KF step 7  (one cluster)

### input parameters
initialframe = 1
n = 10 # ending frame 
 
initialcluster = 5

###
from collections import defaultdict

import matplotlib.pyplot as plt
import csv

velx= avx/10
vely=avy/10


# parameters of step 5


obnum =1


xvalues = []
yvalues = []

hxvalues =[]
hyvalues= []


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

#print("start point x", avx1)
#print("start point y", avy1)

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
            
            #print("x1", x1)
            #print("x1[0]", x1[0])
            
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
                #print("cluster", clusters[ky])
                
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
            
            
        
