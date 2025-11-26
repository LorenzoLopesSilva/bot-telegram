import requests
import datetime
from datetime import datetime, timedelta
import calendar 
import plotly.graph_objects as go

#Definir os dias do mes
mes_ano = list("062010")

mes = int(mes_ano[0] + mes_ano[1])
ano = int(mes_ano[2] + mes_ano[3] + mes_ano[4] + mes_ano[5])

n_dias = calendar.monthrange(ano, mes)[1]

dias = []
for i in range(1, n_dias + 1):
  dia = f"{mes:02d}{i:02d}{ano}"
  dias.append(dia)

#Contação
def cotar(data):
  url = fr"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$format=json"
  res = requests.get(url)
  res = res.json()
  if res['value']: 
    return res['value'][0]['cotacaoVenda']
  else:
    dia_anterior = datetime.strptime(data, "%m%d%Y") - timedelta(1)
    dia_anterior = datetime.strftime(dia_anterior, "%m%d%Y")
    return cotar(dia_anterior)


cotacao = [cotar(i) for i in dias]



def linear(t):
  return t
t = dias
fig = go.Figure()
fig.add_trace(go.Scatter(x = t, y = cotacao)) 
fig.update_layout(title='Cotação do Dolar',
xaxis_title='Data',
yaxis_title='Cotação')
fig.show() #mostra o gráfico