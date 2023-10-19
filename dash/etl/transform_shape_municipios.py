from .extract_shape_municipios import Extractor
import geopandas as gpd

class Transformer:

    columns = {
        'CD_MUN' : 'cd_municipio_ibge',
        'NM_MUN' : 'nome_municipio',
        'geometry' : 'geometry'
    }

    def __init__(self, verbose:bool=True)->None:

        self.extract = Extractor(verbose)

    def filter_columns(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        return gdf[self.columns.keys()]
    
    def rename_columns(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        return gdf.rename(self.columns, axis=1)
    
    def to_sirgas_2000_utm_23_s(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        return gdf.to_crs(epsg=31983)
    
    def centroid(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        gdf = gdf.copy()
        gdf.geometry = gdf.centroid

        return gdf
    
    def to_wgs_84(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        return gdf.to_crs(epsg=4326)
    
    def cd_municipio_ibge_to_int(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        gdf = gdf.copy()

        gdf['cd_municipio_ibge'] = gdf['cd_municipio_ibge'].astype(int)

        return gdf
    
    def geometry_to_lat_lon(self, gdf:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        gdf = gdf.copy()

        gdf['lon'] = gdf.geometry.x
        gdf['lat'] = gdf.geometry.y

        gdf.drop('geometry', axis=1, inplace=True)

        return gdf
    
    def pipeline(self):

        gdf = self.extract()
        gdf = self.filter_columns(gdf)
        gdf = self.rename_columns(gdf)
        gdf = self.to_sirgas_2000_utm_23_s(gdf)
        gdf = self.centroid(gdf)
        gdf = self.to_wgs_84(gdf)
        gdf = self.cd_municipio_ibge_to_int(gdf)
        gdf = self.geometry_to_lat_lon(gdf)

        return gdf
    
    def __call__(self)->gpd.GeoDataFrame:

        return self.pipeline()