import pandas as pd
import geopandas as gpd
import os

def main():
    data_dir = "C:\code\Seoul_bigdata\Jaeyoung\Data\Gangseo_250m\Gangseo_ConstructureCount_250m\Gangseo_CounstructureCount_250m.shp"
    data = gpd.read_file(data_dir)
    print(data.columns)

if __name__ == '__main__':
    main()