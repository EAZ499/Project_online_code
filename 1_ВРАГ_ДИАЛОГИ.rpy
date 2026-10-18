


# Графика (Shift+G)
default preferences.gl_powersave = False   # Экономия энергии: Отключено
default preferences.gl_framerate = None      # 60 (или 30, или None = "Экранная")
default preferences.gl_tearing = False     # Разрывание кадров: Отключено

init python:
    if hasattr(preferences, "renderer"):
        preferences.renderer =  "gl2" #"angle2"   # "gl2", "gles2", либо None для авто

#                                                                1. из любого места jump в label Underrunefight:

#                                                                2. Из этого лебла вызывается call screen fightbegin

#                                                                          Это переход для начала боля, который включает экран слежения за здоровьем противника check_enemy_status, чтоб можно было следить за хп и пощадой                                                                                                

screen Move_mouse:
    timer 0.00001 action MouseMove(630,360, duration=0.01)
    zorder 99999
    #on "show" action SetVariable("default_mouse", "Null")   # прячем системный курсор
    #on "hide" action SetVariable("default_mouse", "default")# возвращаем обратно
    on "show" action Function(add_borders)
    on "hide" action Function(remove_borders)
    on "show" action [SetVariable("keyboard_control", False), SetVariable("moving_up2", False), SetVariable("moving_down2", False), SetVariable("moving_left2", False), SetVariable("moving_right2", False)]  # сбрасываем все флаги при показе
    on "hide" action [SetVariable("keyboard_control", False), SetVariable("moving_up2", False), SetVariable("moving_down2", False), SetVariable("moving_left2", False), SetVariable("moving_right2", False)]  # сбрасываем все флаги при скрытии
    
    on "show" action [
        #SetVariable("default_mouse", "Null"),
        SetVariable("keyboard_control", False),
        SetVariable("moving_up2", False),
        SetVariable("moving_down2", False),
        SetVariable("moving_left2", False),
        SetVariable("moving_right2", False),
        SetVariable("soul_update_active", True),

    ]

    on "hide" action [
        SetVariable("default_mouse", "default"),
        SetVariable("soul_update_active", False),
        Function(remove_borders)
    ]
    #timer 0.032 repeat True action Function(check_mouse_shift)





screen fightbegin:
    #timer 0.5 action MouseMove(640, 360, duration=0.3)
    timer 0.8 action Jump("fightbegin12")
label fightbegin12:
    hide screen game_screen

    # Сбрасываем выбор атакующего/целей/действия в начале боя.
    $ current_attacker = None
    $ selected_targets = []
    $ target = None
    $ actionid = None

    # Возвращаем всех персонажей в исходную позицию перед началом боя.
    python:
        for _char in store.pers_dict.values():
            _char.step_forward = 0

    # Криса индивидуально переводим из fight_start в idle в начале боя,
    # чтобы для него сразу выбиралась idle-анимация в ConditionSwitch.
    $ store.pers_dict["Крис"].state = "idle"

    # Сброс статуса завершения боя перед запуском нового сражения.
    $ battle_fully_resolved = False
    #$ reset_active_enemies_for_new_battle()
    show screen check_enemy_status

    $ current_round = 0
    $ default_mouse = 'Null'

    # Начало боя: перезарядки способностей снова равны изначальным,
    # одноразовые способности доступны заново, связь «Позвать за щит» разорвана.
    $ reset_battle_ability_cooldowns()
    $ reset_battle_one_time_abilities()
    $ clear_all_kris_shield_links()

    # Пассивки Криса на новый бой: снимаем «Вмятины на щите», возвращаем
    # «Желанию жить» одноразовость, «Причине ошибок» — начальный шанс.
    $ kris_reset_battle_passives()
    $ chara_reset_battle_passives()
    $ frisk_reset_battle_passives()
    $ clover_reset_battle_passives()
    $ izzy_reset_battle_passives()
    $ archie_reset_battle_passives()
    $ sedric_reset_battle_passives()
    $ init_all_frogs_battle_state()
    $ frog_apply_magic_aura_on_battle_start()

    # Пассивки Азриеля на новый бой: облик по умолчанию, «Образ принца»,
    # «Рука помощи», огневые шансы и накопленные бонусы защиты/танка.
    $ azri_reset_battle_state()

    # Сильвия: сброс очереди движений, исполненных танцев, репертуара,
    # прогресса уровней движений, дебаффа «Антракт» и накопленного танка.
    $ sylvia_reset_battle_state()
    # «Без лишнего легче» (ур.2): +3% крит-шанса за каждый пустой слот артефакта.
    $ sylvia_apply_empty_artifact_bonus()

    # Фабри: сброс призванных фамильяров, очереди создания, яйца
    # М-с Пёрышко, накопленных бонусов магии фамильяров и пассивок.
    $ fabri_reset_battle_state()
    $ fabri_reset_battle_passives()
    # «Передышка, чтоб вернуться» (ур.1): бонус к скорости души на бой.
    $ fabri_apply_respite()

    # Новые персонажи: сброс ресурсов, временных эффектов и пользовательских
    # состояний способностей перед каждым новым боем.
    $ new_character_reset_battle_state()

    $ tick_battle_ability_cooldowns()
    $ tick_battle_ability_cooldowns()
    $ tick_battle_ability_cooldowns()
    $ tick_battle_ability_cooldowns()
    $ tick_battle_ability_cooldowns()

    $ store.charicontimetodis = 1
    $ default_mouse = 'damaged'
    $ renpy.pause(0.7, hard=True)
    $ default_mouse = "default2"


    $ renpy.pause (1.0, hard = True)

    




    #show screen turntarget
    #show screen semiblackbg
    show screen targettochoose_sprites
    show screen team_status_display
    $ store.charicontimetodis = 0    

    call first_turn_dialogue


    jump enemy_turn
    
