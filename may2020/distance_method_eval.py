# missed
# continued 
# wrong 

missedmatching=0
continuedmatching=0
wrongmatching=0
clustering_error = 0
totalcomparisons = 0

# lengths 
len1 = len(result) #datastore result
len2 = len(listclusterids) # our result 

print(len1)
print(len2)

setlen = min(len1, len2)

removemissed= 0
removecontinued =0 
contmatching =1 

iframe = initialframe+setlen

if len2 < len1: # missed matching
    # find if there is a wrong matching first 
    setlen = len2-1 # do not compare the last element
    wrongfirst =0
    nolongerwrong =0
    for j1 in range(0, setlen):
        frameno1 = initialframe+j1
        if result[j1] != listclusterids[j1]:
            v1 = errorclusters.get(frameno1)
            if v1 != None:
                if result[j1] in v1:
                    if listclusterids[j1] in v1:
                        nolongerwrong=1
            if nolongerwrong!= 1:
                print("wrong first in missed matching in", c, "at frame",i)
                wrongfirst=1
    # check last element of our array for similar clusters which may match to next cluster of app
    lastelement = listclusterids[setlen]
    if wrongfirst ==0:
        print("missed matching at,", c)
        #print("length of missed", len2)
        missedmatching = missedmatching+1
        totalcomparisons = totalcomparisons+setlen 
        
        v = errorclusters.get(initialframe+ setlen)
        iframe = initialframe+setlen
        print("iframe", iframe)
        if v != None:
            errorarray = errorclusters[initialframe+setlen]
            # must check if similar cluster linked to current 
            res = []
            for el in errorarray:
                # each group of clusters
                if lastelement in el:
                    arraywithlast = el
                    for a in arraywithlast:
                        nc = findnextclusterdist(iframe, a)
                        if nc!= 0:
                            res.append(nc)
            nextlen =len2
            print("res next len", result[nextlen])
            print("res", res)
            if result[nextlen] in res:
                # removed missed matching
                removemissed = 1
                #missedmatching = missedmatching-1
                #clustering_error= clustering_error+1 
                #break # only need 1 match

if removemissed==1:
    print("remove missed matching at", c)
    missedmatching = missedmatching-1
    clustering_error= clustering_error+1 

if len1 < len2: # continued matching 
    setlen = len1 -1 
    iframe = initialframe + setlen
    # must check if wrong first (too)
    wrongfirstcont = 0  # keep this as an indicator for comparison 
    #contmatching= 1 # do not remove cont. matching
    for j2 in range(0, len1 - 1 ): 
        if result[j2] != listclusterids[j2]:
            # first check errorclusters 
            #print("wrong first in continued matching in", c)
            wrongfirstcont = 1
            
    if wrongfirstcont ==0:
        print("cont. matching at ",c)
        continuedmatching = continuedmatching+1
        totalcomparisons = totalcomparisons + setlen
        # scenario 1 : step 1: compare last el of result 
        
        seclast1 = listclusterids[setlen]
        last2 = result[setlen]
        last1 = listclusterids[setlen+1]
        # sim clusters to a1[setlen+1]
        #a1next = listclusterids[setlen+1]
        
        print("v frame", initialframe+setlen)
        
        
        v = errorclusters.get(initialframe+ setlen) # similar clusters to last a2 element 
        v2 = errorclusters.get(initialframe+setlen+1) # similar clusters to last a1 element
        
        print("v2 index", initialframe+setlen+1)
        existsimilarlast1 = 0
        existsimilar2 = 0
        
        print("iframe", iframe)
        
        contmatching = 1
        #print("v2" , v2)
        if v2 != None:
            for gp in v2:
                if last1 in gp:
                    existsimilarlast1 =1 
                    simlast1 = gp # similar clusters to a1 's last

        #initpluslen1 = initialframe+setlen
        if v != None: 
            errorarray = errorclusters[initialframe+setlen]
                        
            if seclast1 ==last2: #scenario 1 
                print("scenario 1")
            # if it is in similar clusters
                res2 = []
                for el in errorarray:
                    if last2 in el:
                        arraywithlast = el
                        for a in arraywithlast:
                            #print("iframe,", iframe,"a",a)
                            nc = appfindnextcluster(iframe, a)
                            if nc != 0:
                                res2.append(nc)
                # if v2 is not none
                if v2 == None:
                    if last1 in res2:
                        print("match discont. v2")
                        contmatching=0
                if v2!=None:
                    for el2 in simlast1:
                        if el2 in res2:
                            print("match discont. cont. matching")
                            contmatching =0 # false cont. matching

            else:
                res2 = []
                # scenario 2 
                print("scen. 2")
                for el in errorarray: # each group of clusters
                    if seclast1 in el and last2 in el:
                        print("exists similar 2")
                        existsimilar2 = 1
                        sim = el # s group
                if existsimilar2 == 1:
                    # next cluster from elements in s
                    print("sim", sim)
                    for s in sim:
                        print("iframe", iframe)
                        nc = appfindnextcluster(iframe, s)
                        if nc != 0:
                            res2.append(nc)
                    print("res2", res2)
                if v2 == None:
                    #print("last1", last1)
                    if last1 in res2:
                        print("match discont. v2")
                        contmatching = 0
                if v2 != None:
                    for el2 in simlast1:
                        if el2 in res2:
                            print("match discont. cont. matching v2 ")
                            contmatching =0
                        
if contmatching == 0: #removecontinued==1:
    print("remove cont. matching at", c)
    continuedmatching = continuedmatching-1
    clustering_error= clustering_error+1

if removemissed==1 or contmatching==0:
    print("do not check wrong")
else:
    for j in range(0, setlen):
        frameno = initialframe+j
        totalcomparisons = totalcomparisons+1
        if result[j] != listclusterids[j]:
            # first check errorclusters for wrong found
            v = errorclusters.get(frameno)
            if v!= None:
                if result[j] in v:
                    if listclusterids[j] in v:
                        print("no longer wrong")
                        break
            print("wrong found")
            wrongmatching = wrongmatching+1
            break 

                    
