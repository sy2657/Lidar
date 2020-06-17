# find the next cluster from our algorithm

# iterate over all the clusters in frame len1+1 to see 
# iframe is frame number 

def findnextcluster(iframe, clusterarray):  # iframe is the current cluster, clusterarray holds ids of similar clusters 

    # sort by increasing order
    sortedarray = np.sort(clusterarray)
    name = "file_out"
    name = name+str(iframe)
    name1 = name+".csv"
    name2 = "file_out"+str(iframe+1)+".csv"

# clear matchfreq
    for j in range(0, mx):
        matchfreq[j] =0

    with open(name1) as csv_file:
        f =0 
        # reset hxvalues , hyvalues
        hxvalues = []
        hyvalues=[]

        countmap= {}

        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            cid= float(row[0]) 
            # determine which cluster id is the highest 
            xr = round(float(row[1]))
            yr = round(float(row[2]))
            fromi = dinvlookupdict[(xr,yr)]
            # function to find highest freq 
            h1, i1 = dhighestfreq(fromi)

            if cid in clusterarray:
                countmap[i1] = 1

    obnum = 1 

    f = 0                   
    with open(name2) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            cid = float(row[0])
            xr =round(float(row[1]))
            yr = round(float(row[2]))
            fromi = dinvlookupdict[(xr,yr)]
            # next cluster 
            if cid != obnum:
                numo1 = float(obnum)
                if matchfreq[numo1] > f:
                    f = matchfreq[numo1]
                    ky = numo1
                obnum = cid

            val = countmap.get(fromi)
            if val != None:
                matchfreq[cid] =matchfreq[cid]+1


    print(ky, "is the next cluster")     
    return ky
