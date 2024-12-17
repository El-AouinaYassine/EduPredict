import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

# getW() function bash kan3rfo l Weigth (w li kat controlli line )
# n7awlo l9aw shnahwa a7san line li ykon 9rib ma 2amkan lga3 lpoints

def predict(res , w , b):
    # 3dna y = x*w
    # res = x dans ce cas la => y =res * w
    # 
    return res * w + b  

def loss(X, Y , w , b):
    return np.average((predict(X, w , b) - Y)**2) 

def gradient(X , Y , w ,b=0):
    grad_w  =  2 * np.average(X * (predict(X,w,b)-Y) )
    grad_b =  2 * np.average((predict(X,w,b)-Y) )
    return grad_w ,grad_b

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

def train_gradiant(X,Y,iterations , lr = 0.001 , tabX=[] , tabY=[] , tabZ=[]):
    w = 0
    b=0
    for i in range(iterations):
        tabX.append((w))
        tabY.append((w))
        tabZ.append((loss(X, Y ,w ,0)))
        print(f"iteration : {iterations}")
        print(f"w:{w}")
        w_gradient, b_gradient = gradient(X, Y, w, b)
        w -= w_gradient * lr
        b -= b_gradient * lr
    return (w , b , tabX , tabY , tabZ)

def predict_upgraded(X ,W, b):
    return np.matmul(X , W)
def loss(X,w):
    return np.average( (predict_upgraded(X,w,0)-Y) ** 2)
sns.set();
plt.axis([0,100 , 0,100])
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("w" , fontsize=20)
plt.ylabel("l" , fontsize =20)
# skiprows => n9z str dyal lktaba li fih "reservation pizza"
# X,Y = np.loadtxt("score.txt" , skiprows = 1, unpack =True)

X1,X2,X3,Y = np.loadtxt("pizza_3_vars.txt" , skiprows=1 , unpack=True)
X = np.column_stack((X1,X2,X3))
print(Y)
Y = Y.reshape(-1,1)
print(Y)

# plt.plot(X , Y , "bo")
    
# the reg linewlahila malk 

x= np.linspace(0 , 10000)
tab = []
# w , b,tab= train(X , Y , 1000000 , 0.01)
# w = 1;
# b=0;
# w , b , tabx , taby , tabz = train_gradiant(X,Y,1000);

plt.plot(X, Y , "bo")
# y=x * w + b
sns.lineplot(y=y, x=x)
plt.title(f"y = x")

plt.grid(True)
# plt.show()

