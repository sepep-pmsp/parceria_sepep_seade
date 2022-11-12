import pandas as pd


class Transform:

    columns = ['municipio', 
                'agropecuaria', 
                'industria',
                'servicos_administracao_publica', 
                'servicos_total_sem_adm_publica',
                'total_geral', 
                'impostos', 
                'PIB', 
                'PIB_per_capita']

    def set_columns(self, df: pd.DataFrame)->pd.DataFrame:
    
        df = df.copy()
        
        
        
        df.columns = self.columns
        
        return df

    def upper_bound(self, df: pd.DataFrame)->pd.DataFrame:
    
        df = df.loc[11:].copy()
        
        return df
    
    def get_lower_bound_idx_fonte(self, df:pd.DataFrame)->pd.DataFrame:
    
        col_fonte = df['municipio'].astype(str).str.lower()
        mask_fonte = col_fonte.str.contains('fonte: ')
        index_fonte = df[mask_fonte].index[0]
        
        idx_final = index_fonte-2
        
        return idx_final

    def get_lower_bound_idx_Zacarias(self, df: pd.DataFrame)->pd.DataFrame:
    
        col_fonte = df['municipio'].astype(str).str.lower()
        mask_fonte = col_fonte=='zacarias'
        idx_final = df[mask_fonte].index[0]
            
        return idx_final

    def lower_bound(self, df: pd.DataFrame)->pd.DataFrame:

        try:
            idx_final = self.get_lower_bound_idx_fonte(df)
        except IndexError:
            idx_final = self.get_lower_bound_idx_Zacarias(df)
        return df.loc[:idx_final].copy()

    def bound_data(self, df:pd.DataFrame)->pd.DataFrame:
    
        df = self.upper_bound(df)
        df = self.lower_bound(df)
        
        return df.reset_index(drop=True).copy()

    def col_to_float(self, df:pd.DataFrame)->pd.DataFrame:
    
        df = df.copy()
        for col in df.columns:
            if col!='municipio':
                df[col] = df[col].astype(float)
        return df

    def multiply_by_thousands(self, df:pd.DataFrame)->pd.DataFrame:
        '''Valores do PIB nos arquivos originais estão em mil reais.
        Vamos colocar na unidade padrão, em Reais, para facilitar análises futuras.'''

        df = df.copy()
        skip_cols = {'municipio', 'ano'}
        for col in df.columns:
            if col not in skip_cols:
                df[col] = df[col] * 1000
        return df

    def add_year_column(self, df:pd.DataFrame, ano: str)->pd.DataFrame:

        df = df.copy()
        df['ano'] = ano

        return df

    def transform(self, df:pd.DataFrame, ano:str)->pd.DataFrame:
    
        df = self.set_columns(df)
        df = self.bound_data(df)
        df = self.col_to_float(df)
        df = self.add_year_column(df, ano)
        df = self.multiply_by_thousands(df)
        
        return df

    def __call__(self, df:pd.DataFrame, ano:str)->pd.DataFrame:

        return self.transform(df, ano)
