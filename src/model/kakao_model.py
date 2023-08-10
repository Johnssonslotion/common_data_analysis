from typing import Any, Optional, List, Union
from dotenv import load_dotenv
from pydantic import Field, computed_field,field_serializer,  field_validator,ConfigDict,InstanceOf
from enum import Enum,EnumMeta
from . import CommonRequest, CommonHeader,CommonQuery, CommonFunction
import os

class KakaoCategory(str, Enum):
    '''
    "ref":"https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword-request-category-group-code"
    '''
    MARKET='MT1'
    STORE='CS2'
    KINDERGARDEN='PS3'
    SCHOOL='SC4'
    ACADEMY='AC5'
    PARKING='PK6'
    GASSTATION='OL7'
    SUBWAY='SW8'
    BANK='BK9'
    CULTURE='CT1'
    AGENT='AG2'
    PUBLIC='PO3'
    ATTRACTION='AT4'
    ACCOMMODATION='AD5'
    RESTAURANT='FD6'
    CAFE='CE7'
    HOSPITAL='HP8'
    def __str__(str):
        return str.value

class KakaoHeader(CommonHeader):
    authKey:str = Field(default="", serialization_alias="Authorization") 
    #_authKey:str = PrivateAttr()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "authKey" in kwargs:
            self.authKey=f"KakaoAK {kwargs['authKey']}"
        else:
            dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
            load_dotenv(dotenv_path)
            auth_key=os.getenv("KAKAOAPI")
            self.authKey=f"KakaoAK {auth_key}"
    

class AddressFunction(CommonQuery):
    function:str = Field(default="AddressFunction", repr=True)
    query:str
    analze_type:str = "similar"
    @computed_field
    @property
    def url(self)->str:
        base="https://dapi.kakao.com/"
        return f"{base}v2/local/search/address.json"
    
    
class GeocodeFunction(CommonQuery):
    function:str = Field(default="GeocodeFunction", repr=True)
    x:str
    y:str
    input_coord:str = "WGS84"
    output_coord:str = "WGS84"
    @computed_field
    @property
    def url(self)->str:
        return f"https://dapi.kakao.com/v2/local/geo/coord2address.json"

class KeywordFunction(CommonQuery):
    function:str = Field(default="KeywordFunction", repr=True)
    query:str
    category_group_code: KakaoCategory #= KakaoCategory.value
    radius:str = "20000"
    x:Optional[str] = None
    y:Optional[str] = None
    rect:Optional[str] = None
    sort:str = "distance"
    page:str = "1"
    size:str = "15"
    @field_serializer("category_group_code")
    def serialize_category_group_code(self, v:KakaoCategory)->str:
        return v.value
    @property
    def url(self)->str:
        base="https://dapi.kakao.com/"
        return f"{base}v2/local/search/keyword.json"
    
class CategoryFunction(CommonQuery):
    function:str = Field(default="CategoryFunction", repr=True)
    category_group_code:KakaoCategory
    x:Optional[str] = None
    y:Optional[str] = None
    radius:Optional[str] = None
    rect:Optional[str] = None
    sort:str = "distance"
    page:str = "1" ## <45
    size:str = "15" ## <15
    
    @computed_field
    @property
    def url(self)->str:
        base="https://dapi.kakao.com/"
        return f"{base}v2/local/search/category.json"

class KakaoFunction(CommonFunction):
    address=AddressFunction
    geocode=GeocodeFunction
    keyword=KeywordFunction
    category=CategoryFunction
    
    @classmethod
    def get_function(cls, function:str)->Any:
        return cls[function]
    

class KakaoRequest(CommonRequest):
    model_config =ConfigDict(revalidate_instances='subclass-instances')
    header:KakaoHeader
    params:Any
    
    def __init__(self, **data):
        url=data["params"].url
        super().__init__(url,**data)
    
    @field_validator("params", mode="before")
    @classmethod
    def check_params(cls, values):
        assert any([isinstance(values, v.value) for v in list(KakaoFunction)]) == True, "params must be one of KakaoFunction"
        return values
    






