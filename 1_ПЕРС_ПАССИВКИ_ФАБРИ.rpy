# ============================================================
# ФАБРИ — фамильяры, пассивки, улучшения
# ============================================================
#
# Согласно спецификации (см. `_FABRI_SPEC.md` и
# `000_Для написания способностей.txt`) Фабри — создатель, а не
# разрушитель: у неё НЕТ активных атак. Весь её ход — это призыв
# рукодельных друзей и управление их магией.
#
# АРХИТЕКТУРНОЕ РЕШЕНИЕ ПО ФАМИЛЬЯРАМ
# Фамильяры — НЕ враги в store.enemies и НЕ персонажи в
# store.characters. Если бы они попадали в store.characters, то
# Pers.change_hp() счёл бы «своих» живыми при подсчёте all_dead, а
# цикл вражеской фазы и check_enemy_status начали бы учитывать их
# как обычных бойцов. Поэтому состояние фамильяров живёт прямо в
# полях Фабри (fabri_*), а их HP/атака/защита считаются от УРОВНЯ
# Фабри (Pers.global_level), а не от текущих (возможно, бафнутых)
# значений — иначе «раздутые» баффами характеристики Фабри
# усиливали бы и фамильяров, чего спецификация не требует.
#
# СЛОИ (методичка требует не собирать всё в одном месте):
#   * этот файл       — состояние, формулы, пассивки, улучшения;
#   * 5_ИНТЕРФЕЙС*    — регистрация кнопок, уровни, перезарядки;
#   * 1_ПЕРС_АТАКИ    — диспетчер исполнения (ветки по attackindex);
#   * 1_ПЕРС_АТАКИ_ЛЕЙБЛЫ — лейблы fabri_summon_is_done /
#                       fabri_familiar_magic_is_done, которые лишь
#                       вызывают fabri_perform_* отсюда.
# ============================================================

# Способность, выбранная игроком в текущем ходу Фабри.
# Объявлено через default, чтобы SetVariable в экранах корректно
# находил переменную, и переживало сохранение/загрузку.
default fabri_pending_summon = None

