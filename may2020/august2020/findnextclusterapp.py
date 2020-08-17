# rename

datastorename = 'datastoreAug16.csv'

def findnextclusterapp(iframe, initialcluster): # frame and cluster
    #datastorename = 'newdatastoreMay17.csv'
    outputmatched =0
    rowid = 0
    with open(datastorename) as datastore_csv_file:
        datastore_csv_reader = csv.reader(datastore_csv_file, delimiter=",")

        for row in datastore_csv_reader:
            rowid = rowid+1
            # 1 - frame 
            framenum = float(row[0])

            # 2 - cluster id
            clusterid = float(row[1])

            matched = float(row[18])  #return this matched

            if framenum < iframe:
                continue
                
            if framenum > iframe:
                break

            if clusterid == initialcluster:
                print("row", rowid)
                print("frame num", framenum)
                print("init cluster", initialcluster)
                print("matched is ", matched)
                outputmatched = matched
                return outputmatched
            
    return outputmatched
