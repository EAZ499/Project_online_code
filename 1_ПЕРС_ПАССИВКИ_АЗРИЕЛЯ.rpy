# ============================================================================
# ПАССИВНЫЕ СПОСОБНОСТИ, ОБЛИКИ И ОГНЕВАЯ ВЕТКА АЗРИЕЛЯ
# ----------------------------------------------------------------------------
# Вся логика собрана здесь, чтобы точки вызова в бою были однострочными.
#
#   Размножение личности ур.1  — облики «пушистый принц» / «отзвуки прошлого»,
#                                от облика зависит доступная магия
#   Строя оборону ур.1         — +5% бонусной защиты за каждую защиту
#   Образ принца ур.1          — в начале боя +3 социализации и +3 власти,
#                                обнуляется при первом провале
#   Лоб в лоб ур.1             — шанс 15%+1%*ур за полученный урон: +1 танк,
#                                +2% бонусной брони
#   Пушистик ур.1              — «Поддержать» поднимает упавшего союзника
#                                и даёт команде +2 комфорта
#   Подсознательная память ур.1— проигранный бой навсегда даёт +7*ур базовой магии
#   Стойкий ур.2 / ур.8        — нельзя повалить (20 MP), на 8 ур. ещё +25% защиты
#                                при 0 хп или повале
#   Голубая кровь ур.3         — дважды за раунд сброс дебаффов с шансом
#                                20%+1,5%*ур, но кровотечение бьёт вдвое сильнее
#   Рука помощи ур.4           — поднимает упавшего союзника, уровень/2 раз, 20 MP
#   Свита голубых кровей ур.6  — «Голубая кровь» на команду с половинным шансом,
#                                без штрафа кровотечения
#   Огневая ветка (ур.3-10)    — Пламенная инфузия, Перегрев, Пиромания,
#                                Хаос в огне, Плавящий луч, Пусть всё горит,
#                                Осколки звёзд, Столбы огня
# ============================================================================

# --- Состояние боя (сбрасывается в начале боя) -------------------------------
default azri_form = "fluffy"
default azri_prince_active = False
default azri_defense_added = 0.0
default azri_tank_added = 0.0
default azri_last_stand_active = False
default azri_helping_hand_uses = 0
default azri_blades_pending = False
default azri_firefly_active = False
default azri_infusion_chance = 0.20
default azri_overheat_chance = 0.15
default azri_chain_bonus = 0.0
default azri_chain_link = 0
default azri_memory_registered = False

# --- Состояние вне слотов сохранения -----------------------------------------
default persistent.azri_memory_bonus = 0


