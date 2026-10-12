default chardespos = 0

default chardes = getattr(store, "pers_dict", None)["Крис"] if getattr(store, "pers_dict", None) and "Крис" in getattr(store, "pers_dict", None) else None # для кнопок
default chardesprepare =  getattr(store, "pers_dict", None)["Крис"] if getattr(store, "pers_dict", None) and "Крис" in getattr(store, "pers_dict", None) else None # для кнопок

default screenstate = "недоступен" ## Доступен 1 -недоступен 0
default sscreenstate_style = 0 ## Динамический 0 -статический 1
default fullstats1_page = "combat"

init python:
    FULLSTATS_DEBUFF_NAMES = (
        "bloodshed_debuff",
        "prone_debuff",
        "atk_debuff",
        "def_debuff",
        "magic_debuff",
        "accuracy_debuff",
        "critrate_debuff",
        "critdmg_debuff",
        "tank_debuff",
    )

    def fullstats_has_any_debuff(char):
        if char is None:
            return False
        return any(getattr(char, debuff_name, 0) != 0 for debuff_name in FULLSTATS_DEBUFF_NAMES)

    def fullstats_bonus_text_layout(char):
        if fullstats_has_any_debuff(char):
            if getattr(char, "name", None) == "Фриск":
                return 40, 81, -25
            return 40, 51, -25
        return 45, 51, -5

    def fullstats_should_show_magic(char):
        if char is None:
            return False

        current_magic = float(getattr(char, "magic", 0) or 0)
        base_magic = float((getattr(char, "base_magic", 0) or 0) + (getattr(char, "base_magic_mod", 0) or 0))
        bonus_magic = float(getattr(char, "bonus_magic", 1) or 1)
        return not (abs(current_magic) < 0.0001 and abs(base_magic) < 0.0001 and abs(bonus_magic - 1.0) < 0.0001)

    def fullstats_magic_state(char):
        if not fullstats_should_show_magic(char):
            return 0

        current_magic = float(getattr(char, "magic", 0) or 0)
        base_magic = float((getattr(char, "base_magic", 0) or 0) + (getattr(char, "base_magic_mod", 0) or 0))
        if current_magic < base_magic:
            return -1
        if current_magic > base_magic:
            return 1
        return 0

    def fullstats_magic_bonus_text(char):
        if not fullstats_should_show_magic(char):
            return "0%"

        current_magic = float(getattr(char, "magic", 0) or 0)
        base_magic = float((getattr(char, "base_magic", 0) or 0) + (getattr(char, "base_magic_mod", 0) or 0))
        if abs(base_magic) > 0.0001:
            delta_percent = int(round(((current_magic - base_magic) / abs(base_magic)) * 100))
        else:
            delta_percent = int(round((float(getattr(char, "bonus_magic", 1) or 1) - 1.0) * 100))
        return "{}%".format(delta_percent)

    class FeednessQueueBar(renpy.Displayable):
        def __init__(self, char, width=100, height=12, gap=10, empty_color="#111111"):
            super(FeednessQueueBar, self).__init__()
            self.char = char
            self.width = width
            self.height = height
            self.gap = gap
            self.empty_color = empty_color

        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            canvas = render.canvas()

            queue = get_feedness_queue(self.char)
            total = len(queue)
            if total <= 0:
                return render

            total_gap = self.gap * max(0, total - 1)
            usable_width = max(1, self.width - total_gap)
            segment_width = max(1, usable_width // total)
            remainder = max(0, usable_width - (segment_width * total))

            x = 0
            for i, food_type in enumerate(queue):
                current_width = segment_width + (1 if i < remainder else 0)
                color = pygame.Color(store.feedness_type_colors.get(food_type, self.empty_color) if food_type is not None else self.empty_color)
                points = [
                    (x, 0),
                    (x + current_width - 1, 0),
                    (x + current_width - 1, self.height - 1),
                    (x, self.height - 1),
                ]
                canvas.polygon(color, points)
                x += current_width + self.gap

            return render

transform semiblack_dynamic_alpha:
    on show:
        alpha 0.0 
        easein 1.0 alpha 1.0
    on hide:
        alpha 1.0 
        easeout 1.0 alpha 0.0

transform semiblack_alpha_0:
    alpha 0.0







transform fullstats1_1:
    xpos 1300


transform fullstats1_2:
    on show:
        xpos 1300 yalign 0.01 alpha 0.0  
        easein 0.5 alpha 1.0 xoffset -1245 #xpos 45 alpha 1.0

    on hide:
        alpha 1.0 yalign 0.01  
        easeout 0.5 xoffset 0 yalign 0.01 alpha 0.0





screen fullstats0:
    zorder 99999


    if chardespos in ["Криснажат", "Азриельнажат", "Чаранажат", "Фрискнажат", "Иззинажат", "Кловернажат", "Седрикнажат", "Сильвиянажат"]:
        timer 0.01 action [Show("fullstats1"), SetVariable("screenstate", "доступен")]
        timer 0.01 action SetVariable("chardes", chardesprepare)

    else:
        timer 0.6 action [Show("fullstats1"), SetVariable("screenstate", "доступен")]
        timer 0.6 action SetVariable("chardes", chardesprepare)





# Экран для отображения персонажа
screen fullstats1():

    zorder 100

    $ fullstats_cache_key = "fullstats_%s" % (chardes.name if chardes and hasattr(chardes, "name") else "none")
    $ fullstats_hp_now = chardes.current_hp if chardes and hasattr(chardes, "current_hp") else 0
    $ fullstats_mp_now = chardes.current_mp if chardes and hasattr(chardes, "current_mp") else 0
    if renpy.has_label("itemchosen") and "get_hp_mp_bar_prev_values" in globals() and "commit_hp_mp_bar_values" in globals():
        timer 1.05 repeat False action Function(commit_hp_mp_bar_values, fullstats_cache_key, fullstats_hp_now, fullstats_mp_now)
        $ prev_hp_value, prev_mp_value = get_hp_mp_bar_prev_values(fullstats_cache_key, fullstats_hp_now, fullstats_mp_now)
    else:
        $ prev_hp_value, prev_mp_value = fullstats_hp_now, fullstats_mp_now

    


    if sscreenstate_style == "статический":    
        imagebutton:
            #at semiblack_dynamic_alpha
            xpos 0 ypos 0
            idle "semiblackbg2.png"
            hover "semiblackbg2.png"
            action NullAction()
    else:
        pass



        

    hbox:
   
        
        # Проверяем, является ли chardespos состоянием 1 для любого персонажа
        if screenstate == "недоступен":
            at fullstats1_1
        elif screenstate == "доступен":
        # Проверяем, является ли chardespos состоянием 2 или 3 для любого персонажа
            at fullstats1_2


        frame:
            yoffset 5     

            background "#ffffff"
            padding (5,5,5,5)
            xysize (1191,580)
            
            frame:
                xalign 0.5 yalign 0.5
                background "#000000"
                padding (5,5,5,5)
                xysize (1182,570)



                hbox: # НАЧАЛО ТАБЛИЦЫ
                    



                    # Первый столбик
                    vbox:

                        spacing 10 xalign 0.5

                        frame:
                        

                            background "#ffffff"
                            padding (4,4,4,4)
                            xysize (270,70)
                            
                            frame:
                                xalign 0.5 yalign 0.5
                                background "#000000"
                                xysize (264, 66)



                                hbox:
                                    xalign 0.4 yalign 0.5 spacing 10
                                    # Изображение души персонажа
                                    add ConditionSwitch(
                                        'chardes == store.pers_dict["Крис"]', "images/Krissoul.png",
                                        'chardes == store.pers_dict["Азриель"]', "images/Asrielsoul.png",
                                        'chardes == store.pers_dict["Чара"]', "images/Charasoul.png",
                                        'chardes == store.pers_dict["Фриск"]', "images/Frisksoul.png",
                                        'chardes == store.pers_dict["Иззи"]', "images/Izzysoul.png",
                                        'chardes == store.pers_dict["Кловер"]', "images/Cloversoul.png",
                                        'chardes == store.pers_dict["Седрик"]', "images/Sedricsoul.png",
                                        # Сильвия: собственного спрайта души пока нет,
                                        # используем имеющуюся иконку как заглушку,
                                        # чтобы карточка не оставалась пустой.
                                        'chardes == store.pers_dict["Сильвия"]', "images/Sedricsoul.png",
                                    ) xysize (40,40) xalign 0.5 yalign 0.5
                                    # Имя персонажа
                                    text "{size=50}{font=determination.otf}[chardes.name if hasattr(chardes, 'name') else '']" xalign 0.5 yalign 0.5 color "#ffffff" at damage_gradient_gray style "damage_text"
                            

                        # Портреты с условиями
                        add ConditionSwitch(
                            'chardes == store.pers_dict["Крис"]', "portraits/kris.png",
                            'chardes == store.pers_dict["Азриель"]', "portraits/asriel.png",
                            'chardes == store.pers_dict["Чара"]', "portraits/chara.png",
                            'chardes == store.pers_dict["Фриск"]', "portraits/frisk.png",
                            'chardes == store.pers_dict["Иззи"]', "portraits/izzy.png",
                            'chardes == store.pers_dict["Кловер"]', "portraits/clover.png",
                            'chardes == store.pers_dict["Седрик"]', "portraits/sedric.png",
                            'chardes == store.pers_dict["Седрик"]', "portraits/sedric.png",
                            'chardes == store.pers_dict["Фабри"]', "portraits/Fabri.png",
                        ) xsize 270 ysize 359
                                


                        vbox:

                            spacing 0




                            vbox:  # названия статов и картинки к ним
                                spacing 0 xalign 0.0
                                
                                # Отображение щита

                                frame:
                                    xoffset 10
                                    xmargin 0
                                    ymargin 0
                                    xalign 0.0
                                    yalign 0.0
                                    xysize (70, 12)
                                    background None

                                    # Фон щита (всегда 4 позиции)
                                    fixed:
                                        hbox:
                                            if chardes == store.pers_dict["Азриель"]:
                                                xoffset -10
                                            else:
                                                xoffset -10
                                            yalign 1.0
                                            spacing 2
                                            for i in range(1, 5):
                                                add Solid("#27250d", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                    # Заполнение щита (текущее значение)
                                    fixed:
                                    
                                        hbox:
                                            if chardes == store.pers_dict["Азриель"]:
                                                xoffset -10
                                            else:
                                                xoffset -10

                                            yalign 1.0
                                            spacing 2
                                            if chardes and chardes.shield >= 4:
                                                # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                                for i in range(1, 5):
                                                    add Solid("#ffea00", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                            else:
                                                # Иначе отображаем обычное заполнение
                                                for i in range(1, min((chardes.shield if chardes else 0) + 1, 5)):
                                                    add Solid("#e1d22e", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray
                                
                                
                                # здлолвье и хп
                                #vbox:
                                #    spacing 10                                    

                                hbox:  # текст значнеий
                                    xalign 0.0 spacing 10
                                        


                                    
                                    vbox:
                                        xalign 0.5

                                        if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):
                                            spacing 30
                                        elif chardes and ((chardes.current_hp > 1000 or chardes.max_hp > 1000) or (chardes.current_mp > 1000 or chardes.max_mp > 1000)):
                                            spacing 20
                                        else: 
                                            spacing 12

                                        # Определяем размер шрифта в зависимости от количества HP
                                        $ textsize1 = 30  # размер по умолчанию
                                        if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):
                                            $ textsize1 = 18
                                        elif chardes and ((chardes.current_hp > 1000 or chardes.max_hp > 1000) or (chardes.current_mp > 1000 or chardes.max_mp > 1000)):
                                            $ textsize1 = 24
                                        else:
                                            $ textsize1 = 30

                                        if chardes:
                                            if chardes.current_hp <= chardes.max_hp* 0.2:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#ff0000" at damage_gradient_for_lowhp style "damage_text"
                                            elif chardes.current_hp > chardes.max_hp:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#00ff00" at damage_gradient_green_bright style "damage_text"
                                            else:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#ffffff"  at damage_gradient_gray style "damage_text"
                                        else:
                                            text "{size=[textsize1]}{font=determination.otf}--/--{/font}" xalign 0.5 color "#ffffff" at damage_gradient_gray style "damage_text"

                                        
                                        

                                        if chardes == store.pers_dict["Седрик"]:
                                            pass
                                        else:
                                            if chardes:
                                                if chardes.current_mp <= chardes.max_mp* 0.2:
                                                    text "{size=[textsize1]}{font=determination.otf}[chardes.current_mp]/[chardes.max_mp]{/font}" color "#ffffffc2" xalign 0.5 min_width 60 yoffset -11 style "damagetext2 damage_text" at damage_gradient_black
                                                elif chardes.current_mp > chardes.max_mp:
                                                    text "{size=[textsize1]}{font=determination.otf}[chardes.current_mp]/[chardes.max_mp]{/font}" color "#3adeff" xalign 0.5 min_width 60 yoffset -11 style  "damagetext2 damage_text" at damage_gradient_semigray
                                                else:
                                                    text "{size=[textsize1]}{font=determination.otf}{color=#ffffff}[chardes.current_mp]/[chardes.max_mp]{/font}{/color}" xalign 0.5 min_width 60 yoffset -11 style  "damagetext2 damage_text" at damage_gradient_gray
                                            else:
                                                text "{size=[textsize1]}{font=determination.otf}{color=#ffffff}--/--{/font}{/color}" xalign 0.5 min_width 60 yoffset -11 style "damagetext2 damage_text" at damage_gradient_gray
                                            #text "/"
                                            #text "{font=determination.otf}[chardes.max_mp]{/font}"


                                
                                    vbox:
                                        spacing 10 xalign 0.0

                                        # Полоска HP
                                        fixed:
                                            #xysize (60, 8) 
                                            xalign 1.0
                                            # Фон HP
                                            hbox:
                                                spacing 3
                                                if chardes and chardes.current_hp > chardes.max_hp:
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
                                                if chardes and chardes.current_hp > chardes.max_hp:
                                                    # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                                    $ hp_overheal_percent = (chardes.current_hp - chardes.max_hp) / chardes.max_hp * 100
                                                    $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                                    for i in range(overheal_icons):
                                                        add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                                elif chardes and chardes.current_hp > 0 and chardes.current_hp <= chardes.max_hp * 0.2:
                                                    # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                                    $ low_fill = int(math.ceil((chardes.current_hp / chardes.max_hp) * 10))
                                                    for i in range(low_fill):
                                                        add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                                else:
                                                    # Обычное отображение HP
                                                    $ hp_fill = int(math.ceil((chardes.current_hp / chardes.max_hp) * 10))
                                                    for i in range(hp_fill):
                                                        add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    

                                        fixed:
                                            yoffset -80 + textsize1*0.3
                                            xysize (60, 10)
                                 
                                            # Фон MP
                                            hbox:
                                                spacing 3 
                                                if chardes and chardes.current_mp > chardes.max_mp:
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
                                                if chardes and chardes.current_mp > chardes.max_mp:
                                                    $ mp_overmana_percent = (chardes.current_mp - chardes.max_mp) / chardes.max_mp * 100
                                                    $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                                    if prev_mp_value > chardes.max_mp:
                                                        $ prev_mp_overmana_percent = (prev_mp_value - chardes.max_mp) / chardes.max_mp * 100
                                                        $ prev_overmana_icons2 = min(5, int(math.ceil(prev_mp_overmana_percent / 10.0)))
                                                    else:
                                                        $ prev_overmana_icons2 = 0
                                                    for i in range(10):
                                                        if i < overmana_icons2:
                                                            if i >= prev_overmana_icons2:
                                                                add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at [hp_mp_bar_app, damage_gradient_semigray]
                                                            else:
                                                                add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray
                                                        elif i < prev_overmana_icons2:
                                                            add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at hp_mp_bar_dis
                                                elif chardes and chardes.current_mp > 0 and chardes.current_mp <= chardes.max_mp * 0.2:
                                                    # Low-MP стиль действует до 20%, число ячеек округляется вверх.
                                                    $ mp_fill = get_display_mp_fill(chardes)
                                                    $ mp_fill = max(0, min(10, mp_fill))
                                                    $ prev_mp_fill_raw = int(math.ceil((prev_mp_value / chardes.max_mp) * 10)) if chardes.max_mp else 0
                                                    $ prev_mp_fill = max(0, min(10, prev_mp_fill_raw))
                                                    for i in range(10):
                                                        if i < mp_fill:
                                                            if i >= prev_mp_fill:
                                                                add "mpactive.png" zoom 1.2 at [hp_mp_bar_app, damage_gradient]
                                                            else:
                                                                add "mpactive.png" zoom 1.2 at damage_gradient
                                                        elif i < prev_mp_fill:
                                                            add "mpactive.png" zoom 1.2 at hp_mp_bar_dis
                                                else:
                                                    # Обычное отображение MP
                                                    $ mp_fill = get_display_mp_fill(chardes)
                                                    $ mp_fill = max(0, min(10, mp_fill))
                                                    $ prev_mp_fill_raw = int(math.ceil((prev_mp_value / chardes.max_mp) * 10)) if chardes.max_mp else 0
                                                    $ prev_mp_fill = max(0, min(10, prev_mp_fill_raw))
                                                    for i in range(10):
                                                        if i < mp_fill:
                                                            if i >= prev_mp_fill:
                                                                add "mpactive.png" zoom 1.2 at hp_mp_bar_app
                                                            else:
                                                                add "mpactive.png" zoom 1.2 at damage_gradient_gray
                                                        elif i < prev_mp_fill:
                                                            add "mpactive.png" zoom 1.2 at hp_mp_bar_dis

                        if chardes and hasattr(chardes, "max_feedness") and chardes.max_feedness > 0:
                            fixed:
                                yoffset -50
                                #yoffset -68 + textsize1*0.3
                                #xoffset -80 - textsize1*0.3
                                xalign 0.0
                                xysize (280, 12)
                                add FeednessQueueBar(chardes, width=280, height=12, gap=10)








































                    
                hbox:
                    
                    xalign 0.6 yalign 0.25 #spacing 30 

                    if (chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 
                        or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or chardes.critrate_debuff != 0
                        or chardes.critdmg_debuff != 0 or chardes.tank_debuff != 0):
                        spacing -10
                        $ multiply_for_text = 0.85
                        xoffset 40
                    else:
                        spacing 30
                        $ multiply_for_text = 0
                        xoffset 20
                    #if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):

                    ######################################### Индикаторы баффов дебаффорв
                    hbox:
                        
                        
                        xalign 0.0
                        vbox:
                            at alpha_to_1
                            xalign 0.0
                            if chardes != store.pers_dict["Крис"]:
                                # условия, есть ли у персонажа любой дебаф
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 12 yoffset 60 xoffset -10
                                else:
                                    spacing 8 xoffset 17 yoffset 65 
                            
                            else:                                
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 12 yoffset 60 xoffset -10
                                else:
                                    spacing 8 xoffset 17 yoffset 65 
                            

                            

                            #aтака

                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            else:
                                # Определение цвета иконки
                                if chardes and chardes.bonus_atk < 0:
                                    add "atk_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_atk == 0:
                                    add "atk_white_indi.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_atk > 0:
                                    add "atk_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                    


                            #Магия 


                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                # Определение цвета иконки
                                if chardes and chardes.bonus_magic < 0:
                                    add "mag_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_magic == 0:
                                    add "mag_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_magic > 0:
                                    add "mag_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                            # шанс попадания
                            # Определение цвета иконки

                            if chardes and chardes.dmgchance > 1:
                                add "dmgchance_overchance.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                            elif chardes and chardes.bonus_dmgchance < 0:
                                add "dmgchance_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_dmgchance == 0:
                                add "dmgchance_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_dmgchance > 0:
                                add "dmgchance_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                            # критшанс
                            # Определение цвета иконки
                            if chardes and chardes.critrate > 1:
                                add "critrate_overcrit.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                            elif chardes and chardes.bonus_critrate < 0:
                                add "critrate_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_critrate == 0:
                                add "critrate_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_critrate > 0:
                                add "critrate_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green



                            if chardes and chardes.bonus_crit < 0:
                                add "critdmg_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_crit == 0:
                                add "critdmg_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_crit > 0:
                                add "critdmg_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green



                            if chardes and chardes.bonus_def < 0:
                                add "def_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_def == 0:
                                add "def_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_def > 0:
                                add "def_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                            # Tank
                            # Определение цвета иконки
                            if chardes and chardes.bonus_tank < 0:
                                add "tank_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) 
                            elif chardes and chardes.bonus_tank == 0:
                                add "tank_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_tank > 0:
                                add "tank_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) 

                            # Отношения (только для Криса)
                            if chardes == store.pers_dict["Крис"]:
                                # Определение иконки в зависимости от значения reltns
                                vbox:
                                    xoffset -10 xalign 0.0
                                    if chardes and hasattr(chardes, 'reltns'):
                                        if chardes.reltns <= -80:
                                            add "awfulmax.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_for_lowhp2
                                        elif chardes.reltns <= -60:
                                            add "awful.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                        elif chardes.reltns <= -40:
                                            add "verybad.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                        elif chardes.reltns <= -20:
                                            add "bad.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                        elif chardes.reltns < 20:
                                            add "normal.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_yellow
                                        elif chardes.reltns < 40:
                                            add "good.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                        elif chardes.reltns < 60:
                                            add "verygood.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                        elif chardes.reltns < 80:
                                            add "excellent.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                        elif chardes.reltns == 100:
                                            add "excellentmax.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green_bright
                                        else:
                                            pass






                        vbox:
                            # Отображение всех bonus_характеристик в текстовом виде
                            at alpha_to_1
                            
                            
                            # условия, есть ли у персонажа любой дебаф
                            if chardes != store.pers_dict["Крис"]:
                                # условия, есть ли у персонажа любой дебаф
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 40 yoffset 45 xoffset -25
                                else:
                                    spacing 45 yoffset 50 xoffset 0
                            
                            else:                                
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 40 yoffset 15 xoffset -25
                                else:
                                    spacing 45 yoffset 17 xoffset 0

                            xalign 0.0 yalign 0.5 
                            
                            
                            # Атака
                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            else:
                                if chardes and chardes.bonus_atk < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_atk*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_atk == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_atk > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_atk*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Магия
                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                if chardes and chardes.bonus_magic < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_magic*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_magic == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_magic > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_magic*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Точность
                            if chardes and chardes.bonus_dmgchance < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_dmgchance*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_dmgchance == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_dmgchance > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_dmgchance*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Шанс крита
                            if chardes and chardes.bonus_critrate < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_critrate*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_critrate == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_critrate > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_critrate*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Критический урон
                            if chardes and chardes.bonus_crit < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_crit*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_crit == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_crit > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_crit*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Защита
                            if chardes and chardes.bonus_def < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_def*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_def == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_def > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_def*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Tank
                            if chardes and chardes.bonus_tank < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_tank == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_tank > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"






























                        ########################################           Название характеристики
                        vbox:
                            # атака
                            at alpha_to_1
                            xalign 0.0 spacing 22 yoffset -5 


                            text "{size=50}{font=determination.otf}Stats" yoffset 0 at damage_gradient_gray style "damage_text"

                                




                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            elif chardes == store.pers_dict["Фриск"]:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Legate's{/font}" style "damage_text"
                            
                            else:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Attack{/font}" xalign 0.0 at damage_gradient_gray style "damage_text" 
                            

                            # Мания
                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Magic{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"

                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Dmg.Chance%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Crit.Rate%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Crit.Dmg%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Defense{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Tank{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            
                            # Отношения (только для Криса)
                            if chardes == store.pers_dict["Крис"]:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Relations{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"






                        vbox: #############################          значение характеристики
                            spacing 22 yoffset -5 xoffset 30 xalign 1.0

                            text "{size=50}{font=determination.otf}Cur/Base" yoffset 0 at damage_gradient_gray style "damage_text"


                            # Атака
                            # Отображение текущего значения цветом
                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            elif chardes == store.pers_dict["Фриск"]:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Secret{/font}" xalign 0.5 style "damage_text"
                            else:
                                if chardes and int(chardes.atk) < int(chardes.base_atk + chardes.base_atk_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and int(chardes.atk) == int(chardes.base_atk + chardes.base_atk_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and int(chardes.atk) > int(chardes.base_atk + chardes.base_atk_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                



                            # Магия
                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                    
                                # Отображение текущего значения цветом
                                if chardes and int(chardes.magic) < int(chardes.base_magic + chardes.base_magic_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and int(chardes.magic) == int(chardes.base_magic + chardes.base_magic_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and int(chardes.magic) > int(chardes.base_magic + chardes.base_magic_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    



                                
                            # Шанспопадания
                            if chardes and int(chardes.dmgchance * 100) < int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.dmgchance * 100) == int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.dmgchance * 100) > int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            

                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.critrate * 100) < int((chardes.base_critrate + chardes.critrate_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.critrate * 100) == int((chardes.base_critrate + chardes.critrate_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.critrate * 100) > int((chardes.base_critrate + chardes.critrate_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                


                                
                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.crit * 100) < int((chardes.base_crit + chardes.crit_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.crit * 100) == int((chardes.base_crit + chardes.crit_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.crit * 100) > int((chardes.base_crit + chardes.crit_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            



                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.defense) < int(chardes.base_def + chardes.base_def_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.defense) == int(chardes.base_def + chardes.base_def_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.defense) > int(chardes.base_def + chardes.base_def_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            

                            # Tank
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.total_tank) < int(chardes.base_tank + chardes.extra_tank):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.total_tank) == int(chardes.base_tank + chardes.extra_tank):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.total_tank) > int(chardes.base_tank + chardes.extra_tank):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Отношения (только для Криса)
                            if chardes == store.pers_dict["Крис"]:
                                # Определение словесного значения в зависимости от reltns
                                if chardes and hasattr(chardes, 'reltns'):
                                    if chardes.reltns <= -80:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Hatred{/font}" xalign 0.5 color "#ff0000" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns <= -60:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Awful{/font}" xalign 0.5 color "#ff4444" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns <= -40:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Very Bad{/font}" xalign 0.5 color "#ff8888" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns <= -20:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Bad{/font}" xalign 0.5 color "#ffaaaa" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns >= 80:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Soulmate{/font}" xalign 0.5 color "#00ff00" at damage_gradient_green_bright style "damage_text"
                                    elif chardes.reltns >= 60:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Excellent{/font}" xalign 0.5 color  "#44ff44" at damage_gradient_green_bright style "damage_text"
                                    elif chardes.reltns >= 40:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Verygood{/font}" xalign 0.5 color  "#88ff88" at damage_gradient_green_bright style "damage_text"
                                    elif chardes.reltns >= 20:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Good{/font}" xalign 0.5 color"#aaffaa" at damage_gradient_green_bright style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Normal{/font}" xalign 0.5 color "#e9e770" at damage_gradient_gray style "damage_text"
                        

                        vbox:

                            xoffset 120 yoffset -20
                            text "{size=50}{font=determination.otf}Buffs" xalign 0.5 yoffset 16 at damage_gradient_gray style "damage_text"
                            
                            # Проверка дебаффов персонажа
                            if chardes.atk_debuff == 0 and chardes.def_debuff == 0 and chardes.magic_debuff == 0 and chardes.accuracy_debuff == 0 and chardes.critrate_debuff == 0 and chardes.critdmg_debuff == 0 and chardes.tank_debuff == 0 and chardes.bloodshed_debuff == 0 and chardes.prone_debuff == 0:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}---" xalign 0.5 yoffset 35 at damage_gradient_gray style "damage_text"
                            else:
                                vbox:
                                    spacing 22 yoffset 30
                                    # Проверка дебаффа кровотечения (Bloodshed)
                                    if chardes.bloodshed_debuff != 0:
                                        if chardes.bloodshed_debuff > 0:
                                            hbox:
                                                xalign 0.5 yalign 0.5 spacing 0
                                                add "bloodshed.png" at damage_gradient
                                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}bloodshed(х[chardes.bloodshed_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        elif chardes.bloodshed_debuff < 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}bloodshed(х[-chardes.bloodshed_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа prone (состояние на земле)
                                    if chardes.prone_debuff != 0:
                                        if chardes.prone_debuff > 0:
                                            hbox:
                                                xalign 0.5 yalign 0.5 spacing 0
                                                add "prone.png" at damage_gradient
                                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Prone(х[chardes.prone_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        elif chardes.prone_debuff < 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Prone(х[-chardes.prone_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа атаки
                                    if chardes.atk_debuff != 0:
                                        if chardes.atk_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Exhaust(х[chardes.atk_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Cheerful(х[-chardes.atk_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа защиты
                                    if chardes.def_debuff != 0:
                                        if chardes.def_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Sorrow(х[chardes.def_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Inspired(х[-chardes.def_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа магии
                                    if chardes.magic_debuff != 0:
                                        if chardes.magic_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Foggyminded(х[chardes.magic_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Enlighted(х[-chardes.magic_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа точности
                                    if chardes.accuracy_debuff != 0:
                                        if chardes.accuracy_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Feared(х[chardes.accuracy_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Focused(х[-chardes.accuracy_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа шанса крита
                                    if chardes.critrate_debuff != 0:
                                        if chardes.critrate_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Unluck(х[chardes.critrate_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Luck(х[-chardes.critrate_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа урона крита
                                    if chardes.critdmg_debuff != 0:
                                        if chardes.critdmg_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Apathy(х[chardes.critdmg_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Anger(х[-chardes.critdmg_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа танка
                                    if chardes.tank_debuff != 0:
                                        if chardes.tank_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Vulnerable(х[chardes.tank_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Stealth(х[-chardes.tank_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    

                if sscreenstate_style == "статический" and fullstats1_page == "social":
                    frame:
                        xpos 290
                        ypos -5
                        xysize (880, 400)
                        background None #"#000000f0"
                        #padding (12, 12, 12, 12)

                        frame:
                            yalign 0.0
                            xfill True
                            yfill True
                            background "#000000"
                            #xpos 315
                            #ypos 250
                            #padding (14, 10, 14, 10)

                            hbox:
                                at alpha_to_1
                                xpos 40

                                spacing 40

                                vbox:
                                    xoffset 20
                                    spacing 12
                                    text "{size=50}{font=determination.otf}Stats{/font}" color "#ffffff" at damage_gradient_gray style "damage_text" xalign 0.5 ypos 0 xoffset -32
                                    text "{size=40}{font=determination.otf}Социализация{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    text "{size=40}{font=determination.otf}Дипломатия{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    text "{size=40}{font=determination.otf}Очарование%{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    null height 12
                                    text "{size=40}{font=determination.otf}Восприятие{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    text "{size=40}{font=determination.otf}Риторика{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    text "{size=40}{font=determination.otf}Артистизм{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    text "{size=40}{font=determination.otf}Комфорт{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    text "{size=40}{font=determination.otf}Власть{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                                    #if chardes == store.pers_dict["Крис"]:
                                    #    text "{size=40}{font=determination.otf}Relations{/font}" color "#ffffff" at damage_gradient_gray style "damage_text" xalign 0.5

                                vbox:
                                    xoffset 40
                                    spacing 12
                                    text "{size=50}{font=determination.otf}Cur/Base{/font}" color "#ffffff" at damage_gradient_gray style "damage_text" xalign 0.5 ypos 0 xoffset -2
                                    if chardes and int(chardes.socialization) < int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.socialization)]/[int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.socialization) == int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.socialization)]/[int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.socialization) > int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.socialization)]/[int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    if chardes and int(chardes.diplomacy) < int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.diplomacy)]/[int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.diplomacy) == int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.diplomacy)]/[int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.diplomacy) > int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.diplomacy)]/[int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    if chardes and int(chardes.charm) < int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.charm)]/[int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.charm) == int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.charm)]/[int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.charm) > int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.charm)]/[int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    null height 12
                                    if chardes and int(chardes.perception) < int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.perception)]/[int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.perception) == int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.perception)]/[int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.perception) > int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.perception)]/[int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    if chardes and int(chardes.rhetoric) < int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.rhetoric)]/[int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.rhetoric) == int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.rhetoric)]/[int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.rhetoric) > int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.rhetoric)]/[int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    if chardes and int(chardes.artistry) < int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.artistry)]/[int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.artistry) == int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.artistry)]/[int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.artistry) > int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.artistry)]/[int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    if chardes and int(chardes.comfort) < int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.comfort)]/[int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.comfort) == int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.comfort)]/[int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.comfort) > int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.comfort)]/[int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    if chardes and int(chardes.power) < int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.power)]/[int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and int(chardes.power) == int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.power)]/[int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and int(chardes.power) > int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)]):
                                        text "{size=40}{font=determination.otf}[int(chardes.power)]/[int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    #if chardes == store.pers_dict["Крис"]:
                                    #    text "{size=40}{font=determination.otf}[int(chardes.reltns)]/100{/font}" color "#ffffff" xalign 1.0 at damage_gradient_gray style "damage_text"

    if sscreenstate_style == "статический" and bottom_x_shown == 1:
        
        imagebutton:
            at fullstats1_3
            #at semiblack_dynamic_alpha
            idle "closestatdesc.png"
            hover "closestatdesc_hover.png"
            action [ SetVariable("fullstats1_page", "combat"), SetVariable("sscreenstate_style", 0), SetVariable("chardespos", 0), SetVariable("bottom_x_shown", 0), SetVariable("screenstate", "недоступен"), Hide("fullstats1"), Hide("fullstats0")]




    button:
        #text"{font=determination.otf}{size=28}" + ("Социальные" if fullstats1_page == "combat" else "Боевые") + "{/size}{/font}"
        
        at fullstats1_4
        xsize 150
        ysize 50
        xoffset -810
        yoffset 2
        background None # "#6f4040"
        xpadding 10
        ypadding 6
        action If(
            fullstats1_page == "combat",
            [SetVariable("fullstats1_page", "social"), SetVariable("stats_tab", 2)],
            [SetVariable("fullstats1_page", "combat"), SetVariable("stats_tab", 1)]
        )

    if fullstats1_page == "combat":
        add "fightstats_icon.png"  xsize 60 ysize 60 xoffset 340 yoffset 20 at alpha_and_shift
    else:
        add "socialstats_icon.png" xsize 60 ysize 60 xoffset 340 yoffset 20 at alpha_and_shift

transform alpha_to_1:
    alpha 0.0 
    easein 0.3 alpha 1.0

transform alpha_and_shift:
    on show:
        ypos -200 alpha 0.0
        easein 0.5 alpha 1.0 ypos 0
    on hide:
        easein 0.5 ypos -200 alpha 0.0

transform fullstats1_3:
    zoom 1 alpha 0.0 xpos 1150 ypos 10
    easein 0.5 alpha 1.0
    
transform fullstats1_4:
    zoom 2 alpha 0.0 xpos 1150 ypos 10
    easein 0.5 alpha 1.0    

default bottom_x_shown = 0






































































# Экран для отображения персонажа
screen fullstats1_copy():

    zorder 100




    hbox:
        xoffset 5


        
        # Проверяем, является ли chardespos состоянием 1 для любого персонажа
        #if screenstate == "недоступен":
        #    at fullstats1_1
        #elif screenstate == "доступен":
        # Проверяем, является ли chardespos состоянием 2 или 3 для любого персонажа
        #    at fullstats1_2

        at fullstats1_2
        

        frame:
            yoffset 5     

            background "#ffffff"
            padding (5,5,5,5)
            xysize (1191,580)
            
            frame:
                xalign 0.5 yalign 0.5
                background "#000000"
                padding (5,5,5,5)
                xysize (1182,570)



                hbox: # НАЧАЛО ТАБЛИЦЫ
                    



                    # Первый столбик
                    vbox:

                        spacing 10 xalign 0.5

                        frame:
                        

                            background "#ffffff"
                            padding (4,4,4,4)
                            xysize (270,70)
                            
                            frame:
                                xalign 0.5 yalign 0.5
                                background "#000000"
                                xysize (264, 66)



                                hbox:
                                    xalign 0.4 yalign 0.5 spacing 10
                                    # Изображение души персонажа
                                    add ConditionSwitch(
                                        'chardes == store.pers_dict["Крис"]', "images/Krissoul.png",
                                        'chardes == store.pers_dict["Азриель"]', "images/Asrielsoul.png",
                                        'chardes == store.pers_dict["Чара"]', "images/Charasoul.png",
                                        'chardes == store.pers_dict["Фриск"]', "images/Frisksoul.png",
                                        'chardes == store.pers_dict["Иззи"]', "images/Izzysoul.png",
                                        'chardes == store.pers_dict["Кловер"]', "images/Cloversoul.png",
                                        'chardes == store.pers_dict["Седрик"]', "images/Sedricsoul.png",
                                        # Сильвия: собственного спрайта души пока нет,
                                        # используем имеющуюся иконку как заглушку,
                                        # чтобы карточка не оставалась пустой.
                                        'chardes == store.pers_dict["Сильвия"]', "images/Sedricsoul.png",
                                    ) xysize (40,40) xalign 0.5 yalign 0.5
                                    # Имя персонажа
                                    text "{size=50}{font=determination.otf}[chardes.name if hasattr(chardes, 'name') else '']" xalign 0.5 yalign 0.5 color "#ffffff" at damage_gradient_gray style "damage_text"
                            

                        # Портреты с условиями
                        add ConditionSwitch(
                            'chardes == store.pers_dict["Крис"]', "portraits/kris.png",
                            'chardes == store.pers_dict["Азриель"]', "portraits/asriel.png",
                            'chardes == store.pers_dict["Чара"]', "portraits/chara.png",
                            'chardes == store.pers_dict["Фриск"]', "portraits/frisk.png",
                            'chardes == store.pers_dict["Иззи"]', "portraits/izzy.png",
                            'chardes == store.pers_dict["Кловер"]', "portraits/clover.png",
                            'chardes == store.pers_dict["Седрик"]', "portraits/sedric.png",
                            'chardes == store.pers_dict["Седрик"]', "portraits/sedric.png",
                            'chardes == store.pers_dict["Фабри"]', "portraits/Fabri.png",
                        ) xsize 270 ysize 359
                                


                        vbox:

                            spacing 0




                            vbox:  # названия статов и картинки к ним
                                spacing 0 xalign 0.0
                                
                                # Отображение щита

                                frame:
                                    xoffset 10
                                    xmargin 0
                                    ymargin 0
                                    xalign 0.0
                                    yalign 0.0
                                    xysize (70, 12)
                                    background None

                                    # Фон щита (всегда 4 позиции)
                                    fixed:
                                        hbox:
                                            if chardes == store.pers_dict["Азриель"]:
                                                xoffset -10
                                            else:
                                                xoffset -10
                                            yalign 1.0
                                            spacing 2
                                            for i in range(1, 5):
                                                add Solid("#27250d", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                    # Заполнение щита (текущее значение)
                                    fixed:
                                    
                                        hbox:
                                            if chardes == store.pers_dict["Азриель"]:
                                                xoffset -10
                                            else:
                                                xoffset -10

                                            yalign 1.0
                                            spacing 2
                                            if chardes and chardes.shield >= 4:
                                                # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                                for i in range(1, 5):
                                                    add Solid("#ffea00", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                            else:
                                                # Иначе отображаем обычное заполнение
                                                for i in range(1, min((chardes.shield if chardes else 0) + 1, 5)):
                                                    add Solid("#e1d22e", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray
                                
                                
                                # здлолвье и хп
                                #vbox:
                                #    spacing 10                                    

                                hbox:  # текст значнеий
                                    xalign 0.0 spacing 10
                                        


                                    
                                    vbox:
                                        xalign 0.5

                                        if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):
                                            spacing 30
                                        elif chardes and ((chardes.current_hp > 1000 or chardes.max_hp > 1000) or (chardes.current_mp > 1000 or chardes.max_mp > 1000)):
                                            spacing 20
                                        else: 
                                            spacing 12

                                        # Определяем размер шрифта в зависимости от количества HP
                                        $ textsize1 = 30  # размер по умолчанию
                                        if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):
                                            $ textsize1 = 18
                                        elif chardes and ((chardes.current_hp > 1000 or chardes.max_hp > 1000) or (chardes.current_mp > 1000 or chardes.max_mp > 1000)):
                                            $ textsize1 = 24
                                        else:
                                            $ textsize1 = 30

                                        if chardes:
                                            if chardes.current_hp <= chardes.max_hp* 0.2:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#ff0000" at damage_gradient_for_lowhp style "damage_text"
                                            elif chardes.current_hp > chardes.max_hp:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#00ff00" at damage_gradient_green_bright style "damage_text"
                                            else:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#ffffff"  at damage_gradient_gray style "damage_text"
                                        else:
                                            text "{size=[textsize1]}{font=determination.otf}--/--{/font}" xalign 0.5 color "#ffffff" at damage_gradient_gray style "damage_text"

                                        
                                        

                                        if chardes == store.pers_dict["Седрик"]:
                                            pass
                                        else:
                                            if chardes:
                                                if chardes.current_mp <= chardes.max_mp* 0.2:
                                                    text "{size=[textsize1]}{font=determination.otf}[chardes.current_mp]/[chardes.max_mp]{/font}" color "#ffffffc2" xalign 0.5 min_width 60 yoffset -11 style "damagetext2 damage_text" at damage_gradient_black
                                                elif chardes.current_mp > chardes.max_mp:
                                                    text "{size=[textsize1]}{font=determination.otf}[chardes.current_mp]/[chardes.max_mp]{/font}" color "#3adeff" xalign 0.5 min_width 60 yoffset -11 style  "damagetext2 damage_text" at damage_gradient_semigray
                                                else:
                                                    text "{size=[textsize1]}{font=determination.otf}{color=#ffffff}[chardes.current_mp]/[chardes.max_mp]{/font}{/color}" xalign 0.5 min_width 60 yoffset -11 style  "damagetext2 damage_text" at damage_gradient_gray
                                            else:
                                                text "{size=[textsize1]}{font=determination.otf}{color=#ffffff}--/--{/font}{/color}" xalign 0.5 min_width 60 yoffset -11 style "damagetext2 damage_text" at damage_gradient_gray
                                            #text "/"
                                            #text "{font=determination.otf}[chardes.max_mp]{/font}"


                                
                                    vbox:
                                        spacing 10 xalign 0.0

                                        # Полоска HP
                                        fixed:
                                            #xysize (60, 8) 
                                            xalign 1.0
                                            # Фон HP
                                            hbox:
                                                spacing 3
                                                if chardes and chardes.current_hp > chardes.max_hp:
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
                                                if chardes and chardes.current_hp > chardes.max_hp:
                                                    # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                                    $ hp_overheal_percent = (chardes.current_hp - chardes.max_hp) / chardes.max_hp * 100
                                                    $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                                    for i in range(overheal_icons):
                                                        add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                                elif chardes and chardes.current_hp > 0 and chardes.current_hp <= chardes.max_hp * 0.2:
                                                    # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                                    $ low_fill = int(math.ceil((chardes.current_hp / chardes.max_hp) * 10))
                                                    for i in range(low_fill):
                                                        add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                                else:
                                                    # Обычное отображение HP
                                                    $ hp_fill = int(math.ceil((chardes.current_hp / chardes.max_hp) * 10))
                                                    for i in range(hp_fill):
                                                        add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    

                                        fixed:
                                            yoffset -80 + textsize1*0.3
                                            xysize (60, 10)
                                 
                                            # Фон MP
                                            hbox:
                                                spacing 3 
                                                if chardes and chardes.current_mp > chardes.max_mp:
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
                                                if chardes and chardes.current_mp > chardes.max_mp:
                                                    $ mp_overmana_percent = (chardes.current_mp - chardes.max_mp) / chardes.max_mp * 100
                                                    $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                                    for i in range(overmana_icons2):
                                                        add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray
                                                elif chardes and chardes.current_mp > 0 and chardes.current_mp <= chardes.max_mp * 0.2:
                                                    # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                                    $ low_fill = get_display_mp_fill(chardes)
                                                    for i in range(low_fill):
                                                        add "mpactive.png" zoom 1.2 at damage_gradient
                                                else:
                                                    # Обычное отображение MP
                                                    $ mp_fill = get_display_mp_fill(chardes)
                                                    for i in range(mp_fill):
                                                        add "mpactive.png" zoom 1.2 at damage_gradient_gray



                        if chardes and hasattr(chardes, "max_feedness") and chardes.max_feedness > 0:
                            fixed:
                                yoffset -50
                                #yoffset -68 + textsize1*0.3
                                #xoffset -80 - textsize1*0.3
                                xalign 0.0
                                xysize (280, 12)
                                add FeednessQueueBar(chardes, width=280, height=12, gap=10)











































                
                hbox:
                    xalign 0.6 yalign 0.25 #spacing 30 

                    if (chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 
                        or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or chardes.critrate_debuff != 0
                        or chardes.critdmg_debuff != 0 or chardes.tank_debuff != 0):
                        spacing -10
                        $ multiply_for_text = 0.85
                        xoffset 40
                    else:
                        spacing 30
                        $ multiply_for_text = 0
                        xoffset 20
                    #if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):

                    ######################################### Индикаторы баффов дебаффорв
                    hbox:
                        xalign 0.0
                        if store.stats_tab != 2:
                            vbox:
                                xalign 0.0

                                if chardes != store.pers_dict["Крис"]:
                                    # условия, есть ли у персонажа любой дебаф
                                    if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                        spacing 12 yoffset 60 xoffset 0
                                    else:
                                        spacing 8 xoffset 17 yoffset 65 
                                
                                else:                                
                                    if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                        spacing 12 yoffset 60 xoffset 0
                                    else:
                                        spacing 8 xoffset 17 yoffset 65 
                                
                                

                                

                                #aтака

                                if chardes == store.pers_dict["Иззи"]:
                                    pass
                                else:
                                    # Определение цвета иконки
                                    if chardes and chardes.bonus_atk < 0:
                                        add "atk_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                    elif chardes and chardes.bonus_atk == 0:
                                        add "atk_white_indi.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                    elif chardes and chardes.bonus_atk > 0:
                                        add "atk_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                        


                                #Магия 


                                if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                    pass
                                else:
                                    # Определение цвета иконки
                                    if chardes and chardes.bonus_magic < 0:
                                        add "mag_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                    elif chardes and chardes.bonus_magic == 0:
                                        add "mag_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                    elif chardes and chardes.bonus_magic > 0:
                                        add "mag_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                                # шанс попадания
                                # Определение цвета иконки

                                if chardes and chardes.dmgchance > 1:
                                    add "dmgchance_overchance.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                elif chardes and chardes.bonus_dmgchance < 0:
                                    add "dmgchance_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_dmgchance == 0:
                                    add "dmgchance_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_dmgchance > 0:
                                    add "dmgchance_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                                # критшанс
                                # Определение цвета иконки
                                if chardes and chardes.critrate > 1:
                                    add "critrate_overcrit.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                elif chardes and chardes.bonus_critrate < 0:
                                    add "critrate_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_critrate == 0:
                                    add "critrate_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_critrate > 0:
                                    add "critrate_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green



                                if chardes and chardes.bonus_crit < 0:
                                    add "critdmg_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_crit == 0:
                                    add "critdmg_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_crit > 0:
                                    add "critdmg_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green



                                if chardes and chardes.bonus_def < 0:
                                    add "def_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_def == 0:
                                    add "def_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_def > 0:
                                    add "def_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                                # Tank
                                # Определение цвета иконки
                                if chardes and chardes.bonus_tank < 0:
                                    add "tank_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) 
                                elif chardes and chardes.bonus_tank == 0:
                                    add "tank_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_tank > 0:
                                    add "tank_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) 

                                vbox:
                                    xoffset -10
                                    # Отношения (только для Криса)
                                    if chardes == store.pers_dict["Крис"]:
                                        # Определение иконки в зависимости от значения reltns
                                        if chardes and hasattr(chardes, 'reltns'):
                                            if chardes.reltns <= -80:
                                                add "awfulmax.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_for_lowhp2
                                            elif chardes.reltns <= -60:
                                                add "awful.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                            elif chardes.reltns <= -40:
                                                add "verybad.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                            elif chardes.reltns <= -20:
                                                add "bad.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                            elif chardes.reltns < 20:
                                                add "normal.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_yellow
                                            elif chardes.reltns < 40:
                                                add "good.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                            elif chardes.reltns < 60:
                                                add "verygood.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                            elif chardes.reltns < 80:
                                                add "excellent.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                            elif chardes.reltns == 100:
                                                add "excellentmax.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green_bright
                                            else:
                                                pass






                            vbox:
                                # Отображение всех bonus_характеристик в текстовом виде

                                at alpha_to_1
                                
                                
                                # условия, есть ли у персонажа любой дебаф
                                if chardes != store.pers_dict["Крис"]:
                                    # условия, есть ли у персонажа любой дебаф
                                    if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                        spacing 40 yoffset 47 xoffset -15
                                    else:
                                        spacing 45 yoffset 53 xoffset 0
                                
                                else:                                
                                    if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                        spacing 40 yoffset 15 xoffset -15
                                    else:
                                        spacing 45 yoffset 18 xoffset 0

                                xalign 0.0 yalign 0.5 
                                
                                
                                # Атака
                                if chardes == store.pers_dict["Иззи"]:
                                    pass
                                else:
                                    if chardes and chardes.bonus_atk < 0:
                                        text "{size=18}{font=determination.otf}[int(chardes.bonus_atk*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and chardes.bonus_atk == 0:
                                        text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and chardes.bonus_atk > 0:
                                        text "{size=18}{font=determination.otf}[int(chardes.bonus_atk*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Магия
                                if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                    pass
                                else:
                                    if chardes and chardes.bonus_magic < 0:
                                        text "{size=18}{font=determination.otf}[int(chardes.bonus_magic*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                    elif chardes and chardes.bonus_magic == 0:
                                        text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                    elif chardes and chardes.bonus_magic > 0:
                                        text "{size=18}{font=determination.otf}[int(chardes.bonus_magic*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Точность
                                if chardes and chardes.bonus_dmgchance < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_dmgchance*100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_dmgchance == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_dmgchance > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_dmgchance*100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Шанс крита
                                if chardes and chardes.bonus_critrate < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_critrate*100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_critrate == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_critrate > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_critrate*100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Критический урон
                                if chardes and chardes.bonus_crit < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_crit*100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_crit == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_crit > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_crit*100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Защита
                                if chardes and chardes.bonus_def < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_def*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_def == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_def > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_def*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Tank
                                if chardes and chardes.bonus_tank < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_tank == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_tank > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"






























                        ########################################           Название характеристики
                        vbox:
                            # атака
                            
                            xalign 0.0 spacing 22 yoffset -5


                            text "{size=50}{font=determination.otf}Stats" yoffset -15 at damage_gradient_gray style "damage_text"

                                




                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            elif chardes == store.pers_dict["Фриск"]:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Legate's{/font}" style "damage_text"
                            
                            else:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Attack{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            

                            # Мания
                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Magic{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"

                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Dmg.Chance%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Crit.Rate%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Crit.Dmg%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Defense{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Tank{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                            
                            # Отношения (только для Криса)
                            if chardes == store.pers_dict["Крис"]:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Relations{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"






                        vbox: #############################          значение характеристики
                            spacing 22 yoffset -5 xoffset 30 xalign 1.0

                            text "{size=50}{font=determination.otf}Cur/Base" yoffset -15 at damage_gradient_gray style "damage_text"


                            # Атака
                            # Отображение текущего значения цветом
                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            elif chardes == store.pers_dict["Фриск"]:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Secret{/font}" xalign 0.5 style "damage_text"
                            else:
                                if chardes and int(chardes.atk) < int(chardes.base_atk + chardes.base_atk_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and int(chardes.atk) == int(chardes.base_atk + chardes.base_atk_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and int(chardes.atk) > int(chardes.base_atk + chardes.base_atk_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                



                            # Магия
                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                    
                                # Отображение текущего значения цветом
                                if chardes and int(chardes.magic) < int(chardes.base_magic + chardes.base_magic_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and int(chardes.magic) == int(chardes.base_magic + chardes.base_magic_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and int(chardes.magic) > int(chardes.base_magic + chardes.base_magic_mod):
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    



                                
                            # Шанспопадания
                            if chardes and int(chardes.dmgchance * 100) < int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.dmgchance * 100) == int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.dmgchance * 100) > int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            

                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.critrate * 100) < int((chardes.base_critrate + chardes.critrate_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.critrate * 100) == int((chardes.base_critrate + chardes.critrate_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.critrate * 100) > int((chardes.base_critrate + chardes.critrate_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                


                                
                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.crit * 100) < int((chardes.base_crit + chardes.crit_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.crit * 100) == int((chardes.base_crit + chardes.crit_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.crit * 100) > int((chardes.base_crit + chardes.crit_mod) * 100):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            



                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.defense) < int(chardes.base_def + chardes.base_def_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.defense) == int(chardes.base_def + chardes.base_def_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.defense) > int(chardes.base_def + chardes.base_def_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            

                            # Tank
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.total_tank) < int(chardes.base_tank + chardes.extra_tank):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.total_tank) == int(chardes.base_tank + chardes.extra_tank):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.total_tank) > int(chardes.base_tank + chardes.extra_tank):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Отношения (только для Криса)
                            if chardes == store.pers_dict["Крис"]:
                                # Определение словесного значения в зависимости от reltns
                                if chardes and hasattr(chardes, 'reltns'):
                                    if chardes.reltns <= -80:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Hatred{/font}" xalign 0.5 color "#ff0000" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns <= -60:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Awful{/font}" xalign 0.5 color "#ff4444" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns <= -40:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Very Bad{/font}" xalign 0.5 color "#ff8888" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns <= -20:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Bad{/font}" xalign 0.5 color "#ffaaaa" at  damage_gradient_black style "damage_text"
                                    elif chardes.reltns >= 80:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Soulmate{/font}" xalign 0.5 color "#00ff00" at damage_gradient_green_bright style "damage_text"
                                    elif chardes.reltns >= 60:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Excellent{/font}" xalign 0.5 color  "#44ff44" at damage_gradient_green_bright style "damage_text"
                                    elif chardes.reltns >= 40:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Verygood{/font}" xalign 0.5 color  "#88ff88" at damage_gradient_green_bright style "damage_text"
                                    elif chardes.reltns >= 20:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Good{/font}" xalign 0.5 color"#aaffaa" at damage_gradient_green_bright style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Normal{/font}" xalign 0.5 color "#e9e770" at damage_gradient_gray style "damage_text"
                        

                        vbox:

                            xoffset 120 yoffset -20
                            text "{size=50}{font=determination.otf}Buffs" xalign 0.5 at damage_gradient_gray style "damage_text"
                            
                            # Проверка дебаффов персонажа
                            if chardes.atk_debuff == 0 and chardes.def_debuff == 0 and chardes.magic_debuff == 0 and chardes.accuracy_debuff == 0 and chardes.critrate_debuff == 0 and chardes.critdmg_debuff == 0 and chardes.tank_debuff == 0 and chardes.bloodshed_debuff == 0 and chardes.prone_debuff == 0:
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}---" xalign 0.5 yoffset 35 at damage_gradient_gray style "damage_text"
                            else:
                                vbox:
                                    spacing 22 yoffset 30
                                    # Проверка дебаффа кровотечения (Bloodshed)
                                    if chardes.bloodshed_debuff != 0:
                                        if chardes.bloodshed_debuff > 0:
                                            hbox:
                                                xalign 0.5 yalign 0.5 spacing 0
                                                add "bloodshed.png" at damage_gradient
                                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}bloodshed(х[chardes.bloodshed_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        elif chardes.bloodshed_debuff < 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}bloodshed(х[-chardes.bloodshed_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа prone (состояние на земле)
                                    if chardes.prone_debuff != 0:
                                        if chardes.prone_debuff > 0:
                                            hbox:
                                                xalign 0.5 yalign 0.5 spacing 0
                                                add "prone.png" at damage_gradient
                                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Prone(х[chardes.prone_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        elif chardes.prone_debuff < 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Prone(х[-chardes.prone_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа атаки
                                    if chardes.atk_debuff != 0:
                                        if chardes.atk_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Exhaust(х[chardes.atk_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Cheerful(х[-chardes.atk_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа защиты
                                    if chardes.def_debuff != 0:
                                        if chardes.def_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Sorrow(х[chardes.def_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Inspired(х[-chardes.def_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа магии
                                    if chardes.magic_debuff != 0:
                                        if chardes.magic_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Foggyminded(х[chardes.magic_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Enlighted(х[-chardes.magic_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа точности
                                    if chardes.accuracy_debuff != 0:
                                        if chardes.accuracy_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Feared(х[chardes.accuracy_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Focused(х[-chardes.accuracy_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа шанса крита
                                    if chardes.critrate_debuff != 0:
                                        if chardes.critrate_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Unluck(х[chardes.critrate_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Luck(х[-chardes.critrate_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа урона крита
                                    if chardes.critdmg_debuff != 0:
                                        if chardes.critdmg_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Apathy(х[chardes.critdmg_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Anger(х[-chardes.critdmg_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                                    # Проверка дебаффа танка
                                    if chardes.tank_debuff != 0:
                                        if chardes.tank_debuff > 0:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Vulnerable(х[chardes.tank_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                        else:
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Stealth(х[-chardes.tank_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                    
                
    if store.stats_tab == 2:
        frame:
            at fullstats1_2
            xoffset 350
            yoffset 10
            xysize (830, 400)
            background None

            frame:
                yalign 0.0
                xfill True
                yfill True
                background "#000000"

                hbox:
                    at alpha_to_1
                    xpos 40
                    spacing 40

                    vbox:
                        xoffset 20
                        spacing 12
                        text "{size=50}{font=determination.otf}Stats{/font}" color "#ffffff" at damage_gradient_gray style "damage_text" xalign 0.5 ypos 0 xoffset -32
                        text "{size=40}{font=determination.otf}Социализация{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        text "{size=40}{font=determination.otf}Дипломатия{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        text "{size=40}{font=determination.otf}Очарование%{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        null height 12
                        text "{size=40}{font=determination.otf}Восприятие{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        text "{size=40}{font=determination.otf}Риторика{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        text "{size=40}{font=determination.otf}Артистизм{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        text "{size=40}{font=determination.otf}Комфорт{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"
                        text "{size=40}{font=determination.otf}Власть{/font}" color "#ffffff" at damage_gradient_gray style "damage_text"

                    vbox:
                        xoffset 40
                        spacing 12
                        text "{size=50}{font=determination.otf}Cur/Base{/font}" color "#ffffff" at damage_gradient_gray style "damage_text" xalign 0.5 ypos 0 xoffset -2
                        if chardes and int(chardes.socialization) < int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.socialization)]/[int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.socialization) == int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.socialization)]/[int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.socialization) > int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.socialization)]/[int(chardes.base_socialization_levels[chardes.get_safe_index(chardes.base_socialization_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        if chardes and int(chardes.diplomacy) < int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.diplomacy)]/[int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.diplomacy) == int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.diplomacy)]/[int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.diplomacy) > int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.diplomacy)]/[int(chardes.base_diplomacy_levels[chardes.get_safe_index(chardes.base_diplomacy_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        if chardes and int(chardes.charm) < int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.charm)]/[int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.charm) == int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.charm)]/[int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.charm) > int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.charm)]/[int(chardes.base_charm_levels[chardes.get_safe_index(chardes.base_charm_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        null height 12
                        if chardes and int(chardes.perception) < int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.perception)]/[int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.perception) == int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.perception)]/[int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.perception) > int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.perception)]/[int(chardes.base_perception_levels[chardes.get_safe_index(chardes.base_perception_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        if chardes and int(chardes.rhetoric) < int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.rhetoric)]/[int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.rhetoric) == int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.rhetoric)]/[int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.rhetoric) > int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.rhetoric)]/[int(chardes.base_rhetoric_levels[chardes.get_safe_index(chardes.base_rhetoric_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        if chardes and int(chardes.artistry) < int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.artistry)]/[int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.artistry) == int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.artistry)]/[int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.artistry) > int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.artistry)]/[int(chardes.base_artistry_levels[chardes.get_safe_index(chardes.base_artistry_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        if chardes and int(chardes.comfort) < int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.comfort)]/[int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.comfort) == int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.comfort)]/[int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.comfort) > int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.comfort)]/[int(chardes.base_comfort_levels[chardes.get_safe_index(chardes.base_comfort_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        if chardes and int(chardes.power) < int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.power)]/[int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)])]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.power) == int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.power)]/[int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)])]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.power) > int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)]):
                            text "{size=40}{font=determination.otf}[int(chardes.power)]/[int(chardes.base_power_levels[chardes.get_safe_index(chardes.base_power_levels)])]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"

    #if store.stats_tab == 1:
    #    add "fightstats_icon.png" xsize 60 ysize 60 xoffset 340 yoffset 20
    #else:
    #    add "socialstats_icon.png" xsize 60 ysize 60 xoffset 340 yoffset 20

    if sscreenstate_style == "статический" and bottom_x_shown == 1:
        
        imagebutton:
            at fullstats1_3
            #at semiblack_dynamic_alpha
            idle "closestatdesc.png"
            hover "closestatdesc_hover.png"
            action [ SetVariable("sscreenstate_style", 0), SetVariable("chardespos", 0), SetVariable("bottom_x_shown", 0), SetVariable("screenstate", "недоступен"), Hide("fullstats1"), Hide("fullstats0")]


transform fullstats1_3:
    zoom 2 alpha 0.0 xpos 1150 ypos 10
    easein 0.5 alpha 1.0
    






















































transform fullstatscopy2:
    on show:
        alpha 0.0 xoffset 1280 yoffset 130
        pause 0.5
        easein 0.8 xoffset 50 alpha 1.0
    on hide:
        yoffset 130
        easein 0.5 alpha 0.0 xoffset 100 



# Экран для отображения персонажа
screen fullstats1_copy2():

    zorder 100




    hbox:
        xoffset 5


        at fullstatscopy2



        frame:
            yoffset 5     

            background "#ffffff"
            padding (5,5,5,5)
            xysize (1191,580)
            
            frame:
                xalign 0.5 yalign 0.5
                background "#000000"
                padding (5,5,5,5)
                xysize (1182,570)



                hbox: # НАЧАЛО ТАБЛИЦЫ
                    



                    # Первый столбик
                    vbox:

                        spacing 10 xalign 0.5

                        frame:
                        

                            background "#ffffff"
                            padding (4,4,4,4)
                            xysize (270,70)
                            
                            frame:
                                xalign 0.5 yalign 0.5
                                background "#000000"
                                xysize (264, 66)



                                hbox:
                                    xalign 0.4 yalign 0.5 spacing 10
                                    # Изображение души персонажа
                                    add ConditionSwitch(
                                        'chardes == store.pers_dict["Крис"]', "images/Krissoul.png",
                                        'chardes == store.pers_dict["Азриель"]', "images/Asrielsoul.png",
                                        'chardes == store.pers_dict["Чара"]', "images/Charasoul.png",
                                        'chardes == store.pers_dict["Фриск"]', "images/Frisksoul.png",
                                        'chardes == store.pers_dict["Иззи"]', "images/Izzysoul.png",
                                        'chardes == store.pers_dict["Кловер"]', "images/Cloversoul.png",
                                        'chardes == store.pers_dict["Седрик"]', "images/Sedricsoul.png",
                                        # Сильвия: собственного спрайта души пока нет,
                                        # используем имеющуюся иконку как заглушку,
                                        # чтобы карточка не оставалась пустой.
                                        'chardes == store.pers_dict["Сильвия"]', "images/Sedricsoul.png",
                                    ) xysize (40,40) xalign 0.5 yalign 0.5
                                    # Имя персонажа
                                    text "{size=50}{font=determination.otf}[chardes.name if hasattr(chardes, 'name') else '']" xalign 0.5 yalign 0.5 color "#ffffff" at damage_gradient_gray style "damage_text"
                            

                        # Портреты с условиями
                        add ConditionSwitch(
                            'chardes == store.pers_dict["Крис"]', "portraits/kris.png",
                            'chardes == store.pers_dict["Азриель"]', "portraits/asriel.png",
                            'chardes == store.pers_dict["Чара"]', "portraits/chara.png",
                            'chardes == store.pers_dict["Фриск"]', "portraits/frisk.png",
                            'chardes == store.pers_dict["Иззи"]', "portraits/izzy.png",
                            'chardes == store.pers_dict["Кловер"]', "portraits/clover.png",
                            'chardes == store.pers_dict["Седрик"]', "portraits/sedric.png",
                            'chardes == store.pers_dict["Седрик"]', "portraits/sedric.png",
                            'chardes == store.pers_dict["Фабри"]', "portraits/Fabri.png",
                        ) xsize 270 ysize 359
                                


                        vbox:

                            spacing 0




                            vbox:  # названия статов и картинки к ним
                                spacing 0 xalign 0.0
                                
                                # Отображение щита

                                frame:
                                    xoffset 10
                                    xmargin 0
                                    ymargin 0
                                    xalign 0.0
                                    yalign 0.0
                                    xysize (70, 12)
                                    background None

                                    # Фон щита (всегда 4 позиции)
                                    fixed:
                                        hbox:
                                            if chardes == store.pers_dict["Азриель"]:
                                                xoffset -10
                                            else:
                                                xoffset -10
                                            yalign 1.0
                                            spacing 2
                                            for i in range(1, 5):
                                                add Solid("#27250d", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_black
                                    # Заполнение щита (текущее значение)
                                    fixed:
                                    
                                        hbox:
                                            if chardes == store.pers_dict["Азриель"]:
                                                xoffset -10
                                            else:
                                                xoffset -10

                                            yalign 1.0
                                            spacing 2
                                            if chardes and chardes.shield >= 4:
                                                # Если щит равен 4 или больше, отображаем все 4 позиции специальным цветом
                                                for i in range(1, 5):
                                                    add Solid("#ffea00", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                                            else:
                                                # Иначе отображаем обычное заполнение
                                                for i in range(1, min((chardes.shield if chardes else 0) + 1, 5)):
                                                    add Solid("#e1d22e", xysize=(65, int(10 * i * 0.20))) yalign 1.0 xalign 1.0 at damage_gradient_gray
                                
                                
                                # здлолвье и хп
                                #vbox:
                                #    spacing 10                                    

                                hbox:  # текст значнеий
                                    xalign 0.0 spacing 10
                                        


                                    
                                    vbox:
                                        xalign 0.5

                                        if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):
                                            spacing 30
                                        elif chardes and ((chardes.current_hp > 1000 or chardes.max_hp > 1000) or (chardes.current_mp > 1000 or chardes.max_mp > 1000)):
                                            spacing 20
                                        else: 
                                            spacing 12

                                        # Определяем размер шрифта в зависимости от количества HP
                                        $ textsize1 = 30  # размер по умолчанию
                                        if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):
                                            $ textsize1 = 18
                                        elif chardes and ((chardes.current_hp > 1000 or chardes.max_hp > 1000) or (chardes.current_mp > 1000 or chardes.max_mp > 1000)):
                                            $ textsize1 = 24
                                        else:
                                            $ textsize1 = 30

                                        if chardes:
                                            if chardes.current_hp <= chardes.max_hp* 0.2:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#ff0000" at damage_gradient_for_lowhp style "damage_text"
                                            elif chardes.current_hp > chardes.max_hp:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#00ff00" at damage_gradient_green_bright style "damage_text"
                                            else:
                                                text "{size=[textsize1]}{font=determination.otf}[chardes.current_hp]/[chardes.max_hp]{/font}" xalign 0.5 color "#ffffff"  at damage_gradient_gray style "damage_text"
                                        else:
                                            text "{size=[textsize1]}{font=determination.otf}--/--{/font}" xalign 0.5 color "#ffffff" at damage_gradient_gray style "damage_text"

                                        
                                        

                                        if chardes == store.pers_dict["Седрик"]:
                                            pass
                                        else:
                                            if chardes:
                                                if chardes.current_mp <= chardes.max_mp* 0.2:
                                                    text "{size=[textsize1]}{font=determination.otf}[chardes.current_mp]/[chardes.max_mp]{/font}" color "#ffffffc2" xalign 0.5 min_width 60 yoffset -11 style "damagetext2 damage_text" at damage_gradient_black
                                                elif chardes.current_mp > chardes.max_mp:
                                                    text "{size=[textsize1]}{font=determination.otf}[chardes.current_mp]/[chardes.max_mp]{/font}" color "#3adeff" xalign 0.5 min_width 60 yoffset -11 style  "damagetext2 damage_text" at damage_gradient_semigray
                                                else:
                                                    text "{size=[textsize1]}{font=determination.otf}{color=#ffffff}[chardes.current_mp]/[chardes.max_mp]{/font}{/color}" xalign 0.5 min_width 60 yoffset -11 style  "damagetext2 damage_text" at damage_gradient_gray
                                            else:
                                                text "{size=[textsize1]}{font=determination.otf}{color=#ffffff}--/--{/font}{/color}" xalign 0.5 min_width 60 yoffset -11 style "damagetext2 damage_text" at damage_gradient_gray
                                            #text "/"
                                            #text "{font=determination.otf}[chardes.max_mp]{/font}"


                                
                                    vbox:
                                        spacing 10 xalign 0.0

                                        # Полоска HP
                                        fixed:
                                            #xysize (60, 8) 
                                            xalign 1.0
                                            # Фон HP
                                            hbox:
                                                spacing 3
                                                if chardes and chardes.current_hp > chardes.max_hp:
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
                                                if chardes and chardes.current_hp > chardes.max_hp:
                                                    # Если HP больше максимума, вычисляем количество иконок на основе превышения
                                                    $ hp_overheal_percent = (chardes.current_hp - chardes.max_hp) / chardes.max_hp * 100
                                                    $ overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                                    for i in range(overheal_icons):
                                                        add "hpactive_overheal.png" zoom 1.2 at damage_gradient_overheal
                                                elif chardes and chardes.current_hp > 0 and chardes.current_hp <= chardes.max_hp * 0.2:
                                                    # Если HP меньше или равно 20% от максимума; число ячеек округляется вверх
                                                    $ low_fill = int(math.ceil((chardes.current_hp / chardes.max_hp) * 10))
                                                    for i in range(low_fill):
                                                        add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                                else:
                                                    # Обычное отображение HP
                                                    $ hp_fill = int(math.ceil((chardes.current_hp / chardes.max_hp) * 10))
                                                    for i in range(hp_fill):
                                                        add "hpactive.png" zoom 1.2 at damage_gradient_gray
                                    

                                        fixed:
                                            yoffset -80 + textsize1*0.3
                                            xysize (60, 10)
                                 
                                            # Фон MP
                                            hbox:
                                                spacing 3 
                                                if chardes and chardes.current_mp > chardes.max_mp:
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
                                                if chardes and chardes.current_mp > chardes.max_mp:
                                                    $ mp_overmana_percent = (chardes.current_mp - chardes.max_mp) / chardes.max_mp * 100
                                                    $ overmana_icons2 = min(5, int(math.ceil(mp_overmana_percent / 10.0)))  # Неполная доля в 5% округляется вверх, но не более 10 иконок
                                                    for i in range(overmana_icons2):
                                                        add Solid("#32eeff", xysize=(12, 22)) zoom 1.2 at damage_gradient_semigray
                                                elif chardes and chardes.current_mp > 0 and chardes.current_mp <= chardes.max_mp * 0.2:
                                                    # Если MP меньше или равно 20% от максимума; число ячеек округляется вверх
                                                    $ low_fill = get_display_mp_fill(chardes)
                                                    for i in range(low_fill):
                                                        add "mpactive.png" zoom 1.2 at damage_gradient
                                                else:
                                                    # Обычное отображение MP
                                                    $ mp_fill = get_display_mp_fill(chardes)
                                                    for i in range(mp_fill):
                                                        add "mpactive.png" zoom 1.2 at damage_gradient_gray








                        if chardes and hasattr(chardes, "max_feedness") and chardes.max_feedness > 0:
                            fixed:
                                yoffset -50
                                #yoffset -68 + textsize1*0.3
                                #xoffset -80 - textsize1*0.3
                                xalign 0.0
                                xysize (280, 12)
                                add FeednessQueueBar(chardes, width=280, height=12, gap=10)







































                
                hbox:
                    xalign 0.6 yalign 0.25 #spacing 30 

                    if (chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 
                        or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or chardes.critrate_debuff != 0
                        or chardes.critdmg_debuff != 0 or chardes.tank_debuff != 0):
                        spacing -10
                        $ multiply_for_text = 0.85
                        xoffset 40
                    else:
                        spacing 30
                        $ multiply_for_text = 0
                        xoffset 20
                    #if chardes and ((chardes.current_hp > 1000 and chardes.max_hp > 1000) or (chardes.current_mp > 1000 and chardes.max_mp > 1000)):

                    ######################################### Индикаторы баффов дебаффорв
                    hbox:
                        xalign 0.0
                        vbox:
                            xalign 0.0

                            if chardes != store.pers_dict["Крис"]:
                                # условия, есть ли у персонажа любой дебаф
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 12 yoffset 60 xoffset -10
                                else:
                                    spacing 8 xoffset 17 yoffset 65 
                            
                            else:                                
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 12 yoffset 60 xoffset -10
                                else:
                                    spacing 8 xoffset 17 yoffset 65 
                            
                            #aтака

                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            else:
                                # Определение цвета иконки
                                if chardes and chardes.bonus_atk < 0:
                                    add "atk_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_atk == 0:
                                    add "atk_white_indi.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_atk > 0:
                                    add "atk_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                    


                            #Магия 


                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                # Определение цвета иконки
                                if chardes and chardes.bonus_magic < 0:
                                    add "mag_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                elif chardes and chardes.bonus_magic == 0:
                                    add "mag_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                                elif chardes and chardes.bonus_magic > 0:
                                    add "mag_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                            # шанс попадания
                            # Определение цвета иконки

                            if chardes and chardes.dmgchance > 1:
                                add "dmgchance_overchance.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                            elif chardes and chardes.bonus_dmgchance < 0:
                                add "dmgchance_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_dmgchance == 0:
                                add "dmgchance_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_dmgchance > 0:
                                add "dmgchance_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                            # критшанс
                            # Определение цвета иконки
                            if chardes and chardes.critrate > 1:
                                add "critrate_overcrit.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                            elif chardes and chardes.bonus_critrate < 0:
                                add "critrate_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_critrate == 0:
                                add "critrate_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_critrate > 0:
                                add "critrate_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green



                            if chardes and chardes.bonus_crit < 0:
                                add "critdmg_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_crit == 0:
                                add "critdmg_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_crit > 0:
                                add "critdmg_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green



                            if chardes and chardes.bonus_def < 0:
                                add "def_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                            elif chardes and chardes.bonus_def == 0:
                                add "def_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_def > 0:
                                add "def_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green


                            # Tank
                            # Определение цвета иконки
                            if chardes and chardes.bonus_tank < 0:
                                add "tank_red_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) 
                            elif chardes and chardes.bonus_tank == 0:
                                add "tank_white_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) alpha 0.0
                            elif chardes and chardes.bonus_tank > 0:
                                add "tank_green_icon.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) 

                            # Отношения (только для Криса)
                            if chardes == store.pers_dict["Крис"]:
                                # Определение иконки в зависимости от значения reltns
                                if chardes and hasattr(chardes, 'reltns'):
                                    if chardes.reltns <= -80:
                                        add "awfulmax.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_for_lowhp2
                                    elif chardes.reltns <= -60:
                                        add "awful.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                    elif chardes.reltns <= -40:
                                        add "verybad.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                    elif chardes.reltns <= -20:
                                        add "bad.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient
                                    elif chardes.reltns < 20:
                                        add "normal.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_yellow
                                    elif chardes.reltns < 40:
                                        add "good.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                    elif chardes.reltns < 60:
                                        add "verygood.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                    elif chardes.reltns < 80:
                                        add "excellent.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green
                                    elif chardes.reltns == 100:
                                        add "excellentmax.png" xysize (int(60*multiply_for_text) if multiply_for_text > 0 else 60, int(60*multiply_for_text) if multiply_for_text > 0 else 60) at damage_gradient_green_bright
                                    else:
                                        pass






                        vbox:
                            # Отображение всех bonus_характеристик в текстовом виде
                            at alpha_to_1
                            
                            
                            # условия, есть ли у персонажа любой дебаф
                            if chardes != store.pers_dict["Крис"]:
                                # условия, есть ли у персонажа любой дебаф
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 40 yoffset 75 xoffset -25
                                else:
                                    spacing 45 yoffset 85 xoffset 0
                            
                            else:                                
                                if chardes.bloodshed_debuff != 0 or chardes.prone_debuff != 0 or chardes.atk_debuff != 0 or chardes.def_debuff != 0 or chardes.magic_debuff != 0 or chardes.accuracy_debuff != 0 or                                            chardes.critrate_debuff != 0 or chardes.critdmg_debuff != 0 or                                            chardes.tank_debuff != 0:
                                    spacing 40 yoffset 45 xoffset -25
                                else:
                                    spacing 45 yoffset 50 xoffset 0

                            xalign 0.0 yalign 0.5 
                                
                            
                            # Атака
                            if chardes == store.pers_dict["Иззи"]:
                                pass
                            else:
                                if chardes and chardes.bonus_atk < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_atk*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_atk == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_atk > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_atk*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Магия
                            if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                                pass
                            else:
                                if chardes and chardes.bonus_magic < 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_magic*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                                elif chardes and chardes.bonus_magic == 0:
                                    text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                                elif chardes and chardes.bonus_magic > 0:
                                    text "{size=18}{font=determination.otf}[int(chardes.bonus_magic*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Точность
                            if chardes and chardes.bonus_dmgchance < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_dmgchance*100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_dmgchance == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_dmgchance > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_dmgchance*100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Шанс крита
                            if chardes and chardes.bonus_critrate < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_critrate*100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_critrate == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_critrate > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_critrate*100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Критический урон
                            if chardes and chardes.bonus_crit < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_crit*100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_crit == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_crit > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_crit*100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Защита
                            if chardes and chardes.bonus_def < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_def*100)]%{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and chardes.bonus_def == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_def > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_def*100)]%{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            
                            # Tank
                            if chardes and chardes.bonus_tank < 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_tank == 0:
                                text "{size=18}{font=determination.otf}{alpha=0}{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and chardes.bonus_tank > 0:
                                text "{size=18}{font=determination.otf}[int(chardes.bonus_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"






























                    ########################################           Название характеристики
                    vbox:
                        # атака
                        
                        xalign 0.0 spacing 22 yoffset -5


                        text "{size=50}{font=determination.otf}Stats" yoffset -15 at damage_gradient_gray style "damage_text"

                            




                        if chardes == store.pers_dict["Иззи"]:
                            pass
                        elif chardes == store.pers_dict["Фриск"]:
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Legate's{/font}" style "damage_text"
                        
                        else:
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Attack{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                        

                        # Мания
                        if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                            pass
                        else:
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Magic{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"

                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Dmg.Chance%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Crit.Rate%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Crit.Dmg%{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Defense{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Tank{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"
                        
                        # Отношения (только для Криса)
                        if chardes == store.pers_dict["Крис"]:
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Relations{/font}" xalign 0.0 at damage_gradient_gray style "damage_text"






                    vbox: #############################          значение характеристики
                        spacing 22 yoffset -5 xoffset 30 xalign 1.0

                        text "{size=50}{font=determination.otf}Cur/Base" yoffset -15 at damage_gradient_gray style "damage_text"


                        # Атака
                        # Отображение текущего значения цветом
                        if chardes == store.pers_dict["Иззи"]:
                            pass
                        elif chardes == store.pers_dict["Фриск"]:
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Secret{/font}" xalign 0.5 style "damage_text"
                        else:
                            if chardes and int(chardes.atk) < int(chardes.base_atk + chardes.base_atk_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.atk) == int(chardes.base_atk + chardes.base_atk_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.atk) > int(chardes.base_atk + chardes.base_atk_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.atk)]/[int((chardes.base_atk + chardes.base_atk_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            



                        # Магия
                        if chardes and chardes.name in ["Крис", "Чара", "Фриск"]:
                            pass
                        else:
                                
                            # Отображение текущего значения цветом
                            if chardes and int(chardes.magic) < int(chardes.base_magic + chardes.base_magic_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                            elif chardes and int(chardes.magic) == int(chardes.base_magic + chardes.base_magic_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                            elif chardes and int(chardes.magic) > int(chardes.base_magic + chardes.base_magic_mod):
                                text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.magic)]/[int((chardes.base_magic + chardes.base_magic_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                



                            
                        # Шанспопадания
                        if chardes and int(chardes.dmgchance * 100) < int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.dmgchance * 100) == int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.dmgchance * 100) > int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.dmgchance * 100)]/[int((chardes.base_dmgchance + chardes.dmgchance_mod) * 100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        

                            
                        # Отображение текущего значения цветом
                        if chardes and int(chardes.critrate * 100) < int((chardes.base_critrate + chardes.critrate_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.critrate * 100) == int((chardes.base_critrate + chardes.critrate_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.critrate * 100) > int((chardes.base_critrate + chardes.critrate_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.critrate * 100)]/[int((chardes.base_critrate + chardes.critrate_mod) * 100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                            


                            
                            
                        # Отображение текущего значения цветом
                        if chardes and int(chardes.crit * 100) < int((chardes.base_crit + chardes.crit_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.crit * 100) == int((chardes.base_crit + chardes.crit_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.crit * 100) > int((chardes.base_crit + chardes.crit_mod) * 100):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.crit * 100-100)]/[int((chardes.base_crit + chardes.crit_mod) * 100-100)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        



                            
                        # Отображение текущего значения цветом
                        if chardes and int(chardes.defense) < int(chardes.base_def + chardes.base_def_mod):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.defense) == int(chardes.base_def + chardes.base_def_mod):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.defense) > int(chardes.base_def + chardes.base_def_mod):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.defense)]/[int((chardes.base_def + chardes.base_def_mod))]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        

                        # Tank
                        # Отображение текущего значения цветом
                        if chardes and int(chardes.total_tank) < int(chardes.base_tank + chardes.extra_tank):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#ff0000" xalign 0.5 at damage_gradient_for_lowhp style "damage_text"
                        elif chardes and int(chardes.total_tank) == int(chardes.base_tank + chardes.extra_tank):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#ffffff" xalign 0.5 at damage_gradient_gray style "damage_text"
                        elif chardes and int(chardes.total_tank) > int(chardes.base_tank + chardes.extra_tank):
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}[int(chardes.total_tank)]/[int(chardes.base_tank + chardes.extra_tank)]{/font}" color "#00ff04" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                        
                        # Отношения (только для Криса)
                        if chardes == store.pers_dict["Крис"]:
                            # Определение словесного значения в зависимости от reltns
                            if chardes and hasattr(chardes, 'reltns'):
                                if chardes.reltns <= -80:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Hatred{/font}" xalign 0.5 color "#ff0000" at  damage_gradient_black style "damage_text"
                                elif chardes.reltns <= -60:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Awful{/font}" xalign 0.5 color "#ff4444" at  damage_gradient_black style "damage_text"
                                elif chardes.reltns <= -40:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Very Bad{/font}" xalign 0.5 color "#ff8888" at  damage_gradient_black style "damage_text"
                                elif chardes.reltns <= -20:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Bad{/font}" xalign 0.5 color "#ffaaaa" at  damage_gradient_black style "damage_text"
                                elif chardes.reltns >= 80:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Soulmate{/font}" xalign 0.5 color "#00ff00" at damage_gradient_green_bright style "damage_text"
                                elif chardes.reltns >= 60:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Excellent{/font}" xalign 0.5 color  "#44ff44" at damage_gradient_green_bright style "damage_text"
                                elif chardes.reltns >= 40:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Verygood{/font}" xalign 0.5 color  "#88ff88" at damage_gradient_green_bright style "damage_text"
                                elif chardes.reltns >= 20:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Good{/font}" xalign 0.5 color"#aaffaa" at damage_gradient_green_bright style "damage_text"
                                else:
                                    text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Normal{/font}" xalign 0.5 color "#e9e770" at damage_gradient_gray style "damage_text"
                    

                    vbox:

                        xoffset 120 yoffset -20
                        text "{size=50}{font=determination.otf}Buffs" xalign 0.5 at damage_gradient_gray style "damage_text"
                        
                        # Проверка дебаффов персонажа
                        if chardes.atk_debuff == 0 and chardes.def_debuff == 0 and chardes.magic_debuff == 0 and chardes.accuracy_debuff == 0 and chardes.critrate_debuff == 0 and chardes.critdmg_debuff == 0 and chardes.tank_debuff == 0 and chardes.bloodshed_debuff == 0 and chardes.prone_debuff == 0:
                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}---" xalign 0.5 yoffset 35 at damage_gradient_gray style "damage_text"
                        else:
                            vbox:
                                spacing 22 yoffset 30
                                # Проверка дебаффа кровотечения (Bloodshed)
                                if chardes.bloodshed_debuff != 0:
                                    if chardes.bloodshed_debuff > 0:
                                        hbox:
                                            xalign 0.5 yalign 0.5 spacing 0
                                            add "bloodshed.png" at damage_gradient
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}bloodshed(х[chardes.bloodshed_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    elif chardes.bloodshed_debuff < 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}bloodshed(х[-chardes.bloodshed_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа prone (состояние на земле)
                                if chardes.prone_debuff != 0:
                                    if chardes.prone_debuff > 0:
                                        hbox:
                                            xalign 0.5 yalign 0.5 spacing 0
                                            add "prone.png" at damage_gradient
                                            text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Prone(х[chardes.prone_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    elif chardes.prone_debuff < 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Prone(х[-chardes.prone_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа атаки
                                if chardes.atk_debuff != 0:
                                    if chardes.atk_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Exhaust(х[chardes.atk_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Cheerful(х[-chardes.atk_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа защиты
                                if chardes.def_debuff != 0:
                                    if chardes.def_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Sorrow(х[chardes.def_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Inspired(х[-chardes.def_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа магии
                                if chardes.magic_debuff != 0:
                                    if chardes.magic_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Foggyminded(х[chardes.magic_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Enlighted(х[-chardes.magic_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа точности
                                if chardes.accuracy_debuff != 0:
                                    if chardes.accuracy_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Feared(х[chardes.accuracy_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Focused(х[-chardes.accuracy_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа шанса крита
                                if chardes.critrate_debuff != 0:
                                    if chardes.critrate_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Unluck(х[chardes.critrate_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Luck(х[-chardes.critrate_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа урона крита
                                if chardes.critdmg_debuff != 0:
                                    if chardes.critdmg_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Apathy(х[chardes.critdmg_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Anger(х[-chardes.critdmg_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                                # Проверка дебаффа танка
                                if chardes.tank_debuff != 0:
                                    if chardes.tank_debuff > 0:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Vulnerable(х[chardes.tank_debuff])" xalign 0.5 at  damage_gradient style "damage_text"
                                    else:
                                        text "{size=[int(40*multiply_for_text) if multiply_for_text > 0 else 40]}{font=determination.otf}Stealth(х[-chardes.tank_debuff])" xalign 0.5 at damage_gradient_green_bright style "damage_text"
                                
                
    if sscreenstate_style == "статический" and bottom_x_shown == 1:
        
        imagebutton:
            at fullstats1_3
            #at semiblack_dynamic_alpha
            idle "closestatdesc.png"
            hover "closestatdesc_hover.png"
            action [ SetVariable("sscreenstate_style", 0), SetVariable("chardespos", 0), SetVariable("bottom_x_shown", 0), SetVariable("screenstate", "недоступен"), Hide("fullstats1"), Hide("fullstats0")]

transform fullstats1_3:
    zoom 2 alpha 0.0 xpos 1150 ypos 10
    easein 0.5 alpha 1.0
    
