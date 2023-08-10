import pandas as pd
import requests


def main():
    placeholder=pd.DataFrame()
    for i in range(1,18):
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
    placeholder.to_csv(f"{contentTypeId}.csv",index=False,encoding="utf-8-sig")

if __name__ == '__main__':
    main()