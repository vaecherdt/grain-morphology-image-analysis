import psycopg

def get_db_connection():
    try:
        connection = psycopg.connect(
            dbname="grain_morphology_db",
            user="user",
            password="password",
            host="db",
            port="5432"
        )
        print("Conexão com o banco de dados estabelecida.")
        return connection
    except psycopg.OperationalError as e:
        print(f"Erro operacional ao conectar ao banco de dados: {e}")
    except Exception as e:
        print(f"Erro inesperado ao conectar ao banco de dados: {e}")
    return None

def close_db_connection(conn):
    if conn:
        try:
            conn.close()
            print("Conexão com o banco de dados fechada.")
        except Exception as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")
