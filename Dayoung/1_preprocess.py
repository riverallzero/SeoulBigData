import pandas as pd
import json
import os
import geopandas as gpd


# 1. 강서구 동별 인구데이터와 행정구역별 데이터를 바탕으로 데이터 병합
def polulation_preprocess():
    output_dir = "Input/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = json.load(open("Data/skorea_submunicipalities_geo.json", encoding="utf-8-sig"))

    # 2023년도 2월기준 강서구 행정구역(동읍면)별 총 인구수
    df = pd.read_csv("Data/강서구_주민등록인구.csv", encoding="cp949")
    df = df[df.columns[:3]][1:].drop(["항목"], axis=1)
    df.columns = ["name", "values"]

    # json파일과 동이름 일치하도록 변경
    df["name"] = df["name"].apply(lambda x: x.replace("제", "") if "제" in x else x)
    dong_list = df["name"][1:].values
    df = df[1:].reset_index(drop=True)
    print(f"강서구 총 동의 개수:{len(dong_list)} \n {dong_list}")

    code_data = []
    features = []
    # 강서구 동에 해당하는 geo 정보 추출
    geo_data = []
    for feature in data["features"]:
        if feature["properties"]["name"] in dong_list:
            code = feature["properties"]["code"]
            if str(code).startswith("2"):
                continue
            geo_data.append(feature)
            code_data.append({"dong": feature["properties"]["name"], "code": feature["properties"]["code"]})

    # 형식 맞추기
    for data in geo_data:
        feature = {
            "type": "Feature",
            "properties": {
                "code": data["properties"]["code"],
                "name": data["properties"]["name"]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": data["geometry"]["coordinates"]
            }
        }
        features.append(feature)

    feature_colelction = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(os.path.join(output_dir, "Gangseogu.geojson"), "w") as f:
        json.dump(feature_colelction, f, indent="\t")

    dong_data = pd.DataFrame.from_dict(code_data)
    dong_data = dong_data.sort_values("dong").reset_index(drop=True)
    df = df.sort_values("name").reset_index(drop=True)

    # 사용할 동 데이터
    df_dong = pd.concat([df, dong_data["code"]], axis=1).reset_index(drop=True)
    df_dong = df_dong.apply(lambda x: x.str.strip(), axis=1)

    map_data = gpd.read_file("Input/Gangseogu.geojson", driver="GeoJSON")

    merged_data = pd.merge(map_data, df_dong, on="code")
    merged_data.to_csv(os.path.join(output_dir, "강서구_인구밀도데이터.csv"), index=False)


def main():
    polulation_preprocess()


if __name__ == "__main__":
    main()