# complete procedure 2


# keep count of total number of comparisons + number of incorrect matches
totalcomparisons = 0

c1 = 1
c2 = int(clusteridfinal)+1

# new params
totresults = []
totclusterids=[]

#diff. category of accuracy index
missedmatching = 0
wrongmatching =0 # matched to a different cluster
continuedmatching = 0 # continues erroneously 

clustering_error = 0 

#####
initialframe = 10
endframe = 20


for c in range(c1, c2):
    arrayx = []
    arrayy=[]

    initialcluster=c

    listclusterids = []

    listclusterids.append(initialcluster)

    obnum = 0


    totalmap={}

    previndices=[]
    currentindices=[]
    totalmap = {}

    finalarray=[]

    xvalues = []
    yvalues = []

    hxvalues =[]
    hyvalues= []

    prevmap={}

    mf = defaultdict(list)
    # maximum object/cluster id in any frame
    mx = 20

    for j in range(0, mx):
        mf[j]=0 

    matchfreq= mf

    for i in range(initialframe, endframe):
        name = "file_out"
        name = name+str(i)
        name = name+".csv"
        firstrow=0
        # clear matchfreq
        for j in range(0, mx):
            matchfreq[j] =0
        with open(name) as csv_file:
            f =0 
            # reset hxvalues , hyvalues
            hxvalues = []
            hyvalues=[]

            currentmap= {}

            csv_reader = csv.reader(csv_file, delimiter=",")

            if i==initialframe:
                for row in csv_reader:
                    # no need for first row skip 
                    clusterid = float(row[0])
                    if clusterid==initialcluster:
                        xpoint = float(row[1])
                        ypoint = float(row[2])
                        #print("xpt", xpoint)
                        #print("ypt", ypoint)
                        arrayx.append(xpoint)
                        arrayy.append(ypoint)
                        xr = round(xpoint)
                        yr = round(ypoint)
                        fromi = dinvlookupdict[(xr,yr)]
                        h1, i1 = dhighestfreq(fromi)
                        prevmap[i1] = 1
                plt.scatter(arrayx, arrayy)
                # reset ky 
                ky = initialcluster
                continue

            for row in csv_reader:
                clusterid = float(row[0])

                if clusterid != obnum:
                    numo1 = float(obnum)
                    # append into dictionary of maps
                    totalmap[numo1] = currentmap
                    if matchfreq[numo1] > f:
                        f = matchfreq[numo1]
                        print("f is", f)
                        ky = numo1

                        hxvalues = xvalues
                        hyvalues = yvalues
                    obnum = clusterid

                    currentindices=[]
                    currentmap= {}

                    xvalues =[]
                    yvalues =[]
                    # append first values
                    #xvalues.append(float(row[1]))
                    #yvalues.append(float(row[2]))

                    continue

                xpoint = float(row[1])
                ypoint = float(row[2])
                xr = round(xpoint)
                yr = round(ypoint)
                xvalues.append(xpoint) # save to array 
                yvalues.append(ypoint)
                fromi = dinvlookupdict[(xr,yr)]
                # function to find highest freq 
                h1, i1 = dhighestfreq(fromi)
                # check outlier
                freqo =0 
                if [xr, yr] in listoutliers:
                    # determine highest outlier count + coordinates
                    listofoutliers = listoutliers2[fromi]
                    for outlierpt in listofoutliers:
                        indexo = dinvlookupdict[(outlierpt[0], outlierpt[1])]
                        ocount = doutlier[fromi, indexo]
                        if ocount > freqo:
                            freqo = ocount
                            highindo = indexo
                # compare with dhighestfreq
                if freqo > h1:
                    i1 = highindo
                # save to indices
                currentindices.append(i1) 
                # save to map
                currentmap[i1] = 1
                # check prev map
                val = prevmap.get(fromi)
                if val ==None:
                    # do nothing
                    if search2==0:
                        print("hi")
                else:
                    numo = float(obnum)
                    matchfreq[numo]= matchfreq[numo]+1
            # check f values at end of file
            numo2 = float(obnum)
            if matchfreq[numo2] > f:
                ky = numo2
                hxvalues = xvalues
                hyvalues = yvalues
                totalmap[ky]= currentmap
            finalarray.append(ky)
            # ky is the cluster id with the highest frequency

            plt.scatter(hxvalues, hyvalues)

            if len(hxvalues) ==0:
                print("0 h vals")
            if len(hxvalues) !=0:
                # set prevmap to the one 
                listclusterids.append(ky) # only append if there is next match
                prevmap = totalmap[ky]
            # obnum

    plt.show()


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
                    print("bool break")
                    print("row,", rownum)

                    break # no more next match

                # append to matched
                print("row num,", rownum)
                
                # if nextmatched is nan, ignore
                
                if str(nextmatched) == 'nan':
                    break
                    
                result.append(nextmatched)

                prevmatched = nextmatched

                boolean = 0

                currentframe = framenum

            #print("frame num", framenum)





            if clusterid == prevmatched:
                nextmatched = matched
                boolean = 1 # found the next match


        totresults.append(result)
        totclusterids.append(listclusterids)
        # accuracy 
        numincorrect = 0

        # lengths 
        len1 = len(result) #datastore result
        len2 = len(listclusterids) # our result 

        setlen = min(len1, len2) 
        
        iframe = initialframe+setlen
        # booleans
        removemissed =0
        removecontinued =0
        contmatching = 1
        
        if len2 < len1: # missed matching
            # find if there is a wrong matching first 
            setlen = len2-1
            wrongfirst =0
            for j1 in range(0, setlen):
                if result[j1] != listclusterids[j1]:
                    #wrongmatching = wrongmatching+1 : count the wrong matching in below
                    print("wrong first in missed matching in", c)
                    wrongfirst=1
            lastelement = listclusterids[setlen] #check last element of our array for sim. clust.
            if wrongfirst ==0:
                missedmatching = missedmatching+1
                print("missed matching at", initialcluster)
                
                # add to total comparisons the frames compared  before missed: setlen
                totalcomparisons = totalcomparisons+ setlen
                v = errorclusters.get(initialframe+ setlen)
                iframe = initialframe+setlen
                if v != None:
                    errorarray = errorclusters[initialframe+setlen]
                    res = []
                    for el in errorarray:
                        #nc = findnextcluster(iframe, el)
                        #res.append(nc)
                        if lastelement in el:
                            arraywithlast = el
                            for a in arraywithlast:
                                nc= findnextcluster(iframe, a)
                                if nc!=0:
                                    res.append(nc)
                # check res
                    nextlen =len2
                    print("res next len", result[nextlen])
                    if result[nextlen] in res:
                        # removed missed matching
                        removemissed= 1 
                    #missedmatching = missedmatching-1
                    #clustering_error= clustering_error+1 
        if removemissed == 1:
            missedmatching = missedmatching-1
            clustering_error = clustering_error+1 
            
        if len1 < len2: # continued matching 
            setlen = len1-1
            # must check if wrong first (too)
            wrongfirstcont = 0  # keep this as an indicator for comparison 
            contmatching = 1 # do not remove a cont matching
            for j2 in range(0, setlen):
                if result[j2] != listclusterids[j2]:
                    # first check errorclusters 
                    print("wrong first in continued matching in", c)
                    wrongfirstcont = 1
                    # double check errorclusters 
            
            if wrongfirstcont ==0:
                continuedmatching = continuedmatching+1 
                # print
                print("continued matching", initialcluster)
                #print("our result", listclusterids)
                #print("datastore result", result)
                totalcomparisons = totalcomparisons +setlen 
                #initpluslen1 = initialframe+len1
                
                seclast1 = listclusterids[setlen]
                last2 = result[setlen]
                last1 = listclusterids[setlen+1]
                
                #print("initial plus len1 ,", initpluslen1)
                v = errorclusters.get(initialframe+ setlen)
                v2 = errorclusters.get(initialframe+setlen+1)
                existsimilarlast1 =0
                existsimilar2 = 0
                
                contmatching = 1
                
                if v2!=None:
                    for gp in v2:
                        if last1 in gp:
                            existsimilarlast1 = 1
                            simlast1 = gp
                
                if v != None:
                    errorarray = errorclusters[initialframe + setlen]
                    
                    if seclast1 == last2: #scenario 1
                        res2 = []
                        for el in errorarray:
                            if last2 in el:
                                arraywithlast = el
                                for a in arraywithlast:
                                    nc = appfindnextcluster(iframe,a)
                                    if nc !=0:
                                        res2.append(nc)
                        # if v2 is not none
                        if v2==None:
                            if last1 in res2:
                                contmatching = 0
                                print("match discont.")
                        if v2!=None:
                            for el2 in simlast1:
                                if el2 in res2:
                                    print("match discont.")
                                    contmatching=0
                    else: # scenario 2
                        res2 = []
                        for el in errorarray:
                            if seclast1 in el and last2 in el:
                                existsimilar2 = 1
                                sim = el # s group
                        if existsimilar2 ==1:
                            print("sim", sim)
                            for s in sim:
                                nc = appfindnextcluster(iframe, s)
                                if nc!=0:
                                    res2.append(nc)
                        if v2 == None:
                            if last1 in res2:
                                print("match discont. scen 2")
                                contmatching=0
                        if v2!= None:
                            for el2 in simlast1:
                                if el2 in res2:
                                    print("match discont. scen 2")
                                    contmatching=0
        if contmatching == 0:#removedcontinued == 1:
            continuedmatching = continuedmatching-1
            clustering_error = clustering_error+1
            
        ## june 7 note: edit to not count errors based on lidar similar labeled clusters file 
        ## also: count wrong based on one transition 

        for j in range(0, setlen):
            frameno = initialframe+j
            totalcomparisons = totalcomparisons+1
            if result[j] != listclusterids[j]:
                # first check errorclusters
                v = errorclusters.get(frameno)
                if v!= None:
                    if result[j] in v:
                        if listclusterids[j] in v:
                            print("no longer wrong")
                            break
                wrongmatching = wrongmatching+1
                #numincorrect = numincorrect+1
                print("incorrect in ",c)
                print("wrong:datastore result",result[j])
                print("wrong:our result",listclusterids[j])
                # break because it is wrong after 1 frame
                break 
        #print('init cluster id', c)
        #print('num incorrect', numincorrect)
        # incorrect = total wrong matchings 
        #incorrect = incorrect + numincorrect 

