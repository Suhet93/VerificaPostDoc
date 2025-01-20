


import requests
import re
from bs4 import BeautifulSoup
import hashlib
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Get the current time


# Configurações do servidor de e-mail
SMTP_SERVER = "smtp.gmail.com"  # Servidor SMTP do Gmail
SMTP_PORT = 587  # Porta para envio de e-mails
EMAIL_ADDRESS = "enviosuhet@gmail.com"  # Seu e-mail
EMAIL_PASSWORD = "pabghvvhddfbsfag"  # Senha ou senha de aplicativo

# Função para enviar e-mail
def send_email(to_email, subject, body):
    try:
        # Criação da mensagem
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Conexão com o servidor SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  # Inicia comunicação segura
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Faz login no servidor
            smtp.send_message(msg)  # Envia o e-mail
            print(f"E-mail enviado para {to_email} com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def get_page_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Garante que não houve erro na requisição
    return response.text

# URL da página
URL3 = "https://gems.usf.edu:4440/psc/gemspro-tam/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_SCHJOB_FL&Action=U"

# Faz a requisição
response = requests.get(URL3)
soup = BeautifulSoup(response.text, "html.parser")

# Localiza o elemento pelo seletor (substitua pela classe ou ID real)


def monitor_page(URL3, interval):
    print(f"Monitorando alterações na página: {URL3}")
    last_numbers = None

    while True:
        try:
            # Obtém o conteúdo atualizado da página
            content = get_page_content(URL3)
            soup = BeautifulSoup(content, "html.parser")  # Atualiza o BeautifulSoup com o novo conteúdo
            
            # Localiza o elemento desejado
            jobs_count = soup.find("div", class_="ps_box-group psc_layout psc_padding-top0_7em")
            
            if jobs_count:
                # Extrai os números do texto do elemento
                numbers = re.findall(r'\d+', jobs_count.text)
                numbers = [int(num) for num in numbers]
                print(f"Números encontrados: {numbers}")
                
                # Verifica alterações
                if last_numbers is None:
                    print("Iniciando monitoramento...")
                elif numbers != last_numbers:
                    print("Alteração detectada na página!")
                    print(f"Números anteriores: {last_numbers}, Números atuais: {numbers}")
                    send_email("suhet93@hotmail.com", "Alteração detectada", f"Números atualizados: {numbers}")
                else:
                    print("Nenhuma alteração detectada.")
                
                # Atualiza a última versão de numbers
                last_numbers = numbers
            else:
                print("Elemento não encontrado na página.")

        except Exception as e:
            print(f"Erro ao monitorar a página: {e}")
        
        # Aguarda antes de verificar novamente
        time.sleep(interval)

# Chamada da função com intervalo de 10 segundos
monitor_page(URL3, interval=10)

