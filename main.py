import oracledb
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QRadioButton, QPushButton, QScrollArea, 
    QMessageBox, QListWidget, QListWidgetItem, QGroupBox,
    QCheckBox, QHBoxLayout
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5 import QtCore
from datetime import datetime
import cv2
from imutils.video import FPS, WebcamVideoStream
import keyboard
from Proctoring import Proctoring
from Auth.authentication import authentication, student
from Utils.constants import *
from Detector.SoftwareNHardware.keyboard_detector import save_screenshoot_pegar, save_screenshoot_copiar, save_screenshot_alt_tab
from Detector.SoftwareNHardware.programs_detector import detector_programas
from WebService.web_service import run_api
from WebService.request import call_web_service
import threading
import base64

def establecerConexion():
    conexion = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DSN)
    return conexion

class SeleccionProgramaApp(QWidget):
    def __init__(self, id_institucion, id_alumno):
        super().__init__()
        self.id_institucion = id_institucion
        self.id_alumno = id_alumno
        self.conexion = establecerConexion()
        
        self.setWindowTitle("Seleccionar Programa")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout_principal = QVBoxLayout()
        self.lista_programas = QListWidget()
        
        self.btn_abrir_programa = QPushButton("Abrir Programa")
        self.btn_abrir_programa.clicked.connect(self.abrir_programa)
        
        self.cargar_programas()
        
        self.layout_principal.addWidget(QLabel("Seleccione un programa:"))
        self.layout_principal.addWidget(self.lista_programas)
        self.layout_principal.addWidget(self.btn_abrir_programa)
        self.setLayout(self.layout_principal)

        self.setWindowModality(Qt.ApplicationModal)

    def cargar_programas(self):
        try:
            fecha_actual = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
            print(fecha_actual)
            data = {'id_institucion': self.id_institucion, 'fecha_actual': fecha_actual}
            programas = call_web_service('programs_by_institution', 'GET', data)
            
            if programas[0]:
                for programa in programas[0]:
                    programa_id, titulo, descripcion, restriccion_resolucion = programa
                    if restriccion_resolucion == 1:
                        item = QListWidgetItem(f"{titulo} - {descripcion} (No disponible)")
                        item.setData(1, programa_id)
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    else:
                        item = QListWidgetItem(f"{titulo} - {descripcion}")
                        item.setData(1, programa_id)
                        self.lista_programas.addItem(item)
        
        except Exception as e:
            print("Error al cargar programas:", e)

    def abrir_programa(self):
        item = self.lista_programas.currentItem()
        if item:
            programa_id = item.data(1)
            self.close()
            self.ventana_programa = ProgramaApp(id_institucion=self.id_institucion, id_programa=programa_id, id_alumno=self.id_alumno)
            self.ventana_programa.setWindowModality(Qt.ApplicationModal)
            self.ventana_programa.showFullScreen()
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un programa de la lista.")

class VentanaFinal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Examen Enviado")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        mensaje = QLabel("¡Gracias! Su examen ha sido enviado correctamente.")
        mensaje.setFont(QFont('Arial', 16))
        layout.addWidget(mensaje)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setFont(QFont('Arial', 14))
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)
        
        self.setLayout(layout)


