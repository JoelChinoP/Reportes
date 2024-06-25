# -*- coding: utf-8 -*
from quickstart import WhatsAppHelp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time, schedule, os.path

# Constantes
XPATH_CHAT = '//*[@id="side"]//div[@id="pane-side"]//span[@title="{}"]'
XPATH_INPUT_MESSAGE = '//*[@id="main"]/footer//*[@contenteditable="true" and @role="textbox"]'
XPATH_ENCUESTA_PREGUNTA = '//*[@class="x12lqup9 x1o1kx08"]//span[contains(text(), "Haz una pregunta.")]/following::div[@contenteditable="true"]'
XPATH_ENCUESTA_OPCION = '//*[@class="x12lqup9 x1o1kx08"]//span[contains(text(), "{}")]/following::div[@contenteditable="true"]'

def selecChat(title):
    chat_element = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_CHAT.format(title))))
    chat_element.click()
    

def enviarMensaje(mensaje):
    message_input = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_INPUT_MESSAGE))) #message_input.click()
    inTexto(message_input, mensaje)
    message_input.send_keys(Keys.ENTER)
    print("\n\n***Mensaje enviado correctamente.")   

def prepararEncuesta(msg_encuesta):
    abrirEncuesta()
    cargarPregunta(msg_encuesta['titulo'])
    cargarOpciones(msg_encuesta['opciones'])
    enviarEncuesta(msg_encuesta['desactivar'])
    print("\n\n***Encuesta enviada correctamente.")

def cargarPregunta(pregunta):
    pregunta_field = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_ENCUESTA_PREGUNTA)))
    pregunta_field.click()
    inTexto(pregunta_field, pregunta)
    time.sleep(0.2)

def cargarOpciones(ops):
    content_op = fieldsEncuesta("Añadir")
    content_op.click()
    inTexto(content_op, ops[0])
    for i in range(1, len(ops)): # opciones de 2 a mas
        if i < len(ops):
            content_op = fieldsEncuesta("Añadir")
            content_op.click()
            inTexto(content_op, ops[i])
    time.sleep(0.2)

def fieldsEncuesta(texto):
    elements = browser.find_elements(By.XPATH, XPATH_ENCUESTA_OPCION.format(texto))
    return elements[0] if elements else None

def inTexto(elem, texto):
    browser.execute_script(
        f'''
        const text = `{texto}`;
        const dataTransfer = new DataTransfer();
        dataTransfer.setData('text', text);
        const event = new ClipboardEvent('paste', {{
        clipboardData: dataTransfer, bubbles: true }});
        arguments[0].dispatchEvent(event)
        ''', elem)

def enviarEncuesta(estado):
    if estado:
        switch = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="x12lqup9 x1o1kx08"]//*[@for="polls-single-option-switch"]')))
        switch.click()
    time.sleep(0.5)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="x12lqup9 x1o1kx08"]//*[@aria-label="Enviar" and @role="button"]')))
    btn.click()

def abrirEncuesta():
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, 
    '//*[@id="main"]/footer//div[@aria-label="Adjuntar" and @title="Adjuntar"]')))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer//span[contains(text(), "Encuesta")]')))
    btn.click()
    
#******************************************************************************************************************************************************

def enviar_encuesta_monos(pregunta, ops):
    try:
        selecChat('')  #seleccionar chat de monos
        msg_encuesta = {
            "titulo": pregunta,
            "opciones": ops,
            "desactivar": True
        }
        if len(ops) > 3:
            msg_encuesta["desactivar"] = False
        prepararEncuesta(msg_encuesta)
        time.sleep(15)
    except Exception as e:
        manejarError(e)

def enviar_msg_supers(cab, content):
    try:
        selecChat('SUPERVISORES - CEPRUNSA I FASE 2025')  #seleccionar chat de supers
        msg = cab+content
        enviarMensaje(msg)
        time.sleep(15)
    except Exception as e:
        manejarError(e)

