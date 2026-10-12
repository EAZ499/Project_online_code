


default animestart = 0


style damagetext2:
    outlines [ (2, "#000000", 0, 0) ]  # Чёрная обводка 2px


#лейбл для вызова экрана
label choose_attacker_screen_label:
    call screen choose_attacker_screen() #xalign 0.5
    #pause 3.0
    #call nolabel

#
default characterspicked = 1
define max_characterspicked = 4
default diedchars = 0
default characterstoturn = characterspicked



#трансформы для кнопок


default zoom_for_choose = 1.0

#transform just_zoom_choose:
    

transform dynammic_alpha:

    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (1.0, 0.0, 0.0, 1.0)   # Красный снизу

    on idle:
        xysize (270,55)
        xalign 0.5
        zoom 1.05
        alpha 0.0
    on hover:
        xysize (270,55)
        xalign 0.5
        alpha 0.0 zoom 1.05 yoffset -4
        easein 0.5 alpha 0.7
        alpha 1.0 zoom 1.05 xalign 0.5 yoffset -4 
    
        pause 0.05
        alpha 0.0 
        pause 0.05
        alpha 0.3
        pause 0.05
        alpha 0.0





transform dynammic_alpha_gray:

    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.4, 0.4, 0.4, 1.0)   # Серый снизу

    on idle:
        xysize (270,57)
        xalign 0.5
        zoom 1.05
        alpha 0.0
    on hover:
        xysize (270,57)
        xalign 0.5
        alpha 0.0 zoom 1.05 yoffset -4
        easein 0.5 alpha 0.7
        alpha 1.0 zoom 1.05 xalign 0.5 yoffset -4 
    
        pause 0.05
        alpha 0.0 
        pause 0.05
        alpha 0.3
        pause 0.05
        alpha 0.0

















transform alpha_mig:
    alpha 1.0 zoom 1.05 xalign 0.5 yoffset -4 
    pause 0.05
    alpha 0.0 
    pause 0.05
    alpha 0.3
    pause 0.05
    alpha 0.0



transform monstertochoose:
    on show:
        ypos 720 alpha 0.0
        easein 0.5 ypos 0 alpha 1
    on hide:
        easein 0.5 ypos 720
    on hover:
        easein 0.3 zoom 1.2
    on idle:
        easeout 0.2 zoom 1.05


transform choosedynamic:
    xsize 270
    ysize 605
    on show:
        ypos 0 alpha 0
        easein 0.5 ypos 720 alpha 1.0
    on hide:
        ypos 720 alpha 1
        easein 0.5 ypos 0 alpha 0.0
    on hover:
        easein 0.3 zoom 1.15
    on idle:
        easeout 0.2 zoom 1.05

transform choosestatic:
    xsize 270
    ysize 605
    zoom 1.05 matrixcolor SaturationMatrix(0.0)*BrightnessMatrix(-0.1)

transform herotochoose:
    on show:
        ypos 0 alpha 0
        easein 0.5 ypos 720 alpha 1.0
    on hide:
        ypos 720 alpha 1
        easein 0.5 ypos 0 alpha 0.0
    on hover:
        easein 0.3 zoom 1.15
    on idle:
        easeout 0.2 zoom 1.05


transform alpha0:
    alpha 0.0

# Возможный щит - теперь используется из класса персонажа
# default shield = 4  # Закомментировано, так как shield теперь берется из класса






####

# Потом добавить разные спрайты для разных варов



#image longchooseKris = ConditionSwitch(
#    "spritestyle == 'above' and kris_turn == False", "krisabovenotturn.png",
#    "spritestyle == 'above' and kris_turn == True",  "krisaboveturn.png",
#    "spritestyle == 'under' and kris_turn == False", "krisundernotturn.png",
#    "spritestyle == 'under' and kris_turn == True",  "krisunderturn.png",
#)

transform finishturntrans:
    on show:
        xpos -720 ypos 600
        pause 0.1
        easein 0.3 xpos 40
    on hide:
        xpos 40 ypos 600
        pause 0.1
        easein 0.3 xpos 720

image finishturnforreal = Animation("finishbel.png", 0.3, "finishzh.png", 0.3)

# Transform для экрана выбора персонажа
transform choose_attacker_transform:
    on show:
        xalign 0.5 yalign -2.5
        easein 0.5 xalign 0.5 yalign 0.0
    on hide:
        xalign 0.5 yalign 0.0
        easein 0.5 xalign 0.5 yalign -2.5


transform choose_attacker_transform2:
    on show:
        xalign 0.5 yalign 0.0



#transform Kris_state_dependent_dynamic:
#    # читаем store.my_state
#    if Krisdynamic_var == "idle":
#        zoom 1.0
#    elif Krismy_state == "hovered":
#        zoom 1.0
#        easein 0.3 zoom 1.2
#    else:
#        zoom 1.2
#        easeout 0.3 zoom 1.0

transform choose_attacker_screen_dynamic:
    on show:
        xalign 0.5 ypos -720 alpha 0.0
        easein 0.5 ypos 5 alpha 1.0
    on hide:
        xalign 0.5 ypos 5 alpha 1.0
        easeout 0.5 ypos 720 alpha 0.0


# Экран выбора персонажа для атаки
default choose_attacker_active = 0

