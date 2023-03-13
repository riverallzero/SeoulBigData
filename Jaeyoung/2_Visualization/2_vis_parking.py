import pandas as pd
import os
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap, MarkerCluster


def mapping_public_parking(output_dir, result_dir, geo_path):
    df = pd.read_csv(os.path.join(output_dir, "geo_서울시_공영주차장_안내_정보.csv"))
    count = df.groupby('주소').count()[['주차장명']].rename(columns = {'주차장명' : 'total'})
    count = pd.merge(df, count, left_on='name', right_on='주소', how='inner')

    df.dropna(axis=0, inplace=True)
    geo_path = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    m = folium.Map(
        location=[37.55, 126.84],
        zoom_start=10,
        tiles="CartoDB positron")
    folium.Choropleth(
        geo_data=geo_path,
        data=count,
        columns=["code", "total"],
        key_on="feature.properties.code",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.4,
        legend_name="주차장 수(개)"
    ).add_to(m)

    coords = df[['주차장 위치 좌표 위도', '주차장 위치 좌표 경도']]

    marker_cluster = MarkerCluster().add_to(m)

    for lat, long in zip(coords['주차장 위치 좌표 위도'], coords['주차장 위치 좌표 경도']):
        folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)

    m.save(os.path.join(result_dir, f"map_서울시_자치구별_공영주차장_현황.html"))

def mapping_gangseo_public_parking(output_dir, result_dir, geo_path):
    df = pd.read_csv(os.path.join(output_dir, "강서구_공영주차장_현황.csv"))
    m = folium.Map(
        location=[37.55, 126.84],
        zoom_start=10,
        tiles="CartoDB positron")

    folium.GeoJson(
        geo_path,
        name='code'
    ).add_to(m)

    coords = df[['주차장 위치 좌표 위도', '주차장 위치 좌표 경도']]

    # marker_cluster = MarkerCluster().add_to(m)
    #
    for lat, long in zip(coords['주차장 위치 좌표 위도'], coords['주차장 위치 좌표 경도']):
        # folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)
        folium.Marker([lat, long]).add_to(m)


    m.save(os.path.join(result_dir, f"map_강서구_공영주차장_현황.html"))

def draw_chart(output_dir, result_dir):
    df = pd.read_csv(os.path.join(output_dir, "주차장_확보율.csv"))
    # print(df.sort_values('2022_자동차등록대수 (대)', ascending=False)['자치구'].unique())
    # print(df.sort_values('2022.1_주차면수 (면수)', ascending=False)['자치구'].unique())
    # print(df.sort_values('2022.2_주차장확보율 (%)', ascending=False)['자치구'].unique())
    # df = df[(df['자치구'] == '강서구') | (df['자치구'] == '은평구') |
    #         (df['자치구'] == '') | (df['자치구'] == '마포구')]
    # df = df.transpose()
    # df = df.rename(columns=df.iloc[0])
    # df.drop('자치구', axis=0, inplace=True)

    # 연도별 상위 10위 자동차등록대수, 주차면수, 주차장확보율 차트
    selected_cols = [col for col in df.columns if "202" in col]
    selected_cols.append('자치구')
    df_selected = df[selected_cols]
    df_selected.set_index(df_selected['자치구'], inplace=True)

    plt.rcParams['font.family'] = 'NanumGothic'
    plt.figure(figsize=(20, 30))
    plt.xlabel('자치구')

    index_list = ['_자동차등록대수 (대)', '.1_주차면수 (면수)', '.2_주차장확보율 (%)']
    for index in index_list:
        for year in range(2020, 2023):
            df_year = df_selected[['자치구', f'{year}{index}']]
            sort = df_year.sort_values(f'{year}{index}', ascending=False).head(10)
            sort = sort.sort_values(f'{year}{index}')
            sort.plot(kind='barh', color='blue', alpha=0.5)
            plt.yticks(fontsize=12)
            title = index.split("_")[-1]
            plt.title(f'{title} - {year}')
            plt.savefig(os.path.join(result_dir, f"chart_{title}_{year}.png"))

    # 강서구 자동차등록대수와 주차장확보율 추이 차트
    # df_gangseo = df[(df['자치구'] == '강서구')]
    # count = [col for col in df_gangseo.columns if "자동차등록대수" in col]
    #
    # df_gangseo = df_gangseo.transpose()
    # df_gangseo = df_gangseo.rename(columns={15:'강서구'})
    # df_gangseo.drop('자치구', axis=0, inplace=True)
    # plt.bar(df_gangseo.index, df_gangseo)
    # plt.show()


    # index_list = ['_자동차등록대수 (대)', '.1_주차면수 (면수)', '.2_주차장확보율 (%)']
    #
    # plt.rcParams['font.family'] = 'NanumGothic'

    # for index in index_list:
    #     selected = df[df.index.str.contains(f'{index}')]
    #     selected.index = selected.index.str[0:4]
    #     selected.plot.bar(rot=0)
    #     plt.title(f'{index}')
    #     plt.show()
    # for year in range(2020, 2023):
    #     for index in index_list:
    #         selected = df[df.index.str.contains(f'{index}')]
    #         sorted = selected.sort_values(f'{year}_자동차등록대수 (대)', ascending=False)
    #         print(sorted)

def main():
    output_dir = "../Output/"
    result_dir = "../Result/parking"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    geo_path = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
    mapping_public_parking(output_dir, result_dir, geo_path)
    draw_chart(output_dir, result_dir)
    mapping_gangseo_public_parking(output_dir, result_dir, geo_path)

if __name__ == '__main__':
    main()