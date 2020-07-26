# plot other clusters

array1 =[7, 5.0, 7.0, 6.0, 5.0, 3.0, 4.0, 3.0, 3.0]
array2 = [7, 5, 7, 6, 7, 4, 5, 4, 3, 2, 3]

result=array1
result2= array2

alen = len(result)
alen2 = len(result2)

acounter=0
# counter for array el

xv1 =[]
yv1=[]
xv2 = []
yv2 = []

for i in range(initialframe, initialframe+alen):
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
        xv1.extend(xarray)
        yv1.extend(yarray)
        #plt.scatter(xarray,yarray)
    
    acounter =acounter +1
    if acounter > alen:
        break

acounter=0
for i in range(initialframe, initialframe+alen2):
    name = "file_out"
    name = name+str(i)
    name = name+".csv"
    
    
    a = result2[acounter]
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
        xv2.extend(xarray)
        yv2.extend(yarray)
        #plt.scatter(xarray,yarray)
    
    acounter =acounter +1
    if acounter > alen:
        break


plt.scatter(xv1, yv1)
plt.scatter(xv2, yv2)
plt.show()



    
