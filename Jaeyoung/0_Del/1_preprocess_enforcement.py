import pandas as pd
import os
import geopandas as gpd

def merge_enforcement(data_dir, output_dir):
    data = gpd.read_file("https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json", driver='GeoJSON')

    df = pd.read_csv(os.path.join(data_dir, "Data/불법_주정차_단속_실적.csv"), header=1) # 2017~2022 서울시 불법 주정차 단속 실적

    # total = df[df['자치구'] == '합계']
    df = df[df['자치구'] != '합계']

    # SIG_KOR_NM와 동일하도록 구 이름 변경
    # df['자치구'] = df['자치구'] + "구"
    df['자치구'] = df['자치구'].apply(lambda x: x + '구' if x != '중구' else x)

    df_merged = pd.merge(data, df, left_on='name', right_on= '자치구', how='inner')
    df_merged.to_csv(os.path.join(output_dir, "geo_불법_주정차_단속_실적.csv"), index=False)

    df.to_csv(os.path.join(output_dir, "Data/불법_주정차_단속_실적.csv"), index=False)

def main():
    data_dir = "../Data/"
    output_dir = "../Output/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    merge_enforcement(data_dir, output_dir)

if __name__ == '__main__':
    main()