import pandas as pd
import numpy as np
import os
import glob
from sklearn.preprocessing import MinMaxScaler

def removendo_duplicadas(df):
    return df.drop_duplicates()

def padronizando_colunas(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df

def tratando_linhas_nulas(df):
    return df.dropna()
##caso não se tenha muitos dados, adicionar um cálculo de fazer a média com base em caracteristicas

##eh necessario checar se a remocao de outliers eh o ideal, talvez eles sejam importantes
def remove_outliers(df, column, factor=1.5):
    Q1 = df[column].quantile(0.25)##esses valores são o máximo e mínimo aceitáveis, talvez seja necessário mudar diante da necessidade
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - factor * IQR
    limite_maximo = Q3 + factor * IQR
    return df[(df[column] >= limite_inferior) & (df[column] <= limite_maximo)]

def normalizando_dados(df, colunas_numericas=None):
    if colunas_numericas is None:
        colunas_numericas = ['velocidade_vento', 'direcao_vento', 'temperatura', 'umidade', 'pressao']
    scaler = MinMaxScaler()
    df_normalizado = df.copy()
    df_normalizado[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])
    return df_normalizado, scaler

def ler_dados_inmet(arquivo_csv):
    """
    Lê os dados do INMET, pulando as linhas de metadados
    """
    # Ler o arquivo pulando as primeiras 8 linhas (metadados)
    df = pd.read_csv(arquivo_csv, sep=';', skiprows=8, encoding='latin-1')
    
    # Remover a última linha que geralmente está vazia
    df = df.dropna(how='all')
    
    return df

def processar_dados_inmet(df):
    """
    Processa e limpa os dados do INMET
    """
    # Renomear colunas para facilitar o trabalho
    colunas_novas = {
        'DATA (YYYY-MM-DD)': 'data',
        'HORA (UTC)': 'hora',
        'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'precipitacao',
        'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'pressao',
        'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'temperatura',
        'UMIDADE RELATIVA DO AR, HORARIA (%)': 'umidade',
        'VENTO, DIREÇÃO HORARIA (gr) (° (gr))': 'direcao_vento',
        'VENTO, VELOCIDADE HORARIA (m/s)': 'velocidade_vento',
        'RADIACAO GLOBAL (KJ/m²)': 'radiacao'
    }
    
    # Aplicar novos nomes se as colunas existirem
    df = df.rename(columns=colunas_novas)
    
    # Selecionar apenas as colunas de interesse
    colunas_interesse = ['data', 'hora', 'precipitacao', 'pressao', 'temperatura', 
                        'umidade', 'direcao_vento', 'velocidade_vento', 'radiacao']
    
    # Manter apenas colunas que existem
    colunas_existentes = [col for col in colunas_interesse if col in df.columns]
    df = df[colunas_existentes]
    
    # Criar coluna datetime combinando data e hora
    if 'data' in df.columns and 'hora' in df.columns:
        df['datetime'] = pd.to_datetime(df['data'] + ' ' + df['hora'])
        df = df.drop(['data', 'hora'], axis=1)
    
    # Converter colunas numéricas
    colunas_numericas = ['precipitacao', 'pressao', 'temperatura', 'umidade', 
                        'direcao_vento', 'velocidade_vento', 'radiacao']
    
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Substituir valores inválidos (-9999) por NaN
    df = df.replace(-9999, np.nan)
    
    return df

def processar_todos_dados_2011():
    """
    Processa todos os arquivos CSV de 2011
    """
    # Caminho para os dados
    caminho_dados = '/home/rafaelbarros/QuartoPeriodo/Quinto-periodo/avd/data/2011/'
    
    # Lista todos os arquivos CSV
    arquivos_csv = glob.glob(os.path.join(caminho_dados, '*.CSV'))
    
    print(f"Encontrados {len(arquivos_csv)} arquivos para processar")
    
    dados_processados = []
    
    for arquivo in arquivos_csv:
        try:
            print(f"Processando: {os.path.basename(arquivo)}")
            
            # Extrair informações do nome do arquivo
            nome_arquivo = os.path.basename(arquivo)
            partes = nome_arquivo.replace('.CSV', '').split('_')
            estado = partes[1] + '_' + partes[2]  # CO_DF, CO_GO, etc.
            estacao = partes[3]  # A001, A002, etc.
            cidade = '_'.join(partes[4:-4])  # Nome da cidade
            
            # Ler e processar dados
            df = ler_dados_inmet(arquivo)
            df_processado = processar_dados_inmet(df)
            
            # Adicionar informações da estação
            df_processado['estado'] = estado
            df_processado['estacao'] = estacao
            df_processado['cidade'] = cidade
            
            # Aplicar funções de tratamento
            df_processado = removendo_duplicadas(df_processado)
            df_processado = padronizando_colunas(df_processado)
            
            dados_processados.append(df_processado)
            
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {str(e)}")
            continue
    
    # Concatenar todos os dados
    if dados_processados:
        df_final = pd.concat(dados_processados, ignore_index=True)
        
        # Tratamento final
        print("Aplicando tratamentos finais...")
        df_final = tratando_linhas_nulas(df_final)
        
        # Salvar dados processados
        caminho_saida = '/home/rafaelbarros/QuartoPeriodo/Quinto-periodo/avd/data/dados_processados_2011.csv'
        df_final.to_csv(caminho_saida, index=False)
        
        print(f"Dados processados salvos em: {caminho_saida}")
        print(f"Total de registros: {len(df_final)}")
        print(f"Colunas disponíveis: {list(df_final.columns)}")
        
        return df_final
    
    else:
        print("Nenhum dado foi processado com sucesso")
        return None

# Executar o processamento se o script for executado diretamente
if __name__ == "__main__":
    df_resultado = processar_todos_dados_2011()