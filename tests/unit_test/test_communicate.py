import os
import pika
import pytest
from dotenv import load_dotenv
import requests

from base.mqmanage_base import MqManager


@pytest.fixture(scope="module",params=[("guest","guest"),("RABBITMQ_WORKER_1_USER","RABBITMQ_WORKER_1_PASS")], ids=["guest","env_settings"])
def connection_(request):
    load_dotenv(verbose=True)
    if request.param[0]=="guest":
        username=request.param[0]
        password=request.param[1]
    else:
        username = os.getenv(request.param[0])
        password = os.getenv(request.param[1])
    try:
        connection=pika.BlockingConnection(
            pika.ConnectionParameters(
                credentials=pika.PlainCredentials(
                    username=username,
                    password=password
                ),
                host='localhost'
            )
        )
        return connection
    except Exception as e:
        pytest.skip(f"connection failed : {e}, {request.param}")
        

def test_rabbitmq_connect(connection_):
    assert connection_.is_open==True
    

def test_rabbitmq_http_connect():
    ## user list
    mqManager=MqManager()
    res=mqManager.worker_list()
    assert res.status_code==200
    assert res.json()[0]["name"]==os.environ.get("RABBITMQ_DEFAULT_USER")
    ## add new user
    user_gen="test"
    pass_gen="test"
    res=mqManager.add_new_worker(user_gen,pass_gen)
    if res.status_code==200:
        ## already exists
        item=[i["name"] for i in res.json() if i["name"]==user_gen]
        assert len(item)!=0, "user already exists"
    else:
        assert res.status_code==201, "user create failed"
    res=mqManager.remove_worker(user_gen)
    assert res.ok == True, "user delete failed" 
    assert res.status_code==204, "user delete failed"

    
    ## check user exists
    ## delete user


