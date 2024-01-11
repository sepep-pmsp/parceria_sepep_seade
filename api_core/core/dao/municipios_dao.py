from pandas import DataFrame
from .load_parquet import LoadParquet


class MunicipiosDAO:

    filename = 'municipios_final.parquet'

    def __init__(self):

        self.load_parquet = LoadParquet()
        self.data = self.load_dict_data()

    def padronizar_col(self, col:str)->str:

        col = col.lower()
        col = col.replace(' ', '_')

        return col

    def padronizar_all_cols(self, df:DataFrame)->DataFrame:

        rename = {col : self.padronizar_col(col) for col in df.columns}

        rename['nome_municipio'] = 'municipio'

        df = df.rename(rename, axis=1)

        print(df.columns)

        return df

    def load_dict_data(self)->dict:

        df = self.load_parquet(self.filename)
        df = self.padronizar_all_cols(df)

        return df.to_dict(orient='records')
    
    def dados_municipio_all(self, municipio:str, ano:int)->dict:

        for record in self.data:
            if record['municipio']==municipio and record['ano']==ano:
                return record
        
        else:
            raise ValueError(f'Municipio {municipio} não encontrado')

    def padronizar_dados(self, dados:dict, target_col:str)->dict:

        renomear = {
                'ano' : 'ano',
                'municipio' : 'municipio',
                target_col : 'valor'
                    }
        
        return {renomear[col] : value for col, value in dados.items()}
        
    def filter_dados(self, dados:dict, target_col:str)->dict:

        cols_index = (
                'municipio', 
                'ano'
                )
        
        filtrado = {col : val for col, val in dados.items() if col
                    in cols_index or col ==target_col}
        
        return self.padronizar_dados(filtrado, target_col)

    def regiao_administrativa(self, municipio:str, ano:int)->dict:

        dados = self.dados_municipio_all(municipio, ano)
        
        return self.filter_dados(dados, 'regiao_administrativa')

    def regiao_metropolitana(self, municipio:str, ano:int)->dict:

        dados = self.dados_municipio_all(municipio, ano)
        
        return self.filter_dados(dados, 'regiao_metropolitana')

    def pib(self, municipio:str, ano:int)->dict:
        
        dados = self.dados_municipio_all(municipio, ano)
        
        return self.filter_dados(dados, 'valor_do_pib')
    
    def habitantes(self, municipio:str, ano:int)->dict:
        
        dados = self.dados_municipio_all(municipio, ano)

        print(dados)
        
        return self.filter_dados(dados, 'habitantes_do_município')
    
    def nascidos_vivos(self, municipio:str, ano:int)->dict:
        
        dados = self.dados_municipio_all(municipio, ano)
        
        return self.filter_dados(dados, 'nascidos_vivos')