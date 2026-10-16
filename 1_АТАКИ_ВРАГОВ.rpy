


                                                                                                    
#              @@@                                                                                   
#             @@@@@                                                                                  
#            @@@@@@                                                                                  
#            @@@ @@@      @@@@@@@@@@@    @@@@@@       @@      @@    @@       @@                      
#           @@@  @@@     @@@@@@@@@@@@  @@@@@@@@@@    @@@    @@@@   @@@     @@@@                      
#          @@@    @@@         @@@      @       @@@   @@@  @@@@     @@@    @@@@@                      
#         @@@@     @@@        @@@           @@@@@@   @@@ @@@       @@@   @@@ @@                      
#         @@@@@@@@@@@@@       @@@      @@@@@@@@@@@   @@@@@@        @@@  @@@  @@                      
#        @@@@@@@@@@@@@@@      @@@     @@@      @@@   @@@ @@@@      @@@@@@@   @@                      
#       @@@@         @@@      @@@     @@@     @@@@   @@@  @@@@     @@@@@@    @@                      
#       @@@           @@@     @@@     @@@@@@@@@@@@   @@@    @@@@   @@@@      @@                      
#      @@@            @@@     @@@       @@@@@  @@@   @@@      @@@  @@@       @@                      
                                                                                                    

default soul_outrange = 0


default enemies_is_attacking = 0


#                                                                   Атаки
#                                       Демо

default enemy_atk_is_done = 0
default current_round = 0
default current_enemy = None

default current_attacking_enemy = None

init python:
    def enemy_can_take_turn(enemy):
        """Возвращает True, если враг может выполнить активную атаку.

        Все эффекты, которые именно блокируют действие, проверяются здесь в
        одном месте. Обычные ослабления (кровотечение, защита, точность и
        т.п.) ход не блокируют и поэтому в список не входят.
        """
        if enemy is None or getattr(enemy, "current_hp", 0) <= 0:
            return False
        if getattr(enemy, "turn", 0) != 1:
            return False
        blocking_statuses = (
            "prone_debuff",                 # оглушение, опрокидывание, тюрьма
            "emily_debuff_distracted",      # «Отвлечён»
            "emily_debuff_disabled",        # «Отключён»
            "sans_prone",                   # «Прижмись»
            "noelle_ice_tomb",              # ледяная могила
            "noelle_cocoon",                # защитный кокон, если наложен на цель
        )
        if any(bool(getattr(enemy, status, 0)) for status in blocking_statuses):
            return False
        if "clover_prison_blocks_turn" in globals() and clover_prison_blocks_turn(enemy):
            return False
        return True

    def enemy_turn_is_done(enemy_name):
        enemy = store.enemies.get(enemy_name) if hasattr(store, "enemies") and store.enemies else None
        return enemy is None or getattr(enemy, "dead", False) or getattr(enemy, "current_hp", 0) <= 0 or getattr(enemy, "turn", 0) == 1

    def all_battle_enemies_done():
        names = get_active_enemies() if "get_active_enemies" in globals() else []
        return bool(names) and all(enemy_turn_is_done(name) for name in names)

    def enemy_attack_and_show_results(enemy):
        """
        Функция для атаки врага по случайному герою и показа результатов.
        """
        if not enemy_can_take_turn(enemy):
            return

        # Проверяем, что team_manager инициализирован
        if store.team_manager is None:
            store.team_manager = TeamManager()
            store.team_manager.rebuild_team_from_picked()
            
        # 1. Выбираем цель для атаки
        target_hero = store.team_manager.get_character_to_hit()

        # 2. Устанавливаем текущего врага для экрана дебафов
        store.current_enemy = enemy

        # 3. Рассчитываем и наносим урон (дебафы применяются внутри calculate_dmg_to_hero)
        damage = enemy.calculate_dmg_to_hero(target_hero)
        
        # 3.5. «Перестрелка в полдень» Кловера (ур.5): когда противник атакует
        # Кловера — неважно, промахнулся, попал или ударил в щит, — тот
        # отвечает выстрелом. Шанс попадания = 18% от текущего шанса
        # попадания Кловера, тратится патрон, урон учитывает калибр.
        if getattr(target_hero, "name", None) == "Кловер":
            if clover_on_enemy_attack(enemy):
                riposte_damage = clover_noon_damage(enemy)
                if riposte_damage > 0:
                    enemy.current_hp = max(0, getattr(enemy, "current_hp", 0) - riposte_damage)
                    add_attack_result("Кловер", enemy.name, riposte_damage, False, "normal")
        
        
        # 5. Добавляем в новую систему множественных атак
        if damage > 0:
            add_attack_result(enemy.name, target_hero.name, damage, enemy.crits == 1, "enemy")
        
        # 4. Проверяем, не проиграли ли мы
        if all(char.current_hp <= 0 for char_name, char in store.characters.items() if char_name in store.team_manager.team_slots):
            renpy.jump("gameover")
        
        # 5. Показываем экран с результатами
        renpy.show_screen("heroes_attacked_visual")


