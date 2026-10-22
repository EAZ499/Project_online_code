# ============================================================================
# СИСТЕМА ДЕБАФОВ И БАФОВ
# ============================================================================
# Этот файл содержит функции для применения и обработки дебафов/бафов персонажей

# Переменные для отслеживания дебафов персонажей
default heroes_debuff_info = {}
# default battlenumber = None  # Закомментировано, так как уже определено в 2_ИНТЕРФЕЙС_БОЯ.rpy

# НОВАЯ СИСТЕМА: Множественные атаки
default multiple_attacks_results = {}  # Словарь для хранения результатов множественных атак
default current_round_attacks = []     # Список атак в текущем раунде

init  python:
    
    # ========================================================================
    # ФУНКЦИЯ ПРИМЕНЕНИЯ ДЕБАФОВ В НАЧАЛЕ РАУНДА
    # ========================================================================
    def apply_debuffs_at_round_end():
        """
        Применяет эффекты всех дебафов в начале раунда врага.
        Вызывается перед атакой врагов.
        """
        # Используем централизованную функцию для инициализации team_manager
        store.ensure_team_manager()
            
        store.heroes_debuff_info = {}
        # Очищаем результаты атак для нового раунда
        store.multiple_attacks_results = {}
        store.current_round_attacks = []
        
        for char_name in store.team_manager.team_slots:
            if char_name and char_name in store.characters:
                char = store.pers_dict[char_name]
                
                # Пропускаем мертвых персонажей
                if char.current_hp <= 0:
                    continue
                
                else:

                    # ============================================================
                    # 1. КРОВОТЕЧЕНИЕ: -5% от макс хп за каждый уровень дебафа
                    # ============================================================
                    if char.bloodshed_debuff > 0:
                        # «Голубая кровь»: Азриель теряет вдвое больше от кровотечения.
                        bleed_damage = int(char.max_hp * 0.05 * (char.bloodshed_debuff)
                                           * azri_bleed_multiplier(char))
                        old_hp = char.current_hp
                        char.current_hp = max(0, char.current_hp-bleed_damage)
                        char.damage_gain_for_vis = bleed_damage
                        char.got_crit_for_visual = 0
                        update_swoon_pending_for_visual(char, old_hp)
                        char.bloodshed_debuff -= 1
                        
                       
                    elif char.bloodshed_debuff < 0:
                        bleed_damage = int(char.max_hp * 0.05 * (char.bloodshed_debuff))
                        old_hp = char.current_hp
                        char.current_hp = max(0, char.current_hp + bleed_damage)
                        # Приближаем к нулю
                        char.bloodshed_debuff += 1
                        char.damage_gain_for_vis = bleed_damage
                        char.got_crit_for_visual = 0
                        update_swoon_pending_for_visual(char, old_hp)

                    # Кровотечение могло добить Криса — проверяем «Желание жить».
                    kris_try_wish_to_live(char)
                    # «Рука помощи» Азриеля поднимает упавшего союзника.
                    azri_try_helping_hand(char)

                    
                    # ============================================================
                    # 2. PRONE: Персонаж лежит, не ходит, +10 к tank
                    # ============================================================
                    if char.prone_debuff != 0:
                        char.turn = 0  # Персонаж не может ходить
                        # Приближаем к нулю
                        if char.prone_debuff < 0:
                            char.prone_debuff += 1
                        elif char.prone_debuff > 0:
                            char.prone_debuff -= 1
                    else:
                        # Восстанавливаем ход, если prone закончился
                        char.turn = 1

        # Конец хода: «Привыкший к общажной жизни» — вредная еда даёт
        # −2 к дебафу кровотечения и +1 комфорт.
        kris_apply_junk_food_end_of_turn()


    def apply_debuffs_at_round_start():
        """
        Применяет эффекты всех дебафов в начале раунда врага.
        Вызывается перед атакой врагов.
        """
        # Используем централизованную функцию для инициализации team_manager
        store.ensure_team_manager()
            
        #store.heroes_debuff_info = {}
        # Очищаем результаты атак для нового раунда
        #store.multiple_attacks_results = {}
        #store.current_round_attacks = []
        
        for char_name in store.team_manager.team_slots:
            if char_name and char_name in store.characters:
                char = store.pers_dict[char_name]
                
                # Пропускаем мертвых персонажей
                if char.current_hp <= 0:
                    continue

                # ============================================================
                # 3. АТАКА ДЕБАФ: Истощение/Бодрость
                # ============================================================
                if char.atk_debuff != 0:
                    # Для персонажей дебаффы учитываются через atk_debuff_var в свойствах класса.
                    # Здесь уменьшаем только длительность эффекта, не трогая bonus_atk/bonus_crit.
                    # Приближаем к нулю
                    if char.atk_debuff < 0:
                        char.atk_debuff += 1
                    elif char.atk_debuff > 0:
                        char.atk_debuff -= 1
                    
                    # ============================================================
                    # 4. ЗАЩИТА ДЕБАФ: Вдохновение/Печаль
                    # ============================================================
                if char.def_debuff != 0:
                        # Для персонажей защита уже учитывает def_debuff_var в формуле defense.
                        # Здесь уменьшаем только длительность эффекта, не трогая bonus_def.
                        # Приближаем к нулю
                        if char.def_debuff < 0:
                            char.def_debuff += 1
                        elif char.def_debuff > 0:
                            char.def_debuff -= 1
                    
                    # ============================================================
                    # 5. МАГИЯ ДЕБАФ: Просвещение/Помутнение
                    # ============================================================
                if char.magic_debuff != 0:
                        # Для персонажей магия уже учитывает magic_debuff_var в формуле magic.
                        # Сохраняем только побочный эффект на MP и уменьшаем длительность дебаффа.
                        #if char.magic_debuff < 0:  # Просвещение
                        #    mp_loss = -int(char.max_mp * 0.05 * abs(char.magic_debuff))
                        #    char.current_mp = max(0, char.current_mp - mp_loss)
                        #elif char.magic_debuff > 0:  # Помутнение
                        #    mp_gain = -int(char.max_mp * 0.05 * char.magic_debuff)
                        #    char.current_mp = min(char.max_mp, char.current_mp + mp_gain)
                        # Приближаем к нулю
                        if char.magic_debuff < 0:
                            char.magic_debuff += 1
                        elif char.magic_debuff > 0:
                            char.magic_debuff -= 1
                    
                    # ============================================================
                    # 6. ТОЧНОСТЬ ДЕБАФ: Концентрация/Страх
                    # ============================================================
                if char.accuracy_debuff != 0:
                        # Для персонажей точность уже учитывает accuracy_debuff_var в свойстве dmgchance.
                        # Здесь уменьшаем только длительность эффекта.
                        # Приближаем к нулю
                        if char.accuracy_debuff < 0:
                            char.accuracy_debuff += 1
                        elif char.accuracy_debuff > 0:
                            char.accuracy_debuff -= 1
                    
                    # ============================================================
                    # 7. КРИТ ШАНС ДЕБАФ: Удача/Сглаз
                    # ============================================================
                if char.critrate_debuff != 0:
                        # Для персонажей шанс крита уже учитывает critrate_debuff_var.
                        # Здесь уменьшаем только длительность эффекта.
                        # Приближаем к нулю
                        if char.critrate_debuff < 0:
                            char.critrate_debuff += 1
                        elif char.critrate_debuff > 0:
                            char.critrate_debuff -= 1
                    
                    # ============================================================
                    # 8. КРИТ УРОН ДЕБАФ: безразличие/злость
                    # ============================================================
                if char.critdmg_debuff != 0:
                        # Для персонажей крит-урон уже учитывает critdmg_debuff_var.
                        # Здесь уменьшаем только длительность эффекта.
                        # Приближаем к нулю
                        if char.critdmg_debuff < 0:
                            char.critdmg_debuff += 1
                        elif char.critdmg_debuff > 0:
                            char.critdmg_debuff -= 1
        
                    
                    # ============================================================
                    # 9. ОВЕРХИЛ БАФ
                    # ============================================================
        
                    # ============================================================
                    # 10. СВЕРХКРИТ БАФ 
                    # ============================================================

                    # ============================================================
                    # 11. Танк бафф: скрытый/уязвимый
                    # ============================================================


                    
                    # Сохраняем информацию о дебафах для отображения
                    #store.heroes_debuff_info[char_name] = debuff_info













        # «Голубая кровь» и «Свита голубых кровей» Азриеля: сброс дебаффов
        # в начале раунда (шанс зависит от уровня персонажей).
        azri_cleanse_round()

    def apply_debuffs_at_round_start_for_char(char):
        """Обновляет дебаффы только одного персонажа."""
        if char is None or getattr(char, "current_hp", 0) <= 0:
            return

        if getattr(char, "bloodshed_debuff", 0) != 0:
            # «Голубая кровь»: вдвое сильнее только урон, не лечение.
            _bleed_mult = azri_bleed_multiplier(char) if char.bloodshed_debuff > 0 else 1.0
            bleed_damage = int(getattr(char, "max_hp", 0) * 0.05 * abs(char.bloodshed_debuff) * _bleed_mult)
            old_hp = char.current_hp
            if char.bloodshed_debuff > 0:
                char.current_hp = max(0, char.current_hp - bleed_damage)
                char.bloodshed_debuff -= 1
            else:
                char.current_hp = max(0, char.current_hp + bleed_damage)
                char.bloodshed_debuff += 1
            char.damage_gain_for_vis = bleed_damage
            char.got_crit_for_visual = 0
            update_swoon_pending_for_visual(char, old_hp)

        # Кровотечение могло добить Криса — проверяем «Желание жить».
        kris_try_wish_to_live(char)
        # «Рука помощи» Азриеля поднимает упавшего союзника.
        azri_try_helping_hand(char)

        if getattr(char, "prone_debuff", 0) != 0:
            char.turn = 0
            if char.prone_debuff < 0:
                char.prone_debuff += 1
            elif char.prone_debuff > 0:
                char.prone_debuff -= 1
        else:
            char.turn = 1

        for debuff_name in (
            "atk_debuff",
            "def_debuff",
            "magic_debuff",
            "accuracy_debuff",
            "critrate_debuff",
            "critdmg_debuff",
        ):
            value = getattr(char, debuff_name, 0)
            if value < 0:
                setattr(char, debuff_name, value + 1)
            elif value > 0:
                setattr(char, debuff_name, value - 1)

    def apply_debuffs_at_round_end_enemies():
        """
        Применяет эффекты всех дебафов в конце раунда для врагов.
        Вызывается после атаки персонажей.
        """

        # Проверяем, что store.enemies существует
        if not hasattr(store, 'enemies') or store.enemies is None:
            renpy.log("ПРЕДУПРЕЖДЕНИЕ: store.enemies не существует или равен None в apply_debuffs_at_round_end_enemies()")
            return
        
        for enemy_name, enemy in store.enemies.items():
            # Пропускаем мертвых врагов
            if enemy.current_hp <= 0:
                continue
            
            else:
                # ============================================================
                # 1. КРОВОТЕЧЕНИЕ: -5% от макс хп за каждый уровень дебафа
                # ============================================================
                if "dummy_prevent_bleeding" in globals() and dummy_prevent_bleeding(enemy):
                    pass
                elif enemy.bloodshed_debuff > 0:
                    bleed_damage = int(enemy.max_hp * 0.05 * abs(enemy.bloodshed_debuff))
                    # Приближаем к нулю
                    old_hp = enemy.current_hp
                    enemy.current_hp = max(0, enemy.current_hp - bleed_damage)
                    
                    enemy.bloodshed_debuff -= 1
                    enemy.damage_gain_for_vis = bleed_damage
                    enemy.got_crit_for_visual = 0
                    update_swoon_pending_for_visual(enemy, old_hp)

                elif enemy.bloodshed_debuff < 0:
                    bleed_damage = int(enemy.max_hp * 0.05 * abs(enemy.bloodshed_debuff))
                    old_hp = enemy.current_hp
                    enemy.current_hp = max(0, enemy.current_hp + bleed_damage)
                    # Приближаем к нулю
                    enemy.bloodshed_debuff += 1
                    enemy.damage_gain_for_vis = bleed_damage
                    update_swoon_pending_for_visual(enemy, old_hp)
                
                # ============================================================
                # 2. PRONE: Враг лежит, не ходит, +10 к tank
                # ============================================================
                if enemy.prone_debuff != 0:
                    enemy.turn = 0  # Враг не может ходить
                    # Приближаем к нулю
                    if enemy.prone_debuff < 0:
                        enemy.prone_debuff += 1
                    elif enemy.prone_debuff > 0:
                        enemy.prone_debuff -= 1
                else:
                    # Восстанавливаем ход, если prone закончился
                    enemy.turn = 1

    def apply_debuffs_at_round_start_enemies():
        """
        Применяет эффекты всех дебафов в начале раунда для врагов.
        Вызывается перед атакой врагов.
        """
        # Проверяем, что store.enemies существует
        if not hasattr(store, 'enemies') or store.enemies is None:
            renpy.log("ПРЕДУПРЕЖДЕНИЕ: store.enemies не существует или равен None в apply_debuffs_at_round_start_enemies()")
            return
        
        for enemy_name, enemy in store.enemies.items():
            # Пропускаем мертвых врагов
            if enemy.current_hp <= 0:
                continue
            
            # ============================================================
            # 3. АТАКА ДЕБАФ: Истощение/Бодрость
            # ============================================================
            if enemy.atk_debuff != 0:
                # Снимаем/восстанавливаем только 1 стак за тик (0.05), затем уменьшаем счётчик на 1.
                if enemy.atk_debuff > 0:  # Истощение (дебафф): возвращаем часть атаки
                    enemy.atk_debuff_var = round(enemy.atk_debuff_var + 0.05, 2)
                elif enemy.atk_debuff < 0:  # Бодрость (бафф): возвращаем к базовому значению
                    enemy.atk_debuff_var = round(max(0.0, enemy.atk_debuff_var - 0.05), 2)
                # Приближаем к нулю
                if enemy.atk_debuff < 0:
                    enemy.atk_debuff += 1
                elif enemy.atk_debuff > 0:
                    enemy.atk_debuff -= 1
            
            # ============================================================
            # 4. ЗАЩИТА ДЕБАФ: Вдохновение/Печаль
            # ============================================================
            if enemy.def_debuff != 0:
                # Снимаем/восстанавливаем только 1 стак за тик (0.05), затем уменьшаем счётчик на 1.
                if enemy.def_debuff > 0:  # Дебафф защиты: возвращаем часть защиты
                    enemy.def_debuff_var = round(enemy.def_debuff_var + 0.05, 2)
                elif enemy.def_debuff < 0:  # Бафф защиты: возвращаем к базовому значению
                    enemy.def_debuff_var = round(max(0.0, enemy.def_debuff_var - 0.05), 2)
                # Приближаем к нулю
                if enemy.def_debuff < 0:
                    enemy.def_debuff += 1
                elif enemy.def_debuff > 0:
                    enemy.def_debuff -= 1

            # ============================================================
            # 5. МАГИЯ ДЕБАФ: Просвещение/Помутнение
            # ============================================================
            if enemy.magic_debuff != 0:
                # Снимаем/восстанавливаем только 1 стак за тик (0.05), затем уменьшаем счётчик на 1.
                if enemy.magic_debuff > 0:  # Дебафф магии: возвращаем часть магии
                    enemy.magic_debuff_var = round(enemy.magic_debuff_var + 0.05, 2)
                elif enemy.magic_debuff < 0:  # Бафф магии: возвращаем к базовому значению
                    enemy.magic_debuff_var = round(max(0.0, enemy.magic_debuff_var - 0.05), 2)
                # Приближаем к нулю
                if enemy.magic_debuff < 0:
                    enemy.magic_debuff += 1
                elif enemy.magic_debuff > 0:
                    enemy.magic_debuff -= 1

            # ============================================================
            # 6. ТОЧНОСТЬ ДЕБАФ: Концентрация/Страх
            # ============================================================
            if enemy.accuracy_debuff != 0:
                # Снимаем/восстанавливаем только 1 стак за тик (0.05), затем уменьшаем счётчик на 1.
                accuracy_shift = 0.05 if enemy.accuracy_debuff > 0 else -0.05
                enemy.accuracy_debuff_var = round(enemy.accuracy_debuff_var + accuracy_shift, 2)
                # Приближаем к нулю
                if enemy.accuracy_debuff < 0:
                    enemy.accuracy_debuff += 1
                elif enemy.accuracy_debuff > 0:
                    enemy.accuracy_debuff -= 1

            # ============================================================
            # 7. КРИТ ШАНС ДЕБАФ: Удача/Сглаз
            # ============================================================
            if enemy.critrate_debuff != 0:
                # Снимаем/восстанавливаем только 1 стак за тик (0.05), затем уменьшаем счётчик на 1.
                critrate_shift = +0.05 if enemy.critrate_debuff > 0 else -0.05
                enemy.critrate_debuff_var = round(enemy.critrate_debuff_var + critrate_shift, 2)
                # Приближаем к нулю
                if enemy.critrate_debuff < 0:
                    enemy.critrate_debuff += 1
                elif enemy.critrate_debuff > 0:
                    enemy.critrate_debuff -= 1

            # ============================================================
            # 8. КРИТ УРОН ДЕБАФ: безразличие/гнев
            # ============================================================
            if enemy.critdmg_debuff != 0:
                # Снимаем/восстанавливаем только 1 стак за тик (0.05), затем уменьшаем счётчик на 1.
                critdmg_shift = 0.05 if enemy.critdmg_debuff > 0 else -0.05
                enemy.critdmg_debuff_var = round(enemy.critdmg_debuff_var + critdmg_shift, 2)
                # Приближаем к нулю
                if enemy.critdmg_debuff < 0:
                    enemy.critdmg_debuff += 1
                elif enemy.critdmg_debuff > 0:
                    enemy.critdmg_debuff -= 1

    # ========================================================================
    # ФУНКЦИЯ ПРИМЕНЕНИЯ РЕГЕНЕРАЦИИ HP И МАНЫ
    # ========================================================================
    def apply_hp_and_mana_regen():
        """
        Применяет регенерацию HP и маны ко всем персонажам и врагам.
        Вызывается в начале или конце раунда.
        """
        # Применяем регенерацию для всех персонажей в команде
        if hasattr(store, 'team_manager') and store.team_manager is not None:
            for char_name in store.team_manager.team_slots:
                if char_name and char_name in store.characters:
                    char = store.pers_dict[char_name]
                    
                    # Пропускаем мёртвых персонажей
                    if char.current_hp <= 0:
                        continue
                    
                    # Применяем регенерацию HP
                    hp_regen = char.hpregen
                    if hp_regen > 0:
                        # Если персонаж уже в оверхиле (>100%), реген не срабатывает и оверхил не сбрасывается.
                        if char.current_hp <= char.max_hp:
                            old_hp = char.current_hp
                            char.current_hp = min(char.current_hp + hp_regen, char.max_hp)
                            # Устанавливаем визуальный индикатор восстановления
                            if char.current_hp > old_hp:
                                char.damage_gain_for_vis = -(char.current_hp - old_hp)
                                if char.current_hp > 1:
                                    char.swoon_visual_shown = False
                                    char.swoon_pending_for_visual = False
                    
                    # Применяем регенерацию маны
                    mp_regen = char.manaregen
                    if mp_regen > 0:
                        old_mp = char.current_mp
                        char.current_mp = min(char.current_mp + mp_regen, char.max_mp)
                        # Можно добавить визуальный индикатор для маны если нужно
        
        # Применяем регенерацию для всех врагов
        if hasattr(store, 'enemies') and store.enemies is not None:
            for enemy_name, enemy in store.enemies.items():
                # Пропускаем мёртвых врагов
                if enemy.current_hp <= 0:
                    continue
                    
                # Применяем регенерацию HP врагов
                hp_regen = enemy.hpregen
                if hp_regen > 0:
                    # Если враг уже в оверхиле (>100%), реген не срабатывает и оверхил не сбрасывается.
                    if enemy.current_hp <= enemy.max_hp:
                        old_hp = enemy.current_hp
                        enemy.current_hp = min(enemy.current_hp + hp_regen, enemy.max_hp)
                        # Устанавливаем визуальный индикатор восстановления
                        if enemy.current_hp > old_hp:
                            enemy.damage_gain_for_vis = -(enemy.current_hp - old_hp)
                            if enemy.current_hp > 1:
                                enemy.swoon_visual_shown = False
                                enemy.swoon_pending_for_visual = False
                
                # Применяем регенерацию маны врагов
                mp_regen = enemy.manaregen
                if mp_regen > 0:
                    old_mp = enemy.current_mp
                    enemy.current_mp = min(enemy.current_mp + mp_regen, enemy.max_mp)
    
