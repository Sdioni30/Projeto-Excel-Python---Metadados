from datetime import datetime

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