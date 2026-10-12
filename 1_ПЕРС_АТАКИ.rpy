# hello world
default Krisatk2random = 1






default wheel_angle = 0.0
default wheel_is_moving = True
default wheel_speed = 1.2
default wheel_attempts_left = 3
default wheel_disappear_count = 0
default knife_press_count = 0
default chara_atk1_udar = 0

init python:
    def update_wheel_position():
        if getattr(store, "wheel_is_moving", False):
            # Берем скорость, которую мы сгенерировали в on "show"
            speed = getattr(store, "wheel_speed", 3.0) 
            store.wheel_angle = (store.wheel_angle - speed) % 360.0

    def calculate_wheel_perform(angle):
        """
        Расчет перформа на основе диапазонов отклонения от цели (-90 градусов):
        Центр:   от -10 до 10  -> 1.0
        Боковые: от -20 до -10 и от 10 до 20 -> 0.85
        Крайние: от -30 до -20 и от 20 до 30 -> 0.7
        Вне зон: иначе -> 0.5
        """
        # 1. Сдвигаем угол на 90 градусов, чтобы наша цель (-90) стала нулем (0)
        shifted_angle = (angle + 90.0) % 360.0
        
        # 2. Приводим к диапазону от -180 до 180, чтобы корректно работать с отрицательными числами
        if shifted_angle > 180.0:
            shifted_angle -= 360.0
            
        # 3. Теперь shifted_angle — это наше отклонение (например, -15, 0, 25 и т.д.)
        # Берем модуль (абсолютное значение), чтобы проверять только расстояние от центра
        dev = abs(shifted_angle)
        
        # 4. Проверяем диапазоны по возрастанию расстояния от центра
        if dev <= 7.0:
            return 1.0
        elif dev <= 13.0:
            return 0.95
        elif dev <= 17:
            return 0.9
        elif dev <= 21.0:
            return 0.85
        elif dev <= 25.0:
            return 0.8
        elif dev <= 30.0:
            return 0.75
        elif dev <= 60.0:
            return 0.6
        elif dev <= 90.0:
            return 0.5
        elif dev <= 120.0:
            return 0.35
        else:
            return 0.2






    def fix_wheel_perform():
        """Фиксирует результат при нажатии центральной кнопки."""
        perf = calculate_wheel_perform(store.wheel_angle)
        store.base_perform = perf                    # ← свойство perform прочитает это значение
        store.pers_dict["Чара"].popal = 1


    def update_wheel_knife_v3():
        """
        Вращает колесо. Если угол > 230, увеличивает счетчик исчезновений
        и сбрасывает угол/скорость. Если счетчик >= 3, останавливает игру.
        """
        if getattr(store, "wheel_is_moving", False):
            speed = getattr(store, "wheel_speed", 1.2)
            store.wheel_angle += speed

            # Проверка на авто-исчезновение (вылет за 230 градусов)
            if store.wheel_angle > 230.0:
                store.wheel_disappear_count += 1
                store.wheel_angle = 0.0
                store.wheel_speed = renpy.random.uniform (4.0, 6.0) #(2.0, 5.0)

                # Проверка на завершение (3 исчезновения)
                if store.wheel_disappear_count >= 3:
                    store.wheel_is_moving = False
                    # Jump обработает таймер в экране, так как прямой Jump из функции недопустим

    def get_knife_multiplier(angle):
        """
        Возвращает множитель для base_perform на основе угла.
        Центр зоны = 180 градусов.
        """
        # Нормализуем угол к диапазону 0-360
        a = angle % 360.0

        # Вычисляем отклонение от 180 градусов
        dev = abs(a - 180.0)

        # Корректировка для перехода через 0/360
        if dev > 180.0:
            dev = 360.0 - dev

        if dev <= 7.0:
            return 1.0
        elif dev <= 13.0:
            return 0.95
        elif dev <= 17:
            return 0.9
        elif dev <= 21.0:
            return 0.85
        elif dev <= 25.0:
            return 0.8
        elif dev <= 30.0:
            return 0.75


        elif dev <= 60.0:
            return 0.6
        elif dev <= 90.0:
            return 0.5
        elif dev <= 120.0:
            return 0.35
        else:
            return 0.2

    def knife_button_action_v3():
        """
        Обработка нажатия кнопки для 'Удара ножом'.
        Добавляет перформ с учетом угла, сбрасывает угол, увеличивает счетчик.
        """
        # 1. Получаем множитель на основе текущего угла
        multiplier = get_knife_multiplier(store.wheel_angle)

        # Счётчик нажатий — для перезапуска анимации текста заряда
        store.knife_press_count += 1

        # 2. Добавляем перформ (базовая прибавка 0.333 * множитель)
        current_perf = getattr(store, "base_perform", 0.0)
        addition = 0.333 * multiplier
        store.base_perform = min(1.0, current_perf + addition)

        # 3. Фиксируем нажатие
        store.kris1_atk_pressed = 1

        # 4. Увеличиваем счетчик исчезновений
        store.wheel_disappear_count += 1

        # 5. Сбрасываем угол и скорость для нового индикатора
        store.wheel_angle = 0.0
        store.wheel_speed = renpy.random.uniform(4.0, 6.0)

        # 6. Проверка на завершение (3 исчезновения)
        if store.wheel_disappear_count >= 3:
            store.wheel_is_moving = False







transform chara_fight1_timer:
    alpha 0.0 xanchor 0.0 xpos 300 ypos 100
    ease 0.5 alpha 1.0
    ease 7.0 xzoom 0.0 xanchor 0.0



transform kris_fight2_bg:
    alpha 0.0 xanchor 1.0 xzoom 0
    easein 0.5 alpha 1.0 xzoom 1.0
    pause 4.0
    xanchor 0.0 xoffset -700
    easeout 0.5 alpha 0.0 xzoom 0.0 


transform kris_fight2_black:
    alpha 0.0
    easein 0.5 alpha 0.5


transform kris_fight2_sword:
    alpha 0.0
    easein 0.5 alpha 1.0

transform kris_fight2_timer:
    alpha 0.0 xanchor 0.0 xpos 300 ypos 10
    ease 0.5 alpha 1.0
    ease 4.0 xzoom 0.0 xanchor 0.0

transform perform_pulse1:
    zoom 1.0
    easein 0.2 zoom 1.6
    easeout 0.5 zoom 1.3

transform perform_pulse2:
    zoom 1.2
    easein 0.1 zoom 1.8
    easeout 0.5 zoom 1.5

transform perform_pulse3:
    zoom 1.5
    easein 0.1 zoom 2.1
    easeout 0.5 zoom 1.8








default kris_fight2_is_done = 0