screen enemyattack:
    zorder 2
    $ jevil_speed = store.enemies["ДжевилV1"].speed
    timer 0.1 action SetVariable ("enemies_is_attacking", 1) repeat False
    if all_battle_enemies_done():
        timer 0.01 action [Function(archie_enemy_attack_phase_hook), Jump("afterenemyattack")]

    #timer 0.5 action SetVariable("souloutrange", 0) repeat True

        # При показе экрана
    on "show" action [
        Hide("turntarget"),
        Function(lambda: config.keymap.update({'screenshot': []})),
        Function(lambda: config.keymap.update({'focus_up': []})),
        Function(lambda: config.keymap.update({'focus_down': []})),
        Function(sync_attack_mouse_position),
    ]
    
    # При скрытии экрана - восстанавливаем стандартные
    on "hide" action [
        Function(lambda: config.keymap.update({'screenshot': ['K_s']})),
        Function(lambda: config.keymap.update({'focus_up': ['K_UP', 'K_w']})),
        Function(lambda: config.keymap.update({'focus_down': ['K_DOWN', 'K_s']})),
        SetVariable("attack_mouse_initialized", False),
    ]
    

    on "show" action Function(add_attack_borders)
    on "hide" action Function(remove_attack_borders)

    #timer 0.01 action [MouseMove(640, 360, duration=0.3)]
    #timer 0.01 action Show ("mouse_restricted_area")
    use mouse_restricted_area
    #textbutton"Значение persistent.hp: [persistent.hp]"

    if battlenumber == 3: #Джевил
        # потом если turn = 0, 1, 2, 3 и т.д.
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Переход через таймер в след часть лейбла
        # timer N action [Setvariable (turn, turn+1), Setvariable(enemy_atk_is_done, 0), Return() ]
        
        

        if current_round == 0:
            use Jevil_bullet_attack1
            timer 10.5 / store.enemies["ДжевилV1"].speed action [Function(setattr, store.enemies["ДжевилV1"], "turn", 1)]
            #Здесь можно диаалоги ввсиавиит перед таймером

        elif current_round == 1:
            $ jevil_attack_roll = renpy.random.randint(0, 100)
            if jevil_attack_roll <= int(store.enemies["ДжевилV1"].critrate2):
                imagebutton:
                    at textbuttontest
                    idle "fightor.png"
                    hover "magicor.png"
                    action [
                        SetVariable("enemymonster", store.enemies.get("ДжевилV1")),
                        Function(enemy_attack_without_closing_screen),
                        Function(setattr, store.enemies["ДжевилV1"], "turn", 1)
                    ]
            use Jevil_bullet_attack1
            timer 10.5 / store.enemies["ДжевилV1"].speed action [Function(setattr, store.enemies["ДжевилV1"], "turn", 1)]

    #timer 0.3 action [Show("heal")] repeat True
    # timer 0.4 action [Hide("heal")] repeat True
    
    elif battlenumber == 1: #Арчи
        if hasattr(store, 'enemies') and store.enemies:
            $ active_enemies = get_active_enemies()
            $ archie_enemy_name = active_enemies[0] if len(active_enemies) > 0 else "Арчи"
            imagebutton:
                idle "atk_idle.png"
                hover "atk_hover.png"
                action [
                    SetVariable("enemy_ind_atk_ratio", 1.0),
                    Function(enemy_attack_and_show_results, store.enemies.get(archie_enemy_name)),
                    Show("protected_screen")
                ]
            timer 5 / store.enemies[archie_enemy_name].speed action [Function(setattr, store.enemies[archie_enemy_name], "turn", 1)]

    elif battlenumber == 2: #Тревор
        if hasattr(store, 'enemies') and store.enemies:
            imagebutton:
                idle "trevor_atk.png"
                hover "trevor_atk_hover.png"
                action [
                    SetVariable("enemy_ind_atk_ratio", 0.8),
                    Function(enemy_attack_and_show_results, store.enemies.get("Тревор"))
                ]
    
    elif battlenumber == 4: #Психолог
        if hasattr(store, 'enemies') and store.enemies:
            imagebutton:
                idle "psycho_atk.png"
                hover "psycho_atk_hover.png"
                action [
                    SetVariable("enemy_ind_atk_ratio", 1.2),
                    Function(enemy_attack_and_show_results, store.enemies.get("Психолог"))
                ]
    
    elif battlenumber == 5: #Спамтон
        if hasattr(store, 'enemies') and store.enemies:
            imagebutton:
                idle "spamton_atk.png"
                hover "spamton_atk_hover.png"
                action [
                    SetVariable("enemy_ind_atk_ratio", 1.5),
                    Function(enemy_attack_and_show_results, store.enemies.get("Спамтон"))
                ]








    
    elif battlenumber == 10:
        timer 0.001 action [Hide ("enemyattack"),Show("faster_attack_10_1")]

    elif battlenumber == 11:
        if hasattr(store, 'enemies') and store.enemies:
            $ active_enemies = get_active_enemies()
            imagebutton:
                xpos 600 ypos 400
                idle "fightor.png"
                hover "magicor.png"
                hovered [SetVariable("enemymonster", store.enemies.get(active_enemies[0] if len(active_enemies) > 0 else "dummy")), Function(enemy_attack_without_closing_screen)]
                action NullAction()
            imagebutton:
                at textbuttontest
                idle "fightor.png"
                hover "magicor.png"
                hovered [SetVariable("enemymonster", store.enemies.get(active_enemies[0] if len(active_enemies) > 0 else "dummy")), Function(enemy_attack_without_closing_screen)]
                action NullAction()
            timer 10.5 / store.enemies["dummy"].speed action [Function(setattr, store.enemies["dummy"], "turn", 1)]
            timer 13 / store.enemies["Тревор"].speed action [Function(setattr, store.enemies["Тревор"], "turn", 1)]
            timer 16 / store.enemies["ДжевилV1"].speed action [Function(setattr, store.enemies["ДжевилV1"], "turn", 1)]



    elif battlenumber == 13:
        if hasattr(store, 'enemies') and store.enemies:
            imagebutton:
                xpos 600 ypos 500
                idle "fightor.png"
                hover "magicor.png"
                action [
                    SetVariable("enemy_ind_atk_ratio", 1.5),
                    Function(enemy_attack_and_show_results, store.enemies.get("dummy2"))
                ]

            imagebutton:
                at textbuttontest_t2
                idle "fightor.png"
                hover "magicor.png"
                hovered [SetVariable("enemymonster", store.enemies.get("dummy2")), Function(enemy_attack_without_closing_screen)]
                action NullAction()
        timer 14 / store.enemies["dummy2"].speed action [Function(setattr, store.enemies["dummy2"], "turn", 1)]





    #add DynamicDisplayable(soul_cursor)
    
    #timer 0.03 action [Function(renpy.restart_interaction)] repeat True
    #timer 999999 action Jump("nolabel")


