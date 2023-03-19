import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import pyproj
import contextily as ctx
from sklearn.cluster import KMeans

def mapping_sales(new):

    # 커피-음료 상권 & 분기별
    df = pd.read_csv("Data/Commercial/서울시_우리마을가게_상권분석서비스(신_상권_추정매출)_2021년.csv", encoding='cp949')
    df['상권_코드'] = df['상권_코드'].astype(str)
    merged = pd.merge(df, new, left_on=['상권_구분_코드','상권_구분_코드_명', '상권_코드', '상권_코드_명'], right_on= ['TRDAR_SE_C', 'TRDAR_SE_1', 'TRDAR_NO', 'TRDAR_NM'], how='inner')
    merged = merged[merged['서비스_업종_코드_명'] == '커피-음료']
    df1 = merged[merged['기준_분기_코드'] == 1]
    df2 = merged[merged['기준_분기_코드'] == 2]
    df3 = merged[merged['기준_분기_코드'] == 3]
    df4 = merged[merged['기준_분기_코드'] == 4]

    # df5 = merged.groupby(['상권_구분_코드','상권_구분_코드_명', '상권_코드', '상권_코드_명']).mean()['']

    infos = [(df1, "1Q"),
             (df2, "2Q"),
             (df3, "3Q"),
             (df4, "4Q")]

    # 단계구분도
    for data, title in infos:
        data = gpd.GeoDataFrame(data, crs='EPSG:4326', geometry=data['geometry'])
        ax = data.plot(figsize=(8, 8), column="분기당_매출_금액", legend=True,
                      edgecolor="0.2", markersize=200, cmap="rainbow")
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        plt.axis("off")
        plt.title(f"{title}")
        plt.savefig(f"Result/{title}.png")

    return df1


def mapping_defactopopulation(old):
    # 상권 생활인구
    df2 = pd.read_csv("Data/Commercial/서울시_우리마을가게_상권분석서비스(구_상권_생활인구)_2021년.csv", encoding='cp949')
    df2['상권_코드'] = df2['상권_코드'].astype(str)
    merged = pd.merge(df2, old, left_on=['상권_구분_코드', '상권_코드', '상권_코드_명'], right_on= ['TRDAR_SE_C', 'TRDAR_CD', 'TRDAR_CD_N'], how='inner')

    # 단계구분도
    data = gpd.GeoDataFrame(merged, crs='EPSG:4326', geometry=merged['geometry'])
    ax = data.plot(figsize=(8, 8), column="총_생활인구_수", legend=True,
                  edgecolor="0.2", markersize=200, cmap="rainbow")
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    plt.axis("off")
    plt.title("defactopopulation")
    plt.savefig(f"Result/defactopopulation.png")

    return merged

def mapping_workerpopulation(old):
    # 상권 직장인구
    df3 = pd.read_csv("Data/Commercial/서울시_우리마을가게_상권분석서비스(구_상권_직장인구)_2021년.csv")
    df3['상권_코드'] = df3['상권_코드'].astype(str)
    merged = pd.merge(df3, old, left_on=['상권_구분_코드', '상권_코드', '상권_코드_명'], right_on= ['TRDAR_SE_C', 'TRDAR_CD', 'TRDAR_CD_N'], how='inner')

    # 단계구분도
    data = gpd.GeoDataFrame(merged, crs='EPSG:4326', geometry=merged['geometry'])
    ax = data.plot(figsize=(8, 8), column="총_직장_인구_수", legend=True,
                  edgecolor="0.2", markersize=200, cmap="rainbow")
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    plt.axis("off")
    plt.title("workerpopulation")
    plt.savefig(f"Result/workerpopulation.png")

    return merged


def main():
    data_dir = "Data/Commercial"

    src_crs = pyproj.CRS('EPSG:5181')
    dst_crs = pyproj.CRS('EPSG:4326')

    transformer = pyproj.Transformer.from_crs(src_crs, dst_crs)

    old = gpd.read_file("Data/Commercial/O_TBGIS_TRDAR_RELM_4326.dbf", encoding="utf-8-sig")
    new = gpd.read_file("Data/Commercial/N_TBGIS_TRDAR_RELM_4326.dbf", encoding="utf-8-sig")
    old = old[old['SIGNGU_CD'] == '11500']
    # old['COR'] = old['XCNTS_VALU'].astype(str) + "," + old['YDNTS_VALU'].astype(str)
    # old['XCNTS_VALU'] = old['COR'].apply(lambda x: transformer.transform(x.split(",")[0], x.split(",")[1])[0])
    # old['YDNTS_VALU'] = old['COR'].apply(lambda x: transformer.transform(x.split(",")[0], x.split(",")[1])[1])

    new = new[new['SIGNGU_CD'] == '11500']
    # new['COR'] = new['XCNTS_VALU'].astype(str) + "," + new['YDNTS_VALU'].astype(str)
    # new['XCNTS_VALU'] = new['COR'].apply(lambda x: transformer.transform(x.split(",")[0], x.split(",")[1])[0])
    # new['YDNTS_VALU'] = new['COR'].apply(lambda x: transformer.transform(x.split(",")[0], x.split(",")[1])[1])

    mapping_sales(new)
    mapping_defactopopulation(old)
    mapping_workerpopulation(old)


if __name__ == '__main__':
    main()