# add in simple distance method where freq method found : single cluster

pframex =[]
pframey= []

from collections import defaultdict
import numpy as np
import math
# v 2 : adjusted method

# test for single starting cluster and frame


initialframe = 100
endframe= 150

arrayx = []
arrayy=[]

initialcluster= 9

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

##
thres=10

for i in range(initialframe, endframe+1):
    name = "file_out"
    name = name+str(i)
    name = name+".csv"
    firstrow=0
    # clear matchfreq
    for j in range(0, mx):
        matchfreq[j] =0
    ## adjust
    currentmap2 = {}
    currentmap3 = {} # average coordinates
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
                    #i1 = newhighestfreq(fromi)
                    prevmap[i1] = 1
                    
                    
            plt.scatter(arrayx, arrayy)

            avx1 = np.mean(arrayx)
            avy1 = np.mean(arrayy)
            plt.annotate(i, (avx1, avy1), textcoords="offset points", xytext=(0,10), ha='center')


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
                
                ## update
                currentmap2[numo1] = [ xvalues, yvalues] 
                
                # take the average
                avecurrentx = np.mean(xvalues)
                avecurrenty = np.mean(yvalues)
                currentmap3[numo1] = [avecurrentx, avecurrenty]
                

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
            ## temp comment out list outliers
            #if [xr, yr] in listoutliers:
                # determine highest outlier count + coordinates
            #    listofoutliers = listoutliers2[fromi]
            #    for outlierpt in listofoutliers:
            #        indexo = dinvlookupdict[(outlierpt[0], outlierpt[1])]
            #        ocount = doutlier[fromi, indexo]
            #        if ocount > freqo:
            #            freqo = ocount
            #            highindo = indexo
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
                pass
                #if search2==0:
                #    print("hi")
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



        if len(hxvalues) ==0:
            print("0 h vals")
            # print this frame
            
            # print previous coordinates
            #print("last x vals", phxvalues)
            #print("last y vals", phyvalues)
            print( "last x", avx)
            print("last y", avy)
            
            # break out
            #break
            mindist = thres
            foundmin = 0
            ## look for dist. of next cluster
            #print("current map is", currentmap3)
            for c in currentmap3:
                cvalue = currentmap3[c]
                cx = cvalue[0]
                cy = cvalue[1]
                dist1 = pow(cx - avx,2) + pow(cy - avy,2)
                dist = math.sqrt(dist1)
                print("cx", cx)
                print("cy", cy)
                print("dist,", dist)
                if dist< thres:
                    foundmin=1
                    minclust = c
                    mcx = cx
                    mcy = cy
                    if dist< mindist:
                        mindist= dist
                        minclust = c
                        mcx = cx
                        mcy = cy
            # add
            if foundmin==1:
                listclusterids.append(minclust)
                print("min cluster:", minclust)
                print("min dist:", mindist)
                # update prevmap
                prevmap = totalmap[minclust]
                # set avx, avy
                avx  = mcx
                avy = mcy
            else:
                print("not found")
                print("after last frame", i)
                break
            
        if len(hxvalues) !=0:
            #print("not 0")
            # set prevmap to the one 
            listclusterids.append(ky) # only append if there is next match
            prevmap = totalmap[ky]
            avx = np.mean(hxvalues)
            avy = np.mean(hyvalues)
        # obnum
        plt.scatter(hxvalues, hyvalues)
        
        # set previous x,y
        phxvalues= hxvalues
        phyvalues = hyvalues
        
        pframex.append(hxvalues)
        pframey.append(hyvalues)
        
        ### add to parrays
        #parrayx.extend(hxvalues)
        #parrayy.extend(hyvalues)

        
        #pavex.append(avx)
        #pavey.append(avy)
        plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

print("length of array", len(listclusterids))
plt.show()
