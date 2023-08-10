from ..src.api_common import ApiCommon
from ..src.model import *
from ..src.utils import *
from pydantic.dataclasses import dataclass

import os
import sys
from dotenv import load_dotenv


def test_common_api_initialize(monkeypatch):
    load_dotenv(verbose=True)
    input=[Apis.kakao,0]
    monkeypatch.setattr('builtins.input', lambda _: input.pop(0))
    conn=ApiCommon()
    assert conn.model==Apis.kakao
    # conn=ApiCommon()
    # assert conn.model==Apis.kakao

def test_common_api_health_check():
    load_dotenv(verbose=True)
    conn=ApiCommon(model=Apis.kakao)
    assert conn.health_check()==True

def test_common_api_set_params():
    conn=ApiCommon(model=Apis.kakao)
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
def test_common_api_set_params_columns():
    conn=ApiCommon(model=Apis.kakao)
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

def test_common_api_get_data_local():
    pass



def test_common_api_get_data_remote_enroll():
    pass



def test_common_api_get_data_remote_update():
    pass
