import pandas as pd
import plotly.express as px
from sklearn import decomposition

penguins_df = pd.read_csv('data/penguins.csv')

X = penguins_df.loc[:, ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
y = penguins_df.loc[:,'species']

pca = decomposition.PCA(n_components=3)
pca.fit(X)
principal_comps = pca.transform(X)

fig = px.scatter_3d(principal_comps, x=0, y=1, z=2, color=y, opacity=0.7)

fig.show()
