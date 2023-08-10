from __future__ import annotations
from enum import Enum
from . import KakaoRequest, CommonRequest, KakaoHeader,KakaoFunction,AddressFunction

class Apis(Enum):
    kakao={
        "request":KakaoRequest,
        "header":KakaoHeader,
        "function":KakaoFunction,
        "health_check":KakaoRequest(
            header=KakaoHeader(),
            params=AddressFunction(
                query="서울특별시 강남구 논현동 279-8",
            )
        ),
    }    
    tourApi=None
    def __str__(self):
        return self.name
    @property
    def function(self):
        return self.value["function"]
    @property
    def header(self):
        return self.value["header"]
    @property
    def request(self):
        return self.value["request"] 
    @property
    def health_check(self):
        return self.value["health_check"]
    
    
    
    








class kakao(Enum):
    header=KakaoHeader
    params=KakaoFunction



