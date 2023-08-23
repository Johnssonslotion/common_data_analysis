from pydantic import BaseModel, Field

class PublicApiTravel(BaseModel):
    serviceKey: str 
    numOfRows: str = "100"
    pageNo: str = "1"
    MobileOS: str = 'ETC'
    MobileApp: str = 'AppTest'
    _type: str = 'json'
    listYN: str = 'Y'
    arrange: str = 'A'
    contentTypeId: str
    areaCode: str
    sigunguCode: str
    
