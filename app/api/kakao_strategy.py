from base import ApiBase
from api import KakaoRequest,KakaoResponse
from typing import List,Any, Dict, Optional, Union
from collections import deque
from shapely.geometry import Polygon,MultiPolygon

class KakaoStrategy:
    '''
    ret 처리 전략을 정의한다.
    - request_cache : request를 저장하는 cache
    - ret : request, response를 저장하는 cache
    - curser : 현재 진행중인 request
    - end : 현재 진행중인 request가 마지막인지 확인하는 flag

    #### area search 에 관련된 변수
    - area : 현재 진행중인 request의 검색영역
    - config : 현재 진행중인 request의 설정값
    >>> geohash_start : 검색영역의 geohash 시작값
    >>> geohash_end : 검색영역의 geohash 끝값    
    '''
    def __init__(self):
        self.ret:List[Dict(str,Union(KakaoRequest,KakaoResponse))]=[]
        self.curser:KakaoRequest=None
        self.end=False
        self.request_candidate:deque(List[KakaoRequest])=deque()
        self.area:Optional[Union[Polygon,MultiPolygon]]=None
        self.config={
            "geohash_start":5,
            "geohash_end":7,
        }

    ###
    def request_analysis_main(self,request_obj:KakaoRequest):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다.
        - area search인 경우 request_analysis_area 함수를 호출한다.
        - default search인 경우 request_analysis_default 함수를 호출한다.
        - 해당 사항에 따라 request_cache에 저장한다.
        '''
        if request_obj.params.get("rect",None):
            return self.request_analysis_rect(request_obj=request_obj)
        elif request_obj.params.get("radius",None):
            return self.request_analysis_radius(request_obj=request_obj)
        else:
            return self.request_analysis_default(request_obj=request_obj)

    def request_analysis_radius(self,request_obj:KakaoRequest):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다.
        해당 요소를 분할하여, 
        '''
        


    def request_analysis_rect(self,request_obj:KakaoRequest):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다.
        '''
        pass

    def request_analysis_default(self,request_obj:KakaoRequest):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다. _ 기본적인 page처리를 한다.
        '''
        ## 현재 커서가 마지막 페이지인지 확인
        if self.curser.meta.is_end:
            self.end=True
            return
        else:
            self.curser.meta.page+=1
            self.request_cache.append(self.curser)
            return

    async def process(self,api,request_obj:KakaoRequest) -> List[Dict]:
        
        response_obj
        self.curser=request_obj
        response_obj= await api.call_api(request_obj=request_obj)
        ret={
            "request":request_obj,
            "response":response_obj
        }
        self.ret.append(ret)
        ## 객체에 담아두기, request 결과에 따라서, 다음 request를 생성한다.
        self.request_analysis_main(request_obj=request_obj)
        if self.end:
            return self.ret
        else:
            self.curser=self.request_cache.pop()
            await self.process(api=api,request_obj=self.curser)
        