screen Heroattacks():
    zorder 99999999
    on "show" action [
        If(
            attackindex == "Удар мечом",
            [
                SetVariable("kris_fight2_is_done", 0),
                SetVariable("base_perform", 0),
                SetVariable("Krisatk2random", renpy.random.randint(1, 5)),
                SetField(pers_dict['Крис'], 'state', "fight2_0"),
            ],
            NullAction(),
        ),
        If(
            attackindex == "Удар щитом",
            [
                SetVariable("base_perform", 0.3),
                SetField(pers_dict['Крис'], 'state', "fight3_0"),
            ],
            NullAction(),
        ),
        If(attackindex in ("Удар бунтарки",), [
            SetVariable("wheel_angle", 0.0),
            SetVariable("wheel_is_moving", True),
            # Генерируем скорость один раз при старте атаки (например, от 2 до 4 градусов за тик)
            SetVariable("wheel_speed", renpy.random.uniform(4.0, 6.0)), 
            SetVariable("kris1_atk_pressed", 0),
            SetVariable("chara_atk1_udar", 0),  # Сброс цвета текста "Удар"
            ], 
            NullAction()
        ),
        If(attackindex == "Удар ножом", [
            SetVariable("wheel_angle", 0.0),
            SetVariable("wheel_is_moving", True),
            SetVariable("wheel_speed", renpy.random.uniform(4.0, 6.0)),  # Начальная скорость
            SetVariable("base_perform", 0.0),  # Начинаем с 0
            SetVariable("kris1_atk_pressed", 0),
            SetVariable("wheel_disappear_count", 0),  # Сбрасываем счетчик
            SetVariable("knife_press_count", 0),  # Сброс для анимации заряда
            SetVariable("chara_atk1_udar", 0),  # Сброс цвета текста "Удар"
        ], NullAction()),
        If(
            attackindex == "Удар неудачника",
            [
                Function(init_kris_atk1_stick),
            ],
            NullAction(),
        ),
        ]
    

    if getattr(store, "itemchoice", 0) == 1 and target is not None:
        timer 0.01 action Jump("perform_item")
    
    elif store.turntype == "totarget" and isinstance(attackindex, str) and attackindex in ACTS_CONFIG:
        timer 0.01 action Jump ("hero_acts")

    #timer 0.01 action Jump("Remove_screens")
    
    # Показываем экран heroattacks для выполнения магии
    # Это заменяет вызов функции perform_magic_by_index

    # ========================================================================
    # ЗАЩИТА
    # ========================================================================
    
    if attackindex and attackindex.startswith("защита_"):
        timer 0.1 action Jump("herodefend")

    # ========================================================================
    # АТАКИ КРИСА
    # ========================================================================

    elif attackindex == "Удар неудачника":
        add Solid("#000000", xysize=(1280, 720)) at kris_fight2_black
        #timer 0.03 action SetVariable ("scalespeed", 5)
        add "kris_atk1_bg.png" at attack_scale

        # Спрайт палочки. Его позиция будет зависеть от переменной stick_xpos
        add DynamicDisplayable(kris_atk1_indic_dd)
                


        # Таймер, который каждые 0.03 секунды вызывает нашу функцию для движения
        timer 0.01 repeat True action Function(update_stick_position)

        # Кнопка для ОСТАНОВКИ движения палочки
        imagebutton:
            at kris_atk1_indic_hide2
            xalign 0.5
            yalign 0.95
            idle "images/Kris_atk1_idle.png"
            hover "images/Kris_atk1_hover.png"
            action [Function(stop_kris_atk1_stick), SetVariable ("kris1_atk_pressed", 1), Jump("kris_atk1_is_done")]
        timer 7 action [Function(stop_kris_atk1_stick), SetVariable ("kris1_atk_pressed", 0), Jump("kris_atk1_is_done")]











    elif attackindex == "Удар мечом":
        
        timer 4.5 action SetVariable("kris_fight2_is_done", 1)
        add Solid("#000000", xysize=(1280, 720)) at kris_fight2_black
        add Solid("#ffffff", xysize=(700, 30)) at kris_fight2_timer 
        # Удар мечом - мини-игра
        frame:
            padding (10,10)
            xysize (700, 600) xpos 1000 ypos 50
            at kris_fight2_bg
            background "#ffffff"
            frame:
                background "#000000"



        if store.kris_fight2_is_done == 0:
            vbox:
                xoffset -50
                at kris_fight2_sword
                xalign 0.5
                yalign 0.5

                if base_perform < (1.0 / 7.0):
                    imagebutton:
                        idle "images/Kris_atk2_{}.1.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.1.png".format(Krisatk2random)
                        focus_mask True
                        hovered SetVariable("base_perform", 1.0 / 7.0)
                        action NullAction()

                elif base_perform < (2.0 / 7.0):
                    imagebutton:
                        idle "images/Kris_atk2_{}.2.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.2.png".format(Krisatk2random)
                        focus_mask True
                        hovered SetVariable("base_perform", 2.0 / 7.0)
                        action NullAction()

                elif base_perform < (3.0 / 7.0):
                    imagebutton:
                        idle "images/Kris_atk2_{}.3.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.3.png".format(Krisatk2random)
                        focus_mask True
                        hovered SetVariable("base_perform", 3.0 / 7.0)
                        action NullAction()
                   
                elif base_perform < (4.0 / 7.0):
                    imagebutton:
                        idle "images/Kris_atk2_{}.4.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.4.png".format(Krisatk2random)
                        focus_mask True
                        hovered SetVariable("base_perform", 4.0 / 7.0)
                        action NullAction()

                elif base_perform < (5.0 / 7.0):
                    imagebutton:
                        idle "images/Kris_atk2_{}.5.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.5.png".format(Krisatk2random)
                        focus_mask True
                        hovered SetVariable("base_perform", 5.0 / 7.0)
                        action NullAction()

                elif base_perform < (6.0 / 7.0):
                    imagebutton:
                        idle "images/Kris_atk2_{}.6.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.6.png".format(Krisatk2random)
                        focus_mask True
                        hovered SetVariable("base_perform", 6.0 / 7.0)
                        action NullAction()

                else:
                    imagebutton:
                        idle "images/Kris_atk2_{}.7.png".format(Krisatk2random)
                        hover "images/Kris_atk2_{}.7.png".format(Krisatk2random)
                        focus_mask True
                        hovered [SetVariable("base_perform", 1.0), Jump("kris_atk2_is_done")]
                        action NullAction()

        
        if store.kris_fight2_is_done == 1:
            timer 0.6 action Jump("kris_atk2_is_done")
            button:
                xysize (1280,720)
                background "#000000"
                at alpha0
                action NullAction()










    elif attackindex == "Удар щитом":
        # Кликер: за четыре секунды нужно заполнить шкалу до 1.0.
        # Каждые 0.2 с сложность цели отнимает difficulty * 0.05 perform.
        timer 10.0 action Jump("kris_atk3_is_done")
        if target is not None:
            timer 0.02 repeat True action SetVariable(
                "base_perform",
                max(0.0, base_perform - target.kris_atk3_difficulty * 0.0025),
            )

        frame:
            xalign 0.5
            yalign 0.5
            xsize 720
            padding (32, 28)
            background "#171b2a"

            vbox:
                xfill True
                spacing 18

                text "Удар щитом" size 46 color "#ffffff" xalign 0.5
                text "Кликайте по щиту, пока шкала не достигнет 100%." size 24 color "#d8d8e6" xalign 0.5

                fixed:
                    xalign 0.5
                    xsize 640
                    ysize 44
                    add Solid("#3d4055") xsize 640 ysize 44
                    add Solid("#65d36e") xsize int(640 * max(0.0, min(base_perform, 1.0))) ysize 44
                    text "[int(base_perform * 100)]%" size 28 color "#ffffff" xalign 0.5 yalign 0.5

                if target is not None:
                    text "Сложность: [target.kris_atk3_difficulty:.2f]" size 26 color "#ffd76a" xalign 0.5
                    text "Сложность = итоговая атака противника / защита Криса" size 20 color "#c5c7d4" xalign 0.5
                    text "[target.atk:.1f] / [pers_dict['Крис'].defense:.1f] = [target.kris_atk3_difficulty:.2f]" size 20 color "#c5c7d4" xalign 0.5
                else:
                    text "Сложность = итоговая атака противника / защита Криса" size 20 color "#c5c7d4" xalign 0.5

                button:
                    xalign 0.5
                    xsize 430
                    ysize 140
                    background "#4268b8"
                    hover_background "#5a83d9"
                    action If(
                        base_perform >= 0.9,
                        [SetVariable("base_perform", 1.0), Jump("kris_atk3_is_done")],
                        SetVariable("base_perform", min(1.0, base_perform + 0.1)),
                    )
                    text "ЩИТ!\n+10%" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5








    elif attackindex == "C разворота!":
        # С Разворота! - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "С Разворота!" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("kris_atk4_is_done"):
                text_size 30

    elif attackindex == "Бонк!":
        # Бонк! - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Бонк!" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("kris_atk5_is_done"):
                text_size 30

    elif attackindex == "Пронзить":
        # Пронзить - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Пронзить" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("kris_atk6_is_done"):
                text_size 30

    elif attackindex == "Отбить руки":
        # Отбить руки - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Отбить руки" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("kris_atk7_is_done"):
                text_size 30

    elif attackindex == "Отчаянное комбо":
        # Отчаянное комбо - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Отчаянное комбо" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("kris_atk10_combo_is_done"):
                text_size 30

    elif attackindex == "Рывок защитника (атака)":
        # Рывок защитника - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Рывок защитника" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("kris_atk11_is_done"):
                text_size 30

    # ========================================================================
    # МАГИЯ КРИСА
    # ========================================================================

    elif attackindex == "Призвать меч":
        timer 0.001 action [Hide("Heroattacks"), Jump("kris_mag1_is_done")]
        # Призвать меч
        #vbox:
        #    xalign 0.5
        #    yalign 0.5
        #    spacing 20
        #    text "Призвать меч" size 40 color "#ffffff"
        #    textbutton "Применить магию" action Jump("kris_mag1_is_done"):
        #        text_size 30
    
    elif attackindex == "Призвать щит":
        timer 0.001 action [Hide("Heroattacks"), Jump("kris_mag2_is_done")]
        # Призвать щит
        #vbox:
        #    xalign 0.5
        #    yalign 0.5
        #    spacing 20
        #    text "Призвать щит" size 40 color "#ffffff"
        #    textbutton "Применить магию" action Jump("kris_mag2_is_done"):
        #        text_size 30
    
    elif attackindex == "Напрячься":
        timer 0.001 action Jump ("kris_mag3_is_done")
        # Напрячься
        #vbox:
        #    xalign 0.5
        #    yalign 0.5
        #    spacing 20
        #    text "Напрячься" size 40 color "#ffffff"
        #    textbutton "Применить магию" action Jump("kris_mag3_is_done"):
        #        text_size 30
    
    elif attackindex == "Позвать за щит":
        # Позвать за щит
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Позвать за щит" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag4_is_done"):
                text_size 30
    
    elif attackindex == "Правильный угол":
        # Правильный угол
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Правильный угол" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag5_is_done"):
                text_size 30
    
    elif attackindex == "Слабое место":
        # Слабое место
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Слабое место" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag6_is_done"):
                text_size 30
    
    elif attackindex == "Концентрация":
        # Концентрация
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Концентрация" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag7_is_done"):
                text_size 30
    
    elif attackindex == "Поднять щиты!":
        # Поднять щиты!
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Поднять щиты!" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag8_is_done"):
                text_size 30
    
    elif attackindex == "Стремление вперёд":
        # Стремление вперёд
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Стремление вперёд" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag9_is_done"):
                text_size 30
    
    elif attackindex == "Рывок защитника (магия)":
        # Рывок защитника
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Рывок защитника" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag10_is_done"):
                text_size 30
    
    elif attackindex == "Пробудиться":
        # Пробудиться
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Пробудиться" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("kris_mag11_is_done"):
                text_size 30

    # ========================================================================
    # АТАКИ АЗРИ
    # ========================================================================

    elif attackindex == "Удар принца":
        # Удар принца
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Удар принца" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("asri_atk1_is_done"):
                text_size 30
    
    elif attackindex == "Взмах мечом":
        # Взмах мечом
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Взмах мечом" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("asri_atk2_is_done"):
                text_size 30
    
    elif attackindex == "Щитовой удар":
        # Щитовой удар
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Щитовой удар" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("asri_atk3_is_done"):
                text_size 30
    
    elif attackindex == "Удар лбом":
        # Удар лбом
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Удар лбом" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("asri_atk4_is_done"):
                text_size 30

    # ========================================================================
    # МАГИЯ АЗРИ
    # ========================================================================

    elif attackindex == "Шаг вперёд":
        # Шаг вперёд
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Шаг вперёд" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag1_is_done"):
                text_size 30
    
    elif attackindex == "Магия огня":
        # Магия огня
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Магия огня" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag2_is_done"):
                text_size 30
    
    elif attackindex == "Горное равновесие":
        # Горное равновесие
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Горное равновесие" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag3_is_done"):
                text_size 30
    
    elif attackindex == "Клинки хаоса":
        # Клинки хаоса
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Клинки хаоса" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag4_is_done"):
                text_size 30
    
    elif attackindex == "Сменить облик":
        # Сменить облик — не тратит ход, переключает облик Азриеля
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Сменить облик" size 40 color "#ffffff"
            textbutton "Сменить" action Jump("asri_form_is_done"):
                text_size 30

    elif attackindex == "За спиною принца":
        # За спиною принца
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "За спиною принца" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag5_is_done"):
                text_size 30
    
    elif attackindex == "Уничтожитель хаоса":
        # Уничтожитель хаоса
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Уничтожитель хаоса" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag6_is_done"):
                text_size 30
    
    elif attackindex == "Встать с колен":
        # Встать с колен
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Встать с колен" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag7_is_done"):
                text_size 30
    
    elif attackindex == "Звёздный блеск":
        # Звёздный блеск
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Звёздный блеск" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag8_is_done"):
                text_size 30
    
    elif attackindex == "Боевой клич!":
        # Боевой клич!
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Боевой клич!" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag9_is_done"):
                text_size 30
    
    elif attackindex == "Луч Бога Гиперсмерти":
        # Луч Бога Гиперсмерти
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Луч Бога Гиперсмерти" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("asri_mag10_is_done"):
                text_size 30

    # ========================================================================
    # АТАКИ ЧАРЫ
    # ========================================================================

    elif attackindex == "Удар бунтарки":
        
            # Затемнение фона, как в оригинале
        add Solid("#000000", xysize=(1280, 720)) at kris_fight2_black
        
        # Множитель перформанса (обновляется в реальном времени, как у ножа)
        text "Множитель: [calculate_wheel_perform(wheel_angle)]" xpos 50 ypos 230 size 24 color "#ff0000"


        add Solid("#ffffff", xysize=(700, 30)) at chara_fight1_timer

        # Неподвижное колесо с секторами
        add "chara_wheel_bg.png":
            xalign 0.5
            yalign 0.5

        # Вращающаяся белая палка
        add "chara_wheel_stick.png":
            xalign 0.5
            yalign 0.5
            rotate wheel_angle + 90

        # Центральная кнопка: останавливает колесо и фиксирует результат
        imagebutton:
            idle "chara_wheel_button.png"
            hover "chara_wheel_button_hover.png"
            focus_mask True
            xalign 0.5
            yalign 0.5
            action [
                SetVariable("wheel_is_moving", False),
                SetVariable("kris1_atk_pressed", 1),
                Function(fix_wheel_perform),
                SetVariable("chara_atk1_udar", 1),
                Jump("CharaAtk1_is_done")   # или имя вашего лейбла (CharaAtk1_is_done2)
            ]
            hovered SetVariable("chara_atk1_udar", 1)
            unhovered SetVariable("chara_atk1_udar", 0)

        if store.chara_atk1_udar == 1:
            text "Удар" color "#ffff00" xalign 0.5 yalign 0.5
        else:
            text "Удар" xalign 0.5 yalign 0.5


        # Вращение колеса (аналог Function(update_stick_position))
        timer 0.032 repeat True action Function(update_wheel_position)

        # Таймаут 7 секунд — промах, как в оригинале
        timer 7 action [
            SetVariable("wheel_is_moving", False),
            SetVariable("kris1_atk_pressed", 0),
            Jump("CharaAtk1_is_done")
        ]

        # Удар бунтарки
        #vbox:
        #    xalign 0.5
        #    yalign 0.5
        #    spacing 20
        #    text "Удар бунтарки" size 40 color "#ffffff"
        #    textbutton "Применить атаку" action Jump("CharaAtk1_is_done"):
        #        text_size 30
    
    elif attackindex == "Удар ножом":
        add Solid("#000000", xysize=(1280, 720)) at kris_fight2_black

        add "chara_wheel_bg_2.png":
            xalign 0.5
            yalign 0.5

        if wheel_is_moving:
            add "chara_wheel_stick.png":
                xalign 0.5
                yalign 0.5
                rotate wheel_angle

        # Визуализация счетчика (сколько индикаторов уже пропало)
        text "Использовано: [wheel_disappear_count]/3" xpos 50 ypos 50 size 30 color "#fff"

        # Визуализация накопленного заряда (пульсация при каждом нажатии)
        # Текст заряда с анимацией
        # Передаем knife_press_count как аргумент. При каждом нажатии он растет,
        # и Ren'Py перезапускает анимацию с начала.
        # Текст заряда внизу экрана
        if knife_press_count == 0:
            text "[int(base_perform * 100)]%":
                yalign 0.9 
                xalign 0.5 
                size 40 
                color "#ffffff"
                
        if knife_press_count == 1:
            text "[int(base_perform * 100)]%":
                yalign 0.9 
                xalign 0.5 
                size 40 
                color "#ffffff"
                at perform_pulse1
                
        if knife_press_count == 2:
            text "[int(base_perform * 100)]%":
                yalign 0.9 
                xalign 0.5 
                size 40 
                color "#ffffff"
                at perform_pulse2
                
        if knife_press_count == 3:
            # Для 3-го и всех последующих нажатий
            if base_perform >= 0.99:
                text "100%":
                    yalign 0.9 
                    xalign 0.5 
                    size 40 
                    color "#ffff00"
                    at perform_pulse3
            else:
                text "[int(base_perform * 100)]%":
                    yalign 0.9 
                    xalign 0.5 
                    size 40 
                    color "#ffffff"
                    at perform_pulse3




        # Текст-подсказка текущего множителя
        $ current_mult = get_knife_multiplier(wheel_angle)
        #if current_mult == 1.0:
        #    text "x1.0 (ИДЕАЛЬНО)" xpos 50 ypos 130 size 24 color "#00ff00"
        #elif current_mult == 0.85:
        #    text "x0.85" xpos 50 ypos 130 size 24 color "#ffff00"
        #elif current_mult == 0.75:
        #    text "x0.75" xpos 50 ypos 130 size 24 color "#ffa500"
        #else:
        #    text "x0.5" xpos 50 ypos 130 size 24 color "#ff0000"
        
        text "[base_perform]" xpos 50 ypos 170 size 24 color "#ff0000"
        text "[kris1_atk_pressed]" xpos 50 ypos 200 size 24 color "#ff0000"
        text "[current_mult]" xpos 50 ypos 230 size 24 color "#ff0000"


        imagebutton:
            idle "chara_wheel_button.png"
            hover "chara_wheel_button_hover.png"
            focus_mask True
            xalign 0.5
            yalign 0.5
            sensitive wheel_is_moving
            action [
                Function(knife_button_action_v3),
                SetVariable("chara_atk1_udar", 1),
                # Переход обрабатывается таймером ниже, когда wheel_is_moving == False
            ]
            hovered SetVariable("chara_atk1_udar", 1)
            unhovered SetVariable("chara_atk1_udar", 0)

        if store.chara_atk1_udar == 1:
            text "Удар" color "#ffff00" xalign 0.5 yalign 0.5
        else:
            text "Удар" xalign 0.5 yalign 0.5

        # Таймер вращения и авто-сброса
        timer 0.01 repeat True action Function(update_wheel_knife_v3)

        # ТАЙМЕР ПЕРЕХОДА: если колесо остановилось (wheel_is_moving == False),
        # но переход еще не произошел (например, из-за авто-исчезновения),
        # этот таймер сработает мгновенно и перекинет в лейбл.
        if not wheel_is_moving:
            timer 1.0 action [Jump("CharaAtk1_is_done")]

        # Общий таймаут безопасности (10 секунд)
        #timer 10 action [
        #    SetVariable("wheel_is_moving", False),
        #    SetVariable("kris1_atk_pressed", 0),
        #    Jump("CharaAtk1_is_done")
        #]


        
    elif attackindex == "Удар шпагой":
        # Удар шпагой

        
        
        timer 3.5 action Jump("CharaAtk1_is_done")
    
        timer 0.01 action [ SetVariable("kris1_atk_pressed", 0), MouseMove(92, renpy.random.randint(102, 645),duration=0.3)]

        # Если base_perform >= 1.0, прыгаем в лейбл
        if base_perform >= 1.0:
            timer 0.5 action Jump("CharaAtk1_is_done")
        if chara_atk3_out == 1:
            timer 0.2 action Jump("CharaAtk1_is_done")

        timer 0.5 action SetVariable("chara_atk3_is_ready", 1)

        add Solid(size=(1280,720), color="000000") at alpha0405

        if chara_atk3_is_ready == 1:
            
            

            # Фон (chara3_atk3_bg.png) - лучше рисовать первым, чтобы он был под кнопками
            add "chara3_atk3_bg.png" xalign 0.5 yalign 0.5 alpha 0.3
            
            
            # 10% (0.1)
            if base_perform >= 0.1:
                add "chara3_atk3_10.png" at darker_trans
                add "chara3_atk3_10.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_10.png"
                    hover "chara3_atk3_10.png"
                    hovered SetVariable("base_perform", 0.1)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 20% (0.2)
            if base_perform >= 0.2:
                add "chara3_atk3_20.png" at darker_trans
                add "chara3_atk3_20.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_20.png"
                    hover "chara3_atk3_20.png"
                    hovered [SetVariable("base_perform", 0.2), SetVariable("kris1_atk_pressed", 1)]
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 30% (0.3)
            if base_perform >= 0.3:
                add "chara3_atk3_30.png" at darker_trans
                add "chara3_atk3_30.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_30.png"
                    hover "chara3_atk3_30.png"
                    hovered SetVariable("base_perform", 0.3)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 40% (0.4)
            if base_perform >= 0.4:
                add "chara3_atk3_40.png" at darker_trans
                add "chara3_atk3_40.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_40.png"
                    hover "chara3_atk3_40.png"
                    hovered SetVariable("base_perform", 0.4)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 50% (0.5)
            if base_perform >= 0.5:
                add "chara3_atk3_50.png" at darker_trans
                add "chara3_atk3_50.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_50.png"
                    hover "chara3_atk3_50.png"
                    hovered SetVariable("base_perform", 0.5)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 60% (0.6)
            if base_perform >= 0.6:
                add "chara3_atk3_60.png" at darker_trans
                add "chara3_atk3_60.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_60.png"
                    hover "chara3_atk3_60.png"
                    hovered SetVariable("base_perform", 0.6)
                    action NullAction()
                    xalign 0.5 yalign 0.5
            
            # 70% (0.7)
            if base_perform >= 0.7:
                add "chara3_atk3_70.png" at darker_trans
                add "chara3_atk3_70.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_70.png"
                    hover "chara3_atk3_70.png"
                    hovered SetVariable("base_perform", 0.7)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 80% (0.8)
            if base_perform >= 0.8:
                add "chara3_atk3_80.png" at darker_trans
                add "chara3_atk3_80.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_80.png"
                    hover "chara3_atk3_80.png"
                    hovered SetVariable("base_perform", 0.8)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 85% (0.85)
            if base_perform >= 0.85:
                add "chara3_atk3_85.png" at darker_trans
                add "chara3_atk3_85.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_85.png"
                    hover "chara3_atk3_85.png"
                    hovered SetVariable("base_perform", 0.85)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 90% (0.9)
            if base_perform >= 0.9:
                add "chara3_atk3_90.png" at darker_trans
                add "chara3_atk3_90.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_90.png"
                    hover "chara3_atk3_90.png"
                    hovered SetVariable("base_perform", 0.9)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 95% (0.95)
            if base_perform >= 0.95:
                add "chara3_atk3_95.png" at darker_trans
                add "chara3_atk3_95.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_95.png"
                    hover "chara3_atk3_95.png"
                    hovered SetVariable("base_perform", 0.95)
                    action NullAction()
                    xalign 0.5 yalign 0.5

            # 100% (1.0)
            if base_perform >= 1.0:
                add "chara3_atk3_100.png" at darker_trans
                add "chara3_atk3_100.png" at trans_checked xalign 0.5 yalign 0.5
            else:
                imagebutton:
                    focus_mask True
                    idle "chara3_atk3_100.png"
                    hover "chara3_atk3_100.png"
                    hovered SetVariable("base_perform", 1.0)
                    action NullAction()
                    xalign 0.5 yalign 0.5


            imagebutton:
                focus_mask True
                idle "chara3_atk3_bg.png"
                hover "chara3_atk3_bg.png"
                hovered SetVariable("chara_atk3_out",1)
                action NullAction()
                xalign 0.5
                yalign 0.5
                at alpha0405

            imagebutton:
                focus_mask True
                idle "chara3_atk3_obod.png"
                hover "chara3_atk3_obod.png"
                hovered SetVariable("chara_atk3_out",1)
                action NullAction()
                xalign 0.5
                yalign 0.5

            # Текст с разными трансформациями в зависимости от base_perform
            if base_perform >= 1.0:
                text "[int(base_perform*100)]%" at chara_atk3_prog_100 xalign 0.5 yalign 0.9 color "#FFD700"
            elif base_perform >= 0.95:
                text "[int(base_perform*100)]%" at chara_atk3_prog_95 xalign 0.5 yalign 0.9 color "#FFE44D"
            elif base_perform >= 0.9:
                text "[int(base_perform*100)]%" at chara_atk3_prog_90 xalign 0.5 yalign 0.9 color "#FFE870"
            elif base_perform >= 0.85:
                text "[int(base_perform*100)]%" at chara_atk3_prog_85 xalign 0.5 yalign 0.9 color "#FFEDA3"
            elif base_perform >= 0.8:
                text "[int(base_perform*100)]%" at chara_atk3_prog_80 xalign 0.5 yalign 0.9 color "#FFF0B3"
            elif base_perform >= 0.7:
                text "[int(base_perform*100)]%" at chara_atk3_prog_70 xalign 0.5 yalign 0.9 color "#FFF5CC"
            elif base_perform >= 0.6:
                text "[int(base_perform*100)]%" at chara_atk3_prog_60 xalign 0.5 yalign 0.9 color "#FFF8D9"
            elif base_perform >= 0.5:
                text "[int(base_perform*100)]%" at chara_atk3_prog_50 xalign 0.5 yalign 0.9 color "#FFFBE6"
            elif base_perform >= 0.4:
                text "[int(base_perform*100)]%" at chara_atk3_prog_40 xalign 0.5 yalign 0.9 color "#FFFDF0"
            elif base_perform >= 0.3:
                text "[int(base_perform*100)]%" at chara_atk3_prog_30 xalign 0.5 yalign 0.9 color "#FFFEF5"
            elif base_perform >= 0.2:
                text "[int(base_perform*100)]%" at chara_atk3_prog_20 xalign 0.5 yalign 0.9 color "#FFFFFA"
            elif base_perform >= 0.1:
                text "[int(base_perform*100)]%" at chara_atk3_prog_10 xalign 0.5 yalign 0.9 color "#FFFFFF"
            else:
                text "[int(base_perform*100)]%" xalign 0.5 yalign 0.9 color "#FFFFFF"

            add Solid("ffffff") at chara_atk3_timer
            
            
        #vbox:
        #    xalign 0.5
        #    yalign 0.5
        #    spacing 20
        #    text "Удар шпагой" size 40 color "#ffffff"
        #    textbutton "Применить атаку" action [SetVariable("kris1_atk_pressed", 1), Jump("CharaAtk1_is_done")]:
        #        text_size 30
    
    elif attackindex == "Удар из-за спины":
        # Удар из-за спины
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Удар из-за спины" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("CharaAtk4_is_done"):
                text_size 30
    
    elif attackindex == "Решето":
        # Решето
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Решето" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("CharaAtk5_is_done"):
                text_size 30
    
    elif attackindex == "Ножевой снаряд":
        # Ножевой снаряд
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Ножевой снаряд" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("CharaAtk6_is_done"):
                text_size 30
    
    elif attackindex == "Реки крови":
        # Реки крови
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Реки крови" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("CharaAtk7_is_done"):
                text_size 30

    # ========================================================================
    # МАГИЯ ЧАРЫ
    # ========================================================================

    elif attackindex == "Гнев" or attackindex == "Безумие":
        timer 0.01 action [Jump("chara_mag_is_done_glava_1"), Hide("Heroattacks")]
        # Гнев
        #vbox:
        #    xalign 0.5
        #    yalign 0.5
        #    spacing 20
        #    text "Гнев" size 40 color "#ffffff"
        #    textbutton "Применить магию" action Jump("chara_mag1_is_done"):
        #        text_size 30

    
    elif attackindex == "Сумасшествие":
        # Сумасшествие
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Сумасшествие" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("chara_mag3_is_done"):
                text_size 30
    
    elif attackindex == "Псих":
        # Псих
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Псих" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("chara_mag4_is_done"):
                text_size 30
    
    elif attackindex == "Моральное разложение":
        # Моральное разложение
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Моральное разложение" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("chara_mag5_is_done"):
                text_size 30
    
    elif attackindex == "Пробуждение прошлого":
        # Пробуждение прошлого
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Пробуждение прошлого" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("chara_mag6_is_done"):
                text_size 30

    # ========================================================================
    # АТАКИ ФРИСКА
    # ========================================================================
    elif attackindex == "Para bellum":
        # Si vis pacem, para bellum - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Para bellum" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("frisk_atk1_is_done"):
                text_size 30
    # У Фриска нет атак в текущей реализации

    # ========================================================================
    # МАГИЯ ФРИСКА
    # ========================================================================

    elif attackindex == "Potentia intellectus":
        # Potentia intellectus
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Potentia intellectus" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("frisk_mag1_is_done"):
                text_size 30
    
    elif attackindex == "Quod licet Iovi, non licet bovi":
        # Quod licet Iovi, non licet bovi
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Quod licet Iovi, non licet bovi" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("frisk_mag2_is_done"):
                text_size 30
    
    elif attackindex == "Проект договора":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Проект договора" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("frisk_mag3_is_done"):
                text_size 30

    elif attackindex == "Foedus icere":
        # Foedus icere
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Foedus icere" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("frisk_mag3_is_done"):
                text_size 30
    
    elif attackindex == "Do ut des":
        # Do ut des
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Do ut des" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("frisk_mag4_is_done"):
                text_size 30
    
    elif attackindex == "Вернуть в диалог":
        # Сохранение решимости
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Вернуть в диалог" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("frisk_mag5_is_done"):
                text_size 30

    # ========================================================================
    # МАГИЯ ИЗЗИ
    # ------------------------------------------------------------------------
    # «Таинство вместо мечей» ур.1: Иззи не может атаковать, у неё есть
    # только базовые заклинания. Все ветки ниже — магия.
    # ========================================================================

    elif attackindex == "Осколок себя":
        # Осколок себя — мини-игра «Саймон»: число успешных нажатий
        # усиливает магию и определяет потерянное HP.
        timer 0.1 action Jump("izzymag1_is_done")

    elif attackindex == "Успокоение":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Успокоение" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag2_is_done"):
                text_size 30

    elif attackindex == "Медитация":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Медитация" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag3_is_done"):
                text_size 30

    elif attackindex == "Правильное дыхание":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Правильное дыхание" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag4_is_done"):
                text_size 30

    elif attackindex == "Благовония":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Благовония" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag5_is_done"):
                text_size 30

    elif attackindex == "Открытие пределов":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Открытие пределов" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag6_is_done"):
                text_size 30

    elif attackindex == "Воспрять дух":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Воспрять дух" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag7_is_done"):
                text_size 30

    elif attackindex == "Карма":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Карма" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag8_is_done"):
                text_size 30

    elif attackindex == "Предвиденье":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Предвиденье" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag9_is_done"):
                text_size 30

    elif attackindex == "Зачарование":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Зачарование" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag10_is_done"):
                text_size 30

    elif attackindex == "Усиление присутствия":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Усиление присутствия" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag11_is_done"):
                text_size 30

    elif attackindex == "Духовный лук":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Духовный лук" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag12_is_done"):
                text_size 30

    elif attackindex == "Пробуждение":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Пробуждение" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("izzymag13_is_done"):
                text_size 30

    # ========================================================================
    # АТАКИ КЛОВЕРА
    # ========================================================================

    elif attackindex == "Навскидку":
        # Запускаем первый экран мини-игры
        timer 0.1 action Jump("Cloveratk1_1")
    elif attackindex == "Прицельный":
        # Прицельный - адаптация атаки Криса с движущимися палками
        timer 0.01 action Jump("cloveratk2_perform")

    elif attackindex == "Лассо":
        # Лассо - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Лассо" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("clover_atk3_is_done"):
                text_size 30

    elif attackindex == "Разрушительный хлыст":
        # Разрушительный хлыст - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Разрушительный хлыст" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("clover_atk4_is_done"):
                text_size 30

    elif attackindex == "Клеймо":
        # Клеймо - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Клеймо" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("clover_atk5_is_done"):
                text_size 30

    elif attackindex == "Скорострел":
        # Скорострел - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Скорострел" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("clover_atk6_is_done"):
                text_size 30

    # ========================================================================
    # МАГИЯ КЛОВЕРА
    # ========================================================================

    elif attackindex == "Выбор калибра":
        # Выбор калибра: три типа патронов, у каждого свой урон и обойма.
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Выбор калибра" size 40 color "#ffffff"
            textbutton "Малый (кровотечение)":
                text_size 30
                action [Function(clover_set_caliber, "small"), Jump("clover_mag1_is_done")]
            textbutton "Средний (баланс)":
                text_size 30
                action [Function(clover_set_caliber, "medium"), Jump("clover_mag1_is_done")]
            textbutton "Большой (броня/слабость)":
                text_size 30
                action [Function(clover_set_caliber, "large"), Jump("clover_mag1_is_done")]

    elif attackindex == "Сыграем!":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Сыграем!" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag2_is_done"):
                text_size 30

    elif attackindex == "Помиловать":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Помиловать" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag3_is_done"):
                text_size 30

    elif attackindex == "Вафельный перерыв":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Вафельный перерыв" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag11_is_done"):
                text_size 30

    elif attackindex == "Суд":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Суд" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag4_is_done"):
                text_size 30

    elif attackindex == "Дробовик":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Дробовик" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag5_is_done"):
                text_size 30

    elif attackindex == "Метка разыскиваемого":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Метка разыскиваемого" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag6_is_done"):
                text_size 30

    elif attackindex == "Вызов на дуэль!":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Вызов на дуэль!" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag8_is_done"):
                text_size 30

    elif attackindex == "Длинный ствол":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Длинный ствол" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag9_is_done"):
                text_size 30

    elif attackindex == "От судьбы не уйдёшь":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "От судьбы не уйдёшь" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag10_is_done"):
                text_size 30

    elif attackindex == "Дикий запад, Крошка!":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Дикий запад, Крошка!" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag7_is_done"):
                text_size 30

    elif attackindex == "Гиперлуч":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Гиперлуч (рут GENO)" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("clover_mag12_is_done"):
                text_size 30

    # ========================================================================
    # ========================================================================
    # АТАКИ АРЧИ
    # ========================================================================

    elif attackindex == "Боксёрское комбо":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Боксёрское комбо" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk1_is_done"):
                text_size 30

    elif attackindex == "По полочкам":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "По полочкам" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk2_is_done"):
                text_size 30

    elif attackindex == "Удары богомола":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Удары богомола" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk3_is_done"):
                text_size 30

    elif attackindex == "Удар орла":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Удар орла" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk4_is_done"):
                text_size 30

    elif attackindex == "Апперкот":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Апперкот" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk5_is_done"):
                text_size 30

    elif attackindex == "Ураган":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Ураган" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk6_is_done"):
                text_size 30

    elif attackindex == "Мягкая ладонь":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Мягкая ладонь" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk7_is_done"):
                text_size 30

    elif attackindex == "Oma yi wa mou":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Oma yi wa mou" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("archie_atk8_is_done"):
                text_size 30

    # ========================================================================
    # МАГИЯ АРЧИ
    # ========================================================================

    elif attackindex == "Ладони чакры":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Ладони чакры" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag1_is_done"):
                text_size 30

    elif attackindex == "Очищение Ци":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Очищение Ци" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag2_is_done"):
                text_size 30

    elif attackindex == "Печати ниндзюцу":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Печати ниндзюцу" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag3_is_done"):
                text_size 30

    elif attackindex == "Укрепление мышц":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Укрепление мышц" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag4_is_done"):
                text_size 30

    elif attackindex == "Рывок":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Рывок" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag5_is_done"):
                text_size 30

    elif attackindex == "Режим храбрости":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Режим храбрости" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag6_is_done"):
                text_size 30

    elif attackindex == "Реверс энергии":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Реверс энергии" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag7_is_done"):
                text_size 30

    elif attackindex == "Травмирующие удары":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Травмирующие удары" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag8_is_done"):
                text_size 30

    elif attackindex == "Вернуть отправителю":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Вернуть отправителю" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag9_is_done"):
                text_size 30

    elif attackindex == "Храбрость!":
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Храбрость!" size 40 color "#ffffff"
            textbutton "Применить магию" action Jump("archiemag10_is_done"):
                text_size 30

    # ========================================================================
    # АТАКИ СЕДРИКА
    # ========================================================================
    elif attackindex == "Удар сковородкой":
        # Удар сковородкой - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Удар сковородкой" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("sedric_atk1_is_done"):
                text_size 30

    elif attackindex == "Пощёчина от шефа":
        # Пощёчина от шефа - текстовая кнопка
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Пощёчина от шефа" size 40 color "#ffffff"
            textbutton "Применить атаку" action Jump("sedric_atk2_is_done"):
                text_size 30
    # У Седрика нет атак в текущей реализации

    # ========================================================================
    # МАГИЯ СЕДРИКА (Кулинария)
    # ========================================================================

    elif attackindex == "Сбегать за продуктами":
        # Сбегать за продуктами
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "Сбегать за продуктами" size 40 color "#ffffff"
            textbutton "Приготовить блюдо" action Jump("sedric_mag1_is_done"):
                text_size 30
    elif attackindex in ("Булочка", "Яичница на завтрак", "Яичница с беконом", "Салат Цезарь", "Сэндвич", "Блинчики с кленовым сиропом", "Бургер", "Чизбургер", "Суши", "Мясо на гриле", "Пицца!"):
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            text "[attackindex]" size 40 color "#ffffff"
            textbutton "Приготовить блюдо" action Jump("sedric_cook_action"):
                text_size 30

    # ========================================================================
    # ДВИЖЕНИЯ СИЛЬВИИ (танец)
    # ========================================================================
    # У Сильвии нет обычных атак: её ход — это одно движение танца.
    # Здесь открывается экран выбора движения, ограниченный текущим
    # уровнем прогресса (2 / 4 / 8 / 16 движений).

    elif attackindex in ("Плие", "Томбе"):
        timer 0.01 action Show("sylvia_movement_screen")

    # ЭМИЛИ: отдельный лейбл на каждую кнопку, как в боевом маршруте Криса.
    elif attackindex == "защита_Эмили":
        timer 0.01 action Jump("emily_defend_is_done")
    elif attackindex == "Вперёд, Мистер коготь!":
        timer 0.01 action Jump("emily_attack_1_is_done")
    elif attackindex == "Назад, Мистер Коготь!":
        timer 0.01 action Jump("emily_attack_2_is_done")
    elif attackindex == "Викторина":
        timer 0.01 action Jump("emily_magic_1_is_done")
    elif attackindex == "Гонка чисел":
        timer 0.01 action Jump("emily_magic_2_is_done")
    elif attackindex == "Цифровой щит":
        timer 0.01 action Jump("emily_magic_3_is_done")
    elif attackindex == "Блеснуть безупречностью":
        timer 0.01 action Jump("emily_magic_4_is_done")
    elif attackindex == "Взлом сети":
        timer 0.01 action Jump("emily_magic_5_is_done")
    elif attackindex == "Блокировка":
        timer 0.01 action Jump("emily_magic_6_is_done")
    elif attackindex == "Левый аккаунт":
        timer 0.01 action Jump("emily_magic_7_is_done")
    elif attackindex == "Заморозка репозитория":
        timer 0.01 action Jump("emily_magic_8_is_done")
    elif attackindex == "Трансляция взлома":
        timer 0.01 action Jump("emily_magic_9_is_done")
    elif attackindex == "Маленькая ошибка":
        timer 0.01 action Jump("emily_magic_10_is_done")
    elif attackindex == "Доксиинг":
        timer 0.01 action Jump("emily_magic_11_is_done")
    elif attackindex == "Взлом аккаунта":
        timer 0.01 action Jump("emily_magic_12_is_done")
    elif attackindex == "Блэк аут":
        timer 0.01 action Jump("emily_magic_13_is_done")
    elif attackindex == "Резервная копия":
        timer 0.01 action Jump("emily_magic_14_is_done")
    elif attackindex == "Игра оптики":
        timer 0.01 action Jump("emily_magic_15_is_done")

    # СЬЮЗИ: отдельный лейбл на каждую кнопку.
    elif attackindex == "защита_Сьюзи":
        timer 0.01 action Jump("susie_defend_is_done")
    elif attackindex == "Пинок ногой":
        timer 0.01 action Jump("susie_attack_1_is_done")
    elif attackindex == "Удар Секирой":
        timer 0.01 action Jump("susie_attack_2_is_done")
    elif attackindex == "Всем и сразу!":
        timer 0.01 action Jump("susie_attack_3_is_done")
    elif attackindex == "Хвостовой хлыст":
        timer 0.01 action Jump("susie_attack_4_is_done")
    elif attackindex == "Подручный снаряд":
        timer 0.01 action Jump("susie_attack_5_is_done")
    elif attackindex == "Кусь!":
        timer 0.01 action Jump("susie_attack_6_is_done")
    elif attackindex == "Об землю!":
        timer 0.01 action Jump("susie_attack_7_is_done")
    elif attackindex == "Пурпурный локоть!":
        timer 0.01 action Jump("susie_attack_8_is_done")
    elif attackindex == "Добивочная!":
        timer 0.01 action Jump("susie_attack_9_is_done")
    elif attackindex == "Смести всё!":
        timer 0.01 action Jump("susie_attack_10_is_done")
    elif attackindex == "Пурпурная инфузия":
        timer 0.01 action Jump("susie_magic_1_is_done")
    elif attackindex == "Зазывала":
        timer 0.01 action Jump("susie_magic_2_is_done")
    elif attackindex == "Rude Buster":
        timer 0.01 action Jump("susie_magic_3_is_done")
    elif attackindex == "Зверский рык":
        timer 0.01 action Jump("susie_magic_4_is_done")
    elif attackindex == "Секираранг":
        timer 0.01 action Jump("susie_magic_5_is_done")
    elif attackindex == "Rude fissure":
        timer 0.01 action Jump("susie_magic_6_is_done")

    # ФАБРИ (призыв фамильяров и их магия)
    # ========================================================================
    # У Фабри, как и у Сильвии, нет обычных атак: её ход — это призыв
    # рукодельного друга. Призывы бесплатны, но всё равно идут через
    # общий путь Heroperformsturn -> Jump в лейбл исполнения.
    # Имена ПОБАЙТОВО совпадают с FABRI_SUMMON_MAP и FABRI_MAGIC_TAGS
    # из 1_ПЕРС_ПАССИВКИ_ФАБРИ.rpy и с реестром способностей.

    elif attackindex in ("Призвать М-ра Панцыря",
                         "Призвать М-с Пёрышко",
                         "Призвать М-с Морковку",
                         "Призвать М-с Манки"):
        timer 0.01 action Jump("fabri_summon_is_done")

    # Магия фамильяров. Внутри fabri_perform_familiar_magic нет разбора
    # по индексам: таблица FABRI_MAGIC_TAGS сама знает владельца и тег.
    elif attackindex in ("Спрятаться",
                         "Надеть панцирь",
                         "Прикрепиться",
                         "Рикошет черепахи",
                         "Орлиная зоркость",
                         "Небесные танцы",
                         "Снести яичко",
                         "Перьевой ураган",
                         "Ускориться",
                         "Не поймаешь",
                         "Поделиться морковкой",
                         "Быстрее и дальше",
                         "Боевой рёв",
                         "Неудержимость",
                         "Бей сильнее!",
                         "Я покажу, как бить!"):
        timer 0.01 action Jump("fabri_familiar_magic_is_done")

    # РАЛЬЗЕЙ: отдельный переход для каждой кнопки, как у Криса.
    elif attackindex == "защита_Ральзей":
        timer 0.01 action Jump("ralsei_defend_is_done")
    elif attackindex == "Умиротворение":
        timer 0.01 action Jump("ralsei_magic_1_is_done")
    elif attackindex == "Лозы":
        timer 0.01 action Jump("ralsei_magic_2_is_done")
    elif attackindex == "Молитва исцеления":
        timer 0.01 action Jump("ralsei_magic_3_is_done")
    elif attackindex == "Агрессивный пузырь":
        timer 0.01 action Jump("ralsei_magic_4_is_done")
    elif attackindex == "Пушистый страж":
        timer 0.01 action Jump("ralsei_magic_5_is_done")
    elif attackindex == "Лечение?...":
        timer 0.01 action Jump("ralsei_magic_6_is_done")
    elif attackindex == "Рассеять!":
        timer 0.01 action Jump("ralsei_magic_7_is_done")
    elif attackindex == "Пламенная казнь":
        timer 0.01 action Jump("ralsei_magic_8_is_done")
    elif attackindex == "Перегной":
        timer 0.01 action Jump("ralsei_magic_9_is_done")
    elif attackindex == "Убеждающий вид":
        timer 0.01 action Jump("ralsei_magic_10_is_done")
    elif attackindex == "Приумножить заслуги":
        timer 0.01 action Jump("ralsei_magic_11_is_done")
    elif attackindex == "Унизить слабого":
        timer 0.01 action Jump("ralsei_magic_12_is_done")
    elif attackindex == "Песнь воскрешения":
        timer 0.01 action Jump("ralsei_magic_13_is_done")
    elif attackindex == "Спустить с небес":
        timer 0.01 action Jump("ralsei_magic_14_is_done")
    elif attackindex == "Концентрация зла":
        timer 0.01 action Jump("ralsei_magic_15_is_done")
    elif attackindex == "Тёмный горящий сад":
        timer 0.01 action Jump("ralsei_magic_16_is_done")

    # НОЭЛЛЬ.
    elif attackindex == "защита_Ноэлль":
        timer 0.01 action Jump("noelle_defend_is_done")
    elif attackindex == "Неуверенный взмах":
        timer 0.01 action Jump("noelle_attack_1_is_done")
    elif attackindex == "Ледяная катана":
        timer 0.01 action Jump("noelle_attack_2_is_done")
    elif attackindex == "Снежок":
        timer 0.01 action Jump("noelle_attack_3_is_done")
    elif attackindex == "Молитва исцеления Ноэлль":
        timer 0.01 action Jump("noelle_magic_1_is_done")
    elif attackindex == "Ледяной шок":
        timer 0.01 action Jump("noelle_magic_2_is_done")
    elif attackindex == "Сонный туман":
        timer 0.01 action Jump("noelle_magic_3_is_done")
    elif attackindex == "Морозная завеса":
        timer 0.01 action Jump("noelle_magic_4_is_done")
    elif attackindex == "Ледяная буря":
        timer 0.01 action Jump("noelle_magic_5_is_done")
    elif attackindex == "Оледенение чувств":
        timer 0.01 action Jump("noelle_magic_6_is_done")
    elif attackindex == "Морозная корка":
        timer 0.01 action Jump("noelle_magic_7_is_done")
    elif attackindex == "Ледяной кокон":
        timer 0.01 action Jump("noelle_magic_8_is_done")
    elif attackindex == "Аура холодного сердца":
        timer 0.01 action Jump("noelle_magic_9_is_done")
    elif attackindex == "Терновый сад":
        timer 0.01 action Jump("noelle_magic_10_is_done")
    elif attackindex == "Цветение бед":
        timer 0.01 action Jump("noelle_magic_11_is_done")
    elif attackindex == "Снежная могила":
        timer 0.01 action Jump("noelle_magic_12_is_done")

    # САНС.
    elif attackindex == "защита_Санс":
        timer 0.01 action Jump("sans_defend_is_done")
    elif attackindex == "Удар костью":
        timer 0.01 action Jump("sans_attack_1_is_done")
    elif attackindex == "Преподать урок":
        timer 0.01 action Jump("sans_attack_2_is_done")
    elif attackindex == "Подойди сюда":
        timer 0.01 action Jump("sans_attack_3_is_done")
    elif attackindex == "Стена костей":
        timer 0.01 action Jump("sans_magic_1_is_done")
    elif attackindex == "Костяной дождь":
        timer 0.01 action Jump("sans_magic_2_is_done")
    elif attackindex == "Прижмись":
        timer 0.01 action Jump("sans_magic_3_is_done")
    elif attackindex == "Поспать":
        timer 0.01 action Jump("sans_magic_4_is_done")
    elif attackindex == "Камнем вниз":
        timer 0.01 action Jump("sans_magic_5_is_done")
    elif attackindex == "Костяной щит":
        timer 0.01 action Jump("sans_magic_6_is_done")
    elif attackindex == "Бластер":
        timer 0.01 action Jump("sans_magic_7_is_done")
    elif attackindex == "Пинг-понг":
        timer 0.01 action Jump("sans_magic_8_is_done")
    elif attackindex == "Костяная клетка":
        timer 0.01 action Jump("sans_magic_9_is_done")
    elif attackindex == "Угрызения совести":
        timer 0.01 action Jump("sans_magic_10_is_done")
    elif attackindex == "Кара за грехи":
        timer 0.01 action Jump("sans_magic_11_is_done")
    elif attackindex == "Телекинез!":
        timer 0.01 action Jump("sans_magic_12_is_done")
    elif attackindex == "Финальная атака":
        timer 0.01 action Jump("sans_magic_13_is_done")

    # БЕРДЛИ.
    elif attackindex == "защита_Бердли":
        timer 0.01 action Jump("berdly_defend_is_done")
    elif attackindex == "Клювом!":
        timer 0.01 action Jump("berdly_attack_1_is_done")
    elif attackindex == "Гениальный план":
        timer 0.01 action Jump("berdly_magic_1_is_done")
    elif attackindex == "Электрический клюв":
        timer 0.01 action Jump("berdly_magic_2_is_done")
    elif attackindex == "Вихрь знаний":
        timer 0.01 action Jump("berdly_magic_3_is_done")
















