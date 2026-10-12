# ============================================================================
# ПАССИВНЫЕ СПОСОБНОСТИ И УЛУЧШЕНИЯ СЕДРИКА
# ----------------------------------------------------------------------------
# В этом файле собрана вся боевая и кулинарная логика Седрика:
#
#   Пассивки:
#   1. Продукты для рецептов (Ур. 1)      — вместо маны используются 4 вида
#                                           ингредиентов (мучное, фрукты/овощи,
#                                           животное, приправы). База 5 шт,
#                                           +1 каждые 2 ур. (5 + level // 2).
#                                           Перезарядка блюд = 0.
#   2. Перфекционизм или ничего! (Ур. 1)  — если блюдо не прошло проверку
#                                           точности, оно выкидывается на помойку.
#   3. Разогрев сковороды (Ур. 1)         — каждый ход готовки увеличивает урон
#                                           следующего «Удара сковородкой» на +5%.
#   4. Уточнение рецептуры (Ур. 1)        — готовка блюда себе даёт +20% к точности
#                                           при следующей готовке этого блюда.
#   5. Массовая готовка (Ур. 1)           — число порций за ход растёт каждые 3 ур.
#                                           (1 на ур 1-3, 2 на 4-6, 3 на 7-9, 4 на 10-12).
#   6. Долг перед голодными (Ур. 3)       — +0.2% к бонусной точности в конце хода
#                                           за каждую пустую ячейку аппетита союзников.
#   7. Выше кулинарного искусства (Ур. 5) — шанс = крит.шанс умножить силу эффектов
#                                           блюда на крит.урон Седрика.
#   8. Сытный дух (Ур. 7)                 — полностью заполнивший аппетит герой
#                                           получает бафф «Бодрость» (x2) в конце хода.
#   9. Экономия продуктов (Ур. 9)         — шанс = крит.шанс / 2 не потратить
#                                           ингредиенты на блюдо.
#
#   Улучшения:
#   - С мыслями о рецепте (Ур. 2)        — «Сбегать за продуктами» даёт +5% крит.шанса,
#                                           +10% крит.урона.
#   - Двойная порция (Ур. 3)             — «Булочка» с шансом 30% создаёт бесплатную
#                                           порцию случайному союзнику.
#   - Хрустящая корочка (Ур. 4)          — «Удар сковородкой»: +10% шанс оглушить
#                                           и гарантированная «Слабость» (x1).
#   - Белковый заряд (Ур. 5)             — «Яичница с беконом» (Животное x3):
#                                           15% HP, +7% атаки, +5% крит.урона.
#   - Фирменная заправка (Ур. 6)         — «Салат Цезарь» дополнительно восстанавливает
#                                           союзникам +15% MP.
#   - Свежая нарезка (Ур. 7)             — «Сэндвич» замедляет снаряды ещё на +10%
#                                           (всего 18%) и снимает 1 случайный дебафф.
#   - Сладкий сироп (Ур. 8)              — «Блинчики с кленовым сиропом» дают бафф
#                                           «Просвещение» (x2) и +30% защиты.
#   - Королевский банкет (Ур. 9)         — шанс = крит.шанс приготовить «Мясо на гриле»
#                                           и себе.
#   - Авторитет шефа (Ур. 10)            — «Пощёчина от шефа» при успехе срезает врагу
#                                           10% атаки и накладывает «Истощение» (x2)
#                                           на 2 хода.
# ============================================================================

# --- Состояние боя (сбрасывается в sedric_reset_battle_passives) --------------
default sedric_skillet_bonus = 0.0
default sedric_refined_recipes = set()
default sedric_temporary_buffs = []
default sedric_last_cook_status = ""

