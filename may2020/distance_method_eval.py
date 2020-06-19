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

setlen = len1

removemissed= 0
removecontinued =0 

if len2 < len1: # missed matching
    # find if there is a wrong matching first 
    setlen = len2
    wrongfirst =0
    for j1 in range(0, setlen):
        if result[j1] != listclusterids[j1]:
            #wrongmatching = wrongmatching+1 : count the wrong matching in below
            #print("wrong first in missed matching in", c)
            wrongfirst=1
    # check last element of our array for similar clusters which may match to next cluster of app
    if wrongfirst ==0:
        missedmatching = missedmatching+1
        totalcomparisons = totalcomparisons+1
        v = errorclusters.get(initialframe+ setlen)
        iframe = initialframe+setlen
        if v != None:
            errorarray = errorclusters[initialframe+setlen]
            res = []
            for el in errorarray:
                nc = findnextclusterdist(iframe, el)
                res.append(nc)
            nextlen =len2+1
            if result[nextlen] in res:
                # removed missed matching
                removemissed = 1
                #missedmatching = missedmatching-1
                #clustering_error= clustering_error+1 
                #break # only need 1 match

if removemissed==1:
    missedmatching = missedmatching-1
    clustering_error= clustering_error+1 

if len1 < len2: # continued matching 
    setlen = len1
    # must check if wrong first (too)
    wrongfirstcont = 0  # keep this as an indicator for comparison 

    for j2 in range(0, setlen):
        if result[j2] != listclusterids[j2]:
            # first check errorclusters 
            print("wrong first in continued matching in", c)
            wrongfirstcont = 1
    if wrongfirstcont ==0:
        continuedmatching = continuedmatching+1 
        v = errorclusters.get(initialframe+ setlen)
        if v != None:
            errorarray = errorclusters[initpluslen1]
            for e in errorarray:
                if e == listclusterids[initpluslen1+1]:
                    print("undo continued matching")
                    removecontinued = 1
                    #continuedmatching = continuedmatching-1
                    #clustering_error = clustering_error+1
                    #break # only need one match 
if removecontinued==1:
    continuedmatching = continuedmatching-1
    clustering_error= clustering_error+1

for j in range(0, setlen):
    totalcomparisons = totalcomparisons+1
    if result[j] != listclusterids[j]:
        # first check errorclusters
        print("wrong found")
        wrongmatching = wrongmatching+1
        break 

                    
