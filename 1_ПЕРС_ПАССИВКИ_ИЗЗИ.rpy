# ============================================================================
# ПАССИВНЫЕ СПОСОБНОСТИ ИЗЗИ
# ----------------------------------------------------------------------------
# Здесь собрана вся логика пассивок Иззи, чтобы точки вызова в бою были
# однострочными, а формулы жили в одном месте.
#
#   Равновесие ур.1              — 45% шанс не отнять HP при магии
#   Посвященная ур.1             — всегда на уровень выше команды
#   Я тоже... ур.1               — магия не может убить Иззи (остаётся 1 HP)
#   Таинство вместо мечей ур.1   — не может атаковать, но есть базовые заклинания
#   Адаптация к диете ур.1       — 2% HP и MP за каждое пустое место аппетита
#   Подозрительная проницательность ур.1 — осмотр открывает 4 эффекта, +1 соц.
#   Подавление инородной ауры ур.3 — магия по врагу снижает его магию на 8%
#   Успокоение близкого ур.5     — +4% к шансу, что Крис повинуется
#   Случайное провиденье ур.7    — шанс = крит-шанс получить просвещение x2
#   Магия сверху ур.9            — 20% от магии применить заклинание дважды
#
#   Улучшения активок:
#   Открытие чакр ур.2           — Медитация даёт 2 стака просвещения
#   Потоки чакр ур.3             — Медитация: 40% восстановить вдвое больше маны
#   Правильное дыхание ур.4      — Успокоение союзника даёт +10% точности
#   Аккуратное деление ур.5      — 30% не потерять HP при «Осколке себя»
#   Любовь вселенной ур.6        — карма на себе превращает часть урона в урон врагу
#   Целебное благовоние ур.7     — при КД «благовония» дыхание лечит Иззи на 20%
#   Духовный диалог ур.8         — Зачарование: 50% вернуть 10% MP и +10% магии
#   Мы отзвуки прошлого нас ур.9 — в начале боя +25% крит-шанс и +30% крит-урон,
#                                  но при крите осколка равновесие теряется
# ============================================================================

# --- Состояние боя (сбрасывается в fightbegin12) -----------------------------
default izzy_equilibrium_broken = False
default izzy_fear_state = False
default izzy_enlightenment_stacks = 0
default izzy_meditation_count = 0
default izzy_double_magic_pending = False
default izzy_double_magic_target = None
default izzy_karma_target = None
default izzy_karma_turns = 0
default izzy_diet_bonus_pending = 0
# Флаги начисленных бонусов (идемпотентность) и улучшений.
default izzy_insight_applied = False
default izzy_echo_applied = False
default izzy_presence_doubled = False

