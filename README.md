
 # 역세권이 아파트에 미치는 영향 구해줘 홈!
 
 ### 기간  
 2021.5.31~2021.6.4  
 
 ### 내용   
 리눅스 가상환경(virtualbox)에 빅데이터 파이프라인을 구축 후 부동산 가격예측 및 역세권과 상관관계 추정 
 
 ### 상세 과정
국토교통부에서 부동산 Data와 공공데이터포탈에서 지하철 역 위치 데이터를 수집하고 서울 열린 데이터 광장에서 Open API로 실시간 거래정보를 가져와 전처리 후 머신러닝 예측을 통해 역세권과 아파트 가격의 상관관계와 미래의 아파트 거래가격을 예측
 
 ### 사용 기술 stack
 
 ![image](./stack.png)


### 인원 및 역할
- 총원 4명 
- 역할 : 영화 정보 크롤링, 웹 페이지 구현

### 상세 역할
**< part (1) : 영화 정보 크롤링 >**    
- beautifulsoup4 활용 영화 제목, 감독, 개봉정보, 줄거리 등 10개 정보 크롤링(2011~2019)
- 크롤링 한 데이터 csv 형태로 Django 자체 db에 저장  

**< part (2) : 웹 페이지 구현 >**  
- django 활용 키워드 검색 추천 웹 페이지 구현  

## 프로젝트 결과(썸네일 Click!)

[![mv](https://img.youtube.com/vi/AfWimVqh24s/hqdefault.jpg)](https://www.youtube.com/watch?v=AfWimVqh24s)


### 개선 사항
- 검색시 속도 문제 해결 필요
- 웹 서버 배포를 통해 홈페이지 구현
- 키워드 기반 추천 방식 외에 다른 추천 시스템 방식 도입 