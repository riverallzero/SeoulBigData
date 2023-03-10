import os
import pandas as pd
import geopandas as gpd

def parking_lot_rate(data_dir, output_dir):
    data = gpd.read_file(
        "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json",
        driver='GeoJSON')

    df = pd.read_csv(os.path.join(data_dir, "주차장_확보율.csv"))
    col = df.columns
    row1 = df.iloc[0].to_list()
    df.columns = [col[i] + "_" + row1[i] for i in range(len(col))]
    df.drop(0, axis=0, inplace=True)
    df.drop('자치구별(1)_자치구별(1)', axis=1, inplace=True)
    df.rename(columns = {'자치구별(2)_자치구별(2)' : '자치구'}, inplace = True)

    df = df[df['자치구'] != '소계']

    df_merged = pd.merge(data, df, left_on='name', right_on= '자치구', how='inner')

    df_merged.to_csv(os.path.join(output_dir, "geo_주차장_확보율.csv"), index=False)
    df.to_csv(os.path.join(output_dir, "주차장_확보율.csv"), index=False)


def main():
    data_dir = "../Data/"
    output_dir = "../Output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    parking_lot_rate(data_dir, output_dir)

if __name__ == '__main__':
    main()