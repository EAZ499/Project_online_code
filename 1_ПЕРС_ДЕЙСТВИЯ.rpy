default base_nego_perform = 0
default dip_multiply = 1
default try_to_nego_result = False
default nego_total_score = 0
default nego_difficulty = 0
default nego_selected_stat_name = "-"
default nego_selected_stat_value = 0
default nego_social_value = 0
default nego_charm_value = 0
default display_nego_value = 0

default act_code = None














init python:
    ACTS_CONFIG = {
        "Оценить":    {"check": "perception", "social": True,  "progress_key": "evaluate_progress",
                        "hero_router": "check_hero_reaction",     "enemy_router": "check_enemy_reaction"},
        "Вопрос":     {"check": "perception", "social": True,  "progress_key": "question_progress",
                        "hero_router": "ask_hero_reaction",       "enemy_router": "ask_enemy_reaction"},
        "Убеждение":  {"check": "rhetoric",   "social": True,  "progress_key": "persuasion_progress",
                        "hero_router": "argue_hero_reaction",     "enemy_router": "argue_enemy_reaction"},
        "Рассказать": {"check": "rhetoric",   "social": True,  "progress_key": "tell_progress",
                        "hero_router": "tell_hero_reaction",      "enemy_router": "tell_enemy_reaction"},
        "Поддержать": {"check": "comfort",    "social": True,  "progress_key": "support_progress",
                        "hero_router": "support_hero_reaction",   "enemy_router": "support_enemy_reaction"},
        "Играть":     {"check": "comfort",    "social": True,  "progress_key": "play_progress",
                        "hero_router": "play_hero_reaction",      "enemy_router": "play_enemy_reaction"},
        "Исполнение": {"check": "artistry",   "social": True,  "progress_key": "perform_progress",
                        "hero_router": "perform_hero_reaction",   "enemy_router": "perform_enemy_reaction"},
        "Унижаться":  {"check": "artistry",   "social": True,  "progress_key": "humiliate_progress",
                        "hero_router": "humiliate_hero_reaction", "enemy_router": "humiliate_enemy_reaction"},
        "Дразнить":   {"check": "artistry",   "social": True,  "progress_key": "tease_progress",
                        "hero_router": "tease_hero_reaction",     "enemy_router": "tease_enemy_reaction"},
        "Запугать":   {"check": "power",      "social": True,  "progress_key": "intimidate_progress",
                        "hero_router": "scare_hero_reaction",     "enemy_router": "scare_enemy_reaction"},
        "Грубить":    {"check": "power",      "social": True,  "progress_key": "rude_progress",
                        "hero_router": "rude_hero_reaction",      "enemy_router": "rude_enemy_reaction"},
        "Пощадить":   {"check": "power",      "social": False, "progress_key": "spare_progress_action",
                        "hero_router": None,                      "enemy_router": None},
    }

    ACT_STAT_RU = {
        "perception": "Восприятие",
        "rhetoric": "Риторика",
        "comfort": "Комфорт",
        "artistry": "Артистизм",
        "power": "Власть",
    }




    HERO_LATIN_NAMES = {
        "Крис":     "kris",
        "Азриель":  "azriel",
        "Чара":     "chara",
        "Фриск":    "frisk",
        "Иззи":     "izzy",
        "Кловер":   "clover",
        "Седрик":   "sedric",
        "Сильвия":  "sylvia",
    }
    ENEMY_LATIN_NAMES = {
        "Тревор":   "trevor",
        "Джевил":   "jevil",
        "Манекен":  "dummy",
        "Манекен 2":"dummy2",
        # добавляй сюда новых врагов
    }



    def apply_enemy_act_mechanics(action_name):
        """Вся механика применения действия к врагу.

        Делает ровно то, что раньше копипастилось в каждом файле 2.x:
            - помечает действие нажатым в журнале текущего настроения,
            - сдвигает spare_progress по mood_action_spare_effects,
            - увеличивает action_progress[progress_key] на 1,
            - добавляет дипломатический вклад,
            - уведомляет о достижении spare_max.

        При провале проверки (try_to_nego_result=False) — не делает ничего.
        Для не-врагов — не делает ничего.
        """
        target = getattr(store, "target", None)
        if target is None:
            return

        # Только для врагов
        if not any(target is e for e in store.enemies.values()):
            return

        # Только при успехе
        if not store.try_to_nego_result:
            return

        cfg = store.ACTS_CONFIG.get(action_name, {})
        progress_key = cfg.get("progress_key")

        attacker_names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск",
                            5: "Иззи", 6: "Кловер", 7: "Седрик", 8: "Арчи", 9: "Сильвия",
                            10: "Фабри", 11: "Эмили", 12: "Сьюзи", 13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
        attacker = store.pers_dict.get(attacker_names.get(store.current_attacker))
        if attacker is None:
            return

        target.spare_max = store.get_enemy_spare_max(target)

        # 1) Пометить действие нажатым и сдвинуть spare_progress по таблице.
        store.apply_act_to_enemy(target, action_name, True)

        # 2) Прогресс самого действия.
        if progress_key and progress_key in target.action_progress:
            target.action_progress[progress_key] += 1

        # 3) Дипломатический вклад (как было раньше).
        target.spare_progress = min(
            target.spare_progress + attacker.diplomacy * store.dip_multiply,
            target.spare_max
        )
        store.process_enemy_routes(target, action_name)

        # 4) Уведомление о готовности к пощаде.
        if target.spare_progress >= target.spare_max:
            renpy.notify("%s готов(а) к пощаде!" % target.name)






