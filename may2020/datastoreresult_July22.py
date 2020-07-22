result=[]
result.append(initialcluster)
iframe = initialframe
currentcluster = initialcluster
t =True
while t:
    nextres = findnextclusterapp(iframe, currentcluster)
    if str(nextres) == "nan":
        break
    if iframe >= endframe:
        break
    result.append(nextres)
    iframe = iframe+1
    currentcluster = nextres
