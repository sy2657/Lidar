# complete procedure distance 
c1 =1 
c2 = 11

missedmatching=0
continuedmatching=0
wrongmatching=0
clustering_error = 0
totalcomparisons = 0

initialframe =70
endframe = 80

maxnumframes = endframe+1 - initialframe

for c in range(c1, c2+1):
    print("current cluster is", c)
    initialcluster = c
    # array to be plotted
    arrayx = []

    arrayy = []

    xvalues = []
    yvalues = []

    finalarray=[]
    
    finalarray.append(initialcluster)

    totxvalues = defaultdict(list)
    totyvalues = defaultdict(list)
    # initialize distances map 
    mapdistances = defaultdict(list)

    obnum =0

    currentdistances = []
    
    listclusterids=[]

    for j in range(0, mx):
        mapdistances[j]=[]
        totxvalues[j] = []
        totyvalues[j] = []


    for i in range(initialframe, endframe+1): # must iterate over endframe
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
                
                #plt.scatter(arrayx, arrayy)

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

            #plt.scatter(hxvalues, hyvalues)

            # print mean
            #print("mean x,",np.mean(hxvalues))
            #print("mean y,",np.mean(hyvalues))

            # reset hxvalues and hyvalues (don't need )
            hxvalues =[]
            hyvalues =[]

    #plt.show()
    
    
    listclusterids =finalarray
    # app 

    currentframe = initialframe

    #initialcluster 

    result = []
    result.append(initialcluster)

    prevmatched = initialcluster

    boolean = 1 # if there is still a next match 

    rownum = 0

    with open(datastorename) as datastore_csv_file:
        datastore_csv_reader = csv.reader(datastore_csv_file, delimiter=",")

        for row in datastore_csv_reader:
            rownum =rownum+1

            # 1 - frame 
            framenum = float(row[0])

            # 2 - cluster id
            clusterid = float(row[1])
            matched = float(row[18]) 

            # if past end frame
            if framenum > endframe:
                break

            if framenum < initialframe:
                continue


            if framenum != currentframe:
                if boolean == 0:
                    #print("bool break")
                    #print("row,", rownum)

                    break # no more next match

                # append to matched
                #print("row num,", rownum)
                result.append(nextmatched)

                prevmatched = nextmatched

                boolean = 0

                currentframe = framenum

            #print("frame num", framenum)





            if clusterid == prevmatched:
                nextmatched = matched
                boolean = 1 # found the next match

    len1 = len(result) #datastore result
    len2 = len(listclusterids) # our result 

    setlen = min(len1, len2)

    removemissed= 0
    removecontinued =0 
    contmatching = 1

    if len2 < len1: # missed matching
        # find if there is a wrong matching first 
        setlen = len2-1 # do not compare last element
        wrongfirst =0
        nolongerwrong=0
        for j1 in range(0, setlen):
            frameno1 = initialframe+j1
            if result[j1] != listclusterids[j1]:
                v1 =errorclusters.get(frameno1)
                if v1 != None:
                    if result[j1] in v1:
                        if listclusterids[j1] in v1:
                            nolongerwrong=1
                if nolongerwrong != 1:
                    print("wrong first in missed matching in", c,"at frame", initialframe+j1)
                    wrongfirst=1
        lastelement = listclusterids[setlen]
        # check last element of our array for similar clusters which may match to next cluster of app
        if wrongfirst ==0:
            print("missed matching at,", c, "at", initialframe+setlen)
            missedmatching = missedmatching+1
            totalcomparisons = totalcomparisons+setlen 
            v = errorclusters.get(initialframe+ setlen)
            iframe = initialframe+setlen
            if v != None:
                errorarray = errorclusters[initialframe+setlen]
                res = []
                for el in errorarray:
                    # ea group of clusters
                    if lastelement in el:
                        arraywithlast = el
                        for a in arraywithlast:
                            nc = findnextclusterdist(iframe, el)
                            if nc!=0:
                                res.append(nc)
                nextlen =len2 # len2 +1 -> subtract 1 to refer to result index
                print("next len", nextlen)
                #if nextlen >= maxnumframes:
                #    continue
                if result[nextlen] in res:
                    # removed missed matching
                    removemissed = 1
                    #missedmatching = missedmatching-1
                    #clustering_error= clustering_error+1 
                    #break # only need 1 match

    if removemissed==1:
        print("remove missed matching at", c, "at frame", initialframe+nextlen)
        missedmatching = missedmatching-1
        clustering_error= clustering_error+1 

    if len1 < len2: # continued matching 
        setlen = len1 -1 
        iframe = initialframe+setlen
        # must check if wrong first (too)
        wrongfirstcont = 0  # keep this as an indicator for comparison 
        nolongerwrong2 =0
        for j2 in range(0, setlen):
            frameno2 = initialframe+j2
            if result[j2] != listclusterids[j2]:
                # first check errorclusters 
                v1 = errorclusters.get(frameno2)
                if v1 !=None:
                    if result[j2] in v1:
                        if listclusterids[j2] in v1:
                            nolongerwrong2=1
                if nolongerwrong2!=1:
                    wrongfirstcont = 1
        if wrongfirstcont ==0:
            print("cont. matching at ",c)
            continuedmatching = continuedmatching+1
            totalcomparisons = totalcomparisons + setlen
            
            seclast1= listclusterids[setlen]
            last2 = result[setlen]
            last1 = listclusterids[setlen+1]
            
            v = errorclusters.get(initialframe+ setlen)
            v2 = errorclusters.get(initialframe + setlen+1)
            
            print("v2 index", initialframe+setlen+1)
            existsimilarlast1 =0
            existsimilar2 = 0
            
            if v2 != None:
                for gp in v2:
                    if last1 in gp:
                        existsimilarlast1 = 1
                        simlast1 = gp
            
            if v != None:
                errorarray = errorclusters[initialframe + setlen]
                if seclast1 == last2:
                    print("scen. 1")
                    res2 = []
                    
                    for el in errorarray:
                        if last2 in el:
                            arraywithlast = el
                            for a in arraywithlast:
                                nc = appfindnextcluster(iframe, a)
                                if nc!=0:
                                    res2.append(nc)
                    if v2 == None:
                        if last1 in res2:
                            print("match discont. cont. 1")
                            contmatching =0
                    if v2!=None:
                        for el2 in simlast1:
                            if el2 in res2:
                                print("match discont. cont. 2")
                                contmatching=0
            else: # scen.2 
                res2 = []
                print("scen. 2")
                for el in errorarray:
                    if seclast1 in el and last2 in el:
                        print("exists similar 2")
                        existsimilar2 = 1
                        sim = el 
                if existsimilar2 == 1:
                    for s in sim:
                        print("iframe", iframe)
                        nc = appfindnextcluster(iframe, s)
                        if nc != 0:
                            res2.append(nc)
                    print("res2", res2)
                if v2 == None:
                    if last1 in res2:
                        print("match discont. scen. 2")
                        contmatching=0
                if v2!=None:
                    for el2 in simlast1:
                        if el2 in res2:
                            print("match discont. scen. 2 p2")
                            contmatching=0
                    
    if contmatching==0:
        print("remove cont. matching at", c)
        continuedmatching = continuedmatching-1
        clustering_error= clustering_error+1

    if removemissed==1 or contmatching==0:
        print("do not check wrong")
    else:
        for j in range(0, setlen):
            frameno = initialframe+j
            totalcomparisons = totalcomparisons+1
            if result[j] != listclusterids[j]:
                # first check errorclusters for wrong found
                v = errorclusters.get(frameno)
                if v!= None:
                    if result[j] in v:
                        if listclusterids[j] in v:
                            print("no longer wrong")
                            break
                print("wrong found")
                wrongmatching = wrongmatching+1
                break 

    
    
    
