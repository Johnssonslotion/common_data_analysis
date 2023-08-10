
# Geospatial data analysis

## 개요
지리공간 정보를 분석하기위한 새로운 플랫폼

## 버전 
v.0 github open


## 소스
### 데이터구조
- 형상관리는 poetry, python 3.11을 기조로 진행
- 레거시 코드들을 재활용함
- 대부분의 좌표규격은 crs4326으로 통일함
- 모듈화를 위해서 각 객체의 입출력은 pydanic 으로 묶고 검증함
- 추후 속도를 위해 검증요소는 제외할 수 있음
- 반복요소는 docker 형태로 이전 혹은 병렬처리를 둘다 사용할수 있도록 고려해야함. 


### 분석하기위한 OpenAPI
- google
- kakao
- naver
- ndsi

### 참고하기위한 util
- geohash 관련 util
- 플랫폼 전체검색

## 자료
- 읍면동 관련 자료 (ndsi)
- 시도 관련 자료 (ndsi) - 준비중
- 부동산 건물자료 (ndsi) - 준비중
