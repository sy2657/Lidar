# plot other clusters
array1 = [1, 1.0, 1.0, 1.0, 1.0, 2.0, 4.0, 5.0, 0, 0, 0]
array2 = [1, 1.0, 1.0, 1.0, 1.0]

alen = len(array1)
xv1=[]
yv1=[]

ax =[]
ay =[]

acounter=0
for i in range(initialframe, initialframe+alen):
    name = "file_out"
    name = name+str(i)
    name = name+".csv"
    
    
    a = array1[acounter]
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
                #xmissed.append(xpoint)
                #ymissed.append(ypoint)
                
                
        # plot
        #xv1.extend(xarray)
        #yv1.extend(yarray)
        
        
        plt.scatter(xarray,yarray)
        avx = np.mean(xarray)
        avy = np.mean(yarray)
        
        print("i is", i)
        print("av coord are", avx, avy)
        
        plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
        
        ax.append(avx)
        ay.append(avy)
    
    acounter =acounter +1
    if acounter > alen:
        break

#plt.scatter(xv1, yv1)
#plt.scatter(xv2, yv2)
plt.show()
