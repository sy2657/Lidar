# include into the traj file read code

tfile =  "2019-9-10-12-0-0-BF1-CL1-Traj(0-18000frames).csv"

import math
import csv

trajnum = 0 
obnum = 1

irow =0

outlier =0

# different lists holding angles
q1angles = []
q2angles= []
q3angles =[]
q4angles =[]
quadrant1 = [] # holding from points 
quadrant2 = []
quadrant3 = []
quadrant4 = []

with open(tfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        irow=irow+1
        trajnum = row[0]
        frameindex = row[17]
        #print("frame:",frameindex)
        if line_count==0:
            line_count=line_count+1
            continue
        if line_count==1:
            line_count=line_count+1
            prevrow = row
            prevx = float(prevrow[6])
            prevy = float(prevrow[7])
            print(prevx)
            print(prevy)
            # use round instead of floor
            pfx = round(prevx)
            pfy = round(prevy)
            continue
        currentx = float(row[6])
        currenty = float(row[7])
        fx = round(currentx)
        fy = round(currenty)
        if pfx ==fx and pfy==fy:
            #i = dinvlookupdict[(pfx, pfy)]
            #altertrajcount[i] = altertrajcount[i]+1 # altertraj holds counts of one cell to same cell 
            prevframe= frameindex
            line_count = line_count+1
        if obnum != trajnum:
            pfx = fx
            pfy = fy
            obnum = trajnum
            prevframe = frameindex
            line_count = line_count+1
            continue
        # save to map
        fromi = dinvlookupdict[(pfx,pfy)]
        toi = dinvlookupdict[(fx,fy)]
        # angle calculation 
        xdiff = fx - pfx
        ydiff = fy - pfy
        rad = math.atan2(ydiff, xdiff)
        ang = math.degrees(rad)
        if ang <0:
          ang = 360+ang
        # find the quadrant where fromi belongs 
        if pfx <0:
          if pfy <0:
            q1angles.append(ang)
            quadrant1.append(fromi)
          if pfy>0:
            q2angles.append(ang)
            quadrant2.append(fromi)
        if pfx >0:
          if pfy<0:
            q3angles.append(ang)
            quadrant3.append(fromi)
          if pfy>0:
            q4angles.append(ang)
            quadrant4.append(fromi)

        # compare angles

        mcount = dtrajcount[(fromi, toi)]
        if mcount>5000:
            print("fromi:", fromi, " toi:", toi)
        dtrajcount[(fromi, toi)]= mcount+1
        pfx = fx
        pfy = fy
        prevframe= frameindex
        line_count = line_count+1
        
# process angles
#https://www.gakhov.com/articles/find-outliers-in-an-array.html

# remove / note outliers
outliers1 = {}
outliers2 = {}
outliers3 = {}
outliers4 = {}

i1 = get_indices_of_outliers(q1angles)
i2 = get_indices_of_outliers(q2angles)
i3 = get_indices_of_outliers(q3angles)
i4 = get_indices_of_outliers(q4angles)

# subset out 

#a = a[:index] + a[index+1:]

# reverse indices

'''
l = [0,1,2,3,4,5,6,7,8,9]
>>> indices=[3,7]
>>> for i in sorted(indices, reverse=True):
...     del l[i]
'''
for ind in sorted(i1, reverse=True):
  # add to dictionary for outliers 
  qf = quadrant1[ind]
  oval = outliers1.get(qf)
  if oval != None:
    ovec = outliers1[qf]
    ovec1 = ovec.append(q1angles[ind])
    outliers1[qf] = ovec1
  else:
    outliers1[qf] = [q1angles[ind]]
  del q1angles[ind]

for ind in sorted(i2, reverse=True):
  # add to dictionary for outliers 
  qf = quadrant2[ind]
  oval = outliers2.get(qf)
  if oval != None:
    ovec = outliers2[qf]
    ovec1 = ovec.append(q2angles[ind])
    outliers2[qf] = ovec1
  else:
    outliers2[qf] = [q2angles[ind]]
  del q2angles[ind]

for ind in sorted(i3, reverse=True):
  # add to dictionary for outliers 
  qf = quadrant3[ind]
  oval = outliers3.get(qf)
  if oval != None:
    ovec = outliers3[qf]
    ovec1 = ovec.append(q3angles[ind])
    outliers3[qf] = ovec1
  else:
    outliers3[qf] = [q3angles[ind]]
  del q3angles[ind]

for ind in sorted(i4, reverse=True):
  # add to dictionary for outliers 
  qf = quadrant4[ind]
  oval = outliers4.get(qf)
  if oval != None:
    ovec = outliers4[qf]
    ovec1 = ovec.append(q4angles[ind])
    outliers4[qf] = ovec1
  else:
    outliers4[qf] = [q4angles[ind]]
  del q4angles[ind]
# average angle
ave_ang1 = np.mean(q1angles)
ave_ang2 = np.mean(q2angles)
ave_ang3 = np.mean(q3angles)
ave_ang4 = np.mean(q4angles)
# use this in hybrid method
