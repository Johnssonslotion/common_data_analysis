from typing import Any, Dict, Optional,Union
from pydantic import BaseModel
import requests
from api.kakao_api import KakaoRequest

from model import CommonResponse, ApiModel

class ApiBase(ApiModel):
    '''
    기본 api base class, 인터페이스 제외 심플한 api를 위한 클래스
    '''
    def __init__(self,model):
        self.model = model
        self.process_strategy = self.model.strategy
    
    async def call_api(self, params:Dict,func=None, request_obj:KakaoRequest=None)-> CommonResponse:
        '''
        단위함수를 호출하는 함수        
        
        '''
        ## 비고 : request_obj, pydantic model
        if request_obj==None:
            request_obj=self.param_parser(params=params,func=func)
        
        res= requests.get(url=request_obj.url,
            headers=request_obj.header.model_dump(by_alias=True),
            params=request_obj.params.model_dump(by_alias=True)
            )
        if res.status_code!=200:
            raise Exception(f"status_code : {res.status_code}, {res.text}")
        return self.model.response(**res.json())
        
    def param_parser(self, params:Union[Dict,BaseModel],func=None):
        '''
        kwargs parser의 기본함수

        - function 과 params 를 받아서, request_obj 를 반환한다.
        - params 를 직접 반환 할 수 있으며, 이 경우 function 은 None 이다.

        '''
        if self.model==None:
            raise Exception("model is None")
        if type(params)==dict:
            if func==None:
                raise Exception("function should be defined")
            else:
                param_obj=self.model.function[function].value(**params)
                request_obj=self.model.request(
                    header=self.model.header(),
                    params=param_obj
                )
        else:
            ##
            assert isinstance(params,BaseModel), f"params should be dict or BaseModel, but {type(params)}"
            param_obj=params ## TODO : type check decorator 추가 
            request_obj=self.model.request(
                header=self.model.header(),
                params=param_obj
            )
        return request_obj
    
    