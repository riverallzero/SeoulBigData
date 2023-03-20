import pandas as pd
import geopandas as gpd
import folium
import os

def main():
    result_dir = "Result/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # 역사_https://data.seoul.go.kr/dataList/OA-21232/S/1/datasetView.do
    # 정류장_https://www.data.go.kr/data/15099368/fileData.do?recommendDataYn=Y
    train_a = pd.read_csv("Data/서울시 역사마스터 정보.csv", encoding='cp949')
    train_g = pd.read_csv("Data/서울교통공사 지하철역 주소 및 전화번호 정보.csv", encoding='cp949')
    train_g = train_g[train_g['도로명주소'].str.contains('강서구')]

    bus = pd.read_csv("Data/서울시 정류장마스터 정보.csv", encoding='cp949')

    train = pd.merge(train_a, train_g, left_on='역사명', right_on='역명', how='inner')

    geo = gpd.read_file(
        ("https://raw.githubusercontent.com/vuski/admdongkor/master/ver20230101/HangJeongDong_ver20230101.geojson"),
        driver='GeoJSON')
    geo_gangseo = geo[geo['sggnm'] == '강서구']

    m = folium.Map([37.55, 126.84], tiles="OpenStreetMap", zoom_start=12)

    for idx, row in train.iterrows():
        folium.CircleMarker([row['경도'], row['위도']],  # 위도 경도
                            radius=2,  # 반지름
                            color='blue',  # 둘레 색상
                            fill=True, fill_color='green',  # 원 안 색상
                            fill_opacity=0.7,  # 투명도
                            popup='<pre>' + row['역사명'] + '</pre>').add_to(m)
    folium.GeoJson(geo_gangseo, name='json_data').add_to(m)
    m.save(os.path.join(result_dir, "Gangseogu_Train.html"))


if __name__ == '__main__':
    main()