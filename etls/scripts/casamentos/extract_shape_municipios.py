
from etls.utils.file_cache import FileCache
from io import BytesIO
from zipfile import ZipFile
import geopandas as gpd
from config import DATA_FOLDER
import os


class Extractor:

    url_shp_sp =('https://geoftp.ibge.gov.br/organizacao_do_territorio/'
                'malhas_territoriais/malhas_municipais/municipio_2022/UFs/'
                'SP/SP_Municipios_2022.zip')
    
    folder = 'shp_municipios'

    def __init__(self, verbose=True)->None:

        self.folder_path = os.path.join(DATA_FOLDER, self.folder)
        self.__create_folder_if_not_exists(self.folder_path)

        self.file_cache = FileCache(verbose)
        self.zip_file_path = os.path.join(self.folder_path, 'municipios_sp.zip')
        self.shp_file_path = os.path.join(self.folder_path, 'shp_municipios')

        self.__create_folder_if_not_exists(self.shp_file_path)

    def __create_folder_if_not_exists(self, folder:str)->None:

        if not os.path.exists(folder):
            os.mkdir(folder)
    
    def load_zip(self)->BytesIO:

        return self.file_cache(self.zip_file_path, self.url_shp_sp, binary=True)
    
    def unzip(self, zip_data:BytesIO)->BytesIO:

        zf = ZipFile(zip_data)

        zf.extractall(self.shp_file_path)


    def check_if_shape_exists(self):

        shp_file = [f for f in os.listdir(self.shp_file_path) if f.endswith('shp')]

        if shp_file:
            return True
        return False
    
    def load_shape(self)->gpd.GeoDataFrame:

        if self.check_if_shape_exists():
            return gpd.read_file(self.shp_file_path)
        
        zip_data = self.load_zip()
        self.unzip(zip_data)

        return gpd.read_file(self.shp_file_path)
    
    def __call__(self):

        return self.load_shape()




    

        


        

