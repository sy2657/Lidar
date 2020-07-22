# fix above code to take care of 1

# check accuracy with datastore.mat
datastorename = 'newdatastoreMay17.csv'
initialcluster=1

#curr_cluster = 0 

initialframe = 1
endframe = 10 

currentframe = initialframe

#initialcluster 

result = []
result.append(initialcluster)

prevmatched = initialcluster

boolean = 1 # if there is still a next match 

rownum = 0

# append from first frame

with open(datastorename) as datastore_csv_file:
    datastore_csv_reader = csv.reader(datastore_csv_file, delimiter=",")
    
    for row in datastore_csv_reader:
        rownum =rownum+1
        
        # 1 - frame 
        framenum = float(row[0])
        
        # 2 - cluster id
        clusterid = float(row[1])
        matched = float(row[18]) 
        
        # if past end frame
        if framenum > endframe:
            break
        
        if framenum < initialframe:
            continue
            
            
        if framenum != currentframe:
            if boolean == 0:
                print("bool break")
                print("row,", rownum)
                
                break # no more next match
                
            # append to matched
            #print("row num,", rownum)
            if str(nextmatched) == "nan":
                break
            
            result.append(nextmatched)
            
            prevmatched = nextmatched
            
            boolean = 0
            
            currentframe = framenum
            
        #print("frame num", framenum)
                
        
        

        
        if clusterid == prevmatched:
            nextmatched = matched
            boolean = 1 # found the next match
            
        
            
        
    
        # keep matching until there is no more next cluster
        
        
