import requests
import os
from dotenv import load_dotenv
import datetime
from datetime import datetime, timedelta
import calendar 


load_dotenv(".env")

updates = requests.get(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/getUpdates")
updates = updates.json()

mensagem_passada = updates["result"][-1]["update_id"]

requests.post(
                url=f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
                data={"chat_id": 8536678599, "text": "Codigo Rodando"}
            ).json()

requests.post(
                url=f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
                data={"chat_id": 8536678599, "text": "Digite a data no formato mm/dd/aaaa: "}
            ).json()

while True:

    updates = requests.get(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/getUpdates")
    updates = updates.json()

    mensagem_atual = updates["result"][-1]["update_id"]

    if mensagem_passada != mensagem_atual:
        mensagem_passada = mensagem_atual

        print(updates["result"][-1]["message"]["text"])

        # if updates["result"][-1]["message"]["text"].lower() == "OI":

        try:
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
                
            dia = str(updates["result"][-1]["message"]["text"])
            
            cotacao = cotar(dia)
            
            requests.post(
            url=f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
            data={"chat_id": 8536678599, "text": f"Cotação do dia {dia}: {cotacao}"}
        ).json()

        
        except:
            requests.post(
                url=f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
                data={"chat_id": 8536678599, "text": "Digite uma data valida"}
            ).json()


        