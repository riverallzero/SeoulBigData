import os
import pandas as pd
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

def parking_lot_rate(data_dir, output_dir, data):
    df = pd.read_csv(os.path.join(data_dir, "주차장_확보율.csv"))
    col = df.columns
    row1 = df.iloc[0].to_list()
    df.columns = [col[i] + "_" + row1[i] for i in range(len(col))]
    df.drop(0, axis=0, inplace=True)
    df.drop('자치구별(1)_자치구별(1)', axis=1, inplace=True)
    df.rename(columns = {'자치구별(2)_자치구별(2)' : '자치구'}, inplace = True)

    df = df[df['자치구'] != '소계']

    df_merged = pd.merge(data, df, left_on='name', right_on='자치구', how='inner')

    df_merged.to_csv(os.path.join(output_dir, "geo_주차장_확보율.csv"), index=False)
    df.to_csv(os.path.join(output_dir, "주차장_확보율.csv"), index=False)

def public_parking(data_dir, output_dir, data):
    df = pd.read_csv(os.path.join(data_dir, "서울시 공영주차장 안내 정보.csv"), encoding='cp949')
    df = df.drop_duplicates(['주차장코드'], keep='first')
    df['주소'] = df['주소'].str.split(" ").str[0]
    df = df[['주차장명', '주소', '주차장 종류', '운영구분명', '총 주자면', '주차장 위치 좌표 위도', '주차장 위치 좌표 경도']]

    df_merged = pd.merge(data, df, left_on='name', right_on='주소', how='inner')
    df_merged.to_csv(os.path.join(output_dir, "geo_서울시_공영주차장_안내_정보.csv"), index=False)
    df.to_csv(os.path.join(output_dir, "서울시_공영주차장_안내_정보.csv"), index=False)

def gangseo_parking(data_dir, output_dir):
    # geo_path = "https://raw.githubusercontent.com/vuski/admdongkor/master/ver20230101/HangJeongDong_ver20230101.geojson"


    df_seoul = pd.read_csv(os.path.join(data_dir, "서울시 공영주차장 안내 정보.csv"), encoding='cp949')
    df_seoul = df_seoul.drop_duplicates(['주차장코드'], keep='first')
    df_seoul['자치구'] = df_seoul['주소'].str.split(" ").str[0]
    df_cor = df_seoul[df_seoul['자치구'] == '강서구']

    df_gangseo = pd.read_csv(os.path.join(data_dir, "강서구시설관리공단_공영주차장_현황.csv"), encoding='cp949')

    # 주차장명
    gangseo_parking_name = df_gangseo['주차장명'].to_list()

    selected = []
    for name in gangseo_parking_name:
        select = df_cor[df_cor['주차장명'].str.contains(name)]
        selected.append(select)

    df_selected = pd.concat(selected)

    df_selected.to_csv(os.path.join(output_dir, "강서구_공영주차장_현황.csv"), index=False)







def main():
    data_dir = "../Data/"
    output_dir = "../Output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = gpd.read_file(
        "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json",
        driver='GeoJSON')

    parking_lot_rate(data_dir, output_dir, data)
    public_parking(data_dir, output_dir, data)
    gangseo_parking(data_dir, output_dir)

if __name__ == '__main__':
    main()