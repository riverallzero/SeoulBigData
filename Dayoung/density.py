import folium
import pandas as pd
import json
import re

# 참고: https://d-hyeon.tistory.com/2

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
# 강서구 동에 해당하는 geo 정보 추출
with open("Data/Gangseogu_geo.json", "w", encoding="utf-8-sig") as f:
    geo_data = []
    for feature in data["features"]:
        if feature["properties"]["name"] in dong_list:
            code = feature["properties"]["code"]
            if str(code).startswith("2"):
                continue
            geo_data.append(feature)
            code_data.append({"dong": feature["properties"]["name"], "code": feature["properties"]["code"]})
    json.dump(geo_data, f, ensure_ascii=False, indent="\t")

dong_data = pd.DataFrame.from_dict(code_data)
dong_data = dong_data.sort_values("dong").reset_index(drop=True)
df = df.sort_values("name").reset_index(drop=True)

# 사용할 동 데이터
df_dong = pd.concat([df, dong_data["code"]], axis=1).reset_index(drop=True)
print(df_dong)

print("-"*10, "[Done] 강서구 데이터 추출 완료")

# Folium 데이터 그리기
geo_str = json.load(open("Data/Gangseogu_geo.json", encoding="utf-8-sig"))
m = folium.Map(
    location=[37.5502, 126.982],
    zoom_start=12,
)
m.choropleth(
    geo_data=geo_str,
    data=df_dong,
    columns=["code", "values"],
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="population(people)",
)
print(m)