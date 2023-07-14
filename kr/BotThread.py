import random
import fightclass
import exceptions
import sqlite3
import decorators



#класс-копия класса Fight из модуля fightclass
#нужен для реализации игры без участия человека + реализация многопоточности
class BotFight(fightclass.Fight): #наследуется от класса Fight

    #скопирована не через super из-за плохой совместимости многопоточности и ассинхронности, которая реализуется в игре между людьми. Исправить это пока что не в силах, которая реализуется в игре между людьми
    def BD_update(self, fighter1, fighter2):
        # Работа с базой данных. После завершения матча будет записывать
        try:
            connection = sqlite3.connect('Poke.db')

            cur = connection.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS tHistory(name_of_win, hp_of_win)")
            decorators.EnablePrint()
            if fighter1.get_hp() <= 0:  # У первого покемона закончилось hp
                print(f"Покемон {fighter1.get_name()} проиграл")
                name = fighter2.get_name()
                hp = fighter2.get_hp()
                win = (name, hp)
                cur.execute('INSERT INTO tHistory(name_of_win, hp_of_win) VALUES (?, ?)', win)
            if fighter2.get_hp() <= 0:  # у второго покемона закончилось hp
                print(f"Покемон {fighter2.get_name()} проиграл")
                name = fighter1.get_name()
                hp = fighter1.get_hp()
                win = (name, hp)
                cur.execute('INSERT INTO tHistory(name_of_win, hp_of_win) VALUES (?, ?)', win)

        except sqlite3.Error:

            print('Не удалось сохранить данные матча')

        finally:
            if (connection):
                connection.commit()
                connection.close()


    #не изменяется
    def take_pokemon(self):
        super(BotFight, self).take_pokemon()


    #игра ботов происходит через  рандомные действия. Ничего логичного здесь нет
    def use_pokemon(self, poke, enemy):
            move = str(random.randint(1,3))
            if move == '1':
                poke.attack(poke, enemy, 1)
            elif move == '2':
                poke.Special1(poke, enemy, 1)
            elif move == '3':
                poke.Special2(poke, enemy, 1)


    #скопироаван не через супер из-за плохой совместимости многопоточности и ассинхронности
    def Battle(self):
        massive = fightclass.Fight.take_pokemon(self)
        warrior1 = massive[0]
        warrior2 = massive[1]
        count = 1  # будет определять порядок ходов

        # Бой идет
        while True:  # Продолжительность битвы
            attack = count % 2  # порядок ходов определяется остатком номера хода при делении на 2
            count += 1  # счетчик ходов, при пропуске хода он не собьется
            # Действия первого
            if attack == 1:
                print(f'Ход покемона {warrior1.get_name()}')
                warrior1.check_my_status()  # Проверка на эффекты
                # использование исключения вместо флага состояния, насколько корректно это я не знаю, но вроде норм
                try:
                    if warrior1.get_PossMove() == 0:
                        raise exceptions.CantTurnError
                    warrior1.fight_help(warrior1)  # напоминание куда жмякать

                    self.use_pokemon(warrior1, warrior2)  # Выбор действия покемона, реализация выбранного способности
                except exceptions.CantTurnError:
                    print(f"Покемон {warrior1.get_name()} пропускает ход")

            # Действия второго
            else:
                print(f'Ход покемона {warrior2.get_name()}')

                warrior2.check_my_status()  # Проверка на эффекты
                # использование исключения вместо флага состояния, насколько корректно это я не знаю, но вроде норм
                try:
                    if warrior2.get_PossMove() == 0:  # Если не оглушен
                        raise exceptions.CantTurnError
                    warrior2.fight_help(warrior2)  # подсказка по способностям
                    self.use_pokemon(warrior2, warrior1)  # Выбор действия покемона, реализация выбранного способности
                except exceptions.CantTurnError:
                    print(f"Покемон {warrior2.get_name()} пропускает ход")

            # Отслеживать конец
            if warrior1.get_hp() <= 0 or warrior2.get_hp() <= 0:
                BotFight.BD_update(self, warrior1, warrior2) #Отличие в этой строке
                print('Спасибо за игру!')
                return


