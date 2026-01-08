class Student:
    def __init__(self):
        self.id = None
        self.id_program = None
        self.name = None
        self.lastname = None
        self.second_lastname = None
        self.dni = None
        self.url = None
        self.email = None
        self.photo = None
        self.username = None
        self.password = None
        self.assistance = None

    def convert(self, data: tuple):
        self.id = data[0]
        self.id_program = data[1]
        self.name = data[2]
        self.lastname = data[3]
        self.second_lastname = data[4]
        self.dni = data[5]
        self.url = data[6]
        self.email = data[7]
        self.photo = data[8]
        self.username = data[9]
        self.password = data[10]
        self.assistance = data[11]