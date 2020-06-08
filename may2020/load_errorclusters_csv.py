# pre processing step: load lidar_similarlabeledclusters.csv

# dictionary mapping framenumber to array of clusterids
errorclusters = {}

firstrow =0


lidarsim = 'lidar_similarlabeledclusters.csv'
with open(lidarsim) as lidarsim_csv_file:
    sim_csv_reader = csv.reader(lidarsim_csv_file, delimiter=",")
    for row in sim_csv_reader:
        # skip header row
        if firstrow==0:
            firstrow=1
            continue
        framenumber = int(row[0])
        arr = []
        cluster1 = row[1]
        cluster2 = row[2]
        cluster3 = row[3]
        arr.append(int(cluster1))
        if len(cluster2) > 0:
            arr.append(int(cluster2))
        if len(cluster3) >0:
            arr.append(int(cluster3))
        
        errorcode = int(row[4])
        if errorcode == 1:
            # add to dictionary
            #print("add")
            errorclusters[framenumber] = arr        
