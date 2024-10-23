from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from PIL import Image
import imagehash
import io
import base64

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Configurar as opções do Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\SEU_USUARIO\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Inicializar o navegador Chrome com as opções especificadas
driver = webdriver.Chrome(options=options)

# Abrir WhatsApp Web
logging.info("Abrindo WhatsApp Web...")
driver.get("https://web.whatsapp.com/")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
logging.info("WhatsApp Web carregado com sucesso.")

def imagens_sao_semelhantes(img1, img2):
    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)
    cutoff = 23  # Ajuste este valor se necessário, ele determina o quanto a comparação tem que ser identica, quanto maior o valor menor a necessidade e ser identica
    return hash1 - hash2 < cutoff

def todas_as_figurinhas_iguais(figurinhas_anteriores, figurinhas_atual):
    if len(figurinhas_anteriores) != len(figurinhas_atual):
        return False
    for figurinha_anterior, figurinha_atual in zip(figurinhas_anteriores, figurinhas_atual):
        try:
            figurinha_anterior_screenshot = figurinha_anterior.screenshot_as_png
            figurinha_atual_screenshot = figurinha_atual.screenshot_as_png
            imagem_anterior = Image.open(io.BytesIO(figurinha_anterior_screenshot))
            imagem_atual = Image.open(io.BytesIO(figurinha_atual_screenshot))

            if not imagens_sao_semelhantes(imagem_anterior, imagem_atual):
                return False
        except Exception as e:
            logging.error(f"Erro ao comparar as figurinhas: {e}")
            return False
    return True

def enviar_figurinha(nome_contato, imagem_referencia_path, nome_imgs):
    try:
        # Abrir a conversa específica
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(nome_contato)
        search_box.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="smiley"]')))
        logging.info(f"Procurando o contato: {nome_contato}")

        for img in nome_imgs:
            # Clicar no ícone de emoji
            emoji_icon = driver.find_element(By.XPATH, '//span[@data-icon="smiley"]')
            emoji_icon.click()
            time.sleep(5)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="sticker"]')))
            logging.info("Ícone de emoji clicado.")

            # Clicar no ícone de sticker
            sticker_icon = driver.find_element(By.XPATH, '//span[@data-icon="sticker"]')
            sticker_icon.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="panel-starred"]')))
            logging.info("Ícone de sticker clicado.")

            # Clicar no ícone de favoritos
            panelstarred_icon = driver.find_element(By.XPATH, '//span[@data-icon="panel-starred"]')
            panelstarred_icon.click()
            time.sleep(1)  # Adicionando o delay aqui

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_ahrb _ahra"]//img')))
            logging.info("Ícone de favoritos clicado.")
            logging.info("Aguardando as figurinhas...")

            # Carregar a imagem de referência
            imagem_referencia = Image.open(f"{imagem_referencia_path}\\{img}")
            logging.info("Imagem de referência carregada.")

            figurinhas_anteriores = []
            while True:
                # Verificar figurinhas visíveis
                figurinhas = driver.find_elements(By.XPATH, '//div[@class="_ahrb _ahra"]//img')
                encontrado = False

                for figurinha in figurinhas:
                    try:
                        figurinha_screenshot = figurinha.screenshot_as_png
                        imagem_atual = Image.open(io.BytesIO(figurinha_screenshot))

                        if imagens_sao_semelhantes(imagem_referencia, imagem_atual):
                            figurinha.click()
                            encontrado = True
                            break
                    except Exception as e:
                        logging.error(f"Erro ao capturar a figurinha: {e}")

                if encontrado:
                    break

                if todas_as_figurinhas_iguais(figurinhas_anteriores, figurinhas):
                    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                    search_box.click()
                    search_box.send_keys(Keys.CONTROL + 'a')
                    search_box.send_keys(Keys.BACKSPACE)
                    logging.info("A figurinha desejada não foi encontrada.")
                    break

                figurinhas_anteriores = figurinhas

                # Rolar para baixo um pouco
                driver.execute_script("arguments[0].scrollBy(0, 250);", driver.find_element(By.XPATH, '//div[@class="x1n2onr6 x9f619 x1dbpiyn xndytuk x1olqfoz x1rife3k"]'))
                logging.info("Rolando para baixo...")
                # Esperar um pouco antes de verificar novamente
                time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="msg-check"]')))  # Espera até que a mensagem seja enviada

            x_icon = driver.find_element(By.XPATH, '//span[@data-icon="x"]')
            x_icon.click()
            time.sleep(5)
    except Exception as e:
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(Keys.CONTROL + 'a')
        search_box.send_keys(Keys.BACKSPACE)
        logging.error(f"Erro ao enviar a figurinha: {e}")

enviar_figurinha("Contato", "C:\\Caminho\\Para\\As\\Figurinhas\\Do\\Whatsapp", ["figurinha1.png", "Figuinha2.png"])

driver.quit()