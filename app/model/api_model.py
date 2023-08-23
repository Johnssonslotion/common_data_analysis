from typing import Any, Dict
from abc import *

class ApiModel(metaclass=ABCMeta):
    '''
    상속 위한 ApiModel 메타클래스
    '''
    @abstractmethod
    def __init__(self, model):
        pass
    
    @abstractmethod
    async def call_api(self, url, params, headers)->Dict:
        pass

   
        



