from decorators import BotDec



#Класс абилок всех покемонов, чтобы при создании новых покемонов было удобно добавлять новые способности или миксовать старые
#Класс миксин
class Abilities():

    def Nuzzle(self, me, enemy, bot):
        if enemy.get_status() != 'Shield':
            enemy.set_status('Stan')
            enemy.set_timeEff(1)
            enemy.set_hp(enemy.get_hp() - 5)
            print(f"У покемона {enemy.get_name()} не было щита, поэтому теперь он углушен")


    def IronTeil(self, me, enemy, bot):
        if enemy.get_status() == "Shield":
            enemy.set_hp(enemy.get_hp() - 10)
            enemy.set_status("Normal")
            print(f"У покемона {enemy.get_name()} был щит. Теперь он сбит\n"
                  f"Покемон {enemy.get_name()} потерял 10 очков здоровья. Теперь его здоровье равно {enemy.get_hp()}")
        else:
            enemy.set_hp(enemy.get_hp() - 30)
            print(f"У покемона {enemy.get_name()} не было щита\n"
                  f"Покемон {enemy.get_name()} потерял 30 очков здоровья. Теперь его здоровье равно {enemy.get_hp()}")


    def FireFang(self, me, enemy, bot): #FireFang
        if enemy.get_status() != "Shield" and enemy.get_type() != 'Water':
            enemy.set_status("Fire")
            enemy.set_timeEff(2)
            enemy.set_hp(enemy.get_hp() - 10)
            print(f"Покемон {enemy.get_name()} атакован. Он потерял 10 очков здоровья. Теперь его здоровье равно {enemy.get_hp()}\n"
                  f"Покемон {enemy.get_name()} горит\n"
                  f"Покемон {enemy.get_name()} потерял 3 очка здоровья. Теперь его здоровье равно {enemy.get_hp()}\n"
                  f"Осталось ходов до окончания эффекта: {me.get_timeEff()}")
        else:
            if enemy.get_status() == "Shield":
                print(f'Покемон {enemy.get_name()} имеет щит. Способность не сработала')
            elif enemy.get_type() == 'Water':
                print(f'Покемон {enemy.get_name()} является водным типом. Способность не сработала')


    def Protect(self, me, enemy, bot): #Protect
        me.set_status("Shield")
        me.set_hp(me.get_hp() + 10)
        me.set_timeEff(2)
        print(f"Покемон {me.get_name()} получил щит. Теперь он неуязвим с эффектами контроля\n"
              f"Покемон {me.get_name()} получает 10 дополнительных очков здоровья от щита. Теперь его здоровье равно {me.get_hp()}\n"
              f"До конца эффекта щита осталось {me.get_timeEff()} ходов")


    def PoisonPowder(self, me, enemy, bot): #Poison Powder
        if enemy.get_status() != "Shield":
            enemy.set_status("Poison")
            enemy.set_timeEff(2)
            enemy.set_hp(enemy.get_hp() - 10)
            print(f"Покемон {enemy.get_name()} атакован. Он потерял 10 очков здоровья. Теперь его здоровье равно {enemy.get_hp()}\n"
                  f"Покемон {enemy.get_name()} отравлен\n"
                  f"Покемон {enemy.get_name()} потерял 2 очка здоровья. Теперь его здоровье равно {enemy.get_hp()}\n"
                  f"до снятия эффекта отравления осталось {enemy.get_timeEff()} ходов\n")


    def LeechSeed(self, me, enemy, bot): #НЕ СООТВЕТСТВУЕТ ОПИСАНИЮ: Leech Seed
        if enemy.get_status() == "Poison":
            enemy.set_hp(enemy.get_hp() - 25)
            me.set_hp(me.get_hp() + 25)
            print(f"Покемон {enemy.get_name()} является отравленным.\n"
                  f"Покемон {enemy.get_name()} атакован. Он теряет 25 очков здоровья. Теперь его здоровье равно {enemy.get_hp()}\n"
                  f"Покемон {me.get_name()} восстанавливает 25 очков здоровья благодаря эффекту вамиризма. Теперь его здоровье равно {me.get_hp()}")
        else:
            print(f"Покемон {enemy.get_name()} не отравлен. Атака не имеет никакого эффекта")


    def Withdraw(self, me, enemy, bot): #НЕ СООТВЕТСТВУЕТ ОПИСАНИЮ: Withdraw
        me.set_hit(me.get_hit() + 5)
        enemy.set_hp(enemy.get_hp() - (me.get_hit() // 2))
        print(f"Покемон {me.get_name()} повышает свою базовую атаку на 5 очков. Теперь его атака равна {me.get_hit()}\n"
              f"Покемон {me.get_name()} атакует покемона {enemy.get_name()} в пол силы\n"
              f"Покемон {enemy.get_name()} атакован. Он потерял {me.get_hit() // 2} hp. Теперь его здоровье равно {enemy.get_hp()}")


    def RainDance(self, me, enemy, bot): #НЕ СООТВЕТСТВУЕТ ОПИСАНИЮ: Rain Dance
        if me.get_hit() > 5:
            me.set_hp(me.get_hp() + 25)
            me.set_hit(me.get_hit() - 5)
            print(f'Покемон {me.get_name()} восстанавливает 25 очков здоровья. Теперь его здоровье равно {me.get_hp()}\n'
                  f'Покемон {me.get_name()} теряет 5 очков атаки. Теперь его атака равна {me.get_hit()}')