label Attacktohero:
    $ store.enemymonster.calculate_dmg_to_hero(store.team_manager.get_character_to_hit())
    return

# Функция для атаки врага без закрытия экрана
init python:
    def enemy_attack_without_closing_screen():
        """
        Функция для атаки врага без закрытия экрана.
        """
        if (hasattr(store, 'enemymonster') and store.enemymonster and
                enemy_can_take_turn(store.enemymonster)):
            # Проверяем, что team_manager инициализирован
            if store.team_manager is None:
                store.team_manager = TeamManager()
                store.team_manager.rebuild_team_from_picked()
            
            # Выбираем цель для атаки
            target_hero = store.team_manager.get_character_to_hit()
            
            # Устанавливаем текущего врага для экрана дебафов
            store.current_enemy = store.enemymonster
            
            # Рассчитываем и наносим урон (дебафы применяются внутри calculate_dmg_to_hero)
            damage = store.enemymonster.calculate_dmg_to_hero(target_hero)
            

            # Показываем результаты атаки без закрытия экрана
            renpy.show_screen("attacked_compiled")
            # Устанавливаем таймер для скрытия экрана с результатами через 2 секунды
            #renpy.timer(2.0, renpy.hide_screen("heroes_attacked_visual"))



default pressedbullet = 0

