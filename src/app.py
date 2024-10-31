from scripts.db_connection import get_db_connection, close_db_connection
from scripts.model_loader import load_model
from scripts.image_processor import preprocess_image, predict_image
from scripts.db_operations import insert_prediction_to_db
import os
import argparse

defect_classes = [
    "Fermentados",
    "Germinados",
    "Mancha Parda",
    "Mancha Púrpura",
    "MEI",
    "Mofados",
    "Partidos",
    "Picados por Insetos",
    "Queimados",
    "Sadios",
    "Vários Defeitos"
]

def main():
    parser = argparse.ArgumentParser(description="Menu para inserir informações de grãos e realizar predições.")
    args = parser.parse_args()

    print("Iniciando o aplicativo...")

    model_path = os.path.join('data', 'outputs', 'model.pth')
    model = load_model(model_path)
    print("Modelo carregado com sucesso.")

    conn = get_db_connection()
    if not conn:
        print("Não foi possível estabelecer a conexão com o banco de dados.")
        return

    print("Conexão estabelecida com o banco de dados.")

    while True:
        print("\nMenu:")
        print("1. Inserir informações de um grão e realizar predição")
        print("2. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            file_name = input("Digite o nome do arquivo da imagem: ")
            exif = input("Digite as informações EXIF (ou deixe vazio se não houver): ")
            region = input("Digite a região de coleta: ")
            cooperative = input("Digite a cooperativa: ")
            harvest_information = input("Digite informações da colheita: ")
            notes = input("Digite notas adicionais (ou deixe vazio): ")

            image_path = os.path.join('data/raw/train', file_name)
            if os.path.isfile(image_path):
                try:
                    prediction_index = predict_image(image_path, model)
                    if prediction_index is not None:
                        prediction_name = defect_classes[prediction_index]
                        print(f"Predição para {file_name}: {prediction_name}")

                        insert_prediction_to_db(conn, file_name, prediction_name, exif, notes, region, cooperative, harvest_information)
                    else:
                        print("Erro ao fazer a predição.")
                except Exception as e:
                    print(f"Erro ao processar {file_name}: {e}")
            else:
                print(f"Erro: O arquivo {file_name} não foi encontrado.")
        
        elif choice == "2":
            break
        
        else:
            print("Opção inválida. Por favor, escolha novamente.")

    close_db_connection(conn)
    print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()