transform alpha_hero_act_1:
    yoffset -40 alpha 0.0
    easein 0.5 yoffset 0 alpha 1.0

transform alpha_hero_act_bg:
    alpha 0.0
    easein 0.5 alpha 1.0

default random_number_for_social_fake = 1

screen hero_acts_perform:
    zorder 999999
    #modal True
    timer 0.05 action SetVariable("random_number_for_social_fake", renpy.random.randint(1,30)) repeat True
    add "semiblackbg" at alpha_hero_act_bg
    vbox:
        at alpha_hero_act_1
        xalign 0.5
        yalign 0.4
        spacing 20
        vbox:
            
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                xysize (280, 140)
                padding (5, 5)
                frame:
                    xalign 0.5
                    background "#000000"
                    xysize (270, 130)
                    text "Сложность\n[int(nego_difficulty)]" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5



        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                padding (5, 5)
                frame:
                    background "#000000"
                    xysize (260, 120)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        text "[int(random_number_for_social_fake or 1)]" size 52 color "#ffffff" xalign 0.5 yalign 0.5

        hbox:
            xalign 0.5
            spacing 35
            if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
                frame:
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        
                        vbox:
                            xalign 0.5
                            text "Социализация" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.socialization)]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "[nego_selected_stat_name]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "Очарование" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.charm)]%" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

        #textbutton "Начать" action [Hide("hero_acts_perform"), Show("hero_acts_perform_base")]
        frame:
            background "#ffffff"
            padding (5, 5)
            button:
                at begin_act
                background "#000000"
                xysize (870, 60)
                text "Начать" xalign 0.5 yalign 0.5 size 45 
                action [Hide("hero_acts_perform"), Jump("perform_act")]


transform begin_act:
    on hover:
        block:        
            easein 0.5 matrixcolor TintMatrix("#ffffff")
            easeout 0.7 matrixcolor TintMatrix("#ffff00")
            repeat
    on idle:  
        easein 1.0 matrixcolor TintMatrix("#ffffff")          


transform value_zoom:
    easein 0.5 zoom 1.05
    easeout 0.5 zoom 1.0

transform all_in_to_down:
    easein 0.385 yoffset 35

transform Nullaction_to_zero:
    easein 0.385 alpha 0.0

transform to_yellow_075:
    easein 0.385 matrixcolor TintMatrix("#ffff00")

screen hero_acts_perform_base:
    zorder 999999
    add "semiblackbg"
    #timer 2.0 action [Hide("hero_acts_perform_base"), Jump("perform_act2")]
    #modal True
    vbox:
        
        at all_in_to_down


        xalign 0.5
        yalign 0.4
        spacing 20
        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                xysize (280, 140)
                padding (5, 5)
                frame:
                    xalign 0.5
                    background "#000000"
                    xysize (270, 130)
                    text "Сложность\n[int(nego_difficulty)]" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5

        
        vbox:
            at value_zoom
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                padding (5, 5)
                frame:
                    background "#000000"
                    xysize (260, 120)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        if display_nego_value >= nego_difficulty:
                            text "[int(display_nego_value)]" size 48 color "#56d15c"
                        else:
                            text "[int(display_nego_value)]" size 48 color "#da4747"


        hbox:
            xalign 0.5
            spacing 35
            if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
                vbox:
                    xalign 0.5
                    frame:
                        xalign 0.5
                        background "#ffffff"
                        padding (5, 5)
                        frame:
                            background "#000000"
                            xysize (260, 80)
                            vbox:
                                xalign 0.5
                                text "Социализация" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                                text "[int(attacker.socialization)]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "[nego_selected_stat_name]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "Очарование" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.charm)]%" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

        frame:
            at Nullaction_to_zero
            background "#ffffff"
            padding (5, 5)
            button:                
                background "#000000"
                xysize (870, 60)
                text "Начать" xalign 0.5 yalign 0.5 size 45 at to_yellow_075
                action NullAction()


transform number1_soc:
    xoffset 0 yoffset -40
    linear 0.385 xoffset 300 yoffset -200 alpha 0.0
transform number1_box:
    easein 0.385 xoffset 20 yoffset -20
    easeout 0.385 xoffset 0 yoffset 0



