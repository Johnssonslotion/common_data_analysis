import os
from celery import Task
import pytest
from base.celery_base import CeleryBase
from dotenv import load_dotenv
from cryptography.fernet import Fernet




@pytest.fixture(scope="module")
def celeryBase():
    load_dotenv(verbose=True)
    username=os.environ.get("RABBITMQ_WORKER_1_USER")
    password=os.environ.get("RABBITMQ_WORKER_1_PASS_ENC")
    manager=CeleryBase(username=username,password=password,ENV="DEV")
    return manager

def test_secret_key_password():
    load_dotenv(verbose=True)
    password="guest"
    encoded=CeleryBase.encrypt(password)
    assert encoded!=password
    assert CeleryBase.decrypt(encoded)==password


def test_celery_base_outside_defined(celeryBase:CeleryBase):
    ## no connection backend
    @celeryBase.app.task(name="sub")
    def sub(x,y):
        return x-y
    results=celeryBase.app.tasks['sub'].apply(args=[1,2]).result
    assert results == -1

def test_celery_base_function_injection(celeryBase:CeleryBase):
    ## no connection backend
    def add_1(x,y):
        return x+y+1
    celeryBase.register_task("add_1",add_1)
    results=celeryBase.app.tasks['add_1'].apply(args=[1,2]).result
    assert results == 4




