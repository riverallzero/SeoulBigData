import folium as folium
import pandas as pd
import geopandas as gpd
import os

def main():
    data_dir = "Data/"
    result_dir = "Result/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    df = pd.read_csv(os.path.join(data_dir, "Ganseogu_cafe_chain.csv"))

    geo = gpd.read_file(("https://raw.githubusercontent.com/vuski/admdongkor/master/ver20230101/HangJeongDong_ver20230101.geojson"), driver='GeoJSON')
    geo_gangseo = geo[geo['sggnm'] == '강서구']

    lat = df['longitude'].mean()
    long = df['latitude'].mean()

    cafe_name = df['업소명']
    chg_x = df['longitude']
    chg_y = df['latitude']

    m = folium.Map([lat, long], tiles="OpenStreetMap", zoom_start=12)


    for name, lat, lng in zip(cafe_name, chg_x, chg_y):
        folium.CircleMarker([lat, lng],  # 위도 경도
                            radius=5,  # 반지름
                            color='brown',  # 둘레 색상
                            fill=True, fill_color='coral',  # 원 안 색상
                            fill_opacity=0.7,  # 투명도
                            popup='<pre>' + name + '</pre>').add_to(m)

    folium.GeoJson(geo_gangseo, name='json_data').add_to(m)
    m.save(os.path.join(result_dir, "Gangseogu_Cafe.html"))

if __name__ == '__main__':
    main()