#Cursor=manipulação, gerenciamento
cursor.execute(var_query) #Define a query
results = cursor.fetchall() #fetchall coleta "busca" por tudo o que estiver na query
for item in results:
    data = item[0]



print(results)


