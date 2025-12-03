"""
Database Service
===============

Serviços para conexão com banco de dados.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Optional

def get_db_connection():
    """
    Obter conexão com banco PostgreSQL.
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5433"),
            database=os.getenv("POSTGRES_DB", "avd_wind_data"),
            user=os.getenv("POSTGRES_USER", "user"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar com banco: {e}")
        return None