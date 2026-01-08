import time
from datetime import datetime
import pyautogui

from Auth.authentication import authentication, student
from WebService.web_service import save_student_image, save_event

def save_screenshoot_pegar():
    codigo = "001217"
    now = datetime.now()
    hora = now.strftime("%H:%M:%S")
    evento1 = "Evento Pegar de la tecla CTRL+V"
    time.sleep(0.5)
    pyautogui.press('printscreen')
    im1 = pyautogui.screenshot()
    im1.save(r'.\temp\EventoPegar.png')
    aviso1 = "El usuario ha usado la tecla de pegar, se ha tomado un screenshot"
    print(aviso1)
    with open('temp\EventoPegar.png', 'rb') as f:
        img_data = f.read()
    save_event(student.id_program, student.name, student.lastname, evento1, hora, img_data, codigo, aviso1,'120200000001')

def save_screenshoot_copiar():
    codigo = "001218"
    now = datetime.now()
    hora = now.strftime("%H:%M:%S")
    evento2 = "Evento Copiar de tecla CTRL+C"
    time.sleep(0.5)
    pyautogui.press('printscreen')
    im2 = pyautogui.screenshot()
    im2.save(r'.\temp\EventoCopiar.png')
    aviso2 = "El usuario ha usado la tecla de copiar, se ha tomado un screenshot"
    print(aviso2)
    with open('temp\EventoCopiar.png', 'rb') as f:
        img_data = f.read()
    save_event(student.id_program, student.name, student.lastname, evento2, hora, img_data, codigo, aviso2,'120200000001')


def save_screenshot_alt_tab():
    codigo = "001219"
    now = datetime.now()
    hora = now.strftime("%H:%M:%S")
    evento3 = 'Evento alt tab'
    time.sleep(0.5)
    pyautogui.press('printscreen')
    im3 = pyautogui.screenshot()
    im3.save(r'.\temp\EventoAltTab.png')
    aviso3 = "El usuario ha usado las teclas alt tab, se ha tomado un screenshot"
    print(aviso3)
    with open('temp\EventoAltTab.png', 'rb') as f:
        img_data = f.read()
    save_event(student.id_program, student.name, student.lastname, evento3, hora, img_data, codigo, aviso3,'120200000001')




