from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer
from time import strftime
from datetime import datetime
from Utils.constants import *
from Auth.authentication import student
from WebService.web_service import get_program, get_docent

# Clase para la ventana principal de examen
class ExamWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(EXAM_WINDOW_TITLE)
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        
        self.layout = QVBoxLayout()

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: yellow; font-size: 50px;")
        self.layout.addWidget(self.time_label)

        self.program_label = QLabel()
        self.program_label.setStyleSheet("color: yellow;")
        self.layout.addWidget(self.program_label)

        self.docent_label = QLabel()
        self.docent_label.setStyleSheet("color: yellow;")
        self.layout.addWidget(self.docent_label)

        self.student_label = QLabel(student.name)
        self.student_label.setStyleSheet("color: yellow;")
        self.layout.addWidget(self.student_label)

        self.validate_button = QPushButton("Empezar el Examen")
        self.validate_button.clicked.connect(self.validate_time)
        self.layout.addWidget(self.validate_button)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.fetch_program_data()

    def fetch_program_data(self):
        temp = get_program(student.id_program)
        temp1 = get_docent(student.id_program)

        self.program_label.setText(temp[5])
        self.docent_label.setText(temp[2])
        self.student_label.setText(student.name)

    def update_time(self):
        current_time = strftime('%H:%M:%S')
        self.time_label.setText(current_time)

    def validate_time(self):
        current_hour = datetime.now().hour
        try:
            temp = get_program(student.id_program)
            if current_hour == temp[4].hour:
                self.close()  # Exit exam window
            else:
                QMessageBox.showError('Error', 'No es la hora del examen aún')
        except Exception:
            QMessageBox.showError('Error', 'Database error')


# Clase para la ventana principal de la aplicación
class ExamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Exámenes")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Bienvenido, {student.name} {student.lastname}")
        self.layout.addWidget(self.welcome_label)

        self.view_exams_button = QPushButton("Ver exámenes disponibles")
        self.view_exams_button.clicked.connect(self.view_exams)
        self.layout.addWidget(self.view_exams_button)

        self.exit_button = QPushButton("Salir")
        self.exit_button.clicked.connect(self.exit_app)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    def view_exams(self):
        self.hide()
        exam_window = ExamWindow()  # Crear y mostrar la ventana de examen
        exam_window.show()

    def exit_app(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExamApp()  # Instanciar la ventana principal
    window.show()  # Mostrar la ventana principal
    sys.exit(app.exec_())
