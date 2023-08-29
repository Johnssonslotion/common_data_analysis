import itertools
import os
import pickle
import pandas as pd
import pytest
from api.apis import Apis
from api.kakao_api import KakaoFunction, KakaoRequest, KeywordFunction
from api_function import ApiFunction
from geohash_manager import GeohashManager
from geohash_manager import RectShape

@pytest.fixture(scope="module")
def conn():
    return ApiFunction(model=Apis.kakao)

@pytest.fixture(params=["AddressFunction","KeywordFunction"])
def test_function(func):
    return Apis.kakao.function[func]()

@pytest.mark.parametrize("test_query, expected_request_counts, expected_documents_counts", [("안산해양초등학교",1,3),("카카오",3,45),("초등학교 서울특별시 강남구 논현동",3,45)])
@pytest.mark.asyncio
async def test_kakao_single_process(conn,test_query, expected_request_counts, expected_documents_counts):
    params=KeywordFunction(
        query=test_query,
    )
    ret =await conn.process(params=params)
    assert len(ret) == expected_request_counts, f"expected request counts : {expected_request_counts} but {len(ret)}"
    ## merge step
    merged_documents = [j for i in ret for j in i["response"].documents] ## 추후 pandas로 변경
    assert len(merged_documents) == expected_documents_counts, f"expected documents counts : {expected_documents_counts} but {len(ret[0]['response'].documents)}"

@pytest.mark.parametrize("test_query, expected_request_counts, expected_documents_counts", [(("127.031767","37.497175","200"),10,150)])
@pytest.mark.asyncio
async def test_kakao_area_search(conn,test_query, expected_request_counts, expected_documents_counts): 
    params=KakaoFunction.category.value(
        category_group_code="FD6",
        x=test_query[0],
        y=test_query[1],
        radius=test_query[2],
    )
    #ret = await conn.call_api(params=params)
    ret =await conn.process(params=params)
    assert len(ret) == expected_request_counts, f"expected request counts : 1 but {len(ret)}"
    ## merge step
    merged_documents = [j for i in ret for j in i["response"].documents] ## 추후 pandas로 변경
    assert len(merged_documents) == 150, f"expected documents counts : {expected_documents_counts} but {len(merged_documents)}"


@pytest.mark.parametrize("index,expected_request_counts,expected_documents_counts",[(0,1513,5570)])
@pytest.mark.asyncio
async def test_kakao_rect(conn,index,expected_request_counts,expected_documents_counts):    
    ## duplicate 제거 안됨
    try:
        df=pd.read_csv("./data/rect/rect.csv",encoding="utf-8-sig")
    except FileNotFoundError as e:
        pytest.skip("file not found - because of gitignore")
    rects=[ GeohashManager.geohash_rect(i)for i in list(df["rect"])]    
    params=KakaoFunction.category.value(
        category_group_code="FD6",
        rect=rects[index]
    )
    ret,df =await conn.process(params=params)
    assert len(ret) == expected_request_counts, f"expected request counts : 1 but {len(ret)}"
    ## merge step
    merged_documents = [j for i in ret for j in i["response"].documents] ## 추후 pandas로 변경
    assert len(merged_documents) == expected_documents_counts, f"expected documents counts : {expected_documents_counts} but {len(merged_documents)}"

def test_ret_decode(conn):
    ret=None
    try: 
        with open('./data/ret_obj.pkl','rb') as f:
            ret=pickle.load(f)
    except FileNotFoundError as e:
        pytest.skip("file not found - because of gitignore")
    df=conn.insert_geohash(ret)
    assert len(df) == 5570
    
    
        