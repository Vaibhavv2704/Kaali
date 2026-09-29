"""Open-source environmental features; no commercial place database dependency."""
import geopandas as gpd
import pandas as pd

def lighting_fraction(length, tags, complete=False):
    if not complete or not tags.isin(['yes','no']).all() or not length.sum():
        return None
    return float(length[tags.eq('yes')].sum()/length.sum())

def environmental_features(zones,pois,roads,metric_crs,*,road_inventory_complete=False):
    zones=zones.to_crs(metric_crs);pois=pois.to_crs(metric_crs);roads=roads.to_crs(metric_crs)
    rows=[]
    for _,z in zones.iterrows():
        local=pois[pois.geometry.within(z.geometry)];segments=roads[roads.geometry.intersects(z.geometry)]
        length=segments.geometry.intersection(z.geometry).length
        # Deliberately conservative: complex opening_hours strings need a proper parser.
        # 24/7 is an explicit open-late proxy; other strings remain unknown.
        late=local.get('opening_hours',pd.Series(index=local.index,dtype=str)).eq('24/7')
        # A help-layer query selects lit=yes roads only. Its denominator cannot
        # support a lighting fraction. Even a complete road inventory needs
        # known yes/no lighting tags for every intersecting segment.
        tags=segments.get('lit',pd.Series(index=segments.index,dtype=str))
        row={'neighbourhood_id':z['id'],'poi_density':len(local)/max(z.geometry.area/1e6,1e-6),'open_late_density':int(late.sum())/max(z.geometry.area/1e6,1e-6),'lighting':lighting_fraction(length,tags,road_inventory_complete)}
        for kind in ['police','metro']:
            points=pois[pois['kind']==kind]
            row[f'distance_{kind}']=float(points.distance(z.geometry.centroid).min()) if len(points) else None
        row['distance_main_road']=float(roads.distance(z.geometry.centroid).min()) if len(roads) else None
        rows.append(row)
    return pd.DataFrame(rows)
