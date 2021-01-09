# Find the maximum trajectory lengths from initial frame and all initial clusters; record the found clusters in every 10th frame that start with

# version where finding max trajectories

c1 = 1
c2 = 4 # 6

ca = list(range(c1, c2+1))




# new params
totresults = []
totclusterids=[]

#diff. category of accuracy index
missedmatching = 0
wrongmatching =0 # matched to a different cluster
continuedmatching = 0 # continues erroneously 

clustering_error = 0 

#####
initialframe = 390
endframe = 480

# unew = map10[initialframe]
#carray = np.setdiff1d(ca, unew)


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

        #print("curr frame is:", i)


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
                    #print("found min")
                    #print("dist is", mindist)
                    #print("minclust is", minclust)
                    if len(angles)==0:
                        #print("angles length 0 and minclust:", minclust)
                        prevmap = totalmap[minclust]
                        avx = mcx
                        avy = mcy 
                        finalarray.append(minclust)
                        finalx.append(mcx)
                        finaly.append(mcy)
                        ky = minclust
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

                    #print("prev ang :", prev_ang)
                    #print("curr ang:", ang)

                    #print("ang_diff is:", ang_diff)
                    if ang_diff <= 45:
                        print("angle holds")
                        prevmap= totalmap[minclust]
                        avx = mcx
                        avy =mcy
                        finalarray.append(minclust)
                        finalx.append(mcx)
                        finaly.append(mcy)
                        ky = minclust # set key
                        # append to slopes / diffs
                        #xdiff.append(avx - avex[-1])
                        #ydiff.append(avy - avey[-1])
                        #avex.append(avx)
                        #avey.append(avy)
                else:
                    print("not found and end, after last frame", i)
                    break
            if len(hxvalues) !=0:
                finalarray.append(ky)
                prevmap = totalmap[ky]

                avx = np.mean(hxvalues)
                avy = np.mean(hyvalues)

                finalx.append(avx)
                finaly.append(avy)

            #print("final x", finalx)
            #print("final y", finaly)
            
            # add final key to map10
            if i % 10==0:
                print("(map10) i is", i)
                print("(map10) key is", ky)
                m10 = map10[i]
                m10.append(ky)
                # check sim clusts
                v1 = errorclusters.get(i)
                if v1!=None:
                    errorarray= errorclusters[i]
                    for el in errorarray:
                        for e in el:
                            if e == ky:
                                m10.extend(el)
                map10[i] = m10

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
