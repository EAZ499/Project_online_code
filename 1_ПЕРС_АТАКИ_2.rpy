



default undertale_ratio = 0.0
default xalign_val = 0.0
default direction = 1

default atk_ind_ratio = 1

# Функция для записи отладочных логов в файл
init python:
    import datetime
    
    def debug_log(message):
        """Записывает отладочное сообщение в файл с временной меткой"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open("debug_log.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            renpy.log(f"Ошибка записи в лог-файл: {e}")
        
        # Также выводим в консоль Ren'Py
        renpy.log(message)

label Remove_screens:
    #экраны появления кнопок
    hide screen fvapp
    hide screen ivapp
    hide screen avapp
    hide screen mvapp

    # экран toc
    hide screen ftoc
    hide screen itoc
    hide screen mtoc
    hide screen atoc

    # экран tob
    hide screen ftob
    hide screen itob
    hide screen mtob
    hide screen atob


    hide dialogue1round
    hide dialogue
    show dialogue at dud

    # экраны choice из 2_ПЕРС_АТАКИ.rpy
    hide screen choose_attack_screen
    hide screen actchoice1
    hide screen choose_magic_screen
    hide screen itemchoice2
    
    # экраны choice из 2_ИНТЕРФЕЙС_БОЯ_МЕНЮ.rpy
    if attackdesisopen == 1:
        hide screen attack_description
    hide screen turntarget
    #hide screen team_status_display
    
    # экран attack_name_display из 2_ИНТЕРФЕЙС_БОЯ.rpy
    hide screen attack_name_display
    
    # дополнительные экраны из 2_ИНТЕРФЕЙС_БОЯ.rpy
    hide screen fbackapp
    hide screen fbackdis
    hide screen abackapp
    hide screen abackdis
    hide screen ibackapp
    hide screen ibackdis
    hide screen mbackapp
    hide screen mbackdis
    hide screen fightbuttom
    hide screen fightbackbuttom
    hide screen actbuttom
    hide screen actbackbuttom
    hide screen magicbuttom
    hide screen magicbackbuttom
    hide screen itembuttom
    hide screen itembackbuttom
    hide screen pause
    
    # Установка переменных статуса в 0 (закомментировано, чтобы не скрывать экраны персонажей)
    $ show_enemy_status = 0
    # $ show_team_status = 0
    
    # Показываем переключатели
    if nextswitch_style == 1:
        show switchnext at nud
    if prevswitch_style == 1:
        show switchprev at pud
    $ nextswitch_style = 0
    $ prevswitch_style = 0

    # Пауза и скрытие переключателей
    $ renpy.pause(0.6, hard=True)
    hide switchnext
    hide switchprev
    # Добавляем логирование для диагностики проблемы
    #$ renpy.log(">>> Вызываем экран Heroattacks, текущие экраны: " + str(renpy.get_screen_stack()))

    #$ renpy.log("<<< Экран Heroattacks завершил работу")

# Лейбл для выполнения хода персонажа
# Сначала скрывает все экраны, затем вызывает экран атаки
label Heroperformsturn:
    $ store.pokaz_poshad = 0
    # Магия оплачивается только после подтверждения цели. Наведение на кнопку
    # использует тот же расчёт, но не меняет текущие MP/HP.
    if not pay_ability_cost(attackindex):
        $ renpy.notify("Недостаточно MP или HP для этого умения.")
        jump playerturn2
    # Фиксируем КД/одноразовость после подтверждения цели и оплаты,
    # чтобы отменённый выбор не сжигал способность.
    $ commit_battle_ability(attackindex)
    # Учёт действий: обычное действие +1, магия обнуляет счётчик.
    # Значение до обнуления сохраняется для «Слабого места».
    $ register_action_for_current(attackindex)
    # Добавляем логирование для диагностики проблемы
    #$ renpy.log(">>> Вызываем Remove_screens, текущие экраны: " + str(renpy.get_screen_stack()))
    
    #call Remove_screens
    hide screen inventory_desc

    hide screen enemydesc
    hide screen fullstats1_copy2

    #экраны появления кнопок
    hide screen fvapp
    hide screen ivapp
    hide screen avapp
    hide screen mvapp

    # экран toc
    hide screen ftoc
    hide screen itoc
    hide screen mtoc
    hide screen atoc

    # экран tob
    hide screen ftob
    hide screen itob
    hide screen mtob
    hide screen atob


    hide dialogue1round
    hide dialogue
    show dialogue at dud

    # экраны choice из 2_ПЕРС_АТАКИ.rpy
    hide screen choose_attack_screen
    hide screen actchoice1
    hide screen choose_magic_screen
    hide screen itemchoice2
    
    # экраны choice из 2_ИНТЕРФЕЙС_БОЯ_МЕНЮ.rpy
    if attackdesisopen == 1:
        hide screen attack_description
    hide screen turntarget
    #hide screen team_status_display
    
    # экран attack_name_display из 2_ИНТЕРФЕЙС_БОЯ.rpy
    hide screen attack_name_display
    
    # дополнительные экраны из 2_ИНТЕРФЕЙС_БОЯ.rpy
    hide screen fbackapp
    hide screen fbackdis
    hide screen abackapp
    hide screen abackdis
    hide screen ibackapp
    hide screen ibackdis
    hide screen mbackapp
    hide screen mbackdis
    hide screen fightbuttom
    hide screen fightbackbuttom
    hide screen actbuttom
    hide screen actbackbuttom
    hide screen magicbuttom
    hide screen magicbackbuttom
    hide screen itembuttom
    hide screen itembackbuttom
    hide screen pause
    
    # Установка переменных статуса в 0 (закомментировано, чтобы не скрывать экраны персонажей)
    $ show_enemy_status = 0
    # $ show_team_status = 0
    
    # Показываем переключатели
    if nextswitch_style == 1:
        show switchnext at nud
    if prevswitch_style == 1:
        show switchprev at pud
    $ nextswitch_style = 0
    $ prevswitch_style = 0

    # Пауза и скрытие переключателей
    #$ renpy.pause(0.6, hard=True)
    hide switchnext
    hide switchprev
    
    
    
    $ renpy.pause (0.7, hard = True)
    #$ renpy.log("<<< Remove_screens завершил работу, текущие экраны: " + str(renpy.get_screen_stack()))
    
    call screen Heroattacks()

    






# Инициализация переменных. `default` используется, чтобы переменные
# сбрасывались при загрузке или начале новой игры.
# Переменные для атаки Кловера "Прицельный"
default clover_stick_xpos = 1400  # Начальная позиция горизонтальной палки по X
default clover_stick_ypos = 600   # Начальная позиция вертикальной палки по Y
default clover_x_moving = True    # Флаг движения горизонтальной палки
default clover_y_moving = True    # Флаг движения вертикальной палки
default clover_final_xpos = 0     # Финальная позиция X для перекрестья
default clover_final_ypos = 0     # Финальная позиция Y для перекрестья

# Создаем специальный transform для палочки, который будет обновляться
transform stick_transform:
    xpos kris_atk1_stick_xpos
    yalign 0.5

init python:
    import random

    kris_atk1_stick_xpos = 1400
    kris_atk1_stick_speed = 0
    kris_atk1_stick_is_moving = True

    def init_kris_atk1_stick():
        global kris_atk1_stick_xpos, kris_atk1_stick_speed, kris_atk1_stick_is_moving
        kris_atk1_stick_xpos = 1280
        kris_atk1_stick_speed = get_random_speed()
        kris_atk1_stick_is_moving = True

    def stop_kris_atk1_stick():
        global kris_atk1_stick_is_moving
        kris_atk1_stick_is_moving = False
    # Эта функция будет вызываться таймером на экране

    def get_random_speed():
        return random.randint(5, 10)
    
    def calculate_kris_atk1_perform(x_position):
        """
        Вычисляет значение perform для атаки Криса "удар неудачника" на основе положения индикатора.
        
        Args:
            x_position: Текущая позиция индикатора по оси X
             
        Returns:
            float: Значение perform в соответствии с таблицей
        """
        renpy.log(f"=== НАЧАЛО РАСЧЕТА PERFORM ===")
        renpy.log(f"Позиция индикатора: {x_position}")
        
        # Определяем значение perform на основе прямой позиции stick_xpos
        # Диапазон движения от 1400 до -40
        if x_position >= 1041 and x_position <= 1400:
            result = 0.20
        elif x_position >= 951 and x_position <= 1040:
            result = 0.40
        elif x_position >= 831 and x_position <= 950:
            result = 0.60
        elif x_position >= 701 and x_position <= 830:
            result = 0.80
        elif x_position >= 661 and x_position <= 700:
            result = 0.90
        elif x_position >= 621 and x_position <= 660:
            result = 1.00
        elif x_position >= 591 and x_position <= 620:
            result = 0.90
        elif x_position >= 451 and x_position <= 590:
            result = 0.80
        elif x_position >= 351 and x_position <= 450:
            result = 0.60
        elif x_position >= 236 and x_position <= 350:
            result = 0.40
        elif x_position >= 0 and x_position <= 235:
            result = 0.20
        elif x_position >= -40 and x_position <= -1:
            result = 0.20
        else:
            # Вне диапазона, возвращаем минимальное значение
            result = 0
        
        renpy.log(f"Рассчитанный perform: {result}")
        renpy.log(f"=== КОНЕЦ РАСЧЕТА PERFORM ===")
        return result

    def kris_atk1_indic_dd(st, at):
        if st < 0.5:
            cur_ysize = int(242 * (st / 0.5))
        else:
            cur_ysize = 242

        return Transform(
            "kris_atk1_indic.png",
            xpos=kris_atk1_stick_xpos - 20,
            yalign=0.5,
            ysize=cur_ysize,
        ), 0
    

    def update_stick_position():
        global kris_atk1_stick_xpos, kris_atk1_stick_is_moving

        if not kris_atk1_stick_is_moving:
            return

        # Используем текущую скорость, установленную в переменной stick_speed
        # Двигаем спрайт влево. Меняйте число, чтобы изменить скорость.
        # Чем меньше число, тем медленнее движение.
        kris_atk1_stick_xpos -= kris_atk1_stick_speed
        
        # Обновляем значение base_perform на основе текущей позиции индикатора
        store.base_perform = calculate_kris_atk1_perform(kris_atk1_stick_xpos)

        # Если спрайт достиг конечной точки (xpos 200)
        if kris_atk1_stick_xpos <= -40:
            kris_atk1_stick_xpos = -40  # Останавливаем его на границе
            kris_atk1_stick_is_moving = False # И отключаем движение
            # Устанавливаем popal для текущего атакующего персонажа
            if current_attacker == 1:  # Крис
                store.pers_dict["Крис"].popal = 0
            elif current_attacker == 2:  # Азриель
                store.pers_dict["Азриель"].popal = 0
            elif current_attacker == 3:  # Чара
                store.pers_dict["Чара"].popal = 0
            elif current_attacker == 4:  # Фриск
                store.pers_dict["Фриск"].popal = 0
            elif current_attacker == 5:  # Иззи
                store.pers_dict["Иззи"].popal = 0
            elif current_attacker == 6:  # Кловер
                store.pers_dict["Кловер"].popal = 0
            elif current_attacker == 7:  # Седрик
                store.pers_dict["Седрик"].popal = 0
        # popal теперь устанавливается в методе calculate_dmg персонажа

    def update_clover_x_position():
        # Обновляем позицию горизонтальной палки Кловера
        global clover_stick_xpos, clover_x_moving, clover_final_xpos

        # Если движение остановлено, ничего не делаем
        if not clover_x_moving:
            return
        
        # Используем случайную скорость, определенную в экране
        # Если переменная не установлена, используем значение по умолчанию
        if not hasattr(store, 'clover_x_speed'):
            store.clover_x_speed = 30

        # Двигаем палку влево
        clover_stick_xpos -= store.clover_x_speed

        # Если палка достигла конечной точки (xpos 200)
        if clover_stick_xpos <= 200:
            clover_stick_xpos = 200  # Останавливаем её на границе
            clover_x_moving = False # И отключаем движение
            clover_final_xpos = 200  # Сохраняем финальную позицию X

    def update_clover_y_position():
        # Обновляем позицию вертикальной палки Кловера
        global clover_stick_ypos, clover_y_moving, clover_final_ypos

        # Если движение остановлено, ничего не делаем
        if not clover_y_moving:
            return
        
        # Используем случайную скорость, определенную в экране
        # Если переменная не установлена, используем значение по умолчанию
        if not hasattr(store, 'clover_y_speed'):
            store.clover_y_speed = 30

        # Двигаем палку вверх (уменьшаем Y)
        clover_stick_ypos -= store.clover_y_speed

        # Если палка достигла конечной точки (ypos 100)
        if clover_stick_ypos <= 100:
            clover_stick_ypos = 100  # Останавливаем её на границе
            clover_y_moving = False # И отключаем движение
            clover_final_ypos = 100  # Сохраняем финальную позицию Y



