from scripts.db_connection import get_db_connection, close_db_connection
import psycopg

def insert_prediction_to_db(conn, image_file, prediction, exif, notes, region, cooperative, harvest_information):
    if conn is None:
        print("A conexão com o banco de dados não foi estabelecida.")
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO images (file_name, defect, exif, notes) VALUES (%s, %s, %s, %s) RETURNING id",
                (image_file, prediction, exif, notes)
            )
            image_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO grains (image_id, region, cooperative, harvest_information, timestamp) VALUES (%s, %s, %s, %s, NOW()) RETURNING id",
                (image_id, region, cooperative, harvest_information)
            )
            conn.commit()
            print(f"Predição inserida no banco de dados para {image_file}.")
    except psycopg.Error as db_error:
        print(f"Erro no banco de dados ao inserir predição: {db_error}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado ao inserir predição no banco de dados: {e}")
        conn.rollback()


def insert_weather_data(conn, grain_id, weather_data):
    if conn is None:
        print("A conexão com o banco de dados não foi estabelecida.")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO climate (grains_id, temperature, humidity, weather_conditions, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (grain_id, weather_data["temperature"], weather_data["humidity"],
                 weather_data["weather_conditions"], weather_data["timestamp"])
            )
            conn.commit()
            print(f"Dados climáticos inseridos no banco de dados para grain_id: {grain_id}.")
    except psycopg.Error as db_error:
        print(f"Erro no banco de dados ao inserir dados climáticos: {db_error}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado ao inserir dados climáticos no banco de dados: {e}")
        conn.rollback()
