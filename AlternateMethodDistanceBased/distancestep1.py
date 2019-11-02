# Euclidean distance

# PART B STEP 1 
# average the previous cluster for single pt 
# measure the min dist from cluster 

# average over the distances 

path = "april2019/2019-02-27-12-19-36_Velodyne-HDL-32-Data-BF1-CL1-Cluster_csv"

from collections import defaultdict

import matplotlib.pyplot as plt


# array to be plotted
arrayx = []

arrayy = []
# set tarray values as the frame number to track the evolution
tarray = []


# parameters of step 5
n = 67

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
initialcluster = 1


# must intialize matchfreq
mf = defaultdict(list)

mx = 11

for j in range(0, mx):
    mf[j]=0 

matchfreq= mf

initialframe = 5

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


    
for i in range(initialframe, n):
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

    
    with open(pathname) as csv_file:
        
            
        m = f
        
        currentmap= {}
            
        
        
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        if i==initialframe:
            #print("i",i)
            for row in csv_reader:
                # skip label or first row
                if firstrowfirstfile==0:
                    firstrowfirstfile=1
                    continue
                clusterid = float(row[0])
                vehped = float(row[1])
                #print("clusterid", clusterid)
                if clusterid==initialcluster and vehped==1:
                    xpoint = float(row[2])
                    ypoint = float(row[3])
                    arrayx.append(xpoint)
                    arrayy.append(ypoint)
                    
            # find average 
            avx = np.mean(arrayx)
            avy = np.mean(arrayy)
            avprev = [avx, avy ]
            #plt.plot(arrayx, arrayy)
            plt.scatter(arrayx, arrayy)
        
            continue # don't need this continue statement?
            #break
                    
            
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
            dx1 = avx - xpoint
            dy1 = avy - ypoint
            d1 = pow(dx1, 2) + pow(dy1, 2)
            dist = pow(d1, 0.5)
            # save to indices
            currentdistances.append(dist) 
        
        # find min 
        for j in range(0, mx):
            meandistances = np.mean(mapdistances[j])
            if meandistances < m:
                m = meandistances
                ky = j 
                
        print("min meandist", m)
        finalarray.append(ky)
        hxvalues = totxvalues[ky]
        hyvalues = totyvalues[ky]
        
        #plt.plot(hxvalues, hyvalues)
        plt.scatter(hxvalues, hyvalues)
        # reset hxvalues and hyvalues (don't need )
        hxvalues =[]
        hyvalues =[]
        
        # set prevmap to the one 
        #prevmap = totalmap[ky]
        
#plt.legend(['file1', 'file2', 'file3', 'file4', 'file5', 'file6', 'file7', 'file8'], loc='upper left')

plt.show()



