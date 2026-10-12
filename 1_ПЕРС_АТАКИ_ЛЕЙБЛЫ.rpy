

init python:
    def clear_kris_shield_link(*chars):
        """Разрывает связь магии «Позвать за щит» и обнуляет бонус защиты.

        Бонус kris_shield_def_bonus входит в Pers.defense, поэтому снимать
        его нужно вместе со связью — иначе союзник навсегда останется
        с повышенной защитой. Функция идемпотентна.
        """
        for char in chars:
            # Связь есть только у героев (Pers); врагов не трогаем.
            if char is None or not hasattr(char, "kris_shield_partner"):
                continue
            partner = getattr(char, "kris_shield_partner", None)
            if partner is not None:
                partner.kris_shield_partner = None
                partner.kris_shield_def_bonus = 0
            char.kris_shield_partner = None
            char.kris_shield_def_bonus = 0

    def clear_all_kris_shield_links():
        """Снимает связь «Позвать за щит» со всех героев."""
        for _char in store.pers_dict.values():
            clear_kris_shield_link(_char)

    def get_kris_relations_check(reltns):
        if reltns <= -80:
            return 10
        elif reltns <= -60:
            return 30
        elif reltns <= -40:
            return 40
        elif reltns <= -20:
            return 50
        elif reltns < 20:
            return 60
        elif reltns < 40:
            return 70
        elif reltns < 60:
            return 80
        elif reltns < 80:
            return 90
        else:
            return 100

    def get_random_alive_enemy():
        enemies = getattr(store, "enemies", {})
        active_names = get_active_enemies() if "get_active_enemies" in globals() else []
        alive = [
            enemies[name] for name in active_names
            if name in enemies and getattr(enemies[name], "current_hp", 0) > 0
        ]
        if not alive:
            alive = [
                enemy for enemy in enemies.values()
                if getattr(enemy, "current_hp", 0) > 0
            ]
        if not alive:
            return None
        return alive[renpy.random.randint(0, len(alive) - 1)]

    # VESSEL CONTROL: подбор автоатаки при срыве управления перенесён в
    # 1_ПЕРС_ПАССИВКИ_КРИСА.rpy (get_kris_failed_attack_index /
    # kris_failed_control_attack) — там добавлена проверка перезарядки атак.

    def apply_enemy_slow(enemy, amount=0.1):
        """Замедление врага: enemy.speed (таймеры атаки) и bullet_speed снарядов.

        Эффект накапливается: -10% дважды даёт -19%, но speed не опускается
        ниже 0.5 (тот же диапазон, что и в Enemy.__init__).
        """
        if enemy is None:
            return 1.0
        factor = max(0.0, 1.0 - float(amount))
        if hasattr(enemy, "speed"):
            enemy.speed = max(0.5, min(1.5, float(enemy.speed) * factor))
        if hasattr(enemy, "bullet_speed"):
            enemy.bullet_speed *= factor
        return getattr(enemy, "speed", 1.0)


label Kris_check_control:
    $ Kris_relations_check = get_kris_relations_check(store.pers_dict["Крис"].reltns)
    #$ Kris_control_roll = renpy.random.randint(0, 100)
    $ Kris_control_roll = 0
    if Kris_relations_check >= 100 or Kris_control_roll < Kris_relations_check:
        jump playerturn2
    else:
        jump Kris_failed_control

label Kris_failed_control:
    hide screen choose_attack_screen
    hide screen turntarget
    hide screen attack_description

    $ current_attacker = 1
    $ target = get_random_alive_enemy()
    # VESSEL CONTROL: берём самую сильную доступную атаку Криса из очереди
    # (не то оружие, низкий уровень и перезарядка пропускаются) и сразу
    # ставим ей перезарядку.
    $ attackindex = kris_failed_control_attack()
    $ attackindexdesc = attackindex
    $ turntype = "toenemy"
    $ atk_ind_ratio = 0.6 if attackindex == "Удар неудачника" else 1
    $ base_perform =  renpy.random.uniform(0.6, 0.9)
    $ stick_xpos = 640
    $ kris1_atk_pressed = 1
    $ store.pers_dict["Крис"].step_forward = 1

    # У каждой атаки Криса свой лейбл завершения.
    $ kris_failed_label = KRIS_ATTACK_LABELS.get(attackindex, "kris_atk1_is_done")
    jump expression kris_failed_label


label set_buttons_to_default:
    $ fightchoice = 0
    $ actchoice = 0
    $ magicchoice = 0
    $ itemchoice = 0
    $ target = None
    $ attackindex = None
    return

label herodefend:
    # current_attacker теперь содержит номер персонажа
    #if current_attacker:
    #    # Определяем имя персонажа по номеру
    #    $ attacker_names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск", 5: "Иззи", 6: "Кловер", 7: "Седрик"}
    #    $ attacker_name = attacker_names.get(current_attacker)
    #    if attacker_name and attacker_name in store.pers_dict:
    #        # Устанавливаем параметры для объекта персонажа
    #        $ store.pers_dict[attacker_name].indefense = 1
    #        $ store.pers_dict[attacker_name].bonus_def *= 2
    #        $ store.pers_dict[attacker_name].turn = 0
    
    hide screen Heroattacks
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    # «Правильный угол» ур.5: 10% шанс получить 1 щит за защиту.
    $ kris_on_defend_action()
    # «Строя оборону» ур.1: каждая защита Азриеля даёт +5% бонусной защиты.
    $ azri_on_defend()
    
    # «Причина ошибок»: у Криса защита тоже может дать дополнительный ход.
    # Для остальных персонажей turn не трогаем — поведение прежнее.
    $ kris_apply_action_turn_for_current()
    
    call screen choose_attacker_screen()

label afterheroattack:
    $ characterstoturn =- 1
    call screen choose_attacker_screen()


#                                                                           АТАКА КРИСА 1


screen enemeyhpinfo:
    # Проверяем, существует ли враг с именем "Джевил"
    $ enemy_hp = 0
    python:
        if 'ДжевилV1' in enemies:
            enemy_hp = enemies['ДжевилV1'].current_hp
        else:
            # Если врага с таким именем нет, берём первого доступного врага
            if enemies:
                first_enemy = next(iter(enemies.values()))
                enemy_hp = first_enemy.current_hp
    text "[enemy_hp]" xpos 500 ypos 500



label kris_atk1_is_done:
    # Параметры атаки
    $ atk_ind_ratio = 1.0

    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    

    
    

    # === НАЧАЛО ДИАГНОСТИКИ ===
    #$ renpy.notify("=== НАЧАЛО АТАКИ КРИСА (УДАР НЕУДАЧНИКА) ===")
    #$ renpy.pause(3.0, hard=False)
    #$ renpy.notify(f"Обновленный base_perform: {store.base_perform}")
    #$ renpy.pause(3.0, hard=False)

    #$ renpy.notify(f"stick_xpos: {stick_xpos}")
    #$ renpy.pause(3.0, hard=False)

    #$ renpy.notify(f"target: {target}")
    #$ renpy.pause(3.0, hard=False)
    #$ renpy.notify(f"target is None: {target is None}")
    #$ renpy.pause(3.0, hard=False)


    #$ renpy.notify(f"store.pers_dict['Крис'].atk: {store.pers_dict['Крис'].atk}")
    #$ renpy.pause(3.0, hard=False)
    #$ renpy.notify(f"store.pers_dict['Крис'].dmgchance: {store.pers_dict['Крис'].dmgchance}")
    #$ renpy.pause(3.0, hard=False)

    #$ renpy.notify(f"store.pers_dict['Крис'].perform: {store.pers_dict['Крис'].perform}")
    #$ renpy.pause(3.0, hard=False)




    # Нанесение урона

    if kris1_atk_pressed == 1:
        $ prepare_turn_effect_target(target)
        $ store.pers_dict["Крис"].state = "fight1"
        show screen targettochoose_sprites_effect_universal
        $ renpy.pause(1.3, hard=True)
        # Проверяем, что цель выбрана
        if target is not None:

            # 20% шанс различных эффектов
            $ effect_roll = renpy.random.randint(1, 100)
            if effect_roll <= 20:
                $ sub_effect = renpy.random.randint(1, 4)
                if sub_effect == 1:
                    # Повалить, выбить дух противника (stun)
                    $ target.debuff("prone", +1)
                    #$ renpy.notify("Застанили противника")
                    #$ renpy.pause(3.0, hard=False)

                elif sub_effect == 2:
                    # Ушибить себе руки (дебаф атаки для Криса)
                    $ store.pers_dict["Крис"].bonus_atk -= 0.2
                    $ store.pers_dict["Крис"].atk_debuff_got = 1
                    #$ renpy.notify("Крис отбил руки")
                    #$ renpy.pause(3.0, hard=False)
                elif sub_effect == 3:
                    # Взбесить врага (увеличить атаку врага)
                    $ target.debuff("atk", +3)
                    #$ renpy.notify("Взбесили")
                    #$ renpy.pause(3.0, hard=False)

                elif sub_effect == 4:
                    # Упасть (prone для Криса)
                    #store.pers_dict["Крис"].bloodshed_debuff
                    $ store.upal = 1
                    #$ store.pers_dict["Крис"].prone_debuff += 2
                    #$ store.pers_dict["Крис"].prone_debuff_got += 2

                    #$ renpy.notify("Крис бухнул")
                    #$ renpy.pause(3.0, hard=False)
            
            # Добавляем результат атаки в новую систему множественных атак
            if dmg > 0 and store.pers_dict["Крис"].popal == 1:
                $ store.is_crit = store.pers_dict["Крис"].crit > 1.0
                #$ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
                
                # Эффект hpunch всегда; при критическом ударе усиливаем
            
            #if is_crit:
            #    with crit_vpunch
            #    pause 1
            #else:
            #    with vpunch
            #    pause 1


            #$ renpy.notify("Цель выбрана, продолжаем атаку")
            #$ renpy.pause(3.0, hard=False)
            #$ renpy.notify(f"Цель: {target.name}, HP до атаки: {target.current_hp}")
            
            # Обновляем значение base_perform на основе текущей позиции

            $ store.base_perform = calculate_kris_atk1_perform(kris_atk1_stick_xpos)
                
            #$ renpy.notify(f"Обновленный base_perform: {store.base_perform}")
            #$ renpy.pause(3.0, hard=False)

            # Рассчитываем урон по выбранной цели
            $ target_hp_before = target.current_hp
            $ damage = store.pers_dict["Крис"].calculate_dmg(target, apply_shield=True)
            $ dmg = damage



            



            #$ renpy.notify(f"Рассчитанный урон: {damage}")
            #$ renpy.pause(3.0, hard=False)
            #$ renpy.notify(f"popal после расчета: {store.pers_dict[current_attacker].popal}")
            #$ renpy.pause(3.0, hard=False)
            #$ renpy.notify(f"store.is_crit после расчета: {store.is_crit}")
            #$ renpy.pause(3.0, hard=False)
            #$ renpy.notify(f"target.damage_gain_for_vis: {target.damage_gain_for_vis}")
            #$ renpy.pause(3.0, hard=False)
            #$ renpy.notify(f"target.got_crit_for_visual: {target.got_crit_for_visual}")
            #$ renpy.pause(3.0, hard=False)

            # Проверяем детали расчета урона
            #$ renpy.notify(f"Броня цели: {target.armor}")
            #$ renpy.pause(3.0, hard=False)

            #if store.is_crit:
            #    $ renpy.notify(f"Расчет КРИТИЧЕСКОГО урона: ({store.pers_dict['Крис'].atk} * {store.pers_dict['Крис'].crit} * {store.pers_dict['Крис'].perform} * {store.atk_ind_ratio} - {target.armor}) * {store.popal}")
            #else:
            #    $ renpy.notify(f"Расчет ОБЫЧНОГО урона: ({store.pers_dict['Крис'].atk} * {store.pers_dict['Крис'].perform} * {store.atk_ind_ratio} - {target.armor}) * {store.popal}")
            #$ renpy.pause(3.0, hard=False)

           
            #$ renpy.notify(f"HP цели изменен с {old_hp} на {target.current_hp}")
            #$ renpy.pause(3.0, hard=False)
            #$ renpy.notify(f"Фактический урон (max(0, old_hp - damage)): {max(0, old_hp - damage)}")
            #$ renpy.pause(3.0, hard=False)
            
            #"Крис нанес [damage] урона!"
            #"Оставшееся HP: [target.current_hp]"
        else:
            #$ renpy.log("ОШИБКА: Цель не выбрана (target is None)")
            # Если цель не выбрана, просто завершаем ход без нанесения урона и эффектов
            
            $ store.pers_dict["Крис"].popal = 0
            if target is not None:
                $ target.damage_gain_for_vis = 0
                $ store.clear_swoon_pending_for_visual(target)
            
            #"Цель не выбрана! Урон равен 0."
    elif kris1_atk_pressed == 0:
        if target is not None:
            $ target.damage_gain_for_vis = -1
            $ store.clear_swoon_pending_for_visual(target)
        pass

    hide screen Heroattacks

    $ renpy.pause(0.2, hard=False)

    if dmg > 0 and store.pers_dict["Крис"].popal == 1:

        if is_crit:
            with vpunch
            with vpunch
        else:
            pass
        
    #$ sub_effect= 4
    #$ store.upal = 1
    if store.upal == 1:
        $ store.pers_dict["Крис"].debuff("prone", +1)
        $ store.upal = 0
    # Показываем результаты
    show screen attacked_compiled_heroturn
   
   
    $ renpy.pause(2.5, hard=False)
    
    #$ renpy.pause (3, hard=True)
    #show screen heroes_attacked_visual
 
    









    # Возвращение к базе и индивидуальная пауза
    $ base_perform = 0
    $ stick_xpos = 1400

    
    $ store.pers_dict["Крис"].step_forward = 2
    
    
    $ store.is_crit = None
    $ store.pers_dict["Крис"].state = "idle"
    hide screen targettochoose_sprites_effect_universal
    hide screen attacked_compiled_heroturn
    
    
    
    $ renpy.pause (0.4, hard=True)
    call set_buttons_to_default
    call screen choose_attacker_screen()


default upal = 0



















transform strong_hpunch:
    xalign 0.5
    yalign 0.5
    xoffset 0

    linear 0.045 xoffset 60 #zoom 1.02
    linear 0.045 xoffset -60
    linear 0.045 xoffset 50
    linear 0.045 xoffset -50
    linear 0.045 xoffset 40
    linear 0.045 xoffset -40
    linear 0.045 xoffset 30
    linear 0.045 xoffset -30
    linear 0.045 xoffset 20
    linear 0.045 xoffset -20
    linear 0.045 xoffset 10
    linear 0.045 xoffset -10
    linear 0.045 xoffset 0 #zoom 1.0










