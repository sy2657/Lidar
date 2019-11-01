# STEP 5 G 
# track multiple vehicles, ea is separate color
# similar to 5 C 2 but each trajectory is diff color 

# inputs 
initialframe =30
endframe = 130


# initialization of data arrays
firstrow= 0
firstrowfirstfile =0
obnum =0

arrayx = []
arrayy = []
tarray = []
totalmap = {}
currentdict = {}
xvalues = []
yvalues = []

hxvalues =[]
hyvalues= []

prevmap={}
# must intialize matchfreq
mf = defaultdict(list)
mx =20 
for j in range(0, mx):
    mf[j]=0 
matchfreq = mf

# first determine how many diff cars there are 
name1 = "Cluster_Frame"
name1 = name1+str(initialframe)
name1 = name1+".csv"
pathname1 = path+"/"+name1

maxinitclusterid= 0 # number of vehicles to track

firstrowfirstfile1=0

with open(pathname1) as csv_file1:
    csv_reader1 = csv.reader(csv_file1, delimiter=",")
    for row1 in csv_reader1:
        if firstrowfirstfile1==0:
            firstrowfirstfile1=1
            continue
        vehped1 = float(row1[1])
        clusterid1 = float(row1[0])
        if vehped1 ==2:
            continue
        if clusterid1 > maxinitclusterid:
            maxinitclusterid = clusterid1

# loop over the clusters 
maxinitclusterid = int(maxinitclusterid)
for j in range(0, maxinitclusterid):
    initialcluster = j 
    firstrowfirstfile = 0 
    for i in range(initialframe, endframe):
        name = "Cluster_Frame"
        name = name+str(i)
        name = name+".csv"
        pathname = path+"/"+name
        firstrow=0
        # clear matchfreq
        for k in range(0, mx):
            matchfreq[k] = 0
        with open(pathname) as csv_file:
            f=0 # max match freq compare
            #reset 
            hxvalues= []
            hyvalues = []
            currentmap = {}
            csv_reader = csv.reader(csv_file, delimiter =",")
            if i == initialframe:
                for row in csv_reader:
                    if firstrowfirstfile==0:
                        firstrowfirstfile=1
                        continue
                    clusterid =float(row[0])
                    vehped = float(row[1])
                    if clusterid == initialcluster and vehped ==1: 
                        xpoint = float(row[2])
                        ypoint = float(row[3])
                        arrayx.append(xpoint)
                        arrayy.append(ypoint)
                        xfloor = round(xpoint)
                        yfloor = round(ypoint)
                        fromi = invlookupdict[(xfloor, yfloor)]
                        h1, i1 = highestfreq(fromi)
                        prevmap[i1] = 1
                # plt.scatter(arrayx, arrayy)
                ky = initialcluster
                continue
            for row in csv_reader:
                if firstrow==0:
                    firstrow=1
                    continue
                vehped = float(row[1])
                if vehped == 2:
                    continue # only track vehicles
                clusterid = float(row[0])
                if clusterid != obnum:
                    numo1 = float(obnum)
                    totalmap[numo1] = currentmap
                    if matchfreq[numo1] > f:
                        f= matchfreq[numo1]
                        ky = numo1
                        hxvalues = xvalues
                        hyvalues = yvalues
                    obnum = clusterid
                    currentmap = {}
                    
                    xvalues = []
                    yvalues = []
                    # append first vals
                    xvalues.append(float(row[2]))
                    yvalues.append(float(row[3]))
                    continue
                xpoint = float(row[2])
                ypoint = float(row[3])
                xr = round(xpoint)
                yr = round(ypoint)
                xvalues.append(xpoint)
                yvalues.append(ypoint)
                fromi = invlookupdict[(xr,yr)]
                h1, i1 = highestfreq(fromi)
                currentmap[i1] = 1
                val = prevmap.get(fromi)
                if val != None:
                    numo = float(obnum)
                    matchfreq[numo] = matchfreq[numo]+1 
            # check f vals at end of file
            numo2 = float(obnum)
            if matchfreq[numo2] > f:
                ky = numo2
                hxvalues = xvalues
                hyvalues = yvalues
                totalmap[ky] = currentmap
            # finalarray.append(ky)
            arrhxvalues.extend(hxvalues)
            arrhyvalues.extend(hyvalues)
            
            # set prevmap
            if len(hxvalues) != 0:
                prevmap = totalmap[ky]
    # at end of this j 
    plt.scatter(arrhxvalues, arrhyvalues)
    arrhxvalues = []
    arrhyvalues= []
    

plt.show()
                