#screen Damagedscreen:

    #SetVariable("pressedbullet", 1)
    #if souloutrange == 1 and store.pressedbullet == 1:
    #    timer 0.3 action Hide("Damagedscreen")
    #    timer 0.001 action SetVariable("souloutrange", 0) repeat True
    #    #timer 0.001 action MouseMove(640,320)
    #    pass
        #timer 0.01 action SetVariable("pressendbullet", 0) repeat True
    #elif souloutrange == 0 and store.pressedbullet == 1:
    #    timer 0.1 action Function(enemy_attack_without_closing_screen)
        
    #    add ("whitebg.png") xpos 0 ypos 0
    #    timer 0.5 action Hide("Damagedscreen")















transform textbuttontest_t2:
    xpos 1200 yalign 0.5
    easein 20*store.enemies.get("dummy2").speed xpos 0






transform textbuttontest:
    xpos 1200 yalign 0.5
    easein 20 xpos 0

transform alpha05:
    alpha 0.5

transform alpha052:
    alpha 0.5 xzoom 0.2





screen Jevil_bullet_attack1():
    # Основной фрейм 1000x1000 - вращается 5 кругов и двигается влево
    frame:
        xsize 1000
        ysize 1000
        xalign 0.5
        yalign 0.5
        background None
        
        # Анимация вращения (5 полных оборотов = 1800 градусов) и движения влево
        at rotate1800
        
        # Внутренний фрейм с imagebutton'ами
        frame:
            xalign 0.0  # Влево
            yalign 0.0  # Максимально высоко
            background None
            
            # Бесконечное вращение внутреннего фрейма
            at rotateinf
            
            # Горизонтальная часть (максимально высоко и влево)
            imagebutton:
                idle "bullet_horizontal.png"
                action NullAction()
                xalign 0.0
                yalign 0.0
            
            # Вертикальная часть (влево, ниже горизонтальной)
            imagebutton:
                idle "bullet_vertical.png"
                action NullAction()
                xalign 0.0
                ypos 100  # Отступ от верха, настройте под размер вашего изображения
transform rotate1800:
    rotate 0
    xoffset 0
    linear 5.0 rotate 1800 xoffset -500

transform rotateinf:
    rotate 0
    linear 3.0 rotate 360
    repeat True








init python:
    def click_screen_center():
        """
        Программно симулирует клик мыши точно по центру экрана.
        Безопасна для использования в любом контексте (бой, меню, диалоги).
        """
        import pygame
        
        # 1. Получаем актуальные размеры экрана из конфига Ren'Py
        center_x = config.screen_width // 2
        center_y = config.screen_height // 2
        
        # 2. Формируем события нажатия и отпускания кнопки мыши
        # button=1 соответствует левой кнопке мыши
        pos = (center_x, center_y)
        
        down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, 
            {'pos': pos, 'button': 1}
        )
        up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP, 
            {'pos': pos, 'button': 1}
        )
        
        # 3. Отправляем события в очередь обработки Ren'Py/Pygame
        pygame.event.post(down_event)
        pygame.event.post(up_event)


    
label afterenemyattack:
    $ store.default_mouse = "default"
    $ store.current_round += 1
    
    # ШАГ 1: Полная остановка физики (ПЕРВЫМ ДЕЛОМ)
    $ reset_soul_state()

    if battlenumber == 1:
        $ archie_on_battle_round_tick()

    # ШАГ 2: Освобождение мыши с сохранением позиции
    $ force_release_mouse()
    
    $ store.enemies_is_attacking = 0
    $ active_enemies = get_active_enemies()
    
    python:
        for enemy_name in active_enemies:
            enemy = store.enemies.get(enemy_name) if hasattr(store, 'enemies') and store.enemies else None
            if enemy is not None:
                enemy.turn = 0
    
    hide screen enemybgappears

    $ apply_debuffs_at_round_start()
    $ apply_debuffs_at_round_start_enemies()
    $ chara_on_round_end()
    $ frisk_prepare_round_end()
    # Иззи: диета, случайное провиденье, отсчёт кармы.
    $ izzy_on_round_end()
    # «Подозрительная проницательность»: соц. бонус за осмотр (идемпотентно).
    $ izzy_apply_insight_bonus()
    # Кловер: вафелька, угощение в салуне, отсчёт тюремных сроков,
    # метка судьбы и «Внезапная заначка» в конце хода.
    $ clover_on_round_end()
    # «Зоркий Глаз - Зоркий ум»: соц. характеристики пересчитываются от
    # текущих боевых (точность/крит-шанс/крит-урон).
    $ clover_apply_sharp_eye()
    # Арчи: регенерация 8%+ур*0.5 HP и MP, попытка подняться после падения,
    # отсчёт храбрости и сроков эффектов.
    $ archie_on_round_end()
    $ archie_tick_courage()
    $ archie_tick_all()
    $ sedric_on_round_end()
    # Фабри: перезарядка магии фамильяров сбрасывается 1 раз за раунд
    # ВСЕГДА, независимо от того, жив фамильяр или нет. Здесь же идёт
    # отсчёт яйца М-с Пёрышко, тик бонуса скорости М-с Морковки и
    # бонус «Разнообразие – лучшее вдохновение» за еду разного типа.
    $ fabri_familiar_tick_round()
    $ fabri_egg_tick_round()
    $ fabri_tick_round_effects()
    # Конец раунда (после атак врага): вместе со стаками дебафов
    # на 1 уменьшается текущая перезарядка всех способностей.
    # current_round == 1 — это стартовая атака врага (раунд 0) до первого
    # хода игрока, поэтому initial_cooldown там ещё не трогаем.
    if current_round > 1:
        $ tick_battle_ability_cooldowns()

    python:
        for _char in store.pers_dict.values():
            _char.step_forward = 0

    # ШАГ 3: Пауза ТОЛЬКО после полной остановки физики
    $ renpy.pause(2.0, hard=True)

    if battlenumber == 3:
        if current_round == 0:
            jump enemydialogue_after_turn
        elif current_round == 1:
            jump enemydialogue_after_turn
        elif current_round == 2:
            jump enemydialogue_after_turn
        elif current_round == 3:
            jump enemydialogue_after_turn
        elif current_round == 4:
            call screen choose_attacker_screen()
        elif current_round == 5:
            call screen choose_attacker_screen()
    else:
        call screen choose_attacker_screen()























