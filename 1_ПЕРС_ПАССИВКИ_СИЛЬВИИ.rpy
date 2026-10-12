# ============================================================
# СИЛЬВИЯ — дерево движений, комбинации танцев, пассивки
# ============================================================
#
# Согласно спецификации вся «магия» Сильвии — это танец.
# Игрок набирает последовательность движений (1 ход = 1 шаг).
# Когда набранная очередь совпадает с комбинацией одного из
# выбранных на бой танцев — исполняется эффект танца, очередь
# сбрасывается.
#
# Уровни движений — это ГЛУБИНА УЗЛА в дереве ветвления, а не
# уровень персонажа:
#    ур.1 — 2 движения   (Tombé, Plié)
#    ур.2 — 4 движения   (Glissade, Chassé, Passé, Relevé)
#    ур.3 — 8 движений
#    ур.4 — 16 движений
# Всего 30 движений.
#
# Движения открываются ПОСЛЕДОВАТЕЛЬНО по ходам Сильвии:
# после 1-го хода открывается ур.2, после 2-го — ур.3,
# после 3-го — ур.4, после 4-го прогресс сбрасывается в начало.
# Игроку при этом доступны ВСЕ уже открытые движения, вне
# зависимости от выбранного репертуара.
# ============================================================

# Движение, выбранное игроком на текущем ходу танца.
# Объявлено через default, чтобы SetVariable в экране выбора
# движения корректно его находил. Сбрасывается в лейбле
# sylvia_movement_is_done после обработки.
default sylvia_pending_move = None

