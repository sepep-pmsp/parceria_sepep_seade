from .transform_shape_municipios import Transformer
import os
import geopandas as gpd
from config import DATA_FOLDER

class Load:

    folder = 'shp_municipios'
    file_final = 'municipios_final.parquet'

    def __init__(self, verbose:bool=True):

        self.transform = Transformer(verbose)
        self.folder_path = os.path.join(DATA_FOLDER, self.folder)
        self.__create_folder_if_not_exists(self.folder_path)
        self.file_final_path = os.path.join(self.folder_path, self.file_final)

    def __create_folder_if_not_exists(self, folder:str)->None:

        if not os.path.exists(folder):
            os.mkdir(folder)

    def load_file_final(self)->gpd.GeoDataFrame:

        return gpd.read_parquet(self.file_final_path)
    
    def save_file_final(self, gdf:gpd.GeoDataFrame)->None:

        gdf.to_parquet(self.file_final_path)

    def pipeline(self)->gpd.GeoDataFrame:

        if os.path.exists(self.file_final_path):
            return self.load_file_final()
        
        gdf = self.transform()

        self.save_file_final(gdf)

        return gdf
