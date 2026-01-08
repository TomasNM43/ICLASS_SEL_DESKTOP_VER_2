from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame
from WebService.web_service import get_student
from WebService.request import call_web_service
from Models.Student import Student
from Models.Program import Program

# --- Configuración de Estilo (Tema) ---
COLORS = {
    'bg_app': '#2C3E50',       # Fondo principal (Azul oscuro)
    'bg_card': '#ECF0F1',      # Fondo de la tarjeta (Gris muy claro)
    'text_head': '#2C3E50',    # Color de títulos
    'text_label': '#7F8C8D',   # Color de etiquetas (Gris medio)
    'accent': '#27AE60',       # Verde principal
    'accent_hover': '#219150', # Verde oscuro (hover)
    'entry_bg': '#ECF0F1',     # Fondo de los inputs
    'entry_fg': '#2C3E50',     # Texto de los inputs
    'error': '#E74C3C'         # Rojo para errores
}

FONTS = {
    'h1': ('Segoe UI', 24, 'bold'),
    'h2': ('Segoe UI', 10),
    'label': ('Segoe UI', 9, 'bold'),
    'entry': ('Segoe UI', 11),
    'btn': ('Segoe UI', 11, 'bold')
}

# --- Variables Globales ---
state = False
window = None # Se inicializará en username_password o main
student = Student()
program = Program()

def authentication(method):
    global window
    window = Tk() # Inicializamos Tk aquí si no existe
    
    if method == 1:
        photo()
    elif method == 2:
        username_password()
    elif method == 3:
        print("Via photo and username and password")
    else:
        print("Invalid type of authentication")
    
    return state

def photo():
    pass # Needs implementation

def validateLogin(u_n, p, z, btn_login):
    global state, window, student
    
    # 1. Validación local rápida
    if not u_n.get() or not p.get() or not z.get():
        messagebox.showwarning('Campos Incompletos', 'Por favor complete todos los campos para continuar.')
        return
    
    # 2. Feedback visual de "Cargando"
    original_text = btn_login.cget('text')
    btn_login.config(state='disabled', text='Verificando...', bg=COLORS['text_label'], cursor='watch')
    window.update() # Forzar actualización de UI
    
    try:
        # Simulación de la llamada (Tu código original)
        response = call_web_service(f'student/{u_n.get()}', 'GET')
        
        if response[1] == 200:
            temp = response[0]
            student.convert(temp)
            
            # Verificación de credenciales
            # Nota: Asegúrate de que los tipos de datos coincidan (str vs int)
            if (u_n.get() == student.username and 
                p.get() == student.password and 
                str(z.get()) == str(student.id_program)):
                
                state = True
                window.destroy()
                return # Salir exitosamente
            else:
                messagebox.showerror('Acceso Denegado', 'Usuario, contraseña o ID incorrectos.')
        else:
            messagebox.showerror('Error', 'No se encontró el estudiante en la base de datos.')

    except Exception as e:
        messagebox.showerror('Error de Conexión', f'No se pudo conectar con el servidor:\n{e}')
    
    # 3. Restaurar botón si falló (bloque finally implícito por flujo)
    btn_login.config(state='normal', text=original_text, bg=COLORS['accent'], cursor='hand2')


def create_styled_entry(parent, label_text, var, is_password=False):
    """Ayuda a crear inputs consistentes y limpios"""
    frame = Frame(parent, bg=COLORS['bg_card'])
    frame.pack(fill='x', pady=(0, 15))
    
    lbl = Label(frame, text=label_text.upper(), font=FONTS['label'], 
                bg=COLORS['bg_card'], fg=COLORS['text_label'], anchor='w')
    lbl.pack(fill='x')
    
    ent = Entry(frame, textvariable=var, font=FONTS['entry'], 
                bg=COLORS['bg_card'], fg=COLORS['entry_fg'],
                relief='flat', bd=0, insertbackground=COLORS['text_head'])
    
    if is_password:
        ent.config(show='●')
        
    ent.pack(fill='x', pady=(5, 2))
    
    # Línea decorativa debajo del input
    line = Frame(frame, height=2, bg=COLORS['text_label'], width=100)
    line.pack(fill='x')
    
    # Efecto de foco: Cambiar color de la línea
    def on_focus_in(e): line.config(bg=COLORS['accent'])
    def on_focus_out(e): line.config(bg=COLORS['text_label'])
    
    ent.bind('<FocusIn>', on_focus_in)
    ent.bind('<FocusOut>', on_focus_out)
    
    return ent

def username_password():
    global window
    
    # Configuración base de la ventana
    window.title('Inicio de Sesión - IClassSel')
    window.configure(bg=COLORS['bg_app'])
    
    # Centrar ventana
    w, h = 400, 580
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    window.geometry(f'{w}x{h}+{x}+{y}')
    window.resizable(False, False)

    # --- Título Principal (Fuera de la tarjeta) ---
    header_frame = Frame(window, bg=COLORS['bg_app'])
    header_frame.pack(pady=(40, 20))
    
    Label(header_frame, text="IClassSel", font=FONTS['h1'], 
          bg=COLORS['bg_app'], fg='white').pack()
    Label(header_frame, text="Sistema de Evaluación", font=FONTS['h2'], 
          bg=COLORS['bg_app'], fg='#BDC3C7').pack()

    # --- Tarjeta del Formulario (Contenedor Blanco) ---
    card = Frame(window, bg=COLORS['bg_card'], padx=30, pady=40)
    card.pack(padx=20, fill='both', expand=True) # expand=True llena el espacio
    
    # Variables
    username = StringVar()
    password = StringVar()
    id_program = StringVar()

    # Campos de texto (Usando la función helper)
    entry_user = create_styled_entry(card, "Usuario", username)
    entry_pass = create_styled_entry(card, "Contraseña", password, is_password=True)
    entry_prog = create_styled_entry(card, "ID Programa", id_program)
    
    # Foco inicial
    entry_user.focus()

    # --- Botón de Acción ---
    def on_enter(e): btn_login.config(bg=COLORS['accent_hover'])
    def on_leave(e): btn_login.config(bg=COLORS['accent'])

    btn_login = Button(
        card, 
        text='INGRESAR', 
        font=FONTS['btn'],
        bg=COLORS['accent'], 
        fg='white',
        activebackground=COLORS['accent_hover'], 
        activeforeground='white',
        relief='flat', 
        cursor='hand2',
        command=lambda: validateLogin(username, password, id_program, btn_login)
    )
    btn_login.pack(fill='x', pady=(20, 0), ipady=10)
    
    # Bindings para efectos
    btn_login.bind('<Enter>', on_enter)
    btn_login.bind('<Leave>', on_leave)
    window.bind('<Return>', lambda e: btn_login.invoke())

    # --- Footer ---
    Label(window, text="© 2026 IClassSel", bg=COLORS['bg_app'], 
          fg='#7F8C8D', font=('Segoe UI', 8)).pack(side='bottom', pady=10)

    window.mainloop()

# Para probarlo directamente si ejecutas este archivo:
if __name__ == "__main__":
    # Mockeamos las clases para que corra el ejemplo visual sin backend
    authentication(2)