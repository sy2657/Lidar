# hybrid: distance, angle, and convex hull area method

# hybrid 2 edit
import math


arrayx = []
arrayy = []
pavex = []
pavey = []

phx = [] # previous high x values
phy =[] 

initialframe = 420
endframe= 450

initialcluster=3

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

areas = []

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
        
        # convex hull area
        xlen = len(hxvalues)
        minx = avx
        minx_y = avy
        maxx = avx
        maxx_y = avy

        miny = avy
        miny_x = avx
        maxy = avy
        maxy_x = avx
        
        pdiff = 0
        map_diff_xy = {}
        
        for i in range(xlen):
            xv = xvalues[i]
            yv = yvalues[i]
            if xv > maxx:
                maxx = xv
                maxx_y = yv

            if xv < minx:
                minx = xv
                minx_y = yv

            if yv> maxy:
                maxy = yv
                maxy_x = xv

            if yv < miny:
                miny = yv
                miny_x = xv

          # calculate the magnitude
            xdiff = abs(xv - avx)
            ydiff = abs(yv - avy)
            diff = xdiff + ydiff
            if diff > pdiff:
                pdiff = diff
                # save to a map 
                map_diff_xy[diff] = [xv, yv]
                
        avgdist= 3
        athres = 5
        ch = [] # convex hull
        # append to array if the diff is big enough
        for key in map_diff_xy:
            if key > avgdist:
                coord = map_diff_xy[key]
                ch.append(coord)
        area = PolyArea2D(ch)
        
        if len(areas) >0:
            prev_area = areas[-1]
            #diff in areas
            adiff = abs( area - prev_area)
            print("area diff", adiff)
            if adiff > athres:
                print("areas are too different")
                break
                
        
        areas.append(area)
        #print("final x", finalx)
        #print("final y", finaly)
        
        
        #print(currentmap3)
