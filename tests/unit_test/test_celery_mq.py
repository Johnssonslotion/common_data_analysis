from multiprocessing.pool import AsyncResult
import os
import pickle
import pytest
from base.celery_base import CeleryBase
from threading import Thread
import redis


@pytest.fixture(scope="function")
def celery_worker():
    #load_dotenv(verbose=True)
    username=os.environ.get("RABBITMQ_DEFAULT_USER")
    password=os.environ.get("RABBITMQ_DEFAULT_PASS")
    password=CeleryBase.encrypt(password)
    celeryBase = CeleryBase(
        username=username,
        password=password,
        ENV="DEV",
    )
    thread=Thread(target=celeryBase.run_worker)
    thread.daemon=True
    thread.start()
    yield


@pytest.fixture(scope="function")
def celeryBase():
    username=os.environ.get("RABBITMQ_DEFAULT_USER")
    password=os.environ.get("RABBITMQ_DEFAULT_PASS")
    password=CeleryBase.encrypt(password)
    celeryBase = CeleryBase(
        username=username,
        password=password,
        ENV="DEV",
    )
    return celeryBase


def test_single_function(celeryBase,celery_worker):
    def new_process(x,y):
        return x+y
    celeryBase.register_task("new_process",new_process)
    ret=celeryBase.app.tasks["new_process"].delay(1,2)
    print(ret.id)
    result_get=ret.get()
    assert result_get == 3
    r=redis.Redis(host="localhost",port=6379,db=0)
    task="task"
    unpickled=r.get(f"celery-{task}-meta-{ret.id}")
    results=pickle.loads(unpickled)
    assert results["result"]==result_get, "redis에 저장된 결과값과 celery 결과값이 일치해야함"
    
    
    
def test_redis():
    r=redis.Redis(host="localhost",port=6379,db=0)
    # data=r.get(r.keys()[0])
    # unpickled=pickle.loads(data)
    # print(unpickled.keys())
    
    group_id=[]
    for i in r.keys():
        data=r.get(i)
        unpickled=pickle.loads(data)
        if unpickled.get("group_id") not in group_id:
            group_id.append(unpickled.get("group_id"))
    print(group_id)
    print("breakpoint")







