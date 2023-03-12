from geopy.geocoders import Nominatim
import pandas as pd
import warnings
import os
from tqdm import tqdm
import folium
from folium.plugins import HeatMap


warnings.simplefilter("ignore")


def data_merge():
    df_address = pd.DataFrame()

    value_list = []
    address_list = []
    area_list = []

    filenames = ["공동주택", "교육연구시설", "노유자시설", "단독주택", "문화및집회시설", "숙박시설", "업무시설", "운동시설", "운수시설", "의료시설",
                 "제1종근린생활시설", "제2종근린생활시설", "종교시설", "판매시설"]
    for filename in filenames:
        df = pd.read_excel(f"Data/Building/강서구_{filename}.xlsx", sheet_name="상세현황", engine="openpyxl")

        for i in range(len(df["도로명주소"])):
            value_list.append(filename)
        address_list.append(list(df["도로명주소"].values))
        area_list.append(list(df["건축면적(㎡)"].values))

    df_address["values"] = value_list
    df_address["address"] = sum(address_list, [])
    df_address["area(m2)"] = sum(area_list, [])

    print(f"[Done] {'-'*10} Merge complete")

    return df_address


def geocoding():
    output_dir = "Input/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = data_merge()
    geo_local = Nominatim(user_agent="South Korea")

    lat_list = []
    lng_list = []

    for address in tqdm(df["address"]):
        try:
            geo = geo_local.geocode(address)
            x_y = [geo.latitude, geo.longitude]
            lat_list.append(x_y[0])
            lng_list.append(x_y[1])
        except:
            lat_list.append(0)
            lng_list.append(0)

    df.to_csv(os.path.join(output_dir, "강서구_건물데이터.csv"), index=False)


def geocoding_add():
    # 누락된 위경도 데이터 입력
    df = pd.read_csv("Input/강서구_건물데이터.csv")
    df_0 = df[df["latitude"] == 0]
    df_n0 = df[df["latitude"] != 0]

    loc_list = ["공항대로7라길", "공항대로10가길", "등촌로35가길", "방화대로52가길", "방화대로35길", "방화대로31길", "금낭화로16길",
                "양천로20가길", "금낭화로3길", "곰달래로53나길", "곰달래로22길", "강서로5길", "공항대로7마길", "공항대로7라길",
                "방화대로21다길", "공항대로3나길", "양천로20길", "공항대로3가길", "서울특별시 강서구 오정로 443-198"]
    lat_list = [37.562544, 37.560201, 37.536958, 37.578421, 37.569376, 37.567941, 37.573954,
                37.572832, 37.566163, 37.537132, 37.529504, 37.528822, 37.562552, 37.562604,
                37.564584, 37.562360, 37.572944, 37.562235, 37.545498]
    lng_list = [126.812080, 126.812822, 126.862347, 126.818365, 126.815634, 126.815480, 126.812563,
                126.813758, 126.811207, 126.856065, 126.844304, 126.848029, 126.812312, 126.811903,
                126.812554, 126.809937, 126.813316, 126.809593, 126.798294]

    for loc, lat, lng in zip(loc_list, lat_list, lng_list):
        idx = df_0[df_0["address"].str.contains(loc)].index
        df_0.loc[idx, "latitude"] = lat
        df_0.loc[idx, "longitude"] = lng

    df = pd.concat([df_n0, df_0])
    df.to_csv("Input/강서구_건물데이터.csv", index=False)


def making_population_density():
    output_dir = "Result/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv("Input/강서구_인구밀도데이터.csv")
    df["values"] = df["values"].apply(lambda x: 100)

    geo_path = "Input/Gangseogu.geojson"

    m = folium.Map(
        location=[37.55, 126.84],
        zoom_start=12,
        tiles="CartoDB positron")
    folium.Choropleth(
        geo_data=geo_path,
        name="Gangseogu",
        data=df,
        columns=["code", "values"],
        key_on="feature.properties.code",
        fill_color="YlOrRd",
        fill_opacity=0.0,
        line_opacity=0.4,
        legend_name="Geo"
    ).add_to(m)
    HeatMap(df[["values", "code"]]).add_to(folium.FeatureGroup(name="Heat map").add_to(m))
    folium.LayerControl().add_to(m)

    filenames = ["공동주택", "교육연구시설", "노유자시설", "단독주택", "문화및집회시설", "숙박시설", "업무시설", "운동시설", "운수시설", "의료시설",
                 "제1종근린생활시설", "제2종근린생활시설", "종교시설", "판매시설"]
    colors = ['orange', 'black', 'blue', 'cadetblue', 'darkblue', 'darkgreen', 'darkpurple', 'darkred', 'gray', 'green',
              'lightblue', 'pink', 'lightgreen', 'lightred']

    df_building = pd.read_csv("Input/강서구_건물데이터.csv")
    df_building["color"] = df_building["values"].apply(lambda x: colors[filenames.index(x)])

    for index, row in df_building.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2,
            color=row["color"],
            fill=True,
            fill_color=row["color"],
            fill_opacity=0.3,).add_to(m)

    m.save(os.path.join(output_dir, "Gangseogu_building.html"))


def main():
    # 1. geocoding()으로 데이터 변환 -> 3시간 소요
    # geocoding()

    # 2. geocoding_add()으로 누락된 데이터 채워넣기
    geocoding_add()

    making_population_density()


if __name__ == "__main__":
    main()