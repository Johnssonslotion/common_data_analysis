import os
import pytest
from base.celery_base import CeleryBase

@pytest.fixture(scope="function")
def celery_worker():
    ## worker & mq check
    passward=CeleryBase.encrypt(os.environ.get("RABBITMQ_DEFAULT_PASS"))
    client=CeleryBase(
        username=os.environ.get("RABBITMQ_DEFAULT_USER"),
        password=passward,
    )
    return client.app

def test_health_worker(celery_worker):
    i=celery_worker.control.inspect()
    items=[j for j in i.ping()]
    print(items)
    assert len(items) >= 1


