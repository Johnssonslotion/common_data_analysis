import itertools
import pandas as pd
from model import CommonSet
def setting_params(param_config:CommonSet):    
    '''
    ## selected_params 을 통해서 기본값을 추출하고 가져온다.
    ## 해당 파라미터는 model에서 정의되어있어야 하고, 해당 검증은 pydantic 을 통해서 실시한다.
    ## TODO: pydantic 을 통해서 검증하는 로직을 추가한다.

    ## parameters 의 구조
    ## Class CommonSet을 따름
    '''
    
    ret=[]
    df=pd.DataFrame()
    base={}
    if param_config.src is not None:
        if type(param_config.src) is str:
            df=loading_df(param_config)
        elif type(param_config.src) is pd.DataFrame:
            df=param_config.src
        if type(param_config.selection) is list:
            ele_cols=zip(*[df[jj] for jj in param_config.selection])        
        else:
            ele_cols=df[param_config.selection].tolist()

    base.update(param_config.params)
    for i,comb in enumerate(ele_cols):
        combinations=itertools.product([comb],*base.values())
        for combination in combinations:
            params=dict({key : value for key,value in zip(base.keys(),combination[1:])})
            if type(param_config.selection) is list:
                for j in range(len(param_config.selection)):
                    params[param_config.selection[j]]=combination[0][j]
            else:
                params[param_config.selection]=combination[0]
            ret.append({
                "index":i,
                "params":params
            })
    return ret,df

def loading_df(param_config:CommonSet):
    ## TODO : df 에 대한 다양한 포멧 호출을 가능하도록 변경
    f=param_config.src
    t=param_config.selection
    if f is None:
        raise Exception("src is None")
    if f.split(".")[-1] not in ["csv","xlsx"]:
        raise Exception("file type is not supported")
    if f.split(".")[-1]=="csv":
        df=pd.read_csv(f)
    elif f.split(".")[-1]=="xlsx":
        df=pd.read_excel(f)
    else:
        raise Exception("file type is not supported")
    
    if type(t) is list:
        for i in t:
            if i not in df.columns:
                raise Exception("target column is not in df")
    else:
        if t not in df.columns:
            raise Exception("target column is not in df")
    return df 


