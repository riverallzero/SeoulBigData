# 2023년도 서울 강서구 빅데이터 분석 공모전

## 강서구 분석 개요

### <공모 주제> 다회용 컵 반납·세척기 길거리 설치를 위한 최적 입지 선정
- 사용 데이터
  - 총인구 통계지도, 카페, 도시공원, 지하철역, 정류장, 역사마스터 정보
- 알고리즘
  - K-Mean, Elbow Method
- 선정결과
  - 노란색 -> 최적 입지(시범 운영)
  - 빨간색 -> 확대 운영 입지

<img width="500" alt="image" src="https://user-images.githubusercontent.com/93754504/227243063-f2cdbb23-0240-4d47-a73d-3230e0da548a.png">
<img width="500" alt="image" src="https://user-images.githubusercontent.com/93754504/227248821-73f93f10-977f-498d-9c46-d40787b4d76b.png">

### 코드
- [Gangseogu](Gangseogu) 폴더
  - [model.py](Gangseogu%2Fmodel.py) 실행
  ```python
      # 1. Csv data to .shp file
      shp_create = ShpfileCreate(data_dir, output_dir)
    
      shp_create.train_shp()
      shp_create.cafe_shp()
      shp_create.park_shp()
      shp_create.busstop_shp()
      print(f"{'*'*10} [Done] {'*'*10} \n Preprocessing(Csv to .shp)")
    
      # 2. Modeling
      mark_point()
      create_shp(output_dir)
      print(f"{'*'*10} [Done] {'*'*10} \n Modeling(Check Result/)")
  ```

### 과정(결과)
- [분석보고서](https://github.com/riverallzero/SeoulBigData/blob/main/reports.pdf) 참고