init python:
    # ========================================================================
    # КОНСТАНТЫ ПАССИВОК
    # ========================================================================

    # «Равновесие» ур.1: шанс не отнять HP при применении магии.
    IZZY_EQUILIBRIUM_LEVEL = 1
    IZZY_EQUILIBRIUM_CHANCE = 0.45

    # «Посвященная» ур.1: всегда на уровень выше команды.
    IZZY_INITIATE_LEVEL = 1

    # «Я тоже...» ур.1: магия не может убить Иззи.
    IZZY_TOO_LEVEL = 1
    IZZY_MIN_HP = 1

    # «Адаптация к диете» ур.1: 2% HP и MP за пустое место аппетита.
    IZZY_DIET_LEVEL = 1
    IZZY_DIET_PER_SLOT = 0.02

    # «Подозрительная проницательность» ур.1.
    IZZY_INSIGHT_LEVEL = 1
    IZZY_INSIGHT_EFFECTS = 4
    IZZY_INSIGHT_SOCIAL = 1

    # «Подавление инородной ауры» ур.3: −8% магии врага за применение.
    IZZY_SUPPRESSION_LEVEL = 3
    IZZY_SUPPRESSION_AMOUNT = 0.08

    # «Успокоение близкого» ур.5: +4% к шансу подчинения Криса.
    IZZY_CALM_KRIS_LEVEL = 5
    IZZY_CALM_KRIS_CHANCE = 0.04

    # «Случайное провиденье» ур.7: шанс = крит-шанс получить просвещение x2.
    IZZY_PROVIDENCE_LEVEL = 7
    IZZY_PROVIDENCE_STACKS = 2

    # «Магия сверху» ур.9: 20% от текущей магии применить заклинание дважды.
    IZZY_DOUBLE_LEVEL = 9
    IZZY_DOUBLE_RATIO = 0.20

    # --- Улучшения активок -------------------------------------------------
    IZZY_CHAKRA_OPEN_LEVEL = 2          # «Открытие чакр»
    IZZY_CHAKRA_OPEN_STACKS = 2

    IZZY_CHAKRA_FLOW_LEVEL = 3          # «Потоки чакр»
    IZZY_CHAKRA_FLOW_CHANCE = 0.40

    IZZY_BREATHING_LEVEL = 4            # «Правильное дыхание» (улучшение)
    IZZY_BREATHING_ACCURACY = 0.10

    IZZY_CARE_DIVISION_LEVEL = 5        # «Аккуратное деление»
    IZZY_CARE_DIVISION_CHANCE = 0.30

    IZZY_UNIVERSE_LOVE_LEVEL = 6        # «Любовь вселенной»
    IZZY_UNIVERSE_LOVE_RATIO = 0.50

    IZZY_HEALING_INCENSE_LEVEL = 7      # «Целебное благовоние»
    IZZY_HEALING_INCENSE_HEAL = 0.20

    IZZY_SPIRIT_DIALOGUE_LEVEL = 8      # «Духовный диалог»
    IZZY_SPIRIT_DIALOGUE_CHANCE = 0.50
    IZZY_SPIRIT_DIALOGUE_MP = 0.10
    IZZY_SPIRIT_DIALOGUE_MAGIC = 0.10

    IZZY_ECHO_LEVEL = 9                 # «Мы отзвуки прошлого нас»
    IZZY_ECHO_CRITRATE = 0.25
    IZZY_ECHO_CRITDMG = 0.30
    IZZY_ECHO_BACKLASH = 1.5

    # ========================================================================
    # ОБЩИЕ ХЕЛПЕРЫ
    # ========================================================================

    def izzy_char():
        """Объект Иззи из команды, либо None."""
        return (getattr(store, "pers_dict", {}) or {}).get("Иззи")

    def izzy_level():
        """Уровень Иззи (для проверки открытия способностей)."""
        char = izzy_char()
        return max(1, int(getattr(char, "level", 1) or 1)) if char else 1

    def izzy_is_char(char):
        return char is not None and getattr(char, "name", None) == "Иззи"

    def izzy_reset_battle_passives():
        """Сброс боевых пассивок Иззи в начале боя (fightbegin12)."""
        store.izzy_equilibrium_broken = False
        store.izzy_fear_state = False
        store.izzy_enlightenment_stacks = 0
        store.izzy_meditation_count = 0
        store.izzy_double_magic_pending = False
        store.izzy_double_magic_target = None
        store.izzy_karma_target = None
        store.izzy_karma_turns = 0
        store.izzy_diet_bonus_pending = 0
        store.izzy_apply_echo_bonuses()
        return True

    # ========================================================================
    # РАВНОВЕСИЕ (шанс не отнять HP при магии)
    # ========================================================================

    def izzy_spell_hp_cost(percent):
        """Стоимость магии в HP с проверкой «Равновесия».

        «Равновесие» ур.1: 45% шанс не отнять HP.
        «Аккуратное деление» ур.5: 30% не потерять HP при «Осколке себя»
        (учитывается вызывающим кодом через extra_chance).
        «Я тоже...» ур.1: магия не может убить Иззи — остаётся 1 HP.
        """
        char = izzy_char()
        if char is None:
            return 0

        if izzy_level() >= IZZY_EQUILIBRIUM_LEVEL and renpy.random.random() < IZZY_EQUILIBRIUM_CHANCE:
            renpy.log("[Иззи][Равновесие] HP не отнято")
            return 0

        cost = int(getattr(char, "max_hp", 0) * float(percent))
        if cost <= 0:
            return 0
        # «Я тоже...»: заклинание не может убить Иззи.
        new_hp = int(getattr(char, "current_hp", 0)) - cost
        if izzy_level() >= IZZY_TOO_LEVEL:
            char.current_hp = max(IZZY_MIN_HP, new_hp)
        else:
            char.current_hp = max(0, new_hp)
        return cost

    def izzy_shard_hp_cost(percent):
        """«Осколок себя»: обычная стоимость плюс шанс «Аккуратного деления»."""
        if izzy_level() >= IZZY_CARE_DIVISION_LEVEL and renpy.random.random() < IZZY_CARE_DIVISION_CHANCE:
            renpy.log("[Иззи][Аккуратное деление] HP не потеряно")
            return 0
        return izzy_spell_hp_cost(percent)

    # ========================================================================
    # ПОСВЯЩЕННАЯ (уровень выше команды)
    # ========================================================================

    def izzy_initiate_level_bonus():
        """«Посвященная» ур.1: максимальный уровень на 1 больше команды."""
        if izzy_level() < IZZY_INITIATE_LEVEL:
            return 0
        global_level = max(1, int(getattr(getattr(store, "Pers", None), "global_level", 1) or 1))
        return max(0, (izzy_level() - global_level))

    # ========================================================================
    # ТАИНСТВО ВМЕСТО МЕЧЕЙ (не может атаковать)
    # ========================================================================

    def izzy_can_attack():
        """«Таинство вместо мечей» ур.1: Иззи не может атаковать."""
        if izzy_level() >= IZZY_TOO_LEVEL:
            return False
        return True

    # ========================================================================
    # АДАПТАЦИЯ К ДИЕТЕ (2% HP и MP за пустое место аппетита)
    # ========================================================================

    def izzy_on_round_end():
        """Конец раунда: диета, провиденье, карма, страх."""
        char = izzy_char()
        if char is None:
            return

        # «Адаптация к диете» ур.1: 2% HP и MP за каждое пустое место очереди.
        if izzy_level() >= IZZY_DIET_LEVEL:
            max_feedness = max(0, int(getattr(char, "max_feedness", 0) or 0))
            queue = list(getattr(char, "feedness_queue", []) or [])
            empty_slots = max(0, max_feedness - len([q for q in queue if q is not None]))
            if empty_slots > 0:
                hp_gain = int(getattr(char, "max_hp", 0) * IZZY_DIET_PER_SLOT * empty_slots)
                mp_gain = int(getattr(char, "max_mp", 0) * IZZY_DIET_PER_SLOT * empty_slots)
                char.current_hp = min(int(getattr(char, "max_hp", 0)), int(getattr(char, "current_hp", 0)) + hp_gain)
                char.current_mp = min(int(getattr(char, "max_mp", 0)), int(getattr(char, "current_mp", 0)) + mp_gain)

        # «Случайное провиденье» ур.7: шанс = крит-шанс получить просвещение x2.
        if izzy_level() >= IZZY_PROVIDENCE_LEVEL:
            if renpy.random.random() < float(getattr(char, "critrate", 0)):
                store.izzy_enlightenment_stacks = int(
                    getattr(store, "izzy_enlightenment_stacks", 0) or 0) + IZZY_PROVIDENCE_STACKS
                renpy.log("[Иззи][Случайное провиденье] просвещение +{}".format(IZZY_PROVIDENCE_STACKS))

        # Карма: отсчёт длительности печати.
        store.izzy_tick_karma()

    # ========================================================================
    # ПОДОЗРИТЕЛЬНАЯ ПРОНИЦАТЕЛЬНОСТЬ (осмотр)
    # ========================================================================

    def izzy_insight_effects(available_effects):
        """Ур.1: при осмотре Иззи открывает эффект сразу 4 действий."""
        if izzy_level() < IZZY_INSIGHT_LEVEL:
            return list(available_effects or [])[:1]
        return list(available_effects or [])[:IZZY_INSIGHT_EFFECTS]

    def izzy_insight_social_bonus():
        """Ур.1: +1 к социальным характеристикам для действий с плюсом."""
        if izzy_level() < IZZY_INSIGHT_LEVEL:
            return 0
        return IZZY_INSIGHT_SOCIAL

    def izzy_apply_insight_bonus():
        """Начисляет соц. бонус проницательности (идемпотентно)."""
        if izzy_level() < IZZY_INSIGHT_LEVEL:
            return False
        char = izzy_char()
        if char is None:
            return False
        if bool(getattr(store, "izzy_insight_applied", False)):
            return False
        bonus = IZZY_INSIGHT_SOCIAL
        char.bonus_perception = float(getattr(char, "bonus_perception", 0)) + bonus
        char.bonus_rhetoric = float(getattr(char, "bonus_rhetoric", 0)) + bonus
        char.bonus_power = float(getattr(char, "bonus_power", 0)) + bonus
        char.bonus_charm = float(getattr(char, "bonus_charm", 0)) + bonus
        store.izzy_insight_applied = True
        return True

    # ========================================================================
    # ПОДАВЛЕНИЕ ИНОРОДНОЙ АУРЫ (−8% магии врага)
    # ========================================================================

    def izzy_on_magic_used(target=None):
        """Каждое применение магии Иззи по противнику снижает его магию на 8%."""
        char = izzy_char()
        if char is None:
            return

        if target is not None and izzy_level() >= IZZY_SUPPRESSION_LEVEL:
            if getattr(target, "current_hp", 0) > 0:
                target.bonus_magic = float(getattr(target, "bonus_magic", 0.0)) - IZZY_SUPPRESSION_AMOUNT
                renpy.log("[Иззи][Подавление ауры] {}: магия {:.2f}".format(
                    getattr(target, "name", "?"), target.bonus_magic))

        # «Магия сверху» ур.9: 20% от текущей магии применить заклинание дважды.
        if izzy_level() >= IZZY_DOUBLE_LEVEL:
            if renpy.random.random() < float(getattr(char, "magic", 0)) * IZZY_DOUBLE_RATIO / 100.0:
                store.izzy_double_magic_pending = True
                store.izzy_double_magic_target = target
                renpy.log("[Иззи][Магия сверху] заклинание применится дважды")

    def izzy_consume_double_magic():
        """Возвращает цель для повторного применения, если сработала «Магия сверху»."""
        if not bool(getattr(store, "izzy_double_magic_pending", False)):
            return None
        store.izzy_double_magic_pending = False
        target = getattr(store, "izzy_double_magic_target", None)
        store.izzy_double_magic_target = None
        return target

    # ========================================================================
    # УСПОКОЕНИЕ БЛИЗКОГО (+4% к подчинению Криса)
    # ========================================================================

    def izzy_calm_kris_bonus():
        """Ур.5: каждый ход даёт +4% к шансу, что Крис повинуется."""
        if izzy_level() < IZZY_CALM_KRIS_LEVEL:
            return 0.0
        return IZZY_CALM_KRIS_CHANCE

    def izzy_calm_kris_chance(base_chance=0.0):
        """Итоговый шанс подчинения Криса с учётом пассивки Иззи."""
        if izzy_char() is None or getattr(izzy_char(), "picked", 0) != 1:
            return base_chance
        return min(1.0, float(base_chance) + izzy_calm_kris_bonus())

    # ========================================================================
    # МЕДИТАЦИЯ (улучшения ур.2 и ур.3)
    # ========================================================================

    def izzy_meditation_bonus():
        """«Открытие чакр» ур.2: Медитация даёт 2 стака просвещения.

        Возвращает множитель восстановления маны:
        «Потоки чакр» ур.3 — 40% шанс восстановить вдвое больше маны.
        """
        if izzy_level() >= IZZY_CHAKRA_OPEN_LEVEL:
            store.izzy_enlightenment_stacks = int(
                getattr(store, "izzy_enlightenment_stacks", 0) or 0) + IZZY_CHAKRA_OPEN_STACKS
            renpy.log("[Иззи][Открытие чакр] просвещение +{}".format(IZZY_CHAKRA_OPEN_STACKS))

        store.izzy_meditation_count = int(getattr(store, "izzy_meditation_count", 0) or 0) + 1

        if izzy_level() >= IZZY_CHAKRA_FLOW_LEVEL and renpy.random.random() < IZZY_CHAKRA_FLOW_CHANCE:
            renpy.log("[Иззи][Потоки чакр] мана восстановлена вдвое")
            return 2.0
        return 1.0

    # ========================================================================
    # ПРАВИЛЬНОЕ ДЫХАНИЕ (улучшения ур.4 и ур.7)
    # ========================================================================

    def izzy_on_calm_ally(target):
        """«Правильное дыхание» ур.4: Успокоение союзника даёт +10% точности."""
        if izzy_level() < IZZY_BREATHING_LEVEL or target is None:
            return False
        target.bonus_dmgchance = float(getattr(target, "bonus_dmgchance", 0)) + IZZY_BREATHING_ACCURACY
        renpy.log("[Иззи][Правильное дыхание] {}: точность +10%".format(getattr(target, "name", "?")))
        return True

    def izzy_on_breathing_used(cooldown_is_active=False):
        """«Целебное благовоние» ур.7: если «благовоние» на КД, дыхание лечит Иззи.

        Возвращает True, если лечение применено.
        """
        if izzy_level() < IZZY_HEALING_INCENSE_LEVEL:
            return False
        if not cooldown_is_active:
            return False
        char = izzy_char()
        if char is None:
            return False
        heal = max(1, int(getattr(char, "max_hp", 0) * IZZY_HEALING_INCENSE_HEAL))
        char.current_hp = min(int(getattr(char, "max_hp", 0)), int(getattr(char, "current_hp", 0)) + heal)
        renpy.log("[Иззи][Целебное благовоние] восстановлено {} HP".format(heal))
        return True

    def izzy_incense_on_cooldown():
        """Проверяет, находится ли «Благовония» на перезарядке."""
        for ability in (getattr(store, "BATTLE_ABILITY_DEFINITIONS", []) or []):
            if ability.get("name") == "Благовония":
                return get_battle_ability_current_cd(ability) > 0
        return False

    # ========================================================================
    # ЛЮБОВЬ ВСЕЛЕННОЙ (карма на себе)
    # ========================================================================

    def izzy_set_karma(target, turns=2):
        """«Карма» ур.5: накладывает печать кармы."""
        if target is None:
            return False
        store.izzy_karma_target = getattr(target, "name", None) or str(target)
        store.izzy_karma_turns = max(1, int(turns))
        target.karma_active = True
        return True

    def izzy_karma_is_self():
        """Наложена ли карма на саму Иззи."""
        char = izzy_char()
        if char is None:
            return False
        return getattr(store, "izzy_karma_target", None) == getattr(char, "name", None)

    def izzy_tick_karma():
        turns = int(getattr(store, "izzy_karma_turns", 0) or 0)
        if turns <= 0:
            return False
        turns -= 1
        store.izzy_karma_turns = turns
        if turns <= 0:
            name = getattr(store, "izzy_karma_target", None)
            store.izzy_karma_target = None
            holder = (getattr(store, "pers_dict", {}) or {}).get(name) or (getattr(store, "enemies", {}) or {}).get(name)
            if holder is not None:
                holder.karma_active = False
            return False
        return True

    def izzy_universe_love_reflect(damage, attacker=None):
        """«Любовь вселенной» ур.6: при карме на себе половина урона от
        «Осколка себя» превращается в дополнительный урон по противнику."""
        if izzy_level() < IZZY_UNIVERSE_LOVE_LEVEL:
            return 0
        if not izzy_karma_is_self():
            return 0
        bonus = int(float(damage) * IZZY_UNIVERSE_LOVE_RATIO)
        if bonus > 0 and attacker is not None and getattr(attacker, "current_hp", 0) > 0:
            attacker.current_hp = max(0, getattr(attacker, "current_hp", 0) - bonus)
            add_attack_result("Иззи", attacker.name, bonus, False, "magic")
            renpy.log("[Иззи][Любовь вселенной] отражено {} урона".format(bonus))
        return bonus

    # ========================================================================
    # ДУХОВНЫЙ ДИАЛОГ (зачарование союзника)
    # ========================================================================

    def izzy_on_enchant_ally(target):
        """Ур.8: 50% восстановить Иззи 10% MP и увеличить свою магию на 10%."""
        if izzy_level() < IZZY_SPIRIT_DIALOGUE_LEVEL or target is None:
            return False
        if renpy.random.random() >= IZZY_SPIRIT_DIALOGUE_CHANCE:
            return False
        char = izzy_char()
        if char is None:
            return False
        mp_gain = int(getattr(char, "max_mp", 0) * IZZY_SPIRIT_DIALOGUE_MP)
        char.current_mp = min(int(getattr(char, "max_mp", 0)), int(getattr(char, "current_mp", 0)) + mp_gain)
        char.bonus_magic = float(getattr(char, "bonus_magic", 0)) + IZZY_SPIRIT_DIALOGUE_MAGIC
        renpy.log("[Иззи][Духовный диалог] MP +{}, магия +10%".format(mp_gain))
        return True

    # ========================================================================
    # МЫ ОТЗВУКИ ПРОШЛОГО НАС (бонусы в начале боя, расплата за крит)
    # ========================================================================

    def izzy_apply_echo_bonuses():
        """Ур.9: в начале боя +25% крит-шанса и +30% крит-урона."""
        if izzy_level() < IZZY_ECHO_LEVEL:
            return False
        char = izzy_char()
        if char is None:
            return False
        char.bonus_critrate = float(getattr(char, "bonus_critrate", 0)) + IZZY_ECHO_CRITRATE
        char.bonus_crit = float(getattr(char, "bonus_crit", 0)) + IZZY_ECHO_CRITDMG
        store.izzy_echo_applied = True
        renpy.log("[Иззи][Отзвуки прошлого] крит-шанс +25%, крит-урон +30%")
        return True

    def izzy_on_shard_crit():
        """Ур.9: при крите духовного осколка равновесие теряется."""
        if izzy_level() < IZZY_ECHO_LEVEL:
            return False
        store.izzy_equilibrium_broken = True
        char = izzy_char()
        if char is not None:
            # Иззи получает в 1.5 раза больше урона.
            char.critdmg_debuff = int(getattr(char, "critdmg_debuff", 0) or 0) + 1
        renpy.log("[Иззи][Отзвуки прошлого] равновесие потеряно: урон x1.5")
        return True

    def izzy_equilibrium_damage_multiplier():
        """Множитель получаемого урона при потерянном равновесии."""
        if bool(getattr(store, "izzy_equilibrium_broken", False)):
            return IZZY_ECHO_BACKLASH
        return 1.0

    # ========================================================================
    # ПРОБУЖДЕНИЕ (страх перед миссией)
    # ========================================================================

    def izzy_enter_fear():
        """«Пробуждение»: после атаки Иззи впадает в страх перед миссией."""
        store.izzy_fear_state = True
        store.izzy_meditation_count = 0
        renpy.log("[Иззи][Пробуждение] страх: доступны только медитация и успокоение")
        return True

    def izzy_in_fear():
        return bool(getattr(store, "izzy_fear_state", False))

    def izzy_can_use_spell(ability_name):
        """В состоянии страха доступны только Медитация и Успокоение."""
        if not izzy_in_fear():
            return True
        if ability_name in ("Медитация", "Успокоение"):
            return True
        # Другие заклинания — только после 2 медитаций/успокоений.
        return int(getattr(store, "izzy_meditation_count", 0) or 0) >= 2

    def izzy_try_clear_fear(action_name):
        """Медитация и Успокоение снимают страх с шансом 50%."""
        if not izzy_in_fear():
            return False
        if action_name not in ("Медитация", "Успокоение"):
            return False
        store.izzy_meditation_count = int(getattr(store, "izzy_meditation_count", 0) or 0) + 1
        if renpy.random.random() < 0.5:
            store.izzy_fear_state = False
            renpy.log("[Иззи][Пробуждение] страх снят")
            return True
        return False

    def izzy_on_damage_received(target=None, **kwargs):
        """Ур.9: при потерянном равновесии Иззи получает в 1.5 раза больше урона."""
        if not izzy_is_char(target):
            return False
        if not bool(getattr(store, "izzy_equilibrium_broken", False)):
            return False
        char = izzy_char()
        if char is None or int(getattr(char, "current_hp", 0)) <= 0:
            return False
        # Дополнительный урон — половина уже полученного.
        extra = max(1, int((IZZY_ECHO_BACKLASH - 1.0) * 10))
        char.current_hp = max(0, int(getattr(char, "current_hp", 0)) - extra)
        return True
