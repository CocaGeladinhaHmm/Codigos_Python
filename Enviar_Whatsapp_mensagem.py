from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar as opções do Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\SEU_USUARIO\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Inicializar o navegador Chrome com as opções especificadas
driver = webdriver.Chrome(options=options)

# Abrir WhatsApp Web
driver.get("https://web.whatsapp.com/")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))

def enviar_mensagem(nome_contato, msgs):
    try:
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(nome_contato)
        search_box.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
        chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        chat_box.click()
        for msg in msgs:
            chat_box.send_keys(msg)
            chat_box.send_keys(Keys.ENTER)
            time.sleep(0.2)

        time.sleep(5)
    except Exception as e:
        print(f"Erro ao enviar Mensagem")

enviar_mensagem("Contato", ["Mensagem1","Mensagem2"])

# Fechar o navegador após a conclusão
driver.quit()