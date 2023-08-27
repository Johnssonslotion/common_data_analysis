import os
import time
from celery import Celery
from dotenv import load_dotenv
from api.apis import Apis
from api_function import ApiFunction
from base.celery_base import CeleryBase
from base.mqmanage_base import MqManager
from utils.log import BaseLogger


class CeleryManager(BaseLogger):
    '''
    scope: 
    연결하고 관리하고 호출하고, 
    혹은 개별 워커로서 동작하게 하는 관리자 클래스
    '''
    def __init__(self, *args,**kwargs):
        #환경변수 설정 ## ENV = DEV, PROD
        self.env=kwargs.get("env","DEV")
        self.init_logger(logger_name="celery_manager")

    def server_run(self,**kwargs):
        '''
        celery worker를 실행한다.
        '''
        flag = True
        username=os.environ.get("RABBITMQ_WORKER_USER")
        password=os.environ.get("RABBITMQ_WORKER_PASS_ENC")
        password=CeleryBase.decrypt(password)
        
        while flag:
            ## health check mqserver
            try:
                mq_manager=MqManager()
                mq_manager.config(env=self.env)
                res=mq_manager.health_check()
                if res.status_code==200:
                    flag=False
                else:
                    self.report(fn="server_run",state="wait")
                    time.sleep(5)
            except Exception as e:
                self.report(fn="server_run",state="wait")
                time.sleep(30)
                continue


        ## assign mq user
        
        ## check user exists
        mq_manager.add_new_worker(username,password)
        mq_manager.assign_permission(username)
            
            
        self.report(fn="server_run",state="start")
        self.celeryBase=CeleryBase(
            username=os.environ.get("RABBITMQ_WORKER_USER"),
            password=os.environ.get("RABBITMQ_WORKER_PASS_ENC"),
            ENV=self.env
        )
        def process(params=None, function=None, request_obj=None):
            conn=ApiFunction(model=Apis.kakao)
            return conn.process(params=params, function=function, request_obj=request_obj)
        self.celeryBase.register_task("process",process)
        self.celeryBase.run_worker()

    def client_run(self):
        '''
        celery client를 실행한다.
        '''
        pass
        


if __name__ == "__main__":
    load_dotenv()
    env=os.environ["ENV"]
    manager=CeleryManager(env=env)
    manager.server_run()
    #manager.client_run()





