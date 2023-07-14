from tkinter import *
from tkinter import ttk
import sqlite3
import Cars
import datetime
import Exceptions


class BD: #класс для методов работы с бд
    def view_BD(self, numb_of_table): #Получение всех данных из БД
        try:
            connection1 = sqlite3.connect('AllBD.db')
            cur = connection1.cursor()
            if numb_of_table == 1:
                m = cur.execute("""SELECT * FROM tUsers""")
                all_values = list(m.fetchall())
            elif numb_of_table == 2:
                m = cur.execute("""SELECT * FROM tCars""")
                all_values = list(m.fetchall())
            elif numb_of_table == 3:
                m = cur.execute("""SELECT * FROM tOrders""")
                all_values = list(m.fetchall())
            cur.close()
            return all_values
        except sqlite3.Error as error:
            print('Ошибка при получении данных из базы данных', error)
        finally:
            if (connection1):
                connection1.commit()
                connection1.close()


    def BD_update(self, name, password, admin, frame): #Запись данных нового аккаунта
        try:
            if password.isnumeric() == False:
                raise Exceptions.IncorrectInputExcError
            user_list = self.view_BD(1)
            print(user_list)
            for i in user_list:
                if i[0] == name:
                    raise Exceptions.DublicatenameError
            connection2 = sqlite3.connect('AllBD.db')
            cur = connection2.cursor()
            new_item = (name, int(password), admin)
            cur.execute("""INSERT INTO tUsers Values (?, ?, ?)""", new_item)
            cur.close()
            Succes_Label = Label(frame, text='Регистрация прошла успешно', bg='blue', fg='white', font=20,
                               width=300)
            Succes_Label.place(relx=0.395, rely=0.22, width=300)
        except Exceptions.DublicatenameError:
            ErrorLabel = Label(frame, text='Данное имя уже занято', bg='blue', fg='red', font=20,
                               width=300)
            ErrorLabel.place(relx=0.395, rely=0.22)

        except sqlite3.Error as error:
            print('Ошибка при подключение SQLite', error)

        except Exceptions.IncorrectInputExcError:
            ErrorLabel = Label(frame, text='Пароль должен содержать только цифры', bg='blue', fg='red', font=20, width=30)
            ErrorLabel.place(relx=0.395, rely=0.22, width=300)

        finally:
            if (connection2):
                connection2.commit()
                connection2.close()

    def BD_check(self, name, password, admin, frame): #Проверка нахождения аккаунта в БД
        conection = sqlite3.connect('AllBD.db')
        cur = conection.cursor()
        users = cur.execute("""SELECT * FROM tUsers""")
        for i in users:
            if name == (i[0]) and str(password) == str(i[1]) and admin == (i[2]):
                cur.close()
                v = InterFace()
                if admin == 1:
                    v.admin_page(name)
                else:
                    v.main_page(name)
        cur.close()
        conection.close()
        ErrorLabel = Label(frame, text='Неверный логин или пароль', bg = 'blue',fg='red', font=20, width=30)
        ErrorLabel.place(relx=0.395, rely=0.22)


    def car_bd(self, model, id, frame): #Добавление новой машины в БД
        try:
            connection3 = sqlite3.connect('AllBD.db')
            cur = connection3.cursor()
            if model == 'ГАЗ-3302 «Газель»':
                car = Cars.Gazel(int(id))
            elif model == 'ЗИЛ-5301 (Бычок)':
                car = Cars.Bull(int(id))
            elif model == 'MAN-10':
                car = Cars.MAN(int(id))
            elif model == 'Фура Mercedes-Benz Actros':
                car = Cars.Truck(int(id))
            check_list = self.view_BD(2)
            for i in check_list:
                if int(i[1]) == int(id):
                    raise Exceptions.DublicateidError
            new_item = (car.get_name(), car.get_id(), car.get_length(), car.get_width(), car.get_height(), car.get_LeftCap(), 0)
            cur.execute("""INSERT INTO tCars Values (?, ?, ?, ?, ?, ?, ?)""", new_item)
            cur.close()
            succes_label = Label(frame, text='Новый автомобиль успешно добавлен', bg='blue', fg='white', font=30)
            succes_label.place(relx=0.3, rely=0.4, width=500)
        except sqlite3.Error:
            pass
        except Exceptions.DublicateidError:
            Error_label = Label(frame, text='Такой id уже существует', bg='blue', fg='red', font=30)
            Error_label.place(relx=0.4, rely=0.4, width=500)
        except ValueError:
            Errorlab = Label(frame, text='Ошибка ввода! id - только числа', bg='blue', fg='red', font=30)
            Errorlab.place(relx=0.4, rely=0.4, width=500)
        finally:
            if (connection3):
                print('Новый автомобиль успешно добавлен в базу')
                connection3.commit()
                connection3.close()

    def car_del(self, name_andid_of_car, frame): #Удаление машины из базы
        try:
            id_of_car = int(name_andid_of_car[-6:])
            connection4 = sqlite3.connect('AllBD.db')
            cur = connection4.cursor()
            cur.execute("""DELETE FROM tCars WHERE id=?""", (id_of_car,))
            cur.close()
            succes_label = Label(frame, text='Новый автомобиль успешно удален', bg='blue', fg='white', font=30)
            succes_label.place(relx=0.3, rely=0.4, width=500)
        except sqlite3.Error as error:
            succes_label = Label(frame, text='Ошибка при удалении автомобиля', bg='blue', fg='red', font=30)
            succes_label.place(relx=0.3, rely=0.4, width=500)
        finally:
            if (connection4):
                print('Автомобиль успешно удален из базы')
                connection4.commit()
                connection4.close()

    def add_offer(self, name_of_user, name_and_id_of_car, offer_name, end_date, end_month, end_day, end_hour,end_minute, frame):
        try:
            connection5 = sqlite3.connect('AllBD.db')
            cur = connection5.cursor()
            if int(end_date) < 2023:
                raise Exceptions.IncorrectyearError
            end_month= int(end_month)
            if end_month > 12 or end_month < 1:
                raise Exceptions.IncorrectmonthError
            end_day = int(end_day)
            if ((end_day not in range(1,32) and (end_month == 1 or end_month == 3 or end_month == 5 or end_month == 7 or end_month==8 or end_month==10 or end_month == 12)) or \
                    (end_day not in range(1, 31) and (end_month == 4 or end_month == 6 or end_month == 9 or end_month == 11)) or \
                    (end_day not in range(1, 29) and end_month == 2)):
                raise Exceptions.IncorrectdayError
            if int(end_hour) not in range(0, 25):
                raise Exceptions.IncorrecthourError
            if int(end_minute) not in range(0, 61):
                raise Exceptions.IncorrectminuteError
            offer = (name_of_user, name_and_id_of_car[-6:], offer_name, (datetime.datetime(int(end_date), int(end_month), int(end_day), int(end_hour), int(end_minute))))
            cur.execute("""INSERT INTO tOrders Values (?, ?, ?, ?)""", offer)
            cur.close()
            cur1 = connection5.cursor()
            if offer[2] == 'Бронирование':
                cur1.execute("""UPDATE tCars set Busy=2 where id=?""", (int(offer[1]),))
                succes_title = Label(frame, text='Бронь оформлена', bg='blue', fg='white', font=30)
                succes_title.place(relx=0.4, rely=0.65, width=300)
            else:
                cur1.execute("""UPDATE tCars set Busy=1 where id=?""", (int(offer[1]),))
                succes_title = Label(frame, text='Заказ успешно отправлен', bg='blue',fg='white', font=30)
                succes_title.place(relx=0.4, rely=0.3, width=300)
            cur1.close()
        except Exceptions.IncorrectyearError:
            error_lab = Label(frame, text='Неверный ввод года', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        except Exceptions.IncorrectmonthError:
            error_lab = Label(frame, text='Неверный ввод месяца', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        except Exceptions.IncorrectdayError:
            error_lab = Label(frame, text='Неверный ввод дня', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        except Exceptions.IncorrecthourError:
            error_lab = Label(frame, text='Неверный ввод часов', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        except Exceptions.IncorrectminuteError:
            error_lab = Label(frame, text='Неверный ввод минут', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        except sqlite3.Error as error:
            print('При сохранении заказа произошла ошибка', error)
        except ValueError:
            error_lab = Label(frame, text='Неверный формат ввода!', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        finally:
            if (connection5):
                connection5.commit()
                connection5.close()
                print('Новый заказ успешно оформлен')


    def delete_by_time(self):
        try:
            connection6 = sqlite3.connect('AllBD.db')
            list_of_offers = self.view_BD(3)
            for i in range(len(list_of_offers)):
                if self.normal_vid(datetime.datetime.now()) >= self.normal_vid(list_of_offers[i][-1]):
                    cur = connection6.cursor()
                    cur.execute("""DELETE FROM tOrders WHERE end_datetime=?""",(list_of_offers[i][-1],))
                    cur.close()
                    cur1 = connection6.cursor()
                    cur1.execute("""UPDATE tCars set Busy=0 where id=?""", (int(list_of_offers[i][1]),))
                    cur1.close()
        except sqlite3.Error as error:
            print('Ошибка проверки заказов', error)
        finally:
            if (connection6):
                print('Появился новый свободный автомобиль')
                connection6.commit()
                connection6.close()

    def normal_vid(self, time):
        time = str(time)
        stroka = ''
        for i in time:
            if i in '1234567890':
                stroka += i
        return stroka




class InterFace(BD):

    def place_good_cars(self, frame, offer_LeftCap, offer_length, offer_width, offer_height):
        try:
            list_of_cars_for_check = self.view_BD(2)
            best_parametres = [10000000000000, 10000000000000, 10000000000000, 10000000000000,
                               'FFF']  # длина ширина высота тяжесть
            for i in range(len(list_of_cars_for_check)):
                if list_of_cars_for_check[i][-1] != 1:
                    if offer_LeftCap <= list_of_cars_for_check[i][5] and offer_length <= list_of_cars_for_check[i][
                        2] and offer_width <= list_of_cars_for_check[i][3] \
                            and offer_height <= list_of_cars_for_check[i][4]:
                        if best_parametres[0] >= list_of_cars_for_check[i][2] and best_parametres[1] >= \
                                list_of_cars_for_check[i][3] \
                                and best_parametres[2] >= list_of_cars_for_check[i][4] and best_parametres[3] >= \
                                list_of_cars_for_check[i][5]:
                            best_parametres = [list_of_cars_for_check[i][2], list_of_cars_for_check[i][3],
                                               list_of_cars_for_check[i][4], list_of_cars_for_check[i][5],
                                               list_of_cars_for_check[i][0]]

            if best_parametres[-1] == 'FFF':
                havent_label = Label(frame, text='нет подходящих машин', bg='blue', fg='red')
                havent_label.place(relx=0.32, rely=0.5, width=500)
            else:
                if int(offer_LeftCap) < 0 or int(offer_length) < 0 or int(offer_width) < 0 or int(offer_height) < 0:
                    raise Exceptions.IncorrectcargoinfoError

                var3 = StringVar()
                good_title = Label(frame, text=f'Вам подходит автомобиль модели {best_parametres[-1]}')
                good_title.place(relx=0.32, rely=0.5, width=500)
                good_cars = []
                for i in range(len(list_of_cars_for_check)):
                    if best_parametres[-1] == list_of_cars_for_check[i][0] and list_of_cars_for_check[i][-1] != 1:
                        good_cars.append([list_of_cars_for_check[i][0], list_of_cars_for_check[i][1]])
                combobox = ttk.Combobox(frame, textvariable=var3)
                combobox['values'] = good_cars
                combobox['state'] = 'readonly'
                combobox.place(relx=0.32, rely=0.55, width=500)
                my_date = str(datetime.datetime.now()+datetime.timedelta(days=3))
                date_str, time_str = my_date.split(' ')[0], my_date.split(' ')[1]
                fdate = date_str.split('-')
                ftime = time_str.split(':')
                param_button = Button(frame, text='Выбрать', bg='white', command=lambda: (self.add_offer(self.name, combobox.get(), 'Бронирование', fdate[0], fdate[1], fdate[2], ftime[0], ftime[1], frame), self.delete_by_time()))
                param_button.place(relx=0.43, rely=0.6, width=150)



        except ValueError:
            error_lab = Label(frame, text='Вводите только числа', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.5, width=300)
        except Exceptions.IncorrectcargoinfoError:
            error_lab = Label(frame, text='Некорректная информация о грузе', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.5, width=350)






    def parametres_page(self):
        parametres_frame = Frame(root, bg='blue')
        parametres_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(parametres_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        prmt_title = Label(parametres_frame, text='Введите необходимые параметры', bg='red', font=30)
        prmt_title.place(relx=0.4, rely=0.1, width=300)

        LeftCap_title = Label(parametres_frame, text='Введите вес груза', bg='blue', font=30)
        LeftCap_title.place(relx=0.3, rely=0.2, width=300)

        offer_LeftCap = Entry(parametres_frame, bg='white')
        offer_LeftCap.place(relx=0.55, rely=0.21)

        length_title = Label(parametres_frame, text='Введите длину груза', bg='blue', font=30)
        length_title.place(relx=0.3, rely=0.26, width=300)

        offer_length = Entry(parametres_frame, bg='white')
        offer_length.place(relx=0.55, rely=0.27)

        width_title = Label(parametres_frame, text='Введите ширину груза', bg='blue', font=30)
        width_title.place(relx=0.3, rely=0.32, width=300)

        offer_width = Entry(parametres_frame, bg='white')
        offer_width.place(relx=0.55, rely=0.33)

        height_title = Label(parametres_frame, text='Введите высоту груза', bg='blue', font=30)
        height_title.place(relx=0.3, rely=0.38, width=300)

        offer_height = Entry(parametres_frame, bg='white')
        offer_height.place(relx=0.55, rely=0.39)

        param_button = Button(parametres_frame, text='Подобрать автомобиль', bg='white', command= lambda: (self.delete_by_time(), self.place_good_cars(parametres_frame, int(offer_LeftCap.get()), int(offer_length.get()), int(offer_width.get()), int(offer_height.get()))))
        param_button.place(relx=0.55, rely=0.45, width=150)

        back_btn = Button(parametres_frame, text='Назад', bg='white',
                          command=lambda: (parametres_frame.destroy(), self.delete_by_time()))
        back_btn.place(relx=0.3, rely=0.45, width=150)




    def pick_car_for_offer_page(self, name_of_offer, LeftCap_offer, lenght_offer, width_offer, height_offer, date_offer, month_offer, day_offer,hour_offer, minute_offer):
        try:
            pick_car_frame = Frame(root, bg='blue')
            pick_car_frame.place(relwidth=1, relheight=1)

            exit_btn = Button(pick_car_frame, text='X', bg='red', fg='white', command=exit, font=200)
            exit_btn.place(relx=0.98, rely=0, height=30, width=40)

            pcf_title = Label(pick_car_frame, text='Выберите автомобиль', bg='red', font=30)
            pcf_title.place(relx=0.4, rely=0.1, width=300)
            good_cars = []
            list_of_cars_for_offer = self.view_BD(2)
            for i in range(len(list_of_cars_for_offer)):
                if list_of_cars_for_offer[i][-1] != 1:
                    if int(LeftCap_offer) <= list_of_cars_for_offer[i][5] and int(lenght_offer) <= \
                            list_of_cars_for_offer[i][
                                2] and int(width_offer) <= list_of_cars_for_offer[i][3] and int(height_offer) <= \
                            list_of_cars_for_offer[i][4]:
                        good_cars.append([list_of_cars_for_offer[i][0], list_of_cars_for_offer[i][1]]) #модель и id

            back_btn = Button(pick_car_frame, text='Назад', bg='white',
                              command=lambda: (pick_car_frame.destroy(), self.delete_by_time()))
            back_btn.place(relx=0.45, rely=0.45, width=150)

            if int(LeftCap_offer) < 0 or int(lenght_offer) < 0 or int(width_offer) < 0 or int(height_offer) < 0:
                raise Exceptions.IncorrectcargoinfoError

            var2 = StringVar()
            combobox = ttk.Combobox(pick_car_frame, textvariable=var2)
            combobox['values'] = good_cars
            combobox['state'] = 'readonly'
            combobox.place(relx=0.35, rely=0.2, width=500)

            final_button = Button(pick_car_frame, bg='white', text='Отправить заказ', command=lambda: (self.add_offer(self.name, combobox.get(), name_of_offer, date_offer, month_offer, day_offer, hour_offer, minute_offer, pick_car_frame), self.delete_by_time()))
            final_button.place(relx=0.45, rely=0.4, width=150)

        except ValueError:
            error_lab = Label(pick_car_frame, text='Вводите только числа', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=300)
        except Exceptions.IncorrectcargoinfoError:
            error_lab = Label(pick_car_frame, text='Некорректная информация о грузе', bg='red', font=30)
            error_lab.place(relx=0.4, rely=0.3, width=350)


    def new_offer_page(self):
        offer_frame = Frame(root, bg='blue')
        offer_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(offer_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        offer_title = Label(offer_frame, text='Новый заказ', bg='red', font=30)
        offer_title.place(relx=0.4, rely=0.1, width=300)

        LeftCap_title = Label(offer_frame, text='Введите вес груза', bg='blue', font=30)
        LeftCap_title.place(relx=0.3, rely=0.2, width=300)

        offer_LeftCap = Entry(offer_frame, bg='white')
        offer_LeftCap.place(relx=0.55, rely=0.21)

        length_title = Label(offer_frame, text='Введите длину груза', bg='blue', font=30)
        length_title.place(relx=0.3, rely=0.26, width=300)

        offer_length = Entry(offer_frame, bg='white')
        offer_length.place(relx=0.55, rely=0.27)

        width_title = Label(offer_frame, text='Введите ширину груза', bg='blue', font=30)
        width_title.place(relx=0.3, rely=0.32, width=300)

        offer_width = Entry(offer_frame, bg='white')
        offer_width.place(relx=0.55, rely=0.33)

        height_title = Label(offer_frame, text='Введите высоту груза', bg='blue', font=30)
        height_title.place(relx=0.3, rely=0.38, width=300)

        offer_height = Entry(offer_frame, bg='white')
        offer_height.place(relx=0.55, rely=0.39)

        name_title = Label(offer_frame, text='Введите название груза', bg='blue', font=30)
        name_title.place(relx=0.3, rely=0.44, width=300)

        offer_name = Entry(offer_frame, bg='white')
        offer_name.place(relx=0.55, rely=0.45)

        date_title = Label(offer_frame, text='Введите срок доставки груза', bg='red', font=30)
        date_title.place(relx=0.4, rely=0.1, width=300)

        year_title = Label(offer_frame, text='Год:', bg='blue', fg='white', font=30)
        year_title.place(relx=0.3, rely=0.5, width=300)

        offer_date = Entry(offer_frame, bg='white')
        offer_date.place(relx=0.55, rely=0.5)

        month_title = Label(offer_frame, text='Месяц:', bg='blue', fg='white', font=30)
        month_title.place(relx=0.3, rely=0.55, width=300)

        offer_month = Entry(offer_frame, bg='white')
        offer_month.place(relx=0.55, rely=0.55)

        day_title = Label(offer_frame, text='День:', bg='blue', fg='white', font=30)
        day_title.place(relx=0.3, rely=0.6, width=300)

        offer_day = Entry(offer_frame, bg='white')
        offer_day.place(relx=0.55, rely=0.6)

        hour_title = Label(offer_frame, text='Час:', bg='blue', fg='white', font=30)
        hour_title.place(relx=0.3, rely=0.65, width=300)

        offer_hour = Entry(offer_frame, bg='white')
        offer_hour.place(relx=0.55, rely=0.65)

        minute_title = Label(offer_frame, text='Минуты:', bg='blue', fg='white', font=30)
        minute_title.place(relx=0.3, rely=0.7, width=300)

        offer_minute = Entry(offer_frame, bg='white')
        offer_minute.place(relx=0.55, rely=0.7)

        offer_button = Button(offer_frame, bg='white', text='Продолжить заказ', command=lambda: (self.pick_car_for_offer_page(offer_name.get(), offer_LeftCap.get(), offer_length.get(), offer_width.get(), offer_height.get(), offer_date.get(), offer_month.get(), offer_day.get(),offer_hour.get(), offer_minute.get()), self.delete_by_time()))
        offer_button.place(relx=0.4, rely=0.75, width=150)

        back_btn = Button(offer_frame, text='Назад', bg='white',
                          command=lambda: (offer_frame.destroy(), self.delete_by_time()))
        back_btn.place(relx=0.4, rely=0.80, width=150)


    def sort_models_page(self):
        sort_cars_frame = Frame(root, bg='blue')
        sort_cars_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(sort_cars_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        acf_title = Label(sort_cars_frame, text='Автомобили по грузоподъемности', bg='red', font=30)
        acf_title.place(relx=0.4, rely=0.1, width=300)

        list_of_types_cars = ['ГАЗ-3302 «Газель»', 'ЗИЛ-5301 (Бычок)', 'MAN-10', 'Фура Mercedes-Benz Actros']

        vozr_title = Label(sort_cars_frame, text='По возрастанию', bg='blue', fg='white', font=30)
        vozr_title.place(relx=0.2, rely=0.3, width=250)

        ubiv_title = Label(sort_cars_frame, text='По убыванию', bg='blue', fg='white', font=30)
        ubiv_title.place(relx=0.6, rely=0.3, width=250)

        start_place = 0.4
        end_place = 0.55
        for i in range(len(list_of_types_cars)):
            left_title = Label(sort_cars_frame, text=list_of_types_cars[i], bg='blue', fg='white', font=30)
            left_title.place(relx=0.2, rely=start_place)
            start_place +=0.05

            right_title = Label(sort_cars_frame, text=list_of_types_cars[i], bg='blue', fg='white', font=30)
            right_title.place(relx=0.6, rely=end_place)
            end_place -= 0.05

        back_btn = Button(sort_cars_frame, text='Назад', bg='white',
                          command=lambda: (sort_cars_frame.destroy(), self.delete_by_time()))
        back_btn.place(relx=0.45, rely=0.6, width=150)

    def add_new_car_page(self): #Добавление нового транспорта
        add_car_frame = Frame(root, bg='blue')
        add_car_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(add_car_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        acf_title = Label(add_car_frame, text='Добавление нового автомобиля', bg='red', font=30)
        acf_title.place(relx=0.4, rely=0.1, width=300)

        var = StringVar()
        combobox = ttk.Combobox(add_car_frame, textvariable=var)
        cars = ['ГАЗ-3302 «Газель»', 'ЗИЛ-5301 (Бычок)', 'MAN-10', 'Фура Mercedes-Benz Actros']
        combobox['values'] = cars
        combobox['state'] = 'readonly'
        combobox.place(relx=0.35, rely=0.2, width=500)

        id_label = Label(add_car_frame, text='id автомобиля:', bg='blue', fg='white', font=30)
        id_label.place(relx=0.4, rely=0.25, width=150)

        id_for_new_car = Entry(add_car_frame, bg='white')
        id_for_new_car.place(relx = 0.51, rely=0.26)

        add_button = Button(add_car_frame, text='Добавить автомобиль', bg='white', command=lambda: (self.car_bd(combobox.get(), id_for_new_car.get(), add_car_frame), self.delete_by_time()))
        add_button.place(relx = 0.45, rely=0.30, width=150)

        back_btn = Button(add_car_frame, text='Назад', bg='white', command=lambda: (add_car_frame.destroy(), self.delete_by_time()))
        back_btn.place(relx = 0.45, rely=0.35, width=150)

    def delete_car_page(self):
        del_car_frame = Frame(root, bg='blue')
        del_car_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(del_car_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        dcf_title = Label(del_car_frame, text='Удаление автомобилей', bg='red', font=30)
        dcf_title.place(relx=0.4, rely=0.1, width=300)
        list_of_car = self.view_BD(2)
        clear_list = []
        for i in list_of_car:
            if int(i[-1]) == 0:
                clear_list.append([i[0], i[1]])
        var1 = StringVar()
        combobox = ttk.Combobox(del_car_frame, textvariable=var1)
        combobox['values'] = clear_list
        combobox['state'] = 'readonly'
        combobox.place(relx=0.35, rely=0.2, width=500)
        del_btn = Button(del_car_frame, text='удалить автомобиль', bg='white', command=lambda: (self.car_del(combobox.get(), del_car_frame)))
        del_btn.place(relx = 0.45, rely=0.30, width=150)
        back_btn = Button(del_car_frame, text='Назад', bg='white', command=lambda: (del_car_frame.destroy(), self.delete_by_time()))
        back_btn.place(relx = 0.45, rely=0.35, width=150)



    def view_free_cars_page(self): #Просмотр свободных машин
        view_free_frame = Frame(root, bg='blue')
        view_free_frame.place(relwidth=1, relheight=1)
        vfcp_title = Label(view_free_frame, text='Просмотр доступных автомобилей', bg='red', font=30)
        vfcp_title.place(relx=0.35, rely=0.1, width=350)
        list_of_free_cars = self.view_BD(2)
        list_of_offers = self.view_BD(3)
        free_cars = []
        for i in list_of_free_cars:
            for j in list_of_offers:
                if int(i[-1]) == 1:
                    continue
                if int(i[-1]) == 0 or (int(i[-1]) == 2 and j[0] == self.name and int(i[1]) == int(j[1])):
                    free_cars.append(i)
        free_cars = set(list_of_free_cars)
        output_list = []
        for i in free_cars:
            output_list.append(str(i[0])+' ' + str(i[1]))
        print(output_list)
        cars_var = StringVar(value=output_list)
        listbox = Listbox(view_free_frame,listvariable=cars_var)
        listbox.place(relx=0.35,  rely=0.2, width=500, height=300)

        scrollbar = ttk.Scrollbar(listbox,orient="vertical", command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox["yscrollcommand"] = scrollbar.set
        # for i in range(len(all_cars)):
        #     new_label = Label(view_Frame,text=all_cars[i], bg='blue', font=30)
        #     new_label.pack()
        back_btn = Button(view_free_frame, text='Назад', bg='white',
                          command=lambda: (view_free_frame.destroy(), self.delete_by_time()))
        back_btn.place(relx=0.45, rely=0.7, width=150)


    def view_all_cars_page(self): #Просмотр всего имеющегося транспорта
        view_Frame = Frame(root, bg='blue')
        view_Frame.place(relwidth=1, relheight=1)
        vacp_title = Label(view_Frame, text='Просмотр всех автомобилей', bg='red', font=30)
        vacp_title.place(relx=0.4, rely=0.1, width=300)
        all_cars = self.view_BD(2)
        output_list = []
        for i in all_cars:
            output_list.append(str(i[0])+' ' + str(i[1]))
        cars_var = StringVar(value=output_list)
        listbox = Listbox(view_Frame,listvariable=cars_var)
        listbox.place(relx=0.35,  rely=0.2, width=500, height=300)

        scrollbar = ttk.Scrollbar(listbox,orient="vertical", command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox["yscrollcommand"] = scrollbar.set
        # for i in range(len(all_cars)):
        #     new_label = Label(view_Frame,text=all_cars[i], bg='blue', font=30)
        #     new_label.pack()
        back_btn = Button(view_Frame, text='Назад', bg='white',
                          command=lambda: (view_Frame.destroy(), self.delete_by_time()))
        back_btn.place(relx=0.45, rely=0.7, width=150)

    def main_page(self, name): #Основная страница пользователя
        self.name = name
        main_Frame = Frame(root, bg='blue')
        main_Frame.place(relwidth=1, relheight=1)
        main_title = Label(main_Frame, text='Главное меню', bg='red', font=30)
        main_title.place(relx=0.4, rely=0.1, width=300)

        mnbtn1 = Button(main_Frame, text='Просмотреть весь доступный транспорт', bg='white', command=lambda: (self.view_all_cars_page(), self.delete_by_time()))
        mnbtn1.place(relx=0.41, rely=0.2, width=270)

        mnbtn2= Button(main_Frame, text='Просмотреть весь свободный транспорт', bg='white', command=lambda: (self.view_free_cars_page(), self.delete_by_time()))
        mnbtn2.place(relx=0.41, rely=0.25, width=270)

        mnbtn3 = Button(main_Frame, text='Просмотреть транспорт по грузоподъёмности', bg='white', command=lambda: (self.sort_models_page(), self.delete_by_time()))
        mnbtn3.place(relx=0.41, rely=0.3, width=270)

        mnbtn4 = Button(main_Frame, text='Создать новую заявку на перевоз', bg='white', command=lambda: (self.new_offer_page(), self.delete_by_time()))
        mnbtn4.place(relx=0.41, rely=0.35, width=270)

        mnbtn5 = Button(main_Frame, text='Подобрать и забронировать транспорт', bg='white', command=lambda: (self.parametres_page(), self.delete_by_time()))
        mnbtn5.place(relx=0.41, rely=0.4, width=270)

        mnbtn6 = Button(main_Frame, text='Выйти из аккаунта', bg='white', command=lambda: (self.start_page(), main_Frame.destroy(), self.delete_by_time()))
        mnbtn6.place(relx=0.41, rely=0.45, width=270)

        mnbtn7 = Button(main_Frame, text='Выйти из системы', bg='white', command=exit)
        mnbtn7.place(relx=0.41, rely=0.5, width=270)


    def admin_page(self, name):
        self.name =name
        admin_Frame = Frame(root, bg='blue')
        admin_Frame.place(relwidth=1, relheight=1)


        main_title = Label(admin_Frame, text='Главное меню', bg='red', font=30)
        main_title.place(relx=0.4, rely=0.1, width=300)

        admbtn1 = Button(admin_Frame, text='Добавить автомобиль', bg='white', command=lambda: (self.add_new_car_page(), self.delete_by_time()))
        admbtn1.place(relx=0.41, rely=0.2, width=270)

        admbtn2 = Button(admin_Frame, text='Удалить автомобиль', bg='white', command=lambda: (self.delete_car_page(), self.delete_by_time()))
        admbtn2.place(relx=0.41, rely=0.25, width=270)

        mnbtn1 = Button(admin_Frame, text='Просмотреть весь доступный транспорт', bg='white', command=lambda: (self.view_all_cars_page(), self.delete_by_time()))
        mnbtn1.place(relx=0.41, rely=0.3, width=270)

        mnbtn2 = Button(admin_Frame, text='Просмотреть весь свободный транспорт', bg='white', command=lambda: (self.view_free_cars_page(), self.delete_by_time()))
        mnbtn2.place(relx=0.41, rely=0.35, width=270)

        mnbtn3 = Button(admin_Frame, text='Просмотреть транспорт по грузоподъёмности', bg='white', command=lambda: (self.sort_models_page(), self.delete_by_time()))
        mnbtn3.place(relx=0.41, rely=0.4, width=270)

        mnbtn4 = Button(admin_Frame, text='Создать новую заявку на перевоз', bg='white', command=lambda : (self.new_offer_page(), self.delete_by_time()))
        mnbtn4.place(relx=0.41, rely=0.45, width=270)

        mnbtn5 = Button(admin_Frame, text='Подобрать и забронировать транспорт', bg='white', command=lambda: (self.parametres_page(), self.delete_by_time()))
        mnbtn5.place(relx=0.41, rely=0.5, width=270)

        mnbtn6 = Button(admin_Frame, text='Выйти из аккаунта', bg='white',
                        command=lambda: (self.start_page(), admin_Frame.destroy(), self.delete_by_time()))
        mnbtn6.place(relx=0.41, rely=0.55, width=270)

        mnbtn7 = Button(admin_Frame, text='Выйти из системы', bg='white', command=exit)
        mnbtn7.place(relx=0.41, rely=0.6, width=270)


    def log_in_page0(self): #Обычный вход
        frame.destroy()
        log_frame = Frame(root, bg='blue')
        log_frame.place(relwidth=1, relheight=1)

        #Добавить на все страницы кроме главной
        exit_btn = Button(log_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        title1 = Label(log_frame, text='Введите логин и пароль', bg='red', font=30, width=300)
        title1.place(relx=0.4, rely=0.05, width=300)

        title_login = Label(log_frame, text='Логин:', bg='blue', font=30, fg='white')
        title_login.place(relx=0.4, rely=0.1, width=130)

        self.LoginInput = Entry(log_frame, bg='white')
        self.LoginInput.place(relx=0.47, rely=0.11)

        title_password = Label(log_frame, text='Пароль:', bg='blue', font=30, fg='white')
        title_password.place(relx=0.4, rely=0.18, width=130)

        PasswordInput = Entry(log_frame, bg='white', show='*')
        PasswordInput.place(relx=0.47, rely=0.19)

        self.name=self.LoginInput.get()
        password = PasswordInput.get()
        btn_in = Button(log_frame, text='Зайти', bg='white', command=lambda: (self.BD_check(self.LoginInput.get(), PasswordInput.get(), 0, log_frame), self.delete_by_time()))
        btn_in.place(relx=0.45, rely=0.25, width=150)
        back_button = Button(log_frame, text='Вернуться в главное меню', bg='white',
                             command=lambda: (log_frame.destroy(), self.delete_by_time(), self.start_page()))
        back_button.place(relx=0.45, rely=0.3, width=150)

    def log_in_page1(self): #админский вход
        frame.destroy()
        log_frame = Frame(root, bg='blue')
        log_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(log_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)


        title1 = Label(log_frame, text='Введите свои данные', bg='red', font=30)
        title1.place(relx=0.4, rely=0.05, width=300)
        title_login = Label(log_frame, text='Логин:', bg='blue', font=30, fg='white')
        title_login.place(relx=0.4, rely=0.1, width=130)

        self.LoginInput = Entry(log_frame, bg='white')
        self.LoginInput.place(relx=0.47, rely=0.1)

        title_password = Label(log_frame, text='Пароль:', bg='blue', font=30, fg='white')
        title_password.place(relx=0.4, rely=0.18, width=130)

        PasswordInput = Entry(log_frame, bg='white', show='*')
        PasswordInput.place(relx=0.47, rely=0.18)

        self.name = self.LoginInput.get()
        password = PasswordInput.get()
        btn_in1 = Button(log_frame, text='Зайти', bg='white', command=lambda: (self.BD_check(self.LoginInput.get(), PasswordInput.get(), 1, log_frame), self.delete_by_time()))
        btn_in1.place(relx=0.45, rely=0.25, width=150)
        back_button = Button(log_frame, text='Вернуться в главное меню', bg='white',
                             command=lambda: (log_frame.destroy(), self.delete_by_time(), self.start_page()))
        back_button.place(relx=0.45, rely=0.3, width=150)


    def log_in_page2(self): #регистрация
        frame.destroy()
        log_frame = Frame(root, bg='blue')
        log_frame.place(relwidth=1, relheight=1)

        exit_btn = Button(log_frame, text='X', bg='red', fg='white', command=exit, font=200)
        exit_btn.place(relx=0.98, rely=0, height=30, width=40)

        title1 = Label(log_frame, text='Введите свои данные', bg='red', font=30)
        title1.place(relx=0.4, rely=0.05, width=300)
        title_login = Label(log_frame, text='Логин:', bg='blue', font=30, fg='white')
        title_login.place(relx=0.4, rely=0.1, width=130)

        self.LoginInput = Entry(log_frame, bg='white')
        self.LoginInput.place(relx=0.47, rely=0.1)

        title_password = Label(log_frame, text='Пароль:', bg='blue', font=30, fg='white')
        title_password.place(relx=0.4, rely=0.18, width=130)

        PasswordInput = Entry(log_frame, bg='white', show='*')
        PasswordInput.place(relx=0.47, rely=0.18)

        btn_in2 = Button(log_frame, text='Зарегистрироваться', bg='white', command=lambda: (self.BD_update(self.LoginInput.get(), PasswordInput.get(), 0, log_frame), self.delete_by_time()))
        btn_in2.place(relx=0.45, rely=0.25, width=150)
        back_button = Button(log_frame, text='Вернуться в главное меню', bg='white',
                             command=lambda: (log_frame.destroy(), self.delete_by_time(), self.start_page()))
        back_button.place(relx=0.45, rely=0.3, width=150)


    def start_page(self):
        canvas = Canvas(root, height=700, width=700)
        canvas.pack()
        global frame
        frame = Frame(root, bg='blue')
        frame.place(relwidth=1, relheight=1)
        title = Label(frame, text='Truck manager 2023', bg='red', font=30)
        title.place(relx=0.4, rely=0.05, width=300)
        title = Label(frame, text='Добро пожаловать', bg='blue', font=30)
        title.place(relx=0.4, rely=0.1, width=300)
        btn = Button(frame, text='Войти', bg='white', command=lambda: (self.log_in_page0(), self.delete_by_time()))
        btn.place(relx=0.45, rely=0.2, width=150)
        btn2 = Button(frame, text='Войти как администратор', bg='white', command=lambda: (self.log_in_page1(), self.delete_by_time()))
        btn2.place(relx=0.45, rely=0.25, width=150)
        btn3 = Button(frame, text='Зарегистрироваться', bg='white', command=lambda: (self.log_in_page2(), self.delete_by_time()))
        btn3.place(relx=0.45, rely=0.3, width=150)
        btn4 = Button(frame, text='Выйти', bg='white', command=exit)
        btn4.place(relx=0.45, rely=0.35, width=150)

    def start_app(self):
        global root
        root = Tk()
        root.attributes('-fullscreen', True)
        root.title('Грузоперевозки')
        # root.geometry('1024x960')
        self.start_page()
        root.mainloop()

v = InterFace()
v.start_app()