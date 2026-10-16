# ============================================================================
# ПАССИВНЫЕ СПОСОБНОСТИ АРЧИ
# ----------------------------------------------------------------------------
# Здесь собрана вся логика пассивок Арчи, чтобы точки вызова в бою были
# однострочными, а формулы жили в одном месте.
#
#   Удар! Удар! ур.1              — шанс крит-шанс/2 получить второй ход
#   Не медля! ур.1                — ходит всегда первым
#   Уворот! Контрудар! ур.1       — попеременно уворот и контратака
#   Вперёд! Вперёд! ур.1          — поддержка союзника: +10%+2*ур к боевым
#   Не считайте до десяти! ур.1   — подъём после падения с растущим шансом
#   Правильное дыхание ур.2       — 8%+ур*0.5 HP и MP каждый ход
#   Эй! Я здесь! ур.4             — каждый удар: шанс = крит-шанс +1 танк
#   Боевое зеркало ур.6           — шанс магия/2 отразить дебафф снарядом
#   Запаха достаточно! ур.8       — 30% от эффекта расходника союзника
#   Прости, но это мне! ур.10     — шанс = магия забрать половину баффа
#
#   Улучшения активок:
#   И ещё один! ур.2              — +1 удар к боксёрскому комбо
#   Быстрые комбинации ур.3       — 50% сложить печать, снимающую штраф
#   Твёрдые мускулы ур.4          — шанс = магия на второй щит
#   Движение жизнь! ур.5          — рывок сбрасывает случайный дебафф
#   Далеко и надолго! ур.6        — удар орла и ураган выкидывают на 1 ход дольше
#   Нежное перенаправление силы ур.7 — мягкая ладонь даёт союзнику 40% магии
#   Новые каналы энергии ур.8     — очищение Ци и реверс меняют на 1 больше
#   Быстрое восстановление ур.9   — режим храбрости 3 сек, заряды каждые 9 сек
#   Ради других! ур.10            — храбрость длится 5 ходов
# ============================================================================

# --- Состояние боя (сбрасывается в fightbegin12) -----------------------------
default archie_dodge_next = True
default archie_extra_turns_used = 0
default archie_revive_rounds = 0
default archie_muscle_shield = 0
default archie_courage_turns = 0
default archie_courage_charges = 0
default archie_soft_palm_bonus = 0.0
# Сроки жизни эффектов активок Арчи (убывают в конце раунда).
default archie_trauma_turns = 0
default archie_return_turns = 0
default archie_chakra_turns = 0
# «Не медля!» ур.1: Арчи уже сходил первым в этом бою.
default archie_first_done = False

# --- Состояние вне слотов сохранения (persistent) ----------------------------
default persistent.archie_revive_streak = 0

