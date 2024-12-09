import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

# getW() function bash kan3rfo l Weigth (w li kat controlli line )
# n7awlo l9aw shnahwa a7san line li ykon 9rib ma 2amkan lga3 lpoints

def predict(res , w , b):
    # 3dna y = x*w
    # res = x dans ce cas la => y =res * w
    # 
    return res * w + b  

def loss(X, Y , w , b):
    return np.average((predict(X, w , b) - Y)**2)

def train(X , Y , iterations , lr=0.01):
    w = b = 0 
    for i in range(iterations):
        curr_loss = loss(X, Y, w ,b)
        print("Iteration %4d => Loss: %.6f (b calue : %.6f)" % (i, curr_loss , b))
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
            return w , b
    raise Exception("Couldn't converge within %d iterations" % iterations)

sns.set();
plt.axis([0,100 , 0,100])
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("Reservations" , fontsize=20)
plt.ylabel("Pizzas" , fontsize =20)
# skiprows => n9z str dyal lktaba li fih "reservation pizza"
X,Y = np.loadtxt("score.txt" , skiprows = 1, unpack =True)
plt.plot(X , Y , "bo")
# plt.plot(X , Y , "bo")
    
# the reg linewlahila malk 

x= np.linspace(0 , 10000)
w , b= train(X , Y , 1000000 , 0.01)
y=x * w + b
sns.lineplot(y=y, x=x)
plt.title(f"y = x")


# wv = predict(15 , w.12269999985915,b )
print(f"wieght => {w}")

# print(predict(20, 2))
plt.grid(True)
plt.show()