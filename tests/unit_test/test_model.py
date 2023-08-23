import os
import sys
from dotenv import load_dotenv
import requests

from api.apis import Apis
from api.kakao_api import *
from model import *


def test_common_model():
    headers=CommonHeader(
        #authKey="sample_key"
    )
    req=CommonRequest(
        url="https://dapi.kakao.com/v2/search/web",
        header=headers,
        params=CommonQuery(),
    )
    assert req.url=="https://dapi.kakao.com/v2/search/web"
    #assert req.header.authKey=="sample_key"
    assert req.params==CommonQuery()
    

def test_specific_model():
    # 
    header=KakaoHeader(
        authKey="kakaoAK aaaa"
    )
    params=KakaoFunction.keyword.function(
        query="카카오",
        category_group_code=KakaoCategory.CAFE,
        radius="20000",
    )
    req=KakaoRequest(
        header=header,
        params=params
    )
    assert req.url=="https://dapi.kakao.com/v2/local/search/keyword.json"

def test_specific_request():
    load_dotenv(verbose=True)
    kakao_key=os.environ["KAKAOAPI"]
    header=KakaoHeader(
        authKey=kakao_key
    )
    header_parsing_result=header.model_dump(by_alias=True)
    assert header_parsing_result["Authorization"]==f"KakaoAK {kakao_key}"
    params=KeywordFunction(
        query="카카오",
        category_group_code=KakaoCategory.CAFE,
        radius="20000",
    )
    item=KakaoRequest(
        header=header,
        params=params
    )
    
    assert item.url=="https://dapi.kakao.com/v2/local/search/keyword.json"
    assert item.params.query=="카카오"
    
def test_specific_request_w_get():   
    header=KakaoHeader()
    params=CategoryFunction(
        category_group_code=KakaoCategory.CAFE,
        x="127.056146",
        y="37.505308",
        radius="20000",
    )
    item=KakaoRequest(
        header=header,
        params=params
    )
    res=requests.get(item.url, headers=item.header.model_dump(by_alias=True), params=item.params.model_dump(by_alias=True)
    )
    assert res.status_code==200
    assert res.json()["meta"]["total_count"]>0

def test_specific_request_w_get_forced_authKey():
    load_dotenv(verbose=True)
    kakao_key=os.environ["KAKAOAPI"]
    header=KakaoHeader(
        authKey=kakao_key
    )
    header=KakaoHeader()
    params=CategoryFunction(
        category_group_code=KakaoCategory.CAFE,
        x="127.056146",
        y="37.505308",
        radius="20000",
    )
    item=KakaoRequest(
        header=header,
        params=params
    )
    res=requests.get(item.url, headers=item.header.model_dump(by_alias=True), params=item.params.model_dump(by_alias=True)
    )
    assert res.status_code==200
    assert res.json()["meta"]["total_count"]>0


def test_setting_params():
    load_dotenv(verbose=True)
    ##
    src='../data/addr.csv'
    src_selection="rect" 
    set={
        "model":Apis.kakao,
        "function":"keyword",
        "src":src,
        "selection":src_selection,
        "params":{
            "category_group_code":[KakaoCategory.ACADEMY,KakaoCategory.CAFE],
            "query":["카카오"],
        },
    }
    config=CommonSet(**set)
    assert config.model==Apis.kakao
    assert config.function=="keyword"
    assert config.src==src
    assert config.selection==src_selection

## 패키지로 마이그레이션
# def test_spatial_model():
#     center_1= (37.505308, 127.056146)
#     center_2= (127.056146,37.505308)
#     rect_1= (37.505308, 127.056146, 37.505308, 127.056146)
#     rect_2= (127.056146,37.505308, 127.056146,37.505308)

#     case_1=CircleShape(x=center_1[0],y=center_1[1],radius=2000)
#     assert case_1.x==center_1[0] and case_1.y==center_1[1] and case_1.radius==2000, "case_1"
#     case_2=CircleShape(center=center_1,radius=20000)
#     assert case_2.x==center_1[0] and case_2.y==center_1[1] and case_2.radius==20000, "case_2"
#     case_3=CircleShape(center=center_2,radius=20000)
#     assert case_3.x==center_2[1] and case_3.y==center_2[0] and case_3.radius==20000, "case_3"
    
#     rect_1=RectShape(xmin=rect_1[0],ymin=rect_1[1],xmax=rect_1[2],ymax=rect_1[3])
#     assert rect_1.xmin==rect_1[0] and rect_1.ymin==rect_1[1] and rect_1.xmax==rect_1[2] and rect_1.ymax==rect_1[3], "rect_1"
#     rect_2=RectShape(xmin=rect_2[0],ymin=rect_2[1],xmax=rect_2[2],ymax=rect_2[3])
#     assert rect_2.xmin==rect_2[1] and rect_2.ymin==rect_2[0] and rect_2.xmax==rect_2[3] and rect_2.ymax==rect_2[2], "rect_2"



    









