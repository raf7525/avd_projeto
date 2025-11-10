def endpoint(
    path_param: int,                    # /user/{path_param}
    query_param: str = Query("default"), # ?query_param=valor
    body_data: MyModel                  # JSON no body
):import pandas as pd
import numpy as np


def removendo_duplicadas(df):
    return df.drop_duplicates()

def padronizando_coluas(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df

def tratando_linhas_nulas(df):
    return df.dropna()
##caso não se tenha muitos dados, adicionar um cálculo de fazer a média com base em caracteristicas



##eh necessario checar se a remocao de outliers eh o ideal, talvez eles sejam importantes
def remove_outliers(df, column,factor=1.5):
        Q1 = df[column].quantile(0.25)##esses valores são o máximo e mínimo aceitáveis, talvez seja necessário mudar diante da necessidade
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - factor * IQR
        limite_maximo = Q3 + factor * IQR
        return df[(df[column] >= limite_inferior) & (df[column] <= limite_maximo)]