init python:

    # ------------------------------------------------------------
    # 1) КОНСТАНТЫ
    # ------------------------------------------------------------

    # Порог уровня персонажа для каждой пассивки. Хранится рядом с
    # кодом, чтобы не было «пассивки ур.7» только в комментарии.
    FABRI_LVL_CREATOR        = 1   # Созидатель, а не разрушитель
    FABRI_LVL_HANDMADE       = 1   # Рукодельные друзья
    FABRI_LVL_RESPITE        = 1   # Передышка, чтоб вернуться
    FABRI_LVL_VARIETY        = 1   # Разнообразие – лучшее вдохновение
    FABRI_LVL_ENTHUSIASM     = 3   # Энтузиазм и усердие
    FABRI_LVL_HASTY          = 5   # Сотворить наспех
    FABRI_LVL_CREATION_LIVES = 7   # Творчество будет жить...
    FABRI_LVL_JOYFUL         = 9   # Радующее творчество

    # Улучшения способностей фамильяров (отдельно от уровня
    # открытия самой способности — это разные вещи).
    FABRI_UP_HIDE_ALL        = 2   # Всем прятаться!          (Панцырь)
    FABRI_UP_NO_SLOWDOWN     = 3   # Не сбавляя скорости       (Морковка)
    FABRI_UP_OFF_THE_CHAIN   = 4   # Сорваться с цепи          (Манки)
    FABRI_UP_WARMUP_DANCES   = 5   # Разминающие танцы         (Пёрышко)
    FABRI_UP_TOUGHER_PREDATOR= 7   # Выносливее хищника        (Морковка)
    FABRI_UP_HIT_HARDER_TOO  = 8   # Я тоже бей сильнее!       (Манки)
    FABRI_UP_TEMPERING       = 9   # Закаляя панцирь           (Панцырь)
    FABRI_UP_MOTHERHOOD      = 10  # Правильное материнство    (Пёрышко)

    # Сколько фамильяров можно держать одновременно (Рукодельные друзья).
    FABRI_MAX_FAMILIARS = 2

    # Доля хила, которую фамильяры получают вместе с Фабри.
    FABRI_FAMILIAR_SHARE_HEAL = 0.20

    # «Спрятаться»: базовое снижение танка цели и улучшенное.
    FABRI_HIDE_TANK_BASE  = 7
    FABRI_HIDE_TANK_UP    = 3

    # Яйцо М-с Пёрышко: сколько ходов до вылупления и улучшение.
    FABRI_EGG_HATCH_TURNS     = 5
    FABRI_EGG_HATCH_TURNS_UP  = 3

    # «Не поймаешь»: длительность и улучшение.
    FABRI_DODGE_TURNS     = 2
    FABRI_DODGE_TURNS_UP  = 3

    # «Ускориться»: базовый бонус и режим затухания с улучшением.
    FABRI_HASTE_BASE      = 15.0
    FABRI_HASTE_DECAY     = 5.0
    FABRI_HASTE_DECAY_TURNS = 3

    # «Закаляя панцирь»: бонус защиты за каждую цель «Рикошета».
    FABRI_SHELL_TEMPER_PER_TARGET = 10.0

    # «Я тоже бей сильнее!»: доля магии Фабри, идущая в урон Манки.
    FABRI_MONKEY_EXTRA_MAGIC_PERCENT = 0.20

    # «Сорваться с цепи»: бонусы «Неудержимости».
    FABRI_UNCHAINED_ATK_PERCENT  = 5.0
    FABRI_UNCHAINED_CRITDMG_BONUS = 0.20

    # «Радующее творчество»: множитель баффа вдохновения союзникам.
    FABRI_JOYFUL_INSPIRATION_MULT = 3

    # «Энтузиазм и усердие» ур.3: доля макс. MP, возвращаемая при
    # бесплатном призыве (призывы в реестре бесплатны).
    FABRI_FREE_SUMMON_REFUND_PERCENT = 0.10

    # «Рукодельные друзья»: доля магии Фабри, добавляемая к автоатаке
    # М-с Манки (пассивка действует с ур.1).
    FABRI_MONKEY_MAGIC_SHARE = 0.40

    # «Передышка, чтоб вернуться»: прибавка к store.soul_speed за уровень.
    FABRI_RESPITE_PER_LEVEL = 0.20

    # Аура М-с Пёрышко: доля бонуса, которую получает каждый союзник
    # за один стак случайного баффа.
    FABRI_FEATHER_STACK_PERCENT = 0.02

    # «Прикрепиться»: доля урона, которая остаётся персонажу.
    FABRI_ATTACH_TARGET_SHARE = 0.70

    # Аура М-с Морковки: доля лечения HP/MP за ход.
    FABRI_CARROT_HEAL_TARGET_PERCENT = 0.35
    FABRI_CARROT_HEAL_OTHER_PERCENT = 0.45

    # «Разнообразие – лучшее вдохновение»: бонусы в конце раунда.
    FABRI_VARIETY_MAGIC_PERCENT = 10.0
    FABRI_VARIETY_CRIT_PERCENT  = 4.0

    # «Творчество будет жить...»: бонусы при крите.
    FABRI_CREATION_SELF_DMG_PERCENT     = 150.0
    FABRI_CREATION_FAMILIAR_DMG_PERCENT = 20.0

    # Предельный уровень Фабри в таблицах характеристик.
    FABRI_MAX_TABLE_LEVEL = 12

    # Описание каждого фамильяра: id -> (отображаемое имя, доля HP,
    # доля атаки, доля защиты, крит-шанс(%), крит-урон(бонус к 1.0)).
    # Значения взяты построчно из спецификации, раздел
    # «Характеристики Фамильяров».
    FABRI_FAMILIARS = {
        "shell": {
            "name": "М-р Панцырь",
            "hp_percent": 0.60, "atk_percent": 0.30, "def_percent": 0.60,
            "critrate": 1, "crit": 1.05,      # крит.шанс и крит.урон — оч. плохо
            "summon_label": "Призвать М-ра Панцыря",
        },
        "feather": {
            "name": "М-с Пёрышко",
            "hp_percent": 0.40, "atk_percent": 0.20, "def_percent": 0.35,
            "critrate": 60, "crit": 1.10,     # крит.шанс — оч. хорошо, урон — плохо
            "summon_label": "Призвать М-с Пёрышко",
        },
        "carrot": {
            "name": "М-с Морковка",
            "hp_percent": 0.35, "atk_percent": 0.50, "def_percent": 0.40,
            "critrate": 10, "crit": 1.25,     # крит.шанс — плохо, крит.урон — хорошо
            "summon_label": "Призвать М-с Морковку",
        },
        "monkey": {
            "name": "М-с Манки",
            "hp_percent": 0.50, "atk_percent": 0.50, "def_percent": 0.30,
            "critrate": 60, "crit": 1.25,     # крит.шанс и урон — оч. хорошо
            "summon_label": "Призвать М-с Манки",
        },
    }

    # М-р Пёрышко младший (третий фамильяр) — живёт отдельно от
    # очереди и НЕ занимает слот («не мешает очереди создания
    # фамильяров»). Его характеристики заданы долями от М-с Пёрышко.
    FABRI_JUNIOR_ID = "junior"
    FABRI_JUNIOR_NAME = "М-р Пёрышко младший"
    FABRI_JUNIOR_HP_PERCENT = 0.70      # получает на 30% меньше урона
    FABRI_JUNIOR_SOCIAL_CHANCE = 0.50   # шанс +1 соц. характеристики за ход

    # Соответствие «элемент меню призыва» -> id фамильяра.
    FABRI_SUMMON_MAP = {
        "Призвать М-ра Панцыря": "shell",
        "Призвать М-с Пёрышко": "feather",
        "Призвать М-с Морковку": "carrot",
        "Призвать М-с Манки": "monkey",
    }

    # Идентификаторы магии фамильяров: имя способности -> (fid, тег).
    # Нужны, чтобы лейбл один раз делегировал в fabri_perform_familiar_magic.
    FABRI_MAGIC_TAGS = {
        "Спрятаться":            ("shell",   "hide"),
        "Надеть панцирь":        ("shell",   "shell_on"),
        "Прикрепиться":          ("shell",   "attach"),
        "Рикошет черепахи":      ("shell",   "ricochet"),

        "Орлиная зоркость":      ("feather", "eagle_eye"),
        "Небесные танцы":        ("feather", "sky_dance"),
        "Снести яичко":          ("feather", "lay_egg"),
        "Перьевой ураган":       ("feather", "feather_storm"),

        "Ускориться":            ("carrot",  "haste"),
        "Не поймаешь":           ("carrot",  "uncatchable"),
        "Поделиться морковкой":  ("carrot",  "share_carrot"),
        "Быстрее и дальше":      ("carrot",  "faster_further"),

        "Боевой рёв":            ("monkey",  "battle_roar"),
        "Неудержимость":         ("monkey",  "uncontrollable"),
        "Бей сильнее!":          ("monkey",  "hit_harder"),
        "Я покажу, как бить!":   ("monkey",  "show_how"),
    }


    # ------------------------------------------------------------
    # 2) БАЗОВЫЕ ДОСТУПЫ И БЕЗОПАСНОЕ ЧТЕНИЕ
    # ------------------------------------------------------------

    def fabri_level():
        """Уровень персонажа Фабри (глобальный уровень развития).

        Единственная точка чтения уровня: пассивки не читают
        store.Pers.global_level напрямую, чтобы правило «пассивка
        обязана проверять свой уровень» было легко проверить.
        """
        return int(getattr(store.Pers, "global_level", 1) or 1)

    def fabri_char():
        """Объект Фабри из pers_dict, либо None."""
        return (getattr(store, "pers_dict", {}) or {}).get("Фабри")

    def fabri_get(field, default=0):
        """Безопасное чтение поля состояния Фабри.

        Нужно для совместимости со старыми сохранениями: поле может
        отсутствовать до первого запуска новой версии.
        """
        char = fabri_char()
        if char is None:
            return default
        return getattr(char, field, default)

    def fabri_set(field, value):
        """Запись поля состояния Фабри, если персонаж в команде."""
        char = fabri_char()
        if char is not None:
            setattr(char, field, value)

    def fabri_in_battle():
        """True, если Фабри сейчас в выбранной команде и жива."""
        char = fabri_char()
        if char is None:
            return False
        return getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0

    def fabri_party_members():
        """Живые союзники текущей команды (включая саму Фабри).

        Берём только реальные слоты team_manager, а не весь
        store.characters: иначе баффы уходили бы персонажам, которых
        нет в бою.
        """
        result = []
        tm = getattr(store, "team_manager", None)
        slots = getattr(tm, "team_slots", None) or []
        pers = getattr(store, "pers_dict", {}) or {}
        for slot in slots:
            if not slot:
                continue
            char = pers.get(slot)
            if char is None:
                continue
            if getattr(char, "current_hp", 0) <= 0:
                continue
            if char not in result:
                result.append(char)
        return result

    def fabri_party_members_without(exclude):
        """Живые союзники, кроме указанного персонажа."""
        return [c for c in fabri_party_members() if c is not exclude]

    def fabri_living_enemies():
        """Живые активные противники ТЕКУЩЕГО боя.

        Используется get_active_enemies(), а не весь store.enemies —
        иначе массовые эффекты задевали бы врагов другого боя.
        """
        result = []
        try:
            names = get_active_enemies()
        except Exception:
            names = []
        enemies = getattr(store, "enemies", {}) or {}
        for enemy_name in names:
            enemy = enemies.get(enemy_name)
            if enemy is None:
                continue
            if getattr(enemy, "dead", False):
                continue
            if getattr(enemy, "current_hp", 0) <= 0:
                continue
            result.append(enemy)
        return result


    # ------------------------------------------------------------
    # 3) ПОДСИСТЕМА ФАМИЛЬЯРОВ
    # ------------------------------------------------------------

    def fabri_familiar_display_name(fid):
        """Отображаемое имя фамильяра."""
        if fid == FABRI_JUNIOR_ID:
            return FABRI_JUNIOR_NAME
        data = FABRI_FAMILIARS.get(fid)
        return data["name"] if data else str(fid)

    def fabri_familiar_queue():
        """Очередь призванных фамильяров (список id, максимум 2).

        junior в очереди НЕ хранится: он не занимает слот.
        """
        queue = fabri_get("fabri_familiar_queue", [])
        if not isinstance(queue, list):
            return []
        return [fid for fid in queue if fid in FABRI_FAMILIARS]

    def fabri_familiar_is_summoned(fid):
        """Призван ли фамильяр с указанным id.

        Публичная функция: её вызывают требования меню
        (`requirements={"familiar": ...}`), поэтому она обязана
        корректно отвечать и для junior.
        """
        if fid == FABRI_JUNIOR_ID:
            return bool(fabri_get("fabri_junior_alive", False))
        return fid in fabri_familiar_queue()

    def fabri_familiar_count():
        """Сколько призванных фамильяров занимают очередь (включая мёртвых).

        Мёртвый фамильяр остаётся в очереди до вытеснения, поэтому для
        проверки «есть ли ещё свободный слот» используйте
        fabri_familiar_alive_count().
        """
        return len(fabri_familiar_queue())

    def fabri_familiar_alive_count():
        """Сколько призванных фамильяров живы (HP > 0)."""
        return sum(1 for fid in fabri_familiar_queue()
                   if not fabri_familiar_dead(fid))

    def fabri_familiar_status():
        """Краткий статус фамильяров для интерфейса.

        Возвращает список словарей: id, имя, текущее и максимальное HP,
        признак смерти. Одна точка чтения, чтобы UI не дублировал
        расчёт характеристик.
        """
        result = []
        for fid in fabri_familiar_queue():
            result.append({
                "id": fid,
                "name": fabri_familiar_display_name(fid),
                "hp": fabri_familiar_hp(fid),
                "max_hp": fabri_familiar_max_hp(fid),
                "dead": fabri_familiar_dead(fid),
            })
        return result

    def fabri_familiar_stats(fid):
        """Характеристики фамильяра от УРОВНЯ Фабри.

        Возвращает словарь с max_hp/atk/def/critrate/crit. Считаем
        от таблиц уровня, а не от текущих (бафнутых) значений Фабри,
        как и требует согласованная спецификация.
        """
        char = fabri_char()
        if char is None:
            return {}

        # junior наследует характеристики М-с Пёрышко.
        source_fid = "feather" if fid == FABRI_JUNIOR_ID else fid
        data = FABRI_FAMILIARS.get(source_fid)
        if data is None:
            return {}

        index = max(0, min(fabri_level() - 1, FABRI_MAX_TABLE_LEVEL - 1))

        def _level_value(levels, default=0):
            if not levels:
                return default
            idx = max(0, min(index, len(levels) - 1))
            return levels[idx]

        base_hp    = _level_value(getattr(char, "max_hp_levels", []), 50)
        base_atk   = _level_value(getattr(char, "base_atk_levels", []), 12)
        base_def   = _level_value(getattr(char, "base_def_levels", []), 1)

        max_hp = max(1, int(round(base_hp * data["hp_percent"])))
        atk    = max(0, int(round(base_atk * data["atk_percent"])))
        defense = max(0, int(round(base_def * data["def_percent"])))

        if fid == FABRI_JUNIOR_ID:
            # «Получает на 30% меньше, чем фамильяр М-с Пёрышко» —
            # трактуем как его HP/атаку/защиту в тех же долях от
            # М-с Пёрышко (то есть 70% от её значений).
            jr_base = fabri_familiar_stats("feather")
            if jr_base:
                return {
                    "max_hp": max(1, int(round(jr_base.get("max_hp", 1) * FABRI_JUNIOR_HP_PERCENT))),
                    "atk": max(0, int(round(jr_base.get("atk", 0) * FABRI_JUNIOR_HP_PERCENT))),
                    "defense": max(0, int(round(jr_base.get("defense", 0) * FABRI_JUNIOR_HP_PERCENT))),
                    "critrate": jr_base.get("critrate", 0),
                    "crit": jr_base.get("crit", 1.0),
                    "name": FABRI_JUNIOR_NAME,
                }

        # «Я покажу, как бить!» ур.10: М-с Манки получает +40% от
        # магии, крит.шанса и крит.урона Фабри. Надбавка живёт в
        # состоянии Фабри (fabri_monkey_show_how), а не в самих
        # фамильярах, у которых нет собственных bonus_*-полей.
        if fid == "monkey" and fabri_get("fabri_monkey_show_how", False):
            magic = float(getattr(char, "magic", 0) or 0.0)
            critrate = float(getattr(char, "critrate", 0.0) or 0.0)
            crit = float(getattr(char, "crit", 1.0) or 1.0)
            atk = max(0, int(round(atk + magic * 0.40)))
            critrate = critrate + critrate * 0.40
            crit = crit + crit * 0.40
            return {
                "max_hp": max_hp,
                "atk": atk,
                "defense": defense,
                "critrate": critrate,
                "crit": crit,
                "name": data["name"],
            }

        return {
            "max_hp": max_hp,
            "atk": atk,
            "defense": defense,
            "critrate": data["critrate"],
            "crit": data["crit"],
            "name": data["name"],
        }

    def fabri_familiar_hp(fid):
        """Текущее HP фамильяра (0, если он не призван)."""
        if fid == FABRI_JUNIOR_ID:
            if not fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
                return 0
            return int(fabri_get("fabri_junior_hp", 0) or 0)
        if not fabri_familiar_is_summoned(fid):
            return 0
        hp_map = fabri_get("fabri_familiar_hp", {}) or {}
        return int(hp_map.get(fid, 0) or 0)

    def fabri_familiar_max_hp(fid):
        """Максимальное HP фамильяра."""
        stats = fabri_familiar_stats(fid)
        return int(stats.get("max_hp", 0) or 0)

    def fabri_familiar_dead(fid):
        """Мёртв ли фамильяр (призван, но HP <= 0)."""
        if fid == FABRI_JUNIOR_ID:
            return fabri_familiar_is_summoned(fid) and fabri_familiar_hp(fid) <= 0
        return fid in fabri_familiar_queue() and fabri_familiar_hp(fid) <= 0

    def fabri_familiar_set_hp(fid, value):
        """Записывает текущее HP фамильяра."""
        max_hp = fabri_familiar_max_hp(fid)
        clamped = int(max(0, min(int(value), max_hp)))
        if fid == FABRI_JUNIOR_ID:
            fabri_set("fabri_junior_hp", clamped)
            return clamped
        hp_map = dict(fabri_get("fabri_familiar_hp", {}) or {})
        hp_map[fid] = clamped
        fabri_set("fabri_familiar_hp", hp_map)
        return clamped

    def fabri_create_familiar(fid):
        """Создаёт фамильяра с полным HP и регистрирует его.

        НЕ добавляет объект в store.characters/store.enemies: все
        характеристики читаются через fabri_familiar_* и живут в
        полях Фабри.
        """
        if fid not in FABRI_FAMILIARS:
            return None
        stats = fabri_familiar_stats(fid)
        hp_map = dict(fabri_get("fabri_familiar_hp", {}) or {})
        hp_map[fid] = int(stats.get("max_hp", 0) or 0)
        fabri_set("fabri_familiar_hp", hp_map)
        # Перезарядка магии этого фамильяра начинается заново при
        # создании: сбрасываем счётчик раундов до очередного сброса.
        cd_map = dict(fabri_get("fabri_familiar_cd", {}) or {})
        cd_map[fid] = 0
        fabri_set("fabri_familiar_cd", cd_map)
        renpy.log("[Фабри][Рукодельные друзья] создан {} (HP {})".format(
            fabri_familiar_display_name(fid), hp_map[fid]))
        return fid

    def fabri_summon_familiar(fid):
        """Призывает фамильяра с учётом правил очереди.

        Правила спецификации:
          * одновременно не более 2 призванных;
          * при создании следующего (третьего) уничтожается тот,
            что был призван ПЕРВЫМ;
          * повторный призыв уже призванного пересоздаёт его
            (HP восстанавливается полностью).

        Возвращает id призванного фамильяра.
        """
        if fid not in FABRI_FAMILIARS:
            return None

        queue = fabri_familiar_queue()

        if fid in queue:
            # Пересоздание существующего: слот сохраняется, HP полное.
            fabri_create_familiar(fid)
            return fid

        # Освобождаем место: вытесняем самого первого призванного.
        # Считаем по локальной очереди (она ещё не сохранена в
        # состояние), а не через fabri_familiar_count(): та читает
        # сохранённое значение и дала бы бесконечный цикл.
        evicted = None
        while len(queue) >= FABRI_MAX_FAMILIARS:
            evicted = queue.pop(0)
            renpy.log("[Фабри][Рукодельные друзья] вытеснен {}".format(
                fabri_familiar_display_name(evicted)))

        queue.append(fid)
        fabri_set("fabri_familiar_queue", queue)

        if evicted is not None:
            # Снимаем HP вытесненного, чтобы его состояние не
            # выглядело как «живой фамильяр» при следующей проверке.
            hp_map = dict(fabri_get("fabri_familiar_hp", {}) or {})
            hp_map.pop(evicted, None)
            fabri_set("fabri_familiar_hp", hp_map)
            # М-с Пёрышко младший существует, только пока в очереди
            # есть М-с Пёрышко. Если её вытеснили — младший теряет
            # поддержку и больше не считается призванным.
            if evicted == "feather" and fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
                fabri_dismiss_junior("мать вытеснена другим фамильяром")

        fabri_create_familiar(fid)
        return fid

    def fabri_dismiss_familiar(fid, reason=None):
        """Убирает фамильяра из очереди."""
        queue = fabri_familiar_queue()
        if fid in queue:
            queue.remove(fid)
            fabri_set("fabri_familiar_queue", queue)
        hp_map = dict(fabri_get("fabri_familiar_hp", {}) or {})
        hp_map.pop(fid, None)
        fabri_set("fabri_familiar_hp", hp_map)
        if reason:
            renpy.log("[Фабри][Рукодельные друзья] {} убран: {}".format(
                fabri_familiar_display_name(fid), reason))

    def fabri_dismiss_junior(reason=None):
        """Убирает М-р Пёрышко младшего."""
        if fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
            fabri_set("fabri_junior_alive", False)
            fabri_set("fabri_junior_hp", 0)
            if reason:
                renpy.log("[Фабри][Правильное материнство] младший убран: {}".format(reason))

    def fabri_clear_familiars():
        """Полный сброс фамильяров (начало/конец боя)."""
        fabri_set("fabri_familiar_queue", [])
        fabri_set("fabri_familiar_hp", {})
        fabri_set("fabri_familiar_cd", {})
        fabri_set("fabri_junior_alive", False)
        fabri_set("fabri_junior_hp", 0)
        fabri_set("fabri_egg_turns", 0)
        fabri_set("fabri_egg_owner", None)

    def fabri_random_familiar_id():
        """Случайный призываемый фамильяр («Сотворить наспех»)."""
        ids = list(FABRI_FAMILIARS.keys())
        if not ids:
            return None
        return renpy.random.choice(ids)


    # ------------------------------------------------------------
    # 4) УРОН И ХИЛ ФАМИЛЬЯРОВ
    # ------------------------------------------------------------

    def fabri_familiar_damage(fid, amount, reason=None):
        """Наносит урон фамильяру.

        junior получает на 30% меньше (FABRI_JUNIOR_HP_PERCENT
        применяется к урону), но только пока в очереди есть
        М-с Пёрышко; иначе получает все 100%.

        Возвращает фактически снятое HP.
        """
        if not fabri_familiar_is_summoned(fid):
            return 0

        # «Рукодельные друзья»: баффы и дебаффы на фамильяров в основном
        # не действуют. Прямое получение урона — исключение, но
        # модификаторы урона от баффов/дебаффов цели к фамильярам не
        # применяются: считаем только «сырой» урон.
        if fabri_familiar_immune_to_buffs():
            amount = int(amount)

        incoming = max(0, int(amount))

        if fid == FABRI_JUNIOR_ID:
            mother_summoned = fabri_familiar_is_summoned("feather")
            if mother_summoned:
                # «Получает на 30% меньше» — срезаем 30% урона.
                incoming = int(incoming * FABRI_JUNIOR_HP_PERCENT)
            # Если матери нет — урон идёт полностью (100%).

        # «Творчество будет жить...» ур.7: фамильяры не получают
        # смертельный урон. Оставляем 1 HP вместо гибели.
        current = fabri_familiar_hp(fid)
        lethal = incoming >= current
        if lethal and fabri_level() >= FABRI_LVL_CREATION_LIVES:
            fabri_familiar_set_hp(fid, 1)
            renpy.log("[Фабри][Творчество будет жить] {} спасён от смертельного урона".format(
                fabri_familiar_display_name(fid)))
            return max(0, current - 1)

        new_hp = max(0, current - incoming)
        fabri_familiar_set_hp(fid, new_hp)

        if new_hp <= 0:
            # Погибший фамильяр освобождает слот очереди.
            if fid != FABRI_JUNIOR_ID:
                fabri_dismiss_familiar(fid, reason="погиб в бою")
            else:
                fabri_dismiss_junior("погиб в бою")
        if reason:
            renpy.log("[Фабри] {} получил {} урона ({})".format(
                fabri_familiar_display_name(fid), incoming, reason))
        return min(current, incoming)

    def fabri_familiar_share_damage(amount):
        """Передаёт фамильярам тот же урон, что получила Фабри.

        По спецификации («Рукодельные друзья»): «получают урон и 20%
        хилл вместе с Фабри». Урон передаётся ПОЛНОСТЬЮ — каждый
        призванный фамильяр получает ровно столько же, сколько
        получила сама Фабри (не долю). Долю имеет только хилл:
        FABRI_FAMILIAR_SHARE_HEAL в fabri_familiar_share_heal().
        """
        share = max(0, int(amount))
        if share <= 0:
            return
        for fid in list(fabri_familiar_queue()):
            fabri_familiar_damage(fid, share, reason="урон вместе с Фабри")
        if fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
            fabri_familiar_damage(FABRI_JUNIOR_ID, share, reason="урон вместе с Фабри")

    def fabri_familiar_share_heal(amount):
        """Фамильяры получают 20% от лечения Фабри."""
        heal = int(max(0, amount) * FABRI_FAMILIAR_SHARE_HEAL)
        if heal <= 0:
            return
        for fid in list(fabri_familiar_queue()):
            max_hp = fabri_familiar_max_hp(fid)
            fabri_familiar_set_hp(fid, min(max_hp, fabri_familiar_hp(fid) + heal))
        if fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
            max_hp = fabri_familiar_max_hp(FABRI_JUNIOR_ID)
            fabri_familiar_set_hp(FABRI_JUNIOR_ID,
                                  min(max_hp, fabri_familiar_hp(FABRI_JUNIOR_ID) + heal))

    def fabri_attached_is(char):
        """Прикреплён ли Панцырь именно к этому персонажу."""
        if not fabri_get("fabri_attached_active", False):
            return False
        return fabri_get("fabri_attached_target", None) == getattr(char, "name", None)

    def fabri_attach_damage_split(char, amount):
        """Переносит часть урона цели на прикрепившегося Панцыря.

        «Прикрепиться»: персонаж получает 70% урона, черепаха — весь
        (то есть оставшиеся 30% берёт на себя фамильяр). Возвращает
        долю урона, которую цель реально получает.
        """
        if not fabri_attached_is(char):
            return amount
        if not fabri_familiar_is_summoned("shell"):
            # Панцыря нет — эффект больше не действует.
            fabri_set("fabri_attached_active", False)
            fabri_set("fabri_attached_target", None)
            return amount

        amount = max(0, int(amount))
        taken_by_target = int(amount * FABRI_ATTACH_TARGET_SHARE)
        to_shell = amount - taken_by_target
        if to_shell > 0:
            fabri_familiar_damage("shell", to_shell, reason="прикрыл цель «Прикрепиться»")
            renpy.log("[Фабри][Прикрепиться] Панцырь принял {} урона за {}".format(
                to_shell, getattr(char, "name", "?")))
        return taken_by_target

    def fabri_on_hp_change(delta):
        """Реакция фамильяров на изменение HP Фабри.

        Вызывается из обработки урона/лечения Фабри. Один вызов —
        одна реакция, чтобы урон не учитывался дважды.
        """
        if not fabri_in_battle():
            return
        if delta < 0:
            fabri_familiar_share_damage(-delta)
        elif delta > 0:
            fabri_familiar_share_heal(delta)


    # ------------------------------------------------------------
    # 5) СБРОС ПЕРЕЗАРЯДКИ МАГИИ ФАМИЛЬЯРОВ ЗА РАУНД
    # ------------------------------------------------------------

    def fabri_familiar_tick_round():
        """Сброс перезарядки магии фамильяров — 1 раз за раунд ВСЕГДА.

        спецификация: «Перезарядка магии фамильяров сбрасывается
        постоянно 1 раз за раунд вне зависимости от того, жив
        фамильяр или нет». Поэтому чистим счётчики по всем известным
        фамильярам, а не только по призванным.
        """
        cd_map = {}
        for fid in FABRI_FAMILIARS:
            cd_map[fid] = 0
        fabri_set("fabri_familiar_cd", cd_map)

    def fabri_egg_tick_round():
        """Ход яйца М-с Пёрышко в конце раунда."""
        if not fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
            turns = int(fabri_get("fabri_egg_turns", 0) or 0)
            if turns > 0:
                turns -= 1
                fabri_set("fabri_egg_turns", turns)
                if turns <= 0:
                    fabri_hatch_egg()

    def fabri_hatch_egg():
        """Яйцо вылупляется — появляется М-р Пёрышко младший."""
        fabri_set("fabri_egg_turns", 0)
        fabri_set("fabri_egg_owner", None)
        stats = fabri_familiar_stats(FABRI_JUNIOR_ID)
        fabri_set("fabri_junior_alive", True)
        fabri_set("fabri_junior_hp", int(stats.get("max_hp", 1) or 1))
        renpy.log("[Фабри][Правильное материнство] вылупился {}".format(FABRI_JUNIOR_NAME))

    def fabri_tick_haste():
        """Тик бонуса скорости М-с Морковки в конце раунда.

        Без улучшения «Не сбавляя скорости» бонус просто живёт один
        ход. С улучшением ур.3 он затухает на 5% за ход в течение
        FABRI_HASTE_DECAY_TURNS ходов.
        """
        stacks = int(fabri_get("fabri_haste_stacks", 0) or 0)
        if stacks <= 0:
            return
        turns = int(fabri_get("fabri_haste_turns", 0) or 0) + 1
        fabri_set("fabri_haste_turns", turns)
        if fabri_haste_decay_enabled():
            bonus = fabri_haste_bonus_for_turn(turns)
            fabri_set("fabri_haste_bonus", bonus)
            if turns >= FABRI_HASTE_DECAY_TURNS or bonus <= 0.0:
                fabri_set("fabri_haste_stacks", 0)
                fabri_set("fabri_haste_turns", 0)
                fabri_set("fabri_haste_bonus", 0.0)
        else:
            # Без улучшения эффект действует один следующий ход.
            fabri_set("fabri_haste_stacks", 0)
            fabri_set("fabri_haste_turns", 0)
            renpy.log("[Фабри][Ускориться] бонус истёк")

    def fabri_tick_dodge():
        """Тик уклонения «Не поймаешь» в конце раунда."""
        turns = int(fabri_get("fabri_dodge_turns", 0) or 0)
        if turns <= 0:
            return
        turns -= 1
        fabri_set("fabri_dodge_turns", turns)
        if turns <= 0:
            # Эффект истёк: чистим и цель, и шанс, чтобы fabri_try_dodge
            # больше не срабатывал.
            fabri_set("fabri_dodge_target", None)
            fabri_set("fabri_dodge_chance", 0.0)

    def fabri_tick_junior_social():
        """М-р Пёрышко младший: +1 соц. характеристика с шансом 50%."""
        if not fabri_familiar_is_summoned(FABRI_JUNIOR_ID):
            return
        if renpy.random.random() > FABRI_JUNIOR_SOCIAL_CHANCE:
            return
        # Пишем в bonus_*-поля, а НЕ через одноимённые свойства:
        # их сеттеры перезаписывают base_*_levels, то есть навсегда
        # портят базовую таблицу персонажа.
        options = ["bonus_socialization", "bonus_perception", "bonus_rhetoric",
                   "bonus_comfort", "bonus_artistry", "bonus_power"]
        field = renpy.random.choice(options)
        char = fabri_char()
        if char is None:
            return
        if not hasattr(char, field):
            return
        current = float(getattr(char, field, 0.0) or 0.0)
        setattr(char, field, current + 1.0)
        renpy.log("[Фабри][Пёрышко младший] +1 к {}".format(field))

    def fabri_tick_round_effects():
        """Тики эффектов Фабри в конце раунда.

        Единая точка вызова из afterenemyattack: скорость Морковки,
        уклонение «Не поймаешь», соц. бонус младшего и «Разнообразие –
        лучшее вдохновение» за еду разного типа.
        """
        fabri_tick_haste()
        fabri_tick_dodge()
        fabri_tick_junior_social()
        fabri_apply_variety_bonus()


    # ------------------------------------------------------------
    # 6) АУРЫ ПРИЗВАННЫХ ФАМИЛЬЯРОВ (каждый ход)
    # ------------------------------------------------------------
    # Ауры действуют автоматически, пока фамильяр призван. Каждая
    # аура проверяет и уровень способности, и улучшение, меняющее
    # её числа.

    def fabri_aura_defense_percent():
        """Панцырь: 3-5% защиты команде."""
        if not fabri_familiar_is_summoned("shell"):
            return 0.0
        return 3.0 + min(2.0, 0.2 * fabri_level())

    def fabri_aura_accuracy_percent():
        """Пёрышко: 2-3% точности команде."""
        if not fabri_familiar_is_summoned("feather"):
            return 0.0
        return 2.0 + min(1.0, 0.1 * fabri_level())

    def fabri_aura_speed_percent():
        """Морковка: 1-2% скорости."""
        if not fabri_familiar_is_summoned("carrot"):
            return 0.0
        return 1.0 + min(1.0, 0.1 * fabri_level())

    def fabri_aura_heal_percent():
        """Морковка: лечение 2-3% HP/MP за ход."""
        if not fabri_familiar_is_summoned("carrot"):
            return 0.0
        return 2.0 + min(1.0, 0.1 * fabri_level())

    def fabri_aura_attack_percent():
        """Манки: 2% атаки команде."""
        if not fabri_familiar_is_summoned("monkey"):
            return 0.0
        return 2.0

    def fabri_apply_auras(run_attacks=True):
        """Применяет ауры призванных фамильяров.

        run_attacks=False используется при вызове сразу после призыва:
        баффы должны обновиться немедленно, а автоатака Манки —
        сработать ровно один раз за раунд (в начале хода Фабри),
        иначе Манки била бы за каждого призванного фамильяра.

        Возвращает список применённых описаний (для визуализации).
        """
        if not fabri_in_battle():
            return []

        applied = []
        party = fabri_party_members()

        def_percent = fabri_aura_defense_percent()
        if def_percent > 0:
            for member in party:
                # bonus_def — МНОЖИТЕЛЬ (см. Pers.defense: base*bonus_def).
                member.bonus_def = float(getattr(member, "bonus_def", 0.0) or 0.0) + def_percent / 100.0
            applied.append("Панцырь: +{:.1f}% защиты команде".format(def_percent))

        atk_percent = fabri_aura_attack_percent()
        if atk_percent > 0:
            for member in party:
                member.bonus_atk = float(getattr(member, "bonus_atk", 0.0) or 0.0) + atk_percent / 100.0
            applied.append("Манки: +{:.1f}% атаки команде".format(atk_percent))

        acc_percent = fabri_aura_accuracy_percent()
        if acc_percent > 0:
            for member in party:
                # dmgchance — read-only property (base + mods), поэтому
                # пишем в writable bonus_dmgchance. Точность хранится
                # долей (0..1), значит проценты переводим в доли.
                member.bonus_dmgchance = float(getattr(member, "bonus_dmgchance", 0.0) or 0.0) + acc_percent / 100.0
            applied.append("Пёрышко: +{:.1f}% точности команде".format(acc_percent))

        heal_percent = fabri_aura_heal_percent()
        if heal_percent > 0:
            for member in party:
                hp_heal = int(member.max_hp * heal_percent / 100.0)
                mp_heal = int(getattr(member, "max_mp", 0) * heal_percent / 100.0)
                if hp_heal:
                    member.change_hp(hp_heal)
                if mp_heal:
                    member.current_mp = min(member.max_mp, member.current_mp + mp_heal)
            applied.append("Морковка: лечение {:.1f}% HP/MP".format(heal_percent))

        # Морковка также даёт прибавку скорости души (штатная боевая
        # переменная store.soul_speed, ограничивается clamp_soul_speed).
        speed_percent = fabri_aura_speed_percent()
        if speed_percent > 0:
            base_speed = float(getattr(store, "soul_speed", 6))
            try:
                store.soul_speed = store.clamp_soul_speed(
                    base_speed * (1.0 + speed_percent / 100.0))
            except Exception:
                store.soul_speed = base_speed
            applied.append("Морковка: скорость души +{:.1f}%".format(speed_percent))

        # «Пёрышко» даёт союзникам 1 стак случайного баффа в начале хода.
        if fabri_familiar_is_summoned("feather"):
            stack = fabri_random_buff_stack()
            if stack:
                applied.append("Пёрышко: стак «{}»".format(stack))

        # Манки бьёт случайного противника — ровно раз за раунд.
        if run_attacks and fabri_familiar_is_summoned("monkey"):
            hit = fabri_monkey_auto_attack()
            if hit:
                applied.append(hit)

        return applied

    def fabri_random_buff_stack():
        """1 стак случайного баффа союзникам (аура М-с Пёрышко).

        Союзникам, а не самой Фабри: она — создатель фамильяров и не
        должна усиливать себя собственной аурой.
        """
        options = [
            ("атака",   "bonus_atk"),
            ("защита",  "bonus_def"),
            ("магия",   "bonus_magic"),
        ]
        label, field = renpy.random.choice(options)
        for member in fabri_party_members_without(fabri_char()):
            current = float(getattr(member, field, 0.0) or 0.0)
            setattr(member, field, current + FABRI_FEATHER_STACK_PERCENT)
        return label

    def fabri_monkey_auto_attack():
        """М-с Манки бьёт случайного противника в начале хода."""
        enemies = fabri_living_enemies()
        if not enemies:
            return None
        target = renpy.random.choice(enemies)
        monkey = fabri_familiar_stats("monkey")
        base_atk = int(monkey.get("atk", 0) or 0)
        damage = max(1, base_atk)
        # «Рукодельные друзья»: урон фамильяров зависит от магии Фабри.
        # Пассивка активна с ур.1 и является гейтом для надбавки магии.
        if fabri_handmade_friends_active():
            char = fabri_char()
            magic = int(getattr(char, "magic", 0) or 0) if char else 0
            damage += int(magic * FABRI_MONKEY_MAGIC_SHARE)
        old_hp = target.current_hp
        target.current_hp = max(0, target.current_hp - damage)
        try:
            add_attack_result("М-с Манки", target.name, damage, False, "normal")
        except Exception:
            pass
        try:
            store.update_swoon_pending_for_visual(target, old_hp)
        except Exception:
            pass
        return "Манки бьёт {} на {}".format(getattr(target, "name", "?"), damage)


    # ------------------------------------------------------------
    # 7) ПАССИВКИ
    # ------------------------------------------------------------

    # --- ур.1 «Созидатель, а не разрушитель» ---------------------
    # Фабри не имеет активных атак; когда союзник (или противник)
    # получает бафф, у Фабри есть шанс = её магия (в %) забрать
    # половину этого баффа себе.
    def fabri_creator_siphon_chance():
        """Шанс забрать половину баффа = магия Фабри в процентах."""
        if fabri_level() < FABRI_LVL_CREATOR:
            return 0.0
        char = fabri_char()
        if char is None:
            return 0.0
        magic = float(getattr(char, "magic", 0) or 0.0)
        # Магия — абсолютное число (27..114 на ур.1..12). Шанс в
        # процентах ограничиваем 100%, иначе он был бы бессмысленным.
        return max(0.0, min(100.0, magic))

    def fabri_try_siphon_buff(field, amount):
        """Шанс забрать половину баффа себе.

        Возвращает реально добавленную Фабри долю (0, если бросок
        не прошёл или пассивка недоступна).
        """
        if fabri_level() < FABRI_LVL_CREATOR:
            return 0.0
        if fabri_char() is None:
            return 0.0
        amount = float(amount or 0.0)
        if amount == 0.0:
            return 0.0
        chance = fabri_creator_siphon_chance() / 100.0
        if renpy.random.random() > chance:
            return 0.0
        half = amount * 0.5
        char = fabri_char()
        current = float(getattr(char, field, 0.0) or 0.0)
        setattr(char, field, current + half)
        renpy.log("[Фабри][Созидатель] забрала половину баффа {}: +{}".format(field, half))
        return half

    # --- ур.1 «Рукодельные друзья» -------------------------------
    def fabri_handmade_friends_active():
        """Пассивка активна: магия Фабри зависит от фамильяров."""
        return fabri_level() >= FABRI_LVL_HANDMADE

    def fabri_familiar_immune_to_buffs():
        """Фамильяры не получают баффы/дебаффы союзников и врагов.

        Возвращает True, если эффект должен быть проигнорирован для
        фамильяров. По спецификации — «в большинстве случаев»,
        поэтому исключение сделано только для снятия дебаффов
        («Неудержимость» лечит сама себя через fabri_perform_*).
        """
        return fabri_level() >= FABRI_LVL_HANDMADE

    # --- ур.1 «Передышка, чтоб вернуться» ------------------------
    def fabri_respite_seconds():
        """Бонус к скорости возврата души от уровня Фабри.

        «Скорость души» в проекте — общая боевая переменная
        store.soul_speed, ограничиваемая clamp_soul_speed (как в
        пассивке Арчи «Рывок»). Поэтому пассивка применяется к ней,
        а не к несуществующему полю персонажа.
        """
        if fabri_level() < FABRI_LVL_RESPITE:
            return 0.0
        return FABRI_RESPITE_PER_LEVEL * fabri_level()

    def fabri_apply_respite():
        """Применяет «Передышку» в начале боя (один раз за бой)."""
        if not fabri_in_battle():
            return False
        bonus = fabri_respite_seconds()
        if bonus <= 0:
            return False
        base = float(getattr(store, "soul_speed", 6))
        try:
            store.soul_speed = store.clamp_soul_speed(base + bonus)
        except Exception:
            store.soul_speed = base + bonus
        renpy.log("[Фабри][Передышка] скорость души +{:.2f}".format(bonus))
        return True

    # --- ур.1 «Разнообразие – лучшее вдохновение» ----------------
    def fabri_food_types():
        """Типы еды, которой наелась Фабри в этом бою."""
        types = fabri_get("fabri_food_types", [])
        return list(types) if isinstance(types, list) else []

    def fabri_note_food(type_id):
        """Запоминает тип съеденной еды (для «Разнообразия»)."""
        if not type_id:
            return
        types = fabri_food_types()
        if type_id not in types:
            types.append(type_id)
        fabri_set("fabri_food_types", types)

    def fabri_note_battle_food_types():
        """Собирает типы еды, которой наелась команда за этот бой.

        «Разнообразие – лучшее вдохновение» ур.1: если у Фабри вся еда
        разного типа, в конце раунда она получает +10% бонусной магии
        и +4% крит.шанса. Источник — уже существующий менеджер
        аппетита/готовки: читаем его, а не заводим второй учёт.
        """
        if fabri_level() < FABRI_LVL_VARIETY:
            return
        manager = getattr(store, "cooking_manager", None)
        feed = getattr(manager, "feed_amount", None) if manager else None
        if isinstance(feed, dict):
            for dish_id, amount in feed.items():
                if amount and amount > 0:
                    fabri_note_food(dish_id)
        # Дополнительно учитываем очередь аппетита, если она есть.
        for field in ("heroes_feedness", "feedness_queue"):
            queue = getattr(store, field, None)
            if isinstance(queue, dict):
                for dish_id, count in queue.items():
                    if count:
                        fabri_note_food(dish_id)

    def fabri_food_is_varied():
        """Вся ли еда разного типа.

        Проверяем, что в списке типов нет повторов и он не пуст.
        """
        types = fabri_food_types()
        if not types:
            return False
        return len(types) == len(set(types))

    def fabri_apply_variety_bonus():
        """Конец раунда: бонус за разнообразную еду."""
        if fabri_level() < FABRI_LVL_VARIETY:
            return False
        if not fabri_food_is_varied():
            return False
        char = fabri_char()
        if char is None:
            return False
        # bonus_magic — аддитивная доля (defense/magic: base*(1+bonus)),
        # проценты переводим в доли.
        char.bonus_magic = float(getattr(char, "bonus_magic", 0.0) or 0.0) + \
            FABRI_VARIETY_MAGIC_PERCENT / 100.0
        # critrate — read-only property, пишем в writable bonus_critrate.
        char.bonus_critrate = float(getattr(char, "bonus_critrate", 0.0) or 0.0) + \
            FABRI_VARIETY_CRIT_PERCENT / 100.0
        renpy.log("[Фабри][Разнообразие] +{}% магии, +{}% крит.шанса".format(
            FABRI_VARIETY_MAGIC_PERCENT, FABRI_VARIETY_CRIT_PERCENT))
        return True

    # --- ур.3 «Энтузиазм и усердие» ------------------------------
    def fabri_roll_free_summon():
        """Шанс = крит.шанс не потратить ману на создание фамильяра."""
        if fabri_level() < FABRI_LVL_ENTHUSIASM:
            return False
        char = fabri_char()
        if char is None:
            return False
        chance = float(getattr(char, "critrate", 0.0) or 0.0)
        # critrate хранится как доля (0..1) у Pers.
        ok = renpy.random.random() <= max(0.0, min(1.0, chance))
        if ok:
            renpy.log("[Фабри][Энтузиазм и усердие] призыв бесплатен")
        return ok

    # --- ур.5 «Сотворить наспех» ---------------------------------
    def fabri_haste_summon_second():
        """Создаёт случайного второго фамильяра («Сотворить наспех»)."""
        if fabri_level() < FABRI_LVL_HASTY:
            return None
        fid = fabri_random_familiar_id()
        if fid is None:
            return None
        if fid in fabri_familiar_queue():
            # Уже призван — берём другого, если есть.
            others = [f for f in FABRI_FAMILIARS if f not in fabri_familiar_queue()]
            if not others:
                return None
            fid = renpy.random.choice(others)
        renpy.log("[Фабри][Сотворить наспех] случайный фамильяр: {}".format(
            fabri_familiar_display_name(fid)))
        return fid

    # --- ур.7 «Творчество будет жить...» -------------------------
    def fabri_roll_creation_lives():
        """С крит.шансом Фабри получает 150% урона, фамильяры 20%.

        Возвращает True, если эффект сработал. Само спасение
        фамильяров от смертельного урона реализовано в
        fabri_familiar_damage() и не зависит от броска.
        """
        if fabri_level() < FABRI_LVL_CREATION_LIVES:
            return False
        char = fabri_char()
        if char is None:
            return False
        chance = float(getattr(char, "critrate", 0.0) or 0.0)
        ok = renpy.random.random() <= max(0.0, min(1.0, chance))
        if ok:
            renpy.log("[Фабри][Творчество будет жить] урон Фабри +150%, фамильяров +20%")
        return ok

    def fabri_creation_lives_multiplier(target):
        """Множитель получаемого урона по пассивке «Творчество будет жить».

        Фабри получает 150% урона, фамильяры — 20%. Бросок делается
        один раз за попадание; читается из обоих путей нанесения урона,
        поэтому пассивка реально влияет на бой.
        """
        if not fabri_roll_creation_lives():
            return 1.0
        name = getattr(target, "name", None)
        if name == "Фабри":
            return 1.5
        # Фамильяры не являются объектами Pers; их урон считается
        # в fabri_familiar_damage(), где множитель берётся напрямую.
        return 1.0

    # --- ур.9 «Радующее творчество» ------------------------------
    def fabri_inspiration_multiplier():
        """Множитель баффа вдохновения союзникам (x3 с ур.9)."""
        if fabri_level() < FABRI_LVL_JOYFUL:
            return 1
        return FABRI_JOYFUL_INSPIRATION_MULT

    def fabri_apply_inspiration(party=None):
        """Каждое создание фамильяра даёт союзникам вдохновение."""
        mult = fabri_inspiration_multiplier()
        if mult <= 1:
            return False
        for member in (party if party is not None else fabri_party_members()):
            member.bonus_atk = float(getattr(member, "bonus_atk", 0.0) or 0.0) + 0.02 * mult
        renpy.log("[Фабри][Радующее творчество] вдохновение x{}".format(mult))
        return True


    # ------------------------------------------------------------
    # 8) УЛУЧШЕНИЯ СПОСОБНОСТЕЙ (уровень улучшения != уровень открытия)
    # ------------------------------------------------------------

    def fabri_hide_tank_reduction():
        """«Спрятаться»: −7 танка, с ур.2 «Всем прятаться!» — −3."""
        if fabri_level() >= FABRI_UP_HIDE_ALL:
            return FABRI_HIDE_TANK_UP
        return FABRI_HIDE_TANK_BASE

    def fabri_haste_decay_enabled():
        """«Не сбавляя скорости» ур.3: 15% → −5% за 3 хода."""
        return fabri_level() >= FABRI_UP_NO_SLOWDOWN

    def fabri_haste_bonus_for_turn(turns_elapsed):
        """Бонус скорости «Ускориться» с учётом улучшения."""
        if not fabri_haste_decay_enabled():
            return FABRI_HASTE_BASE
        decayed = FABRI_HASTE_BASE - FABRI_HASTE_DECAY * int(turns_elapsed)
        return max(0.0, decayed)

    def fabri_unchained_bonuses():
        """«Сорваться с цепи» ур.4: +5% атаки и +20% крит.урона."""
        if fabri_level() < FABRI_UP_OFF_THE_CHAIN:
            return (0.0, 0.0)
        return (FABRI_UNCHAINED_ATK_PERCENT, FABRI_UNCHAINED_CRITDMG_BONUS)

    def fabri_warmup_dances_active():
        """«Разминающие танцы» ур.5: откат способностей цели на 1."""
        return fabri_level() >= FABRI_UP_WARMUP_DANCES

    def fabri_dodge_turns():
        """«Не поймаешь»: 2 хода, с ур.7 — 3 хода."""
        if fabri_level() >= FABRI_UP_TOUGHER_PREDATOR:
            return FABRI_DODGE_TURNS_UP
        return FABRI_DODGE_TURNS

    def fabri_hit_harder_extra_percent():
        """«Я тоже бей сильнее!» ур.8: +20% магии Фабри уроном Манки."""
        if fabri_level() < FABRI_UP_HIT_HARDER_TOO:
            return 0.0
        return FABRI_MONKEY_EXTRA_MAGIC_PERCENT * 100.0

    def fabri_tempering_defense_bonus(targets_hit):
        """«Закаляя панцирь» ур.9: +10% защиты за каждую цель."""
        if fabri_level() < FABRI_UP_TEMPERING:
            return 0.0
        return FABRI_SHELL_TEMPER_PER_TARGET * max(0, int(targets_hit))

    def fabri_egg_hatch_turns():
        """Яйцо: 5 ходов, с ур.10 «Правильное материнство» — 3."""
        if fabri_level() >= FABRI_UP_MOTHERHOOD:
            return FABRI_EGG_HATCH_TURNS_UP
        return FABRI_EGG_HATCH_TURNS

    def fabri_monkey_show_how_active():
        """«Я покажу, как бить!» ур.10 — пассивный бонус Манки."""
        return fabri_level() >= 10


    # ------------------------------------------------------------
    # 9) ИСПОЛНЕНИЕ: ПРИЗЫВ И МАГИЯ ФАМИЛЬЯРОВ
    # ------------------------------------------------------------
    # Эти функции вызываются из лейблов fabri_summon_is_done и
    # fabri_familiar_magic_is_done. Оплата маны выполняется общим
    # путём (Heroperformsturn -> pay_ability_cost) и здесь НЕ
    # дублируется.

    def fabri_perform_summon(ability_name):
        """Обрабатывает призыв фамильяра.

        Возвращает текст результата для визуализации.
        """
        fid = FABRI_SUMMON_MAP.get(ability_name)
        if fid is None:
            return None

        summoned = [fid]

        # «Энтузиазм и усердие» ур.3: шанс = крит.шанс не потратить ману
        # на создание фамильяра. Призывы в реестре бесплатны, поэтому
        # бесплатный призыв даёт компенсацию маны — иначе пассивка была
        # бы мёртвой. Компенсация равна доле от макс. MP, чтобы она была
        # заметной, но не бесконечной.
        if fabri_roll_free_summon():
            char = fabri_char()
            if char is not None:
                max_mp = int(getattr(char, "max_mp", 0) or 0)
                refund = int(max_mp * FABRI_FREE_SUMMON_REFUND_PERCENT)
                char.current_mp = min(max_mp, int(getattr(char, "current_mp", 0) or 0) + refund)
                renpy.log("[Фабри][Энтузиазм и усердие] призыв бесплатен, "
                          "возвращено {} MP".format(refund))

        fabri_summon_familiar(fid)

        # «Сотворить наспех» ур.5: 1 выбранный + 1 случайный.
        extra = fabri_haste_summon_second()
        if extra:
            fabri_summon_familiar(extra)
            summoned.append(extra)

        # «Радующее творчество» ур.9: вдохновение союзникам.
        fabri_apply_inspiration()

        # Призванные ауры начинают действовать сразу в этом же ходу.
        # run_attacks=False: автоатака Манки уже отработала в начале
        # хода Фабри и не должна повторяться за каждый призыв.
        fabri_apply_auras(run_attacks=False)

        names = ", ".join(fabri_familiar_display_name(f) for f in summoned)
        return "Призваны: {}".format(names)

    def fabri_perform_familiar_magic(ability_name):
        """Обрабатывает магию фамильяра.

        Возвращает текст результата. Каждая ветка проверяет, что
        нужный фамильяр действительно призван: иначе кнопка была бы
        доступна без работающего эффекта.
        """
        entry = FABRI_MAGIC_TAGS.get(ability_name)
        if entry is None:
            return None
        fid, tag = entry

        if not fabri_familiar_is_summoned(fid):
            renpy.log("[Фабри] магия {} недоступна: {} не призван".format(
                ability_name, fabri_familiar_display_name(fid)))
            return None

        char = fabri_char()
        if char is None:
            return None

        handler = {
            "hide":            fabri_magic_hide,
            "shell_on":        fabri_magic_shell_on,
            "attach":          fabri_magic_attach,
            "ricochet":        fabri_magic_ricochet,
            "eagle_eye":       fabri_magic_eagle_eye,
            "sky_dance":       fabri_magic_sky_dance,
            "lay_egg":         fabri_magic_lay_egg,
            "feather_storm":   fabri_magic_feather_storm,
            "haste":           fabri_magic_haste,
            "uncatchable":     fabri_magic_uncatchable,
            "share_carrot":    fabri_magic_share_carrot,
            "faster_further":  fabri_magic_faster_further,
            "battle_roar":     fabri_magic_battle_roar,
            "uncontrollable":  fabri_magic_uncontrollable,
            "hit_harder":      fabri_magic_hit_harder,
            "show_how":        fabri_magic_show_how,
        }.get(tag)

        if handler is None:
            return None
        return handler(char)

    # --- Панцырь -------------------------------------------------

    def fabri_magic_hide(char):
        """«Спрятаться»: снижает танк Фабри и даёт бонусную защиту.

        Важно: Pers.total_tank() считает `base_tank + bonus_tank`
        (в диапазоне 25..50) и НЕ читает extra_tank, поэтому снижать
        нужно именно bonus_tank — иначе эффект был бы мёртвым флагом.
        """
        reduction = fabri_hide_tank_reduction()
        char.bonus_tank = float(getattr(char, "bonus_tank", 0.0) or 0.0) - reduction
        # 2-3% бонусной защиты цели (сама Фабри — цель по умолчанию).
        char.bonus_def = float(getattr(char, "bonus_def", 0.0) or 0.0) + 0.02
        renpy.log("[Фабри][Спрятаться] танк -{}, +2% защиты".format(reduction))
        return "Спрятаться: танк −{0}, +2% защиты".format(reduction)

    def fabri_magic_shell_on(char):
        """«Надеть панцирь»: даёт цели 1 щит."""
        char.shield = int(getattr(char, "shield", 0) or 0) + 1
        renpy.log("[Фабри][Надеть панцирь] щитов: {}".format(char.shield))
        return "Надеть панцирь: щит x{0}".format(char.shield)

    def fabri_magic_attach(char):
        """«Прикрепиться»: персонаж получает 70% урона, черепаха — весь.

        Реализуется флагом: доля входящего урона по цели переносится
        на фамильяра.
        """
        fabri_set("fabri_attached_target", getattr(char, "name", None))
        fabri_set("fabri_attached_active", True)
        renpy.log("[Фабри][Прикрепиться] цель: {}".format(fabri_get("fabri_attached_target")))
        return "Панцырь прикрепился к цели"

    def fabri_magic_ricochet(char):
        """«Рикошет черепахи»: снижает атаку всех врагов на 15%.

        `atk` — read-only свойство и у Pers, и у Enemy, поэтому
        снижаем через writable `bonus_atk` (аддитивная доля:
        atk = base_atk*(1 + bonus_atk) + ...). Знак минус понижает.
        """
        enemies = fabri_living_enemies()
        if not enemies:
            return None
        for enemy in enemies:
            if not hasattr(enemy, "bonus_atk"):
                continue
            enemy.bonus_atk = float(getattr(enemy, "bonus_atk", 0.0) or 0.0) - 0.15
        # «Закаляя панцирь» ур.9: +10% защиты за каждую цель.
        temper = fabri_tempering_defense_bonus(len(enemies))
        if temper > 0:
            char.bonus_def = float(getattr(char, "bonus_def", 0.0) or 0.0) + temper / 100.0
        renpy.log("[Фабри][Рикошет] целей {}, защита +{}%".format(len(enemies), temper))
        return "Рикошет: атака врагов −15%, защита +{0:.0f}%".format(temper)

    # --- Пёрышко -------------------------------------------------

    def fabri_magic_eagle_eye(char):
        """«Орлиная зоркость»: бафф точности x3 цели.

        dmgchance — read-only property (base_dmgchance + mods), поэтому
        пишем в writable bonus_dmgchance. Утроение считаем от текущего
        итогового значения, чтобы «x3» соответствовал спеке.
        """
        current = float(getattr(char, "dmgchance", 0.0) or 0.0)
        target = min(1.0, current * 3.0)
        bonus = float(getattr(char, "bonus_dmgchance", 0.0) or 0.0) + (target - current)
        char.bonus_dmgchance = bonus
        renpy.log("[Фабри][Орлиная зоркость] точность x3 ({:.2f} -> {:.2f})".format(current, target))
        return "Орлиная зоркость: точность x3"

    def fabri_magic_sky_dance(char):
        """«Небесные танцы»: +3 артистизма и уязвимость x3.

        Артистизм пишем в bonus_artistry, а НЕ через свойство artistry:
        его сеттер перезаписывает base_artistry_levels, то есть
        необратимо портит базовую таблицу персонажа.
        """
        char.bonus_artistry = float(getattr(char, "bonus_artistry", 0.0) or 0.0) + 3.0
        # Уязвимость x3: tank_debuff в проекте означает уязвимость,
        # поэтому снижаем его (артистизм считается за вычетом tank_debuff).
        char.tank_debuff = int(getattr(char, "tank_debuff", 0) or 0) - 3
        # «Разминающие танцы» ур.5: откат всех способностей цели на 1.
        if fabri_warmup_dances_active():
            fabri_cooldown_rewind(char, 1)
        renpy.log("[Фабри][Небесные танцы] +3 артистизма, уязвимость x3")
        return "Небесные танцы: +3 артистизма; улучшение откатило КД на 1"

    def fabri_magic_lay_egg(char):
        """«Снести яичко»: кладка, вылупляется через N ходов."""
        if fabri_get("fabri_egg_turns", 0) > 0:
            # Яйцо уже насиживается — второе не кладём.
            return None
        turns = fabri_egg_hatch_turns()
        fabri_set("fabri_egg_turns", turns)
        fabri_set("fabri_egg_owner", "feather")
        renpy.log("[Фабри][Снести яичко] вылупится через {}".format(turns))
        return "Яйцо снесено: вылупится через {0} ходов".format(turns)

    def fabri_magic_feather_storm(char):
        """«Перьевой ураган»: страх x3 (дебафф точности) по врагам.

        Используем штатный механизм проекта: accuracy_debuff (стаки
        страха) + accuracy_debuff_var (пересчёт точности), как это
        делает 1_ДЕБАФЫ_СИСТЕМА.rpy. Прямая запись в enemy.dmgchance
        невозможна — это read-only property.
        """
        enemies = fabri_living_enemies()
        if not enemies:
            return None
        for enemy in enemies:
            enemy.accuracy_debuff = int(getattr(enemy, "accuracy_debuff", 0) or 0) + 3
            # Шаг страха — 5% к сдвигу точности, как в общей системе
            # дебаффов. У Enemy у accuracy_debuff_var есть сеттер
            # (внутреннее поле *_var2); на случай другой сущности
            # пишем внутреннее поле напрямую.
            current_var = float(getattr(enemy, "accuracy_debuff_var", 0.0) or 0.0)
            new_var = max(-0.5, current_var - 0.05 * 3)
            try:
                enemy.accuracy_debuff_var = new_var
            except AttributeError:
                enemy.accuracy_debuff_var2 = new_var
        renpy.log("[Фабри][Перьевой ураган] страх x3 по {} врагам".format(len(enemies)))
        return "Перьевой ураган: страх x3"

    # --- Морковка ------------------------------------------------

    def fabri_magic_haste(char):
        """«Ускориться»: бонус скорости на следующий ход."""
        bonus = fabri_haste_bonus_for_turn(0)
        # extra_tank используется как «скорость» в проекте: скорость
        # ускоряет порядок действий, поэтому храним как стак.
        stacks = int(fabri_get("fabri_haste_stacks", 0) or 0) + 1
        fabri_set("fabri_haste_stacks", stacks)
        fabri_set("fabri_haste_bonus", bonus)
        fabri_set("fabri_haste_turns", 0)
        renpy.log("[Фабри][Ускориться] +{:.0f}% скорости".format(bonus))
        return "Ускориться: +{0:.0f}% скорости".format(bonus)

    def fabri_magic_uncatchable(char):
        """«Не поймаешь»: шанс уклонения = танк цели − 35.

        Шанс хранится в состоянии Фабри (`fabri_dodge_chance`), а не в
        поле самой цели: у Pers нет поля dodge_chance, и такой флаг
        никто бы не прочитал. Читает его fabri_try_dodge(), которая
        вызывается из общего пути нанесения урона.
        """
        # Pers не имеет свойства `tank`; итоговый танк — total_tank.
        tank = float(getattr(char, "total_tank", 0) or 0.0)
        chance = max(0.0, tank - 35.0)
        fabri_set("fabri_dodge_chance", chance)
        fabri_set("fabri_dodge_target", getattr(char, "name", None))
        fabri_set("fabri_dodge_turns", fabri_dodge_turns())
        renpy.log("[Фабри][Не поймаешь] уклонение {:.1f}% на {} ходов".format(
            chance, fabri_dodge_turns()))
        return "Не поймаешь: уклонение {0:.1f}% на {1} ходов".format(
            chance, fabri_dodge_turns())

    def fabri_try_dodge(target_char):
        """Попытка уклонения цели по эффекту «Не поймаешь».

        Возвращает True, если урон полностью избегнут. Вызывается из
        общего пути нанесения урона (как sylvia_try_dodge), поэтому
        эффект реально влияет на бой, а не остаётся мёртвым флагом.
        """
        if target_char is None:
            return False
        if fabri_level() < 1:
            return False
        turns = int(fabri_get("fabri_dodge_turns", 0) or 0)
        if turns <= 0:
            return False
        # Эффект действует только на выбранную цель.
        target_name = fabri_get("fabri_dodge_target", None)
        if target_name and getattr(target_char, "name", None) != target_name:
            return False
        if getattr(target_char, "current_hp", 0) <= 0:
            return False

        chance = float(fabri_get("fabri_dodge_chance", 0.0) or 0.0)
        roll = renpy.random.random() * 100.0
        if roll <= chance:
            renpy.log("[Фабри][Не поймаешь] уклонение сработало "
                      "({:.1f} <= {:.1f})".format(roll, chance))
            return True
        return False

    def fabri_magic_share_carrot(char):
        """«Поделиться морковкой»: 35% HP себе и 45% другому фамильяру."""
        healed_self = int(fabri_familiar_max_hp("carrot") * 0.35)
        fabri_familiar_set_hp("carrot",
                              min(fabri_familiar_max_hp("carrot"),
                                  fabri_familiar_hp("carrot") + healed_self))
        other = None
        for fid in fabri_familiar_queue():
            if fid != "carrot":
                other = fid
                break
        if other:
            healed_other = int(fabri_familiar_max_hp(other) * 0.45)
            fabri_familiar_set_hp(other,
                                  min(fabri_familiar_max_hp(other),
                                      fabri_familiar_hp(other) + healed_other))
        renpy.log("[Фабри][Поделиться морковкой] +{} себе".format(healed_self))
        return "Поделиться морковкой: восстановлено {0} HP".format(healed_self)

    def fabri_magic_faster_further(char):
        """«Быстрее и дальше»: даёт цели ещё 1 ход."""
        char.turn = 1
        renpy.log("[Фабри][Быстрее и дальше] {} получил ещё ход".format(
            getattr(char, "name", "?")))
        return "Быстрее и дальше: цель получает ещё 1 ход"

    # --- Манки ---------------------------------------------------

    def fabri_magic_battle_roar(char):
        """«Боевой рёв»: другой фамильяр атакует случайного врага."""
        enemies = fabri_living_enemies()
        if not enemies:
            return None
        attacker_fid = None
        for fid in fabri_familiar_queue():
            if fid != "monkey":
                attacker_fid = fid
                break
        if attacker_fid is None:
            return None
        target = renpy.random.choice(enemies)
        stats = fabri_familiar_stats(attacker_fid)
        monkey_stats = fabri_familiar_stats("monkey")
        damage = max(1, int(stats.get("atk", 0) or 0) + int(monkey_stats.get("atk", 0) or 0))
        old_hp = target.current_hp
        target.current_hp = max(0, target.current_hp - damage)
        try:
            add_attack_result(fabri_familiar_display_name(attacker_fid),
                              target.name, damage, False, "normal")
        except Exception:
            pass
        try:
            store.update_swoon_pending_for_visual(target, old_hp)
        except Exception:
            pass
        renpy.log("[Фабри][Боевой рёв] {} бьёт {} на {}".format(
            fabri_familiar_display_name(attacker_fid), target.name, damage))
        return "Боевой рёв: {0} бьёт {1} на {2}".format(
            fabri_familiar_display_name(attacker_fid), target.name, damage)

    def fabri_magic_uncontrollable(char):
        """«Неудержимость»: снимает 2 стака всех дебаффов с цели."""
        cleared = []
        for field in ("bloodshed_debuff", "prone_debuff"):
            value = int(getattr(char, field, 0) or 0)
            if value > 0:
                new_value = max(0, value - 2)
                setattr(char, field, new_value)
                cleared.append(field)
        # «Сорваться с цепи» ур.4: +5% атаки и +20% крит.урона.
        atk_percent, crit_bonus = fabri_unchained_bonuses()
        if atk_percent:
            char.bonus_atk = float(getattr(char, "bonus_atk", 0.0) or 0.0) + atk_percent / 100.0
        if crit_bonus:
            # crit — read-only property, поэтому пишем в bonus_crit
            # (внутренний формат Pers: 1.20 = +20% крит.урона).
            char.bonus_crit = float(getattr(char, "bonus_crit", 0.0) or 0.0) + crit_bonus
        renpy.log("[Фабри][Неудержимость] снято дебаффов: {}".format(len(cleared)))
        return "Неудержимость: снято 2 стака дебаффов, +{0:.0f}% атаки".format(atk_percent)

    def fabri_magic_hit_harder(char):
        """«Бей сильнее!»: +30% магии Фабри к урону цели."""
        bonus_percent = 30.0
        # «Я тоже бей сильнее!» ур.8 добавляет урон самой Манки.
        if fabri_level() >= FABRI_UP_HIT_HARDER_TOO:
            bonus_percent += fabri_hit_harder_extra_percent()
        char.bonus_magic = float(getattr(char, "bonus_magic", 0.0) or 0.0) + bonus_percent / 100.0
        renpy.log("[Фабри][Бей сильнее!] +{:.0f}% магии Фабри".format(bonus_percent))
        return "Бей сильнее!: +{0:.0f}% магии Фабри к урону".format(bonus_percent)

    def fabri_magic_show_how(char):
        """«Я покажу, как бить!» (ур.10): бонусы М-с Манки от Фабри.

        По спецификации надбавка идёт ИМЕННО характеристикам
        М-с Манки (её урону, крит.урону и крит.шансу), а не Фабри.
        Фамильяры не хранят собственные bonus_*-поля, поэтому
        надбавка запоминается в состоянии Фабри и применяется в
        fabri_familiar_stats()/fabri_monkey_auto_attack().
        """
        if not fabri_monkey_show_how_active():
            return None
        # Надбавка = 40% от соответствующих значений Фабри.
        fabri_set("fabri_monkey_show_how", True)
        magic = float(getattr(char, "magic", 0) or 0.0)
        critrate = float(getattr(char, "critrate", 0.0) or 0.0)
        crit = float(getattr(char, "crit", 1.0) or 1.0)
        renpy.log("[Фабри][Я покажу, как бить] Манки: +40% магии ({:.1f}), "
                  "крит.шанса ({:.3f}) и крит.урона ({:.3f}) от Фабри".format(
                      magic * 0.4, critrate * 0.4, crit * 0.4))
        return "Я покажу, как бить!: бонусы М-с Манки +40% от Фабри"

    # --- Общие утилиты магии --------------------------------------

    def fabri_cooldown_rewind(char, amount):
        """Откатывает перезарядки способностей цели на amount.

        Используется «Разминающими танцами» ур.5: цель получает откат
        СВОИХ перезарядок. Таблица store.battle_ability_current_cds
        ключуется именами способностей, а владелец определяется общей
        функцией _battle_ability_owner() — свой список владельцев не
        заводим, чтобы не разошёлся с реестром.
        """
        if amount <= 0:
            return
        cds = getattr(store, "battle_ability_current_cds", None)
        if not isinstance(cds, dict):
            return
        target_name = getattr(char, "name", None)
        if not target_name:
            return
        for ability_name in list(cds.keys()):
            try:
                owner = _battle_ability_owner(ability_name)
            except Exception:
                owner = None
            if owner != target_name:
                continue
            value = cds.get(ability_name, 0)
            if isinstance(value, int) and value > 0:
                cds[ability_name] = max(0, value - amount)


    # ------------------------------------------------------------
    # 10) СОСТОЯНИЕ И СБРОС
    # ------------------------------------------------------------

    def fabri_init_battle_state():
        """Полная инициализация боевого состояния Фабри.

        ВСЕ поля, объявленные здесь, восстанавливаются в
        Pers.__setstate__ для совместимости со старыми сохранениями —
        список должен совпадать.
        """
        char = fabri_char()
        if char is None:
            return

        # --- Фамильяры ---
        char.fabri_familiar_queue = []      # до 2 призванных id
        char.fabri_familiar_hp = {}         # id -> текущее HP
        char.fabri_familiar_cd = {}         # id -> счётчик до сброса за раунд
        char.fabri_junior_alive = False     # М-р Пёрышко младший жив
        char.fabri_junior_hp = 0
        char.fabri_egg_turns = 0            # ходов до вылупления
        char.fabri_egg_owner = None
        char.fabri_attached_target = None   # цель «Прикрепиться»
        char.fabri_attached_active = False

        # --- Временные бонусы/эффекты магии фамильяров ---
        char.fabri_haste_stacks = 0
        char.fabri_haste_bonus = 0.0
        char.fabri_haste_turns = 0
        char.fabri_dodge_target = None
        char.fabri_dodge_turns = 0
        char.fabri_dodge_chance = 0.0

        # --- Пассивки ---
        char.fabri_food_types = []          # типы еды («Разнообразие»)
        char.fabri_free_summon_pending = False
        char.fabri_created_familiars_this_battle = 0
        char.fabri_inspiration_stacks = 0
        # «Я покажу, как бить!» ур.10: надбавка М-с Манки от Фабри.
        char.fabri_monkey_show_how = False

    def fabri_reset_battle_state():
        """Сброс боевого состояния при старте нового боя."""
        fabri_init_battle_state()

    def fabri_reset_battle_passives():
        """Сброс одноразовых пассивок (соглашение *_reset_battle_passives)."""
        char = fabri_char()
        if char is None:
            return
        char.fabri_free_summon_pending = False
        char.fabri_created_familiars_this_battle = 0
        char.fabri_inspiration_stacks = 0
        char.fabri_monkey_show_how = False
        char.fabri_food_types = []
        char.fabri_haste_stacks = 0
        char.fabri_haste_bonus = 0.0
        char.fabri_haste_turns = 0
        char.fabri_dodge_target = None
        char.fabri_dodge_turns = 0
        char.fabri_dodge_chance = 0.0
        char.fabri_attached_target = None
        char.fabri_attached_active = False
        fabri_clear_familiars()
