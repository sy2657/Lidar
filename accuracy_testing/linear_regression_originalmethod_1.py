# accuracy step 1

# save average x, y values of each frame to an array

import numpy as np

xv = []
yv = []


xmedian=[]
ymedian=[]

x_largest = []
y_largest = []

x_smallest = []
y_smallest = []

xlargest_x = []
xlargest_y = []
xsmallest_x = []
xsmallest_y = []

ylargest_x = []
ylargest_y = []
ysmallest_x = []
ysmallest_y = []

import matplotlib.pyplot as plt
from collections import defaultdict

# inputs 
dpath = "dec2019/Ramp/2019-9-9-15-0-0-BF1-CL1(0-18000frames)-Cluster_csv"

initialframe =1300
endframe = 1400


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

arrhxvalues=[]
arrhyvalues=[]

prevmap={}
# must intialize matchfreq
mf = defaultdict(list)
mx =20 
for j in range(0, mx):
    mf[j]=0 
matchfreq = mf


initialcluster = 8

for i in range(initialframe, endframe):
    name = "Cluster_Frame"
    name = name+str(i)
    name = name+".csv"
    # dec path
    pathname = dpath+"/"+name
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
                    arrhxvalues.append(xpoint)
                    arrhyvalues.append(ypoint)
                    xfloor = round(xpoint)
                    yfloor = round(ypoint)
                    # dec 
                    fromi = dinvlookupdict[(xfloor, yfloor)]
                    h1, i1 = dhighestfreq(fromi)
                    prevmap[i1] = 1
                    prevmap3 = prevmap
            # plt.scatter(arrayx, arrayy)
            #add to arrhxvalues

            #arrhxvalues = arrayx
            #arrhyvalues = arrayy
            # test with break statement
            # check prevmap here 

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
            # dec dictionary, highest frequency
            fromi = dinvlookupdict[(xr,yr)]
            h1, i1 = dhighestfreq(fromi)
            # check if in "outliers from" list
            freqo = 0
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
                print("high outlier")
            currentmap[i1] = 1
            # check prev map
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
        
        if len(hxvalues) != 0:
        # calc average 
            mean_x = np.mean(hxvalues)
            mean_y = np.mean(hyvalues)
            # try median 
            xv.append(mean_x)
            yv.append(mean_y)
            
            xmedian.append(np.median(hxvalues))
            ymedian.append(np.median(hyvalues))
            
            # np. argmax  in x 
            amx = np.argmax(hxvalues)        
            xlargest_x.append(np.max(hxvalues))
            xlargest_y.append(hyvalues[amx])
            
            x_largest.append(np.max(hxvalues))
            y_largest.append(hyvalues[amx])
            
            # in y            
            amy =np.argmax(hyvalues)
            
            ylargest_x.append(hxvalues[amy])
            ylargest_y.append(hyvalues[amy])
            
            y_largest.append(np.max(hyvalues))
            x_largest.append(hxvalues[amy])

            # smallest
            amin_x =  np.argmin(hxvalues)
            
            xsmallest_x.append(hxvalues[amin_x])
            xsmallest_y.append(hyvalues[amin_x])
            
            x_smallest.append(np.min(hxvalues))
            y_smallest.append(hyvalues[amin_x])
            
            amin_y = np.argmin(hyvalues)
            
            ysmallest_x.append(hxvalues[amin_y])
            ysmallest_y.append(hyvalues[amin_y])
            
            y_smallest.append(np.min(hyvalues))
            x_smallest.append(hxvalues[amin_y])
            
            

        # set prevmap
        if len(hxvalues) != 0:
            prevmap = totalmap[ky]

# at end of this j 
plt.scatter(arrhxvalues, arrhyvalues)
plt.scatter(xv, yv)
plt.scatter(xmedian, ymedian)

plt.scatter(xlargest_x, xlargest_y)
plt.scatter(xsmallest_x, xsmallest_y)

plt.show()
