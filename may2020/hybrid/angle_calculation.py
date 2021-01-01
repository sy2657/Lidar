# calculate angle differences

p384 = [1.87133215, 33.336261538]
# 385 and 386
p385 = [-3.33425679, 33.9082716]
p386 = [ -5.216461842, 7.102238157894]

xdiff1 = p385[0] - p384[0]
ydiff1 = p385[1] - p384[1]

xdiff2 = p386[0] - p385[0]
ydiff2 = p386[1] - p385[1]

r1 =math.atan2(ydiff1, xdiff1)

math.degrees(r1)

r2 = math.atan2(ydiff2, xdiff2)
math.degrees(r2)

# if negative, convert to positive 
360 - 94

# abs value of difference
266- 173.7
