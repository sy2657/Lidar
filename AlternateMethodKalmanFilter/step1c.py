# STEP 1 c

# determine the measurements from a trajectory

# given the trajnum
#124
tnum = 153

import math
import csv

trajnum = 0
obnum = 1

irow =0

setx =[]
sety =[]

with open(tfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        irow=irow+1
        if line_count==0:
            line_count=line_count+1
            continue
        if line_count==1:
            line_count=line_count+1
            prevrow = row
            prevx = float(prevrow[6])
            prevy = float(prevrow[7])
            pos0 = [prevx, prevy]
            # change floor to round
            #pfx = round(prevx)
            #pfy = round(prevy)
            pts = float(prevrow[2])*0.000001
            continue
        vehped = row[1]
        if vehped ==2:
            continue
        trajnum= float(row[0])
        currx = float(row[6])
        curry = float(row[7])
        if trajnum != tnum:
            continue
        setx.append(currx)
        sety.append(curry)

plt.scatter(setx, sety)

plt.show()