############################
############################       ФУНКЦИИ
############################




init  python:
    import pygame
    import time
    import threading

    class DelayedAction:
        """
        Действие, которое ждет указанное время (секунды),
        а затем выполняет переданную функцию.
        """
        def __init__(self, delay, callback):
            self.delay = delay
            self.callback = callback

        def __call__(self):
            # Запускаем отдельный поток, чтобы не зависла игра во время ожидания
            def run_delayed():
                time.sleep(self.delay)
                # Вызываем функцию в главном потоке Ren'Py, чтобы избежать ошибок
                renpy.invoke_in_main_thread(self.callback)
            
            threading.Thread(target=run_delayed).start()

    def apply_clover_recoil():
        """
        Применяет отдачу для атаки кловера "стрельба навскидку"
        Двигает мышку на 100 пикселей выше в течение 0.3 сек * 10/global_level
        """
        # Получаем текущую позицию мыши
        mx, my = renpy.get_mouse_pos()
        
        # Вычисляем смещение вверх с учетом уровня
        recoil_distance = 100
        recoil_duration = 0.3 * (10 / (max(1, Pers.global_level)*2))
        
        # Новая позиция мыши (выше на recoil_distance пикселей)
        new_y = max(0, my - recoil_distance)  # Убеждаемся, что не выходим за пределы экрана
        
        # Создаем событие mousemove для плавного движения мыши вверх
        pygame.mouse.set_pos(mx, new_y)
        
        # Создаем задержку для возврата мыши в исходное положение
        DelayedAction(recoil_duration, lambda: pygame.mouse.set_pos(mx, my))

    def simulate_click_(x, y):
        """Симулирует клик мыши в указанных координатах"""
        pygame.mouse.set_pos(x, y)
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (x, y)}))
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (x, y)}))

    def perform_single_attack(attacker, target):
        """
        Выполняет одиночную атаку персонажа по врагу.
        Сохраняет результаты для отображения на экране enemies_attacked_visual.
        
        Args:
            attacker: Объект персонажа, который атакует
            target: Объект врага, который получает урон
        """
        # Рассчитываем урон
        damage = attacker.calculate_dmg(target)
        
        # Применяем урон к врагу
        target.current_hp = max(0, target.current_hp - damage)
        
        # Сохраняем информацию для отображения
        store.last_attacked_enemy = target
        store.last_enemy_damage_dealt = damage
        
        # Обновляем информацию о дебафах врага (если будет реализовано)
        if hasattr(store, 'enemies_debuff_info'):
            store.enemies_debuff_info = {}
        
        return damage
    
    def perform_multiple_attacks(attacker, targets):
        """
        Выполняет множественную атаку персонажа по нескольким врагам.
        
        Args:
            attacker: Объект персонажа, который атакует
            targets: Список объектов врагов
        """
        results = {}
        for target in targets:
            if target.current_hp > 0:
                damage = attacker.calculate_dmg(target)
                target.current_hp = max(0, target.current_hp - damage)
                results[target.name] = damage
        
        return results
    
    def apply_damage_to_all_characters(damage_percentage=0.1): # урон по всем
        """ 
        Наносит урон всем персонажам в указанном проценте от их максимального HP.
        По умолчанию 10% (0.1).
        
        Args:
            damage_percentage (float): Процент урона от максимального HP (0.0-1.0)
        
        Returns:
            dict: Словарь с информацией о нанесенном уроне {имя_персонажа: урон}
        """
        results = {}
        
        # Проверяем, что team_manager инициализирован
        if not hasattr(store, 'team_manager') or store.team_manager is None:
            store.ensure_team_manager()
        
        # Получаем список всех персонажей в команде
        for slot in store.team_manager.team_slots:
            if slot and slot in store.characters:
                char = store.pers_dict[slot]
                
                # Рассчитываем урон как указанный процент от максимального HP
                damage = int(char.max_hp * damage_percentage)
                
                # Применяем урон, но не убиваем персонажа (оставляем минимум 1 HP)
                if char.current_hp > 0:  # Наносим урон только живым персонажам
                    actual_damage = min(damage, char.current_hp - 1) if char.current_hp > 1 else 0
                    char.current_hp = max(1, char.current_hp - actual_damage)
                    

                    # Устанавливаем переменные для визуализации урона
                    char.damage_gain_for_vis = actual_damage
                    char.got_crit_for_visual = 0  # Не критический урон
                    store.clear_swoon_pending_for_visual(char)
        
        return results

    # ------------------------------------------------------------------
    # Дебаффы врагов.
    # Раньше эти функции складывали значения в словарь enemy_debuffs,
    # который никто не читал, поэтому эффекты не работали вообще. Теперь
    # каждая функция меняет ту характеристику врага, которая входит в
    # формулы урона/защиты, — то есть работает напрямую.
    # ------------------------------------------------------------------
    enemy_debuffs = {}  # оставлено для совместимости (используется ключ 'daze')

    def apply_enemy_bleeding(enemy, duration=2):
        """Кровотечение: enemy.bloodshed_debuff.

        Входит в расчёт конца раунда: 5% от max HP за каждый стак,
        затем счётчик уменьшается на 1.
        """
        if enemy is None:
            return 0
        enemy.bloodshed_debuff = getattr(enemy, "bloodshed_debuff", 0) + int(duration)
        return enemy.bloodshed_debuff

    def apply_enemy_stun(enemy, duration=1):
        """Оглушение: враг сбит с ног (prone_debuff), пока стаки не выгорят.

        prone_debuff — тот же канал, что и «повалить» у игрока. Стаки
        снимаются системой дебафов по одному за раунд.
        """
        if enemy is None:
            return 0
        enemy.debuff("prone", int(duration))
        return getattr(enemy, "prone_debuff", 0)

    def apply_enemy_weaken_armor(enemy, amount=0.2):
        """Ослабление брони: бонусная защита врага падает на amount.

        Входит в armor как (base_def * bonus_def), то есть -0.2 = -20%
        базовой защиты врага.
        """
        if enemy is None:
            return 0.0
        enemy.bonus_def = max(0.0, float(getattr(enemy, "bonus_def", 0.0)) - float(amount))
        return enemy.bonus_def

    def apply_enemy_weaken_attack(enemy, amount=0.3):
        """Ослабление атаки: бонусная атака врага падает на amount.

        Входит в atk как (base_atk * bonus_atk), то есть -0.3 = -30%
        базовой атаки врага.
        """
        if enemy is None:
            return 0.0
        enemy.bonus_atk = max(0.0, float(getattr(enemy, "bonus_atk", 0.0)) - float(amount))
        return enemy.bonus_atk

    def apply_enemy_atk_debuff(enemy, stacks=1):
        """Истощение: -5% атаки за стак, стаки гаснут по одному за раунд.

        У врага счётчик atk_debuff сам в формулу не входит, поэтому вместе с
        ним опускаем atk_debuff_var — система дебафов вернёт его по 0.05 за
        стак в начале раунда.
        """
        if enemy is None:
            return 0
        applied = enemy.debuff("atk", int(stacks))
        enemy.atk_debuff_var = max(0.0, float(getattr(enemy, "atk_debuff_var", 1.0)) - 0.05 * applied)
        return applied

    











