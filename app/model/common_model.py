from enum import Enum
import pandas as pd
from pydantic_core import CoreSchema, core_schema
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, computed_field, GetCoreSchemaHandler, GetJsonSchemaHandler, model_validator
from pydantic.json_schema import JsonSchemaValue
from typing import Optional, List, Union, Any
#from ..base import ApiBase


class CommonHeader(BaseModel):
    Content_Type:Optional[str]="application/json;"
    charset:Optional[str]="utf-8"
    
class CommonQuery(BaseModel):
    '''
    범용적으로 사용되는 Query를 정의하는 Class    
    '''
    pass

class CommonRequest(BaseModel):
    _url:str = PrivateAttr()
    @computed_field
    def url(self)->str:
        return self._url
    header:CommonHeader
    params:CommonQuery

    def __init__(self, url=None, **data):
        super().__init__(**data)
        self._url=url

class CommonFunction(Enum):
    '''
    일반적인 기능들을 정의하는 Enum class 
    기능들은 params의 Query를 파라미터로 받아서 처리한다.
    '''
    @property
    def function(self):
       return self.value
    @classmethod
    def __repr__(cls)->str:
        return f"{cls.value}"
    @property
    def schema(self):
        return self.value.model_json_schema()


class CommonMeta(BaseModel):
    pass

class CommonResponse(BaseModel):
    pass


class CommonSet(BaseModel):
    '''
    Setting을 정의하기 위한 class,
    model내부의 함수에 function이 있으면 해당 함수를 실행하며,
    해당 함수가 없을 시 오류를 발생한다.
    params의 dict은 function의 변수를 받아서 처리하되,
    해당 변수가 없을 시 오류를 발생한다.
    변수를 받을때 List 형태로 받을 수 있으며,
    List 형태 내부의 형태는 function 으로 정의된 기존 파라미터의 형태로 정의한다.    
    '''
    model_config = ConfigDict(arbitrary_types_allowed=True)
    model:Any ## TODO : Apis Enum 에 적합한 형태로 정의하기
    src: Optional[Union[str,pd.DataFrame]] = Field(None, description="source file path")
    selection: Optional[Union[List,str]] = Field(None, description="column selection")
    function: str = Field(...,description="function name")
    params: dict  = Field(...,description="function params")    

    @model_validator(mode="before")
    @classmethod
    def check_function(cls, data):
        model=data["model"]
        f=data["function"]
        assert hasattr(model.function, f), "function is not defined" 
        all_parameters=model.function[f].schema["properties"]
        required_parameters=model.function[f].schema["required"]
        for i in data["params"].keys():
            assert i in all_parameters.keys(), f"{i} is not defined parameter"
        if "src" in data.keys():
            if type(data["selection"]) is list:
                for j in data["selection"]:
                    assert j in all_parameters.keys(), f"{j} is not defined parameter"
                    if j in required_parameters:
                        required_parameters.remove(j)
            else:
                assert data["selection"] in all_parameters.keys(), "selection is not defined"
                if data['selection'] in required_parameters:
                    required_parameters.remove(data['selection']) ## selection으로 필수 파라미터가 제공됨
            ## dataframe 내부에 있는 컬럼은 추후 데이터 로딩시 검증예정
        for i in required_parameters:
            assert i in data["params"].keys(), f"{i} is required parameter"
        ## TODO : params 내부의 dict에서 type을 확인할 것
        return data
    
    


    