"""Jurisdiction-aware spatial transforms; never infer jurisdiction from a city centre."""
import numpy as np
import geopandas as gpd
import h3
from shapely.geometry import Polygon

def neighbourhood_grid(jurisdictions, resolution=8):
    if resolution not in (8, 9):
        raise ValueError('Use H3 resolution 8 or 9')
    jurisdictions = jurisdictions.to_crs(4326)
    records = []
    for _, row in jurisdictions.iterrows():
        # Include intersecting edge cells using overlap containment, then clip exactly.
        shape = h3.geo_to_h3shape(row.geometry.__geo_interface__)
        for cell in h3.h3shape_to_cells_experimental(shape, resolution, contain='overlap'):
            polygon = Polygon([(lng, lat) for lat, lng in h3.cell_to_boundary(cell)])
            clipped = polygon.intersection(row.geometry)
            if clipped.is_empty or clipped.area == 0:
                continue
            records.append({'id':f"{row['city_id']}:{cell}", 'city_id':row['city_id'], 'geometry':clipped})
    return gpd.GeoDataFrame(records, crs=4326)

def assign_incidents(incidents, zones):
    matched = gpd.sjoin(incidents.to_crs(zones.crs), zones[['id','city_id','geometry']], how='left', predicate='within')
    if matched.index.duplicated().any():
        raise ValueError('Overlapping neighbourhoods: ambiguous incident assignment')
    # Border points and unmatched records remain unmatched for manual review.
    return matched

def allocate(count, cells):
    """Cells must already be clipped to ONE official reporting unit."""
    if not np.isfinite(count) or count < 0:
        raise ValueError('Invalid count')
    weights = np.zeros(len(cells))
    for field, importance in [('area',.2),('female_population',.6),('road_length',.2)]:
        values = np.asarray(cells[field], dtype=float)
        if not np.isfinite(values).all() or (values < 0).any():
            raise ValueError(f'Invalid {field}')
        if values.sum() > 0:
            weights += importance * values / values.sum()
    if weights.sum() == 0:
        raise ValueError('No allocation evidence')
    return count * weights / weights.sum()
