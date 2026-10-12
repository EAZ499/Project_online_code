# ============================================================================
# ПАССИВНЫЕ СПОСОБНОСТИ КРИСА
# ----------------------------------------------------------------------------
# Здесь собрана вся логика пассивок Криса, чтобы точки вызова в бою были
# однострочными, а формулы жили в одном месте.
#
#   VESSEL CONTROL ур.1              — порог контроля по отношениям
#                                      + проверка перезарядки у автоатаки
#   DECAYING ур.1                    — −1 max HP за каждую смерть
#                                      (регистрируется в лейбле game_over)
#   Причина ошибок ур.1              — шанс на дополнительный ход после действия
#   Привыкший к общажной жизни ур.1  — вредная еда: −2 кровотечение в конце
#                                      хода и +1 комфорт
#   Следы на мече ур.3               — навсегда +0.25% крит.урона и +0.15% атаки
#                                      за каждого добитого врага
#   Вмятины на щите ур.7             — +2% бонусной защиты за каждый полученный
#                                      удар в стойке со щитом
#   Желание жить ур.9                — 1 раз за бой 20% HP при падении до 0
# ============================================================================

# --- Состояние боя (сбрасывается в fightbegin12) -----------------------------
default kris_error_chance = 0.0
default kris_error_extra_turn_granted = False
default kris_wish_to_live_used = False
default kris_junk_food_pending = 0
default kris_shield_dents = 0
default kris_shield_dents_baseline = None
default kris_decaying_registered = False
default actions_count_snapshot = 0

# --- Состояние вне слотов сохранения (persistent) ----------------------------
default persistent.kris_decaying_deaths = 0
default persistent.kris_sword_marks = 0