screen hero_acts_perform_social:
    zorder 999999
    add "semiblackbg"
    #timer 2.0 action [Hide("hero_acts_perform_base"), Jump("perform_act2")]
    #modal True
    vbox:
        


        xalign 0.5
        yalign 0.4
        spacing 20
        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                xysize (280, 140)
                padding (5, 5)
                frame:
                    xalign 0.5
                    background "#000000"
                    xysize (270, 130)
                    text "Сложность\n[int(nego_difficulty)]" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5



        vbox:
            at value_zoom
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                padding (5, 5)
                frame:
                    background "#000000"
                    xysize (260, 120)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        if display_nego_value >= nego_difficulty:
                            text "[int(display_nego_value)]" size 48 color "#56d15c"
                        else:
                            text "[int(display_nego_value)]" size 48 color "#da4747"

        hbox:
            spacing 35
            if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
                vbox:
                    at number1_box
                    xalign 0.5
                    frame:
                        xalign 0.5
                        background "#ffffff"
                        padding (5, 5)
                        frame:
                            background "#000000"
                            xysize (260, 80)
                            vbox:
                                xalign 0.5
                                text "Социализация" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                                text "[int(attacker.socialization)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                                text "[int(attacker.socialization)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5 at number1_soc

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "[nego_selected_stat_name]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "Очарование" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.charm)]%" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5


transform number2_soc:
    xoffset 0 yoffset -40
    linear 0.385 yoffset -200 alpha 0.0
transform number2_box:
    easein 0.385 yoffset -20
    easeout 0.385 yoffset 0


screen hero_acts_perform_characteristic:
    zorder 999999
    add "semiblackbg"
    #modal True
    vbox:
        


        xalign 0.5
        yalign 0.4
        spacing 20
        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                xysize (280, 140)
                padding (5, 5)
                frame:
                    xalign 0.5
                    background "#000000"
                    xysize (270, 130)
                    text "Сложность\n[int(nego_difficulty)]" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5


        vbox:
            at value_zoom
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                padding (5, 5)
                frame:
                    background "#000000"
                    xysize (260, 120)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        if display_nego_value >= nego_difficulty:
                            text "[int(display_nego_value)]" size 48 color "#56d15c"
                        else:
                            text "[int(display_nego_value)]" size 48 color "#da4747"
            
        hbox:
            spacing 35

            if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
                vbox:
                    
                    xalign 0.5
                    frame:
                        xalign 0.5
                        background "#ffffff"
                        padding (5, 5)
                        frame:
                            background "#000000"
                            xysize (260, 80)
                            vbox:
                                xalign 0.5
                                text "Социализация" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                                text "[int(attacker.socialization)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5 

            vbox:
                at number2_box
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "[nego_selected_stat_name]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5 at number2_soc

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "Очарование" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.charm)]%" color "#ffffff" size 30 xalign 0.5 yalign 0.5 text_align 0.5

transform charm_cool:
    easein 0.385 matrixcolor TintMatrix("#00ff00") zoom 1.05
    easeout 0.385 matrixcolor TintMatrix("#ffffff") zoom 1.00

screen hero_acts_perform_charm_true:
    zorder 999999
    add "semiblackbg"
    #modal True
    vbox:



        xalign 0.5
        yalign 0.4
        spacing 20
        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                xysize (280, 140)
                padding (5, 5)
                frame:
                    xalign 0.5
                    background "#000000"
                    xysize (270, 130)
                    text "Сложность\n[int(nego_difficulty)]" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5



        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                padding (5, 5)
                frame:
                    background "#000000"
                    xysize (260, 120)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        if display_nego_value >= nego_difficulty:
                            text "[int(display_nego_value)]" size 48 color "#56d15c"
                        else:
                            text "[int(display_nego_value)]" size 48 color "#da4747"


        hbox:
            spacing 35
            if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
                vbox:
                    xalign 0.5
                    frame:
                        xalign 0.5
                        background "#ffffff"
                        padding (5, 5)
                        frame:
                            background "#000000"
                            xysize (260, 80)
                            vbox:
                                xalign 0.5
                                text "Социализация" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                                text "[int(attacker.socialization)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "[nego_selected_stat_name]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                at charm_cool
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "Очарование" color "#88ff88" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.charm)]%" color "#88ff88" size 30 xalign 0.5 yalign 0.5 text_align 0.5


transform charm_bad:
    pause 0.1
    easein 0.35 matrixcolor TintMatrix("#ff0000")
    easeout 0.35 alpha 0.0 yoffset 50

screen hero_acts_perform_charm_false:
    zorder 999999
    add "semiblackbg"
    #modal True
    vbox:


        xalign 0.5
        yalign 0.4
        spacing 20
        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                xysize (280, 140)
                padding (5, 5)
                frame:
                    xalign 0.5
                    background "#000000"
                    xysize (270, 130)
                    text "Сложность\n[int(nego_difficulty)]" size 36 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5



        vbox:
            xalign 0.5
            frame:
                xalign 0.5
                background "#ffffff"
                padding (5, 5)
                frame:
                    background "#000000"
                    xysize (260, 120)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        if nego_difficulty < display_nego_value:
                            text "[int(display_nego_value)]" size 48 color "#66ff66"
                        else:
                            text "[int(display_nego_value)]" size 48 color "#ff8888"
        hbox:
            spacing 35
            if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
                vbox:
                    xalign 0.5
                    frame:
                        xalign 0.5
                        background "#ffffff"
                        padding (5, 5)
                        frame:
                            background "#000000"
                            xysize (260, 80)
                            vbox:
                                xalign 0.5
                                text "Социализация" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                                text "[int(attacker.socialization)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                xalign 0.5
                frame:
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "[nego_selected_stat_name]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(nego_selected_stat_value)]" color "#ffee55" size 30 xalign 0.5 yalign 0.5 text_align 0.5

            vbox:
                
                xalign 0.5
                frame:
                    at charm_bad
                    xalign 0.5
                    background "#ffffff"
                    padding (5, 5)
                    frame:
                        background "#000000"
                        xysize (260, 80)
                        vbox:
                            xalign 0.5
                            text "Очарование" color "#ff5555" size 30 xalign 0.5 yalign 0.5 text_align 0.5
                            text "[int(attacker.charm)]%" color "#ff5555" size 30 xalign 0.5 yalign 0.5 text_align 0.5








