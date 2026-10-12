# ============================================================================
# ПАССИВНЫЕ СПОСОБНОСТИ КЛОВЕРА
# ----------------------------------------------------------------------------
# Здесь собрана вся логика пассивок Кловера, чтобы точки вызова в бою были
# однострочными, а формулы жили в одном месте.
#
#   Ковбой ур.1                  — патроны и урон зависят от калибра
#   Зоркий Глаз - Зоркий ум ур.1 — соц. характеристики от боевых
#   Делу - время, потехе - час ур.1 — дебафф «игроман», обязан играть
#   Расследование дела ур.1      — шкала виновного, суд, тюрьма
#   Поправка на ветер ур.1       — исполнение атак +20% к максимуму, +2*ур
#   Всем в салуне за мой счёт! ур.1 — напиток команде, падение ничком
#   Инструктор по бою ур.2       — +1-2% точности союзнику за выстрел
#   Проценты с казино ур.3       — команда делит 25% от игр
#   Холостой наоборот ур.4       — шанс сэкономить патрон
#   Перестрелка в полдень ур.5   — ответный выстрел на атаку по Кловеру
#   Удачный пристрелочный ур.6   — первый выстрел точнее в 3*ур
#   Рикошет ур.7                 — отскок в 1/2/3 противников
#   Шутки кончились ур.8         — концентрация x5 при первом попадании
#   Внезапная заначка ур.9       — восстановление половины обоймы
#   Смертельная удача ур.10      — двойная удача
#
#   Улучшения активок:
#   Ловкие пальчики ур.2         — «Навскидку» +1 выстрел
#   Правильное перевоспитание ур.4 — после отсидки 2 безразличия, 2 слабости
#   Ставка на удачу ур.4         — выигрыш 3 удачи, проигрыш 4 сглаза
#   Допрос с пристрастием ур.6   — преимущество по метке розыска
#   Лучше живым, чем мёртвым ур.8 — пощада 100% при метке охотника
# ============================================================================

# --- Состояние боя (сбрасывается в fightbegin12) -----------------------------
default clover_caliber = "medium"
default clover_ammo = 6
default clover_ammo_max = 6
default clover_gambler_debuff = True
default clover_investigation = {}
default clover_concentration_hits = 0
default clover_wanted_targets = {}
default clover_luck_charges = 0
default clover_evil_eye_charges = 0
default clover_instructor_bonus = 0.0
default clover_saloon_pending = False
default clover_saloon_prone = 0
default clover_saloon_drink = None
default clover_waffle_turns = 0
default clover_duel_pending = False
default clover_fate_mark = None
default clover_fate_turns = 0
default clover_dual_wield = False
default clover_first_shot_done = False
# «Зоркий Глаз - Зоркий ум»: последние начисленные соц. бонусы (идемпотентность).
default clover_sharp_eye_applied = (0, 0, 0)
# Одноразовые флаги эффектов активок.
default clover_shotgun_exploded = False
default clover_winchester_exploded = False
default clover_wildwest_shots = 0
default clover_wildwest_damage = 0
default clover_result = None

# --- Состояние вне слотов сохранения (persistent) ----------------------------
default persistent.clover_casino_earnings = 0
default persistent.clover_prison_breaks = 0

# Состояние заключения целей: имя -> {"turns": int, "ally": bool}
default clover_prison = {}
# Метка охотника: имя -> кол-во ходов
default clover_hunter_mark = {}


