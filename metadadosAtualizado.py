import pyodbc
import pandas as pd
import os
import re
import shutil
from dotenv import load_dotenv

from encontrar_audio import encontrar_audio
from datetime import datetime

#Carrega as variaveis do do arquivo ".env"
load_dotenv()

# Função para escolher a campanha
def escolher_campanha() -> list[(list[str], str)]:
# Dicionário de campanhas e códigos
    lista_call_queue = {
        '28': ('call_queue_28', '14'),
        '30': ('call_queue_30', '8'),
        '31': ('call_queue_31', '9'),
        '32': ('call_queue_32', '10'),
        '35': ('call_queue_35', '12'),
        '36': ('call_queue_36', '1'),
        '37': ('call_queue_37', '13'),
        '49': ('call_queue_49', '17'),
        '54': ('call_queue_54', '20'),
        '55': ('call_queue_55', '21'),
        '56': ('call_queue_56', '23'),
        '57': ('call_queue_57', '24'),
        '63': ('call_queue_63', '25'),
        '64': ('call_queue_64', '26'),
        '65': ('call_queue_65', '27'),
        '66': ('call_queue_66', '28'),
        '67': ('call_queue_67', '29'),
        '68': ('call_queue_68', '30'),
        '69': ('call_queue_69', '31'),
        '93': ('call_queue_93', '32'),
        '94': ('call_queue_94', '33'),
        '95': ('call_queue_95', '34'),
        '96': ('call_queue_96', '35'),
        '97': ('call_queue_97', '36'),
        '98': ('call_queue_98', '37'),
        '114': ('call_queue_114', '38'),
        '115': ('call_queue_115', '39'),
        '122': ('call_queue_122', '40'),
        '123': ('call_queue_123', '41'),
        '124': ('call_queue_124', '42')
        
        }

    validador_pergunta = True
    list_caminhos_campaign : list[(str, str)] = []
    caminho_da_pasta_gravacao = r'\\216.238.103.49\Gravacao'
    user = 'backup'
    comando = f'net use {caminho_da_pasta_gravacao} /user:{user} {user}'
    
    try:
        os.system(comando)
    except Exception as e:
        print(f'Não foi possível acessar pasta gravação, Motivo: {e}')


    while validador_pergunta:
        
        pergunta_usuario = input('Digite o código da campanha: ').strip()
        print('\n')

        if not pergunta_usuario:
            print('O campo não pode estar vazio. Tente novamente.')
            continue

        if pergunta_usuario in lista_call_queue:
            nome_campanha = lista_call_queue[pergunta_usuario]
            caminho_call_queue = os.path.join(caminho_da_pasta_gravacao, nome_campanha[0])
            
            if os.path.exists(caminho_call_queue):
                lista_pastas = [pasta for pasta in os.listdir(caminho_call_queue) if os.path.isdir(os.path.join(caminho_call_queue, pasta))]
                #parte que verifica a pasta campaing com a ultima data de alteração
                    
                # Expressão regular para encontrar "campaign_" seguido de um número
                padrao = re.compile(r"campaign_(\d+)")

                # Filtra e extrai o número das pastas que seguem o padrão
                pastas_com_numeros = [
                (pasta, int(padrao.search(pasta).group(1)))  # Captura o número e converte para inteiro
                for pasta in lista_pastas if padrao.search(pasta)
                ]

                # Seleciona a pasta com o maior número
                pasta_mais_recente = max(pastas_com_numeros, key=lambda x: x[1], default=(None, None))[0]

                if pasta_mais_recente in lista_pastas:
                    print(f'Pasta campaign encontrada em: {caminho_call_queue}')
                    caminho_campaign = os.path.join(caminho_call_queue, pasta_mais_recente)
                    list_caminhos_campaign.append((caminho_campaign, nome_campanha[1]))
                    
                    deseja_continuar = int(input('Se deseja adicionar outra campanha digite 1: \nCaso contrario digite 0: \n'))
                    
                    if deseja_continuar == 0:
                        validador_pergunta = False
                    else:
                        continue

                else:
                    print(f'Pastas "campaign" não foram encontradas, somente incoming_calls')
                    continue
        
            else:
                print('A pasta  não foi encontrada, tente novamente.')
                continue
        else:
            print('Número inválido, digite novamente\n')
    
    return list_caminhos_campaign