############################
############################                                                ТРАНСФОРМЫ
############################


transform heroes_attacked_visual_trans:
    on show:
        #xoffset 0 yoffset 0  alpha 0.0 
        #easein 0.5 xoffset 30 alpha 1.0 
        xpos 0 alpha 0.0
        easein 0.5 xpos 30 alpha 1.0 
    on hide:
        #xoffset 30 yoffset 0 alpha 1.0 
        #easeout 0.5 xoffset 60 alpha 0.0
        xpos 30 alpha 1.0 
        easeout 0.5 xpos 60 alpha 0.0



transform heroes_attacked_visual_trans_enemy:
    on show:
        xoffset 860 yoffset 190 alpha 0.0 
        easein 1.0 xoffset 890 alpha 1.0 
    on hide:
        xoffset 890 yoffset 190 alpha 1.0
        easeout 0.7 xoffset 930 alpha 0.0


#                                                                           АТАКА КРИСА 1

default scalespeed = 0

default kris1_atk_pressed = 0

transform attack_scale:
    on show:
        xalign 0.5 ypos -500 ysize 0
        easein 0.7 xalign 0.5 yalign 0.5 ysize 242
    on hide:
        alpha 1 yoffset 0 ysize 242
        easein 0.5 alpha 0 yoffset 50 ysize 0

    