# ============================================================================
# ЭКРАН ОТОБРАЖЕНИЯ РЕГЕНЕРАЦИИ HP И МАНЫ
# ============================================================================

screen heroes_attacked_visual2():
    zorder 100
    timer 1.0 action Hide("heroes_attacked_visual2")
    
    frame:
        at heroes_attacked_visual_trans
        xsize 1280
        ysize 720
        background None
        
        # Заголовок экрана
        #text "Регенерация" size 35 xalign 0.5 yalign 0.1 color "#ffffff"
        
        # ============================================================
        # VBOX ДЛЯ СОЮЗНИКОВ
        # ============================================================
        if store.team_manager is not None:
            vbox:
                xalign 0.2
                yalign 0.3
                spacing 15
                
                # Информация о персонажах в команде
                for char_name in store.team_manager.team_slots:
                    if char_name and char_name in store.characters:
                        $ char = store.pers_dict[char_name]
                        $ prev_hp_value, prev_mp_value = get_hp_mp_bar_prev_values(char.name, char.current_hp, char.current_mp)
                        $ mp_delta = char.current_mp - prev_mp_value
                        
                        if char.current_hp > 0:
                            # Получаем значения регенерации
                            $ hp_regen = char.hpregen
                            $ mp_regen = char.manaregen
                            
                            hbox:
                                spacing 10
                                
                                # Имя персонажа
                                text "[char_name]:" size 25 color "#ffffff" min_width 120
                                
                                # Регенерация HP (зелёный)
                                if hp_regen > 0:
                                    text ("{font=determination.otf}+[hp_regen] HP{/font}") style "damage_text" size 30 color "#00ff00" xalign 0.5 at damage_gradient_green
                                elif hp_regen < 0:
                                    text ("{font=determination.otf}[hp_regen] HP{/font}") style "damage_text" size 30 color "#ff0000" xalign 0.5 at damage_gradient_green
                                
                                # Регенерация MP (синий)
                                if mp_regen > 0:
                                    text ("{font=determination.otf}+[mp_regen] MP{/font}") style "damage_text" size 30 color "#00aaff" xalign 0.5 at damage_gradient_cyan
                                elif mp_regen < 0:
                                    text ("{font=determination.otf}[mp_regen] MP{/font}") style "damage_text" size 30 color "#0000ff" xalign 0.5 at damage_gradient_cyan
        
        # ============================================================
        # VBOX ДЛЯ ВРАГОВ
        # ============================================================
        if battlenumber:
            vbox:
                xalign 0.95
                yalign 0.3
                spacing 15
                
                # Заголовок врагов
                #text "Регенерация врагов" size 30 xalign 0.5 yalign 0.1 color "#ff0000"
                
                # Получаем список врагов для текущего боя
                $ active_enemies = get_active_enemies()
                
                for enemy_name in active_enemies:
                    if hasattr(store, 'enemies') and store.enemies and enemy_name in store.enemies:
                        $ enemy = store.enemies[enemy_name]
                        
                        if enemy.current_hp > 0:
                            # Получаем значения регенерации
                            $ hp_regen = enemy.hpregen
                            $ mp_regen = enemy.manaregen
                            
                            hbox:
                                spacing 10
                                
                                # Имя врага
                                text "[enemy.name]:" size 25 color "#ffffff" min_width 120
                                
                                # Регенерация HP (зелёный)
                                if hp_regen > 0:
                                    text ("{font=determination.otf}+[hp_regen] HP{/font}") style "damage_text" size 30 color "#00ff00" xalign 0.5 at damage_gradient_green
                                elif hp_regen < 0:
                                    text ("{font=determination.otf}[hp_regen] HP{/font}") style "damage_text" size 30 color "#ff0000" xalign 0.5 at damage_gradient_green
                                
                                # Регенерация MP (синий)
                                if mp_regen > 0:
                                    text ("{font=determination.otf}+[mp_regen] MP{/font}") style "damage_text" size 30 color "#00aaff" xalign 0.5 at damage_gradient_cyan
                                elif mp_regen < 0:
                                    text ("{font=determination.otf}[mp_regen] MP{/font}") style "damage_text" size 30 color "#0000ff" xalign 0.5 at damage_gradient_cyan



