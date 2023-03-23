import os
import pandas as pd
import geopandas as gpd
from sklearn.cluster import KMeans
import numpy as np
import folium
from geopandas import GeoDataFrame
from shapely.geometry import Point
import matplotlib.pyplot as plt

def preprocess_feature():
    df = gpd.read_file("Data/Gangseo_Grid_Bus.dbf")
    df = df[["gid", "경도", "위도", "train_name", "park_name", "cafe_name", "bus_name", "val"]]
    df.columns = ['grid', 'longitude', 'latitude', 'train', 'park', 'cafe', 'bus', 'population']

    chainnames = ["스타벅스", "엔제리너스", "투썸플레이스", "파리바게뜨", "폴바셋", "더벤티"]
    chains = []
    commons = []
    for name in df["cafe"]:
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

    return df

def model_kmeans():
    df = preprocess_feature()
    items = ["train", "park", "population", "cafe_chain", "cafe_common", "bus"]
    _weights = [0.1, 0.1, 0.2, 0.3, 0.2, 0.1]  # 가중치
    _points = []  # 위경도
    for item in items:
        df_ = df[["longitude", "latitude", item]].dropna().reset_index(drop=True)
        _points.append(df_[["longitude", "latitude"]].values)


    weighted_points = []
    for i in range(len(_weights)):
        weighted_points.append(_points[i] * _weights[i])
    weighted_mean = np.mean(np.concatenate(weighted_points), axis=0)  # 가중 평균

    points_point = np.concatenate(_points, axis=0)
    num_bins = 16
    kmeans = KMeans(n_clusters=num_bins, random_state=42).fit(points_point)
    bins = kmeans.cluster_centers_
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(points_point)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, 11), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.savefig("Result/Results_ElbowMethod")

    print(f"쓰레기통 선정 위경도\n{bins}")

    # weighted_mean과 가장 가까운 클러스터의 중심점
    distances = np.linalg.norm(bins - weighted_mean, axis=1)
    trash_can_location = bins[np.argmin(distances)]
    print(f"가중 평균과 가장 가까운 클러스터의 중심점\n{trash_can_location}")

    df_latng = pd.DataFrame()
    lats = []
    lngs = []
    for b in bins:
        lats.append(b[0])
        lngs.append(b[1])
    df_latng["lat"] = lats
    df_latng["lng"] = lngs
    df_latng["color"] = df_latng["lat"].apply(lambda x: "red")

    return df_latng

def mark_point():
    df_latng = model_kmeans()

    geo = gpd.read_file(
        ("https://raw.githubusercontent.com/vuski/admdongkor/master/ver20230101/HangJeongDong_ver20230101.geojson"),
        driver='GeoJSON')
    geo_gangseo = geo[geo['sggnm'] == '강서구']

    m = folium.Map([37.55, 126.83], tiles="CartoDB positron", zoom_start=12)
    tiles = "http://mt0.google.com/vt/lyrs=y&hl=ko&x={x}&y={y}&z={z}"
    # 속성 설정
    attr = "Google"
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

    m.save("Result/결과_최적입지.html")

def create_shp(output_dir):

    # 최적입지 위경도 df
    df = model_kmeans()
    print(df)

    geometry = [Point(xy) for xy in zip(df.lat, df.lng)]
    gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
    gdf.to_file(os.path.join(output_dir, "R_Best_Station_.shp"), encoding="cp949", driver='ESRI Shapefile')


def main():
    output_dir = "Output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    mark_point()
    create_shp(output_dir)

if __name__ == '__main__':
    main()