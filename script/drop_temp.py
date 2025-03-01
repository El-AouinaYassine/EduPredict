import pandas as pd

df = pd.read_csv('./script/data/basedData.csv')

# newDf = df.drop('Timestamp')
newDf = df.drop('Quelle est votre filière d cette specialite ?')

newDf.to_csv(newBasedData, index=False)