label hero_acts:
    
    hide screen Heroattacks
    if isinstance(attackindex, str) and attackindex in ACTS_CONFIG:
        $ cfg = ACTS_CONFIG[attackindex]
        $ nego_selected_stat_name = ACT_STAT_RU.get(cfg["check"], cfg["check"])
        # Получаем имя персонажа по индексу
        $ attacker_name = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"][current_attacker - 1]
        # Получаем объект персонажа из словаря
        $ attacker = store.pers_dict[attacker_name]
        $ nego_selected_stat_value = int(getattr(attacker, cfg["check"], 0))
        $ nego_social_value = int(attacker.socialization if cfg["social"] else 0)
    else:
        $ nego_selected_stat_name = "-"
        $ nego_selected_stat_value = 0
        $ nego_social_value = 0

    if target and hasattr(target, 'base_difficulty') and isinstance(attackindex, str) and attackindex in ACTS_CONFIG:
        $ mood = getattr(target, "mood", "neutral")
        $ stat_key = ACTS_CONFIG[attackindex]["check"]
        $ mod_map = getattr(target, stat_key + "_difficulty_mod", {})
        $ nego_difficulty = int(target.base_difficulty + mod_map.get(mood, 0))
        if getattr(target, "name", None) == "Арчи":
            $ nego_difficulty = archie_difficulty(target, attackindex)
    else:
        $ nego_difficulty = 0
    
    # Получаем имя персонажа по индексу
    $ attacker_name = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"][current_attacker - 1]
    # Получаем объект персонажа из словаря
    $ attacker = store.pers_dict[attacker_name]

    call screen hero_acts_perform


















label perform_act:
    hide screen hero_acts_perform
    hide screen Heroattacks

    # === СПЕЦИАЛЬНЫЙ СЛУЧАЙ: «Пощадить» без проверок ===
    if attackindex == "Пощадить":
        jump perform_spare

    if isinstance(attackindex, str) and attackindex in ACTS_CONFIG:
        $ act_code = ACTS_CONFIG[attackindex].get("act_code", None)
    else:
        $ act_code = None

    # Санс использует свой кубик d30 вместо d20.
    $ base_nego_perform = renpy.random.randint(1, 30 if current_attacker == 15 else 20)
    $ display_nego_value = base_nego_perform

    show screen hero_acts_perform_base
    
    pause 1.0

    #label perform_act2:
    #$ renpy.pause(0.5, hard=True)
    hide screen hero_acts_perform_base
    #"{alpha=0.0}{fast}.{nw}"
    

    if isinstance(attackindex, str) and attackindex in ACTS_CONFIG and ACTS_CONFIG[attackindex]["social"]:
        $ display_nego_value = display_nego_value + nego_social_value

    show screen hero_acts_perform_social
    pause 1.0
    #$ renpy.pause(0.5, hard=True)

    #label perform_act3:
    hide screen hero_acts_perform_social
    
    #"{alpha=0.0}{fast}.{nw}"

    $ display_nego_value = display_nego_value + nego_selected_stat_value

    show screen hero_acts_perform_characteristic
    pause 1.0
    #$ renpy.pause(0.5, hard=True)
    hide screen hero_acts_perform_characteristic
    #"{alpha=0.0}{fast}.{nw}"

    # Получаем имя персонажа по индексу
    $ attacker_name = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"][current_attacker - 1]
    # Получаем объект персонажа из словаря
    $ attacker = store.pers_dict[attacker_name]
    $ try_to_nego_result = attacker.try_to_nego(target)
    # «Образ принца»: первый провал Азриеля обнуляет бонус социализации и власти.
    $ azri_on_action_result(attacker, try_to_nego_result)

    if try_to_nego_result == True and dip_multiply == 2:
        show screen hero_acts_perform_charm_true
        pause 1.4
        #$ renpy.pause(0.5, hard=True)
        hide screen hero_acts_perform_charm_true
    else:
        show screen hero_acts_perform_charm_false
        pause 1.4
        #$ renpy.pause(0.5, hard=True)
        hide screen hero_acts_perform_charm_false

    window show
    #show image "gui/textbox.png" 

    # current_attacker хранит номер персонажа, поэтому сначала
    # получаем имя, а затем объект персонажа из pers_dict.
    $ attacker_party_order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"]
    $ attacker_name = attacker_party_order[current_attacker - 1]
    $ attacker = store.pers_dict[attacker_name]
    $ attacker.state = "act"

    "сейчас должен быть прыжок"
    kris "Ну го, чё"
    $ attacker_party_order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"]
    $ attacker_name = attacker_party_order[current_attacker - 1]
    $ attacker = store.pers_dict[attacker_name]
    $ attacker.state = "act"

    kris "Ну го, чё"

    # ▼▼▼ УНИВЕРСАЛЬНЫЙ ДИСПЕТЧЕР ▼▼▼
    # Внутри:
    #   1) определяет attacker и target;
    #   2) если цель — враг и проверка успешна:
    #      помечает действие нажатым, двигает action_progress и spare_progress;
    #   3) вызывает hero_router или enemy_router из ACTS_CONFIG;
    #   4) jump finish_act.
    call act_dispatch(attackindex) from _call_act_dispatch







