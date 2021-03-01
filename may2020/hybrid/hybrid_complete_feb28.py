# check initial angle if angles array is empty : if y>0 check it is moving +y, -x; if y<0 check it moving -y, +x

# hybrid 2 complete procedure

totalcomparisons = 0

c1 = 1
c2 = 7 # 6

# new params
totresults = []
totclusterids=[]

#diff. category of accuracy index
missedmatching = 0
wrongmatching =0 # matched to a different cluster
continuedmatching = 0 # continues erroneously 

clustering_error = 0 

#####
initialframe = 80
endframe = 90


for initialcluster in range(c1, c2+1):
    
    
    arrayx = []
    arrayy = []
    pavex = []
    pavey = []

    phx = [] # previous high x values
    phy =[] 


    obnum = 1

    totalmap ={}

    prevmap = {}

    mf = defaultdict(list)
    # maximum object/cluster id in any frame
    mx = 20

    for j in range(0, mx):
        mf[j]=0 

    matchfreq= mf


    thres= 10

    finalarray=[]

    finalarray.append(initialcluster)

    finalx =[]
    finaly =[]

    avex =[]
    avey =[]

    xvalues =[]
    yvalues =[]

    # edited method
    angles = []
    
    for i in range(initialframe, endframe+1):
        name = "file_out"
        name = name+str(i)
        name = name+".csv"
        firstrow=0
        # clear matchfreq
        for j in range(0, mx):
            matchfreq[j] =0

        currentmap3 = {} # average coordinates

        print("curr frame is:", i)


        with open(name) as csv_file:
            f =0 
            # reset hxvalues , hyvalues
            hxvalues = []
            hyvalues=[]

            obnum=1 

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
                        #i1 = newhighestfreq(fromi)
                        prevmap[i1] = 1

                plt.scatter(arrayx, arrayy)

                avx = np.mean(arrayx)
                avy = np.mean(arrayy)

                finalx.append(avx)
                finaly.append(avy)

                # save angle

                plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

                #append avx and avy
                avex.append(avx)
                avey.append(avy)

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
                    obnum= clusterid
                    currentmap={}
                    # take the average
                    avecurrentx = np.mean(xvalues)
                    avecurrenty = np.mean(yvalues)
                    currentmap3[numo1] = [avecurrentx, avecurrenty]

                    xvalues =[]
                    yvalues =[]

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
                # save to map
                currentmap[i1] = 1
                # check prev map
                val = prevmap.get(fromi)
                if val == None:
                    pass
                else:
                    numo = float(obnum)
                    matchfreq[numo] = matchfreq[numo]+1
            numo2 = float(clusterid)
            avecurrentx = np.mean(xvalues) ##USE AS CURRENT X
            avecurrenty = np.mean(yvalues)
            currentmap3[numo2] = [avecurrentx, avecurrenty]
            totalmap[numo2] = currentmap
            xvalues=[] ##RESET
            yvalues=[]
            if matchfreq[numo2] > f:
                ky = numo2
                hxvalues = xvalues
                hyvalues = yvalues
                totalmap[ky]= currentmap

            if len(hxvalues) ==0:
                foundmin=0
                mindist = thres
                c_first=0
                for c in currentmap3:
                    cvalue = currentmap3[c]
                    cx = cvalue[0]
                    cy = cvalue[1]
                    ax = finalx[-1]
                    ay = finaly[-1]
                    dist1 = pow(cx - ax,2) + pow(cy - ay,2)
                    dist = math.sqrt(dist1)
                    if dist < thres:
                        if c_first==0:
                            c_first=1
                            minclust=c
                            mcx = cx
                            mcy= cy
                            mindist = dist
                        foundmin=1
                        if dist< mindist:
                            mindist = dist
                            minclust=c
                            mcx = cx
                            mcy = cy
                if foundmin==1:
                    print("found min")
                    print("dist is", mindist)
                    print("minclust is", minclust)
                    if len(angles)==0:
                        print("angles array is of length 0 and minclust:", minclust)
                        prevmap = totalmap[minclust]
                        avx = mcx
                        avy = mcy 
                        finalarray.append(minclust)                       
                        # add to angles
                        xdiff = avx - finalx[-1]
                        ydiff = avy - finaly[-1]
                        ## check initial direction 2/28/21 
                        if avy >0: # +y, -x
                            # break if both directions are unsatisfied / one direction unsat.
                            if xdiff >0 and ydiff <0:
                                print("both dir. unsat.")
                                # plot
                                plt.scatter(mcx, mcy)
                                plt.annotate("wrong dir.", (mcx, mcy))
                                break
                        if avy <0: # -y, +x
                            if xdiff<0 and ydiff>0:
                                print("both dir. unsat.")
                                plt.scatter(mcx, mcy)
                                #plot 
                                plt.annotate("wrong dir.", (mcx, mcy))
                                break
                        rad = math.atan2(ydiff, xdiff)
                        ang = math.degrees(rad)
                        if ang<0:
                            ang = 360+ang
                        angles.append(ang)

                        finalx.append(mcx)
                        finaly.append(mcy)



                        #plt.scatter(mcx, mcy)
                        #plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
                        continue
                    prev_avex = finalx[-1]
                    prev_avey = finaly[-1]

                    xdiff_curr = mcx - prev_avex #how is avx set?
                    ydiff_curr = mcy - prev_avey 
                    # calc angle
                    rad = math.atan2(ydiff_curr, xdiff_curr)

                    ang = math.degrees(rad)
                    if ang<0:
                        ang = 360+ang

                    prev_ang = angles[-1]

                    ang_diff = abs(ang - prev_ang)

                    print("prev ang :", prev_ang)
                    print("curr ang:", ang)

                    print("ang_diff is:", ang_diff)
                    if ang_diff <= 30: # change from 45 to 30
                        print("angle holds")
                        prevmap= totalmap[minclust]
                        avx = mcx
                        avy =mcy
                        finalarray.append(minclust)
                        finalx.append(mcx)
                        finaly.append(mcy)
                        # append to slopes / diffs
                        #xdiff.append(avx - avex[-1])
                        #ydiff.append(avy - avey[-1])
                        #avex.append(avx)
                        #avey.append(avy)
                        #append to angles
                        angles.append(ang)
                    else:
                        print("angles too large, stop")
                        break
                else:
                    print("not found and end, after last frame", i)
                    break
            if len(hxvalues) !=0:
                finalarray.append(ky)
                prevmap = totalmap[ky]

                avx = np.mean(hxvalues)
                avy = np.mean(hyvalues)

                prev_avx = finalx[-1]
                prev_avy = finaly[-1]

                # update angles
                xdiff = avx - prev_avx
                ydiff = avy - prev_avy 
                rad = math.atan2(ydiff, xdiff)
                ang = math.degrees(rad)
                if ang <0:
                    ang = 360+ang
                angles.append(ang)

                finalx.append(avx)
                finaly.append(avy)

            #print("final x", finalx)
            #print("final y", finaly)


    print("initial cluster", initialcluster)
    print("initial frame", initialframe)

    print("final array is", finalarray)
    
    listclusterids= finalarray
    
    print("listclusterids is", listclusterids)
    
    # plot
    
    
    alen = len(finalarray)
    print("length of array ", alen)
    
    xv1=[]
    yv1=[]

    ax =[]
    ay =[]

    acounter=0
    for i in range(initialframe, initialframe+alen):
        name = "file_out"
        name = name+str(i)
        name = name+".csv"


        a = finalarray[acounter]
        xarray = []
        yarray = []
        with open(name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                clusterid = float(row[0])
                xpoint = float(row[1])
                ypoint = float(row[2])

                if clusterid == a:
                    xarray.append(xpoint)
                    yarray.append(ypoint)


            # plot
            plt.scatter(xarray,yarray)
            avx = np.mean(xarray)
            avy = np.mean(yarray)
            plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

            ax.append(avx)
            ay.append(avy)

        acounter =acounter +1
        if acounter > alen:
            break

    plt.show()
    
    # app result
    result = []
    result.append(initialcluster)
    
    iframe = initialframe
    currentcluster = initialcluster
    t = True
    while t:
        nextres = findnextclusterapp(iframe, currentcluster)
        if str(nextres) == "nan":
            break
        if iframe >= endframe:
            break
        result.append(nextres)
        iframe = iframe+1
        currentcluster = nextres
        
    len1 = len(result) #datastore result
    len2 = len(listclusterids) # our result 

    setlen = min(len1, len2)
    od1 = {}
    od2 = {}
    booleanwrong=[]
    
    for j1 in range(0,setlen):
        nolongerwrong=0
        nolongerwrongoriginal=0
        frameno=initialframe+j1
        od1[frameno]=[result[j1]]
        od2[frameno]=[listclusterids[j1]]
        if result[j1]==listclusterids[j1]:
            nolongerwrong=1
            nolongerwrongoriginal=1
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
            if nolongerwrongoriginal==0:
                clustering_error = clustering_error+1
    maxlen= max(len1, len2)
    last1 = result[setlen-1]
    last2 = listclusterids[setlen-1]
    
    if len1 != len2:
# iterate over setlen to max len
        for j2 in range(setlen, maxlen):
            nolongerwrong=0
            nolongerwrongoriginal = 0 
            frameno2 = initialframe+j2
            if len1 > len2:
                next2 = findnextcluster(frameno2, last2)
                if next2 == result[j2]:
                    nolongerwrong=1
                    nolongerwrongoriginal=1
                v2 = errorclusters.get(frameno2)
                if v2 != None:
                    errorarray = errorclusters[frameno2]
                    for el in errorarray:
                        if result[j2] in el:
                            if next2 in el:
                                nolongerwrong=1
                if nolongerwrong==1:
                    booleanwrong.append(0)
                    if nolongerwrongoriginal ==0:
                        clustering_error= clustering_error+1
                else:
                    booleanwrong.append(1)
                last2 = next2
            if len2 > len1:
                next2 = findnextclusterapp(frameno2, last2)
                if next2 == listclusterids[j2]:
                    nolongerwrong=1
                    nolongerwrongoriginal=1
                v2 = errorclusters.get(frameno2)
                if v2 != None:
                    errorarray = errorclusters[frameno2]
                    for el in errorarray:
                        if listclusterids[j2] in el:
                            if next2 in el:
                                nolongerwrong=1
                if nolongerwrong==1:
                    booleanwrong.append(0)
                    if nolongerwrongoriginal==0:
                        clustering_error=clustering_error+1
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
    setlen = min(len1, len2)
    maxlen= max(len1,len2)
    
    for j in range(0, maxlen):

        frameno = initialframe+j 
        #print("j is", j)
        #print("frame num is", frameno)

        # all clusters within current frame
        clust1 = d1[frameno]
        clust2 = d2[frameno]


        # check clusters to next step
        for c1 in clust1:
            nc1 = findnextclusterapp(frameno, c1)
            if str(nc1) == "nan":
                #print("nc1 is nan")
                continue
            #print("frameno plus one", frameno+1)
            #print("nc1", nc1)
            nclust1 = d1[frameno+1]
            # only append if not already there
            if nc1 not in nclust1:
                nclust1.append(nc1)
            #nclust1.append(nc1)
            #nclust1 = np.unique(nclust1)
            d1[frameno+1] = nclust1
        for c2 in clust2:
            nc2 = findnextcluster(frameno, c2)
            if nc2 == -1:
                continue
            nclust2 = d2[frameno+1]
            if nc2 not in nclust2:
                nclust2.append(nc2)
            d2[frameno+1] = nclust2
        if booleanwrong[j]==1:
            set1 = set(clust1)
            intersect = set1.intersection(clust2)
            if len(intersect)>0:
                print("intersect")
                booleanwrong[j]=0
                clustering_error=clustering_error+1

    bindex = 1
    firstframewrong = -1
    for b in booleanwrong:
        if b == 1:
            firstframewrong = bindex
            break
        bindex= bindex+1

    if firstframewrong == -1:
        totalcomparisons= totalcomparisons+maxlen
    else:
        totalcomparisons= totalcomparisons+firstframewrong
        
    contflag = 0
    missedflag= 0
    
    # print length of array found
    print("len of listclusterids", len(listclusterids))
    
    if np.sum(booleanwrong) >0:
        if firstframewrong>len1:
            print("continued")
            print("array1", result) # array1 is app result
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
        
        if contflag==1 and missedflag==1:
            print("BOTH CONTINUED AND MISSED")
        
print("missed matchings:", missedmatching)
print("cont matchings:", continuedmatching)
print("wrong matchings:", wrongmatching)
print("total :", totalcomparisons)
print("clust. errors:", clustering_error)
