from copy import deepcopy
from base import ApiBase
from api import KakaoRequest,KakaoResponse
from typing import List,Any, Dict, Optional, Union
from collections import deque
from shapely.geometry import Polygon,MultiPolygon
from pydantic import BaseModel, Field
from utils.log import BaseLogger
from geohash_manager import GeohashManager
import re
import pygeohash as pgh

class KakaoStrategyConfig(BaseModel):
    geohash_start:int=Field(4,description="검색영역의 geohash 시작값")
    geohash_end:int=Field(8,description="검색영역의 geohash 시작값")

class KakaoStrategy(BaseLogger):
    '''
    ret 처리 전략을 정의한다.
    - request_cache : request를 저장하는 cache
    - ret : request, response를 저장하는 cache
    - curser : 현재 진행중인 request
    - end : 현재 진행중인 request가 마지막인지 확인하는 flag

    #### area search 에 관련된 변수
    - area : 현재 진행중인 request의 검색영역
    - config : 현재 진행중인 request의 설정값
    >>> geohash_start : 검색영역의 geohash 시작길이
    >>> geohash_end : 검색영역의 geohash 종료길이
    '''
    def __init__(self,request_obj:KakaoRequest):
        self.ret:List[Dict(str,Union(KakaoRequest,KakaoResponse))]=[]
        self.curser:KakaoRequest=None
        self.end=False
        self.request_candidate=deque()
        self.area:Optional[Union[Polygon,MultiPolygon]]=None
        self.config=KakaoStrategyConfig()
        self.init_request=request_obj
        super().__init__(logger_name="app_common.kakao_api")

    ###
    def request_analysis_main(self,request_obj:KakaoRequest,response_obj:KakaoResponse):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다.
        - area search인 경우 request_analysis_area 함수를 호출한다.
        - default search인 경우 request_analysis_default 함수를 호출한다.
        - 해당 사항에 따라 request_cache에 저장한다.
        '''
        if response_obj.meta.total_count>45:
            if request_obj.params.rect is not None:
                return self.request_analysis_rect(request_obj=request_obj)
            elif request_obj.params.radius is not None:
                return self.request_analysis_radius(request_obj=request_obj)
            else: ## 따로 구분할 방법이 없으므로 45개 이상이면 defalut 처리 한다.
                return self.request_analysis_default(request_obj=request_obj,response_obj=response_obj)
        else:## 따로 구분할 방법이 없으므로 45개 이상이면 defalut 처리 한다.
            return self.request_analysis_default(request_obj=request_obj,response_obj=response_obj)

    def request_analysis_radius(self,request_obj:KakaoRequest):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다.
        
        * 비고 response는 고려하지 않음.

        생성에 대한 요소는 패키지로 이전됨.
        - step 1: request의 Radius,x,y를 통해서 ploygon을 생성한다. 그리고 bound 를 생성한다.
        - step 2: 생성된 bound를 기준으로, geohash를 생성한다.
        - step 3: 만약 생성된 geohash가 단일이면 subgeohash를 생성하고, 그에 따른 rect을 생성함
        - step 4: 단일이 아니면, 
        '''
        x=float(request_obj.params.x)
        y=float(request_obj.params.y)
        radius=int(request_obj.params.radius)
        
        ### remove radius
        base_request_obj=request_obj
        base_request_obj.params.x=None
        base_request_obj.params.y=None
        base_request_obj.params.radius=None
        base_request_obj.params.sort=None
        ### 
                
        manager=GeohashManager(limits=6)
        candidate=manager.xyr_to_rects(x=x,y=y,r=radius)
        if len(candidate)<=1:
            manager=GeohashManager(limits=7)
            candidate=manager.xyr_to_rects(x=x,y=y,r=radius)
        #print(candidate)
        for i in candidate:
            base_request_obj.params.rect=i ##RectShape 객체로 변경완료
            self.request_candidate.append(base_request_obj)
            #request_obj.params.rect=i ## TODO : Rect객체에서 str로 변환하는 함수를 만들어야함.
        return
    
    def request_analysis_rect(self,request_obj:KakaoRequest):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다.
        ## step 1: request의 rect를 통해서 ploygon을 생성한다. 그리고 bound 를 생성한다.
        ## step 2: 생성된 bound를 기준으로, geohash를 생성한다.
        ## step 3: 만약 생성된 geohash가 
        ## step 3: 생성된 geohash 를 1단계 나누어서(1단계 길이를 증가시켜서) request를 생성한다.
        '''
        #print("devided start")
        #print(f"\n quene:{len(self.request_candidate)} total_count:{ret['response'].meta.total_count},size:{100*(self.curser.params.rect.xmax-self.curser.params.rect.xmin):2.2f}:{100*(self.curser.params.rect.ymax-self.curser.params.rect.ymin):2.2f},rect:{self.curser.params.rect} page:{self.curser.params.page},request_candidate:{len(self.request_candidate)}")
        base_request_obj=request_obj
        bbox=request_obj.params.rect.items
        manager=GeohashManager(limits=7)
        candidate, geohash_set=manager.rect_to_rects(bbox=bbox)
        if len(candidate)<=1:
            manager=GeohashManager(limits=8)
            candidate, geohash_set=manager.rect_to_rects(bbox=bbox)
        for i,jj in zip(candidate,geohash_set):
            base_request_obj.params.page=1
            base_request_obj.params.rect=i ##RectShape 객체로 변경완료
            #print(base_request_obj.params.rect)
            copied_request_obj=deepcopy(base_request_obj)
            self.request_candidate.append(copied_request_obj)
            #request_obj.params.rect=i ## TODO : Rect객체에서 str로 변환하는 함수를 만들어야함.
            # print(f"request_candidate:{len(self.request_candidate)}")
            # print(f"base_request_obj:{jj} _ {copied_request_obj.params.rect}")
        return
        
    def request_analysis_default(self,request_obj:KakaoRequest,response_obj:KakaoResponse):
        '''
        request_obj 를 분석하여, 검색영역을 분할한다. _ 기본적인 page처리를 한다.
        '''
        ## 현재 커서가 마지막 페이지인지 확인
        if response_obj.meta.is_end:
            request_obj.params.page=1
            self.end=True
            return
        elif request_obj.params.page == 3:
            request_obj.params.page=1
            self.end=True
            return
        else:
            page=int(request_obj.params.page)
            page+=1
            request_obj.params.page=page
            self.request_candidate.append(self.curser)
            return

    async def process(self,api,request_obj:KakaoRequest) -> List[Dict]:
        '''
        연산을 진행하는 재귀함수
        - request를 1차적으로 처리 한 후, 결과를 분석해서 다음 request를 생성한다.
        - 
        - request_cache에 저장된 request를 순차적으로 처리한다.
        - request_cache에 저장된 request가 없으면, 현재 request를 처리한다.
        '''
        self.curser=request_obj
        while self.curser:
            response_obj= await api.call_api(request_obj=self.curser)
            if self.curser.params.rect is not None:
                geohash=GeohashManager.rect_geohash(self.curser.params.rect)
                ret={
                    "geohash":geohash,
                    "request":request_obj,
                    "response":response_obj
                }
            else: 
                ret={
                    "request":request_obj,
                    "response":response_obj
                }
            # if ret['response'].meta.total_count > 100:
            #     print(f"\n quene:{len(self.request_candidate)} total_count:{ret['response'].meta.total_count},size:{100*(self.curser.params.rect.xmax-self.curser.params.rect.xmin):2.2f}:{100*(self.curser.params.rect.ymax-self.curser.params.rect.ymin):2.2f},rect:{self.curser.params.rect} page:{self.curser.params.page},request_candidate:{len(self.request_candidate)}")
            #     print("break")
            ## 객체에 담아두기, request 결과(response)에 따라서, 다음 request를 생성한다.
            self.request_analysis_main(request_obj=self.curser,response_obj=response_obj)
            ## request_cache에 저장된 request를 순차적으로 처리한다.
            self.ret.append(ret)
            if len(self.request_candidate)>0:
                self.curser=self.request_candidate.pop()
            else:
                self.curser=None    
        return self.ret
            