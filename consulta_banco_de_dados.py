from conectando_banco_de_dados import conectando_ao_banco

def consulta_dados_banco(date_inicial: str, date_final: str):
    
    cursor = conectando_ao_banco()
    print('\n')
    print('Carregando banco de dados, aguarde: \n')
    
    var_query = f"""
        SELECT 
        Format(A.DATA_LIG,'dd/MM/yyyy') AS DATA,
        format(A.data_lig,'HH:mm:ss') as hora,
        '' as ARQ,
        A.DURACAO,
        '' AS CPF_OPERADOR,
        A.STATUS,
        'Ativo' as origem,
        '' as TIPO,
        A.TELEFONE,
        '' AS CONTRATO,
        'ICR' AS ASSESSORIA,
        '' AS NOME_OPERADOR,
        ID_CAMP
        FROM MAILING.DBO.HISTORICO_DISCADOR A
        WHERE A.DATA_LIG BETWEEN '{date_inicial}' AND '{date_final}'
        AND a.ID_STATUS NOT IN (8,1054,11,1014,1059,1057,1058,3,7,1056,1007,1012,1055,13,1001,258,
		119, 45, 126, 29, 245, 54, 251, 158, 118, 102, 34, 131, 128, 253, 94, 264, 52,
		113, 42, 53, 51, 262, 130, 88, 224, 116, 145,1040,1041,1036,1031,1038,1039,1047,1044)
    """
    
    cursor.execute(var_query)
    return cursor.fetchall()




