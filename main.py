import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

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
y=x*w
sns.lineplot(x=x , y=y)
plt.title(f"y = x")
plt.xlabel("x")
plt.ylabel("y")

def predict():
    print('workig');
plt.show()