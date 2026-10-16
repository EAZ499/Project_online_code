transform washslot_art:
    subpixel True
    xysize (120,120)
    xanchor 0.5 yanchor 0.5 xalign 0.5 yalign 0.5 
    on idle:
        easeout 0.15 zoom 1.0
    on hover:
        easein 0.15 zoom 1.1


# ============================================================
# СИСТЕМА ЭФФЕКТОВ ДЛЯ CONSUMABLES (РАСХОДУЕМЫХ ПРЕДМЕТОВ)
# ============================================================

# ------------------------------------------------------------
# 1 УРОВЕНЬ: ВОССТАНОВЛЕНИЕ HP, MP И ЩИТА
# ------------------------------------------------------------
# Формат: hp_heal, mp_heal, shield_heal, over_heal, over_mana
# over_heal = 1 - позволяет HP превышать max значения (до 1.5x)
# over_mana = 1 - позволяет MP превышать max значения (до 1.5x)

default consumable_effects_level1 = {
    "pot1": {
        "hp_heal": 3,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot2": {
        "hp_heal": 3,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot3": {
        "hp_heal": 3,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_atk_3": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_atk_5": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_def_3": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_def_5": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_crit_3": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_crit_5": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_acc_3": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_acc_5": {
        "hp_heal": 5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_all_3": {
        "hp_heal": 10,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "pot_all_5": {
        "hp_heal": 10,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },













    # Food предметы - уровень 1
    "food_clubsandwich": {
        "hp_heal": 30,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_sans_sandwich": {
        "hp_percent": 0.25,
        "hp_heal": 20,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_banana": {
        "hp_heal": 20,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0,
        "hp_regen": 5
    },
    # Монстроконфета удачи - эффекты определяются случайно при поедании
    "food_lucky_monstercandy": {
        "hp_heal": 0,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    
    "food_icecream": {
        "hp_heal": 20,
        "mp_heal": 10,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_readymeal_1": {
        "hp_percent": 0.35,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_readymeal_2": {
        "hp_percent": 0.4,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_readymeal_3": {
        "hp_percent": 0.5,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 1,
        "over_mana": 0
    },
    "food_cookiesharing": {
        "hp_heal_all_picked": 15,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_pepperoni": {
        "hp_heal_all_picked": 20,
        "hp_percent_all_picked": 0.2,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 1,
        "over_mana": 0
    },
    "food_mint_gum": {
        "hp_heal": 0,
        "mp_heal": 10,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_lottery_candy": {
        "hp_heal": 20,
        "mp_heal": 10,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_colacoffee": {
        "hp_heal": 1,
        "mp_heal": 25,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 1,
        "revive": 1
    },
    "food_tonic": {
        "hp_heal": 1,
        "mp_heal": 20,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 1,
        "revive": 1
    },
    "food_crab_apple": {
        "hp_percent": 0.15,
        "hp_heal": 20,
        "mp_heal": 20,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_diet_salad": {
        "hp_percent": 0.15,
        "hp_heal": 0,
        "mp_heal": 25,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_broccoli": {
        "hp_percent": 0.25,
        "hp_heal": 10,
        "mp_heal": 10,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_noodles": {
        "hp_heal": 15,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 1,
        "over_mana": 0
    },
    "food_sparkling_water": {
        "hp_heal": 10,
        "mp_heal": 30,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_still_water": {
        "hp_heal": 20,
        "mp_heal": 10,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
    "food_frenchfries": {
        "hp_heal": 30,
        "mp_heal": 0,
        "shield_heal": 0,
        "over_heal": 0,
        "over_mana": 0
    },
}

# ------------------------------------------------------------
# 2 УРОВЕНЬ: БАФФЫ И ДЕБАФФЫ ХАРАКТЕРИСТИК
# ------------------------------------------------------------
# Формат: atk_debuff, def_debuff, magic_debuff, accuracy_debuff, critrate_debuff, critdmg_debuff
# Положительные значения = дебафф (уменьшение характеристики)
# Отрицательные значения = бафф (увеличение характеристики)
# Значения прибавляются к текущим значениям переменных

default consumable_effects_level2 = {
    "pot_atk_3": {
        "atk_debuff": -2,  # Отрицательное = бафф (увеличение атаки)
        "def_debuff": 0,
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_atk_5": {
        "atk_debuff": -2,  # Отрицательное = бафф (увеличение атаки)
        "def_debuff": 0,
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_def_3": {
        "atk_debuff": 0,
        "def_debuff": -2,  # Отрицательное = бафф (увеличение защиты)
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_def_5": {
        "atk_debuff": 0,
        "def_debuff": -2,  # Отрицательное = бафф (увеличение защиты)
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_crit_3": {
        "atk_debuff": 0,
        "def_debuff": 0,
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": -2,  # Отрицательное = бафф (увеличение шанса крита)
        "critdmg_debuff": 0
    },
    "pot_crit_5": {
        "atk_debuff": 0,
        "def_debuff": 0,
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": -2,  # Отрицательное = бафф (увеличение шанса крита)
        "critdmg_debuff": 0
    },
    "pot_acc_3": {
        "atk_debuff": 0,
        "def_debuff": 0,
        "magic_debuff": 0,
        "accuracy_debuff": -2,  # Отрицательное = бафф (увеличение точности)
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_acc_5": {
        "atk_debuff": 0,
        "def_debuff": 0,
        "magic_debuff": 0,
        "accuracy_debuff": -2,  # Отрицательное = бафф (увеличение точности)
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_all_3": {
        "atk_debuff": -2,  # Отрицательное = бафф (увеличение атаки)
        "def_debuff": -2,  # Отрицательное = бафф (увеличение защиты)
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },
    "pot_all_5": {
        "atk_debuff": -2,  # Отрицательное = бафф (увеличение защиты)
        "def_debuff": -2,  # Отрицательное = бафф (увеличение защиты)
        "magic_debuff": 0,
        "accuracy_debuff": 0,
        "critrate_debuff": 0,
        "critdmg_debuff": 0
    },




















    # Food предметы - уровень 2
    "food_cookiesharing": {
        "def_debuff_all_picked": -2
    },
    "food_pepperoni": {
        "def_debuff_all_picked": -4
    },
    "food_colacoffee": {
        "accuracy_debuff": 3
    },
    "food_crab_apple": {
        "magic_debuff": -4
    },
    "food_broccoli": {
        "atk_debuff": 3,
        "def_debuff": 6
    },
    "food_colacoffee": {
        "atk_debuff": -2,
    },
    #"food_noodles": {
    #    "critdmg_debuff": 4
    #},
    "food_still_water": {
        "magic_debuff": -3
    },
    "food_lottery_candy": { 
        "critrate_debuff": -2,
    },
    "food_icecream": {
        "atk_debuff": -2,
    },
}

# ------------------------------------------------------------
# 3 УРОВЕНЬ: УВЕЛИЧЕНИЕ БОНУСНЫХ ХАРАКТЕРИСТИК НА 0.1
# ------------------------------------------------------------
# Формат: bonus_atk, bonus_def, bonus_magic, bonus_accuracy, bonus_critrate, bonus_critdmg
# Значения добавляются к соответствующим переменным bonus_* персонажа

default consumable_effects_level3 = {
    "pot_atk_3": {
        "bonus_atk": 0.1,
        "bonus_def": 0,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_atk_5": {
        "bonus_atk": 0.1,
        "bonus_def": 0,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_def_3": {
        "bonus_atk": 0,
        "bonus_def": 0.1,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_def_5": {
        "bonus_atk": 0,
        "bonus_def": 0.1,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_crit_3": {
        "bonus_atk": 0,
        "bonus_def": 0,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0.1,
        "bonus_critdmg": 0
    },
    "pot_crit_5": {
        "bonus_atk": 0,
        "bonus_def": 0,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0.1,
        "bonus_critdmg": 0
    },
    "pot_acc_3": {
        "bonus_atk": 0,
        "bonus_def": 0,
        "bonus_magic": 0,
        "bonus_accuracy": 0.1,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_acc_5": {
        "bonus_atk": 0,
        "bonus_def": 0,
        "bonus_magic": 0,
        "bonus_accuracy": 0.1,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_all_3": {
        "bonus_atk": 0.1,
        "bonus_def": 0.1,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },
    "pot_all_5": {
        "bonus_atk": 0.1,
        "bonus_def": 0.1,
        "bonus_magic": 0,
        "bonus_accuracy": 0,
        "bonus_critrate": 0,
        "bonus_critdmg": 0
    },







































    # Food предметы - уровень 3
    "food_sans_sandwich": {
        "bonus_atk": 0.2,
        "bonus_def": 0.2,
        "bonus_accuracy": 0.05,
        "bonus_critrate": 0.05,
        "bonus_critdmg": 0.03,
        "bonus_socialization": 1,
    },
    "food_readymeal_1": {
        "bonus_atk": 0.1
    },
    "food_readymeal_2": {
        "bonus_def": 0.1
    },
    "food_mint_gum": {
        "merchant_relation_bonus": 3,
        "merchant_relation_duration_sec": 30 * 60,
        "bonus_socialization": 2,
        "bonus_rhetoric": 1,
        "bonus_charm": 8
    },
    "food_colacoffee": {
        "bonus_tank": 5,
        "soul_speed": 1.0
    },
    "food_tonic": {
        "soul_speed": 0.2

    },
    #"food_crab_apple": {
        # Крабовое яблоко должно давать только Просвещение (magic_debuff на уровне 2).
        # Бонусные характеристики (уровень 3) для него не применяются.
    #},
    "food_noodles": {
        "ordinarynumber": 1,
        "bonus_def": 0.15,
        "bonus_critrate": -0.05,
        "bonus_critdmg": -0.03,
        "bonus_charm": -10,
    },
    "food_cookiesharing": {
        "bonus_socialization_all_picked": 1,
        "bonus_comfort": 1,
    },
    "food_pepperoni": {
        "bonus_socialization_all_picked": 1
    },
    "food_sparkling_water": {
        "bonus_tank": 5,
        "bonus_critrate": 0.02,
        "bonus_critdmg": 0.05,
        "bonus_perception": 1,
    },

    "food_still_water": {
        "bonus_tank": -5,
        "bonus_critrate": -0.05,
        "bonus_critdmg": -0.10,
        "bonus_rhetoric": 2,
    },
    "food_frenchfries": {
        "bonus_socialization": 1,
        "bonus_comfort": 1,
    },
    "food_icecream": {
        "bonus_magic": 0.25,
        "bonus_critrate": -0.1,
        "bonus_critdmg": -0.15,
        "bonus_power": -1
    },
    "food_lottery_candy": { 
        "bonus_accuracy": 0.08,
        "bonus_critrate": 0.05,
    },
    "food_diet_salad": {
        "bonus_diplomacy": 1,
        "bonus_charm": 15,
        "bonus_rhetoric": 1,
    },
}

init python:
    # При autoreload `default` может не обновить уже созданный словарь.
    # Принудительно добавляем revive к предметам, которые должны поднимать павшего.
    if hasattr(store, "consumable_effects_level3"):
        store.consumable_effects_level3.update({
            "food_colacoffee": dict(store.consumable_effects_level3.get("food_colacoffee", {}), revive=1),
            "food_tonic": dict(store.consumable_effects_level3.get("food_tonic", {}), revive=1),
        })

# ------------------------------------------------------------
# ФУНКЦИЯ ПРИМЕНЕНИЯ ВСЕХ ЭФФЕКТОВ CONSUMABLE
# ------------------------------------------------------------
init python:
    import time

    # Таймеры для эффекта "Сточная канава" (каждый таймер независим)
    if not hasattr(store, "sewer_timers"):
        store.sewer_timers = []

    if not hasattr(store, "merchant_relation_timers"):
        store.merchant_relation_timers = []

    def _apply_trade_relation_penalty(delta, duration_sec):
        """Добавляет штраф к отношениям торговцев с таймером."""
        store.merchant_relation_bonus += delta
        expiry = time.time() + duration_sec
        store.merchant_relation_timers.append((delta, expiry))

    def _apply_sewer_penalty():
        """Применяет эффект 'Сточная канава' на 30 минут."""
        delta = -15
        duration_sec = 30 * 60
        store.merchant_relation_bonus += delta
        expiry = time.time() + duration_sec
        store.sewer_timers.append((delta, expiry))
        renpy.show_screen("consume_trade_relation")
        # Применяем дебаффы к героям
        for c in getattr(store, "pers_dict", {}).values():
            if hasattr(c, "bonus_atk"):
                c.bonus_atk -= 0.05
        # Применяем дебаффы к врагам (используем bonus_atk2 напрямую)
        for e in getattr(store, "enemies", {}).values():
            if hasattr(e, "bonus_atk2"):
                e.bonus_atk2 -= 0.01

    def cleanup_merchant_relation_timers():
        """Очищает истёкшие таймеры отношений торговцев."""
        now = time.time()
        active = []
        for delta, expiry in getattr(store, "merchant_relation_timers", []):
            if now >= expiry:
                store.merchant_relation_bonus -= delta
            else:
                active.append((delta, expiry))
        store.merchant_relation_timers = active

    def cleanup_sewer_timers():
        """Очищает истёкшие таймеры 'Сточная канава'."""
        now = time.time()
        active = []
        for delta, expiry in getattr(store, "sewer_timers", []):
            if now >= expiry:
                store.merchant_relation_bonus -= delta
                # Восстанавливаем бонусы атаки
                for c in getattr(store, "pers_dict", {}).values():
                    if hasattr(c, "bonus_atk"):
                        c.bonus_atk += 0.05
                for e in getattr(store, "enemies", {}).values():
                    if hasattr(e, "bonus_atk2"):
                        e.bonus_atk2 += 0.01
            else:
                active.append((delta, expiry))
        store.sewer_timers = active

    def get_sewer_timers_info():
        """Возвращает список активных таймеров 'Сточная канава' для экрана."""
        cleanup_sewer_timers()
        now = time.time()
        timers_info = []
        for delta, expiry in getattr(store, "sewer_timers", []):
            remaining = max(0, expiry - now)
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            timers_info.append({"delta": delta, "minutes": minutes, "seconds": seconds, "active": remaining > 0})
        return timers_info

    def get_scaled_consumable_price(item_id):
        base_price = store.consumable_prices.get(item_id, 0)
        if item_id in ("food_readymeal_1", "food_readymeal_2", "food_readymeal_3"):
            level = max(1, int(getattr(store, "level", 1)))
            return int(6 * 1.5 * level)
        return base_price

    def _apply_lucky_monstercandy_roll(char):
        """Случайный эффект монстроконфеты удачи."""
        roll = renpy.random.randint(1, 6)
        is_ally_target = getattr(char, "is_ally", True)

        def _heal_hp_to_normal_cap(entity, flat_amount):
            current_hp = getattr(entity, "current_hp", 0)
            max_hp = getattr(entity, "max_hp", 0)
            if max_hp <= 0 or current_hp >= max_hp:
                return False
            entity.current_hp = int(max(0, min(current_hp + flat_amount, max_hp)))
            return entity.current_hp > current_hp

        def _heal_mp_to_normal_cap(entity, percent_amount):
            current_mp = getattr(entity, "current_mp", 0)
            max_mp = getattr(entity, "max_mp", 0)
            if max_mp <= 0 or current_mp >= max_mp:
                return False
            mana_gain = int(max_mp * percent_amount)
            entity.current_mp = int(max(0, min(current_mp + mana_gain, max_mp)))
            return entity.current_mp > current_mp

        def _apply_speed_bonus(entity, delta):
            if is_ally_target:
                store.soul_speed = store.clamp_soul_speed(getattr(store, "soul_speed", 10) + delta*10)
                return
            if hasattr(entity, "speed"):
                entity.speed = store.clamp_enemy_speed(getattr(entity, "speed", 1.0) + delta)

        if roll == 1:
            # Вкус ириски: +30 ОЗ
            healed = _heal_hp_to_normal_cap(char, 30)
            if healed:
                renpy.notify("Монстроконфета: вкус ириски (+20 ОЗ).")
            else:
                renpy.notify("Монстроконфета: вкус ириски не подействовал.")

        elif roll == 2:
            # Вкус кофе: +0.1 soul_speed, +бодрость на 2 хода
            _apply_speed_bonus(char, 0.1)
            if hasattr(char, "atk_debuff"):
                char.atk_debuff -= 2
            renpy.notify("Монстроконфета: вкус кофе (+скорость, бодрость на 2 хода).")

        elif roll == 3:
            # Вкус чистой воды: +20% маны + 1 ordinarynumber
            restored = _heal_mp_to_normal_cap(char, 0.2)
            store.ordinarynumber = int(getattr(store, "ordinarynumber", 0)) + 1
            if restored:
                renpy.notify("Монстроконфета: вкус чистой воды (+20% ОМ, +1 ordinarynumber).")
            else:
                renpy.notify("Монстроконфета: вкус чистой воды (+1 ordinarynumber).")

        elif roll == 4:
            # Вкус слитка золота: -1 ОЗ + 20 кромеров
            char.current_hp = int(max(0, char.current_hp - 20))
            store.money = int(getattr(store, "money", 0)) + 35
            renpy.notify("Монстроконфета: вкус золота (-1 ОЗ, +20 кромеров).")

        elif roll == 5:
            # Острый чили: -20 ОЗ + следующая атака +30% урона
            char.current_hp = int(max(0, char.current_hp - 20))
            char.next_attack_damage_multiplier = getattr(char, "next_attack_damage_multiplier", 1.0) + 0.3
            renpy.notify("Монстроконфета: острый чили (-20 ОЗ, следующая атака +30% урона).")

        else:
            # Сточная канава: -15% отношений торговцев на 30 мин, дебаффы
            _apply_sewer_penalty()
            if hasattr(char, "sad_debuff"):
                char.sad_debuff += 2  # Грусть на 2 хода
            if hasattr(char, "bonus_socialization"):
                char.bonus_socialization -= 3
            renpy.notify("Монстроконфета: вкус сточной канавы (-15% отношений торговцев на 30 мин).")

    def is_weapon_consumable_item(item_id):
        return isinstance(item_id, str) and item_id.startswith("wep_")

    def get_consumable_item_effects_level1(item_id):
        if is_weapon_consumable_item(item_id):
            return getattr(store, "weapon_consumable_effects_level1", {}).get(item_id, {})
        return getattr(store, "consumable_effects_level1", {}).get(item_id, {})

    def get_consumable_item_effects_level2(item_id):
        if is_weapon_consumable_item(item_id):
            return getattr(store, "weapon_consumable_effects_level2", {}).get(item_id, {})
        return getattr(store, "consumable_effects_level2", {}).get(item_id, {})

    def get_consumable_item_effects_level3(item_id):
        if is_weapon_consumable_item(item_id):
            return getattr(store, "weapon_consumable_effects_level3", {}).get(item_id, {})
        return getattr(store, "consumable_effects_level3", {}).get(item_id, {})

    def _capture_consumable_visual_state(char):
        tracked_fields = (
            "current_hp",
            "shield",
            "bloodshed_debuff",
            "prone_debuff",
            "atk_debuff",
            "def_debuff",
            "magic_debuff",
            "accuracy_debuff",
            "critrate_debuff",
            "critdmg_debuff",
        )
        state = {field: getattr(char, field, 0) for field in tracked_fields}

        bonus_fields = {
            "bonus_atk_visual": ("bonus_atk2", "bonus_atk"),
            "bonus_def_visual": ("bonus_def2", "bonus_def"),
            "bonus_magic_visual": ("bonus_magic2", "bonus_magic"),
            "bonus_accuracy_visual": ("bonus_dmgchance2", "bonus_dmgchance"),
            "bonus_critrate_visual": ("bonus_critrate2", "bonus_critrate"),
            "bonus_critdmg_visual": ("bonus_crit2", "bonus_crit"),
            "bonus_tank_visual": ("bonus_tank2", "bonus_tank"),
        }

        for state_name, attr_names in bonus_fields.items():
            state[state_name] = 0
            for attr_name in attr_names:
                if hasattr(char, attr_name):
                    state[state_name] = getattr(char, attr_name)
                    break

        state["base_atk_mod_visual"] = getattr(char, "base_atk_mod", 0)
        state["base_def_mod_visual"] = getattr(char, "base_def_mod", 0)

        return state

    def _apply_consumable_visual_state(char, old_state):
        hp_delta = getattr(char, "current_hp", 0) - old_state["current_hp"]
        shield_delta = getattr(char, "shield", 0) - old_state["shield"]

        if hp_delta > 0:
            char.damage_gain_for_vis = -hp_delta
            store.clear_swoon_pending_for_visual(char)
        elif shield_delta > 0:
            char.damage_gain_for_vis = 1
            store.clear_swoon_pending_for_visual(char)
        else:
            char.damage_gain_for_vis = -1
            store.clear_swoon_pending_for_visual(char)

        char.got_crit_for_visual = 0

        for debuff_name in (
            "bloodshed_debuff",
            "prone_debuff",
            "atk_debuff",
            "def_debuff",
            "magic_debuff",
            "accuracy_debuff",
            "critrate_debuff",
            "critdmg_debuff",
        ):
            old_value = old_state.get(debuff_name, 0)
            new_value = getattr(char, debuff_name, 0)
            setattr(char, debuff_name + "_got", new_value - old_value)

        bonus_to_visual = (
            ("bonus_atk_visual", "atk_debuff_got"),
            ("bonus_def_visual", "def_debuff_got"),
            ("bonus_magic_visual", "magic_debuff_got"),
            ("bonus_accuracy_visual", "accuracy_debuff_got"),
            ("bonus_critrate_visual", "critrate_debuff_got"),
            ("bonus_critdmg_visual", "critdmg_debuff_got"),
            ("bonus_tank_visual", "tank_debuff_got"),
        )

        for bonus_field, visual_field in bonus_to_visual:
            old_value = old_state.get(bonus_field, 0)
            new_value = old_value

            if bonus_field == "bonus_atk_visual":
                new_value = getattr(char, "bonus_atk2", getattr(char, "bonus_atk", old_value))
            elif bonus_field == "bonus_def_visual":
                new_value = getattr(char, "bonus_def2", getattr(char, "bonus_def", old_value))
            elif bonus_field == "bonus_magic_visual":
                new_value = getattr(char, "bonus_magic2", getattr(char, "bonus_magic", old_value))
            elif bonus_field == "bonus_accuracy_visual":
                new_value = getattr(char, "bonus_dmgchance2", getattr(char, "bonus_dmgchance", old_value))
            elif bonus_field == "bonus_critrate_visual":
                new_value = getattr(char, "bonus_critrate2", getattr(char, "bonus_critrate", old_value))
            elif bonus_field == "bonus_critdmg_visual":
                new_value = getattr(char, "bonus_crit2", getattr(char, "bonus_crit", old_value))
            elif bonus_field == "bonus_tank_visual":
                new_value = getattr(char, "bonus_tank2", getattr(char, "bonus_tank", old_value))

            setattr(char, visual_field, getattr(char, visual_field, 0) - (new_value - old_value))

        base_atk_mod_delta = getattr(char, "base_atk_mod", 0) - old_state.get("base_atk_mod_visual", 0)
        if base_atk_mod_delta != 0:
            char.atk_debuff_got = getattr(char, "atk_debuff_got", 0) - base_atk_mod_delta

        base_def_mod_delta = getattr(char, "base_def_mod", 0) - old_state.get("base_def_mod_visual", 0)
        if base_def_mod_delta != 0:
            char.def_debuff_got = getattr(char, "def_debuff_got", 0) - base_def_mod_delta

    def _get_active_party_member_names(target_char=None):
        """
        Возвращает имена активных членов команды.
        Основной источник истины в проекте - флаг `char.picked == 1`,
        но поддерживаем и старый формат `store.picked = [имя, ...]`.
        """
        names = []
        pers_dict = getattr(store, "pers_dict", {})

        store_picked = getattr(store, "picked", None)
        if isinstance(store_picked, (list, tuple, set)):
            for picked_name in store_picked:
                if isinstance(picked_name, str) and picked_name in pers_dict and picked_name not in names:
                    names.append(picked_name)

        for char_name, team_char in pers_dict.items():
            if getattr(team_char, "picked", 0) == 1 and char_name not in names:
                names.append(char_name)

        if target_char is not None and getattr(target_char, "name", None) in pers_dict:
            target_name = target_char.name
            if target_name not in names:
                names.append(target_name)

        return names

    def consumable_has_all_picked_effects(item_id):
        for effects in (
            getattr(store, "consumable_effects_level1", {}).get(item_id, {}),
            getattr(store, "consumable_effects_level2", {}).get(item_id, {}),
            getattr(store, "consumable_effects_level3", {}).get(item_id, {}),
        ):
            for effect_name, effect_value in effects.items():
                if effect_name.endswith("_all_picked") and effect_value:
                    return True
        return False

    def get_feedable_party_targets(target_char=None):
        targets = []
        seen_names = set()
        pers_dict = getattr(store, "pers_dict", {})
        for picked_name in _get_active_party_member_names(target_char):
            team_char = pers_dict.get(picked_name)
            if not team_char:
                continue
            team_name = getattr(team_char, "name", None)
            if team_name in seen_names:
                continue
            if hasattr(team_char, "can_be_fed") and not team_char.can_be_fed():
                continue
            if team_name is not None:
                seen_names.add(team_name)
            targets.append(team_char)
        return targets

    def _is_alive_for_item_effects(entity):
        if entity is None:
            return False
        if not hasattr(entity, "current_hp"):
            return True
        return getattr(entity, "current_hp", 0) > 0

    def _get_target_side_entities(target_char=None):
        pers_dict = getattr(store, "pers_dict", {})
        enemies_dict = getattr(store, "enemies", {})

        if target_char is not None and target_char in enemies_dict.values():
            active_enemy_names = get_active_enemies() if "get_active_enemies" in globals() else list(enemies_dict.keys())
            result = []
            for enemy_name in active_enemy_names:
                enemy = enemies_dict.get(enemy_name)
                if enemy is not None and enemy not in result:
                    result.append(enemy)
            if target_char not in result:
                result.append(target_char)
            return result, "enemy"

        result = []
        for hero_name in _get_active_party_member_names(target_char):
            hero = pers_dict.get(hero_name)
            if hero is not None and hero not in result:
                result.append(hero)
        if target_char is not None and getattr(target_char, "name", None) in pers_dict and target_char not in result:
            result.append(target_char)
        return result, "hero"

    def _apply_debuff_bonus_changes(entity, atk_debuff_delta=0, def_debuff_delta=0, magic_debuff_delta=0,
                                    accuracy_debuff_delta=0, critrate_debuff_delta=0, critdmg_debuff_delta=0):
        """
        Применяет мгновенные изменения бонусных характеристик при получении дебаффа.
        Работает по аналогии с apply_debuffs_at_round_start_enemies(), но с коэффициентом 0.05.

        Важно: эта функция применяется только к объектам класса/стороны врагов.
        Для героев бонусные характеристики здесь не изменяются.
        """
        enemies_dict = getattr(store, "enemies", {})
        if entity not in enemies_dict.values():
            return
        def _resolve_attr(entity_obj, *attr_names):
            for attr_name in attr_names:
                if hasattr(entity_obj, attr_name):
                    return attr_name
            return None

        def _round_attr_if_float(entity_obj, attr_name, digits=2):
            if not hasattr(entity_obj, attr_name):
                return
            value = getattr(entity_obj, attr_name)
            if isinstance(value, float):
                setattr(entity_obj, attr_name, round(value, digits))

        # Атака: если получен дебафф атаки, сразу меняем atk_debuff_var
        if atk_debuff_delta != 0:
            current_atk_var = getattr(entity, "atk_debuff_var", 1.0)
            if atk_debuff_delta > 0:  # Дебафф (Истощение)
                current_atk_var *= max(0.0, 1 - 0.05 * atk_debuff_delta)
            elif atk_debuff_delta < 0:  # Бафф (Бодрость)
                current_atk_var *= max(0.0, 1 + 0.05 * abs(atk_debuff_delta))
            entity.atk_debuff_var = round(current_atk_var, 2)

        # Защита: если получен дебафф защиты, сразу меняем def_debuff_var
        if def_debuff_delta != 0:
            current_def_var = getattr(entity, "def_debuff_var", 1.0)
            if def_debuff_delta > 0:  # Дебафф (Вдохновение)
                current_def_var *= max(0.0, 1 - 0.05 * def_debuff_delta)
            elif def_debuff_delta < 0:  # Бафф (Печаль)
                current_def_var *= max(0.0, 1 + 0.05 * abs(def_debuff_delta))
            entity.def_debuff_var = round(current_def_var, 2)

        # Магия: если получен дебафф/бафф магии, сразу меняем magic_debuff_var.
        # Важно: шаг 0.05 * стаки округляем заранее, чтобы убрать погрешности вида 2.0000001.
        if magic_debuff_delta != 0:
            current_magic_var = getattr(entity, "magic_debuff_var", 1.0)
            magic_step = round(0.05 * abs(magic_debuff_delta), 4)
            if magic_debuff_delta > 0:  # Дебафф (Просвещение)
                        magic_factor = max(0.0, round(1 - magic_step, 4))
            else:  # Бафф (Помутнение)
                magic_factor = max(0.0, round(1 + magic_step, 4))
            current_magic_var *= magic_factor
            entity.magic_debuff_var = round(current_magic_var, 2)

        # Точность: если получен дебафф точности, сразу меняем accuracy_debuff_var
        if accuracy_debuff_delta != 0:
            current_accuracy_var = getattr(entity, "accuracy_debuff_var", 0.0)
            if accuracy_debuff_delta > 0:  # Дебафф (Концентрация)
                current_accuracy_var -= 0.05 * accuracy_debuff_delta
            elif accuracy_debuff_delta < 0:  # Бафф (Страх)
                current_accuracy_var += 0.05 * abs(accuracy_debuff_delta)
            entity.accuracy_debuff_var = round(current_accuracy_var, 2)

        # Крит шанс: если получен дебафф крит шанса, сразу меняем critrate_debuff_var
        if critrate_debuff_delta != 0:
            current_critrate_var = getattr(entity, "critrate_debuff_var", 0.0)
            if critrate_debuff_delta > 0:  # Дебафф (Удача)
                current_critrate_var -= 0.05 * critrate_debuff_delta
            elif critrate_debuff_delta < 0:  # Бафф (Сглаз)
                current_critrate_var += 0.05 * abs(critrate_debuff_delta)
            entity.critrate_debuff_var = round(current_critrate_var, 2)

        # Крит урон: если получен дебафф крит урона, сразу меняем critdmg_debuff_var
        if critdmg_debuff_delta != 0:
            current_critdmg_var = getattr(entity, "critdmg_debuff_var", 0.0)
            if critdmg_debuff_delta > 0:  # Дебафф (безразличие)
                current_critdmg_var -= 0.05 * critdmg_debuff_delta
            elif critdmg_debuff_delta < 0:  # Бафф (гнев)
                current_critdmg_var += 0.05 * abs(critdmg_debuff_delta)
            entity.critdmg_debuff_var = round(current_critdmg_var, 2)

    def apply_consumable_all_effects(char, item_id):
        cleanup_merchant_relation_timers()
        cleanup_sewer_timers()

        side_entities, target_side = _get_target_side_entities(char)
        has_teamwide_effects = consumable_has_all_picked_effects(item_id)
        active_hero_targets = get_feedable_party_targets(char) if target_side == "hero" else []
        extra_hero_targets = get_feedable_party_targets(None) if (target_side == "enemy" and item_id in ("food_cookiesharing", "food_pepperoni")) else []
        hero_teamwide_targets = []
        seen_hero_names = set()
        for hero in active_hero_targets + extra_hero_targets:
            hero_name = getattr(hero, "name", None)
            if hero_name in seen_hero_names:
                continue
            if hero_name is not None:
                seen_hero_names.add(hero_name)
            hero_teamwide_targets.append(hero)

        appetite_targets = []
        selected_target_name = getattr(char, "name", None)
        for hero in hero_teamwide_targets:
            hero_name = getattr(hero, "name", None)
            if target_side == "hero" and hero_name == selected_target_name:
                continue
            appetite_targets.append(hero)

        enemy_teamwide_targets = list(side_entities) if target_side == "enemy" else []
        teamwide_targets = []
        seen_target_names = set()
        for entity in hero_teamwide_targets + enemy_teamwide_targets:
            entity_name = getattr(entity, "name", None)
            if entity_name in seen_target_names:
                continue
            if entity_name is not None:
                seen_target_names.add(entity_name)
            teamwide_targets.append(entity)

        tracked_chars = {char.name: char}
        is_party_target = hasattr(store, "pers_dict") and char.name in getattr(store, "pers_dict", {})
        for team_char in side_entities:
            if hasattr(team_char, "name"):
                tracked_chars[team_char.name] = team_char
        for team_char in hero_teamwide_targets:
            if hasattr(team_char, "name"):
                tracked_chars[team_char.name] = team_char

        visual_states = {
            char_name: _capture_consumable_visual_state(team_char)
            for char_name, team_char in tracked_chars.items()
        }

        effects1 = store.consumable_effects_level1.get(item_id, {})
        effects3 = store.consumable_effects_level3.get(item_id, {})
        hp_heal = effects1.get("hp_heal", 0)
        mp_heal = effects1.get("mp_heal", 0)
        shield_heal = effects1.get("shield_heal", 0)
        over_heal = effects1.get("over_heal", 0)
        over_mana = effects1.get("over_mana", 0)

        hp_percent = effects1.get("hp_percent", 0)
        hp_regen = effects1.get("hp_regen", 0)
        hp_heal_all_picked = effects1.get("hp_heal_all_picked", 0)
        hp_percent_all_picked = effects1.get("hp_percent_all_picked", 0)
        revive_effect = int(effects3.get("revive", effects1.get("revive", 0)))
        can_heal_zero_hp_enemy = not (
            target_side == "enemy" and
            getattr(char, "current_hp", 0) <= 0 and
            revive_effect != 1
        )
        skip_overheal_food_heal = (over_heal == 0 and char.current_hp > char.max_hp)
        skip_overmana_food_heal = (over_mana == 0 and char.current_mp > char.max_mp)

        revive_floor_hp = 1 if (
            target_side == "enemy" and
            revive_effect == 1 and
            getattr(char, "current_hp", 0) <= 0
        ) else 0

        can_affect_target = _is_alive_for_item_effects(char) or revive_effect == 1

        if hp_heal and not skip_overheal_food_heal and can_heal_zero_hp_enemy and can_affect_target:
            max_limit = char.max_hp * 1.5 if over_heal == 1 else char.max_hp
            char.current_hp = int(max(revive_floor_hp, min(char.current_hp + hp_heal, max_limit)))

        if hp_percent and not skip_overheal_food_heal and can_heal_zero_hp_enemy and can_affect_target:
            max_limit = char.max_hp * 1.5 if over_heal == 1 else char.max_hp
            char.current_hp = int(max(revive_floor_hp, min(char.current_hp + int(char.max_hp * hp_percent), max_limit)))

        if mp_heal and not skip_overmana_food_heal and can_affect_target:
            max_limit = char.max_mp * 1.5 if over_mana == 1 else char.max_mp
            char.current_mp = int(max(0, min(char.current_mp + mp_heal, max_limit)))

        if shield_heal and can_affect_target:
            char.shield += shield_heal

        if hp_regen and can_affect_target:
            char.basehpregen += hp_regen

        if hp_heal_all_picked or hp_percent_all_picked:
            for team_char in teamwide_targets:
                if not _is_alive_for_item_effects(team_char) and revive_effect != 1:
                    continue
                skip_team_overheal_food_heal = (over_heal == 0 and team_char.current_hp > team_char.max_hp)
                if skip_team_overheal_food_heal:
                    continue
                if target_side == "enemy" and getattr(team_char, "current_hp", 0) <= 0 and revive_effect != 1:
                    continue

                team_revive_floor_hp = 1 if (
                    target_side == "enemy" and
                    revive_effect == 1 and
                    getattr(team_char, "current_hp", 0) <= 0
                ) else 0

                max_limit = team_char.max_hp * 1.5 if over_heal == 1 else team_char.max_hp
                if hp_heal_all_picked:
                    team_char.current_hp = int(max(team_revive_floor_hp, min(team_char.current_hp + hp_heal_all_picked, max_limit)))
                if hp_percent_all_picked:
                    team_char.current_hp = int(max(team_revive_floor_hp, min(team_char.current_hp + int(team_char.max_hp * hp_percent_all_picked), max_limit)))

        effects2 = store.consumable_effects_level2.get(item_id, {})
        
        # Общие effects2-дебаффы применяются здесь только к героям.
        # Для врагов они обрабатываются ниже в enemy_targets, иначе эффект наложится дважды.
        if target_side != "enemy" and can_affect_target:
            for debuff_name in ("atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff", "critrate_debuff", "critdmg_debuff"):
                if effects2.get(debuff_name, 0) and hasattr(char, debuff_name):
                    old_value = getattr(char, debuff_name)
                    setattr(char, debuff_name, old_value + effects2[debuff_name])
                    debuff_delta = getattr(char, debuff_name) - old_value
                    _apply_debuff_bonus_changes(char, **{debuff_name + "_delta": debuff_delta})

        # Применяем дебаффы ко всем союзникам (teamwide)
        for debuff_name in ("atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff", "critrate_debuff", "critdmg_debuff"):
            team_key = debuff_name + "_all_picked"
            if not effects2.get(team_key, 0):
                continue
            for team_char in teamwide_targets:
                if not _is_alive_for_item_effects(team_char):
                    continue
                if hasattr(team_char, debuff_name):
                    old_value = getattr(team_char, debuff_name)
                    setattr(team_char, debuff_name, old_value + effects2[team_key])
                    debuff_delta = getattr(team_char, debuff_name) - old_value
                    _apply_debuff_bonus_changes(team_char, **{debuff_name + "_delta": debuff_delta})

        def _resolve_effect_attr(target_entity, attr_name):
            redirected_attr = {
                "base_atk": "base_atk_mod",
                "base_def": "base_def_mod",
                "base_magic": "base_magic_mod",
            }.get(attr_name, attr_name)

            if hasattr(target_entity, redirected_attr):
                return redirected_attr
            return attr_name if hasattr(target_entity, attr_name) else None

        def _apply_to_target_attrs(target_entity, attr_names, delta, minimum=0):
            if delta == 0:
                return
            for attr_name in attr_names:
                resolved_attr = _resolve_effect_attr(target_entity, attr_name)
                if not resolved_attr:
                    continue
                old_value = getattr(target_entity, resolved_attr)
                try:
                    new_value = old_value + delta
                except Exception:
                    continue
                if minimum is not None:
                    new_value = max(minimum, new_value)
                try:
                    setattr(target_entity, resolved_attr, new_value)
                    break
                except Exception:
                    continue

        # Для обычного применения расходника по врагу эффект должен идти только в выбранную цель,
        # а не во всех врагов на стороне.
        enemy_targets = [char] if target_side == "enemy" else []
        enemy_debuff_keys = ("atk", "magic", "critrate", "critdmg", "accuracy", "def")
        for stat_name in enemy_debuff_keys:
            enemy_key = "enemy_{}_debuff".format(stat_name)
            common_key = "{}_debuff".format(stat_name)
            enemy_debuff_value = effects2.get(enemy_key, effects2.get(common_key, 0) if target_side == "enemy" else 0)
            if not enemy_debuff_value:
                continue
            debuff_attr = "{}_debuff".format(stat_name)
            for target_entity in enemy_targets:
                if not _is_alive_for_item_effects(target_entity):
                    continue
                if not hasattr(target_entity, debuff_attr):
                    continue
                old_value = getattr(target_entity, debuff_attr)
                setattr(target_entity, debuff_attr, old_value + enemy_debuff_value)
                debuff_delta = getattr(target_entity, debuff_attr) - old_value
                _apply_debuff_bonus_changes(target_entity, **{debuff_attr + "_delta": debuff_delta})

        enemy_bonus_atk = effects3.get("enemy_bonus_atk", effects3.get("enemy_bonus_atk_debuff", 0))
        enemy_bonus_magic = effects3.get("enemy_bonus_magic", effects3.get("enemy_bonus_magic_debuff", 0))
        enemy_bonus_critrate = effects3.get("enemy_bonus_critrate", effects3.get("enemy_bonus_critrate_debuff", 0))
        enemy_bonus_critdmg = effects3.get("enemy_bonus_critdmg", effects3.get("enemy_bonus_critdmg_debuff", 0))
        enemy_bonus_accuracy = effects3.get("enemy_bonus_accuracy", effects3.get("enemy_bonus_accuracy_debuff", 0))
        enemy_bonus_def = effects3.get("enemy_bonus_def", effects3.get("enemy_bonus_def_debuff", 0))
        enemy_base_atk = effects3.get("enemy_base_atk", effects3.get("enemy_base_atk_debuff", 0))
        enemy_base_def = effects3.get("enemy_base_def", effects3.get("enemy_base_def_debuff", 0))
        enemy_speed_debuff = effects3.get("enemy_speed_debuff", 0)

        for target_entity in enemy_targets:
            if not _is_alive_for_item_effects(target_entity):
                continue
            _apply_to_target_attrs(target_entity, ("bonus_atk2", "bonus_atk", "attack"), -enemy_bonus_atk)
            _apply_to_target_attrs(target_entity, ("bonus_magic2", "bonus_magic", "bonus_magic_armor"), -enemy_bonus_magic)
            if hasattr(target_entity, "bonus_magic") and isinstance(target_entity.bonus_magic, float):
                target_entity.bonus_magic = round(target_entity.bonus_magic, 2)
            if hasattr(target_entity, "bonus_magic2") and isinstance(target_entity.bonus_magic2, float):
                target_entity.bonus_magic2 = round(target_entity.bonus_magic2, 2)
            _apply_to_target_attrs(target_entity, ("bonus_critrate2", "bonus_critrate", "critrate2", "critrate"), -enemy_bonus_critrate)
            _apply_to_target_attrs(target_entity, ("bonus_crit2", "bonus_crit", "critdmg", "crit_damage"), -enemy_bonus_critdmg)
            _apply_to_target_attrs(target_entity, ("bonus_dmgchance2", "bonus_dmgchance", "accuracy"), -enemy_bonus_accuracy)
            _apply_to_target_attrs(target_entity, ("bonus_def2", "bonus_def", "base_def"), -enemy_bonus_def)
            _apply_to_target_attrs(target_entity, ("attack", "base_atk", "atk"), -enemy_base_atk)
            _apply_to_target_attrs(target_entity, ("base_def", "defense", "def"), -enemy_base_def)
            if enemy_speed_debuff and hasattr(target_entity, "speed"):
                target_entity.speed = store.clamp_enemy_speed(target_entity.speed * (1 - enemy_speed_debuff))

        if can_affect_target and effects3.get("bonus_atk", 0) and hasattr(char, "bonus_atk"):
            char.bonus_atk += effects3["bonus_atk"]
        if can_affect_target and effects3.get("bonus_def", 0) and hasattr(char, "bonus_def"):
            char.bonus_def += effects3["bonus_def"]
        if can_affect_target and effects3.get("bonus_magic", 0) and hasattr(char, "bonus_magic"):
            char.bonus_magic += effects3["bonus_magic"]
            if isinstance(char.bonus_magic, float):
                char.bonus_magic = round(char.bonus_magic, 2)
        if can_affect_target and effects3.get("bonus_accuracy", 0) and hasattr(char, "bonus_dmgchance"):
            char.bonus_dmgchance += effects3["bonus_accuracy"]
        if can_affect_target and effects3.get("bonus_critrate", 0):
            if hasattr(char, "bonus_critrate"):
                char.bonus_critrate += effects3["bonus_critrate"]
            elif hasattr(char, "bonus_critrate2"):
                char.bonus_critrate2 += effects3["bonus_critrate"]
        if can_affect_target and effects3.get("bonus_critdmg", 0):
            if hasattr(char, "bonus_crit"):
                char.bonus_crit += effects3["bonus_critdmg"]
            elif hasattr(char, "bonus_crit2"):
                char.bonus_crit2 += effects3["bonus_critdmg"]
        if can_affect_target and effects3.get("bonus_tank", 0) and hasattr(char, "bonus_tank"):
            char.bonus_tank += effects3["bonus_tank"]
        if can_affect_target and effects3.get("bonus_perform", 0) and hasattr(char, "bonus_perform"):
            char.bonus_perform += effects3["bonus_perform"]
        if can_affect_target and effects3.get("bonus_socialization", 0) and hasattr(char, "bonus_socialization"):
            char.bonus_socialization += effects3["bonus_socialization"]
        if can_affect_target and effects3.get("bonus_diplomacy", 0) and hasattr(char, "bonus_diplomacy"):
            char.bonus_diplomacy += effects3["bonus_diplomacy"]
        if can_affect_target and effects3.get("bonus_charm", 0) and hasattr(char, "bonus_charm"):
            char.bonus_charm += effects3["bonus_charm"]
        if can_affect_target and effects3.get("bonus_perception", 0) and hasattr(char, "bonus_perception"):
            char.bonus_perception += effects3["bonus_perception"]
        if can_affect_target and effects3.get("bonus_rhetoric", 0) and hasattr(char, "bonus_rhetoric"):
            char.bonus_rhetoric += effects3["bonus_rhetoric"]
        if can_affect_target and effects3.get("bonus_artistry", 0) and hasattr(char, "bonus_artistry"):
            char.bonus_artistry += effects3["bonus_artistry"]
        if can_affect_target and effects3.get("bonus_comfort", 0) and hasattr(char, "bonus_comfort"):
            char.bonus_comfort += effects3["bonus_comfort"]
        if can_affect_target and effects3.get("bonus_power", 0) and hasattr(char, "bonus_power"):
            char.bonus_power += effects3["bonus_power"]

        # Фабри «Созидатель» (ур.6): при наложении баффа на союзника есть
        # шанс (равный магии Фабри) забрать половину прибавки себе.
        # Единая точка: все поля баффов выше уже применены, поэтому
        # копируем их фактическими значениями, а не дублируем список.
        if can_affect_target and getattr(char, "name", None) != "Фабри":
            for _field in ("bonus_atk", "bonus_def", "bonus_magic",
                           "bonus_dmgchance", "bonus_critrate", "bonus_crit",
                           "bonus_tank", "bonus_perform", "bonus_socialization"):
                _amount = effects3.get(_field, 0)
                if _amount:
                    fabri_try_siphon_buff(_field, _amount)

        if effects3.get("bonus_socialization_all_picked", 0):
            for team_char in teamwide_targets:
                if not _is_alive_for_item_effects(team_char):
                    continue
                if hasattr(team_char, "bonus_socialization"):
                    team_char.bonus_socialization += effects3["bonus_socialization_all_picked"]

        merchant_relation_bonus = effects3.get("merchant_relation_bonus", 0)
        merchant_relation_duration_sec = int(effects3.get("merchant_relation_duration_sec", 0))
        if merchant_relation_bonus and can_affect_target:
            if merchant_relation_duration_sec > 0:
                _apply_trade_relation_penalty(merchant_relation_bonus, merchant_relation_duration_sec)
            else:
                store.merchant_relation_bonus += merchant_relation_bonus

        is_friendly_target = hasattr(store, "pers_dict") and getattr(char, "name", None) in store.pers_dict
        if is_friendly_target and can_affect_target:
            store.soul_speed = store.clamp_soul_speed(getattr(store, "soul_speed", 10) + effects3.get("soul_speed", 0))
        if can_affect_target:
            store.ordinarynumber = int(getattr(store, "ordinarynumber", 0)) + int(effects3.get("ordinarynumber", 0))

        if has_teamwide_effects:
            for team_char in appetite_targets:
                if not _is_alive_for_item_effects(team_char):
                    continue
                if hasattr(team_char, "feed_character"):
                    team_char.feed_character(1)
                if hasattr(store, "push_feedness_item"):
                    store.push_feedness_item(team_char, item_id)

        for char_name, team_char in tracked_chars.items():
            _apply_consumable_visual_state(team_char, visual_states[char_name])

        # Синхронизируем флаг смерти сразу после обработки расходника.
        # Иначе персонаж/враг может визуально оставаться "мёртвым" при уже восстановленном HP.
        for char_name, team_char in tracked_chars.items():
            was_dead_before_item = visual_states.get(char_name, {}).get("current_hp", 0) <= 0
            is_alive_after_item = getattr(team_char, "current_hp", 0) > 0

            if hasattr(team_char, "dead"):
                team_char.dead = not is_alive_after_item

            # Если персонажа только что воскресили, возвращаем ему возможность ходить,
            # если её не блокирует prone и персонаж всё ещё в активной команде.
            if (
                was_dead_before_item and
                is_alive_after_item and
                hasattr(store, "pers_dict") and
                getattr(team_char, "name", None) in getattr(store, "pers_dict", {}) and
                getattr(team_char, "picked", 0) == 1 and
                getattr(team_char, "prone_debuff", 0) == 0 and
                hasattr(team_char, "turn")
            ):
                team_char.turn = 1

        if item_id == "food_lottery_candy" and target_side == "hero" and renpy.random.random() <= 0.95:
            store.lottery = int(getattr(store, "lottery", 0)) + 1
            renpy.notify("Вы получили лотерейный билет!")

        if item_id == "food_lucky_monstercandy":
            _apply_lucky_monstercandy_roll(char)

        if has_teamwide_effects:
            return bool(teamwide_targets)

        return is_party_target or bool(tracked_chars)


# ============================================================
# ЭКРАН ОТОБРАЖЕНИЯ ТАЙМЕРОВ "СТОЧНАЯ КАНАВА"
# ============================================================

screen consume_trade_relation():
    zorder 9999
    timer 1.0 repeat True action Function(lambda: renpy.restart_interaction())

    vbox:
        xalign 1.0
        yalign 0.5
        xoffset -20
        spacing 5

        $ sewer_timers = get_sewer_timers_info() if "get_sewer_timers_info" in dir(store) else []

        if sewer_timers:
            text "{font=determination.otf}{size=18}Сточная канава:{/font}{/size}" color "#ff0000"
            for timer_info in sewer_timers:
                if timer_info["active"]:
                    text "{font=determination.otf}{size=14}–15% ([timer_info['minutes']]:[timer_info['seconds']:02d]){/font}{/size}" color "#ff6600"





# ============================================================================
# ИНТЕГРАЦИЯ ЭФФЕКТОВ CONSUMABLES В СИСТЕМУ БОЯ
# ============================================================================

# ============================================================================
# ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ АКТИВНЫХ ЭФФЕКТОВ В ИНТЕРФЕЙСЕ
# ============================================================================

init python:
    def get_char_buffs_display(char_name):
        """
        Возвращает список активных эффектов для отображения в интерфейсе.
        Новая система: показывает текущие значения дебаффов/баффов персонажа.
        Возвращает список словарей с информацией о баффах/дебаффах.
        """
        if char_name not in store.pers_dict:
            return []
        
        char = store.pers_dict[char_name]
        active_buffs = []
        
        # Проверяем каждое значение дебаффа/баффа
        # Если значение не 0, добавляем в список
        
        # Bloodshed (кровотечение)
        if char.bloodshed_debuff != 0:
            active_buffs.append({
                "name": "Bloodshed",
                "display_name": "bloodshed",
                "value": char.bloodshed_debuff,
                "is_buff": char.bloodshed_debuff < 0,  # Отрицательное = бафф
                "icon": "bloodshed.png"
            })
        
        # Prone (состояние на земле)
        if char.prone_debuff != 0:
            active_buffs.append({
                "name": "Prone",
                "display_name": "Prone",
                "value": char.prone_debuff,
                "is_buff": char.prone_debuff < 0,
                "icon": "prone.png"
            })
        
        # Атака (atk_debuff: <0 = истощение, >0 = бодрость)
        if char.atk_debuff != 0:
            active_buffs.append({
                "name": "Атака",
                "display_name": "Exhaust" if char.atk_debuff > 0 else "Cheerful",
                "value": char.atk_debuff,
                "is_buff": char.atk_debuff < 0,
                "icon": None
            })
        
        # Защита (def_debuff: <0 = вдохновение, >0 = печаль)
        if char.def_debuff != 0:
            active_buffs.append({
                "name": "Защита",
                "display_name": "Sorrow" if char.def_debuff > 0 else "Inspired",
                "value": char.def_debuff,
                "is_buff": char.def_debuff < 0,
                "icon": None
            })
        
        # Магия (magic_debuff: <0 = просвещение, >0 = помутнение)
        if char.magic_debuff != 0:
            active_buffs.append({
                "name": "Магия",
                "display_name": "Foggyminded" if char.magic_debuff > 0 else "Enlighted",
                "value": char.magic_debuff,
                "is_buff": char.magic_debuff < 0,
                "icon": None
            })
        
        # Точность (accuracy_debuff: <0 = концентрация, >0 = страх)
        if char.accuracy_debuff != 0:
            active_buffs.append({
                "name": "Точность",
                "display_name": "Feared" if char.accuracy_debuff > 0 else "Focused",
                "value": char.accuracy_debuff,
                "is_buff": char.accuracy_debuff < 0,
                "icon": None
            })
        
        # Шанс крита (critrate_debuff: <0 = неудача, >0 = удача)
        if char.critrate_debuff != 0:
            active_buffs.append({
                "name": "Шанс крита",
                "display_name": "Unluck" if char.critrate_debuff > 0 else "Luck",
                "value": char.critrate_debuff,
                "is_buff": char.critrate_debuff < 0,
                "icon": None
            })
        
        # Критический урон (critdmg_debuff: <0 = апатия, >0 = гнев)
        if char.critdmg_debuff != 0:
            active_buffs.append({
                "name": "Крит. урон",
                "display_name": "Apathy" if char.critdmg_debuff > 0 else "Anger",
                "value": char.critdmg_debuff,
                "is_buff": char.critdmg_debuff < 0,
                "icon": None
            })
        
        # Tank (tank_debuff: <0 = скрытность, >0 = уязвимость)
        if char.tank_debuff != 0:
            active_buffs.append({
                "name": "Tank",
                "display_name": "Vulnerable" if char.tank_debuff > 0 else "Stealth",
                "value": char.tank_debuff,
                "is_buff": char.tank_debuff < 0,
                "icon": None
            })
        
        return active_buffs
    
    def get_buff_color(buff_type, is_buff):
        """Возвращает цвет для отображения эффекта в зависимости от типа и является ли это баффом."""
        # Цвета для разных типов эффектов
        if is_buff:
            return "#00ff04"  # Зелёный для баффа
        else:
            return "#ff0000"  # Красный для дебаффа
    
    def get_buff_display_name(buff_info):
        """Возвращает название эффекта для отображения."""
        return buff_info["display_name"]
    
    def get_buff_icon(buff_info):
        """Возвращает иконку эффекта или None."""
        return buff_info.get("icon", None)

# ============================================================================
# ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ИСПОЛЬЗОВАНИЯ CONSUMABLE
# ============================================================================

init python:
    def can_use_consumable(item_id):
        """
        Проверяет, можно ли использовать consumable.
        Новая система: проверяет наличие предмета в инвентаре.
        """
        if store.consumable_inventory.get(item_id, 0) <= 0:
            return False
        if getattr(store, "battlenumber", 0) == 1:
            archie = (getattr(store, "enemies", {}) or {}).get("Арчи")
            if (archie is not None and getattr(archie, "mood", "happy") == "angry" and
                    renpy.random.random() <= float(getattr(archie, "critrate", 0.20))):
                renpy.notify("Арчи заблокировал использование предмета!")
                return False
        return True

# ============================================================================
# ИНИЦИАЛИЗАЦИЯ НАЧАЛЬНЫХ CONSUMABLES С ЭФФЕКТАМИ
# ============================================================================

# Добавляем все consumables с эффектами в инвентарь игрока для тестирования
init python:
    def init_buff_consumables():
        """Инициализирует начальные consumables с эффектами."""
        # Проверяем, существует ли consumable_inventory
        if not hasattr(store, 'consumable_inventory'):
            return
        # Добавляем все расходники в инвентарь
        consumables_to_add = [
            "pot1", "pot2", "pot3",
            "pot_atk_3", "pot_atk_5",
            "pot_def_3", "pot_def_5",
            "pot_crit_3", "pot_crit_5",
            "pot_acc_3", "pot_acc_5",
            "pot_all_3", "pot_all_5"
        ]
        for item_id in consumables_to_add:
            if item_id not in store.consumable_inventory:
                store.add_consumable(item_id, 1)

# Вызываем инициализацию при запуске игры (после инициализации default переменных)
init 1 python:
    init_buff_consumables()







# ============================================================
# ОДНОРАЗОВОЕ ОРУЖИЕ (CONSUMABLES-WEAPONS)
# ============================================================
# Предметы, которые используются один раз и исчезают из инвентаря.
# Наносят урон врагам и/или накладывают дебаффы.
# ============================================================

# ------------------------------------------------------------
# ЭФФЕКТЫ УРОВНЯ 1: УРОН И БАЗОВЫЕ ЭФФЕКТЫ
# ------------------------------------------------------------
# Формат: damage (урон всем врагам), damage_single (урон одной цели)
# ------------------------------------------------------------
init python:
    if not hasattr(store, "weapon_consumable_effects_level1"):
        store.weapon_consumable_effects_level1 = {}
    
    store.weapon_consumable_effects_level1.update({
        # Водяной пистолет: без урона, только дебафф скорости
        "wep_water_pistol": {
            "damage": 0,
            "damage_single": 0,
            "bleeding": 0,
            "rage": 0,
        },
        # Водяная бомба: 10 урона всем врагам
        "wep_water_bomb": {
            "damage": 10,
            "damage_single": 0,
            "bleeding": 0,
            "rage": 0,
        },
        # Зубочистка: 15 урона одной цели, кровотечение 4 хода
        "wep_toothpick": {
            "damage": 0,
            "damage_single": 15,
            "bleeding": 0,
            "rage": 0,
        },
        # Резинка: 5 урона, дебафф скорости
        "wep_rubber_band": {
            "damage": 0,
            "damage_single": 5,
            "bleeding": 0,
            "rage": 0,
        },
        # Трубочка с бумажкой: 10 урона одной цели
        "wep_paper_shooter": {
            "damage": 0,
            "damage_single": 10,
            "bleeding": 0,
            "rage": 0,
        },
        # Линейка: 30 урона одной цели
        "wep_ruler": {
            "damage": 0,
            "damage_single": 30,
            "bleeding": 0,
            "rage": 0,
        },
        # Мыльные пузыри: 10 урона всем врагам
        "wep_soap_bubbles": {
            "damage": 10,
            "damage_single": 0,
            "bleeding": 0,
            "rage": 0,
        },
        # Листок с сомнительными стихами: без урона, только дебафф
        "wep_poetry_leaf": {
            "damage": 0,
            "damage_single": 0,
            "bleeding": 0,
            "rage": 0,
        },
        # Бомбочки для ванной: 20 урона всем в бою + ещё 20 выбранной цели
        "wep_bath_bombs": {
            "damage": 20,
            "damage_single": 40,
            "bleeding": 0,
            "rage": 0,
            "damage_allies": 20,
        },
        # Конструктор: 45 урона одной цели
        "wep_constructor": {
            "damage": 0,
            "damage_single": 45,
            "bleeding": 0,
            "rage": 0,
        },
        # Фонарик: без урона, только эффекты
        "wep_flashlight": {
            "damage": 0,
            "damage_single": 0,
            "bleeding": 0,
            "rage": 0,
        },
    })

# ------------------------------------------------------------
# ЭФФЕКТЫ УРОВНЯ 2: СТАТУСЫ И ДЕБАФФЫ ХАРАКТЕРИСТИК ВРАГОВ
# ------------------------------------------------------------
# Формат: bleeding, enemy_atk_debuff, enemy_def_debuff, enemy_magic_debuff,
# enemy_accuracy_debuff, enemy_critrate_debuff, enemy_critdmg_debuff
# ------------------------------------------------------------
init python:
    if not hasattr(store, "weapon_consumable_effects_level2"):
        store.weapon_consumable_effects_level2 = {}
    
    store.weapon_consumable_effects_level2.update({
        # Водяной пистолет: статусных дебаффов 2 уровня нет
        "wep_water_pistol": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Водяная бомба: base_bonus_atk -0.03 всех врагов
        "wep_water_bomb": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Зубочистка: кровотечение обрабатывается в уровне 1
        "wep_toothpick": {
            "bleeding": 4,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Резинка: статусных дебаффов 2 уровня нет
        "wep_rubber_band": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Трубочка с бумажкой: -0.02 bonus_atk
        "wep_paper_shooter": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Линейка: –0.05 bonus_def
        "wep_ruler": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_bonus_def_debuff": 0,  # Уменьшает bonus_def врага на 0.05
            "enemy_critrate_debuff": 0,
        },
        # Мыльные пузыри: -0.04 бонус_крит. шанс, -0.04 бонус_крит. урон
        "wep_soap_bubbles": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,  # -0.04 к шансу крита
            "enemy_critdmg_debuff": 0,  # -0.04 к криту урону
        },
        # Листок с сомнительными стихами: базовые статы цели уменьшаются на 1 * poetry_efficiency
        # Зависит от poetry_efficiency у врагов, ослабевает со временем
        "wep_poetry_leaf": {
            "bleeding": 0,
            "enemy_base_atk_debuff": 0,
            "enemy_base_def_debuff": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Бомбочки для ванной: без дебаффов
        "wep_bath_bombs": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
        },
        # Конструктор: без дебаффов (ярость и кровотечение в уровне 1)
        "wep_constructor": {
            "bleeding": 2,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,
            "enemy_critdmg_debuff": -3,
        },
        # Фонарик: шанс крита -0.1
        "wep_flashlight": {
            "bleeding": 0,
            "enemy_bonus_atk_debuff": 0,
            "enemy_atk_debuff": 0,
            "enemy_def_debuff": 0,
            "enemy_critrate_debuff": 0,  # -0.1 к шансу крита врага
        },
    })

# ------------------------------------------------------------
# ЭФФЕКТЫ УРОВНЯ 3: БОНУСЫ И МОДИФИКАТОРЫ ЦЕЛИ
# ------------------------------------------------------------
# Формат: bonus_tank (бонус к танку использовавшего)
# ------------------------------------------------------------
init python:
    if not hasattr(store, "weapon_consumable_effects_level3"):
        store.weapon_consumable_effects_level3 = {}
    
    store.weapon_consumable_effects_level3.update({
        # Водяной пистолет: без бонусов
        "wep_water_pistol": {
            "bonus_tank": 0,
            "enemy_bonus_atk_debuff": 0.05,
            "enemy_speed_debuff": 0.01,
        },
        # Водяная бомба: без бонусов
        "wep_water_bomb": {
            "bonus_tank": 0,
            "enemy_bonus_atk_debuff": 0.03,
        },
        # Зубочистка: без бонусов
        "wep_toothpick": {
            "bonus_tank": 0,
        },
        # Резинка: без бонусов
        "wep_rubber_band": {
            "bonus_tank": 0,
            "enemy_speed_debuff": 0.03,
        },
        # Трубочка с бумажкой: без бонусов
        "wep_paper_shooter": {
            "bonus_tank": 0,
            "enemy_bonus_atk_debuff": 0.02,
        },
        # Линейка: без бонусов
        "wep_ruler": {
            "bonus_tank": 0,
            "enemy_bonus_def_debuff": 0.05,
        },
        # Мыльные пузыри: -0.04 критшанса и критурона у цели
        "wep_soap_bubbles": {
            "bonus_tank": 0,
            "enemy_bonus_critrate_debuff": 0.04,
            "enemy_bonus_critdmg_debuff": 0.04,
        },
        # Листок с сомнительными стихами: без бонусов
        "wep_poetry_leaf": {
            "bonus_tank": 0,
            "enemy_base_atk_debuff": 1,
            "enemy_base_def_debuff": 1,
        },
        # Бомбочки для ванной: без бонусов
        "wep_bath_bombs": {
            "bonus_tank": 0,
        },
        # Конструктор: без бонусов
        "wep_constructor": {
            "bonus_tank": 0,
        },
        # Фонарик: bonus_tank использовавшего +5
        "wep_flashlight": {
            "bonus_tank": 5,
            "enemy_bonus_critrate_debuff": 0.05,
        },
    })

# ------------------------------------------------------------
# СПЕЦИАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ ЛИСТКА СО СТИХАМИ
# ------------------------------------------------------------
# poetry_efficiency уменьшается с каждым использованием
# ------------------------------------------------------------
default poetry_efficiency = 3  # Начальная эффективность (максимум 3 использования)

# ------------------------------------------------------------
# ФУНКЦИЯ ПРИМЕНЕНИЯ ЭФФЕКТОВ ОДНОРАЗОВОГО ОРУЖИЯ
# ------------------------------------------------------------
init python:
    def apply_weapon_consumable_effects(char, item_id, target_enemy=None):
        """
        Применяет эффекты одноразового оружия.
        char - персонаж, использующий предмет
        item_id - ID предмета
        target_enemy - целевой враг (для одиночных атак)
        """
        effects1 = store.weapon_consumable_effects_level1.get(item_id, {})
        effects2 = store.weapon_consumable_effects_level2.get(item_id, {})
        effects3 = store.weapon_consumable_effects_level3.get(item_id, {})

        item_name = getattr(store, "consumable_names", {}).get(item_id, item_id)

        def _resolve_effect_attr(obj, attr_name):
            """Перенаправляет base-статы в mod-поля, если база вычисляется через property."""
            redirected_attr = {
                "base_atk": "base_atk_mod",
                "base_def": "base_def_mod",
                "base_magic": "base_magic_mod",
            }.get(attr_name, attr_name)

            if hasattr(obj, redirected_attr):
                return redirected_attr
            return attr_name if hasattr(obj, attr_name) else None

        def _clamp_set(obj, attr_name, delta, minimum=0):
            """Безопасно добавляет/вычитает значение атрибута."""
            if delta == 0:
                return False

            resolved_attr = _resolve_effect_attr(obj, attr_name)
            if not resolved_attr:
                return False

            current_value = getattr(obj, resolved_attr)
            try:
                new_value = current_value + delta
            except Exception:
                return False
            if minimum is not None:
                new_value = max(minimum, new_value)
            setattr(obj, resolved_attr, new_value)
            return True

        def _apply_to_enemy_attrs(enemy, attr_names, delta, minimum=0):
            """Применяет изменение напрямую к существующим атрибутам врага."""
            for attr_name in attr_names:
                if _clamp_set(enemy, attr_name, delta, minimum):
                    break

        def _is_alive_for_weapon_effects(entity):
            if entity is None or not hasattr(entity, "current_hp"):
                return False
            return getattr(entity, "current_hp", 0) > 0

        enemies_dict = getattr(store, "enemies", {}) if hasattr(store, "enemies") else {}
        heroes_dict = getattr(store, "pers_dict", {}) if hasattr(store, "pers_dict") else {}
        active_enemy_names = get_active_enemies() if "get_active_enemies" in globals() else []
        active_enemies = [
            enemies_dict[name]
            for name in active_enemy_names
            if name in enemies_dict and _is_alive_for_weapon_effects(enemies_dict[name])
        ]

        # Активные герои в бою: живые и отмеченные как picked.
        active_heroes = []
        for hero in heroes_dict.values():
            if not hasattr(hero, "current_hp"):
                continue
            is_picked = getattr(hero, "picked", 1) == 1
            if is_picked and hero.current_hp > 0:
                active_heroes.append(hero)

        def _capture_weapon_visual_state(entity):
            tracked_fields = (
                "current_hp",
                "shield",
                "bloodshed_debuff",
                "prone_debuff",
                "atk_debuff",
                "def_debuff",
                "magic_debuff",
                "accuracy_debuff",
                "critrate_debuff",
                "critdmg_debuff",
            )
            state = {field: getattr(entity, field, 0) for field in tracked_fields}

            bonus_fields = {
                "bonus_atk_visual": ("bonus_atk2", "bonus_atk"),
                "bonus_def_visual": ("bonus_def2", "bonus_def"),
                "bonus_magic_visual": ("bonus_magic2", "bonus_magic"),
                "bonus_accuracy_visual": ("bonus_dmgchance2", "bonus_dmgchance"),
                "bonus_critrate_visual": ("bonus_critrate2", "bonus_critrate"),
                "bonus_critdmg_visual": ("bonus_crit2", "bonus_crit"),
                "bonus_tank_visual": ("bonus_tank2", "bonus_tank"),
            }

            for state_name, attr_names in bonus_fields.items():
                state[state_name] = 0
                for attr_name in attr_names:
                    if hasattr(entity, attr_name):
                        state[state_name] = getattr(entity, attr_name)
                        break

            state["base_atk_mod_visual"] = getattr(entity, "base_atk_mod", 0)
            state["base_def_mod_visual"] = getattr(entity, "base_def_mod", 0)

            return state

        def _apply_weapon_visual_state(entity, old_state):
            hp_delta = getattr(entity, "current_hp", 0) - old_state["current_hp"]
            shield_delta = getattr(entity, "shield", 0) - old_state["shield"]

            if hp_delta < 0:
                entity.damage_gain_for_vis = -hp_delta
                store.update_swoon_pending_for_visual(entity, old_state["current_hp"])
            elif hp_delta > 0:
                entity.damage_gain_for_vis = -hp_delta
                store.clear_swoon_pending_for_visual(entity)
            elif shield_delta != 0:
                entity.damage_gain_for_vis = 1
                store.clear_swoon_pending_for_visual(entity)
            else:
                entity.damage_gain_for_vis = -1
                store.clear_swoon_pending_for_visual(entity)

            entity.got_crit_for_visual = 0

            for debuff_name in (
                "bloodshed_debuff",
                "prone_debuff",
                "atk_debuff",
                "def_debuff",
                "magic_debuff",
                "accuracy_debuff",
                "critrate_debuff",
                "critdmg_debuff",
            ):
                old_value = old_state.get(debuff_name, 0)
                new_value = getattr(entity, debuff_name, 0)
                setattr(entity, debuff_name + "_got", new_value - old_value)

            bonus_to_visual = (
                ("bonus_atk_visual", "atk_debuff_got"),
                ("bonus_def_visual", "def_debuff_got"),
                ("bonus_magic_visual", "magic_debuff_got"),
                ("bonus_accuracy_visual", "accuracy_debuff_got"),
                ("bonus_critrate_visual", "critrate_debuff_got"),
                ("bonus_critdmg_visual", "critdmg_debuff_got"),
                ("bonus_tank_visual", "tank_debuff_got"),
            )

            for bonus_field, visual_field in bonus_to_visual:
                old_value = old_state.get(bonus_field, 0)
                new_value = old_value

                if bonus_field == "bonus_atk_visual":
                    new_value = getattr(entity, "bonus_atk2", getattr(entity, "bonus_atk", old_value))
                elif bonus_field == "bonus_def_visual":
                    new_value = getattr(entity, "bonus_def2", getattr(entity, "bonus_def", old_value))
                elif bonus_field == "bonus_magic_visual":
                    new_value = getattr(entity, "bonus_magic2", getattr(entity, "bonus_magic", old_value))
                elif bonus_field == "bonus_accuracy_visual":
                    new_value = getattr(entity, "bonus_dmgchance2", getattr(entity, "bonus_dmgchance", old_value))
                elif bonus_field == "bonus_critrate_visual":
                    new_value = getattr(entity, "bonus_critrate2", getattr(entity, "bonus_critrate", old_value))
                elif bonus_field == "bonus_critdmg_visual":
                    new_value = getattr(entity, "bonus_crit2", getattr(entity, "bonus_crit", old_value))
                elif bonus_field == "bonus_tank_visual":
                    new_value = getattr(entity, "bonus_tank2", getattr(entity, "bonus_tank", old_value))

                setattr(entity, visual_field, getattr(entity, visual_field, 0) - (new_value - old_value))

            base_atk_mod_delta = getattr(entity, "base_atk_mod", 0) - old_state.get("base_atk_mod_visual", 0)
            if base_atk_mod_delta != 0:
                entity.atk_debuff_got = getattr(entity, "atk_debuff_got", 0) - base_atk_mod_delta

            base_def_mod_delta = getattr(entity, "base_def_mod", 0) - old_state.get("base_def_mod_visual", 0)
            if base_def_mod_delta != 0:
                entity.def_debuff_got = getattr(entity, "def_debuff_got", 0) - base_def_mod_delta

        tracked_entities = {}
        for entity in active_enemies + active_heroes:
            tracked_entities[id(entity)] = entity
        if char is not None:
            tracked_entities[id(char)] = char
        if target_enemy is not None:
            tracked_entities[id(target_enemy)] = target_enemy

        visual_states = {
            entity_id: _capture_weapon_visual_state(entity)
            for entity_id, entity in tracked_entities.items()
        }

        # Для одиночных эффектов принимаем цель только если она принадлежит текущему бою.
        # Применяем урон
        damage = effects1.get("damage", 0)
        damage_single = effects1.get("damage_single", 0)
        damage_allies = effects1.get("damage_allies", 0)
        valid_targets = active_enemies + active_heroes
        is_target_active = target_enemy in valid_targets if target_enemy is not None else False
        target_had_shield = is_target_active and getattr(target_enemy, "shield", 0) > 0
        apply_to_all_enemies = effects2.get("apply_to_all_enemies", False) or (damage > 0 and damage_single == 0)
        target_entities = active_enemies if apply_to_all_enemies else ([target_enemy] if is_target_active else active_enemies)
        
        # Урон всем врагам
        if damage > 0:
            for enemy in active_enemies:
                if not hasattr(enemy, "current_hp"):
                    continue
                if getattr(enemy, "shield", 0) > 0:
                    enemy.shield -= 1
                    enemy.damage_gain_for_vis = 1
                    if hasattr(enemy, "got_crit_for_visual"):
                        enemy.got_crit_for_visual = 0
                    renpy.notify("Урон поглощен щитом у {}!".format(
                        getattr(enemy, "name", "Враг")))
                    continue
                enemy.current_hp = max(0, enemy.current_hp - damage)
                renpy.notify("{} получает {} урона!".format(
                    getattr(enemy, "name", "Враг"), damage))

        # Урон одной цели
        if damage_single > 0 and is_target_active:
            if hasattr(target_enemy, "current_hp"):
                if getattr(target_enemy, "shield", 0) > 0:
                    target_enemy.shield -= 1
                    target_enemy.damage_gain_for_vis = 1
                    if hasattr(target_enemy, "got_crit_for_visual"):
                        target_enemy.got_crit_for_visual = 0
                    renpy.notify("Урон поглощен щитом у {}!".format(
                        getattr(target_enemy, "name", "Цель")))
                else:
                    target_enemy.current_hp = max(0, target_enemy.current_hp - damage_single)
                    renpy.notify("{} получает {} урона!".format(
                        getattr(target_enemy, "name", "Цель"), damage_single))

        # Урон по союзникам (для бомбочек)
        if damage_allies > 0 and hasattr(store, "pers_dict"):
            for ally in store.pers_dict.values():
                if not _is_alive_for_weapon_effects(ally):
                    continue
                if getattr(ally, "shield", 0) > 0:
                    ally.shield -= 1
                    ally.damage_gain_for_vis = 1
                    if hasattr(ally, "got_crit_for_visual"):
                        ally.got_crit_for_visual = 0
                    renpy.notify("Урон поглощен щитом у {}!".format(
                        getattr(ally, "name", "Союзник")))
                    continue
                ally_old_hp = ally.current_hp
                ally.current_hp = max(0, ally.current_hp - damage_allies)
                # Пассивки Криса: «Вмятины на щите» и «Желание жить».
                kris_passive_on_hero_damage(ally, ally_old_hp)
                # Пассивки Азриеля: «Лоб в лоб», «Стойкий», «Рука помощи».
                azri_on_damage_taken(ally, ally_old_hp)
                azri_try_helping_hand(ally)

        # Статусные эффекты лежат во 2 уровне вместе с прочими системными дебаффами.
        bleeding_turns = effects2.get("bleeding", 0)
        if bleeding_turns > 0 and is_target_active and not target_had_shield:
            if hasattr(target_enemy, "bloodshed_debuff"):
                target_enemy.bloodshed_debuff += bleeding_turns
                if hasattr(target_enemy, "bloodshed_debuff_got"):
                    target_enemy.bloodshed_debuff_got += bleeding_turns
            else:
                if not hasattr(target_enemy, "bleeding_turns"):
                    target_enemy.bleeding_turns = 0
                target_enemy.bleeding_turns += bleeding_turns
            renpy.notify("У {} кровотечение на {} хода!".format(
                getattr(target_enemy, "name", "Цели"), bleeding_turns))
        
        # Применяем дебаффы целям.
        enemy_atk_debuff = effects2.get("enemy_atk_debuff", 0)
        enemy_magic_debuff = effects2.get("enemy_magic_debuff", 0)
        enemy_critrate_debuff = effects2.get("enemy_critrate_debuff", 0)
        enemy_critdmg_debuff = effects2.get("enemy_critdmg_debuff", 0)
        enemy_accuracy_debuff = effects2.get("enemy_accuracy_debuff", 0)
        enemy_def_debuff = effects2.get("enemy_def_debuff", 0)

        # Уровень 3: поддерживаем и новое имя ключа, и legacy-вариант *_debuff.
        enemy_bonus_atk = effects3.get("enemy_bonus_atk", effects3.get("enemy_bonus_atk_debuff", 0))
        enemy_bonus_magic = effects3.get("enemy_bonus_magic", effects3.get("enemy_bonus_magic_debuff", 0))
        enemy_bonus_critrate = effects3.get("enemy_bonus_critrate", effects3.get("enemy_bonus_critrate_debuff", 0))
        enemy_bonus_critdmg = effects3.get("enemy_bonus_critdmg", effects3.get("enemy_bonus_critdmg_debuff", 0))
        enemy_bonus_accuracy = effects3.get("enemy_bonus_accuracy", effects3.get("enemy_bonus_accuracy_debuff", 0))
        enemy_bonus_def = effects3.get("enemy_bonus_def", effects3.get("enemy_bonus_def_debuff", 0))
        enemy_speed_debuff = effects3.get("enemy_speed_debuff", 0)

        enemy_base_atk = effects3.get("enemy_base_atk", effects3.get("enemy_base_atk_debuff", 0))
        enemy_base_def = effects3.get("enemy_base_def", effects3.get("enemy_base_def_debuff", 0))

        def _apply_debuff_bonus_changes(entity, atk_debuff_delta=0, def_debuff_delta=0, magic_debuff_delta=0,
                                        accuracy_debuff_delta=0, critrate_debuff_delta=0, critdmg_debuff_delta=0):
            """
            Применяет мгновенные изменения бонусных характеристик при получении дебаффа.
            Для всех статов шаг изменения фиксирован: 0.05 за стак.
            """
            def _shift_attr(attr_names, delta):
                if delta == 0:
                    return
                for attr_name in attr_names:
                    if not hasattr(entity, attr_name):
                        continue
                    old_value = getattr(entity, attr_name)
                    new_value = max(0.0, old_value + delta)
                    setattr(entity, attr_name, round(new_value, 2))

            # >0 — дебафф (снижаем), <0 — бафф (повышаем)
            atk_shift = -0.05 * atk_debuff_delta
            def_shift = -0.05 * def_debuff_delta
            magic_shift = -0.05 * magic_debuff_delta
            accuracy_shift = -0.05 * accuracy_debuff_delta
            critrate_shift = -0.05 * critrate_debuff_delta
            critdmg_shift = -0.05 * critdmg_debuff_delta

            _shift_attr(("bonus_atk", "bonus_atk2"), atk_shift)
            _shift_attr(("bonus_def", "bonus_def2"), def_shift)
            _shift_attr(("bonus_magic", "bonus_magic2"), magic_shift)
            _shift_attr(("bonus_dmgchance", "bonus_dmgchance2", "accuracy"), accuracy_shift)
            _shift_attr(("bonus_critrate2", "bonus_critrate", "critrate2", "critrate"), critrate_shift)
            _shift_attr(("critdmg", "bonus_crit", "bonus_crit2", "crit_damage"), critdmg_shift)

        for target_entity in target_entities:
            if not _is_alive_for_weapon_effects(target_entity):
                continue

            is_hero_target = getattr(target_entity, "is_ally", False) or target_entity in active_heroes

            if item_id == "wep_poetry_leaf":
                poetry_eff = max(0, int(getattr(target_entity, "poetry_efficiency", 3)))

                if poetry_eff > 0:
                    if enemy_base_atk:
                        _clamp_set(target_entity, "base_atk_mod", -(enemy_base_atk * poetry_eff), None)
                    if enemy_base_def:
                        _clamp_set(target_entity, "base_def_mod", -(enemy_base_def * poetry_eff), None)
                    target_entity.poetry_efficiency = max(0, poetry_eff - 1)
                continue

            _apply_to_enemy_attrs(target_entity, ("bonus_atk2", "bonus_atk", "attack"), -enemy_bonus_atk)
            _apply_to_enemy_attrs(target_entity, ("bonus_magic2", "bonus_magic"), -enemy_bonus_magic)
            _apply_to_enemy_attrs(target_entity, ("bonus_critrate2", "bonus_critrate", "critrate2", "critrate"), -enemy_bonus_critrate)
            _apply_to_enemy_attrs(target_entity, ("bonus_crit2", "bonus_crit", "critdmg", "crit_damage"), -enemy_bonus_critdmg)
            _apply_to_enemy_attrs(target_entity, ("bonus_dmgchance2", "bonus_dmgchance", "accuracy"), -enemy_bonus_accuracy)

            # Применяем дебафф атаки и сразу меняем бонусные характеристики
            if enemy_atk_debuff > 0 and hasattr(target_entity, "atk_debuff"):
                old_atk_debuff = target_entity.atk_debuff
                target_entity.atk_debuff += enemy_atk_debuff
                atk_debuff_delta = target_entity.atk_debuff - old_atk_debuff
                _apply_debuff_bonus_changes(target_entity, atk_debuff_delta=atk_debuff_delta)

            _apply_to_enemy_attrs(target_entity, ("bonus_def2", "bonus_def", "base_def"), -enemy_bonus_def)

            if enemy_speed_debuff > 0:
                if is_hero_target:
                    store.soul_speed = store.clamp_soul_speed(getattr(store, "soul_speed", 10) - enemy_speed_debuff * 10)
                elif hasattr(target_entity, "speed"):
                    target_entity.speed = store.clamp_enemy_speed(target_entity.speed * (1 - enemy_speed_debuff))

            _apply_to_enemy_attrs(target_entity, ("attack", "base_atk", "atk"), -enemy_base_atk)
            _apply_to_enemy_attrs(target_entity, ("base_def", "defense", "def"), -enemy_base_def)

            # Применяем дебафф защиты и сразу меняем бонусные характеристики
            if enemy_def_debuff > 0:
                if hasattr(target_entity, "def_debuff"):
                    old_def_debuff = target_entity.def_debuff
                    target_entity.def_debuff += enemy_def_debuff
                    def_debuff_delta = target_entity.def_debuff - old_def_debuff
                    _apply_debuff_bonus_changes(target_entity, def_debuff_delta=def_debuff_delta)
                elif hasattr(target_entity, "bonus_def2"):
                    target_entity.bonus_def2 = max(0, target_entity.bonus_def2 * (1 - enemy_def_debuff))

            # Применяем дебафф магзащиты и сразу меняем бонусные характеристики
            if enemy_magic_debuff > 0:
                if hasattr(target_entity, "magic_debuff"):
                    old_magic_debuff = target_entity.magic_debuff
                    target_entity.magic_debuff += enemy_magic_debuff
                    magic_debuff_delta = target_entity.magic_debuff - old_magic_debuff
                    _apply_debuff_bonus_changes(target_entity, magic_debuff_delta=magic_debuff_delta)

            # Применяем дебафф крит шанса и сразу меняем бонусные характеристики
            if enemy_critrate_debuff > 0:
                if hasattr(target_entity, "critrate_debuff"):
                    old_critrate_debuff = target_entity.critrate_debuff
                    target_entity.critrate_debuff += enemy_critrate_debuff
                    critrate_debuff_delta = target_entity.critrate_debuff - old_critrate_debuff
                    _apply_debuff_bonus_changes(target_entity, critrate_debuff_delta=critrate_debuff_delta)
                else:
                    _apply_to_enemy_attrs(target_entity, ("bonus_critrate2", "bonus_critrate", "critrate2", "critrate"), -enemy_critrate_debuff)

            # Применяем дебафф крит урона и сразу меняем бонусные характеристики
            if enemy_critdmg_debuff != 0:
                if is_hero_target and hasattr(target_entity, "critdmg_debuff_var"):
                    current_critdmg_var = getattr(target_entity, "critdmg_debuff_var", 0.0)
                    if enemy_critdmg_debuff > 0:
                        current_critdmg_var -= 0.05 * enemy_critdmg_debuff
                    elif enemy_critdmg_debuff < 0:
                        current_critdmg_var += 0.05 * abs(enemy_critdmg_debuff)
                    new_critdmg_var = round(current_critdmg_var, 2)
                    try:
                        target_entity.critdmg_debuff_var = new_critdmg_var
                    except Exception:
                        if hasattr(target_entity, "critdmg_debuff"):
                            target_entity.critdmg_debuff = int(round(-new_critdmg_var / 0.1))
                elif hasattr(target_entity, "critdmg_debuff"):
                    old_critdmg_debuff = target_entity.critdmg_debuff
                    target_entity.critdmg_debuff += enemy_critdmg_debuff
                    critdmg_debuff_delta = target_entity.critdmg_debuff - old_critdmg_debuff
                    _apply_debuff_bonus_changes(target_entity, critdmg_debuff_delta=critdmg_debuff_delta)
                else:
                    _apply_to_enemy_attrs(target_entity, ("bonus_crit2", "bonus_crit", "critdmg", "crit_damage"), -enemy_critdmg_debuff)

            # Применяем дебафф точности и сразу меняем бонусные характеристики
            if enemy_accuracy_debuff > 0:
                if hasattr(target_entity, "accuracy_debuff"):
                    old_accuracy_debuff = target_entity.accuracy_debuff
                    target_entity.accuracy_debuff += enemy_accuracy_debuff
                    accuracy_debuff_delta = target_entity.accuracy_debuff - old_accuracy_debuff
                    _apply_debuff_bonus_changes(target_entity, accuracy_debuff_delta=accuracy_debuff_delta)

        # Применяем бонусы tank
        bonus_tank = effects3.get("bonus_tank", 0)
        tank_target = char
        if item_id == "wep_flashlight" and is_target_active:
            target_is_hero = getattr(target_enemy, "is_ally", False) or target_enemy in active_heroes
            if target_is_hero:
                tank_target = target_enemy

        if bonus_tank > 0 and hasattr(tank_target, "bonus_tank"):
            tank_target.bonus_tank += bonus_tank
            renpy.notify("{} получает +{} к танку!".format(
                getattr(tank_target, "name", "Персонаж"), bonus_tank))
        
        for entity_id, entity in tracked_entities.items():
            _apply_weapon_visual_state(entity, visual_states[entity_id])

        renpy.notify("{} применён(о).".format(item_name))

# ------------------------------------------------------------
# ЭКРАН ДЛЯ ОТОБРАЖЕНИЯ poetry_efficiency (для каждого врага)
# ------------------------------------------------------------
screen poetry_efficiency_display():
    zorder 100

    if hasattr(store, "enemies"):
        vbox:
            xalign 0.5
            yalign 0.1
            spacing 5

            for enemy_id, enemy in store.enemies.items():
                $ poetry_eff = getattr(enemy, "poetry_efficiency", 0)
                if poetry_eff > 0:
                    text "{font=determination.otf}{size=18}[getattr(enemy, 'name', 'Враг')]: [poetry_eff]/3{/font}{/size}" color "#ff66ff"
















# ============================================================================
# ФУНКЦИИ БАФОВ ДЛЯ МАГИИ СЕДРИКА (ГОТОВКА)
# ============================================================================
# Каждая функция применяет эффекты блюда к персонажу
# Эффекты умножаются на amount (количество порций для персонажа)
# 
# ВАЖНО: Используется новая система с bonus_x
# - Для мультипликативных характеристик (атака, магия, защита): изменяем bonus_x
# - bonus_x работает как множитель (1.0 = 100%, 1.05 = 105%)
# ============================================================================

init  python:
    
    # ========================================================================
    # SEDRICMAG1: Сбегать за продуктами
    # ========================================================================
    # Восстанавливает ингредиенты (не б��ф персонажу)
    # ВАЖНО: Седрик временно покидает бой, его tank обнуляется
    def sedric_mag1_effect():
        """Сбегать за продуктами - восстанавливает ингредиенты"""
        sedric = store.characters.get("Седрик")
        
        if sedric:
            # ============================================================
            # РЕЗЕРВИРОВАНИЕ ПАРАМЕТРОВ TANK
            # ============================================================
            # Резервируем bonus_tank для последующего восстановления
            if not hasattr(sedric, 'reserved_bonus_tank'):
                sedric.reserved_bonus_tank = sedric.bonus_tank
            else:
                # Если уже есть резерв, обновляем его текущим значением
                sedric.reserved_bonus_tank = sedric.bonus_tank
            
            # Резервируем изначальные значения base_tank и extra_tank
            # Эти значения будут восстановлены автоматически
            if not hasattr(sedric, 'original_base_tank'):
                sedric.original_base_tank = 10  # Изначальное значен��е base_tank
            if not hasattr(sedric, 'original_extra_tank'):
                sedric.original_extra_tank = 15  # Изначальное значение extra_tank
            
            # ============================================================
            # ОБНУЛЕНИЕ TANK (Седрик покидает бой)
            # ============================================================
            sedric.base_tank = 0
            sedric.bonus_tank = 0
            sedric.extra_tank = 0
            
            renpy.log("Седрик покинул бой и побежал за продуктами!")
        
        # Обновляем ингредиенты от текущего уровня Седрика
        store.cooking_manager.update_from_sedric()
    
    
    # ========================================================================
    # ФУНКЦИЯ ВОЗВРАЩЕНИЯ СЕДРИКА В БОЙ
    # ========================================================================
    def sedric_return_to_battle():
        """Возвращает Седрика в бой, восстанавливая его tank параметры"""
        sedric = store.characters.get("Седрик")
        
        if sedric:
            # Восстанавливаем base_tank и extra_tank к изна��альным значениям
            if hasattr(sedric, 'original_base_tank'):
                sedric.base_tank = sedric.original_base_tank
            else:
                sedric.base_tank = 10  # Значение по умолчанию
            
            if hasattr(sedric, 'original_extra_tank'):
                sedric.extra_tank = sedric.original_extra_tank
            else:
                sedric.extra_tank = 15  # Значение по умолчанию
            
            # bonus_tank НЕ восстанавливаем автоматически!
            # Он будет восстановлен вручную через restore_sedric_bonus_tank()
            # или останется 0 до следующего бафа
            
            renpy.log("Седрик вернулся в бой!")
    
    
    # ========================================================================
    # ФУНКЦИЯ ВОССТАНОВЛЕНИЯ BONUS_TANK СЕДРИКА
    # ========================================================================
    def restore_sedric_bonus_tank():
        """Восстанавливает зарезервированный bonus_tank Седрика"""
        sedric = store.characters.get("Седрик")
        
        if sedric and hasattr(sedric, 'reserved_bonus_tank'):
            sedric.bonus_tank = sedric.reserved_bonus_tank
            renpy.log(f"Седрик: bonus_tank восстановлен ({sedric.bonus_tank})")
        else:
            renpy.log("Седрик: нет зарезервированного bonus_tank")
    
    
    # ========================================================================
    # SEDRICMAG2: Яичница на завтрак
    # ========================================================================
    # Восполняет 10% хп и увеличивает силу атаки на 5%
    def sedric_mag2_effect(char, amount):
        """Яичница на завтрак - 10% хп + 5% атака"""
        if amount > 0:
            # Восстановление HP (10% за порцию)
            hp_restore = int(char.max_hp * 0.10 * amount)
            char.change_hp(hp_restore)
            
            # Увеличение атаки (5% за порцию) - МУЛЬТИПЛИКАТИВНЫЙ БОНУС
            # bonus_atk работает как множитель: 1.0 = 100%, 1.05 = 105%
            char.bonus_atk += 0.05 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{int(0.05 * amount * 100)}% атака")
    
    
    # ========================================================================
    # SEDRICMAG3: Булочка
    # ========================================================================
    # Восполняет 8% хп
    def sedric_mag3_effect(char, amount):
        """Булочка - 8% хп"""
        if amount > 0:
            # Восстановление HP (8% за порцию)
            hp_restore = int(char.max_hp * 0.08 * amount)
            char.change_hp(hp_restore)
            
            renpy.log(f"{char.name}: +{hp_restore} HP")
    
    
    # ========================================================================
    # SEDRICMAG4: Салат Цезарь
    # ========================================================================
    # 10% хп + 20 мп + 10% маг урона
    def sedric_mag4_effect(char, amount):
        """Салат Цезарь - 10% хп + 20 мп + 10% маг урона"""
        if amount > 0:
            # Восстановление HP (10% за порцию)
            hp_restore = int(char.max_hp * 0.10 * amount)
            char.change_hp(hp_restore)
            
            # Восстановление MP (20 за порцию)
            mp_restore = 20 * amount
            char.current_mp = min(char.current_mp + mp_restore, char.max_mp)
            
            # Увеличение магического урона (10% за порцию) - МУЛЬТИПЛИКАТИВНЫЙ БОНУС
            if hasattr(char, 'bonus_magic'):
                char.bonus_magic += 0.10 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{mp_restore} MP, +{int(0.10 * amount * 100)}% маг.урон")
    
    
    # ========================================================================
    # SEDRICMAG5: Сэндвич
    # ========================================================================
    # Восполняет 20% хп и замедляет перемещение пуль противника
    def sedric_mag5_effect(char, amount):
        """Сэндвич - 20% хп + замедление пуль врага"""
        if amount > 0:
            # Восстановление HP (20% за порцию)
            hp_restore = int(char.max_hp * 0.20 * amount)
            char.change_hp(hp_restore)
            
            # TODO: Добавить эффект замедления пуль врага
            # Это требует реализации систем�� статусов врагов
            
            renpy.log(f"{char.name}: +{hp_restore} HP, замедление пуль врага")
    
    
    # ========================================================================
    # SEDRICMAG6: Блинчики с кленовым сиропом
    # ========================================================================
    # 50% мп + 25% защита
    def sedric_mag6_effect(char, amount):
        """Блинчики с кленовым сиропом - 50% мп + 25% защита"""
        if amount > 0:
            # Восстановление MP (50% за порцию)
            mp_restore = int(char.max_mp * 0.50 * amount)
            char.current_mp = min(char.current_mp + mp_restore, char.max_mp)
            
            # Увеличение защиты (25% за порцию) - МУЛЬТИПЛИКАТИВНЫЙ БОНУС
            char.bonus_def += 0.25 * amount
            
            renpy.log(f"{char.name}: +{mp_restore} MP, +{int(0.25 * amount * 100)}% защита")
    
    
    # ========================================================================
    # SEDRICMAG7: Чизбургер
    # ========================================================================
    # Шанс попасть -20%, хп + 50%, защита + 15%
    def sedric_mag7_effect(char, amount):
        """Чизбургер - 50% хп + 15% защита - 20% точность"""
        if amount > 0:
            # Восстановление HP (50% за порцию)
            hp_restore = int(char.max_hp * 0.50 * amount)
            char.change_hp(hp_restore)
            
            # Увеличение защиты (15% за порцию) - МУЛЬТИПЛИКАТИВНЫЙ БОНУС
            char.bonus_def += 0.15 * amount
            
            # Уменьшение точности (20% за порцию) - АДДИТИВНЫЙ ШТРАФ
            char.bonus_dmgchance -= 0.20 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{int(0.15 * amount * 100)}% защита, -{int(0.20 * amount * 100)}% точность")
    
    
    # ========================================================================
    # SEDRICMAG8: Суши
    # ========================================================================
    # Шанс попасть +20% хп + 10%
    def sedric_mag8_effect(char, amount):
        """Суши - 10% хп + 20% точность"""
        if amount > 0:
            # Восстановление HP (10% за порцию)
            hp_restore = int(char.max_hp * 0.10 * amount)
            char.change_hp(hp_restore)
            
            # Увеличение точности (20% за порцию) - АДДИТИВНЫЙ БОНУС
            char.bonus_dmgchance += 0.20 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{int(0.20 * amount * 100)}% точность")
    
    
    # ========================================================================
    # SEDRICMAG9: Мясо на гриле
    # ========================================================================
    # 50% хп + 5% Крит урона + 2% Крит шанса
    def sedric_mag9_effect(char, amount):
        """Мясо на гриле - 50% хп + 5% крит.урон + 2% крит.шанс"""
        if amount > 0:
            # Восстановление HP (50% за порцию)
            hp_restore = int(char.max_hp * 0.50 * amount)
            char.change_hp(hp_restore)
            
            # Увеличение крит урона (5% за порцию) - АДДИТИВНЫЙ БОНУС
            char.bonus_crit += 0.05 * amount
            
            # Увеличение крит шанса (2% за порцию) - АДДИТИВНЫЙ БОНУС
            char.bonus_critrate += 0.02 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{int(0.05 * amount * 100)}% крит.урон, +{int(0.02 * amount * 100)}% крит.шанс")
    
    
    # ========================================================================
    # SEDRICMAG10: Пицца!
    # ========================================================================
    # +30% хп + 20% маг урона + 20% шанс попасть
    def sedric_mag10_effect(char, amount):
        """Пицца! - 30% хп + 20% маг.урон + 20% точность"""
        if amount > 0:
            # Восстановление HP (30% за порцию)
            hp_restore = int(char.max_hp * 0.30 * amount)
            char.change_hp(hp_restore)
            
            # Увеличение магического урона (20% за порцию) - МУЛЬТИПЛИКАТИВНЫЙ БОНУС
            if hasattr(char, 'bonus_magic'):
                char.bonus_magic += 0.20 * amount
            
            # Увеличение точности (20% за порцию) - АДДИТИВНЫЙ БОНУС
            char.bonus_dmgchance += 0.20 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{int(0.20 * amount * 100)}% маг.урон, +{int(0.20 * amount * 100)}% точность")
    
    
    # ========================================================================
    # УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ПРИМЕНЕНИЯ БАФОВ
    # ========================================================================
    def apply_sedric_magic_buffs(magic_index):
        """
        Применяет бафы от магии Седрика ко всем персонажам в команде
        на основе их amount в cooking_manager.feed_amount
        
        Args:
            magic_index (str): Индекс магии (например, "Sedricmag2")
        """
        # Словарь соответствия магии и функций
        magic_functions = {
            "Sedricmag1": sedric_mag1_effect,  # Особый случай - не требует персонажей
            "Sedricmag2": sedric_mag2_effect,
            "Sedricmag3": sedric_mag3_effect,
            "Sedricmag4": sedric_mag4_effect,
            "Sedricmag5": sedric_mag5_effect,
            "Sedricmag6": sedric_mag6_effect,
            "Sedricmag7": sedric_mag7_effect,
            "Sedricmag8": sedric_mag8_effect,
            "Sedricmag9": sedric_mag9_effect,
            "Sedricmag10": sedric_mag10_effect,
        }
        
        # Особый случай для Sedricmag1 (сбегать за продуктами)
        if magic_index == "Sedricmag1":
            sedric_mag1_effect()
            return
        
        # Получаем функцию для данной магии
        magic_func = magic_functions.get(magic_index)
        
        if magic_func:
            # Применяем эффект ко всем персонажам с amount > 0
            for char_name, amount in store.cooking_manager.feed_amount.items():
                if amount > 0 and char_name in store.characters:
                    char = store.characters[char_name]
                    magic_func(char, amount)
        else:
            renpy.log(f"Магия {magic_index} не найдена!")


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ЯИЧНИЦЫ С БЕКОНОМ (5 УРОВЕНЬ)
# ============================================================================
# Это улучшенная версия Sedricmag2, доступная с 5 уровня

init  python:
    
    def sedric_mag2_upgraded_effect(char, amount):
        """Яичница с беконом (улучшенная) - 15% хп + 7% атака"""
        if amount > 0:
            # Восстановление HP (15% за порцию)
            hp_restore = int(char.max_hp * 0.15 * amount)
            char.change_hp(hp_restore)
            
            # Увеличение атаки (7% за порцию) - МУЛЬТИПЛИКАТИВНЫЙ БОНУС
            char.bonus_atk += 0.07 * amount
            
            renpy.log(f"{char.name}: +{hp_restore} HP, +{int(0.07 * amount * 100)}% атака")


# ============================================================================
# ФУНКЦИИ ДЛЯ СБРОСА БАФОВ
# ============================================================================
# Используйте эти функции для сброса бафов после боя или при необходимости

init  python:
    
    def reset_character_buffs(char):
        """Сбрасывает все временные бафы персонажа к значениям по умолчанию"""
        # Сброс мультипликативных бонусов (возврат к 1.0)
        char.bonus_atk = 1
        char.bonus_magic = 1
        char.bonus_def = 1
        
        # Сброс аддитивных бонусов (во��врат к 0)
        char.bonus_dmgchance = 0
        char.bonus_critrate = 0
        char.bonus_crit = 0
        char.bonus_tank = 0
        
        renpy.log(f"{char.name}: бафы сброшены")
    
    
    def reset_all_buffs():
        """Сбрасывает бафы вс��х персонажей"""
        for char_name, char in store.characters.items():
            reset_character_buffs(char)
        
        renpy.log("Все бафы сброшены!")


# ============================================================================
# СПРАВОЧНАЯ ИНФОРМАЦИЯ
# ============================================================================
# 
# ТИПЫ БОНУСОВ:
# 
# 1. МУЛЬТИПЛИКАТИВНЫЕ (работают как множители):
#    - bonus_atk (атака)
#    - bonus_magic (магия)
#    - bonus_def (защита)
#    По умолчанию = 1.0 (100%)
#    Пример: bonus_atk = 1.05 означает +5% к атаке
# 
# 2. АДДИТИВНЫЕ (работают как прибавки):
#    - bonus_dmgchance (точность)
#    - bonus_critrate (шанс крита)
#    - bonus_crit (крит урон)
#    - bonus_tank (шанс получить урон)
#    По умолчанию = 0
#    Пример: bonus_dmgchance = 0.20 означает +20% к точности
# 
# ============================================================================
# СИСТЕМА TANK ДЛЯ СЕДРИКА
# ============================================================================
# 
# Когда Седрик использует "Сбегать за продуктами" (Sedricmag1):
# 
# 1. РЕЗЕРВИРУЮТСЯ:
#    - bonus_tank → reserved_bonus_tank (сохраняется для восстановления)
#    - original_base_tank = 10 (изначальное значение)
#    - original_extra_tank = 15 (изначальное значение)
# 
# 2. ОБНУЛЯЮТСЯ (Седрик покидает бой):
#    - base_tank = 0
#    - bonus_tank = 0
#    - extra_tank = 0
#    Результат: total_tank = 0, Седрик не может получить урон
# 
# 3. ВОССТАНОВЛЕНИЕ:
#    
#    А) Автоматическое (base_tank и extra_tank):
#       $ sedric_return_to_battle()
#       - base_tank → 10 (восстановлено)
#       - extra_tank → 15 (восстановлено)
#       - bonus_tank → 0 (НЕ восстановлен!)
#    
#    Б) Ручное (bonus_tank):
#       $ restore_sedric_bonus_tank()
#       - bonus_tank → reserved_bonus_tank (восстановле��о)
# 
# ПРИМЕР ИСПОЛЬЗОВАНИЯ:
# 
# # Седрик бежит за продуктами (автоматически при Sedricmag1)
# # tank обнуляется
# 
# # Седрик возвращается в бой
# $ sedric_return_to_battle()
# 
# # Позже восстанавливаем bonus_tank
# $ restore_sedric_bonus_tank()
# 
# ============================================================================
# 
# ФОРМУЛЫ:
# 
# Атака:
# ATK = (base_atk + (base_atk_mod × bonus_atk_mod × atk_sphere_multiply)) × bonus_atk × rtlns_mod
# 
# Магия:
# MAGIC = (base_magic + (base_magic_mod × bonus_magic_mod × magic_sphere_multiply)) × bonus_magic × rtlns_mod
# 
# Защита:
# DEFENSE = (base_def + (base_def_mod × bonus_def_mod × def_sphere_multiply)) × bonus_def × rtlns_mod_for_def
# 
# Точность:
# DMGCHANCE = (base_dmgchance + (dmgchance_mod × dmgchance_sphere_multiply)) + bonus_dmgchance
# 
# Шанс крита:
# CRITRATE = (base_critrate + (critrate_mod × critrate_sphere_multiply)) + bonus_critrate + сверхточность
# 
# Крит урон:
# CRIT = (base_crit + (crit_mod × crit_sphere_multiply)) + bonus_crit + сверхкрит
# 
# Tank (шанс получить урон):
# TOTAL_TANK = (base_tank + extra_tank + bonus_tank + prone_tank_bonus + tank_debuff_mod) × picked
# 
# ============================================================================