def manejarError(error):
    print(error)
    time.sleep(30)

def prepBrowser():
    wsp = WhatsAppHelp()
    return wsp.abrir_whatsapp()

def main():
    global browser      # variables globales de wait y el driver
    global wait

    browser = prepBrowser()     #Inicio de sesion y asigancion d valores
    wait = WebDriverWait(browser, 5)

    for hora, cab, ops in REPORTE_MONOS:    #programar encuesta  amonis
        schedule.every().day.at(hora).do(enviar_encuesta_monos, cab, ops)
    for hora, cab, cnt in REPORTE_SUPERS:   #programar mensaje a supers
        schedule.every().day.at(hora).do(enviar_msg_supers, cab, cnt)
    schedule.every().day.at('21:20').do(browser.quit)

    time.sleep(1)
    
    while True:
        os.system('cls')      # ´cls' para windows y 'clear' para bash
        print("x: ctrl+c")
        print("\n  ESPERANDING...   ", end="", flush=True)
        for _ in range(5):  # Mostrar animación 
            for char in "|/-\\":
                print(f"\b{char}", end="", flush=True)
                time.sleep(0.1)
        print("\b ", end="", flush=True)
        schedule.run_pending()
        time.sleep(1)

    	
en_ops = [
    ['SII 🤗', 'NO ☠️'],
    ["🎓 Docente Puntual", "🎓 Docente Continua"],
    ['🗿 ENLACE DESHABILITADO', '🗿 GRABACIÓN DETENIDA', '🗿 SESIÓN FINALIZADA']
]

REPORTE_MONOS = [
    ('15:40', '⏳ ENLACE HABILITADO Y MONITOR EN MEET', en_ops[0]),
    ('15:51', '🔴 GRABACIÓN INICIADA', en_ops[0]),
    ('15:57', '👨‍💻‼️ DOCENTE PUNTUAL', en_ops[0]),
    ('16:40', '👨‍💻‼️ 2da HORA', en_ops[1]),
    ('17:25', '👨‍💻‼️ 3ra HORA', en_ops[1]),
    ('18:10', '👨‍💻‼️ 4ta HORA', en_ops[1]),
    ('18:16:30', '📷 CÁMARA APAGADA 🚫', en_ops[0]),      #Receso--
    ('18:55', '👨‍💻‼️ 5ta HORA', en_ops[1]),
    ('19:40', '👨‍💻‼️ 6ta HORA', en_ops[1]),
    ('20:25', '👨‍💻‼️ 7ma HORA', en_ops[1]),
    ('21:05', 'REPORTE FINAL!!', en_ops[2])
]

msg_cab = r'🤓☝️ *SUPERVISOR 08* 🌟\n\`AULAS:\` \`311 B - 320 B\`\n'
msg_bd = [
    f'> 🫦 _LISTO PARA EL TURNO_',
    f'✅ Enlaces habilitados\n✅ Monitores en meet',
    f'✅ Grabaciones iniciadas',
    f'✅ Todos con docentes',
    f'✅ Todos con docentes\n✅ Monitores comiendo',
    f'✅ Enlaces ocultos\n✅ Grabaciones finalizadas\n✅ Sesiones finalizadas'
]

REPORTE_SUPERS = [
    ('15:10', msg_cab, msg_bd[0]),
    ('15:52', msg_cab, msg_bd[1]),
    ('15:56', msg_cab, msg_bd[2]),
    ('16:03', msg_cab, msg_bd[3]),
    ('16:48', msg_cab, msg_bd[3]),
    ('17:33', msg_cab, msg_bd[3]),
    ('18:18', msg_cab, msg_bd[4]),
    ('19:03', msg_cab, msg_bd[3]),
    ('19:48', msg_cab, msg_bd[3]),
    ('20:33', msg_cab, msg_bd[3]),
    ('21:15', msg_cab, msg_bd[5])
]

if __name__ == "__main__":
    main()