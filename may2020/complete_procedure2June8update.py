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

        setlen = len1

        if len1 < len2: # continued matching 
            setlen = len1
            continuedmatching = continuedmatching+1 
            # print
            print("continued matching", initialcluster)
            print("our result", listclusterids)
            print("datastore result", result)
            totalcomparisons = totalcomparisons +1
            # also examine the frame where the continued matching was found 
            # from frame initialframe+ len1 check if there are similar clusters
            initpluslen1 = initialframe+len1
            v = errorclusters.get(initialframe+ len1)
            if v != None:
                errorarray = errorclusters[initpluslen1]
                # look for listclusterids[initialframe+len1+1] value 
                for e in errorarray:
                    if e == listclusterids[initpluslen1+1]:
                        print("undo continued matching")
                        continuedmatching = continuedmatching-1
            
        if len2 < len1: # missed matching
            # find if there is a wrong matching first 
            setlen = len2
            wrongfirst =0
            for j1 in range(0, setlen):
                if result[j1] != listclusterids[j1]:
                    #wrongmatching = wrongmatching+1 : count the wrong matching in below
                    print("wrong first in missed matching in", c)
                    wrongfirst=1
            if wrongfirst ==0:
                missedmatching = missedmatching+1
                print("missed matching", initialcluster)
                print("our result", listclusterids)
                print("datastore result", result)
            totalcomparisons = totalcomparisons+1
            
            
        ## june 7 note: edit to not count errors based on lidar similar labeled clusters file 
        ## also: count wrong based on one transition 

        for j in range(0, setlen):
            totalcomparisons = totalcomparisons+1
            if result[j] != listclusterids[j]:
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
        incorrect = incorrect + numincorrect 

