
default hovered_artifact_id = None
default mx1 = 0
default my1 = 0

init python:
    def update_mouse_pos():
        global mx1, my1
        mx1, my1 = renpy.get_mouse_pos()

    # Читаемые имена и категории модификаторов артефактов
    battle_mod_names = {
        "atkartifactmod": "Атака",
        "defartifactmod": "Защита",
        "maxhpartifactmod": "HP",
        "maxmpartifactmod": "Мана",
        "hpregenartifactmod": "Реген HP",
        "mpregenartifactmod": "Реген маны",
        "magicartifactmod": "Магия",
        "accuracyartifactmod": "Точность",
        "critrateartifactmod": "Шанс крита",
        "critdmgartifactmod": "Крит урон",
        "tankartifactmod": "Танк",
    }
    social_mod_names = {
        "socializationartifactmod": "Социализация",
        "diplomacyartifactmod": "Дипломатия",
        "charmartifactmod": "Очарование",
        "perceptionartifactmod": "Восприятие",
        "rhetoricartifactmod": "Риторика",
        "artistryartifactmod": "Артистизм",
        "comfortartifactmod": "Комфорт",
        "powerartifactmod": "Власть",
    }

    def format_artifact_mod_value(mod_type, value):
        """Форматирует значение модификатора (учитывает знак и проценты/множители)."""
        if value == 0:
            return None
        sign = "+" if value > 0 else ""
        if "critdmg" in mod_type or "critrate" in mod_type or "dmgchance" in mod_type or "accuracy" in mod_type:
            return "{}{}%".format(sign, "{:g}".format(value * 100.0))
        else:
            return "{}{}".format(sign, value)

    def get_artifact_relation_display_bonus(artifact_id):
        """Возвращает бонус к отношению торговцев от ношения этого артефакта.

        «Искусство переговоров» (art33) даёт +2, «Краткий экскурс в торговлю»
        (art32) — +9. Дипломатия на торговлю не влияет.
        """
        if artifact_id == "art32":
            return 9
        if artifact_id == "art33":
            return 2
        return 0

    def get_artifact_description_stats(artifact_id, char_name=None):
        """Возвращает (боевые, социальные) характеристики артефакта.
        Значения уже включают применённые бонусы опознания и стирки.
        Если указан char_name, учитываются и индивидуальные (персонажные) бонусы.
        Каждая запись — (имя, значение, цвет):
        жёлтый — получено опознанием, фиолетовый — стиркой, белый — базовые."""
        battle = {}
        social = {}
        identified = set()
        washed = set()
        char_mods = set()

        def add(mod_type, val, source=None):
            if mod_type in battle_mod_names:
                battle[mod_type] = battle.get(mod_type, 0) + val
            elif mod_type in social_mod_names:
                social[mod_type] = social.get(mod_type, 0) + val
            else:
                return
            if source == "identified":
                identified.add(mod_type)
            elif source == "washed":
                washed.add(mod_type)
            elif source == "char":
                char_mods.add(mod_type)

        def stat_color(mod_type, val):
            if mod_type in char_mods:
                return "#48b448" if val > 0 else "#ff4444"
            if mod_type in washed:
                return "#cc88ff"
            elif mod_type in identified:
                return "#ffff00"
            return "#ffffff"

        # Базовые боевые характеристики
        base_mods = store.artifact_modifiers.get(artifact_id, [])
        base_vals = store.artifact_modifier_values.get(artifact_id, [])
        for m, v in zip(base_mods, base_vals):
            add(m, v)

        # Базовые социальные характеристики
        social_mods = store.artifact_social_modifiers.get(artifact_id, [])
        social_vals = store.artifact_social_modifier_values.get(artifact_id, [])
        for m, v in zip(social_mods, social_vals):
            add(m, v)

        # Индивидуальные (персонажные) бонусы артефакта
        if char_name is not None:
            char_overrides = store.artifact_character_modifiers.get((artifact_id, char_name), {})
            for m, v in char_overrides.items():
                add(m, v, source="char")

        # Находим экземпляр, чтобы учесть состояние опознания и стирки
        inst_idx = None
        if store.artifact_instances:
            for i, inst in enumerate(store.artifact_instances):
                if inst.get("id") == artifact_id:
                    inst_idx = i
                    break

        # Бонусы опознания уже добавлены в artifact_modifiers/
        # artifact_modifier_values при успешном опознании. Здесь отмечаем только
        # источник бонуса для цвета, не прибавляя его повторно.
        if inst_idx is not None and store.artifact_identified_state.get(inst_idx, 0) == 1:
            ib = store.artifact_identified_bonuses.get(artifact_id, {})
            identified.update(ib.get("modifiers", []))

        # Бонусы стирки также уже находятся в итоговых словарях модификаторов.
        if inst_idx is not None and store.artifact_wash_state.get(inst_idx, 0) == 2:
            wb = store.artifact_wash_extras.get(artifact_id, {})
            washed.update(wb.get("modifiers", []))

        def split_colored(text):
            half = len(text) // 2
            return "{color=#cc88ff}" + text[:half] + "{/color}{color=#ffff00}" + text[half:] + "{/color}"

        def build_stat_list(items, names):
            result = []
            for m, v in items.items():
                s = format_artifact_mod_value(m, v)
                if s is None:
                    continue
                if m in char_mods:
                    result.append((names[m], s, stat_color(m, v)))
                elif m in identified and m in washed:
                    result.append((split_colored(names[m]), split_colored(s), "#ffffff"))
                else:
                    result.append((names[m], s, stat_color(m, v)))
            return result

        battle_list = build_stat_list(battle, battle_mod_names)
        social_list = build_stat_list(social, social_mod_names)
        return battle_list, social_list

transform art_desc:
    on show:
        xpos 445 ypos 730 alpha 0.0
        easein 0.5 yoffset -630 alpha 1.0
    on hide:
        xpos 445 #ypos 100 alpha 1.0
        easeout 0.5 yoffset 0 alpha 0.0

transform art_desc2:    
    xpos 405 ypos 100 alpha 1.0
    easeout 1 ypos 730 alpha 0.0


transform white_bar_transf:
    on show:
        xsize 0 ysize 3 alpha 0.0
        linear 2 xsize 20 alpha 1.0
        pause 0.01
        linear 0.01 alpha 0.0
        pause 0.01
        linear 0.01 alpha 1.0
        pause 0.01
        linear 0.01 alpha 0.0
        pause 0.01
        linear 0.01 alpha 1.0
        pause 0.01
        linear 0.2 alpha 0.0
    on hide:
        linear 0.5 alpha 0.0







default artdescprogress= False
default art_desc_still_checking = False