# ============================================================================
# ФУНКЦИЯ УСТАНОВКИ ФЛАГОВ ПОЛУЧЕНИЯ ДЕБАФОВ ДЛЯ ВСЕХ ПЕРСОНАЖЕЙ И ВРАГОВ
# ============================================================================
init python:
    def clear_swoon_pending_for_visual(entity):
        """
        Сбрасывает флаг ожидания показа Swoon для конкретной цели.
        """
        if entity is not None:
            entity.swoon_pending_for_visual = False
            entity.swoon_display_active = False
            if getattr(entity, "current_hp", 0) > 1:
                entity.swoon_visual_shown = False

    def update_swoon_pending_for_visual(entity, old_hp):
        """
        Помечает текущий визуальный эффект как смертельный,
        только если цель была жива до получения урона и умерла после него.
        """
        if entity is None:
            return

        is_fatal_hit = old_hp > 0 and getattr(entity, "current_hp", 0) <= 0

        if is_fatal_hit:
            entity.swoon_visual_shown = False
            entity.swoon_display_active = True
        elif old_hp > 1:
            entity.swoon_visual_shown = False
            entity.swoon_display_active = False

        entity.swoon_pending_for_visual = is_fatal_hit

    def reset_debuff_flags_for_all():
        """
        Устанавливает флаги получения дебафов в 0 для всех персонажей и врагов.
        Также устанавливает damage_gain_for_vis = -1 для всех.
        """
        # Сброс флагов для всех персонажей
        if hasattr(store, 'pers_dict') and store.pers_dict:
            for char_name, char in store.pers_dict.items():
                # Флаги получения дебафов
                char.bloodshed_debuff_got = 0
                char.prone_debuff_got = 0
                char.atk_debuff_got = 0
                char.def_debuff_got = 0
                char.magic_debuff_got = 0
                char.accuracy_debuff_got = 0
                char.critrate_debuff_got = 0
                char.critdmg_debuff_got = 0
                char.tank_debuff_got = 0
                char.overheal_debuff_got = 0
                
                # Сброс урона для визуализации
                char.damage_gain_for_vis = -1
                char.mp_delta = 0
                char.swoon_pending_for_visual = False
                char.swoon_display_active = False
                if getattr(char, "current_hp", 0) > 1:
                    char.swoon_visual_shown = False
        
        # Сброс флагов для всех врагов
        if hasattr(store, 'enemies') and store.enemies:
            for enemy_name, enemy in store.enemies.items():
                # Флаги получения дебафов
                enemy.bloodshed_debuff_got = 0
                enemy.prone_debuff_got = 0
                enemy.atk_debuff_got = 0
                enemy.def_debuff_got = 0
                enemy.magic_debuff_got = 0
                enemy.accuracy_debuff_got = 0
                enemy.critrate_debuff_got = 0
                enemy.critdmg_debuff_got = 0
                enemy.tank_debuff_got = 0
                enemy.overheal_debuff_got = 0
                
                # Сброс урона для визуализации
                enemy.damage_gain_for_vis = -1
                enemy.mp_delta = 0
                enemy.swoon_pending_for_visual = False
                enemy.swoon_display_active = False
                if getattr(enemy, "current_hp", 0) > 1:
                    enemy.swoon_visual_shown = False
        
        renpy.log("Флаги получения дебафов сброшены для всех персонажей и врагов!")

    def normalize_current_attacker_name(attacker):
        """
        Возвращает имя текущего активного героя независимо от того,
        хранится ли current_attacker как объект персонажа или как индекс.
        """
        if attacker is None:
            return None

        if hasattr(attacker, "name"):
            return attacker.name

        attacker_party_order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"]
        if isinstance(attacker, int) and 0 < attacker <= len(attacker_party_order):
            return attacker_party_order[attacker - 1]

        return None

    def get_hero_visual_offsets(char, slot_index, is_enemy_turn):
        """
        Возвращает смещения overlay-визуала героя.
        Позиция зависит от индекса героя в активной команде.
        Во время хода врага активный герой не выделяется дополнительным смещением.
        """
        # Эти значения повторяют offset'ы hbox со спрайтами героев
        # в 1_ВЫБОР_ЦЕЛИ_СПРАЙТЫ.rpy:
        # offset_x = i * (-50) - 32
        # offset_y = i * (-90 - 32) + 90
        base_x = slot_index * (-48) 
        base_y = slot_index * (+32) 

        if is_enemy_turn:
            return base_x, base_y

        # Смещаем overlay только пока герой действительно выдвинут вперёд.
        # Иначе старый current_attacker может визуально "держать" его в центре.
        if getattr(char, "step_forward", 0) != 1:
            return base_x, base_y

        active_attacker_name = normalize_current_attacker_name(getattr(store, "current_attacker", None))
        if active_attacker_name != getattr(char, "name", None):
            return base_x, base_y

        active_step_offsets = [55, 105, 160, 210]
        step_offset_x = active_step_offsets[slot_index] if 0 <= slot_index < len(active_step_offsets) else 0
        return base_x + step_offset_x, base_y

