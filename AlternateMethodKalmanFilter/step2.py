# STEP 2

# above but for our setting

#from https://arxiv.org/pdf/1204.0375.pdf
import numpy as np
import csv
#time step of mobile movement
dt = 0.1
v0 = 5.2

# obtain pos and v from data file frame1
initialcluster = 2

i=1

arrayx = []
arrayy =[]

# x with pos(0) and pos(1) and v(0) and v(1) at time k
# initial speed v is average speed
X = np.array([[0.0], [0.0], [v0], [v0]])

# state covariance of the previous step (k-1)
P = np.diag((0.01, 0.01, 0.01, 0.01))

dt = 0.2


# state transition model
A = np.array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])

B = np.diag((0.5*pow(dt, 2) , 0.5*pow(dt, 2), dt, dt))

# x-acceleration and y-acceleration  xa , ya
xa = 1
ya=1
U = np.diag((xa, ya, xa, ya))

# process noise covariance matrix Q
# draw sigma from standard deviation
# process noise wk ~ N(0, Q) equals
# Q = np.eye(x.shape() [0])
Q = np.array([[0.25*pow(dt,4), 0.25*pow(dt,4), 0.5*pow(dt,3), 0.5*pow(dt,3)], [0.25*pow(dt,4), 0.25*pow(dt,4), 0.5*pow(dt,3), 0.5*pow(dt,3)], [0.5*pow(dt,3), 0.5*pow(dt,3), pow(dt,2),pow(dt,2)], [0.5*pow(dt,3), 0.5*pow(dt,3), pow(dt,2),pow(dt,2)]])

# measurement matrices
#Y = np.array([[X[0,0]+abs(random.random()[0])], [X[1,0]+abs(random.random()[0])]])
#Y = array([[X[0,0] + abs(random.random())], [X[1,0] + abs(random.random())]])

Y = array([[1], [1]])


H = array([[1,0,0,0], [0,1,0,0]])

n_iter= len(setx)
# y_k is measurement at time k

# applying the kalman filter
for i in range(0, n_iter):
    (X, P) = kf_predict(X, P, A, Q, B, U)
    # use the measurement from the file to update Y; Y = x_i, y_i
    Y = array([[setx[i]], [sety[i]]])
    (X, P, K, IM, IS, LH) = kf_update(X, P, Y, H, R)

    Z = array([[X[0,0] + abs(random.random())], [X[1,0] + abs(random.random())]])
    plt.scatter(Z[0], Z[1])

plt.show()


