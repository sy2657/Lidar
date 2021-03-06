# complete procedure distance 
c1 =1 
c2 = 7

missedmatching=0
continuedmatching=0
wrongmatching=0
clustering_error = 0
totalcomparisons = 0

initialframe =10
endframe = 20

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
                if str(nextmatched) == "nan":
                    break
                result.append(nextmatched)

                prevmatched = nextmatched

                boolean = 0

                currentframe = framenum

            #print("frame num", framenum)





            if clusterid == prevmatched:
                nextmatched = matched
                boolean = 1 # found the next match

    print("array1 result is,", result)
    
    len1 = len(result) #datastore result
    len2 = len(listclusterids) # our result 

    setlen = min(len1, len2)

    #removemissed= 0
    #removecontinued =0 
    #contmatching = 1
    
    od1 = {}
    od2 = {}
    booleanwrong=[]
    
    for j1 in range(0,setlen):
        nolongerwrong=0
        frameno=initialframe+j1
        od1[frameno]=[result[j1]]
        od2[frameno]=[listclusterids[j1]]
        if result[j1]==listclusterids[j1]:
            nolongerwrong=1
        if result[j1]!= listclusterids[j1]:
            v1 = errorclusters.get(frameno)
            if v1!=None:
                errorarray= errorclusters[frameno]
                for el in errorarray:
                    if result[j1] in el:
                        if listclusterids[j1] in el:
                            nolongerwrong=1
        if nolongerwrong!=1:
            booleanwrong.append(1) # wrong
        else:
            booleanwrong.append(0) # not wrong
    maxlen= max(len1, len2)
    last1 = result[setlen-1]
    last2 = listclusterids[setlen-1]
    
    if len1 != len2:
# iterate over setlen to max len
        for j2 in range(setlen, maxlen):
            nolongerwrong=0

            frameno2 = initialframe+j2

            if len1 > len2:
                # look up
                next2 = findnextclusterdist(frameno2, last2)
                
                if next2 == result[j2]:
                    nolongerwrong=1
                    #booleanwrong.append(0)
                # check error clusters
                v2 = errorclusters.get(frameno2)
                #print("v2", v2)
                if v2 != None:
                    errorarray = errorclusters[frameno2]
                    for el in errorarray:
                        if result[j2] in el:
                            if next2 in el:
                                nolongerwrong=1
                if nolongerwrong==1:
                    booleanwrong.append(0) # not wrong
                else:
                    booleanwrong.append(1) # wrong

                last2 = next2
                # look up 

            if len2 > len1:
                next2 = findnextclusterapp(frameno2, last2)
                if next2 == listclusterids[j2]:
                    nolongerwrong=1
                v2 = errorclusters.get(frameno2)
                if v2 != None:
                    errorarray = errorclusters[frameno2]
                    for el in errorarray:
                        if listclusterids[j2] in el:
                            if next2 in el:
                                nolongerwrong=1
                if nolongerwrong==1:
                    booleanwrong.append(0)
                else:
                    booleanwrong.append(1) # wrong
                last2 = next2
    d1 = {}
    d2 = {}
    
    for j1 in range(0, setlen):
        frameno = initialframe+j1
        # check similar clusters
        clusters1 = od1[frameno]
        clusters2 = od2[frameno]

        simclusters = errorclusters.get(frameno)
        if simclusters != None:
            simarray = errorclusters[frameno]
            # check if matches
            for el in simarray:
                if od1[frameno] in el:
                    clusters1.extend(el)
                if od2[frameno] in el:
                    clusters2.extend(el)
        d1[frameno] = clusters1
        d2[frameno] = clusters2

    # add empty entries for range setlen to maxlen   
    maxlen= max(len1, len2)
    # set original clusters for up to maxlen
    for j2 in range(setlen, maxlen):
        frameno = initialframe+j2
        d1[frameno] = []
        d2[frameno] = []
        if len1>len2:
            d1[frameno]= [result[j2]]
        if len2>len1:
            d2[frameno]=[listclusterids[j2]]

    d1[initialframe+maxlen] = []
    d2[initialframe+maxlen] = []
    
    # evaluation 3
    
    setlen = min(len1, len2)
    maxlen= max(len1,len2)
# look for wrong matching

    for j in range(0, maxlen):

        frameno = initialframe+j 
        print("j is", j)
        print("frame num is", frameno)

        # all clusters within current frame
        clust1 = d1[frameno]
        clust2 = d2[frameno]


        # check clusters to next step
        for c1 in clust1:
            nc1 = findnextclusterapp(frameno, c1)
            if str(nc1) == "nan":
                print("nc1 is nan")
                continue
            #print("frameno plus one", frameno+1)
            print("nc1", nc1)
            nclust1 = d1[frameno+1]
            # only append if not already there
            if nc1 not in nclust1:
                nclust1.append(nc1)
            #nclust1.append(nc1)
            #nclust1 = np.unique(nclust1)
            d1[frameno+1] = nclust1

        for c2 in clust2:
            print("frame", frameno)
            print("clust", c2)
            nc2 = findnextclusterdist(frameno, c2)
            if nc2 == -1:
                continue
            nclust2 = d2[frameno+1]
            if nc2 not in nclust2:
                nclust2.append(nc2)
            d2[frameno+1] = nclust2

        if booleanwrong[j] == 1: # look for wrong
            # look for matching id from both arrays
            print("clust1,", clust1)
            print("clust2", clust2)
            set1 = set(clust1)
            intersect= set1.intersection(clust2)
            if len(intersect) >0:
                print("intersect")
                booleanwrong[j]=0 
                # increment clustering error
                clustering_error = clustering_error+1

    # last step: find first frame where it is wrong:
    #if is last element of array1 -> continued
    #if is last element of array2 -> missed
    # else: wrong 
    bindex = 1
    firstframewrong = -1
    for b in booleanwrong:
        if b == 1:
            firstframewrong = bindex
            break
        bindex= bindex+1

    contflag = 0
    missedflag= 0
    
    if np.sum(booleanwrong) >0:
        if firstframewrong>len1:
            print("continued")
            print("array1", result)
            print("array2", listclusterids)
            contflag= 1
            continuedmatching= continuedmatching+1
        if firstframewrong > len2: 
            print("missed")
            print("array1", result)
            print("array2", listclusterids)
            missedmatching = missedmatching+1
            missedflag=1
        if contflag==0 and missedflag==0:
            print("wrong")
            print("array1", result)
            print("array2", listclusterids)
            wrongmatching= wrongmatching+1
        
    '''
    if firstframewrong==len1:
        print("continued")
        totalcomparisons = totalcomparisons+len1
        continuedmatching=continuedmatching+1

    if firstframewrong==len2:
        print("missed")
        totalcomparisons=totalcomparisons+len2
        missedmatching= missedmatching+1

    # else, wrong
    if firstframewrong!=len1 and firstframewrong!=len2:
        if np.sum(booleanwrong)>0:
            print("wrong")
            print("first frame wrong", firstframewrong)
            print("len1", len1)
            print("len2", len2)
            print("array1", result)
            print("array2", listclusterids)
            if firstframewrong != -1:
                totalcomparisons=totalcomparisons+firstframewrong
            else:
                print("firstframewrong eq. -1")
            wrongmatching=wrongmatching+1

    '''
    
