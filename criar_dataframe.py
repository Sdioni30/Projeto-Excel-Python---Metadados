import pandas as pd

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