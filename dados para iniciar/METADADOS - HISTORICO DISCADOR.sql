select format(DATA_LIG,'dd/MM/yyyy'),
format(data_lig,'HH:mm:ss'),
'' as ARQ,
DURACAO,
'' AS CPF_OPERADOR,
STATUS,
'Ativo' as origem,
''as tipo,
TELEFONE,
'' contrato,
'ICR', NOME_CAMP from HISTORICO_DISCADOR
where DATA_LIG between '2024-12-09 00:00:00.000' and '2024-12-27 23:59:59.999'
and ID_STATUS not in (8,1054,13,1058,1059,1057,7,3,1007,1056,1014,11,1014,1001,1012,224)
AND NOME_CAMP LIKE '%OVER 90%'