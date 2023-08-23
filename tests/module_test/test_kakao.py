import pytest
from api.apis import Apis
from api.kakao_api import KakaoFunction, KakaoRequest, KeywordFunction
from api_function import ApiFunction


#@pytest.mark.parametrize()
@pytest.mark.asyncio
async def test_kakao_process():
    conn=ApiFunction(model=Apis.kakao)
    params=KeywordFunction(
        query="안산해양초등학교",
    )
    ret =await conn.process(params=params)
    assert len(ret)>0





    
    