import os
from django.contrib.gis.utils import LayerMapping

from .models import Ward


wards_path = os.path.join(
    os.getcwd(), 'spatial_data', 'market_wards.shp'
)

# Auto-generated `LayerMapping` dictionary for Ward model
ward_mapping = {
    'county': 'county',
    'sub_county': 'sub_county',
    'ward': 'ward',
    'geom': 'MULTIPOLYGON',
}


def run(verbose=True):
    layermap = LayerMapping(
        Ward,
        wards_path,
        ward_mapping,
        transform=False #the shapeﬁle is already in wgs84
    )
    layermap.save(strict=True,verbose=verbose)