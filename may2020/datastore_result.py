# check accuracy with datastore.mat


#curr_cluster = 0 

initialframe = 1
endframe = 10 

currentframe = 1

#initialcluster 

result = []
result.append(initialcluster)

prevmatched = initialcluster

boolean = 1 # if there is still a next match 

rownum = 0

with open(datastorename) as datastore_csv_file:
    datastore_csv_reader = csv.reader(datastore_csv_file, delimiter=",")
    
    for row in datastore_csv_reader:
        rownum =rownum+1
        
        # 1 - frame 
        framenum = float(row[0])
        
        # if past end frame
        if framenum > endframe:
            break
        
        if framenum < initialframe:
            continue
                
        # 2 - cluster id
        clusterid = float(row[1])
        
        matched = float(row[18]) 
        
        if clusterid == prevmatched:
            nextmatched = matched
            boolean = 1 # found the next match
            
        if framenum != currentframe:
            if boolean == 0:
                print("bool break")
                print("row,", rownum)
                
                break # no more next match
                
            # append to matched
            result.append(nextmatched)
            
            prevmatched = nextmatched
            
            boolean = 0
            
            currentframe = framenum
            
        
    
        # keep matching until there is no more next cluster
        
