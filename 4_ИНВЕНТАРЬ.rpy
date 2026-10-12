
image white_bar = "whitebar.png"

# === ОПТИМИЗИРОВАННЫЕ ФУНКЦИИ ДЛЯ wash_screen ===
init python:
    def get_washable_artifacts():
        """Возвращает список артефактов, доступных для стирки (кэшируется)"""
        result = []
        if not hasattr(store, 'artifact_instances') or not store.artifact_instances:
            return result
        
        for inst_idx, inst in enumerate(store.artifact_instances):
            artifact_id = inst["id"]
            wash_type = store.artifact_wash_type.get(artifact_id, "nothing")
            wash_state = store.artifact_wash_state.get(inst_idx, 0)
            
            # Пропускаем мусор
            if artifact_id == "trash":
                continue
            # Пропускаем уже постиранные
            if wash_state == 2:
                continue
            # Пропускаем в слотах стирки
            if inst_idx in store.wash_slots:
                continue
                
            result.append({
                'inst_idx': inst_idx,
                'artifact_id': artifact_id,
                'owner': inst.get("owner"),
                'wash_type': wash_type,
                'wash_state': wash_state
            })
        return result
    
    def get_washable_count():
        """Возвращает количество предметов для стирки"""
        return len(get_washable_artifacts())
    
    def needs_wash_scroll():
        """Нужен ли скроллбар (>= 7 предметов)"""
        return get_washable_count() >= 7
    
    def get_artifact_display_data(inst_idx):
        """Возвращает данные для отображения артефакта в wash_screen"""
        if not store.artifact_instances or inst_idx >= len(store.artifact_instances):
            return None
        inst = store.artifact_instances[inst_idx]
        artifact_id = inst["id"]
        return {
            'artifact_id': artifact_id,
            'artifact_name': store.artifact_names.get(artifact_id, artifact_id),
            'owner': inst.get("owner"),
            'wash_type': store.artifact_wash_type.get(artifact_id, "nothing"),
            'wash_state': store.artifact_wash_state.get(inst_idx, 0)
        }
    
    def get_wash_slot_data(slot_idx):
        """Возвращает данные для слота стирки"""
        if not hasattr(store, 'wash_slots') or slot_idx >= len(store.wash_slots):
            return None
        inst_idx = store.wash_slots[slot_idx]
        if not store.artifact_instances or inst_idx >= len(store.artifact_instances):
            return None
        inst = store.artifact_instances[inst_idx]
        artifact_id = inst["id"]
        return {
            'inst_idx': inst_idx,
            'artifact_id': artifact_id,
            'artifact_name': store.artifact_names.get(artifact_id, artifact_id),
            'wash_type': store.artifact_wash_type.get(artifact_id, "nothing")
        }
    
    def get_wash_type_text(wash_type):
        """Возвращает текст описания типа стирки"""
        if wash_type == "delete":
            return "(уничтожится)", "#ff6666"
        elif wash_type == "extra":
            return "(улучшится)", "#66ff66"
        else:
            return "(без эффекта)", "#666666"

    def get_inventory_text_line_count(text_value, width=200, size=26):
        """Возвращает фактическое количество строк текста в инвентаре."""
        text_displayable = Text(
            text_value,
            font="determination.otf",
            size=size,
            xmaximum=width
        )
        rendered = renpy.render(text_displayable, width, 1000, 0, 0)

        sample_displayable = Text("Ag", font="determination.otf", size=size)
        sample_rendered = renpy.render(sample_displayable, width, 1000, 0, 0)
        line_height = sample_rendered.get_size()[1]

        if line_height <= 0:
            return 1
        return max(1, int(round(rendered.get_size()[1] / float(line_height))))




screen check_initiated:
    modal True
    key "K_ESCAPE" action NullAction()
    imagebutton:
        at alpha0
        idle "semiblack.png"
        hover "semiblack.png"
        action NullAction()


    ## Фон
    #add "#00000080"

    # Текст опознания
    #text "[store.is_checking]" size 30 color "#ffffff" xalign 0.5 yalign 0.4

    # Индикатор прогресса
    hbox:
        yoffset 20
        if store.is_checking == "is_checking":
            add "check_progress_white.png" at bar_in_progress
        elif store.is_checking == "success":
            add "check_progress_green.png" at bar_success
        elif store.is_checking == "fail":
            add "check_progress_red.png" at bar_fail

    
    if store.is_checking == "success":
        add "zvezda_opoz" at zvezdi_center
    if store.is_checking == "fail":
        add "perdezh" at perdezh_center

    add "huge_loopa.png" at big_loopa
    add "huge_loopa_steklo" at big_loopa_zerkalo

    


    # Таймеры
    timer 0.01 action SetVariable("is_checking", "is_checking")
    timer 1.5 action Function(identify_artifact_from_slot)

    if store.is_checking == "success":
        timer 1 action Hide ("check_initiated")
    if store.is_checking == "fail":
        timer 0.6 action Hide("check_initiated")


transform big_loopa:
    matrixcolor BrightnessMatrix(-0.05)
    yoffset 560 xoffset -300
    xanchor 0.2 yanchor 0.8
    alpha 0.0

    easein 0.5 rotate -360 xoffset 430 alpha 1.0

    xanchor 0.8 yanchor 0.2 yoffset 263 xoffset 727 #xoffset 747  
    
    easeout 1.0 rotate -450 xoffset 890 #xoffset 850

    easeout 0.5 rotate -810 xoffset 1580 alpha 0.0

transform big_loopa_zerkalo: 
    yoffset 560 xoffset -300
    xanchor 0.2 yanchor 0.8
    alpha 0.0

    easein 0.5 rotate -360 xoffset 430 alpha 0.5

    xanchor 0.8 yanchor 0.2 yoffset 263 xoffset 727 #xoffset 747  
    
    easeout 1.0 rotate -450 xoffset 890 #xoffset 850

    easeout 0.5 rotate -810 xoffset 1580 alpha 0.0
    

transform perdezh_center:
    xalign 0.5 yalign 0.5 xoffset 10
    alpha 0.0
    easein 0.1 alpha 1.0
    pause 0.5
    easeout 0.1 alpha 0.0

transform zvezdi_center:
    xalign 0.5 yalign 0.5 xoffset 20
    alpha 0.0
    easein 0.1 alpha 1.0
    pause 2.3
    easeout 0.1 alpha 0.0

image perdezh:
    "Пердёжик1.png"
    pause 0.05
    "Пердёжик2.png"
    pause 0.05
    "Пердёжик3.png"
    pause 0.05
    "Пердёжик4.png"
    pause 0.05
    "Пердёжик5.png"
    pause 0.05
    "Пердёжик6.png"
    pause 0.05
    "Пердёжик7.png"
    pause 0.05
    "Пердёжик8.png"
    pause 0.05
    "Пердёжик9.png"
    pause 0.045
    "Пердёжик10.png"
    pause 0.045
    "Пердёжик11.png"
    pause 0.045
    "Пердёжик12.png"
    pause 0.045
    "null_sprite.png"


image zvezda_opoz:
    "Звёздочка пёздочка1.png"
    pause 0.05
    "Звёздочка пёздочка2.png"
    pause 0.05
    "Звёздочка пёздочка3.png"
    pause 0.05
    "Звёздочка пёздочка4.png"
    pause 0.05
    "Звёздочка пёздочка5.png"
    pause 0.05
    "Звёздочка пёздочка6.png"
    pause 0.05
    "Звёздочка пёздочка7.png"
    pause 0.05
    "Звёздочка пёздочка8.png"
    pause 0.05
    "Звёздочка пёздочка9.png"
    pause 0.05
    "Звёздочка пёздочка10.png"
    pause 0.05
    "Звёздочка пёздочка11.png"
    pause 0.05
    "Звёздочка пёздочка12.png"
    pause 0.05
    "Звёздочка пёздочка13.png"
    pause 0.05
    "Звёздочка пёздочка14.png"
    pause 0.05
    "Звёздочка пёздочка15.png"
    pause 0.05
    "Звёздочка пёздочка16.png"
    pause 0.05
    "Звёздочка пёздочка17.png"
    pause 0.05
    "Звёздочка пёздочка18.png"
    pause 0.05
    "null_sprite.png"



screen wash_debug_overlay():
    zorder 200  # Высокий zorder для показа поверх других экранов

    if store.wash_in_progress:
        frame:
            background "#000000cc"
            padding (10, 10)
            xalign 0.05
            yalign 0.05
            xysize (300, 250)

            vbox:
                spacing 5
                text "=== СТИРКА В ПРОЦЕССЕ ===" size 16 color "#ffcc00"
                text "Прошло: [store.wash_timer_elapsed] сек" size 14 color "#ffffff"
                text "Всего: [store.wash_timer_total] сек" size 14 color "#ffffff"
                text "Слоты заблокированы: [store.wash_slots_locked]" size 14 color "#ffffff"
                text "Состояние: [store.is_washing]" size 14 color "#ffffff"
                null height 5
                text "Предметы в слотах:" size 14 color "#ffffff"
                if store.wash_slots:
                    for slot_idx, inst_idx in enumerate(store.wash_slots):
                        if inst_idx < len(store.artifact_instances):
                            $ inst = store.artifact_instances[inst_idx]
                            $ artifact_id = inst["id"]
                            $ artifact_name = store.artifact_names.get(artifact_id, artifact_id)
                            $ wash_type = store.artifact_wash_type.get(artifact_id, "nothing")
                            text "  [slot_idx+1]. [artifact_name] ([wash_type])" size 12 color "#cccccc"
                else:
                    text "{font=determination.otf}{size=30} ---" color "#ffffff" xalign 0.5


screen wash_initiated:
    modal True

    ## Фон
    #add "#00000080"

    # Индикатор прогресса стирки
    if store.is_washing == "is_washing":
        add "check_progress_white.png" at bar_in_progress
    elif store.is_washing == "success":
        add "check_progress_green.png" at bar_success
    elif store.is_washing == "fail":
        add "check_progress_red.png" at bar_fail

    # Таймеры
    timer 0.01 action SetVariable("is_washing", "is_washing")
    timer 1.5 action Function(wash_artifacts_from_slots)
    timer 2.5 action Hide("wash_initiated")


# ------------------------------------------------------------
# 8) ЭКРАН СТИРКИ ВЕЩЕЙ
# ------------------------------------------------------------

transform glowing:
# Исходное состояние
    yoffset -5 xoffset 5 zoom 0.9
    blur 0.0
    matrixcolor BrightnessMatrix(0.0)
    
    # Эффект свечения при наведении
    on hover:
        easein 0.2 blur 2.0 matrixcolor BrightnessMatrix(0.2)
    on idle:
        easeout 0.2 blur 0.0 matrixcolor BrightnessMatrix(0.0)


# Общая переменная наведения для кнопок стирки
# Принимает значения: None, "stop", "start", "pullout"
default wash_hovered_button = None

# Позиция индикатора (координаты подберите под свою разметку)
transform wash_indicator:
    xpos 732 ypos 120

# Мигание для состояния "стирка остановлена"
transform stop_miganie:
    matrixcolor TintMatrix("#ff4444")
    alpha 1.0
    linear 0.35 alpha 0.25 
    pause 0.1
    linear 0.35 alpha 1.0 blur 3
    pause 0.1
    linear 0.35 alpha 0.25
    pause 0.1
    linear 0.35 alpha 1.0 blur 3
    pause 0.1
    linear 0.35 alpha 0.25
    pause 0.1
    linear 0.35 alpha 1.0 
    
    


transform stop_miganie_just:
    matrixcolor TintMatrix("#ff4444")


transform washing_miganie:
    linear 0.35 alpha 0.25 
    pause 0.1
    linear 0.35 alpha 1.0
    pause 0.1

    repeat 









screen wash_screen():
    key "K_ESCAPE" action [CloseWashScreenAction(), Jump("close_wash_screen_to_game_menu")]
    #tag menu
    modal True

    # Сразу актуализирует прогресс при каждом показе/перерисовке
    $ store.wash_background_update()

    # Обновление, пока экран открыт
    #timer 2 repeat True action Function(store.wash_background_update)

    key "K_TAB" action None


    add "washing_bg.png" 

    if store.wash_in_progress:
        add "стиралка2.png" xpos 280 ypos -40 at washing_shake
    else:
        add "стиралка2.png" xpos 280 ypos -40
        add "Стиралка_дверь.png" xpos 280 ypos -40





    $ wash_active_slot_transforms = [
        wash_slot_0_active,
        wash_slot_1_active,
        wash_slot_2_active,
        wash_slot_3_active
    ]

    $ wash_rotate_slot_transforms = [
        wash_slot_0_rotate,
        wash_slot_1_rotate,
        wash_slot_2_rotate,
        wash_slot_3_rotate
    ]
 

    

    hbox:
        xpos 370 ypos -15
        if store.wash_in_progress:
            at washing_shake
        

        if store.is_washing == "fail":
            # Стирку остановили кнопкой - мигающий stop
            add "washing_stop.png" xalign 0.5  at stop_miganie 

        elif store.wash_in_progress:
            # Стирка в процессе
            if wash_hovered_button == "stop": 
                add "washing_stop.png" xalign 0.5 at stop_miganie_just
            else:
                add "washing_process.png" xalign 0.5 at washing_miganie

        elif store.is_washing == "success":
            # Стирка окончена
            if wash_hovered_button == "pullout":
                add "washing_out.png" xalign 0.5 xoffset -6 at green_trans
            else:
                add "washing_done.png" xalign 0.5 at green_miganie

        elif len(store.wash_slots) > 0:
            # Есть хотя бы 1 артефакт в слотах
            if wash_hovered_button == "start":
                add "washing_start.png" xalign 0.5 
            else:
                add "washing_ready.png" xalign 0.5 

 




    # 10 solid-сегментов, показывающих прогресс стирки.
    if len(store.wash_slots) > 0 or store.is_washing in ("fail", "success"):
        $ total_time = store.wash_timer_total if store.wash_timer_total else 0.0
        $ filled = min(10.0, (store.wash_timer_elapsed / total_time) * 10.0) if total_time > 0 else 0.0

        #hbox:
        #    xpos 735 ypos 80
        #    spacing 6
        #    if store.wash_in_progress:
        #        at washing_shake

        #    for seg in range(10):
        #        if filled >= seg + 1:
        #            if store.is_washing == "success":
        #                add Solid("#22dd66") xysize (11, 3)

        #            elif store.is_washing == "fail":
        #                add Solid("#ff5555") xysize (11, 3)

        #            else:
        #                add Solid("#d8dcff") xysize (11, 3)
        #        else:
        #            add Solid("#4c4d58") xysize (11, 3)


        hbox:
            xpos 735 ypos 80
            spacing 6
            if store.wash_in_progress:
                at washing_shake, glow_layer
            else:
                at glow_layer

            for seg in range(10):
                if filled >= seg + 1:
                    if store.is_washing == "success":
                        add Solid("#22dd66") xysize (11, 3)

                    elif store.is_washing == "fail":
                        add Solid("#ff5555") xysize (11, 3)

                    else:
                        add Solid("#d8dcff") xysize (11, 3)
                else:
                    add Solid("#4c4d58") xysize (11, 3)


    # Кнопка закрытия
    vbox:
        
        spacing 10
        xsize 100
        textbutton "Закрыть" action [CloseWashScreenAction(), ShowMenu("artifacts_menu")]:
            xpos 1200
            text_size 16
            text_color "#ffffff"
            text_hover_color "#ff6666"
        textbutton "escape_k" action [CloseWashScreenAction(), Jump("close_wash_screen_to_game_menu")]:
            xpos 1200
            text_size 16
            text_color "#ffffff"
            text_hover_color "#ff6666"

    hbox:
        spacing 20

        # Левая колонка: инвентарь с вещами
        vbox:
            xpos 10
            spacing 10
            xsize 400

            frame:
                ypos 10
                background "#ffffff"
                xysize (380, 50)

                frame:
                    background "#000000"
                    xysize (370, 40)
                    xalign 0.5 yalign 0.5
                    hbox:
                        text "{font=determination.otf}{size=40}Инвентарь" color "#ffffff" xalign 0.5 ypos -7 xoffset 100 
                        
                        hbox:
                            xoffset -190 yoffset 5
                            if pokaz_desc == 0:
                                imagebutton:
                                    #xysize(40,40)
                                    xalign 1.0
                                    idle "hide_fast_desc.png"
                                    hover "hide_fast_desc.png" at glowing
                                    action SetVariable("pokaz_desc", 1)
                            elif pokaz_desc == 1:
                                imagebutton:
                                    #xysize(40,40)
                                    xalign 1.0
                                    idle "show_fast_desc.png"
                                    hover "show_fast_desc.png" at glowing
                                    action SetVariable("pokaz_desc", 0)
                            else:
                                imagebutton:
                                    #xysize(40,40)
                                    xalign 1.0
                                    idle "show_fast_desc.png"
                                    hover "show_fast_desc.png" at glowing
                                    action SetVariable("pokaz_desc", 0)
                            
                    
                        
                        

            frame:
                background "#ffffff"
                padding (10, 10)
                xysize (380, 550)

                frame:
                    background "#000000"
                    padding (10, 10)
                    xysize (370, 540)
                    xalign 0.5 yalign 0.5

                    # Оптимизировано: используем кэшированные функции
                    $ washable_artifacts = get_washable_artifacts()
                    $ washable_count = len(washable_artifacts)
                    $ needs_scroll = washable_count >= 7

                    if needs_scroll:
                        viewport:
                            xysize (360, 530)
                            scrollbars "vertical"
                            mousewheel True

                            vbox:
                                spacing 0
                                if washable_artifacts:
                                    for art_data in washable_artifacts:
                                        $ inst_idx = art_data['inst_idx']
                                        $ artifact_id = art_data['artifact_id']
                                        $ owner = art_data['owner']
                                        $ wash_type = art_data['wash_type']
                                        $ wash_type_text, wash_type_color = get_wash_type_text(wash_type)
                                        frame:
                                            xoffset -10
                                            background "#000000"
                                            padding (5, 5)
                                            xysize (340, 90)
                                            $ hovered_actions = [SetVariable("hovered_artifact_id", artifact_id)]
                                            $ unhovered_actions = [SetVariable("hovered_artifact_id", None)]
                                            if pokaz_desc > 0:
                                                $ hovered_actions.append(Show("art_desc_wash"))
                                                $ unhovered_actions.append(Hide("art_desc_wash"))
                                            button action AddArtifactToWashSlotAction(inst_idx) hovered hovered_actions unhovered unhovered_actions at inventory_artifact_trans:
                                                xoffset -4
                                                hbox:
                                                    spacing 10
                                                    if owner:
                                                        $ owner_data = store.pers_dict[owner]
                                                        add "images/[owner_data.nameeng]head.png" size (50, 50) xalign 0.0 ypos -10
                                                    else:
                                                        add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                    text "{font=determination.otf}{size=26}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ffffff" xoffset 10 yoffset -7 text_align 0.5 xalign 0.5 yalign 0.5
                                                    null width 10
                                                    text wash_type_text size 10 color wash_type_color
                                else:
                                    text "{font=determination.otf}{size=30}---" size 14 color "#ffffff" xpos 150
                    else:
                        vbox:
                            spacing 5
                            if washable_artifacts:
                                for art_data in washable_artifacts:
                                    $ inst_idx = art_data['inst_idx']
                                    $ artifact_id = art_data['artifact_id']
                                    $ owner = art_data['owner']
                                    $ wash_type = art_data['wash_type']
                                    $ wash_type_text, wash_type_color = get_wash_type_text(wash_type)
                                    frame:
                                        xoffset -10
                                        background "#000000"
                                        padding (5, 5)
                                        xysize (340, 80)
                                        $ hovered_actions = [SetVariable("hovered_artifact_id", artifact_id)]
                                        $ unhovered_actions = [SetVariable("hovered_artifact_id", None)]
                                        if pokaz_desc > 0:
                                            $ hovered_actions.append(Show("art_desc_wash"))
                                            $ unhovered_actions.append(Hide("art_desc_wash"))
                                        button action AddArtifactToWashSlotAction(inst_idx) hovered hovered_actions unhovered unhovered_actions:
                                            hbox:
                                                spacing 10
                                                if owner:
                                                    $ owner_data = store.pers_dict[owner]
                                                    add "images/[owner_data.nameeng]head.png" size (50, 50) xalign 0.0 ypos -10
                                                else:
                                                    add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                text "{font=determination.otf}{size=29}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ffffff" ypos -9
                                                null width 10
                                                text wash_type_text size 10 color wash_type_color
                            else:
                                text "{font=determination.otf}{size=30}---" size 14 color "#ffffff" xpos 150

        # Правая колонка: grid 2x2 и кнопки управления
        vbox:
            xpos 450
            ypos 170
            spacing 10
            xsize 400
            xoffset -330
            yoffset 150

            if store.wash_in_progress:
                at washing_shake
            
            frame:
                background None
                if store.wash_in_progress:
                    at washing_rotate1
                    xanchor 0.5 yanchor 0.5
                    xoffset 125 yoffset 125

                grid 2 2:
                    spacing 10
                    xalign 0.0
                    yalign 0.5
                    xoffset -35
                    yoffset -30

                    # 4 слота для стирки - оптимизировано
                    for slot_idx in range(4):

                        $ slot_at = [wash_active_slot_transforms[slot_idx], wash_rotate_slot_transforms[slot_idx]] if store.is_washing == "is_washing" else idle_null

                        frame:
                            if store.wash_in_progress:
                                background None
                            else:
                                background "#ffffff"
                            xysize (130, 130)
                            padding (5,5)
                            frame at slot_at:
                                if store.wash_in_progress:
                                    background None
                                    
                                else:
                                    background "#000000"
                                xysize (120, 120)

                                $ slot_data = get_wash_slot_data(slot_idx)
                                if slot_data:
                                    $ inst_idx = slot_data['inst_idx']
                                    $ artifact_id = slot_data['artifact_id']
                                    $ artifact_name = slot_data['artifact_name']
                                    $ wash_type = slot_data['wash_type']
                                    $ wash_type_text, wash_type_color = get_wash_type_text(wash_type)

                                    python:
                                        if store.is_washing == "success":
                                            slot_actions = [Hide("art_desc_wash")] if not store.wash_slots_locked else None
                                        else:
                                            slot_actions = [RemoveArtifactFromWashSlotAction(slot_idx), Hide("art_desc_wash")] if not store.wash_slots_locked else None


                                        slot_hovered = [SetVariable("hovered_artifact_id", artifact_id)]
                                        slot_unhovered = [SetVariable("hovered_artifact_id", None)]
                                        if pokaz_desc > 0:
                                            slot_hovered.append(Show("art_desc_wash"))
                                            slot_unhovered.append(Hide("art_desc_wash"))

                                    imagebutton:
                                        at washslot_art
                                        xalign 0.5
                                        yalign 0.5                                    
                                        idle f"{store.artifact_names.get(artifact_id, artifact_id)}.png"
                                        hover f"{store.artifact_names.get(artifact_id, artifact_id)}.png" 
                                        action slot_actions hovered slot_hovered unhovered slot_unhovered
                                else:
                                    if store.wash_in_progress:
                                        pass
                                    else:
                                        text "---" xalign 0.5 yalign 0.5
                                    #text "Слот [slot_idx+1]" size 14 color "#888888" xalign 0.5 yalign 0.5

            # Кнопки управления
    hbox:
    
        if store.wash_in_progress:
            at washing_shake
        spacing 10
        yoffset -10
        xoffset 70
        xalign 0.54
        yalign 0.12
        if store.wash_in_progress:
            imagebutton:
                focus_mask True
                idle "stop_wash.png"
                hover "stop_wash.png"
                action StopWashAction()
                hovered SetVariable("wash_hovered_button", "stop")
                unhovered SetVariable("wash_hovered_button", None)


        elif store.is_washing == "success":
            # Стирка завершена
            if len(store.wash_slots) > 0:
                # Есть вещи в слотах - показываем кнопку "достать вещи"
                imagebutton:
                    
                    focus_mask True
                    idle "finished_wash.png"
                    hover "finished_wash.png"
                    action RetrieveWashedArtifactsAction()
                    hovered SetVariable("wash_hovered_button", "pullout")
                    unhovered SetVariable("wash_hovered_button", None)

                    

            else:
                timer 0.01 action SetVariable("is_washing", None)
                # Слоты пусты (вещи уничтожены) - показываем "начать стирку"
                #textbutton "{font=determination.otf}{size=25}НАЧАТЬ СТИРКУ{/font}{/size}" action None:
                #    text_size 18
                #    text_color "#666666"
                #    text_hover_color "#ff0000"
                #    xalign 0.5
                #    yalign 0.5

                add "start_wash.png"




        elif store.is_washing == "fail":
            # Стирка отменена/не выполнена
            if len(store.wash_slots) > 0:
                # Вещи остались в слотах - можно запустить стирку заново
                imagebutton:
                    focus_mask True                                                                                                                                                                                                                     
                    idle "start_wash.png"
                    hover "start_wash.png"                    
                    action StartWashAction()
                    hovered SetVariable("wash_hovered_button", "start")
                    unhovered SetVariable("wash_hovered_button", None)
            else:
                timer 0.01 action SetVariable("is_washing", None)
                add "start_wash.png"
        else:
            # Процесс стирки не идёт
            if len(store.wash_slots) > 0:
                #textbutton "{font=determination.otf}{size=25}НАЧАТЬ СТИРКУ{/font}{/size}" action StartWashAction():
                #    text_size 18
                #    text_color "#ffffff"
                #    text_hover_color "#ffff00"
                #    xalign 0.5
                #    yalign 0.5

                imagebutton:
                    focus_mask True
                    idle "start_wash.png"
                    hover "start_wash.png"
                    hovered SetVariable("wash_hovered_button", "start")
                    unhovered SetVariable("wash_hovered_button", None)
                    action StartWashAction()

            else:
                #textbutton "{font=determination.otf}{size=25}НАЧАТЬ СТИРКУ{/font}{/size}" action None:
                #    text_size 18
                #    text_color "#666666"
                #    text_hover_color "#ff0000"
                #    xalign 0.5
                #    yalign 0.5
                add "start_wash.png"

    if store.wash_in_progress:
        add "Стиралка_вода.png" xpos 370 ypos 150 alpha 0.65 at washing_shake, voda_rotate
        add "Стиралка_закрыто.png" xpos 280 ypos -40 at washing_shake
        add "Стиралка_стекло.png" xpos 280 ypos -40 at alpha_wash_steklo, washing_shake
    else:
        add "Стиралка_дверь_стекло.png" xpos 280 ypos -40 at alpha_wash_steklo
        
