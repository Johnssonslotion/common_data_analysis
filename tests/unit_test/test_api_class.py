from api_function import ApiFunction
from model import *
from utils import *
from api.apis import Apis
from api.kakao_api import *


import asyncio
import os
import sys

import pytest


def test_common_api_initialize(monkeypatch):
    input=[Apis.kakao,0]
    monkeypatch.setattr('builtins.input', lambda _: input.pop(0))
    conn=ApiFunction()
    assert conn.model==Apis.kakao
    # conn=ApiFunction()
    # assert conn.model==Apis.kakao

def test_common_api_health_check():
    
    conn=ApiFunction(model=Apis.kakao)
    assert conn.health_check()==True

def test_common_api_set_params():
    conn=ApiFunction(model=Apis.kakao)
    ## default src
    src='./data/kimhae_target_section.csv'
    src_selection="x"

    config=CommonSet(
        model=Apis.kakao,
        function="keyword",
        src=src,
        selection=src_selection,
        params={
            "category_group_code":[KakaoCategory.ACADEMY,KakaoCategory.CAFE],
            "query":["카카오"],
        },
    )
    matrix,df=setting_params(config)
    conn.define_iter(
        config=config
    )
    assert len(conn.queue)==len(matrix)

def test_common_api_set_params_columns():
    conn=ApiFunction(model=Apis.kakao)
    src='./data/kimhae_target_section.csv'
    src_selection=["x","y"]
    config=CommonSet(
        model=Apis.kakao,
        function="keyword",
        src=src,
        selection=src_selection,
        params={
            "category_group_code":[KakaoCategory.ACADEMY,KakaoCategory.CAFE],
            "query":["카카오"],
        },
    )
    matrix,df=setting_params(config)
    conn.define_iter(
        config=config
    )
    assert len(conn.queue)==len(matrix)



@pytest.mark.asyncio
async def test_common_api_call_api_local_case_1_no_area():
    '''
       
    
    '''
    conn=ApiFunction(model=Apis.kakao)
    params=KeywordFunction(
        query="안산해양초등학교",
    )
    ret=await conn.call_api(params=params)
    assert ret.meta.is_end ==True, "기본 출력값 확인" 
    assert ret.meta.total_count==3, "기본 출력값 확인" 

def test_common_api_call_api_remote_enroll():
    pass



def test_common_api_call_api_remote_update():
    pass