init python:

    # ------------------------------------------------------------
    # 1) КОНСТАНТЫ
    # ------------------------------------------------------------

    # Стоимость одного движения: ровно 10% от МАКСИМАЛЬНОЙ маны
    # («Репертуар»). Текущая мана при расчёте не участвует.
    SYLVIA_MOVEMENT_MP_PERCENT = 0.10

    # Прогресс открытия уровней движений сбрасывается после
    # стольких ходов Сильвии.
    SYLVIA_TIER_PROGRESS_MAX = 4

    # Сколько танцев игрок выбирает в репертуар на бой.
    SYLVIA_REPERTOIRE_SIZE = 3

    # «Антракт»: длительность блокировки хода при обнулении маны.
    SYLVIA_ENTRACTE_DURATION = 3

    # «Ловкость в бою»: шанс уклонения = база + шаг*уровень (в %).
    SYLVIA_DODGE_BASE = 14.0
    SYLVIA_DODGE_PER_LEVEL = 1.5

    # «Пластика требует диеты»: шанс второго хода за стак здоровой еды.
    SYLVIA_HEALTHY_FOOD_SECOND_TURN_PERCENT = 2.0
    # Восстановление HP за каждую пустую позицию очереди аппетита (в конце хода).
    SYLVIA_EMPTY_FOOD_SLOT_HP_PERCENT = 2.0

    # «Без лишнего легче» (ур.2): +3% крит-шанса за каждый пустой слот артефакта.
    SYLVIA_EMPTY_ARTIFACT_CRIT_PERCENT = 3.0

    # «Диалог культур»: доля дипломатии, идущая в прогресс пощады.
    # По решению согласования снижено с 40% до 20%.
    SYLVIA_DIALOGUE_SPARE_PERCENT = 0.20

    # Порог уровня персонажа, при котором открывается окно выбора
    # репертуара. Ниже порога репертуар берётся автоматически.
    SYLVIA_REPERTOIRE_CHOICE_LEVEL = 4


    # ------------------------------------------------------------
    # 2) ДЕРЕВО ДВИЖЕНИЙ
    # ------------------------------------------------------------
    # Каждый элемент: (внутренний id, отображаемое имя, tier).
    # Порядок важен: он определяет, какие движения доступны на
    # каждом уровне прогресса.

    SYLVIA_MOVEMENTS = [
        # --- Ур.1 (2 движения) ---
        ("tombe",            "Томбе",                 1),
        ("plie",             "Плие",                  1),

        # --- Ур.2 (4 движения) ---
        ("glissade",         "Глиссада",              2),
        ("chasse",           "Шассе",                 2),
        ("passe",            "Пассе",                 2),
        ("releve",           "Релеве",                2),

        # --- Ур.3 (8 движений) ---
        ("changement",       "Шажман де пье",         3),
        ("echappe",          "Эшапе соте",            3),
        ("jete_entrelace",   "Жете антреласе",        3),
        ("saut_de_basque",   "Со де баск",            3),
        ("developpe",        "Девелоппе",             3),
        ("degage",           "Дегаже",                3),
        ("sus_sus",          "Сю-сю",                 3),
        ("battement_fondu",  "Батман фондю",          3),

        # --- Ур.4 (16 движений) ---
        ("temps_leve",       "Тан леве",              4),
        ("brise",            "Бризе",                 4),
        ("assemble",         "Ассамбле",              4),
        ("sissonne",         "Сиссон",                4),
        ("grand_jete",       "Гран жете",             4),
        ("cabriole",         "Кабриоль",              4),
        ("tour_en_lair",     "Тур ан лер",            4),
        ("pirouette",        "Пируэт а ля сэконд",    4),
        ("arabesque",        "Арабеск",               4),
        ("attitude",         "Аттитюд",               4),
        ("tour_lent",        "Тур лан",               4),
        ("fouette",          "Фуэте",                 4),
        ("pas_de_bourree",   "Па-де-бурре",           4),
        ("battement_soutenu","Батман сутеню",         4),
        ("temps_lie",        "Тан лье",               4),
        ("rond_de_jambe",    "Рон де жамб ан лер",    4),
    ]

    def sylvia_movement_name(move_id):
        """Возвращает отображаемое имя движения по внутреннему id."""
        for mid, label, _tier in SYLVIA_MOVEMENTS:
            if mid == move_id:
                return label
        return move_id

    def sylvia_movement_tier(move_id):
        """Возвращает уровень (глубину узла) движения по внутреннему id."""
        for mid, _label, tier in SYLVIA_MOVEMENTS:
            if mid == move_id:
                return tier
        return 0

    def sylvia_movements_up_to_tier(tier):
        """Список движений, доступных при заданном прогрессе открытия."""
        return [mid for mid, _label, mtier in SYLVIA_MOVEMENTS if mtier <= tier]

    def sylvia_all_movement_ids():
        return [mid for mid, _label, _tier in SYLVIA_MOVEMENTS]


    # ------------------------------------------------------------
    # 3) ТАНЦЫ И ИХ КОМБИНАЦИИ
    # ------------------------------------------------------------
    # Комбинации взяты дословно из спецификации. Каждый танец —
    # это последовательность движений, которую игрок набирает.

    SYLVIA_DANCES = {
        "kitri": {
            "name": "Каприз Китри",
            "combo": ["plie", "releve", "degage", "fouette"],
            "desc": "Даёт Сильвии +1 щит.",
        },
        "dulcinea": {
            "name": "Видение Дульсинеи",
            "combo": ["tombe", "chasse", "saut_de_basque", "grand_jete"],
            "desc": "Следующая атака всех союзников нанесёт на 30% больше.",
        },
        "solor": {
            "name": "Тень Солора",
            "combo": ["tombe", "passe", "developpe", "attitude"],
            "desc": "Накладывает бафф «Тень Солора» (x2). Персонажи не могут "
                    "ходить, но восстанавливают 20% HP и маны за ход. Танк = 0.",
        },
        "bluebird": {
            "name": "Синяя птица",
            "combo": ["plie", "glissade", "echappe", "brise"],
            "desc": "Накладывает на команду «Крылья птицы» (x3). Атаки команды "
                    "наносят дополнительно 50% урона от магии.",
        },
        "gisele": {
            "name": "Дыхание Жизели",
            "combo": ["plie", "releve", "developpe", "arabesque"],
            "desc": "Снимает все дебаффы страха с союзников, восстанавливает "
                    "15% HP и даёт всей команде 20% защиты.",
        },
        "desire": {
            "name": "Кавалерский круг Дезире",
            "combo": ["tombe", "chasse", "saut_de_basque", "tour_en_lair"],
            "desc": "Умножает бонусный крит-урон персонажа с самым высоким "
                    "значением на 1.5.",
        },
        "amur": {
            "name": "Искры Амура",
            "combo": ["plie", "glissade", "changement", "temps_leve"],
            "desc": "Накладывает на команду «Пламя Амура» (x4). Каждый персонаж "
                    "наносит всем противникам 40% урона от своей магии.",
        },
        "spartacus": {
            "name": "Винт Спартака",
            "combo": ["tombe", "chasse", "jete_entrelace", "pirouette"],
            "desc": "Даёт всей команде прибавку к бонусной атаке. Все персонажи "
                    "наносят всем противникам урон = 30% от текущей атаки.",
        },
        "gamzatti": {
            "name": "Динамика Гамзатти",
            "combo": ["tombe", "glissade", "echappe", "cabriole"],
            "desc": "Накладывает всем персонажам точность x4.",
        },
        "swan": {
            "name": "Кантилена Белого лебедя",
            "combo": ["plie", "releve", "battement_fondu", "temps_lie"],
            "desc": "Сбрасывает все штрафные характеристики и дебаффы, "
                    "восстанавливает 30% HP всей команде.",
        },
    }

    def sylvia_dance_name(dance_id):
        return SYLVIA_DANCES.get(dance_id, {}).get("name", dance_id)

    def sylvia_dance_combo(dance_id):
        return list(SYLVIA_DANCES.get(dance_id, {}).get("combo", []))

    def sylvia_all_dance_ids():
        return list(SYLVIA_DANCES.keys())

    def sylvia_dances_for_level(level):
        """
        Репертуар по умолчанию, когда окно выбора недоступно
        (уровень персонажа ниже порога). Берутся три первых танца.
        """
        ids = sylvia_all_dance_ids()
        return ids[:SYLVIA_REPERTOIRE_SIZE]


    # ------------------------------------------------------------
    # 4) СОСТОЯНИЕ СИЛЬВИИ
    # ------------------------------------------------------------
    # Хранится в объекте персонажа. Поля рассчитаны на то, чтобы
    # отсутствовать в старых сохранениях, поэтому чтение — через
    # sylvia_get() с безопасным значением по умолчанию.

    def sylvia_char():
        """Возвращает объект персонажа Сильвии или None."""
        pers = getattr(store, "pers_dict", None) or {}
        return pers.get("Сильвия")

    def sylvia_get(field, default=0):
        """Безопасное чтение поля состояния Сильвии (для старых сохранений)."""
        char = sylvia_char()
        if char is None:
            return default
        return getattr(char, field, default)

    def sylvia_set(field, value):
        """Запись поля состояния Сильвии."""
        char = sylvia_char()
        if char is not None:
            setattr(char, field, value)

    def sylvia_init_battle_state():
        """
        Инициализирует/сбрасывает боевое состояние Сильвии.
        Вызывается при создании персонажа и в начале каждого боя.
        """
        char = sylvia_char()
        if char is None:
            return

        # Очередь набранных движений (внутренние id).
        char.sylvia_queue = []
        # Выбранный на бой репертуар (до 3 танцев).
        char.sylvia_repertoire = []
        # Признак, что репертуар уже выбран в этом бою.
        char.sylvia_repertoire_chosen = False
        # Уже исполненные в этом бою танцы (повтор запрещён).
        char.sylvia_dances_used = []
        # Прогресс открытия уровней движений: 1..4, сбрасывается по достижении 4.
        char.sylvia_tier_progress = 1
        # Счётчик ходов Сильвии в текущем цикле прогресса.
        char.sylvia_progress_steps = 0
        # Стаки дебаффа «Антракт».
        char.sylvia_entracte = 0
        # Накопленный бонус танка от «Раскрываясь в свете прожекторов».
        char.sylvia_spotlight_tank = 0
        # Крылья птицы / Пламя Амура / Тень Солора / точность — счётчики ходов.
        char.sylvia_wings = 0
        char.sylvia_amur_flame = 0
        char.sylvia_solor_shadow = 0
        char.sylvia_precision_stacks = 0
        # Бонус следующей атаки команды («Видение Дульсинеи») хранится в
        # штатном поле Pers.next_attack_multiplier — второго поля не заводим,
        # чтобы не дублировать одно состояние в двух местах.
        # Проверка на «Важность исполнения» в текущем действии.
        char.sylvia_last_check_failed = False
        char.sylvia_last_check_crit = False
        # Число исполненных движений за бой (для «Диалога культур» и статистики).
        char.sylvia_movements_this_battle = 0
        # Флаг, что в этом ходу уже сработала защита от «Своей очереди».
        char.sylvia_initiative_applied = False
        # Кто был по очереди в этом раунде: "first" или "last".
        char.sylvia_last_initiative = None
        # Счётчик бесплатных движений «Пластики и выносливости» (ур.3);
        # каждый следующий ход повышает шанс на 0.2.
        char.sylvia_free_move_steps = 0
        # Резерв танка на время «Тени Солора» (танк обнуляется, потом возвращается).
        char.sylvia_solor_saved_tank = 0.0


    # ------------------------------------------------------------
    # 5) СБРОС СОСТОЯНИЯ НА НОВЫЙ БОЙ
    # ------------------------------------------------------------

    def sylvia_reset_battle_state():
        """Полный сброс боевого состояния Сильвии при старте боя."""
        sylvia_init_battle_state()

    def sylvia_reset_battle_passives():
        """
        Сброс одноразовых пассивок на новый бой.
        Отдельная функция, чтобы соответствовать соглашению проекта
        (*_reset_battle_passives), вызываемому из fightbegin12.
        """
        char = sylvia_char()
        if char is None:
            return
        char.sylvia_entracte = 0
        char.sylvia_spotlight_tank = 0
        char.sylvia_wings = 0
        char.sylvia_amur_flame = 0
        char.sylvia_solor_shadow = 0
        char.sylvia_precision_stacks = 0
        char.sylvia_dances_used = []
        char.sylvia_repertoire = []
        char.sylvia_repertoire_chosen = False
        char.sylvia_tier_progress = 1
        char.sylvia_progress_steps = 0
        char.sylvia_movements_this_battle = 0


    # ------------------------------------------------------------
    # 6) ПРОВЕРКИ «ВАЖНОСТЬ ИСПОЛНЕНИЯ»
    # ------------------------------------------------------------
    # Каждое действие Сильвии проходит проверку на точность и крит-шанс.
    #   провал точности  -> эффекты движения делятся на 2 (вниз)
    #   успешный крит    -> эффекты движения множатся на 1.5 (вверх)
    # Проверка происходит автоматически при использовании движения.

    def sylvia_roll_accuracy():
        """
        Бросок точности. Возвращает True, если проверка ПРОЙДЕНА.
        Использует dmgchance персонажа (точность в долях единицы).
        """
        char = sylvia_char()
        if char is None:
            return True
        chance = float(getattr(char, "dmgchance", 0.0) or 0.0)
        # Точность хранится как доля (0..1). Сравниваем с броском.
        return renpy.random.random() <= max(0.0, min(1.0, chance))

    def sylvia_roll_crit():
        """Бросок крит-шанса. Возвращает True при успешном крите."""
        char = sylvia_char()
        if char is None:
            return False
        chance = float(getattr(char, "critrate", 0.0) or 0.0)
        return renpy.random.random() <= max(0.0, min(1.0, chance))

    def sylvia_roll_performance():
        """
        Выполняет проверки «Важности исполнения» для текущего движения
        и СОХРАНЯЕТ результат в состоянии, чтобы эффекты танца могли
        применить множитель через sylvia_performance_modifier().

        Провал точности -> эффекты движения делятся на 2 (округление вниз).
        Успешный крит  -> эффекты движения умножаются на 1.5 (округление вверх).
        Вызывается в начале обработки хода Сильвии.
        """
        char = sylvia_char()
        if char is None:
            return 1.0
        failed = not sylvia_roll_accuracy()
        crit = sylvia_roll_crit()
        char.sylvia_last_check_failed = failed
        char.sylvia_last_check_crit = crit
        if failed:
            renpy.log("Сильвия: «Важность исполнения» — провал точности, эффекты /2")
        if crit:
            renpy.log("Сильвия: «Важность исполнения» — крит, эффекты x1.5")
        return sylvia_performance_modifier()

    def sylvia_apply_performance_check(base_value):
        """
        Применяет к базовому значению эффекта проверки «Важность исполнения».
        Провал точности -> /2 с округлением вниз.
        Успешный крит  -> *1.5 с округлением вверх.
        Возвращает (итоговое_значение, провал, крит).
        """
        char = sylvia_char()
        failed = not sylvia_roll_accuracy()
        crit = sylvia_roll_crit()

        if char is not None:
            char.sylvia_last_check_failed = failed
            char.sylvia_last_check_crit = crit

        value = float(base_value)
        if failed:
            value = float(math.floor(value / 2.0))
        if crit:
            value = float(math.ceil(value * 1.5))
        return value, failed, crit

    def sylvia_performance_modifier():
        """
        Возвращает множитель эффектов движения от «Важности исполнения».
        Удобно для тех эффектов, где деление/умножение применяется целиком.
        """
        m = 1.0
        if sylvia_get("sylvia_last_check_failed", False):
            m *= 0.5
        if sylvia_get("sylvia_last_check_crit", False):
            m *= 1.5
        return m


    # ------------------------------------------------------------
    # 7) СТОИМОСТЬ И ОПЛАТА МАНЫ
    # ------------------------------------------------------------
    # «Репертуар»: каждое движение тратит ровно 10% от МАКСИМАЛЬНОЙ маны.

    def sylvia_movement_cost():
        """Стоимость одного движения в единицах маны."""
        char = sylvia_char()
        if char is None:
            return 0
        max_mp = int(getattr(char, "max_mp", 0) or 0)
        return int(round(max_mp * SYLVIA_MOVEMENT_MP_PERCENT))

    def sylvia_can_afford_movement():
        """Хватает ли маны на одно движение."""
        char = sylvia_char()
        if char is None:
            return False
        return int(getattr(char, "current_mp", 0) or 0) >= sylvia_movement_cost()

    def sylvia_pay_movement_cost():
        """
        Списывает ману за движение.
        Возвращает True при успешной оплате, False при нехватке.
        """
        char = sylvia_char()
        if char is None:
            return False
        cost = sylvia_movement_cost()
        if int(getattr(char, "current_mp", 0) or 0) < cost:
            return False
        char.current_mp = max(0, int(char.current_mp) - cost)
        return True

    def sylvia_mp_empty():
        """Проверка обнуления маны — условие наложения «Антракта»."""
        char = sylvia_char()
        if char is None:
            return False
        return int(getattr(char, "current_mp", 0) or 0) <= 0


    # ------------------------------------------------------------
    # 8) ОЧЕРЕДЬ ДВИЖЕНИЙ И РАСПОЗНАВАНИЕ ТАНЦА
    # ------------------------------------------------------------

    def sylvia_queue():
        """Текущая очередь движений (список внутренних id)."""
        return list(sylvia_get("sylvia_queue", []) or [])

    def sylvia_queue_names():
        """Очередь в отображаемых именах — для интерфейса."""
        return [sylvia_movement_name(mid) for mid in sylvia_queue()]

    def sylvia_clear_queue(reason=None):
        """
        Сбрасывает очередь движений.
        Вызывается при получении урона (комбинация сбита), если не
        сработала пассивка «Не сбиваясь с Ритма», а также после
        успешного исполнения танца.
        """
        sylvia_set("sylvia_queue", [])
        if reason:
            renpy.log(f"Сильвия: очередь движений сброшена ({reason})")

    def sylvia_push_movement(move_id):
        """Добавляет движение в очередь и возвращает новую очередь."""
        queue = sylvia_queue()
        queue.append(move_id)
        sylvia_set("sylvia_queue", queue)
        return queue

    def sylvia_match_dance():
        """
        Проверяет, совпадает ли текущая очередь с комбинацией одного
        из выбранных в репертуар танцев.

        Возвращает id танца или None. Танец должен быть:
          - выбран в репертуаре;
          - ещё не исполнен в этом бою («один и тот же танец — 1 раз»).
        """
        queue = sylvia_queue()
        if not queue:
            return None

        repertoire = list(sylvia_get("sylvia_repertoire", []) or [])
        used = list(sylvia_get("sylvia_dances_used", []) or [])

        for dance_id in repertoire:
            if dance_id in used:
                continue
            combo = sylvia_dance_combo(dance_id)
            if combo and queue == combo:
                return dance_id
        return None

    def sylvia_partial_match_exists():
        """
        Есть ли среди выбранных танцев такой, чья комбинация ещё может
        продолжиться от текущей очереди. Нужно, чтобы показать игроку,
        что комбинация ещё «жива».
        """
        queue = sylvia_queue()
        if not queue:
            return True

        repertoire = list(sylvia_get("sylvia_repertoire", []) or [])
        used = list(sylvia_get("sylvia_dances_used", []) or [])

        for dance_id in repertoire:
            if dance_id in used:
                continue
            combo = sylvia_dance_combo(dance_id)
            if len(queue) <= len(combo) and combo[:len(queue)] == queue:
                return True
        return False

    def sylvia_mark_dance_used(dance_id):
        """Помечает танец исполненным в этом бою."""
        used = list(sylvia_get("sylvia_dances_used", []) or [])
        if dance_id not in used:
            used.append(dance_id)
        sylvia_set("sylvia_dances_used", used)


    # ------------------------------------------------------------
    # 9) ПРОГРЕСС ОТКРЫТИЯ УРОВНЕЙ ДВИЖЕНИЙ
    # ------------------------------------------------------------
    # После каждого хода Сильвии открывается следующий уровень.
    # После 4-го хода прогресс сбрасывается к началу.

    def sylvia_current_tier():
        """Текущий доступный уровень движений (1..4)."""
        return int(sylvia_get("sylvia_tier_progress", 1) or 1)

    def sylvia_available_movements():
        """Список доступных сейчас движений."""
        return sylvia_movements_up_to_tier(sylvia_current_tier())

    def sylvia_advance_tier_progress():
        """
        Вызывается в конце хода Сильвии. Открывает следующий уровень,
        а после 4 шагов сбрасывает прогресс в начало.
        """
        steps = int(sylvia_get("sylvia_progress_steps", 0) or 0) + 1
        tier = int(sylvia_get("sylvia_tier_progress", 1) or 1) + 1

        if steps >= SYLVIA_TIER_PROGRESS_MAX or tier > 4:
            # Цикл завершён — начинаем заново с первого уровня.
            sylvia_set("sylvia_progress_steps", 0)
            sylvia_set("sylvia_tier_progress", 1)
        else:
            sylvia_set("sylvia_progress_steps", steps)
            sylvia_set("sylvia_tier_progress", min(4, tier))

    def sylvia_on_movement_made():
        """Учёт выполненного движения: прогресс уровней и статистика боя."""
        char = sylvia_char()
        if char is not None:
            char.sylvia_movements_this_battle = int(
                getattr(char, "sylvia_movements_this_battle", 0) or 0) + 1
        sylvia_advance_tier_progress()


    # ------------------------------------------------------------
    # 10) ПАССИВКА «АНТРАКТ» (ур.1)
    # ------------------------------------------------------------
    # В начале каждого хода проверяется мана. Если она равна 0 —
    # на Сильвию накладывается дебафф «Антракт». Пока он активен,
    # в начале каждого хода её turn становится 0 (она не ходит).
    # Сбрасывается 1 стак в конце хода.

    def sylvia_tick_entracte_start():
        """
        Вызывается в начале хода. Если мана обнулилась — накладывает
        «Антракт» и блокирует ход. Возвращает True, если ход заблокирован.
        """
        char = sylvia_char()
        if char is None:
            return False

        # Если мана пуста и Антракт ещё не наложен — накладываем.
        if sylvia_mp_empty() and int(getattr(char, "sylvia_entracte", 0) or 0) <= 0:
            char.sylvia_entracte = SYLVIA_ENTRACTE_DURATION
            renpy.log("Сильвия: мана исчерпана — наложен «Антракт»")

        # Пока Антракт висит — блокируем ход.
        if int(getattr(char, "sylvia_entracte", 0) or 0) > 0:
            char.turn = 0
            return True
        return False

    def sylvia_tick_entracte_end():
        """
        Вызывается в конце хода. Уменьшает «Антракт» на 1 и, когда он
        спадает, восстанавливает Сильвии всю ману (она «отдохнула»).
        """
        char = sylvia_char()
        if char is None:
            return

        stacks = int(getattr(char, "sylvia_entracte", 0) or 0)
        if stacks <= 0:
            return

        stacks -= 1
        char.sylvia_entracte = stacks

        if stacks <= 0:
            char.current_mp = int(getattr(char, "max_mp", 0) or 0)
            renpy.log("Сильвия: «Антракт» завершён, мана восстановлена")


    # ------------------------------------------------------------
    # 11) ПАССИВКА «ЛОВКОСТЬ В БОЮ» (ур.1)
    # ------------------------------------------------------------
    # При получении урона Сильвия имеет шанс уклониться полностью.
    # Работает только когда целью атаки является сама Сильвия.
    # Шанс = 14% + 1.5% * уровень.

    def sylvia_dodge_chance():
        """Шанс полного уклонения Сильвии в процентах."""
        level = sylvia_level()
        return SYLVIA_DODGE_BASE + SYLVIA_DODGE_PER_LEVEL * max(0, int(level))

    def sylvia_try_dodge(target_char):
        """
        Попытка уклонения при получении урона.
        Возвращает True, если урон полностью избегнут.
        Вызывается из общего пути нанесения урона, когда цель — Сильвия.
        """
        if target_char is None or getattr(target_char, "name", None) != "Сильвия":
            return False
        if target_char.current_hp <= 0:
            return False

        chance = sylvia_dodge_chance()
        roll = renpy.random.random() * 100.0
        if roll <= chance:
            renpy.log(f"Сильвия: уклонение сработало ({roll:.1f} <= {chance:.1f})")
            # «Вдохновение танцем» (ур.7): восстановление 20% маны при уклонении.
            sylvia_on_dodge()
            return True
        return False

    def sylvia_on_dodge():
        """Обработчик успешного уклонения: пассивки, зависящие от него."""
        char = sylvia_char()
        if char is None:
            return
        # «Вдохновение танцем» (ур.7)
        if sylvia_level() >= 7:
            max_mp = int(getattr(char, "max_mp", 0) or 0)
            restore = int(max_mp * 0.20)
            char.current_mp = min(max_mp, int(getattr(char, "current_mp", 0) or 0) + restore)
            renpy.log(f"Сильвия: «Вдохновение танцем» восстановило {restore} маны")


    # ------------------------------------------------------------
    # 12) ПАССИВКА «НЕ СБИВАЯСЬ С РИТМА» (ур.4)
    # ------------------------------------------------------------
    # Урон по Сильвии не сбивает комбинацию с шансом = 2.5 * уровень.

    def sylvia_keep_combo_chance():
        """Шанс сохранить комбинацию при получении урона, в процентах."""
        return 2.5 * sylvia_level()

    def sylvia_on_damage_received(amount=0):
        """
        Обработчик получения урона Сильвией.
        Сбивает очередь движений, если не сработала «Не сбиваясь с Ритма».
        Возвращает True, если комбинация сохранена.
        """
        char = sylvia_char()
        if char is None:
            return False

        # «Раскрываясь в свете прожекторов» (ур.1): бонус танка сбрасывается уроном.
        sylvia_spotlight_reset()

        # «Не сбиваясь с Ритма» (ур.4): шанс сохранить комбинацию.
        if sylvia_level() >= 4:
            chance = sylvia_keep_combo_chance()
            if renpy.random.random() * 100.0 <= chance:
                renpy.log("Сильвия: «Не сбиваясь с Ритма» сохранила комбинацию")
                return True

        sylvia_clear_queue("получен урон")
        return False


    # ------------------------------------------------------------
    # 13) ПАССИВКА «РАСКРЫВАЯСЬ В СВЕТЕ ПРОЖЕКТОРОВ» (ур.1)
    # ------------------------------------------------------------
    # С каждым движением +2 танк. Урон сбрасывает накопленный бонус.

    def sylvia_spotlight_on_movement():
        """Начисляет +2 танка за выполненное движение."""
        char = sylvia_char()
        if char is None:
            return
        char.sylvia_spotlight_tank = int(
            getattr(char, "sylvia_spotlight_tank", 0) or 0) + 2
        # Бонус танка влияет на получаемый урон — увеличиваем bonus_tank.
        char.bonus_tank = int(getattr(char, "bonus_tank", 0) or 0) + 2

    def sylvia_spotlight_reset():
        """Сбрасывает накопленный бонус танка от прожекторов."""
        char = sylvia_char()
        if char is None:
            return
        accumulated = int(getattr(char, "sylvia_spotlight_tank", 0) or 0)
        if accumulated:
            char.bonus_tank = max(0, int(getattr(char, "bonus_tank", 0) or 0) - accumulated)
        char.sylvia_spotlight_tank = 0


    # ------------------------------------------------------------
    # 14) ПАССИВКА «СВОЯ ОЧЕРЕДЬ» (ур.1)
    # ------------------------------------------------------------
    # Первой в раунде  -> +4% / +6% / +8% бонусной защиты
    #                     (уровни 1–3 / 4–6 / 7–10)
    # Последней        -> +5% / +9% / +14% бонусного крит-шанса в ходу
    # Вызывается из лейбла начала хода персонажа.

    def sylvia_initiative_def_bonus():
        """Бонус защиты (в процентах), если Сильвия ходит первой в раунде."""
        level = sylvia_level()
        if level <= 3:
            return 4.0
        if level <= 6:
            return 6.0
        return 8.0

    def sylvia_initiative_crit_bonus():
        """Бонус крит-шанса (в процентах), если Сильвия ходит последней."""
        level = sylvia_level()
        if level <= 3:
            return 5.0
        if level <= 6:
            return 9.0
        return 14.0

    def sylvia_count_available_heroes():
        """
        Возвращает число героев, которые ещё могут действовать
        в этом раунде (не израсходовали ход и живы).
        """
        pers = getattr(store, "pers_dict", None) or {}
        count = 0
        for char in pers.values():
            if getattr(char, "picked", 0) != 1:
                continue
            if getattr(char, "current_hp", 0) <= 0:
                continue
            if getattr(char, "turn", 0) == 1:
                count += 1
        return count

    def sylvia_apply_initiative():
        """
        Применяет эффект «Своей очереди» в начале хода Сильвии.
        Возвращает строку-описание применённого эффекта или None.
        """
        char = sylvia_char()
        if char is None:
            return None
        if getattr(char, "sylvia_initiative_applied", False):
            return None

        char.sylvia_initiative_applied = True

        # Ходит первой: кроме неё в раунде больше никто не действовал.
        others_available = sylvia_count_available_heroes()
        # Если доступна только она одна — считается первой.
        if others_available <= 1:
            bonus = sylvia_initiative_def_bonus()
            # bonus_def — МНОЖИТЕЛЬ к базовой защите (Pers.defense:
            # base_def * bonus_def), поэтому проценты переводим в доли.
            char.bonus_def = float(getattr(char, "bonus_def", 0.0) or 0.0) + (bonus / 100.0)
            char.sylvia_last_initiative = "first"
            renpy.log(f"Сильвия: «Своя очередь» — первая, +{bonus}% защиты")
            return "first"

        # Последней в раунде: все остальные уже сходили.
        bonus = sylvia_initiative_crit_bonus()
        # critrate_mod — аддитивная добавка к крит-шансу в долях,
        # поэтому проценты делим на 100.
        char.critrate_mod = float(getattr(char, "critrate_mod", 0.0) or 0.0) + (bonus / 100.0)
        char.sylvia_last_initiative = "last"
        renpy.log(f"Сильвия: «Своя очередь» — последняя, +{bonus}% крит-шанса")
        return "last"


    # ------------------------------------------------------------
    # 15) ПАССИВКА «ПЛАСТИКА ТРЕБУЕТ ДИЕТЫ» (ур.1)
    # ------------------------------------------------------------
    # Здоровой считается еда типа "healthy" (зелёная в очереди аппетита).

    def sylvia_healthy_food_stacks():
        """Число стаков здоровой еды в очереди аппетита Сильвии."""
        char = sylvia_char()
        if char is None:
            return 0
        queue = getattr(char, "feedness_queue", None) or []
        count = 0
        for item_id in queue:
            if item_id is None:
                continue
            if store.consumable_food_types.get(item_id, "other") == "healthy":
                count += 1
        return count

    def sylvia_empty_food_slots():
        """Число пустых позиций в очереди аппетита."""
        char = sylvia_char()
        if char is None:
            return 0
        queue = getattr(char, "feedness_queue", None) or []
        return sum(1 for x in queue if x is None)

    def sylvia_roll_second_turn():
        """Шанс сделать второй ход за каждый стак здоровой еды."""
        stacks = sylvia_healthy_food_stacks()
        if stacks <= 0:
            return False
        chance = stacks * SYLVIA_HEALTHY_FOOD_SECOND_TURN_PERCENT
        return renpy.random.random() * 100.0 <= chance

    def sylvia_end_turn_food_regen():
        """Восстанавливает 2% HP за каждую пустую позицию очереди аппетита."""
        char = sylvia_char()
        if char is None:
            return
        empty = sylvia_empty_food_slots()
        if empty <= 0:
            return
        max_hp = int(getattr(char, "max_hp", 0) or 0)
        heal = int(max_hp * SYLVIA_EMPTY_FOOD_SLOT_HP_PERCENT / 100.0 * empty)
        if heal > 0:
            char.current_hp = min(max_hp, int(getattr(char, "current_hp", 0) or 0) + heal)


    # ------------------------------------------------------------
    # 16) ПАССИВКА «БЕЗ ЛИШНЕГО ЛЕГЧЕ» (ур.2)
    # ------------------------------------------------------------
    # +3% крит-шанса за каждый пустой слот артефакта, в начале боя.

    def sylvia_empty_artifact_slots():
        """Число пустых слотов артефактов."""
        char = sylvia_char()
        if char is None:
            return 0
        try:
            max_slots = char.get_max_slots()
        except Exception:
            max_slots = 0
        equipped = [a for a in (getattr(char, "equipped_artifacts", []) or []) if a is not None]
        return max(0, int(max_slots) - len(equipped))

    def sylvia_apply_empty_artifact_bonus():
        """Начисляет крит-шанс за пустые слоты артефактов в начале боя."""
        char = sylvia_char()
        if char is None:
            return
        if sylvia_level() < 2:
            return
        empty = sylvia_empty_artifact_slots()
        bonus = empty * SYLVIA_EMPTY_ARTIFACT_CRIT_PERCENT / 100.0
        if bonus > 0:
            char.critrate_mod = float(getattr(char, "critrate_mod", 0.0) or 0.0) + bonus
            renpy.log(f"Сильвия: «Без лишнего легче» +{bonus*100:.0f}% крит-шанса "
                      f"({empty} пустых слотов)")


    # ------------------------------------------------------------
    # 17) ПАССИВКА «ПЛАСТИКА И ВЫНОСЛИВОСТЬ» (ур.3)
    # ------------------------------------------------------------
    # Шанс не потратить ману при движении: крит-шанс*0.5 + уровень.
    # С каждым ходом он увеличивается на 0.2.

    def sylvia_free_movement_chance():
        """Шанс не потратить ману, в процентах."""
        char = sylvia_char()
        if char is None:
            return 0.0
        crit = float(getattr(char, "critrate", 0.0) or 0.0) * 100.0
        base = crit * 0.5 + sylvia_level()
        steps = int(getattr(char, "sylvia_free_move_steps", 0) or 0)
        return base + steps * 0.2

    def sylvia_roll_free_movement():
        """Проверка на бесплатное движение (ур.3+)."""
        if sylvia_level() < 3:
            return False
        chance = sylvia_free_movement_chance()
        ok = renpy.random.random() * 100.0 <= chance
        if ok:
            char = sylvia_char()
            if char is not None:
                char.sylvia_free_move_steps = int(
                    getattr(char, "sylvia_free_move_steps", 0) or 0) + 1
            renpy.log(f"Сильвия: «Пластика и выносливость» — мана не потрачена ({chance:.1f}%)")
        return ok


    # ------------------------------------------------------------
    # 18) ПАССИВКА «ДИАЛОГ КУЛЬТУР» (ур.5)
    # ------------------------------------------------------------
    # Каждое выполненное движение даёт 20% дипломатии Сильвии
    # в прогресс пощады каждого противника, с шансом = крит-шанс.
    # (По решению согласования ставка снижена с 40% до 20%.)

    def sylvia_dialogue_cultures():
        """Применяет «Диалог культур» после выполненного движения."""
        if sylvia_level() < 5:
            return
        char = sylvia_char()
        if char is None:
            return

        # Шанс срабатывания равен крит-шансу Сильвии.
        if renpy.random.random() > float(getattr(char, "critrate", 0.0) or 0.0):
            return

        diplomacy = int(getattr(char, "diplomacy", 0) or 0)
        progress = diplomacy * SYLVIA_DIALOGUE_SPARE_PERCENT
        if progress <= 0:
            return

        # Только живые активные противники текущего боя.
        for enemy in sylvia_living_enemies():
            if getattr(enemy, "dead", False):
                continue
            if getattr(enemy, "current_hp", 0) <= 0:
                continue
            current = getattr(enemy, "spare_progress", 0) or 0
            spare_max = getattr(enemy, "spare_max", 0) or 0
            enemy.spare_progress = min(spare_max, current + progress) if spare_max else current + progress


    # ------------------------------------------------------------
    # 19) ПАССИВКА «ИСКУССТВО ДЛЯ СЕБЯ» (ур.9)
    # ------------------------------------------------------------
    # Все баффы, которые Сильвия даёт союзникам, она получает и сама,
    # но на 30% сильнее. Реализуется через коэффициент ниже; вызывается
    # из лейблов танцев, когда применяется командный бафф.

    def sylvia_self_buff_multiplier():
        """Множитель собственного баффа от «Искусства для себя»."""
        if sylvia_level() < 9:
            return 0.0
        return 1.3


    # ------------------------------------------------------------
    # 20) ПАССИВКА «ГРОМКИЙ ФИНАЛ» (ур.10)
    # ------------------------------------------------------------
    # Шанс = крит-шанс нанести эффекты танца дважды.

    def sylvia_roll_loud_finale():
        """Проверка удвоения эффектов танца (ур.10)."""
        if sylvia_level() < 10:
            return False
        char = sylvia_char()
        if char is None:
            return False
        ok = renpy.random.random() <= float(getattr(char, "critrate", 0.0) or 0.0)
        if ok:
            renpy.log("Сильвия: «Громкий финал» — эффекты танца удвоены")
        return ok


    # ------------------------------------------------------------
    # 21) УРОВЕНЬ ПЕРСОНАЖА
    # ------------------------------------------------------------
    # Источник уровня централизован в одном хелпере, как требует
    # методичка: пассивки читают уровень только отсюда.

    def sylvia_level():
        """Уровень персонажа Сильвии (глобальный уровень развития)."""
        return int(getattr(store.Pers, "global_level", 1) or 1)
