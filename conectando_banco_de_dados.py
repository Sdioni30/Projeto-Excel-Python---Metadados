import pyodbc
import os
from pyodbc import Cursor


def conectando_ao_banco() -> Cursor:
    # Conectando ao banco de dados
    string_de_conexao = os.getenv("DATABASE_URL")
    conn = pyodbc.connect(string_de_conexao)
    cursor = conn.cursor()
    print('\n')
    print('Carregando banco de dados, aguarde: \n')
    return cursor