import pyodbc
import os


def buscar_contratos_no_banco_de_dados():#Query para pegar o campo Contratos e preencher no excel > contrato = str(item[9]).strip() if item[9]
    
    # Conectando ao banco de dados
    string_de_conexao = os.getenv("DATABASE_URL")
    conn = pyodbc.connect(string_de_conexao)
    cursor = conn.cursor()
    print('\n')
    print('Carregando banco de dados, aguarde: \n')
    
    var_query_contratos = """
            SELECT distinct DDD_TEL+NR_TEL as Telefone, RTRIM(CONTRATO_TIT) AS Contrato,LEN(DDD_TEL+NR_TEL)
            FROM [192.168.0.143].cobsystems3.dbo.TITULOS A
            INNER JOIN [192.168.0.143].cobsystems3.dbo.V_DEVEDORES B ON A.COD_DEV = B.COD_DEV
            INNER JOIN [192.168.0.143].cobsystems3.dbo.PESSOAS_TELEFONES C ON B.COD_PES = C.COD_PES
            WHERE A.COD_CRED IN (4,5,9,16,6)
            AND NOT LEN(DDD_TEL+NR_TEL) < 8
            ORDER BY 1,2 DESC
            """
    cursor.execute(var_query_contratos)
    resultado_linha_tabela1 = cursor.fetchall() #Selecionar todos os campos da variável
    return resultado_linha_tabela1