# disjoint where only find if prev matched not in current
def disjoint1(e,f):
    c = e.copy() # [:] works also, but I think this is clearer
    d = f.copy()
    for i in e:
        for j in f:
            if i==j:
                c.remove(i)
                d.remove(j)
    return c

def unique(list1): 
      
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    return unique_list
    
# input params

initialframe = 10
endframe = 15
#####

# method to find new cluster id without parent cluster id 
newclusters = []

newstartframes = [] # corresponding starting frame

# go over datastore file

# ignore the starting point if it does not have a next cluster id 

matchedto = []
prevmatchedto = []
currentclusters = [] # compare with matched previous
unmatched =[]

currframe = initialframe # current frame

with open(datastorename) as datastore_csv_file:
    datastore_csv_reader = csv.reader(datastore_csv_file, delimiter=",")
    
    for row in datastore_csv_reader:
        rownum =rownum+1
        
        # 1 - frame 
        framenum = float(row[0])
        clusterid = float(row[1])
        matched = float(row[18]) 
        
         # if past end frame
        if framenum > endframe:
            break
        
        if framenum < initialframe:
            continue
        
            
        if framenum != currframe:
            if currframe==initialframe:
                prevmatchedto=matchedto
                matchedto=[]
                currentclusters=[]
                currframe = framenum
                continue
            # compare currentclusters and prevmatchedto 
            unmatched = disjoint1(unique(currentclusters), unique(prevmatchedto)) 
            print("current clusters for", currframe, "is:", unique(currentclusters))
            print("prev matched for", currframe, "is:", unique(prevmatchedto))
            print("unmatched:", unmatched)
            for el in unmatched:
                newclusters.append(el)
                newstartframes.append(currframe)
            
            # reset 
            prevmatchedto = matchedto
            matchedto= []
            currentclusters = []
            currframe = framenum
       
        currentclusters.append(clusterid)
        matchedto.append(matched)
        
        
        # check the matched 
        
       
            
        # look for ids that were not mapped to 
        