transform attack_bg_Kris1:
    on show:
        xzoom 0.0 xpos 30 ypos -20    
        easein 0.5 xpos 30 ypos 190 xzoom 1.0
        #easein 0.3 xzoom 1.0
    on hide:
        xpos 30 ypos 190 xzoom 1.0
        easein 0.5 xzoom 0.0 xpos 30 ypos -20 

transform kris_atk1_buttom:
    on show:
        xzoom 0.0 xpos 600 ypos -20
        easein 0.5 xzoom 1.0 xpos 600 ypos 340    
    on hide: 
        xzoom 1.0 xpos 600 ypos 340
        easein 0.5 xzoom 0.0 xpos 600 ypos -20 

transform vpunch_for_stick:

    xpos stick_xpos ypos 360
    linear 0.02 yoffset 30
    linear 0.02 yoffset -30
    linear 0.02 yoffset 25
    linear 0.02 yoffset -25
    linear 0.03 yoffset 20
    linear 0.03 yoffset -20
    linear 0.03 yoffset 15
    linear 0.03 yoffset -15
    linear 0.06 yoffset 10
    linear 0.06 yoffset -10
    linear 0.06 yoffset 5
    linear 0.06 yoffset -5
    linear 0.06 yoffset 0

transform crit_vpunch(old_widget=None, new_widget=None):
    linear 0.02 yoffset 30
    linear 0.02 yoffset -30
    linear 0.02 yoffset 25
    linear 0.02 yoffset -25
    linear 0.03 yoffset 20
    linear 0.03 yoffset -20
    linear 0.03 yoffset 15
    linear 0.03 yoffset -15
    linear 0.06 yoffset 10
    linear 0.06 yoffset -10
    linear 0.06 yoffset 5
    linear 0.06 yoffset -5
    linear 0.06 yoffset 0


transform  kris_atk1_indic_hide:
    xpos stick_xpos - 20
    yalign 0.5
    on show:
        ysize 0 
        easein 0.5 ysize 242
    on hide:
        alpha 1 yoffset 0 ysize 242
        easein 0.5 alpha 0 yoffset 50 ysize 0



transform  kris_atk1_indic_hide2:
    on show:
        ysize 0 
        easein 0.5 ysize 45
    on hide:
        alpha 1 yoffset 0 ysize 45
        easein 0.5 alpha 0 yoffset 50 ysize 0




















