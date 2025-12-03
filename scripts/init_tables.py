import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def get_db_connection(db_name="avd_wind_data"):
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5433"),
        database=db_name,
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password")
    )

def create_database():
    try:
        # Connect to default 'postgres' database to create new db
        conn = get_db_connection(db_name="postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'avd_wind_data'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute('CREATE DATABASE avd_wind_data')
            print("Database 'avd_wind_data' created successfully!")
        else:
            print("Database 'avd_wind_data' already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def init_tables():
    create_database()
    
    commands = (
        """
        CREATE TABLE IF NOT EXISTS thermal_measurements (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            temperature FLOAT NOT NULL,
            humidity FLOAT NOT NULL,
            wind_velocity FLOAT NOT NULL,
            pressure FLOAT NOT NULL,
            solar_radiation FLOAT NOT NULL,
            thermal_sensation FLOAT,
            comfort_zone VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("Tables created successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating tables: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # Wait for DB to be ready if running in docker-compose startup
    # time.sleep(5) 
    init_tables()