# ============================================================================
# ФУНКЦИЯ СБРОСА ВСЕХ ДЕБАФОВ
# ============================================================================
init python:
    def reset_all_debuffs():
        """Сбрасывает все дебафы всех персонажей"""
        for char_name, char in store.characters.items():
            char.bloodshed_debuff = 0
            char.prone_debuff = 0
            char.atk_debuff = 0
            char.def_debuff = 0
            char.magic_debuff = 0
            char.accuracy_debuff = 0
            char.critrate_debuff = 0
            char.critdmg_debuff = 0
            char.next_attack_damage_multiplier = 1.0
            # Восстанавливаем ход
            if char.turn == 0:
                char.turn = 1
        
        renpy.log("Все дебафы сброшены!")
        
        
    def add_attack_result(attacker_name, target_name, damage, is_crit=False, attack_type="normal"):
        """
        Добавляет результат атаки в систему множественных атак.
        
        Args:
            attacker_name (str): Имя атакующего
            target_name (str): Имя цели
            damage (int): Нанесенный урон
            is_crit (bool): Был ли критический удар
            attack_type (str): Тип атаки ("normal", "magic", "enemy")
        """
        if target_name not in store.multiple_attacks_results:
            store.multiple_attacks_results[target_name] = []
        
        attack_result = {
            'attacker': attacker_name,
            'damage': damage,
            'is_crit': is_crit,
            'attack_type': attack_type,
            'timestamp': len(store.current_round_attacks)
        }
        
        store.multiple_attacks_results[target_name].append(attack_result)
        store.current_round_attacks.append(attack_result)

        # «Рвущиеся швы»: крит по манекену снижает его бонусную защиту
        if is_crit and "dummy_on_crit" in globals():
            dummy_on_crit(target_name)

        # «Следы на мече»: если этим ударом Крис добил врага — вечный бонус
        # (+0.25% крит.урона и +0.15% атаки за каждого добитого).
        kris_register_kill_from_attack(attacker_name, target_name)

        # «Расследование дела» Кловера: любой урон, нанесённый кем-либо кроме
        # самого Кловера, заполняет шкалу виновного цели. Убийство — сразу 100%.
        # Цели под «Меткой разыскиваемого» шкалу не заполняют.
        if attacker_name != "Кловер":
            _victim = (getattr(store, "enemies", {}) or {}).get(target_name)
            if _victim is None:
                _victim = (getattr(store, "pers_dict", {}) or {}).get(target_name)
            if _victim is not None:
                _killed = getattr(_victim, "current_hp", 1) <= 0
                if damage > 0 or _killed:
                    clover_on_damage(_victim, damage, killed=_killed)
    
    def add_multiple_attack_results(attacker_name, targets_data, attack_type="normal"):
        """
        Добавляет результаты атаки по нескольким целям одновременно.
        
        Args:
            attacker_name (str): Имя атакующего
            targets_data (list): Список словарей с данными о целях
                [{'name': 'Цель1', 'damage': 50, 'is_crit': False}, ...]
            attack_type (str): Тип атаки
        """
        for target_data in targets_data:
            add_attack_result(
                attacker_name,
                target_data['name'],
                target_data['damage'],
                target_data.get('is_crit', False),
                attack_type
            )
    
    def get_attacks_for_character(char_name):
        """Возвращает все атаки по указанному персонажу"""
        return store.multiple_attacks_results.get(char_name, [])
    
    def get_total_damage_for_character(char_name):
        """Возвращает общий урон по персонажу"""
        attacks = get_attacks_for_character(char_name)
        return sum(attack['damage'] for attack in attacks)
    



    
    #def show_attack_results():
    #    """Показывает результаты атак в едином экране"""
    #    # Показываем единый экран с союзниками и противниками
    #    renpy.show_screen("heroes_attacked_visual")
    
    #def show_damage_results():
    #    """Показывает только урон от атак (включая кровотечение)"""
    #    renpy.show_screen("damage_visual")
    
    #def show_debuff_status():
    #    """Показывает только дебафы (исключая кровотечение)"""
    #    renpy.show_screen("debuff_visual")
    
    #def show_battle_status():
    #    """Показывает состояние всех участников боя (союзники + противники)"""
    #    # Применяем дебафы в начале раунда
    #    apply_debuffs_at_round_start()
    #    # Показываем единый экран состояния
    #    renpy.show_screen("heroes_attacked_visual")
    
    
    # ========================================================================
    # ФУНКЦИЯ ПОЛУЧЕНИЯ НАЗВАНИЯ ДЕБАФА
    # ========================================================================
    def get_debuff_name(debuff_type, value):
        """Возвращает название дебафа/бафа на основе типа и значения"""
        if debuff_type == 'bloodshed' and value < 0:
            return "Кровотечение"
        elif debuff_type == 'prone':
            return "Лежит"
        elif debuff_type == 'atk':
            if value > 0:
                return "Истощение"
            elif value < 0:
                return "Бодрость"
        elif debuff_type == 'def':
            if value < 0:
                return "Вдохновение"
            elif value > 0:
                return "Печаль"
        elif debuff_type == 'magic':
            if value < 0:
                return "Просвещение"
            elif value > 0:
                return "Помутнение"
        elif debuff_type == 'accuracy':
            if value < 0:
                return "Концентрация"
            elif value > 0:
                return "Страх"
        elif debuff_type == 'critrate':
            if value < 0:
                return "Удача"
            elif value > 0:
                return "Сглаз"
        elif debuff_type == 'critdmg':
            if value < 0:
                return "Безразличие"
            elif value > 0:
                return "Гнев"
        return ""
    
    
    # ========================================================================
    # ФУНКЦИЯ ПОЛУЧЕНИЯ ИКОНКИ ДЕБАФА
    # ========================================================================
