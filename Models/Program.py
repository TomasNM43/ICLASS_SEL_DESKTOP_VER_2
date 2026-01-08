class Program:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.timeStart = None
        self.timeEnd = None

    def convert(self, data: tuple):
        self.id = data[0]
        self.name = data[1]
        self.description = data[2]
        self.type = data[3]
        self.start = data[4]
        self.end = data[5]