transform alpha_wash_steklo:
    alpha 0.625

transform washing_shake:
    xoffset 5 yoffset 5
    pause 0.05
    xoffset 5 yoffset -5
    pause 0.05
    xoffset -5 yoffset 5
    pause 0.05
    xoffset -5 yoffset -5
    pause 0.05
    repeat 


transform voda_rotate:
    rotate 0
    pause 0.2
    rotate -60
    pause 0.2
    rotate -120
    pause 0.2
    rotate -180
    pause 0.2
    rotate -240
    pause 0.2
    rotate -300
    pause 0.2
    rotate -360
    pause 0.2
    repeat
            #frame:
            #        background "#ffffff"
            #        padding (10, 10)
            #        xysize (380, 60)
            #
            #        frame:
            #            background "#000000"
            #            padding (10, 10)
            #            xysize (370, 50)
            #            xalign 0.5
            #            yalign 0.5
            #
            #            text "{font=determination.otf}{size=20}Слоты: [len(store.wash_slots)]/4{/font}{/size}" color "#ffffff" xalign 0.5 yalign 0.5








    #vbox:
        #xpos 300 ypos 10
        # Информация о слотах


        # Отладочная информация: 4 артефакта с информацией о стирке
        #frame:
        #    background "#333333"
        #    padding (10, 10)
        #    xysize (850, 80)
        #    xalign 0.5
        #
        #    frame:
        #        background "#000000"
        #        padding (10, 10)
        #        xysize (830, 70)
        #
        #        text "{font=determination.otf}{size=14}=== ИНФОРМАЦИЯ О СТИРКЕ ==={/font}{/size}" color "#ffcc00" xalign 0.5 ypos -5
        #
        #        hbox:
        #            spacing 10
        #            xalign 0.5
        #            yalign 0.5
        #
        #            # Показываем информацию о 4 артефактах, которые можно стирать
        #            $ washable_count = 0
        #            for inst_idx, inst in enumerate(store.artifact_instances):
        #                if washable_count >= 4:
        #                    break
        #                $ artifact_id = inst["id"]
        #                $ wash_type = store.artifact_wash_type.get(artifact_id, "nothing")
        #                $ wash_state = store.artifact_wash_state.get(inst_idx, 0)
        #
        #                # Пропускаем мусор и артефакты, которые нельзя стирать
        #                if artifact_id == "trash" or wash_type == "nothing":
        #                    continue
        #
        #                $ washable_count += 1
        #                $ artifact_name = store.artifact_names.get(artifact_id, artifact_id)
        #
        #                # Определяем текст состояния
        #                if wash_state == 0:
        #                    $ state_text = "Не помыт"
        #                elif wash_state == 1:
        #                    $ state_text = "В слоте"
        #                elif wash_state == 2:
        #                    $ state_text = "Постирка"
        #                else:
        #                    $ state_text = "?"
        #
        #                # Определяем текст последствия
        #                if wash_type == "delete":
        #                    $ effect_text = "Уничтожится"
        #                elif wash_type == "extra":
        #                    $ effect_text = "Улучшится"
        #                else:
        #                    $ effect_text = "Без эффекта"
        #
        #                # Определяем цвет состояния
        #                $ state_color = "#ffffff"
        #                if wash_state == 1:
        #                    $ state_color = "#ffcc00"
        #                elif wash_state == 2:
        #                    $ state_color = "#66ff66"##

        #                vbox:
        #                    spacing 2
        #                    text "{font=determination.otf}{size=12}[artifact_name]{/font}{/size}" color "#ffffff" size 12
        #                    text "{font=determination.otf}{size=10}[effect_text]{/font}{/size}" size 10
        #
        #                    text "{font=determination.otf}{size=10}[state_text]{/font}{/size}" color "#ffffff" size 10

transform alpha0505:
    alpha 0.0
    easein 0.5 alpha 0.8

screen wash_proceed_in_progress():
    zorder 150  # Ниже чем debug_overlay, но выше других экранов
    modal False  # НЕ modal, чтобы другие экраны могли работать поверх него

    # Фон с прозрачностью
    #add "#00000040"
    #add "semiblackbg.png" at alpha0505

    # Индикатор прогресса стирки
    if store.is_washing == "is_washing":
        pass
        #add "check_progress_white.png" at wash_bar_in_progress
    elif store.is_washing == "success":
        pass
        #add "check_progress_green.png" at wash_bar_success
    elif store.is_washing == "fail":
        pass
        #add "check_progress_red.png" at wash_bar_fail

    # 10 solid-сегментов, показывающих прогресс стирки.
    # Нужен хотя бы 1 артефакт в слотах, чтобы рисовать шкалу.
    #if len(store.wash_slots) > 0:
    #    $ filled = store.wash_timer_total and (store.wash_timer_elapsed / store.wash_timer_total) * 10.0 or 0.0
    #    hbox:
    #        xalign 0.5
    #        yalign 0.88
    #        spacing 6
    #        for seg in range(10):
    #            if filled >= seg + 1:
    #                add Solid((102, 255, 102, 220)) xysize (36, 26)
    #            else:
    #                add Solid((70, 70, 70, 160)) xysize (36, 26)

    # Таймер для обновления времени больше не нужен:
    # прогресс и завершение стирки теперь обрабатываются глобально
    # через config.per_frame_callback (wash_background_update).
    # timer 0.1 action UpdateWashTimerAction() repeat True

    # Таймер для выполнения стирки больше не нужен:
    # timer store.wash_timer_total action [
    #     Function(store.wash_artifacts_from_slots),
    #     Hide("wash_proceed_in_progress")
    # ]

    # Обновление фоновой логики стирки, пока этот экран активен
    timer 1 repeat True action Function(store.wash_background_update)

    # Самоскрытие, когда стирка больше не идёт (прогресс или завершение
    # обрабатываются в wash_background_update).
    if not store.wash_in_progress:
        timer 0.05 action Hide("wash_proceed_in_progress")














































































# ___   __    _  __   __  _______  __    _  _______  _______  ______    __   __
#|   | |  |  | ||  | |  ||       ||  |  | ||       ||       ||    _ |  |  | |  |
#|   | |   |_| ||  |_|  ||    ___||   |_| ||_     _||   _   ||   | ||  |  |_|  |
#|   | |       ||       ||   |___ |       |  |   |  |  | |  ||   |_||_ |       |
#|   | |  _    ||       ||    ___||  _    |  |   |  |  |_|  ||    __  ||_     _|
#|   | | | |   | |     | |   |___ | | |   |  |   |  |       ||   |  | |  |   |
#|___| |_|  |__|  |___|  |_______||_|  |__|  |___|  |_______||___|  |_|  |___|




default unequip_zh = 0




# ------------------------------------------------------------
# 5) ЭКРАН МЕНЮ АРТЕФАКТОВ
# ------------------------------------------------------------

define size_for_invent = 30

default pokaz_desc = 1
default block_desc_show = False

label to_main_menu:
    $ store.sync_equipped_artifacts()
    #$ store.save_coordinates_before_save()
    show screen game_screen
    hide screen game_screen
    call screen main_menu

label Return_to_game_screen:
    # Синхронизируем экипированные артефакты перед выходом
    $ store.sync_equipped_artifacts()
    hide screen artifacts_menu
    call screen game_screen
    #call nolabel


default invent = "closed"

default ch = getattr(store, "pers_dict", None)["Крис"] if getattr(store, "pers_dict", None) and "Крис" in getattr(store, "pers_dict", None) else None

transform dim_colors:
    # Не-выбранный персонаж: полная серация + лёгкое затемнение.
    # При наведении: серость остаётся, затемнение убирается.
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.1)
    on hover:
        easein 0.15 matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.05)
    on idle:
        easeout 0.15 matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.1)


