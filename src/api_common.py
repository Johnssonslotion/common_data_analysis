import itertools
from ..src.model import Apis
from ..src.utils import base_logger,setting_params
import pandas as pd
import requests
import json
from ..src.model import *

class ApiCommon(base_logger):
    def __init__(self,model:Apis=None,**kwargs):
        kwargs["logger_name"]="api_common"
        super().__init__(**kwargs)
        ### TODO : argparser should be added
        if model is not None:
            if model in Apis:
                self.model=model
            else:
                raise Exception("model not in Apis")
        else:
            ## selection of model
            self.interact()
        super().__init__(**kwargs)
        self.report(obj=str(self.model),fn=f'initFn',state='init',msg='api_common init')
        #self.health_check()
        if "iterable" in kwargs.keys():
            self.df = pd.DataFrame()
    def interact(self):
        '''
        to select api, input int or str
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
            ## TODO : apikey overflow case 때 sub key 로 변경하는 로직 추가
            raise Exception("health check failed")
        else:        
            return True
        
    def define_iter(self, **kwargs):
        self.report(fn='define_model',state='start',msg='define_model success')
        if self.model==None:
            raise Exception("model is None")
        ## iteration model 정의
        obj=kwargs["config"]
        assert type(obj)==CommonSet ## TODO : type check decorator 추가
        param_config=obj
        self.report(fn='define_model',state='end',msg=f'{obj}') ## TODO : pydantic V2 에 적합한 출력폼으로 변경
        queue,df=setting_params(param_config)
        self.df=df
        self.queue=queue
        self.report(fn='define_model',state='end',msg=f'num_of_length : {len(queue)}') ## TODO : pydantic V2 에 적합한 출력폼으로 변경

    ##############################
    def get_data(self, **kwargs):
        self.report(fn='get_data',state='start',msg='get_data success')
        ## TODO : static url should be change to env
        if self.model==None:
            raise Exception("model is None")
        if "iterable" in kwargs.keys():
            iterable=kwargs["iterable"]

        

        

        



    

        
        



    
def main():
    placeholder=pd.DataFrame()
    for i in range(1,19):
        print(f"sigungu : {i}")
        contentTypeId=12
        areacode=i
        res=requests.get(
            f"http://apis.data.go.kr/B551011/KorWithService1/areaBasedList1?serviceKey=9KfxRkDosyTVhj2D2gRnVT0sZwTeX1baryBAMcOCnEiPE8wzgLgE6rzwtheZm79e%2FBpHPgBVvi2ppZJ%2FIYj8mg%3D%3D&numOfRows=500&pageNo=1&MobileOS=ETC&MobileApp=AppTest&listYN=Y&arrange=C&_type=json&contentTypeId={contentTypeId}&areaCode={areacode}"
        )
        if res.json()["response"]["body"]["items"]=='':
            continue
        else:
            ret=res.json()["response"]["body"]["items"]["item"]
            df=pd.DataFrame(ret)
            #df.to_csv(f"{contentTypeId}_{areacode}_{sigungucode}.csv",index=False,encoding="utf-8-sig")
            placeholder=pd.concat([placeholder,df])
    placeholder.to_csv(f"{contentTypeId}_{areacode}.csv",index=False,encoding="utf-8-sig")








if __name__ == "__main__":
    main()




        


        








    