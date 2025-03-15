import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import OneHotEncoder
import pandas as pd 

def predict(X, w):
    return np.matmul(X, w) 
def loss(X, Y, w ):
    return np.average((predict(X, w ) - Y) ** 2)
def gradient(X, Y, w):
    m = X.shape[0]
    return (2 / m) * np.matmul(X.T, (predict(X, w) - Y))

def train_gradient(X, Y, iterations, lr):
    w = np.zeros((X.shape[1], 1))
    for i in range(iterations):
        prev_loss = loss(X, Y, w)
        print("Iteration %4d => Loss: %.2f" % (i, loss(X, Y, w)))
        w -= gradient(X, Y, w) * lr
        curr_loss = loss(X , Y ,w)
        if i > 0 and np.isclose(curr_loss, prev_loss, atol=1e-6):
            break
    return w




X1,X2,X3,X4,X5,X6,X7,X8,Y = np.loadtxt("fff.txt" , skiprows=1 , unpack=True) #load data
X = np.column_stack((np.ones(X1.size), X1,X2,X3,X4,X5,X6,X7,X8)) # shape data as a matrix +  we slipped a matrix of (1,n) (bias)
Y = Y.reshape(-1,1) # turn Y (1 dimensinal array) into matrix with (1,n)

w = train_gradient(X , Y , 1000000 , 0.001)

for i in range(10):
    p = predict(X[i] , w)
    v = Y[i]
    print("----------------------")
    print("prediction => %4d" % p)
    print("value      => %4d" % v)
    print("----------------------")


# Feature importance analysis
feature_importances = pd.DataFrame({
    'feature': X.columns,
    'performance_importance': model.feature_importances_[0],
    'satisfaction_importance': model.feature_importances_[1]
}).sort_values(by='performance_importance', ascending=False)

