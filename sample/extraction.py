import asyncio
import os
import pickle
import time
from celery import group
from dotenv import load_dotenv
import pandas as pd
from geohash_manager import GeohashManager
import redis
from tqdm import tqdm

from api.apis import Apis
from api.kakao_api import CategoryFunction, KakaoCategory
from api_function import ApiFunction
from base.celery_base import CeleryBase
from model.common_model import CommonSet
from celery.result import AsyncResult

def quene(celery_worker):
    sample_path="./data/rect/rect.csv"
    df=pd.read_csv(sample_path,encoding="utf-8-sig")
    rects=[{
    "geohash": i,
    "rect": GeohashManager.geohash_rect(i)  
            }for i in list(df["rect"])]    
    df=pd.DataFrame(rects)  
    
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
    print(f"n of q:{len(quene)}")
    
    celery_worker.app.control.inspect().active_queues()
    list_quene=[celery_worker.create_signature("process",
                                               kwargs={
                                                   "params":CategoryFunction(**i["params"]),"function":None,"request_obj":None}) for i in quene]
    group_sign=group(list_quene)
    ret=group_sign.apply_async()
    print(ret.id)
    return ret
    
def wait_groupjob(celery_worker:CeleryBase,id):
    groupResults=celery_worker.get_result_by_group(id)
    return groupResults

def celery_worker_define():
    username=os.environ.get("RABBITMQ_DEFAULT_USER")
    password=os.environ.get("RABBITMQ_DEFAULT_PASS")
    password=CeleryBase.encrypt(password)

    celery_worker=CeleryBase(
        username=username,
        password=password,
        #ENV="DOCKER"
    ) ## 비고 client에서는 Localhost로 open된 port로 접근해야함
    def process(**kwargs):
        params=kwargs.get("params",None)
        function=kwargs.get("function",None)
        request_obj=kwargs.get("request_obj",None)
        conn=ApiFunction(model=Apis.kakao)
        ret,df = asyncio.run(conn.process(params=params, function=function, request_obj=request_obj)) 
        return ret,df
    celery_worker.register_task("process",process)
    return celery_worker

if __name__ == '__main__':
    load_dotenv(verbose=True)
    celery_worker=celery_worker_define()
    jobid=quene(celery_worker)
    ## hard extract from redis
    while True:
        r=redis.Redis(host="localhost",port=6379,db=0)
        ## from redis
        done=[]
        pending=[]
        fail=[]
        all_status=[]
        for i,j in tqdm(enumerate(r.keys())):
            data=r.get(j)
            unpickled=pickle.loads(data)
            if unpickled.get("group_id")==jobid:
                all_status.append(unpickled.get("status"))
                if unpickled.get("status")=="SUCCESS":
                    done.append(unpickled)
                elif unpickled.get("status")=="PENDING":
                    pending.append(unpickled)
                elif unpickled.get("status")=="FAILURE":
                    fail.append(unpickled)
        with open("./data/results/done.pkl","wb") as f:
            pickle.dump(done,f)
        with open("./data/results/pending.pkl","wb") as f:
            pickle.dump(pending,f)
        with open("./data/results/fail.pkl","wb") as f:
            pickle.dump(fail,f)
        ## break
        time.sleep(60)
        if len(all_status)==len(done):
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}-{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}-{time.time()-time.time()}-{len(all_status)}-{len(done)}")
            break
        elif len(all_status)==len(done)+len(fail):
            break
        else:
            ## format = current time-start time-elapsed time-total-job-done-fail
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}-{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}-{time.time()-time.time()}-{len(all_status)}-{len(done)}-{len(fail)}")
            continue