init python:
    # ========================================================================
    # КОНСТАНТЫ
    # ========================================================================

    AZRI_FORM_FLUFFY = "fluffy"
    AZRI_FORM_ECHO = "echo"
    AZRI_FORM_NAMES = {
        AZRI_FORM_FLUFFY: "Пушистый принц",
        AZRI_FORM_ECHO: "Отзвуки прошлого",
    }
    # «Размножение личности»: какие магии доступны в каком облике.
    AZRI_FORM_ABILITIES = {
        AZRI_FORM_FLUFFY: ("Шаг вперёд", "Горное равновесие", "За спиною принца",
                           "Встать с колен", "Боевой клич!"),
        AZRI_FORM_ECHO: ("Магия огня", "Клинки хаоса", "Уничтожитель хаоса",
                         "Звёздный блеск", "Луч Бога Гиперсмерти"),
    }

    # «Строя оборону» ур.1
    AZRI_DEFEND_BONUS = 0.05
    # «Образ принца» ур.1
    AZRI_PRINCE_BONUS = 3
    # «Лоб в лоб» ур.1
    AZRI_HEAD_ON_CHANCE_BASE = 0.15
    AZRI_HEAD_ON_CHANCE_PER_LEVEL = 0.01
    AZRI_HEAD_ON_TANK = 1
    AZRI_HEAD_ON_DEF = 0.02
    # «Пушистик» ур.1
    AZRI_FLUFFY_COMFORT = 2
    # «Подсознательная память» ур.1
    AZRI_MEMORY_MAGIC_PER_LEVEL = 7
    # «Стойкий» ур.2 / ур.8
    AZRI_STEADFAST_LEVEL = 2
    AZRI_STEADFAST_MP = 20
    AZRI_LAST_STAND_LEVEL = 8
    AZRI_LAST_STAND_DEF = 0.25
    # «Голубая кровь» ур.3 / «Свита голубых кровей» ур.6
    AZRI_BLUE_BLOOD_LEVEL = 3
    AZRI_BLUE_BLOOD_CHANCE_BASE = 0.20
    AZRI_BLUE_BLOOD_CHANCE_PER_LEVEL = 0.015
    AZRI_BLUE_BLOOD_CLEANSES = 2
    AZRI_BLUE_BLOOD_BLEED_MULTIPLIER = 2.0
    AZRI_BLUE_BLOOD_RETINUE_LEVEL = 6
    # «Рука помощи» ур.4
    AZRI_HELPING_HAND_LEVEL = 4
    AZRI_HELPING_HAND_MP = 20
    AZRI_HELPING_HAND_HEAL = 0.20
    # «2 шага вперёд» ур.2
    AZRI_TWO_STEPS_LEVEL = 2
    AZRI_STEP_FORWARD_TANK = 3
    AZRI_STEP_FORWARD_TANK_MASTERED = 6
    AZRI_STEP_FORWARD_COOLDOWN = 2
    AZRI_STEP_FORWARD_COOLDOWN_MASTERED = 4
    # Огневая ветка
    AZRI_INFUSION_LEVEL = 3
    AZRI_INFUSION_BASE = 0.20
    AZRI_INFUSION_MAX = 0.80
    AZRI_INFUSION_DAMAGE = 0.25
    AZRI_OVERHEAT_LEVEL = 4
    AZRI_OVERHEAT_BASE = 0.15
    AZRI_OVERHEAT_MAX = 0.40
    AZRI_OVERHEAT_DAMAGE = 0.15
    AZRI_FIRE_CHANCE_STEP_PER_LEVEL = 0.005
    AZRI_PYROMANIA_LEVEL = 5
    AZRI_PYROMANIA_STEP_PER_LEVEL = 0.015
    AZRI_CHAOS_FIRE_LEVEL = 6
    AZRI_CHAOS_FIRE_BASE = 0.20
    AZRI_CHAOS_FIRE_PER_LEVEL = 0.03
    AZRI_MELT_BEAM_LEVEL = 7
    AZRI_MELT_BEAM_CHANCE = 0.25
    AZRI_MELT_BEAM_ARMOR = 0.20
    AZRI_EVERYTHING_BURNS_LEVEL = 8
    AZRI_EVERYTHING_BURNS_STEP = 0.05
    AZRI_STAR_SHARDS_LEVEL = 9
    AZRI_STAR_SHARDS_CHANCE = 0.30
    AZRI_STAR_SHARDS_DAMAGE = 0.20
    AZRI_FIRE_PILLARS_LEVEL = 10

    # Дебаффы, которые смывает «Голубая кровь».
    AZRI_CLEANSE_ATTRS = (
        "bloodshed_debuff", "prone_debuff", "atk_debuff", "def_debuff",
        "magic_debuff", "accuracy_debuff", "critrate_debuff",
        "critdmg_debuff", "tank_debuff",
    )

    # ========================================================================
    # ОБЩИЕ ХЕЛПЕРЫ
    # ========================================================================

    def azri_level():
        """Общий уровень персонажей для формул пассивок Азриеля."""
        return max(1, int(getattr(getattr(store, "Pers", None), "global_level", 0) or 0))

    def azri_char():
        """Объект Азриеля из команды, либо None."""
        return (getattr(store, "pers_dict", {}) or {}).get("Азриель")

    def azri_is_azri(char):
        return char is not None and getattr(char, "name", None) == "Азриель"

    def azri_bonus_def_add(char, amount):
        """Добавляет бонусную защиту и запоминает вклад пассивок (для сброса)."""
        if char is None or amount == 0:
            return
        char.bonus_def = float(getattr(char, "bonus_def", 0.0)) + amount
        store.azri_defense_added = float(getattr(store, "azri_defense_added", 0.0)) + amount

    def azri_bonus_tank_add(char, amount):
        if char is None or amount == 0:
            return
        char.bonus_tank = float(getattr(char, "bonus_tank", 0.0)) + amount
        store.azri_tank_added = float(getattr(store, "azri_tank_added", 0.0)) + amount

    # ========================================================================
    # РАЗМНОЖЕНИЕ ЛИЧНОСТИ (облики)
    # ========================================================================

    def azri_current_form():
        form = getattr(store, "azri_form", AZRI_FORM_FLUFFY)
        return form if form in AZRI_FORM_ABILITIES else AZRI_FORM_FLUFFY

    def azri_form_name():
        return AZRI_FORM_NAMES.get(azri_current_form(), "Пушистый принц")

    def azri_toggle_form():
        """«Сменить облик»: пушистый принц ⇄ отзвуки прошлого."""
        new_form = (AZRI_FORM_ECHO if azri_current_form() == AZRI_FORM_FLUFFY
                    else AZRI_FORM_FLUFFY)
        store.azri_form = new_form
        renpy.log("[Азриель][Облик] теперь: {}".format(AZRI_FORM_NAMES.get(new_form, new_form)))
        return new_form

    def azri_form_allows(ability_name):
        """Доступна ли магия в текущем облике (для реестра кнопок)."""
        if ability_name not in (AZRI_FORM_ABILITIES[AZRI_FORM_FLUFFY]
                                + AZRI_FORM_ABILITIES[AZRI_FORM_ECHO]):
            return True  # не магия облика — облик не ограничивает
        return ability_name in AZRI_FORM_ABILITIES.get(azri_current_form(), ())

    # ========================================================================
    # СБРОС В НАЧАЛЕ БОЯ
    # ========================================================================

    def azri_reset_battle_state():
        """Сброс боевого состояния Азриеля в начале боя."""
        azri = azri_char()

        # Снимаем накопленные пассивками бонусы защиты и танка.
        if azri is not None:
            if getattr(store, "azri_defense_added", 0.0):
                azri.bonus_def = max(0.0, float(getattr(azri, "bonus_def", 0.0))
                                     - float(store.azri_defense_added))
            if getattr(store, "azri_tank_added", 0.0):
                azri.bonus_tank = max(0.0, float(getattr(azri, "bonus_tank", 0.0))
                                      - float(store.azri_tank_added))
            # «За спиною принца»: бонус снимается с того, кому его дали.
            for _ally in (getattr(store, "pers_dict", {}) or {}).values():
                if getattr(_ally, "azri_def_bonus", 0):
                    _ally.azri_def_bonus = 0

        store.azri_defense_added = 0.0
        store.azri_tank_added = 0.0
        store.azri_last_stand_active = False
        store.azri_blades_pending = False
        store.azri_firefly_active = False
        store.azri_infusion_chance = AZRI_INFUSION_BASE
        store.azri_overheat_chance = AZRI_OVERHEAT_BASE
        store.azri_chain_bonus = 0.0
        store.azri_chain_link = 0
        store.azri_memory_registered = False

        # «Размножение личности»: в начале боя облик по умолчанию.
        store.azri_form = AZRI_FORM_FLUFFY

        # «Рука помощи»: количество подъёмов = уровень / 2.
        store.azri_helping_hand_uses = max(1, azri_level() // 2)

        # «Образ принца»: +3 социализации и власти до первого провала.
        azri_apply_prince_image()
        return True

    # ========================================================================
    # СТРОЯ ОБОРОНУ / ОБРАЗ ПРИНЦА
    # ========================================================================

    def azri_apply_prince_image():
        """«Образ принца» ур.1: +3 социализации и +3 власти в начале боя."""
        azri = azri_char()
        if azri is None or azri_level() < 1:
            return False
        if getattr(store, "azri_prince_active", False):
            return False
        azri.bonus_socialization = float(getattr(azri, "bonus_socialization", 0.0)) + AZRI_PRINCE_BONUS
        azri.bonus_power = float(getattr(azri, "bonus_power", 0.0)) + AZRI_PRINCE_BONUS
        store.azri_prince_active = True
        return True

    def azri_on_fail():
        """«Образ принца»: первый провал обнуляет бонус."""
        if not getattr(store, "azri_prince_active", False):
            return False
        azri = azri_char()
        if azri is None:
            return False
        azri.bonus_socialization = max(0.0, float(getattr(azri, "bonus_socialization", 0.0)) - AZRI_PRINCE_BONUS)
        azri.bonus_power = max(0.0, float(getattr(azri, "bonus_power", 0.0)) - AZRI_PRINCE_BONUS)
        store.azri_prince_active = False
        renpy.log("[Азриель][Образ принца] бонус обнулён из-за провала")
        return True

    def azri_on_action_result(attacker, success):
        """Хук после проверки действия: провал Азриеля ломает «Образ принца»."""
        if azri_is_azri(attacker) and not success:
            return azri_on_fail()
        return False

    def azri_on_defend():
        """«Строя оборону» ур.1: каждая защита даёт +5% бонусной защиты."""
        if getattr(store, "current_attacker", None) != 2:
            return False
        azri = azri_char()
        if not azri_is_azri(azri):
            return False
        azri_bonus_def_add(azri, AZRI_DEFEND_BONUS)
        renpy.log("[Азриель][Строя оборону] bonus_def = {}".format(azri.bonus_def))
        return True

    # ========================================================================
    # ЛОБ В ЛОБ / СТОЙКИЙ
    # ========================================================================

    def azri_on_damage_taken(char, old_hp=None):
        """«Лоб в лоб» ур.1 и «Стойкий» ур.8 — реакция на полученный урон."""
        if not azri_is_azri(char):
            return False
        took_damage = old_hp is None or getattr(char, "current_hp", 0) < old_hp
        if took_damage:
            chance = AZRI_HEAD_ON_CHANCE_BASE + AZRI_HEAD_ON_CHANCE_PER_LEVEL * azri_level()
            if renpy.random.random() < chance:
                azri_bonus_tank_add(char, AZRI_HEAD_ON_TANK)
                azri_bonus_def_add(char, AZRI_HEAD_ON_DEF)
        # «Стойкий» ур.8: +25% защиты, когда Азриель на нуле.
        if getattr(char, "current_hp", 1) <= 0:
            azri_last_stand(char)
        return True

    def azri_last_stand(char=None):
        """«Стойкий» ур.8: +25% защиты при 0 хп или повале (один раз за бой)."""
        azri = azri_char() if char is None else char
        if not azri_is_azri(azri) or azri_level() < AZRI_LAST_STAND_LEVEL:
            return False
        if getattr(store, "azri_last_stand_active", False):
            return False
        store.azri_last_stand_active = True
        azri_bonus_def_add(azri, AZRI_LAST_STAND_DEF)
        renpy.log("[Азриель][Стойкий ур.8] +25% защиты")
        return True

    def azri_try_prevent_prone(char):
        """«Стойкий» ур.2: повалить Азриеля нельзя, если есть 20 MP."""
        if not azri_is_azri(char):
            return False
        if azri_level() < AZRI_STEADFAST_LEVEL:
            return False
        if float(getattr(char, "current_mp", 0)) < AZRI_STEADFAST_MP:
            return False
        char.current_mp = max(0.0, float(char.current_mp) - AZRI_STEADFAST_MP)
        renpy.log("[Азриель][Стойкий] повал отменён, списано {} MP".format(AZRI_STEADFAST_MP))
        return True

    # ========================================================================
    # ГОЛУБАЯ КРОВЬ / РУКА ПОМОЩИ / ПУШИСТИК
    # ========================================================================

    def azri_blue_blood_chance():
        """Шанс «Голубой крови»: 20% + 1,5% * уровень."""
        if azri_level() < AZRI_BLUE_BLOOD_LEVEL:
            return 0.0
        return AZRI_BLUE_BLOOD_CHANCE_BASE + AZRI_BLUE_BLOOD_CHANCE_PER_LEVEL * azri_level()

    def azri_bleed_multiplier(char):
        """«Голубая кровь»: Азриель теряет вдвое больше от кровотечения."""
        if not azri_is_azri(char):
            return 1.0
        if azri_level() < AZRI_BLUE_BLOOD_LEVEL:
            return 1.0
        return AZRI_BLUE_BLOOD_BLEED_MULTIPLIER

    def azri_cleanse_char(char, cleanses):
        """Сбрасывает до `cleanses` негативных эффектов с персонажа."""
        removed = 0
        for attr in AZRI_CLEANSE_ATTRS:
            if removed >= cleanses:
                break
            if getattr(char, attr, 0) > 0:
                setattr(char, attr, 0)
                got_attr = attr + "_got"
                if hasattr(char, got_attr):
                    setattr(char, got_attr, 0)
                removed += 1
        return removed

    def azri_cleanse_round():
        """Начало раунда: «Голубая кровь» и «Свита голубых кровей»."""
        azri = azri_char()
        if azri is None:
            return 0
        cleansed = 0

        # Себя: два эффекта с полным шансом.
        if getattr(azri, "current_hp", 0) > 0 and renpy.random.random() < azri_blue_blood_chance():
            cleansed += azri_cleanse_char(azri, AZRI_BLUE_BLOOD_CLEANSES)

        # «Свита голубых кровей» ур.6: то же для команды с половинным шансом.
        if azri_level() >= AZRI_BLUE_BLOOD_RETINUE_LEVEL:
            half = azri_blue_blood_chance() * 0.5
            for _ally in (getattr(store, "pers_dict", {}) or {}).values():
                if _ally is azri or not getattr(_ally, "is_ally", False):
                    continue
                if getattr(_ally, "current_hp", 0) <= 0 or getattr(_ally, "picked", 0) != 1:
                    continue
                if renpy.random.random() < half:
                    cleansed += azri_cleanse_char(_ally, AZRI_BLUE_BLOOD_CLEANSES)
        return cleansed

    def azri_try_helping_hand(fallen):
        """«Рука помощи» ур.4: поднимает упавшего союзника за 20 MP."""
        if fallen is None or azri_is_azri(fallen):
            return False
        if not getattr(fallen, "is_ally", False) or getattr(fallen, "picked", 0) != 1:
            return False
        if getattr(fallen, "current_hp", 1) > 0:
            return False

        azri = azri_char()
        if azri is None or getattr(azri, "current_hp", 0) <= 0:
            return False
        if azri_level() < AZRI_HELPING_HAND_LEVEL:
            return False
        if int(getattr(store, "azri_helping_hand_uses", 0) or 0) <= 0:
            return False
        if float(getattr(azri, "current_mp", 0)) < AZRI_HELPING_HAND_MP:
            return False

        azri.current_mp = max(0.0, float(azri.current_mp) - AZRI_HELPING_HAND_MP)
        store.azri_helping_hand_uses = int(store.azri_helping_hand_uses) - 1
        fallen.current_hp = max(1, int(getattr(fallen, "max_hp", 0) * AZRI_HELPING_HAND_HEAL))
        if "clear_swoon_pending_for_visual" in globals():
            store.clear_swoon_pending_for_visual(fallen)
        fallen.damage_gain_for_vis = -fallen.current_hp
        renpy.notify("Рука помощи: {} поднят".format(getattr(fallen, "name", "союзник")))
        renpy.log("[Азриель][Рука помощи] поднят {}, осталось {}".format(
            getattr(fallen, "name", "?"), store.azri_helping_hand_uses))
        return True

    def azri_fluffy_raise(fallen):
        """«Пушистик» ур.1: поддержка поднимает упавшего союзника."""
        if fallen is None or azri_is_azri(fallen):
            return False
        if not getattr(fallen, "is_ally", False) or getattr(fallen, "picked", 0) != 1:
            return False
        if getattr(fallen, "current_hp", 1) > 0:
            return False
        fallen.current_hp = max(1, int(getattr(fallen, "max_hp", 0) * AZRI_HELPING_HAND_HEAL))
        if "clear_swoon_pending_for_visual" in globals():
            store.clear_swoon_pending_for_visual(fallen)
        fallen.damage_gain_for_vis = -fallen.current_hp
        renpy.notify("Пушистик: {} поднят поддержкой".format(getattr(fallen, "name", "союзник")))
        return True

    def azri_on_support(attacker_name, target):
        """«Пушистик» ур.1: поддержка поднимает упавшего и даёт команде комфорт."""
        if attacker_name != "Азриель":
            return False
        if not bool(getattr(store, "try_to_nego_result", False)):
            return False

        raised = azri_fluffy_raise(target)
        for _ally in (getattr(store, "pers_dict", {}) or {}).values():
            if getattr(_ally, "is_ally", False) and getattr(_ally, "picked", 0) == 1:
                _ally.bonus_comfort = float(getattr(_ally, "bonus_comfort", 0.0)) + AZRI_FLUFFY_COMFORT
        renpy.log("[Азриель][Пушистик] команда получила +{} комфорта".format(AZRI_FLUFFY_COMFORT))
        return raised

    # ========================================================================
    # ПОДСОЗНАТЕЛЬНАЯ ПАМЯТЬ
    # ========================================================================

    def azri_memory_bonus():
        """Навсегда накопленная прибавка к базовой магии Азриеля."""
        return max(0, int(getattr(persistent, "azri_memory_bonus", 0) or 0))

    def azri_register_battle_lost():
        """Проигранный бой: +7 * уровень к базовой магии (навсегда)."""
        if bool(getattr(store, "azri_memory_registered", False)):
            return 0
        store.azri_memory_registered = True
        gain = AZRI_MEMORY_MAGIC_PER_LEVEL * azri_level()
        persistent.azri_memory_bonus = azri_memory_bonus() + gain
        renpy.log("[Азриель][Подсознательная память] +{} базовой магии, всего {}".format(
            gain, azri_memory_bonus()))
        return gain

    # ========================================================================
    # ОГНЕВАЯ ВЕТКА
    # ========================================================================

    def azri_fire_damage(ratio):
        """Урон огнём по формуле ratio * магия Азриеля."""
        azri = azri_char()
        if azri is None:
            return 0
        return max(1, int(float(getattr(azri, "magic", 0)) * ratio))

    def azri_fire_chances():
        """(шанс инфузии, шанс перегрева) с учётом накопленного бонуса."""
        bonus = float(getattr(store, "azri_chain_bonus", 0.0) or 0.0)
        infusion = min(AZRI_INFUSION_MAX, float(getattr(store, "azri_infusion_chance", AZRI_INFUSION_BASE)) + bonus)
        overheat = min(AZRI_OVERHEAT_MAX, float(getattr(store, "azri_overheat_chance", AZRI_OVERHEAT_BASE)) + bonus)
        return infusion, overheat

    def azri_fire_grow(kind, success):
        """Шанс растёт только при провале, до своего максимума.

        Сбрасывает накопленное только «Пусть всё горит» ур.8
        (azri_burning_chain уменьшает azri_chain_bonus).
        """
        if success:
            return
        step = AZRI_FIRE_CHANCE_STEP_PER_LEVEL * azri_level()
        if kind == "infusion":
            base = float(getattr(store, "azri_infusion_chance", AZRI_INFUSION_BASE))
            store.azri_infusion_chance = min(AZRI_INFUSION_MAX, base + step)
        else:
            base = float(getattr(store, "azri_overheat_chance", AZRI_OVERHEAT_BASE))
            store.azri_overheat_chance = min(AZRI_OVERHEAT_MAX, base + step)

    def azri_pyromania_grow():
        """«Пиромания» ур.5: каждое попадание поднимает оба шанса."""
        if azri_level() < AZRI_PYROMANIA_LEVEL:
            return 0.0
        if not getattr(store, "azri_firefly_active", False):
            return 0.0
        step = AZRI_PYROMANIA_STEP_PER_LEVEL * azri_level()
        store.azri_chain_bonus = min(AZRI_INFUSION_MAX,
                                     float(getattr(store, "azri_chain_bonus", 0.0)) + step)
        return step

    def azri_overheat(primary, base_damage):
        """«Перегрев» ур.4: поджигает и бьёт остальных врагов."""
        if azri_level() < AZRI_OVERHEAT_LEVEL:
            return 0
        _infusion, chance = azri_fire_chances()
        if renpy.random.random() >= chance:
            azri_fire_grow("overheat", False)
            return 0
        azri_fire_grow("overheat", True)

        burn = max(1, int(azri_fire_damage(AZRI_OVERHEAT_DAMAGE)))
        hit = 0
        for _name in get_active_enemies():
            _enemy = store.enemies.get(_name)
            if _enemy is None or _enemy is primary or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            _enemy.current_hp = max(0, _enemy.current_hp - burn)
            _enemy.damage_gain_for_vis = burn
            if "add_attack_result" in globals():
                add_attack_result("Азриель", _enemy.name, burn, False, "magic")
            hit += 1
        if hit:
            renpy.log("[Азриель][Перегрев] загорелись {} врагов по {}".format(hit, burn))
        return burn

    def azri_infusion(target, base_damage, depth=0):
        """«Пламенная инфузия» ур.3 (+ «Столбы огня» ур.10)."""
        if azri_level() < AZRI_INFUSION_LEVEL or target is None:
            return 0
        if getattr(target, "current_hp", 0) <= 0:
            return 0
        if depth > 5:
            return 0

        chance, _overheat = azri_fire_chances()
        if renpy.random.random() >= chance:
            azri_fire_grow("infusion", False)
            return 0
        azri_fire_grow("infusion", True)

        burn = azri_fire_damage(AZRI_INFUSION_DAMAGE)
        target.current_hp = max(0, target.current_hp - burn)
        target.damage_gain_for_vis = burn
        if "add_attack_result" in globals():
            add_attack_result("Азриель", target.name, burn, False, "magic")
        renpy.log("[Азриель][Пламенная инфузия] {} урона по {}".format(burn, target.name))

        # «Столбы огня» ур.10: инфузия может вызвать ещё одну на ту же цель.
        if azri_level() >= AZRI_FIRE_PILLARS_LEVEL:
            azri_infusion(target, base_damage, depth + 1)

        # «Пусть всё горит» ур.8: цепочка с перегревом до первого провала.
        if azri_level() >= AZRI_EVERYTHING_BURNS_LEVEL:
            azri_burning_chain(target, base_damage)
        return burn

    def azri_burning_chain(target, base_damage, depth=0):
        """«Пусть всё горит» ур.8: инфузия и перегрев вызывают друг друга."""
        if depth > 5:
            return 0
        step = AZRI_EVERYTHING_BURNS_STEP
        bonus = float(getattr(store, "azri_chain_bonus", 0.0))
        if bonus <= 0:
            return 0
        store.azri_chain_bonus = max(0.0, bonus - step)
        return azri_overheat(target, base_damage)

    def azri_chaos_in_fire(target, base_damage):
        """«Хаос в огне» ур.6: попадание клинками провоцирует огонь."""
        if azri_level() < AZRI_CHAOS_FIRE_LEVEL:
            return 0
        chance = min(1.0, AZRI_CHAOS_FIRE_BASE + AZRI_CHAOS_FIRE_PER_LEVEL * azri_level())
        if renpy.random.random() >= chance:
            return 0
        azri_infusion(target, base_damage)
        azri_overheat(target, base_damage)
        return 1

    def azri_fire_on_damage(target, base_damage, from_fireflies=False):
        """Общий хук огневой ветки: вызывается после урона Азриеля."""
        if target is None or not azri_is_azri(azri_char()):
            return 0
        azri_pyromania_grow()
        azri_infusion(target, base_damage)
        if from_fireflies:
            azri_overheat(target, base_damage)
        return 1

    def azri_delayed_blades():
        """«Клинки хаоса»: огоньки бьют в начале хода врага."""
        if not getattr(store, "azri_blades_pending", False):
            return 0
        store.azri_blades_pending = False
        if azri_level() < 4:
            return 0
        total = 0
        for _name in get_active_enemies():
            _enemy = store.enemies.get(_name)
            if _enemy is None or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            hit = max(1, int(azri_fire_damage(0.40)))
            _enemy.current_hp = max(0, _enemy.current_hp - hit)
            _enemy.damage_gain_for_vis = hit
            if "add_attack_result" in globals():
                add_attack_result("Азриель", _enemy.name, hit, False, "magic")
            azri_chaos_in_fire(_enemy, hit)
            azri_overheat(_enemy, hit)
            total += hit
        return total

    def azri_melt_beam(target):
        """«Плавящий луч» ур.7: шанс снизить броню цели на 20%."""
        if target is None or azri_level() < AZRI_MELT_BEAM_LEVEL:
            return False
        if renpy.random.random() >= AZRI_MELT_BEAM_CHANCE:
            return False
        target.def_debuff_var = max(0.0, float(getattr(target, "def_debuff_var", 1.0))
                                    * (1.0 - AZRI_MELT_BEAM_ARMOR))
        renpy.log("[Азриель][Плавящий луч] броня {} снижена на 20%".format(getattr(target, "name", "?")))
        return True

    def azri_star_shards(source, damage):
        """«Осколки звёзд» ур.9: малые звёзды бьют других врагов."""
        if azri_level() < AZRI_STAR_SHARDS_LEVEL or damage <= 0:
            return 0
        if renpy.random.random() >= AZRI_STAR_SHARDS_CHANCE:
            return 0
        splash = max(1, int(damage * AZRI_STAR_SHARDS_DAMAGE))
        for _name in get_active_enemies():
            _enemy = store.enemies.get(_name)
            if _enemy is None or _enemy is source or getattr(_enemy, "current_hp", 0) <= 0:
                continue
            _enemy.current_hp = max(0, _enemy.current_hp - splash)
            _enemy.damage_gain_for_vis = splash
            if "add_attack_result" in globals():
                add_attack_result("Азриель", _enemy.name, splash, False, "magic")
        return splash

    def azri_step_forward_tank():
        """«Шаг вперёд»: +3 танка, с «2 шага вперёд» ур.2 — вдвое больше."""
        if azri_level() >= AZRI_TWO_STEPS_LEVEL:
            return AZRI_STEP_FORWARD_TANK_MASTERED
        return AZRI_STEP_FORWARD_TANK

    def azri_apply_back_of_prince(ally):
        """«За спиною принца»: бонусная защита Азриеля уходит союзнику."""
        azri = azri_char()
        if azri is None or ally is None or ally is azri:
            return 0
        bonus_value = float(getattr(azri, "base_def", 0)) * float(getattr(azri, "bonus_def", 0.0))
        ally.azri_def_bonus = float(getattr(ally, "azri_def_bonus", 0.0)) + bonus_value
        renpy.log("[Азриель][За спиною принца] {} получает +{:.1f} защиты".format(
            getattr(ally, "name", "?"), bonus_value))
        return bonus_value