label enemy_turn:
    hide screen turntarget
    if current_round == 0:
        # Первый ход: сразу на экран атаки, без диалога
        #$ default_mouse = 'Null'
        $ default_mouse = "default2"
        call screen enemyattack
    else:
        # Последующие ходы: сначала диалог, потом атака
        jump enemydialogue
    
    # После того, как экран атаки закроется (через perform_enemy_attack),
    # мы возвращаемся сюда и переходим к завершению хода.



#                                                                3. Лейблы firstattack notfirstattack и экран attack содержит в себе атаки противников и прыжок в choose_attacker_screen_label то есть выбора перса. СЮДА ЖЕ МОЖНО ВСТАВИТЬ ЭКСТРАЛЕЙБЛЫ С СЮЖЕТНЫМИ ПОВОРОТАМИ И ДОП ПИЗДЕЖОМ
#                                                                4. Выбор перса устанавливает, кто ходит и сколько осталось ходить. После выбора перса отправляемся в playerturn с экранами хп и лейблом buttoms. Надо следить за txt который следит за стилем текстбокса
#                                                                5. Ход персонажей будет использовать экраны и/или лейблы с функциями. После которых через таймер или обычную строчку будет приходить к выбора перса в лейбл choose_attacker_screen_label
#                                                                6. Если все сходили,то будет прыжок в лейбл firstattack
#                                                                7. Если бой по сценарию окончен, то будет прыжок в нужный лейбл после боя, который представляет из себя очистку данных и либо вызов нужного экрана с полем приключений, либо лейбл со сценарием.









#                                                                 ЭКРАН



label playerturn:
    # Уменьшаем длительность всех баффов на 1 ход
    #$ reduce_all_consumable_buffs()
    #Начало раунда. Игрок выбирает персонажа
    #$ txt = 0
    call character_to_choose
label playerturn2:
    $ target = None
    $ attackindex = None
    # Тип цели сбрасывается, чтобы «залипший» toally/totarget от прошлого
    # действия не запускал исполнение при клике по цели в выборе персонажа.
    $ turntype = 0

    # Начало хода Сильвии: пассивки, привязанные к началу её хода.
    if current_attacker == 9:
        # «Антракт» (ур.1): если мана была исчерпана, Сильвия пропускает ход.
        $ _sylvia_entracte_blocked = sylvia_tick_entracte_start()

        # «Своя очередь» (ур.1): бонус защиты/крит-шанса в зависимости
        # от того, ходит она первой или последней в раунде.
        if not _sylvia_entracte_blocked:
            $ sylvia_apply_initiative()

            # Репертуар: на первом ходу игрок выбирает до 3 танцев,
            # если уровень не ниже порога; иначе набор берётся сам.
            if sylvia_ensure_repertoire():
                call screen sylvia_repertoire_screen()

    # Начало хода Фабри (ID 10): ауры призванных фамильяров действуют
    # каждый ход. Если ход она не тратит (например, отменила выбор),
    # ауры всё равно применятся корректно — их эффекты аддитивны.
    if current_attacker == 10:
        $ _fabri_aura_log = fabri_apply_auras()
        # «Разнообразие – лучшее вдохновение» ур.1 требует, чтобы вся еда
        # была разного типа; типы копятся по ходу боя.
        $ fabri_note_battle_food_types()
        # Игрок должен видеть состояние своих фамильяров: «Рукодельные
        # друзья» — вся их механика построена на живых призванных.
        $ _fabri_status = fabri_familiar_status()
        if _fabri_status:
            $ renpy.notify("Рукодельные друзья: " + ", ".join(
                "{} {}/{}".format(f["name"], f["hp"], f["max_hp"]) for f in _fabri_status))

    show screen turntarget
    hide screen semiblackbg
    $ renpy.pause (1, hard = True)
    
    #$ txt = 1
    show dialogue1round at ddu



    # Используем централизованную функцию для инициализации team_manager
    $ store.ensure_team_manager()
    
    #show screen charhpbg

    #call screen turnchoose_analogue
    
    jump buttoms

