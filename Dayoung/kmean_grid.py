from simpledbf import Dbf5
import pandas as pd
import numpy as np
import geopandas as gpd
import folium

import os
from sklearn.cluster import KMeans


def main():
    output_dir = "Input/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dbf = Dbf5("../Jaeyoung/Data/Gangseo_Grid.dbf")
    df = dbf.to_dataframe()
    df = df[["gid", "경도", "위도", "train_name", "park_name", "cafe_name", "val"]]
    df.rename(columns={"gid": "grid", "경도": "longitude", "위도": "latitude", "train_name": "train", "park_name": "park", "cafe_name": "cafe_all", "val": "population"}, inplace=True)

    chainnames = ["스타벅스", "엔제리너스", "투썸플레이스", "파리바게뜨", "폴바셋", "더벤티"]
    chains = []
    commons = []
    for name in df["cafe_all"]:
        if type(name) is str and chainnames[0] in name:
            chains.append(chainnames[0])
            commons.append(np.NaN)
        elif type(name) is str and chainnames[1] in name:
            chains.append(chainnames[1])
            commons.append(np.NaN)
        elif type(name) is str and chainnames[2] in name:
            chains.append(chainnames[2])
            commons.append(np.NaN)
        elif type(name) is str and chainnames[3] in name:
            chains.append(chainnames[3])
            commons.append(np.NaN)
        elif type(name) is str and chainnames[4] in name:
            chains.append(chainnames[4])
            commons.append(np.NaN)
        elif type(name) is str and chainnames[5] in name:
            chains.append(chainnames[5])
            commons.append(np.NaN)
        else:
            chains.append(np.NaN)
            commons.append(name)

    df["cafe_chain"] = chains
    df["cafe_common"] = commons
    df.to_csv(os.path.join(output_dir, "Gangseo_grid.csv"), index=False)


    items = ["train", "park", "population", "cafe_chain", "cafe_common"]
    _weights = [0.2, 0.1, 0.2, 0.4, 0.3] # 가중치
    _points = [] # 위경도
    for item in items:
        df_ = df[["longitude", "latitude", item]].dropna().reset_index(drop=True)
        _points.append(df_[["longitude", "latitude"]].values)

    weighted_points = []
    for i in range(len(_weights)):
        weighted_points.append(_points[i]*_weights[i])
    weighted_mean = np.mean(np.concatenate(weighted_points), axis=0) # 가중 평균

    points_point = np.concatenate(_points, axis=0)
    num_bins = 5
    kmeans = KMeans(n_clusters=num_bins, random_state=42).fit(points_point)
    bins = kmeans.cluster_centers_

    print(f"쓰레기통 선정 위경도\n{bins}")

    # weighted_mean과 가장 가까운 클러스터의 중심점
    distances = np.linalg.norm(bins - weighted_mean, axis=1)
    trash_can_location = bins[np.argmin(distances)]
    print(f"가중 평균과 가장 가까운 클러스터의 중심점\n{trash_can_location}")

    # 결과 위도, 경도
    df_latng = pd.DataFrame()
    lats = []
    lngs = []
    for b in bins:
        lats.append(b[0])
        lngs.append(b[1])
    df_latng["lat"] = lats
    df_latng["lng"] = lngs
    df_latng["color"] = df_latng["lat"].apply(lambda x: "red")
    print(df_latng)

    # ----- Folium
    geo_gangseo = gpd.read_file("Input/Gangseogu.geojson")
    m = folium.Map([37.55, 126.83], tiles="CartoDB positron", zoom_start=12)

    folium.GeoJson(geo_gangseo,
                   name="json_data",
                   style_function=lambda feature: {
                       "fillColor": "gray",
                       "color": "gray",
                       "weight": 0,
                       "fillOpacity": 0.2,
                   }
                   ).add_to(m)

    for index, row in df_latng.iterrows():
        folium.Marker(
            location=[row["lng"], row["lat"]],
            fill_color=row["color"],
            color=row["color"],
            radius=5
        ).add_to(m)

    m.save("Result/결과.html")


if __name__ == "__main__":
    main()