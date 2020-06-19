
import matplotlib.pyplot as plt


# array to be plotted
arrayx = []

arrayy = []

xvalues = []
yvalues = []

finalarray=[]

totxvalues = defaultdict(list)
totyvalues = defaultdict(list)
# initialize distances map 
mapdistances = defaultdict(list)

obnum =0

currentdistances = []

for j in range(0, mx):
    mapdistances[j]=[]
    totxvalues[j] = []
    totyvalues[j] = []
    

for i in range(initialframe, endframe):
    name = "file_out"
    name = name+str(i)
    name = name+".csv"
    firstrow=0
    # clear map
    for j in range(0, mx):
        mapdistances[j] =[]
        totxvalues[j] =[]
        totyvalues[j]=[]
        
    with open(name) as csv_file:
        m = 1000
        
        f =0 
        # reset hxvalues , hyvalues
        hxvalues = []
        hyvalues=[]

        currentmap= {}

        csv_reader = csv.reader(csv_file, delimiter=",")
        
        if i==initialframe:
            #print("i",i)
            for row in csv_reader:
                
                clusterid = float(row[0])
                
                #print("clusterid", clusterid)
                if clusterid==initialcluster:
                    xpoint = float(row[1])
                    ypoint = float(row[2])
                    arrayx.append(xpoint)
                    arrayy.append(ypoint)
                    
            # find average 
            avx = np.mean(arrayx)
            avy = np.mean(arrayy)
            avprev = [avx, avy ]
            #plt.plot(arrayx, arrayy)
            plt.scatter(arrayx, arrayy)
        
            continue
            
        for row in csv_reader:
            clusterid = float(row[0]) # current cluster id 
            
            if clusterid != obnum:
                numo1 = float(obnum)
                mapdistances[numo1] = currentdistances
                totxvalues[numo1] = xvalues
                totyvalues[numo1] = yvalues
                # new comparisons 
                obnum = clusterid
                
                currentdistances=[]
                #currentmap= {}
                
                xvalues =[]
                yvalues =[]
                
                continue
            xpoint = float(row[1])
            ypoint = float(row[2])
            xvalues.append(xpoint) # save to array 
            yvalues.append(ypoint)
            # calc distance
            dx1 = avx - xpoint
            dy1 = avy - ypoint
            d1 = pow(dx1, 2) + pow(dy1, 2)
            dist = pow(d1, 0.5)
            currentdistances.append(dist) 
            
        for j in range(0, mx):
            meandistances = np.mean(mapdistances[j])
            if meandistances < m:
                m = meandistances
                ky = j 
        finalarray.append(ky)
        hxvalues = totxvalues[ky]
        hyvalues = totyvalues[ky]
        
        avx = np.mean(hxvalues)
        avy = np.mean(hyvalues)
        
        #plt.plot(hxvalues, hyvalues)
        plt.scatter(hxvalues, hyvalues)
        
        # print mean
        #print("mean x,",np.mean(hxvalues))
        #print("mean y,",np.mean(hyvalues))
        
        # reset hxvalues and hyvalues (don't need )
        hxvalues =[]
        hyvalues =[]
        
plt.show()
