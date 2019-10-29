# STEP 4 B

# above function with timestamp check 
    
# for row_i , look ahead rows until 0.1 or 0.2 sec reached 

import math
import csv

trajnum = 0 
obnum = 1

irow =0

outlier =0

settimestamp={0}
setx ={0}
sety ={0}

settimestamp.clear()
setx.clear()
sety.clear()

# change settimestamp to a normal array

with open(tfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        irow=irow+1
        trajnum = row[0]
        frameindex = row[17]
        # load current info
        currx =float(row[6])
        curry =float(row[7])
        fx = math.floor(currx)
        fy = math.floor(curry)
        timestamp = float(row[2])
        # compare current + previous timestamps 
        ts = timestamp*0.000001
        pts = prevtimestamp*0.000001
        diff = ts - pts 
        
        # first check if in the same trajectory
        if obnum != trajnum:
            pfx = fx
            pfy= fy
            obnum = trajnum
            prevtrajnum = trajnum
            prevframe=frameindex
            prevtimestamp = timestamp
            continue
        #print("frame:",frameindex)
        if line_count==0:
            line_count=line_count+1
            continue
        if line_count==1:
            line_count=line_count+1
            prevrow = row
            prevx = float(prevrow[6])
            prevy = float(prevrow[7])
            pfx = math.floor(prevx)
            pfy = math.floor(prevy)
            prevtimestamp = float(prevrow[2])
            continue
        
        # test the diff in set 
        if !settimestamp.isEmpty():
            setlen = len(settimestamp)
            for i in range(0, setlen):
                sts1 = settimestamp[i]
                pfx1 = setx[i]
                pfy1 = sety[i]
                ts1 = sts1*0.000001
                pts1 = prevtimestamp*0.000001
                diff1 = ts1 - pts1
            # if current distance greater than 0.15, discard
                if diff1 > 0.15:
                    settimestamp.remove(sts1)
                    # also remove from setx and sety
                    setx.remove()
                    continue
                if diff1< 0.05:
                    continue
                # if falls within 0.05 to 0.15 
                pfx1 = setx[i]
                pfy1 = sety[i]
                # add to the trajectory 
        # higher than 0.15
        if diff > 0.15:
            # set previous values
            pfx = fx
            pfy = fy
            prevtimestamp = timestamp
            # clear the sets?
            continue
        # lower than 0.05
        if diff < 0.05: 
            # add to sets 
            #prevtimestamp stays the same 
            # pfx and pfy stay the same 
            settimestamp.add(prevtimestamp)
            prevtimestamp =timestamp
            setx.add(pfx)
            pfx =fx
            sety.add(pfy)
            pfy = fy
        # if falls within 0.05 to 0.15 
        print('current timestamp:',ts)
        if pfx==fx and pfy==fy:
            prevframe=frameindex
            prevtimestamp = timestamp
            continue
        
        # now save to the map(i,j)
        
        fromi = invlookupdict[(pfx,pfy)]
        #topt = []
        toi = invlookupdict[(fx,fy)]
        #print("row",irow)
        mcount = trajcount1[(fromi,toi)]
        trajcount1[(fromi, toi)] = mcount+1
        # set previous
        pfx = fx
        pfy = fy
        prevframe = frameindex
        prevtrajnum= trajnum
        prevtimestamp = timestamp 
        
        # condition break
        if irow == 5:
            break
            