#    def get_debuff_icon(debuff_type, value):
#        """Возвращает путь к иконке дебафа/бафа"""
#        if debuff_type == 'bloodshed' and value != 0:
#            return "debuff_bloodshed.png"
#        elif debuff_type == 'prone':
#            return "debuff_prone.png"
#        elif debuff_type == 'atk':
#            if value < 0:
#                return "debuff_atk_down.png"
#            elif value > 0:
#                return "debuff_atk_up.png"
#        elif debuff_type == 'def':
#            if value < 0:
#                return "debuff_def_down.png"
#            elif value > 0:
#                return "debuff_def_up.png"
#        elif debuff_type == 'magic':
#            if value < 0:
#                return "debuff_magic_down.png"
#            elif value > 0:
#                return "debuff_magic_up.png"
#        elif debuff_type == 'accuracy':
#            if value < 0:
#                return "debuff_accuracy_down.png"
#            elif value > 0:
#                return "debuff_accuracy_up.png"
#        elif debuff_type == 'critrate':
#            if value < 0:
#                return "debuff_critrate_down.png"
#            elif value > 0:
#                return "debuff_critrate_up.png"
#        elif debuff_type == 'critdmg':
#           if value < 0:
#               return "debuff_critdmg_down.png"
#           elif value > 0:
#                return "debuff_critdmg_up.png"
#        return None


# ============================================================================
# ЭКРАН ОТОБРАЖЕНИЯ УРОНА ОТ АТАК (ВКЛЮЧАЯ КРОВОТЕЧЕНИЕ)
# ============================================================================

#screen damage_visual():
#    zorder 100
#    modal True
#    
#    frame:
#        xalign 0.5
#        yalign 0.5
#        xsize 1000
#        ysize 600
#        background "#000000cc"
#        
#        vbox:
#            spacing 30
#            xalign 0.5
#            yalign 0.5
#            
#            # Заголовок
#            text "Урон от атак" size 35 xalign 0.5 color "#ff4444"
#            
#            # Основной контейнер с двумя vbox'ами
#            hbox:
#                spacing 450
#                xalign 0.5
#                
#                # ============================================================
#                # VBOX ДЛЯ СОЮЗНИКОВ
#                # ============================================================
#                vbox:
#                    spacing 15
#                    xsize 450
#                    
#                    # Заголовок союзников
#                    text "Союзники" size 30 xalign 0.5 color "#00ff00"
#                    
#                    # Используем централизованную функцию для инициализации team_manager
#                    if store.team_manager is not None:
#                        # Информация о персонажах в команде
#                        for char_name in store.team_manager.team_slots:
#                            if char_name and char_name in store.characters:
#                                $ char = store.pers_dict[char_name]
#                                $ attacks = get_attacks_for_character(char_name)
#                                $ total_damage = get_total_damage_for_character(char_name)
#                                
#                                hbox:
#                                    spacing 15
#                                    
#                                    # Имя персонажа
#                                    text "[char_name]:" size 25 color "#ffffff" min_width 120
#                                    
#                                    # Множественные атаки по персонажу
#                                    if attacks:
#                                        vbox:
#                                            spacing 3
#                                            for attack in attacks:
#                                                $ crit_text = "!" if attack['is_crit'] else ""
#                                                $ color = "#ff0000" if attack['attack_type'] == "enemy" else "#00ff00"
#                                                $ attacker_name = attack['attacker']
#                                                text ("{font=determination.otf}[attacker_name]: [crit_text][attack['damage']] HP{/font}") style "damage_text" size 20 color color at damage_gradient
#                                            
#                                            # Общий урон
#                                            if len(attacks) > 1:
#                                                text ("{font=determination.otf}Всего: -[total_damage] HP{/font}") style "damage_text" size 18 color "#ffaa00" at damage_gradient
                                    
                
#                # ============================================================
#                # VBOX ДЛЯ ПРОТИВНИКОВ
#                # ============================================================
#                vbox:
#                    spacing 15
#                    xsize 450
#                    
#                    # Заголовок противников
#                    text "Противники" size 30 xalign 0.5 color "#ff0000"
#                    
#                    # Информация о противниках в зависимости от battlenumber
#                    if battlenumber:
#                        # Получаем список противников для текущего боя
#                        $ current_enemies = get_active_enemies()
#                        
#                        for enemy_name in current_enemies:
#                            if hasattr(store, 'enemies') and store.enemies and enemy_name in store.enemies:
#                                $ enemy = store.enemies.get(enemy_name)
#                                $ attacks = get_attacks_for_character(enemy_name)
#                                $ total_damage = get_total_damage_for_character(enemy_name)
#                                
#                                hbox:
#                                    spacing 15
#                                    
#                                    # Имя противника
#                                    text "[enemy_name]:" size 25 color "#ffffff" min_width 120
#                                    
#                                    # Атаки по противнику
#                                    if attacks:
#                                        vbox:
#                                            spacing 3
#                                            for attack in attacks:
#                                                $ crit_text = "!" if attack['is_crit'] else ""
#                                                $ color = "#00ff00" if attack['attack_type'] == "normal" else "#ff0000"
#                                                $ attacker_name = attack['attacker']
#                                                text ("{font=determination.otf}[attacker_name]: [crit_text][attack['damage']] HP{/font}") style "damage_text" size 20 color color at damage_gradient
#                                            
#                                            # Общий урон
#                                            if len(attacks) > 1:
#                                                text ("{font=determination.otf}Всего: -[total_damage] HP{/font}") style "damage_text" size 18 color "#ffaa00" at damage_gradient
#                                    else:
#                                        # Если нет атак, показываем промах или отсутствие урона
#                                        text "Нет попаданий" size 20 color "#aaaaaa"
#            
#            null height 30
#            
#            # Кнопка продолжения
#            textbutton "Продолжить" action Hide("damage_visual") xalign 0.5:
#                text_size 30


