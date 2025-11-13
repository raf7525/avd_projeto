#!/usr/bin/env python3
"""
Script para análise básica dos dados meteorológicos processados de 2011
"""

import pandas as pd
import numpy as np

def analisar_dados():
    """
    Faz uma análise exploratória básica dos dados processados
    """
    # Carregar os dados
    caminho_dados = '/home/rafaelbarros/QuartoPeriodo/Quinto-periodo/avd/data/dados_processados_2011.csv'
    
    try:
        df = pd.read_csv(caminho_dados)
        
        print("="*60)
        print("ANÁLISE DOS DADOS METEOROLÓGICOS 2011")
        print("="*60)
        
        # Informações básicas
        print("\n📊 INFORMAÇÕES GERAIS:")
        print(f"   Total de registros: {len(df)}")
        print(f"   Total de colunas: {len(df.columns)}")
        print(f"   Período: {df['datetime'].min()} até {df['datetime'].max()}")
        
        # Converter datetime
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Contagem por estados
        print("\n🗺️  DISTRIBUIÇÃO POR ESTADO:")
        estados = df['estado'].value_counts()
        for estado, count in estados.head(10).items():
            print(f"   {estado}: {count} registros")
        
        # Contagem por cidades
        print("\n🏙️  PRINCIPAIS CIDADES (Top 10):")
        cidades = df['cidade'].value_counts()
        for cidade, count in cidades.head(10).items():
            print(f"   {cidade}: {count} registros")
        
        # Estatísticas das variáveis meteorológicas
        print("\n🌡️  ESTATÍSTICAS METEOROLÓGICAS:")
        
        vars_numericas = ['temperatura', 'umidade', 'pressao', 'precipitacao', 'velocidade_vento']
        
        for var in vars_numericas:
            if var in df.columns:
                stats = df[var].describe()
                print(f"\n   {var.upper()}:")
                print(f"      Média: {stats['mean']:.2f}")
                print(f"      Min: {stats['min']:.2f}")
                print(f"      Max: {stats['max']:.2f}")
                print(f"      Desvio Padrão: {stats['std']:.2f}")
        
        # Dados faltantes
        print("\n❌ DADOS FALTANTES:")
        missing = df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                print(f"   {col}: {count} ({percentage:.1f}%)")
        
        # Resumo por mês
        print("\n📅 DISTRIBUIÇÃO TEMPORAL:")
        df['mes'] = df['datetime'].dt.month
        meses = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        
        distribucao_mes = df['mes'].value_counts().sort_index()
        for mes, count in distribucao_mes.items():
            print(f"   {meses[mes]}: {count} registros")
        
        print("\n" + "="*60)
        print("ANÁLISE CONCLUÍDA!")
        print("="*60)
        
        return df
        
    except Exception as e:
        print(f"Erro ao analisar os dados: {str(e)}")
        return None

if __name__ == "__main__":
    dados = analisar_dados()