def escolher_data():
    while True:
        digitar_periodo_inicio = input(f'Digite o início do período desejado DD-MM-AAAA: \n')

        digitar_periodo_final = input(f'Digite o final do período desejado DD-MM-AAAA: \n')
        
        try:
            # Converte a string para um objeto datetime
            data_formatada_inicio = datetime.strptime(digitar_periodo_inicio, "%d-%m-%Y")
            data_formatada_final = datetime.strptime(digitar_periodo_final, "%d-%m-%Y")
            if data_formatada_final < data_formatada_inicio:
                print(f'Erro, verifique as datas, e digite novamente: ')
                continue
            if data_formatada_inicio > datetime.now():
                print(f'Erro, verifique as datas, e digite novamente: ')
                continue
            if data_formatada_final > datetime.now():
                print(f'Erro, verifique as datas, e digite novamente: ')
                continue
            
            print(f'Ligações no período de {data_formatada_inicio} á {data_formatada_final}')
            return data_formatada_inicio, data_formatada_final
        
        except ValueError:
            print(f'Formato errado, digite novamente')

def tempo_audio_em_minutos(segundos):
    segundos = int(segundos)
    if segundos:  
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        return f'{horas:02}:{minutos:02}:{segundos:02}'
    return "00:00:00"


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

def consulta_dados_banco(date_inicial: str, date_final: str, cod_camp: str):
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
        AND A.ID_CAMP = '{cod_camp}'
        AND a.ID_STATUS NOT IN (8,1054,11,1014,1059,1057,1058,3,7,1056,1007,1012,1055,13,1001,258, 119, 45, 126, 29, 245, 54, 251, 158, 118, 102, 34, 131, 128, 253, 94, 264, 52, 113, 42, 53, 51, 262, 130, 88, 224, 116, 145)
    """
    
    cursor.execute(var_query)
    return cursor.fetchall()

def encontrar_audio(caminho_pasta, telefone, list_datas: list[str], list_horas: list[str]):
    
    try:
        arquivos = os.listdir(caminho_pasta)  # Lista os arquivos na pasta
        telefone_str = str(telefone).strip().replace(" ", "").replace("-", "").replace("_", "")
        
        for data in reversed(list_datas):
            telefone_str = f'{telefone_str}_{str(int(data))}'
        
        for hora in list_horas:
            telefone_str = f'{telefone_str}_{str(int(hora))}'
        
        padrao = re.compile(rf".*{telefone_str}.*")
        
        for arquivo in arquivos:
            if padrao.search(arquivo):  # Se o telefone for encontrado no nome do arquivo
                print(f"------------------------------ Arquivo encontrado ------------------------------\n {arquivo}")
                return os.path.join(caminho_pasta, arquivo)
            
    except FileNotFoundError:
        print(f"Erro: A pasta {caminho_pasta} não existe.")
    
    return ""

caminhos_incoming_calls = escolher_campanha()
periodo_desejado = escolher_data()
data_inicial_banco_de_dados = periodo_desejado[0].strftime("%Y-%m-%d 00:00:00.000")
data_final_banco_de_dados = periodo_desejado[1].strftime("%Y-%m-%d 23:59:59.999")

# Conectando ao banco de dados
string_de_conexao = os.getenv("DATABASE_URL")
conn = pyodbc.connect(string_de_conexao)
cursor = conn.cursor()
print('\n')
print('Carregando banco de dados, aguarde: \n')


#Query para pegar o campo Contratos e preencher no excel > contrato = str(item[9]).strip() if item[9]
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
resultado_linha_tabela1 = cursor.fetchall()#Selecionar todos os campos da variável

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

caminho_de_destino = r'C:\Users\dioni.silva\Desktop\primeiroprojeto'

for caminho_incoming_calls in caminhos_incoming_calls:
    resultado_linha_tabela = consulta_dados_banco(
        data_inicial_banco_de_dados, data_final_banco_de_dados, caminho_incoming_calls[1]
    )
    
    for item in resultado_linha_tabela:
        contrato = 'Não encontrado'
        inicio_cpf = 'Não encontrado'  # Valor padrão
        telefone = item[8] if item[8] else "Telefone Desconhecido"
        tempo_em_segundos = item[3] if item[3] else 0
        tempo_formatado = tempo_audio_em_minutos(tempo_em_segundos)
        list_horas = item[1].split(':') if item[1] else ["00"]
        data = item[0] if item[0] else "Desconhecido"
        data_separada = data.split('/')
        caminho_arquivo = os.path.join(
            caminho_incoming_calls[0], 
            str(int(data_separada[2])),
            str(int(data_separada[1])),
            str(int(data_separada[0])),
            str(int(list_horas[0]))
        )
        
        caminho_arquivo_com_audio = encontrar_audio(caminho_arquivo, telefone, data_separada, list_horas)
        nome_arquivo = caminho_arquivo_com_audio.split("\\")[-1]
        
        if os.path.exists(caminho_arquivo_com_audio):
            try:
                caminho_destino = os.path.join(caminho_de_destino, nome_arquivo)
                shutil.copy(caminho_arquivo_com_audio, caminho_destino)
            except Exception as e:
                print(e)
        
        if caminho_arquivo_com_audio:
            caminho_arquivo_audio_em_listas = caminho_arquivo_com_audio.split('\\')[-1]
            inicio_cpf = caminho_arquivo_audio_em_listas[:5]
            resposta_cpf = pegar_cpf_jogar_na_tabela(inicio_cpf)

            if not resposta_cpf:
                cpf_encontrado = "Não encontrado"
                resposta_cpf = None,None,None
            else:
                cpf_encontrado = resposta_cpf[1].strip()
        else:
            caminho_arquivo_audio_em_listas = "Não encontrado"
            resposta_cpf = None,None,None
            cpf_encontrado = "Não encontrado"

        list_contract = [linha[1] for linha in resultado_linha_tabela1 if str(telefone) in linha[0]]
        lista_vazia = [itemm[:-1] if itemm[-1].isalpha() else itemm for itemm in list_contract]
        contrato_escolhido = max(list_contract, default="Desconsiderar")

        if lista_vazia:
            contrato_inicial = lista_vazia[0] #LINHA ALTERADA#
            
            for contrato in lista_vazia:
                if contrato_inicial != contrato:
                    contrato_escolhido = "Desconsiderar"
                    break

        '''if contrato_escolhido != "Desconsiderar" and contrato_escolhido in tabela['Contrato']:
            indice = tabela["Contrato"].index(contrato_escolhido)

            
            if tabela["Arquivo de áudio"][indice] != "Não encontrado":
                continue  
            
            if tabela["Arquivo de áudio"][indice] == "Não encontrado" and caminho_arquivo == "":
                continue

            tabela['Contrato'][indice] = contrato_escolhido
            tabela['Data'][indice] = data
            tabela['Hora'][indice] = item[1] if item[1] else "00:00:00"
            tabela["Arquivo de áudio"][indice] = caminho_arquivo_audio_em_listas
            tabela['Tempo do Áudio'][indice] = (tempo_formatado)
            tabela['CPF Operador'][indice] = cpf_encontrado
            tabela['Nome do Operador'][indice] = resposta_cpf[2]
            tabela['Tabulação'][indice] = (item[5] if item[5] else "Desconhecido")
            tabela['Origem'][indice] = (item[6] if item[6] else "Desconhecido")
            tabela['Tipo'][indice] = ("CPC")  
            tabela['Telefone'][indice] = (telefone)
            tabela['Assessoria'][indice] = (item[10] if len(item) > 10 else "Desconhecido")
            print(resposta_cpf)
            tabela['Nome do Operador'][indice] = resposta_cpf[2]

        else:'''
        tabela['Contrato'].append(contrato_escolhido)
        tabela['Data'].append(data)
        tabela['Hora'].append(item[1] if item[1] else "00:00:00")
        tabela['Arquivo de áudio'].append(caminho_arquivo_audio_em_listas if caminho_arquivo else "Não encontrado")
        tabela['Tempo do Áudio'].append(tempo_formatado)
        tabela['CPF Operador'].append(cpf_encontrado)
        tabela['Nome do Operador'].append(resposta_cpf[2])
        tabela['Tabulação'].append(item[5] if item[5] else "Desconhecido")
        tabela['Origem'].append(item[6] if item[6] else "Desconhecido")
        tabela['Tipo'].append("CPC")  
        tabela['Telefone'].append(telefone)
        tabela['Assessoria'].append(item[10] if len(item) > 10 else "Desconhecido")
            


# Criando o DataFrame
df = pd.DataFrame(tabela)

# Caminho do arquivo Excel
caminho_arquivo_excel = r'C:\Users\dioni.silva\Desktop\primeiroprojeto\tabela_resultado.xlsx'

# Salvando o DataFrame em um arquivo Excel
try:
    df.to_excel(caminho_arquivo_excel, index=False, engine='openpyxl')
    print('Tabela criada e salva com sucesso em Excel!')
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel: {e}")

# Exibindo o DataFrame
print(df)