label character_to_choose:
    $ turntype = 0
    #$ show_team_status = 0
    #$ show_enemy_status = 0
    show screen turntarget
    
    show screen targettochoose_sprites
    show screen team_status_display
    #show screen semiblackbg
    $ compact_consumable_inventory_after_stack_depleted()
    call screen choose_attacker_screen()
    $ renpy.pause (1.0, hard=True)
    jump playerturn2




###############################################

label turn_is_done:
    # Теперь current_attacker содержит номер персонажа
    if current_attacker:
        # Определяем имя персонажа по номеру
        $ attacker_names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск", 5: "Иззи", 6: "Кловер", 7: "Седрик", 8: "Арчи", 9: "Сильвия", 10: "Фабри", 11: "Эмили", 12: "Сьюзи", 13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
        $ attacker_name = attacker_names.get(current_attacker)
        if attacker_name and attacker_name in store.pers_dict:
            # Устанавливаем turn = 0 для объекта персонажа
            $ store.pers_dict[attacker_name].turn = 0
    
    jump playerturn


screen semiblackbg:
    zorder 2
    #add "semiblackbg.png" at alphatransformforbg
    vbox:
        at alphatransformforbg
        imagebutton:
            idle "semiblackbg3.png"
            hover "semiblackbg3.png"
            action NullAction()

transform alphatransformforbg:
    on show:
        xpos 0 ypos 0 alpha 0.0
        easeout 0.5 alpha 0.5
    on hide:
        xpos 0 ypos 0
        easein 0.5 alpha 0.0



























label first_turn_dialogue:
    $ default_mouse = 'default2'

    if battlenumber == 11: 
        "Готовься к битве!"
    elif battlenumber == 13:
        "Манекен 2 вышел на бой!"
    $ default_mouse = "default2"

    window hide

    $ renpy.pause (1.0, hard = True)
    $ default_mouse = "Null"
    $ default_mouse = "default2"



    $ lock_mouse_input()
    show screen enemybgappears
    $ renpy.set_mouse_pos(screenxpos+0.5*xbord, screenypos+0.5*ybord, duration = 1)
    $ renpy.pause(1.2, hard=True)
    $ unlock_mouse_input()

    #поставь здесь стилькурсора Null
    $ default_mouse = "default2"

    show screen Move_mouse

    


    hide screen Move_mouse

init python:
    def _safe_keymap_list(value):
        """Некоторые записи в config.keymap могут быть None."""
        if value is None:
            return []
        if isinstance(value, (list, tuple, set)):
            return list(value)
        return [value]

    def lock_mouse_input():
        """Сохраняем keymap и глушим ЛКМ/пробел/энтер."""
        store._saved_keymap = {
            k: _safe_keymap_list(v) for k, v in config.keymap.items()
        }
        for k in ("dismiss", "button_select", "button_ignore",
                    "mouseup_1", "mousedown_1"):
            if k in config.keymap:
                config.keymap[k] = []
        renpy.restart_interaction()

    def unlock_mouse_input():
        """Возвращаем keymap в исходное состояние."""
        if getattr(store, "_saved_keymap", None):
            for k, v in store._saved_keymap.items():
                config.keymap[k] = v
            store._saved_keymap = None
        renpy.restart_interaction()









# Создайте пустую метку для диалога врага
label enemydialogue:
    # Здесь будет диалог врага. В конце диалога нужно вызвать экран атаки.
    # Например:
    if battlenumber == 3: #Джевил
        if current_round == 0:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 1: 
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 2:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 3:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 4:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 5:
            "Джевил: Хи-хи, пора потанцевать!"
    






    $ MouseMove(640, 360, duration = 0.3)
    #$ renpy.pause(0.3, hard=True)
    #$ default_mouse = 'Null'
    $ default_mouse = 'default2'
    call screen enemyattack # После атаки возвращаемся сюда, а оттуда - в player_turn_sequence









label enemydialogue_after_turn: # диалоги во время хода противника
    if battlenumber == 3:
        if current_round == 0: #Джевил
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 1:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 2:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 3:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 4:
            "Джевил: Хи-хи, пора потанцевать!"
        elif current_round == 5:
            "Джевил: Хи-хи, пора потанцевать!"
        else:
            pass
    



    $ store.default_mouse = "default"
    call screen choose_attacker_screen()