screen artifacts_menu():
    #$ store.invent = "opened"

    # Фоновая логика стирки, пока открыто меню инвентаря
    #timer 3 repeat True action Function(store.wash_background_update)

    timer 0.00000000000000000000001 action SetVariable("invent", "opened")
    timer 0.0001 action [SetVariable("chardes", store.pers_dict["Крис"]), SetVariable("chardesprepare", store.pers_dict["Крис"])]

    #key "K_ESCAPE" action None #Function(store.save_and_open_artifacts2)
    #key "K_TAB" action [Show("inventory_obertka_close")]
    key "K_TAB" action  [Function(save_and_open_artifacts2), Call("close_inventory")]
    key "K_ESCAPE" action  [Function(save_and_open_artifacts2), Call("close_inventory")]




    tag menu
    modal True






    # Гарантируем инициализацию персонажей до обращения к текущему герою.
    $ store.ensure_team_manager()
    $ sprite_suffix = "_down" if store.spritestyle == "down" else ""
    $ ch = store.pers_dict.get(store.current_char)
    if ch is None and store.pers_dict:
        $ ch = store.pers_dict.get("Крис", next(iter(store.pers_dict.values())))

    # Примеры использования таймера для изменения уровня:
    # Установить уровень 3 для всех персонажей:
    # timer 5 action SetAllCharactersLevelAction(3)

    # Увеличить уровень всех персонажей на +1:
    #timer 5 action ModifyAllCharactersLevelAction(1)

    # Уменьшить уровень всех персонажей на -1:
    # timer 5 action ModifyAllCharactersLevelAction(-1)

    #null height 10
    vbox:
        spacing 10 xpos 1200 ypos 5
        #textbutton "Закрыть" action Return()
        textbutton "Закрыть" action Hide("artifacts_menu")
        textbutton "Вернуться в игру" action Call("Return_to_game_screen")



    hbox:
        xpos 70
        ypos 60
        spacing -50

        # Верхний hbox с двумя колонками
        hbox:


            # Левая колонка: вкладки и инвентарь
            vbox:
                spacing -5
                xsize 420
                ypos 90
                xoffset -40



                # Содержимое инвентаря
                frame:
                    background "#ffffff"
                    padding (10, 10)
                    xysize (410,604)
                    ypos -50
                    frame:
                        background "#000000"
                        padding (10, 10)
                        xysize (400,594)
                        xalign 0.5 yalign 0.5









                        # Вычисляем количество предметов для текущей вкладки
                        $ artifact_count = len(store.artifact_instances) if store.inventory_tab == "artifacts" else 0
                        $ consumable_count = len([k for k, v in store.consumable_inventory.items() if not k.startswith("wep_")]) if store.inventory_tab == "consumables" else 0
                        $ weapon_count = len([k for k, v in store.consumable_inventory.items() if k.startswith("wep_")]) if store.inventory_tab == "weapons" else 0
                        $ total_items = artifact_count + consumable_count + weapon_count
                        $ needs_scroll = total_items >= 8

                        # Прокручиваемый viewport (только если больше 8 предметов)
                        if needs_scroll:
                            viewport:
                                ypos 30 xpos -5
                                id "inventory_viewport"
                                xysize (390, 550)
                                scrollbars "vertical"
                                mousewheel True
                                draggable True
                                vscrollbar_xsize 20

                                vbox:
                                    ypos 30
                                    spacing -10
                                    #text "{size=30}_" color"#000000"

                                    # Содержимое вкладки артефактов
                                    if store.inventory_tab == "artifacts":
                                        #text "Инвентарь артефактов:" size 25 color "#000000"
                                        if store.artifact_instances:
                                            for inst_idx, inst in enumerate(store.artifact_instances):
                                                $ owner_name = inst["owner"]
                                                $ is_equipped_by_current = owner_name == ch.name
                                                $ artifact_id = inst["id"]
                                                $ artifact_name = store.artifact_names.get(artifact_id, artifact_id)
                                                $ item_name_lines = get_inventory_text_line_count(artifact_name, 240, 27)

                                                # Пропускаем "мусорные" артефакты
                                                if artifact_id == "trash":
                                                    continue

                                                # Пропускаем артефакты в стиральной машинке (in washing machine = 1)
                                                $ in_wash_slot = store.is_artifact_in_wash_slot(inst_idx)
                                                if in_wash_slot:
                                                    continue

                                                # Постиранные артефакты (get_washed = 2) видны в обычном инвентаре

                                                hbox:
                                                    spacing -245

                                                    # Первый VBOX: hbox с head
                                                    vbox:
                                                        spacing 0
                                                        #ypos 10
                                                        xfill True
                                                        hbox:
                                                            spacing 5
                                                            if owner_name:
                                                                $ owner = store.pers_dict[owner_name]
                                                                vbox:
                                                                    if pokaz_desc > 0:
                                                                            if not is_equipped_by_current:
                                                                                frame:
                                                                                    xoffset -10
                                                                                    background "#000000"
                                                                                    padding (5, 5)
                                                                                    xysize (340, 90)
                                                                                    button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc"), PreviewArtifactStatsAction(ch.name, artifact_id, "equip"), SetVariable("art_desc_still_checking", True)] unhovered [Hide("art_desc"), Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                        hbox:
                                                                                            spacing 10

                                                                                            add "images/[owner.nameeng]headcolored.png" size (50, 50) #ypos -10
                                                                                            hbox:
                                                                                                xalign 0.5
                                                                                                text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                            else:
                                                                                frame:
                                                                                    xoffset -10
                                                                                    background "#000000"
                                                                                    padding (5, 5)
                                                                                    xysize (340, 90)
                                                                                    button action NullAction() hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                                        hbox:
                                                                                            spacing 10
                                                                                            add "images/[owner.nameeng]headcolored.png" size (50, 50) #ypos -10
                                                                                            hbox:
                                                                                                xalign 0.5
                                                                                                text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)

                                                                    else:
                                                                            if not is_equipped_by_current:
                                                                                frame:
                                                                                    xoffset -10
                                                                                    background "#000000"
                                                                                    padding (5, 5)
                                                                                    xysize (340, 90)
                                                                                    button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), PreviewArtifactStatsAction(ch.name, artifact_id, "equip")] unhovered [SetVariable("hovered_artifact_id", None), Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                        hbox:
                                                                                            spacing 10

                                                                                            add "images/[owner.nameeng]headcolored.png" size (50, 50) #ypos -10
                                                                                            hbox:
                                                                                                xalign 0.5
                                                                                                text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                            else:
                                                                                frame:
                                                                                    xoffset -10
                                                                                    background "#000000"
                                                                                    padding (5, 5)
                                                                                    xysize (340, 90)
                                                                                    button action NullAction() at inventory_artifact_trans:
                                                                                        hbox:
                                                                                            spacing 10
                                                                                            add "images/[owner.nameeng]headcolored.png" size (50, 50) #ypos -10
                                                                                            hbox:
                                                                                                xalign 0.5
                                                                                                text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)



                                                            else:

                                                                if pokaz_desc > 0:

                                                                    # Второй VBOX: кнопка экипировки
                                                                    vbox:
                                                                        if not is_equipped_by_current:
                                                                            frame:
                                                                                xoffset -10
                                                                                background "#000000"
                                                                                padding (5, 5)
                                                                                xysize (340, 90)
                                                                                button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc"), PreviewArtifactStatsAction(ch.name, artifact_id, "equip"), SetVariable("art_desc_still_checking", True)] unhovered [Hide("art_desc"), Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                    hbox:
                                                                                        spacing 10

                                                                                        add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                                        hbox:
                                                                                            text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                        else:
                                                                            frame:
                                                                                xoffset -10
                                                                                background "#000000"
                                                                                padding (5, 5)
                                                                                xysize (340, 90)
                                                                                button action NullAction() hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                                    hbox:
                                                                                        spacing 10
                                                                                        add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                                        hbox:
                                                                                            xalign 0.5
                                                                                            text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                else:
                                                                    vbox:
                                                                        if not is_equipped_by_current:
                                                                            frame:
                                                                                xoffset -10
                                                                                background "#000000"
                                                                                padding (5, 5)
                                                                                xysize (340, 90)
                                                                                button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), PreviewArtifactStatsAction(ch.name, artifact_id, "equip"), SetVariable("art_desc_still_checking", True)] unhovered [Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                    hbox:
                                                                                        spacing 10

                                                                                        add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                                        hbox:
                                                                                            xalign 0.5
                                                                                            text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                        else:
                                                                            frame:
                                                                                xoffset -10
                                                                                background "#000000"
                                                                                padding (5, 5)
                                                                                xysize (340, 90)
                                                                                button action NullAction() at inventory_artifact_trans:
                                                                                    hbox:
                                                                                        spacing 10
                                                                                        add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                                        hbox:
                                                                                            xalign 0.5
                                                                                            text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)


                                        else:
                                            text "{font=determination.otf}{size=30}---" xalign 0.5















                                    # Содержимое вкладки consumables
                                    elif store.inventory_tab == "consumables":


                                        #text "{size=30}Ф" color"#000000"
                                        if store.consumable_inventory:
                                            for item_id, cnt in store.consumable_inventory.items():
                                                if item_id.startswith("wep_"):
                                                    continue
                                                hbox:
                                                    yoffset 10
                                                    xoffset -10
                                                    spacing 10
                                                    $ button_key = f"use_{ch.name}_{item_id}"
                                                    $ button_state = store.button_states.get(button_key, 0)
                                                    $ item_name = store.consumable_names.get(item_id, item_id)
                                                    $ item_name_lines = get_inventory_text_line_count(item_name, 200, 27)
                                                    if pokaz_desc > 0:
                                                        if button_state == 0:
                                                            frame:

                                                                background "#000000"
                                                                padding (5, 5)
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                    hbox:
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                            if int(cnt) > 1:
                                                                                text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffffff" ypos (-9 if item_name_lines >= 2 else 5)
                                                        else:
                                                            frame:

                                                                background "#000000"
                                                                padding (5, 5)
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                    hbox:
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffff00" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                            if int(cnt) > 1:
                                                                                text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffff00" ypos (-9 if item_name_lines >= 2 else 5)
                                                    else:
                                                        if button_state == 0:

                                                            frame:

                                                                background "#000000"
                                                                padding (5, 5)
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                    hbox:
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                            if int(cnt) > 1:
                                                                                text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffffff" ypos (-9 if item_name_lines >= 2 else 5)
                                                        else:
                                                            frame:

                                                                background "#000000"
                                                                padding (5, 5)
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                    hbox:
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffff00" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                            text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffff00" ypos (-9 if item_name_lines >= 2 else 5)
                                        else:
                                            text "{font=determination.otf}{size=30}---" color "#ffffff" xalign 0.5

                                    # Содержимое вкладки оружия
                                    elif store.inventory_tab == "weapons":
                                        if store.consumable_inventory:
                                            for item_id, cnt in store.consumable_inventory.items():
                                                if item_id.startswith("wep_"):
                                                    hbox:
                                                        yoffset 10
                                                        xoffset -10
                                                        spacing 10
                                                        $ button_key = f"use_{ch.name}_{item_id}"
                                                        $ button_state = store.button_states.get(button_key, 0)
                                                        $ item_name = store.consumable_names.get(item_id, item_id)
                                                        $ item_name_lines = get_inventory_text_line_count(item_name, 200, 27)
                                                        if pokaz_desc > 0:
                                                            if button_state == 0:
                                                                frame:
                                                                    background "#000000"
                                                                    padding (5, 5)
                                                                    xysize (330, 90)
                                                                    button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                        hbox:
                                                                            spacing 10
                                                                            add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                            hbox:
                                                                                spacing 10
                                                                                xsize 260
                                                                                text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                                if int(cnt) > 1:
                                                                                    text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffffff" ypos (-9 if item_name_lines >= 2 else 5)
                                                            else:
                                                                frame:
                                                                    background "#000000"
                                                                    padding (5, 5)
                                                                    xysize (330, 90)
                                                                    button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                        hbox:
                                                                            spacing 10
                                                                            add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                            hbox:
                                                                                spacing 10
                                                                                xsize 260
                                                                                text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffff00" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                                if int(cnt) > 1:
                                                                                    text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffff00" ypos (-9 if item_name_lines >= 2 else 5)
                                                        else:
                                                            if button_state == 0:
                                                                frame:
                                                                    background "#000000"
                                                                    padding (5, 5)
                                                                    xysize (330, 90)
                                                                    button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                        hbox:
                                                                            spacing 10
                                                                            add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                            hbox:
                                                                                spacing 10
                                                                                xsize 260
                                                                                text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                                if int(cnt) > 1:
                                                                                    text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffffff" ypos (-5 if item_name_lines >= 2 else 5)
                                                            else:
                                                                frame:
                                                                    background "#000000"
                                                                    padding (5, 5)
                                                                    xysize (330, 90)
                                                                    button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                        hbox:
                                                                            spacing 10
                                                                            add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                                            hbox:
                                                                                spacing 10
                                                                                xsize 260
                                                                                text "{font=determination.otf}{size=27}[item_name]{/font}{/size}" color "#ffff00" xalign 0.5 text_align 0.5 xmaximum 200 ypos (-12 if item_name_lines >= 2 else 5)
                                                                                if int(cnt) > 1:
                                                                                    text "{font=determination.otf}{size=27}х[int(cnt)]{/font}{/size}" color "#ffff00" ypos (-9 if item_name_lines >= 2 else 5)
                                        else:                                            
                                            text "{font=determination.otf}{size=30}---" color "#ffffff" xalign 0.5







































                        # Обычный vbox (если 8 или меньше предметов)
                        else:
                            vbox:
                                yoffset 30
                                spacing -13
                                #text "{size=30}Ф" color"#000000"

                                # Содержимое вкладки артефактов
                                if store.inventory_tab == "artifacts":
                                    if store.artifact_instances:
                                        for inst_idx, inst in enumerate(store.artifact_instances):
                                            $ owner_name = inst["owner"]
                                            $ is_equipped_by_current = owner_name == ch.name
                                            $ artifact_id = inst["id"]
                                            $ artifact_name = store.artifact_names.get(artifact_id, artifact_id)
                                            $ item_name_lines = get_inventory_text_line_count(artifact_name, 200, 27)

                                            # Пропускаем "мусорные" артефакты
                                            if artifact_id == "trash":
                                                continue

                                            # Пропускаем артефакты в стиральной машинке (in washing machine = 1)
                                            $ in_wash_slot = store.is_artifact_in_wash_slot(inst_idx)
                                            if in_wash_slot:
                                                continue

                                            hbox:
                                                spacing -245

                                                # Первый VBOX: hbox с head
                                                vbox:
                                                    spacing 0
                                                    yalign 0.5
                                                    xfill True
                                                    hbox:
                                                        spacing 5
                                                        if owner_name:
                                                            $ owner = store.pers_dict[owner_name]
                                                            vbox:
                                                                if pokaz_desc > 0:
                                                                    if not is_equipped_by_current:
                                                                        frame:
                                                                            xoffset -10
                                                                            background "#000000"
                                                                            padding (5, 5)
                                                                            xysize (340, 90)
                                                                            button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc"), PreviewArtifactStatsAction(ch.name, artifact_id, "equip")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc"), Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10

                                                                                    add "images/[owner.nameeng]headcolored.png" size (50, 50)
                                                                                    hbox:
                                                                                        xalign 0.5
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                    else:
                                                                        frame:
                                                                            xoffset -10
                                                                            background "#000000"
                                                                            padding (5, 5)
                                                                            xysize (340, 90)
                                                                            button action NullAction() hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10
                                                                                    add "images/[owner.nameeng]headcolored.png" size (50, 50)
                                                                                    hbox:
                                                                                        xalign 0.5
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                else:
                                                                    frame:
                                                                        xoffset -10
                                                                        background "#000000"
                                                                        padding (5, 5)
                                                                        xysize (340, 90)
                                                                        if not is_equipped_by_current:
                                                                            button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), PreviewArtifactStatsAction(ch.name, artifact_id, "equip")] unhovered [SetVariable("hovered_artifact_id", None), Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10

                                                                                    add "images/[owner.nameeng]headcolored.png" size (50, 50)
                                                                                    hbox:
                                                                                        xalign 0.5
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                        else:
                                                                            frame:
                                                                                xoffset -10
                                                                                background "#000000"
                                                                                padding (5, 5)
                                                                                xysize (340, 90)
                                                                                button action NullAction() at inventory_artifact_trans:
                                                                                    hbox:
                                                                                        spacing 10
                                                                                        add "images/[owner.nameeng]headcolored.png" size (50, 50)
                                                                                        hbox:
                                                                                            xalign 0.5
                                                                                            text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)

                                                        else:

                                                            if pokaz_desc > 0:
                                                                # Второй VBOX: кнопка экипировки
                                                                vbox:
                                                                    if not is_equipped_by_current:
                                                                        frame:
                                                                            xoffset -10
                                                                            background "#000000"
                                                                            padding (5, 5)
                                                                            xysize (340, 90)
                                                                            button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc"), PreviewArtifactStatsAction(ch.name, artifact_id, "equip"), SetVariable("art_desc_still_checking", True)] unhovered [Hide("art_desc"), Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10

                                                                                    add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0
                                                                                    hbox:
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                    else:
                                                                        frame:
                                                                            xoffset -10
                                                                            background "#000000"
                                                                            padding (5, 5)
                                                                            xysize (340, 90)
                                                                            button action NullAction() hovered [SetVariable("hovered_artifact_id", artifact_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10
                                                                                    add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0
                                                                                    hbox:
                                                                                        xalign 0.5
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                            else:
                                                                vbox:
                                                                    if not is_equipped_by_current:
                                                                        frame:
                                                                            xoffset -10
                                                                            background "#000000"
                                                                            padding (5, 5)
                                                                            xysize (340, 90)
                                                                            button action EquipArtifactAction(ch.name, artifact_id, inst_idx) hovered [SetVariable("hovered_artifact_id", artifact_id), PreviewArtifactStatsAction(ch.name, artifact_id, "equip"), SetVariable("art_desc_still_checking", True)] unhovered [Function(store.update_hp_preview, None)] at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10

                                                                                    add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0
                                                                                    hbox:
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)
                                                                    else:
                                                                        frame:
                                                                            xoffset -10
                                                                            background "#000000"
                                                                            padding (5, 5)
                                                                            xysize (340, 90)
                                                                            button action NullAction() at inventory_artifact_trans:
                                                                                hbox:
                                                                                    spacing 10
                                                                                    add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0
                                                                                    hbox:
                                                                                        xalign 0.5
                                                                                        text "{font=determination.otf}{size=26}[artifact_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5 ypos (-12 if item_name_lines >= 2 else 10)

                                    else:
                                        text "{font=determination.otf}{size=30}---" xalign 0.5





                                # Содержимое вкладки consumables

                                elif store.inventory_tab == "consumables":


                                    #text "{size=30}Ф" color"#000000"
                                    if store.consumable_inventory:
                                        for item_id, cnt in store.consumable_inventory.items():
                                            if item_id.startswith("wep_"):
                                                continue
                                            #vbox:
                                            #    #yoffset 20
                                            #    spacing 20
                                            hbox:
                                                xalign 0.0
                                                #yoffset 20
                                                xoffset -10
                                                spacing 10
                                                $ button_key = f"use_{ch.name}_{item_id}"
                                                $ button_state = store.button_states.get(button_key, 0)
                                                $ item_name = store.consumable_names.get(item_id, item_id)
                                                $ item_name_lines = get_inventory_text_line_count(item_name, 200, 26)
                                                if pokaz_desc > 0:
                                                    if button_state == 0:
                                                        frame:

                                                            background "#000000"
                                                            #padding (5, 5)
                                                            xysize (330, 90)
                                                            button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                hbox:
                                                                    xalign 0.0
                                                                    spacing 10
                                                                    add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                    hbox:
                                                                        spacing 10
                                                                        xsize 260
                                                                        if item_name_lines >= 2:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 ypos -3
                                                                        else:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 yalign 0.5
                                                                    if int(cnt) > 1:
                                                                        text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 1.0
                                                    else:
                                                        frame:

                                                            background "#000000"
                                                            #padding (5, 5)
                                                            xysize (330, 90)
                                                            button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                hbox:
                                                                    xalign 0.0
                                                                    spacing 10
                                                                    add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                    hbox:
                                                                        spacing 10
                                                                        xsize 260
                                                                        if item_name_lines >= 2:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 ypos -3
                                                                        else:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 yalign 0.5
                                                                    text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffff00" yalign 0.5
                                                else:
                                                    if button_state == 0:

                                                        frame:

                                                            background "#000000"
                                                            #padding (5, 5)
                                                            xysize (330, 90)
                                                            button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                hbox:
                                                                    xalign 0.0
                                                                    spacing 10
                                                                    add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                    hbox:
                                                                        spacing 10
                                                                        xsize 260
                                                                        if item_name_lines >= 2:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 ypos -3
                                                                        else:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 yalign 0.5
                                                                    if int(cnt) > 1:
                                                                        text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 1.0
                                                    else:
                                                        frame:

                                                            background "#000000"
                                                            #padding (5, 5)
                                                            xysize (330, 90)
                                                            button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                hbox:
                                                                    xalign 0.0
                                                                    spacing 10
                                                                    add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 #ypos -10
                                                                    hbox:
                                                                        spacing 10
                                                                        xsize 260
                                                                        if item_name_lines >= 2:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 ypos -3
                                                                        else:
                                                                            text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 yalign 0.5
                                                                    text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffff00" yalign 0.5 xalign 1.0
                                    else:
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xalign 0.5

                                # Содержимое вкладки оружия
                                if store.inventory_tab == "weapons":
                                    if store.consumable_inventory:
                                        for item_id, cnt in store.consumable_inventory.items():
                                            if item_id.startswith("wep_"):
                                                hbox:
                                                    xalign 0.0
                                                    xoffset -10
                                                    spacing 10
                                                    $ button_key = f"use_{ch.name}_{item_id}"
                                                    $ button_state = store.button_states.get(button_key, 0)
                                                    $ item_name = store.consumable_names.get(item_id, item_id)
                                                    $ item_name_lines = get_inventory_text_line_count(item_name, 200, 26)
                                                    if pokaz_desc > 0:
                                                        if button_state == 0:
                                                            frame:
                                                                background "#000000"
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                    hbox:
                                                                        xalign 0.0
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            if item_name_lines >= 2:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 ypos -9
                                                                            else:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 ypos 9
                                                                    if int(cnt) > 1:
                                                                        text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 1.0
                                                        else:
                                                            frame:
                                                                background "#000000"
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) hovered [SetVariable("hovered_artifact_id", item_id), Show("art_desc")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc")] at inventory_artifact_trans:
                                                                    hbox:
                                                                        xalign 0.0
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            if item_name_lines >= 2:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 ypos -3
                                                                            else:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 yalign 0.5
                                                                        text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffff00" yalign 0.5
                                                    else:
                                                        if button_state == 0:
                                                            frame:
                                                                background "#000000"
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                    hbox:
                                                                        xalign 0.0
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            if item_name_lines >= 2:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 ypos -3
                                                                            else:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffffff" xmaximum 200 yalign 0.5
                                                                    if int(cnt) > 1:
                                                                        text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 1.0
                                                        else:
                                                            frame:
                                                                background "#000000"
                                                                xysize (330, 90)
                                                                button action DoubleClickAction(button_key, ch.name, "use_consumable", (item_id,), "Использовать", "use_consumable", item_id) at inventory_artifact_trans:
                                                                    hbox:
                                                                        xalign 0.0
                                                                        spacing 10
                                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0
                                                                        hbox:
                                                                            spacing 10
                                                                            xsize 260
                                                                            if item_name_lines >= 2:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 ypos -3
                                                                            else:
                                                                                text "{font=determination.otf}{size=26}[item_name]{/font}{/size}" color "#ffff00" xmaximum 200 yalign 0.5
                                                                        text "{font=determination.otf}{size=26}х[int(cnt)]{/font}{/size}" color "#ffff00" yalign 0.5 xalign 1.0
                                    else:
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xalign 0.5
















                frame:
                    background "#ffffff"
                    #padding (10, 10)
                    xysize (405,40)
                    xpos 5 ypos -640

                    frame:
                        background "#000000"
                        #padding (10, 10)
                        xysize (400,35)
                        xpos -4 ypos -4


                        hbox:
                            #xalign 0.5

                            xalign 0.0
                            
                            spacing 0
                            fixed:                        
                                xalign 0.5
                                # Текст вкладки
                                if store.inventory_tab == "artifacts":
                                    text "{font=determination.otf}{size=35}Предметы" size 24 xalign 0.5 ypos -5
                                elif store.inventory_tab == "consumables":
                                    text "{font=determination.otf}{size=35}Расходники" size 24 xalign 0.5 ypos -5
                                elif store.inventory_tab == "weapons":
                                    text "{font=determination.otf}{size=35}Оружие" size 24 xalign 0.5 ypos -5
                                else:
                                    text "{font=determination.otf}{size=35}Расходники" size 24 xalign 0.5 ypos -5

                                if pokaz_desc == 0:
                                    imagebutton:
                                        at glowing
                                        
                                        idle "hide_fast_desc.png"
                                        hover "hide_fast_desc.png"
                                        action SetVariable("pokaz_desc", 1)
                                elif pokaz_desc == 1:
                                    imagebutton:
                                        at glowing
                                        
                                        idle "show_fast_desc.png"
                                        hover "show_fast_desc.png"
                                        action SetVariable("pokaz_desc", 2)
                                else:
                                    imagebutton:
                                        at glowing
                                        
                                        idle "show_full_desc.png"
                                        hover "show_full_desc.png"
                                        action SetVariable("pokaz_desc", 0)















                # Кнопки переключения между артефактами и consumables
                hbox:
                    ypos -754
                    xpos 45
                    spacing 10
                    if store.inventory_tab == "artifacts":
                        imagebutton:
                            idle "art_bel_chosen.png"
                            hover "art_bel_chosen.png"
                            action None
                        #textbutton "Артефакты *" action None

                        imagebutton:
                            idle "con_bel.png"
                            hover "con_zh.png"
                            action SetInventoryTabWithReset("consumables")

                        imagebutton:
                            idle "weap_bel.png"
                            hover "weap_zh.png"
                            action SetInventoryTabWithReset("weapons")

                        #textbutton "Consumables" action SetInventoryTabWithReset("consumables")



                    elif store.inventory_tab == "consumables":

                        imagebutton:
                            idle "art_bel.png"
                            hover "art_zh.png"
                            action SetInventoryTabWithReset("artifacts")

                        #textbutton "Артефакты" action SetInventoryTabWithReset("artifacts")

                        imagebutton:
                            idle "con_bel_chosen.png"
                            hover "con_bel_chosen.png"
                            action None

                        #textbutton "Consumables *" action None
                        imagebutton:
                            idle "weap_bel.png"
                            hover "weap_zh.png"
                            action SetInventoryTabWithReset("weapons")
                  
                    

                    else:
                        imagebutton:
                            idle "art_bel.png"
                            hover "art_zh.png"
                            action SetInventoryTabWithReset("artifacts")

                        imagebutton:
                            idle "con_bel.png"
                            hover "con_zh.png"
                            action SetInventoryTabWithReset("consumables")

                        imagebutton:
                            idle "weap_bel_chosen.png"
                            hover "weap_zh.png"
                            action None




























        vbox:
            xpos 5 ypos -31 spacing 5

            # Отладочная информация персонажа
            frame:
                background "#ffffff"
                padding (10, 10)
                xsize 650 ysize 65

                frame:
                    background "#000000"
                    padding (10, 10)
                    xsize 640 ysize 55
                    xalign 0.5 yalign 0.5

                    hbox:
                        
                        frame:
                            background "#ffffff"
                            #padding (10, 10)
                            xsize 300 ysize 65
                            xpos -15 ypos -15


                            frame:
                                background "#000000"
                                #padding (10, 10)
                                xsize 290 ysize 55
                                xalign 0.5 yalign 0.5

                                hbox:
                                    spacing 20 xalign 0.35
                                    add "[ch.nameeng]soul.png" xalign 0.5 yalign 0.7 xysize (40,40)
                                    text "{font=determination.otf}{size=50}[ch.name]" color "#ffffff" xalign 0.5 ypos -2


                        hbox:
                            ypos -15 xalign 0.5
                            spacing 20


                            xoffset (max(0, 4 - len([slot for slot in store.team_manager.team_slots if slot is not None])) * 35) #if store.team_manager is not None else 0

                           

                            # Крис
                            if store.pers_dict["Крис"].picked == 1:
                                if store.current_char == "Крис":
                                    imagebutton:
                                        idle "images/Krisheadcolored[sprite_suffix].png"
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Krisheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Крис"), SetVariable("chardes", store.pers_dict["Крис"]), SetVariable("chardesprepare", store.pers_dict["Крис"])]
                            # Азриель
                            if store.pers_dict["Азриель"].picked == 1:
                                if store.current_char == "Азриель":
                                    imagebutton:
                                        idle "images/Asrielheadcolored[sprite_suffix].png"
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Asrielheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Азриель"), SetVariable("chardes", store.pers_dict["Азриель"]), SetVariable("chardesprepare", store.pers_dict["Азриель"])]
                            # Чара
                            if store.pers_dict["Чара"].picked == 1:
                                if store.current_char == "Чара":
                                    imagebutton:
                                        idle "images/Charaheadcolored[sprite_suffix].png"
                                        
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Charaheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Чара"), SetVariable("chardes", store.pers_dict["Чара"]), SetVariable("chardesprepare", store.pers_dict["Чара"])]
                            # Фриск
                            if store.pers_dict["Фриск"].picked == 1:
                                if store.current_char == "Фриск":
                                    imagebutton:
                                        idle "images/Friskheadcolored[sprite_suffix].png"
                                        
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Friskheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Фриск"), SetVariable("chardes", store.pers_dict["Фриск"]), SetVariable("chardesprepare", store.pers_dict["Фриск"])]
                            # Иззи
                            if store.pers_dict["Иззи"].picked == 1:
                                if store.current_char == "Иззи":
                                    imagebutton:
                                        idle "images/Izzyheadcolored[sprite_suffix].png"
                                        
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Izzyheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Иззи"), SetVariable("chardes", store.pers_dict["Иззи"]), SetVariable("chardesprepare", store.pers_dict["Иззи"])]
                            # Кловер
                            if store.pers_dict["Кловер"].picked == 1:
                                if store.current_char == "Кловер":
                                    imagebutton:
                                        idle "images/Cloverheadcolored[sprite_suffix].png"
                                        
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Cloverheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Кловер"), SetVariable("chardes", store.pers_dict["Кловер"]), SetVariable("chardesprepare", store.pers_dict["Кловер"])]
                            # Седрик
                            if store.pers_dict["Седрик"].picked == 1:
                                if store.current_char == "Седрик":
                                    imagebutton:
                                        idle "images/Sedricheadcolored[sprite_suffix].png"
                                        
                                        action None
                                else:
                                    imagebutton:
                                        at dim_colors
                                        idle "images/Sedricheadcolored[sprite_suffix].png"
                                        
                                        action [SetCurrentCharWithReset("Седрик"), SetVariable("chardes", store.pers_dict["Седрик"]), SetVariable("chardesprepare", store.pers_dict["Седрик"])]








            # Отладочная информация персонажа
            frame:
                background "#ffffff"
                padding (10, 10)
                xsize 650 ysize 550

                frame:
                    background "#000000"
                    padding (10, 10)
                    xsize 640 ysize 540
                    xalign 0.5 yalign 0.5





                    hbox:

                        add "images/[ch.nameeng]miniportrait.png" xpos -13 ypos -13 xysize (300, 545)

                        # Вкладка 1: Боевые характеристики
                        vbox:
                            hbox:
                                xpos 40
                                text "{font=determination.otf}Характеристики" size 30 xalign 0.0
                                fixed:
                                    xalign 1.0 ypos -4
                                    xysize (40, 40)
                                    add FeednessPieChart(ch, size=40)
                            if store.stats_tab == 1:
                                vbox:
                                    ypos 20
                                    spacing 20
                                    xalign 0.5

                                    if store.hp_preview_enabled and ch.name in store.hp_preview_values:
                                        $ preview = store.hp_preview_values[ch.name]
                                        hbox:
                                            vbox:
                                                spacing 15

                                                if preview['hp_changed']:
                                                    $ hp_color = "#66ff66" if preview['max_hp'] > ch.max_hp else "#ff6666" if preview['max_hp'] < ch.max_hp else "#ffffff"
                                                    text "{font=determination.otf}{color=[hp_color]}Здоровье:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Здоровье:{/font}" size size_for_invent color "#ffffff"
                                                if preview['mp_changed']:
                                                    $ mp_color = "#66ff66" if preview['max_mp'] > ch.max_mp else "#ff6666" if preview['max_mp'] < ch.max_mp else "#ffffff"
                                                    text "{font=determination.otf}{color=[mp_color]}Мана:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Мана:{/font}" size size_for_invent color "#ffffff"
                                                if preview['atk_changed']:
                                                    $ atk_color = "#66ff66" if preview['atk'] > ch.base_atk else "#ff6666" if preview['atk'] < ch.base_atk else "#ffffff"
                                                    text "{font=determination.otf}{color=[atk_color]}Атака:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Атака:{/font}" size size_for_invent color "#ffffff"
                                                if preview['magic_changed']:
                                                    $ magic_color = "#66ff66" if preview['magic'] > ch.base_magic else "#ff6666" if preview['magic'] < ch.base_magic else "#ffffff"
                                                    text "{font=determination.otf}{color=[magic_color]}Магия:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Магия:{/font}" size size_for_invent color "#ffffff"
                                                if preview['accuracy_changed']:
                                                    $ accuracy_color = "#66ff66" if preview['accuracy'] > ch.base_dmgchance else "#ff6666" if preview['accuracy'] < ch.base_dmgchance else "#ffffff"
                                                    text "{font=determination.otf}{color=[accuracy_color]}Точность%:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Точность%:{/font}" size size_for_invent color "#ffffff"
                                                if preview['critrate_changed']:
                                                    $ critrate_color = "#66ff66" if preview['critrate'] > ch.base_critrate else "#ff6666" if preview['critrate'] < ch.base_critrate else "#ffffff"
                                                    text "{font=determination.otf}{color=[critrate_color]}Крит. шанс%:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Крит. шанс%:{/font}" size size_for_invent color "#ffffff"
                                                if preview['crit_changed']:
                                                    $ crit_color = "#66ff66" if preview['crit'] > ch.base_crit else "#ff6666" if preview['crit'] < ch.base_crit else "#ffffff"
                                                    text "{font=determination.otf}{color=[crit_color]}Крит. урон%:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Крит. урон%:{/font}" size size_for_invent color "#ffffff"

                                                if preview['def_changed']:
                                                    $ def_color = "#66ff66" if preview['defense'] > ch.base_def else "#ff6666" if preview['defense'] < ch.base_def else "#ffffff"
                                                    text "{font=determination.otf}{color=[def_color]}Защита:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Защита:{/font}" size size_for_invent color "#ffffff"
                                                if preview['tank_changed']:
                                                    $ tank_color = "#66ff66" if preview['tank'] > ch.total_tank else "#ff6666" if preview['tank'] < ch.total_tank else "#ffffff"
                                                    text "{font=determination.otf}{color=[tank_color]}Танк:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Танк:{/font}" size size_for_invent color "#ffffff"


                                            vbox:
                                                spacing 15

                                                if preview['hp_changed']:
                                                    $ hp_color = "#66ff66" if preview['max_hp'] > ch.max_hp else "#ff6666" if preview['max_hp'] < ch.max_hp else "#ffffff"
                                                    text "{font=determination.otf}{color=[hp_color]}[int(ch.max_hp)]>[int(preview['max_hp'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.current_hp)]/[int(ch.max_hp)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['mp_changed']:
                                                    $ mp_color = "#66ff66" if preview['max_mp'] > ch.max_mp else "#ff6666" if preview['max_mp'] < ch.max_mp else "#ffffff"
                                                    text "{font=determination.otf}{color=[mp_color]}[int(ch.max_mp)]>[int(preview['max_mp'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.current_mp)]/[int(ch.max_mp)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['atk_changed']:
                                                    $ atk_color = "#66ff66" if preview['atk'] > ch.base_atk else "#ff6666" if preview['atk'] < ch.base_atk else "#ffffff"
                                                    text "{font=determination.otf}{color=[atk_color]}[int(ch.base_atk)]>[int(preview['atk'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.base_atk)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['magic_changed']:
                                                    $ magic_color = "#66ff66" if preview['magic'] > ch.base_magic else "#ff6666" if preview['magic'] < ch.base_magic else "#ffffff"
                                                    text "{font=determination.otf}{color=[magic_color]}[int(ch.base_magic)]>[int(preview['magic'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.base_magic)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['accuracy_changed']:
                                                    $ accuracy_color = "#66ff66" if preview['accuracy'] > ch.base_dmgchance else "#ff6666" if preview['accuracy'] < ch.base_dmgchance else "#ffffff"
                                                    text "{font=determination.otf}{color=[accuracy_color]}[int(ch.base_dmgchance*100)]>[int(preview['accuracy']*100)]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.base_dmgchance*100)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['critrate_changed']:
                                                    $ critrate_color = "#66ff66" if preview['critrate'] > ch.base_critrate else "#ff6666" if preview['critrate'] < ch.base_critrate else "#ffffff"
                                                    text "{font=determination.otf}{color=[critrate_color]}[int(ch.base_critrate*100)]>[int(preview['critrate']*100)]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.base_critrate*100)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['crit_changed']:
                                                    $ crit_color = "#66ff66" if preview['crit'] > ch.base_crit else "#ff6666" if preview['crit'] < ch.base_crit else "#ffffff"
                                                    text "{font=determination.otf}{color=[crit_color]}[int(ch.base_crit*100)]>[int(preview['crit']*100)]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.base_crit*100)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['def_changed']:
                                                    $ def_color = "#66ff66" if preview['defense'] > ch.base_def else "#ff6666" if preview['defense'] < ch.base_def else "#ffffff"
                                                    text "{font=determination.otf}{color=[def_color]}[int(ch.base_def)]>[int(preview['defense'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.base_def)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview['tank_changed']:
                                                    $ tank_color = "#66ff66" if preview['tank'] > ch.total_tank else "#ff6666" if preview['tank'] < ch.total_tank else "#ffffff"
                                                    text "{font=determination.otf}{color=[tank_color]}[int(ch.total_tank)]>[int(preview['tank'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.total_tank)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                    else:

                                        hbox:
                                            vbox:
                                                spacing 15
                                                text "{font=determination.otf}Здоровье:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Мана:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Атака:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Магия:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Точность%:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Крит. шанс%:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Крит. урон%:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Защита:" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Танк:" size size_for_invent color "#ffffff"


                                            vbox:
                                                spacing 15
                                                text "{font=determination.otf}[int(ch.current_hp)]/[int(ch.max_hp)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.current_mp)]/[int(ch.max_mp)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.base_atk)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.base_magic)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.base_dmgchance*100)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.base_critrate*100)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.base_crit*100)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.base_def)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.total_tank)]{/font}" size size_for_invent color "#ffffff" xalign 0.5




                            # Вкладка 2: Дипломатические характеристики
                            else:
                                #text "{font=determination.otf}Характеристики" size 30 xpos 45
                                vbox:
                                    ypos 20
                                    spacing 40



                                    if store.hp_preview_enabled and ch.name in store.hp_preview_values:
                                        $ preview = store.hp_preview_values[ch.name]

                                        hbox:
                                            spacing 20
                                            xalign 0.5
                                            vbox:

                                                spacing 15

                                                if preview.get('socialization_changed', False):
                                                    $ socialization_color = "#66ff66" if preview['socialization'] > ch.socialization else "#ff6666" if preview['socialization'] < ch.socialization else "#ffffff"
                                                    text "{font=determination.otf}{color=[socialization_color]}Социализация:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Социализация:{/font}" size size_for_invent color "#ffffff"
                                                if preview.get('diplomacy_changed', False):
                                                    $ diplomacy_color = "#66ff66" if preview['diplomacy'] > ch.diplomacy else "#ff6666" if preview['diplomacy'] < ch.diplomacy else "#ffffff"
                                                    text "{font=determination.otf}{color=[diplomacy_color]}Дипломатия:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Дипломатия:{/font}" size size_for_invent color "#ffffff"
                                                if preview.get('charm_changed', False):
                                                    $ charm_color = "#66ff66" if preview['charm'] > ch.charm else "#ff6666" if preview['charm'] < ch.charm else "#ffffff"
                                                    text "{font=determination.otf}{color=[charm_color]}Очарование:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Очарование:{/font}" size size_for_invent color "#ffffff"
                                                null height 30
                                                if preview.get('perception_changed', False):
                                                    $ perception_color = "#66ff66" if preview['perception'] > ch.perception else "#ff6666" if preview['perception'] < ch.perception else "#ffffff"
                                                    text "{font=determination.otf}{color=[perception_color]}Восприятие:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Восприятие:{/font}" size size_for_invent color "#ffffff"
                                                if preview.get('rhetoric_changed', False):
                                                    $ rhetoric_color = "#66ff66" if preview['rhetoric'] > ch.rhetoric else "#ff6666" if preview['rhetoric'] < ch.rhetoric else "#ffffff"
                                                    text "{font=determination.otf}{color=[rhetoric_color]}Риторика:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Риторика:{/font}" size size_for_invent color "#ffffff"
                                                if preview.get('artistry_changed', False):
                                                    $ artistry_color = "#66ff66" if preview['artistry'] > ch.artistry else "#ff6666" if preview['artistry'] < ch.artistry else "#ffffff"
                                                    text "{font=determination.otf}{color=[artistry_color]}Артистизм:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Артистизм:{/font}" size size_for_invent color "#ffffff"
                                                if preview.get('comfort_changed', False):
                                                    $ comfort_color = "#66ff66" if preview['comfort'] > ch.comfort else "#ff6666" if preview['comfort'] < ch.comfort else "#ffffff"
                                                    text "{font=determination.otf}{color=[comfort_color]}Комфорт:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Комфорт:{/font}" size size_for_invent color "#ffffff"
                                                if preview.get('power_changed', False):
                                                    $ power_color = "#66ff66" if preview['power'] > ch.power else "#ff6666" if preview['power'] < ch.power else "#ffffff"
                                                    text "{font=determination.otf}{color=[power_color]}Власть:{/color}{/font}" size size_for_invent
                                                else:
                                                    text "{font=determination.otf}Власть:{/font}" size size_for_invent color "#ffffff"

                                            vbox:


                                                spacing 15


                                                if preview.get('socialization_changed', False):
                                                    $ socialization_color = "#66ff66" if preview['socialization'] > ch.socialization else "#ff6666" if preview['socialization'] < ch.socialization else "#ffffff"
                                                    text "{font=determination.otf}{color=[socialization_color]}[int(ch.socialization)]>[int(preview['socialization'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.socialization)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview.get('diplomacy_changed', False):
                                                    $ diplomacy_color = "#66ff66" if preview['diplomacy'] > ch.diplomacy else "#ff6666" if preview['diplomacy'] < ch.diplomacy else "#ffffff"
                                                    text "{font=determination.otf}{color=[diplomacy_color]}[int(ch.diplomacy)]>[int(preview['diplomacy'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.diplomacy)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview.get('charm_changed', False):
                                                    $ charm_color = "#66ff66" if preview['charm'] > ch.charm else "#ff6666" if preview['charm'] < ch.charm else "#ffffff"
                                                    text "{font=determination.otf}{color=[charm_color]}[int(ch.charm)]>[int(preview['charm'])]%{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.charm)]%{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                null height 30
                                                if preview.get('perception_changed', False):
                                                    $ perception_color = "#66ff66" if preview['perception'] > ch.perception else "#ff6666" if preview['perception'] < ch.perception else "#ffffff"
                                                    text "{font=determination.otf}{color=[perception_color]}[int(ch.perception)]>[int(preview['perception'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.perception)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview.get('rhetoric_changed', False):
                                                    $ rhetoric_color = "#66ff66" if preview['rhetoric'] > ch.rhetoric else "#ff6666" if preview['rhetoric'] < ch.rhetoric else "#ffffff"
                                                    text "{font=determination.otf}{color=[rhetoric_color]}[int(ch.rhetoric)]>[int(preview['rhetoric'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.rhetoric)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview.get('artistry_changed', False):
                                                    $ artistry_color = "#66ff66" if preview['artistry'] > ch.artistry else "#ff6666" if preview['artistry'] < ch.artistry else "#ffffff"
                                                    text "{font=determination.otf}{color=[artistry_color]}[int(ch.artistry)]>[int(preview['artistry'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.artistry)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview.get('comfort_changed', False):
                                                    $ comfort_color = "#66ff66" if preview['comfort'] > ch.comfort else "#ff6666" if preview['comfort'] < ch.comfort else "#ffffff"
                                                    text "{font=determination.otf}{color=[comfort_color]}[int(ch.comfort)]>[int(preview['comfort'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.comfort)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                if preview.get('power_changed', False):
                                                    $ power_color = "#66ff66" if preview['power'] > ch.power else "#ff6666" if preview['power'] < ch.power else "#ffffff"
                                                    text "{font=determination.otf}{color=[power_color]}[int(ch.power)]>[int(preview['power'])]{/color}{/font}" size size_for_invent xalign 0.5
                                                else:
                                                    text "{font=determination.otf}[int(ch.power)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                    else:
                                        hbox:
                                            spacing 20
                                            xalign 0.5

                                            vbox:
                                                spacing 15
                                                text "{font=determination.otf}Социализация:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Дипломатия:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Очарование:{/font}" size size_for_invent color "#ffffff"
                                                null height 30
                                                text "{font=determination.otf}Восприятие:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Риторика:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Артистизм:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Комфорт:{/font}" size size_for_invent color "#ffffff"
                                                text "{font=determination.otf}Власть:{/font}" size size_for_invent color "#ffffff"

                                            vbox:
                                                spacing 15
                                                text "{font=determination.otf}[int(ch.socialization)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.diplomacy)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.charm)]%{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                null height 30
                                                text "{font=determination.otf}[int(ch.perception)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.rhetoric)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.artistry)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.comfort)]{/font}" size size_for_invent color "#ffffff" xalign 0.5
                                                text "{font=determination.otf}[int(ch.power)]{/font}" size size_for_invent color "#ffffff" xalign 0.5















            hbox:
                #xpos 305
                yalign 1.0 yoffset -10
                spacing 5
                imagebutton:
                    yoffset 10
                    idle "char_full_desc.png"
                    hover "char_full_desc_zh.png" # Optional: different image on hover
                    # Text must be a child of the button, not a property                
                    hovered [SetVariable("chardesprepare", ch), Show("fullstats1_copy"), SetVariable("presize_zh", 1)]
                    unhovered [Hide("fullstats1_copy"), SetVariable("presize_zh", 0)]
                    action [SetVariable("screenstate", "доступен"), SetVariable("chardes", ch), SetVariable("sscreenstate_style", "статический"), SetVariable("chardespos", store.current_char + "нажат")]

                    
                hbox:
                    spacing 5
                    if store.stats_tab == 1:

                        imagebutton:
                            idle "fightstats_opened.png"
                            hover "fightstats_opened.png"
                            action None

                        #textbutton "Боевая*" action None



                        imagebutton:
                            idle "dipstats_bel.png"
                            hover "dipstats_zh.png"
                            unhovered SetVariable("soc_zh", 0)
                            hovered SetVariable("soc_zh", 1)
                            action [SetStatsTabAction(2),SetVariable("soc_zh", 0)]
                        #textbutton "Дипломатия" action SetStatsTabAction(2)
                    else:


                        imagebutton:
                            idle "fightstats_bel.png"
                            hover "fightstats_zh.png"
                            unhovered SetVariable("fight_zh", 0)
                            hovered SetVariable("fight_zh", 1)
                            action [SetStatsTabAction(1),SetVariable("fight_zh", 0)]



                        imagebutton:
                            idle "dipstats_opened.png"
                            hover "dipstats_opened.png"
                            action None

            
 

                    #textbutton "Боевая" action SetStatsTabAction(1)
                    #textbutton "Дипломатия*" action None





                hbox:
                    $ has_washed_artifacts = any(store.artifact_wash_state.get(inst_idx, 0) == 1 for inst_idx, inst in enumerate(store.artifact_instances) if inst["id"] != "trash")


                    ypos -650 xpos 40 xoffset -240
                    textbutton "Магазин" action [Show("shop_screen"), Hide("artifacts_menu")]

                    # Кнопка опознания
                    textbutton "Опознать" action Show("identify_screen")

                    # Кнопка стирки - светло-зелёная, если есть постиранные артефакты
                    if has_washed_artifacts:
                        textbutton "Постирать" action Show("wash_screen"):
                            text_color "#66ff66"
                            text_hover_color "#99ff99"
                    else:
                        textbutton "Постирать" action Show("wash_screen")















        # Нижний hbox с Grid слотов
        hbox:
            xpos -400
            spacing 10

            # Grid (2 на 6) со слотами
            # Количество ячеек зависит от уровня (1 уровень = 1 ячейка) + extraequip
            frame:
                background None #"#555555"
                padding (10, 10)
                vbox:
                    spacing 5
                    #text "=== СЛОТЫ ЭКИПИРОВКИ ===" size 18 color "#ffffff"
                    #text "Всего слотов: [int(ch.level)] (уровень) + [int(ch.extraequip)] (extra) = [int(ch.get_max_slots())]" size 14 color "#ffffff"

                    # --- Активные/неполные сетовые бонусы ---
                    #if store.artifact_sets:
                    #    vbox:
                    #        ypos 0
                    #        spacing 2
                    #        $ _set_status = store.get_set_status(ch)
                    #        for _sid, _sdata in store.artifact_sets.items():
                    #            $ _ec, _req, _act = _set_status.get(_sid, (0, 1, False))
                    #            $ _sname = _sdata["name"]
                    #            if _act:
                    #                text "{font=determination.otf}{size=16}✓ [_sname] ([_ec]/[_req]){/font}{/size}" color "#66ff66"
                    #            else:
                    #                text "{font=determination.otf}{size=16}✗ [_sname] ([_ec]/[_req]){/font}{/size}" color "#ff6666"

                    # Grid 2 на 6, но отображаем только нужное количество ячеек
                    grid 2 6:
                        ypos 30
                        spacing 5
                        # Вычисляем общее количество слотов
                        $ total_slots = ch.get_max_slots()
                        for i in range(12):  # 2x6 = 12 ячеек максимум
                            if i < total_slots:
                                # Проверяем, занят ли этот слот
                                $ slot_item = ch.equipped_artifacts[i] if i < len(ch.equipped_artifacts) else None

                                # Пропускаем "мусорные" артефакты в слотах
                                if slot_item == "trash":
                                    $ slot_item = None

                                frame:
                                    background "#ffffff"
                                    xysize (70, 70)

                                    frame:
                                        xalign 0.5
                                        yalign 0.5
                                        background "#000000"
                                        xysize (60, 60)



                                        if slot_item:
                                            vbox:
                                                xoffset -15 yoffset -15
                                                spacing 2
                                                if pokaz_desc > 0:
                                                    button action UnequipArtifactAction(ch.name, i) hovered [SetVariable("hovered_artifact_id", slot_item), Show("art_desc"), PreviewArtifactStatsAction(ch.name, slot_item, "unequip")] unhovered [SetVariable("hovered_artifact_id", None), Hide("art_desc"), Function(store.update_hp_preview, None)] at [artifact_menu]:
                                                        add f"{store.artifact_names.get(slot_item, slot_item)}.png" xysize (50, 50) xalign 0.0 yalign 0.0
                
                                                else:
                                                    button action UnequipArtifactAction(ch.name, i) hovered [SetVariable("hovered_artifact_id", slot_item), PreviewArtifactStatsAction(ch.name, slot_item, "unequip")] unhovered [SetVariable("hovered_artifact_id", None), Function(store.update_hp_preview, None)] at [artifact_menu]:
                                                        add f"{store.artifact_names.get(slot_item, slot_item)}.png" xysize (50, 50) xalign 0.0 yalign 0.0
                                                        

                                            if slot_item and store.is_artifact_in_set(slot_item):
                                                $ _flash = store.set_event_flash.get(slot_item, None)
                                                if _flash and renpy.get_game_runtime() < _flash[0]:
                                                    $ _flash_color = "#ffcc00" if _flash[1] == "equip" else "#ff6666"
                                                    add Solid(_flash_color, xysize=(70, 70)) at alpha_set



                                                # Кнопка опознания экипированного артефакта
                                                #$ can_identify = store.artifact_identifiable.get(slot_item, 0) == 1
                                                #if can_identify:
                                                #    hbox:
                                                #        spacing 2
                                                #        # Находим индекс экземпляра этого артефакта
                                                #        $ inst_idx = None
                                                #        for idx, inst in enumerate(store.artifact_instances):
                                                #            if inst["id"] == slot_item and inst["owner"] == ch.name:
                                                #                $ inst_idx = idx
                                                #                break
                                                #        if inst_idx is not None:
                                                #            $ is_identified = store.artifact_identified_state.get(inst_idx, 0) == 1
                                                #            if not is_identified:
                                                #                textbutton "🔍" action IdentifyEquippedArtifactAction(ch.name, i):
                                                #                    text_size 10
                                                #                    text_color "#ccccff"
                                                #                    text_hover_color "#ffffff"
                                                #            else:
                                                #                textbutton "✓" action None:
                                                #                    text_size 10
                                                #                    text_color "#66ff66"






                                        else:
                                            #text "Слот [i+1]" size 12 color "#ffffff" xalign 0.5 yalign 0.5
                                            text "{font=determination.otf}---" size 25 color "#ffffff" xalign 0.5 yalign 0.5
                            else:
                                pass
                                # Пустая ячейка (неактивная)
                                #frame:
                                #    background "#333333"
                                #    xysize (80, 80)
    imagebutton:
        idle "unequipall.png"
        hover "unequipall2.png"
        action [UnequipAllArtifactsAction(), SetVariable("unequip_zh", 0)]
        hovered [PreviewUnequipAllArtifactsAction(), SetVariable("unequip_zh", 1)]
        unhovered [Function(store.update_hp_preview, None), SetVariable("unequip_zh", 0)]
        xpos 1100 ypos 35



    # Отладочная информация для Криса
    vbox:
        xalign 1.0
        yalign 0.5
        spacing 2
        if store.pers_dict and "Крис" in store.pers_dict:
            $ kris = store.pers_dict["Крис"]
            text "=== КРИС (DEBUG) ===" size 18 color "#ffff00"
            text "HP: [kris.current_hp]/[kris.max_hp]" size 14 color "#ffffff"
            text "MP: [kris.current_mp]/[kris.max_mp]" size 14 color "#ffffff"
            text "Атака: [kris.bonus_atk]" size 14 color "#ffffff"
            text "Защита: [kris.bonus_def]" size 14 color "#ffffff"
            text "Магия: [kris.bonus_magic]" size 14 color "#ffffff"
            text "Точность: [kris.bonus_dmgchance]" size 14 color "#ffffff"
            text "Крит шанс: [kris.bonus_critrate]" size 14 color "#ffffff"
            text "Крит урон: [kris.bonus_crit]" size 14 color "#ffffff"
            text "Tank: [kris.bonus_tank]" size 14 color "#ffffff"
            text "=== ДЕБАФЫ/БАФФЫ ===" size 18 color "#ffff00"
            text "[store.is_washing]" size 20 color "#ffff00"

            textbutton "бой" action Jump("fightstarts")


            if kris.bloodshed_debuff > 0:
                text "Кровотечение: [kris.bloodshed_debuff]" size 14 color "#ff0000"
            elif kris.bloodshed_debuff < 0:
                text "Кровотечение: [kris.bloodshed_debuff]" size 14 color "#00ff00"
            else:
                text "Кровотечение: [kris.bloodshed_debuff]" size 14 color "#888888"
            if kris.prone_debuff > 0:
                text "Prone: [kris.prone_debuff]" size 14 color "#ff0000"
            elif kris.prone_debuff < 0:
                text "Prone: [kris.prone_debuff]" size 14 color "#00ff00"
            else:
                text "Prone: [kris.prone_debuff]" size 14 color "#888888"
            if kris.atk_debuff > 0:
                text "Атака: [kris.atk_debuff]" size 14 color "#ff0000"
            elif kris.atk_debuff < 0:
                text "Атака: [kris.atk_debuff]" size 14 color "#00ff00"
            else:
                text "Атака: [kris.atk_debuff]" size 14 color "#888888"
            if kris.def_debuff > 0:
                text "Защита: [kris.def_debuff]" size 14 color "#ff0000"
            elif kris.def_debuff < 0:
                text "Защита: [kris.def_debuff]" size 14 color "#00ff00"
            else:
                text "Защита: [kris.def_debuff]" size 14 color "#888888"
            if kris.magic_debuff > 0:
                text "Магия: [kris.magic_debuff]" size 14 color "#ff0000"
            elif kris.magic_debuff < 0:
                text "Магия: [kris.magic_debuff]" size 14 color "#00ff00"
            else:
                text "Магия: [kris.magic_debuff]" size 14 color "#888888"
            if kris.accuracy_debuff > 0:
                text "Точность: [kris.accuracy_debuff]" size 14 color "#ff0000"
            elif kris.accuracy_debuff < 0:
                text "Точность: [kris.accuracy_debuff]" size 14 color "#00ff00"
            else:
                text "Точность: [kris.accuracy_debuff]" size 14 color "#888888"
            if kris.critrate_debuff > 0:
                text "Крит шанс: [kris.critrate_debuff]" size 14 color "#ff0000"
            elif kris.critrate_debuff < 0:
                text "Крит шанс: [kris.critrate_debuff]" size 14 color "#00ff00"
            else:
                text "Крит шанс: [kris.critrate_debuff]" size 14 color "#888888"
            if kris.critdmg_debuff > 0:
                text "Крит урон: [kris.critdmg_debuff]" size 14 color "#ff0000"
            elif kris.critdmg_debuff < 0:
                text "Крит урон: [kris.critdmg_debuff]" size 14 color "#00ff00"
            else:
                text "Крит урон: [kris.critdmg_debuff]" size 14 color "#888888"
            if kris.tank_debuff > 0:
                text "Танк: [kris.tank_debuff]" size 14 color "#ff0000"
            elif kris.tank_debuff < 0:
                text "Танк: [kris.tank_debuff]" size 14 color "#00ff00"
            else:
                text "Танк: [kris.tank_debuff]" size 14 color "#888888"

    #add "Спрайт-0001.png" xpos 500 ypos 500 xsize 40 ysize 40
    #   add "Спрайт-0001.png" xpos 550 ypos 550 xsize 120 ysize 120

    #add DynamicDisplayable(white_bar_func) at white_bar_transf
    #add DynamicDisplayable(soul_cursor) at white_bar_transf
    
    hbox:
        xpos 510 ypos 660
        if presize_zh == 0:
            text "Подробнее" 
        else:
            text "Подробнее" color "#ffff00"
        add "char_precise.png" xysize (40,40) 

    hbox:
        xpos 800 ypos 660
        if fight_zh == 0:
            text "Бой" 
        else:
            text "Бой" color "#ffff00"
        add "fight_sign.png" yoffset -5
    hbox:
        xpos 970 ypos 660
        if soc_zh == 0:
            text "Соц" 
        else:
            text "Соц" color "#ffff00"
        add "social_sign.png" yoffset -5

    vbox:
        xpos 1110 ypos 50
        if unequip_zh == 1:
            text "Снять всё" color "#ffff00" size 22
        else:
            text "Снять всё" size 22


    imagebutton:
        idle "sets_ency.png"
        hover "sets_ency2.png"
        action Show("sets_encyclopedia") xpos 1100 ypos 652
        hovered SetVariable("ency", "zh")
        unhovered SetVariable("ency", None)
    if store.ency == "zh":
        text "Сеты" color "#ffff00" xpos 1115 ypos 660    
    else:
        text "Сеты" xpos 1115 ypos 660    

default ency = None




transform alpha_set:
    xalign 0.5 yalign 0.5
    alpha 0.0 
    easein 0.5 blur 100 alpha 1 
    easeout 0.5 alpha 0.0

    




default presize_zh = 0
default fight_zh = 0
default soc_zh = 0


transform artifact_menu:
    on hover:
        easein 0.15 matrixcolor BrightnessMatrix(0.08)
    on idle:
        easeout 0.15 matrixcolor BrightnessMatrix(0.0)
    

transform inventory_artifact_trans:
    
    on hover:
        easein 0.15 zoom 1.1
    on idle:
        easeout 0.15 zoom 1.0





screen switch_char_inventory:
    add "nameswitch.png"
    add "portraitswitch.png"






















































































































#    ▄████████    ▄█    █▄     ▄██████▄     ▄███████▄
#   ███    ███   ███    ███   ███    ███   ███    ███
#   ███    █▀    ███    ███   ███    ███   ███    ███
#   ███         ▄███▄▄▄▄███▄▄ ███    ███   ███    ███
# ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ ▀█████████▀
#          ███   ███    ███   ███    ███   ███
#    ▄█    ███   ███    ███   ███    ███   ███
#  ▄████████▀    ███    █▀     ▀██████▀   ▄████▀







default quittrade_zh = 0
default deny_zh = 0
default accept_zh = 0




# ------------------------------------------------------------
# 6) ЭКРАН МАГАЗИНА
# ------------------------------------------------------------

label from_shop_to_trader:
    hide screen shop_screen
    hide screen trader_screen_background
    hide screen trader_screen_options
    call screen trader_screen
    #call screen trader_screen_options

screen shop_screen():



    key "K_ESCAPE" action Jump("from_shop_to_trader")
    key "K_TAB" action None

    tag menu
    modal True

    # Инициализация торговца при первом открытии
    on "show" action Function(store.init_merchant)
    # timer 3.0 action SetMerchantAction("merchant2")   # ← ОТЛАДОЧНЫЙ ТАЙМЕР УДАЛЁН

    # Главный hbox с 3 колонками
    hbox:
        spacing -20
        xpos 20 ypos 20

        # 1 vbox: переключатели, наш инвентарь, наши деньги
        vbox:
            xpos -10
            ypos -15
            spacing 10
            xsize 380

            # 1.1 Vbox: Text "вкладка которую мы выбрали", перечень предметов нашего инвентаря
            frame:
                yoffset 75
                background "#ffffff"
                padding (10, 10)
                xysize (355, 50)
                frame:
                    background "#000000"
                    xysize (345, 40)
                    xalign 0.5 yalign 0.5




            # 1.2 hbox из text/button для переключения между артефактами и расходниками
            hbox:
                yoffset -55 xoffset 15
                spacing 10
                if store.player_shop_tab == "artifacts":
                    imagebutton:
                        idle "art_bel_chosen.png"
                        hover "art_bel_chosen.png"
                        action None
                    imagebutton:
                        idle "con_bel.png"
                        hover "con_zh.png"
                        action SetPlayerShopTabAction("consumables")
                    imagebutton:
                        idle "weap_bel.png"
                        hover "weap_zh.png"
                        action SetPlayerShopTabAction("weapons")
                elif store.player_shop_tab == "consumables":
                    imagebutton:
                        idle "art_bel.png"
                        hover "art_zh.png"
                        action SetPlayerShopTabAction("artifacts")
                    imagebutton:
                        idle "con_bel_chosen.png"
                        hover "con_bel_chosen.png"
                        action None
                    imagebutton:
                        idle "weap_bel.png"
                        hover "weap_zh.png"
                        action SetPlayerShopTabAction("weapons")
                else:
                    imagebutton:
                        idle "art_bel.png"
                        hover "art_zh.png"
                        action SetPlayerShopTabAction("artifacts")
                    imagebutton:
                        idle "con_bel.png"
                        hover "con_zh.png"
                        action SetPlayerShopTabAction("consumables")
                    imagebutton:
                        idle "weap_bel_chosen.png"
                        hover "weap_bel_chosen.png"
                        action None

            frame:
                ypos -15
                yoffset -15
                background "#ffffff"
                padding (10, 10)
                xysize (355, 530)
                frame:
                    background "#000000"
                    padding (10, 10)
                    xysize (345, 520)
                    xalign 0.5 yalign 0.5

                    # Вычисляем количество предметов для текущей вкладки игрока
                    $ player_artifact_count = 0
                    $ player_consumable_count = 0
                    $ player_weapon_count = 0
                    if store.artifact_instances:
                        for inst_idx, inst in enumerate(store.artifact_instances):
                            if inst_idx not in store.player_selling:
                                $ artifact_id = inst["id"]
                                if artifact_id != "trash":
                                    $ in_wash_slot = store.is_artifact_in_wash_slot(inst_idx)
                                    if not in_wash_slot:
                                        $ player_artifact_count += 1
                    if store.consumable_inventory:
                        for item_id, cnt in store.consumable_inventory.items():
                            $ available_count = max(0, cnt - store.player_selling_consumables.count(item_id))
                            if available_count > 0:
                                if item_id.startswith("wep_"):
                                    $ player_weapon_count += 1
                                else:
                                    $ player_consumable_count += 1
                    $ player_artifacts_need_scroll = player_artifact_count > 6
                    $ player_consumables_need_scroll = player_consumable_count > 6
                    $ player_weapons_need_scroll = player_weapon_count > 6
                    if store.player_shop_tab == "artifacts":
                        $ player_needs_scroll = player_artifacts_need_scroll
                    elif store.player_shop_tab == "weapons":
                        $ player_needs_scroll = player_weapons_need_scroll
                    else:
                        $ player_needs_scroll = player_consumables_need_scroll






                    viewport:
                        xalign 0.0 yalign 0.5
                        id "player_inventory_viewport"
                        xysize (345, 520)
                        if player_needs_scroll:
                            scrollbars "vertical"
                        #draggable True
                        mousewheel True


                        #вкладка артефакты
                        vbox:
                            xoffset -10
                            yalign 0.5
                            spacing -5
                            # Содержимое вкладки артефактов
                            if store.player_shop_tab == "artifacts":
                                if store.artifact_instances:
                                    for inst_idx, inst in enumerate(store.artifact_instances):
                                        if inst_idx not in store.player_selling:
                                            $ artifact_id = inst["id"]
                                            $ owner = inst.get("owner")

                                            # Пропускаем "мусорные" артефакты
                                            if artifact_id == "trash":
                                                continue

                                            # Пропускаем артефакты в стиральной машинке (in washing machine = 1)
                                            $ in_wash_slot = store.is_artifact_in_wash_slot(inst_idx)
                                            if in_wash_slot:
                                                continue

                                            # Постиранные артефакты (get_washed = 2) видны в магазине
                                            $ base_price = store.artifact_prices.get(artifact_id, 0)


                                            frame:
                                                xoffset -10
                                                yoffset -20
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "right"), SetVariable("hovered_artifact_id", artifact_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", None ), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToPlayerSellingAction(inst_idx)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 290 ysize 80 xalign 0.0
                                                        if owner:
                                                            $ owner_data = store.pers_dict[owner]
                                                            add "images/[owner_data.nameeng]headcolored.png" size (50, 50) xalign 0.0 yalign 0.5
                                                        else:
                                                            add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            xsize 220
                                                            yalign 0.45
                                                            text "{font=determination.otf}{size=24}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                vbox:
                                                    xoffset 140
                                                    yoffset 5
                                                    xalign 0.5 yalign 0.5
                                                    null width 10
                                                    text "{font=determination.otf}[int(base_price)]" size 20 color "#ffff00" xalign 1.0 ypos 5
                                else:
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xpos 140

                            # Содержимое вкладки оружия
                            elif store.player_shop_tab == "weapons":
                                if store.consumable_inventory:
                                    for item_id, cnt in store.consumable_inventory.items():
                                        $ available_count = max(0, cnt - store.player_selling_consumables.count(item_id))
                                        if available_count > 0 and item_id.startswith("wep_"):
                                            $ base_price = store.consumable_prices.get(item_id, 0)

                                            frame:
                                                xoffset -10
                                                yoffset -25
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "right"), SetVariable("hovered_artifact_id", item_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToPlayerSellingConsumablesAction(item_id)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 290 ysize 90 xalign 0.0
                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            xsize 220
                                                            yalign 0.45
                                                            if available_count == 1:
                                                                text "{font=determination.otf}{size=24}[store.consumable_names.get(item_id, item_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                            else:
                                                                text "{font=determination.otf}{size=22}[store.consumable_names.get(item_id, item_id)](х[int(available_count)]){/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                vbox:
                                                    xoffset 140
                                                    yoffset 10
                                                    xalign 0.5 yalign 0.5
                                                    null width 10
                                                    text "{font=determination.otf}[int(base_price)]" size 20 color "#ffff00" xalign 1.0 ypos 5
                                else:
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xpos 140

                            # Содержимое вкладки consumables
                            else:
                                if store.consumable_inventory:
                                    for item_id, cnt in store.consumable_inventory.items():
                                        $ available_count = max(0, cnt - store.player_selling_consumables.count(item_id))
                                        if available_count > 0 and not item_id.startswith("wep_"):
                                            $ base_price = store.consumable_prices.get(item_id, 0)

                                            frame:
                                                xoffset -10
                                                yoffset -25
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "right"), SetVariable("hovered_artifact_id", item_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToPlayerSellingConsumablesAction(item_id)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 290 ysize 90 xalign 0.0
                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            xsize 220
                                                            yalign 0.45
                                                            if available_count == 1:
                                                                text "{font=determination.otf}{size=24}[store.consumable_names.get(item_id, item_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                            else:
                                                                text "{font=determination.otf}{size=22}[store.consumable_names.get(item_id, item_id)](х[int(available_count)]){/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                vbox:
                                                    xoffset 140
                                                    yoffset 10
                                                    xalign 0.5 yalign 0.5
                                                    null width 10
                                                    text "{font=determination.otf}[int(base_price)]" size 20 color "#ffff00" xalign 1.0 ypos 5
                                else:
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xpos 140

            # 1.3 Frame с переменной, обозначающей наши деньги
            frame:
                ypos -30
                background "#ffffff"
                padding (10, 10)
                xysize (355, 50)
                frame:
                    background "#000000"
                    xysize (345, 40)
                    xalign 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "{font=determination.otf}{size=30}Деньги: [store.money] золота{/font}{/size}" color "#ffff00" xalign 0.5 ypos -5






























        # 2 vbox: центр экрана с товарами для обмена и прочим
        vbox:
            spacing 10
            xsize 380


            # 2.2 надпись «к оплате/к получению: х»
            frame:
                xalign 0.5
                background "#ffffff"
                padding (10, 10)
                xysize (510, 50)
                frame:
                    background "#000000"
                    xysize (500, 40)
                    xalign 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        $ trade_cost = store.calculate_trade_cost()
                        if trade_cost >= 0:
                            text "{font=determination.otf}{size=30}К оплате: [trade_cost] золота{/font}{/size}" color "#ff6666" xalign 0.5 ypos -5
                        else:
                            text "{font=determination.otf}{size=30}К получению: [-trade_cost] золота{/font}{/size}" color "#66ff66" xalign 0.5 ypos -5

            # 2.3 hbox с двумя vbox
            hbox:
                spacing 10

                # 2.3.1 vbox: vbox из наших товаров на продажу, кнопка очистить всё
                vbox:
                    spacing 5
                    xsize 185

                    frame:
                        background "#ffffff"
                        padding (10, 10)
                        xysize (250, 40)
                        frame:
                            background "#000000"
                            xysize (240, 30)
                            xalign 0.5 yalign 0.5
                            text "{font=determination.otf}{size=25}На продажу{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5

                    frame:
                        ypos -10
                        background "#ffffff"
                        padding (10, 10)
                        xysize (250, 530)
                        frame:
                            background "#000000"
                            padding (10, 10)
                            xysize (240, 520)
                            xalign 0.5 yalign 0.5

                            # Вычисляем количество товаров на продажу
                            $ player_selling_count = len(store.player_selling) + len(store.player_selling_consumables)
                            $ player_selling_needs_scroll = player_selling_count >= 8

                            viewport:
                                ypos -10
                                id "player_selling_viewport"
                                xysize (240, 520)
                                if player_selling_needs_scroll:
                                    scrollbars "vertical"
                                draggable True
                                mousewheel True
                                vbox:

                                    spacing 15
                                    # Сначала артефакты
                                    if store.player_selling:
                                        for inst_idx in store.player_selling:
                                            if inst_idx < len(store.artifact_instances):
                                                $ inst = store.artifact_instances[inst_idx]
                                                $ artifact_id = inst["id"]
                                                $ owner = inst.get("owner")

                                                # Пропускаем "мусорные" артефакты
                                                if artifact_id == "trash":
                                                    continue
                                                $ base_price = store.artifact_prices.get(artifact_id, 0)
                                                $ price = store.get_player_sell_price(base_price)

                                                frame:
                                                    xoffset -10
                                                    background "#000000"
                                                    padding (5, 5)
                                                    xysize (240, 60)
                                                    $ hovered_actions = [SetVariable("xoffset_for_art_desc", "right"), SetVariable("hovered_artifact_id", artifact_id)]
                                                    $ unhovered_actions = [SetVariable("xoffset_for_art_desc", None), SetVariable("hovered_artifact_id", None)]
                                                    if pokaz_desc > 0:
                                                        $ hovered_actions.append(Show("art_desc"))
                                                        $ unhovered_actions.append(Hide("art_desc"))
                                                    $ button_action = [RemoveFromPlayerSellingAction(inst_idx)]
                                                    if pokaz_desc > 0:
                                                        $ button_action.append(Hide("art_desc"))
                                                    button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                        hbox:
                                                            xsize 180 xalign 0.0 yalign 0.5
                                                            if owner:
                                                                $ owner_data = store.pers_dict[owner]
                                                                add "images/[owner_data.nameeng]headcolored.png" size (50, 50) xalign 0.0 yalign 0.5
                                                            else:
                                                                add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                            hbox:
                                                                yalign 0.5
                                                                text "{font=determination.otf}{size=18}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                        hbox:
                                                            xoffset 90
                                                            #yoffset -5
                                                            xalign 0.5 yalign 0.5

                                                            text "{font=determination.otf}[int(price)]" size 18 color "#ffff00" #ypos 5

                                    # Затем consumables
                                    if store.player_selling_consumables:
                                        for item_id in dict.fromkeys(store.player_selling_consumables):
                                            $ stack_count = store.player_selling_consumables.count(item_id)
                                            $ base_price = store.consumable_prices.get(item_id, 0)
                                            $ price = store.get_player_sell_price(base_price) * stack_count

                                            frame:
                                                #yoffset -10
                                                xoffset -10
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (240, 60)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "right"), SetVariable("hovered_artifact_id", item_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", None), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToPlayerSellingConsumablesAction(item_id)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 180 xalign 0.0 yalign 0.5
                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            yalign 0.5
                                                            if stack_count == 1:
                                                                text "{font=determination.otf}{size=18}[store.consumable_names.get(item_id, item_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                            else:
                                                                text "{font=determination.otf}{size=18}[store.consumable_names.get(item_id, item_id)](х[stack_count]){/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                    hbox:
                                                        xoffset 90
                                                        #yoffset -5
                                                        xalign 0.5 yalign 0.45
                                                        text "{font=determination.otf}[int(price)]" size 18 color "#ffff00" xalign 1.0 ypos 5

                                    # Если оба списка пусты
                                    if not store.player_selling and not store.player_selling_consumables:
                                        vbox:
                                            xalign 0.5
                                            text "{font=determination.otf}{size=20}---" color "#ffffff" xpos 100


                    #textbutton "Очистить всё" action ClearTradeListsAction():
                    #    xsize 185
                    #    text_size 14
                    #    text_color "#ff6666"
                    #    text_hover_color "#ff0000"

                # 2.3.2 vbox: vbox из чужих товаров на покупку, кнопка подтвердить сделку
                vbox:
                    spacing 5
                    xsize 185

                    frame:
                        background "#ffffff"
                        padding (10, 10)
                        xysize (250, 40)
                        frame:
                            background "#000000"
                            xysize (240, 30)
                            xalign 0.5 yalign 0.5
                            text "{font=determination.otf}{size=25}На покупку{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5

                    frame:
                        ypos -10
                        background "#ffffff"
                        padding (10, 10)
                        xysize (250, 530)
                        frame:
                            background "#000000"
                            padding (10, 10)
                            xysize (240, 520)
                            xalign 0.5 yalign 0.5

                            # Вычисляем количество товаров на покупку
                            $ merchant_selling_count = len(store.merchant_selling) + len(store.merchant_selling_consumables)
                            $ merchant_selling_needs_scroll = merchant_selling_count >= 8

                            viewport:
                                ypos -10
                                id "merchant_selling_viewport"
                                xysize (240, 520)
                                if merchant_selling_needs_scroll:
                                    scrollbars "vertical"
                                draggable True
                                mousewheel True
                                vbox:

                                    spacing 15
                                    # Сначала артефакты
                                    if store.merchant_selling:
                                        for merch_idx in store.merchant_selling:
                                            if merch_idx < len(store.merchant_inventory):
                                                $ item = store.merchant_inventory[merch_idx]
                                                $ base_price = item["price"]
                                                $ item_id = item["id"]

                                                # Пропускаем "мусорные" артефакты (на всякий случай)
                                                if item_id == "trash":
                                                    continue
                                                $ price = store.get_merchant_sell_price(base_price)

                                                frame:
                                                    xoffset -10
                                                    background "#000000"
                                                    padding (5, 5)
                                                    xysize (240, 60)
                                                    $ hovered_actions = [SetVariable("xoffset_for_art_desc", "left"), SetVariable("hovered_artifact_id", item_id)]
                                                    $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                    if pokaz_desc > 0:
                                                        $ hovered_actions.append(Show("art_desc"))
                                                        $ unhovered_actions.append(Hide("art_desc"))
                                                    $ button_action = [RemoveFromMerchantSellingAction(merch_idx)]
                                                    if pokaz_desc > 0:
                                                        $ button_action.append(Hide("art_desc"))
                                                    button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                        hbox:
                                                            xsize 180 xalign 0.0 yalign 0.5
                                                            add f"{store.artifact_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                            hbox:
                                                                yalign 0.5
                                                                text "{font=determination.otf}{size=18}[store.artifact_names.get(item['id'], item['id'])]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                        hbox:
                                                            xoffset 90
                                                            #yoffset -5
                                                            xalign 0.5 yalign 0.5

                                                            text "{font=determination.otf}[int(price)]" size 18 color "#ffff00" #ypos 5

                                    # Затем consumables
                                    if store.merchant_selling_consumables:
                                        for item_id in dict.fromkeys(store.merchant_selling_consumables):
                                            $ stack_count = store.merchant_selling_consumables.count(item_id)
                                            $ base_price = store.consumable_prices.get(item_id, 0)
                                            $ price = store.get_merchant_sell_price(base_price) * stack_count

                                            frame:
                                                    xoffset -10
                                                    background "#000000"
                                                    padding (5, 5)
                                                    xysize (240, 60)
                                                    $ hovered_actions = [SetVariable("xoffset_for_art_desc", "left"), SetVariable("hovered_artifact_id", item_id)]
                                                    $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                    if pokaz_desc > 0:
                                                        $ hovered_actions.append(Show("art_desc"))
                                                        $ unhovered_actions.append(Hide("art_desc"))
                                                    $ button_action = [RemoveFromMerchantSellingConsumablesAction(item_id)]
                                                    if pokaz_desc > 0:
                                                        $ button_action.append(Hide("art_desc"))
                                                    button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                        hbox:
                                                            xsize 180 xalign 0.0 yalign 0.5
                                                            add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                            hbox:
                                                                yalign 0.5
                                                                #add "images/Nullhead.png" size (50, 50) xalign 0.0 yalign 0.5

                                                                if stack_count == 1:
                                                                    text "{font=determination.otf}{size=18}[store.consumable_names.get(item_id, item_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                                else:
                                                                    text "{font=determination.otf}{size=18}[store.consumable_names.get(item_id, item_id)](х[stack_count]){/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5

                                                        hbox:
                                                            xoffset 90
                                                            yoffset -5
                                                            xalign 0.5 yalign 0.5
            
                                                            #add "images/Nullhead.png" size (50, 50) xalign 0.0 yalign 0.5
                                                            text "{font=determination.otf}[int(price)]" size 18 color "#ffff00" #ypos 5

                                    # Если оба списка пусты
                                    if not store.merchant_selling and not store.merchant_selling_consumables:
                                        vbox:
                                            xalign 0.5
                                            text "{font=determination.otf}{size=20}---" color "#ffffff" xpos 100
            hbox:
                spacing 7 yoffset -5
                imagebutton:
                    idle "quittrade.png"
                    hover "quittrade2.png"
                    hovered SetVariable("quittrade_zh", 1)
                    unhovered SetVariable("quittrade_zh", 0)
                    action Hide("shop_screen")

                imagebutton:
                    idle "deny.png"
                    hover "deny2.png"
                    hovered SetVariable("deny_zh", 1)
                    unhovered SetVariable("deny_zh", 0)
                    action ClearTradeListsAction()

                imagebutton:
                    idle "accept.png"
                    hover "accept2.png"
                    hovered SetVariable("accept_zh", 1)
                    unhovered SetVariable("accept_zh", 0)
                    action ConfirmTradeAction()

            hbox:
                yoffset -60 xoffset 10
                if quittrade_zh == 0:
                    text "Выйти" xoffset 10
                else:
                    text "Выйти" color "ffff00" xoffset 10 yoffset 4

                if deny_zh == 0:
                    text "Отмена" xoffset 80
                else:
                    text "Отмена" color "ff0000" xoffset 80 yoffset 4

                if accept_zh == 0:
                    text "ОК" xoffset 190
                else:
                    text "ОК" color "00ff00" xoffset 190 yoffset 4


            #textbutton "Подтвердить сделку" action ConfirmTradeAction():
            #    xsize 185
            #    text_size 14
            #    text_color "#66ff66"
            #    text_hover_color "#00ff00"



        # 3 vbox
        vbox:
            xpos 40
            ypos -15
            spacing 10
            xsize 380

            # 3.2 vbox товаров инвентаря торговца
            frame:
                yoffset 75
                background "#ffffff"
                padding (10, 10)
                xysize (355, 50)
                frame:
                    background "#000000"
                    xysize (345, 40)
                    xalign 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        if store.merchant_shop_tab == "artifacts":
                            text "{font=determination.otf}{size=35}Предметы{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5
                        elif store.merchant_shop_tab == "consumables":
                            text "{font=determination.otf}{size=35}Расходники{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5
                        elif store.merchant_shop_tab == "weapons":
                            text "{font=determination.otf}{size=35}Оружие{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5
                        else:
                            text "{font=determination.otf}{size=35}Расходники{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5

            # 3.3 кнопки переключения артефактов и расходников
            hbox:
                yoffset -55 xoffset 15
                spacing 10
                if store.merchant_shop_tab == "artifacts":
                    imagebutton:
                        idle "art_bel_chosen.png"
                        hover "art_bel_chosen.png"
                        action None
                    imagebutton:
                        idle "con_bel.png"
                        hover "con_zh.png"
                        action SetMerchantShopTabAction("consumables")
                    imagebutton:
                        idle "weap_bel.png"
                        hover "weap_zh.png"
                        action SetMerchantShopTabAction("weapons")
                elif store.merchant_shop_tab == "consumables":
                    imagebutton:
                        idle "art_bel.png"
                        hover "art_zh.png"
                        action SetMerchantShopTabAction("artifacts")
                    imagebutton:
                        idle "con_bel_chosen.png"
                        hover "con_bel_chosen.png"
                        action None
                    imagebutton:
                        idle "weap_bel.png"
                        hover "weap_zh.png"
                        action SetMerchantShopTabAction("weapons")
                else:
                    imagebutton:
                        idle "art_bel.png"
                        hover "art_zh.png"
                        action SetMerchantShopTabAction("artifacts")
                    imagebutton:
                        idle "con_bel.png"
                        hover "con_zh.png"
                        action SetMerchantShopTabAction("consumables")
                    imagebutton:
                        idle "weap_bel_chosen.png"
                        hover "weap_bel_chosen.png"
                        action None


            frame:
                ypos -15
                yoffset -15
                background "#ffffff"
                padding (10, 10)
                xysize (355, 520)
                frame:
                    background "#000000"
                    padding (10, 10)
                    xysize (345, 510)
                    xalign 0.5 yalign 0.5

                    # Вычисляем количество предметов для текущей вкладки торговца
                    $ merchant_artifact_count = 0
                    $ merchant_consumable_count = 0
                    $ merchant_weapon_count = 0
                    if store.merchant_inventory:
                        for merch_idx, item in enumerate(store.merchant_inventory):
                            if merch_idx not in store.merchant_selling:
                                $ item_id = item["id"]
                                if item_id != "trash":
                                    $ merchant_artifact_count += 1
                    if store.merchant_consumables_inventory:
                        for stack in store.get_merchant_consumables_stacks():
                            $ item_id = stack["id"]
                            $ available_count = max(0, stack["count"] - store.merchant_selling_consumables.count(item_id))
                            if available_count > 0:
                                if item_id.startswith("wep_"):
                                    $ merchant_weapon_count += 1
                                else:
                                    $ merchant_consumable_count += 1
                    $ merchant_artifacts_need_scroll = merchant_artifact_count > 6
                    $ merchant_consumables_need_scroll = merchant_consumable_count > 6
                    $ merchant_weapons_need_scroll = merchant_weapon_count > 6
                    if store.merchant_shop_tab == "artifacts":
                        $ merchant_needs_scroll = merchant_artifacts_need_scroll
                    elif store.merchant_shop_tab == "consumables":
                        $ merchant_needs_scroll = merchant_consumables_need_scroll
                    else:
                        $ merchant_needs_scroll = merchant_weapons_need_scroll

                    viewport:
                        xalign 0.0 yalign 0.5
                        xysize (345, 510)
                        if merchant_needs_scroll:
                            scrollbars "vertical"
                        #draggable True
                        mousewheel True
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        vbox:
                            yoffset 0
                            xoffset -10
                            yalign 0.5
                            spacing 5
                            # Содержимое вкладки артефактов
                            if store.merchant_shop_tab == "artifacts":
                                if store.merchant_inventory:
                                    for merch_idx, item in enumerate(store.merchant_inventory):
                                        if merch_idx not in store.merchant_selling:
                                            $ base_price = item["price"]
                                            $ item_id = item["id"]

                                            # Пропускаем "мусорные" артефакты (на всякий случай)
                                            if item_id == "trash":
                                                continue

                                            $ price = store.get_merchant_sell_price(base_price)

                                            frame:
                                                xoffset -10
                                                yoffset -10
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "left"), SetVariable("hovered_artifact_id", item_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToMerchantSellingAction(merch_idx)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 220 ysize 65 xalign 0.0
                                                        add f"{store.artifact_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            yalign 0.5 
                                                            text "{font=determination.otf}{size=24}[store.artifact_names.get(item['id'], item['id'])]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5 xoffset 10
                                                    vbox:
                                                        xoffset 140
                                                        yoffset 5
                                                        xalign 0.5 yalign 0.5
                                                        null width 10
                                                        text "{font=determination.otf}[int(price)]" size 20 color "#ffff00" xalign 1.0 ypos 5
                                else:
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xpos 140

                            # Содержимое вкладки оружия
                            elif store.merchant_shop_tab == "weapons":
                                if store.merchant_consumables_inventory:
                                    for stack in store.get_merchant_consumables_stacks():
                                        $ item_id = stack["id"]
                                        $ available_count = max(0, stack["count"] - store.merchant_selling_consumables.count(item_id))
                                        if available_count > 0 and item_id.startswith("wep_"):
                                            $ base_price = stack["price"]
                                            $ price = store.get_merchant_sell_price(base_price)

                                            frame:
                                                yoffset -10
                                                xoffset -10
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "left"), SetVariable("hovered_artifact_id", item_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToMerchantSellingConsumablesAction(item_id)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 290 ysize 65 xalign 0.0
                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            yalign 0.5
                                                            if available_count == 1:
                                                                text "{font=determination.otf}{size=24}[store.consumable_names.get(item_id, item_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                            else:
                                                                text "{font=determination.otf}{size=24}[store.consumable_names.get(item_id, item_id)](х [int(available_count)]){/font}{/size}" color "#ffffff" yalign 0.5 xalign 0

                                                vbox:
                                                    xoffset 140
                                                    yoffset 5
                                                    xalign 0.5 yalign 0.5
                                                    null width 10
                                                    text "{font=determination.otf}[int(price)]" size 20 color "#ffff00" xalign 1.0 ypos 5
                                else:
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xpos 140
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            # Содержимое вкладки consumables
                            else:
                                if store.merchant_consumables_inventory:
                                    for stack in store.get_merchant_consumables_stacks():
                                        $ item_id = stack["id"]
                                        $ available_count = max(0, stack["count"] - store.merchant_selling_consumables.count(item_id))
                                        if available_count > 0 and not item_id.startswith("wep_"):
                                            $ base_price = stack["price"]
                                            $ price = store.get_merchant_sell_price(base_price)

                                            frame:
                                                yoffset -10
                                                xoffset -10
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ hovered_actions = [SetVariable("xoffset_for_art_desc", "left"), SetVariable("hovered_artifact_id", item_id)]
                                                $ unhovered_actions = [SetVariable("xoffset_for_art_desc", False), SetVariable("hovered_artifact_id", None)]
                                                if pokaz_desc > 0:
                                                    $ hovered_actions.append(Show("art_desc"))
                                                    $ unhovered_actions.append(Hide("art_desc"))
                                                $ button_action = [AddToMerchantSellingConsumablesAction(item_id)]
                                                if pokaz_desc > 0:
                                                    $ button_action.append(Hide("art_desc"))
                                                button action button_action hovered hovered_actions unhovered unhovered_actions:
                                                    hbox:
                                                        xsize 290 ysize 65 xalign 0.0
                                                        add f"{store.consumable_names.get(item_id, item_id)}.png" xysize (50, 50) xalign 0.0 yalign 0.5
                                                        hbox:
                                                            yalign 0.5
                                                            if available_count == 1:
                                                                text "{font=determination.otf}{size=24}[store.consumable_names.get(item_id, item_id)]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5
                                                            else:
                                                                text "{font=determination.otf}{size=24}[store.consumable_names.get(item_id, item_id)](х [int(available_count)]){/font}{/size}" color "#ffffff" yalign 0.5 xalign 0

                                                vbox:
                                                    xoffset 140
                                                    yoffset 5
                                                    xalign 0.5 yalign 0.5
                                                    null width 10
                                                    text "{font=determination.otf}[int(price)]" size 20 color "#ffff00" xalign 1.0 ypos 5
                                else:
                                    vbox:
                                        xalign 0.5
                                        text "{font=determination.otf}{size=30}---" color "#ffffff" xpos 140

            # 3.4 Отношение торговца
            frame:
                ypos -30
                background "#ffffff"
                padding (10, 10)
                xysize (355, 50)
                frame:
                    background "#000000"
                    xysize (345, 40)
                    xalign 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        $ relation = store.get_total_relation()
                        if relation > 0:
                            text "{font=determination.otf}{size=30}Отношение: +[int(relation)]%{/font}{/size}" color "#66ff66" xalign 0.5 ypos -5
                        elif relation < 0:
                            text "{font=determination.otf}{size=30}Отношение: [int(relation)]%{/font}{/size}" color "#ff6666" xalign 0.5 ypos -5
                        else:
                            text "{font=determination.otf}{size=30}Отношение: 0%{/font}{/size}" color "#ffffff" xalign 0.5 ypos -5

    # 3.1 кнопка закрыть
    textbutton "Закрыть" action [Hide("shop_screen"), Show("artifacts_menu")]:
        xpos 300 ypos 700
        xsize 380
        text_size 18
        text_color "#ffffff"
        text_hover_color "#ff6666"




    # 2.1 hbox с кнопками переключения торговцев
    hbox:
        xpos 400 ypos 700
        spacing 10
        for merch_id, merch_data in store.merchants_data.items():
            if merch_id == store.current_merchant_id:
                textbutton "[merch_data['name']]" action None:
                    text_color "#66ff66"
                    text_hover_color "#66ff66"
            else:
                textbutton "[merch_data['name']]" action SetMerchantAction(merch_id)


    

    
    fixed:
        xpos 20 ypos 85 xoffset -470
        if store.player_shop_tab == "artifacts":
            text "{font=determination.otf}{size=35}Предметы" size 24 xalign 0.5 ypos -5
        elif store.player_shop_tab == "weapons":
            text "{font=determination.otf}{size=35}Оружие" size 24 xalign 0.5 ypos -5
        else:
            text "{font=determination.otf}{size=35}Расходники" size 24 xalign 0.5 ypos -5


    vbox:
        xpos 20 ypos 90
        if pokaz_desc == 0:
            imagebutton:
                idle "hide_fast_desc.png"
                hover "hide_fast_desc.png" at glowing
                action SetVariable("pokaz_desc", 1)
        elif pokaz_desc == 1:
            imagebutton:
                idle "show_fast_desc.png"
                hover "show_fast_desc.png" at glowing
                action SetVariable("pokaz_desc", 2)
        else:
            imagebutton:
                idle "show_full_desc.png"
                hover "show_full_desc.png" at glowing
                action SetVariable("pokaz_desc", 0)



    text "[merchant_name]" size 18 color "#000000" xpos 1000 ypos 700




















# ------------------------------------------------------------
# 7) ЭКРАН ОПОЗНАНИЯ АРТЕФАКТОВ
# ------------------------------------------------------------

# Трансформации для позиционирования иконки прогресса опознания
transform bar_in_progress:
    # Начальные параметры
    xpos 873 ypos 411 xsize 0 ysize 52 alpha 0.0
    # Первый параллельный процесс: ширина меняется 1.5 секунды
    parallel:
        linear 1.5 xsize 385
    # Второй параллельный процесс: прозрачность меняется 1.0 секунду
    parallel:
        linear 1.3 alpha 1.0



transform bar_success:
    # Позиция для состояния "success"
    xpos 873 ypos 411 xsize 372 ysize 52 alpha 0.0
    linear 0.01 alpha 1.0
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

transform bar_fail:
    # Позиция для состояния "fail"
    xpos 873 ypos 411 xsize 372 ysize 52 alpha 0.0
    linear 0.01 alpha 1.0
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

# Трансформации для анимации прогресса стирки
transform wash_bar_in_progress:
    # Начальные параметры
    xpos 873 ypos 411 xsize 0 ysize 52 alpha 0.0
    parallel:
        linear 5.0 xsize 372
    parallel:
        linear 0.5 alpha 1.0

transform wash_bar_success:
    # Позиция для состояния "success"
    xpos 873 ypos 411 xsize 372 ysize 52 alpha 0.0
    linear 0.01 alpha 1.0
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

transform wash_bar_fail:
    # Позиция для состояния "fail"
    xpos 873 ypos 411 xsize 372 ysize 52 alpha 0.0
    linear 0.01 alpha 1.0
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
















































#  ▄████████    ▄█    █▄       ▄████████  ▄████████    ▄█   ▄█▄
# ███    ███   ███    ███     ███    ███ ███    ███   ███ ▄███▀
# ███    █▀    ███    ███     ███    █▀  ███    █▀    ███▐██▀
# ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███         ▄█████▀
# ███        ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███        ▀▀█████▄
# ███    █▄    ███    ███     ███    █▄  ███    █▄    ███▐██▄
# ███    ███   ███    ███     ███    ███ ███    ███   ███ ▀███▄
# ████████▀    ███    █▀      ██████████ ████████▀    ███   ▀█▀
#                                                     ▀


label identify_screen_to_trader:
    hide screen identify_screen
    hide screen trader_screen_background
    hide screen trader_screen_options
    call screen trader_screen

screen identify_screen():

    key "K_ESCAPE" action Jump("identify_screen_to_trader")
    key "K_TAB" action None

    tag menu
    modal True

    # Часть 2: слот для артефакта
    # Показываем иконку выбранного артефакта, если слот для опознания не пустой
    if store.identify_slot is not None:
        $ identify_artifact_id = store.artifact_instances[store.identify_slot]["id"]
        $ identify_artifact_name = store.artifact_names.get(identify_artifact_id, identify_artifact_id)
        add f"{identify_artifact_name}.png" xysize (120, 120) xpos 590 ypos 300

    # Кнопка закрытия
    vbox:
        spacing 10
        xsize 100
        textbutton "Закрыть" action Return():
            xpos 1200
            text_size 16
            text_color "#ffffff"
            text_hover_color "#ff6666"

    #frame:
    #    xalign 0.5
    #    yalign 0.5
    #    padding (20, 20)
    #    xysize (1200, 650)

        hbox:
            spacing 20

            # Левый vbox: список артефактов для опознания
            vbox:
                xpos 10
                spacing 10
                xsize 400

                frame:
                    background "#ffffff"
                    #padding (10, 10)
                    xysize (380, 50)

                    frame:
                        background "#000000"
                        #padding (10, 10)
                        xysize (370, 40)
                        xalign 0.5 yalign 0.5
                        hbox:
                            xalign 0.5

                            text "{font=determination.otf}{size=40}Инвентарь" color "#ffffff" xalign 0.5 ypos -7
                            if pokaz_desc == 0:
                                imagebutton:
                                    xsize 50
                                    xalign 1.0
                                    idle "hide_fast_desc.png"
                                    hover "hide_fast_desc.png" at glowing
                                    action SetVariable("pokaz_desc", 1)
                            elif pokaz_desc == 1:
                                imagebutton:
                                    xsize 50
                                    xalign 1.0
                                    idle "show_fast_desc.png"
                                    hover "show_fast_desc.png" at glowing
                                    action SetVariable("pokaz_desc", 2)
                            else:
                                imagebutton:
                                    xsize 50
                                    xalign 1.0
                                    idle "show_full_desc.png"
                                    hover "show_full_desc.png" at glowing
                                    action SetVariable("pokaz_desc", 0)

                frame:
                    background "#ffffff"
                    padding (10, 10)
                    xysize (380, 550)

                    frame:
                        background "#000000"
                        padding (10, 10)
                        xysize (370, 540)
                        xalign 0.5 yalign 0.5

                        # Вычисляем количество артефактов для опознания
                        $ identify_count = 0
                        if store.artifact_instances:
                            for inst_idx, inst in enumerate(store.artifact_instances):
                                $ artifact_id = inst["id"]
                                $ can_identify = store.artifact_identifiable.get(artifact_id, 0) == 1
                                $ is_identified = store.artifact_identified_state.get(inst_idx, 0) == 1
                                if can_identify and not is_identified:
                                    $ identify_count += 1

                        # Используем viewport с прокруткой только если больше 10 артефактов
                        viewport:
                            xysize (360, 530)
                            if identify_count >= 7:
                                scrollbars "vertical"
                                mousewheel True

                            vbox:
                                spacing 0

                                # Показываем только артефакты, которые можно опознать и ещё не опознаны
                                if store.artifact_instances:
                                    $ has_artifacts = False
                                    for inst_idx, inst in enumerate(store.artifact_instances):
                                        $ artifact_id = inst["id"]

                                        # Пропускаем "мусорные" артефакты
                                        if artifact_id == "trash":
                                            continue

                                        # Пропускаем артефакты в стиральной машинке (in washing machine = 1)
                                        $ in_wash_slot = store.is_artifact_in_wash_slot(inst_idx)
                                        if in_wash_slot:
                                            continue

                                        # Постиранные артефакты (get_washed = 2) видны в экране опознания

                                        $ can_identify = store.artifact_identifiable.get(artifact_id, 0) == 1
                                        $ is_identified = store.artifact_identified_state.get(inst_idx, 0) == 1
                                        $ owner = inst.get("owner")

                                        if can_identify and not is_identified:
                                            $ has_artifacts = True
                                            frame:
                                                xoffset -10
                                                background "#000000"
                                                padding (5, 5)
                                                xysize (340, 90)
                                                $ desc_screen = "art_desc_check" if pokaz_desc > 0 else None
                                                button action [PlaceArtifactToIdentifySlotAction(inst_idx), Hide("art_desc_check")] hovered [SetVariable("hovered_artifact_id", artifact_id), Show(desc_screen) if desc_screen else None] unhovered [SetVariable("hovered_artifact_id", None), Hide(desc_screen) if desc_screen else None] at inventory_artifact_trans:
                                                    hbox:
                                                        spacing 10
                                                        if owner:
                                                            $ owner_data = store.pers_dict[owner]
                                                            add "images/[owner_data.nameeng]head.png" size (50, 50) xalign 0.0 ypos -10
                                                        else:
                                                            add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) xalign 0.0 ypos -10
                                                        text "{font=determination.otf}{size=24}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ffffff" xoffset 10 yoffset -5 xalign 0.5 text_align 0.5

                                    if not has_artifacts:
                                        text "{font=determination.otf}{size=30}---" size 14 color "#ffffff" xpos 140
                                else:
                                    text "{font=determination.otf}{size=30}---" size 14 color "#ffffff" xpos 140






            # Правый vbox: слот опознания и информация
            vbox:
                xpos 450
                ypos 150
                spacing 10
                xsize 400



                #text "Слот опознания" size 20 color "#ffffff"

                # Часть 1: текст с эффектами при опознании
                frame:
                    background "#ffffff"
                    padding (10, 10)
                    xysize (380, 120)
                    frame:
                        background "#000000"
                        padding (10, 10)
                        xysize (370, 110)
                        xalign 0.5
                        yalign 0.5

                        if store.identify_slot is not None:
                            $ inst_idx = store.identify_slot
                            $ inst = store.artifact_instances[inst_idx]
                            $ artifact_id = inst["id"]
                            $ is_identified = store.artifact_identified_state.get(inst_idx, 0) == 1

                            if is_identified:
                                $ bonuses = store.artifact_identified_bonuses.get(artifact_id, {})
                                $ bonus_modifiers = bonuses.get("modifiers", [])
                                $ bonus_values = bonuses.get("values", [])

                                vbox:
                                    xalign 0.5
                                    yalign 0.5
                                    spacing -5
                                    #text "Эффекты при опознании:" size 14 color "#ffffff"

                                    if bonus_modifiers:
                                        for i, mod_type in enumerate(bonus_modifiers):
                                            if i < len(bonus_values):
                                                $ value = bonus_values[i]
                                                # Форматируем значение в зависимости от типа модификатора
                                                if "critdmg" in mod_type:
                                                    $ value_str = f"+{value}x"
                                                elif "critrate" in mod_type or "dmgchance" in mod_type or "accuracy" in mod_type:
                                                    $ value_str = f"+{value}%"
                                                else:
                                                    $ value_str = f"+{value}"

                                                # Переводим тип модификатора в читаемый формат
                                                $ mod_names = {
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
                                                    "socializationartifactmod": "Социализация",
                                                    "diplomacyartifactmod": "Дипломатия",
                                                    "charmartifactmod": "Очарование",
                                                    "perceptionartifactmod": "Восприятие",
                                                    "rhetoricartifactmod": "Риторика",
                                                    "artistryartifactmod": "Артистизм",
                                                    "comfortartifactmod": "Комфорт",
                                                    "powerartifactmod": "Власть"
                                                }
                                                $ mod_name = mod_names.get(mod_type, mod_type)

                                                hbox:
                                                    yalign 0.5 xalign 0.5
                                                    spacing 10
                                                    vbox:
                                                        yalign 0.5 xalign 0.5
                                                        text "{font=determination.otf}{size=30}[mod_name]:{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5 text_align 0.5
                                                    vbox:
                                                        yalign 0.5 xalign 0.5
                                                        text "{font=determination.otf}{size=30}[value_str]{/font}{/size}" color "#ffffff" yalign 0.5 xalign 0.5 text_align 0.5


                                    else:
                                        text "Нет дополнительных эффектов" size 12 color "#888888"
                            else:
                                text "{font=determination.otf}{size=40}???{/font}{/size}" xalign 0.5 yalign 0.5 color "#ffffff"
                        else:
                            text "{font=determination.otf}{size=40}???{/font}{/size}" xalign 0.5 yalign 0.5 color "#ffffff"


                # Часть 2: слот для артефакта
                frame:
                    background "#ffffff"
                    padding (10, 10)
                    xysize (380, 80)

                    frame:
                        xalign 0.5
                        yalign 0.5
                        background "#000000"
                        padding (10, 10)
                        xysize (370, 70)

                        if store.identify_slot is not None:
                            $ inst_idx = store.identify_slot
                            $ inst = store.artifact_instances[inst_idx]
                            $ artifact_id = inst["id"]

                            vbox:
                                xalign 0.5
                                yalign 0.5
                                #ypos 10
                                spacing 5
                                #text "Выбранный артефакт:" size 14 color "#ffffff"
                                #text "{font=determination.otf}{size=29}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ccccff" ypos -9

                                $ desc_screen = "art_desc_check" if pokaz_desc > 0 else None
                                button action [ClearIdentifySlotAction(), Hide("art_desc_check")] hovered [SetVariable("hovered_artifact_id", artifact_id), Show(desc_screen) if desc_screen else None] unhovered [SetVariable("hovered_artifact_id", None), Hide(desc_screen) if desc_screen else None]:
                                    hbox:
                                        yalign 0.5
                                        spacing 10
                                        #add f"{store.artifact_names.get(artifact_id, artifact_id)}.png" xysize (50, 50) yalign 0.5
                                        text "{font=determination.otf}{size=24}[store.artifact_names.get(artifact_id, artifact_id)]{/font}{/size}" color "#ffffff" yalign 0.5 text_align 0.5
                        else:
                            text "{font=determination.otf}{size=39}---" size 14 color "#ffffff" xalign 0.5 yalign 0.5





                # Часть 3: кнопка опознать с индикатором прогресса
                frame:
                    background "#ffffff"
                    padding (10, 10)
                    xysize (380, 60)

                    frame:
                        background "#000000"
                        padding (10, 10)
                        xysize (370, 50)
                        xalign 0.5
                        yalign 0.5

                        if store.identify_slot is not None:
                            $ inst_idx = store.identify_slot
                            $ inst = store.artifact_instances[inst_idx]
                            $ artifact_id = inst["id"]

                            hbox:
                                xalign 0.5
                                yalign 0.5
                                spacing 10
                                # Проверяем, опознан ли артефакт
                                $ is_identified = store.artifact_identified_state.get(inst_idx, 0) == 1
                                # Кнопка опознать
                                $ cost = store.artifact_identify_cost.get(artifact_id, 0)

                                if store.money < cost:
                                    text "{font=determination.otf}{size=30}НЕДОСТАТОЧНО ДЕНЕГ" color "#c61e1e" xalign 0.5 yalign 0.5


                                elif not is_identified:
                                    textbutton "{font=determination.otf}{size=30}ОПОЗНАТЬ" action Show("check_initiated"):
                                        text_size 18
                                        text_color "#ffffff"
                                        text_hover_color "#ffff00"
                                        xalign 0.5 
                                        yalign 0.5
                                else:
                                    textbutton "{font=determination.otf}{size=30}АРТЕФАКТ ОПОЗНАН" action None:
                                        text_size 18
                                        text_color "#22ff00"
                                        text_hover_color "#54e43d"
                                        #xpos 50
                                        #ypos -5
                                        xalign 0.5 yalign 0.5



                                # Индикатор прогресса
                                #if store.is_checking == "is_checking":
                                #   add "check_progress.png" at bar_in_progress
                                #elif store.is_checking == "success":
                                #    add "check_progress.png" at bar_success
                                #elif store.is_checking == "fail":
                                #    add "check_progress.png" at bar_fail
                        else:
                            textbutton "{font=determination.otf}{size=30}ОПОЗНАТЬ" action None:
                                text_size 18
                                text_color "#666666"
                                text_hover_color "#ff0000"
                                xalign 0.5 
                                yalign 0.5





                # Часть 4: hbox со стоимостью и шансом
                frame:
                    background "#ffffff"
                    padding (10, 10)
                    xysize (380, 80)

                    frame:
                        background "#000000"
                        padding (10, 10)
                        xysize (370, 70)
                        xalign 0.5
                        yalign 0.5

                        if store.identify_slot is not None:
                            $ inst_idx = store.identify_slot
                            $ inst = store.artifact_instances[inst_idx]
                            $ artifact_id = inst["id"]
                            $ cost = store.artifact_identify_cost.get(artifact_id, 0)
                            $ chance = store.artifact_identify_chance.get(artifact_id, 0)

                            hbox:
                                spacing 20
                                vbox:
                                    text "{font=determination.otf}{size=25}Имеется:" size 14 color "#ffffff"
                                    if store.money < cost:
                                        text "{font=determination.otf}{size=25}[store.money]К" size 16 color "#ff0000"
                                    else:
                                        text "{font=determination.otf}{size=25}[store.money]К" size 16 color "#ffff00"
                                vbox:
                                    text "{font=determination.otf}{size=25}Стоимость:" size 14 color "#ffffff"
                                    text "{font=determination.otf}{size=25}[cost]К" size 16 color "#ffffff"
                                vbox:
                                    text "{font=determination.otf}{size=25}Шанс:" size 14 color "#ffffff"
                                    text "{font=determination.otf}{size=25}[chance]%" size 16 color "#ffffff"
                        else:
                            hbox:
                                spacing 20
                                vbox:
                                    text "{font=determination.otf}{size=25}Имеется:" size 14 color "#ffffff"
                                    text "{font=determination.otf}{size=25}[store.money]К" size 16 color "#ffff00"
                                vbox:
                                    text "{font=determination.otf}{size=25}Стоимость:" size 14 color "#ffffff"
                                    text "{font=determination.otf}{size=25}---" size 16 color "#ffffff" xalign 0.5
                                vbox:
                                    text "{font=determination.otf}{size=25}Шанс:" size 14 color "#ffffff"
                                    text "{font=determination.otf}{size=25}---" size 16 color "#ffffff" xalign 0.5




