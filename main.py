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

# plt.xlabel("x")
# plt.ylabel("y")



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
w = 2
y=x * getW("pizza.txt")
sns.lineplot(y=y, x=x)
plt.title(f"y = x")

# print(predict(20, 2))
plt.show()