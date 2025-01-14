import numpy as np 
import pandas as pd
data = pd.read_csv(
    'DATASET.csv',
    delimiter=',',
    quotechar='"',
    skipinitialspace=True,  # Skip spaces after delimiters
    engine='python',       
    )
np_data = data.to_numpy()
col_names = (data.columns).to_numpy()
i = 0
for item in np_data:
    i+=1
    print("\033[31mitem(%d):\033[0m" % i)
    j=0
    for col_val in item:
        print("\033[32m\t(%s):\033[34m{%s} \033[0m\033[0m"%(col_names[j] , col_val))
        j+=1