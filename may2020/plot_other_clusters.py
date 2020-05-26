# plot the other clusters 

alen = len(result)

# counter for array el
acounter = 0

for i in range(initialframe, endframe):
    name = "file_out"
    name = name+str(i)
    name = name+".csv"
    
    a = result[acounter]
    xarray = []
    yarray = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            clusterid = float(row[0])
            xpoint = float(row[1])
            ypoint = float(row[2])
            
            if clusterid == a:
                xarray.append(xpoint)
                yarray.append(ypoint)
                
                
        # plot
        plt.scatter(xarray,yarray)
    
    acounter =acounter +1
    if acounter > alen:
        break

plt.show()
    
            