screen faster_attack_10_1:


    zorder 2
    $ jevil_speed = store.enemies["ДжевилV1"].speed
    timer 0.1 action SetVariable ("enemies_is_attacking", 1) repeat False
    if all_battle_enemies_done():
        timer 0.01 action [Hide("faster_attack_10_1"),Jump("afterenemyattack")]

    #timer 0.5 action SetVariable("souloutrange", 0) repeat True

        # При показе экрана
    on "show" action [
        Hide("turntarget"),
        Function(lambda: config.keymap.update({'screenshot': []})),
        Function(lambda: config.keymap.update({'focus_up': []})),
        Function(lambda: config.keymap.update({'focus_down': []})),
        Function(sync_attack_mouse_position),
    ]
    
    # При скрытии экрана - восстанавливаем стандартные
    on "hide" action [
        Function(unlock_mouse_input),
        Function(lambda: config.keymap.update({'screenshot': ['K_s']})),
        Function(lambda: config.keymap.update({'focus_up': ['K_UP', 'K_w']})),
        Function(lambda: config.keymap.update({'focus_down': ['K_DOWN', 'K_s']})),
        SetVariable("attack_mouse_initialized", False),
        SetVariable("enemies_is_attacking", 0),
        SetVariable("soul_update_active", False),
        Function(remove_borders)
    ]
    

    on "show" action Function(add_attack_borders)
    on "hide" action Function(remove_attack_borders)

    #timer 0.01 action [MouseMove(640, 360, duration=0.3)]
    #timer 0.01 action Show ("mouse_restricted_area")
    use mouse_restricted_area

    if hasattr(store, 'enemies') and store.enemies:
        $ active_enemies = get_active_enemies()
    
    $ active_enemy = store.enemies.get(active_enemies[0] if len(active_enemies) > 0 else "�������")
    if enemy_can_take_turn(active_enemy):
        imagebutton:
            idle "spamton_atk.png"
            hover "spamton_atk_hover.png"
            action [
                SetVariable("enemy_ind_atk_ratio", 1.5),
                Function(enemy_attack_and_show_results, active_enemy)
            ]
        imagebutton:
            at textbuttontest
            idle "fightor.png"
            hover "magicor.png"
            hovered [SetVariable("enemymonster", active_enemy), Function(enemy_attack_without_closing_screen)]
            action NullAction()
    
    
    timer 1 / store.enemies[active_enemies[0]].speed action [Function(setattr, store.enemies[active_enemies[0]], "turn", 1)]
    timer 1/ store.enemies["Тревор"].speed action [Function(setattr, store.enemies["Тревор"], "turn", 1)]
    timer 1 / store.enemies["ДжевилV1"].speed action [Function(setattr, store.enemies["ДжевилV1"], "turn", 1)]
    timer 1 / store.enemies["Психолог"].speed action [Function(setattr, store.enemies["Психолог"], "turn", 1)]