# =====================================================================
#  УНИВЕРСАЛЬНЫЙ ДИСПЕТЧЕР ACT-ДЕЙСТВИЙ
#
#  Вызывается из perform_act. Сам решает:
#    - кто атакующий и кто цель;
#    - если цель — враг и проверка успешна, применяет механику
#      (журнал настроений + пощада + action_progress);
#    - вызывает нужный роутер реакций (hero/enemy) через
#      call expression;
#    - уходит на finish_act.
#
#  Всё, что нужно файлу действия — определить два лейбла:
#     <base>_hero_reaction  — реакция, если цель герой
#     <base>_enemy_reaction — реакция, если цель враг
#  Имена берутся из ACTS_CONFIG[action_name]["hero_router"/"enemy_router"].
# =====================================================================
label act_dispatch(action_name):

    $ attacker_names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск",
                    5: "Иззи", 6: "Кловер", 7: "Седрик", 8: "Арчи", 9: "Сильвия", 10: "Фабри", 11: "Эмили", 12: "Сьюзи", 13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
    $ attacker_name = attacker_names.get(current_attacker)
    $ attacker = store.pers_dict.get(attacker_name) if attacker_name else None

    if target is None or attacker is None:
        jump finish_act

    $ cfg = ACTS_CONFIG.get(action_name, None)
    if cfg is None:
        jump finish_act

    $ progress_key = cfg.get("progress_key", None)
    $ hero_router   = cfg.get("hero_router",   None)
    $ enemy_router  = cfg.get("enemy_router",  None)

    $ target_is_hero  = any(target is h for h in store.pers_dict.values())
    $ target_is_enemy = any(target is e for e in store.enemies.values())

    # Единая точка применения прогресса и эффектов переговоров.
    if target_is_enemy:
        if target.name == "Арчи":
            $ apply_act_to_enemy(target, action_name, try_to_nego_result)
            $ archie_apply_act(target, attacker, action_name, try_to_nego_result)
        elif target.name in ("Фроглин", "Фрогетта", "Фрогестер", "Фрогис"):
            $ apply_act_to_enemy(target, action_name, try_to_nego_result)
            $ frog_apply_act(target, attacker, action_name, try_to_nego_result)
            $ renpy.notify("[target.name]: [target.spare_progress]/[target.spare_max]")
        else:
            $ apply_enemy_act_mechanics(action_name)

    # --- ЦЕЛЬ: ГЕРОЙ ---
    if target_is_hero and hero_router:
        call expression hero_router pass (attacker_name, target) from _call_act_hero

    # --- ЦЕЛЬ: ВРАГ ---
    elif target_is_enemy and enemy_router:
        call expression enemy_router pass (attacker_name, target) from _call_act_enemy




































