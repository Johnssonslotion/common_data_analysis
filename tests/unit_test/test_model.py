import os
import sys
from dotenv import load_dotenv
import pytest
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


@pytest.mark.parametrize("test_input,expected_code,expected_count",[((127.056146,37.505308,100),200,11),((127.056146,37.505308,127.066146,37.515308),200,224)])
def test_specific_request_w_get_forced_authKey(test_input,expected_code,expected_count):
    load_dotenv(verbose=True)
    if len(test_input) == 3:
        params=CategoryFunction( ##TODO : CircleShape에서 받아서 처리하도록 수정
            category_group_code=KakaoCategory.CAFE,
            x=str(test_input[0]),
            y=str(test_input[1]),
            radius=str(test_input[2]),
        )
    elif len(test_input) == 4:
        params=CategoryFunction(
            category_group_code=KakaoCategory.CAFE,
            rect=RectShape(
                xmin=test_input[0],
                ymin=test_input[1],
                xmax=test_input[2],
                ymax=test_input[3],
            )
        )
    else:
        raise ValueError("test_input is invalid")    
    kakao_key=os.environ["KAKAOAPI"]
    header=KakaoHeader(
        authKey=kakao_key
    )
    header=KakaoHeader()
    
    item=KakaoRequest(
        header=header,
        params=params
    )
    p=item.params.model_dump(by_alias=True)
    res=requests.get(item.url, headers=item.header.model_dump(by_alias=True), params=p)
    assert res.status_code==expected_code
    assert res.json()["meta"]["total_count"]==expected_count, f"test_input : {test_input}, expected_count : {expected_count}, actual_count : {res.json()['meta']['total_count']}"


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





    












