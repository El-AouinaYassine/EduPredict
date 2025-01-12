import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

# def predict(X , w , b):
#     return X * w + b  
# def mtx_predict(X, W , b=0):
#     return np.matmul(X,W)

# def mtx_loss(X, Y , w , b):
#     return np.average((mtx_predict(X , w) - Y)**2)
# def loss(X, Y , w , b):
#     return np.average((predict(X, w , b) - Y)**2) 

# def gradient(X , Y , w ,b=0):
#     grad_w  =  2 * np.average(X * (predict(X,w,b)-Y) )
#     grad_b =  2 * np.average((predict(X,w,b)-Y) )
#     return grad_w ,grad_b
# def mtx_gradient(X, Y, w):
#     return 2 * np.matmul(X.T, (mtx_predict(X, w) - Y)) / X.shape[0]

def predict(X, w):
    return np.matmul(X, w)
def loss(X, Y, w):
    return np.average((predict(X, w) - Y) ** 2)
def gradient(X, Y, w):
    return 2 * np.matmul(X.T, (predict(X, w) - Y)) / X.shape[0]


def train(X , Y , iterations , lr=0.01 ):
    w = b = 0 
    tab = [];
    for i in range(iterations):
        tab.append(int(gradient(X,Y,w,0)))
        curr_loss = loss(X, Y, w ,b)
        # print("Iteration %4d => Loss: %.6f (b calue : %.6f)" % (i, curr_loss , b))
        if curr_loss > loss(X , Y , w+lr , b):
        # ila zdna +lr w kan loss jdid 7sn mn dyal db (sghr mno) 
            w+=lr # zid +lr l weigth
        elif curr_loss > loss(X , Y , w-lr , b):
        # ila n9sna -lr w kan loss jdid 7sn mn dyal db (sghr mno) 
            w-=lr #n9s -lr lweigth
        elif curr_loss > loss(X , Y , w, b+lr):
            b+=lr
        elif curr_loss > loss(X , Y , w, b-lr):
            b-=lr    
        else:
        # mor matsali zada wn9san wywli curr_loss mkytbdlsh return w
            return w , b ,tab
    raise Exception("Couldn't converge within %d iterations" % iterations)

def train_gradiant(X,Y,iterations , lr = 0.001 ):
    w = np.zeros((X.shape[1], 1))
    for i in range(iterations):
        print(f"iteration : {i}")
        print(f"lose:{mtx_loss(X,Y,w,0)}")
        w -= mtx_gradient(X,Y,w) * lr
    return w


sns.set();
plt.axis([0,100 , 0,100])
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("w" , fontsize=20)
plt.ylabel("l" , fontsize =20)


X1,X2,X3,Y = np.loadtxt("pizza_3_vars.txt" , skiprows=1 , unpack=True) #load data
X = np.column_stack((X1,X2,X3)) # shape data as a matrix
Y = Y.reshape(-1,1) # turn Y (1 dimensinal array) into matrix with (1,n)

w = train_gradiant(X , Y , 100 , 0.1)
x= np.linspace(0 , 10000)

plt.plot(X, Y , "bo")




sns.lineplot(y=Y, x=x)
plt.title(f"y = x")
plt.grid(True)
plt.show()

