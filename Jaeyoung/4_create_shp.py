import pandas as pd
import geopandas as gpd
import os
from geopandas import GeoDataFrame
from shapely.geometry import Point

def train_shp(data_dir, output_dir):
    train_a = pd.read_csv(os.path.join(data_dir,"서울시 역사마스터 정보.csv"), encoding='cp949')
    train_g = pd.read_csv(os.path.join(data_dir,"서울교통공사 지하철역 주소 및 전화번호 정보.csv"), encoding='cp949')
    train_g = train_g[train_g['도로명주소'].str.contains('강서구')]
    train = pd.merge(train_a, train_g, left_on='역사명', right_on='역명', how='inner')

    train = train[['역사명', '위도', '경도']]
    train.columns = ['train_name', 'train_lat', 'train_lon']
    geometry = [Point(xy) for xy in zip(train.train_lat, train.train_lon)]
    gdf = GeoDataFrame(train, crs="EPSG:4326", geometry=geometry)
    gdf.to_file(os.path.join(output_dir,"Gangseo_Train.shp"), encoding="cp949", driver='ESRI Shapefile')

def cafe_shp(data_dir, output_dir):

    df = pd.read_csv(os.path.join(data_dir, "서울시_강서구_카페현황_202212.csv"))

    df = df[['상호명', '지점명', '위도', '경도']]
    df.columns = ['cafe_name', 'cafe_point', 'cafe_lat', 'cafe_lon']
    geometry = [Point(xy) for xy in zip(df.cafe_lon, df.cafe_lat)]
    gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
    gdf.to_file(os.path.join(output_dir,"Gangseo_Cafe.shp"), encoding="cp949", driver='ESRI Shapefile')

    drop_con = "엔제리너스|투썸플레이스|스타벅스|더벤티|폴바셋"

    chain = gdf[gdf['cafe_name'].str.contains(drop_con)]
    chain.to_file(os.path.join(output_dir,"Gangseo_CafeChain.shp"), encoding="cp949", driver='ESRI Shapefile')

    general = gdf[~gdf['cafe_name'].str.contains(drop_con)]
    general.to_file(os.path.join(output_dir,"Gangseo_CafeGeneral.shp"), encoding="cp949", driver='ESRI Shapefile')

def park_shp(data_dir, output_dir):
    df = pd.read_csv(os.path.join(data_dir, "서울특별시_강서구_도시공원정보_20230310.csv"), encoding='cp949')
    df = df[['위도', '경도', '공원명']]
    df.columns = ['park_lat', 'park_lon', 'park_name']
    geometry = [Point(xy) for xy in zip(df.park_lon, df.park_lat)]
    gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
    gdf.to_file(os.path.join(output_dir,"Gangseo_Park.shp"), encoding="cp949", driver='ESRI Shapefile')

def main():
    data_dir = "Data/"

    output_dir = "Output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    train_shp(data_dir, output_dir)
    cafe_shp(data_dir, output_dir)
    park_shp(data_dir, output_dir)

if __name__ == '__main__':
    main()