label kris_atk2_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    if store.base_perform > 0:
        $ prepare_turn_effect_target(target)
        $ store.pers_dict["Крис"].state = "fight2"
        show screen targettochoose_sprites_effect_universal
    
    hide screen Heroattacks
    
    $ renpy.pause(0.6, hard=True)

    if target is not None:
        # Сохраняем оригинальные значения
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        $ original_crit = store.pers_dict["Крис"].bonus_crit
        
        # 1. Проверка perform > 0.9
        $ is_perfect_perform = store.pers_dict["Крис"].perform >= 1.0
        
        # 2. Проверка на попадание (как в calculate_dmg)
        $ hit_prob = min(store.pers_dict["Крис"].dmgchance, 1.0)
        $ hit_roll = renpy.random.random()
        
        # Совпадает с логикой calculate_dmg(): при попадании roll должен быть <= hit_prob.
        if hit_roll > hit_prob:
            $ store.pers_dict["Крис"].popal = 0
            $ dmg = 0
            $ store.is_crit = False
            $ target.damage_gain_for_vis = 0
            $ target.got_crit_for_visual = 0
            $ store.clear_swoon_pending_for_visual(target)
        else:
            $ store.pers_dict["Крис"].popal = 1
            
            # 3. Если попадание И perform > 0.9, применяем бонусы
            if is_perfect_perform:
                # +3% Крит. шанс (при идеальной атаке)
                $ store.pers_dict["Крис"].bonus_critrate += 0.03
                # +6% Крит урон (при идеальной атаке)
                $ store.pers_dict["Крис"].bonus_crit += 0.06
            
            # 4. Определение критического удара (как в calculate_dmg)
            $ crit_roll = renpy.random.random()
            $ store.is_crit = crit_roll < store.pers_dict["Крис"].critrate
            
            # 5. Расчет базового урона (как в calculate_dmg)
            if is_crit:
                $ base_dmg = (store.pers_dict["Крис"].atk * store.pers_dict["Крис"].crit * store.pers_dict["Крис"].perform * store.atk_ind_ratio - target.armor) * store.pers_dict["Крис"].popal
            else:
                $ base_dmg = (store.pers_dict["Крис"].atk * store.pers_dict["Крис"].perform * store.atk_ind_ratio - target.armor) * store.pers_dict["Крис"].popal
            
            # Применение прогрессивных штрафов
            $ final_dmg = store.pers_dict["Крис"].calculate_progressive(base_dmg, store.pers_dict["Крис"].DAMAGE_THRESHOLDS)
            $ dmg = int(max(min(final_dmg, 600), 0))
            
            # 6. Применяем урон
            $ target.current_hp = max(0, target.current_hp - dmg)
            $ target.damage_gain_for_vis = dmg
            $ target.got_crit_for_visual = int(is_crit)

            
            # Если не идеальная атака, восстанавливаем оригинальные значения
            if not is_perfect_perform:
                $ store.pers_dict["Крис"].bonus_critrate = original_critrate
                $ store.pers_dict["Крис"].bonus_crit = original_crit
        
            # 10% Шанс вызвать кровотечение на 3 хода
            if renpy.random.randint(1, 100) <= 10:
                $ apply_enemy_bleeding(target, 2)
        
            # Добавляем результат атаки
            if dmg > 0 and store.pers_dict["Крис"].popal == 1:
                $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            
            # Визуальные эффекты
            if dmg > 0 and store.pers_dict["Крис"].popal == 1:
                if is_crit:
                    hide screen Heroattacks
                    camera screens at strong_hpunch
                    $ renpy.pause(0.2, hard=True)
                    #with crit_vpunch
                    #$ renpy.pause(1.0, hard=False)
                else:
                    hide screen Heroattacks
                    #with vpunch
                    #$ renpy.pause(1.0, hard=False)
    
            if is_perfect_perform:
                # +3% Крит. шанс (при идеальной атаке)
                $ store.pers_dict["Крис"].bonus_critrate -= 0.03
                # +6% Крит урон (при идеальной атаке)
                $ store.pers_dict["Крис"].bonus_crit -= 0.06
    show screen attacked_compiled_heroturn
    $ renpy.pause(1, hard=True)
    if store.base_perform > 0:
        $ store.pers_dict["Крис"].state = "fight2_2"
    $ renpy.pause(1, hard=True)
    $ store.base_perform = 0

    $ store.pers_dict["Крис"].step_forward = 2 
    $ store.is_crit = None
    $ store.pers_dict["Крис"].state = "idle"
    hide screen targettochoose_sprites_effect_universal
    hide screen attacked_compiled_heroturn
    
    
    

    
    $ renpy.pause (0.4, hard=True)
    call set_buttons_to_default
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 3: Удар щитом
# ========================================================================
label kris_atk3_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    if store.base_perform > 0:
        $ prepare_turn_effect_target(target)
        $ store.pers_dict["Крис"].state = "fight3"
        show screen targettochoose_sprites_effect_universal

    hide screen Heroattacks

    

    if target is not None:
        # Сохраняем оригинальные значения
        $ original_dmgchance = store.pers_dict["Крис"].bonus_dmgchance
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        
        # +15% Шанс попасть
        $ store.pers_dict["Крис"].bonus_dmgchance += 0.15
        # Удар щитом не критует.
        $ store.pers_dict["Крис"].bonus_critrate = -store.pers_dict["Крис"].base_critrate
        
        # Рассчитываем урон
        #$ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ dmg = store.pers_dict["Крис"].calculate_dmg_from_def(target)

        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(bool(store.is_crit))
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Крис"].bonus_dmgchance = original_dmgchance
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        
        # 20% шанс повалить противника (prone_debuff) и 20% замедлить его на 10%
        if renpy.random.randint(1, 100) <= 20:
            $ target.debuff("prone", 1)
        if renpy.random.randint(1, 100) <= 20:
            $ apply_enemy_slow(target, 0.10)
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            #$ store.is_crit = False  # Удар не критует
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            #with vpunch

    $ renpy.pause(2.0, hard=True)
    show screen attacked_compiled_heroturn
    $ renpy.pause(2.0, hard=True)
    if store.base_perform > 0:
        $ store.pers_dict["Крис"].state = "fight3_2"
    $ renpy.pause(0.9, hard=True)
    $ store.pers_dict["Крис"].state = "idle"
    $ renpy.pause(0.5, hard=True)
    $ store.base_perform = 0
    $ store.pers_dict["Крис"].step_forward = 2
    $ store.is_crit = None
    hide screen targettochoose_sprites_effect_universal
    hide screen attacked_compiled_heroturn

    

    $ renpy.pause(0.4, hard=True)
    call set_buttons_to_default
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 4: С Разворота!
# ========================================================================
label kris_atk4_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "fight4"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_perform = store.pers_dict["Крис"].bonus_perform
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        $ original_crit = store.pers_dict["Крис"].bonus_crit
        
        # Дополнительный урон: 130%, с «Привычкой к вращению» ур.6 — 150%.
        python:
            _kris_spin = store.pers_dict["Крис"]
            _spin_mastered = kris_passive_level() >= KRIS_SPIN_LEVEL
            _kris_spin.bonus_perform *= (KRIS_SPIN_DAMAGE_MASTERED if _spin_mastered
                                         else KRIS_SPIN_DAMAGE)
        # 10% Крит. шанс
        $ store.pers_dict["Крис"].bonus_critrate += 0.10
        # 10% Крит. урон
        $ store.pers_dict["Крис"].bonus_crit += 0.10
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Крис"].bonus_perform = original_perform
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        $ store.pers_dict["Крис"].bonus_crit = original_crit
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            $ store.is_crit = store.pers_dict["Крис"].crit > 1.0
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
        
        # «Привычка к вращению» ур.6: 30% шанс задеть остальных врагов
        # половиной нанесённого урона.
        if _spin_mastered and dmg > 0:
            python:
                if renpy.random.randint(1, 100) <= int(KRIS_SPIN_SPLASH_CHANCE * 100):
                    _splash = int(dmg * KRIS_SPIN_SPLASH_RATIO)
                    for _enemy_name in get_active_enemies():
                        _enemy = store.enemies.get(_enemy_name)
                        if _enemy is None or _enemy is target or _enemy.current_hp <= 0:
                            continue
                        _enemy.current_hp = max(0, _enemy.current_hp - _splash)
                        _enemy.damage_gain_for_vis = _splash
                        add_attack_result(store.pers_dict["Крис"].name, _enemy.name,
                                          _splash, False, "normal")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 5: Бонк!
