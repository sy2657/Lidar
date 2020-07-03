def appfindnextcluster(initialcluster, iframe): # frame and cluster
    datastorename = 'newdatastoreMay17.csv'
    outputmatched =0
    with open(datastorename) as datastore_csv_file:
        datastore_csv_reader = csv.reader(datastore_csv_file, delimiter=",")

        for row in datastore_csv_reader:
            
            # 1 - frame 
            framenum = float(row[0])

            # 2 - cluster id
            clusterid = float(row[1])

            matched = float(row[18])  #return this matched

            if framenum < iframe:
                continue

            if clusterid == initialcluster:
                outputmatched = matched
                
            if framenum > iframe+1:
                break
    return outputmatched