init python:
    # ========================================================================
    # КОНСТАНТЫ ПАССИВОК
    # ========================================================================

    # «Удар! Удар!» ур.1: шанс второго хода = крит-шанс/2.
    ARCHIE_DOUBLE_LEVEL = 1
    ARCHIE_DOUBLE_RATIO = 0.5

    # «Не медля!» ур.1: ходит всегда первым.
    ARCHIE_FIRST_LEVEL = 1

    # «Уворот! Контрудар!» ур.1: шанс = крит-шанс.
    ARCHIE_COUNTER_LEVEL = 1
    ARCHIE_COUNTER_DAMAGE = 0.5

    # «Вперёд! Вперёд!» ур.1: +10% + 2*ур ко всем боевым характеристикам.
    ARCHIE_SUPPORT_LEVEL = 1
    ARCHIE_SUPPORT_BASE = 0.10
    ARCHIE_SUPPORT_PER_LEVEL = 0.02
    ARCHIE_SUPPORT_COMFORT = 1

    # «Не считайте до десяти!» ур.1: подъём с растущим шансом.
    ARCHIE_REVIVE_LEVEL = 1
    ARCHIE_REVIVE_CHANCES = (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
    ARCHIE_REVIVE_HP = 0.10

    # «Правильное дыхание» ур.2: 8% + ур*0.5 HP и MP каждый ход.
    ARCHIE_BREATHING_LEVEL = 2
    ARCHIE_BREATHING_BASE = 0.08
    ARCHIE_BREATHING_PER_LEVEL = 0.005

    # «Эй! Я здесь!» ур.4: шанс = крит-шанс увеличить танк на 1.
    ARCHIE_HERE_LEVEL = 4
    ARCHIE_HERE_TANK = 1

    # «Боевое зеркало» ур.6: шанс = магия/2 отразить дебафф снарядом.
    ARCHIE_MIRROR_LEVEL = 6
    ARCHIE_MIRROR_RATIO = 0.5

    # «Запаха достаточно!» ур.8: 30% от эффекта расходника союзника.
    ARCHIE_SMELL_LEVEL = 8
    ARCHIE_SMELL_RATIO = 0.30

    # «Прости, но это мне!» ур.10: шанс = магия забрать половину баффа.
    ARCHIE_MINE_LEVEL = 10
    ARCHIE_MINE_RATIO = 0.5

    # --- Улучшения активок -------------------------------------------------
    ARCHIE_ONE_MORE_LEVEL = 2           # «И ещё один!»
    ARCHIE_COMBO_LEVEL = 3              # «Быстрые комбинации»
    ARCHIE_COMBO_CHANCE = 0.50
    ARCHIE_COMBO_CLEANSE = 0.10         # 10% + магия/2 штрафа

    ARCHIE_MUSCLES_LEVEL = 4            # «Твёрдые мускулы»
    ARCHIE_DASH_LEVEL = 5               # «Движение жизнь!»
    ARCHIE_EAGLE_LEVEL = 6              # «Далеко и надолго!»
    ARCHIE_EAGLE_EXTRA = 1

    ARCHIE_SOFT_PALM_LEVEL = 7          # «Нежное перенаправление силы»
    ARCHIE_SOFT_PALM_RATIO = 0.40

    ARCHIE_CHANNELS_LEVEL = 8           # «Новые каналы энергии»
    ARCHIE_CHANNELS_EXTRA = 1

    ARCHIE_FAST_RECOVERY_LEVEL = 9      # «Быстрое восстановление»
    ARCHIE_COURAGE_SECONDS = 5
    ARCHIE_COURAGE_SECONDS_FAST = 3
    ARCHIE_COURAGE_RECHARGE = 9

    ARCHIE_FOR_OTHERS_LEVEL = 10        # «Ради других!»
    ARCHIE_COURAGE_TURNS = 5

    # ========================================================================
    # ОБЩИЕ ХЕЛПЕРЫ
    # ========================================================================

    def archie_char():
        """Объект Арчи из команды, либо None."""
        return (getattr(store, "pers_dict", {}) or {}).get("Арчи")

    def archie_level():
        """Уровень Арчи (для проверки открытия способностей)."""
        char = archie_char()
        return max(1, int(getattr(char, "level", 1) or 1)) if char else 1

    def archie_is_char(char):
        return char is not None and getattr(char, "name", None) == "Арчи"

    def archie_reset_battle_passives():
        """Сброс боевых пассивок Арчи в начале боя (fightbegin12)."""
        store.archie_dodge_next = True
        store.archie_extra_turns_used = 0
        store.archie_revive_rounds = 0
        store.archie_muscle_shield = 0
        store.archie_courage_turns = 0
        store.archie_courage_charges = 0
        store.archie_soft_palm_bonus = 0.0
        store.archie_trauma_turns = 0
        store.archie_return_turns = 0
        store.archie_chakra_turns = 0
        store.archie_first_done = False
        enemy = (getattr(store, "enemies", {}) or {}).get("Арчи")
        if enemy is not None:
            init_archie_battle_state(enemy)
        return True

    # ========================================================================
    # НЕ МЕДЛЯ! (ходит всегда первым)
    # ========================================================================

    def archie_first_turn_available():
        """«Не медля!» ур.1: нельзя выбрать других, пока не сходил Арчи."""
        char = archie_char()
        if char is None or archie_level() < ARCHIE_FIRST_LEVEL:
            return False
        if getattr(char, "picked", 0) != 1:
            return False
        if getattr(char, "current_hp", 0) <= 0:
            return False
        # Первый ход ещё не сделан — Арчи должен сходить.
        return int(getattr(char, "turn", 0)) == 1 and not bool(getattr(store, "archie_first_done", False))

    def archie_blocks_other_picks(char_name):
        """Можно ли выбрать этого персонажа, пока Арчи не сходил."""
        if not archie_first_turn_available():
            return False
        return char_name != "Арчи"

    def archie_mark_first_done():
        store.archie_first_done = True
        return True

    # ========================================================================
    # УДАР! УДАР! (шанс второго хода)
    # ========================================================================

    def archie_double_turn_chance():
        """Шанс второго хода = крит-шанс Арчи / 2."""
        char = archie_char()
        if char is None or archie_level() < ARCHIE_DOUBLE_LEVEL:
            return 0.0
        return max(0.0, min(1.0, float(getattr(char, "critrate", 0)) * ARCHIE_DOUBLE_RATIO))

    def archie_max_extra_turns():
        """Максимум дополнительных ходов = ур/2."""
        return max(0, archie_level() // 2)

    def archie_try_extra_turn():
        """Возвращает True, если Арчи получил дополнительный ход."""
        char = archie_char()
        if char is None or archie_level() < ARCHIE_DOUBLE_LEVEL:
            return False
        if int(getattr(store, "archie_extra_turns_used", 0) or 0) >= archie_max_extra_turns():
            return False
        chance = archie_double_turn_chance()
        if renpy.random.random() >= chance:
            return False
        store.archie_extra_turns_used = int(getattr(store, "archie_extra_turns_used", 0) or 0) + 1
        char.turn = 1
        renpy.log("[Арчи][Удар! Удар!] дополнительный ход (шанс {:.1%})".format(chance))
        return True

    # ========================================================================
    # УВОРОТ! КОНТРУДАР! (попеременно)
    # ========================================================================

    def archie_counter_chance():
        """Шанс уворота/контратаки = крит-шанс Арчи."""
        char = archie_char()
        if char is None or archie_level() < ARCHIE_COUNTER_LEVEL:
            return 0.0
        return max(0.0, min(1.0, float(getattr(char, "critrate", 0))))

    def archie_on_damage_received(target=None, attacker=None, **kwargs):
        """Попеременно уворот и контратака при получении урона."""
        if not archie_is_char(target):
            return None
        if archie_level() < ARCHIE_COUNTER_LEVEL:
            return None
        if renpy.random.random() >= archie_counter_chance():
            return None

        if bool(getattr(store, "archie_dodge_next", True)):
            # Уворот: урон не проходит.
            store.archie_dodge_next = False
            renpy.log("[Арчи][Уворот!] атака уклонена")
            return "dodge"

        # Контрудар: отвечает уроном.
        store.archie_dodge_next = True
        char = archie_char()
        if char is not None and attacker is not None and getattr(attacker, "current_hp", 0) > 0:
            dmg = max(1, int(float(getattr(char, "atk", 0)) * ARCHIE_COUNTER_DAMAGE))
            attacker.current_hp = max(0, getattr(attacker, "current_hp", 0) - dmg)
            add_attack_result("Арчи", attacker.name, dmg, False, "normal")
        renpy.log("[Арчи][Контрудар!] ответная атака")
        return "counter"

    # ========================================================================
    # ВПЕРЁД! ВПЕРЁД! (поддержка союзника)
    # ========================================================================

    def archie_support_bonus():
        """Бонус поддержки: 10% + 2*ур ко всем боевым характеристикам."""
        if archie_level() < ARCHIE_SUPPORT_LEVEL:
            return 0.0
        return ARCHIE_SUPPORT_BASE + ARCHIE_SUPPORT_PER_LEVEL * archie_level()

    def archie_support_ally(ally):
        """При поддержке союзника даёт ему бонус ко всем боевым статам."""
        if ally is None or archie_level() < ARCHIE_SUPPORT_LEVEL:
            return False
        if archie_is_char(ally):
            return False
        bonus = archie_support_bonus()
        ally.bonus_atk = float(getattr(ally, "bonus_atk", 1.0) or 1.0) + bonus
        ally.bonus_def = float(getattr(ally, "bonus_def", 1.0) or 1.0) + bonus
        ally.bonus_magic = float(getattr(ally, "bonus_magic", 1.0) or 1.0) + bonus
        ally.bonus_dmgchance = float(getattr(ally, "bonus_dmgchance", 0)) + bonus
        ally.bonus_critrate = float(getattr(ally, "bonus_critrate", 0)) + bonus
        ally.bonus_comfort = float(getattr(ally, "bonus_comfort", 0)) + ARCHIE_SUPPORT_COMFORT
        renpy.log("[Арчи][Вперёд! Вперёд!] {}: +{:.0%} к боевым статам".format(
            getattr(ally, "name", "?"), bonus))
        return True

    # ========================================================================
    # НЕ СЧИТАЙТЕ ДО ДЕСЯТИ! (подъём после падения)
    # ========================================================================

    def archie_revive_chance():
        """Шанс подняться растёт с каждым раундом: 10%..100%."""
        rounds = int(getattr(store, "archie_revive_rounds", 0) or 0)
        index = max(0, min(len(ARCHIE_REVIVE_CHANCES) - 1, rounds))
        return ARCHIE_REVIVE_CHANCES[index]

    def archie_try_revive():
        """Поднимает Арчи, если он упал. Шанс растёт по раундам."""
        char = archie_char()
        if char is None or archie_level() < ARCHIE_REVIVE_LEVEL:
            return False
        if int(getattr(char, "current_hp", 0)) > 0:
            return False

        chance = archie_revive_chance()
        store.archie_revive_rounds = int(getattr(store, "archie_revive_rounds", 0) or 0) + 1
        if renpy.random.random() >= chance:
            return False

        heal = max(1, int(float(getattr(char, "max_hp", 0)) * ARCHIE_REVIVE_HP))
        char.current_hp = heal
        char.turn = 1
        store.archie_revive_rounds = 0
        if "clear_swoon_pending_for_visual" in globals():
            store.clear_swoon_pending_for_visual(char)
        renpy.log("[Арчи][Не считайте до десяти] поднялся с {} HP (шанс {:.0%})".format(heal, chance))
        return True

    # ========================================================================
    # ПРАВИЛЬНОЕ ДЫХАНИЕ (регенерация HP и MP)
    # ========================================================================

    def archie_on_round_end():
        """Арчи каждый ход регенерирует 8%+ур*0.5 HP и MP."""
        char = archie_char()
        if char is None or archie_level() < ARCHIE_BREATHING_LEVEL:
            return False
        if int(getattr(char, "current_hp", 0)) <= 0:
            return False
        ratio = ARCHIE_BREATHING_BASE + ARCHIE_BREATHING_PER_LEVEL * archie_level()
        hp_gain = max(1, int(float(getattr(char, "max_hp", 0)) * ratio))
        mp_gain = max(1, int(float(getattr(char, "max_mp", 0)) * ratio))
        char.current_hp = min(int(getattr(char, "max_hp", 0)), int(getattr(char, "current_hp", 0)) + hp_gain)
        char.current_mp = min(int(getattr(char, "max_mp", 0)), int(getattr(char, "current_mp", 0)) + mp_gain)
        # Попытка подняться, если Арчи упал.
        store.archie_try_revive()
        return True

    # ========================================================================
    # ЭЙ! Я ЗДЕСЬ! (танк за удары)
    # ========================================================================

    def archie_on_hit_landed():
        """Каждый удар: шанс = крит-шанс увеличить свой танк на 1."""
        if archie_level() < ARCHIE_HERE_LEVEL:
            return False
        char = archie_char()
        if char is None:
            return False
        if renpy.random.random() >= float(getattr(char, "critrate", 0)):
            return False
        char.bonus_tank = float(getattr(char, "bonus_tank", 0)) + ARCHIE_HERE_TANK
        renpy.log("[Арчи][Эй! Я здесь!] танк +{}".format(ARCHIE_HERE_TANK))
        return True

    # ========================================================================
    # БОЕВОЕ ЗЕРКАЛО (отражение дебаффов)
    # ========================================================================

    def archie_on_debuff_received(target=None, attacker=None, debuff=None, **kwargs):
        """Шанс = магия/2 отразить в противника наложенный снарядом дебафф."""
        if not archie_is_char(target):
            return False
        if archie_level() < ARCHIE_MIRROR_LEVEL:
            return False
        char = archie_char()
        if char is None or attacker is None:
            return False
        chance = min(1.0, float(getattr(char, "magic", 0)) * ARCHIE_MIRROR_RATIO / 100.0)
        if renpy.random.random() >= chance:
            return False
        # Отражаем: снимаем с Арчи и накладываем на противника.
        if debuff:
            field, value = debuff
            setattr(char, field, int(getattr(char, field, 0) or 0) - int(value))
            setattr(attacker, field, int(getattr(attacker, field, 0) or 0) + int(value))
        renpy.log("[Арчи][Боевое зеркало] дебафф отражён в {}".format(getattr(attacker, "name", "?")))
        return True

    # ========================================================================
    # ЗАПАХА ДОСТАТОЧНО! (30% от эффекта расходника союзника)
    # ========================================================================

    def archie_on_consumable_used(user, item_id, effects=None):
        """Шанс = магия получить 30% от эффекта расходника союзника.

        Аппетит Арчи при этом не заполняется.
        """
        if archie_level() < ARCHIE_SMELL_LEVEL:
            return False
        char = archie_char()
        if char is None or getattr(char, "picked", 0) != 1:
            return False
        if archie_is_char(user):
            return False
        chance = min(1.0, float(getattr(char, "magic", 0)) / 100.0)
        if renpy.random.random() >= chance:
            return False

        effects = effects or {}
        hp_heal = int(effects.get("hp_heal", 0) * ARCHIE_SMELL_RATIO)
        mp_heal = int(effects.get("mp_heal", 0) * ARCHIE_SMELL_RATIO)
        if hp_heal:
            char.current_hp = min(int(getattr(char, "max_hp", 0)), int(getattr(char, "current_hp", 0)) + hp_heal)
        if mp_heal:
            char.current_mp = min(int(getattr(char, "max_mp", 0)), int(getattr(char, "current_mp", 0)) + mp_heal)
        # Аппетит НЕ заполняется — push_feedness_item намеренно не вызывается.
        renpy.log("[Арчи][Запаха достаточно] +{} HP, +{} MP".format(hp_heal, mp_heal))
        return True

    # ========================================================================
    # ПРОСТИ, НО ЭТО МНЕ! (забрать половину баффа)
    # ========================================================================

    def archie_on_buff_gained(holder, buff_field, amount):
        """Шанс = магия забрать половину баффа или бонусной характеристики."""
        if archie_level() < ARCHIE_MINE_LEVEL:
            return False
        char = archie_char()
        if char is None or holder is None:
            return False
        if archie_is_char(holder):
            return False
        if getattr(char, "picked", 0) != 1:
            return False
        chance = min(1.0, float(getattr(char, "magic", 0)) / 100.0)
        if renpy.random.random() >= chance:
            return False

        taken = float(amount) * ARCHIE_MINE_RATIO
        holder_value = float(getattr(holder, buff_field, 0) or 0)
        setattr(holder, buff_field, holder_value - taken)
        char_value = float(getattr(char, buff_field, 0) or 0)
        setattr(char, buff_field, char_value + taken)
        renpy.log("[Арчи][Прости, но это мне] забрал {:.2f} {}".format(taken, buff_field))
        return True

    # ========================================================================
    # УЛУЧШЕНИЯ АКТИВОК
    # ========================================================================

    def archie_combo_hits():
        """«И ещё один!» ур.2: к боксёрскому комбо добавляется ещё один удар."""
        base = 4
        if archie_level() >= ARCHIE_ONE_MORE_LEVEL:
            base += 1
        return base

    def archie_try_combo_seal():
        """«Быстрые комбинации» ур.3: 50% сложить печать, снимающую штраф."""
        if archie_level() < ARCHIE_COMBO_LEVEL:
            return False
        if renpy.random.random() >= ARCHIE_COMBO_CHANCE:
            return False
        char = archie_char()
        if char is None:
            return False
        # 10% + магия/2 штрафа к бонусной характеристике.
        clean = ARCHIE_COMBO_CLEANSE + float(getattr(char, "magic", 0)) / 200.0
        for field in ("atk_debuff", "def_debuff", "magic_debuff",
                      "accuracy_debuff", "critrate_debuff", "critdmg_debuff"):
            value = int(getattr(char, field, 0) or 0)
            if value > 0:
                setattr(char, field, max(0, value - int(round(clean * 10))))
                break
        renpy.log("[Арчи][Быстрые комбинации] печать сложена, штраф снят")
        return True

    def archie_try_muscle_shield():
        """«Твёрдые мускулы» ур.4: шанс = магия наложить второй щит."""
        if archie_level() < ARCHIE_MUSCLES_LEVEL:
            return False
        char = archie_char()
        if char is None:
            return False
        chance = min(1.0, float(getattr(char, "magic", 0)) / 100.0)
        if renpy.random.random() >= chance:
            return False
        char.shield = int(getattr(char, "shield", 0) or 0) + 1
        store.archie_muscle_shield = int(getattr(store, "archie_muscle_shield", 0) or 0) + 1
        renpy.log("[Арчи][Твёрдые мускулы] второй щит")
        return True

    def archie_on_dash():
        """«Движение жизнь!» ур.5: рывок сбрасывает случайный дебафф."""
        if archie_level() < ARCHIE_DASH_LEVEL:
            return False
        char = archie_char()
        if char is None:
            return False
        chance = min(1.0, float(getattr(char, "magic", 0)) / 100.0)
        if renpy.random.random() >= chance:
            return False
        active = [f for f in ("atk_debuff", "def_debuff", "magic_debuff",
                              "accuracy_debuff", "critrate_debuff", "critdmg_debuff")
                  if int(getattr(char, f, 0) or 0) != 0]
        if not active:
            return False
        field = renpy.random.choice(active)
        setattr(char, field, 0)
        renpy.log("[Арчи][Движение жизнь] сброшен дебафф {}".format(field))
        return True

    def archie_eagle_extra_turn():
        """«Далеко и надолго!» ур.6: удар орла и ураган выкидывают на 1 ход дольше."""
        if archie_level() < ARCHIE_EAGLE_LEVEL:
            return 0
        return ARCHIE_EAGLE_EXTRA

    def archie_on_soft_palm():
        """«Нежное перенаправление силы» ур.7: мягкая ладонь даёт союзнику
        40% магии Арчи."""
        if archie_level() < ARCHIE_SOFT_PALM_LEVEL:
            return False
        char = archie_char()
        if char is None:
            return False
        allies = [c for c in (getattr(store, "pers_dict", {}) or {}).values()
                  if c is not None and not archie_is_char(c)
                  and getattr(c, "picked", 0) == 1 and getattr(c, "current_hp", 0) > 0]
        if not allies:
            return False
        ally = renpy.random.choice(allies)
        bonus = float(getattr(char, "magic", 0)) * ARCHIE_SOFT_PALM_RATIO / 100.0
        ally.bonus_magic = float(getattr(ally, "bonus_magic", 1.0) or 1.0) + bonus
        store.archie_soft_palm_bonus = bonus
        renpy.log("[Арчи][Нежное перенаправление] {}: магия +{:.1%}".format(
            getattr(ally, "name", "?"), bonus))
        return True

    def archie_channels_extra():
        """«Новые каналы энергии» ур.8: очищение Ци и реверс меняют на 1 больше."""
        if archie_level() < ARCHIE_CHANNELS_LEVEL:
            return 0
        return ARCHIE_CHANNELS_EXTRA

    def archie_courage_seconds():
        """«Быстрое восстановление» ур.9: режим храбрости длится 3 сек, а не 5."""
        if archie_level() >= ARCHIE_FAST_RECOVERY_LEVEL:
            return ARCHIE_COURAGE_SECONDS_FAST
        return ARCHIE_COURAGE_SECONDS

    def archie_courage_turn_count():
        """«Ради других!» ур.10: количество ходов храбрости увеличивается до 5."""
        if archie_level() >= ARCHIE_FOR_OTHERS_LEVEL:
            return ARCHIE_COURAGE_TURNS
        return 3

    def archie_courage_charges():
        """Доступные заряды храбрости: 3 / 4 на ур.6 / 5 на ур.8."""
        level = archie_level()
        if level >= 8:
            return 5
        if level >= 6:
            return 4
        return 3

    def archie_start_courage():
        """«Храбрость!» ур.9: весь урон получает Арчи вместо союзников."""
        char = archie_char()
        if char is None:
            return False
        store.archie_courage_turns = archie_courage_turn_count()
        store.archie_courage_charges = archie_courage_charges()
        char.courage_active = True
        renpy.log("[Арчи][Храбрость] активна {} ходов".format(store.archie_courage_turns))
        return True

    def archie_tick_courage():
        turns = int(getattr(store, "archie_courage_turns", 0) or 0)
        if turns <= 0:
            return False
        turns -= 1
        store.archie_courage_turns = turns
        char = archie_char()
        if turns <= 0 and char is not None:
            char.courage_active = False
        return True

    def archie_redirect_damage_to_self(target):
        """Если активна храбрость, урон получает Арчи вместо цели."""
        if int(getattr(store, "archie_courage_turns", 0) or 0) <= 0:
            return False
        char = archie_char()
        if char is None or archie_is_char(target):
            return False
        if int(getattr(char, "current_hp", 0)) <= 0:
            return False
        return True

    # ========================================================================
    # ТРАВМИРУЮЩИЕ УДАРЫ И ВЕРНУТЬ ОТПРАВИТЕЛЮ (сроки жизни)
    # ========================================================================

    def archie_tick_trauma():
        """«Травмирующие удары» ур.6: отсчёт ходов замедления."""
        turns = int(getattr(store, "archie_trauma_turns", 0) or 0)
        if turns <= 0:
            return False
        store.archie_trauma_turns = turns - 1
        return True

    def archie_trauma_active():
        return int(getattr(store, "archie_trauma_turns", 0) or 0) > 0

    def archie_apply_trauma_slow(target):
        """Каждый удар Арчи замедляет атаку противника на 3%."""
        if not archie_trauma_active() or target is None:
            return False
        target.bonus_atk = float(getattr(target, "bonus_atk", 1.0) or 1.0) - 0.03
        return True

    def archie_tick_return():
        """«Вернуть отправителю» ур.7: отсчёт ходов отражения снарядов."""
        turns = int(getattr(store, "archie_return_turns", 0) or 0)
        if turns <= 0:
            return False
        store.archie_return_turns = turns - 1
        return True

    def archie_return_active():
        """Активно ли отражение снарядов (Арчи не получает урона)."""
        return int(getattr(store, "archie_return_turns", 0) or 0) > 0

    def archie_tick_chakra():
        """«Ладони чакры»: отсчёт длительности эффекта."""
        turns = int(getattr(store, "archie_chakra_turns", 0) or 0)
        if turns <= 0:
            return False
        store.archie_chakra_turns = turns - 1
        return True

    def archie_tick_all():
        """Единый тик эффектов Арчи в конце раунда."""
        store.archie_tick_trauma()
        store.archie_tick_return()
        store.archie_tick_chakra()
        return True
