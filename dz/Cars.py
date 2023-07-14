

class Car: #Базовый класс
    def __init__(self, id):
        self.__id = id #если будет больше одного экземпляра одной машины
        self.__lifting_capacity = 1 #кг
        self.__length = 1  # см
        self.__width = 1 #см
        self.__height = 1 #см
    #get
    def get_LeftCap(self):
        return self.__lifting_capacity

    def get_id(self):
        return self.__id

    def get_width(self):
        return self.__width

    def get_length(self):
        return self.__length

    def get_height(self):
        return self.__height

    #set
    def set_LeftCap(self, lifting_capacity):
        self.__lifting_capacity = lifting_capacity

    def set_width(self, width):
        self.__width = width

    def set_length(self, length):
        self.__length = length

    def set_height(self, height):
        self.__height = height

class Gazel(Car):
    def __init__(self, id):
        super().__init__(id)
        self.__name = 'ГАЗ-3302 «Газель»'
        self.__lifting_capacity = self.set_LeftCap(2000)  # кг
        self.__length = self.set_length(300)  # см
        self.__width = self.set_width(200)  # см
        self.__height = self.set_height(170)  # см

    def get_name(self):
        return self.__name

class Bull(Car):
    def __init__(self,id):
        super().__init__(id)
        self.__name = 'ЗИЛ-5301 (Бычок)'
        self.__lifting_capacity = self.set_LeftCap(3000)  # кг
        self.__length = self.set_length(420)  # см
        self.__width = self.set_width(200)  # см
        self.__height = self.set_height(200)  # см

    def get_name(self):
        return self.__name

class MAN(Car):
    def __init__(self,id):
        super().__init__(id)
        self.__name = 'MAN-10'
        self.__lifting_capacity = self.set_LeftCap(10000)  # кг
        self.__length = self.set_length(600)  # см
        self.__width = self.set_width(245)  # см
        self.__height = self.set_height(230)  # см

    def get_name(self):
        return self.__name

class Truck(Car):
    def __init__(self,id):
        super().__init__(id)
        self.__name = 'Фура Mercedes-Benz Actros'
        self.__lifting_capacity = self.set_LeftCap(20000)  # кг
        self.__length = self.set_length(1360)  # см
        self.__width = self.set_width(246)  # см
        self.__height = self.set_height(250)  # см

    def get_name(self):
        return self.__name