# ========================================================================
label kris_atk5_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "fight5"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_dmgchance = store.pers_dict["Крис"].bonus_dmgchance
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        
        # +15% шанс попасть
        $ store.pers_dict["Крис"].bonus_dmgchance += 0.15
        # Удар не критует
        $ store.pers_dict["Крис"].bonus_critrate = -store.pers_dict["Крис"].base_critrate
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Крис"].bonus_dmgchance = original_dmgchance
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        
        # Бонк: 25% ослабить атаку на 10%, 15% истощение (х2)
        if renpy.random.randint(1, 100) <= 25:
            $ apply_enemy_weaken_attack(target, 0.10)
        if renpy.random.randint(1, 100) <= 15:
            $ apply_enemy_atk_debuff(target, 2)
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            $ store.is_crit = False  # Удар не критует
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 6: Пронзить
# ========================================================================
label kris_atk6_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "fight6"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_dmgchance = store.pers_dict["Крис"].bonus_dmgchance
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        $ original_crit = store.pers_dict["Крис"].bonus_crit
        
        # +20% шанс попадания
        $ store.pers_dict["Крис"].bonus_dmgchance += 0.20
        # -15% Крит. урон
        $ store.pers_dict["Крис"].bonus_crit -= 0.15
        # -15% Крит. шанс
        $ store.pers_dict["Крис"].bonus_critrate -= 0.15
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Крис"].bonus_dmgchance = original_dmgchance
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        $ store.pers_dict["Крис"].bonus_crit = original_crit
        
        # 80% шанс кровотечения: «х2» — это +2 к дебаффу кровотечения врага
        if renpy.random.randint(1, 100) <= 80:
            $ apply_enemy_bleeding(target, 2)
        
        # 20% снизить бонусную броню цели на 20%
        if renpy.random.randint(1, 100) <= 20:
            $ target.bonus_def = max(0.0, float(getattr(target, "bonus_def", 0.0)) * 0.8)
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            $ store.is_crit = store.pers_dict["Крис"].crit > 1.0
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 7: Отбить руки
# ========================================================================
label kris_atk7_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "fight7"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_dmgchance = store.pers_dict["Крис"].bonus_dmgchance
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        
        # Удар не критует
        $ store.pers_dict["Крис"].bonus_critrate = -store.pers_dict["Крис"].base_critrate
        # +15% шанс попасть
        $ store.pers_dict["Крис"].bonus_dmgchance += 0.15
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Крис"].bonus_dmgchance = original_dmgchance
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        
        # 30% Ослабить атаку врага
        if renpy.random.randint(1, 100) <= 30:
            $ apply_enemy_weaken_attack(target, 0.3)
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            $ store.is_crit = False  # Удар не критует
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 10: Отчаянное комбо
# ========================================================================
label kris_atk10_combo_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "fight10"
    
    hide screen Heroattacks
    
    if target is not None:
        # -20% Your hp
        $ hp_loss = int(store.pers_dict["Крис"].max_hp * 0.20)
        $ store.pers_dict["Крис"].current_hp = max(1, store.pers_dict["Крис"].current_hp - hp_loss)
        
        # -20% Your armor (defense)
        $ original_def = store.pers_dict["Крис"].bonus_def
        $ store.pers_dict["Крис"].bonus_def *= 0.8
        
        # Сохраняем оригинальные значения
        $ original_armor = target.armor
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        $ original_crit = store.pers_dict["Крис"].bonus_crit
        
        # Ignores enemy's armor - временно устанавливаем броню врага в 0
        $ target.armor = 0
        # +30% Crit rate
        $ store.pers_dict["Крис"].bonus_critrate += 0.30
        # +30% crit damage
        $ store.pers_dict["Крис"].bonus_crit += 0.30
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ target.armor = original_armor
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        $ store.pers_dict["Крис"].bonus_crit = original_crit
        $ store.pers_dict["Крис"].bonus_def = original_def
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            $ store.is_crit = store.pers_dict["Крис"].crit > 1.0
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# АТАКА КРИСА 11: Рывок защитника
# ========================================================================
label kris_atk11_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "fight11"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_def = store.pers_dict["Крис"].bonus_def
        $ original_critrate = store.pers_dict["Крис"].bonus_critrate
        $ original_tank = store.pers_dict["Крис"].bonus_tank
        
        # Танк Криса +2. Щит даётся с шансом, равным магии Криса.
        $ store.pers_dict["Крис"].bonus_tank += 2
        $ _kris_shield_roll = renpy.random.randint(1, 100)
        if _kris_shield_roll <= int(store.pers_dict["Крис"].magic):
            $ store.pers_dict["Крис"].shield += 1
        # Удар не критует
        $ store.pers_dict["Крис"].bonus_critrate = -store.pers_dict["Крис"].base_critrate
        # Рассчитываем урон
        $ dmg = store.pers_dict["Крис"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения (кроме tank, он остается увеличенным)
        $ store.pers_dict["Крис"].bonus_def = original_def
        $ store.pers_dict["Крис"].bonus_critrate = original_critrate
        
        if dmg > 0 and store.pers_dict["Крис"].popal == 1:
            $ store.is_crit = False  # Удар не критует
            $ add_attack_result(store.pers_dict["Крис"].name, target.name, dmg, is_crit, "normal")
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# МАГИЯ КРИСА
# ========================================================================

label kris_mag1_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic1"
    
    hide screen Heroattacks
    

    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    #hide screen heroes_attacked_visual
    # Призвать меч - позволяет использовать атаки мечом
    $ store.summoned = 1
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    $ store.pers_dict["Крис"].sprite_style = "down"
    $ store.pers_dict["Крис"].step_forward = 2
    # turn уже выставлен «Причиной ошибок» в начале лейбла.

    call screen choose_attacker_screen()

label kris_mag2_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic2"
    
    #hide screen Heroattacks
    
    
    #show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    #hide screen heroes_attacked_visual

    $ store.summoned = 2
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    $ store.pers_dict["Крис"].sprite_style = "down"
    $ store.pers_dict["Крис"].step_forward = 2
    # turn уже выставлен «Причиной ошибок» в начале лейбла.
    
    call screen choose_attacker_screen()

label kris_mag3_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic3"
    
    hide screen Heroattacks
    
    # Напрячься: +30% атаки. «Направить фокус» ур.3 даёт 20% шанс двойного
    # бонуса, но списывает ещё столько же маны (итого вдвое больше).
    python:
        _kris_focus = store.pers_dict["Крис"]
        _focus_double = (kris_passive_level() >= KRIS_FOCUS_LEVEL
                         and renpy.random.random() < KRIS_FOCUS_CHANCE)
        _kris_focus.bonus_atk += KRIS_FOCUS_BONUS * (2 if _focus_double else 1)
        if _focus_double:
            _focus_extra_mp = get_ability_resource_cost("Напрячься", _kris_focus).get("mp", 0)
            _kris_focus.current_mp = max(0, _kris_focus.current_mp - _focus_extra_mp)
            renpy.notify("Направить фокус: двойной бонус, мана x2")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    $ store.pers_dict["Крис"].step_forward = 2
    # turn уже выставлен «Причиной ошибок» в начале лейбла.
    call screen choose_attacker_screen()

label kris_mag4_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic4"
    
    hide screen Heroattacks
    
    # Позвать за щит: выбранный союзник получает 30% защиты Криса и
    # связывается с ним. Попадание по одному из них наносит урон обоим.
    python:
        kris = store.pers_dict["Крис"]
        ally = target
        # Снимаем прежнюю связь — и у Криса, и у его бывшего партнёра.
        clear_kris_shield_link(kris)

        if ally is not None and ally is not kris and getattr(ally, "is_ally", False) and ally.current_hp > 0:
            kris.kris_shield_partner = ally
            ally.kris_shield_partner = kris
            # Отдельный атрибут класса Pers, входит в итоговую defense.
            ally.kris_shield_def_bonus = kris.defense * 0.3
            # «Удачные прятки» ур.4: союзник дополнительно получает 1 щит.
            if kris_passive_level() >= KRIS_ALLY_SHIELD_LEVEL:
                ally.shield = getattr(ally, "shield", 0) + 1
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag5_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic5"
    
    hide screen Heroattacks
    
    # Правильный угол: даёт бафф «Правильный угол» x1. Проверка уворота живёт
    # в функции нанесения урона по персонажу (kris_try_right_angle_dodge).
    $ kris_grant_right_angle()
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag6_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic6"
    
    hide screen Heroattacks
    
    # Слабое место: следующий удар бьёт сильнее.
    #   ур.4–7 — 180% урона (нужно 3 действия);
    #   ур.8+  — «Гибкое терпение»: доступно после 1 действия и даёт +50%
    #            урона за каждое накопленное действие.
    python:
        _kris_weak = store.pers_dict["Крис"]
        _weak_actions = int(getattr(store, "actions_count_snapshot", 0) or 0)
        if kris_passive_level() >= KRIS_FLEXIBLE_PATIENCE_LEVEL:
            _kris_weak.next_attack_multiplier = (1.0 + KRIS_FLEXIBLE_PATIENCE_STEP
                                                 * max(1, _weak_actions))
        else:
            _kris_weak.next_attack_multiplier = 1.8
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag7_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic7"
    
    hide screen Heroattacks
    
    # Концентрация: +10% бонусной точности и -3 к дебаффу точности
    # (отрицательный дебафф даёт прибавку через accuracy_debuff_var).
    $ store.pers_dict["Крис"].bonus_dmgchance += 0.1
    $ store.pers_dict["Крис"].debuff("accuracy", -3)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag8_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic8"
    
    hide screen Heroattacks
    
    # Поднять щиты! - +20% защиты всем союзникам
    python:
        for char_name in store.characters:
            if store.pers_dict[char_name].is_ally and store.pers_dict[char_name].current_hp > 0:
                original_def = store.pers_dict[char_name].bonus_def
                store.pers_dict[char_name].bonus_def *= 1.2
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag9_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic9"
    
    hide screen Heroattacks
    
    # Стремление вперёд - лечит Криса на 8% от текущей маны
    $ heal_amount = int(store.pers_dict["Крис"].current_mp * 8)
    $ store.pers_dict["Крис"].current_hp = min(store.pers_dict["Крис"].max_hp, store.pers_dict["Крис"].current_hp + heal_amount)
    $ store.pers_dict["Крис"].current_mp = 0
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag10_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic10"
    
    hide screen Heroattacks
    
    # Рывок защитника - +30% защиты всем союзникам
    $ original_def = store.pers_dict["Крис"].bonus_def
    $ original_tank = store.pers_dict["Крис"].bonus_tank
    $ store.pers_dict["Крис"].bonus_def *= 1.3
    $ store.pers_dict["Крис"].bonus_tank += store.pers_dict["Крис"].base_tank * 2
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label kris_mag11_is_done:
    # «Причина ошибок»: бросок на дополнительный ход.
    $ kris_prepare_action_turn()
    $ store.pers_dict["Крис"].state = "magic11"
    
    hide screen Heroattacks
    
    # Пробудиться (геноцид) - +50% к крит.шансу и крит.урону, одноразовая
    $ original_critrate = store.pers_dict["Крис"].bonus_critrate
    $ original_crit = store.pers_dict["Крис"].bonus_crit
    $ store.pers_dict["Крис"].bonus_critrate += 0.5
    $ store.pers_dict["Крис"].bonus_crit += 0.5
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Крис"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# МАГИЯ АЗРИ
# ========================================================================

label asri_form_is_done:
    # «Сменить облик»: не тратит ход и ману, только переключает облик.
    $ store.pers_dict["Азриель"].state = "magic1"
    $ renpy.pause(0.6, hard=False)
    $ renpy.notify("Облик: " + azri_form_name())
    $ toggled_form = azri_toggle_form()
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0

    call screen choose_attacker_screen()

label asri_mag1_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic1"
    
    hide screen Heroattacks
    
    # Шаг вперёд: танк +3 (с «2 шага вперёд» ур.2 — вдвое больше),
    # поэтому враги чаще выбирают Азриеля целью.
    python:
        _azri = store.pers_dict["Азриель"]
        azri_bonus_tank_add(_azri, azri_step_forward_tank())
        # «2 шага вперёд»: откат вдвое больше.
        _azri_step_cd = 2
        if azri_level() >= AZRI_TWO_STEPS_LEVEL:
            _azri_step_cd = AZRI_STEP_FORWARD_COOLDOWN_MASTERED
        set_battle_ability_current_cd("Шаг вперёд", _azri_step_cd)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag2_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic2"
    
    hide screen Heroattacks
    
    # Магия огня: призывает пляшущие огоньки, урон всем противникам.
    python:
        _azri = store.pers_dict["Азриель"]
        store.azri_firefly_active = True
        for _enemy_name in get_active_enemies():
            _enemy = store.enemies.get(_enemy_name)
            if _enemy is None or _enemy.current_hp <= 0:
                continue
            _dmg = int(_azri.magic * 0.8 - _enemy.armor * 0.5)
            _dmg = max(0, _dmg)
            _enemy.current_hp = max(0, _enemy.current_hp - _dmg)
            _enemy.damage_gain_for_vis = _dmg
            if _dmg > 0:
                add_attack_result(_azri.name, _enemy.name, _dmg, False, "magic")
                azri_fire_on_damage(_enemy, _dmg, from_fireflies=True)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag3_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic3"
    
    hide screen Heroattacks
    
    # Горное равновесие: +20% атаки, +30% защиты, +20% магии, +15% точности.
    # Бонусы аддитивные — базовые значения bonus_* в проекте нулевые.
    python:
        _azri = store.pers_dict["Азриель"]
        _azri.bonus_atk += 0.20
        azri_bonus_def_add(_azri, 0.30)
        _azri.bonus_magic += 0.20
        _azri.bonus_dmgchance += 0.15
        renpy.notify("Горное равновесие: +20% атаки, +30% защиты, +20% магии, +15% точности")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag4_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic4"
    
    hide screen Heroattacks
    
    # Клинки хаоса: рубят цель сейчас, огоньки добивают на ходу противника.
    python:
        _azri = store.pers_dict["Азриель"]
        store.azri_firefly_active = True
        store.azri_blades_pending = True
        if target is not None and target.current_hp > 0:
            _dmg = max(0, int(_azri.magic * 0.6 - target.armor * 0.3))
            target.current_hp = max(0, target.current_hp - _dmg)
            target.damage_gain_for_vis = _dmg
            if _dmg > 0:
                add_attack_result(_azri.name, target.name, _dmg, False, "magic")
                azri_fire_on_damage(target, _dmg, from_fireflies=True)
                # «Хаос в огне» ур.6: клинки провоцируют инфузию и перегрев.
                azri_chaos_in_fire(target, _dmg)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag5_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic5"
    
    hide screen Heroattacks
    
    # За спиною принца: бонусная защита Азриеля уходит выбранному союзнику.
    $ azri_apply_back_of_prince(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag6_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic6"
    
    hide screen Heroattacks
    
    # Уничтожитель хаоса: волны пуль по всем врагам, затем заряженный луч
    # по цели. «Плавящий луч» ур.7 может снять 20% брони цели.
    python:
        _azri = store.pers_dict["Азриель"]
        for _enemy_name in get_active_enemies():
            _enemy = store.enemies.get(_enemy_name)
            if _enemy is None or _enemy.current_hp <= 0:
                continue
            for _wave in range(10):
                _dmg = max(0, int(_azri.magic * 0.3 - _enemy.armor * 0.2))
                _enemy.current_hp = max(0, _enemy.current_hp - _dmg)
                if _dmg > 0:
                    add_attack_result(_azri.name, _enemy.name, _dmg, False, "magic")
            _enemy.damage_gain_for_vis = _dmg
            azri_fire_on_damage(_enemy, _dmg, from_fireflies=True)
        if target is not None:
            azri_melt_beam(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag7_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic7"
    
    hide screen Heroattacks
    
    # Встать с колен - восстанавливает 200 хп и мп в % от отсутствующих хп
    $ store.pers_dict["Азриель"].current_hp = min(store.pers_dict["Азриель"].max_hp, store.pers_dict["Азриель"].current_hp + 200)
    $ missing_hp = store.pers_dict["Азриель"].max_hp - store.pers_dict["Азриель"].current_hp
    $ mp_restore = int(missing_hp * 0.5)
    $ store.pers_dict["Азриель"].current_mp = min(store.pers_dict["Азриель"].max_mp, store.pers_dict["Азриель"].current_mp + mp_restore)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag8_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic8"
    
    hide screen Heroattacks
    
    # Звёздный блеск: 5 волн по всем врагам, последняя — огромная звезда.
    # «Осколки звёзд» ур.9: малые звёзды задевают остальных врагов.
    python:
        _azri = store.pers_dict["Азриель"]
        for _enemy_name in get_active_enemies():
            _enemy = store.enemies.get(_enemy_name)
            if _enemy is None or _enemy.current_hp <= 0:
                continue
            for _wave in range(5):
                _mult = 2.0 if _wave == 4 else 1.0
                _dmg = max(0, int((_azri.magic * 0.8 - _enemy.armor * 0.5) * _mult))
                _enemy.current_hp = max(0, _enemy.current_hp - _dmg)
                _enemy.damage_gain_for_vis = _dmg
                if _dmg > 0:
                    add_attack_result(_azri.name, _enemy.name, _dmg, _wave == 4, "magic")
                    if _wave < 4:
                        azri_star_shards(_enemy, _dmg)
            azri_fire_on_damage(_enemy, _dmg, from_fireflies=True)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag9_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic9"
    
    hide screen Heroattacks
    
    # Боевой клич!: +20 защиты всем в отряде и лечение 200 HP.
    python:
        for _ally in (getattr(store, "pers_dict", {}) or {}).values():
            if not getattr(_ally, "is_ally", False) or getattr(_ally, "picked", 0) != 1:
                continue
            if getattr(_ally, "current_hp", 0) <= 0:
                continue
            _ally.base_def_mod = float(getattr(_ally, "base_def_mod", 0.0)) + 20
            _ally.current_hp = min(getattr(_ally, "max_hp", 0), _ally.current_hp + 200)
            _ally.damage_gain_for_vis = -200
        renpy.notify("Боевой клич!: +20 защиты и 200 HP всей команде")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_mag10_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "magic10"
    
    hide screen Heroattacks
    
    # Луч Бога Гиперсмерти: всю ману и 50% HP уже списала оплата способности.
    # Луч бьёт по всем врагам и обнуляет баффы/дебаффы характеристик,
    # накопленные за бой.
    python:
        _azri = store.pers_dict["Азриель"]
        for _enemy_name in get_active_enemies():
            _enemy = store.enemies.get(_enemy_name)
            if _enemy is None or _enemy.current_hp <= 0:
                continue
            _dmg = max(0, int(_azri.magic * 1.5 - _enemy.armor * 0.1))
            _enemy.current_hp = max(0, _enemy.current_hp - _dmg)
            _enemy.damage_gain_for_vis = _dmg
            if _dmg > 0:
                add_attack_result(_azri.name, _enemy.name, _dmg, True, "magic")
            # Обнуляем боевые баффы и дебаффы врага.
            _enemy.bonus_atk = 0.0
            _enemy.bonus_def = 0.0
            _enemy.atk_debuff_var = 1.0
            _enemy.def_debuff_var = 1.0
            _enemy.magic_debuff_var = 1.0
            for _attr in AZRI_CLEANSE_ATTRS:
                if hasattr(_enemy, _attr):
                    setattr(_enemy, _attr, 0)
        # И собственные боевые накопления Азриеля.
        _azri.bonus_atk = 0.0
        _azri.bonus_magic = 0.0
        _azri.bonus_def = 0.0
        _azri.bonus_tank = 0.0
        _azri.bonus_dmgchance = 0.0
        _azri.bonus_crit = 0.0
        _azri.bonus_critrate = 0.0
        azri_cleanse_char(_azri, len(AZRI_CLEANSE_ATTRS))
        store.azri_defense_added = 0.0
        store.azri_tank_added = 0.0
        _azri.azri_def_bonus = 0.0
        renpy.notify("Луч Бога Гиперсмерти: все баффы и дебаффы обнулены")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# МАГИЯ ЧАРЫ
# ========================================================================

label chara_mag_is_done_glava_1:
    $ prepare_turn_effect_target(target)
    $ store.pers_dict["Чара"].turn = 1
    if attackindex == "Гнев":
        $ store.pers_dict["Чара"].state = "magic1"
        $ store.pers_dict["Чара"].bonus_atk += 0.20
    elif attackindex == "Безумие":
        $ store.pers_dict["Чара"].state = "magic2"
        $ store.pers_dict["Чара"].bonus_crit +=0.2


    #$ store.pers_dict["Чара"].current_mp = 30
    #show screen heroes_attacked_visual
    
    hide screen Heroattacks
    if attackindex == "Гнев":
        $ renpy.pause(3.0, hard=True)
    elif attackindex == "Безумие":
        $ renpy.pause(2.9, hard=True)


    #hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    $ store.pers_dict["Чара"].step_forward = 2
    call screen choose_attacker_screen()



label chara_mag2_is_done:
    $ store.pers_dict["Чара"].turn = 1
    $ store.pers_dict["Чара"].state = "magic2"
    
    hide screen Heroattacks
    
    # Безумие - увеличить шанс крита на 20%
    $ original_critrate = store.pers_dict["Чара"].bonus_critrate
    $ store.pers_dict["Чара"].bonus_critrate += 0.2
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label chara_mag3_is_done:
    $ store.pers_dict["Чара"].turn = 1
    $ store.pers_dict["Чара"].state = "magic3"
    
    hide screen Heroattacks
    
    # Сумасшествие - увеличить крит урон на 30%
    $ original_crit = store.pers_dict["Чара"].bonus_crit
    $ store.pers_dict["Чара"].bonus_crit += 0.30
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label chara_mag4_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "magic4"
    
    hide screen Heroattacks
    
    # Псих — следующая атака получает +100% урона.
    $ store.pers_dict["Чара"].next_attack_damage_multiplier += 1.0
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label chara_mag5_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "magic5"
    
    hide screen Heroattacks
    
    # Моральное разложение - броня игнорируется в следующей атаке
    $ store.pers_dict["Чара"].next_ignore_armor = True
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label chara_mag6_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "magic6"
    
    hide screen Heroattacks
    
    # Пробуждение прошлого — один удар ножом с +300% критического шанса и смертью Чары.
    $ original_critrate = store.pers_dict["Чара"].bonus_critrate
    $ store.pers_dict["Чара"].bonus_critrate += 3.0
    
    if target is not None and target.current_hp > 0:
        $ store.pers_dict["Чара"].next_ignore_armor = True
        $ _chara_attack_bonus_before = store.pers_dict["Чара"].bonus_atk
        $ chara_prepare_next_attack(store.pers_dict["Чара"])
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ store.pers_dict["Чара"].bonus_atk = _chara_attack_bonus_before
        $ target.damage_gain_for_vis = dmg
        $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, True, "normal")
    
    # Чара умирает после этой атаки
    $ store.pers_dict["Чара"].current_hp = 0
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# МАГИЯ ФРИСКА
# ========================================================================

label frisk_mag1_is_done:
    $ store.pers_dict["Фриск"].turn = 0
    $ store.pers_dict["Фриск"].state = "magic1"
    
    hide screen Heroattacks
    
    # Potentia intellectus - снижает атаку на 5% себе и противнику
    $ original_atk = store.pers_dict["Фриск"].bonus_atk
    $ store.pers_dict["Фриск"].bonus_atk *= 0.95
    
    if target is not None:
        $ target.bonus_atk *= 0.95
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Фриск"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label frisk_mag2_is_done:
    $ store.pers_dict["Фриск"].turn = 0
    $ store.pers_dict["Фриск"].state = "magic2"
    
    hide screen Heroattacks
    
    # Quod licet Iovi, non licet bovi - снижает броню противнику на 5% и увеличивает броню и урон себе на 5%
    $ original_def = store.pers_dict["Фриск"].bonus_def
    $ original_atk = store.pers_dict["Фриск"].bonus_atk
    $ store.pers_dict["Фриск"].bonus_def *= 1.05
    $ store.pers_dict["Фриск"].bonus_atk *= 1.05
    
    if target is not None:
        $ target.bonus_def *= 0.95
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Фриск"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label frisk_mag3_is_done:
    $ store.pers_dict["Фриск"].turn = 0
    $ store.pers_dict["Фриск"].state = "magic3"
    
    hide screen Heroattacks
    
    # Foedus icere - увеличивает степень договорённости до максимума, если договор с противником достиг 50%+
    # Эта магия требует выбора цели
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Фриск"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label frisk_mag4_is_done:
    $ store.pers_dict["Фриск"].turn = 0
    $ store.pers_dict["Фриск"].state = "magic4"
    
    hide screen Heroattacks
    
    # Do ut des - хилит противника на 200 хп, но хилит всю команду на 400 хп
    if target is not None:
        $ target.current_hp = min(target.max_hp, target.current_hp + 200)
    
    python:
        for char_name in store.characters:
            if store.pers_dict[char_name].is_ally and store.pers_dict[char_name].current_hp > 0:
                store.pers_dict[char_name].current_hp = min(store.pers_dict[char_name].max_hp, store.pers_dict[char_name].current_hp + 400)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Фриск"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label frisk_mag5_is_done:
    $ store.pers_dict["Фриск"].turn = 0
    $ store.pers_dict["Фриск"].state = "magic5"
    
    hide screen Heroattacks
    
    # Сохранение решимости - если кто-то из людей умер, Фриск восстанавливает ему 150% от его здоровья
    # Эта магия требует выбора цели
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Фриск"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# МАГИЯ КЛОВЕРА
# ========================================================================

label clover_mag1_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Выбор калибра» ур.1: Кловер выбирает малый, средний или большой тип
    # патронов. Малый с шансом 50% крит-шанса вызывает кровотечение.
    # Большой снижает броню на 5% с шансом крит-шанса и/или навешивает
    # 2 стака слабости. Смена калибра перезаряжает обойму.
    # ========================================================================
    $ clover_set_caliber("small")
    
    if target is not None:
        $ clover_obj = store.pers_dict["Кловер"]
        # Малый калибр: кровотечение с шансом 50% крит-шанса.
        if renpy.random.random() < float(getattr(clover_obj, "critrate", 0)) * 0.5:
            $ apply_enemy_bleeding(target, 2)
            $ renpy.log("[Кловер][Калибр] малый: {} получает кровотечение".format(target.name))
    
    $ renpy.notify("Кловер: малый калибр (урон x0.75, %d патронов)" % store.clover_ammo_max)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag2_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Сыграем!» ур.1: Кловер обязан поставить ставку в виде своих бонусных
    # характеристик. Реализация игр — в экране clover_gamble_screen.
    # ========================================================================
    $ clover_result = renpy.call_screen("clover_gamble_screen")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag3_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Помиловать» ур.1: освободить цель из тюрьмы под залог,
    # равный 2 * числу оставшихся ходов.
    # ========================================================================
    if target is not None and clover_is_in_prison(target):
        $ bail = clover_prison_bail_cost(target)
        if clover_current_money() >= bail:
            $ clover_add_money(-bail)
            $ clover_free_from_prison(target)
            $ renpy.notify("%s освобождён за %d золота" % (target.name, bail))
        else:
            $ renpy.notify("Недостаточно золота: нужно %d" % bail)
    else:
        $ renpy.notify("Цель не находится за решёткой")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag4_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Суд» ур.3: садит цель за решётку, моментально выводя степень виновного
    # до 100%. Срок = число преступлений (урон 1, штраф характеристик 1,
    # дебафф 1, убийство 2). Цель может выбраться, бросив дубль на 2 кубиках.
    # За решёткой цель лежит ничком, её танк становится равным 0.
    # Бросив её на союзника, мы спасаем союзника от атак.
    # ========================================================================
    if target is not None:
        $ target_name_key = target.name
        $ crimes = dict(getattr(store, "clover_investigation", {}) or {})
        $ entry = dict(crimes.get(target_name_key, {"progress": 0, "prison": 1, "crimes": []}))
        $ entry["progress"] = 100
        if entry["prison"] < 1:
            $ entry["prison"] = 1
        $ crimes[target_name_key] = entry
        $ store.clover_investigation = crimes
        $ clover_send_to_prison(target, entry["prison"])
        $ renpy.notify("%s за решёткой на %d ход(ов)" % (target_name_key, entry["prison"]))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag5_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Дробовик» ур.4: 2 выстрела по цели, остальные получают 25% урона.
    # Урон = атака Кловера * (40% + текущий танк/100), не зависит от калибра,
    # тратит все пули. С шансом 85% − крит.шанс − 5*удача дробовик взрывается
    # и уходит на перезарядку вдвое дольше.
    # ========================================================================
    $ clover_obj = store.pers_dict["Кловер"]
    $ clover_shotgun_damage = 0
    if target is not None:
        $ clover_tank_value = float(getattr(clover_obj, "total_tank", 0))
        $ clover_shotgun_ratio = 0.40 + clover_tank_value / 100.0
        $ clover_shotgun_damage = int(float(getattr(clover_obj, "atk", 0)) * clover_shotgun_ratio)
        python:
            for _shot in range(2):
                _dmg = clover_shotgun_damage
                target.current_hp = max(0, target.current_hp - _dmg)
                target.damage_gain_for_vis = _dmg
                add_attack_result("Кловер", target.name, _dmg, False, "normal")
                # Остальные живые враги получают 25% урона.
                for _enemy in (store.enemies or {}).values():
                    if _enemy is None or _enemy is target or getattr(_enemy, "current_hp", 0) <= 0:
                        continue
                    _splash = max(1, int(_dmg * 0.25))
                    _enemy.current_hp = max(0, _enemy.current_hp - _splash)
                    add_attack_result("Кловер", _enemy.name, _splash, False, "normal")
            # Взрыв дробовика: шанс = 85% − крит.шанс − 5 * удача.
            _luck = max(0.0, -float(getattr(clover_obj, "critrate_debuff", 0) or 0))
            _explode_chance = 0.85 - float(getattr(clover_obj, "critrate", 0)) - 5 * _luck / 100.0
            if renpy.random.random() < max(0.0, _explode_chance):
                store.clover_shotgun_exploded = True
                renpy.log("[Кловер][Дробовик] ствол взорвался — перезарядка вдвое дольше")
        $ store.clover_ammo = 0
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag6_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Метка разыскиваемого» ур.4: накладывает метку на врага. Союзники,
    # атакующие его, получают +5% бонус к точности, а команда получает деньги
    # в размере 40% от нанесённого урона, когда противник умрёт. Под меткой
    # персонажи не заполняют шкалу виновного.
    # ========================================================================
    if target is not None:
        $ clover_mark_wanted(target)
        $ target.wanted_bounty_damage = 0
        $ renpy.notify("%s под меткой разыскиваемого" % target.name)
        $ renpy.log("[Кловер][Метка разыскиваемого] {} помечен".format(target.name))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag7_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Дикий запад, Крошка!» ур.9: призывает два крупнокалиберных револьвера.
    # Базовое исполнение всегда равно 1.0, можно делать до 15 выстрелов за
    # 10 секунд. Каждый выстрел уменьшает бонусный урон, шанс попадания,
    # крит-шанс и крит-урон на 5%.
    # ========================================================================
    $ store.clover_dual_wield = True
    $ store.clover_wildwest_shots = 0
    
    python:
        _orig_atk = store.pers_dict["Кловер"].bonus_atk
        _orig_hit = store.pers_dict["Кловер"].bonus_dmgchance
        _orig_critrate = store.pers_dict["Кловер"].bonus_critrate
        _orig_crit = store.pers_dict["Кловер"].bonus_crit
        _total = 0
        for _shot in range(15):
            _dmg = store.pers_dict["Кловер"].calculate_dmg(target) if target is not None else 0
            if store.pers_dict["Кловер"].popal == 1 and _dmg > 0:
                _total += _dmg
                add_attack_result("Кловер", target.name, _dmg, bool(store.is_crit), "normal")
            # Каждый выстрел ослабляет следующие на 5%.
            store.pers_dict["Кловер"].bonus_atk *= 0.95
            store.pers_dict["Кловер"].bonus_dmgchance -= 0.05
            store.pers_dict["Кловер"].bonus_critrate -= 0.05
            store.pers_dict["Кловер"].bonus_crit *= 0.95
            store.clover_wildwest_shots = _shot + 1
        store.pers_dict["Кловер"].bonus_atk = _orig_atk
        store.pers_dict["Кловер"].bonus_dmgchance = _orig_hit
        store.pers_dict["Кловер"].bonus_critrate = _orig_critrate
        store.pers_dict["Кловер"].bonus_crit = _orig_crit
        store.clover_wildwest_damage = _total
    
    if store.clover_wildwest_damage > 0:
        with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag8_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Вызов на дуэль!» ур.5: увеличивает танк Кловера до максимума в
    # следующий ход. В следующий ход Кловер получает 15% шанс попадания,
    # 20% крит-шанса и 40% крит-урона.
    # ========================================================================
    $ clover_start_duel()
    $ renpy.notify("Кловер вызывает на дуэль: танк на максимум")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag9_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Длинный ствол» ур.6: призывает винчестер с уроном 200% − текущий танк*2.
    # С шансом 85% − крит.шанс − 5*удача винчестер взрывается после выстрела
    # и уходит на перезарядку вдвое дольше.
    # ========================================================================
    if target is not None:
        $ clover_obj = store.pers_dict["Кловер"]
        $ clover_winch_damage = int(float(getattr(clover_obj, "atk", 0)) * 2.0 - float(getattr(clover_obj, "total_tank", 0)) * 2.0)
        $ clover_winch_damage = max(1, clover_winch_damage)
        $ target.current_hp = max(0, target.current_hp - clover_winch_damage)
        $ target.damage_gain_for_vis = clover_winch_damage
        $ add_attack_result("Кловер", target.name, clover_winch_damage, False, "normal")
        python:
            _luck = max(0.0, -float(getattr(clover_obj, "critrate_debuff", 0) or 0))
            _explode_chance = 0.85 - float(getattr(clover_obj, "critrate", 0)) - 5 * _luck / 100.0
            if renpy.random.random() < max(0.0, _explode_chance):
                store.clover_winchester_exploded = True
                renpy.log("[Кловер][Длинный ствол] винчестер взорвался")
        with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag10_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «От судьбы не уйдёшь» ур.8: накладывает на противника метку судьбы.
    # При промахе союзник имеет шанс всё равно нанести урон с шансом
    # собственный крит-шанс/2 + шанс попадания/3. Если герой попал без помощи
    # этой пассивки, то получает +30% от крит-шанса Кловера и +10% от его
    # крит-урона на момент удара. Длится 2 хода.
    # ========================================================================
    if target is not None:
        $ clover_mark_fate(target)
        $ renpy.notify("%s: метка судьбы на 2 хода" % target.name)
        $ renpy.log("[Кловер][От судьбы не уйдёшь] {} помечен".format(target.name))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag11_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Вафельный перерыв» ур.2: вместо 2 использований «Сыграем!» Кловер может
    # съесть вафельку, которую будет есть 3 хода: +5% точности и +3% HP
    # каждый ход. Один раз за бой.
    # ========================================================================
    $ clover_start_waffle()
    $ renpy.notify("Кловер ест вафельку 3 хода")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_mag12_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Гиперлуч» ур.10: тратит все патроны и 80% жизни. Наносит урон, равный
    # 120% от атаки, 200% от текущей точности, 170% от текущего крит-шанса
    # и 120% от текущего крит-урона. Наносит урон всем противникам.
    # Доступен, если текущий рут — GENO.
    # ========================================================================
    $ clover_obj = store.pers_dict["Кловер"]
    $ clover_hyper_damage = int(
        float(getattr(clover_obj, "atk", 0)) * 1.20
        + float(getattr(clover_obj, "dmgchance", 0)) * 2.00
        + float(getattr(clover_obj, "critrate", 0)) * 1.70
        + float(getattr(clover_obj, "crit", 1.0)) * 1.20
    )
    $ clover_obj.current_hp = max(1, int(clover_obj.current_hp * 0.2))
    $ store.clover_ammo = 0
    
    python:
        for _enemy in (store.enemies or {}).values():
            if _enemy is None or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            _enemy.current_hp = max(0, _enemy.current_hp - clover_hyper_damage)
            _enemy.damage_gain_for_vis = clover_hyper_damage
            add_attack_result("Кловер", _enemy.name, clover_hyper_damage, False, "magic")
        renpy.log("[Кловер][Гиперлуч] урон {} по всем противникам".format(clover_hyper_damage))
    
    with crit_vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()


# ========================================================================
# МАГИЯ СЕДРИКА (КУЛИНАРИЯ)
# ========================================================================

# (Лейблы магии Седрика перенесены в 1_ПЕРС_ПАССИВКИ_СЕДРИКА.rpy:
#  sedric_cook_action — готовка блюда, sedric_mag1_is_done — «Сбегать за продуктами»)


# ========================================================================
# АТАКА КЛОВЕРА 1: Стрельба навскидку
# ========================================================================

# Экраны для атаки навскидку (3 выстрела базово, 4 на 2 уровне)
screen Cloveratk1_1:
    timer 3.0 action Jump("clover_atk1_is_done")
    
    # Генерируем случайную позицию для фрейма
    $ frame_xpos = renpy.randint(100, 1000)
    $ frame_ypos = renpy.randint(100, 500)
    
    # Фрейм с двумя imagebutton внутри
    frame:
        xpos frame_xpos
        ypos frame_ypos
        xysize (200, 200)  # Размер фрейма
        
        # Первый imagebutton с 8points.png
        imagebutton:
            idle "8points.png"
            hover "8points.png"
            action [SetVariable("base_perform", base_perform + 0.14 * 0.8), Hide("Cloveratk1_1"), Show("Cloveratk1_2"), Function(apply_clover_recoil)]
            xalign 0.0
            yalign 0.0
        
        # Второй imagebutton с 10points.png
        imagebutton:
            idle "10points.png"
            hover "10points.png"
            action [SetVariable("base_perform", base_perform + 0.14 * 1.0), Hide("Cloveratk1_1"), Show("Cloveratk1_2"), Function(apply_clover_recoil)]
            xalign 1.0
            yalign 1.0

screen Cloveratk1_2:
    timer 3.0 action Jump("clover_atk1_is_done")
    
    # Генерируем случайную позицию для фрейма
    $ frame_xpos = renpy.randint(100, 1000)
    $ frame_ypos = renpy.randint(100, 500)
    
    # Фрейм с двумя imagebutton внутри
    frame:
        xpos frame_xpos
        ypos frame_ypos
        xysize (200, 200)  # Размер фрейма
        
        # Первый imagebutton с 8points.png
        imagebutton:
            idle "8points.png"
            hover "8points.png"
            action [SetVariable("base_perform", base_perform + 0.14 * 0.8), Hide("Cloveratk1_2"), Show("Cloveratk1_3"), Function(apply_clover_recoil)]
            xalign 0.0
            yalign 0.0
        
        # Второй imagebutton с 10points.png
        imagebutton:
            idle "10points.png"
            hover "10points.png"
            action [SetVariable("base_perform", base_perform + 0.14 * 1.0), Hide("Cloveratk1_2"), Show("Cloveratk1_3"), Function(apply_clover_recoil)]
            xalign 1.0
            yalign 1.0

screen Cloveratk1_3:
    timer 3.0 action Jump("clover_atk1_is_done")
    
    # Генерируем случайную позицию для фрейма
    $ frame_xpos = renpy.randint(100, 1000)
    $ frame_ypos = renpy.randint(100, 500)
    
    # Фрейм с двумя imagebutton внутри
    frame:
        xpos frame_xpos
        ypos frame_ypos
        xysize (200, 200)  # Размер фрейма
        
        # Первый imagebutton с 8points.png
        imagebutton:
            idle "8points.png"
            hover "8points.png"
            if store.pers_dict["Кловер"].level >= 2:
                action [SetVariable("base_perform", base_perform + 0.14 * 0.8), Hide("Cloveratk1_3"), Show("Cloveratk1_4"), Function(apply_clover_recoil)]
            else:
                action [SetVariable("base_perform", base_perform + 0.14 * 0.8), Hide("Cloveratk1_3"), Jump("clover_atk1_is_done"), Function(apply_clover_recoil)]
            xalign 0.0
            yalign 0.0
        
        # Второй imagebutton с 10points.png
        imagebutton:
            idle "10points.png"
            hover "10points.png"
            if store.pers_dict["Кловер"].level >= 2:
                action [SetVariable("base_perform", base_perform + 0.14 * 1.0), Hide("Cloveratk1_3"), Show("Cloveratk1_4"), Function(apply_clover_recoil)]
            else:
                action [SetVariable("base_perform", base_perform + 0.14 * 1.0), Hide("Cloveratk1_3"), Jump("clover_atk1_is_done"), Function(apply_clover_recoil)]
            xalign 1.0
            yalign 1.0

screen Cloveratk1_4:
    # Этот экран появляется только на 2 уровне и выше
    timer 3.0 action Jump("clover_atk1_is_done")
    
    # Генерируем случайную позицию для фрейма
    $ frame_xpos = renpy.randint(100, 1000)
    $ frame_ypos = renpy.randint(100, 500)
    
    # Фрейм с двумя imagebutton внутри
    frame:
        xpos frame_xpos
        ypos frame_ypos
        xysize (200, 200)  # Размер фрейма
        
        # Первый imagebutton с 8points.png
        imagebutton:
            idle "8points.png"
            hover "8points.png"
            action [SetVariable("base_perform", base_perform + 0.14 * 0.8), Hide("Cloveratk1_4"), Jump("clover_atk1_is_done"), Function(apply_clover_recoil)]
            xalign 0.0
            yalign 0.0
        
        # Второй imagebutton с 10points.png
        imagebutton:
            idle "10points.png"
            hover "10points.png"
            action [SetVariable("base_perform", base_perform + 0.14 * 1.0), Hide("Cloveratk1_4"), Jump("clover_atk1_is_done"), Function(apply_clover_recoil)]
            xalign 1.0
            yalign 1.0

label clover_atk1_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Навскидку» ур.1: до 3 (4 с «Ловкими пальчиками» ур.2) выстрелов навскидку.
    # Стрельба навскидку: +10% точности, но −5% крит. шанса.
    # Каждый выстрел тратит патрон, урон считается по калибру.
    # ========================================================================
    $ clover_shots = 4 if clover_level() >= CLOVER_QUICK_FINGERS_LEVEL else 3
    
    if target is not None and clover_has_ammo(1):
        # Сохраняем оригинальные значения (только на время этой атаки).
        $ original_dmgchance = store.pers_dict["Кловер"].bonus_dmgchance
        $ original_critrate = store.pers_dict["Кловер"].bonus_critrate
        $ original_atk = store.pers_dict["Кловер"].bonus_atk
        
        # Навскидку: +10% точности, −5% крит. шанса, урон по калибру.
        $ store.pers_dict["Кловер"].bonus_dmgchance += 0.10
        $ store.pers_dict["Кловер"].bonus_critrate -= 0.05
        $ store.pers_dict["Кловер"].bonus_atk *= clover_shot_damage_multiplier()
        
        python:
            clover_total_damage = 0
            for _shot in range(clover_shots):
                if not clover_has_ammo(1):
                    break
                # «Холостой наоборот» ур.4: шанс сэкономить патрон.
                if not clover_try_blank_save():
                    clover_shot_cost(1)
                # «Удачный пристрелочный» ур.6: первый выстрел точнее.
                if _shot == 0 and not store.clover_first_shot_done:
                    _bonus = clover_sighting_bonus()
                    store.pers_dict["Кловер"].bonus_dmgchance += _bonus
                _dmg = store.pers_dict["Кловер"].calculate_dmg(target)
                if _shot == 0 and not store.clover_first_shot_done:
                    store.pers_dict["Кловер"].bonus_dmgchance -= _bonus
                    store.clover_first_shot_done = True
                if store.pers_dict["Кловер"].popal == 1:
                    clover_total_damage += _dmg
                    add_attack_result("Кловер", target.name, _dmg, bool(store.is_crit), "normal")
                    # «Инструктор по бою» ур.2: каждый выстрел даёт союзнику точность.
                    clover_on_shot_fired()
        
        $ store.pers_dict["Кловер"].bonus_dmgchance = original_dmgchance
        $ store.pers_dict["Кловер"].bonus_critrate = original_critrate
        $ store.pers_dict["Кловер"].bonus_atk = original_atk
        
        # «Внезапная заначка» ур.9: если обойма опустела — шанс восстановить половину.
        $ clover_ammo_empty_refill()
        
        if clover_total_damage > 0:
            $ store.is_crit = False
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    $ store.clover_first_shot_done = False
    
    call screen choose_attacker_screen()

# Лейбл для запуска атаки Кловера "Прицельный"
label cloveratk2_perform:
    call screen clover_atk2_target
    #call nolabel

# ========================================================================
# АТАКА КЛОВЕРА 2: Прицельный (адаптация атаки Криса)
# ========================================================================

# Экран с мишенью и imagebutton
screen clover_atk2_target:
    # Генерируем случайную позицию для фрейма
    $ frame_xpos = renpy.randint(100, 1000)
    $ frame_ypos = renpy.randint(100, 500)
    
    timer 0.1 action Show("clover_atk2_xpos")

    # Фрейм с несколькими imagebutton внутри
    frame:
        xpos frame_xpos
        ypos frame_ypos
        xysize (700, 700)  # Размер фрейма

        imagebutton:
            idle "2points.png"
            hover "2points.png"
            action SetVariable("base_perform", "0.2")
            xalign 1.0
            yalign 1.0

        imagebutton:
            idle "4points.png"
            hover "4points.png"
            action SetVariable("base_perform", "0.4")
            xalign 0.5
            yalign 0.5
        
        imagebutton:
            idle "6points.png"
            hover "6points.png"
            action SetVariable("base_perform", "0.6")
            xalign 0.5
            yalign 0.5

        imagebutton:
            idle "8points.png"
            hover "8points.png"
            action SetVariable("base_perform", "0.8")
            xalign 0.5
            yalign 0.5

        imagebutton:
            idle "10points.png"
            hover "10points.png"
            action SetVariable("base_perform", "1.0")
            xalign 0.5
            yalign 0.5




# Экран с горизонтальной палкой
screen clover_atk2_xpos:
    # Генерируем случайную скорость для горизонтальной палки (от 20 до 50)
    $ store.clover_x_speed = renpy.random.randint(20, 50)
    
    # Горизонтальная палка
    add "stick.png":
        yalign 0.5
        xpos clover_stick_xpos

    # Таймер, который каждые 0.03 секунды вызывает нашу функцию для движения
    timer 0.03 repeat True action Function(update_clover_x_position)

    # Кнопка для ОСТАНОВКИ движения горизонтальной палки
    textbutton "Остановить":
        xalign 0.5
        yalign 0.95
        text_size 30
        action [SetVariable("clover_x_moving", False), Show("clover_atk2_ypos")]

# Экран с вертикальной палкой
screen clover_atk2_ypos:
    # Генерируем случайную скорость для вертикальной палки (от 20 до 50)
    $ store.clover_y_speed = renpy.random.randint(20, 50)
    
    # Вертикальная палка (поворачиваем stick.png на 90 градусов)
    add "stick.png":
        xpos clover_final_xpos
        ypos clover_stick_ypos
        rotate 90

    # Таймер, который каждые 0.03 секунды вызывает нашу функцию для движения
    timer 0.03 repeat True action Function(update_clover_y_position)

    # Кнопка для ОСТАНОВКИ движения вертикальной палки
    textbutton "Остановить":
        xalign 0.5
        yalign 0.95
        text_size 30
        action [SetVariable("clover_y_moving", False), Jump("clover_atk2_is_done")]



# ========================================================================
# АТАКИ АЗРИ
# ========================================================================

label asri_atk1_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "fight1"
    
    hide screen Heroattacks
    
    if target is not None:
        $ dmg = store.pers_dict["Азриель"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # 30% шанс уменьшить атаку противника на 10%
        if renpy.random.randint(1, 100) <= 30:
            $ apply_enemy_atk_debuff(target, 1)
        
        if dmg > 0 and store.pers_dict["Азриель"].popal == 1:
            $ store.is_crit = store.pers_dict["Азриель"].crit > 1.0
            $ add_attack_result(store.pers_dict["Азриель"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
            # «Пламенная инфузия» ур.3: обычные атаки могут поджечь.
            $ azri_fire_on_damage(target, dmg)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_atk2_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "fight2"
    
    hide screen Heroattacks
    
    if target is not None:
        # «Взмах мечом»: +10% атаки и +5% точности с каждым ударом, накопительно.
        $ store.pers_dict["Азриель"].bonus_atk += 0.10
        $ store.pers_dict["Азриель"].bonus_dmgchance += 0.05
        
        $ dmg = store.pers_dict["Азриель"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        if dmg > 0 and store.pers_dict["Азриель"].popal == 1:
            $ store.is_crit = store.pers_dict["Азриель"].crit > 1.0
            $ add_attack_result(store.pers_dict["Азриель"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
            $ azri_fire_on_damage(target, dmg)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_atk3_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "fight3"
    
    hide screen Heroattacks
    
    # «Щитовой удар»: урон по ВСЕМ противникам, сила растёт от защиты Азриеля.
    python:
        _azri = store.pers_dict["Азриель"]
        _orig_atk = _azri.bonus_atk
        _orig_critrate = _azri.bonus_critrate
        _azri.bonus_atk += _azri.defense * 0.5
        _azri.bonus_critrate = -_azri.base_critrate
        for _enemy_name in get_active_enemies():
            _enemy = store.enemies.get(_enemy_name)
            if _enemy is None or _enemy.current_hp <= 0:
                continue
            _dmg = _azri.calculate_dmg(_enemy)
            _enemy.current_hp = max(0, _enemy.current_hp - _dmg)
            _enemy.damage_gain_for_vis = _dmg
            _enemy.got_crit_for_visual = 0
            if _dmg > 0:
                add_attack_result(_azri.name, _enemy.name, _dmg, False, "normal")
                azri_fire_on_damage(_enemy, _dmg)
        _azri.bonus_atk = _orig_atk
        _azri.bonus_critrate = _orig_critrate
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label asri_atk4_is_done:
    $ store.pers_dict["Азриель"].turn = 0
    $ store.pers_dict["Азриель"].state = "fight4"
    
    hide screen Heroattacks
    
    if target is not None:
        $ original_critrate = store.pers_dict["Азриель"].bonus_critrate
        
        # Удар не критует
        $ store.pers_dict["Азриель"].bonus_critrate = -store.pers_dict["Азриель"].base_critrate
        
        $ dmg = store.pers_dict["Азриель"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        $ store.pers_dict["Азриель"].bonus_critrate = original_critrate
        
        # 30% шанс повалить противника и наложить истощение х2
        if renpy.random.randint(1, 100) <= 30:
            $ target.debuff("prone", 1)
            $ apply_enemy_atk_debuff(target, 2)
        
        if dmg > 0 and store.pers_dict["Азриель"].popal == 1:
            $ store.is_crit = False  # Удар не критует
            $ add_attack_result(store.pers_dict["Азриель"].name, target.name, dmg, is_crit, "normal")
            with vpunch
            $ azri_fire_on_damage(target, dmg)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Азриель"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

# ========================================================================
# АТАКИ ЧАРЫ
# ========================================================================

label CharaAtk1_is_done2:
    hide screen Heroattacks                         # Закрываем экран, который привёл к этому лейблу
    $ store.pers_dict["Чара"].turn = 0              # Cбрасываем ход у персонажа, чтоб он был = 0
    
    $ renpy.notify([store.base_perform])

    if target is not None and store.kris1_atk_pressed == 1:

        $ store.pers_dict["Чара"].state = "fight1"      # Состояние перса для текущего лейбла
        $ prepare_turn_effect_target(target)            # Подготовка координат цели
        show screen targettochoose_sprites_effect_universal
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_critrate = store.pers_dict["Чара"].bonus_critrate
        
        # +20% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.20
        # +10% крит. шанс
        $ store.pers_dict["Чара"].bonus_critrate += 0.10
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.current_hp = max(0, target.current_hp - dmg)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit) if is_crit is not None else 0
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_critrate = original_critrate
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = store.pers_dict["Чара"].crit > 1.0
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    $ renpy.pause(0.5,hard=True)
    show screen attacked_compiled_heroturn 
    $ renpy.pause(3, hard=True)
    hide screen attacked_compiled_heroturn
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    hide screen targettochoose_sprites_effect_universal
    $ store.pers_dict["Чара"].turn = 1
    $ store.pers_dict["Чара"].step_forward = 2
    
    call screen choose_attacker_screen()




transform alpha0405:
    alpha 0.0
    easein 0.5 alpha 0.3 xalign 0.5 yalign 0.5

transform chara_atk3_timer:
    xsize 1000 ysize 30 xpos 20 ypos 20 alpha 0.0
    parallel:
        ease 3.0 xsize 0 
    parallel:
        easein 0.2 alpha 1.0

default chara_atk3_is_ready = 0
default chara_atk3_out = 0

label CharaAtk1_is_done:
    $ chara_atk3_out = 0
    $ chara_atk3_is_ready = 0
    $ atk_ind_ratio = 1.0
    $ store.pers_dict["Чара"].turn = 1
    $ renpy.notify([base_perform])
    # kris1_atk_pressed устанавливается в 1 при нажатии кнопки в мини-игре,
    # или остается 0 при таймауте.
    # (Если для "Удара бунтарки" и "Удара шпагой" вы не используете мини-игру,
    # убедитесь, что перед переходом в этот лейбл вы пишете $ kris1_atk_pressed = 1)
    
    if kris1_atk_pressed == 1:
        # Устанавливаем состояние в зависимости от атаки (для правильной анимации полета)
        if store.attackindex == "Удар бунтарки":
            $ store.pers_dict["Чара"].state = "fight1"
        elif store.attackindex == "Удар ножом":
            $ store.pers_dict["Чара"].state = "fight2"
            if base_perform >= 0.9:
                $ base_perform = 1.0
        elif store.attackindex == "Удар шпагой":
            $ store.pers_dict["Чара"].state = "fight3"
        else:
            $ store.pers_dict["Чара"].state = "fight1"

        $ prepare_turn_effect_target(target)
        show screen targettochoose_sprites_effect_universal
        $ renpy.pause(0.5, hard=True)
        
        if target is not None:
            if  store.attackindex == "Удар бунтарки":
                $ renpy.pause(0.65, hard=False)
            elif store.attackindex == "Удар ножом":
                $ renpy.pause(3.5, hard=False)
            elif store.attackindex == "Удар шпагой":
                $ renpy.pause(1.5, hard=False)

                
            # === ОСОБЕННОСТИ ЧАРЫ (МОДИФИКАТОРЫ АТАК) ===
            $ original_atk = store.pers_dict["Чара"].bonus_atk
            $ original_critrate = store.pers_dict["Чара"].bonus_critrate
            $ original_crit = store.pers_dict["Чара"].bonus_crit
            
            if store.attackindex == "Удар бунтарки":
                $ store.pers_dict["Чара"].bonus_atk += 0.20
                $ store.pers_dict["Чара"].bonus_critrate += 0.10  # ИСПРАВЛЕНО: было 1.10
            elif store.attackindex == "Удар ножом":
                $ store.pers_dict["Чара"].bonus_atk += 0.15
                $ store.pers_dict["Чара"].bonus_crit += 0.20
            elif store.attackindex == "Удар шпагой":
                $ store.pers_dict["Чара"].bonus_atk += 0.10
                $ store.pers_dict["Чара"].bonus_critrate += 0.10
                $ store.pers_dict["Чара"].bonus_crit += 0.10

            # Рассчитываем урон по выбранной цели
            # calculate_dmg ВНУТРИ СЕБЯ определяет крит, записывает его в store.is_crit И СНИМАЕТ HP
            $ target_hp_before = target.current_hp
            $ dmg = store.pers_dict["Чара"].calculate_dmg(target)

            # Визуализация урона на экране
            $ target.damage_gain_for_vis = dmg
            $ target.got_crit_for_visual = 1 if store.is_crit else 0
            
            # Восстанавливаем оригинальные значения
            $ store.pers_dict["Чара"].bonus_atk = original_atk
            $ store.pers_dict["Чара"].bonus_critrate = original_critrate
            $ store.pers_dict["Чара"].bonus_crit = original_crit

            # Добавляем результат атаки в историю
            if dmg > 0 and store.pers_dict["Чара"].popal == 1:
                $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, store.is_crit, "normal")
                
            # === ПОСТ-ЭФФЕКТЫ ЧАРЫ ===
            # Удар ножом имеет 25% шанс вызвать кровотечение
            if store.attackindex == "Удар ножом" and dmg > 0 and store.pers_dict["Чара"].popal == 1 and target.shield== 0:
                if renpy.random.randint(1, 100) <= 25:
                    $ target.bloodshed_debuff += 2
                    $ target.bloodshed_debuff_got += 1
                    
        else:
            $ store.pers_dict["Чара"].popal = 0
            if target is not None:
                $ target.damage_gain_for_vis = 0
                $ store.clear_swoon_pending_for_visual(target)
                
    elif kris1_atk_pressed == 0:
        # Таймаут мини-игры (промах)
        $ dmg = 0
        if target is not None:
            $ target.damage_gain_for_vis = -1
            $ store.clear_swoon_pending_for_visual(target)

    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    hide screen Heroattacks
    
##

    # === ТРЯСКА ЭКРАНА ===
    # Проверяем store.is_crit (результат кубика из calculate_dmg)
    if dmg > 0 and store.pers_dict["Чара"].popal == 1 and store.is_crit:
        with vpunch
        with vpunch

    # Показываем результаты
    show screen attacked_compiled_heroturn
    $ renpy.pause(1.5, hard=False)
    hide screen attacked_compiled_heroturn
    $ renpy.pause(1.0, hard=True)
    
    $ store.pers_dict["Чара"].turn = 1
    hide screen targettochoose_sprites_effect_universal
    $ store.pers_dict["Чара"].step_forward = 2
    $ store.is_crit = None
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0

    call set_buttons_to_default
    call screen choose_attacker_screen()










label CharaAtk2_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "fight2"
    show screen targettochoose_sprites_effect_universal
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_crit = store.pers_dict["Чара"].bonus_crit
        
        # +15% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.15
        # +20% крит. урон
        $ store.pers_dict["Чара"].bonus_crit *= 1.20
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_crit = original_crit
        
        # 25% шанс вызвать кровотечение
        if renpy.random.randint(1, 100) <= 25:
            $ apply_enemy_bleeding(target, 2)
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = store.pers_dict["Чара"].crit > 1.0
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    $ store.pers_dict["Чара"].turn = 1

    call screen choose_attacker_screen()

label CharaAtk3_is_done:
    show screen targettochoose_sprites_effect_universal
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "fight3"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_critrate = store.pers_dict["Чара"].bonus_critrate
        $ original_crit = store.pers_dict["Чара"].bonus_crit
        
        # +10% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.10
        # +15% крит. шанс
        $ store.pers_dict["Чара"].bonus_critrate += 0.15
        # +10% крит. урон
        $ store.pers_dict["Чара"].bonus_crit *= 1.10
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_critrate = original_critrate
        $ store.pers_dict["Чара"].bonus_crit = original_crit
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = store.pers_dict["Чара"].crit > 1.0
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    $ store.pers_dict["Чара"].turn = 1
    call screen choose_attacker_screen()

label CharaAtk4_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "fight4"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_critrate = store.pers_dict["Чара"].bonus_critrate
        
        # +25% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.25
        # Удар не критует
        $ store.pers_dict["Чара"].bonus_critrate = -store.pers_dict["Чара"].base_critrate
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_critrate = original_critrate
        
        # 40% шанс ослабить защиту врага на 20%
        if renpy.random.randint(1, 100) <= 40:
            $ apply_enemy_weaken_armor(target, 0.2)
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = False  # Удар не критует
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            with vpunch
    
    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label CharaAtk5_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "fight5"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_critrate = store.pers_dict["Чара"].bonus_critrate
        
        # +5% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.05
        # +30% крит. шанс
        $ store.pers_dict["Чара"].bonus_critrate += 0.30
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_critrate = original_critrate
        
        # 50% шанс оглушить врага
        if renpy.random.randint(1, 100) <= 50:
            $ apply_enemy_stun(target, 1)
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = store.pers_dict["Чара"].crit > 1.0
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label CharaAtk6_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "fight6"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_critrate = store.pers_dict["Чара"].bonus_critrate
        $ original_crit = store.pers_dict["Чара"].bonus_crit
        
        # +15% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.15
        # +20% крит. шанс
        $ store.pers_dict["Чара"].bonus_critrate += 0.20
        # +25% крит. урон
        $ store.pers_dict["Чара"].bonus_crit *= 1.25
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_critrate = original_critrate
        $ store.pers_dict["Чара"].bonus_crit = original_crit
        
        # 30% шанс ослабить атаку врага на 30%
        if renpy.random.randint(1, 100) <= 30:
            $ apply_enemy_weaken_attack(target, 0.3)
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = store.pers_dict["Чара"].crit > 1.0
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label CharaAtk7_is_done:
    $ store.pers_dict["Чара"].turn = 0
    $ store.pers_dict["Чара"].state = "fight7"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Чара"].bonus_atk
        $ original_critrate = store.pers_dict["Чара"].bonus_critrate
        $ original_crit = store.pers_dict["Чара"].bonus_crit
        
        # +50% атака
        $ store.pers_dict["Чара"].bonus_atk *= 1.50
        # +40% крит. шанс
        $ store.pers_dict["Чара"].bonus_critrate += 0.40
        # +50% крит. урон
        $ store.pers_dict["Чара"].bonus_crit *= 1.50
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Чара"].calculate_dmg(target)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Чара"].bonus_atk = original_atk
        $ store.pers_dict["Чара"].bonus_critrate = original_critrate
        $ store.pers_dict["Чара"].bonus_crit = original_crit
        
        # 80% шанс кровотечения: «х2» — это +2 к дебаффу кровотечения врага
        if renpy.random.randint(1, 100) <= 80:
            $ apply_enemy_bleeding(target, 2)
        
        if dmg > 0 and store.pers_dict["Чара"].popal == 1:
            $ store.is_crit = store.pers_dict["Чара"].crit > 1.0
            $ add_attack_result(store.pers_dict["Чара"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    $ chara_on_attack_result(store.pers_dict["Чара"].popal == 1, target, store.attackindex)
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Чара"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

# ========================================================================
# АТАКИ СЕДРИКА
# ========================================================================

# (Лейблы атак Седрика sedric_atk1_is_done и sedric_atk2_is_done перенесены в 1_ПЕРС_ПАССИВКИ_СЕДРИКА.rpy)

# ========================================================================
# АТАКИ КЛОВЕРА (дополнительные)
# ========================================================================

label clover_atk2_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    hide screen clover_atk2_ypos
    
    # Перемещаем мышь к координатам перекрестья
    $ Mousemove(clover_final_xpos, clover_final_ypos, duration=0.1)
    $ renpy.pause(0.1)
    
    # Симулируем клик на координатах перекрестья
    $ simulate_click(clover_final_xpos, clover_final_ypos)
    $ renpy.pause(0.1)
    
    if target is not None and clover_has_ammo(1):
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Кловер"].bonus_atk
        $ original_dmgchance = store.pers_dict["Кловер"].bonus_dmgchance
        
        # «Прицельный» ур.3: до 3 выстрелов, повышенный крит-урон и точность.
        # Урон зависит от калибра.
        $ store.pers_dict["Кловер"].bonus_atk *= 1.20 * clover_shot_damage_multiplier()
        $ store.pers_dict["Кловер"].bonus_dmgchance += 0.15
        
        python:
            clover_total_damage = 0
            for _shot in range(3):
                if not clover_has_ammo(1):
                    break
                if not clover_try_blank_save():
                    clover_shot_cost(1)
                # «Удачный пристрелочный» ур.6: первый выстрел точнее в 3*ур.
                _bonus = 0.0
                if _shot == 0 and not store.clover_first_shot_done:
                    _bonus = clover_sighting_bonus()
                    store.pers_dict["Кловер"].bonus_dmgchance += _bonus
                _dmg = store.pers_dict["Кловер"].calculate_dmg(target)
                if _shot == 0 and not store.clover_first_shot_done:
                    store.pers_dict["Кловер"].bonus_dmgchance -= _bonus
                    store.clover_first_shot_done = True
                if store.pers_dict["Кловер"].popal == 1:
                    clover_total_damage += _dmg
                    add_attack_result("Кловер", target.name, _dmg, bool(store.is_crit), "normal")
                    clover_on_shot_fired()
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Кловер"].bonus_atk = original_atk
        $ store.pers_dict["Кловер"].bonus_dmgchance = original_dmgchance
        
        # «Рикошет» ур.7: выстрел может отскочить в других противников.
        python:
            for _enemy, _chance in clover_ricochet_targets(target):
                if renpy.random.random() < _chance:
                    _rdmg = clover_ricochet_damage(_enemy, 0.5)
                    _enemy.current_hp = max(0, _enemy.current_hp - _rdmg)
                    add_attack_result("Кловер", _enemy.name, _rdmg, False, "normal")
        
        $ clover_ammo_empty_refill()
        
        if clover_total_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    # Сбрасываем переменные для следующей атаки
    $ clover_stick_xpos = 1400
    $ clover_stick_ypos = 600
    $ clover_x_moving = True
    $ clover_y_moving = True
    
    # Сбрасываем переменные скорости для следующей атаки
    $ store.clover_x_speed = 30
    $ store.clover_y_speed = 30
    
    call screen choose_attacker_screen()

label clover_atk3_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Лассо» ур.5: связывает врага. Не наносит урон, но атаки по нему точнее
    # на 20%. Делает его упавшим на 1 ход с шансом 50% от крит-шанса.
    # ========================================================================
    if target is not None:
        $ target.lasso_marked = 2
        $ target.bonus_dmgchance_taken = float(getattr(target, "bonus_dmgchance_taken", 0.0)) + 0.20
        $ clover_obj = store.pers_dict["Кловер"]
        $ lasso_prone_chance = float(getattr(clover_obj, "critrate", 0)) * 0.5
        if renpy.random.random() < lasso_prone_chance:
            $ apply_enemy_stun(target, 1)
            $ renpy.log("[Кловер][Лассо] {} повален".format(target.name))
        $ renpy.log("[Кловер][Лассо] {} связан: +20% точности по нему".format(target.name))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_atk4_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Разрушительный хлыст» ур.7: удар снимает 20% от защиты жертвы.
    # То же, что лассо, но несколько раз и в разных местах.
    # ========================================================================
    if target is not None:
        $ apply_enemy_weaken_armor(target, 0.20)
        $ original_atk = store.pers_dict["Кловер"].bonus_atk
        $ store.pers_dict["Кловер"].bonus_atk *= clover_shot_damage_multiplier()
        
        python:
            clover_total_damage = 0
            for _hit in range(3):
                # Каждый удар дополнительно снимает по 20% защиты.
                if _hit > 0:
                    apply_enemy_weaken_armor(target, 0.20)
                _dmg = store.pers_dict["Кловер"].calculate_dmg(target)
                if store.pers_dict["Кловер"].popal == 1:
                    clover_total_damage += _dmg
                    add_attack_result("Кловер", target.name, _dmg, bool(store.is_crit), "normal")
        
        $ store.pers_dict["Кловер"].bonus_atk = original_atk
        
        if clover_total_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_atk5_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Клеймо» ур.7: прижигает врага раскалённым клеймом, горение 5 ходов.
    # ========================================================================
    if target is not None:
        $ original_atk = store.pers_dict["Кловер"].bonus_atk
        $ store.pers_dict["Кловер"].bonus_atk *= clover_shot_damage_multiplier()
        
        $ dmg = store.pers_dict["Кловер"].calculate_dmg(target)
        
        $ store.pers_dict["Кловер"].bonus_atk = original_atk
        
        if store.pers_dict["Кловер"].popal == 1:
            $ add_attack_result("Кловер", target.name, dmg, bool(store.is_crit), "normal")
            # Горение 5 ходов через канал кровотечения (5% max HP за стак).
            $ apply_enemy_bleeding(target, 5)
            $ renpy.log("[Кловер][Клеймо] {} горит 5 ходов".format(target.name))
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label clover_atk6_is_done:
    $ store.pers_dict["Кловер"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Скорострел» ур.9: выпускает все пули по цели, но шанс попадания −30%.
    # ========================================================================
    if target is not None and clover_has_ammo(1):
        $ original_atk = store.pers_dict["Кловер"].bonus_atk
        $ original_dmgchance = store.pers_dict["Кловер"].bonus_dmgchance
        $ store.pers_dict["Кловер"].bonus_atk *= clover_shot_damage_multiplier()
        $ store.pers_dict["Кловер"].bonus_dmgchance -= 0.30
        
        python:
            clover_total_damage = 0
            _shots = clover_ammo_count()
            for _shot in range(_shots):
                if not clover_has_ammo(1):
                    break
                if not clover_try_blank_save():
                    clover_shot_cost(1)
                _dmg = store.pers_dict["Кловер"].calculate_dmg(target)
                if store.pers_dict["Кловер"].popal == 1:
                    clover_total_damage += _dmg
                    add_attack_result("Кловер", target.name, _dmg, bool(store.is_crit), "normal")
                    clover_on_shot_fired()
        
        $ store.pers_dict["Кловер"].bonus_atk = original_atk
        $ store.pers_dict["Кловер"].bonus_dmgchance = original_dmgchance
        
        # «Рикошет» ур.7 срабатывает и на скоростреле.
        python:
            for _enemy, _chance in clover_ricochet_targets(target):
                if renpy.random.random() < _chance:
                    _rdmg = clover_ricochet_damage(_enemy, 0.3)
                    _enemy.current_hp = max(0, _enemy.current_hp - _rdmg)
                    add_attack_result("Кловер", _enemy.name, _rdmg, False, "normal")
        
        $ clover_ammo_empty_refill()
        
        if clover_total_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    $ store.clover_first_shot_done = False
    
    call screen choose_attacker_screen()

# ========================================================================
# АТАКИ ФРИСКА
# ========================================================================

label frisk_atk1_is_done:
    $ store.pers_dict["Фриск"].turn = 0
    $ store.pers_dict["Фриск"].state = "fight1"
    
    hide screen Heroattacks
    
    if target is not None:
        # Сохраняем оригинальные значения
        $ original_atk = store.pers_dict["Фриск"].bonus_atk
        $ original_def = store.pers_dict["Фриск"].bonus_def
        
        # Para bellum — мощная атака с бонусом от недостающего HP команды.
        $ store.pers_dict["Фриск"].bonus_atk *= (1.0 + frisk_si_vis_damage_bonus())
        
        # Рассчитываем урон
        $ dmg = store.pers_dict["Фриск"].calculate_dmg(target)
        $ target.current_hp = max(0, target.current_hp - dmg)
        $ target.damage_gain_for_vis = dmg
        $ target.got_crit_for_visual = int(is_crit)
        
        # Восстанавливаем оригинальные значения
        $ store.pers_dict["Фриск"].bonus_atk = original_atk
        $ store.pers_dict["Фриск"].bonus_def = original_def
        
        # 40% шанс убедить врага прекратить бой (ослабить атаку на 30%)
        if renpy.random.randint(1, 100) <= 40:
            $ apply_enemy_weaken_attack(target, 0.3)
        
        if dmg > 0 and store.pers_dict["Фриск"].popal == 1:
            $ store.is_crit = store.pers_dict["Фриск"].crit > 1.0
            $ add_attack_result(store.pers_dict["Фриск"].name, target.name, dmg, is_crit, "normal")
            if is_crit:
                with crit_vpunch
            else:
                with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ store.pers_dict["Фриск"].state = "idle"
    $ base_perform = 0
    
    call screen choose_attacker_screen()

# ========================================================================
# МАГИЯ ИЗЗИ
# ------------------------------------------------------------------------
# Все заклинания Иззи реализованы здесь. «Осколок себя» (izzymag1) имеет
# собственную мини-игру и живёт в отдельном файле.
# ========================================================================

label izzymag2_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Успокоение» ур.1: снимает дебаффы выбранной цели. −5% макс. HP, 10 MP.
    # Даёт шанс контроля Криса на 40% в этот ход, если применено на Криса.
    # Улучшение «Правильное дыхание» ур.4: союзник получает +10% точности.
    # ========================================================================
    $ izzy_self_hp = izzy_spell_hp_cost(0.05)
    
    if target is not None:
        # Снимаем дебаффы цели.
        python:
            _cleared = 0
            for _field in ("atk_debuff", "def_debuff", "magic_debuff",
                           "accuracy_debuff", "critrate_debuff", "critdmg_debuff",
                           "tank_debuff"):
                _val = int(getattr(target, _field, 0) or 0)
                if _val != 0:
                    setattr(target, _field, 0)
                    _cleared += 1
            if _cleared > 0:
                renpy.log("[Иззи][Успокоение] снято дебаффов: {}".format(_cleared))
            # Крис: шанс контроля 40% в этот ход.
            if getattr(target, "name", None) == "Крис":
                if renpy.random.random() < 0.40:
                    store.kris_control_chance_bonus = 0.40
                    renpy.notify("Крис повинуется (40%)")
        # «Правильное дыхание» ур.4: +10% точности союзнику.
        $ izzy_on_calm_ally(target)
        # Если применено на Криса — «Успокоение близкого» ур.5 повышает шанс.
        $ izzy_calm_kris_bonus()
        # «Магия сверху» ур.9 / «Подавление ауры» ур.3.
        $ izzy_on_magic_used(target)
        $ izzy_try_clear_fear("Успокоение")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag3_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Медитация» ур.1: даёт понимание прежде всего о себе. +40% MP Иззи.
    # Цель — автоматически сама Иззи.
    # «Открытие чакр» ур.2: даёт 2 стака просвещения.
    # «Потоки чакр» ур.3: 40% шанс восстановить вдвое больше маны.
    # ========================================================================
    $ izzy_mp_multiplier = izzy_meditation_bonus()
    $ mp_restore = int(store.pers_dict["Иззи"].max_mp * 0.40 * izzy_mp_multiplier)
    $ store.pers_dict["Иззи"].current_mp = min(
        store.pers_dict["Иззи"].max_mp,
        store.pers_dict["Иззи"].current_mp + mp_restore)
    $ izzy_try_clear_fear("Медитация")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag4_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Правильное дыхание» ур.1: снижает текущую перезарядку всех способностей
    # на 2 у выбранной цели. 24 MP.
    # «Целебное благовоние» ур.7: если «Благовония» на КД, дыхание лечит
    # Иззи, восстанавливая 20% HP.
    # ========================================================================
    $ izzy_success = False
    
    if target is not None:
        python:
            # Снижаем текущую перезарядку способностей цели на 2.
            _target_name = getattr(target, "name", None)
            for _ability in (getattr(store, "BATTLE_ABILITY_DEFINITIONS", []) or []):
                if _ability.get("owner") != _target_name:
                    continue
                _cd = int(_ability.get("current_cd", 0) or 0)
                if _cd > 0:
                    _ability["current_cd"] = max(0, _cd - 2)
                    _key = _ability.get("name")
                    if _key in getattr(store, "BATTLE_ABILITY_COOLDOWNS", {}):
                        store.BATTLE_ABILITY_COOLDOWNS[_key]["current_cd"] = _ability["current_cd"]
            izzy_success = True
            renpy.log("[Иззи][Правильное дыхание] КД {} снижены на 2".format(_target_name))
        # «Целебное благовоние» ур.7.
        $ izzy_on_breathing_used(izzy_incense_on_cooldown())
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag5_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Благовония» ур.2: снять с врагов все стаки гнева, а с союзников —
    # печали. 28 MP.
    # Гнев — положительный atk_debuff у врага (истощение), печаль —
    # положительный def_debuff у союзника.
    # ========================================================================
    python:
        for _enemy in (store.enemies or {}).values():
            if _enemy is None or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            if int(getattr(_enemy, "atk_debuff", 0) or 0) > 0:
                _enemy.atk_debuff = 0
        for _ally in (store.pers_dict or {}).values():
            if _ally is None or getattr(_ally, "picked", 0) != 1:
                continue
            if int(getattr(_ally, "def_debuff", 0) or 0) > 0:
                _ally.def_debuff = 0
        renpy.log("[Иззи][Благовония] гнев с врагов и печаль с союзников сняты")
    
    $ izzy_on_magic_used(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag6_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Открытие пределов» ур.3: даёт 2 уровня цели на 4 хода. 35 MP.
    # ========================================================================
    if target is not None:
        $ target.level_bonus = int(getattr(target, "level_bonus", 0) or 0) + 2
        $ target.level_bonus_turns = 4
        $ renpy.notify("%s: +2 уровня на 4 хода" % target.name)
        $ izzy_on_magic_used(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag7_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Воспрять дух» ур.4: даёт цели второй ход. 44 MP.
    # ========================================================================
    if target is not None:
        $ target.turn = 1
        $ renpy.notify("%s получает второй ход" % target.name)
        $ izzy_on_magic_used(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag8_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Карма» ур.5: накладывает на одного из героев печать кармы. 100% урона,
    # полученного персонажем, отражается противнику, но с учётом его брони.
    # Накладывающий теряет 20% HP. 50 MP.
    # «Любовь вселенной» ур.6: при карме на себе половина урона от
    # «Осколка себя» превращается в дополнительный урон по противнику.
    # ========================================================================
    $ izzy_self_hp = izzy_spell_hp_cost(0.20)
    
    if target is not None:
        $ izzy_set_karma(target, 2)
        $ renpy.notify("%s: печать кармы" % target.name)
        $ izzy_on_magic_used(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag9_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Предвиденье» ур.6: уменьшает скорость полёта снарядов всех противников
    # на 10%. Стакается. Стоит 20% HP.
    # ========================================================================
    $ izzy_self_hp = izzy_spell_hp_cost(0.20)
    
    python:
        for _enemy in (store.enemies or {}).values():
            if _enemy is None or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            _enemy.bullet_speed = float(getattr(_enemy, "bullet_speed", 1.0)) * 0.90
        renpy.log("[Иззи][Предвиденье] скорость снарядов −10%")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag10_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Зачарование» ур.7: увеличивает бонусную силу атаки союзника на
    # показатель своей магии * 20%.
    # «Духовный диалог» ур.8: 50% восстановить Иззи 10% MP и +10% своей магии.
    # ========================================================================
    if target is not None:
        $ izzy_magic_value = float(getattr(store.pers_dict["Иззи"], "magic", 0))
        $ target.bonus_atk = float(getattr(target, "bonus_atk", 0)) + izzy_magic_value * 0.20 / 100.0
        $ renpy.notify("%s: атака усилена" % target.name)
        $ izzy_on_enchant_ally(target)
        $ izzy_on_magic_used(target)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag11_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Усиление присутствия» ур.8: удваивает значения своих пассивных
    # способностей в два раза. Одноразовая.
    # ========================================================================
    $ store.izzy_presence_doubled = True
    $ izzy_obj = store.pers_dict["Иззи"]
    $ izzy_obj.bonus_critrate = float(getattr(izzy_obj, "bonus_critrate", 0)) + 0.25
    $ izzy_obj.bonus_crit = float(getattr(izzy_obj, "bonus_crit", 0)) + 0.30
    $ renpy.notify("Усиление присутствия: пассивки Иззи удвоены")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag12_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Духовный лук» ур.9: наносит урон 4 раза. 1 — от стрелы, а 1 осколка
    # себя, который наносит урон цели 200%, а затем всем врагам — 50%.
    # −40% от макс. HP Иззи. 70% MP.
    # ========================================================================
    $ izzy_self_hp = izzy_spell_hp_cost(0.40)
    
    python:
        _izzy = store.pers_dict["Иззи"]
        _total = 0
        # Стрела + осколок: 4 удара по цели.
        if target is not None and getattr(target, "current_hp", 0) > 0:
            for _shot in range(4):
                _dmg = max(1, int(float(getattr(_izzy, "magic", 0)) * (2.0 if _shot == 1 else 0.5)))
                target.current_hp = max(0, target.current_hp - _dmg)
                _total += _dmg
                add_attack_result("Иззи", target.name, _dmg, bool(store.is_crit), "magic")
                # «Отзвуки прошлого»: при крите равновесие теряется.
                if store.is_crit:
                    izzy_on_shard_crit()
        # Осколок задевает всех остальных врагов на 50%.
        _splash = max(1, int(float(getattr(_izzy, "magic", 0)) * 0.5))
        for _enemy in (store.enemies or {}).values():
            if _enemy is None or _enemy is target or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            _enemy.current_hp = max(0, _enemy.current_hp - _splash)
            add_attack_result("Иззи", _enemy.name, _splash, False, "magic")
        renpy.log("[Иззи][Духовный лук] урон по цели {}, сплэш {}".format(_total, _splash))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label izzymag13_is_done:
    $ store.pers_dict["Иззи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Пробуждение» ур.10: создаёт из своей души нож и наносит 3 удара с
    # повышенным крит-шансом и крит-уроном. Игнорирует защиту. После этой
    # атаки впадает в страх перед своей миссией и может использовать лишь
    # медитацию и успокоение. Не теряет HP. 100% MP. Одноразовая.
    # ========================================================================
    if target is not None:
        $ izzy_obj = store.pers_dict["Иззи"]
        $ original_critrate = izzy_obj.bonus_critrate
        $ original_crit = izzy_obj.bonus_crit
        $ izzy_obj.bonus_critrate = original_critrate + 0.50
        $ izzy_obj.bonus_crit = original_crit + 0.50
        
        python:
            _total = 0
            for _hit in range(3):
                # Игнорирует защиту: считаем урон от магии напрямую.
                _dmg = max(1, int(float(getattr(izzy_obj, "magic", 0)) * 1.5))
                target.current_hp = max(0, target.current_hp - _dmg)
                _total += _dmg
                add_attack_result("Иззи", target.name, _dmg, True, "magic")
            renpy.log("[Иззи][Пробуждение] суммарный урон {}".format(_total))
        
        $ izzy_obj.bonus_critrate = original_critrate
        $ izzy_obj.bonus_crit = original_crit
        with crit_vpunch
        
        # После атаки Иззи впадает в страх перед миссией.
        $ izzy_enter_fear()
    
    # «Магия сверху» ур.9: 20% от текущей магии применить заклинание дважды.
    if getattr(store, "izzy_double_magic_pending", False):
        jump izzy_double_cast_is_done
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

# ========================================================================
# ПОВТОРНОЕ ПРИМЕНЕНИЕ МАГИИ («Магия сверху» ур.9)
# ------------------------------------------------------------------------
# Если пассивка сработала, заклинание применяется второй раз по той же цели.
# Лейбл вызывается после основного эффекта и повторяет его.
# ========================================================================

label izzy_double_cast_is_done:
    $ izzy_double_target = izzy_consume_double_magic()
    
    if izzy_double_target is not None:
        python:
            _izzy = store.pers_dict["Иззи"]
            _dmg = max(1, int(float(getattr(_izzy, "magic", 0)) * 0.75))
            if getattr(izzy_double_target, "current_hp", 0) > 0:
                izzy_double_target.current_hp = max(0, izzy_double_target.current_hp - _dmg)
                add_attack_result("Иззи", izzy_double_target.name, _dmg, False, "magic")
                renpy.log("[Иззи][Магия сверху] повторное применение: {} урона".format(_dmg))
        $ renpy.notify("Магия сверху: заклинание сработало дважды")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

# ========================================================================
# АТАКИ АРЧИ
# ------------------------------------------------------------------------
# Арчи — боец ближнего боя. Его атаки наносят урон через calculate_dmg
# (который сам применяет урон, щиты и криты) и накладывают эффекты.
# ========================================================================

label archie_atk1_is_done:
    # Ход израсходован; «Удар! Удар!» ур.1 ниже может вернуть его обратно
    # (шанс = крит-шанс/2 получить второй ход).
    $ store.pers_dict["Арчи"].turn = 0
    $ archie_mark_first_done()
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Боксёрское комбо» ур.1: 4 удара руками (5 с «И ещё один!» ур.2).
    # Каждый удар −5% к броне цели с шансом 25%.
    # ========================================================================
    $ archie_hits = archie_combo_hits()
    
    if target is not None:
        python:
            _total = 0
            for _hit in range(archie_hits):
                if getattr(target, "current_hp", 0) <= 0:
                    break
                _dmg = store.pers_dict["Арчи"].calculate_dmg(target)
                if store.pers_dict["Арчи"].popal == 1:
                    _total += _dmg
                    add_attack_result("Арчи", target.name, _dmg, bool(store.is_crit), "normal")
                    # «Эй! Я здесь!» ур.4: каждый удар может поднять танк.
                    archie_on_hit_landed()
                    # «Травмирующие удары» ур.6: замедление атаки на 3%.
                    archie_apply_trauma_slow(target)
                # −5% брони с шансом 25%.
                if renpy.random.random() < 0.25:
                    apply_enemy_weaken_armor(target, 0.05)
            # «Быстрые комбинации» ур.3: шанс сложить печать.
            archie_try_combo_seal()
            store.archie_combo_damage = _total
        
        if store.archie_combo_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    $ archie_try_extra_turn()
    
    call screen choose_attacker_screen()

label archie_atk2_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «По полочкам» ур.1: 3 удара — внизу, по туловищу и голове.
    #  1 удар: шанс (магия) повалить врага
    #  2 удар: шанс (магия) получить 3 истощения
    #  3 удар: шанс (магия) замедлить противника на 15%
    # ========================================================================
    if target is not None:
        $ archie_magic_value = float(getattr(store.pers_dict["Арчи"], "magic", 0)) / 100.0
        python:
            _total = 0
            for _hit in range(3):
                if getattr(target, "current_hp", 0) <= 0:
                    break
                _dmg = store.pers_dict["Арчи"].calculate_dmg(target)
                if store.pers_dict["Арчи"].popal == 1:
                    _total += _dmg
                    add_attack_result("Арчи", target.name, _dmg, bool(store.is_crit), "normal")
                    archie_on_hit_landed()
            store.archie_combo_damage = _total
        
        # 1 удар: повалить.
        if renpy.random.random() < archie_magic_value:
            $ apply_enemy_stun(target, 1)
        # 2 удар: 3 истощения (atk_debuff).
        if renpy.random.random() < archie_magic_value:
            $ apply_enemy_atk_debuff(target, 3)
        # 3 удар: замедление на 15%.
        if renpy.random.random() < archie_magic_value:
            $ target.speed = float(getattr(target, "speed", 1.0)) * 0.85
        
        if store.archie_combo_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archie_atk3_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Удары богомола» ур.2: 3 удара с шансом кровотечения и −3% брони,
    # и минус 3 магии.
    # ========================================================================
    if target is not None:
        python:
            _total = 0
            for _hit in range(3):
                if getattr(target, "current_hp", 0) <= 0:
                    break
                _dmg = store.pers_dict["Арчи"].calculate_dmg(target)
                if store.pers_dict["Арчи"].popal == 1:
                    _total += _dmg
                    add_attack_result("Арчи", target.name, _dmg, bool(store.is_crit), "normal")
                    archie_on_hit_landed()
                    # Кровотечение и −3% брони.
                    apply_enemy_bleeding(target, 1)
                    apply_enemy_weaken_armor(target, 0.03)
                    # Минус 3 магии.
                    target.bonus_magic = float(getattr(target, "bonus_magic", 0.0)) - 0.03
            store.archie_combo_damage = _total
        
        if store.archie_combo_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archie_atk4_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Удар орла» ур.3 (с разбега удар одной ногой): гарантированно откидывает
    # противника в противника сзади, нанося урон 20% от Арчи + урон противника.
    # Если сзади противника нет, то гарантированно выкидывает его на 1 ход
    # из боя («Далеко и надолго!» ур.6 — на 1 ход дольше).
    # ========================================================================
    if target is not None:
        $ dmg = store.pers_dict["Арчи"].calculate_dmg(target)
        $ add_attack_result("Арчи", target.name, dmg, bool(store.is_crit), "normal")
        $ archie_on_hit_landed()
        
        python:
            # Ищем живого противника «сзади» (любого другого живого врага).
            _others = [e for e in (store.enemies or {}).values()
                       if e is not None and e is not target and getattr(e, "current_hp", 0) > 0]
            if _others:
                _behind = renpy.random.choice(_others)
                _bonus = max(1, int(float(getattr(store.pers_dict["Арчи"], "atk", 0)) * 0.20))
                _behind.current_hp = max(0, _behind.current_hp - _bonus)
                add_attack_result("Арчи", _behind.name, _bonus, False, "normal")
                renpy.log("[Арчи][Удар орла] {} откинут в {}".format(target.name, _behind.name))
            else:
                # Сзади никого нет — выкидываем из боя на 1(+1) ход.
                apply_enemy_stun(target, 1 + archie_eagle_extra_turn())
                renpy.log("[Арчи][Удар орла] {} выкинут из боя".format(target.name))
        
        with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archie_atk5_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Апперкот» ур.4: удар, который имеет шанс (крит-шанс Арчи) опрокинуть
    # противника и шанс, равный магии Арчи, наложить −20% атаки.
    # ========================================================================
    if target is not None:
        $ dmg = store.pers_dict["Арчи"].calculate_dmg(target)
        $ add_attack_result("Арчи", target.name, dmg, bool(store.is_crit), "normal")
        $ archie_on_hit_landed()
        $ archie_critrate = float(getattr(store.pers_dict["Арчи"], "critrate", 0))
        $ archie_magic_value = float(getattr(store.pers_dict["Арчи"], "magic", 0)) / 100.0
        
        if renpy.random.random() < archie_critrate:
            $ apply_enemy_stun(target, 1)
        if renpy.random.random() < archie_magic_value:
            $ apply_enemy_weaken_attack(target, 0.20)
        
        with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archie_atk6_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Ураган» ур.5: 5 атак с шансом крит-шанса выкинуть противника из боя
    # на 1 ход + магия/10 («Далеко и надолго!» ур.6 добавляет 1 ход).
    # ========================================================================
    if target is not None:
        $ archie_critrate = float(getattr(store.pers_dict["Арчи"], "critrate", 0))
        $ archie_extra = 1 + archie_eagle_extra_turn()
        python:
            _total = 0
            for _hit in range(5):
                if getattr(target, "current_hp", 0) <= 0:
                    break
                _dmg = store.pers_dict["Арчи"].calculate_dmg(target)
                if store.pers_dict["Арчи"].popal == 1:
                    _total += _dmg
                    add_attack_result("Арчи", target.name, _dmg, bool(store.is_crit), "normal")
                    archie_on_hit_landed()
                if renpy.random.random() < archie_critrate:
                    apply_enemy_stun(target, archie_extra)
            store.archie_combo_damage = _total
        
        if store.archie_combo_damage > 0:
            with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archie_atk7_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Мягкая ладонь» ур.6: 0.3 от урона, но отнимает у всех противников
    # −40% от текущей магии. «Нежное перенаправление силы» ур.7: после удара
    # даёт случайному союзнику 40% магии Арчи.
    # ========================================================================
    $ store.archie_soft_palm_bonus = 0.0
    
    if target is not None:
        $ original_atk = store.pers_dict["Арчи"].bonus_atk
        $ store.pers_dict["Арчи"].bonus_atk *= 0.30
        $ dmg = store.pers_dict["Арчи"].calculate_dmg(target)
        $ store.pers_dict["Арчи"].bonus_atk = original_atk
        $ add_attack_result("Арчи", target.name, dmg, bool(store.is_crit), "normal")
        $ archie_on_hit_landed()
        
        python:
            # Отнимаем у ВСЕХ живых противников −40% текущей магии.
            for _enemy in (store.enemies or {}).values():
                if _enemy is None or getattr(_enemy, "current_hp", 0) <= 0:
                    continue
                _enemy.bonus_magic = float(getattr(_enemy, "bonus_magic", 0.0)) - 0.40
            renpy.log("[Арчи][Мягкая ладонь] магия всех противников −40%")
        
        # «Нежное перенаправление силы» ур.7.
        $ archie_on_soft_palm()
        with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archie_atk8_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Oma yi wa mou» ур.8: наносит 10 ударов, снижая случайные
    # характеристики на 10%. Одноразовая.
    # ========================================================================
    if target is not None:
        python:
            _total = 0
            _fields = ("bonus_atk", "bonus_def", "bonus_magic", "bonus_dmgchance",
                       "bonus_critrate", "bonus_crit", "bonus_tank")
            for _hit in range(10):
                if getattr(target, "current_hp", 0) <= 0:
                    break
                _dmg = store.pers_dict["Арчи"].calculate_dmg(target)
                if store.pers_dict["Арчи"].popal == 1:
                    _total += _dmg
                    add_attack_result("Арчи", target.name, _dmg, bool(store.is_crit), "normal")
                    archie_on_hit_landed()
                # Снижаем случайную характеристику на 10%.
                _field = renpy.random.choice(_fields)
                _value = float(getattr(target, _field, 0) or 0)
                setattr(target, _field, _value * 0.90)
            store.archie_combo_damage = _total
            renpy.log("[Арчи][Oma yi wa mou] суммарный урон {}".format(_total))
        
        with crit_vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

# ========================================================================
# МАГИЯ АРЧИ
# ========================================================================

label archiemag1_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Ладони чакры» ур.1: каждый удар наносит 2 стака 2 случайных дебаффов
    # врагу или 3 стака 3 случайных баффов союзнику.
    # Длится 1 ход + текущая магия/10. При ударе по союзнику урон режется,
    # нанося 25% от максимума.
    # ========================================================================
    $ archie_duration = 1 + int(float(getattr(store.pers_dict["Арчи"], "magic", 0)) / 10.0)
    $ store.archie_chakra_turns = archie_duration
    
    if target is not None:
        $ is_ally_target = getattr(target, "name", None) in (getattr(store, "pers_dict", {}) or {})
        if is_ally_target:
            # Союзник: 3 стака 3 случайных баффов.
            python:
                _buffs = ("def_debuff", "magic_debuff", "accuracy_debuff")
                for _field in _buffs:
                    target_deb = int(getattr(target, _field, 0) or 0)
                    setattr(target, _field, target_deb - 3)
                renpy.log("[Арчи][Ладони чакры] союзник {}: баффы x3".format(target.name))
        else:
            # Враг: 2 стака 2 случайных дебаффов.
            python:
                _debuffs = ("atk_debuff", "critrate_debuff", "critdmg_debuff")
                for _field in renpy.random.sample(_debuffs, 2):
                    _val = int(getattr(target, _field, 0) or 0)
                    setattr(target, _field, _val + 2)
                renpy.log("[Арчи][Ладони чакры] враг {}: дебаффы x2".format(target.name))
    
    $ renpy.notify("Ладони чакры активны %d ход(ов)" % archie_duration)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag2_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Очищение Ци» ур.1: снимает с себя 2 случайных дебаффа/штрафа к
    # характеристикам и все баффы (если они есть) с Арчи. Чем больше стаков
    # дебаффов, тем больше откат.
    # «Новые каналы энергии» ур.8: изменяет на 1 дебафф/штраф больше.
    # ========================================================================
    $ archie_cleanse_count = 2 + archie_channels_extra()
    $ archie_obj = store.pers_dict["Арчи"]
    
    python:
        _active = [f for f in ("atk_debuff", "def_debuff", "magic_debuff",
                               "accuracy_debuff", "critrate_debuff", "critdmg_debuff",
                               "tank_debuff", "bloodshed_debuff", "prone_debuff")
                   if int(getattr(archie_obj, f, 0) or 0) != 0]
        _removed = 0
        for _field in _active[:archie_cleanse_count]:
            setattr(archie_obj, _field, 0)
            _removed += 1
        renpy.log("[Арчи][Очищение Ци] снято {} дебаффов".format(_removed))
        store.archie_current_cd = _removed
    
    with vpunch
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag3_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Печати ниндзюцу» ур.2: складывает печати руками, получая 20% к
    # случайной характеристике 3 раза.
    # ========================================================================
    python:
        _fields = ("bonus_atk", "bonus_def", "bonus_magic", "bonus_dmgchance",
                   "bonus_critrate", "bonus_crit")
        _archie = store.pers_dict["Арчи"]
        for _seal in range(3):
            _field = renpy.random.choice(_fields)
            _value = float(getattr(_archie, _field, 0) or 0)
            if _field in ("bonus_atk", "bonus_def", "bonus_magic") and _value == 0:
                _value = 1.0
            setattr(_archie, _field, _value * 1.20)
            renpy.log("[Арчи][Печати ниндзюцу] {} +20%".format(_field))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag4_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Укрепление мышц» ур.3: ставит Арчи в защитную стойку и накладывает
    # 1 щит. «Твёрдые мускулы» ур.4: шанс = магия наложить второй щит.
    # ========================================================================
    $ archie_obj = store.pers_dict["Арчи"]
    $ archie_obj.shield = int(getattr(archie_obj, "shield", 0) or 0) + 1
    $ archie_obj.defend_stance = 1
    $ archie_try_muscle_shield()
    $ renpy.notify("Арчи: защитная стойка, щит +1")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    $ archie_try_extra_turn()
    
    call screen choose_attacker_screen()

label archiemag5_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Рывок» ур.4: увеличивает скорость души при уворотах на 12%.
    # «Движение жизнь!» ур.5: рывок сбрасывает с себя полностью случайный
    # дебафф с шансом, равным магии Арчи.
    # Скорость души — общая боевая переменная store.soul_speed,
    # которая ограничивается через clamp_soul_speed.
    # ========================================================================
    $ store.soul_speed = store.clamp_soul_speed(getattr(store, "soul_speed", 6) + 0.12 * 10)
    $ archie_on_dash()
    $ renpy.notify("Арчи: рывок, скорость души +12%")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag6_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Режим храбрости» ур.4: позволяет душе в следующий ход двигаться
    # рывками через пули противника, уклоняясь от них.
    # Доступно 3 заряда (на 6 ур. — 4, на 8 ур. — 5).
    # «Быстрое восстановление» ур.9: режим открывается 3 сек, а не 5,
    # а заряды восстанавливаются каждые 9 сек.
    # ========================================================================
    $ store.archie_courage_charges = archie_courage_charges()
    $ store.archie_courage_seconds = archie_courage_seconds()
    $ renpy.notify("Режим храбрости: %d заряда, %d сек" % (
        store.archie_courage_charges, store.archie_courage_seconds))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag7_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Реверс энергии» ур.5: снимает с себя 2 случайных дебаффа/штрафа к
    # характеристикам и все баффы (если они есть) с Арчи и превращает их в
    # положительные. Чем больше стаков дебаффов, тем больше откат.
    # «Новые каналы энергии» ур.8: изменяет на 1 дебафф/штраф больше.
    # ========================================================================
    $ archie_reverse_count = 2 + archie_channels_extra()
    $ archie_obj = store.pers_dict["Арчи"]
    
    python:
        _active = [f for f in ("atk_debuff", "def_debuff", "magic_debuff",
                               "accuracy_debuff", "critrate_debuff", "critdmg_debuff",
                               "tank_debuff")
                   if int(getattr(archie_obj, f, 0) or 0) != 0]
        _converted = 0
        for _field in _active[:archie_reverse_count]:
            _val = int(getattr(archie_obj, _field, 0) or 0)
            # Превращаем дебафф в противоположный по знаку (положительный).
            setattr(archie_obj, _field, -abs(_val))
            _converted += 1
        renpy.log("[Арчи][Реверс энергии] обращено {} дебаффов".format(_converted))
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag8_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Травмирующие удары» ур.6: следующие 2 хода + магия/10 каждый удар
    # Арчи будет замедлять атаку противника на 3%.
    # ========================================================================
    $ store.archie_trauma_turns = 2 + int(float(getattr(store.pers_dict["Арчи"], "magic", 0)) / 10.0)
    $ renpy.notify("Травмирующие удары: %d ход(ов)" % store.archie_trauma_turns)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag9_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Вернуть отправителю» ур.7: Арчи в следующие 2 хода не получает урона
    # и возвращает все снаряды противника обратно в него. Шанс попадания и
    # урон равны точности и атаке Арчи.
    # ========================================================================
    $ store.archie_return_turns = 2
    $ renpy.notify("Вернуть отправителю: 2 хода отражения снарядов")
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    
    call screen choose_attacker_screen()

label archiemag10_is_done:
    $ store.pers_dict["Арчи"].turn = 0
    
    hide screen Heroattacks
    
    # ========================================================================
    # «Храбрость!» ур.9: следующие 3 хода весь урон получает Арчи вместо
    # других персонажей, и он получает случайные бонусы и баффы.
    # «Ради других!» ур.10: количество ходов увеличивается до 5.
    # ========================================================================
    $ archie_start_courage()
    
    python:
        _fields = ("bonus_atk", "bonus_def", "bonus_magic", "bonus_dmgchance",
                   "bonus_critrate", "bonus_crit")
        _archie = store.pers_dict["Арчи"]
        for _bonus in range(2):
            _field = renpy.random.choice(_fields)
            _value = float(getattr(_archie, _field, 0) or 0)
            if _field in ("bonus_atk", "bonus_def", "bonus_magic") and _value == 0:
                _value = 1.0
            setattr(_archie, _field, _value * 1.15)
        renpy.log("[Арчи][Храбрость!] активна {} ходов".format(store.archie_courage_turns))
    
    $ renpy.notify("Храбрость! Арчи держит удар %d ходов" % store.archie_courage_turns)
    
    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0
    $ archie_try_extra_turn()
    
    call screen choose_attacker_screen()


# ========================================================================
# СИЛЬВИЯ — ДВИЖЕНИЯ ТАНЦА И ЭФФЕКТЫ
# ========================================================================
#
# Логика хода Сильвии:
#   1) Игрок выбирает одно движение (это и есть её ход).
#   2) Движение добавляется в очередь.
#   3) Оплачивается мана (10% от максимума); пассивка «Пластика и
#      выносливость» (ур.3) может сделать движение бесплатным.
#   4) Проверяется, собралась ли комбинация одного из танцев
#      репертуара. Если да — исполняются эффекты и очередь чистится.
#   5) Если очередь больше не может продолжиться ни в один танец —
#      она тоже чистится, чтобы игрок не копил мусор.
# ========================================================================

label sylvia_movement_is_done:
    $ store.pers_dict["Сильвия"].turn = 0

    hide screen Heroattacks
    hide screen sylvia_movement_screen

    python:
        _sylvia = store.pers_dict["Сильвия"]

        # --- 1) Движение, выбранное игроком -------------------------
        _move = getattr(store, "sylvia_pending_move", None)
        _sylvia.sylvia_pending_move = None
        _dance_to_play = None

        if _move is None:
            renpy.log("Сильвия: движение не выбрано")
        else:
            # --- 0) «Важность исполнения» (ур.1) ---------------------
            # Каждое действие проходит проверку на точность и крит-шанс:
            # провал точности делит эффекты на 2, крит умножает на 1.5.
            # Результат сохраняется и читается эффектами танца.
            sylvia_roll_performance()

            # --- 2) Оплата маны -------------------------------------
            # «Пластика и выносливость» (ур.3) может отменить трату.
            _free = sylvia_roll_free_movement()
            if not _free:
                sylvia_pay_movement_cost()

            # --- 3) Добавление в очередь ----------------------------
            sylvia_push_movement(_move)

            # «Раскрываясь в свете прожекторов»: +2 танка за движение.
            sylvia_spotlight_on_movement()

            # Прогресс открытия уровней + счётчик движений за бой.
            sylvia_on_movement_made()

            # --- 4) Проверка комбинации -----------------------------
            _dance_to_play = sylvia_match_dance()

            if _dance_to_play is None:
                # Комбинация не собрана. Если она больше не может
                # продолжиться в какой-либо танец — очищаем очередь.
                if not sylvia_partial_match_exists():
                    sylvia_clear_queue("комбинация не совпала ни с одним танцем")

            # «Диалог культур» (ур.5) — за каждое выполненное движение.
            sylvia_dialogue_cultures()

    # --- 5) Исполнение эффектов танца ---------------------------------
    if _dance_to_play:
        $ _sylvia_dance_name = sylvia_dance_name(_dance_to_play)
        $ renpy.notify("Танец исполнен: %s" % _sylvia_dance_name)

        python:
            sylvia_run_dance_effect(_dance_to_play)
            sylvia_mark_dance_used(_dance_to_play)
            # После исполнения танца очередь сбрасывается.
            sylvia_clear_queue("танец исполнен")

    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    # --- 6) Завершение хода Сильвии -----------------------------------
    python:
        # Восстановление HP за пустые позиции очереди аппетита.
        sylvia_end_turn_food_regen()

        # Тик дебаффа «Антракт» (1 стак в конце хода).
        sylvia_tick_entracte_end()

        # Тик «Тени Солора», если она активна.
        sylvia_solor_tick()

    # «Пластика требует диеты»: шанс второго хода за здоровую еду.
    if sylvia_roll_second_turn():
        $ store.pers_dict["Сильвия"].turn = 1
        $ renpy.notify("Пластика требует диеты: Сильвия получает второй ход!")
    else:
        # Сброс флага «Своей очереди» на следующий раунд.
        $ store.pers_dict["Сильвия"].sylvia_initiative_applied = False

    call screen choose_attacker_screen()


# ========================================================================
# ФАБРИ: ИСПОЛНЕНИЕ ПРИЗЫВА И МАГИИ ФАМИЛЬЯРОВ
# ========================================================================
# Слой-контракт (см. _FABRI_SPEC.md, раздел 9): вся логика живёт в
# 1_ПЕРС_ПАССИВКИ_ФАБРИ.rpy. Здесь только:
#   1) проверка, что выбранная способность действительно пришла в
#      attackindex (иначе не запускаем ничего);
#   2) один вызов fabri_perform_summon / fabri_perform_familiar_magic;
#   3) завершение хода и тот же переход, что у соседних лейблов.
#
# ОПЛАТА МАНЫ ЗДЕСЬ НЕ ДЕЛАЕТСЯ: общий путь Heroperformsturn ->
# pay_ability_cost уже списал стоимость, а fabri_perform_* намеренно
# не списывает ману повторно.
#
# УЧЁТ ДЕЙСТВИЙ ЗДЕСЬ ТОЖЕ НЕ ДЕЛАЕТСЯ: register_action_for_current
# уже вызван в Heroperformsturn (1_ПЕРС_АТАКИ_2.rpy, стр. 119) для
# любой способности, включая способности Фабри.
#
# turn = 0 выставляется ДО исполнения эффекта — как в izzymag*/
# sedric_* и в sylvia_movement_is_done: без этого герой ходил бы
# бесконечно (известная проблема проекта).
# ========================================================================

label fabri_summon_is_done:
    # Призыв мог прийти только из меню атаки: 4 призыва + «защита_Фабри».
    # turn сбрасывается и в ветке ошибки: иначе Фабри зациклилась бы.
    if attackindex not in ("Призвать М-ра Панцыря",
                           "Призвать М-с Пёрышко",
                           "Призвать М-с Морковку",
                           "Призвать М-с Манки"):
        $ store.pers_dict["Фабри"].turn = 0
        $ renpy.log("[Фабри] fabri_summon_is_done: неизвестный призыв {}".format(store.attackindex))
        jump afterheroattack

    $ store.pers_dict["Фабри"].turn = 0

    hide screen Heroattacks
    hide screen choose_attack_screen
    hide screen turntarget
    hide screen attack_name_display
    hide screen attack_description

    $ fabri_summon_result = fabri_perform_summon(store.attackindex)

    if fabri_summon_result:
        $ renpy.notify(fabri_summon_result)

    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    call screen choose_attacker_screen()


label fabri_familiar_magic_is_done:
    # Магия фамильяров: 16 способностей из FABRI_MAGIC_TAGS.
    if attackindex not in ("Спрятаться",
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
        $ store.pers_dict["Фабри"].turn = 0
        $ renpy.log("[Фабри] fabri_familiar_magic_is_done: неизвестная магия {}".format(store.attackindex))
        jump afterheroattack

    $ store.pers_dict["Фабри"].turn = 0

    hide screen Heroattacks
    hide screen choose_magic_screen
    hide screen turntarget
    hide screen attack_name_display
    hide screen attack_description

    # fabri_perform_familiar_magic сам проверяет, призван ли нужный
    # фамильяр, и вернёт None, если магия недоступна.
    $ fabri_magic_result = fabri_perform_familiar_magic(store.attackindex)

    if fabri_magic_result:
        $ renpy.notify(fabri_magic_result)

    show screen heroes_attacked_visual
    $ renpy.pause(2, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    call screen choose_attacker_screen()

