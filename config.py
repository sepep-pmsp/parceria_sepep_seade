
import os
from dotenv import load_dotenv 

class MissingEnvironmentVariable(Exception):
    pass

def get_my_env_var(var_name):

    #carrega valores do .env para quando rodar fora do docker
    load_dotenv()

    envvar = os.environ.get(var_name)
    if envvar is None:
        raise MissingEnvironmentVariable(f"ENV '{var_name}' must be set")
    return envvar

def anchor_folder(folder:str)->str:


    path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(path, folder)

def create_folder_if_not_exists(folder:str)->str:

    if not os.path.exists(folder):
        os.mkdir(folder)

    return folder


CKAN_DOMAIN = get_my_env_var('CKAN_DOMAIN')
DATA_FOLDER = create_folder_if_not_exists(anchor_folder(get_my_env_var('DATA_FOLDER')))
MAPBOX_ACCESS_TOKEN = get_my_env_var('MAPBOX_ACCESS_TOKEN')