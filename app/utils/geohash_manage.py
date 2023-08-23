# import pygeohash as pgh
# import geopandas as gpd
# from shapely.geometry import Polygon
# from src.model.spatial_model import *

# class GeohashManage:
#     def __init__(self,precision=4,**kwargs):
#         '''
#         R-Tree를 이요안 geohash를 관리 하는 클래스
#         '''
#         ## input_type : geohash, area, center
#         self.precision=precision
#         self.gen_polygon(**kwargs)
#         self.geohashset=[]
    
#     def gen_polygon(self,**kwargs):
#         ## input_type : circle, rect, polygon
#         if "circle" in kwargs.keys():
#             dicts=kwargs["circle"]
#             circle=CircleShape(**dicts)            
            
#         elif "rect" in kwargs.keys():
#             dicts=kwargs["rect"]
#             rect=RectShape(**dicts)

#         elif "polygon" in kwargs.keys():
#             dicts=kwargs["polygon"]
#             self.polygon=Polygon(dicts["coords"])
#         else:
#             raise ValueError("input_type is not defined")
    

            






        
    
    


    

        
