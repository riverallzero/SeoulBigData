import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from matplotlib import pyplot as plt


def mapping(output_dir, result_dir):

    df = pd.read_csv(os.path.join(output_dir, "geo_불법_주정차_단속_실적.csv"))
    geo_path = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    for year in range(2017, 2023):
        m = folium.Map(
            location=[37.55, 126.84],
            zoom_start=12,
            tiles="CartoDB positron")

        folium.Choropleth(
            geo_data=geo_path,
            data=df,
            columns=["code", f"{year}"],
            key_on="feature.properties.code",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.4,
            legend_name="신고건수 "
        ).add_to(m)

        HeatMap(df[["code", f"{year}"]]).add_to(folium.FeatureGroup(name="Heat map").add_to(m))
        folium.LayerControl().add_to(m)

        m.save(os.path.join(result_dir, f"enforcement_map_{year}.html"))

def draw_chart(output_dir, result_dir):

    df = pd.read_csv(os.path.join(output_dir, "불법_주정차_단속_실적.csv"))
    df.set_index(df['자치구'], inplace=True)

    plt.rcParams['font.family'] = 'NanumGothic'
    plt.figure(figsize=(20, 30))
    plt.ylabel('자치구')
    plt.xlabel('불법 주정차 단속 실적(건)')

    for year in range(2017, 2023):
        df_year = df[['자치구', f'{year}']]
        sort = df_year.sort_values(f'{year}').head(10)
        sort = sort.sort_values(f'{year}')
        sort.plot(kind='barh', color='blue', alpha=0.5)
        plt.yticks(fontsize=12)
        plt.title(f'서울시 자치구별 불법 주정차 단속 실적 - {year}')
        plt.savefig(os.path.join(result_dir, f"chart_enforcement_{year}.png"))


    plt.rcParams['figure.figsize'] = [30, 30]
    plt.suptitle('서울시 자치구별 2020 - 2022 불법 주정차 단속 실적')
    # max_val = np.ceil(max(df['2021']))

    for i, year in enumerate([2020, 2021, 2022]):
        sorted =  df.sort_values(f'{year}', ascending=False).head(5)
        sorted = sorted.sort_values(f'{year}')
        plt.subplot(3, 1, i + 1)
        plt.barh(sorted['자치구'], sorted[f'{year}'], color='blue', alpha=0.5)
        # plt.title(f'{year}', fontsize=10)
        plt.xlabel('단속 건수', fontsize=10)
        plt.ylabel(f'{year}', fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.xlim(0, 220000)
    plt.savefig(os.path.join(result_dir, "chart_enforcement_3"))

def main():
    output_dir = "../Output/"
    result_dir = "../Result/enforcement"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    mapping(output_dir, result_dir)
    draw_chart(output_dir, result_dir)

if __name__ == '__main__':
    main()