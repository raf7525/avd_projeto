from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

from app.models.schemas import ThermalDataInput, ThermalDataOutput, APIResponse, ThermalDataBatch
from app.services.storage_service import StorageService
from app.services.database import get_db_connection

router = APIRouter()
storage_service = StorageService()

def calculate_thermal_sensation(temp, humidity, wind_speed, pressure=None, solar_radiation=None):
    # ... (implementation remains the same)
    import math
    
    if temp < 27:
        if wind_speed > 1.79:
            wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind_speed * 3.6)**0.16 + 0.3965 * temp * (wind_speed * 3.6)**0.16
            return round(wind_chill, 2)
        return round(temp, 2)
    
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 0.002211732
    c8 = 0.00072546
    c9 = -0.000003582
    
    heat_index = (c1 + (c2 * temp) + (c3 * humidity) + 
                 (c4 * temp * humidity) + (c5 * temp**2) + 
                 (c6 * humidity**2) + (c7 * temp**2 * humidity) + 
                 (c8 * temp * humidity**2) + (c9 * temp**2 * humidity**2))
    
    if wind_speed > 0:
        wind_factor = 1 - (wind_speed * 0.05)
        wind_factor = max(wind_factor, 0.7)
        heat_index *= wind_factor
    
    if solar_radiation is not None and solar_radiation > 200:
        solar_factor = 1 + (solar_radiation - 200) / 2000
        heat_index *= solar_factor
    
    return round(heat_index, 2)

def get_comfort_zone(thermal_sensation):
    if thermal_sensation < 16:
        return "Frio"
    elif thermal_sensation < 20:
        return "Fresco" 
    elif thermal_sensation < 26:
        return "Confortável"
    elif thermal_sensation < 30:
        return "Quente"
    else:
        return "Muito Quente"

