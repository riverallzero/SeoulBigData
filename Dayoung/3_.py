import geopandas as gpd
import matplotlib.pyplot as plt

seoul_ = gpd.read_file("Data/nlsp_021001001.shp")
seoul_.plot()
plt.show()