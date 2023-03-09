import pandas as pd
from konlpy.tag import Okt
from collections import Counter # 빈도 수 세기
from wordcloud import WordCloud, STOPWORDS # wordcloud 만들기
import matplotlib.pyplot as plt # 시각화
import matplotlib as mp
import os

def token_konlpy(text):
    okt=Okt()
    return [word for word in okt.nouns(text) if len(word)>1]

def main():
    output_dir = "../output/complaints/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(os.path.join(output_dir, "강서구_민원.csv"), index_col = 0)

    script = df['title']
    script.to_csv(os.path.join(output_dir,'word.txt'), encoding='utf-8-sig')

    text = open(os.path.join(output_dir,'word.txt'), encoding='utf-8-sig').read()
    spwords = set(STOPWORDS)

    noun = token_konlpy(text) # 명사추출
    print(len(noun))
    noun_set = set(noun) # 중복명사 단일화
    print(len(noun_set))


    # word = dict(count.most_common(20)) # 빈도수 상위 20개 까지 딕셔너리 형태로 자료 변환 {'noun':'key'}
    count = Counter(noun)


    del_list = ['강서구', '강서', '구청', '센터', '개선',
                '요청', '처리', '제안', '이용', '활용', '시설',
                '방안', '운영', '지역', '관련', '대한', '건의', '민원',
                '서비스', '변경', '관리', '주민', '대하', '실시', '구민', '문제']

    for i in del_list:
        count.pop(i)

    word = dict(count.most_common(20))

    wc = WordCloud(max_font_size=200,
                   font_path='C:\Windows\Fonts\malgun.ttf',
                   stopwords=spwords, background_color="white",
                   width=2000, height=500).generate_from_frequencies(word)

    plt.figure(figsize=(40, 40))
    plt.imshow(wc)
    plt.tight_layout(pad=0)
    plt.axis('off')
    # plt.show()
    plt.savefig(os.path.join(output_dir, '강서구_민원_워드클라우드.png'))

    common = dict(count.most_common(10))
    print(common)

if __name__ == '__main__':
    main()