screen art_desc_show:
    
    text "[artdescprogress]"

    
    #Если не прошло 1 сек и плашка не убралась, то при наведении показывается прогресс 
    #if art_desc_still_checking == False:
    #    timer 0.01 action [Show("art_desc_progress_screen")] 
    #elif art_desc_still_checking == True:
    #    pass
    #else:
    #    timer 0.01 action [Show("art_desc_progress_screen")]
    

    #Переключатель экранов
    timer 0.01 action Hide("art_desc_hide")

    #Скрыть экран который уходит вниз, если мы уже нажимали на него
    timer 0.001 action Hide("art_desc2")
    timer 1 action [Show("art_desc")]


    #if art_desc_still_checking == False:
    #    timer 0.0015 action Hide("art_desc2") at art_desc2   
    #    timer 0.001 action Show ("art_desc2") at art_desc2

    #timer 0.5 action SetVariable("art_desc_progress", None)

        
    


screen art_desc_hide:

    text "[art_desc_progress]"


    #при убирании прогресс скрывается в любом случае
    timer 0.01 action Hide("art_desc_progress_screen")

    # переключатель функциональных экранов
    timer 0.01 action Hide("art_desc_show")

    
    #timer 0.5 action [Hide("art_desc_hide")]


    #Если отвели более чем на сек, то перестаём чекать, скрываем экран восходящий, показываем нисходящий
    timer 1 action [SetVariable("art_desc_still_checking", False), Hide("art_desc")]
    timer 1 action [Show("art_desc2")]

    #    timer 1.5 action SetVariable("art_desc_progress", None)
 
        

    
screen art_desc_progress_screen:
    
    add DynamicDisplayable(white_bar_func) at white_bar_transf





default xoffset_for_art_desc = None


screen art_desc:
    key "K_TAB" action None
    key "K_ESCAPE" action None
    
    $ xright = 40
    $ xleft1 = -40
    $ xleft2 = -300


    zorder 100
    vbox:
        
        
        
        if xoffset_for_art_desc == "right":
            xoffset 180
            yoffset -20
        
        if xoffset_for_art_desc == "left":
            if pokaz_desc == 1:
                xoffset -100
                yoffset -20
            if pokaz_desc == 2:
                xoffset -430
                yoffset -20
        at art_desc
    
        if hovered_artifact_id is not None:
            $ item_id = hovered_artifact_id
            # Проверяем, это артефакт или расходник или оружие
            $ is_artifact = hovered_artifact_id in store.artifact_names
            $ is_consumable = hovered_artifact_id in store.consumable_names and not hovered_artifact_id.startswith("wep_")
            $ is_weapon = hovered_artifact_id.startswith("wep_")

            if is_artifact:
                $ artifact_name = store.artifact_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.artifact_identified_bonuses.get(hovered_artifact_id, {})
                $ bonus_modifiers = bonuses.get("modifiers", [])
                $ bonus_values = bonuses.get("values", [])
            elif is_consumable or is_weapon:
                $ artifact_name = store.consumable_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.consumable_buff_data.get(hovered_artifact_id, {}) if hasattr(store, 'consumable_buff_data') else {}
                $ bonus_modifiers = []
                $ bonus_values = []
            else:
                $ artifact_name = hovered_artifact_id
                $ bonuses = {}
                $ bonus_modifiers = []
                $ bonus_values = []

            $ item_icon_name = artifact_name
            





            
            frame:
                
                padding (10, 10)
                xysize (300, 605)
                background "#ffffff"
                #xalign 0.5
                #yalign 0.5
                
                frame:
                    padding (10, 10)
                    xysize (290, 595)
                    background "#000000"
                    xalign 0.5 yalign 0.5
                    
                    vbox:
                        xalign 0.5
                        spacing 10
                        
                        text "{font=determination.otf}{size=32}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                        
                        frame:
                            xysize (110,110)
                            background "#ffffff"
                            xalign 0.5 yalign 0.5

                            frame:
                                xysize (100,100)
                                background "#000000"
                                xalign 0.5 yalign 0.5
                            

                                add f"{item_icon_name}.png" xysize (100, 100) xalign 0.5 yalign 0.5

                        # Для артефактов показываем состояние стирки и опознания
                        if is_artifact:

                            # Состояние стирки
                            if store.artifact_wash_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 2:
                                text "{font=determination.otf}{size=22}Постирано{/font}{/size}" color "#48b448" xalign 0.5 text_align 0.5 
                            else:
                                text "{font=determination.otf}{size=22}Не постирано{/font}{/size}" color "#7a3e3e" xalign 0.5 text_align 0.5
                            
                            # Состояние опознания
                            if store.artifact_identifiable.get(hovered_artifact_id, 0) == 1:
                                if store.artifact_identified_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 1:
                                    text "{font=determination.otf}{size=22}Опознан{/font}{/size}" color "#48b448" xalign 0.5 text_align 0.5
                                else:
                                    text "{font=determination.otf}{size=22}Не опознан{/font}{/size}" color "#7a3e3e" xalign 0.5 text_align 0.5
                            else:
                                pass
                                #text "{font=determination.otf}{size=25}Опознание: Нельзя опознать{/font}{/size}" color "#666666" xalign 0.5

                            # Боевые и социальные характеристики
                            $ battle_stats, social_stats = get_artifact_description_stats(hovered_artifact_id, store.current_char)

                            if battle_stats:
                                text "{font=determination.otf}{size=27}Боевые{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                                for s_name, s_val, s_color in battle_stats:
                                    hbox:
                                        xalign 0.5
                                        spacing 10
                                        text "{font=determination.otf}{size=20}[s_name]:{/font}{/size}" color s_color
                                        text "{font=determination.otf}{size=20}[s_val]{/font}{/size}" color s_color

                            if social_stats:
                                text "{font=determination.otf}{size=27}Социальные{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                                for s_name, s_val, s_color in social_stats:
                                    hbox:
                                        xalign 0.5
                                        spacing 10
                                        text "{font=determination.otf}{size=20}[s_name]:{/font}{/size}" color s_color
                                        text "{font=determination.otf}{size=20}[s_val]{/font}{/size}" color s_color

                            # Бонус к отношению торговцев (как у расходников)
                            $ art_relation_bonus = get_artifact_relation_display_bonus(hovered_artifact_id)
                            if art_relation_bonus != 0:
                                text "{font=determination.otf}{size=20}Бонус к торговле:[art_relation_bonus]%{/font}{/size}" color "#ffffff" xalign 0.5

                            

                        # Для расходников показываем эффекты через get_inventory_desc_lines
                        elif is_consumable:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if item_id == "food_lottery_candy":
                                text "{font=determination.otf}{size=22}15% шанс получить лотерейный билет{/font}{/size}" color "#ffcc00" xalign 0.5
                            elif item_id == "food_lucky_monstercandy":
                                vbox:
                                    xalign 0.5
                                    spacing 2
                                    text "{font=determination.otf}{size=26}Случайный вкус:{/font}{/size}" color "#ffffff" xalign 0.5
                                    hbox:
                                        xalign 0.0
                                        spacing 20
                                        vbox:
                                            spacing 2
                                            text "{font=determination.otf}{size=18}Ириска:{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}Кофе:{/font}{/size}" color "#ffffff"
                                            null height 16
                                            text "{font=determination.otf}{size=18}Вода:{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}Золото:{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}Чили:{/font}{/size}" color "#ffffff"
                                            null height 14
                                            text "{font=determination.otf}{size=18}Канава:{/font}{/size}" color "#ffffff"
                                        vbox:
                                            spacing 2
                                            text "{font=determination.otf}{size=18}+20 ХП{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}+10% скорость души, бодрость (2х){/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}+20% маны{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}-1 ХП, +20 кромеров{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}-20 ХП, +30% урона след. атака{/font}{/size}" color "#ffffff"
                                            text "{font=determination.otf}{size=18}-15% бонус торговли на 30 мин.{/font}{/size}" color "#ffffff"
                            elif visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=22}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ consumable_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ consumable_description_text = consumable_desc_data.get("description", "")