# ============================================================================
# ЭКРАН ОТОБРАЖЕНИЯ ДЕБАФОВ (ИСКЛЮЧАЯ КРОВОТЕЧЕНИЕ)
# ============================================================================

#screen debuff_visual():
#    zorder 100
#    modal True
#    
#    frame:
#        xalign 0.5
#        yalign 0.5
#        xsize 1000
#        ysize 700
#        background "#000000cc"
#        
#        vbox:
#            spacing 30
#            xalign 0.5
#            yalign 0.5
#            
#            # Заголовок
#            text "Состояние дебафов" size 35 xalign 0.5 color "#ffaa00"
#            
#            # Основной контейнер с двумя vbox'ами
#            hbox:
#                spacing 450
#                xalign 0.5
#                
#                # ============================================================
#                # VBOX ДЛЯ СОЮЗНИКОВ
#                # ============================================================
#                vbox:
#                    spacing 15
#                    xsize 450
#                    
#                    # Заголовок союзников
#                    text "Союзники" size 30 xalign 0.5 color "#00ff00"
#                    
#                    # Используем централизованную функцию для инициализации team_manager
#                    if store.team_manager is not None:
#                        # Информация о персонажах в команде
#                        for char_name in store.team_manager.team_slots:
#                            if char_name and char_name in store.characters:
#                                $ char = store.pers_dict[char_name]
#                                
#                                hbox:
#                                    spacing 15
#                                    
#                                    # Имя персонажа
#                                    text "[char_name]:" size 25 color "#ffffff" min_width 120
#                                    
#                                    # Дебафы персонажа
#                                    if char_name in store.heroes_debuff_info:
#                                        $ debuff_info = store.heroes_debuff_info[char_name]
#                                        
#                                        hbox:
#                                            spacing 8
#                                            
#                                            # Кровотечение
#                                            if debuff_info['bloodshed'] > 0:
#                                                add "bloodshed_debuff_red.png" size (24, 24)
#                                            
#                                            # Prone
#                                            if debuff_info['prone']:
#                                                add "prone_debuff_red.png" size (24, 24)
#                                            
#                                            # Остальные дебафы
#                                            if debuff_info['atk'] != 0:
#                                                if debuff_info['atk'] > 0:
#                                                    add "atk_green_icon.png" size (24, 24)
#                                                elif debuff_info['atk'] < 0:
#                                                    add "atk_debuff_red.png" size (24, 24)
#                                            
#                                            if debuff_info['def'] != 0:
#                                                if debuff_info['def'] > 0:
#                                                    add "def_debuff_green.png" size (24, 24)
#                                                elif debuff_info['def'] < 0:
#                                                    add "def_red_icon.png" size (24, 24)
#                                            
#                                            if debuff_info['magic'] != 0:
#                                                if debuff_info['magic'] > 0:
#                                                    add "magic_debuff_green.png" size (24, 24)
#                                                elif debuff_info['magic'] < 0:
#                                                    add "magic_debuff_red.png" size (24, 24)
#                                            
#                                            if debuff_info['accuracy'] != 0:
#                                                if debuff_info['accuracy'] > 0:
#                                                    add "accuracy_debuff_green.png" size (24, 24)
#                                                elif debuff_info['accuracy'] < 0:
#                                                    add "dmgchance_red_icon.png" size (24, 24)
#                                            
#                                            if debuff_info['critrate'] != 0:
#                                                if debuff_info['critrate'] > 0:
#                                                    add "critrate_debuff_green.png" size (24, 24)
#                                                elif debuff_info['critrate'] < 0:
#                                                    add "critrate_debuff_red.png" size (24, 24)
#                                            
#                                            if debuff_info['critdmg'] != 0:
#                                                if debuff_info['critdmg'] > 0:
#                                                    add "critdmg_debuff_green.png" size (24, 24)
#                                                elif debuff_info['critdmg'] < 0:
#                                                    add "critdmg_debuff_red.png" size (24, 24)
#                                
#                                    # Если нет дебафов
#                                    if char_name not in store.heroes_debuff_info or not any([
#                                        debuff_info.get('bloodshed', 0) > 0,
#                                        debuff_info.get('prone', False),
#                                        debuff_info.get('atk', 0) != 0,
#                                        debuff_info.get('def', 0) != 0,
#                                        debuff_info.get('magic', 0) != 0,
#                                        debuff_info.get('accuracy', 0) != 0,
#                                        debuff_info.get('critrate', 0) != 0,
#                                        debuff_info.get('critdmg', 0) != 0
#                                    ]):
#                                        pass
#            
#            null height 30
#            
#            # Кнопка продолжения
#            textbutton "Продолжить" action Hide("debuff_visual") xalign 0.5:
#                text_size 30


# ============================================================================
# ЭКРАН ОТОБРАЖЕНИЯ АТАКОВАННЫХ ГЕРОЕВ И ДЕБАФОВ (ОРИГИНАЛЬНЫЙ)
# ============================================================================

transform visual_screen_transform:
    xpos 0 ypos 0
    easein 4.5 xpos -60



