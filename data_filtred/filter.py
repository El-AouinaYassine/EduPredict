import numpy as np 
import pandas as pd
data = pd.read_csv(
    'catData.csv',
    delimiter=',',
    quotechar='"',
    skipinitialspace=True, 
    engine='python',       
    )
data.columns = data.columns.str.strip()

def convert_cat(col , merged):
    dummie = pd.get_dummies(data[col])
    dummie = dummie.astype(int)
    merged  = pd.concat([data,dummie] , axis='columns')
    merged.drop([col] , axis='columns' , inplace=True)

convert_cat('Ville' ,  data)
# print(data["Age"])
# np_data = data.to_numpy()

def show_data():
    col_names = (data.columns).to_numpy()
    i = 0
    for item in np_data:
        i+=1
        print("\033[31mitem(%d):\033[0m" % i)
        j=0
        for col_val in item:
            print("\033[32m\t(%s):\033[34m{%s} \033[0m\033[0m"%(col_names[j] , col_val))
            j+=1
# show_data()