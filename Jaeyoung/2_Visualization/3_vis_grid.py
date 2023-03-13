import os
import re
import pandas as pd
import folium
from folium.plugins import HeatMap
import numpy as np
# import pydeck as pdk


# def mapping_grid():
#     layer = pdk.Layer(
#         'CPUGridLayer',  # 대용량 데이터의 경우 'GPUGridLayer'
#         df,
#         get_position='[lng, lat]',
#         pickable=True,
#         auto_highlight=True
#     )
#
#     center = [126.986, 37.565]
#     view_state = pdk.ViewState(
#         longitude=center[0],
#         latitude=center[1],
#         zoom=10)
#
#     r = pdk.Deck(layers=[layer], initial_view_state=view_state)
#     r.show()

def main():
    output_dir = "../Output/"
    result_dir = "../Result/grid"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    df = pd.read_csv(os.path.join(output_dir, "Gangseo_250m.csv"))
    df = df.fillna(0)

    grid_size = 250

    map = folium.Map(location=[37.55, 126.84], zoom_start=12)

    # 격자 그리기
    for index, row in df.iterrows():
        sw = [row['위도'] - grid_size / 2 / 111319.9,
              row['경도'] - grid_size / 2 / (111319.9 * np.cos(row['위도'] * np.pi / 180))]
        ne = [row['위도'] + grid_size / 2 / 111319.9,
              row['경도'] + grid_size / 2 / (111319.9 * np.cos(row['위도'] * np.pi / 180))]
        folium.Rectangle(
            bounds=[sw, ne],
            fill=False,
            color='gray'
        ).add_to(map)

    # map.save(os.path.join(result_dir,'grid_map.html'))

    HeatMap(
        data=list(zip([row['위도'] for index, row in df.iterrows()], [row['경도'] for index, row in df.iterrows()], [row['floorarea_lbl'] for index, row in df.iterrows()])),
        name='heatmap'
    ).add_to(map)

    # 지도에 legend 추가
    map.add_child(folium.map.LayerControl())

    map.save(os.path.join(result_dir,'grid_heatmap.html'))


if __name__ == '__main__':
    main()