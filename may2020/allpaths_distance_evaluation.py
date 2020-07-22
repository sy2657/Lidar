# evaluation 2

missedmatching=0
continuedmatching=0
wrongmatching=0
clustering_error = 0
totalcomparisons = 0

# lengths 
len1 = len(result) #datastore result
len2 = len(listclusterids) # our result 


iframe = initialframe+min(len1, len2)

# calculate diff
difflen = max(len1, len2) - min(len1, len2)
# iterate over shorter length 

setlen = min(len1, len2)


# orig dictionary
od1 = {} # app 
od2 = {}

booleanwrong = []

for j1 in range(0, setlen):
    nolongerwrong = 0
    frameno = initialframe+j1
    od1[frameno] = [result[j1]] # original dictionary 
    od2[frameno] = [listclusterids[j1]]
    if result[j1] == listclusterids[j1]:
        nolongerwrong=1
    if result[j1] != listclusterids[j1]:
        v1 = errorclusters.get(frameno)
        print("j1", j1, "frameno", frameno)
        if v1 != None:
            errorarray = errorclusters[frameno]
            for el in errorarray:
                if result[j1] in el:
                    if listclusterids[j1] in el:
                        print("sim clusters")
                        nolongerwrong=1
    if nolongerwrong != 1:
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

# eval 2 b
# dictionary: frameno -> set of clusters for both results
d1 = {}
d2 = {}
# find path from each sim cluster
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

# make map for comparing
#m1 = {}
#m2 = {}


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
        nc2 = findnextclusterdist(frameno, c2)
        if nc2 ==-1:
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
            clustering_error= clustering_error+1

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

contflag=0
missedflag=0
if np.sum(booleanwrong) >0:
    
    if firstframewrong>len1:
        print("continued")
        contflag=1
        continuedmatching=continuedmatching+1

    if firstframewrong > len2:
        print("missed")
        missedflag=1
        missedmatching= missedmatching+1
 
    if contflag==0 and missedflag==0:
        print("wrong)
        wrongmatching=wrongmatching+1

