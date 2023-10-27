from .extract import Extractor
from .load_shape_municipios import Load
import pandas as pd
from typing import Tuple

class Transformer:

    colunas_mapper = {
        'anoreferencia' : 'ano_casamento',
        'codrescj1' : 'cod_residencia_cj1',
        'codrescj2' : 'cod_residencia_cj2',
    }

    codigo_ibge_estado_sp = 35
    codigo_ibge_cidade_sp = 3550308

    def __init__(self, verbose:bool=True):

        self.extract = Extractor()
        self.resources_gen = self.extract()
        self.load_shape = Load(verbose)

        self.shp_mun = self.load_shape()

    def filter_cols(self, df:pd.DataFrame)->pd.DataFrame:

        return df[self.colunas_mapper.keys()]
    
    def rename_cols(self, df:pd.DataFrame)->pd.DataFrame:

        return df.rename(self.colunas_mapper, axis=1)
    
    def __filter(self, df:pd.DataFrame, filtro:Tuple[bool])->pd.DataFrame:

        df_filtrado = df[filtro].copy().reset_index(drop=True)

        return df_filtrado

    def filtrar_casamentos_paulistanos(self, df:pd.DataFrame)->pd.DataFrame:

        filtro = ((df['cod_residencia_cj1']==self.codigo_ibge_cidade_sp)|
                  (df['cod_residencia_cj2']==self.codigo_ibge_cidade_sp))
        
        df_filtrado = self.__filter(df, filtro)

        return df_filtrado
    
    def remover_casamentos_sp_para_sp(self, df:pd.DataFrame)->pd.DataFrame:

        filtro = (
                (df['cod_residencia_cj1']==self.codigo_ibge_cidade_sp)
                &
                (df['cod_residencia_cj2']==self.codigo_ibge_cidade_sp)
                )
        
        df_filtrado = self.__filter(df, ~filtro)

        return df_filtrado
    
    def casamentos_com_sp_na_origem(self, df:pd.DataFrame)->pd.DataFrame:

        cj1_sp = df[df['cod_residencia_cj1']==self.codigo_ibge_cidade_sp].copy()
        cj2_sp = df[df['cod_residencia_cj2']==self.codigo_ibge_cidade_sp].copy()


        cj1_sp['origem'] = cj1_sp['cod_residencia_cj1']
        cj2_sp['origem'] = cj2_sp['cod_residencia_cj2']

        cj1_sp['destino'] = cj1_sp['cod_residencia_cj2']
        cj2_sp['destino'] = cj2_sp['cod_residencia_cj1']

        colunas = ['origem', 'destino', 'ano_casamento']

        cj1_sp = cj1_sp[colunas]
        cj2_sp = cj2_sp[colunas]

        final = pd.concat([cj1_sp, cj2_sp], axis=0)

        return final


    def contagem_casamentos_destino(self, df:pd.DataFrame)->pd.DataFrame:


        #pegando o ano para colocar depois
        ano = df['ano_casamento'].unique()[0]

        df['total_casamentos']=1
        df = df.groupby(['origem', 'destino']).sum().reset_index()[['origem', 'destino', 'total_casamentos']]

        #colocando o ano
        df['ano'] = ano

        return df
    
    def casamentos_destino_no_estado_sp(self, df:pd.DataFrame)->pd.DataFrame:

        filtro = df['destino'].astype(str).str.startswith(f'{self.codigo_ibge_estado_sp}')

        filtrado = self.__filter(df, filtro)

        return filtrado
    
    def lat_lon_destino(self, df:pd.DataFrame)->pd.DataFrame:

        merged = pd.merge(self.shp_mun, df, left_on='cd_municipio_ibge', right_on='destino', how='right')
        merged.drop('cd_municipio_ibge', axis=1, inplace=True)

        merged.rename({'lat' : 'lat_destino', 'lon' : 'lon_destino',
                       'nome_municipio' : 'nome_municipio_destino'},
                      axis=1, inplace=True)

        return merged
    
    def lat_lon_origem(self, df:pd.DataFrame)->pd.DataFrame:

        df = df.copy()
        
        sp = self.shp_mun[self.shp_mun['cd_municipio_ibge']==3550308]
        lon = sp['lon'].values[0]
        lat = sp['lat'].values[0]

        df['lon_origem'] = lon
        df['lat_origem'] = lat

        return df
    
    def dropar_estado_sp(self, df:pd.DataFrame)->pd.DataFrame:

        df = df[df['destino']!=3500000].reset_index(drop=True)

        return df

    def pipeline(self, df:pd.DataFrame)->pd.DataFrame:

        df = self.filter_cols(df)
        df = self.rename_cols(df)
        df = self.filtrar_casamentos_paulistanos(df)
        df = self.remover_casamentos_sp_para_sp(df)
        df = self.casamentos_com_sp_na_origem(df)
        df = self.contagem_casamentos_destino(df)
        df = self.casamentos_destino_no_estado_sp(df)
        df = self.lat_lon_destino(df)
        df = self.lat_lon_origem(df)
        df = self.dropar_estado_sp(df)

        return df
    
    def __call__(self)->pd.DataFrame:

        for df in self.resources_gen:
            yield self.pipeline(df)