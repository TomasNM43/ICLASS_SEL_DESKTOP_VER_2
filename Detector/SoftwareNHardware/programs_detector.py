from tkinter import messagebox, Tk
import wmi
from datetime import datetime
import pyautogui
from PIL import ImageGrab
from multiprocessing import Process
from Auth.authentication import authentication, student
from WebService.web_service import save_student_image, save_event

def detector_programas():
    f = wmi.WMI()
    flag = 0
    if flag == 0:
        for process in f.Win32_Process():
            if "Discord.exe" == process.Name:
                codigo = "001211"
                now = datetime.now()
                hora = now.strftime("%H:%M:%S")
                aviso1 = ("Usted tiene abierto el programa Discord, por favor ciérrelo")
                evento1 = "Evento apertura de Discord"
                pyautogui.press('printscreen')
                im1 = pyautogui.screenshot()
                im1.save(r'.\temp\EventoDiscord.png')
                print(aviso1)
                with open('temp\EventoDiscord.png', 'rb') as f:
                    img_data = f.read()
                save_event(student.id_program, student.name, student.lastname, evento1, hora, img_data, codigo, aviso1,'120200000001')
                messagebox.showwarning("advertencia", aviso1)

            if "Teams.exe" == process.Name:
                codigo = "001212"
                now = datetime.now()
                hora = now.strftime("%H:%M:%S")
                aviso2 = ("Usted tiene abierto el programa Microsoft Teams, por favor ciérrelo")
                evento2 = "Evento apertura de Teams"
                pyautogui.press('printscreen')
                im2 = pyautogui.screenshot()
                im2.save(r'\temp\EventoTeams.png')
                print(aviso2)
                with open('temp\EventoTeams.png', 'rb') as f:
                    img_data = f.read()
                save_event(student.id_program, student.name, student.lastname, evento2, hora, img_data, codigo, aviso2,'120200000001')
                messagebox.showwarning("advertencia", aviso2)


            if "Skypehost.exe" == process.Name:
                codigo = "001214"
                now = datetime.now()
                hora = now.strftime("%H:%M:%S")
                aviso4 = ("Usted tiene abierto Skype, por favor ciérrelo")
                evento4 = "Evento apertura de Skype"
                pyautogui.press('printscreen')
                im4 = pyautogui.screenshot()
                im4.save(r'G:\temp\EventoSkype.png')
                print(aviso4)
                with open('temp\EventoSkype.png', 'rb') as f:
                    img_data = f.read()
                save_event(student.id_program, student.name, student.lastname, evento4, hora, img_data, codigo, aviso4,'120200000001')
                messagebox.showwarning("advertencia", aviso4)



            if "Zoom.exe" == process.Name:
                codigo = "001215"
                now = datetime.now()
                hora = now.strftime("%H:%M:%S")
                aviso5 = ("Usted tiene abierto el programa Zoom, por favor ciérrelo")
                evento5 = "Evento apertura de Zoom"
                pyautogui.press('printscreen')
                im5 = pyautogui.screenshot()
                im5.save(r'.\temp\EventoZoom.png')
                print(aviso5)
                with open('temp\EventoZoom.png', 'rb') as f:
                    img_data = f.read()
                save_event(student.id_program, student.name, student.lastname, evento5, hora, img_data, codigo, aviso5,'120200000001')
                messagebox.showwarning("advertencia", aviso5)



            if "devenv.exe" == process.Name:
                codigo = "001216"
                now = datetime.now()
                hora = now.strftime("%H:%M:%S")
                aviso6 = ("Usted tiene abierto Visual Studio, por favor ciérrelo")
                evento6 = "Evento apertura de Visual Studio"
                pyautogui.press('printscreen')
                im6 = pyautogui.screenshot()
                im6.save(r'.\temp\EventoVisual.png')
                print(aviso6)
                with open('temp\EventoVisual.png', 'rb') as f:
                    img_data = f.read()
                save_event(student.id_program, student.name, student.lastname, evento6, hora, img_data, codigo, aviso6,'120200000001')
                messagebox.showwarning("Advertencia", aviso6)