# Эффект действия на пощаду в зависимости от НАСТРОЕНИЯ врага.
# >0 — зелёный (даёт положительный эффект)
#  0 — жёлтый (ничего не даёт)
# <0 — красный (ухудшает положение дел)
#
# Если действие ещё НЕ нажималось при данном настроении — кнопка остаётся белой.
default mood_action_spare_effects = {
    "neutral": {
        "Оценить":    0,
        "Вопрос":     1,
        "Убеждение":  1,
        "Рассказать": 0,
        "Поддержать": 1,
        "Играть":     1,
        "Запугать":  -1,
        "Грубить":   -1,
        "Исполнение": 1,
        "Унижаться":  0,
        "Дразнить":  -1,
        "Пощадить":   2,
    },
    "sad": {
        "Оценить":    0,
        "Вопрос":     0,
        "Убеждение": -1,
        "Рассказать": 1,
        "Поддержать": 2,
        "Играть":     1,
        "Запугать":  -2,
        "Грубить":   -1,
        "Исполнение": 2,
        "Унижаться":  1,
        "Дразнить":  -2,
        "Пощадить":   2,
    },
    "happy": {
        "Оценить":    0,
        "Вопрос":     1,
        "Убеждение":  1,
        "Рассказать": 0,
        "Поддержать": 1,
        "Играть":     2,
        "Запугать":  -2,
        "Грубить":   -2,
        "Исполнение": 2,
        "Унижаться":  0,
        "Дразнить":  -1,
        "Пощадить":   2,
    },
    "angry": {
        "Оценить":    0,
        "Вопрос":    -1,
        "Убеждение": -2,
        "Рассказать": 0,
        "Поддержать": 0,
        "Играть":    -1,
        "Запугать":  -2,
        "Грубить":   -2,
        "Исполнение": 1,
        "Унижаться": -1,
        "Дразнить":  -2,
        "Пощадить":   1,
    },
    "feared": {
        "Оценить":    0,
        "Вопрос":     1,
        "Убеждение":  0,
        "Рассказать": 0,
        "Поддержать": 2,
        "Играть":    -1,
        "Запугать":   1,
        "Грубить":   -1,
        "Исполнение": 1,
        "Унижаться":  2,
        "Дразнить":  -1,
        "Пощадить":   2,
    },

    # НОВОЕ: смущён, потерян.
    # Логика не доходит — убеждать бесполезно. Зато он открыт для поддержки
    # и не хочет агрессии: запугивание и дразнилки только усугубляют.
    "confused": {
        "Оценить":    0,
        "Вопрос":     0,   # он сам не понимает, что отвечает
        "Убеждение": -1,   # логика не заходит
        "Рассказать": 1,   # хоть что-то понятное
        "Поддержать": 2,   # лучшее, что можно сделать
        "Играть":     1,
        "Запугать":  -2,
        "Грубить":   -2,
        "Исполнение": 1,
        "Унижаться":  1,   # показать уязвимость — сработает
        "Дразнить":  -2,
        "Пощадить":   2,
    },

    # НОВОЕ: задумчив.
    # Он готов думать и слушать, но не терпит давления.
    # Вопрос и разговор заходят лучше всего. Исполнение/унижение — на грани.
    "thoughtful": {
        "Оценить":    1,   # сам себя оценивает, интересно
        "Вопрос":     2,   # готов отвечать
        "Убеждение":  1,   # можно достучаться, но осторожно
        "Рассказать": 2,
        "Поддержать": 1,
        "Играть":     0,
        "Запугать":  -2,
        "Грубить":   -2,
        "Исполнение": 1,
        "Унижаться":  0,
        "Дразнить":  -1,
        "Пощадить":   2,
    },

    # НОВОЕ: усталый.
    # Как у sad, но мягче: поддержка/рассказ помогают, давление бесит меньше.
    "tired": {
        "Оценить":    0,
        "Вопрос":     0,
        "Убеждение":  0,
        "Рассказать": 1,
        "Поддержать": 2,
        "Играть":     0,
        "Запугать":  -1,
        "Грубить":   -1,
        "Исполнение": 1,
        "Унижаться":  1,
        "Дразнить":  -1,
        "Пощадить":   2,
    },
}

# Индивидуальные (персональные) реакции противника на конкретного атакующего.
# Если для (враг, настроение, действие, атакующий) есть запись —
# именно она используется вместо базовой mood_action_spare_effects.
#
# Иерархия:
#   1. mood_action_spare_effects_by_char[враг][настроение][действие][атакующий]
#   2. mood_action_spare_effects[настроение][действие]
#
# Значение — целое число: >0 зелёная кнопка, 0 жёлтая, <0 красная.
default mood_action_spare_effects_by_char = {
    "Тревор": {
        "neutral": {
            # Азриель пытается «Убедить» нейтрального Тревора — срабатывает в минус,
            # хотя для остальных убеждение нейтрально (+1).
            "Убеждение": {
                "Азриель": -1,
            },
            # Пример: Крис и «Рассказать» — наоборот, даёт +1 (у остальных 0).
            "Рассказать": {
                "Крис": 1,
            },
        },
        "angry": {
            # В ярости Тревор особенно не выносит именно Азриеля.
            "Поддержать": {
                "Азриель": -2,
                "Чара":    -1,
            },
        },
        "confused": {
            # Когда Тревор смущён, Крис — единственный, кому он ещё верит.
            "Убеждение": {
                "Крис": 1,
            },
        },
    },

     # Шаблон для других врагов — оставь пустым или дополни по мере надобности.
     "ДжевилV1": {},
     "Психолог": {},
     "Спамтон":  {},
     "Арчи":     {},
     "Фроглин": {
         "happy": {
             "Убеждение":  {"default":  1},
             "Рассказать": {"default":  1},
             "Поддержать": {"default":  0},
             "Играть":     {"default":  1},
             "Запугать":   {"default": -1},
             "Грубить":    {"default": -1},
             "Исполнение": {"default":  0},
             "Дразнить":   {"default":  0},
         },
     },
     "Фрогетта": {
         "happy": {
             "Убеждение":  {"default":  0},
             "Рассказать": {"default":  0},
             "Поддержать": {"default":  1},
             "Играть":     {"default":  1},
             "Запугать":   {"default": -1},
             "Грубить":    {"default": -1},
             "Исполнение": {"default":  0},
             "Дразнить":   {"default":  1},
         },
     },
     "Фрогестер": {
         "happy": {
             "Убеждение":  {"default":  0},
             "Рассказать": {"default":  0},
             "Поддержать": {"default":  1},
             "Играть":     {"default":  1},
             "Запугать":   {"default": -1},
             "Грубить":    {"default": -1},
             "Исполнение": {"default":  1},
             "Дразнить":   {"default": -1},
         },
     },
     "Фрогис": {
         "happy": {
             "Убеждение":  {"default": -1},
             "Рассказать": {"default":  0},
             "Поддержать": {"default":  0},
             "Играть":     {"default":  0},
             "Запугать":   {"default":  0},
             "Грубить":    {"default": -1},
             "Исполнение": {"default":  0},
             "Дразнить":   {"default": -1},
         },
     },
}

