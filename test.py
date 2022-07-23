import datetime

duracao_desafio = 10

date = datetime.datetime.now() + datetime.timedelta(duracao_desafio)
print(date)

print(date.timestamp())
