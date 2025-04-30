import pyodbc
import os

def pegar_cpf_jogar_na_tabela(inicio_cpf: str):
    string_de_conexao = os.getenv("DATABASE_URL")    
    conn = pyodbc.connect(string_de_conexao)
    cursor = conn.cursor()
    var_query_cpf = f"""
        SELECT a.RAMAL_LOG, b.cpfcgc_pes, b.NOME_PES 
        FROM [192.168.0.143].cobsystems3.dbo.LOGIN a
        INNER JOIN [192.168.0.143].cobsystems3.dbo.PESSOAS b ON a.cod_pes = b.cod_pes
        WHERE RAMAL_LOG <> '' AND RAMAL_LOG IN ({inicio_cpf})
    """
    cursor.execute(var_query_cpf)
    response = cursor.fetchone()
    return response