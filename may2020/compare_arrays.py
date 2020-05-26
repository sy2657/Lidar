# compare the two arrays 
numincorrect = 0

# lengths 
len1 = len(result)
len2 = len(listclusterids)

setlen = len1

if len1 < len2:
    setlen = len1
if len2 < len1:
    setlen = len2

for i in range(0, setlen):
    if result[i] != listclusterids[i]:
        numincorrect = numincorrect+1