# Список допустимых настроений (используется для инициализации словарей)
default MOODS_LIST = ("neutral", "sad", "happy", "angry", "feared", "confused", "thoughtful", "tired")



init python:
    ALL_MOODS = ("neutral", "sad", "happy", "angry", "feared", "confused", "thoughtful", "tired")

    def _ensure_mood_action_used(entity):
        """Гарантирует наличие журналов: used, revealed и izzy_revealed."""
        if not hasattr(entity, "mood_action_used") or not isinstance(entity.mood_action_used, dict):
            entity.mood_action_used = {m: {} for m in ALL_MOODS}
        else:
            for m in ALL_MOODS:
                entity.mood_action_used.setdefault(m, {})

        if not hasattr(entity, "mood_action_revealed") or not isinstance(entity.mood_action_revealed, dict):
            entity.mood_action_revealed = {m: {} for m in ALL_MOODS}
        else:
            for m in ALL_MOODS:
                entity.mood_action_revealed.setdefault(m, {})

        if not hasattr(entity, "izzy_revealed_mood_actions") or not isinstance(entity.izzy_revealed_mood_actions, dict):
            entity.izzy_revealed_mood_actions = {m: {} for m in ALL_MOODS}
        else:
            for m in ALL_MOODS:
                entity.izzy_revealed_mood_actions.setdefault(m, {})

    def get_act_spare_effect(enemy, action_name, attacker_name=None):
        """
        Возвращает эффект на spare_progress для конкретной пары
        (враг, действие, атакующий) с учётом текущего настроения.

        Приоритет:
          1. Тревор — trevor_act_effects.
          2. Индивидуальное переопределение mood_action_spare_effects_by_char.
          3. Базовое значение mood_action_spare_effects.
        """
        if enemy is None:
            return 0

        if getattr(enemy, "name", None) == "Тревор":
            return trevor_get_effect(enemy, action_name, attacker_name)

        enemy_name = getattr(enemy, "name", None)
        mood = getattr(enemy, "mood", "neutral")

        # Для Арчи прогресс и откаты задаются его собственным деревом.
        if enemy_name == "Арчи":
            return 0

        if enemy_name and attacker_name:
            char_overrides = mood_action_spare_effects_by_char.get(enemy_name, {})
            mood_overrides = char_overrides.get(mood, {})
            action_overrides = mood_overrides.get(action_name, {})
            if attacker_name in action_overrides:
                return action_overrides[attacker_name]

        return mood_action_spare_effects.get(mood, {}).get(action_name, 0)

    def get_current_attacker_name():
        attacker = getattr(store, "current_attacker", None)
        if attacker is None:
            return None
        if hasattr(attacker, "name"):
            return attacker.name
        order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Сильвия"]
        if isinstance(attacker, int) and 0 < attacker <= len(order):
            return order[attacker - 1]
        return None

    def set_enemy_mood(enemy, new_mood):
        if enemy is None:
            return
        _ensure_mood_action_used(enemy)
        if new_mood not in ALL_MOODS:
            return
        mood_changed = getattr(enemy, "mood", None) != new_mood
        enemy.mood = new_mood
        if mood_changed:
            # Новый этап требует повторного осмотра, даже если настроение
            # уже встречалось в старом бою или старом сохранении.
            enemy.mood_action_used[new_mood] = {}
            enemy.mood_action_revealed[new_mood] = {}
            enemy.izzy_revealed_mood_actions[new_mood] = {}
        else:
            enemy.mood_action_used.setdefault(new_mood, {})
            enemy.mood_action_revealed.setdefault(new_mood, {})

    def get_act_button_color(action_name):
        """Возвращает hex‑цвет для текста кнопки действия.

        Белый   — ещё не нажимали при текущем настроении цели.
        Зелёный — эффект на пощаду > 0.
        Жёлтый  — эффект на пощаду == 0.
        Красный — эффект на пощаду < 0.
        """
        target = getattr(store, "target", None)
        if target is None:
            return "#FFFFFF"

        # ▼▼▼ ЭТИ ДВЕ КНОПКИ ВСЕГДА БЕЛЫЕ ▼▼▼
        if action_name in ("Пощадить", "Оценить"):
            return "#FFFFFF"

        _ensure_mood_action_used(target)
        mood = getattr(target, "mood", "neutral")
        used     = target.mood_action_used.get(mood, {}).get(action_name, False)
        revealed = target.mood_action_revealed.get(mood, {}).get(action_name, False)

        # Ни нажато, ни разведано — белая кнопка.
        if not used and not revealed:
            return "#FFFFFF"

        attacker_name = get_current_attacker_name()
        effect = get_act_spare_effect(target, action_name, attacker_name)

        if effect > 0:
            return "#66FF66"   # зелёный
        elif effect < 0:
            return "#FF6666"   # красный
        return "#FFFF66"       # жёлтый

    def reveal_random_acts_to_enemy(enemy, count=2):
        """Помечает count случайных действий как «разведанных» для текущего настроения.

        Разведённое действие отображается цветом, как будто его уже нажимали,
        но НЕ считается нажатым и не влияет на spare_progress / action_progress.

        Возвращает список разведанных действий.
        """
        if enemy is None:
            return []

        _ensure_mood_action_used(enemy)
        mood = getattr(enemy, "mood", "neutral")
        used     = enemy.mood_action_used.setdefault(mood, {})
        revealed = enemy.mood_action_revealed.setdefault(mood, {})

        # Пул — все действия из ACTS_CONFIG, кроме самого «Оценить».
        # Если хочешь исключить «Пощадить» из разведки — добавь его в исключения.
        all_acts = [a for a in store.ACTS_CONFIG.keys() if a not in ("Оценить", "Пощадить")]

        candidates = [
            a for a in all_acts
            if not used.get(a, False) and not revealed.get(a, False)
        ]
        if not candidates:
            return []

        import random as _random
        picked = _random.sample(candidates, min(count, len(candidates)))
        for a in picked:
            revealed[a] = True
        return picked



    IZZY_ATTACKER_INDEX = 5  # индекс Иззи в attacker_party_order

    def _ensure_izzy_reveals_for_target(target):
        """
        Пассивная способность Иззи:
        пока она — текущий атакующий, для ТЕКУЩЕГО настроения цели
        раскрываются 2 случайных ACT-действия.
        Хранится отдельно от общего revealed и НЕ показывается другим.
        """
        if target is None:
            return
        if getattr(store, "current_attacker", None) != IZZY_ATTACKER_INDEX:
            return

        _ensure_mood_action_used(target)

        mood = getattr(target, "mood", "neutral")
        bucket = target.izzy_revealed_mood_actions.setdefault(mood, {})

        revealed_count = sum(1 for v in bucket.values() if v)
        if revealed_count >= 2:
            return

        import random as _random
        all_acts = [a for a in store.ACTS_CONFIG.keys() if a not in ("Оценить", "Пощадить")]
        used = target.mood_action_used.get(mood, {})

        candidates = [a for a in all_acts if not used.get(a, False) and not bucket.get(a, False)]
        need = 2 - revealed_count
        if need <= 0 or not candidates:
            return

        picked = _random.sample(candidates, min(need, len(candidates)))
        for a in picked:
            bucket[a] = True






    def make_act_action_list(action_name):
        """Возвращает список действий для кнопки ACT.

        Если цель не выбрана — NullAction().
        """
        target = getattr(store, "target", None)
        if target is None:
            return NullAction()
        return [
            SetVariable("attackindex", action_name),
            SetVariable("attackindexdesc", action_name),
            SetVariable("turntype", "totarget"),
            Show("turntarget"),
            Show("attack_name_display"),
        ]

    # ------------------------------------------------------------------
    # ЭТИ ФУНКЦИИ ВЫЗЫВАЮТСЯ ИЗ ЛЕЙБЛОВ
    # ------------------------------------------------------------------
    def apply_act_to_enemy(enemy, action_name, success=True):
        """Применяет действие к врагу.

        success=False — НИЧЕГО не делает: ни метки в журнале настроений,
                        ни сдвига пощады. Кнопка в UI остаётся белой,
                        как будто игрок её вообще не нажимал.

        success=True  — помечает действие нажатым для ТЕКУЩЕГО настроения
                        и сдвигает spare_progress согласно
                        get_act_spare_effect (с учётом атакующего).

        Возвращает фактическую дельту пощады (0 при провале).
        """
        if enemy is None or not success:
            return 0

        _ensure_mood_action_used(enemy)
        mood = getattr(enemy, "mood", "neutral")
        enemy.mood_action_used.setdefault(mood, {})[action_name] = True

        attacker_name = get_current_attacker_name()

        # ▼▼▼ Успешный «Оценить» увеличивает счётчик осмотров,
        # но НЕ влияет на прогресс пощады ▼▼▼
        if action_name == "Оценить":
            enemy.evaluate_success_count = min(
                5,
                int(getattr(enemy, "evaluate_success_count", 0)) + 1
            )
            return 0
        # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

        effect = get_act_spare_effect(enemy, action_name, attacker_name)

        enemy.spare_max = get_enemy_spare_max(enemy)
        old = getattr(enemy, "spare_progress", 0)
        enemy.spare_progress = max(0, min(old + effect, enemy.spare_max))

        return enemy.spare_progress - old
























label finish_act:
    window hide
    # Получаем имя персонажа по индексу
    $ attacker_name = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик"][current_attacker - 1]
    # Получаем объект персонажа из словаря
    $ attacker.state = "act2"
    $ renpy.pause(1.0,hard=True)

    $ attacker = store.pers_dict[attacker_name]
    $ attacker.turn = 1
    # «Причина ошибок»: действие Криса тоже может дать дополнительный ход.
    $ kris_apply_action_turn_for_current()
    $ attacker.step_forward = 2
    $ actchosen = 0
    $ target = None
    # current_attacker хранит номер персонажа, поэтому сначала
    # получаем имя, а затем объект персонажа из pers_dict.
    $ attacker_party_order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"]
    $ attacker_name = attacker_party_order[current_attacker - 1]
    $ attacker = store.pers_dict[attacker_name]
    $ attacker.state = "idle"

    call screen choose_attacker_screen()

