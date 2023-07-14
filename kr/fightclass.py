import fighters
import exceptions
import sqlite3
import decorators
import asyncio
class Fight:


    #Пик покемонов
    def take_pokemon(self):
        list_of_pokemons = ['Пикачу', 'Чармандер', 'Бульбозавр', 'Сквиртл']
        while True: #Добивается правильного ввода
            print('Выберите покемона:')
            for i in range(len(list_of_pokemons)):
                print(f'{i+1}) {list_of_pokemons[i]}')
            first_pick = (input())
            # Насколько я понимаю, в этом if-elif-else реализована композиция
            try:
                if first_pick == '1':
                    poke1 = fighters.Pikachu()
                    poke1.set_name("Pikachu")
                    poke1.tutorial(poke1)
                    break
                elif first_pick == "2":
                    poke1 = fighters.Charmander()
                    poke1.set_name("Charmander")
                    poke1.tutorial(poke1)
                    break
                elif first_pick == '3':
                    poke1 = fighters.Bulbosaur()
                    poke1.set_name("Bulbosaur")
                    poke1.tutorial(poke1)
                    break
                elif first_pick == '4':
                    poke1 = fighters.Squirtle()
                    poke1.set_name("Squirtle")
                    poke1.tutorial(poke1)
                    break
                else:
                    raise exceptions.IncorrectInputExcError("Значение введено некорректно")
            except exceptions.IncorrectInputExcError:
                print('Неправильный ввод')

        while True: #Добивается правильного ввода
            print('Выберите покемона')
            for i in range(len(list_of_pokemons)):
                print(f'{i+1}) {list_of_pokemons[i]}')
            second_pick = input()
            #Насколько я понимаю, в этом if-elif-else реализована композиция
            try:
                if second_pick == '1':
                    poke2 = fighters.Pikachu()
                    poke2.set_name("Pikachu")
                    poke2.tutorial(poke2)
                    break
                elif second_pick == '2':
                    poke2 = fighters.Charmander()
                    poke2.set_name("Charmander")
                    poke2.tutorial(poke2)
                    break
                elif second_pick == '3':
                    poke2 = fighters.Bulbosaur()
                    poke2.set_name("Bulbosaur")
                    poke2.tutorial(poke2)
                    break
                elif second_pick == '4':
                    poke2 = fighters.Squirtle()
                    poke2.set_name("Squirtle")
                    poke2.tutorial(poke2)
                    break
                else:
                    raise exceptions.IncorrectInputExcError
            except exceptions.IncorrectInputExcError:
                print('Неправильный ввод')

        return [poke1, poke2]  #возвращает массив из двух выбранных покемонов (они могут быть и одинаковыми - это нормально)


    def use_pokemon(self, poke, enemy): #функция на использование абилок покемона
        while True:
            move = input('Введите порядковый номер атаки: ')
            if move == '1':
                poke.attack(poke, enemy, 0)
                break
            elif move == '2':
                poke.Special1(poke, enemy, 0)
                break
            elif move == '3':
                poke.Special2(poke, enemy, 0)
                break
            else:
                print("Неверный ввод")


    #ассинхронный метод
    async def BD_update(self, fighter1, fighter2):
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





    #Битва покемонов
    def Battle(self):
        #В следующих 3 строках (80, 81, 82) обозначаются выбранные бойцы-покемоны
        massive = Fight.take_pokemon(self)
        warrior1 = massive[0]
        warrior2 = massive[1]
        count = 1 # будет определять порядок ходов

        #Бой идет
        while True: #Продолжительность битвы
            attack = count%2 #порядок ходов определяется остатком номера хода при делении на 2
            count+=1 #счетчик ходов, при пропуске хода он не собьется
            #Действия первого
            if attack == 1:
                print(f'Ход покемона {warrior1.get_name()}')
                warrior1.check_my_status() #Проверка на эффекты
                # использование исключения вместо флага состояния, насколько корректно это я не знаю, но вроде норм
                try:
                    if warrior1.get_PossMove() == 0:
                        raise exceptions.CantTurnError
                    warrior1.fight_help(warrior1) #напоминание куда жмякать

                    self.use_pokemon(warrior1, warrior2) #Выбор действия покемона, реализация выбранного способности
                except exceptions.CantTurnError:
                    print(f"Покемон {warrior1.get_name()} пропускает ход")

            #Действия второго
            else:
                print(f'Ход покемона {warrior2.get_name()}')

                warrior2.check_my_status() #Проверка на эффекты
                #использование исключения вместо флага состояния, насколько корректно это я не знаю, но вроде норм
                try:
                    if warrior2.get_PossMove() == 0:#Если не оглушен
                        raise exceptions.CantTurnError
                    warrior2.fight_help(warrior2) #подсказка по способностям
                    self.use_pokemon(warrior2, warrior1) #Выбор действия покемона, реализация выбранного способности
                except exceptions.CantTurnError:
                    print(f"Покемон {warrior2.get_name()} пропускает ход")

            #Отслеживать конец
            if warrior1.get_hp() <= 0 or warrior2.get_hp() <=0:
                #создание цикла событий
                loop = asyncio.get_event_loop()
                #Добавление события и его исполнение
                loop.run_until_complete(Fight.BD_update(self, warrior1, warrior2))
                print('Спасибо за игру!')
                return


