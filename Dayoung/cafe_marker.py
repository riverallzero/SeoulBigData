import pandas as pd
import numpy as np

import geopandas as gpd
from geopy.geocoders import Nominatim

from tqdm import tqdm

import json
import requests
import re
import os

import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

import plotly.express as px


def making_dataset():
    output_dir = "Input/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv("Data/서울특별시 강서구_카페 현황_20230314.csv", encoding="cp949")

    df_cafe = df[["업소명", "소재지도로명주소", "소재지지번주소"]]
    df_cafe = df_cafe.copy()

    df_cafe["address"] = df_cafe["소재지지번주소"].apply(lambda x: " ".join(x.split(" ")[0:4]) if " ".join(x.split(" ")[0:4])[-1].isdigit() else " ".join(x.split(" ")[0:5]))
    df_cafe["소재지도로명주소"] = df_cafe["소재지도로명주소"].apply(lambda x: x.split("(")[0].strip())
    df_cafe["소재지도로명주소"] = df_cafe["소재지도로명주소"].apply(lambda x: x.split(",")[0] if "," in x else x)

    lat = []
    lng = []
    with tqdm(total=len(df_cafe)) as pbar:
        for a, address in enumerate(df_cafe["address"]):
            try:
                url = "https://dapi.kakao.com/v2/local/search/address.json?query={address}".format(address=df["소재지도로명주소"][a])
                headers = {"Authorization": "KakaoAK " + "20bd06443491e44ed4863cec9f4c8134"}
                result = json.loads(str(requests.get(url, headers=headers).text))
                match_first = result["documents"][0]["address"]
                lat.append(float(match_first["x"]))
                lng.append(float(match_first["y"]))

            except:
                url = "https://dapi.kakao.com/v2/local/search/address.json?query={address}".format(address=address)
                headers = {"Authorization": "KakaoAK " + "20bd06443491e44ed4863cec9f4c8134"}
                result = json.loads(str(requests.get(url, headers=headers).text))
                match_first = result["documents"][0]["address"]
                lat.append(float(match_first["x"]))
                lng.append(float(match_first["y"]))
            pbar.update(1)

    df_cafe["latitude"] = lat
    df_cafe["longitude"] = lng

    df_cafe.to_csv(os.path.join(output_dir, "Gangseogu_cafe.csv"), index=False, encoding="utf-8-sig")


def cafe_chain():
    output_dir = "Input/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chainnames = ["스타벅스", "엔제리너스", "투썸플레이스", "파리바게뜨", "폴바셋", "더벤티"]

    df_cafe = pd.read_csv("Input/Gangseogu_cafe.csv")

    chains = []
    for name in df_cafe["업소명"]:
        if chainnames[0] in name:
            chains.append(chainnames[0])
        elif chainnames[1] in name:
            chains.append(chainnames[1])
        elif chainnames[2] in name:
            chains.append(chainnames[2])
        elif chainnames[3] in name:
            chains.append(chainnames[3])
        elif chainnames[4] in name:
            chains.append(chainnames[4])
        elif chainnames[5] in name:
            chains.append(chainnames[5])
        else:
            chains.append(np.NaN)
    df_cafe["chain"] = chains

    df_cafe_chain = df_cafe.dropna().reset_index(drop=True)
    df_cafe_chain.to_csv(os.path.join(output_dir, "Gangseogu_cafe_chain.csv"), index=False)


def making_density():
    output_dir = "Result/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    geo_gangseo = gpd.read_file("Input/Gangseogu.geojson")

    df = pd.read_csv("Input/Gangseogu_cafe_chain.csv")
    df["color"] = df["chain"].apply(lambda x: "green" if x == "스타벅스" else("darkblue" if x == "엔제리너스" else("orange" if x == "투썸플레이스" else ("darkred" if x == "더벤티" else ("blue" if x == "파리바게트" else "black")))))
    lat = df["longitude"].mean()
    long = df["latitude"].mean()

    # ----- Folium
    m = folium.Map([lat, long], tiles="CartoDB positron", zoom_start=12)

    folium.GeoJson(geo_gangseo,
                   name="json_data",
                   style_function=lambda feature: {
                       "fillColor": "gray",
                       "color": "gray",
                       "weight": 0,
                       "fillOpacity": 0.2,
                   }
                   ).add_to(m)

    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row["longitude"], row["latitude"]],
            fill_color=row["color"],
            color=row["color"],
            radius=3
        ).add_to(m)

    m.save(os.path.join(output_dir, "Chain_cafe.html"))
    

def main():
    # ------- 1. 도로명주소 & 지번주소를 이용한 좌표변환
    # making_dataset()

    # ------- 2. 카페 체인점
    # cafe_chain()

    making_density()


if __name__ == "__main__":
    main()