class ProgramaApp(QWidget):
    def __init__(self, id_institucion, id_programa, id_alumno):
        super().__init__()
        self.id_institucion = id_institucion
        self.id_programa = id_programa
        self.id_alumno = id_alumno
        self.conexion = establecerConexion()
        
        self.respuestas_seleccionadas = {}
        self.pregunta_actual = 0
        self.tipos_programa = {}
        self.preguntas_widgets = []  

        self.setWindowTitle("Programa")

        self.layout_principal = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.layout_principal)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        
        self.btn_enviar = QPushButton("Enviar Programa")
        self.btn_enviar.setFont(QFont('Arial', 14))
        self.btn_enviar.clicked.connect(self.enviar_programa)

        self.btn_avanzar = QPushButton("Avanzar")
        self.btn_avanzar.setFont(QFont('Arial', 14))
        self.btn_avanzar.clicked.connect(self.avanzar_pregunta)
        
        self.btn_retroceder = QPushButton("Retroceder")
        self.btn_retroceder.setFont(QFont('Arial', 14))
        self.btn_retroceder.clicked.connect(self.retroceder_pregunta)
        
        self.cargar_configuracion_programa()
        self.cargar_preguntas()
        self.cargar_informacion_programa()  # Nueva función para cargar información del programa
        
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.btn_retroceder)
        botones_layout.addWidget(self.btn_avanzar)
        layout.addLayout(botones_layout)
        
        layout.addWidget(self.btn_enviar)
        self.setLayout(layout)

        self.setWindowModality(Qt.ApplicationModal)
        self.showFullScreen()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.setFixedSize(self.size()) 

        # Iniciar el proctoring en un hilo separado
        self.proctoring_thread = threading.Thread(target=self.start_proctoring)
        self.proctoring_thread.start()

    def cargar_informacion_programa(self):
        try:
            data = {'id_institucion': self.id_institucion, 'id_programa': self.id_programa}
            informacion_programa, status_code = call_web_service(f'program/{self.id_programa}', 'GET')
            
            if status_code == 200 and informacion_programa:
                descripcion_programa = informacion_programa[2]
                id_institucion = informacion_programa[6]
                nombre_programa = informacion_programa[1]
                fecha_inicio = informacion_programa[4]
                fecha_fin = informacion_programa[5]
                duracion = informacion_programa[8]
                
                info_label = QLabel(f"Titulo: {descripcion_programa}\n"
                                    f"ID Institución: {id_institucion}\n"
                                    f"Curso: {nombre_programa}\n"
                                    f"Fecha Inicio: {fecha_inicio}\n"
                                    f"Fecha Fin: {fecha_fin}")
                
                info_label.setFont(QFont('Arial', 12))
                self.layout_principal.addWidget(info_label)
                
                # Crear y agregar el label del contador
                self.contador_label = QLabel(f"Tiempo restante: {duracion}:00")
                self.contador_label.setFont(QFont('Arial', 12))
                self.layout_principal.addWidget(self.contador_label)
                
                # Configurar el contador
                self.duracion = duracion * 60  # Convertir duración a segundos
                self.fecha_fin = QDateTime.fromString(fecha_fin, 'yyyy-MM-dd HH:mm:ss')
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.actualizar_contador)
                self.timer.start(1000)  # Actualizar cada segundo
                
        except Exception as e:
            print("Error al cargar información del programa:", e)

    def actualizar_contador(self):
        if self.duracion > 0:
            self.duracion -= 1
            minutos, segundos = divmod(self.duracion, 60)
            self.contador_label.setText(f"Tiempo restante: {minutos:02d}:{segundos:02d}")
        else:
            self.timer.stop()
            QMessageBox.information(self, "Tiempo Finalizado", "Se acabó el tiempo del examen.")
            self.close()
        
        if QDateTime.currentDateTime() >= self.fecha_fin:
            self.timer.stop()
            QMessageBox.information(self, "Tiempo Finalizado", "Se acabó el tiempo del examen.")
            self.close()
            
    def cargar_configuracion_programa(self):
        try:
            config = call_web_service(f'configuracion_programa/{self.id_programa}', 'GET')
            if config[0]:
                self.tipos_programa = {
                    "TIPO_PROGRAMA": config[0][0],
                    "RETROCESO": config[0][1]
                }
        
        except Exception as e:
            print("Error al cargar configuración del programa:", e)

    def cargar_preguntas(self):
        for i in range(self.layout_principal.count()):
            widget = self.layout_principal.itemAt(i).widget()
            if widget:
                widget.setVisible(False)
        
        try:
            data = {'id_institucion': self.id_institucion, 'id_programa': self.id_programa}
            preguntas, status_code = call_web_service('preguntas', 'GET', data)
            
            if status_code == 200:
                self.total_preguntas = len(preguntas)
                
                if self.pregunta_actual < self.total_preguntas:
                    pregunta = preguntas[self.pregunta_actual]
                    pregunta_id = pregunta['ID_PROGRAMA_PREGUNTA']
                    descripcion = pregunta['pregunta_descripcion']
                    tipo_pregunta = pregunta['tipo_pregunta']
                    pregunta_imagen = pregunta['pregunta_imagen']
                    
                    group_box = QGroupBox(descripcion)
                    group_box_layout = QVBoxLayout()

                    group_box.setLayout(group_box_layout)
                    self.layout_principal.addWidget(group_box)
                    
                    if pregunta_imagen:
                        image_data = base64.b64decode(pregunta_imagen)
                        image = QImage.fromData(image_data)
                        pixmap = QPixmap(image)
                        image_label = QLabel()
                        image_label.setPixmap(pixmap)
                        group_box_layout.addWidget(image_label)

                    if tipo_pregunta == "UNICA":
                        tipo_respuesta_label = QLabel("Seleccione una respuesta.")
                        group_box_layout.addWidget(tipo_respuesta_label)
                        data = {
                            'id_institucion': self.id_institucion,
                            'id_programa': self.id_programa,
                            'id_pregunta': pregunta_id
                        }
                        respuestas, status_code = call_web_service('respuestas', 'GET', data)
                        
                        if status_code == 200:
                            self.respuestas_seleccionadas[pregunta_id] = None
                            
                            for respuesta in respuestas:
                                respuesta_id = respuesta[0]
                                respuesta_texto = respuesta[1]
                                radio_button = QRadioButton(respuesta_texto)
                                radio_button.toggled.connect(lambda checked, pid=pregunta_id, rid=respuesta_id: self.seleccionar_respuesta_unica(pid, rid, checked))
                                group_box_layout.addWidget(radio_button)

                    elif tipo_pregunta == "MULTIPLE":
                        tipo_respuesta_label = QLabel("Seleccione varias respuestas.")
                        group_box_layout.addWidget(tipo_respuesta_label)
                        data = {
                            'id_institucion': self.id_institucion,
                            'id_programa': self.id_programa,
                            'id_pregunta': pregunta_id
                        }
                        respuestas, status_code = call_web_service('respuestas', 'GET', data)
                        
                        if status_code == 200:
                            self.respuestas_seleccionadas[pregunta_id] = []
                            
                            for respuesta in respuestas:
                                respuesta_id = respuesta[0]
                                respuesta_texto = respuesta[1]
                                check_box = QCheckBox(respuesta_texto)
                                check_box.toggled.connect(lambda checked, pid=pregunta_id, rid=respuesta_id: self.seleccionar_respuesta_multiple(pid, rid, checked))
                                group_box_layout.addWidget(check_box)

                    self.preguntas_widgets.append(group_box)

        except Exception as e:
            print("Error al cargar preguntas:", e)

    def avanzar_pregunta(self):
        if self.pregunta_actual + 1 < self.total_preguntas:
            self.pregunta_actual += 1
            self.cargar_preguntas()

    def retroceder_pregunta(self):
        if self.pregunta_actual - 1 >= 0:
            self.pregunta_actual -= 1
            self.cargar_preguntas()

    def seleccionar_respuesta_unica(self, pregunta_id, respuesta_id, checked):
        if checked:
            self.respuestas_seleccionadas[pregunta_id] = respuesta_id

    def seleccionar_respuesta_multiple(self, pregunta_id, respuesta_id, checked):
        if checked:
            self.respuestas_seleccionadas[pregunta_id].append(respuesta_id)
        else:
            self.respuestas_seleccionadas[pregunta_id].remove(respuesta_id)

    def enviar_programa(self):
        try:
            if not self.respuestas_seleccionadas:
                QMessageBox.warning(self, "Advertencia", "No ha respondido ninguna pregunta.")
                return

            respuestas_list = []
            for id_pregunta, id_respuesta in self.respuestas_seleccionadas.items():
                respuestas_list.append({
                    'id_alumno': self.id_alumno,
                    'id_programa': self.id_programa,
                    'id_pregunta': id_pregunta,
                    'id_respuesta': id_respuesta
                })

            # Llamada al endpoint
            response, status_code = call_web_service('guardar_respuestas', 'POST', respuestas_list)

            if status_code == 200:
                QMessageBox.information(self, "Enviado", "¡Respuestas enviadas correctamente!")
                self.close()
                self.ventana_final = VentanaFinal()
                self.ventana_final.show()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al enviar las respuestas.")

        except Exception as e:
            print("Error al enviar programa:", e)
            QMessageBox.critical(self, "Error", f"Ocurrió un error al enviar: {str(e)}")

    def start_proctoring(self):
        self.proctoring_active = True
        video_source = WebcamVideoStream(src=0).start()
        fps = FPS().start()
        proctoring = Proctoring()

        keyboard.add_hotkey("ctrl+v", save_screenshoot_pegar)
        keyboard.add_hotkey("alt+tab", save_screenshot_alt_tab)
        keyboard.add_hotkey("ctrl+c", save_screenshoot_copiar)
        detector_programas()

        while self.proctoring_active:
            frame = video_source.read()
            if proctoring.process(frame):
                save_event(student.id_program, student.name, student.lastname, EVENT_DESCRIPTION, datetime.now().strftime("%H:%M:%S"), convertImageToByte(frame), ID_EVENT, 'Posible plagio detectado', '000120220000001')
            cv2.imshow("Proctoring", frame)

            if cv2.waitKey(1) == 27:
                save_event(student.id_program, student.name, student.lastname, EVENT_DESCRIPTION_END, datetime.now().strftime("%H:%M:%S"), convertImageToByte(frame), ID_EVENT_END, 'Examen terminado', '000120220000001')
                break

        fps.stop()
        save_student_no_assistance(student.id)
        print(f"[INFO] Tiempo transcurrido: {fps.elapsed():.2f}")
        print(f"[INFO] Aproximadamente FPS: {fps.fps():.2f}")
        cv2.destroyAllWindows()
        video_source.stop()

    def stop_proctoring(self):
        self.proctoring_active = False
        cv2.destroyAllWindows()

def start_application():
    if authentication(2):
        app = QApplication([])
        seleccion_programa_app = SeleccionProgramaApp(id_institucion=120220000002, id_alumno=student.id)
        seleccion_programa_app.show()
        app.exec_()
    else:
        print("Autenticación fallida. No se puede continuar.")

if __name__ == "__main__":
    ##api_thread = threading.Thread(target=run_api)
    ##api_thread.daemon = True
    ##api_thread.start()

    start_application()