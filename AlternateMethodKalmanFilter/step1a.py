# STEP 1 A
from numpy.linalg import inv

# from kalman filter

# prediction

def kf_predict(X, P, A, Q, B, U):
    X = np.dot(A, X) + np.dot(B, U)
    P = np.dot(A, np.dot(P, A.transpose())) + Q
    return (X, P)

def kf_update(X,P,Y,H,R):
    IM= np.dot(H,X)
    IS = R+ np.dot(H, np.dot(P, H.transpose()))
    K = np.dot(P, np.dot(H.transpose(), inv(IS)))
    X = X+ np.dot(K, (Y-IM))
    P= P - np.dot(K, np.dot(IS, K.transpose()))
    LH = gauss_pdf(Y, IM, IS)
    return (X, P, K, IM, IS, LH)


def gauss_pdf(X, M, S):
    if size(M)== 1:
        DX = X - np.tile(M, size(X))
        E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
        E = E + 0.5 * np.zeros(size(M)) * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    elif size(X) == 1:
        DX = tile(X, size(M))- M
        E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
        E = E + 0.5 * np.zeros(size(M))* log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    else:
        DX = X-M
        E = 0.5 * np.dot(DX.transpose(), np.dot(inv(S), DX))
        E = E + 0.5 * np.zeros((size(M, 1), size(M,1))) * log(2 * pi) + 0.5 * log(np.linalg.det(S))
        P = np.exp(-E)
    return (P[0],E[0]) 
