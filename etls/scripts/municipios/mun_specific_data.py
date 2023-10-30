from core.ckan_api_reader import Ckan
import pandas as pd
from config import CKAN_DOMAIN

ckan = Ckan(CKAN_DOMAIN)

population_package = ckan('populacao-municipal-2010-2022', search_string='2021', attr='name', how='contains', as_list=True, extract=True, parser_params={'sep': ';'})[0]
pib_package =  ckan('pib-municipal-2002-2020', search_string='PIB Municipal 2002 a 2020', attr='name', how='contains', as_list=True, extract=True, parser_params={'sep': ';'})[0]
born_alive_package = ckan('estatisticas-vitais', search_string='Nascidos Vivos por sexo - 2021', attr='name', how='contains', as_list=True, extract=True, parser_params={'sep': ';'})[0]
country_code_package = ckan('microdados-casamentos', search_string='códigos de países', how='contains', extract=True, as_list=True, parser_params={'sep' : ';'})[0]

population_package_filter = (population_package['ano'] == 2021)
pib_package_filter = (pib_package['Setor'] == 'PIB')
born_alive_package_filter = (born_alive_package[' '] == 2021)
country_code_package_filter = ((country_code_package['ra_desc'] != 'SP - Município ignorado') & (country_code_package['uf'] == 35))

population_package = population_package[population_package_filter].filter(['cod_ibge', 'populacao'], axis=1)
pib_package = pib_package [pib_package_filter].filter(['Cod_Ibge', 'Valor'], axis=1)
born_alive_package = born_alive_package [born_alive_package_filter].filter(['Código IBGE', 'Nascidos vivos'], axis=1)
country_code_package = country_code_package[country_code_package_filter]

population_package.columns =['cod_municipio', 'habitantes']
pib_package.columns =['cod_municipio', 'PIB']
born_alive_package.columns =['cod_municipio', 'nascidos_vivos']
colunas = {
    'cod_pais' : 'cod_municipio',
    'nome_pais' : 'nome_municipio',
    'ra_desc' : 'regiao_administrativa',
    'rm_desc' : 'regiao_metropolitana'
}
country_code_package = country_code_package[colunas.keys()].rename(colunas, axis=1)

population_package = population_package.reset_index(drop=True)
pib_package = pib_package.reset_index(drop=True)
born_alive_package = born_alive_package.reset_index(drop=True)
country_code_package = country_code_package.reset_index(drop=True)


#aqui já é outro transformer
dataframes = [population_package, pib_package, born_alive_package]

pivot = country_code_package.copy()

for df in dataframes:
    df['cod_municipio'] = pivot['cod_municipio'].astype(int)
    pivot = pd.merge(pivot, df, how='left', on='cod_municipio')



print(pivot)
pivot.to_csv('extra_dataframe.csv', sep=';')