screen choose_attacker_screen():

    on "show" action [
        SetVariable("choose_attacker_active", 1),
        SetVariable("target", None),
        SetVariable("attackindex", None),
        Function(reset_soul_state),
        SetVariable("defaultmouse","default2")
        #SetVariable("default_mouse", "default"),
    ]

    on "hide" action SetVariable("choose_attacker_active", 0)

    #timer 0.001 action SetVariable("defaultmouse","default2")
    vbox:
        at alphatransformforbg
        imagebutton:
            idle "semiblackbg3.png"
            hover "semiblackbg3.png"
            action NullAction()
    $ show_enemy_status = 0
    # Сбрасываем флаг нажатия кнопки при каждом показе экрана

        # Проверяем, есть ли хотя бы один доступный персонаж для выбора
    $ available_chars = 0
    # Проверяем доступных персонажей с учетом состояния prone_debuff
    $ available_chars += 1 if (store.pers_dict["Крис"].picked == 1 and store.pers_dict["Крис"].current_hp > 0 and store.pers_dict["Крис"].turn == 1 and store.pers_dict["Крис"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Азриель"].picked == 1 and store.pers_dict["Азриель"].current_hp > 0 and store.pers_dict["Азриель"].turn == 1 and store.pers_dict["Азриель"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Чара"].picked == 1 and store.pers_dict["Чара"].current_hp > 0 and store.pers_dict["Чара"].turn == 1 and store.pers_dict["Чара"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Фриск"].picked == 1 and store.pers_dict["Фриск"].current_hp > 0 and store.pers_dict["Фриск"].turn == 1 and store.pers_dict["Фриск"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Седрик"].picked == 1 and store.pers_dict["Седрик"].current_hp > 0 and store.pers_dict["Седрик"].turn == 1 and store.pers_dict["Седрик"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Кловер"].picked == 1 and store.pers_dict["Кловер"].current_hp > 0 and store.pers_dict["Кловер"].turn == 1 and store.pers_dict["Кловер"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Иззи"].picked == 1 and store.pers_dict["Иззи"].current_hp > 0 and store.pers_dict["Иззи"].turn == 1 and store.pers_dict["Иззи"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Арчи"].picked == 1 and store.pers_dict["Арчи"].current_hp > 0 and store.pers_dict["Арчи"].turn == 1 and store.pers_dict["Арчи"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Сильвия"].picked == 1 and store.pers_dict["Сильвия"].current_hp > 0 and store.pers_dict["Сильвия"].turn == 1 and store.pers_dict["Сильвия"].prone_debuff == 0) else 0
    # Фабри: без этой строки ход Фабри никогда не считался бы доступным,
    # и боевая система не открыла бы выбор героя для неё.
    $ available_chars += 1 if (store.pers_dict["Фабри"].picked == 1 and store.pers_dict["Фабри"].current_hp > 0 and store.pers_dict["Фабри"].turn == 1 and store.pers_dict["Фабри"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict.get("Эмили") is not None and store.pers_dict["Эмили"].picked == 1 and store.pers_dict["Эмили"].current_hp > 0 and store.pers_dict["Эмили"].turn == 1 and store.pers_dict["Эмили"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict.get("Сьюзи") is not None and store.pers_dict["Сьюзи"].picked == 1 and store.pers_dict["Сьюзи"].current_hp > 0 and store.pers_dict["Сьюзи"].turn == 1 and store.pers_dict["Сьюзи"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict.get("Ральзей") is not None and store.pers_dict["Ральзей"].picked == 1 and store.pers_dict["Ральзей"].current_hp > 0 and store.pers_dict["Ральзей"].turn == 1 and store.pers_dict["Ральзей"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict.get("Ноэлль") is not None and store.pers_dict["Ноэлль"].picked == 1 and store.pers_dict["Ноэлль"].current_hp > 0 and store.pers_dict["Ноэлль"].turn == 1 and store.pers_dict["Ноэлль"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict.get("Санс") is not None and store.pers_dict["Санс"].picked == 1 and store.pers_dict["Санс"].current_hp > 0 and store.pers_dict["Санс"].turn == 1 and store.pers_dict["Санс"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict.get("Бердли") is not None and store.pers_dict["Бердли"].picked == 1 and store.pers_dict["Бердли"].current_hp > 0 and store.pers_dict["Бердли"].turn == 1 and store.pers_dict["Бердли"].prone_debuff == 0) else 0
    

    timer 0.01 action SetVariable("timer_to_hide_chars", 3)

    zorder 4
    hbox:
        at choose_attacker_screen_dynamic


        spacing 20
        #at choose_attacker_transform2
        xalign 0.5

        #if get_character_picked_for_shift() == 4:
        #    xoffset 455
        #elif get_character_picked_for_shift() == 3:
            #$extra_offset_when_kris_is_not_alone = -320
        #    xoffset 150
        #elif get_character_picked_for_shift() == 2:
        #    xoffset 300  #character_picked_for_shift
        #else:
        #    xoffset 450  #character_picked_for_shift
            #$ total_offset = -320 - 3







        #                                    @@                                                                                                                                                      
        #                    @@@      @@@@   @@@@@@@@@@@    @@@@       @@@@       @@@@@@@@@@                                                                                                                                                  
        #                    @@@     @@@@    @@@@   @@@@@   @@@@      @@@@@     @@@@@    @@@@                                                                                                                                                 
        #                    @@@    @@@@     @@@@     @@@   @@@@     @@@@@@    @@@@                                                                                                                                                           
        #                    @@@   @@@@      @@@@     @@@   @@@@    @@@@@@@   @@@@                                                                                                                                                            
        #                    @@@@@@@@@       @@@@   @@@@@   @@@@  @@@@  @@@   @@@@                                                                                                                                                            
        #                    @@@@@@@@@@      @@@@@@@@@@@    @@@@ @@@@   @@@   @@@@                                                                                                                                                            
        #                    @@@    @@@@     @@@@@@@@       @@@@@@@@    @@@   @@@@                                                                                                                                                            
        #                    @@@     @@@@    @@@@           @@@@@@@     @@@    @@@@                                                                                                                                                           
        #                    @@@      @@@@   @@@@           @@@@@       @@@     @@@@@    @@@@                                                                                                                                                 
        #                    @@@       @@@   @@@@           @@@@        @@@      @@@@@@@@@@@@                                                                                                                                                 
        #                                                                            @@@                                                                                                                                                      
                                                                                                                                                                                                








        if store.pers_dict["Крис"].picked == 1:
            hbox: # каждого отдельного персонажа
                spacing 0
                
                at herotochoose
                
                $ yoffset_for_Kris_desc=0
            
                vbox:   
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Криса
                        vbox:
                            if store.pers_dict["Крис"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Крис"].bloodshed_debuff != 0 or store.pers_dict["Крис"].prone_debuff != 0 or
                                        store.pers_dict["Крис"].atk != (store.pers_dict["Крис"].base_atk + store.pers_dict["Крис"].base_atk_mod) or
                                        store.pers_dict["Крис"].defense != (store.pers_dict["Крис"].base_def + store.pers_dict["Крис"].base_def_mod) or
                                        store.pers_dict["Крис"].bonus_tank != 0 or
                                        store.pers_dict["Крис"].dmgchance != (store.pers_dict["Крис"].base_dmgchance + store.pers_dict["Крис"].dmgchance_mod) or
                                        store.pers_dict["Крис"].critrate != (store.pers_dict["Крис"].base_critrate + store.pers_dict["Крис"].critrate_mod) or
                                        store.pers_dict["Крис"].crit != (store.pers_dict["Крис"].base_crit + store.pers_dict["Крис"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Kris_desc= -50

                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                    if store.pers_dict["Крис"].prone_debuff != 0: 
                                        imagebutton:
                                            idle "longchooseKris.png"
                                            hover "longchooseKris.png"
                                                                                        
                                                                                        
                                            #unhovered SetVariable("Zoomforvis", 1)
                                            #hovered   SetVariable("Zoomforvis", 1.2 )
                                            action NullAction()
                                            at choosestatic

                                    elif store.pers_dict["Крис"].current_hp > 0 and store.pers_dict["Крис"].turn == 1:

                                        imagebutton:
                                            idle "longchooseKris.png"
                                            hover "longchooseKris.png"
                                            action [SetVariable("current_attacker", 1), Function(lambda: setattr(store.pers_dict['Крис'], 'step_forward', 1)), Jump("Kris_check_control")]
                                            at choosedynamic
                                    else:
                                        imagebutton:
                                            idle "longchooseKris.png"
                                            hover "longchooseKris.png"
                                            #unhovered SetVariable("Zoomforvis", 1)
                                            #hovered   SetVariable("Zoomforvis", 1.2 )
                                            action NullAction()
                                            at choosestatic

                    if store.pers_dict["Крис"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:
                        xalign 0.5 yalign -1.0
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Крис"].shield == 0:
                            frame:
                                padding (0,0)
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Крис"].shield >= 1:
                            frame:
                                xoffset -90 
                                xmargin 0
                                ymargin 0
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Крис"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Крис"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray


                        # Отображение HP для Криса
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3

                            if store.pers_dict['Крис'].current_hp <= store.pers_dict['Крис'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Крис'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Крис'].current_hp > store.pers_dict['Крис'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Крис'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Крис'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray


                            # Полоска HP
                            fixed:
                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Крис"].current_hp > store.pers_dict["Крис"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Крис"].current_hp > store.pers_dict["Крис"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Крис"].current_hp - store.pers_dict["Крис"].max_hp) / store.pers_dict["Крис"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Крис"].current_hp > 0 and store.pers_dict["Крис"].current_hp <= store.pers_dict["Крис"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Крис"].current_hp / store.pers_dict["Крис"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Крис"].current_hp / store.pers_dict["Крис"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Криса
                        hbox:
                            yalign 0.0
                            xalign 0.5
                            spacing 5
                            xoffset -60 #yoffset -40

                            if store.pers_dict['Крис'].current_mp <=  store.pers_dict['Крис'].max_mp* 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Крис'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                            elif store.pers_dict['Крис'].current_mp > store.pers_dict['Крис'].max_mp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Крис'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Крис'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            fixed:
                                xysize (60, 8) xalign 1.0
                                fixed:
                                    # Фон MP
                                    hbox:
                                        spacing 3
                                        if store.pers_dict["Крис"].current_mp > store.pers_dict["Крис"].max_mp:
                                            # Если HP больше максимума, используем зеленый градиент
                                            for i in range(10):
                                                add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

                                        else:
                                            # Если MP меньше или равно максимуму, используем черный градиент
                                            for i in range(10):
                                                add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения MP
                                    if store.pers_dict["Крис"].current_mp > store.pers_dict["Крис"].max_mp:
                                        $ mp_overmana_percent = (store.pers_dict["Крис"].current_mp - store.pers_dict["Крис"].max_mp) / store.pers_dict["Крис"].max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок

                                        # Если MP больше максимума, отображаем 10 иконок mpactive.png
                                        #for i in range(10):
                                        #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

                                    elif store.pers_dict["Крис"].current_mp > 0 and store.pers_dict["Крис"].current_mp <= store.pers_dict["Крис"].max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(store.pers_dict["Крис"])
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(store.pers_dict["Крис"])
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray


                        if (store.pers_dict["Крис"].bloodshed_debuff != 0 or store.pers_dict["Крис"].prone_debuff != 0 or
                            store.pers_dict["Крис"].atk != (store.pers_dict["Крис"].base_atk + store.pers_dict["Крис"].base_atk_mod) or
                            store.pers_dict["Крис"].defense != (store.pers_dict["Крис"].base_def + store.pers_dict["Крис"].base_def_mod) or
                            store.pers_dict["Крис"].bonus_tank != 0 or
                            store.pers_dict["Крис"].dmgchance != (store.pers_dict["Крис"].base_dmgchance + store.pers_dict["Крис"].dmgchance_mod) or
                            store.pers_dict["Крис"].critrate != (store.pers_dict["Крис"].base_critrate + store.pers_dict["Крис"].critrate_mod) or
                            store.pers_dict["Крис"].crit != (store.pers_dict["Крис"].base_crit + store.pers_dict["Крис"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Криса
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Крис"].bloodshed_debuff != 0:
                                    if store.pers_dict["Крис"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Крис"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Крис"].prone_debuff != 0:
                                    if store.pers_dict["Крис"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Крис"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Крис"].atk != (store.pers_dict["Крис"].base_atk + store.pers_dict["Крис"].base_atk_mod):
                                    if store.pers_dict["Крис"].atk > (store.pers_dict["Крис"].base_atk + store.pers_dict["Крис"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].atk < (store.pers_dict["Крис"].base_atk + store.pers_dict["Крис"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Крис"].defense != (store.pers_dict["Крис"].base_def + store.pers_dict["Крис"].base_def_mod):
                                    if store.pers_dict["Крис"].defense > (store.pers_dict["Крис"].base_def + store.pers_dict["Крис"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].defense < (store.pers_dict["Крис"].base_def + store.pers_dict["Крис"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Крис"].bonus_tank != 0:
                                    if store.pers_dict["Крис"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                



                                #if store.pers_dict["Крис"].magic != (store.pers_dict["Крис"].base_magic + store.pers_dict["Крис"].base_magic_mod):
                                #    if store.pers_dict["Крис"].magic > (store.pers_dict["Крис"].base_magic + store.pers_dict["Крис"].base_magic_mod):
                                #        add "mag_green_icon.png" size (40, 40) at damage_gradient_green
                                #    elif store.pers_dict["Крис"].magic < (store.pers_dict["Крис"].base_magic + store.pers_dict["Крис"].base_magic_mod):
                                #        add "mag_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Крис"].dmgchance != (store.pers_dict["Крис"].base_dmgchance + store.pers_dict["Крис"].dmgchance_mod):
                                    if store.pers_dict["Крис"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].dmgchance > (store.pers_dict["Крис"].base_dmgchance + store.pers_dict["Крис"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].dmgchance < (store.pers_dict["Крис"].base_dmgchance + store.pers_dict["Крис"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Крис"].critrate != (store.pers_dict["Крис"].base_critrate + store.pers_dict["Крис"].critrate_mod):
                                    if store.pers_dict["Крис"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].critrate > (store.pers_dict["Крис"].base_critrate + store.pers_dict["Крис"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].critrate < (store.pers_dict["Крис"].base_critrate + store.pers_dict["Крис"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Крис"].crit != (store.pers_dict["Крис"].base_crit + store.pers_dict["Крис"].crit_mod):
                                    if store.pers_dict["Крис"].crit > (store.pers_dict["Крис"].base_crit + store.pers_dict["Крис"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Крис"].crit < (store.pers_dict["Крис"].base_crit + store.pers_dict["Крис"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Крис'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Крис'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic


                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Kris_desc
                                    at dynammic_alpha
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Крис"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0),Hide("fullstats1"), Hide("fullstats0")] #,SetVariable("chardespos", 0)]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Крис"]), SetVariable("sscreenstate_style", "статический"),  SetVariable("chardespos", "Криснажат")]#, #Show ("fullstats1")]
                            

                            elif chardespos == "Криснажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Kris_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()
                            
                        






#                        @@@          @@@@@@       @@@@@@@       @@@         @@                                                                                                                                                                                                                                                                                      
#                       @@@@@       @@@@@@@@@@    @@@@@@@@@@@    @@@       @@@@                                                                                                                                                                                                                                                                                      
#                      @@@@@@@      @@     @@@@   @@@@   @@@@@   @@@      @@@@@                                                                                                                                                                                                                                                                                      
#                     @@@@@@@@             @@@@   @@@@     @@@   @@@     @@@@@@                                                                                                                                                                                                                                                                                      
#                     @@@  @@@@           @@@@    @@@@    @@@@   @@@   @@@@ @@@                                                                                                                                                                                                                                                                                      
#                    @@@@   @@@@    @@@@@@@@@     @@@@@@@@@@@    @@@  @@@@  @@@                                                                                                                                                                                                                                                                                      
#                    @@@    @@@@          @@@@@   @@@@@@@@@@     @@@ @@@@   @@@                                                                                                                                                                                                                                                                                      
#                   @@@@@@@@@@@@@           @@@@  @@@@           @@@@@@@    @@@                                                                                                                                                                                                                                                                                      
#                  @@@@       @@@@         @@@@@  @@@@           @@@@@      @@@                                                                                                                                                                                                                                                                                      
#                 @@@@         @@@ @@@@@@@@@@@@   @@@@           @@@@       @@@                                                                                                                                                                                                                                                                                      
#                 @@@@         @@@@ @@@@@@@@@     @@@@           @@@        @@@                                                                                                                                                                                                                                                                                      
                                                                                


        if store.pers_dict["Азриель"].picked ==1:
            hbox: # каждого отдельного персонажа
                spacing 0
                
                at monstertochoose
                
                $ yoffset_for_Azriel_desc=0

            
                vbox:
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Азриельа
                        vbox:
                            if store.pers_dict["Азриель"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Азриель"].bloodshed_debuff != 0 or store.pers_dict["Азриель"].prone_debuff != 0 or
                                        store.pers_dict["Азриель"].atk != (store.pers_dict["Азриель"].base_atk + store.pers_dict["Азриель"].base_atk_mod) or
                                        store.pers_dict["Азриель"].defense != (store.pers_dict["Азриель"].base_def + store.pers_dict["Азриель"].base_def_mod) or
                                        store.pers_dict["Азриель"].bonus_tank != 0 or
                                        store.pers_dict["Азриель"].magic != (store.pers_dict["Азриель"].base_magic + store.pers_dict["Азриель"].base_magic_mod) or
                                        store.pers_dict["Азриель"].dmgchance != (store.pers_dict["Азриель"].base_dmgchance + store.pers_dict["Азриель"].dmgchance_mod) or
                                        store.pers_dict["Азриель"].critrate != (store.pers_dict["Азриель"].base_critrate + store.pers_dict["Азриель"].critrate_mod) or
                                        store.pers_dict["Азриель"].crit != (store.pers_dict["Азриель"].base_crit + store.pers_dict["Азриель"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Azriel_desc= -50

                                        if store.pers_dict["Азриель"].current_hp > 0 and store.pers_dict["Азриель"].turn == 1 and store.pers_dict["Азриель"].prone_debuff == 0:

                                            imagebutton:

                                                idle "longchooseAsriel.png"
                                                hover "longchooseAsriel.png"
                                                                                                
                                                action [SetVariable("current_attacker", 2), Function(lambda: setattr(store.pers_dict['Азриель'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseAsriel.png"
                                                hover "longchooseAsriel.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic
                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                        if store.pers_dict["Азриель"].current_hp > 0 and store.pers_dict["Азриель"].turn == 1 and store.pers_dict["Азриель"].prone_debuff == 0:

                                            imagebutton:
                                                idle "longchooseAsriel.png"
                                                hover "longchooseAsriel.png"
                                                action [SetVariable("current_attacker", 2), Function(lambda: setattr(store.pers_dict['Азриель'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseAsriel.png"
                                                hover "longchooseAsriel.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic

                    if store.pers_dict["Азриель"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:
                        xalign 0.5 yalign -1.0
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Азриель"].shield == 0:
                            frame:
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Азриель"].shield >= 1:
                            frame:
                                xmargin 0
                                ymargin 0
                                xoffset -90 
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Азриель"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Азриель"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                        # Отображение HP для Азриельа
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3


                            if store.pers_dict['Азриель'].current_hp <= store.pers_dict['Азриель'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Азриель'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Азриель'].current_hp > store.pers_dict['Азриель'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Азриель'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Азриель'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            # Полоска HP
                            fixed:

                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Азриель"].current_hp > store.pers_dict["Азриель"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Азриель"].current_hp > store.pers_dict["Азриель"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Азриель"].current_hp - store.pers_dict["Азриель"].max_hp) / store.pers_dict["Азриель"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Азриель"].current_hp > 0 and store.pers_dict["Азриель"].current_hp <= store.pers_dict["Азриель"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Азриель"].current_hp / store.pers_dict["Азриель"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Азриель"].current_hp / store.pers_dict["Азриель"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Азриельа
                        hbox:
                            yalign 0.0
                            xalign 0.5
                            spacing 5
                            xoffset -60 #yoffset -40

                            if store.pers_dict['Азриель'].current_mp <=  store.pers_dict['Азриель'].max_mp* 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Азриель'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                            elif store.pers_dict['Азриель'].current_mp > store.pers_dict['Азриель'].max_mp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Азриель'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Азриель'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            fixed:
                                xysize (60, 8) xalign 1.0
                                fixed:
                                    # Фон MP
                                    hbox:
                                        spacing 3
                                        if store.pers_dict["Азриель"].current_mp > store.pers_dict["Азриель"].max_mp:
                                            # Если HP больше максимума, используем зеленый градиент
                                            for i in range(10):
                                                add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

                                        else:
                                            # Если MP меньше или равно максимуму, используем черный градиент
                                            for i in range(10):
                                                add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения MP
                                    if store.pers_dict["Азриель"].current_mp > store.pers_dict["Азриель"].max_mp:
                                        $ mp_overmana_percent = (store.pers_dict["Азриель"].current_mp - store.pers_dict["Азриель"].max_mp) / store.pers_dict["Азриель"].max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок

                                        # Если MP больше максимума, отображаем 10 иконок mpactive.png
                                        #for i in range(10):
                                        #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

                                    elif store.pers_dict["Азриель"].current_mp > 0 and store.pers_dict["Азриель"].current_mp <= store.pers_dict["Азриель"].max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(store.pers_dict["Азриель"])
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(store.pers_dict["Азриель"])
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray

                        if (store.pers_dict["Азриель"].bloodshed_debuff != 0 or store.pers_dict["Азриель"].prone_debuff != 0 or
                            store.pers_dict["Азриель"].atk != (store.pers_dict["Азриель"].base_atk + store.pers_dict["Азриель"].base_atk_mod) or
                            store.pers_dict["Азриель"].defense != (store.pers_dict["Азриель"].base_def + store.pers_dict["Азриель"].base_def_mod) or
                            store.pers_dict["Азриель"].bonus_tank != 0 or
                            store.pers_dict["Азриель"].magic != (store.pers_dict["Азриель"].base_magic + store.pers_dict["Азриель"].base_magic_mod) or
                            store.pers_dict["Азриель"].dmgchance != (store.pers_dict["Азриель"].base_dmgchance + store.pers_dict["Азриель"].dmgchance_mod) or
                            store.pers_dict["Азриель"].critrate != (store.pers_dict["Азриель"].base_critrate + store.pers_dict["Азриель"].critrate_mod) or
                            store.pers_dict["Азриель"].crit != (store.pers_dict["Азриель"].base_crit + store.pers_dict["Азриель"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Азриельа
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Азриель"].bloodshed_debuff != 0:
                                    if store.pers_dict["Азриель"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Азриель"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Азриель"].prone_debuff != 0:
                                    if store.pers_dict["Азриель"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Азриель"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Азриель"].atk != (store.pers_dict["Азриель"].base_atk + store.pers_dict["Азриель"].base_atk_mod):
                                    if store.pers_dict["Азриель"].atk > (store.pers_dict["Азриель"].base_atk + store.pers_dict["Азриель"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].atk < (store.pers_dict["Азриель"].base_atk + store.pers_dict["Азриель"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Азриель"].defense != (store.pers_dict["Азриель"].base_def + store.pers_dict["Азриель"].base_def_mod):
                                    if store.pers_dict["Азриель"].defense > (store.pers_dict["Азриель"].base_def + store.pers_dict["Азриель"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].defense < (store.pers_dict["Азриель"].base_def + store.pers_dict["Азриель"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Азриель"].bonus_tank != 0:
                                    if store.pers_dict["Азриель"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                


                                if store.pers_dict["Азриель"].magic != (store.pers_dict["Азриель"].base_magic + store.pers_dict["Азриель"].base_magic_mod):
                                    if store.pers_dict["Азриель"].magic > (store.pers_dict["Азриель"].base_magic + store.pers_dict["Азриель"].base_magic_mod):
                                        add "mag_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].magic < (store.pers_dict["Азриель"].base_magic + store.pers_dict["Азриель"].base_magic_mod):
                                        add "mag_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Азриель"].dmgchance != (store.pers_dict["Азриель"].base_dmgchance + store.pers_dict["Азриель"].dmgchance_mod):
                                    if store.pers_dict["Азриель"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].dmgchance > (store.pers_dict["Азриель"].base_dmgchance + store.pers_dict["Азриель"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].dmgchance < (store.pers_dict["Азриель"].base_dmgchance + store.pers_dict["Азриель"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Азриель"].critrate != (store.pers_dict["Азриель"].base_critrate + store.pers_dict["Азриель"].critrate_mod):
                                    if store.pers_dict["Азриель"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].critrate > (store.pers_dict["Азриель"].base_critrate + store.pers_dict["Азриель"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].critrate < (store.pers_dict["Азриель"].base_critrate + store.pers_dict["Азриель"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Азриель"].crit != (store.pers_dict["Азриель"].base_crit + store.pers_dict["Азриель"].crit_mod):
                                    if store.pers_dict["Азриель"].crit > (store.pers_dict["Азриель"].base_crit + store.pers_dict["Азриель"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Азриель"].crit < (store.pers_dict["Азриель"].base_crit + store.pers_dict["Азриель"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Азриель'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Азриель'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic

                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Azriel_desc
                                    at  dynammic_alpha_gray
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Азриель"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Азриель"]), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", "Азриельнажат"), Show ("fullstats1")]
                            
                            elif chardespos == "Азриельнажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Azriel_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()









    #               @@       @@@                                                                                                                                                                                                                                                                                                                                     
    #              @@@@      @@@                                                                                                                                                                                                                                                                                                                                     
    #              @@@@      @@@                                                                                                                                                                                                                                                                                                                                     
    #              @@@@      @@@    @@@@@@@@@    @@@@@@@@@@@     @@@@@@@@                                                                                                                                                                                                                                                                                            
    #              @@@@      @@@    @@@  @@@@@   @@@@@@@@@@@@   @@@@  @@@@                                                                                                                                                                                                                                                                                           
    #               @@@@@@@@@@@@           @@@   @@@@     @@@@         @@@@                                                                                                                                                                                                                                                                                          
    #                @@@@@@@@@@@     @@@@@@@@@   @@@@     @@@@    @@@@@@@@@                                                                                                                                                                                                                                                                                          
    #                        @@@   @@@@@@@@@@@   @@@@     @@@@  @@@@@@@@@@@                                                                                                                                                                                                                                                                                          
    #                        @@@   @@@     @@@   @@@@     @@@@ @@@@    @@@@                                                                                                                                                                                                                                                                                          
    #                        @@@   @@@@@@@@@@@   @@@@@@@@@@@@   @@@@@@@@@@@                                                                                                                                                                                                                                                                                          
    #                        @@@    @@@@@@@@@@   @@@@@@@@@@      @@@@@@@@@@                                                                                                                                                                                                                                                                                          
    #                                            @@@@                                                                                                                                                                                                                                                                                                                
    #                                            @@@@                                                                                                                                                                                                                                                                                                                
    #                                             @@                            



        if store.pers_dict["Чара"].picked == 1:
            hbox: # каждого отдельного персонажа
                spacing 0
                
                at herotochoose
                
                $ yoffset_for_Chara_desc=0

            
                vbox:
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Чараа
                        vbox:
                            if store.pers_dict["Чара"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Чара"].bloodshed_debuff != 0 or store.pers_dict["Чара"].prone_debuff != 0 or
                                        store.pers_dict["Чара"].atk != (store.pers_dict["Чара"].base_atk + store.pers_dict["Чара"].base_atk_mod) or
                                        store.pers_dict["Чара"].defense != (store.pers_dict["Чара"].base_def + store.pers_dict["Чара"].base_def_mod) or
                                        store.pers_dict["Чара"].bonus_tank != 0 or
                                        store.pers_dict["Чара"].dmgchance != (store.pers_dict["Чара"].base_dmgchance + store.pers_dict["Чара"].dmgchance_mod) or
                                        store.pers_dict["Чара"].critrate != (store.pers_dict["Чара"].base_critrate + store.pers_dict["Чара"].critrate_mod) or
                                        store.pers_dict["Чара"].crit != (store.pers_dict["Чара"].base_crit + store.pers_dict["Чара"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Chara_desc= -50

                                        if store.pers_dict["Чара"].current_hp > 0 and store.pers_dict["Чара"].turn == 1 and store.pers_dict["Чара"].prone_debuff == 0:

                                            imagebutton:

                                                idle "longchooseChara.png"
                                                hover "longchooseChara.png"
                                                                                                
                                                action [SetVariable("current_attacker", 3), Function(lambda: setattr(store.pers_dict['Чара'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseChara.png"
                                                hover "longchooseChara.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic
                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                        if store.pers_dict["Чара"].current_hp > 0 and store.pers_dict["Чара"].turn == 1 and store.pers_dict["Чара"].prone_debuff == 0:

                                            imagebutton:
                                                idle "longchooseChara.png"
                                                hover "longchooseChara.png"
                                                action [SetVariable("current_attacker", 3), Function(lambda: setattr(store.pers_dict['Чара'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseChara.png"
                                                hover "longchooseChara.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic

                    if store.pers_dict["Чара"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:

                        xalign 0.5 yalign -1.0 
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Чара"].shield == 0:
                            frame:
                                padding (0,0)
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Чара"].shield >= 1:
                            frame:
                                xoffset -90 
                                xmargin 0
                                ymargin 0
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Чара"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Чара"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                        # Отображение HP для Чараа
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3

                            if store.pers_dict['Чара'].current_hp <= store.pers_dict['Чара'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Чара'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Чара'].current_hp > store.pers_dict['Чара'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Чара'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Чара'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            # Полоска HP
                            fixed:
                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Чара"].current_hp > store.pers_dict["Чара"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Чара"].current_hp > store.pers_dict["Чара"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Чара"].current_hp - store.pers_dict["Чара"].max_hp) / store.pers_dict["Чара"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Чара"].current_hp > 0 and store.pers_dict["Чара"].current_hp <= store.pers_dict["Чара"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Чара"].current_hp / store.pers_dict["Чара"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Чара"].current_hp / store.pers_dict["Чара"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Чараа
                        hbox:
                            yalign 0.0
                            xalign 0.5
                            spacing 5
                            xoffset -60 #yoffset -40

                            if store.pers_dict['Чара'].current_mp <=  store.pers_dict['Чара'].max_mp* 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Чара'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                            elif store.pers_dict['Чара'].current_mp > store.pers_dict['Чара'].max_mp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Чара'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Чара'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            fixed:
                                xysize (60, 8) xalign 1.0
                                fixed:
                                    # Фон MP
                                    hbox:
                                        spacing 3
                                        if store.pers_dict["Чара"].current_mp > store.pers_dict["Чара"].max_mp:
                                            # Если HP больше максимума, используем зеленый градиент
                                            for i in range(10):
                                                add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

                                        else:
                                            # Если MP меньше или равно максимуму, используем черный градиент
                                            for i in range(10):
                                                add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения MP
                                    if store.pers_dict["Чара"].current_mp > store.pers_dict["Чара"].max_mp:
                                        $ mp_overmana_percent = (store.pers_dict["Чара"].current_mp - store.pers_dict["Чара"].max_mp) / store.pers_dict["Чара"].max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок

                                        # Если MP больше максимума, отображаем 10 иконок mpactive.png
                                        #for i in range(10):
                                        #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

                                    elif store.pers_dict["Чара"].current_mp > 0 and store.pers_dict["Чара"].current_mp <= store.pers_dict["Чара"].max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(store.pers_dict["Чара"])
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(store.pers_dict["Чара"])
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray

                        if (store.pers_dict["Чара"].bloodshed_debuff != 0 or store.pers_dict["Чара"].prone_debuff != 0 or
                            store.pers_dict["Чара"].atk != (store.pers_dict["Чара"].base_atk + store.pers_dict["Чара"].base_atk_mod) or
                            store.pers_dict["Чара"].defense != (store.pers_dict["Чара"].base_def + store.pers_dict["Чара"].base_def_mod) or
                            store.pers_dict["Чара"].bonus_tank != 0 or
                            store.pers_dict["Чара"].dmgchance != (store.pers_dict["Чара"].base_dmgchance + store.pers_dict["Чара"].dmgchance_mod) or
                            store.pers_dict["Чара"].critrate != (store.pers_dict["Чара"].base_critrate + store.pers_dict["Чара"].critrate_mod) or
                            store.pers_dict["Чара"].crit != (store.pers_dict["Чара"].base_crit + store.pers_dict["Чара"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Чараа
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Чара"].bloodshed_debuff != 0:
                                    if store.pers_dict["Чара"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Чара"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Чара"].prone_debuff != 0:
                                    if store.pers_dict["Чара"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Чара"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Чара"].atk != (store.pers_dict["Чара"].base_atk + store.pers_dict["Чара"].base_atk_mod):
                                    if store.pers_dict["Чара"].atk > (store.pers_dict["Чара"].base_atk + store.pers_dict["Чара"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].atk < (store.pers_dict["Чара"].base_atk + store.pers_dict["Чара"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Чара"].defense != (store.pers_dict["Чара"].base_def + store.pers_dict["Чара"].base_def_mod):
                                    if store.pers_dict["Чара"].defense > (store.pers_dict["Чара"].base_def + store.pers_dict["Чара"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].defense < (store.pers_dict["Чара"].base_def + store.pers_dict["Чара"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Чара"].bonus_tank != 0:
                                    if store.pers_dict["Чара"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Чара"].dmgchance != (store.pers_dict["Чара"].base_dmgchance + store.pers_dict["Чара"].dmgchance_mod):
                                    if store.pers_dict["Чара"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].dmgchance > (store.pers_dict["Чара"].base_dmgchance + store.pers_dict["Чара"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].dmgchance < (store.pers_dict["Чара"].base_dmgchance + store.pers_dict["Чара"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Чара"].critrate != (store.pers_dict["Чара"].base_critrate + store.pers_dict["Чара"].critrate_mod):
                                    if store.pers_dict["Чара"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].critrate > (store.pers_dict["Чара"].base_critrate + store.pers_dict["Чара"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].critrate < (store.pers_dict["Чара"].base_critrate + store.pers_dict["Чара"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Чара"].crit != (store.pers_dict["Чара"].base_crit + store.pers_dict["Чара"].crit_mod):
                                    if store.pers_dict["Чара"].crit > (store.pers_dict["Чара"].base_crit + store.pers_dict["Чара"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Чара"].crit < (store.pers_dict["Чара"].base_crit + store.pers_dict["Чара"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Чара'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Чара'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic

                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Chara_desc
                                    at dynammic_alpha
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Чара"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Чара"]), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", "Чаранажат"), Show ("fullstats1")]
                            
                            elif chardespos == "Чаранажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Chara_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()










    #                     @@@@                                                                                                                                                                                                                                                                                                                                       
    #                    @@@@@@@                                                                                                                                                                                                                                                                                                                                     
    #                @@@@@@@@@@@@@@                                                                                                                                                                                                                                                                                                                                  
    #               @@@@  @@@@  @@@@@   @@@@@@@@@@     @@@     @@@@     @@@@@@@   @@@    @@@@                                                                                                                                                                                                                                                                        
    #              @@@@   @@@@   @@@@   @@@@@@@@@@@    @@@    @@@@@   @@@@@ @@@@  @@@    @@@@                                                                                                                                                                                                                                                                        
    #              @@@@   @@@@    @@@   @@@@    @@@@   @@@   @@@@@@   @@@         @@@@  @@@@                                                                                                                                                                                                                                                                         
    #              @@@@   @@@@   @@@@   @@@      @@@   @@@ @@@@@@@@  @@@@         @@@@@@@@                                                                                                                                                                                                                                                                           
    #               @@@@@ @@@@ @@@@@    @@@      @@@   @@@@@@@ @@@@  @@@@         @@@@@@@@@                                                                                                                                                                                                                                                                          
    #                @@@@@@@@@@@@@@     @@@@    @@@@   @@@@@   @@@@   @@@         @@@   @@@@                                                                                                                                                                                                                                                                         
    #                     @@@@          @@@@@@@@@@@    @@@@    @@@@   @@@@@@@@@@  @@@    @@@@                                                                                                                                                                                                                                                                        
    #                     @@@@          @@@@@@@@@@     @@@      @@@     @@@@@@@   @@@     @@@                                                                                                                                                                                                                                                                        
    #                                   @@@                                                                                                                                                                                                                                                                                                                          
    #                                   @@@                                                                                                                                                                                                                                                                                                                          
    #                                   @@                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                    
                                                              



        if store.pers_dict["Фриск"].picked == 1:
            hbox: # каждого отдельного персонажа
                spacing 0
                
                at herotochoose
                
                $ yoffset_for_Frisk_desc=0

            
                vbox:
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Фриска
                        vbox:
                            if store.pers_dict["Фриск"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Фриск"].bloodshed_debuff != 0 or store.pers_dict["Фриск"].prone_debuff != 0 or
                                        store.pers_dict["Фриск"].atk != (store.pers_dict["Фриск"].base_atk + store.pers_dict["Фриск"].base_atk_mod) or
                                        store.pers_dict["Фриск"].defense != (store.pers_dict["Фриск"].base_def + store.pers_dict["Фриск"].base_def_mod) or
                                        store.pers_dict["Фриск"].bonus_tank != 0 or
                                        store.pers_dict["Фриск"].dmgchance != (store.pers_dict["Фриск"].base_dmgchance + store.pers_dict["Фриск"].dmgchance_mod) or
                                        store.pers_dict["Фриск"].critrate != (store.pers_dict["Фриск"].base_critrate + store.pers_dict["Фриск"].critrate_mod) or
                                        store.pers_dict["Фриск"].crit != (store.pers_dict["Фриск"].base_crit + store.pers_dict["Фриск"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Frisk_desc= -50

                                        if store.pers_dict["Фриск"].current_hp > 0 and store.pers_dict["Фриск"].turn == 1 and store.pers_dict["Фриск"].prone_debuff == 0:

                                            imagebutton:

                                                idle "longchooseFrisk.png"
                                                hover "longchooseFrisk.png"
                                                                                                
                                                action [SetVariable("current_attacker", 4), Function(lambda: setattr(store.pers_dict['Фриск'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseFrisk.png"
                                                hover "longchooseFrisk.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic
                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                        if store.pers_dict["Фриск"].current_hp > 0 and store.pers_dict["Фриск"].turn == 1 and store.pers_dict["Фриск"].prone_debuff == 0:

                                            imagebutton:
                                                idle "longchooseFrisk.png"
                                                hover "longchooseFrisk.png"
                                                action [SetVariable("current_attacker", 4), Function(lambda: setattr(store.pers_dict['Фриск'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseFrisk.png"
                                                hover "longchooseFrisk.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic

                    if store.pers_dict["Фриск"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:
                        xalign 0.5 yalign -1.0
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Фриск"].shield == 0:
                            frame:
                                padding (0,0)
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Фриск"].shield >= 1:
                            frame:
                                xoffset -90 
                                xmargin 0
                                ymargin 0
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Фриск"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Фриск"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                        # Отображение HP для Фриска
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3

                            if store.pers_dict['Фриск'].current_hp <= store.pers_dict['Фриск'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Фриск'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Фриск'].current_hp > store.pers_dict['Фриск'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Фриск'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Фриск'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            # Полоска HP
                            fixed:
                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Фриск"].current_hp > store.pers_dict["Фриск"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Фриск"].current_hp > store.pers_dict["Фриск"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Фриск"].current_hp - store.pers_dict["Фриск"].max_hp) / store.pers_dict["Фриск"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Фриск"].current_hp > 0 and store.pers_dict["Фриск"].current_hp <= store.pers_dict["Фриск"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Фриск"].current_hp / store.pers_dict["Фриск"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Фриск"].current_hp / store.pers_dict["Фриск"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Фриска
                        hbox:
                            yalign 0.0
                            xalign 0.5
                            spacing 5
                            xoffset -60 #yoffset -40

                            if store.pers_dict['Фриск'].current_mp <=  store.pers_dict['Фриск'].max_mp* 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Фриск'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                            elif store.pers_dict['Фриск'].current_mp > store.pers_dict['Фриск'].max_mp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Фриск'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Фриск'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            fixed:
                                xysize (60, 8) xalign 1.0
                                fixed:
                                    # Фон MP
                                    hbox:
                                        spacing 3
                                        if store.pers_dict["Фриск"].current_mp > store.pers_dict["Фриск"].max_mp:
                                            # Если HP больше максимума, используем зеленый градиент
                                            for i in range(10):
                                                add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

                                        else:
                                            # Если MP меньше или равно максимуму, используем черный градиент
                                            for i in range(10):
                                                add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения MP
                                    if store.pers_dict["Фриск"].current_mp > store.pers_dict["Фриск"].max_mp:
                                        $ mp_overmana_percent = (store.pers_dict["Фриск"].current_mp - store.pers_dict["Фриск"].max_mp) / store.pers_dict["Фриск"].max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок

                                        # Если MP больше максимума, отображаем 10 иконок mpactive.png
                                        #for i in range(10):
                                        #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

                                    elif store.pers_dict["Фриск"].current_mp > 0 and store.pers_dict["Фриск"].current_mp <= store.pers_dict["Фриск"].max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(store.pers_dict["Фриск"])
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(store.pers_dict["Фриск"])
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray

                        if (store.pers_dict["Фриск"].bloodshed_debuff != 0 or store.pers_dict["Фриск"].prone_debuff != 0 or
                            store.pers_dict["Фриск"].atk != (store.pers_dict["Фриск"].base_atk + store.pers_dict["Фриск"].base_atk_mod) or
                            store.pers_dict["Фриск"].defense != (store.pers_dict["Фриск"].base_def + store.pers_dict["Фриск"].base_def_mod) or
                            store.pers_dict["Фриск"].bonus_tank != 0 or
                            store.pers_dict["Фриск"].dmgchance != (store.pers_dict["Фриск"].base_dmgchance + store.pers_dict["Фриск"].dmgchance_mod) or
                            store.pers_dict["Фриск"].critrate != (store.pers_dict["Фриск"].base_critrate + store.pers_dict["Фриск"].critrate_mod) or
                            store.pers_dict["Фриск"].crit != (store.pers_dict["Фриск"].base_crit + store.pers_dict["Фриск"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Фриска
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Фриск"].bloodshed_debuff != 0:
                                    if store.pers_dict["Фриск"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Фриск"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Фриск"].prone_debuff != 0:
                                    if store.pers_dict["Фриск"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Фриск"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Фриск"].atk != (store.pers_dict["Фриск"].base_atk + store.pers_dict["Фриск"].base_atk_mod):
                                    if store.pers_dict["Фриск"].atk > (store.pers_dict["Фриск"].base_atk + store.pers_dict["Фриск"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].atk < (store.pers_dict["Фриск"].base_atk + store.pers_dict["Фриск"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Фриск"].defense != (store.pers_dict["Фриск"].base_def + store.pers_dict["Фриск"].base_def_mod):
                                    if store.pers_dict["Фриск"].defense > (store.pers_dict["Фриск"].base_def + store.pers_dict["Фриск"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].defense < (store.pers_dict["Фриск"].base_def + store.pers_dict["Фриск"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Фриск"].bonus_tank != 0:
                                    if store.pers_dict["Фриск"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Фриск"].dmgchance != (store.pers_dict["Фриск"].base_dmgchance + store.pers_dict["Фриск"].dmgchance_mod):
                                    if store.pers_dict["Фриск"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].dmgchance > (store.pers_dict["Фриск"].base_dmgchance + store.pers_dict["Фриск"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].dmgchance < (store.pers_dict["Фриск"].base_dmgchance + store.pers_dict["Фриск"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Фриск"].critrate != (store.pers_dict["Фриск"].base_critrate + store.pers_dict["Фриск"].critrate_mod):
                                    if store.pers_dict["Фриск"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].critrate > (store.pers_dict["Фриск"].base_critrate + store.pers_dict["Фриск"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].critrate < (store.pers_dict["Фриск"].base_critrate + store.pers_dict["Фриск"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Фриск"].crit != (store.pers_dict["Фриск"].base_crit + store.pers_dict["Фриск"].crit_mod):
                                    if store.pers_dict["Фриск"].crit > (store.pers_dict["Фриск"].base_crit + store.pers_dict["Фриск"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Фриск"].crit < (store.pers_dict["Фриск"].base_crit + store.pers_dict["Фриск"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Фриск'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Фриск'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic

                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Frisk_desc
                                    at dynammic_alpha
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Фриск"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Фриск"]), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", "Фрискнажат"), Show ("fullstats1")]
                            
                            elif chardespos == "Фрискнажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Frisk_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()












#                    @@         @@                                                                                                                                                                                                                                                                                                                                   
#                   @@@@       @@@@                                                                                                                                                                                                                                                                                                                                  
#                   @@@@     @@@@@@                                                                                                                                                                                                                                                                                                                                  
#                   @@@@    @@@@@@@   @@@@@@@@    @@@@@@@@    @@@      @@@                                                                                                                                                                                                                                                                                           
#                   @@@@   @@@ @@@@  @@@@  @@@@  @@@@  @@@@   @@@@    @@@@                                                                                                                                                                                                                                                                                           
#                   @@@@  @@@@ @@@@         @@@         @@@   @@@@  @@@@@@                                                                                                                                                                                                                                                                                           
#                   @@@@@@@@   @@@@    @@@@@@@     @@@@@@@@   @@@@ @@@@@@@                                                                                                                                                                                                                                                                                           
#                   @@@@@@@    @@@@    @@@@@@@@    @@@@@@@@   @@@@@@@  @@@                                                                                                                                                                                                                                                                                           
#                   @@@@@      @@@@         @@@@        @@@@  @@@@@@   @@@                                                                                                                                                                                                                                                                                           
#                   @@@@@      @@@@  @@@@@@@@@@@ @@@@@@@@@@   @@@@@    @@@                                                                                                                                                                                                                                                                                           
#                   @@@@       @@@@   @@@@@@@@    @@@@@@@@    @@@      @@@                                                                                                                                                                                                                                                                                           
                                                                           








        if store.pers_dict["Иззи"].picked == 1:
            hbox: # каждого отдельного персонажа
                spacing 0
                
                at herotochoose
                
                $ yoffset_for_Izzy_desc=0

            
                vbox:
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Иззиа
                        vbox:
                            if store.pers_dict["Иззи"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Иззи"].bloodshed_debuff != 0 or store.pers_dict["Иззи"].prone_debuff != 0 or
                                        store.pers_dict["Иззи"].atk != (store.pers_dict["Иззи"].base_atk + store.pers_dict["Иззи"].base_atk_mod) or
                                        store.pers_dict["Иззи"].defense != (store.pers_dict["Иззи"].base_def + store.pers_dict["Иззи"].base_def_mod) or
                                        store.pers_dict["Иззи"].bonus_tank != 0 or
                                        store.pers_dict["Иззи"].magic != (store.pers_dict["Иззи"].base_magic + store.pers_dict["Иззи"].base_magic_mod) or
                                        store.pers_dict["Иззи"].dmgchance != (store.pers_dict["Иззи"].base_dmgchance + store.pers_dict["Иззи"].dmgchance_mod) or
                                        store.pers_dict["Иззи"].critrate != (store.pers_dict["Иззи"].base_critrate + store.pers_dict["Иззи"].critrate_mod) or
                                        store.pers_dict["Иззи"].crit != (store.pers_dict["Иззи"].base_crit + store.pers_dict["Иззи"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Izzy_desc= -50

                                        if store.pers_dict["Иззи"].current_hp > 0 and store.pers_dict["Иззи"].turn == 1 and store.pers_dict["Иззи"].prone_debuff == 0:

                                            imagebutton:

                                                idle "longchooseIzzy.png"
                                                hover "longchooseIzzy.png"
                                                                                                
                                                action [SetVariable("current_attacker", 5), Function(lambda: setattr(store.pers_dict['Иззи'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseIzzy.png"
                                                hover "longchooseIzzy.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic
                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                        if store.pers_dict["Иззи"].current_hp > 0 and store.pers_dict["Иззи"].turn == 1 and store.pers_dict["Иззи"].prone_debuff == 0:

                                            imagebutton:
                                                idle "longchooseIzzy.png"
                                                hover "longchooseIzzy.png"
                                                action [SetVariable("current_attacker", 5), Function(lambda: setattr(store.pers_dict['Иззи'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseIzzy.png"
                                                hover "longchooseIzzy.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic

                    if store.pers_dict["Иззи"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:
                        xalign 0.5 yalign -1.0
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Иззи"].shield == 0:
                            frame:
                                padding (0,0)
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Иззи"].shield >= 1:
                            frame:
                                xoffset -90 
                                xmargin 0
                                ymargin 0
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Иззи"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Иззи"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                        # Отображение HP для Иззиа
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3

                            if store.pers_dict['Иззи'].current_hp <= store.pers_dict['Иззи'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Иззи'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Иззи'].current_hp > store.pers_dict['Иззи'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Иззи'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Иззи'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            # Полоска HP
                            fixed:
                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Иззи"].current_hp > store.pers_dict["Иззи"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Иззи"].current_hp > store.pers_dict["Иззи"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Иззи"].current_hp - store.pers_dict["Иззи"].max_hp) / store.pers_dict["Иззи"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Иззи"].current_hp > 0 and store.pers_dict["Иззи"].current_hp <= store.pers_dict["Иззи"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Иззи"].current_hp / store.pers_dict["Иззи"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Иззи"].current_hp / store.pers_dict["Иззи"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Иззиа
                        hbox:
                            yalign 0.0
                            xalign 0.5
                            spacing 5
                            xoffset -60 #yoffset -40

                            if store.pers_dict['Иззи'].current_mp <=  store.pers_dict['Иззи'].max_mp* 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Иззи'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                            elif store.pers_dict['Иззи'].current_mp > store.pers_dict['Иззи'].max_mp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Иззи'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Иззи'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            fixed:
                                xysize (60, 8) xalign 1.0
                                fixed:
                                    # Фон MP
                                    hbox:
                                        spacing 3
                                        if store.pers_dict["Иззи"].current_mp > store.pers_dict["Иззи"].max_mp:
                                            # Если HP больше максимума, используем зеленый градиент
                                            for i in range(10):
                                                add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

                                        else:
                                            # Если MP меньше или равно максимуму, используем черный градиент
                                            for i in range(10):
                                                add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения MP
                                    if store.pers_dict["Иззи"].current_mp > store.pers_dict["Иззи"].max_mp:
                                        $ mp_overmana_percent = (store.pers_dict["Иззи"].current_mp - store.pers_dict["Иззи"].max_mp) / store.pers_dict["Иззи"].max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок

                                        # Если MP больше максимума, отображаем 10 иконок mpactive.png
                                        #for i in range(10):
                                        #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

                                    elif store.pers_dict["Иззи"].current_mp > 0 and store.pers_dict["Иззи"].current_mp <= store.pers_dict["Иззи"].max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(store.pers_dict["Иззи"])
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(store.pers_dict["Иззи"])
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray

                        if (store.pers_dict["Иззи"].bloodshed_debuff != 0 or store.pers_dict["Иззи"].prone_debuff != 0 or
                            store.pers_dict["Иззи"].atk != (store.pers_dict["Иззи"].base_atk + store.pers_dict["Иззи"].base_atk_mod) or
                            store.pers_dict["Иззи"].defense != (store.pers_dict["Иззи"].base_def + store.pers_dict["Иззи"].base_def_mod) or
                            store.pers_dict["Иззи"].bonus_tank != 0 or
                            store.pers_dict["Иззи"].magic != (store.pers_dict["Иззи"].base_magic + store.pers_dict["Иззи"].base_magic_mod) or
                            store.pers_dict["Иззи"].dmgchance != (store.pers_dict["Иззи"].base_dmgchance + store.pers_dict["Иззи"].dmgchance_mod) or
                            store.pers_dict["Иззи"].critrate != (store.pers_dict["Иззи"].base_critrate + store.pers_dict["Иззи"].critrate_mod) or
                            store.pers_dict["Иззи"].crit != (store.pers_dict["Иззи"].base_crit + store.pers_dict["Иззи"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Иззиа
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Иззи"].bloodshed_debuff != 0:
                                    if store.pers_dict["Иззи"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Иззи"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Иззи"].prone_debuff != 0:
                                    if store.pers_dict["Иззи"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Иззи"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Иззи"].atk != (store.pers_dict["Иззи"].base_atk + store.pers_dict["Иззи"].base_atk_mod):
                                    if store.pers_dict["Иззи"].atk > (store.pers_dict["Иззи"].base_atk + store.pers_dict["Иззи"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].atk < (store.pers_dict["Иззи"].base_atk + store.pers_dict["Иззи"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Иззи"].defense != (store.pers_dict["Иззи"].base_def + store.pers_dict["Иззи"].base_def_mod):
                                    if store.pers_dict["Иззи"].defense > (store.pers_dict["Иззи"].base_def + store.pers_dict["Иззи"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].defense < (store.pers_dict["Иззи"].base_def + store.pers_dict["Иззи"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Иззи"].bonus_tank != 0:
                                    if store.pers_dict["Иззи"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                


                                if store.pers_dict["Иззи"].magic != (store.pers_dict["Иззи"].base_magic + store.pers_dict["Иззи"].base_magic_mod):
                                    if store.pers_dict["Иззи"].magic > (store.pers_dict["Иззи"].base_magic + store.pers_dict["Иззи"].base_magic_mod):
                                        add "mag_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].magic < (store.pers_dict["Иззи"].base_magic + store.pers_dict["Иззи"].base_magic_mod):
                                        add "mag_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Иззи"].dmgchance != (store.pers_dict["Иззи"].base_dmgchance + store.pers_dict["Иззи"].dmgchance_mod):
                                    if store.pers_dict["Иззи"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].dmgchance > (store.pers_dict["Иззи"].base_dmgchance + store.pers_dict["Иззи"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].dmgchance < (store.pers_dict["Иззи"].base_dmgchance + store.pers_dict["Иззи"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Иззи"].critrate != (store.pers_dict["Иззи"].base_critrate + store.pers_dict["Иззи"].critrate_mod):
                                    if store.pers_dict["Иззи"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].critrate > (store.pers_dict["Иззи"].base_critrate + store.pers_dict["Иззи"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].critrate < (store.pers_dict["Иззи"].base_critrate + store.pers_dict["Иззи"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Иззи"].crit != (store.pers_dict["Иззи"].base_crit + store.pers_dict["Иззи"].crit_mod):
                                    if store.pers_dict["Иззи"].crit > (store.pers_dict["Иззи"].base_crit + store.pers_dict["Иззи"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Иззи"].crit < (store.pers_dict["Иззи"].base_crit + store.pers_dict["Иззи"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Иззи'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Иззи'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic

                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Izzy_desc
                                    at dynammic_alpha
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Иззи"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Иззи"]), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", "Иззинажат"), Show ("fullstats1")]
                            
                            elif chardespos == "Иззинажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Izzy_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()










#                    @@      @@@                                                                                                                                                                                                                                                                                                                                     
#                   @@@@    @@@@                                                                                                                                                                                                                                                                                                                                     
#                   @@@@    @@@@                                                                                                                                                                                                                                                                                                                                     
#                   @@@@   @@@@       @@@@@@@@@     @@@@@@@@     @@@@@@@@@      @@@@@@@@     @@@@@@@@@@                                                                                                                                                                                                                                                              
#                   @@@@  @@@@       @@@@@@@@@@   @@@@@ @@@@@@   @@@   @@@@    @@@@  @@@@    @@@@@@@@@@@                                                                                                                                                                                                                                                             
#                   @@@@@@@@@        @@@@  @@@@  @@@@      @@@   @@@    @@@@  @@@@     @@@   @@@@    @@@@                                                                                                                                                                                                                                                            
#                   @@@@ @@@@@       @@@   @@@@  @@@@      @@@@  @@@@@@@@@@   @@@@@@@@@@@@   @@@      @@@                                                                                                                                                                                                                                                            
#                   @@@@   @@@@     @@@@   @@@@  @@@@      @@@@  @@@@@@@@@@@  @@@@@@@@@@@@   @@@      @@@                                                                                                                                                                                                                                                            
#                   @@@@    @@@@    @@@@   @@@@  @@@@      @@@   @@@     @@@  @@@@           @@@@    @@@@                                                                                                                                                                                                                                                            
#                   @@@@     @@@@ @@@@@    @@@@   @@@@@@@@@@@    @@@@@@@@@@@   @@@@@@@@@@@   @@@@@@@@@@@                                                                                                                                                                                                                                                             
#                   @@@@     @@@@@@@@      @@@@     @@@@@@@      @@@@@@@@@      @@@@@@@@@    @@@@@@@@@@                                                                                                                                                                                                                                                              
#                                                                                            @@@                                                                                                                                                                                                                                                                     
#                                                                                            @@@                                                                                                                                                                                                                                                                     
#                                                                                            @@                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                          



        if store.pers_dict["Кловер"].picked == 1:

            hbox: # каждого отдельного персонажа
                spacing 0
                
                at herotochoose
                
                $ yoffset_for_Clover_desc=0

            
                vbox:
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Кловера
                        vbox:
                            if store.pers_dict["Кловер"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Кловер"].bloodshed_debuff != 0 or store.pers_dict["Кловер"].prone_debuff != 0 or
                                        store.pers_dict["Кловер"].atk != (store.pers_dict["Кловер"].base_atk + store.pers_dict["Кловер"].base_atk_mod) or
                                        store.pers_dict["Кловер"].defense != (store.pers_dict["Кловер"].base_def + store.pers_dict["Кловер"].base_def_mod) or
                                        store.pers_dict["Кловер"].bonus_tank != 0 or
                                        store.pers_dict["Кловер"].magic != (store.pers_dict["Кловер"].base_magic + store.pers_dict["Кловер"].base_magic_mod) or
                                        store.pers_dict["Кловер"].dmgchance != (store.pers_dict["Кловер"].base_dmgchance + store.pers_dict["Кловер"].dmgchance_mod) or
                                        store.pers_dict["Кловер"].critrate != (store.pers_dict["Кловер"].base_critrate + store.pers_dict["Кловер"].critrate_mod) or
                                        store.pers_dict["Кловер"].crit != (store.pers_dict["Кловер"].base_crit + store.pers_dict["Кловер"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Clover_desc= -50

                                        if store.pers_dict["Кловер"].current_hp > 0 and store.pers_dict["Кловер"].turn == 1 and store.pers_dict["Кловер"].prone_debuff == 0:

                                            imagebutton:

                                                idle "longchooseClover.png"
                                                hover "longchooseClover.png"
                                                                                                  
                                                action [SetVariable("current_attacker", 6), Function(lambda: setattr(store.pers_dict['Кловер'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseClover.png"
                                                hover "longchooseClover.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic
                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                        if store.pers_dict["Кловер"].current_hp > 0 and store.pers_dict["Кловер"].turn == 1 and store.pers_dict["Кловер"].prone_debuff == 0:

                                            imagebutton:
                                                idle "longchooseClover.png"
                                                hover "longchooseClover.png"
                                                action [SetVariable("current_attacker", 6), Function(lambda: setattr(store.pers_dict['Кловер'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseClover.png"
                                                hover "longchooseClover.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                at choosestatic

                    if store.pers_dict["Кловер"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:
                        xalign 0.5 yalign -1.0
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Кловер"].shield == 0:
                            frame:
                                padding (0,0)
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Кловер"].shield >= 1:
                            frame:
                                xoffset -90 
                                xmargin 0
                                ymargin 0
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Кловер"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Кловер"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                        # Отображение HP для Кловера
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3

                            if store.pers_dict['Кловер'].current_hp <= store.pers_dict['Кловер'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Кловер'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Кловер'].current_hp > store.pers_dict['Кловер'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Кловер'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Кловер'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            # Полоска HP
                            fixed:
                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Кловер"].current_hp > store.pers_dict["Кловер"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Кловер"].current_hp > store.pers_dict["Кловер"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Кловер"].current_hp - store.pers_dict["Кловер"].max_hp) / store.pers_dict["Кловер"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Кловер"].current_hp > 0 and store.pers_dict["Кловер"].current_hp <= store.pers_dict["Кловер"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Кловер"].current_hp / store.pers_dict["Кловер"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Кловер"].current_hp / store.pers_dict["Кловер"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Кловера
                        hbox:
                            yalign 0.0
                            xalign 0.5
                            spacing 5
                            xoffset -60 #yoffset -40

                            if store.pers_dict['Кловер'].current_mp <=  store.pers_dict['Кловер'].max_mp* 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Кловер'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                            elif store.pers_dict['Кловер'].current_mp > store.pers_dict['Кловер'].max_mp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Кловер'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Кловер'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            fixed:
                                xysize (60, 8) xalign 1.0
                                fixed:
                                    # Фон MP
                                    hbox:
                                        spacing 3
                                        if store.pers_dict["Кловер"].current_mp > store.pers_dict["Кловер"].max_mp:
                                            # Если HP больше максимума, используем зеленый градиент
                                            for i in range(10):
                                                add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

                                        else:
                                            # Если MP меньше или равно максимуму, используем черный градиент
                                            for i in range(10):
                                                add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения MP
                                    if store.pers_dict["Кловер"].current_mp > store.pers_dict["Кловер"].max_mp:
                                        $ mp_overmana_percent = (store.pers_dict["Кловер"].current_mp - store.pers_dict["Кловер"].max_mp) / store.pers_dict["Кловер"].max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок

                                        # Если MP больше максимума, отображаем 10 иконок mpactive.png
                                        #for i in range(10):
                                        #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

                                    elif store.pers_dict["Кловер"].current_mp > 0 and store.pers_dict["Кловер"].current_mp <= store.pers_dict["Кловер"].max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(store.pers_dict["Кловер"])
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(store.pers_dict["Кловер"])
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray

                        if (store.pers_dict["Кловер"].bloodshed_debuff != 0 or store.pers_dict["Кловер"].prone_debuff != 0 or
                            store.pers_dict["Кловер"].atk != (store.pers_dict["Кловер"].base_atk + store.pers_dict["Кловер"].base_atk_mod) or
                            store.pers_dict["Кловер"].defense != (store.pers_dict["Кловер"].base_def + store.pers_dict["Кловер"].base_def_mod) or
                            store.pers_dict["Кловер"].bonus_tank != 0 or
                            store.pers_dict["Кловер"].magic != (store.pers_dict["Кловер"].base_magic + store.pers_dict["Кловер"].base_magic_mod) or
                            store.pers_dict["Кловер"].dmgchance != (store.pers_dict["Кловер"].base_dmgchance + store.pers_dict["Кловер"].dmgchance_mod) or
                            store.pers_dict["Кловер"].critrate != (store.pers_dict["Кловер"].base_critrate + store.pers_dict["Кловер"].critrate_mod) or
                            store.pers_dict["Кловер"].crit != (store.pers_dict["Кловер"].base_crit + store.pers_dict["Кловер"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Кловера
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Кловер"].bloodshed_debuff != 0:
                                    if store.pers_dict["Кловер"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Кловер"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Кловер"].prone_debuff != 0:
                                    if store.pers_dict["Кловер"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Кловер"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Кловер"].atk != (store.pers_dict["Кловер"].base_atk + store.pers_dict["Кловер"].base_atk_mod):
                                    if store.pers_dict["Кловер"].atk > (store.pers_dict["Кловер"].base_atk + store.pers_dict["Кловер"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].atk < (store.pers_dict["Кловер"].base_atk + store.pers_dict["Кловер"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Кловер"].defense != (store.pers_dict["Кловер"].base_def + store.pers_dict["Кловер"].base_def_mod):
                                    if store.pers_dict["Кловер"].defense > (store.pers_dict["Кловер"].base_def + store.pers_dict["Кловер"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].defense < (store.pers_dict["Кловер"].base_def + store.pers_dict["Кловер"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Кловер"].bonus_tank != 0:
                                    if store.pers_dict["Кловер"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                


                                if store.pers_dict["Кловер"].magic != (store.pers_dict["Кловер"].base_magic + store.pers_dict["Кловер"].base_magic_mod):
                                    if store.pers_dict["Кловер"].magic > (store.pers_dict["Кловер"].base_magic + store.pers_dict["Кловер"].base_magic_mod):
                                        add "mag_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].magic < (store.pers_dict["Кловер"].base_magic + store.pers_dict["Кловер"].base_magic_mod):
                                        add "mag_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Кловер"].dmgchance != (store.pers_dict["Кловер"].base_dmgchance + store.pers_dict["Кловер"].dmgchance_mod):
                                    if store.pers_dict["Кловер"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].dmgchance > (store.pers_dict["Кловер"].base_dmgchance + store.pers_dict["Кловер"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].dmgchance < (store.pers_dict["Кловер"].base_dmgchance + store.pers_dict["Кловер"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Кловер"].critrate != (store.pers_dict["Кловер"].base_critrate + store.pers_dict["Кловер"].critrate_mod):
                                    if store.pers_dict["Кловер"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].critrate > (store.pers_dict["Кловер"].base_critrate + store.pers_dict["Кловер"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].critrate < (store.pers_dict["Кловер"].base_critrate + store.pers_dict["Кловер"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Кловер"].crit != (store.pers_dict["Кловер"].base_crit + store.pers_dict["Кловер"].crit_mod):
                                    if store.pers_dict["Кловер"].crit > (store.pers_dict["Кловер"].base_crit + store.pers_dict["Кловер"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Кловер"].crit < (store.pers_dict["Кловер"].base_crit + store.pers_dict["Кловер"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Кловер'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Кловер'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic

                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Clover_desc
                                    at dynammic_alpha
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Кловер"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Кловер"]), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", "Кловернажат"), Show ("fullstats1")]
                            
                            elif chardespos == "Кловернажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Clover_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()







                                                                                                                                                                                                                                                                                                                                                                    
#                        @@@@@                                                                                                                                                                                                                                                                                                                                       
#                     @@@@@@@@@@@                                                                                                                                                                                                                                                                                                                                    
#                   @@@@@     @@@                                                                                                                                                                                                                                                                                                                                    
#                   @@@@             @@@@@@@       @@@@@@@@@@    @@@@@@@@@@     @@@      @@@   @@@    @@@@                                                                                                                                                                                                                                                           
#                  @@@@            @@@@@  @@@@     @@@@@@@@@@    @@@@@@@@@@@@   @@@    @@@@@   @@@    @@@                                                                                                                                                                                                                                                            
#                  @@@@            @@@     @@@@    @@@   @@@@    @@@@    @@@@   @@@   @@@@@@   @@@   @@@                                                                                                                                                                                                                                                             
#                  @@@@           @@@@@@@@@@@@@    @@@   @@@@    @@@      @@@@  @@@  @@@ @@@   @@@@@@@@                                                                                                                                                                                                                                                              
#                  @@@@           @@@@@@@@@@@@    @@@@   @@@@    @@@      @@@@  @@@@@@@  @@@   @@@@@@@@@                                                                                                                                                                                                                                                             
#                   @@@@           @@@            @@@    @@@@    @@@@    @@@@   @@@@@@   @@@   @@@   @@@@                                                                                                                                                                                                                                                            
#                    @@@@@@@@@@@@  @@@@@@@@@@@ @@@@@@@@@@@@@@@@  @@@@@@@@@@@    @@@@     @@@   @@@    @@@@                                                                                                                                                                                                                                                           
#                      @@@@@@@@      @@@@@@@@  @@@@@@@@@@@@@@@@  @@@@@@@@@@     @@@      @@@   @@@     @@@                                                                                                                                                                                                                                                           
#                                              @@@          @@@  @@@                                                                                                                                                                                                                                                                                                 
#                                              @@@          @@@  @@@                      




        if store.pers_dict["Седрик"].picked == 1:

            hbox: # каждого отдельного персонажа
                spacing 0
                
                at herotochoose
                
                $ yoffset_for_Sedric_desc=0

            
                vbox:
                    spacing 10
                    frame:
                        yalign 0.0
                        padding (0, 0)  # Убираем внутренние отступы
                        xmargin 0       # Убираем горизонтальные поля
                        ymargin 0   
                        background None
                        # Кнопка для Седрика
                        vbox:
                            if store.pers_dict["Седрик"].picked == 1:
                                vbox:

                                    spacing 10

                                    if (store.pers_dict["Седрик"].bloodshed_debuff != 0 or store.pers_dict["Седрик"].prone_debuff != 0 or
                                        store.pers_dict["Седрик"].atk != (store.pers_dict["Седрик"].base_atk + store.pers_dict["Седрик"].base_atk_mod) or
                                        store.pers_dict["Седрик"].defense != (store.pers_dict["Седрик"].base_def + store.pers_dict["Седрик"].base_def_mod) or
                                        store.pers_dict["Седрик"].bonus_tank != 0 or
                                        store.pers_dict["Седрик"].dmgchance != (store.pers_dict["Седрик"].base_dmgchance + store.pers_dict["Седрик"].dmgchance_mod) or
                                        store.pers_dict["Седрик"].critrate != (store.pers_dict["Седрик"].base_critrate + store.pers_dict["Седрик"].critrate_mod) or
                                        store.pers_dict["Седрик"].crit != (store.pers_dict["Седрик"].base_crit + store.pers_dict["Седрик"].crit_mod)):
                                        
                                        $ yoffset_for_vbox = 0
                                        $ yoffset_for_vbox_name = 0
                                        $ yoffset_for_Sedric_desc= -50

                                        if store.pers_dict["Седрик"].current_hp > 0 and store.pers_dict["Седрик"].turn == 1 and store.pers_dict["Седрик"].prone_debuff == 0:

                                            imagebutton:

                                                idle "longchooseSedric.png"
                                                hover "longchooseSedric.png"
                                                                                                  
                                                action [SetVariable("current_attacker", 7), Function(lambda: setattr(store.pers_dict['Седрик'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseSedric.png"
                                                hover "longchooseSedric.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                #at choosedynamic
                                    else:

                                        $ yoffset_for_vbox = 35
                                        $ yoffset_for_vbox_name = 50

                                        if store.pers_dict["Седрик"].current_hp > 0 and store.pers_dict["Седрик"].turn == 1 and store.pers_dict["Седрик"].prone_debuff == 0:

                                            imagebutton:
                                                idle "longchooseSedric.png"
                                                hover "longchooseSedric.png"
                                                action [SetVariable("current_attacker", 7), Function(lambda: setattr(store.pers_dict['Седрик'], 'step_forward', 1)), Jump("playerturn2")]
                                                at choosedynamic
                                        else:
                                            imagebutton:
                                                idle "longchooseSedric.png"
                                                hover "longchooseSedric.png"
                                                #unhovered SetVariable("Zoomforvis", 1)
                                                #hovered   SetVariable("Zoomforvis", 1.2 )
                                                action NullAction()
                                                #at choosedynamic

                    if store.pers_dict["Седрик"].current_hp == 0:
                        $ yoffset_for_dead = 2
                    else:
                        $ yoffset_for_dead = 0
                    vbox:
                        xalign 0.5 yalign -1.0
                        spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                        if store.pers_dict["Седрик"].shield == 0:
                            frame:
                                padding (0,0)
                                xmargin 0
                                ymargin 0
                                yoffset -5
                                xysize (70, 12)
                                background None 
                                text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 

                        elif store.pers_dict["Седрик"].shield >= 1:
                            frame:
                                xoffset -90 
                                xmargin 0
                                ymargin 0
                                #yoffset -5
                                xalign 0.5
                                yalign 0.0
                                xysize (70, 12)
                                background None         

                                # Фон щита (всегда 4 позиции)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        for i in range(1, 5):
                                            add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                # Заполнение щита (текущее значение)
                                fixed:
                                    hbox:
                                        xalign 0.0 yalign 1.0
                                        spacing 2
                                        if store.pers_dict["Седрик"].shield >= 4:
                                            # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                            for i in range(1, 5):
                                                add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                        else:
                                            # Иначе отображаем обычное заполнение
                                            for i in range(1, min(store.pers_dict["Седрик"].shield + 1, 5)):
                                                add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                        # Отображение HP для Седрика
                        hbox:
                            xoffset -60  #yoffset -15
                            xalign 0.5 yalign 1
                            spacing 3

                            if store.pers_dict['Седрик'].current_hp <= store.pers_dict['Седрик'].max_hp * 0.2:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Седрик'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                            elif store.pers_dict['Седрик'].current_hp > store.pers_dict['Седрик'].max_hp:
                                text "{font=determination.otf}{size=40}[store.pers_dict['Седрик'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_green_bright
                            else:
                                text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Седрик'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

                            # Полоска HP
                            fixed:
                                xysize (60, 8) xalign 1.0
                                # Фон HP
                                hbox:
                                    spacing 3
                                    if store.pers_dict["Седрик"].current_hp > store.pers_dict["Седрик"].max_hp:
                                        # Если HP больше максимума, используем зеленый градиент
                                        for i in range(10):
                                            add Solid("#ff2020", xysize=(12, 22)) zoom 1.2 at damage_gradient_green_bright

                                    else:
                                        # Если HP меньше или равно максимуму, используем черный градиент
                                        for i in range(10):
                                            add "hppassive.png" zoom 1.2 at damage_gradient_black
                                # Заполнение HP
                                hbox:
                                    spacing 3
                                    # Проверяем условия для отображения HP
                                    if store.pers_dict["Седрик"].current_hp > store.pers_dict["Седрик"].max_hp:
                                        # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                        $ hp_overheal_percent = (store.pers_dict["Седрик"].current_hp - store.pers_dict["Седрик"].max_hp) / store.pers_dict["Седрик"].max_hp * 100
                                        $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                        for i in range(overheal_icons):
                                            add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                    elif store.pers_dict["Седрик"].current_hp > 0 and store.pers_dict["Седрик"].current_hp <= store.pers_dict["Седрик"].max_hp * 0.2:
                                        # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = int(math.ceil((store.pers_dict["Седрик"].current_hp / store.pers_dict["Седрик"].max_hp) * 10))
                                        for i in range(low_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    else:
                                        # Обычное отображение HP
                                        $ hp_fill = int(math.ceil((store.pers_dict["Седрик"].current_hp / store.pers_dict["Седрик"].max_hp) * 10))
                                        for i in range(hp_fill):
                                            add "hpactive.png" zoom 1.2 at damage_gradient_gray
                        
                        # Отображение MP для Седрика
    #                    hbox:
    #                        yalign 0.0
    #                        xalign 0.5
    #                        spacing 5
    #                        xoffset -60 #yoffset -40
    #
    #                        if store.pers_dict['Седрик'].current_mp <=  store.pers_dict['Седрик'].max_mp* 0.2:
    #                            text "{font=determination.otf}{size=40}[store.pers_dict['Седрик'].current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
    #                        elif store.pers_dict['Седрик'].current_mp > store.pers_dict['Седрик'].max_mp:
    #                            text "{font=determination.otf}{size=40}[store.pers_dict['Седрик'].current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_semigray
    #                        else:
    #                            text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Седрик'].current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style  "damagetext2" at damage_gradient_gray

    #                        fixed:
    #                            xysize (60, 8) xalign 1.0
    #                            fixed:
    #                                # Фон MP
    #                                hbox:
    #                                    spacing 3
    #                                    if store.pers_dict["Седрик"].current_mp > store.pers_dict["Седрик"].max_mp:
    #                                        # Если HP больше максимума, используем зеленый градиент
    #                                        for i in range(10):
    #                                            add Solid("#4fa6f8", xysize=(12, 22)) zoom 1.2 at damage_gradient_gray

    #                                    else:
    #                                        # Если MP меньше или равно максимуму, используем черный градиент
    #                                        for i in range(10):
    #                                            add "mppassive.png" zoom 1.2 at damage_gradient_black

                                # Заполнение MP
    #                            hbox:
    #                                spacing 3
    #                                # Проверяем условия для отображения MP
    #                                if store.pers_dict["Седрик"].current_mp > store.pers_dict["Седрик"].max_mp:
    #                                    $ mp_overmana_percent = (store.pers_dict["Седрик"].current_mp - store.pers_dict["Седрик"].max_mp) / store.pers_dict["Седрик"].max_mp * 100
    #                                    $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
    #
    #                                    # Если MP больше максимума, отображаем 10 иконок mpactive.png
    #                                    #for i in range(10):
    #                                    #    add "mpactive.png" zoom 1.2 at damage_gradient_cyan
    #                                    for i in range(overmana_icons2):
    #                                        add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray

    #                                elif store.pers_dict["Седрик"].current_mp > 0 and store.pers_dict["Седрик"].current_mp <= store.pers_dict["Седрик"].max_mp * 0.2:
    #                                    # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
    #                                    add "mpactive.png" zoom 1.2 at damage_gradient
    #                                else:
    #                                    # Обычное отображение MP
    #                                    $ mp_fill = int(math.ceil((store.pers_dict["Седрик"].current_mp / store.pers_dict["Седрик"].max_mp) * 10))
    #                                    for i in range(mp_fill):
    #                                        add "mpactive.png" zoom 1.2 at damage_gradient_gray

                        if (store.pers_dict["Седрик"].bloodshed_debuff != 0 or store.pers_dict["Седрик"].prone_debuff != 0 or
                            store.pers_dict["Седрик"].atk != (store.pers_dict["Седрик"].base_atk + store.pers_dict["Седрик"].base_atk_mod) or
                            store.pers_dict["Седрик"].defense != (store.pers_dict["Седрик"].base_def + store.pers_dict["Седрик"].base_def_mod) or
                            store.pers_dict["Седрик"].bonus_tank != 0 or
                            store.pers_dict["Седрик"].dmgchance != (store.pers_dict["Седрик"].base_dmgchance + store.pers_dict["Седрик"].dmgchance_mod) or
                            store.pers_dict["Седрик"].critrate != (store.pers_dict["Седрик"].base_critrate + store.pers_dict["Седрик"].critrate_mod) or
                            store.pers_dict["Седрик"].crit != (store.pers_dict["Седрик"].base_crit + store.pers_dict["Седрик"].crit_mod)):
                            # Отображение эффектов (дебафов/бафов) для Седрика
                            grid 5 2:
                                xalign 0.5
                                spacing 5
                                xoffset 0 yoffset -15
                                
                                #oверхил

                                # Кровотечение
                                if store.pers_dict["Седрик"].bloodshed_debuff != 0:
                                    if store.pers_dict["Седрик"].bloodshed_debuff > 0:
                                        add "bloodshed.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Седрик"].bloodshed_debuff < 0:
                                        add "healing.png" size (40, 40) at damage_gradient_green
                                
                                # Prone
                                if store.pers_dict["Седрик"].prone_debuff != 0:
                                    if store.pers_dict["Седрик"].prone_debuff > 0:
                                        add "prone.png" size (40, 40) at damage_gradient
                                    elif store.pers_dict["Седрик"].prone_debuff < 0:
                                        add "antiprone.png" size (40, 40) at damage_gradient_green
                                
                                # Остальные дебафы
                                if store.pers_dict["Седрик"].atk != (store.pers_dict["Седрик"].base_atk + store.pers_dict["Седрик"].base_atk_mod):
                                    if store.pers_dict["Седрик"].atk > (store.pers_dict["Седрик"].base_atk + store.pers_dict["Седрик"].base_atk_mod):
                                        add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].atk < (store.pers_dict["Седрик"].base_atk + store.pers_dict["Седрик"].base_atk_mod):
                                        add "atk_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Седрик"].defense != (store.pers_dict["Седрик"].base_def + store.pers_dict["Седрик"].base_def_mod):
                                    if store.pers_dict["Седрик"].defense > (store.pers_dict["Седрик"].base_def + store.pers_dict["Седрик"].base_def_mod):
                                        add "def_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].defense < (store.pers_dict["Седрик"].base_def + store.pers_dict["Седрик"].base_def_mod):
                                        add "def_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Седрик"].bonus_tank != 0:
                                    if store.pers_dict["Седрик"].bonus_tank > 0:
                                        add "tank_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].bonus_tank < 0:
                                        add "tank_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Седрик"].dmgchance != (store.pers_dict["Седрик"].base_dmgchance + store.pers_dict["Седрик"].dmgchance_mod):
                                    if store.pers_dict["Седрик"].dmgchance > 1:
                                        add "dmgchance_overchance.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].dmgchance > (store.pers_dict["Седрик"].base_dmgchance + store.pers_dict["Седрик"].dmgchance_mod):
                                        add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].dmgchance < (store.pers_dict["Седрик"].base_dmgchance + store.pers_dict["Седрик"].dmgchance_mod):
                                        add "dmgchance_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Седрик"].critrate != (store.pers_dict["Седрик"].base_critrate + store.pers_dict["Седрик"].critrate_mod):
                                    if store.pers_dict["Седрик"].critrate > 1:
                                        add "critrate_overcrit.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].critrate > (store.pers_dict["Седрик"].base_critrate + store.pers_dict["Седрик"].critrate_mod):
                                        add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].critrate < (store.pers_dict["Седрик"].base_critrate + store.pers_dict["Седрик"].critrate_mod):
                                        add "critrate_red_icon.png" size (40, 40) at damage_gradient
                                
                                if store.pers_dict["Седрик"].crit != (store.pers_dict["Седрик"].base_crit + store.pers_dict["Седрик"].crit_mod):
                                    if store.pers_dict["Седрик"].crit > (store.pers_dict["Седрик"].base_crit + store.pers_dict["Седрик"].crit_mod):
                                        add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                                    elif store.pers_dict["Седрик"].crit < (store.pers_dict["Седрик"].base_crit + store.pers_dict["Седрик"].crit_mod):
                                        add "critdmg_red_icon.png" size (40, 40) at damage_gradient

                        hbox:
                            xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                            add "[store.pers_dict['Седрик'].nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2 #at Kris_state_dependent_dynamic
                            text"{font=determination.otf}{size=50}[store.pers_dict['Седрик'].name]":
                                yalign 0.5 yoffset -5  #at Kris_state_dependent_dynamic

                        
                        if available_chars == 0:
                            pass
                        else:

                            if chardespos == 0:
                                imagebutton:
                                    yoffset -5 + yoffset_for_Sedric_desc
                                    at dynammic_alpha
                                    idle "summondesc2.png"
                                    hover "summondesc2.png"
                                    hovered [SetVariable("chardesprepare", store.pers_dict["Седрик"]), Show("fullstats0")]
                                    unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                                    action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), SetVariable("chardes", store.pers_dict["Седрик"]), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", "Седрикнажат"), Show ("fullstats1")]
                            
                            elif chardespos == "Седрикнажат":
                                imagebutton:
                                    yoffset -5 + yoffset_for_Sedric_desc
                                    at alpha_mig
                                    idle "summondesc.png"
                                    hover "summondesc.png"
                                    action NullAction()




                        

    # ========================================================================
    # АРЧИ
    # ========================================================================
    if store.pers_dict["Арчи"].picked == 1:

        hbox: # каждого отдельного персонажа
            spacing 0

            at herotochoose

            $ yoffset_for_Archie_desc = 0

            vbox:
                spacing 10
                frame:
                    yalign 0.0
                    padding (0, 0)
                    xmargin 0
                    ymargin 0
                    background None
                    # Кнопка для Арчи
                    vbox:
                        if store.pers_dict["Арчи"].picked == 1:
                            vbox:

                                spacing 10

                                if (store.pers_dict["Арчи"].bloodshed_debuff != 0 or store.pers_dict["Арчи"].prone_debuff != 0 or
                                    store.pers_dict["Арчи"].atk != (store.pers_dict["Арчи"].base_atk + store.pers_dict["Арчи"].base_atk_mod) or
                                    store.pers_dict["Арчи"].defense != (store.pers_dict["Арчи"].base_def + store.pers_dict["Арчи"].base_def_mod) or
                                    store.pers_dict["Арчи"].bonus_tank != 0 or
                                    store.pers_dict["Арчи"].dmgchance != (store.pers_dict["Арчи"].base_dmgchance + store.pers_dict["Арчи"].dmgchance_mod) or
                                    store.pers_dict["Арчи"].critrate != (store.pers_dict["Арчи"].base_critrate + store.pers_dict["Арчи"].critrate_mod) or
                                    store.pers_dict["Арчи"].crit != (store.pers_dict["Арчи"].base_crit + store.pers_dict["Арчи"].crit_mod)):

                                    $ yoffset_for_vbox = 0
                                    $ yoffset_for_vbox_name = 0
                                    $ yoffset_for_Archie_desc = -50

                                    if store.pers_dict["Арчи"].current_hp > 0 and store.pers_dict["Арчи"].turn == 1 and store.pers_dict["Арчи"].prone_debuff == 0:

                                        imagebutton:
                                            idle "longchooseArchie.png"
                                            hover "longchooseArchie.png"
                                            action [SetVariable("current_attacker", 8), Function(lambda: setattr(store.pers_dict['Арчи'], 'step_forward', 1)), Jump("playerturn2")]
                                            at choosedynamic
                                    else:
                                        imagebutton:
                                            idle "longchooseArchie.png"
                                            hover "longchooseArchie.png"
                                            action NullAction()
                                else:

                                    $ yoffset_for_vbox = 35
                                    $ yoffset_for_vbox_name = 50

                                    if store.pers_dict["Арчи"].current_hp > 0 and store.pers_dict["Арчи"].turn == 1 and store.pers_dict["Арчи"].prone_debuff == 0:

                                        imagebutton:
                                            idle "longchooseArchie.png"
                                            hover "longchooseArchie.png"
                                            action [SetVariable("current_attacker", 8), Function(lambda: setattr(store.pers_dict['Арчи'], 'step_forward', 1)), Jump("playerturn2")]
                                            at choosedynamic
                                    else:
                                        imagebutton:
                                            idle "longchooseArchie.png"
                                            hover "longchooseArchie.png"
                                            action NullAction()

                if store.pers_dict["Арчи"].current_hp == 0:
                    $ yoffset_for_dead = 2
                else:
                    $ yoffset_for_dead = 0

                vbox:
                    xalign 0.5 yalign -1.0
                    spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                    if store.pers_dict["Арчи"].shield == 0:
                        frame:
                            padding (0,0)
                            xmargin 0
                            ymargin 0
                            yoffset -5
                            xysize (70, 12)
                            background None
                            text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5
                    elif store.pers_dict["Арчи"].shield >= 1:
                        frame:
                            xoffset -90
                            xmargin 0
                            ymargin 0
                            xalign 0.5
                            yalign 0.0
                            xysize (70, 12)
                            background None
                            # Фон щита (всегда 4 позиции)
                            fixed:
                                hbox:
                                    xalign 0.0 yalign 1.0
                                    spacing 2
                                    for i in range(1, 5):
                                        add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                            # Заполнение щита (текущее значение)
                            fixed:
                                hbox:
                                    xalign 0.0 yalign 1.0
                                    spacing 2
                                    if store.pers_dict["Арчи"].shield >= 4:
                                        for i in range(1, 5):
                                            add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                    else:
                                        for i in range(1, min(store.pers_dict["Арчи"].shield + 1, 5)):
                                            add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                    # Отображение HP для Арчи
                    hbox:
                        xoffset -60
                        xalign 0.5 yalign 1
                        spacing 3

                        if store.pers_dict['Арчи'].current_hp <= store.pers_dict['Арчи'].max_hp * 0.2:
                            text "{font=determination.otf}{size=40}[store.pers_dict['Арчи'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                        elif store.pers_dict['Арчи'].current_hp > store.pers_dict['Арчи'].max_hp:
                            text "{font=determination.otf}{size=40}[store.pers_dict['Арчи'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_green_bright
                        else:
                            text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Арчи'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_gray

                    # Имя Арчи
                    text"{font=determination.otf}{size=50}[store.pers_dict['Арчи'].name]":
                        xalign 0.5
                        yoffset -5 + yoffset_for_Archie_desc

            # ============================================================
            # Кнопка Фабри (ID 10)
            # ============================================================
            # У Фабри нет активных атак: её ход — призыв фамильяров и их
            # магия. Кнопка выбора героя нужна обязательно, иначе Фабри
            # учитывается в available_chars, но выбрать её невозможно и
            # раунд зацикливается. Ассет images/longchooseFabri.png в
            # проекте уже присутствует.
            vbox:
                spacing 10
                frame:
                    yalign 0.0
                    padding (0, 0)
                    xmargin 0
                    ymargin 0
                    background None
                    vbox:
                        if store.pers_dict["Фабри"].picked == 1:
                            vbox:
                                spacing 10

                                if (store.pers_dict["Фабри"].bloodshed_debuff != 0 or store.pers_dict["Фабри"].prone_debuff != 0 or
                                    store.pers_dict["Фабри"].atk != (store.pers_dict["Фабри"].base_atk + store.pers_dict["Фабри"].base_atk_mod) or
                                    store.pers_dict["Фабри"].defense != (store.pers_dict["Фабри"].base_def + store.pers_dict["Фабри"].base_def_mod) or
                                    store.pers_dict["Фабри"].bonus_tank != 0 or
                                    store.pers_dict["Фабри"].dmgchance != (store.pers_dict["Фабри"].base_dmgchance + store.pers_dict["Фабри"].dmgchance_mod) or
                                    store.pers_dict["Фабри"].critrate != (store.pers_dict["Фабри"].base_critrate + store.pers_dict["Фабри"].critrate_mod) or
                                    store.pers_dict["Фабри"].crit != (store.pers_dict["Фабри"].base_crit + store.pers_dict["Фабри"].crit_mod)):

                                    $ yoffset_for_vbox = 0
                                    $ yoffset_for_vbox_name = 0
                                    $ yoffset_for_Fabri_desc = -50

                                    if store.pers_dict["Фабри"].current_hp > 0 and store.pers_dict["Фабри"].turn == 1 and store.pers_dict["Фабри"].prone_debuff == 0:
                                        imagebutton:
                                            idle "longchooseFabri.png"
                                            hover "longchooseFabri.png"
                                            action [SetVariable("current_attacker", 10), Function(lambda: setattr(store.pers_dict['Фабри'], 'step_forward', 1)), Jump("playerturn2")]
                                            at choosedynamic
                                    else:
                                        imagebutton:
                                            idle "longchooseFabri.png"
                                            hover "longchooseFabri.png"
                                            action NullAction()
                                else:

                                    $ yoffset_for_vbox = 35
                                    $ yoffset_for_vbox_name = 50

                                    if store.pers_dict["Фабри"].current_hp > 0 and store.pers_dict["Фабри"].turn == 1 and store.pers_dict["Фабри"].prone_debuff == 0:
                                        imagebutton:
                                            idle "longchooseFabri.png"
                                            hover "longchooseFabri.png"
                                            action [SetVariable("current_attacker", 10), Function(lambda: setattr(store.pers_dict['Фабри'], 'step_forward', 1)), Jump("playerturn2")]
                                            at choosedynamic
                                    else:
                                        imagebutton:
                                            idle "longchooseFabri.png"
                                            hover "longchooseFabri.png"
                                            action NullAction()

                if store.pers_dict["Фабри"].current_hp == 0:
                    $ yoffset_for_dead = 2
                else:
                    $ yoffset_for_dead = 0

                vbox:
                    xalign 0.5 yalign -1.0
                    spacing 0 yoffset -250 + yoffset_for_vbox + yoffset_for_dead

                    if store.pers_dict["Фабри"].shield == 0:
                        frame:
                            padding (0,0)
                            xmargin 0
                            ymargin 0
                            yoffset -5
                            xysize (70, 12)
                            background None
                            text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5
                    elif store.pers_dict["Фабри"].shield >= 1:
                        frame:
                            xoffset -90
                            xmargin 0
                            ymargin 0
                            xalign 0.5
                            yalign 0.0
                            xysize (70, 12)
                            background None
                            fixed:
                                hbox:
                                    xalign 0.0 yalign 1.0
                                    spacing 2
                                    for i in range(1, 5):
                                        add Solid("#27250d", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                            fixed:
                                hbox:
                                    xalign 0.0 yalign 1.0
                                    spacing 2
                                    if store.pers_dict["Фабри"].shield >= 4:
                                        for i in range(1, 5):
                                            add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                    else:
                                        for i in range(1, min(store.pers_dict["Фабри"].shield + 1, 5)):
                                            add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray

                    # Отображение HP для Фабри
                    hbox:
                        xoffset -60
                        xalign 0.5 yalign 1
                        spacing 3

                        if store.pers_dict['Фабри'].current_hp <= store.pers_dict['Фабри'].max_hp * 0.2:
                            text "{font=determination.otf}{size=40}[store.pers_dict['Фабри'].current_hp]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                        elif store.pers_dict['Фабри'].current_hp > store.pers_dict['Фабри'].max_hp:
                            text "{font=determination.otf}{size=40}[store.pers_dict['Фабри'].current_hp]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_green_bright
                        else:
                            text "{font=determination.otf}{size=40}{color=#ffffff}[store.pers_dict['Фабри'].current_hp]{/color}{/font}{/size}" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_gray

                    # Имя Фабри
                    text"{font=determination.otf}{size=50}[store.pers_dict['Фабри'].name]":
                        xalign 0.5
                        yoffset -5 + yoffset_for_Fabri_desc

    # Эмили (ID 11). Минимальная карточка использует текстовую кнопку, чтобы
    # персонаж был доступен даже без отдельного спрайта.
    if store.pers_dict.get("Эмили") is not None:
        vbox:
            spacing 4
            textbutton "Эмили":
                action [SetVariable("current_attacker", 11), Function(lambda: setattr(store.pers_dict['Эмили'], 'step_forward', 1)), Jump("playerturn2")]
                sensitive (store.pers_dict["Эмили"].picked == 1 and store.pers_dict["Эмили"].current_hp > 0 and store.pers_dict["Эмили"].turn == 1 and store.pers_dict["Эмили"].prone_debuff == 0)

    if store.pers_dict.get("Сьюзи") is not None:
        textbutton "Сьюзи":
            action [SetVariable("current_attacker", 12), Function(lambda: setattr(store.pers_dict['Сьюзи'], 'step_forward', 1)), Jump("playerturn2")]
            sensitive (store.pers_dict["Сьюзи"].picked == 1 and store.pers_dict["Сьюзи"].current_hp > 0 and store.pers_dict["Сьюзи"].turn == 1 and store.pers_dict["Сьюзи"].prone_debuff == 0)

    # Персонажи из новой спецификации. Текстовые карточки не требуют
    # дополнительных спрайтов и используют тот же путь playerturn2.
    for _new_id, _new_name in ((13, "Ральзей"), (14, "Ноэлль"), (15, "Санс"), (16, "Бердли")):
        if store.pers_dict.get(_new_name) is not None:
            textbutton _new_name:
                action [SetVariable("current_attacker", _new_id), Function(lambda n=_new_name: setattr(store.pers_dict[n], 'step_forward', 1)), Jump("playerturn2")]
                sensitive (store.pers_dict[_new_name].picked == 1 and store.pers_dict[_new_name].current_hp > 0 and store.pers_dict[_new_name].turn == 1 and store.pers_dict[_new_name].prone_debuff == 0)

    # Если нет доступных персонажей, переходим к атаке врагов
    if available_chars == 0:
        #timer 0.0001 action Show("Unclickable")
    
        
        


        frame:
            at plashka_transfrom
            background "#ffffff" 
            padding (5,5)
            xsize 1270
            frame:
                xalign 0.5 yalign 0.5 background "#000000" xsize 1260
                text "{size=50}{font=determination.otf}[timer_to_hide_chars]" xalign 0.5
        timer 0.7 action SetVariable("timer_to_hide_chars", timer_to_hide_chars-1) repeat 3
        timer 2.2 action [Hide("choose_attacker_screen"), Jump("enemyattacklabel"),  SetVariable("timer_to_hide_chars", 3)]



        
    text "{size=40}{font=determination.otf}{color=#ffffff}Раунд [store.current_round]{/color}{/font}{/size}" xalign 0.5 yalign 0.9 


screen Unclickable:

    timer 2.5 action Hide("Unclickable")
    zorder 99999
    imagebutton:
        at alpha03 xpos 0 ypos 0
        idle "semiblackbg.png"
        hover "semiblacbg.png"
        action NullAction()#Function(renpy.play("spongebob.mp3"))


transform alpha03:
    on show:
        alpha 0
    on hide:
        alpha 0
        easein 2 alpha 0


transform plashka_transfrom:
    on show:
        xalign 0.5 ypos 820
        easein 0.5 xalign 0.5 yalign 0.95
    on hide:
        xalign 0.5 yalign 0.95
        easein 0.5 xalign 0.5 ypos 820

default showblood = 0

default timer_to_hide_chars = 3

label enemyattacklabel:
    $ current_attacker = None
    $reset_heroes_feedness_step()
    $apply_debuffs_at_round_end()
    $apply_debuffs_at_round_end_enemies()
    $new_character_round_end_effects()
    # «Клинки хаоса»: отложенные огоньки бьют в начале хода противника.
    $ azri_delayed_blades()

    # Сильвия: тик длительных командных баффов «Крылья птицы» (x3),
    # «Пламя Амура» (x4) и точности x4 — уменьшение счётчиков за раунд.
    $ sylvia_tick_team_effects()

    $ renpy.show_screen("heroes_attacked_visual")
    $ renpy.pause(2.0,hard=True)

    # проверка, есть ли у кого-то из героев или врагов хп и мана реген

    if check_any_regen():
        $ store.apply_hp_and_mana_regen()
        $ renpy.show_screen("heroes_attacked_visual")
        $ renpy.pause(2.0,hard=True)

    show screen enemybgappears

    #поставь здесь стилькурсора Null
    $ default_mouse = "default2"
    $ renpy.set_mouse_pos(screenxpos+0.5*xbord-10, screenypos+0.5*ybord-10, duration = 1)




    $ renpy.pause (1.0, hard = True)
    #$ default_mouse = "Null"
    $ default_mouse = "default2"
    jump enemy_turn


transform enemybgappears_trans:
    on show:
        xalign 0.50 yalign 0.515 xysize (0,0) yoffset -40
        easein 1 rotate -270 xsize (xbord+20) ysize(ybord+20) yoffset 0
    on hide:
        xsize (xbord+20) ysize(ybord+20) xalign 0.50 yalign 0.515 yoffset 0
        easeout 1 rotate -540 xysize (0,0) yoffset 40

transform enemybgappears_trans2:
    on show:
        xalign 0.5 yalign 0.515 xsize (xbord+20) ysize(ybord+20)
        easein 1 rotate -270 xsize (xbord) ysize(ybord)

screen enemybgappears:
    on "show" action Hide ("turntarget")

    frame:
        if store.box_style == "shield":
            at savedspace_colour_yellow
        elif store.box_style == "damaged":
            at savedspace_colour
        at enemybgappears_trans
        background "#ffffff"
        padding (5,5)
        frame:
            
            background "#000000"
            padding (5,5)
    #timer 3 action Hide("enemybgappears")
