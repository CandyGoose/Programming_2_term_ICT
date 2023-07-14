#Здесь содержатся различные декораторы
import time
import sys, os

#Делает задержку в 3 секунды до вызова функции
def My_decorator(method_for_decorate):
    def wrapper_for_dec(self, name_of_poke):
        timing = time.time()
        while True:
            if time.time() - timing > 3.0:
                timing = time.time()
                return method_for_decorate(self, name_of_poke)
    return wrapper_for_dec



#Попытка сделать битву ботов скрытой от глаз. Пока что не успешная, заготовка на будущее
def BotDec(method_for_decorate):
    # Отключает отображение принта
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    #восстанавливает отображение принта
    def enablePrint():
        sys.stdout = sys.__stdout__

    def wrapper_for_dec(self, me, enemy, bot):
        if bot == 1:
                blockPrint()
        else:
                enablePrint()

        return method_for_decorate(self, me, enemy, bot)
    return wrapper_for_dec

#восстанавливает отображение принта
def EnablePrint():
    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__

