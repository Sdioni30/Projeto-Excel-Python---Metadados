from sftp_daycred_repository import SftpDaycredRepository
from datetime import date

data_inicio = date(2024, 5, 2)
data_fim = date(2024, 5, 3)

SftpDaycredRepository().listar_pastas_sftp_por_data(data_inicio, data_fim)