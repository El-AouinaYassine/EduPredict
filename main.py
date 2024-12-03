import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
def getW(path):
    y , x = np.loadtxt(path , skiprows=1 , unpack = True)
    
    y= np.array(y)
    x= np.array(x)

    all = y/x
    res = 0 
    for item in all :
        res += item
    return res

def predict(res , w):
    return res * w 

def loss(X, Y , w):
    return np.average(predict(X, w) - Y)**2

def train(X , Y , iterations , lr=0.01):
    w = 0 
    for i in range(iterations):
        curr_loss = loss(X, Y, w)
        print("Iteration %4d => Loss: %.6f" % (i, curr_loss))
        if curr_loss > loss(X , Y , w+lr):
            w+=lr
        elif curr_loss > loss(X , Y , w-lr):
            w-=lr
        else:
            return w
    raise Exception("Couldn't converge within %d iterations" % iterations)

  



sns.set();
plt.axis([0,100 , 0,100])
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("Reservations" , fontsize=20)
plt.ylabel("Pizzas" , fontsize =20)
X,Y = np.loadtxt("pizza.txt" , skiprows = 1, unpack =True)
plt.plot(X , Y , "bo")
plt.plot(X , Y , "bo")
    
# the reg line
x= np.linspace(0 , 10000)
w = train(X , Y , 100000 , 0.01)
y=x * getW("pizza.txt")
sns.lineplot(y=y, x=x)
plt.title(f"y = x")

# print(predict(20, 2))
plt.show()