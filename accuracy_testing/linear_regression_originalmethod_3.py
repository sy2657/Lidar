# calculate MSE and r2 and plot

# step 6

# regression on xlargest, xsmallest, ylargest, ysmallest

# check if the vehicle stays in place
 
xlargest_x = array(xlargest_x)
xlargest_y = array(xlargest_y)

a_xlargestx =xlargest_x.reshape(xlargest_x.shape[0],1)

lr = LinearRegression()
lr.fit(a_xlargestx, xlargest_y)

#print(lr.score(a_xlargestx, xlargest_y))


ay_pred = lr.predict(a_xlargestx)

print("xlargest MSE:",mean_squared_error(xlargest_y, ay_pred))

print("xlargest r2:",r2_score(xlargest_y, ay_pred))


plt.scatter(xlargest_x, xlargest_y)
plt.plot(xlargest_x, ay_pred, color='blue', linewidth=3)

# xsmallest 
axsmallest_x = array(xsmallest_x)
axsmallest_y = array(xsmallest_y)
a_xsmallestx = axsmallest_x.reshape(axsmallest_x.shape[0], 1)

lr2 = LinearRegression()
lr2.fit(a_xsmallestx, axsmallest_y)

pred2 = lr2.predict(a_xsmallestx)

print("xsmallest MSE:",mean_squared_error(axsmallest_y, pred2))

print("xsmallest r2:",r2_score(axsmallest_y, pred2))


plt.scatter(xsmallest_x, xsmallest_y)
plt.plot(xsmallest_x, pred2, color='red', linewidth=3)

# ylargest

aylargest_x = array(ylargest_x)
aylargest_y = array(ylargest_y)

a_ylargestx = aylargest_x.reshape(aylargest_x.shape[0], 1)

lr3 = LinearRegression()
lr3.fit(a_ylargestx, aylargest_y)

pred3 = lr3.predict(a_ylargestx)

print("ylargest MSE:",mean_squared_error(aylargest_y, pred3))

print("ylargest r2:",r2_score(aylargest_y, pred3))

plt.scatter(ylargest_x, ylargest_y)
plt.plot(ylargest_x, pred3, color='green', linewidth=3)


# ysmallest 
aysmallest_x = array(ysmallest_x)
aysmallest_y = array(ysmallest_y)

a_ysmallestx = aysmallest_x.reshape(aysmallest_x.shape[0], 1)
lr4 = LinearRegression()

lr4.fit(a_ysmallestx, aysmallest_y)

pred4 = lr4.predict(a_ysmallestx)

print("ysmallest MSE:",mean_squared_error(aysmallest_y, pred4))

print("ysmallest r2:",r2_score(aysmallest_y, pred4))

plt.scatter(ysmallest_x, ysmallest_y)
plt.plot(ysmallest_x, pred4, color='purple', linewidth=3)

plt.show()
