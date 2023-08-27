import os
import argparse
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
from utils.log import BaseLogger
import pika


class MqHttpModel(BaseModel):
    headers:dict


class MqManager(BaseLogger):
    '''
    Mq를 관리하는 클래스, 초기 work를 생성하고, mq의 권한을 부여하기 위한 클래스.
    
    워커의 경우 단일 쓰레드로 동작하는 것을 가정하며, BlockingConnection을 기본값으로 사용함.
    다중 쓰레드로 동작하는 경우, (ex. celery), MqManager의 인스턴스를 직접사용하지 않음.
    local의 경우는 인증문제를 고려하지 않아도 되나, production의 경우는 인증문제를 고려해야함.
    그에 따라 인증문제를 해결하기 위한 인터페이스
    ref: https://pika.readthedocs.io/en/stable/
    ref: https://www.rabbitmq.com/management.html
    ref: https://rawcdn.githack.com/rabbitmq/rabbitmq-server/v3.12.3/deps/rabbitmq_management/priv/www/api/index.html

    '''
    def __init__(self,**kwargs):
        load_dotenv(verbose=True)
        self.init_logger(logger_name="mq_manager")
        self.config(**kwargs)

    def config(self, **kwargs):
        '''
        mq의 설정을 변경한다.
        '''
        default_url_aws=os.environ.get("RABBITMQ_URL")
        self.env=kwargs.get("ENV","DEV")

        if self.env=="DEV":
            self.url="localhost"
        elif self.env=="PROD":
            self.url=default_url_aws
        else:
            raise Exception("ENV is not defined")

    def check_user(self, user, passward):
        '''
        user가 있는지 확인한다.
        '''
        return pika.PlainCredentials(username=user,password=passward)

    def worker_list(self):
        '''
        worker를 생성한다.
        '''
        if self.env=="DEV":    
            admin_user=os.environ.get("RABBITMQ_DEFAULT_USER")
            admin_pass=os.environ.get("RABBITMQ_DEFAULT_PASS")
        elif self.env=='PROD':
            admin_user=os.environ.get("RABBITMQ_ADMIN_USER")
            admin_pass=os.environ.get("RABBITMQ_ADMIN_PASS")
        else:
            raise Exception("ENV is not defined")
        res=requests.get(
            url=f"http://{self.url}:15672/api/users/",
            auth=(admin_user,admin_pass)
        )
        return res

    def add_new_worker(self, user, passward, administartor=False):
        '''
        worker를 생성한다.
        '''
        if self.env=="DEV":    
            admin_user=os.environ.get("RABBITMQ_DEFAULT_USER")
            admin_pass=os.environ.get("RABBITMQ_DEFAULT_PASS")
        elif self.env=='PROD':
            admin_user=os.environ.get("RABBITMQ_ADMIN_USER")
            admin_pass=os.environ.get("RABBITMQ_ADMIN_PASS")
        else:
            raise Exception("ENV is not defined")
        self.logger.info(f"add new worker : {user}")
        ## check user exists
        res=self.worker_list()
        if res.status_code==200:
            if user in [i["name"] for i in res.json()]:
                self.logger.info(f"user {user} already exists")
                return res
        if administartor:
            tags="administrator"
        else:
            tags=""
        res=requests.put(
            url=f"http://{self.url}:15672/api/users/{user}",
            auth=(admin_user,admin_pass),
            json={
                "password":passward,
                "tags":tags
            }
        )
        return res
    def remove_worker(self, user):
        '''
        worker를 제거한다.
        '''
        if self.env=="DEV":    
            admin_user=os.environ.get("RABBITMQ_DEFAULT_USER")
            admin_pass=os.environ.get("RABBITMQ_DEFAULT_PASS")
        elif self.env=='PROD':
            admin_user=os.environ.get("RABBITMQ_ADMIN_USER")
            admin_pass=os.environ.get("RABBITMQ_ADMIN_PASS")
        else:
            raise Exception("ENV is not defined")
        self.logger.info(f"remove worker : {user}")
        ## check user exists
        res=self.worker_list()
        if res.status_code==200:
            if user not in [i["name"] for i in res.json()]:
                self.logger.info(f"user {user} not exists")
                return res
        res=requests.delete(
            url=f"http://{self.url}:15672/api/users/{user}",
            auth=(admin_user,admin_pass),
        )
        return res





       
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="mq manager")
    parser.add_argument("--env",type=str,help="environment",default="DEV")
    kwargs=parser.parse_args()
    mq_manager=MqManager(kwargs=kwargs)