init python:
    # ========================================================================
    # КОНСТАНТЫ ПАССИВОК
    # ========================================================================

    # «Ковбой» ур.1 — таблица калибров: множитель урона и размер обоймы.
    CLOVER_CALIBER_DATA = {
        "small":  {"damage": 0.75, "ammo": 8, "name": "малый"},
        "medium": {"damage": 1.00, "ammo": 6, "name": "средний"},
        "large":  {"damage": 1.35, "ammo": 4, "name": "большой"},
    }

    # «Зоркий Глаз - Зоркий ум» ур.1: за каждые 40% боевой характеристики +1 соц.
    CLOVER_SHARP_EYE_LEVEL = 1
    CLOVER_SHARP_EYE_STEP = 0.40

    # «Расследование дела» ур.1: прирост шкалы виновного.
    CLOVER_CRIME_DAMAGE = 10
    CLOVER_CRIME_DEBUFF = 12
    CLOVER_CRIME_STAT_LOSS = 9
    CLOVER_CRIME_KILL = 100
    CLOVER_PRISON_PER_CRIME = 1
    CLOVER_PRISON_PER_KILL = 2
    CLOVER_BAIL_PER_TURN = 2

    # «Поправка на ветер» ур.1.
    CLOVER_WIND_MAX_BONUS = 0.20
    CLOVER_WIND_BONUS_PER_LEVEL = 2

    # «Всем в салуне за мой счёт!» ур.1
    CLOVER_SALOON_ACCURACY = -0.10
    CLOVER_SALOON_CRITRATE = 0.08
    CLOVER_SALOON_CRIT = 0.15
    CLOVER_SALOON_PRONE_TURNS = 1

    # «Инструктор по бою» ур.2
    CLOVER_INSTRUCTOR_LEVEL = 2
    CLOVER_INSTRUCTOR_MIN = 0.01
    CLOVER_INSTRUCTOR_MAX = 0.02

    # «Проценты с казино» ур.3
    CLOVER_CASINO_LEVEL = 3
    CLOVER_CASINO_SHARE = 0.25

    # «Холостой наоборот» ур.4
    CLOVER_BLANK_LEVEL = 4
    CLOVER_BLANK_BASE = 0.03
    CLOVER_BLANK_PER_LEVEL = 1.0 / 3.0

    # «Перестрелка в полдень» ур.5
    CLOVER_NOON_LEVEL = 5
    CLOVER_NOON_CHANCE = 0.18

    # «Удачный пристрелочный» ур.6
    CLOVER_SIGHTING_LEVEL = 6
    CLOVER_SIGHTING_PER_LEVEL = 3.0

    # «Рикошет» ур.7
    CLOVER_RICOCHET_LEVEL = 7
    CLOVER_RICOCHET_CHANCES = (0.28, 0.20, 0.12)

    # «Шутки кончились» ур.8
    CLOVER_JOKES_OVER_LEVEL = 8
    CLOVER_CONCENTRATION_MULT = 5

    # «Внезапная заначка» ур.9
    CLOVER_STASH_LEVEL = 9
    CLOVER_STASH_BASE = 0.10
    CLOVER_STASH_PER_LUCK = 3

    # «Смертельная удача» ур.10
    CLOVER_DEADLY_LUCK_LEVEL = 10

    # --- Улучшения активок -------------------------------------------------
    CLOVER_QUICK_FINGERS_LEVEL = 2          # «Ловкие пальчики»
    CLOVER_REEDUCATION_LEVEL = 4            # «Правильное перевоспитание»
    CLOVER_REEDUCATION_APATHY = 2
    CLOVER_REEDUCATION_WEAKNESS = 2

    CLOVER_LUCK_BET_LEVEL = 4               # «Ставка на удачу»
    CLOVER_LUCK_BET_WIN = 3
    CLOVER_LUCK_BET_LOSE = 4

    CLOVER_INTERROGATION_LEVEL = 6          # «Допрос с пристрастием»
    CLOVER_ALIVE_LEVEL = 8                  # «Лучше живым, чем мёртвым»

    # Игры «Сыграем!» и их максимальные ставки (доля характеристики).
    CLOVER_GAME_STAKES = {
        "Покер": 0.25,
        "Слоты": 0.21,          # до 7 монет по 3%
        "Русская рулетка": 1.0,
        "Рулетка": 0.12,
        "Дайсы": 0.20,
        "КНБ": 0.40,
    }

    # ========================================================================
    # ОБЩИЕ ХЕЛПЕРЫ
    # ========================================================================

    def clover_char():
        """Объект Кловера из команды, либо None."""
        return (getattr(store, "pers_dict", {}) or {}).get("Кловер")

    def clover_level():
        """Уровень Кловера (для проверки открытия способностей)."""
        char = clover_char()
        return max(1, int(getattr(char, "level", 1) or 1)) if char else 1

    def clover_is_char(char):
        return char is not None and getattr(char, "name", None) == "Кловер"

    def clover_reset_battle_passives():
        """Сброс боевых пассивок Кловера в начале боя (fightbegin12)."""
        char = clover_char()
        if char is not None:
            # Снимаем бонусы, накопленные «Всем в салуне» и «Инструктором».
            char.bonus_dmgchance = max(
                0.0, float(getattr(char, "bonus_dmgchance", 0.0)) - float(getattr(store, "clover_instructor_bonus", 0.0) or 0.0)
            )
        store.clover_instructor_bonus = 0.0
        store.clover_reset_caliber_ammo()
        store.clover_gambler_debuff = True
        store.clover_investigation = {}
        store.clover_concentration_hits = 0
        store.clover_wanted_targets = {}
        store.clover_luck_charges = 0
        store.clover_evil_eye_charges = 0
        store.clover_saloon_pending = False
        store.clover_saloon_prone = 0
        store.clover_waffle_turns = 0
        store.clover_duel_pending = False
        store.clover_fate_mark = None
        store.clover_fate_turns = 0
        store.clover_dual_wield = False
        store.clover_first_shot_done = False
        store.clover_prison = {}
        store.clover_hunter_mark = {}
        return True

    def clover_reset_caliber_ammo():
        """Приводит обойму в соответствие текущему калибру."""
        data = CLOVER_CALIBER_DATA.get(getattr(store, "clover_caliber", "medium"), CLOVER_CALIBER_DATA["medium"])
        store.clover_ammo_max = data["ammo"]
        store.clover_ammo = data["ammo"]
        return data["ammo"]

    # ========================================================================
    # КОВБОЙ (калибр, патроны, урон)
    # ========================================================================

    def clover_caliber_data(caliber=None):
        key = caliber if caliber is not None else getattr(store, "clover_caliber", "medium")
        return CLOVER_CALIBER_DATA.get(key, CLOVER_CALIBER_DATA["medium"])

    def clover_set_caliber(caliber):
        """«Выбор калибра» ур.1: смена типа патронов с перезарядкой обоймы."""
        if caliber not in CLOVER_CALIBER_DATA:
            return False
        store.clover_caliber = caliber
        store.clover_reset_caliber_ammo()
        renpy.log("[Кловер][Ковбой] калибр: {} (урон x{}, патронов {})".format(
            caliber, clover_caliber_data()["damage"], store.clover_ammo_max))
        return True

    def clover_ammo_count():
        return max(0, int(getattr(store, "clover_ammo", 0) or 0))

    def clover_shot_damage_multiplier():
        """Множитель урона от калибра."""
        return clover_caliber_data()["damage"]

    def clover_shot_cost(count=1):
        """Списывает патроны. Возвращает, сколько реально потрачено."""
        available = clover_ammo_count()
        spent = min(available, max(0, int(count)))
        store.clover_ammo = available - spent
        return spent

    def clover_has_ammo(count=1):
        return clover_ammo_count() >= max(0, int(count))

    def clover_shot_bonus_perform():
        """«Поправка на ветер» ур.1: постоянный бонус исполнения 2*ур."""
        return CLOVER_WIND_BONUS_PER_LEVEL * clover_level() / 100.0

    def clover_max_perform_bonus():
        """«Поправка на ветер»: максимум исполнения выше на 20%."""
        return CLOVER_WIND_MAX_BONUS

    # ========================================================================
    # ЗОРКИЙ ГЛАЗ - ЗОРКИЙ УМ (соц. характеристики от боевых)
    # ========================================================================

    def clover_sharp_eye_bonus():
        """Возвращает (к восприятию, к риторике, к власти)."""
        if clover_level() < CLOVER_SHARP_EYE_LEVEL:
            return (0, 0, 0)
        char = clover_char()
        if char is None:
            return (0, 0, 0)
        step = CLOVER_SHARP_EYE_STEP
        perception = int(float(getattr(char, "dmgchance", 0)) / step)
        rhetoric = int(float(getattr(char, "critrate", 0)) / step)
        power = int(float(getattr(char, "crit", 1.0) - 1.0) / step)
        return (perception, rhetoric, max(0, power))

    def clover_apply_sharp_eye():
        """Начисляет соц. бонус «Зоркого глаза» (идемпотентно)."""
        if clover_level() < CLOVER_SHARP_EYE_LEVEL:
            return False
        char = clover_char()
        if char is None:
            return False
        perception, rhetoric, power = clover_sharp_eye_bonus()
        applied = getattr(store, "clover_sharp_eye_applied", None)
        current = (perception, rhetoric, power)
        if applied == current:
            return False
        # Снимаем прошлый бонус, ставим новый — не трогаем другие источники.
        prev = applied or (0, 0, 0)
        char.bonus_perception = float(getattr(char, "bonus_perception", 0)) - prev[0] + perception
        char.bonus_rhetoric = float(getattr(char, "bonus_rhetoric", 0)) - prev[1] + rhetoric
        char.bonus_power = float(getattr(char, "bonus_power", 0)) - prev[2] + power
        store.clover_sharp_eye_applied = current
        return True

    # ========================================================================
    # ДЕЛУ - ВРЕМЯ, ПОТЕХЕ - ЧАС (дебафф «игроман»)
    # ========================================================================

    def clover_has_gambler_debuff():
        return bool(getattr(store, "clover_gambler_debuff", True))

    def clover_clear_gambler_debuff():
        """Игра сыграна — дебафф снят до следующего хода."""
        store.clover_gambler_debuff = False
        return True

    def clover_apply_gambler_debuff():
        """Проверка в начале хода: без игры висит дебафф «игроман»."""
        return clover_has_gambler_debuff()

    # ========================================================================
    # РАССЛЕДОВАНИЕ ДЕЛА (шкала виновного, тюрьма)
    # ========================================================================

    def clover_investigation_entry(name):
        crimes = getattr(store, "clover_investigation", {}) or {}
        return crimes.get(name, {"progress": 0, "prison": 0, "crimes": []})

    def clover_wanted_targets():
        return getattr(store, "clover_wanted_targets", {}) or {}

    def clover_record_crime(target, crime, amount=None):
        """Начисляет преступление цели. Возвращает запись цели."""
        if target is None:
            return None
        key = getattr(target, "name", None) or str(target)

        # «Метка разыскиваемого»: под меткой шкала виновного не заполняется.
        if key in clover_wanted_targets():
            return clover_investigation_entry(key)

        if amount is None:
            amount = {
                "damage": CLOVER_CRIME_DAMAGE,
                "debuff": CLOVER_CRIME_DEBUFF,
                "stat": CLOVER_CRIME_STAT_LOSS,
                "kill": CLOVER_CRIME_KILL,
            }.get(crime, CLOVER_CRIME_DAMAGE)

        crimes = dict(getattr(store, "clover_investigation", {}) or {})
        entry = dict(crimes.get(key, {"progress": 0, "prison": 0, "crimes": []}))
        entry["progress"] = min(100, int(entry.get("progress", 0)) + int(amount))
        entry["crimes"] = list(entry.get("crimes", [])) + [crime]

        if crime == "kill":
            entry["prison"] = int(entry.get("prison", 0)) + CLOVER_PRISON_PER_KILL
        else:
            entry["prison"] = int(entry.get("prison", 0)) + CLOVER_PRISON_PER_CRIME

        crimes[key] = entry
        store.clover_investigation = crimes
        renpy.log("[Кловер][Расследование] {} — {}: виновность {}/100, тюрьмы {}".format(
            key, crime, entry["progress"], entry["prison"]))
        return entry

    def clover_on_damage(target, damage=0, debuff=False, killed=False, stat_loss=False):
        """Единая точка учёта преступлений (урон/дебафф/штраф/убийство)."""
        if target is None:
            return None
        if killed:
            return clover_record_crime(target, "kill")
        if debuff:
            return clover_record_crime(target, "debuff")
        if stat_loss:
            return clover_record_crime(target, "stat")
        return clover_record_crime(target, "damage")

    def clover_is_wanted(target):
        key = getattr(target, "name", None) or str(target)
        return key in clover_wanted_targets()

    def clover_mark_wanted(target):
        """«Метка разыскиваемого»: цель под меткой розыска."""
        if target is None:
            return False
        key = getattr(target, "name", None) or str(target)
        marks = dict(clover_wanted_targets())
        marks[key] = True
        store.clover_wanted_targets = marks
        # Метка снимает уже накопленную виновность.
        crimes = dict(getattr(store, "clover_investigation", {}) or {})
        if key in crimes:
            crimes.pop(key)
            store.clover_investigation = crimes
        return True

    def clover_send_to_prison(target, turns=None, ally=False):
        """Помещает цель за решётку на указанное число ходов."""
        if target is None:
            return False
        key = getattr(target, "name", None) or str(target)
        if turns is None:
            entry = clover_investigation_entry(key)
            turns = max(1, int(entry.get("prison", 1)))
        turns = max(1, int(turns))
        prison = dict(getattr(store, "clover_prison", {}) or {})
        prison[key] = {"turns": turns, "ally": bool(ally)}
        store.clover_prison = prison

        # За решёткой цель лежит ничком, танк обнуляется: в «Суде» указано,
        # что узник не должен перетягивать на себя атаки (танк = 0).
        target.prone_debuff = max(int(getattr(target, "prone_debuff", 0) or 0), turns)
        target.tank_debuff = int(getattr(target, "tank_debuff", 0) or 0) - 20
        renpy.log("[Кловер][Расследование] {} за решёткой на {} ход(ов)".format(key, turns))
        return True

    def clover_prison_entry(target):
        key = getattr(target, "name", None) or str(target)
        return (getattr(store, "clover_prison", {}) or {}).get(key)

    def clover_is_in_prison(target):
        return clover_prison_entry(target) is not None

    def clover_prison_bail_cost(target):
        """«Помиловать»: залог = 2 * число оставшихся ходов."""
        entry = clover_prison_entry(target)
        if entry is None:
            return 0
        return CLOVER_BAIL_PER_TURN * max(1, int(entry.get("turns", 1)))

    def clover_free_from_prison(target):
        """Освобождает цель из тюрьмы. Возвращает True при успехе."""
        if target is None:
            return False
        key = getattr(target, "name", None) or str(target)
        prison = dict(getattr(store, "clover_prison", {}) or {})
        entry = prison.pop(key, None)
        if entry is None:
            return False
        store.clover_prison = prison
        target.prone_debuff = 0
        target.tank_debuff = int(getattr(target, "tank_debuff", 0) or 0) + 20
        store.clover_apply_reeducation(target, entry)
        return True

    def clover_apply_reeducation(target, entry=None):
        """«Правильное перевоспитание» ур.4: после полной отсидки — стаки.

        В проекте «безразличие» — это critdmg_debuff (см. 1_ДЕБАФЫ_СИСТЕМА.rpy,
        п.8 «безразличие/злость»), «слабость» — magic_debuff (п.5).
        """
        if clover_level() < CLOVER_REEDUCATION_LEVEL or target is None:
            return False
        if entry is not None and int(entry.get("turns", 0)) > 0:
            return False
        target.critdmg_debuff = int(getattr(target, "critdmg_debuff", 0) or 0) + CLOVER_REEDUCATION_APATHY
        target.magic_debuff = int(getattr(target, "magic_debuff", 0) or 0) + CLOVER_REEDUCATION_WEAKNESS
        renpy.log("[Кловер][Перевоспитание] {}: безразличие +{}, слабость +{}".format(
            getattr(target, "name", "?"), CLOVER_REEDUCATION_APATHY, CLOVER_REEDUCATION_WEAKNESS))
        return True

    def clover_try_prison_escape(target):
        """Побег из тюрьмы: дубль на 2 кубиках (противник — 3 кубика)."""
        if target is None:
            return False
        dice_count = 3 if getattr(target, "is_enemy", True) else 2
        rolls = [renpy.random.randint(1, 6) for _ in range(dice_count)]
        if len(set(rolls)) == 1:
            renpy.log("[Кловер][Тюрьма] {} выбросил дубль {} и вышел".format(
                getattr(target, "name", "?"), rolls))
            return clover_free_from_prison(target)
        return False

    def clover_tick_prison():
        """Конец хода: уменьшает сроки и снимает отсидку."""
        prison = dict(getattr(store, "clover_prison", {}) or {})
        if not prison:
            return 0
        released = 0
        for key in list(prison.keys()):
            entry = dict(prison[key])
            entry["turns"] = int(entry.get("turns", 1)) - 1
            target = (getattr(store, "pers_dict", {}) or {}).get(key)
            if target is None:
                target = (getattr(store, "enemies", {}) or {}).get(key)
            if entry["turns"] <= 0:
                prison.pop(key, None)
                if target is not None:
                    target.prone_debuff = 0
                    target.tank_debuff = int(getattr(target, "tank_debuff", 0) or 0) + 20
                    store.clover_apply_reeducation(target, entry)
                released += 1
            else:
                prison[key] = entry
                if target is not None:
                    target.prone_debuff = max(int(getattr(target, "prone_debuff", 0) or 0), entry["turns"])
        store.clover_prison = prison
        return released

    def clover_prison_blocks_turn(target):
        """Находясь за решёткой, персонаж не может действовать."""
        return clover_is_in_prison(target)

    # ========================================================================
    # ПЕРЕСТРЕЛКА В ПОЛДЕНЬ (ответный выстрел)
    # ========================================================================

    def clover_noon_available():
        return clover_level() >= CLOVER_NOON_LEVEL

    def clover_on_enemy_attack(attacker=None):
        """Ответный выстрел, когда противник атаковал Кловера.

        Шанс попадания = 18% от текущего шанса попадания Кловера.
        Тратит патрон. Урон учитывает коэффициент калибра.
        """
        char = clover_char()
        if char is None:
            return False
        if clover_level() < CLOVER_NOON_LEVEL:
            return False
        if not clover_has_ammo(1):
            return False

        chance = max(0.0, min(1.0, float(getattr(char, "dmgchance", 0)) * CLOVER_NOON_CHANCE))
        if renpy.random.random() >= chance:
            return False

        clover_shot_cost(1)
        renpy.log("[Кловер][Перестрелка в полдень] ответный выстрел (шанс {:.1%})".format(chance))
        return True

    def clover_noon_damage(target):
        """Урон ответного выстрела с учётом калибра."""
        char = clover_char()
        if char is None or target is None:
            return 0
        base = float(getattr(char, "atk", 0)) * clover_shot_damage_multiplier()
        armor = float(getattr(target, "armor", 0) or 0)
        return max(1, int(base - armor * 0.5))

    # ========================================================================
    # ИНСТРУКТОР ПО БОЮ (+точность союзнику за выстрел)
    # ========================================================================

    def clover_on_shot_fired():
        """Каждый выстрел: +1-2% точности случайному союзнику."""
        if clover_level() < CLOVER_INSTRUCTOR_LEVEL:
            return None
        allies = [
            c for c in (getattr(store, "pers_dict", {}) or {}).values()
            if c is not None and not clover_is_char(c)
            and getattr(c, "picked", 0) == 1 and getattr(c, "current_hp", 0) > 0
        ]
        if not allies:
            return None
        ally = renpy.random.choice(allies)
        bonus = renpy.random.uniform(CLOVER_INSTRUCTOR_MIN, CLOVER_INSTRUCTOR_MAX)
        ally.bonus_dmgchance = float(getattr(ally, "bonus_dmgchance", 0)) + bonus
        store.clover_instructor_bonus = float(getattr(store, "clover_instructor_bonus", 0.0)) + bonus
        renpy.log("[Кловер][Инструктор по бою] {}: точность +{:.1%}".format(
            getattr(ally, "name", "?"), bonus))
        return ally

    # ========================================================================
    # ХОЛОСТОЙ НАОБОРОТ (экономия патрона)
    # ========================================================================

    def clover_blank_chance():
        """Шанс сэкономить патрон: 3% + ур/3 * коэффициент калибра."""
        if clover_level() < CLOVER_BLANK_LEVEL:
            return 0.0
        return CLOVER_BLANK_BASE + (clover_level() / 3.0) * clover_shot_damage_multiplier() * 0.01

    def clover_try_blank_save():
        """Возвращает True, если патрон сэкономлен."""
        chance = clover_blank_chance()
        if chance <= 0.0:
            return False
        return renpy.random.random() < min(1.0, chance)

    # ========================================================================
    # УДАЧНЫЙ ПРИСТРЕЛОЧНЫЙ (первый выстрел точнее)
    # ========================================================================

    def clover_sighting_bonus():
        """Множитель шанса попадания для первого выстрела атаки."""
        if clover_level() < CLOVER_SIGHTING_LEVEL:
            return 1.0
        return 1.0 + CLOVER_SIGHTING_PER_LEVEL * clover_level() / 10.0

    # ========================================================================
    # РИКОШЕТ (отскок в нескольких противников)
    # ========================================================================

    def clover_ricochet_targets(primary=None, max_targets=3):
        """Список противников для рикошета с их шансами."""
        if clover_level() < CLOVER_RICOCHET_LEVEL:
            return []
        char = clover_char()
        if char is None:
            return []
        base_chance = float(getattr(char, "dmgchance", 0))
        candidates = [
            e for e in (getattr(store, "enemies", {}) or {}).values()
            if e is not None and getattr(e, "current_hp", 0) > 0 and e is not primary
        ]
        if not candidates:
            return []
        renpy.random.shuffle(candidates)
        result = []
        for index, enemy in enumerate(candidates[:max_targets]):
            chance = base_chance * CLOVER_RICOCHET_CHANCES[index]
            result.append((enemy, chance))
        return result

    def clover_ricochet_damage(target, ratio=0.5):
        """Урон рикошета — доля от обычного выстрела."""
        char = clover_char()
        if char is None or target is None:
            return 0
        base = float(getattr(char, "atk", 0)) * clover_shot_damage_multiplier() * ratio
        armor = float(getattr(target, "armor", 0) or 0)
        return max(1, int(base - armor * 0.5))

    # ========================================================================
    # ШУТКИ КОНЧИЛСЯ (концентрация при первом попадании)
    # ========================================================================

    def clover_on_damage_received(target=None, **kwargs):
        """Первое попадание по Кловеру даёт бафф концентрация x5.

        В проекте «концентрация» — это отрицательный accuracy_debuff
        (см. 1_ПЕРС_ХАРАКТ.rpy: <0 — концентрация, >0 — страх),
        дающий +5% точности за стак.
        """
        if clover_level() < CLOVER_JOKES_OVER_LEVEL:
            return False
        char = clover_char()
        if char is None:
            return False
        if int(getattr(store, "clover_concentration_hits", 0) or 0) > 0:
            return False
        store.clover_concentration_hits = 1
        char.accuracy_debuff = int(getattr(char, "accuracy_debuff", 0) or 0) - CLOVER_CONCENTRATION_MULT
        renpy.log("[Кловер][Шутки кончились] концентрация x{} (accuracy_debuff = {})".format(
            CLOVER_CONCENTRATION_MULT, char.accuracy_debuff))
        return True

    # ========================================================================
    # ВНЕЗАПНАЯ ЗАНАЧКА (восстановление обоймы)
    # ========================================================================

    def clover_stash_chance():
        """10% + удача*3.

        «Удача» в проекте — отрицательный critrate_debuff, поэтому берём
        модуль накопленной удачи (см. 1_ПЕРС_ХАРАКТ.rpy, п.7).
        """
        char = clover_char()
        luck = 0.0
        if char is not None:
            luck = max(0.0, -float(getattr(char, "critrate_debuff", 0) or 0))
        return CLOVER_STASH_BASE + luck * CLOVER_STASH_PER_LUCK / 100.0

    def clover_ammo_empty_refill():
        """Пустая обойма: шанс восстановить половину патронов."""
        if clover_ammo_count() > 0:
            return False
        if clover_level() < CLOVER_STASH_LEVEL:
            return False
        if renpy.random.random() >= min(1.0, clover_stash_chance()):
            return False
        restore = max(1, int(getattr(store, "clover_ammo_max", 6) / 2))
        store.clover_ammo = restore
        renpy.log("[Кловер][Внезапная заначка] восстановлено {} патронов".format(restore))
        return True

    # ========================================================================
    # СМЕРТЕЛЬНАЯ УДАЧА (двойная удача)
    # ========================================================================

    def clover_apply_luck(amount):
        """Выдаёт удачу; на ур.10 количество удваивается.

        В проекте бафф «удача» — это отрицательный critrate_debuff
        (см. комментарий в 1_ПЕРС_ХАРАКТ.rpy: <0 — удача, >0 — сглаз).
        """
        char = clover_char()
        if char is None:
            return 0
        if clover_level() >= CLOVER_DEADLY_LUCK_LEVEL:
            amount *= 2
        amount = int(amount)
        store.clover_luck_charges = int(getattr(store, "clover_luck_charges", 0) or 0) + amount
        char.critrate_debuff = int(getattr(char, "critrate_debuff", 0) or 0) - amount
        renpy.log("[Кловер][Смертельная удача] удача +{} (critrate_debuff = {})".format(
            amount, char.critrate_debuff))
        return amount

    def clover_apply_evil_eye(amount):
        """Сглаз — положительный critrate_debuff."""
        char = clover_char()
        if char is None:
            return 0
        amount = int(amount)
        store.clover_evil_eye_charges = int(getattr(store, "clover_evil_eye_charges", 0) or 0) + amount
        char.critrate_debuff = int(getattr(char, "critrate_debuff", 0) or 0) + amount
        renpy.log("[Кловер][Ставка на удачу] сглаз +{} (critrate_debuff = {})".format(
            amount, char.critrate_debuff))
        return amount

    # ========================================================================
    # ВСЕМ В САЛУНЕ ЗА МОЙ СЧЁТ! (напиток команде)
    # ========================================================================

    def clover_mark_saloon_drink(drink_id=None):
        """Кловер выпил напиток — в конце хода угощает команду."""
        store.clover_saloon_pending = True
        store.clover_saloon_drink = drink_id
        return True

    def clover_apply_saloon_end_of_turn():
        """Конец хода: эффекты напитка команде и падение Кловера ничком."""
        if not bool(getattr(store, "clover_saloon_pending", False)):
            return False
        char = clover_char()
        if char is None:
            return False
        store.clover_saloon_pending = False

        # Сам Кловер: −10% точности, +8% крит-шанс, +15% крит-урон.
        char.bonus_dmgchance = float(getattr(char, "bonus_dmgchance", 0)) + CLOVER_SALOON_ACCURACY
        char.bonus_critrate = float(getattr(char, "bonus_critrate", 0)) + CLOVER_SALOON_CRITRATE
        char.bonus_crit = float(getattr(char, "bonus_crit", 0)) + CLOVER_SALOON_CRIT

        # Команда: 2 дебаффа радости и вдохновения, аппетит не заполняется.
        # «Радость» — отрицательный def_debuff, «вдохновение» — отрицательный
        # magic_debuff (см. 1_ДЕБАФЫ_СИСТЕМА.rpy, пп. 4-5).
        for ally in (getattr(store, "pers_dict", {}) or {}).values():
            if ally is None or clover_is_char(ally):
                continue
            if getattr(ally, "picked", 0) != 1 or getattr(ally, "current_hp", 0) <= 0:
                continue
            ally.def_debuff = int(getattr(ally, "def_debuff", 0) or 0) - 2
            ally.magic_debuff = int(getattr(ally, "magic_debuff", 0) or 0) - 2

        # После угощения Кловер падает ничком на 1 ход.
        char.prone_debuff = max(int(getattr(char, "prone_debuff", 0) or 0), CLOVER_SALOON_PRONE_TURNS)
        store.clover_saloon_prone = CLOVER_SALOON_PRONE_TURNS
        renpy.log("[Кловер][Салун] команда выпила, Кловер падает ничком")
        return True

    # ========================================================================
    # ПРОЦЕНТЫ С КАЗИНО (доля команды от игр)
    # ========================================================================

    def clover_casino_share(amount):
        """Команда получает 25% от выигрыша/проигрыша в играх «Сыграем!».

        Деньги проекта живут в store.money (см. 1_ПЕРС_ХАРАКТ.rpy: default money).
        """
        if clover_level() < CLOVER_CASINO_LEVEL:
            return 0
        share = int(amount * CLOVER_CASINO_SHARE)
        if share != 0:
            store.money = int(getattr(store, "money", 0) or 0) + share
            persistent.clover_casino_earnings = int(
                getattr(persistent, "clover_casino_earnings", 0) or 0) + share
        return share

    def clover_current_money():
        return int(getattr(store, "money", 0) or 0)

    def clover_add_money(amount):
        store.money = clover_current_money() + int(amount)
        return store.money

    # ========================================================================
    # СТАВКА НА УДАЧУ (улучшение ур.4)
    # ========================================================================

    def clover_apply_bet_result(won):
        """Выигрыш — 3 удачи, проигрыш — 4 сглаза (с ур.4)."""
        if clover_level() < CLOVER_LUCK_BET_LEVEL:
            return 0
        char = clover_char()
        if char is None:
            return 0
        if won:
            store.clover_apply_luck(CLOVER_LUCK_BET_WIN)
            renpy.log("[Кловер][Ставка на удачу] выигрыш: +{} удачи".format(CLOVER_LUCK_BET_WIN))
            return CLOVER_LUCK_BET_WIN
        store.clover_apply_evil_eye(CLOVER_LUCK_BET_LOSE)
        renpy.log("[Кловер][Ставка на удачу] проигрыш: +{} сглаза".format(CLOVER_LUCK_BET_LOSE))
        return -CLOVER_LUCK_BET_LOSE

    # ========================================================================
    # ДОПРОС С ПРИСТРАСТИЕМ / ЛУЧШЕ ЖИВЫМ (улучшения ур.6 и ур.8)
    # ========================================================================

    def clover_interrogation_advantage(target):
        """Ур.6: преимущество на восприятие и власть по цели под меткой."""
        if clover_level() < CLOVER_INTERROGATION_LEVEL or target is None:
            return False
        if not clover_is_wanted(target):
            return False
        entry = clover_investigation_entry(getattr(target, "name", str(target)))
        return len(entry.get("crimes", [])) > 0

    def clover_mercy_on_hunter_mark(target):
        """Ур.8: цель за решёткой под меткой охотника — пощада 100%."""
        if clover_level() < CLOVER_ALIVE_LEVEL or target is None:
            return False
        key = getattr(target, "name", None) or str(target)
        if key not in (getattr(store, "clover_hunter_mark", {}) or {}):
            return False
        if not clover_is_in_prison(target):
            return False
        target.spare_progress = int(getattr(target, "spare_max", 100) or 100)
        renpy.log("[Кловер][Лучше живым] {}: пощада 100%".format(key))
        return True

    def clover_mark_hunter(target):
        """Ставит метку охотника на цель."""
        if target is None:
            return False
        key = getattr(target, "name", None) or str(target)
        marks = dict(getattr(store, "clover_hunter_mark", {}) or {})
        marks[key] = 2
        store.clover_hunter_mark = marks
        return True

    # ========================================================================
    # ВАФЕЛЬНЫЙ ПЕРЕРЫВ (еда на 3 хода)
    # ========================================================================

    def clover_start_waffle():
        store.clover_waffle_turns = 3
        return True

    def clover_tick_waffle():
        """+5% точности и +3% HP каждый ход, пока Кловер ест вафельку."""
        turns = int(getattr(store, "clover_waffle_turns", 0) or 0)
        if turns <= 0:
            return False
        char = clover_char()
        if char is None:
            return False
        char.bonus_dmgchance = float(getattr(char, "bonus_dmgchance", 0)) + 0.05
        heal = max(1, int(getattr(char, "max_hp", 0) * 0.03))
        char.current_hp = min(int(getattr(char, "max_hp", 0)), int(getattr(char, "current_hp", 0)) + heal)
        store.clover_waffle_turns = turns - 1
        return True

    # ========================================================================
    # ВЫЗОВ НА ДУЭЛЬ! (танк до максимума, бонусы на следующий ход)
    # ========================================================================

    def clover_start_duel():
        char = clover_char()
        if char is None:
            return False
        char.bonus_tank = float(getattr(char, "total_tank", 0)) or 0.0
        store.clover_duel_pending = True
        return True

    def clover_apply_duel_bonuses():
        """Следующий ход: +15% попадания, +20% крит-шанса, +40% крит-урона."""
        if not bool(getattr(store, "clover_duel_pending", False)):
            return False
        char = clover_char()
        if char is None:
            return False
        char.bonus_dmgchance = float(getattr(char, "bonus_dmgchance", 0)) + 0.15
        char.bonus_critrate = float(getattr(char, "bonus_critrate", 0)) + 0.20
        char.bonus_crit = float(getattr(char, "bonus_crit", 0)) + 0.40
        store.clover_duel_pending = False
        return True

    # ========================================================================
    # ОТ СУДЬБЫ НЕ УЙДЁШЬ (метка судьбы)
    # ========================================================================

    def clover_mark_fate(target):
        char = clover_char()
        if char is None or target is None:
            return False
        store.clover_fate_mark = getattr(target, "name", None) or str(target)
        store.clover_fate_turns = 2
        return True

    def clover_fate_target():
        name = getattr(store, "clover_fate_mark", None)
        if name is None:
            return None
        return (getattr(store, "enemies", {}) or {}).get(name)

    def clover_fate_miss_chance(target):
        """Шанс нанести урон при промахе: крит-шанс/2 + попадание/3."""
        char = clover_char()
        if char is None:
            return 0.0
        return min(1.0, float(getattr(char, "critrate", 0)) / 2.0 + float(getattr(char, "dmgchance", 0)) / 3.0)

    def clover_fate_hit_bonus():
        """Бонус при попадании без помощи пассивки: 30% крит-шанса и 10% крит-урона Кловера."""
        char = clover_char()
        if char is None:
            return (0.0, 0.0)
        return (float(getattr(char, "critrate", 0)) * 0.30, float(getattr(char, "crit", 1.0)) * 0.10)

    def clover_tick_fate():
        turns = int(getattr(store, "clover_fate_turns", 0) or 0)
        if turns <= 0:
            store.clover_fate_mark = None
            return False
        turns -= 1
        store.clover_fate_turns = turns
        if turns <= 0:
            store.clover_fate_mark = None
        return True

    # ========================================================================
    # ГИПЕРЛУЧ (условие GENO)
    # ========================================================================

    def clover_geno_route_available():
        """Гиперлуч доступен только на руте GENO.

        Рут хранится в store.phone_role_mode[имя] и переключается по ПКМ
        в телефоне (см. 0_ТЕЛЕФОН.rpy, phone_toggle_role_set).
        """
        mode = (getattr(store, "phone_role_mode", {}) or {}).get("Кловер")
        return str(mode).lower() == "geno"

    # ========================================================================
    # ОБРАБОТЧИКИ, ВЫЗЫВАЕМЫЕ ИЗ ОБЩИХ СИСТЕМ
    # ========================================================================

    def clover_on_round_end():
        """Конец хода Кловера: вафелька, салун, тюрьма, дуэль."""
        store.clover_tick_waffle()
        store.clover_apply_saloon_end_of_turn()
        store.clover_tick_prison()
        store.clover_tick_fate()
        store.clover_ammo_empty_refill()
