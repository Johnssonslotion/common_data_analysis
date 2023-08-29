import asyncio
import os
from celery import group
import pandas as pd
import pytest
from api.apis import Apis
from api.kakao_api import CategoryFunction, KakaoCategory, KeywordFunction
from api_function import ApiFunction
from base.celery_base import CeleryBase
from celery_main import CeleryManager
from model.common_model import CommonSet
from geohash_manager import GeohashManager

@pytest.fixture(scope="function")
def celery_worker():
    ## worker & mq check
    passward=CeleryBase.encrypt(os.environ.get("RABBITMQ_DEFAULT_PASS"))
    client=CeleryBase(
        username=os.environ.get("RABBITMQ_DEFAULT_USER"),
        password=passward,
    )
    return client

def test_health_worker(celery_worker):
    i=celery_worker.app.control.inspect()
    items=[j for j in i.ping()]
    print(items)
    assert len(items) >= 1

def test_celery_worker(celery_worker):
    params=KeywordFunction(
        query="테스트",
    )
    ret=celery_worker.app.send_task("process", kwargs={
        "params":params,"function":None,"request_obj":None
    })
    ret_dict,df=ret.get()
    assert len(ret_dict) == 3 

def test_celery_worker_many_req(celery_worker):
    params_list=[
        KeywordFunction(query="안산도서관",),
        KeywordFunction(query="천안도서관",),
        KeywordFunction(query="상록도서관",),
    ]
    def process(**kwargs):
        params=kwargs.get("params",None)
        function=kwargs.get("function",None)
        request_obj=kwargs.get("request_obj",None)
        conn=ApiFunction(model=Apis.kakao)
        ret = asyncio.run(conn.process(params=params, function=function, request_obj=request_obj)) 
        return ret
    
    celery_worker.register_task("process",process)
    ret=group(celery_worker.create_signature("process",
                                             #args=[i,None,None]
                                             kwargs={
        "params":i,"function":None,"request_obj":None
        }
        ) for i in params_list).apply_async()
    result=ret.join()
    assert len(result) == 3


    
def test_celery_worker_many_req_all(celery_worker):
    
    df=pd.read_csv("./app/rect.csv",encoding="utf-8-sig")
    rect=[GeohashManager.geohash_rect(i) for i in list(df["rect"])]
    df=pd.DataFrame({"rect":rect})
    set={
        "model":Apis.kakao,
        "src":df,
        "selection":"rect",
        "function":"category",
        "params":{
            "category_group_code":[KakaoCategory.CAFE,KakaoCategory.RESTAURANT,KakaoCategory.ACCOMMODATION],
        },
    }
    sets=CommonSet(**set)
    conn=ApiFunction(model=Apis.kakao)
    quene=conn.define_iter(
        config=sets
    )
    def process(params=None, function=None, request_obj=None):
        conn=ApiFunction(model=Apis.kakao)
        ret = asyncio.run(conn.process(params=params, function=function, request_obj=request_obj)) 
        return ret
    celery_worker.register_task("process",process)
    list_quene=[celery_worker.create_signature("process",
                                               kwargs={
                                                   "params":CategoryFunction(**i["params"]),"function":None,"request_obj":None}) for i in quene]
    ret=group(list_quene).apply_async()
    result=ret.join()
    
        
    

    