screen heroes_attacked_visual():
    zorder 100
    #modal True
    timer 1.0 action Hide("heroes_attacked_visual")
    timer 1.0 action Show("clear_visual")

    frame:
        at heroes_attacked_visual_trans

        xsize 1280
        ysize 720
        background None

    
        #spacing 30
        #xalign 0.5
        #yalign 0.5
        
        # Заголовок экрана
        #text "Результаты атаки" size 35 xalign 0.5 color "#ffffff"
        

        # ============================================================
        # VBOX ДЛЯ СОЮЗНИКОВ (такой же как в targettochoose_sprites)
        # ============================================================
              
        # Используем централизованную функцию для инициализации team_manager
        if store.team_manager is not None:
            $ team_slots2 = store.team_manager.team_slots
            $ team_member_count2 = store.team_manager.get_team_member_count()
            $ base_xalign2 = 0.18
            $ xalign_value2 = base_xalign2 - (team_member_count2 * 0.0005)
            $ base_yalign2 = 0.25
            $ yalign_value2 = base_yalign2 + (team_member_count2 * 0.15)
    
            vbox:
                xalign xalign_value2
                yalign yalign_value2

                

                if get_character_picked_for_shift() == 4:
                    $ yoffsetextra = -270
                    $ xoffsetextra = -40
                elif get_character_picked_for_shift() == 3:
                    $ yoffsetextra = -180
                    $ xoffsetextra = 0
                elif get_character_picked_for_shift() == 2:
                    $ yoffsetextra = -90
                    $ xoffsetextra = 0
                elif get_character_picked_for_shift() == 1:
                    $ yoffsetextra = 20
                    $ xoffsetextra = 0
                else:
                    $ yoffsetextra = 20
                    $ xoffsetextra = 0

                for i, char_name in enumerate(team_slots2):
                    if char_name is not None and char_name in store.pers_dict:
                        $ char = store.pers_dict[char_name]
                        $ prev_hp_value, prev_mp_value = get_hp_mp_bar_prev_values(char.name, char.current_hp, char.current_mp)
                        $ mp_delta = char.current_mp - prev_mp_value
                        $ overlay_offset_x2, overlay_offset_y2 = get_hero_visual_offsets(char, i, enemies_is_attacking == 1)
                        $ char_swoon_pending = getattr(char, "swoon_pending_for_visual", False)
                        $ char_swoon_active = getattr(char, "swoon_display_active", False)
                        $ char_swoon_shown = getattr(char, "swoon_visual_shown", False)
                        $ show_char_swoon = char_swoon_active or ((char_swoon_pending or (char.current_hp <= 0 and char.damage_gain_for_vis > 0)) and not char_swoon_shown)

                        if char.current_hp <= 0:
                            $ char.dead = 1
                            if show_char_swoon and not char_swoon_active:
                                $ char.swoon_visual_shown = True
                                $ char.swoon_display_active = True
                        else:
                            $ char.dead = 0
                            if char.current_hp > 1:
                                $ char.swoon_visual_shown = False
                                $ char.swoon_pending_for_visual = False
                                $ char.swoon_display_active = False

                        # Суммарное смещение должно повторять геометрию боевых спрайтов.
                        $ total_offset_x = overlay_offset_x2 + xoffsetextra
                        $ total_offset_y = overlay_offset_y2 + yoffsetextra
                        
                        frame:
                            #at transfrom_for_dmg_numbers_heroes
                            xoffset total_offset_x
                            yoffset total_offset_y
                            padding (0, 0)
                            background None

                                    
                            # Имя персонажа
                            #text "[char_name]:" size 25 color "#ffffff" min_width 120
                            hbox:
                            # Отображение урона с учетом условий

                                if show_char_swoon:
                                    text ("{font=determination.otf}Swoon{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient
                                elif char.damage_gain_for_vis == 1:
                                    text ("{font=determination.otf}Shield{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_yellow
                                elif char.damage_gain_for_vis > 0:       
                                    if char.got_crit_for_visual == 0: # обычный урон
                                        # тут будет условие со щитом
                                        text ("{font=determination.otf}[char.damage_gain_for_vis]{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_gray
                                    else:  # крит.урон
                                        text ("{font=determination.otf}![char.damage_gain_for_vis]{/font}") style "damage_text" size 45 color "#ffffff" xalign 0.5 at damage_gradient
                                elif char.damage_gain_for_vis == -1: # не был целью
                                    text "X" size 30 at invisible
                                elif char.damage_gain_for_vis == 0: # промах
                                    text ("{font=determination.otf}Мимо{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_gray
                                elif char.damage_gain_for_vis <= -2: # исцеление
                                    text ("{font=determination.otf}[-char.damage_gain_for_vis]{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_green
                                if mp_delta > 0:
                                    text ("{font=determination.otf}[mp_delta]{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_cyan
                                elif mp_delta < 0:
                                    text ("{font=determination.otf}[mp_delta]{/font}") style "damage_text" size 30 color "#2b5fff" xalign 0.5 at damage_gradient_cyan

                                #добавить сюда. Если мана прибавилась, то показывает в одном цвете
                                #Если убавилась, то в другом

                            
                                # Множественные атаки по персонажу
                                #if attacks:
                                #    hbox:
                                #        spacing 5
                                #        for attack in attacks:
                                #            $ crit_text = "!" if attack['is_crit'] else ""
                                #            $ color = "#ff0000" if attack['attack_type'] == "enemy" else "#00ff00"
                                #            $ attacker_name = attack['attacker']
                                #            text "[attacker_name]: [crit_text][attack['damage']]" size 18 color color
                                
                                # Дебафы персонажа (обращаемся напрямую к переменным класса)
                                hbox:
                                    xalign 0.5 yalign 0.5
                                    spacing 5
                                    
                                    # Кровотечение
                                    if char.bloodshed_debuff_got > 0:
                                        add "bloodshed.png" size (30, 30) at damage_gradient
                                    elif char.bloodshed_debuff_got < 0:
                                        add "healing.png" size (30, 30) at damage_gradient_green
                                    
                                    # Prone
                                    if char.prone_debuff_got > 0:
                                        add "prone.png" size (30, 30) at damage_gradient
                                    elif char.prone_debuff_got < 0:
                                        add "antiprone.png" size (30, 30) at damage_gradient_green
                                    
                                    # Остальные дебафы
                                    if char.atk_debuff_got != 0:
                                        if char.atk_debuff_got < 0:
                                            add "atk_green_icon.png" size (30, 30) at damage_gradient_green
                                        elif char.atk_debuff_got > 0:
                                            add "atk_red_icon.png" size (30, 30) at damage_gradient
                                    
                                    if char.def_debuff_got != 0:
                                        if char.def_debuff_got > 0:
                                            add "def_red_icon.png" size (30, 30) at damage_gradient
                                        elif char.def_debuff_got < 0:
                                            add "def_green_icon.png" size (30, 30) at damage_gradient_green
                                    
                                    if char not in (store.pers_dict['Крис'], store.pers_dict['Чара'], store.pers_dict['Седрик'], store.pers_dict['Фриск']):
                                        if char.magic_debuff_got != 0:
                                            if char.magic_debuff_got > 0:
                                                add "mag_red_icon.png" size (30, 30) at damage_gradient
                                            elif char.magic_debuff_got < 0:
                                                add "mag_green_icon.png" size (30, 30) at damage_gradient_green
                                    
                                    if char.accuracy_debuff_got != 0:
                                        if char.accuracy_debuff_got > 0:
                                            add "dmgchance_red_icon.png" size (30, 30) at damage_gradient
                                        elif char.accuracy_debuff_got < 0:
                                            add "dmgchance_green_icon.png" size (30, 30) at damage_gradient_green
                                    
                                    if char.critrate_debuff_got != 0:
                                        if char.critrate_debuff_got > 0:
                                            add "critrate_red_icon.png" size (30, 30) at damage_gradient
                                        elif char.critrate_debuff_got < 0:
                                            add "critrate_green_icon.png" size (30, 30) at damage_gradient_green
                                    
                                    if char.critdmg_debuff_got != 0:
                                        if char.critdmg_debuff_got > 0:
                                            add "critdmg_red_icon.png" size (30, 30) at damage_gradient
                                        elif char.critdmg_debuff_got < 0:
                                            add "critdmg_green_icon.png" size (30, 30) at damage_gradient_green

                                    if char.tank_debuff_got != 0:
                                        if char.tank_debuff_got > 0:
                                            add "tank_red_icon.png" size (30, 30) at damage_gradient
                                        elif char.tank_debuff_got < 0:
                                            add "tank_green_icon.png" size (30, 30) at damage_gradient_green

    frame:
        at heroes_attacked_visual_trans_enemy

        xsize 1200
        ysize 800
        background None
        
        

        # ============================================================
        # GRID ДЛЯ ПРОТИВНИКОВ (как в экране выбора цели)
        # ============================================================
        vbox:
            


            # Добавляем логирование, если враги должны отображаться
            $ active_enemies = get_active_enemies()
            $ enemy_count = len(active_enemies)
            $ base_yalign = 0.5
            $ yalign_value = 0.3 if enemy_count > 2 else base_yalign
            $ enemy_effects_yoffset = 100 if enemy_count <= 2 else 0
                
            

            # Используем grid 2 2 как в экране выбора цели
            grid 2 2:
                xalign 0.95
                yalign yalign_value
                yoffset enemy_effects_yoffset
                spacing 20

                
                
                for i, enemy_name in enumerate(active_enemies):
                    $ enemy = store.enemies[enemy_name]
                    $ enemy_swoon_pending = getattr(enemy, "swoon_pending_for_visual", False)
                    $ enemy_swoon_active = getattr(enemy, "swoon_display_active", False)
                    $ enemy_swoon_shown = getattr(enemy, "swoon_visual_shown", False)
                    $ show_enemy_swoon = enemy_swoon_active or ((enemy_swoon_pending or (enemy.current_hp <= 0 and enemy.damage_gain_for_vis > 0)) and not enemy_swoon_shown)

                    if enemy.current_hp <= 0:
                        $ enemy.dead = 1
                        if show_enemy_swoon and not enemy_swoon_active:
                            $ enemy.swoon_visual_shown = True
                            $ enemy.swoon_display_active = True
                    else:
                        $ enemy.dead = 0
                        if enemy.current_hp > 1:
                            $ enemy.swoon_visual_shown = False
                            $ enemy.swoon_pending_for_visual = False
                            $ enemy.swoon_display_active = False
                    $ xoffset_value = 50 if i >= 2 else 0  # если элемент во второй строке
                    
                    frame:
                        xysize (150, 150)
                        background None
                        xoffset xoffset_value
                        
                        # тут можно встаить hbox и add 

                        hbox:
                            
                            xalign 0.5
                            yalign 0.5
                            spacing 5
                            
                            # Имя противника
                            #text "[enemy.name]" size 22 color "#ffffff" xalign 0.5
                            
                            # Отображение урона с учетом условий
                            if show_enemy_swoon:
                                text ("{font=determination.otf}Swoon{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient
                            elif enemy.damage_gain_for_vis == 1:
                                text ("{font=determination.otf}Shield{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_yellow
                            elif enemy.damage_gain_for_vis > 0:
                                if enemy.got_crit_for_visual == 0: # обычный урон
                                    # тут будет условие со щитом
                                    text ("{font=determination.otf}[enemy.damage_gain_for_vis]{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_gray
                                else:  # крит.урон
                                    text ("{font=determination.otf}![enemy.damage_gain_for_vis]{/font}") style "damage_text" size 45 color "#ffffff" xalign 0.5 at damage_gradient
                            elif enemy.damage_gain_for_vis == -1: # не был целью
                                pass
                            elif enemy.damage_gain_for_vis == 0: # промах
                                text ("{font=determination.otf}Мимо{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_gray
                            elif enemy.damage_gain_for_vis <= -2: # исцеление
                                text ("{font=determination.otf}[-enemy.damage_gain_for_vis]{/font}") style "damage_text" size 30 color "#ffffff" xalign 0.5 at damage_gradient_green

                            
                            hbox:
                                xalign 0.5 yalign 0.5
                                spacing 5
                                
                                # Кровотечение
                                if enemy.bloodshed_debuff_got > 0:
                                    add "bloodshed.png" size (30, 30) at damage_gradient
                                elif enemy.bloodshed_debuff_got < 0:
                                    add "healing.png" size (30, 30) at damage_gradient_green
                                
                                # Prone
                                if enemy.prone_debuff_got > 0:
                                    add "prone.png" size (30, 30) at damage_gradient
                                elif enemy.prone_debuff_got < 0:
                                    add "antiprone.png" size (30, 30) at damage_gradient_green
                                
                                # Остальные дебафы
                                if enemy.atk_debuff_got != 0:
                                    if enemy.atk_debuff_got < 0:
                                        add "atk_green_icon.png" size (30, 30) at damage_gradient_green
                                    elif enemy.atk_debuff_got > 0:
                                        add "atk_red_icon.png" size (30, 30) at damage_gradient
                                
                                if enemy.def_debuff_got != 0:
                                    if enemy.def_debuff_got > 0:
                                        add "def_red_icon.png" size (30, 30) at damage_gradient
                                    elif enemy.def_debuff_got < 0:
                                        add "def_green_icon.png" size (30, 30) at damage_gradient_green
                                
                                if enemy.magic_debuff_got != 0:
                                    if enemy.magic_debuff_got > 0:
                                        add "mag_red_icon.png" size (30, 30) at damage_gradient
                                    elif enemy.magic_debuff_got < 0:
                                        add "mag_green_icon.png" size (30, 30) at damage_gradient_green
                                
                                if enemy.accuracy_debuff_got != 0:
                                    if enemy.accuracy_debuff_got > 0:
                                        add "dmgchance_red_icon.png" size (30, 30) at damage_gradient
                                    elif enemy.accuracy_debuff_got < 0:
                                        add "dmgchance_green_icon.png" size (30, 30) at damage_gradient_green
                                
                                if enemy.critrate_debuff_got != 0:
                                    if enemy.critrate_debuff_got > 0:
                                        add "critrate_red_icon.png" size (30, 30) at damage_gradient
                                    elif enemy.critrate_debuff_got < 0:
                                        add "critrate_green_icon.png" size (30, 30) at damage_gradient_green
                                
                                if enemy.critdmg_debuff_got != 0:
                                    if enemy.critdmg_debuff_got > 0:
                                        add "critdmg_red_icon.png" size (30, 30) at damage_gradient
                                    elif enemy.critdmg_debuff_got < 0:
                                        add "critdmg_green_icon.png" size (30, 30) at damage_gradient_green



            #null height 30
        
        #vbox: #проверка других цветов
        #    ypos 200
        #    text ("{font=determination.otf}Пися") size 30 style "damage_text" color "#f7f7f7" xalign 0.5 at damage_gradient

        #    # Для обычного урона (оранжевый)
        #    text ("{font=determination.otf}Попа") size 30 style "damage_text" color "#ffffff" xalign 0.5 at damage_gradient_gray

        #    # Для лечения/защиты (зелёный)
        #    text ("{font=determination.otf}какашечки") size 30 style "damage_text" color "#ffffff" xalign 0.5 at damage_gradient_green

        #    # Для магии/спецэффектов (голубой)
        #    text ("{font=determination.otf}сисечки") size 30 style "damage_text" color "#ffffff" xalign 0.5 at damage_gradient_cyan

        # Кнопка продолжения
        #textbutton "Продолжить" action Hide("heroes_attacked_visual") xalign 0.5:
        #    text_size 30


# ============================================================================
# ЭКРАН ОТОБРАЖЕНИЯ АТАК ПО ВРАГАМ
# ============================================================================

# Старый экран enemies_attacked_visual удален - теперь все в heroes_attacked_visual


# ============================================================================
# СПРАВОЧНАЯ ИНФОРМАЦИЯ
# ============================================================================
# 
# ИСПОЛЬЗОВАНИЕ ЭКРАНОВ:
# 
# 1. В начале раунда врага вызывайте:
#    $ apply_debuffs_at_round_start()
# 
# 2. Показ урона от атак:
#    $ show_damage_results()
# 
# 3. Показ дебафов (включая кровотечение):
#    $ show_debuff_status()
# 
# 4. Показ полного состояния (оригинальный экран):
#    $ show_attack_results()
# 
# НОВАЯ СИСТЕМА МНОЖЕСТВЕННЫХ АТАК:
# 
# 1. Добавление результата атаки:
#    $ add_attack_result("Крис", "Арчи", 50, True, "normal")
# 
# 2. Добавление атаки по нескольким целям:
#    $ targets = [{'name': 'Арчи', 'damage': 50, 'is_crit': True}, 
#                 {'name': 'Тревор', 'damage': 30, 'is_crit': False}]
#    $ add_multiple_attack_results("Крис", targets, "normal")
# 
# 3. Показ результатов:
#    $ show_damage_results()  # Только урон
#    $ show_debuff_status()   # Только дебафы
#    $ show_attack_results()  # Все вместе
# 
# 4. Очистка результатов:
#    $ store.multiple_attacks_results = {}
#    $ store.current_round_attacks = []
#
# 5. Получение информации:
#    $ attacks = get_attacks_for_character("Крис")
#    $ total_damage = get_total_damage_for_character("Крис")
#    $ active_enemies = get_active_enemies()
# 
# ДИЗАЙН ЭКРАНОВ:
# 
# DAMAGE_VISUAL (Урон от атак):
# - Показывает только урон от атак
# - Два vbox'а: союзники (слева) и противники (справа)
# - Цвета: зеленый для атак героев, красный для атак врагов
# 
# DEBUFF_VISUAL (Дебафы):
# - Показывает все дебафы (включая кровотечение)
# - Только союзники (дебафы у врагов не показываются)
# - Иконки для каждого типа дебафа
# - Цвета: зеленый для бафов, красный для дебафов
# 
# HEROES_ATTACKED_VISUAL (Оригинальный):
# - Показывает все: урон + дебафы
# - Полная информация о состоянии боя
# 
# 
# ДЕБАФЫ:
# 
# - Кровотечение: -5% от макс хп з�� раунд (отрицательное значение)
# - Prone: персонаж лежит, turn = 0, +10 к tank
# - Атака: <0 истощение (-5% атк, -2% крит), >0 бодрость (+5% атк, +5% крит)
# - Защита: <0 вдохновение (-5% защ), >0 печаль (+5% защ)
# - Магия: <0 просвещение (-5% маг, -5% мп), >0 помутнение (+5% маг, +5% мп)
# - Точность: <0 концентрация (-5% точн), >0 страх (-5% точн)
# - Крит шанс: <0 удача (-5% крит шанс), >0 сглаз (-5% крит шанс)
# - Крит урон: <0 слабость (-5% крит урон), >0 сила (+5% крит урон)
#
#
# ФУНКЦИИ УПРАВЛЕНИЯ ДЕБАФАМИ:
#
# 1. reset_debuff_flags_for_all():
#    - Сбрасывает флаги получения дебафов для всех персонажей и врагов
#    - Устанавливает damage_gain_for_vis = -1 для всех
#    - Использование: $ reset_debuff_flags_for_all()
#    - Вызывать в начале каждого раунда боя или при необходимости сбросить индикаторы
#
# 2. reset_all_debuffs():
#    - Полностью сбрасывает все дебафы всех персонажей
#    - Восстанавливает возможность ходить для персонажей с turn = 0
#    - Использование: $ reset_all_debuffs()
#
# ============================================================================