init python:
    # ========================================================================
    # КОНСТАНТЫ ПАССИВОК
    # ========================================================================

    # «Причина ошибок»: максимальный шанс = 2% * уровень персонажа,
    # начальное значение = 0.5% * уровень,
    # прибавка за ход = 1% + 0.25% * уровень.
    KRIS_ERROR_MAX_PER_LEVEL = 0.02
    KRIS_ERROR_START_PER_LEVEL = 0.005
    KRIS_ERROR_STEP_BASE = 0.01
    KRIS_ERROR_STEP_PER_LEVEL = 0.0025

    # «Следы на мече»: за каждого добитого врага.
    KRIS_SWORD_MARK_CRIT_DMG = 0.0025   # +0.25% крит. урона
    KRIS_SWORD_MARK_ATK = 0.0015        # +0.15% атаки

    # «Вмятины на щите»: +2% бонусной защиты за удар.
    KRIS_SHIELD_DENT_BONUS = 0.02

    # «Желание жить»: 20% HP один раз за бой.
    KRIS_WISH_TO_LIVE_HEAL = 0.20

    # «DECAYING»: −1 max HP за смерть.
    KRIS_DECAYING_HP_PER_DEATH = 1

    # «Способности возвращаются» ур.2: призыв меча и щита стоит вдвое меньше.
    KRIS_SUMMON_ABILITIES = ("Призвать меч", "Призвать щит")
    KRIS_SUMMON_COST_MULTIPLIER = 0.5
    KRIS_SUMMON_COST_LEVEL = 2

    # «Направить фокус» ур.3: шанс двойного бонуса «Напрячься».
    KRIS_FOCUS_LEVEL = 3
    KRIS_FOCUS_CHANCE = 0.20
    KRIS_FOCUS_BONUS = 0.30          # базовый бонус атаки от «Напрячься»

    # «Удачные прятки» ур.4: «Позвать за щит» даёт союзнику 1 щит.
    KRIS_ALLY_SHIELD_LEVEL = 4

    # «Правильный угол» ур.5: 10% щит при «защищаться»; сам бафф даёт 50% уворот.
    KRIS_DEFEND_SHIELD_LEVEL = 5
    KRIS_DEFEND_SHIELD_CHANCE = 0.10
    KRIS_RIGHT_ANGLE_DODGE_CHANCE = 0.50

    # «Привычка к вращению» ур.6: «С разворота!».
    KRIS_SPIN_LEVEL = 6
    KRIS_SPIN_DAMAGE = 1.3           # дополнительный урон без улучшения
    KRIS_SPIN_DAMAGE_MASTERED = 1.5  # дополнительный урон с улучшением
    KRIS_SPIN_SPLASH_CHANCE = 0.30
    KRIS_SPIN_SPLASH_RATIO = 0.5

    # «Гибкое терпение» ур.8: «Слабое место» после 1 действия, +50% за действие.
    KRIS_FLEXIBLE_PATIENCE_LEVEL = 8
    KRIS_FLEXIBLE_PATIENCE_STEP = 0.5

    # VESSEL CONTROL: очередь атак для сорвавшегося хода Криса —
    # от самой сильной к самой слабой. Порядок правится только здесь.
    KRIS_ATTACK_QUEUE = (
        "Отчаянное комбо",          # ур.8: игнор брони, +30% крит-шанс и крит-урон
        "C разворота!",             # ур.3: 130% (150% с ур.6) и сплэш по остальным
        "Пронзить",                 # ур.5: кровотечение х2 и снятие брони
        "Удар мечом",               # базовый удар мечом
        "Бонк!",                    # ур.4: ослабление атаки и истощение
        "Отбить руки",              # ур.6: сильное ослабление атаки
        "Удар щитом",               # базовый удар щитом
        "Рывок защитника (атака)",  # ур.9: танк и щит, урона мало
        "Удар неудачника",          # фолбэк без оружия
    )

    # Атака → лейбл завершения (диспетчер автоатаки).
    KRIS_ATTACK_LABELS = {
        "Удар неудачника": "kris_atk1_is_done",
        "Удар мечом": "kris_atk2_is_done",
        "Удар щитом": "kris_atk3_is_done",
        "C разворота!": "kris_atk4_is_done",
        "Бонк!": "kris_atk5_is_done",
        "Пронзить": "kris_atk6_is_done",
        "Отбить руки": "kris_atk7_is_done",
        "Отчаянное комбо": "kris_atk10_combo_is_done",
        "Рывок защитника (атака)": "kris_atk11_is_done",
    }

    # «Привыкший к общажной жизни»: вредная еда.
    KRIS_JUNK_FOOD_BLEED = 2            # −2 к дебафу кровотечения
    KRIS_JUNK_FOOD_COMFORT = 1          # +1 комфорт
    # Список «вредной еды». При необходимости состав правится только здесь.
    KRIS_JUNK_FOOD_ITEMS = (
        "food_icecream",
        "food_frenchfries",
        "food_pepperoni",
        "food_cookiesharing",
        "food_colacoffee",
        "food_lottery_candy",
        "food_lucky_monstercandy",
        "food_mint_gum",
        "food_noodles",
        "food_readymeal_1",
        "food_readymeal_2",
        "food_readymeal_3",
        "food_clubsandwich",
        "food_sans_sandwich",
    )

    # ========================================================================
    # ОБЩИЕ ХЕЛПЕРЫ
    # ========================================================================

    def kris_passive_level():
        """Текущий общий уровень персонажей (для формул пассивок)."""
        return max(1, int(getattr(getattr(store, "Pers", None), "global_level", 0) or 0))

    def kris_char():
        """Объект Криса из команды, либо None."""
        return (getattr(store, "pers_dict", {}) or {}).get("Крис")

    def kris_is_char(char):
        return char is not None and getattr(char, "name", None) == "Крис"

    def kris_reset_battle_passives():
        """Сброс «боевых» пассивок в начале боя (fightbegin12).

        Снимает ровно накопленные «Вмятины на щите», обнуляет одноразовые
        флаги и возвращает «Причине ошибок» начальный шанс.
        """
        kris = kris_char()

        # Возвращаем bonus_def к значению до первой вмятины этого боя, чтобы
        # бонус не накапливался между боями.
        dents = int(getattr(store, "kris_shield_dents", 0) or 0)
        baseline = getattr(store, "kris_shield_dents_baseline", None)
        if kris is not None and dents > 0 and baseline is not None:
            kris.bonus_def = max(0.0, float(baseline))

        store.kris_shield_dents = 0
        store.kris_shield_dents_baseline = None
        store.kris_wish_to_live_used = False
        store.kris_junk_food_pending = 0
        store.kris_decaying_registered = False

        # Счётчик действий обнуляется в начале боя у всех бойцов.
        for _ally in (getattr(store, "pers_dict", {}) or {}).values():
            _ally.actions_count = 0
        store.actions_count_snapshot = 0

        kris_reset_error_chance()
        return True

    # ========================================================================
    # ПРИЧИНА ОШИБОК (шанс на дополнительный ход)
    # ========================================================================

    def kris_error_chance_limits():
        """(начальный шанс, максимальный шанс, прибавка за ход)."""
        level = kris_passive_level()
        start = KRIS_ERROR_START_PER_LEVEL * level
        maximum = KRIS_ERROR_MAX_PER_LEVEL * level
        step = KRIS_ERROR_STEP_BASE + KRIS_ERROR_STEP_PER_LEVEL * level
        return start, maximum, step

    def kris_reset_error_chance():
        """Возвращает накопленный шанс к начальному значению."""
        start, _maximum, _step = kris_error_chance_limits()
        store.kris_error_chance = start
        store.kris_error_extra_turn_granted = False
        return start

    def kris_error_current_chance():
        """Текущий шанс «Причины ошибок» (с ленивой инициализацией)."""
        start, maximum, _step = kris_error_chance_limits()
        chance = float(getattr(store, "kris_error_chance", start) or 0.0)
        if chance <= 0.0:
            chance = start
        return min(chance, maximum)

    def kris_prepare_action_turn(char=None):
        """«Причина ошибок»: бросок на дополнительный ход после действия Криса.

        Вызывается из лейблов атак и магии Криса. Возвращает True, если Крис
        получил право сходить ещё раз. При успехе шанс падает до начального,
        при неудаче — растёт на «прибавку за ход» до максимума.
        """
        kris = kris_char() if char is None else char
        if not kris_is_char(kris):
            return False

        start, maximum, step = kris_error_chance_limits()
        chance = kris_error_current_chance()
        got_extra = renpy.random.random() < chance

        if got_extra:
            store.kris_error_chance = start
            store.kris_error_extra_turn_granted = True
            kris.turn = 1
            renpy.log("[Крис][Причина ошибок] DESTROY THE RULES OF REALITY: "
                      "шанс {:.2%} -> дополнительный ход".format(chance))
        else:
            store.kris_error_chance = min(maximum, chance + step)
            store.kris_error_extra_turn_granted = False
            kris.turn = 0

        return got_extra

    def kris_apply_action_turn_for_current():
        """«Причина ошибок» для общих лейблов (защита, ACT, предмет)."""
        if getattr(store, "current_attacker", None) != 1:
            return False
        return kris_prepare_action_turn()

    # ========================================================================
    # DECAYING (−1 max HP за смерть, вне слотов сохранения)
    # ========================================================================

    def kris_decaying_deaths():
        return max(0, int(getattr(persistent, "kris_decaying_deaths", 0) or 0))

    def kris_decaying_penalty():
        """На сколько урезано максимальное HP Криса."""
        return kris_decaying_deaths() * KRIS_DECAYING_HP_PER_DEATH

    def kris_decaying_register_death():
        """Вызывается из лейбла game_over: тело Криса портится ещё сильнее.

        Один game over = одно списание, поэтому вызов идемпотентен.
        """
        if bool(getattr(store, "kris_decaying_registered", False)):
            return kris_decaying_deaths()
        store.kris_decaying_registered = True

        persistent.kris_decaying_deaths = kris_decaying_deaths() + 1
        penalty = kris_decaying_penalty()
        renpy.log("[Крис][DECAYING] смертей: {}, штраф к max HP: -{}".format(
            kris_decaying_deaths(), penalty))

        # Если Крис уже в команде — сразу подрезаем и текущее HP.
        kris = kris_char()
        if kris is not None and getattr(kris, "current_hp", 0) > getattr(kris, "max_hp", 0):
            kris.current_hp = kris.max_hp

        return kris_decaying_deaths()

    def kris_decaying_reset():
        """Полный сброс DECAYING (удаление всех слотов / новая игра)."""
        persistent.kris_decaying_deaths = 0
        store.kris_decaying_registered = False
        renpy.log("[Крис][DECAYING] штраф сброшен")
        return 0

    # ========================================================================
    # ПРИВЫКШИЙ К ОБЩАЖНОЙ ЖИЗНИ (вредная еда)
    # ========================================================================

    def kris_register_junk_food(char, item_id):
        """Помечает, что Крис наелся вредной еды (эффект — в конце хода)."""
        if item_id not in KRIS_JUNK_FOOD_ITEMS:
            return False

        kris = kris_char()
        if kris is None:
            return False

        teamwide = (
            hasattr(store, "consumable_has_all_picked_effects")
            and store.consumable_has_all_picked_effects(item_id)
        )
        eaters = kris_is_char(char)
        if not eaters and teamwide and getattr(kris, "picked", 0) == 1:
            # Командное угощение: Крис ест вместе со всеми.
            eaters = True
        if not eaters:
            return False

        store.kris_junk_food_pending = int(getattr(store, "kris_junk_food_pending", 0) or 0) + 1
        return True

    def kris_apply_junk_food_end_of_turn():
        """Конец хода Криса: −2 кровотечение и +1 комфорт за вредную еду."""
        pending = int(getattr(store, "kris_junk_food_pending", 0) or 0)
        if pending <= 0:
            return 0
        store.kris_junk_food_pending = 0

        kris = kris_char()
        if kris is None:
            return 0

        kris.bloodshed_debuff = getattr(kris, "bloodshed_debuff", 0) - KRIS_JUNK_FOOD_BLEED * pending
        kris.bonus_comfort = getattr(kris, "bonus_comfort", 0) + KRIS_JUNK_FOOD_COMFORT * pending
        renpy.log("[Крис][Общажная жизнь] вредная еда x{}: кровотечение {}, комфорт {}".format(
            pending, kris.bloodshed_debuff, kris.bonus_comfort))
        return pending

    # ========================================================================
    # СЛЕДЫ НА МЕЧЕ (вечные бонусы за добитых)
    # ========================================================================

    def kris_sword_marks_count():
        return max(0, int(getattr(persistent, "kris_sword_marks", 0) or 0))

    def kris_sword_marks_atk_bonus():
        """Доля базовой атаки от «Следов на мече»."""
        return kris_sword_marks_count() * KRIS_SWORD_MARK_ATK

    def kris_sword_marks_crit_bonus():
        """Прибавка к крит. урону от «Следов на мече»."""
        return kris_sword_marks_count() * KRIS_SWORD_MARK_CRIT_DMG

    def kris_register_sword_mark(victim):
        """Враг добит Крисом: навсегда +0.25% крит.урона и +0.15% атаки."""
        if victim is None or getattr(victim, "name", None) is None:
            return False
        if getattr(victim, "current_hp", 1) > 0:
            return False
        if getattr(victim, "kris_sword_mark_registered", False):
            return False

        victim.kris_sword_mark_registered = True
        persistent.kris_sword_marks = kris_sword_marks_count() + 1
        renpy.log("[Крис][Следы на мече] добит {}: следов всего {}, атака +{:.2%}, крит.урон +{:.2%}".format(
            getattr(victim, "name", "?"), kris_sword_marks_count(),
            kris_sword_marks_atk_bonus(), kris_sword_marks_crit_bonus()))
        return True

    def kris_register_kill_from_attack(attacker_name, target_name):
        """Хук из add_attack_result: отметка «Следов на мече» при добивании."""
        if attacker_name != "Крис":
            return False
        victim = (getattr(store, "enemies", {}) or {}).get(target_name)
        if victim is None:
            victim = (getattr(store, "pers_dict", {}) or {}).get(target_name)
        return kris_register_sword_mark(victim)

    # ========================================================================
    # ВМЯТИНЫ НА ЩИТЕ (+2% бонусной защиты за удар в стойке со щитом)
    # ========================================================================

    def kris_add_shield_dent(char=None):
        """Считает удар, полученный Крисом в стойке со щитом."""
        kris = kris_char() if char is None else char
        if not kris_is_char(kris):
            return False
        if int(getattr(store, "summoned", 0) or 0) != 2:
            return False

        dents = int(getattr(store, "kris_shield_dents", 0) or 0)
        if dents == 0:
            # Запоминаем bonus_def до первой вмятины — его вернём в начале
            # следующего боя (см. kris_reset_battle_passives).
            store.kris_shield_dents_baseline = float(getattr(kris, "bonus_def", 1.0))

        store.kris_shield_dents = dents + 1
        kris.bonus_def = float(getattr(kris, "bonus_def", 1.0)) + KRIS_SHIELD_DENT_BONUS
        renpy.log("[Крис][Вмятины на щите] удар x{}: bonus_def = {:.3f}".format(
            store.kris_shield_dents, kris.bonus_def))
        return True

    # ========================================================================
    # ЖЕЛАНИЕ ЖИТЬ (1 раз за бой 20% HP при падении до 0)
    # ========================================================================

    def kris_try_wish_to_live(char=None):
        """Поднимает Криса на 20% HP, если он упал до 0. Один раз за бой."""
        kris = kris_char() if char is None else char
        if not kris_is_char(kris):
            return False
        if getattr(kris, "current_hp", 1) > 0:
            return False
        if bool(getattr(store, "kris_wish_to_live_used", False)):
            return False

        heal = max(1, int(getattr(kris, "max_hp", 0) * KRIS_WISH_TO_LIVE_HEAL))
        kris.current_hp = heal
        store.kris_wish_to_live_used = True

        if "clear_swoon_pending_for_visual" in globals():
            store.clear_swoon_pending_for_visual(kris)
        kris.damage_gain_for_vis = -heal

        renpy.log("[Крис][Желание жить] сработало: восстановлено {} HP (-{:.0%})".format(
            heal, KRIS_WISH_TO_LIVE_HEAL))
        return True

    def kris_passive_on_hero_damage(victim, old_hp=None):
        """Общий хук: вызывается после нанесения урона герою.

        Обрабатывает «Вмятины на щите» и «Желание жить».
        """
        if not kris_is_char(victim):
            return False
        took_damage = old_hp is None or getattr(victim, "current_hp", 0) < old_hp
        if took_damage:
            kris_add_shield_dent(victim)
        return kris_try_wish_to_live(victim)

    # ========================================================================
    # СПОСОБНОСТИ ВОЗВРАЩАЮТСЯ (стоимость призыва от уровня)
    # ========================================================================

    def kris_ability_cost_multiplier(ability_id):
        """Множитель стоимости способности с учётом уровня.

        «Способности возвращаются» ур.2: «Призвать меч» и «Призвать щит»
        стоят вдвое меньше маны.
        """
        if ability_id in KRIS_SUMMON_ABILITIES and kris_passive_level() >= KRIS_SUMMON_COST_LEVEL:
            return KRIS_SUMMON_COST_MULTIPLIER
        return 1.0

    # ========================================================================
    # УЧЁТ ДЕЙСТВИЙ (actions_count)
    # ========================================================================

    def ability_menu_of(ability_name):
        """К какому меню относится способность: "attack", "magic" или None."""
        for _ability in getattr(store, "BATTLE_ABILITY_DEFINITIONS", []) or []:
            if _ability.get("name") == ability_name:
                return _ability.get("menu")
        return None

    def register_action_for_current(action_id=None):
        """Учёт действия в универсальном лейбле (Heroperformsturn).

        Обычное действие увеличивает actions_count персонажа на 1, магия
        обнуляет счётчик. Значение до обнуления сохраняется в
        actions_count_snapshot — его читает «Слабое место».
        """
        _names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск",
                  5: "Иззи", 6: "Кловер", 7: "Седрик", 8: "Арчи",
                  9: "Сильвия", 10: "Фабри", 11: "Эмили", 12: "Сьюзи",
                  13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
        actor = (getattr(store, "pers_dict", {}) or {}).get(
            _names.get(getattr(store, "current_attacker", None)))
        if actor is None:
            return 0

        if action_id is None:
            action_id = getattr(store, "attackindex", None)

        if ability_menu_of(action_id) == "magic":
            store.actions_count_snapshot = int(getattr(actor, "actions_count", 0) or 0)
            actor.actions_count = 0
        else:
            actor.actions_count = int(getattr(actor, "actions_count", 0) or 0) + 1
        return actor.actions_count

    def kris_actions_required(ability_name, base_required):
        """Сколько действий нужно накопить для способности.

        «Гибкое терпение» ур.8 разрешает «Слабое место» уже после 1 действия.
        """
        if ability_name == "Слабое место" and kris_passive_level() >= KRIS_FLEXIBLE_PATIENCE_LEVEL:
            return 1
        return int(base_required)

    # ========================================================================
    # ПРАВИЛЬНЫЙ УГОЛ (бафф, уворот и щит при защите)
    # ========================================================================

    def kris_grant_right_angle(char=None):
        """Даёт Крису бафф «Правильный угол» x1."""
        kris = kris_char() if char is None else char
        if not kris_is_char(kris):
            return 0
        kris.right_angle_charges = int(getattr(kris, "right_angle_charges", 0) or 0) + 1
        renpy.log("[Крис][Правильный угол] зарядов: {}".format(kris.right_angle_charges))
        return kris.right_angle_charges

    def kris_try_right_angle_dodge(char):
        """Проверка баффа «Правильный угол» в момент получения урона.

        Возвращает True, если урон нужно полностью проигнорировать. Заряд
        тратится на первой же атаке по персонажу (следующий уворот).
        """
        if char is None or int(getattr(char, "right_angle_charges", 0) or 0) <= 0:
            return False
        char.right_angle_charges = int(getattr(char, "right_angle_charges", 0)) - 1
        dodged = renpy.random.random() < KRIS_RIGHT_ANGLE_DODGE_CHANCE
        if dodged:
            char.damage_gain_for_vis = 0
        renpy.log("[Крис][Правильный угол] уворот: {}".format(dodged))
        return dodged

    def kris_on_defend_action():
        """«Правильный угол» ур.5: 10% шанс получить 1 щит при «защищаться»."""
        if getattr(store, "current_attacker", None) != 1:
            return False
        kris = kris_char()
        if not kris_is_char(kris) or kris_passive_level() < KRIS_DEFEND_SHIELD_LEVEL:
            return False
        if renpy.random.random() >= KRIS_DEFEND_SHIELD_CHANCE:
            return False
        kris.shield = int(getattr(kris, "shield", 0) or 0) + 1
        renpy.log("[Крис][Правильный угол] защита дала щит: {}".format(kris.shield))
        return True

    # ========================================================================
    # VESSEL CONTROL: подбор автоатаки при срыве управления
    # ========================================================================

    def kris_attack_ability(ability_name):
        """Определение атаки из боевого реестра по названию."""
        for _ability in getattr(store, "BATTLE_ABILITY_DEFINITIONS", []) or []:
            if _ability.get("name") == ability_name:
                return _ability
        return None

    def get_kris_failed_attack_index():
        """Атака для срыва управления: первая доступная из очереди.

        Очередь KRIS_ATTACK_QUEUE содержит все атаки Криса от самой сильной
        к самой слабой. Недоступные пропускаются: не то оружие (store.summoned),
        низкий уровень или перезарядка. Проверка идёт через боевой реестр,
        поэтому правила совпадают с меню способностей.
        """
        for name in KRIS_ATTACK_QUEUE:
            ability = kris_attack_ability(name)
            if ability is None:
                # Способности нет в реестре — ориентируемся только на перезарядку.
                if get_battle_ability_current_cd(name) <= 0:
                    return name
                continue
            if battle_ability_condition_is_met(ability):
                return name

        # Очередь заканчивается «Ударом неудачника», сюда попадаем только
        # если он тоже почему-то недоступен.
        renpy.log("[Крис][VESSEL CONTROL] ни одна атака не доступна, фолбэк")
        return "Удар неудачника"

    def kris_failed_control_attack():
        """Атака при срыве управления: сразу ставит свою перезарядку."""
        name = get_kris_failed_attack_index()
        if name != "Удар неудачника":
            start_battle_ability_cooldown(name)
        return name