# Для оружия показываем эффекты через get_inventory_desc_lines
                        elif is_weapon:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ weapon_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ weapon_description_text = weapon_desc_data.get("description", "")
    if pokaz_desc == 2:
        vbox:
            
            if xoffset_for_art_desc == "right":
                xoffset 180
                yoffset -20
            
            if xoffset_for_art_desc == "left":
                if pokaz_desc == 1:
                    xoffset -100
                    yoffset -20
                if pokaz_desc == 2:
                    xoffset -430
                    yoffset -20
            at art_desc

            frame:
                xoffset 290
                padding (5, 5)
                xysize (360, 605)
                background "#ffffff"
                frame:
                    xalign 0.5
                    yalign 0.5
                    padding (10, 10)
                    xysize (350, 595)
                    background "#000000"
                    vbox:
                        xalign 0.5
                        spacing 10
                        
                        text "Описание" size 25 xalign 0.5 text_align 0.5

                        if is_artifact:
                            $ artifact_desc_data = store.artifact_descriptions.get(hovered_artifact_id, {})
                            $ artifact_description_text = artifact_desc_data.get("description", "")
                            if artifact_description_text:
                                text "[artifact_description_text]" xalign 0.0 text_align 0.0 justify True size 20 xfill True
                        elif is_consumable:
                            if consumable_description_text:
                                text "[consumable_description_text]" xalign 0.0 text_align 0.0 justify True size 20 xfill True
                        elif is_weapon:
                            if weapon_description_text:
                                text "[weapon_description_text]" xalign 0.0 text_align 0.0 justify True size 20 xfill True






screen art_desc2:
    zorder 102
    vbox:
        #if art_desc_progreess == "complete":
        at art_desc2

   
        frame:
            
            padding (10, 10)
            xysize (300, 605)
            background "#ffffff"
            #xalign 0.5
            #yalign 0.5
            
            frame:
                padding (10, 10)
                xysize (290, 595)
                background "#000000"
                xalign 0.5 yalign 0.5
                































###########################################################################














transform art_desc_wash:
    on show:
        xpos 1200 ypos 10 alpha 0.0
        easein 0.5 xpos 920 ypos 10 alpha 1.0
    on hide:
        xpos 920 ypos 10 alpha 1.0
        easeout 0.5 xpos 1200 ypos 10 alpha 0.0


transform art_desc_wash_inv:

    on show:
        xpos -400 ypos 10 alpha 0.0
        easein 0.5 xpos 10 ypos 10 alpha 1.0
    on hide:
        xpos 10 ypos 10 alpha 1.0
        easeout 0.5 xpos -400 ypos 10 alpha 0.0




