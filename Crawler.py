import urllib
import urllib.request

#try:
#    site = urllib.request.urlopen('http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202109.csv')
#except urllib.erros.URLError:
#    print('O URL tá indisponível.')
#else:
#    print('Tudo ok!')
#    print(site.read())
#    df_qui_quadrado.to_csv('Dados dos Qui-Quadrado.csv', encoding='UTF-8')
import requests
from datetime import date
ano = date.today().year
mes = date.today().month
dia = date.today().day
nome_arquivo2 = 'inf_diario_fi_'+str(ano)+str(mes).zfill(2)+'.csv'
url = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'+nome_arquivo2
print(url)
tratado = url.split('/')
nomearquivo = tratado[len(tratado)-1]
r = requests.get(url, allow_redirects=True)
open(nomearquivo, 'wb').write(r.content)

#inicia o cron
service cron start

#ver se o cron está rodando
service cron status

###lista as rotinas agendadas
contrab -l

#edita as rotinas que você quer
contrab -e

##exemplo de rotina todo dia 10 de meia noite
#0 0 10 * * /bin/python script.py


lá no servidor já está rodando
Mas ele ta jogando pro MyQSL?