@router.post("/", response_model=APIResponse)
async def create_thermal_data(thermal_data: ThermalDataInput, conn: RealDictCursor = Depends(get_db_connection)):
    try:
        data_dict = thermal_data.dict()
        
        thermal_sensation = calculate_thermal_sensation(
            temp=thermal_data.temperature, 
            humidity=thermal_data.humidity, 
            wind_speed=thermal_data.wind_velocity,
            pressure=thermal_data.pressure,
            solar_radiation=thermal_data.solar_radiation
        )
        comfort_zone = get_comfort_zone(thermal_sensation)
        
        data_dict.update({
            "created_at": datetime.now(),
            "thermal_sensation": thermal_sensation,
            "comfort_zone": comfort_zone
        })

        # Save to PostgreSQL
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO thermal_measurements 
                (timestamp, temperature, humidity, wind_velocity, pressure, solar_radiation, thermal_sensation, comfort_zone, created_at)
                VALUES (%(timestamp)s, %(temperature)s, %(humidity)s, %(wind_velocity)s, %(pressure)s, %(solar_radiation)s, %(thermal_sensation)s, %(comfort_zone)s, %(created_at)s)
                RETURNING id;
                """,
                data_dict
            )
            db_id = cur.fetchone()['id']
            data_dict["id"] = db_id
            conn.commit()

        # Save to MinIO (S3)
        try:
            s3_path = storage_service.save_json(data_dict)
            data_dict["s3_path"] = s3_path
        except Exception as e:
            print(f"Failed to save to S3: {e}")

        return APIResponse(
            success=True,
            message="Dados térmicos criados com sucesso",
            data=data_dict
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.post("/batch", response_model=APIResponse)
async def create_thermal_data_batch(batch_data: ThermalDataBatch, conn: RealDictCursor = Depends(get_db_connection)):
    try:
        created_records = []
        with conn.cursor() as cur:
            for item in batch_data.data:
                data_dict = item.dict()
                
                thermal_sensation = calculate_thermal_sensation(
                    temp=item.temperature, 
                    humidity=item.humidity, 
                    wind_speed=item.wind_velocity,
                    pressure=item.pressure,
                    solar_radiation=item.solar_radiation
                )
                comfort_zone = get_comfort_zone(thermal_sensation)
                
                data_dict.update({
                    "created_at": datetime.now(),
                    "thermal_sensation": thermal_sensation,
                    "comfort_zone": comfort_zone
                })

                cur.execute(
                    """
                    INSERT INTO thermal_measurements 
                    (timestamp, temperature, humidity, wind_velocity, pressure, solar_radiation, thermal_sensation, comfort_zone, created_at)
                    VALUES (%(timestamp)s, %(temperature)s, %(humidity)s, %(wind_velocity)s, %(pressure)s, %(solar_radiation)s, %(thermal_sensation)s, %(comfort_zone)s, %(created_at)s)
                    RETURNING id;
                    """,
                    data_dict
                )
                db_id = cur.fetchone()['id']
                data_dict["id"] = db_id
                
                # Offload S3 saving to background task if it becomes slow
                storage_service.save_json(data_dict)

                created_records.append(data_dict)
            
            conn.commit()

        return APIResponse(
            success=True,
            message=f"{len(created_records)} registros criados com sucesso",
            data={
                "created_count": len(created_records)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.get("/", response_model=APIResponse)
async def get_thermal_data(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_temp: Optional[float] = None,
    max_temp: Optional[float] = None,
    comfort_zone: Optional[str] = None,
    conn: RealDictCursor = Depends(get_db_connection)
):
    try:
        query_params = []
        where_clauses = []
        
        if start_date:
            where_clauses.append("timestamp >= %s")
            query_params.append(start_date)
        if end_date:
            where_clauses.append("timestamp <= %s")
            query_params.append(end_date)
        if min_temp is not None:
            where_clauses.append("temperature >= %s")
            query_params.append(min_temp)
        if max_temp is not None:
            where_clauses.append("temperature <= %s")
            query_params.append(max_temp)
        if comfort_zone:
            where_clauses.append("comfort_zone = %s")
            query_params.append(comfort_zone)

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        
        with conn.cursor() as cur:
            # Get total records for pagination
            cur.execute(f"SELECT COUNT(*) FROM thermal_measurements {where_sql}", query_params)
            total_records = cur.fetchone()['count']
            
            # Get paginated data
            query = f"""
                SELECT * FROM thermal_measurements 
                {where_sql}
                ORDER BY timestamp DESC
                LIMIT %s OFFSET %s
            """
            cur.execute(query, query_params + [limit, offset])
            records = cur.fetchall()

        return APIResponse(
            success=True,
            message="Dados recuperados com sucesso",
            data={
                "records": [ThermalDataOutput(**rec) for rec in records],
                "pagination": {
                    "total": total_records,
                    "limit": limit,
                    "offset": offset,
                    "has_next": offset + limit < total_records
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.get("/{thermal_id}", response_model=APIResponse)
async def get_thermal_data_by_id(thermal_id: int, conn: RealDictCursor = Depends(get_db_connection)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM thermal_measurements WHERE id = %s", (thermal_id,))
            record = cur.fetchone()
        
        if not record:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        return APIResponse(
            success=True,
            message="Registro encontrado",
            data=ThermalDataOutput(**record)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.delete("/{thermal_id}", response_model=APIResponse)
async def delete_thermal_data(thermal_id: int, conn: RealDictCursor = Depends(get_db_connection)):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM thermal_measurements WHERE id = %s RETURNING *;", (thermal_id,))
            deleted_record = cur.fetchone()
            conn.commit()

        if not deleted_record:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        return APIResponse(
            success=True,
            message="Registro deletado com sucesso",
            data=ThermalDataOutput(**deleted_record)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.get("/stats/summary", response_model=APIResponse)
async def get_thermal_stats(conn: RealDictCursor = Depends(get_db_connection)):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_records,
                    MIN(temperature) as min_temp,
                    MAX(temperature) as max_temp,
                    AVG(temperature) as avg_temp,
                    MIN(thermal_sensation) as min_thermal_sensation,
                    MAX(thermal_sensation) as max_thermal_sensation,
                    AVG(thermal_sensation) as avg_thermal_sensation
                FROM thermal_measurements;
            """)
            summary_stats = cur.fetchone()

            if summary_stats['total_records'] == 0:
                 return APIResponse(success=True, message="Nenhum dado disponível", data={"total_records": 0})

            cur.execute("""
                SELECT comfort_zone, COUNT(*) as count
                FROM thermal_measurements
                GROUP BY comfort_zone;
            """)
            comfort_zones = {row['comfort_zone']: row['count'] for row in cur.fetchall()}

        stats = {
            "total_records": summary_stats['total_records'],
            "temperature": {
                "min": summary_stats['min_temp'],
                "max": summary_stats['max_temp'],
                "avg": round(summary_stats['avg_temp'], 2) if summary_stats['avg_temp'] else None,
            },
            "thermal_sensation": {
                "min": summary_stats['min_thermal_sensation'],
                "max": summary_stats['max_thermal_sensation'],
                "avg": round(summary_stats['avg_thermal_sensation'], 2) if summary_stats['avg_thermal_sensation'] else None,
            },
            "comfort_zones": comfort_zones
        }
        
        return APIResponse(
            success=True,
            message="Estatísticas calculadas com sucesso",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
