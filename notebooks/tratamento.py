import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

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

def normalizando_dados(df,colunas_numericas =None):
     if colunas_numericas is None:
          colunas_numericas = ['velocity', 'direction', 'temperature', 'humidity']##alterar diante das colunas quando tivermos os dados
          scaler = MinMaxScaler()
          df_normalizado = df.copy()
          df_normalizado[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])
          return df_normalizado, scaler