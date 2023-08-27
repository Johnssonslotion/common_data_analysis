import itertools

from celery import Task
from model import *
from base import *
from utils import BaseLogger,setting_params
from api.apis import Apis

import pandas as pd
import requests

class ApiFunction(Task, ApiBase,BaseLogger):
    '''
    APIBase의 인터페이스 wrapper 
    -> ApiBase로 기능 이전, 인터페이스 용 함수만 정의
    -> celery task를 상속받아서, 비동기로 동작하게 함
    - model : Apis     
    ## TODO : argparser 추가
    '''
    def __init__(self,model:Apis=None,**kwargs):
        kwargs["logger_name"]="api_common"        
        self.init_logger(**kwargs)        
        ### TODO : argparser should be added
        if model is not None:
            if model in Apis:
                self.model=model
                self.process_strategy=model.strategy
            else:
                raise Exception("model not in Apis")
        else:
            ## selection of model
            self.interact()
        super().__init__(model=self.model)
        self.report(obj=str(self.model),fn=f'initFn',state='init',msg='api_common init')
        
    def interact(self):
        '''
        작업을 위한 모델을 선택하기 위한 인터페이스 함수, 프롬프트용
        '''
        self.report(fn='interact',state='start',)    
        while True:
            try:
                placeholder=[]
                print("\n")
                for i,j in enumerate(Apis):
                    placeholder.append(j)
                    print(f"{i} : {j}")
                model=input("select model : ")
                if (model in Apis): #or (int(model) in range(len(Apis))):
                    if model in Apis:
                        self.model=model
                    else:
                        self.model=placeholder[model]
                    break
                else:
                    raise Exception("model not in Apis")
            except Exception as e:
                print(e)
                continue
    def args(self):
        '''
        TODO : 필요한 기능들 정의 명세하기
        '''
        pass

    def health_check(self):
        self.report(fn='health_check',state='start')
        if self.model==None:
            raise Exception("model is None")
        ## TODO : health check 시나리오 정의하기
        self.report(fn='health_check',state='end',msg='health_check success')
        healthcheck=self.model.health_check
        res=requests.get(healthcheck.url,
                         headers=healthcheck.header.model_dump(by_alias=True),
                         params=healthcheck.params.model_dump(by_alias=True)
                         )
        if res.status_code!=200:
            ## TODO : error case 별 corrective action 필요
            ## TODO : apikey overflow case 때 subkey 로 변경하는 로직 추가
            raise Exception("health check failed")
        else:        
            return True
    
    def define_iter(self, **kwargs):
        '''
        우선순위 큐를 정의하는 함수.                
        입력 목록을 정의하고, 경우의 수를 생성하여 리스트화 한다. 
        - queue : 우선순위 큐에 들어갈 목록 
        - df : 경우의 수를 생성한 데이터프레임
        '''
        self.report(fn='define_model',state='start',msg='define_model success')
        if self.model==None:
            raise Exception("model is None")
        ## iteration model 정의
        obj=kwargs["config"]
        assert type(obj)==CommonSet ## TODO : type check decorator 추가
        param_config=obj
        self.report(fn='define_model',state='end',msg=f'{obj}') ## TODO : pydantic V2 에 적합한 출력폼으로 변경
        
        ### 개별 파라미터 정의함수 호출 
        queue,df=setting_params(param_config)
        self.df=df
        self.queue=queue
        self.report(fn='define_model',state='end',msg=f'num_of_length : {len(queue)}') ## TODO : pydantic V2 에 적합한 출력폼으로 변경

    
    
    async def run(self,**kwargs):
        '''
        실행함수
        - queue에 내용이 있으면 Queue 등록하고, process를 실행
        - queue에 내용이 없으면, process를 실행
        '''
        if len(self.queue)==0:
            self.report(obj=str(self.model),prefix="direct",fn='run',state='start')
            return await self.call_api(**kwargs)
        else:
            self.report(obj=str(self.model),prefix="queue",fn='run',state='start')
            if "params" not in kwargs.keys():
                raise Exception("params should be defined")
            else:
                ## TODO : Queue 에서 분산처리 로직 추가
                return True

    def enroll(self,**kwargs):
        '''
        TODO : enroll 시나리오 정의하기
        '''
        pass
    
    ##############################
   
    async def call_api(self, **kwargs)-> CommonResponse:
        '''
        single level api call with validation(pydanitc)
        '''
        func=kwargs.get("function")
        params=kwargs.get("params")
        requests_obj=kwargs.get("request_obj",None)
        ret = await super().call_api(params=params, func=func, request_obj=requests_obj)            
        self.report(state='end',msg=f'num_item:{ret.count}') ## 비고 commonResponse에 count property 추가
        return ret
    

    async def process(self,**kwargs):
        '''
        TODO : process 시나리오 정의하기
        process 함수는 api 응답을 받아서, 정제하는 함수
        배분처리 로직은 run 함수에서 처리
        input : api request
        output : api responses
        '''
        self.report(fn='process',state='start')
        func=kwargs.get("function")
        params=kwargs["params"]
        request_obj=kwargs.get("request_obj",None)
        ret= await super().process(params=params, function=func,request_obj=request_obj)
        ## process 함수는 wrapper 처럼 동작해야함
        return ret
        



        
        
        
        
        

        

        

        



    

        
        



    
def main():
    pass







if __name__ == "__main__":
    main()




        


        








    