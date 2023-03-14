import geopandas as gpd
import matplotlib.pyplot as plt
import os


def main():
    output_dir = "Result/graph/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 인구밀도
    population_ = gpd.read_file("Data/nlsp_021001001.shp", encoding="utf-8-sig")

    population_.plot(cmap="OrRd")
    plt.axis(False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "강서구_인구밀도(격자).png"), dpi=400)

    # 건축밀도(건축면적기준: 건축물의 바닥면적과 층수에 기반하여 계산)
    building_area = gpd.read_file("Data/nlsp_021002007.shp", encoding="utf-8-sig")

    building_area.plot(cmap="RdPu")
    plt.axis(False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "강서구_건축면적밀도(격자).png"), dpi=400)

    # 건축밀도(건축개수)
    building_count = gpd.read_file("Data/nlsp_021002021.shp", encoding="utf-8-sig")

    building_count.plot(cmap="PuBuGn")
    plt.axis(False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "강서구_건축개수밀도(격자).png"), dpi=400)
    plt.show()


if __name__ == "__main__":
    main()