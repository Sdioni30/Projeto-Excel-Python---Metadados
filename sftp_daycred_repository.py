from conector_sftp import SftpDaycred
from datetime import date, timedelta
import re
import os

class SftpDaycredRepository(SftpDaycred):
    def __init__(self):
        super().__init__() # <--Herdando de SftpDaycred


    def listar_pastas_sftp_por_data(self, telefone: str, data_pesquisa: list[str], list_horas: list[str]) -> str:
        with self as db:
            caminho_de_destino = os.getenv("CAMINHO_DE_DESTINO")
            telefone_str = str(telefone).strip().replace(" ", "").replace("-", "").replace("_", "")
            ano = str(int(data_pesquisa[2]))
            mes = str(int(data_pesquisa[1]))
            dia = str(int(data_pesquisa[0]))
            hora_arquivo = str(int(list_horas[0]))

            for data in reversed(data_pesquisa):
                telefone_str = f'{telefone_str}_{str(int(data))}'

            for hora in list_horas:
                telefone_str = f'{telefone_str}_{str(int(hora))}'

            caminho_arquivos = f"{self.caminho_base}/{ano}/{mes}/{dia}/{hora_arquivo}"

            try:
                lista_itens = db.sftp.listdir(caminho_arquivos)

                for item in lista_itens:
                    if telefone_str in item:
                        caminho_arquivo = f'{caminho_arquivos}/{item}'
                        destino = f'{caminho_de_destino}/{item}'
                        db.sftp.get(caminho_arquivo, destino)
                        print(f'FEITO - {telefone}')
                        return item

            except FileNotFoundError:
                print(f'NÃO FOI POSSÍVEL - {telefone}')
                return None