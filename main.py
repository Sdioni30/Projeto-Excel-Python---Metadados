import os
import pandas as pd
from dotenv import load_dotenv
from transformar_tempo_para_minutos import tempo_audio_em_minutos
from pegar_cpf_do_banco_de_dados import pegar_cpf_jogar_na_tabela
from consulta_banco_de_dados import consulta_dados_banco
from escolher_data import escolher_data
from buscar_contratos import buscar_contratos_no_banco_de_dados
from sftp_daycred_repository import SftpDaycredRepository

#Carrega as variaveis do do arquivo ".env"
repo_sftp = SftpDaycredRepository()
load_dotenv()
tabela = {
    'Data': [],
    'Hora': [],
    'Arquivo de áudio': [],
    'Tempo do Áudio': [],
    'CPF Operador': [],
    'Nome do Operador': [],
    'Tabulação': [],
    'Origem': [],
    'Tipo': [],
    'Telefone': [],
    'Contrato': [],
    'Assessoria': [],    
}

resultado_linha_tabela1 = buscar_contratos_no_banco_de_dados()
caminho_de_destino = os.getenv("CAMINHO_DE_DESTINO")
periodo_desejado = escolher_data()
data_inicial_banco_de_dados = periodo_desejado[0].strftime("%Y-%m-%d 00:00:00.000")
data_final_banco_de_dados = periodo_desejado[1].strftime("%Y-%m-%d 23:59:59.999")

resultado_linha_tabela = consulta_dados_banco(data_inicial_banco_de_dados, data_final_banco_de_dados)

for item in resultado_linha_tabela:
    contrato = 'Não encontrado'
    inicio_cpf = 'Não encontrado'  
    telefone = item[8] if item[8] else "Telefone Desconhecido"
    tempo_em_segundos = item[3] if item[3] else 0
    tempo_formatado = tempo_audio_em_minutos(tempo_em_segundos)
    list_horas = item[1].split(':') if item[1] else ["00"]
    data = item[0] if item[0] else "Desconhecido"
    data_separada = data.split('-')

    nome_arquivo = repo_sftp.listar_pastas_sftp_por_data(telefone, data_separada, list_horas)
        
    if nome_arquivo:
        #caminho_arquivo_audio_em_listas = nome_arquivo.split('\\')[-1]
        resposta_cpf = pegar_cpf_jogar_na_tabela(nome_arquivo[:5])

        if not resposta_cpf:
            cpf_encontrado = "Não encontrado"
            resposta_cpf = None,None,None
        else:
            cpf_encontrado = resposta_cpf[1].strip()
    else:
        nome_arquivo = "Não encontrado"
        resposta_cpf = None,None,None
        cpf_encontrado = "Não encontrado"

    list_contract = [linha[1] for linha in resultado_linha_tabela1 if str(telefone) in linha[0]]
    lista_vazia = [itemm[:-1] if itemm[-1].isalpha() else itemm for itemm in list_contract]
    contrato_escolhido = max(list_contract, default="Desconsiderar")

    if lista_vazia:
        contrato_inicial = lista_vazia[0] #LINHA ALTERADA
        
        for contrato in lista_vazia:
            if contrato_inicial != contrato:
                contrato_escolhido = "Desconsiderar"
                break


    tabela['Contrato'].append(contrato_escolhido)
    tabela['Data'].append(data)
    tabela['Hora'].append(item[1] if item[1] else "00:00:00")
    tabela['Arquivo de áudio'].append(nome_arquivo)
    tabela['Tempo do Áudio'].append(tempo_formatado)
    tabela['CPF Operador'].append(cpf_encontrado)
    tabela['Nome do Operador'].append(resposta_cpf[2])
    tabela['Tabulação'].append(item[5] if item[5] else "Desconhecido")
    tabela['Origem'].append(item[6] if item[6] else "Desconhecido")
    tabela['Tipo'].append("CPC")  
    tabela['Telefone'].append(telefone)
    tabela['Assessoria'].append(item[10] if len(item) > 10 else "Desconhecido")

df = pd.DataFrame(tabela)

# Caminho do arquivo Excel1
caminho_arquivo_excel = r'C:\Users\dioni.silva\Desktop\primeiroprojeto\tabela_resultado.xlsx'

# Salvando o DataFrame em um arquivo Excel
try:
    df.to_excel(caminho_arquivo_excel, index=False, engine='openpyxl')
    print('Tabela criada e salva com sucesso em Excel!')
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel: {e}")
