import folium as folium
import pandas as pd
import geopandas as gpd
import os

def main():
    data_dir = "Data/"
    result_dir = "Result/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    df = pd.read_csv(os.path.join(data_dir, "서울시_강서구_카페현황_202212.csv"))

    geo = gpd.read_file(
        ("https://raw.githubusercontent.com/vuski/admdongkor/master/ver20230101/HangJeongDong_ver20230101.geojson"),
        driver='GeoJSON')
    geo_gangseo = geo[geo['sggnm'] == '강서구']

    drop_con = "엔제리너스|투썸플레이스|스타벅스|더벤티|폴바셋"
    df['color'] = 'blue'
    df.loc[df['상호명'].str.contains(drop_con), 'color'] = 'coral'

    lat = df['위도'].mean()
    long = df['경도'].mean()

    m = folium.Map([lat, long], tiles="OpenStreetMap", zoom_start=12)
    for idx, row in df.iterrows():
        folium.CircleMarker([row['위도'], row['경도']],  # 위도 경도
                            radius=2,  # 반지름
                            color=row['color'],  # 둘레 색상
                            fill=True, fill_color=row['color'],  # 원 안 색상
                            fill_opacity=0.7,  # 투명도
                            popup='<pre>' + row['상호명'] + '</pre>').add_to(m)
    folium.GeoJson(geo_gangseo, name='json_data').add_to(m)
    m.save(os.path.join(result_dir, "Gangseogu_Cafe.html"))

if __name__ == '__main__':
    main()