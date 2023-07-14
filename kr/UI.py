import asyncio
import threading
import fightclass
import exceptions
import sqlite3
import BotThread

#Класс для потоков
class MyThread(threading.Thread):
    """
    Пример threading
    """

    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter


    #что эти потоки запускают в себе и вызывается сразу с исполнением
    def run(self):
        """Запуск потока"""
        check = BotThread.BotFight()
        check.Battle()

#класс меню, для использования всего функционала без выхода из программы
class InterFace:
    #Метод для создания потоков, класс которых написан выше
    def create_threads(self):
        """
        Создаем группу потоков
        """
        for i in range(2):
            print(f'Бой номер {i + 1}')
            name = 'Thread'
            my_thread = MyThread(name, i)
            my_thread.start()
            my_thread.join() #Если ее убрать они будут идти можно сказать параллельно, что не удобно и не красиво.
            #При испольховании такой меню, без строки выше прога корректно не работает



    def menu(self):
        commands = ['Начать матч', 'Провести быстрые бои между ботами', 'Посмотреть историю матчей', 'Выйти'] #Список возможных опций(Ещё может дополниться)
        print('Выберите опцию:')
        #Вывод всех опций
        for i in range(len(commands)):
            print(i+1, commands[i])
        #Выбор опции (с помощью исключений)
        while True:
            choose = input()
            try:
                if choose not in '0123456789':
                    raise exceptions.IncorrectInputExcError #Ошибка ввода
                else:
                    if int(choose) > len(commands):
                        raise exceptions.IncorrectInputExcError #Ошибка ввода
                    else:
                        #ifы стоят не попорядку, потому что почему то finally для choose == 3 вызывает ошибку, если под ним что-то есть
                        #обычный бой
                        if int(choose) == 1:
                            battle = fightclass.Fight()
                            battle.Battle()
                            return
                        #Бой между ботами (заготовка к турнирам)
                        elif int(choose) == 2:

                            if __name__ == "__main__":
                                self.create_threads()
                            return

                        #Выход из системы
                        elif int(choose) == 4:
                            print('Вы вышли из системы')
                            exit()


                        #Просмотреть историю матчей(в том числе ботов)
                        elif int(choose) == 3:
                            #Обращение к БД
                            try:
                                connection = sqlite3.connect('Poke.db')

                                cur = connection.cursor()
                                print("База данных создана и подключена к SQLite")
                                cur.execute("CREATE TABLE IF NOT EXISTS tHistory(name_of_win, hp_of_win)")

                                print('Прошлые матчи:')
                                res = cur.execute('SELECT * FROM tHistory')
                                print(res.fetchall())

                            except sqlite3.Error:

                                print('Просмотреть историю матчей в данный момент невозможно')
                            finally:
                                if (connection):
                                    connection.commit()
                                    connection.close()
                                    return

            except exceptions.IncorrectInputExcError:
                print('Неверный ввод! Такой команды нет. Повторите попытку')



print('Добро пожаловать в Pokemon Fighting Game')
my_game = InterFace()
#обеспечиваер беспрерывную работу
while True:
    my_game.menu()