init python:
    import random

    # ========================================================================
    # КОНСТАНТЫ ПАССИВОК И УЛУЧШЕНИЙ
    # ========================================================================
    SEDRIC_SKILLET_HEAT_STEP = 0.05        # +5% к урону сковороды за каждый ход готовки
    SEDRIC_REFINED_ACCURACY_BONUS = 0.20   # +20% точности от «Уточнения рецептуры»
    SEDRIC_HUNGRY_DEBT_LEVEL = 3
    SEDRIC_HUNGRY_DEBT_STEP = 0.002        # +0.2% точности за пустую ячейку аппетита
    SEDRIC_CULINARY_ART_LEVEL = 5          # Умножение эффективности на крит. урон
    SEDRIC_FULL_SPIRIT_LEVEL = 7           # Сытный дух: Бодрость x2 при сытости
    SEDRIC_PRODUCT_SAVING_LEVEL = 9        # Шанс не потратить ингредиенты = крит/2

    SEDRIC_GROCERY_CRIT_RATE = 0.05        # +5% шанс крита от «С мыслями о рецепте»
    SEDRIC_GROCERY_CRIT_DMG = 0.10         # +10% крит. урон от «С мыслями о рецепте»
    SEDRIC_DOUBLE_BUN_LEVEL = 3            # Ур. 3: Двойная порция булочки
    SEDRIC_DOUBLE_BUN_CHANCE = 0.30        # 30% шанс дополнительной булочки
    SEDRIC_PAN_CRUST_LEVEL = 4             # Ур. 4: +10% оглушение и Слабость x1
    SEDRIC_EGG_BACON_LEVEL = 5             # Ур. 5: Яичница с беконом
    SEDRIC_CAESAR_UPGRADE_LEVEL = 6        # Ур. 6: Салат Цезарь +15% MP
    SEDRIC_SANDWICH_UPGRADE_LEVEL = 7      # Ур. 7: Сэндвич 18% замедление и снятие дебафа
    SEDRIC_PANCAKES_UPGRADE_LEVEL = 8      # Ур. 8: Блинчики Просвещение x2 и +30% def
    SEDRIC_BANQUET_LEVEL = 9               # Ур. 9: Мясо на гриле себе
    SEDRIC_CHEF_AUTHORITY_LEVEL = 10       # Ур. 10: Пощёчина от шефа

    # Рецепты блюд (базовая стоимость ингредиентов на 1 порцию):
    # bread = Мучное, plant = Фрукты/овощи, animal = Животное, spices = Приправы
    SEDRIC_DISH_RECIPES = {
        "Булочка":                     {"bread": 1, "plant": 0, "animal": 0, "spices": 0},
        "Яичница на завтрак":          {"bread": 0, "plant": 0, "animal": 2, "spices": 0},
        "Яичница с беконом":           {"bread": 0, "plant": 0, "animal": 3, "spices": 0},
        "Салат Цезарь":                {"bread": 1, "plant": 2, "animal": 0, "spices": 0},
        "Сэндвич":                     {"bread": 2, "plant": 2, "animal": 1, "spices": 0},
        "Блинчики с кленовым сиропом": {"bread": 3, "plant": 0, "animal": 0, "spices": 1},
        "Бургер":                      {"bread": 2, "plant": 3, "animal": 2, "spices": 0},
        "Чизбургер":                   {"bread": 2, "plant": 3, "animal": 2, "spices": 0},
        "Суши":                        {"bread": 1, "plant": 1, "animal": 2, "spices": 0},
        "Мясо на гриле":               {"bread": 0, "plant": 0, "animal": 3, "spices": 2},
        "Пицца!":                      {"bread": 4, "plant": 3, "animal": 3, "spices": 5},
    }

    # ========================================================================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ========================================================================
    def sedric_char():
        """Возвращает объект Седрика из store.pers_dict."""
        return store.pers_dict.get("Седрик")

    def sedric_level():
        """Возвращает фактический уровень Седрика."""
        char = sedric_char()
        if char is not None and hasattr(char, "level"):
            return max(1, int(char.level))
        global_level = getattr(getattr(store, "Pers", None), "global_level", 1)
        return max(1, int(global_level))

    def sedric_max_ingredients(lvl=None):
        """Максимум каждого ингредиента: 5 базово + 1 каждые 2 уровня (5 + level // 2)."""
        if lvl is None:
            lvl = sedric_level()
        return 5 + (lvl // 2)

    def sedric_max_portions(lvl=None):
        """Максимум порций за 1 ход: 1 на ур 1-3, 2 на 4-6, 3 на 7-9, 4 на 10-12."""
        if lvl is None:
            lvl = sedric_level()
        return max(1, 1 + (max(1, lvl) - 1) // 3)

    def get_sedric_recipe(dish_name, lvl=None):
        """Возвращает стоимость 1 порции блюда с учётом улучшений."""
        if lvl is None:
            lvl = sedric_level()
        if dish_name in ("Яичница на завтрак", "Яичница с беконом"):
            if lvl >= SEDRIC_EGG_BACON_LEVEL:
                return {"bread": 0, "plant": 0, "animal": 3, "spices": 0}
            else:
                return {"bread": 0, "plant": 0, "animal": 2, "spices": 0}
        return SEDRIC_DISH_RECIPES.get(dish_name, {"bread": 0, "plant": 0, "animal": 0, "spices": 0}).copy()

    def can_cook_dish_single(dish_name, char=None):
        """Проверяет, хватает ли ингредиентов у Седрика хотя бы на 1 порцию блюда."""
        cm = getattr(store, "cooking_manager", None)
        if cm is None:
            return True
        cost = get_sedric_recipe(dish_name)
        return (
            getattr(cm, "current_bread_ing", 0) >= cost["bread"] and
            getattr(cm, "current_plant_ing", 0) >= cost["plant"] and
            getattr(cm, "current_animal_ing", 0) >= cost["animal"] and
            getattr(cm, "current_spices_ing", 0) >= cost["spices"]
        )

    def sedric_cleanse_random_debuff(char):
        """Снимает со съевшего персонажа 1 случайный дебафф (улучшение «Сэндвича» ур.7)."""
        if char is None:
            return None
        debuff_keys = [
            ("bloodshed_debuff", "Кровотечение"),
            ("prone_debuff", "Опрокидывание"),
            ("atk_debuff", "Истощение"),
            ("def_debuff", "Печаль"),
            ("magic_debuff", "Помутнение"),
            ("accuracy_debuff", "Страх"),
            ("critrate_debuff", "Сглаз"),
            ("critdmg_debuff", "Безразличие"),
            ("tank_debuff", "Хрупкость"),
        ]
        active = []
        for attr, name in debuff_keys:
            val = getattr(char, attr, 0)
            if val > 0:
                active.append((attr, name))
        if active:
            chosen_attr, chosen_name = random.choice(active)
            setattr(char, chosen_attr, 0)
            renpy.log(f"[Седрик][Свежая нарезка] С {char.name} снят дебафф: {chosen_name}")
            return chosen_name
        return None

    # ========================================================================
    # СБРОС И ЗАВЕРШЕНИЕ РАУНДА
    # ========================================================================
    def sedric_reset_battle_passives():
        """Сброс состояния пассивок Седрика в начале боя (fightbegin12)."""
        sedric_clear_temporary_buffs()
        store.sedric_skillet_bonus = 0.0
        store.sedric_refined_recipes = set()
        store.sedric_last_cook_status = ""
        cm = getattr(store, "cooking_manager", None)
        if cm is not None:
            cm.restore_all_ingredients()
            cm.reset_feed_amount()
        renpy.log("[Седрик] Боевое состояние и ингредиенты сброшены")

    def sedric_on_round_end():
        """Обработка конца раунда (после атак врагов в afterenemyattack)."""
        sedric = sedric_char()
        lvl = sedric_level()

        # 1. Затухание временных баффов от блюд Седрика
        sedric_tick_temporary_buffs()

        if sedric is None or getattr(sedric, "picked", 0) != 1 or getattr(sedric, "current_hp", 0) <= 0:
            return

        # 2. «Долг перед голодными» (Ур. 3):
        # За каждую пустую ячейку аппетита у союзников, кроме него, +0.2% точности
        if lvl >= SEDRIC_HUNGRY_DEBT_LEVEL:
            empty_slots = 0
            for name, char in store.pers_dict.items():
                if name != "Седрик" and getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0:
                    max_f = max(0, int(getattr(char, "max_feedness", 0) or 0))
                    cur_f = max(0, int(getattr(char, "current_feedness", 0) or 0))
                    empty_slots += max(0, max_f - cur_f)
            if empty_slots > 0:
                bonus = empty_slots * SEDRIC_HUNGRY_DEBT_STEP
                sedric.bonus_dmgchance += bonus
                renpy.log(f"[Седрик][Долг перед голодными] +{bonus*100:.1f}% точности за {empty_slots} пустых ячеек аппетита")

        # 3. «Сытный дух» (Ур. 7):
        # Любой персонаж, полностью заполнивший свой аппетит, получает бафф «Бодрость» (x2)
        if lvl >= SEDRIC_FULL_SPIRIT_LEVEL:
            for name, char in store.pers_dict.items():
                if getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0:
                    max_f = max(0, int(getattr(char, "max_feedness", 0) or 0))
                    cur_f = max(0, int(getattr(char, "current_feedness", 0) or 0))
                    if max_f > 0 and cur_f >= max_f:
                        # Накладываем бафф «Бодрость» (x2): отрицательное значение atk_debuff
                        char.debuff("atk", -2)
                        renpy.log(f"[Седрик][Сытный дух] {name} полностью сыт -> получен бафф Бодрость (x2)")

    # ========================================================================
    # УПРАВЛЕНИЕ ВРЕМЕННЫМИ БАФФАМИ ОТ БЛЮД
    # ========================================================================
    def sedric_add_temporary_buff(char_name, stat_type, value, turns):
        """Регистрирует временный бафф на заданное число раундов."""
        store.sedric_temporary_buffs.append({
            "char_name": char_name,
            "stat": stat_type,
            "value": value,
            "turns": turns
        })

    def sedric_tick_temporary_buffs():
        """Уменьшает длительность временных баффов на 1 раунд и снимает истёкшие."""
        remaining = []
        for buff in getattr(store, "sedric_temporary_buffs", []):
            buff["turns"] -= 1
            if buff["turns"] <= 0:
                char = store.pers_dict.get(buff["char_name"])
                if char is not None:
                    val = buff["value"]
                    stat = buff["stat"]
                    if stat == "def":
                        char.bonus_def = max(0.0, char.bonus_def - val)
                    elif stat == "dmgchance":
                        char.bonus_dmgchance -= val
                    elif stat == "magic":
                        char.bonus_magic = max(0.0, char.bonus_magic - val)
                    elif stat == "crit":
                        char.bonus_crit = max(-0.9, char.bonus_crit - val)
                    elif stat == "critrate":
                        char.bonus_critrate = max(-0.5, char.bonus_critrate - val)
                renpy.log(f"[Седрик] Временный бафф {buff['stat']} для {buff['char_name']} истёк")
            else:
                remaining.append(buff)
        store.sedric_temporary_buffs = remaining

    def sedric_clear_temporary_buffs():
        """Снимает все активные временные баффы Седрика (при сбросе боя)."""
        for buff in getattr(store, "sedric_temporary_buffs", []):
            char = store.pers_dict.get(buff["char_name"])
            if char is not None:
                val = buff["value"]
                stat = buff["stat"]
                if stat == "def":
                    char.bonus_def = max(0.0, char.bonus_def - val)
                elif stat == "dmgchance":
                    char.bonus_dmgchance -= val
                elif stat == "magic":
                    char.bonus_magic = max(0.0, char.bonus_magic - val)
                elif stat == "crit":
                    char.bonus_crit = max(-0.9, char.bonus_crit - val)
                elif stat == "critrate":
                    char.bonus_critrate = max(-0.5, char.bonus_critrate - val)
        store.sedric_temporary_buffs = []

    # ========================================================================
    # ИСПОЛНЕНИЕ АТАК
    # ========================================================================
    def sedric_execute_skillet_attack(target):
        """Атака 1: «Удар сковородкой»."""
        sedric = sedric_char()
        if sedric is None or target is None:
            return 0
        lvl = sedric_level()

        # Разогрев сковороды: увеличивает урон атаки на накопившийся процент
        heat_mult = 1.0 + float(getattr(store, "sedric_skillet_bonus", 0.0) or 0.0)
        sedric.next_attack_multiplier *= heat_mult
        store.sedric_skillet_bonus = 0.0

        dmg = sedric.calculate_dmg(target)

        # Шанс оглушить на 1 ход = крит.шанс (+10% при ур 4 «Хрустящая корочка»)
        stun_chance = float(sedric.critrate)
        if lvl >= SEDRIC_PAN_CRUST_LEVEL:
            stun_chance += 0.10

        if random.random() < stun_chance:
            apply_enemy_stun(target, 1)
            renpy.log(f"[Седрик] Враг {target.name} оглушён сковородкой на 1 ход")

        # При ур 4 гарантированно накладывает дебафф «Слабость» (x1)
        if lvl >= SEDRIC_PAN_CRUST_LEVEL:
            target.debuff("magic", 1)
            renpy.log(f"[Седрик][Хрустящая корочка] На врага {target.name} наложена Слабость (x1)")

        return dmg

    def sedric_execute_chef_slap(target):
        """Атака 2: «Пощёчина от шефа» (Ур. 10)."""
        sedric = sedric_char()
        if sedric is None or target is None:
            return 0
        lvl = sedric_level()

        # Испытание для врага: приготовить шедевр кулинарии.
        # Враги не кулинары: 75% шанс провала испытания.
        test_failed = (random.random() < 0.75)

        if test_failed:
            renpy.notify("Враг провалил кулинарное испытание шефа!")
            # 2x урон
            sedric.next_attack_multiplier *= 2.0
            # Уменьшенная защита на 5%
            apply_enemy_weaken_armor(target, 0.05)
            # Уменьшение скорости снарядов на 10%
            apply_enemy_slow(target, 0.10)
            # При ур 10 («Авторитет шефа»): срезает 10% атаки и накладывает «Истощение» (x2) на 2 хода
            if lvl >= SEDRIC_CHEF_AUTHORITY_LEVEL:
                apply_enemy_weaken_attack(target, 0.10)
                apply_enemy_atk_debuff(target, 2)
                renpy.log(f"[Седрик][Авторитет шефа] {target.name}: -10% атаки и Истощение x2 на 2 хода")
        else:
            renpy.notify("Враг каким-то чудом справился с кулинарным испытанием!")

        dmg = sedric.calculate_dmg(target)
        return dmg

    # ========================================================================
    # ИСПОЛНЕНИЕ МАГИИ: СБЕГАТЬ ЗА ПРОДУКТАМИ
    # ========================================================================
    def sedric_execute_grocery_run():
        """Магия 1: «Сбегать за продуктами»."""
        sedric = sedric_char()
        lvl = sedric_level()
        cm = getattr(store, "cooking_manager", None)
        if cm is not None:
            cm.restore_all_ingredients()

        # «С мыслями о рецепте» (Ур. 2): +5% крит.шанс, +10% крит.урон
        if lvl >= 2 and sedric is not None:
            sedric.bonus_critrate += SEDRIC_GROCERY_CRIT_RATE
            sedric.bonus_crit += SEDRIC_GROCERY_CRIT_DMG
            renpy.notify("Седрик сбегал за продуктами! Крит. шанс +5%, крит. урон +10%!")
            renpy.log("[Седрик][С мыслями о рецепте] Запасы пополнены, +5% крит.шанс, +10% крит.урон")
        else:
            renpy.notify("Седрик сбегал за продуктами! Все запасы полностью пополнены!")
            renpy.log("[Седрик] Запасы ингредиентов полностью пополнены")

    # ========================================================================
    # ИСПОЛНЕНИЕ МАГИИ: ПРИГОТОВЛЕНИЕ БЛЮД
    # ========================================================================
    def sedric_execute_cooking(dish_name):
        """
        Центральная функция приготовления выбранного блюда.
        Учитывает точность («Перфекционизм или ничего!»), «Уточнение рецептуры»,
        «Разогрев сковороды», «Выше кулинарного искусства», «Экономию продуктов»
        и все индивидуальные эффекты и улучшения блюд.
        """
        sedric = sedric_char()
        cm = getattr(store, "cooking_manager", None)
        if sedric is None or cm is None:
            return False, "Ошибка менеджера готовки."

        lvl = sedric_level()
        total_portions = cm.get_total_feed_multiply()
        if total_portions <= 0:
            return False, "Не выбрано ни одной порции."

        # --------------------------------------------------------------------
        # 1. Проверка точности: «Перфекционизм или ничего!» (Ур. 1)
        # --------------------------------------------------------------------
        acc = float(sedric.dmgchance)
        # «Уточнение рецептуры» (Ур. 1): если готовил себе раньше, +20% точности
        refined_bonus = 0.0
        if dish_name in getattr(store, "sedric_refined_recipes", set()):
            refined_bonus = SEDRIC_REFINED_ACCURACY_BONUS
            acc += refined_bonus

        cook_success = (random.random() <= acc)

        # --------------------------------------------------------------------
        # 2. Проверка «Экономии продуктов» (Ур. 9)
        # --------------------------------------------------------------------
        free_ingredients = False
        if lvl >= SEDRIC_PRODUCT_SAVING_LEVEL:
            saving_chance = float(sedric.critrate) / 2.0
            if random.random() < saving_chance:
                free_ingredients = True
                renpy.log("[Седрик][Экономия продуктов] Ингредиенты не потрачены на блюдо!")

        # --------------------------------------------------------------------
        # 3. Списание ингредиентов и разогрев сковороды
        # --------------------------------------------------------------------
        # Каждый ход готовки сковорода разогревается на +5%
        store.sedric_skillet_bonus = getattr(store, "sedric_skillet_bonus", 0.0) + SEDRIC_SKILLET_HEAT_STEP

        if not cook_success:
            # Блюдо выкидывается на помойку!
            if not free_ingredients:
                cm.spend_allocated_ingredients(dish_name)
            cm.reset_feed_amount()
            sedric.turn = 0
            store.sedric_last_cook_status = "failed"
            msg = "Седрик посчитал блюдо несовершенным и выбросил его на помойку! (Перфекционизм или ничего!)"
            renpy.notify(msg)
            renpy.log(f"[Седрик][Перфекционизм] Готовка {dish_name} провалена (точность {acc*100:.1f}%)")
            return False, msg

        # --------------------------------------------------------------------
        # 4. Успешная готовка: расчёт множителя эффективности
        # --------------------------------------------------------------------
        # «Выше кулинарного искусства» (Ур. 5): с шансом крит.шанса умножается на крит.урон
        eff_mult = 1.0
        is_crit_cook = False
        if lvl >= SEDRIC_CULINARY_ART_LEVEL:
            if random.random() < float(sedric.critrate):
                eff_mult = float(sedric.crit)
                is_crit_cook = True
                renpy.log(f"[Седрик][Выше кулинарного искусства] Кулинарный шедевр! Множитель x{eff_mult:.2f}")

        # «Уточнение рецептуры»: если Седрик готовит блюдо себе, запоминаем его
        if cm.feed_amount.get("Седрик", 0) > 0:
            store.sedric_refined_recipes.add(dish_name)
            renpy.log(f"[Седрик][Уточнение рецептуры] Седрик уточнил рецепт «{dish_name}» для себя")

        # Тратим ингредиенты
        if not free_ingredients:
            cm.spend_allocated_ingredients(dish_name)

        # --------------------------------------------------------------------
        # 5. Применение эффектов по порциям для каждого персонажа
        # --------------------------------------------------------------------
        # Копия распределения для применения
        recipients = {k: v for k, v in cm.feed_amount.items() if v > 0}

        # «Королевский банкет» (Ур. 9): для «Мясо на гриле» шанс = крит.шанс приготовить и себе
        if dish_name in ("Мясо на гриле",) and lvl >= SEDRIC_BANQUET_LEVEL:
            if random.random() < float(sedric.critrate):
                recipients["Седрик"] = recipients.get("Седрик", 0) + 1
                renpy.notify("Королевский банкет! Седрик приготовил мясо и себе!")
                renpy.log("[Седрик][Королевский банкет] Седрик дополнительно приготовил мясо себе")

        # «Двойная порция» (Ур. 3): «Булочка» с шансом 30% даёт доп. порцию случайному союзнику
        if dish_name in ("Булочка",) and lvl >= SEDRIC_DOUBLE_BUN_LEVEL:
            if random.random() < SEDRIC_DOUBLE_BUN_CHANCE:
                alive_allies = [
                    n for n, c in store.pers_dict.items()
                    if getattr(c, "picked", 0) == 1 and getattr(c, "current_hp", 0) > 0
                ]
                if alive_allies:
                    lucky_ally = random.choice(alive_allies)
                    recipients[lucky_ally] = recipients.get(lucky_ally, 0) + 1
                    renpy.notify(f"Двойная порция! {lucky_ally} получает дополнительную булочку!")
                    renpy.log(f"[Седрик][Двойная порция] Дополнительная булочка для {lucky_ally}")

        # Применяем эффекты блюда к каждому получателю
        for char_name, portions in recipients.items():
            char = store.pers_dict.get(char_name)
            if char is None or getattr(char, "current_hp", 0) <= 0:
                continue

            # Увеличиваем аппетит персонажа
            char.feed_character(portions)

            # Эффекты конкретного блюда:
            if dish_name == "Булочка":
                # 10% HP цели за порцию
                heal = int(char.max_hp * 0.10 * portions * eff_mult)
                char.change_hp(heal)

            elif dish_name in ("Яичница на завтрак", "Яичница с беконом"):
                if lvl >= SEDRIC_EGG_BACON_LEVEL:
                    # «Яичница с беконом» (ур 5): 15% HP, +7% атаки, +5% крит.урона
                    heal = int(char.max_hp * 0.15 * portions * eff_mult)
                    char.change_hp(heal)
                    char.bonus_atk += 0.07 * portions * eff_mult
                    char.bonus_crit += 0.05 * portions * eff_mult
                else:
                    # База: 15% HP, +5% атаки
                    heal = int(char.max_hp * 0.15 * portions * eff_mult)
                    char.change_hp(heal)
                    char.bonus_atk += 0.05 * portions * eff_mult

            elif dish_name == "Салат Цезарь":
                # 10% HP, 10% MP (на ур 6 «Фирменная заправка»: +15% MP = 25% MP)
                heal = int(char.max_hp * 0.10 * portions * eff_mult)
                char.change_hp(heal)
                mp_pct = 0.25 if lvl >= SEDRIC_CAESAR_UPGRADE_LEVEL else 0.10
                base_mp = int(char.max_mp * mp_pct * portions * eff_mult)
                char.current_mp = min(char.max_mp, int(char.current_mp + base_mp))

            elif dish_name == "Сэндвич":
                # 20% HP, замедляет снаряды противника на 8% (на ур 7: ещё на 10% = 18% и снимает 1 дебафф)
                heal = int(char.max_hp * 0.20 * portions * eff_mult)
                char.change_hp(heal)
                slow_val = 0.18 if lvl >= SEDRIC_SANDWICH_UPGRADE_LEVEL else 0.08
                for _enemy in getattr(store, "enemies", {}).values():
                    if getattr(_enemy, "current_hp", 0) > 0:
                        apply_enemy_slow(_enemy, slow_val)
                if lvl >= SEDRIC_SANDWICH_UPGRADE_LEVEL:
                    sedric_cleanse_random_debuff(char)

            elif dish_name == "Блинчики с кленовым сиропом":
                # 50% MP, +25% защиты на 2 хода (на ур 8: бафф Просвещение x2, защита +30%)
                mp_heal = int(char.max_mp * 0.50 * portions * eff_mult)
                char.current_mp = min(char.max_mp, char.current_mp + mp_heal)
                def_bonus = (0.30 if lvl >= SEDRIC_PANCAKES_UPGRADE_LEVEL else 0.25) * portions * eff_mult
                char.bonus_def += def_bonus
                sedric_add_temporary_buff(char.name, "def", def_bonus, 2)
                if lvl >= SEDRIC_PANCAKES_UPGRADE_LEVEL:
                    char.debuff("magic", -2) # Просвещение x2

            elif dish_name in ("Бургер", "Чизбургер"):
                # Вредный фастфуд: -20% точность, +50% HP, +15% защита на 2 хода
                heal = int(char.max_hp * 0.50 * portions * eff_mult)
                char.change_hp(heal)
                def_val = 0.15 * portions * eff_mult
                acc_penalty = 0.20 * portions * eff_mult
                char.bonus_def += def_val
                char.bonus_dmgchance -= acc_penalty
                sedric_add_temporary_buff(char.name, "def", def_val, 2)
                sedric_add_temporary_buff(char.name, "dmgchance", -acc_penalty, 2)

            elif dish_name == "Суши":
                # +20% точность, +10% HP
                heal = int(char.max_hp * 0.10 * portions * eff_mult)
                char.change_hp(heal)
                char.bonus_dmgchance += 0.20 * portions * eff_mult

            elif dish_name == "Мясо на гриле":
                # 50% HP, +5% крит.урона, +2% крит.шанса на 3 хода
                heal = int(char.max_hp * 0.50 * portions * eff_mult)
                char.change_hp(heal)
                crit_val = 0.05 * portions * eff_mult
                rate_val = 0.02 * portions * eff_mult
                char.bonus_crit += crit_val
                char.bonus_critrate += rate_val
                sedric_add_temporary_buff(char.name, "crit", crit_val, 3)
                sedric_add_temporary_buff(char.name, "critrate", rate_val, 3)

            elif dish_name == "Пицца!":
                # Вредный фастфуд: 30% HP, +20% магии, +20% точности на 2 хода
                heal = int(char.max_hp * 0.30 * portions * eff_mult)
                char.change_hp(heal)
                mag_val = 0.20 * portions * eff_mult
                acc_val = 0.20 * portions * eff_mult
                char.bonus_magic += mag_val
                char.bonus_dmgchance += acc_val
                sedric_add_temporary_buff(char.name, "magic", mag_val, 2)
                sedric_add_temporary_buff(char.name, "dmgchance", acc_val, 2)

        cm.reset_feed_amount()
        sedric.turn = 0
        store.sedric_last_cook_status = "success"

        status_msg = f"Седрик приготовил {dish_name}!"
        if is_crit_cook:
            status_msg += " Кулинарный шедевр (урон x%.2f)!" % eff_mult
        if free_ingredients:
            status_msg += " Ингредиенты сэкономлены!"
        renpy.notify(status_msg)
        renpy.log(f"[Седрик] Успешно приготовлено {dish_name} для: {recipients}")
        return True, status_msg

# ============================================================================
# ЛЕЙБЛЫ ИСПОЛНЕНИЯ СПОСОБНОСТЕЙ СЕДРИКА
# ============================================================================

label sedric_cook_action:
    hide screen turntarget
    hide screen choose_magic_screen
    hide screen attack_name_display
    hide screen attack_description

    $ success, msg = sedric_execute_cooking(store.attackindex)
    $ register_action_for_current(store.attackindex)

    show screen heroes_attacked_visual
    $ renpy.pause(2.0, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    call screen choose_attacker_screen()

label sedric_mag1_is_done:
    hide screen Heroattacks
    hide screen choose_magic_screen
    hide screen turntarget
    hide screen attack_name_display
    hide screen attack_description

    $ sedric = store.pers_dict["Седрик"]
    $ sedric.turn = 0
    $ sedric_execute_grocery_run()
    $ register_action_for_current("Сбегать за продуктами")

    show screen heroes_attacked_visual
    $ renpy.pause(1.5, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    call screen choose_attacker_screen()

label sedric_atk1_is_done:
    hide screen Heroattacks
    hide screen choose_attack_screen
    hide screen turntarget
    hide screen attack_name_display
    hide screen attack_description

    $ sedric = store.pers_dict["Седрик"]
    $ sedric.turn = 0

    if target is not None:
        $ dmg = sedric_execute_skillet_attack(target)
        if dmg > 0 and sedric.popal == 1:
            $ add_attack_result("Седрик", target.name, dmg, store.is_crit, "normal")
            if store.is_crit:
                with crit_vpunch
            else:
                with vpunch

    $ register_action_for_current("Удар сковородкой")

    show screen heroes_attacked_visual
    $ renpy.pause(2.0, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    call screen choose_attacker_screen()

label sedric_atk2_is_done:
    hide screen Heroattacks
    hide screen choose_attack_screen
    hide screen turntarget
    hide screen attack_name_display
    hide screen attack_description

    $ sedric = store.pers_dict["Седрик"]
    $ sedric.turn = 0

    if target is not None:
        $ dmg = sedric_execute_chef_slap(target)
        if dmg > 0 and sedric.popal == 1:
            $ add_attack_result("Седрик", target.name, dmg, store.is_crit, "normal")
            if store.is_crit:
                with crit_vpunch
            else:
                with vpunch

    $ register_action_for_current("Пощёчина от шефа")

    show screen heroes_attacked_visual
    $ renpy.pause(2.0, hard=False)
    hide screen heroes_attacked_visual
    $ base_perform = 0

    call screen choose_attacker_screen()
