from .load_parquet import LoadParquet


class CasamentosDAO:

    filename = 'casamentos_final.parquet'

    def __init__(self):

        self.load_parquet = LoadParquet()
        self.data = self.load_dict_data()      

    def load_dict_data(self)->dict:

        df = self.load_parquet(self.filename)

        return df.to_dict(orient='records')
    
    def casamentos_sp_com_mun(self, municipio:str, ano:int)->dict:

        for record in self.data:
            if record['nome_municipio_destino']==municipio and record['ano']==ano:
                return record
        else:
            raise ValueError(f'Municipio {municipio} não encontrado')

