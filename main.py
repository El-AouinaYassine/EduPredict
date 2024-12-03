import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

# getW() function bash kan3rfo l Weigth (w li kat controlli line )
# n7awlo l9aw shnahwa a7san line li ykon 9rib ma 2amkan lga3 lpoints
def getW(path):
    # y et x sonts des List 
    y , x = np.loadtxt(path , skiprows=1 , unpack = True)
    # anredohom np.array bash n9ro ndiro x/y sinon ay3tina expection
    y= np.array(y)
    x= np.array(x)

    all = y/x # all at5rjlk array , ex : [1.2 , 0.23 , 012]
    res = 0 
    for item in all :
        res += item
    return res

def predict(res , w):
    # 3dna y = x*w
    # res = x dans ce cas la => y =res * w
    # 
    return res * w 

def loss(X, Y , w):
    return np.average(predict(X, w) - Y)**2

def train(X , Y , iterations , lr=0.01):
    w = 0 
    for i in range(iterations):
        curr_loss = loss(X, Y, w)
        print("Iteration %4d => Loss: %.6f" % (i, curr_loss))
        if curr_loss > loss(X , Y , w+lr):
        # ila zdna +lr w kan loss jdid 7sn mn dyal db (sghr mno) 
            w+=lr # zid +lr l weigth
        elif curr_loss > loss(X , Y , w-lr):
        # ila n9sna -lr w kan loss jdid 7sn mn dyal db (sghr mno) 
            w-=lr #n9s -lr lweigth
        else:
        # mor matsali zada wn9san wywli curr_loss mkytbdlsh return w
            return w 
    raise Exception("Couldn't converge within %d iterations" % iterations)

  



sns.set();
plt.axis([0,100 , 0,100])
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("Reservations" , fontsize=20)
plt.ylabel("Pizzas" , fontsize =20)
# skiprows => n9z str dyal lktaba li fih "reservation pizza"
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