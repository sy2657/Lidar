# STEP 1 B
# from the sample code

import numpy as np
from numpy import *
from numpy.linalg import inv

import matplotlib.pyplot as plt

dt = 0.1

X = array(([[0.0], [0.0], [0.1], [0.1]]))
P = diag((0.01, 0.01, 0.01, 0.01))

A = array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])

Q = np.eye(4)

B = np.eye(4)

U = np.zeros(4)

# meas matrices
Y = array([[X[0,0] + abs(random.random())], [X[1,0] + abs(random.random())]])

H = array([[1,0,0,0], [0,1,0,0]])

R = eye(2)

n_iter = 50

# applying the kalman filter
for i in range(0, n_iter):
    (X, P) = kf_predict(X, P, A, Q, B, U)
    (X, P, K, IM, IS, LH) = kf_update(X, P, Y, H, R)
    Y = array([[X[0,0] + abs(random.random())], [X[1,0] + abs(random.random())]])
    plt.scatter(Y[0], Y[1])

plt.show()