transform pop_up_art_screen:
    subpixel True
    alpha 0.0 xoffset -20
    easein 0.25 alpha 1.0 xoffset 0
    linear 1.5 xoffset 5
    easeout 0.25 xoffset 25 alpha 0

# ============================================================
# ЭКРАН ХАРАКТЕРИСТИК СЕТА АРТЕФАКТОВ
# ============================================================
screen set_stats_popup():
    zorder 100

    # Автоматически скрываем через 5 секунд
    timer 2 action Hide("set_stats_popup")

    if store.set_stats_popup is not None:
        $ spop = store.set_stats_popup
        $ s_bonuses = spop["bonuses"]
        $ s_mode = spop["mode"]
        $ s_name = spop["set_name"]
        $ s_count = spop.get("set_count", 1)
        $ col_header = "#ffcc00" if s_mode == "equip" else "#ff6666"

        # Копируем расположение и размеры vbox характеристик персонажа
        vbox:
            at pop_up_art_screen
            xpos 720 ypos 90 spacing 5

            frame:
                background None#"#ffffff"
                padding (10, 10)
                xsize (450 + 10 * s_count) ysize (550 + 20 * s_count)

                frame:
                    background None#"#000000"
                    padding (10, 10)
                    xsize (440 + 10 * s_count) ysize (540 + 20 * s_count)
                    xalign 0.5 yalign 0.5

                    vbox:
                        #ypos 20

                        $ set_labels = store.get_active_set_stats_labels()
                        frame:
                            background None#"#ffffff"
                            padding (5, 5)
                            #xsize 410 ysize 50

                            frame:
                                background None#"#000000"
                                padding (10, 10)
                                xsize 370 ysize 40
                                #xalign 0.5 yalign 0.5
                                #text "{font=determination.otf}{color=[col_header]}[s_name]{/color}{/font}" size 30 xalign 0.5 yalign 0.5
                        #text "{font=determination.otf}Характеристики сета" size 26 xalign 0.5 color "#ffffff"

                        null height 20

                        hbox:
                            spacing 20
                            xalign 0.5
                            xoffset 20

                            vbox:
                                spacing 15
                                for lbl_mod, lbl_name, lbl_is_pct in set_labels:
                                    if lbl_mod == "perceptionartifactmod":
                                        null height 30
                                    text "{font=determination.otf}[lbl_name]:{/font}" size size_for_invent color "#ffffff" at alpha_000

                            vbox:
                                spacing 15
                                for lbl_mod, lbl_name, lbl_is_pct in set_labels:
                                    if lbl_mod == "perceptionartifactmod":
                                        null height 30
                                    $ raw_val = s_bonuses.get(lbl_mod, 0)
                                    $ disp_val = int(raw_val * 100) if lbl_is_pct else int(raw_val)
                                    if disp_val == 0:
                                        $ s_color = "#000000"
                                        $ s_text = ""
                                    elif s_mode == "equip":
                                        $ s_sign = "+" if disp_val > 0 else "-"
                                        $ s_text = "{}{}".format(s_sign, abs(disp_val))
                                        $ s_color = "#ffcc00" if disp_val > 0 else "#ff6666"
                                    else:
                                        $ s_sign = "-" if disp_val > 0 else "+"
                                        $ s_text = "{}{}".format(s_sign, abs(disp_val))
                                        $ s_color = "#ff6666" if disp_val > 0 else "#ffcc00"
                                    text "{font=determination.otf}{color=[s_color]}[s_text]{/color}{/font}" size size_for_invent xalign 0.5
                        
                    frame:
                        xalign 0.5 xoffset -40*s_count
                        background "#ffffff"
                        padding (5, 5)
                        #xsize 410 ysize 50

                        frame:
                            background "#000000"
                            padding (10, 10)
                            #xsize 370 ysize 40
                            #xalign 0.5 yalign 0.5
                            text "{font=determination.otf}{color=[col_header]}[s_name]{/color}{/font}" size 30 xalign 0.5 yalign 0.5

