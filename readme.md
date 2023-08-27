
# Geospatial data analysis

## 개요
지리공간 정보를 분석하기위한 지극히 개인적인 분석플랫폼

## 버전 
- v.0.1.2 병렬처리를 하기위한 worker 및 message broker settings (RabbitMQ를 기초로, 추후 Kafka로 이전필요)
- v.0.1.1 지리처리 함수 설계 및 패키지화 -> geohash_manager (해당 내용은 따로 - 패키지화 및 이관)
- v.0.1.0 api의 공통구조 설계 및 샘플 api (Kakao api 샘플 데이터 편입)
- v.0.0.0 github open

## 소스
### 데이터구조
- 형상관리는 poetry, python 3.11을 기조로 진행
- 레거시 코드들을 재활용함
- 대부분의 좌표규격은 crs4326으로 통일함
- 모듈화를 위해서 각 객체의 입출력은 pydanic 으로 묶고 검증함
- 추가적으로 각 객체는 검증요소로 묶고, 기능을 확장함.
- 추후 속도를 위해 검증요소는 제외할 수 있음
- 반복요소는 docker 형태로 이전 혹은 병렬처리를 둘다 사용할수 있도록 고려해야함.

### API 공통처리함수 구조설계
- 기본적인 파라미터를 받는 모델은 pydantic을 통해 data validation을 진행한다.
- 각 API 별 특이 분기에 대한 내용은 process라는 분기를 따로 정의해서 받고, 해당 분기는 wrapper 로 동작한다.
- 해당 처리는 비동기 처리가 가능해야 한다.
- 이 코드는 워커로도 동작이 가능해야한다. (python level 에서는 celery work로)

### worker등을 cli gcp로 배포하기 (추후 CICD로 편입필요)
- 형상관리를 하기위해서,



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
