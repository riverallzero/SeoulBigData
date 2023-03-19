import pandas as pd
import geopandas as gpd

def main():
    # 역사_https://data.seoul.go.kr/dataList/OA-21232/S/1/datasetView.do
    # 정류장_https://www.data.go.kr/data/15099368/fileData.do?recommendDataYn=Y
    train_a = pd.read_csv("Data/서울시 역사마스터 정보.csv", encoding='cp949')
    train_g = pd.read_csv("Data/서울교통공사 지하철역 주소 및 전화번호 정보.csv", encoding='cp949')
    train_g = train_g[train_g['도로명주소'].str.contains('강서구')]

    bus = pd.read_csv("Data/서울시 정류장마스터 정보.csv", encoding='cp949')

    train = pd.merge(train_a, train_g, left_on='역사명', right_on='역명', how='inner')




if __name__ == '__main__':
    main()