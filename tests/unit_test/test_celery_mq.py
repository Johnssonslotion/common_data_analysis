import os
import pytest
from base.celery_base import CeleryBase
from threading import Thread    



@pytest.fixture(scope="function")
def celery_worker():
    celeryBase = CeleryBase(
        username=os.environ.get("RABBITMQ_WORKER_1_USER"),
        password=os.environ.get("RABBITMQ_WORKER_1_PASS_ENC"),
        ENV="DEV",
    )
    thread=Thread(target=celeryBase.run_worker)
    thread.daemon=True
    thread.start()
    yield


@pytest.fixture(scope="function")
def celeryBase():
    celeryBase = CeleryBase(
        username=os.environ.get("RABBITMQ_WORKER_1_USER"),
        password=os.environ.get("RABBITMQ_WORKER_1_PASS_ENC"),
        ENV="DEV",
    )
    return celeryBase


def test_temp(celeryBase,celery_worker):
    ret=celeryBase.process(1,2).get()
    print(ret)
    assert ret == 3 
    
    