screen art_desc_wash:
    
    zorder 100
    vbox:

        at art_desc_wash
    
        if hovered_artifact_id is not None:
            # Проверяем, это артефакт или расходник или оружие
            $ is_artifact = hovered_artifact_id in store.artifact_names
            $ is_consumable = hovered_artifact_id in store.consumable_names and not hovered_artifact_id.startswith("wep_")
            $ is_weapon = hovered_artifact_id.startswith("wep_")

            if is_artifact:
                $ artifact_name = store.artifact_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.artifact_identified_bonuses.get(hovered_artifact_id, {})
                $ bonus_modifiers = bonuses.get("modifiers", [])
                $ bonus_values = bonuses.get("values", [])
            elif is_consumable or is_weapon:
                $ artifact_name = store.consumable_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.consumable_buff_data.get(hovered_artifact_id, {}) if hasattr(store, 'consumable_buff_data') else {}
                $ bonus_modifiers = []
                $ bonus_values = []
            else:
                $ artifact_name = hovered_artifact_id
                $ bonuses = {}
                $ bonus_modifiers = []
                $ bonus_values = []
            





            
            frame:

                
                padding (10, 10)
                xysize (350, 605)
                background "#ffffff"
                #xalign 0.5
                #yalign 0.5
                
                frame:
                    padding (10, 10)
                    xysize (340, 595)
                    background "#000000"
                    xalign 0.5 yalign 0.5
                    
                    vbox:
                        spacing 10
                        
                        text "{font=determination.otf}{size=35}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5
                        
                        # Для артефактов показываем состояние стирки и опознания
                        if is_artifact:
                            # Состояние стирки
                            if store.artifact_wash_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 2:
                                text "{font=determination.otf}{size=25}Стирка: Постирано{/font}{/size}" color "#66ff66" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Стирка: Не постирано{/font}{/size}" color "#888888" xalign 0.5
                            
                            # Состояние опознания
                            if store.artifact_identifiable.get(hovered_artifact_id, 0) == 1:
                                if store.artifact_identified_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 1:
                                    text "{font=determination.otf}{size=25}Опознание: Опознан{/font}{/size}" color "#66ff66" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Опознание: Не опознан{/font}{/size}" color "#ff6666" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Опознание: Нельзя опознать{/font}{/size}" color "#666666" xalign 0.5
                        
                        # Для расходников показываем эффекты
                        elif is_consumable:
                            # Получаем эффекты всех трёх уровней
                            $ effects1 = store.get_consumable_item_effects_level1(hovered_artifact_id) if hasattr(store, "get_consumable_item_effects_level1") else store.consumable_effects_level1.get(hovered_artifact_id, {})
                            $ effects2 = store.get_consumable_item_effects_level2(hovered_artifact_id) if hasattr(store, "get_consumable_item_effects_level2") else store.consumable_effects_level2.get(hovered_artifact_id, {})
                            $ effects3 = store.get_consumable_item_effects_level3(hovered_artifact_id) if hasattr(store, "get_consumable_item_effects_level3") else store.consumable_effects_level3.get(hovered_artifact_id, {})
                            
                            # 1 уровень: восстановление HP, MP, щита
                            $ hp_heal = effects1.get("hp_heal", 0)
                            $ mp_heal = effects1.get("mp_heal", 0)
                            $ shield_heal = effects1.get("shield_heal", 0)
                            $ over_heal = effects1.get("over_heal", 0)
                            $ hp_percent = effects1.get("hp_percent", 0)
                            $ hp_regen = effects1.get("hp_regen", 0)
                            $ hp_heal_all_picked = effects1.get("hp_heal_all_picked", 0)
                            $ hp_percent_all_picked = effects1.get("hp_percent_all_picked", 0)

                            if hp_heal != 0 or mp_heal != 0 or shield_heal != 0 or hp_percent != 0 or hp_regen != 0 or hp_heal_all_picked != 0 or hp_percent_all_picked != 0:
                                text "{font=determination.otf}{size=25}Восстановление:{/font}{/size}" color "#66ff66" xalign 0.5
                                if hp_heal != 0:
                                    $ over_text = " (сверхлечение)" if over_heal == 1 else ""
                                    text "{font=determination.otf}{size=22}  HP: +[hp_heal][over_text]{/font}{/size}" color "#ffffff" xalign 0.5
                                if mp_heal != 0:
                                    $ over_text = " (сверхлечение)" if over_heal == 1 else ""
                                    text "{font=determination.otf}{size=22}  MP: +[mp_heal][over_text]{/font}{/size}" color "#ffffff" xalign 0.5
                                if shield_heal != 0:
                                    text "{font=determination.otf}{size=22}  Щит: +[shield_heal]{/font}{/size}" color "#ffffff" xalign 0.5
                                if hp_percent != 0:
                                    $ percent_text = f"{int(hp_percent * 100)}%"
                                    text "{font=determination.otf}{size=22}  HP: +[percent_text] от макс.{/font}{/size}" color "#ffffff" xalign 0.5
                                if hp_regen != 0:
                                    text "{font=determination.otf}{size=22}  Регенерация HP: +[hp_regen]/ход{/font}{/size}" color "#ffffff" xalign 0.5
                                if hp_heal_all_picked != 0:
                                    text "{font=determination.otf}{size=22}  HP (вся команда): +[hp_heal_all_picked]{/font}{/size}" color "#ffffff" xalign 0.5
                                if hp_percent_all_picked != 0:
                                    $ percent_text = f"{int(hp_percent_all_picked * 100)}%"
                                    text "{font=determination.otf}{size=22}  HP (вся команда): +[percent_text] от макс.{/font}{/size}" color "#ffffff" xalign 0.5
                            
                            # 2 уровень: баффы/дебаффы характеристик
                            $ atk_debuff = effects2.get("atk_debuff", 0)
                            $ def_debuff = effects2.get("def_debuff", 0)
                            $ magic_debuff = effects2.get("magic_debuff", 0)
                            $ accuracy_debuff = effects2.get("accuracy_debuff", 0)
                            $ critrate_debuff = effects2.get("critrate_debuff", 0)
                            $ critdmg_debuff = effects2.get("critdmg_debuff", 0)
                            $ sad_debuff = effects2.get("sad_debuff", 0)
                            $ apatia_debuff = effects2.get("apatia_debuff", 0)
                            $ happy_debuff = effects2.get("happy_debuff", 0)
                            $ happy_debuff_all_picked = effects2.get("happy_debuff_all_picked", 0)

                            if atk_debuff != 0 or def_debuff != 0 or magic_debuff != 0 or accuracy_debuff != 0 or critrate_debuff != 0 or critdmg_debuff != 0 or sad_debuff != 0 or apatia_debuff != 0 or happy_debuff != 0 or happy_debuff_all_picked != 0:
                                text "{font=determination.otf}{size=25}Изменение характеристик:{/font}{/size}" color "#ffcc00" xalign 0.5
                                if atk_debuff != 0:
                                    $ value_str = f"+{atk_debuff}" if atk_debuff > 0 else f"{atk_debuff}"
                                    if atk_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Атака: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Атака: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if def_debuff != 0:
                                    $ value_str = f"+{def_debuff}" if def_debuff > 0 else f"{def_debuff}"
                                    if def_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Защита: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Защита: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if magic_debuff != 0:
                                    $ value_str = f"+{magic_debuff}" if magic_debuff > 0 else f"{magic_debuff}"
                                    if magic_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Магия: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Магия: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if accuracy_debuff != 0:
                                    $ value_str = f"+{accuracy_debuff}" if accuracy_debuff > 0 else f"{accuracy_debuff}"
                                    if accuracy_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Точность: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Точность: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if critrate_debuff != 0:
                                    $ value_str = f"+{critrate_debuff}" if critrate_debuff > 0 else f"{critrate_debuff}"
                                    if critrate_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Шанс крита: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Шанс крита: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if critdmg_debuff != 0:
                                    $ value_str = f"+{critdmg_debuff}" if critdmg_debuff > 0 else f"{critdmg_debuff}"
                                    if critdmg_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Крит. урон: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Крит. урон: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if sad_debuff != 0:
                                    $ value_str = f"+{sad_debuff}" if sad_debuff > 0 else f"{sad_debuff}"
                                    if sad_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Грусть: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Грусть: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if apatia_debuff != 0:
                                    $ value_str = f"+{apatia_debuff}" if apatia_debuff > 0 else f"{apatia_debuff}"
                                    if apatia_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Апатия: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Апатия: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if happy_debuff != 0:
                                    $ value_str = f"+{happy_debuff}" if happy_debuff > 0 else f"{happy_debuff}"
                                    if happy_debuff > 0:
                                        text "{font=determination.otf}{size=22}  Счастье: [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Счастье: [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                                if happy_debuff_all_picked != 0:
                                    $ value_str = f"+{happy_debuff_all_picked}" if happy_debuff_all_picked > 0 else f"{happy_debuff_all_picked}"
                                    if happy_debuff_all_picked > 0:
                                        text "{font=determination.otf}{size=22}  Счастье (вся команда): [value_str]{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=22}  Счастье (вся команда): [value_str]{/font}{/size}" color "#ff6666" xalign 0.5
                            
                            # 3 уровень: бонусные характеристики
                            $ bonus_atk = effects3.get("bonus_atk", 0)
                            $ bonus_def = effects3.get("bonus_def", 0)
                            $ bonus_magic = effects3.get("bonus_magic", 0)
                            $ bonus_accuracy = effects3.get("bonus_accuracy", 0)
                            $ bonus_critrate = effects3.get("bonus_critrate", 0)
                            $ bonus_critdmg = effects3.get("bonus_critdmg", 0)
                            $ bonus_tank = effects3.get("bonus_tank", 0)
                            $ bonus_perform = effects3.get("bonus_perform", 0)
                            $ bonus_socialization = effects3.get("bonus_socialization", 0)
                            $ merchant_relation_bonus_eff = effects3.get("merchant_relation_bonus", 0)
                            $ soul_speed_eff = effects3.get("soul_speed", 0)
                            $ ordinarynumber_eff = effects3.get("ordinarynumber", 0)

                            if bonus_atk != 0 or bonus_def != 0 or bonus_magic != 0 or bonus_accuracy != 0 or bonus_critrate != 0 or bonus_critdmg != 0 or bonus_tank != 0 or bonus_perform != 0 or bonus_socialization != 0 or merchant_relation_bonus_eff != 0 or soul_speed_eff != 0 or ordinarynumber_eff != 0:
                                text "{font=determination.otf}{size=25}Бонусные характеристики:{/font}{/size}" color "#00ccff" xalign 0.5
                                if bonus_atk != 0:
                                    text "{font=determination.otf}{size=22}  Атака: +[bonus_atk]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_def != 0:
                                    text "{font=determination.otf}{size=22}  Защита: +[bonus_def]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_magic != 0:
                                    text "{font=determination.otf}{size=22}  Магия: +[bonus_magic]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_accuracy != 0:
                                    text "{font=determination.otf}{size=22}  Точность: +[bonus_accuracy]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_critrate != 0:
                                    text "{font=determination.otf}{size=22}  Шанс крита: +[bonus_critrate]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_critdmg != 0:
                                    text "{font=determination.otf}{size=22}  Крит. урон: +[bonus_critdmg]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_tank != 0:
                                    text "{font=determination.otf}{size=22}  Танк: +[bonus_tank]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_perform != 0:
                                    text "{font=determination.otf}{size=22}  Перформанс: +[bonus_perform]{/font}{/size}" color "#ffffff" xalign 0.5
                                if bonus_socialization != 0:
                                    text "{font=determination.otf}{size=22}  Социализация: +[bonus_socialization]{/font}{/size}" color "#ffffff" xalign 0.5
                                if merchant_relation_bonus_eff != 0:
                                    text "{font=determination.otf}{size=22}  Отношения с торговцами: +[merchant_relation_bonus_eff]{/font}{/size}" color "#ffffff" xalign 0.5
                                if soul_speed_eff != 0:
                                    text "{font=determination.otf}{size=22}  Скорость: +[soul_speed_eff]{/font}{/size}" color "#ffffff" xalign 0.5
                                if ordinarynumber_eff != 0:
                                    text "{font=determination.otf}{size=22}  Ordinary number: +[ordinarynumber_eff]{/font}{/size}" color "#ffffff" xalign 0.5

                            # Специальные эффекты
                            if hovered_artifact_id == "food_lottery_candy":
                                text "{font=determination.otf}{size=22}  15% шанс получить лотерейный билет{/font}{/size}" color "#ffcc00" xalign 0.5
                            if hovered_artifact_id == "food_lucky_monstercandy":
                                vbox:
                                    xalign 0.5
                                    spacing 2
                                    text "{font=determination.otf}{size=20}Случайный эффект (1 из 6):{/font}{/size}" color "#ffcc00" xalign 0.5
                                    text "{font=determination.otf}{size=16}  • Ириска: +20 ОЗ{/font}{/size}" color "#ffffff" xalign 0.5
                                    text "{font=determination.otf}{size=16}  • Кофе: +0.1 скорость души, бодрость 2 хода{/font}{/size}" color "#ffffff" xalign 0.5
                                    text "{font=determination.otf}{size=16}  • Вода: +20% маны, +1 ordinarynumber{/font}{/size}" color "#ffffff" xalign 0.5
                                    text "{font=determination.otf}{size=16}  • Золото: -1 ОЗ, +20 кромеров{/font}{/size}" color "#ffffff" xalign 0.5
                                    text "{font=determination.otf}{size=16}  • Чили: -20 ОЗ, +30% урона след. атака{/font}{/size}" color "#ffffff" xalign 0.5
                                    text "{font=determination.otf}{size=16}  • Канава: -15% торг. на 30 мин, дебаффы{/font}{/size}" color "#ff6600" xalign 0.5

                            # Если нет эффектов
                            if hp_heal == 0 and mp_heal == 0 and shield_heal == 0 and atk_debuff == 0 and def_debuff == 0 and magic_debuff == 0 and accuracy_debuff == 0 and critrate_debuff == 0 and critdmg_debuff == 0 and sad_debuff == 0 and apatia_debuff == 0 and happy_debuff == 0 and happy_debuff_all_picked == 0 and bonus_atk == 0 and bonus_def == 0 and bonus_magic == 0 and bonus_accuracy == 0 and bonus_critrate == 0 and bonus_critdmg == 0 and bonus_tank == 0 and bonus_perform == 0 and bonus_socialization == 0 and merchant_relation_bonus_eff == 0 and soul_speed_eff == 0 and ordinarynumber_eff == 0:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ consumable_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ consumable_description_text = consumable_desc_data.get("description", "")
                            if consumable_description_text:
                                text "[consumable_description_text]" xalign 0.5 text_align 0.5

                        # Для оружия показываем эффекты через get_inventory_desc_lines
                        elif is_weapon:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ weapon_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ weapon_description_text = weapon_desc_data.get("description", "")
                            if weapon_description_text:
                                text "[weapon_description_text]" xalign 0.5 text_align 0.5



































