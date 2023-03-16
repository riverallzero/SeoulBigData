import os
import re
import pandas as pd
import geopandas as gpd


def main():
    data_dir = "../../Data/Gangseo_250m"
    output_dir = "../Output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # df1 = pd.read_csv(os.path.join(data_dir, "Gangseo_250m_4326.csv"))
    # df2 = pd.read_csv(os.path.join(data_dir, "Gangseo_Economically_250m_4326.csv"))

    file_list = [x for x in os.listdir(data_dir) if x.endswith(".csv")]
    file_list.remove("Gangseo_Economically_250m_4326.csv")
    df_merged = pd.read_csv(os.path.join(data_dir, "Gangseo_Economically_250m_4326.csv"))
    for file in file_list:
        each = pd.read_csv(os.path.join(data_dir, file)).drop(['위도', '경도'], axis=1)
        df_merged = pd.merge(df_merged, each, on='gid', how='outer')
    df_merged.to_csv(os.path.join(output_dir, "Gangseo_250m.csv"),index=False)
    print(df_merged)
if __name__ == '__main__':
    main()