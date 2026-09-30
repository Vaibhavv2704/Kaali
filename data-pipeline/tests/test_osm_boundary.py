import sys,unittest
from pathlib import Path
from shapely.geometry import Point
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from osm_boundary import relation_polygon,assign_help


def fixture():
    coords=[(0,0),(4,0),(4,4),(0,4),(0,0)]
    return {'elements':[{'type':'relation','id':1,'tags':{'ISO3166-2':'TEST','boundary':'administrative','admin_level':'4'},
                         'members':[{'type':'way','role':'outer','ref':2,'geometry':[{'lon':x,'lat':y} for x,y in coords]}]}]}


class BoundaryTests(unittest.TestCase):
    def test_rejects_partial_geometry_and_wrong_identity(self):
        data=fixture()
        with self.assertRaises(ValueError):relation_polygon(data,1,'WRONG')
        data['elements'][0]['members'][0]['geometry'].pop()
        with self.assertRaises(ValueError):relation_polygon(data,1,'TEST')

    def test_preserves_holes(self):
        data=fixture();data['elements'][0]['members'].append({'type':'way','role':'inner','ref':3,
            'geometry':[{'lon':x,'lat':y} for x,y in [(1,1),(2,1),(2,2),(1,2),(1,1)]]})
        polygon,_=relation_polygon(data,1,'TEST')
        self.assertFalse(polygon.contains(Point(1.5,1.5)))
        self.assertTrue(polygon.contains(Point(3,3)))

    def test_help_assignment_excludes_edges_and_crossing_roads(self):
        polygon,_=relation_polygon(fixture(),1,'TEST')
        geoms=[{'type':'Point','coordinates':[2,2]},{'type':'Point','coordinates':[0,2]},
               {'type':'LineString','coordinates':[[2,2],[5,2]]}]
        data={'features':[{'geometry':g,'properties':{'cityId':''}} for g in geoms]}
        result,count=assign_help(data,polygon,'fixture')
        self.assertEqual(count,1);self.assertEqual([f['properties']['cityId'] for f in result['features']],['fixture','',''])
        self.assertEqual(data['features'][0]['properties']['cityId'],'')


if __name__=='__main__':unittest.main()