################################

transform art_desc_trade_left_side:
    on show:
        xpos 5 ypos 730
        easein 0.5 ypos 80
    on hide:
        xpos 5 ypos 80
        easeout 0.5 ypos 730



screen art_desc_trade_left_side:

    key "K_ESCAPE" action None#[Hide("art_desc_trade_left_side"),Hide ("shop_screen")]
    
    zorder 100
    vbox:

        at art_desc_trade_left_side
    
        if hovered_artifact_id is not None:
            # Проверяем, это артефакт или расходник или оружие
            $ is_artifact = hovered_artifact_id in store.artifact_names
            $ is_consumable = hovered_artifact_id in store.consumable_names and not hovered_artifact_id.startswith("wep_")
            $ is_weapon = hovered_artifact_id.startswith("wep_")

            if is_artifact:
                $ artifact_name = store.artifact_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.artifact_identified_bonuses.get(hovered_artifact_id, {})
                $ bonus_modifiers = bonuses.get("modifiers", [])
                $ bonus_values = bonuses.get("values", [])
            elif is_consumable or is_weapon:
                $ artifact_name = store.consumable_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.consumable_buff_data.get(hovered_artifact_id, {}) if hasattr(store, 'consumable_buff_data') else {}
                $ bonus_modifiers = []
                $ bonus_values = []
            else:
                $ artifact_name = hovered_artifact_id
                $ bonuses = {}
                $ bonus_modifiers = []
                $ bonus_values = []
            

            

            
            frame:
                
                padding (10, 10)
                xysize (630, 635)
                background "#ffffff"
                #xalign 0.5
                #yalign 0.5
                
                frame:
                    padding (10, 10)
                    xysize (620, 625)
                    background "#000000"
                    xalign 0.5 yalign 0.5
                    
                    vbox:
                        spacing 10
                        
                        text "{font=determination.otf}{size=35}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5
                        
                        # Для артефактов показываем состояние стирки и опознания
                        if is_artifact:
                            # Состояние стирки
                            if store.artifact_wash_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 2:
                                text "{font=determination.otf}{size=25}Стирка: Постирано{/font}{/size}" color "#66ff66" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Стирка: Не постирано{/font}{/size}" color "#888888" xalign 0.5
                            
                            # Состояние опознания
                            if store.artifact_identifiable.get(hovered_artifact_id, 0) == 1:
                                if store.artifact_identified_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 1:
                                    text "{font=determination.otf}{size=25}Опознание: Опознан{/font}{/size}" color "#66ff66" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Опознание: Не опознан{/font}{/size}" color "#ff6666" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Опознание: Нельзя опознать{/font}{/size}" color "#666666" xalign 0.5
                        
                            # Боевые и социальные характеристики
                            $ battle_stats, social_stats = get_artifact_description_stats(hovered_artifact_id, store.current_char)

                            if battle_stats:
                                text "{font=determination.otf}{size=30}Боевые характеристики{/font}{/size}" color "#66ccff" xalign 0.5
                                for s_name, s_val, s_color in battle_stats:
                                    hbox:
                                        xalign 0.5
                                        spacing 10
                                        text "{font=determination.otf}{size=25}[s_name]:{/font}{/size}" color s_color
                                        text "{font=determination.otf}{size=25}[s_val]{/font}{/size}" color s_color

                            if social_stats:
                                text "{font=determination.otf}{size=30}Социальные характеристики{/font}{/size}" color "#ffcc66" xalign 0.5
                                for s_name, s_val, s_color in social_stats:
                                    hbox:
                                        xalign 0.5
                                        spacing 10
                                        text "{font=determination.otf}{size=25}[s_name]:{/font}{/size}" color s_color
                                        text "{font=determination.otf}{size=25}[s_val]{/font}{/size}" color s_color

                            # Бонус к отношению торговцев (как у расходников)
                            $ art_relation_bonus = get_artifact_relation_display_bonus(hovered_artifact_id)
                            if art_relation_bonus != 0:
                                text "{font=determination.otf}{size=25}  Отношения с торговцами: +[art_relation_bonus]{/font}{/size}" color "#ffffff" xalign 0.5

                        # Для расходников показываем эффекты через get_inventory_desc_lines
                        elif is_consumable:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if item_id == "food_lottery_candy":
                                text "{font=determination.otf}{size=22}  15% шанс получить лотерейный билет{/font}{/size}" color "#ffcc00" xalign 0.5
                            elif item_id == "food_lucky_monstercandy":
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    text "{font=determination.otf}{size=30}Случайный эффект \nот 1 из 6 вкусов:{/font}{/size}" text_align 0.5
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Ириска{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Кофе{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Чистая вода{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Слиток золота{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Острый чили{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Сточная канава{/font}{/size}" text_align 0.5 xalign 0.5
                            elif visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ consumable_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ consumable_description_text = consumable_desc_data.get("description", "")
                            if consumable_description_text:
                                text "[consumable_description_text]" xalign 0.5 text_align 0.5

                        # Для оружия показываем эффекты через get_inventory_desc_lines
                        elif is_weapon:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if item_id == "wep_bath_bombs":
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    text "{font=determination.otf}{size=35}Свойства{/font}{/size}" text_align 0.5 xalign 0.5
                                    vbox:
                                        spacing 25
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Урон цели: 40{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Урон всем остальным в бою: 20{/font}{/size}" text_align 0.5 xalign 0.5
                            elif item_id == "wep_flashlight":
                                vbox:
                                    spacing 40
                                    xalign 0.5
                                    text "{font=determination.otf}{size=35}Бонусы/штрафы{/font}{/size}" text_align 0.5
                                    vbox:
                                        spacing 25
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Критшанс цели: -5%{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=35}Танк от цели:{/font}{/size}" text_align 0.5 xalign 0.5
                                        vbox:
                                            spacing 15
                                            xalign 0.5
                                            text "{font=determination.otf}{size=25}Если цель - враг:\n +5 у применившего{/font}{/size}" text_align 0.5 xalign 0.5
                                            text "{font=determination.otf}{size=25}Если цель - друг:\n +5 у цели{/font}{/size}" text_align 0.5 xalign 0.5
                            elif item_id == "wep_poetry_leaf":
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    text "{font=determination.otf}{size=30}Эффект слабеет с \nкаждым разом:{/font}{/size}" text_align 0.5
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Базовая атака: -3{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Базовая защита: -3{/font}{/size}" text_align 0.5 xalign 0.5
                            elif visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ weapon_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ weapon_description_text = weapon_desc_data.get("description", "")
                            if weapon_description_text:
                                text "[weapon_description_text]" xalign 0.5 text_align 0.5


















#################################################################




transform art_desc_trade_right_side:
    on show:
        xpos 640 ypos 730
        easein 0.5 ypos 80
    on hide:
        xpos 640 ypos 80
        easeout 0.5 ypos 730



    



screen art_desc_trade_right_side:

    key "K_ESCAPE" action None#[Hide("art_desc_trade_right_side"),Hide ("shop_screen")]
    
    zorder 100
    vbox:

        at art_desc_trade_right_side
    
        if hovered_artifact_id is not None:
            # Проверяем, это артефакт или расходник или оружие
            $ is_artifact = hovered_artifact_id in store.artifact_names
            $ is_consumable = hovered_artifact_id in store.consumable_names and not hovered_artifact_id.startswith("wep_")
            $ is_weapon = hovered_artifact_id.startswith("wep_")

            if is_artifact:
                $ artifact_name = store.artifact_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.artifact_identified_bonuses.get(hovered_artifact_id, {})
                $ bonus_modifiers = bonuses.get("modifiers", [])
                $ bonus_values = bonuses.get("values", [])
            elif is_consumable or is_weapon:
                $ artifact_name = store.consumable_names.get(hovered_artifact_id, hovered_artifact_id)
                $ bonuses = store.consumable_buff_data.get(hovered_artifact_id, {}) if hasattr(store, 'consumable_buff_data') else {}
                $ bonus_modifiers = []
                $ bonus_values = []
            else:
                $ artifact_name = hovered_artifact_id
                $ bonuses = {}
                $ bonus_modifiers = []
                $ bonus_values = []
            





            
            frame:
                
                padding (10, 10)
                xysize (630, 635)
                background "#ffffff"
                #xalign 0.5
                #yalign 0.5
                
                frame:
                    padding (10, 10)
                    xysize (620, 625)
                    background "#000000"
                    xalign 0.5 yalign 0.5
                    
                    vbox:
                        spacing 10
                        
                        text "{font=determination.otf}{size=35}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5
                        
                        # Для артефактов показываем состояние стирки и опознания
                        if is_artifact:
                            # Состояние стирки
                            if store.artifact_wash_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 2:
                                text "{font=determination.otf}{size=25}Стирка: Постирано{/font}{/size}" color "#66ff66" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Стирка: Не постирано{/font}{/size}" color "#888888" xalign 0.5
                            
                            # Состояние опознания
                            if store.artifact_identifiable.get(hovered_artifact_id, 0) == 1:
                                if store.artifact_identified_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 1:
                                    text "{font=determination.otf}{size=25}Опознание: Опознан{/font}{/size}" color "#66ff66" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Опознание: Не опознан{/font}{/size}" color "#ff6666" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Опознание: Нельзя опознать{/font}{/size}" color "#666666" xalign 0.5
                        
                            # Боевые и социальные характеристики
                            $ battle_stats, social_stats = get_artifact_description_stats(hovered_artifact_id, store.current_char)

                            if battle_stats:
                                text "{font=determination.otf}{size=30}Боевые характеристики{/font}{/size}" color "#66ccff" xalign 0.5
                                for s_name, s_val, s_color in battle_stats:
                                    hbox:
                                        xalign 0.5
                                        spacing 10
                                        text "{font=determination.otf}{size=25}[s_name]:{/font}{/size}" color s_color
                                        text "{font=determination.otf}{size=25}[s_val]{/font}{/size}" color s_color

                            if social_stats:
                                text "{font=determination.otf}{size=30}Социальные характеристики{/font}{/size}" color "#ffcc66" xalign 0.5
                                for s_name, s_val, s_color in social_stats:
                                    hbox:
                                        xalign 0.5
                                        spacing 10
                                        text "{font=determination.otf}{size=25}[s_name]:{/font}{/size}" color s_color
                                        text "{font=determination.otf}{size=25}[s_val]{/font}{/size}" color s_color

                            # Бонус к отношению торговцев (как у расходников)
                            $ art_relation_bonus = get_artifact_relation_display_bonus(hovered_artifact_id)
                            if art_relation_bonus != 0:
                                text "{font=determination.otf}{size=25}  Отношения с торговцами: +[art_relation_bonus]{/font}{/size}" color "#ffffff" xalign 0.5

                        # Для расходников показываем эффекты через get_inventory_desc_lines
                        elif is_consumable:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if item_id == "food_lottery_candy":
                                text "{font=determination.otf}{size=22}  15% шанс получить лотерейный билет{/font}{/size}" color "#ffcc00" xalign 0.5
                            elif item_id == "food_lucky_monstercandy":
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    text "{font=determination.otf}{size=30}Случайный эффект \nот 1 из 6 вкусов:{/font}{/size}" text_align 0.5
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Ириска{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Кофе{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Чистая вода{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Слиток золота{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Острый чили{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Сточная канава{/font}{/size}" text_align 0.5 xalign 0.5
                            elif visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ consumable_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ consumable_description_text = consumable_desc_data.get("description", "")
                            if consumable_description_text:
                                text "[consumable_description_text]" xalign 0.5 text_align 0.5

                        # Для оружия показываем эффекты через get_inventory_desc_lines
                        elif is_weapon:
                            $ item_id = hovered_artifact_id
                            $ inv_name_map = getattr(store, "consumable_names", {})
                            $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                            $ inv_desc_lines = get_inventory_desc_lines(item_id)
                            $ visible_inv_desc_lines = inv_desc_lines[:10]

                            if item_id == "wep_bath_bombs":
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    text "{font=determination.otf}{size=35}Свойства{/font}{/size}" text_align 0.5 xalign 0.5
                                    vbox:
                                        spacing 25
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Урон цели: 40{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Урон всем остальным в бою: 20{/font}{/size}" text_align 0.5 xalign 0.5
                            elif item_id == "wep_flashlight":
                                vbox:
                                    spacing 40
                                    xalign 0.5
                                    text "{font=determination.otf}{size=35}Бонусы/штрафы{/font}{/size}" text_align 0.5
                                    vbox:
                                        spacing 25
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Критшанс цели: -5%{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=35}Танк от цели:{/font}{/size}" text_align 0.5 xalign 0.5
                                        vbox:
                                            spacing 15
                                            xalign 0.5
                                            text "{font=determination.otf}{size=25}Если цель - враг:\n +5 у применившего{/font}{/size}" text_align 0.5 xalign 0.5
                                            text "{font=determination.otf}{size=25}Если цель - друг:\n +5 у цели{/font}{/size}" text_align 0.5 xalign 0.5
                            elif item_id == "wep_poetry_leaf":
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    text "{font=determination.otf}{size=30}Эффект слабеет с \nкаждым разом:{/font}{/size}" text_align 0.5
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=25}Базовая атака: -3{/font}{/size}" text_align 0.5 xalign 0.5
                                        text "{font=determination.otf}{size=25}Базовая защита: -3{/font}{/size}" text_align 0.5 xalign 0.5
                            elif visible_inv_desc_lines:
                                for line in visible_inv_desc_lines:
                                    text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                            else:
                                text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                            $ weapon_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                            $ weapon_description_text = weapon_desc_data.get("description", "")
                            if weapon_description_text:
                                text "[weapon_description_text]" xalign 0.5 text_align 0.5



###############################################################



transform art_desc_check:
    on show:
        alpha 0.0 xpos 400 ypos -650
        easein 0.5 xpos 400 ypos 5 alpha 1.0

    on hide:
        xpos 400 ypos 5
        easeout 0.5 xpos 400 ypos -650 alpha 0.0


screen art_desc_check:
    
    key "K_ESCAPE" action Hide("art_desc_check")

    zorder 100
    hbox:
        at art_desc_check
        spacing -290
        vbox:

            
        
            if hovered_artifact_id is not None:
                # Проверяем, это артефакт или расходник или оружие
                $ is_artifact = hovered_artifact_id in store.artifact_names
                $ is_consumable = hovered_artifact_id in store.consumable_names and not hovered_artifact_id.startswith("wep_")
                $ is_weapon = hovered_artifact_id.startswith("wep_")

                if is_artifact:
                    $ artifact_name = store.artifact_names.get(hovered_artifact_id, hovered_artifact_id)
                    $ bonuses = store.artifact_identified_bonuses.get(hovered_artifact_id, {})
                    $ bonus_modifiers = bonuses.get("modifiers", [])
                    $ bonus_values = bonuses.get("values", [])
                elif is_consumable or is_weapon:
                    $ artifact_name = store.consumable_names.get(hovered_artifact_id, hovered_artifact_id)
                    $ bonuses = store.consumable_buff_data.get(hovered_artifact_id, {}) if hasattr(store, 'consumable_buff_data') else {}
                    $ bonus_modifiers = []
                    $ bonus_values = []
                else:
                    $ artifact_name = hovered_artifact_id
                    $ bonuses = {}
                    $ bonus_modifiers = []
                    $ bonus_values = []
                





                
                frame:
                    
                    padding (10, 10)
                    xysize (455, 645)
                    background "#ffffff"
                    #xalign 0.5
                    #yalign 0.5
                    
                    frame:
                        padding (10, 10)
                        xysize (445, 635)
                        background "#000000"
                        xalign 0.5 yalign 0.5
                        
                        vbox:
                            xalign 0.5
                            spacing 10
                            
                            text "{font=determination.otf}{size=35}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5
                            
                            # Для артефактов показываем состояние стирки и опознания
                            if is_artifact:
                                # Состояние стирки
                                if store.artifact_wash_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 2:
                                    text "{font=determination.otf}{size=25}Стирка: Постирано{/font}{/size}" color "#66ff66" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Стирка: Не постирано{/font}{/size}" color "#888888" xalign 0.5
                                
                                # Состояние опознания
                                if store.artifact_identifiable.get(hovered_artifact_id, 0) == 1:
                                    if store.artifact_identified_state.get(next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == hovered_artifact_id), None), 0) == 1:
                                        text "{font=determination.otf}{size=25}Опознание: Опознан{/font}{/size}" color "#66ff66" xalign 0.5
                                    else:
                                        text "{font=determination.otf}{size=25}Опознание: Не опознан{/font}{/size}" color "#ff6666" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Опознание: Нельзя опознать{/font}{/size}" color "#666666" xalign 0.5
                            
                            # Для расходников показываем эффекты через get_inventory_desc_lines
                            elif is_consumable:
                                $ item_id = hovered_artifact_id
                                $ inv_name_map = getattr(store, "consumable_names", {})
                                $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                                $ inv_desc_lines = get_inventory_desc_lines(item_id)
                                $ visible_inv_desc_lines = inv_desc_lines[:10]

                                if item_id == "food_lottery_candy":
                                    text "{font=determination.otf}{size=22}  15% шанс получить лотерейный билет{/font}{/size}" color "#ffcc00" xalign 0.5
                                elif item_id == "food_lucky_monstercandy":
                                    vbox:
                                        xalign 0.5
                                        spacing 2
                                        text "{font=determination.otf}{size=20}Случайный эффект (1 из 6):{/font}{/size}" color "#ffcc00" xalign 0.5
                                        text "{font=determination.otf}{size=16}  • Ириска: +20 ОЗ{/font}{/size}" color "#ffffff" xalign 0.5
                                        text "{font=determination.otf}{size=16}  • Кофе: +0.1 скорость души, бодрость 2 хода{/font}{/size}" color "#ffffff" xalign 0.5
                                        text "{font=determination.otf}{size=16}  • Вода: +20% маны, +1 ordinarynumber{/font}{/size}" color "#ffffff" xalign 0.5
                                        text "{font=determination.otf}{size=16}  • Золото: -1 ОЗ, +20 кромеров{/font}{/size}" color "#ffffff" xalign 0.5
                                        text "{font=determination.otf}{size=16}  • Чили: -20 ОЗ, +30% урона след. атака{/font}{/size}" color "#ffffff" xalign 0.5
                                        text "{font=determination.otf}{size=16}  • Канава: -15% торг. на 30 мин, дебаффы{/font}{/size}" color "#ff6600" xalign 0.5
                                elif visible_inv_desc_lines:
                                    for line in visible_inv_desc_lines:
                                        text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                                $ consumable_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                                $ consumable_description_text = consumable_desc_data.get("description", "")
                                if consumable_description_text:
                                    text "[consumable_description_text]" xalign 0.5 text_align 0.5

                            # Для оружия показываем эффекты через get_inventory_desc_lines
                            elif is_weapon:
                                $ item_id = hovered_artifact_id
                                $ inv_name_map = getattr(store, "consumable_names", {})
                                $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
                                $ inv_desc_lines = get_inventory_desc_lines(item_id)
                                $ visible_inv_desc_lines = inv_desc_lines[:10]

                                if visible_inv_desc_lines:
                                    for line in visible_inv_desc_lines:
                                        text "{font=determination.otf}{size=25}[line]{/font}{/size}" color "#ffffff" xalign 0.5
                                else:
                                    text "{font=determination.otf}{size=25}Нет эффектов{/font}{/size}" color "#888888" xalign 0.5

                                $ weapon_desc_data = store.consumable_descriptions.get(hovered_artifact_id, {})
                                $ weapon_description_text = weapon_desc_data.get("description", "")
                                if weapon_description_text:
                                    text "[weapon_description_text]" xalign 0.5 text_align 0.5

        vbox:
            if pokaz_desc == 2:
                frame:
                    xoffset 280
                    padding (0, 0)
                    xysize (370, 645)
                    background "#ffffff"
                    frame:
                        xalign 0.0
                        yalign 0.5
                        padding (10, 10)
                        xysize (365, 635)
                        background "#000000"
                        vbox:
                            xalign 0.5 yalign 0.5
                            spacing 10
                            if is_artifact:
                                $ artifact_desc_data = store.artifact_descriptions.get(hovered_artifact_id, {})
                                $ artifact_description_text = artifact_desc_data.get("description", "")
                                if artifact_description_text:
                                    text "[artifact_description_text]" xalign 0.0 text_align 0.5 size 25
                            elif is_consumable:
                                if consumable_description_text:
                                    text "[consumable_description_text]" xalign 0.5 text_align 0.5
                            elif is_weapon:
                                if weapon_description_text:
                                    text "[weapon_description_text]" xalign 0.5 text_align 0.5




