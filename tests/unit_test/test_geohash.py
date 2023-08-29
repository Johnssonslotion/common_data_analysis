import pygeohash as pgh
import pytest



@pytest.mark.parametrize("geohash,expected_x,expected_y",[("wyd",1.40625,1.40625),("wydb",0.17578125,0.3515625),("wydbb",0.0439453125,0.0439453125),("wydbbb",0.0054931640625,0.010986328125),("wydbbbb",0.001373291015625,0.001373291015625)])
def test_geohash(geohash,expected_x,expected_y):
    '''
    3:=1.40625:1.40625
    4:=0.17578125:0.3515625
    5:=0.0439453125:0.0439453125
    6:=0.0054931640625:0.010986328125
    7:=0.001373291015625:0.001373291015625
    '''
    ##
    ret=pgh.decode_exactly(geohash)
    print(ret)
    assert ret[2]*2 == expected_x,f"x is not matched, input:{geohash}, ret:{ret}, expected_x:{expected_x}"
    assert ret[3]*2 == expected_y,f"y is not matched, input:{geohash}, ret:{ret}, expected_x:{expected_y}"

        
    