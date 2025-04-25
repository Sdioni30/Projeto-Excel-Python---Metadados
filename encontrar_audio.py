import re
import os

#Função para procurar audio dentro de cada pasta que contenha o numero de telefone no nome do arquivo
def encontrar_audio(caminho_pasta, telefone):
    """Procura um arquivo de áudio na pasta que contenha o número de telefone no nome."""
    try:
        if not os.path.exists(caminho_pasta):

            print(f"Pasta não encontrada: {caminho_pasta}")
            return ""

        arquivos = os.listdir(caminho_pasta)  # Lista os arquivos na pasta
        telefone_str = str(telefone).strip().replace(" ", "").replace("-", "").replace("_", "")

        print(f"Verificando na pasta: {caminho_pasta}")
        print(f"Arquivos encontrados: {len(arquivos)}")
        print(f"Procurando telefone: {telefone_str}") 

        padrao = re.compile(rf".{telefone_str}.")  # Agora aceita qualquer posição

        for arquivo in arquivos:
            if padrao.search(arquivo):  # Se o telefone for encontrado no nome do arquivo
                print(f"------------------------------ Arquivo encontrado ------------------------------\n {arquivo}")
                return os.path.join(caminho_pasta, arquivo)  
    except FileNotFoundError:
        print(f"Erro: A pasta {caminho_pasta} não existe.")
    
    return ""









'''import re
import os

#Função para procurar audio dentro de cada pasta que contenha o numero de telefone no nome do arquivo
def encontrar_audio(caminho_pasta, telefone):
    """Procura um arquivo de áudio na pasta que contenha o número de telefone no nome."""
    try:

        if not os.path.exists(caminho_pasta):

            print(f"Pasta não encontrada: {caminho_pasta}")
            return ""

        arquivos = os.listdir(caminho_pasta)  # Lista os arquivos na pasta
        telefone_str = str(telefone).strip().replace(" ", "").replace("-", "").replace("_", "")

        print(f"Verificando na pasta: {caminho_pasta}")
        print(f"Arquivos encontrados: {len(arquivos)}")
        print(f"Procurando telefone: {telefone_str}") 

        padrao = re.compile(rf".*{telefone_str}.*")  # Agora aceita qualquer posição

        for arquivo in arquivos:
            if padrao.search(arquivo):  # Se o telefone for encontrado no nome do arquivo
                print(f"------------------------------ Arquivo encontrado ------------------------------\n {arquivo}")
                return os.path.join(caminho_pasta, arquivo)  
    except FileNotFoundError:
        print(f"Erro: A pasta {caminho_pasta} não existe.")
    
    return ""  '''




