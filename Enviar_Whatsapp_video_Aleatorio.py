from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
import random
import shutil

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Configurar as opções do Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\SEU_USUARIO\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Inicializar o navegador Chrome com as opções especificadas
driver = webdriver.Chrome(options=options)

# Abrir WhatsApp Web
driver.get("https://web.whatsapp.com/")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
logging.info("WhatsApp Web carregado.")

# Definir as pastas de vídeos
pasta_nao_enviados = "C:\\Caminho\\Onde\\Os\\Videos\\Ainda\\Não\\Enviados\\Estão"
pasta_enviados = "C:\\Caminho\\Onde\\Os\\Videos\\Ja\\Enviados\\Serão\\Guardados\\Para\\Não\\Haver\\Repetição"

# Selecionar o vídeo uma única vez
def selecionar_video():
    if not os.listdir(pasta_nao_enviados):
        logging.info("Pasta de 'não enviados' está vazia. Movendo vídeos de 'enviados' para 'não enviados'.")
        for video in os.listdir(pasta_enviados):
            shutil.move(os.path.join(pasta_enviados, video), pasta_nao_enviados)

    lista_videos = [f for f in os.listdir(pasta_nao_enviados) if f.endswith('.mp4')]
    return os.path.join(pasta_nao_enviados, random.choice(lista_videos))

# Selecionar o vídeo uma única vez
video_selecionado = selecionar_video()

def enviar_video(nome_contato):
    try:
        # Abrir a conversa específica
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(nome_contato)
        search_box.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button"][@title="Anexar"]')))
        logging.info(f"Conversa com {nome_contato} aberta.")
        
        # Clicar no ícone de clipe de anexo
        clip_icon = driver.find_element(By.XPATH, '//div[@role="button"][@title="Anexar"]')
        clip_icon.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Fotos e vídeos")]')))
        logging.info("Botão de anexo clicado.")

        # Clicar na opção "Fotos e vídeos"
        photo_video_option = driver.find_element(By.XPATH, '//span[contains(text(), "Fotos e vídeos")]')
        photo_video_option.click()

        # Aguardar o campo de input de arquivo estar presente
        file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
        
        # Definir o caminho do vídeo no campo de input
        file_input.send_keys(video_selecionado)
        logging.info(f"Arquivo de vídeo selecionado: {video_selecionado}")

        # Aguardar o botão de envio estar clicável e clicar para enviar
        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
        send_button.click()
        logging.info("Vídeo enviado.")

        time.sleep(10)

    except Exception as e:
        logging.error(f"Erro ao enviar o vídeo: {e}")

# Enviar vídeo para múltiplos contatos
enviar_video("Contato2")
enviar_video("Contato2")
enviar_video("Contato3")
enviar_video("Contato4")

# Mover o vídeo para a pasta de "enviados" após a conclusão
shutil.move(video_selecionado, os.path.join(pasta_enviados, os.path.basename(video_selecionado)))
logging.info(f"Vídeo movido para a pasta de 'enviados': {video_selecionado}")

# Fechar o navegador após a conclusão
driver.quit()
