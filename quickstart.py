from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class WhatsAppHelp:
    def __init__(self):
        self.brave_profile_path = "C:/Users/Joel/AppData/Local/BraveSoftware/Brave-Browser/User Data/Profile 3"
        self.brave_binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        self.chromedriver_path = "E:/Cepre/Selenium/chrome-driver/chromedriver.exe"
        self.browser = None

    def abrir_whatsapp(self):
        # Configurar opciones de Chrome
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={self.brave_profile_path}")
        options.binary_location = self.brave_binary_location
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-web-security')  # Opcional: Puede ayudar con algunos problemas de CORS/SSL

        # Configurar el servicio del WebDriver
        serv = Service(self.chromedriver_path)

        # Inicializar el WebDriver con las opciones y el servicio configurados
        self.browser = webdriver.Chrome(service=serv, options=options)

        # Abrir WhatsApp Web
        self.browser.get('https://web.whatsapp.com')

        wait = WebDriverWait(self.browser, 400)  # Esperar 400 segundos
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._aigu")))
        print("\nWhatsApp Web se ha cargado correctamente...")

        return self.browser

    def cerrar_whatsapp(self):
        if self.browser:
            print('cerrando...')
            self.browser.quit()  # Cerrar el navegador

if __name__ == "__main__":
    try:
        # Crear una instancia del bot de WhatsApp
        whatsapp_bot = WhatsAppHelp()
        whatsapp_bot.abrir_whatsapp()
        print('\nLa ventana cerrará en 10 segundos...')
    except Exception as e:
        print(f'\nEl proceso demoró más de 6 min: {e}')
    finally:
        time.sleep(10)
        whatsapp_bot.cerrar_whatsapp()
