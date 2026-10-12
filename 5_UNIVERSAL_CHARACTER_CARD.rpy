# Универсальная карточка персонажа для экрана выбора

# Экран универсальной карточки персонажа
screen choose_attacker_screen2(char):
    zorder 10

    timer 0.01 action SetVariable("timer_to_hide_chars", 3)

    $ is_available = (char.picked == 1 and char.current_hp > 0 and char.turn == 1 and char.prone_debuff == 0)
    
    # Считаем количество доступных персонажей
    $ available_chars = 0
    $ available_chars += 1 if (store.pers_dict["Крис"].picked == 1 and store.pers_dict["Крис"].current_hp > 0 and store.pers_dict["Крис"].turn == 1 and store.pers_dict["Крис"].prone_debuff == 0) else 0
    $ available_chars += 1 if (store.pers_dict["Азриель"].picked == 1 and store.pers_dict["Азриель"].current_hp > 0 and store.pers_dict["Азриель"].turn == 1) else 0
    $ available_chars += 1 if (store.pers_dict["Чара"].picked == 1 and store.pers_dict["Чара"].current_hp > 0 and store.pers_dict["Чара"].turn == 1) else 0
    $ available_chars += 1 if (store.pers_dict["Фриск"].picked == 1 and store.pers_dict["Фриск"].current_hp > 0 and store.pers_dict["Фриск"].turn == 1) else 0
    $ available_chars += 1 if (store.pers_dict["Седрик"].picked == 1 and store.pers_dict["Седрик"].current_hp > 0 and store.pers_dict["Седрик"].turn == 1) else 0
    $ available_chars += 1 if (store.pers_dict["Кловер"].picked == 1 and store.pers_dict["Кловер"].current_hp > 0 and store.pers_dict["Кловер"].turn == 1) else 0
    $ available_chars += 1 if (store.pers_dict["Иззи"].picked == 1 and store.pers_dict["Иззи"].current_hp > 0 and store.pers_dict["Иззи"].turn == 1) else 0
    $ available_chars += 1 if (store.pers_dict["Сильвия"].picked == 1 and store.pers_dict["Сильвия"].current_hp > 0 and store.pers_dict["Сильвия"].turn == 1) else 0
    
    # Вычисляем смещения для различных элементов
    $ has_debuffs = (char.bloodshed_debuff != 0 or char.prone_debuff != 0 or
                    char.atk != (char.base_atk + char.base_atk_mod) or
                    char.defense != (char.base_def + char.base_def_mod) or
                    (hasattr(char, 'magic') and char.magic != (char.base_magic + char.base_magic_mod)) or
                    char.dmgchance != (char.base_dmgchance + char.dmgchance_mod) or
                    char.critrate != (char.base_critrate + char.critrate_mod) or
                    char.crit != (char.base_crit + char.crit_mod))
    
    $ yoffset_for_vbox = 0 if has_debuffs else 35
    $ yoffset_for_vbox_name = 0 if has_debuffs else 50
    $ yoffset_for_desc = -50 if has_debuffs else 0
    
    # Определяем трансформацию для персонажа
    #$ card_transform = herotochoose if char.char_type == 1 else monstertochoose
    
    hbox:
        spacing 0 xalign 0.5
        #at herotochoose
        
        vbox:
            spacing 10
            frame:
                yalign 0.0
                padding (0, 0)
                xmargin 0
                ymargin 0
                background None
                
                # Кнопка персонажа
                vbox:
                    spacing 10
                    
                    # Кнопка изображения персонажа
                    if char.prone_debuff != 0:
                        imagebutton:
                            idle f"[char.nameeng]choose.png"
                            hover f"[char.nameeng]choose.png"
                            action Show("please_choose_target")
                            at choosestatic
                    elif is_available:
                        imagebutton:
                            idle f"[char.nameeng]choose.png"
                            hover f"[char.nameeng]choose.png"
                            action [SetVariable("current_attacker_obj", char),
                                    Function(lambda: setattr(char, 'step_forward', 1)),
                                    Jump("playerturn2")]
                            at choosedynamic
                    else:
                        imagebutton:
                            idle f"[char.nameeng]choose.png"
                            hover f"[char.nameeng]choose.png"
                            action Show("please_choose_target")
                            at choosestatic
            
            # Информационная панель персонажа
            vbox:
                xalign 0.5 yalign -1.0 
                spacing 0 yoffset -250 + yoffset_for_vbox
                
                # Отображение щита
                if char.shield == 0:
                    frame:
                        padding (0,0)
                        xmargin 0
                        ymargin 0
                        yoffset -5
                        xysize (70, 12)
                        background None 
                        text "{color=#000000}а {/color}" size 10 xalign 0.5 yalign 0.5 
                else:
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
                                if char.shield >= 4:
                                    # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                    for i in range(1, 5):
                                        add Solid("#ffea00", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                else:
                                    # Иначе отображаем обычное заполнение
                                    for i in range(1, min(char.shield + 1, 5)):
                                        add Solid("#e1d22e", xysize=(57, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray
                
                # Отображение HP
                hbox:
                    xoffset -60
                    xalign 0.5 yalign 1
                    spacing 3
                    
                    if char.current_hp <= char.max_hp * 0.2:
                        text "{font=determination.otf}{size=40}[int(char.current_hp)]{/font}{/size}" color "#ff0000" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_for_lowhp
                    elif char.current_hp > char.max_hp:
                        text "{font=determination.otf}{size=40}[int(char.current_hp)]{/font}{/size}" color "#ffffff" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_green_bright
                    else:
                        text "{font=determination.otf}{size=40}{color=#ffffff}[int(char.current_hp)]{/color}{/font}{/size}" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_gray
                    
                    # Полоска HP
                    fixed:
                        xysize (60, 8) xalign 1.0
                        # Фон HP
                        hbox:
                            spacing 3
                            if char.current_hp > char.max_hp:
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
                            if char.current_hp > char.max_hp:
                                # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                $ hp_overheal_percent = (char.current_hp - char.max_hp) / char.max_hp * 100
                                $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))
                                for i in range(overheal_icons):
                                    add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                            elif char.current_hp > 0 and char.current_hp <= char.max_hp * 0.2:
                                # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                $ low_fill = int(math.ceil((char.current_hp / char.max_hp) * 10))
                                for i in range(low_fill):
                                    add "hpactive.png" zoom 1.2 at damage_gradient_gray
                            else:
                                # Обычное отображение HP
                                $ hp_fill = int(math.ceil((char.current_hp / char.max_hp) * 10))
                                for i in range(hp_fill):
                                    add "hpactive.png" zoom 1.2 at damage_gradient_gray
                
                # Отображение MP (только для персонажей с максимальным MP > 0)
                # Исключаем Седрика, у которого нет маны
                if char.name != "Седрик":
                    hbox:
                        yalign 0.0
                        xalign 0.5
                        spacing 5
                        xoffset -60
                    
                        if char.current_mp <= char.max_mp * 0.2:
                            text "{font=determination.otf}{size=40}[char.current_mp]{/font}{/size}" color "#ffffffc2" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_black
                        elif char.current_mp > char.max_mp:
                            text "{font=determination.otf}{size=40}[char.current_mp]{/font}{/size}" color "#3adeff" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_semigray
                        else:
                            text "{font=determination.otf}{size=40}{color=#ffffff}[char.current_mp]{/color}{/font}{/size}" min_width 60 yoffset -11 style "damagetext2" at damage_gradient_gray
                        
                        fixed:
                            xysize (60, 8) xalign 1.0
                            fixed:
                                # Фон MP
                                hbox:
                                    spacing 3
                                    if char.current_mp > char.max_mp:
                                        # Если MP больше максимума, используем зеленый градиент
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
                                    if char.current_mp > char.max_mp:
                                        $ mp_overmana_percent = (char.current_mp - char.max_mp) / char.max_mp * 100
                                        $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))
                                        for i in range(overmana_icons2):
                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray
                                    elif char.current_mp > 0 and char.current_mp <= char.max_mp * 0.2:
                                        # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                        $ low_fill = get_display_mp_fill(char)
                                        for i in range(low_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient
                                    else:
                                        # Обычное отображение MP
                                        $ mp_fill = get_display_mp_fill(char)
                                        for i in range(mp_fill):
                                            add "mpactive.png" zoom 1.2 at damage_gradient_gray
                
                # Отображение дебафов
                if has_debuffs:
                    grid 5 2:
                        xalign 0.5
                        spacing 5
                        xoffset 0 yoffset -15
                        
                        # Кровотечение
                        if char.bloodshed_debuff != 0:
                            if char.bloodshed_debuff > 0:
                                add "bloodshed_debuff_red.png" size (40, 40)
                            elif char.bloodshed_debuff < 0:
                                add "bloodshed_debuff_green.png" size (40, 40)
                        
                        # Prone
                        if char.prone_debuff != 0:
                            if char.prone_debuff > 0:
                                add "prone_debuff_red.png" size (40, 40)
                            elif char.prone_debuff < 0:
                                add "prone_debuff_red.png" size (40, 40)
                        
                        # Атака
                        if char.atk != (char.base_atk + char.base_atk_mod):
                            if char.atk > (char.base_atk + char.base_atk_mod):
                                add "atk_green_icon.png" size (40, 40) at damage_gradient_green
                            elif char.atk < (char.base_atk + char.base_atk_mod):
                                add "atk_red_icon.png" size (40, 40) at damage_gradient
                        
                        # Защита
                        if char.defense != (char.base_def + char.base_def_mod):
                            if char.defense > (char.base_def + char.base_def_mod):
                                add "def_green_icon.png" size (40, 40) at damage_gradient_green
                            elif char.defense < (char.base_def + char.base_def_mod):
                                add "def_red_icon.png" size (40, 40) at damage_gradient
                        


                        # Магия (только для персонажей с магией)
                        # Исключаем Криса, Чару и Фриска, у которых нет параметра магии
                        if char.name not in ["Крис", "Чара", "Фриск"] and char.magic != (char.base_magic + char.base_magic_mod):
                            if char.magic > (char.base_magic + char.base_magic_mod):
                                add "mag_green_icon.png" size (40, 40) at damage_gradient_green
                            elif char.magic < (char.base_magic + char.base_magic_mod):
                                add "mag_red_icon.png" size (40, 40) at damage_gradient
                        
                        # Точность
                        if char.dmgchance != (char.base_dmgchance + char.dmgchance_mod):
                            if char.dmgchance > (char.base_dmgchance + char.dmgchance_mod):
                                add "dmgchance_green_icon.png" size (40, 40) at damage_gradient_green
                            elif char.dmgchance < (char.base_dmgchance + char.dmgchance_mod):
                                add "dmgchance_red_icon.png" size (40, 40)
                        
                        # Шанс крита
                        if char.critrate != (char.base_critrate + char.critrate_mod):
                            if char.critrate > (char.base_critrate + char.critrate_mod):
                                add "critrate_green_icon.png" size (40, 40) at damage_gradient_green
                            elif char.critrate < (char.base_critrate + char.critrate_mod):
                                add "critrate_red_icon.png" size (40, 40) at damage_gradient
                        
                        # Критический урон
                        if char.crit != (char.base_crit + char.crit_mod):
                            if char.crit > (char.base_crit + char.crit_mod):
                                add "critdmg_green_icon.png" size (40, 40) at damage_gradient_green
                            elif char.crit < (char.base_crit + char.crit_mod):
                                add "critdmg_red_icon.png" size (40, 40) at damage_gradient
                
                # Имя персонажа
                hbox:
                    xalign 0.4 spacing 10 yoffset 0 + yoffset_for_vbox_name
                    add "[char.nameeng]soul.png" size (25,25) yalign 0.5 yoffset -2
                    text"{font=determination.otf}{size=50}[char.name]":
                        yalign 0.5 yoffset -5
                
                # Кнопка описания персонажа
                if available_chars == 0:
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

                else:
                    $ char_pos_name = "[char.name]нажат"
                    
                    if chardespos == 0:

                        imagebutton:
                            yoffset -5 + yoffset_for_desc
                            at dynammic_alpha  
                            idle "summondesc2.png"
                            hover "summondesc2.png"
                            hovered [SetVariable("chardesprepare", char), Show("fullstats0")]
                            unhovered [SetVariable("bottom_x_shown", 0), Hide("fullstats1"), Hide("fullstats0")]
                            action [SetVariable("bottom_x_shown", 1), SetVariable("screenstate", "доступен"), 
                                    SetVariable("chardes", char), SetVariable("sscreenstate_style", "статический"), 
                                    SetVariable("chardespos", char_pos_name), Show ("fullstats1")]

                    
                    elif chardespos == char_pos_name:
                        imagebutton:
                            yoffset -5 + yoffset_for_desc
                            at alpha_mig
                            idle "summondesc.png"
                            hover "summondesc.png"
                            action NullAction()    # Если нет доступных персонажей, переходим к атаке врагов

        
        
    text "{size=40}{font=determination.otf}{color=#ffffff}Раунд [current_round]{/color}{/font}{/size}" xalign 0.5 yalign 0.9
