#Модуль исключений

#Базовое исключение. Наследуется от питоновского класса исключений
class Error(Exception):
    pass



#исключение некорректного ввода
class IncorrectInputExcError(Error):
    '''Некорректный ввод'''
    pass

class NoDataInBDError(Error):
    '''Таких данных нет в базе данных пользователей'''
    pass

class DublicateidError(Error):
    '''Указанный id уже существует'''
    pass

class DublicatenameError(Error):
    '''Одинаковое имя пользователя при регистрации'''
    pass

class IncorrectmonthError(Error):
    '''Неправильно указан месяц'''
    pass

class IncorrectyearError(Error):
    '''Год меньше 2023'''
    pass

class IncorrectdayError(Error):
    '''Неправильно указан день'''
    pass
class IncorrecthourError(Error):
    '''Неправильной указаны часы'''
    pass
class IncorrectminuteError(Error):
    '''Неправильно указаны минуты'''
    pass

class IncorrectlenghtError(Error):
    '''Неправильно указана длина'''
    pass

class IncorrectwigthError(Error):
    '''Неправильно указана ширина'''
    pass

class IncorrectheightError(Error):
    '''Неправильно указана высота'''
    pass

class IncorrectcargoinfoError(Error):
    '''Неправильно введена информация о грузе(длина, ширина, высота)'''
    pass