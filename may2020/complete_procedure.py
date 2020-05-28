# complete procedure 

initialcluster = 1
endcluster = 6

# accuracy 
# keep count of total number of comparisons + number of incorrect matches

totalcomparisons = 0
incorrect = 0  # total incorrect

totresults = [] # array of result arrays 

totclusterids = [] # array of clusterids 

# array to hold incorrect starting cluster

# data structure to keep track of the list of cluster ids 

obnum = 0

initialframe = 1
endframe = 10

mf = defaultdict(list)
# maximum object/cluster id in any frame
mx = 20

for j in range(0, mx):
    mf[j]=0 
    
for c in range(initialcluster, endcluster):
    # reset data structures
    matchfreq= mf
    xvalues = []
    yvalues = []

    hxvalues =[]
    hyvalues= []

    prevmap={}
    
    listclusterids = []

    listclusterids.append(c)
    
    totalmap = {}
    
    plt.clf()

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
                    if clusterid==c:
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
                #plt.scatter(arrayx, arrayy)
                # reset ky 
                ky = c
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
                #currentindices.append(i1) 
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
            listclusterids.append(ky)
            plt.scatter(hxvalues, hyvalues)

            if len(hxvalues) ==0:
                print("0 h vals")
            if len(hxvalues) !=0:
                # set prevmap to the one 

                prevmap = totalmap[ky]
            # obnum
    plt.show()
    # check with result
    # replace initial frame with c
    currentframe = c
    result= []
    
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
    len1 = len(result)
    len2 = len(listclusterids)

    setlen = len1

    if len1 < len2:
        setlen = len1
    if len2 < len1:
        setlen = len2

    for i in range(0, setlen):
        totalcomparisons = totalcomparisons+1
        if result[i] != listclusterids[i]:
            numincorrect = numincorrect+1
            print("incorrect in ",c)
    #print('init cluster id', c)
    print('num incorrect', numincorrect)
    incorrect = incorrect + numincorrect
    