# ============================================================
# ЭКРАН ЭНЦИКЛОПЕДИИ СЕТОВ АРТЕФАКТОВ
# Показывает сеты, которые игрок хотя бы раз собирал.
# Левая колонка — список кнопок сетов, средняя — состав и описание
# сета, правая — характеристики (боевые / социальные).
# ============================================================
screen sets_encyclopedia():
    modal True
    zorder 200
    key "K_ESCAPE" action Hide("sets_encyclopedia")

    add "#000000CC"

    imagebutton:
        xalign 1.0 yalign 0.01
        #at semiblack_dynamic_alpha
        idle "closestatdesc.png"
        hover "closestatdesc_hover.png"
        action Hide("sets_encyclopedia")

    $ _discovered = store.get_discovered_sets()
    $ _sel = store.sets_ency_selected_set



    hbox:
        xalign 0.5 yalign 0.5 spacing 10

        # ---- Левая колонка: список сетов ----
        vbox:
            spacing 8
            frame:
                background "#ffffff"
                xysize (320, 40)
                #padding (10, 10)
                
                frame:
                    xysize (310, 30)
                    xalign 0.5 yalign 0.5
                    background "#000000"

                    text "{font=determination.otf}{size=30}Сеты{/font}{/size}" color "#ffffff" xalign 0.5 yalign 0.5

            frame:
                background "#ffffff"
                xysize (320, 550)                  
                frame:
                    xysize (310, 540)
                    xalign 0.5 yalign 0.5
                    background "#000000"
                    vbox:
                        
                        spacing 6
                        if not _discovered:
                            xalign 0.5
                            text "---" size 18 color "#ffffff" yfill True xalign 0.5
                        else:
                            xalign 0.0
                            for _sid, _sdata in _discovered:
                                $ _sname = _sdata.get("name", _sid)
                                $ _is_sel = (_sid == _sel)
                                textbutton _sname:
                                    xysize (300, 34)
                                    text_size 25
                                    text_color ("#ffff00" if _is_sel else "#ffffff")
                                    text_hover_color "#ffff00"
                                    background ("#222222" if _is_sel else "#000000")
                                    action SetVariable("sets_ency_selected_set", _sid)




        # ---- Средняя колонка: состав и описание сета ----
        if _sel is not None and _sel in store.artifact_sets:
            $ _sdata = store.artifact_sets[_sel]
            $ _sname = _sdata.get("name", _sel)
            $ _sdesc = _sdata.get("description", "")
            $ _pieces = _sdata.get("pieces", [])

            frame:
                background "#ffffff"
                padding (10, 10)
                xysize (600, 597)

                frame:
                    xalign 0.5 yalign 0.5
                    background "#000000"
                    xysize (590, 587)

                    vbox:
                        xalign 0.5
                        spacing 12

                        text "{font=determination.otf}{size=34}[_sname]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5

                        # Ряд из частей сета
                        hbox:
                            xalign 0.5
                            spacing 10
                            for _aid in _pieces:
                                $ _aname = store.artifact_names.get(_aid, _aid)
                                frame:
                                    background "#ffffff"
                                    xysize (100, 100)
                                    button:
                                        xysize (100, 100)
                                        xalign 0.5 yalign 0.5
                                        action NullAction()
                                        hovered [SetVariable("sets_ency_hovered_set", _sel), SetVariable("sets_ency_hovered_art", _aid)]
                                        unhovered [SetVariable("sets_ency_hovered_set", None), SetVariable("sets_ency_hovered_art", None)]
                                        frame:
                                            xalign 0.5 yalign 0.5
                                            background "#000000"
                                            xysize (90, 90)
                                            add f"{_aname}.png" xysize (90, 90) xalign 0.5 yalign 0.5

                        # Поле описания сета
                        frame:
                            xalign 0.0 xoffset 280 yoffset -20
                            background None
                            xysize (580, 400)
                            text "[_sdesc]" size 25 justify True xfill True color "#ffffff" xalign 0.5 ypos 40 xpos 10

                       
        else:
            frame:
                background "#ffffff"
                padding (10, 10)
                xysize (600, 597)

                frame:
                    xalign 0.5 yalign 0.5
                    background "#000000"
                    xysize (590, 587)

                    text "{font=determination.otf}{size=30}Описание{/font}{/size}" color "#ffffff" xalign 0.5






        # ---- Правая колонка: характеристики ----

        if _sel is not None and _sel in store.artifact_sets:
            $ _battle, _social = store.get_set_stats_split(_sdata)

            frame:
                background "#ffffff"
                xysize (300, 597)
                frame:
                    background "#000000"
                    xalign 0.5 yalign 0.5
                    xysize (290, 587)

                    vbox:
                        xalign 0.5
                        spacing 20

                        text "{font=determination.otf}{size=35}Характеристики{/font}{/size}" color "#ffffff" xalign 0.5

                        #null height 6

                        if _battle:
                            text "{font=determination.otf}{size=30}Боевые{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                            for _sn, _sv in _battle:
                                hbox:
                                    xalign 0.5
                                    spacing 5
                                    text "{font=determination.otf}{size=25}[_sn]:{/font}{/size}" color "#ffffff"
                                    text "{font=determination.otf}{size=25}[_sv]{/font}{/size}" color "#ffffff"

                        #null height 10

                        if _social:
                            text "{font=determination.otf}{size=30}Социальные{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                            for _sn, _sv in _social:
                                hbox:
                                    xalign 0.5
                                    spacing 5
                                    text "{font=determination.otf}{size=25}[_sn]:{/font}{/size}" color "#ffffff"
                                    text "{font=determination.otf}{size=25}[_sv]{/font}{/size}" color "#ffffff"

                        if not _battle and not _social:
                            text "Нет характеристик" size 25 color "#888888"
        else:
            frame:
                background "#ffffff"
                xysize (300, 597)
                frame:
                    background "#000000"
                    xalign 0.5 yalign 0.5
                    xysize (290, 587)

                    text "{font=determination.otf}{size=30}Характеристики{/font}{/size}" color "#ffffff" xalign 0.5



    # Описание наведённого артефакта (формат art_desc)
    if store.sets_ency_hovered_art is not None:
        $ _hart = store.sets_ency_hovered_art
        $ _hart_name = store.artifact_names.get(_hart, _hart)
        $ _adesc = store.artifact_descriptions.get(_hart, {}).get("description", "")
        $ _battle, _social = get_artifact_description_stats(_hart, store.current_char)
        $ _trade_bonus = get_artifact_relation_display_bonus(_hart)

        # Состояния стирки и опознания (как в art_desc)
        $ _inst_idx = next((i for i, inst in enumerate(store.artifact_instances) if inst["id"] == _hart), None)
        $ _washed = store.artifact_wash_state.get(_inst_idx, 0) == 2
        $ _identified = store.artifact_identified_state.get(_inst_idx, 0) == 1

        vbox:
            xpos 365 yalign 0.1
            spacing 6
            frame:
                background "#000000"
                xysize (560, 40)

                text "{font=determination.otf}{size=32}[_hart_name]{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
















        if _adesc:
            frame:
                xpos 360 ypos 250
                background "#000000"
                xysize (580, 400)
                text "[_adesc]" size 25 justify True xfill True color "#ffffff" xalign 0.5


            frame:
                xpos 970 ypos 122
                background "#000000"
                xysize (280, 533)
                vbox:
                    xalign 0.5 
                    spacing 20               

                    if _battle:
                        text "{font=determination.otf}{size=30}Боевые{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                        for _sn, _sv, _sc in _battle:
                            hbox:
                                xalign 0.5
                                spacing 5
                                text "{font=determination.otf}{size=25}[_sn]:{/font}{/size}" color _sc
                                text "{font=determination.otf}{size=25}[_sv]{/font}{/size}" color _sc

                    if _social:
                        text "{font=determination.otf}{size=30}Социальные{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                        for _sn, _sv, _sc in _social:
                            hbox:
                                xalign 0.5
                                spacing 5
                                text "{font=determination.otf}{size=25}[_sn]:{/font}{/size}" color _sc
                                text "{font=determination.otf}{size=25}[_sv]{/font}{/size}" color _sc

                    if _trade_bonus != 0:
                        text "{font=determination.otf}{size=30}Бонус к торговле{/font}{/size}" color "#ffffff" xalign 0.5 text_align 0.5
                        hbox:
                            xalign 0.5
                            spacing 5
                            text "{font=determination.otf}{size=25}Торговля:{/font}{/size}" color "#ffffff"
                            text "{font=determination.otf}{size=25}+[_trade_bonus]%{/font}{/size}" color "#ffffff"
