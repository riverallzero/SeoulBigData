import pandas as pd
import os
import matplotlib.pyplot as plt


def draw_chart(output_dir, result_dir):
    df = pd.read_csv(os.path.join(output_dir, "주차장_확보율.csv"))
    df = df[(df['자치구'] == '강서구') | (df['자치구'] == '은평구') |
            (df['자치구'] == '') | (df['자치구'] == '마포구')]
    df = df.transpose()
    df = df.rename(columns=df.iloc[0])
    df.drop('자치구', axis=0, inplace=True)

    df = df[(df.index.str.contains('2020')) |(df.index.str.contains('2021'))|(df.index.str.contains('2022'))]

    index_list = ['자동차등록대수', '주차면수', '주차장확보율']

    plt.rcParams['font.family'] = 'NanumGothic'

    for index in index_list:
        selected = df[df.index.str.contains(f'{index}')]
        selected.index = selected.index.str[0:4]
        selected.plot.bar(rot=0)
        plt.title(f'{index}')
        plt.show()

def main():
    output_dir = "../Output/"
    result_dir = "../Result/enforcement"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    draw_chart(output_dir, result_dir)

if __name__ == '__main__':
    main()