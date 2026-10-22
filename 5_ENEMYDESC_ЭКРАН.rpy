# Экран описания врага (enemydesc)

# Тестовые особенности врагов.
# Можно позже перенести в отдельный файл/логику, но по задаче достаточно хранить прямо в экране.


default enemy_desc_fallback_traits = ["closed", "agreeable"]

default enemy_desc_target = None

init python:
    def enemydesc_bonus_text(value, percent=False):
        """Возвращает строку для бонуса или '' если отображаемое значение == 0."""
        try:
            value = float(value)
        except Exception:
            return ""

        if percent:
            n = int(round(value * 100))
            if n == 0:
                return ""
            return "{:+d}%".format(n)
        else:
            n = int(round(value))
            if n == 0:
                return ""
            return "{:+d}".format(n)

    def enemydesc_bonus_is_nonzero(bonus_text):
        """True, если в строке бонуса НЕ ноль. Иначе — прячем текст, оставляя только иконку."""
        if not bonus_text:
            return False
        s = str(bonus_text).strip().replace("%", "")
        try:
            return float(s) != 0.0
        except Exception:
            return True

    def enemy_desc_format_number(value):
        try:
            number = float(value)
        except (TypeError, ValueError):
            return str(value)

        rounded = round(number, 2)
        if abs(rounded - int(rounded)) < 0.001:
            return str(int(rounded))
        return ("{:.2f}".format(rounded)).rstrip("0").rstrip(".")

    def enemy_desc_build_stat_formulas(enemy):
        if enemy is None:
            return []

        atk_base = enemy.base_atk + enemy.base_atk_mod
        def_base = enemy.base_def + enemy.base_def_mod
        mag_base = enemy.base_magic + enemy.base_magic_mod

        return [
            (
                "ATK",
                "{0} = max(({1} + {2}) * {3} * {4}, 0) = max({5} * {3} * {4}, 0)".format(
                    enemy_desc_format_number(enemy.atk),
                    enemy_desc_format_number(enemy.base_atk),
                    enemy_desc_format_number(enemy.base_atk_mod),
                    enemy_desc_format_number(enemy.bonus_atk2),
                    enemy_desc_format_number(enemy.atk_debuff_var),
                    enemy_desc_format_number(atk_base),
                ),
            ),
            (
                "DEF",
                "{0} = max(({1} + {2}) * {3} * {4}, 0) = max({5} * {3} * {4}, 0)".format(
                    enemy_desc_format_number(enemy.armor),
                    enemy_desc_format_number(enemy.base_def),
                    enemy_desc_format_number(enemy.base_def_mod),
                    enemy_desc_format_number(enemy.bonus_def),
                    enemy_desc_format_number(enemy.def_debuff_var),
                    enemy_desc_format_number(def_base),
                ),
            ),
            (
                "MAG",
                "{0} = max(({1} + {2}) * {3} * {4}, 0)".format(
                    enemy_desc_format_number(enemy.magic),
                    enemy_desc_format_number(enemy.base_magic),
                    enemy_desc_format_number(enemy.base_magic_mod),
                    enemy_desc_format_number(enemy.bonus_magic2),
                    enemy_desc_format_number(enemy.magic_debuff_var),
                ),
            ),
            (
                "HIT",
                "{0} = max({1} + {2} + {3}, 0)".format(
                    enemy_desc_format_number(enemy.dmgchance),
                    enemy_desc_format_number(enemy.base_dmgchance),
                    enemy_desc_format_number(enemy.bonus_dmgchance2),
                    enemy_desc_format_number(enemy.accuracy_debuff_var),
                ),
            ),
            (
                "CRIT%",
                "{0} = max({1} + {2} + {3}, 0)".format(
                    enemy_desc_format_number(enemy.critrate),
                    enemy_desc_format_number(enemy.base_critrate),
                    enemy_desc_format_number(enemy.bonus_critrate2),
                    enemy_desc_format_number(enemy.critrate_debuff_var),
                ),
            ),
            (
                "CRIT DMG",
                "{0} = max({1} + {2} + {3}, 0)".format(
                    enemy_desc_format_number(enemy.crit),
                    enemy_desc_format_number(enemy.base_crit),
                    enemy_desc_format_number(enemy.bonus_crit2),
                    enemy_desc_format_number(enemy.critdmg_debuff_var),
                ),
            ),
            (
                "PERFORM",
                "{0} = max(1 * {1}, 0)".format(
                    enemy_desc_format_number(enemy.perform),
                    enemy_desc_format_number(enemy.bonus_perform2),
                ),
            ),
            (
                "TANK",
                "{0} = max(1 * {1}, 1)".format(
                    enemy_desc_format_number(enemy.total_tank),
                    enemy_desc_format_number(enemy.bonus_tank2),
                ),
            ),
        ]

    def enemy_desc_build_effects2_rows(enemy):
        if enemy is None:
            return []

        effect_attrs = [
            ("Атака", "atk_debuff"),
            ("Защита", "def_debuff"),
            ("Магия", "magic_debuff"),
            ("Точность", "accuracy_debuff"),
            ("Шанс крита", "critrate_debuff"),
            ("Крит. урон", "critdmg_debuff"),
            ("Кровотечение", "bloodshed_debuff"),
            ("Prone", "prone_debuff"),
        ]

        rows = []
        for label, attr_name in effect_attrs:
            if hasattr(enemy, attr_name):
                value = getattr(enemy, attr_name)
                if value != 0:
                    rows.append((label, enemy_desc_format_number(value)))

        if not rows:
            rows.append(("Нет активных effects2", "0"))

        return rows

transform enemydesc:
    on show:
        xoffset -700 alpha 0.0
        pause 0.5
        easein 0.8 xoffset 0 alpha 1.0
    on hide:
        easein 0.8 xoffset 100 alpha 0.0
















init python:
    # ============================================================
    # ПАССИВКИ ВРАГОВ
    # ============================================================
    # "permanent" — постоянные пассивки (до 3 штук)
    # "mood"      — пассивки по настроению (до 3 штук на настроение)
    # ============================================================
    ENEMY_PASSIVES = {
        "Тревор": {
            "permanent": [
                ("Крепкий орешек",       "Каждый ход даёт себе +6% атаки."),
                ("Инстинкт самосохранения", "Не может упасть от первой атаки в бою."),
                ("Привычка к боли",       "+10% к защите от дебаффов."),
            ],
            "mood": {
                "neutral": [
                    ("Нейтралитет",   "Первый входящий удар всегда на -10% урона."),
                    ("Наблюдение",    "+5% шанс крита в ответной атаке."),
                    ("Собранность",   "Не получает штрафов от кровотечения первые 2 хода."),
                ],
                "sad": [
                    ("Уныние",        "-20% к своей атаке."),
                    ("Апатия",        "+25% урона, если атаковать со спины."),
                    ("Медлительность","Теряет инициативу раз в три хода."),
                ],
                "happy": [
                    ("Кураж",         "+10% к скорости атаки."),
                    ("Беспечность",   "-15% к защите."),
                    ("Щедрость",      "Раз в бой дарит герою 5 HP при попадании."),
                ],
                "angry": [
                    ("Ярость",        "+20% к урону, но -10% к точности."),
                    ("Берсерк",       "Атакует дважды, если HP ниже 30%."),
                    ("Неистовство",   "Игнорирует 25% вашей защиты."),
                ],
                "feared": [
                    ("Паника",        "20% шанс пропустить ход."),
                    ("Защитная реакция", "+30% к защите от физического урона."),
                    ("Заикание",      "Тратит 2 действия вместо 1."),
                ],
                "confused": [
                    ("Растерян",        "Сложнее попасть под влияние."),
                    ("Не верит словам", "Убеждение и риторика почти не работают."),
                    ("Ищет опору",      "Поддержка успокаивает его."),
                ],
                "thoughtful": [
                    ("Размышляет",      "Готов слушать и отвечать."),
                    ("Внутренний диалог","Плохо переносит давление."),
                    ("Собирает мысли",  "Наблюдателен и спокоен."),
                ],
                "tired": [
                    ("Выдохся",       "Атака снижена, но он ещё держится."),
                    ("Безразличие",   "Многие действия его больше не трогают."),
                    ("Сломлен",       "Поддержка и доброта находят отклик."),
                ],
            },
        },

        "Фроглин": {
            "permanent": [
                ("Магическая аура",     "В конце каждой атаки уменьшает магию у всех героев на 5% и увеличивает её у себя на 8%."),
                ("Магическая вредность","Уменьшает каждый ход ману всех персонажей на 6."),
                ("Делёжка",             "Если персонажи используют расходники, дающие ману, Фроглин получает +15% бонусной магии."),
            ],
            "mood": {
                "neutral":    [("—", "Нет особых эффектов настроения.")],
                "sad":        [("—", "Нет особых эффектов настроения.")],
                "happy":      [("—", "Нет особых эффектов настроения.")],
                "angry":      [("—", "Нет особых эффектов настроения.")],
                "feared":     [("—", "Нет особых эффектов настроения.")],
                "confused":   [("—", "Нет особых эффектов настроения.")],
                "thoughtful": [("—", "Нет особых эффектов настроения.")],
                "tired":      [("—", "Нет особых эффектов настроения.")],
            },
        },

        "Фрогетта": {
            "permanent": [
                ("Больно не будет!", "Каждая атака Фрогетты может убить персонажа с шансом, равным её крит.шансу."),
                ("А я могу сильнее!", "Каждый раз, когда получает урон, увеличивает свою бонусную атаку на 20%."),
                ("Готовка к удару",  "Каждый раунд увеличивает точность и крит-шанс +5% себе и +2% союзникам."),
            ],
            "mood": {
                "neutral":    [("—", "Нет особых эффектов настроения.")],
                "sad":        [("—", "Нет особых эффектов настроения.")],
                "happy":      [("—", "Нет особых эффектов настроения.")],
                "angry":      [("—", "Нет особых эффектов настроения.")],
                "feared":     [("—", "Нет особых эффектов настроения.")],
                "confused":   [("—", "Нет особых эффектов настроения.")],
                "thoughtful": [("—", "Нет особых эффектов настроения.")],
                "tired":      [("—", "Нет особых эффектов настроения.")],
            },
        },

        "Фрогис": {
            "permanent": [
                ("Не особо-то и хотелось", "Из-за нежелания драться Фрогис получает в конце каждого хода 15% от своего максимального значения пощады."),
                ("Милое пузеко",           "Оно такое желейное, что не хочется по нему бить. −10% от атаки атакующему персонажу после нанесения урона по Фрогис."),
                ("Наточенные стрелы",      "Каждое попадание снарядом Фрогис наносит 1 стак кровотечения по цели."),
            ],
            "mood": {
                "neutral":    [("—", "Нет особых эффектов настроения.")],
                "sad":        [("—", "Нет особых эффектов настроения.")],
                "happy":      [("—", "Нет особых эффектов настроения.")],
                "angry":      [("—", "Нет особых эффектов настроения.")],
                "feared":     [("—", "Нет особых эффектов настроения.")],
                "confused":   [("—", "Нет особых эффектов настроения.")],
                "thoughtful": [("—", "Нет особых эффектов настроения.")],
                "tired":      [("—", "Нет особых эффектов настроения.")],
            },
        },

        "Фрогестер": {
            "permanent": [
                ("Не задобришь!",            "Каждый ход Фрогестер откатывает прогресс пощады на 15%."),
                ("Видите? Они злодеи!",      "Каждый раз, когда Фрогестер получает урон, он получает −2 дебафф атаки и +10% к крит-урону. Атакующий получает +5% к атаке и +5% к крит-урону."),
                ("Исключительная упёртость", "Фрогис имеет шанс = его крит-шанс превратить удачную проверку социальной характеристики для действия с положительным эффектом в провальную."),
            ],
            "mood": {
                "neutral":    [("—", "Нет особых эффектов настроения.")],
                "sad":        [("—", "Нет особых эффектов настроения.")],
                "happy":      [("—", "Нет особых эффектов настроения.")],
                "angry":      [("—", "Нет особых эффектов настроения.")],
                "feared":     [("—", "Нет особых эффектов настроения.")],
                "confused":   [("—", "Нет особых эффектов настроения.")],
                "thoughtful": [("—", "Нет особых эффектов настроения.")],
                "tired":      [("—", "Нет особых эффектов настроения.")],
            },
        },

        "Манекен": {
            "permanent": [
                ("Это просто манекен",       "Скучающий кусок дерева и старой ткани, набитый соломой. Атак у него нет — но от скуки каждый герой в конце хода может получить Усталость ×3 и Безразличие ×3 с шансом 20%."),
                ("Бескровный, безмагии",     "Ни крови, ни магии — только дерево, ткань и нитки. Манекен не может получить кровотечение."),
                ("Рвущиеся швы",             "Старые швы не выдерживают натиска. Каждый критический удар по манекену снижает его бонусную защиту на 10%."),
            ],
            "mood": {
                "neutral": [
                    ("Полностью поддатливый", "Проверки социальных характеристик при действиях против манекена имеют очень низкую сложность."),
                    ("Особо не пофармишь", "Не даёт денег и опыта при победе над ним. А ты надеялся за него что-то получить?"),
                ],
                "sad":        [("—", "Нет особых эффектов настроения.")],
                "happy":      [("—", "Нет особых эффектов настроения.")],
                "angry":      [("—", "Нет особых эффектов настроения.")],
                "feared":     [("—", "Нет особых эффектов настроения.")],
                "confused":   [("—", "Нет особых эффектов настроения.")],
                "thoughtful": [("—", "Нет особых эффектов настроения.")],
                "tired":      [("—", "Нет особых эффектов настроения.")],
            },
        },

        # Дженерик: используются, если у врага нет своих пассивок
        "_default": {
            "permanent": [
                ("Загадка",         "Свойства неизвестны."),
                ("Скрытность",      "Свойства неизвестны."),
                ("Молчание",        "Свойства неизвестны."),
            ],
            "mood": {
                "neutral": [("Нейтрален",  "Свойства неизвестны."),
                            ("Спокоен",    "Свойства неизвестны."),
                            ("Собран",     "Свойства неизвестны.")],
                "sad":     [("Грустен",    "Свойства неизвестны."),
                            ("Апатичен",   "Свойства неизвестны."),
                            ("Задумчив",   "Свойства неизвестны.")],
                "happy":   [("Весел",      "Свойства неизвестны."),
                            ("Беспечен",   "Свойства неизвестны."),
                            ("Игрив",      "Свойства неизвестны.")],
                "angry":   [("Зол",        "Свойства неизвестны."),
                            ("Раздражён",  "Свойства неизвестны."),
                            ("Неистов",    "Свойства неизвестны.")],
                "feared":  [("Испуган",    "Свойства неизвестны."),
                            ("Паникует",   "Свойства неизвестны."),
                            ("Замирает",   "Свойства неизвестны.")],
                "confused":   [("Смущён",  "Свойства неизвестны."),
                               ("Теряется","Свойства неизвестны."),
                               ("Молчит",  "Свойства неизвестны.")],
                "thoughtful": [("Задумчив","Свойства неизвестны."),
                               ("Спокоен", "Свойства неизвестны."),
                               ("Собран",  "Свойства неизвестны.")],
                "tired": [("Устал",    "Свойства неизвестны."),
                          ("Вял",      "Свойства неизвестны."),
                          ("Без сил",  "Свойства неизвестны.")],
            },
        },
    }

    MOOD_RU = {
        "neutral":    "нейтрален",
        "sad":        "печален",
        "happy":      "весел",
        "angry":      "зол",
        "feared":     "испуган",
        "confused":   "смущён",
        "thoughtful": "задумчив",
        "tired":      "устал",
    }

    # ============================================================
    # ОПИСАНИЕ HP
    # ============================================================
    def describe_enemy_hp(enemy, level):
        """Возвращает (текст, цвет, показывать_полоски)."""
        if enemy is None or level < 1:
            return None
        hp    = max(0, int(getattr(enemy, "current_hp", 0)))
        maxhp = max(1, int(getattr(enemy, "max_hp", 1)))
        ratio = hp / maxhp

        if level == 1:
            # Грубо и ненадёжно — как в реальной «Оценить 1»
            if ratio > 0.85:   return ("Полностью целый", "#00ff00")
            if ratio > 0.6:    return ("Потрёпан",         "#ffff00")
            if ratio > 0.35:   return ("Ранен",            "#ffaa00")
            if ratio > 0.15:   return ("Тяжело ранен",     "#ff5500")
            return ("При смерти", "#ff0000")

        if level == 2:
            base, color = describe_enemy_hp(enemy, 1)
            return (f"{base} ({int(ratio*100)}%)", color)

        # level >= 3 — точное число
        return (f"{hp} ({int(ratio*100)}%)", "#ffffff")

    # ============================================================
    # ХЕЛПЕР: уровень осмотра
    # ============================================================
    def _examine_level(enemy):
        if enemy is None:
            return 0
        return max(0, min(5, int(getattr(enemy, "evaluate_success_count", 0))))

    # ============================================================
    # ПАССИВКИ ДЛЯ ЭКРАНА
    # ============================================================
    def get_enemy_passives_for_screen(enemy, level):
        """Возвращает (permanent_list, mood_list) — списки кортежей (имя, описание).
        Включает только те, что видны на текущем уровне осмотра."""
        if enemy is None:
            return [], []

        name = getattr(enemy, "name", "")
        data = ENEMY_PASSIVES.get(name, ENEMY_PASSIVES["_default"])
        mood = getattr(enemy, "mood", "neutral")

        # Постоянные: L2 → 1, L4 → 2, L5 → все
        if level >= 5:
            perm_count = 99
        elif level >= 4:
            perm_count = 2
        elif level >= 2:
            perm_count = 1
        else:
            perm_count = 0
        perms = data["permanent"][:perm_count]

        # Настроенческие: L1 → 1, L3 → 2, L5 → все
        if level >= 5:
            mood_count = 99
        elif level >= 3:
            mood_count = 2
        elif level >= 1:
            mood_count = 1
        else:
            mood_count = 0
        moods = data["mood"].get(mood, data["mood"]["neutral"])[:mood_count]

        return perms, moods

    # ============================================================
    # СТАТЫ ДЛЯ ЭКРАНА
    # ============================================================
    def get_enemy_stats_for_screen(enemy, level):
        """Возвращает dict со статами. None = не видно."""
        if enemy is None:
            return {}

        stats = {
            "atk":   None,
            "def":   None,
            "critrate": None,
            "critdmg":  None,
            "magic":    None,
            "speed":    None,
        }

        if level >= 2:
            stats["atk"] = int(round(getattr(enemy, "atk", 0)))
            stats["def"] = int(round(getattr(enemy, "armor", 0)))

        if level >= 3:
            cr = getattr(enemy, "critrate", 0)
            cd = getattr(enemy, "crit", 1.0)
            stats["critrate"] = int(round(cr * 100))
            stats["critdmg"]  = int(round(cd * 100))
            stats["accuracy"] = int(round(getattr(enemy, "dmgchance", 0.0) * 100))
            stats["magic"]    = int(round(getattr(enemy, "magic", 0)))
            stats["speed"]    = int(round(getattr(enemy, "speed", 1.0) * 100))

        return stats

    # ============================================================
    # ЩИТ И ПОЩАДА
    # ============================================================
    def get_enemy_shield_for_screen(enemy, level):
        if enemy is None or level < 4:
            return None
        return int(getattr(enemy, "shield", 0))

    def get_enemy_spare_for_screen(enemy, level):
        if enemy is None or level < 2:
            return None
        sp  = int(getattr(enemy, "spare_progress", 0))
        mx  = max(1, int(getattr(enemy, "spare_max", 100)))
        return int(round(sp / mx * 100))

    # ============================================================
    # АКТИВНЫЕ БАФФЫ / ДЕБАФФЫ (только на L5)
    # ============================================================
    def get_enemy_active_effects(enemy, level):
        if enemy is None or level < 5:
            return []

        result = []

        # Статусные эффекты — иконка + простой текст (не бонус)
        _bleed = getattr(enemy, "bloodshed_debuff", 0)
        if _bleed > 0:
            result.append(("bloodshed.png", False, "x%d" % int(round(_bleed))))
        if getattr(enemy, "prone_debuff", 0) > 0:
            result.append(("prone.png", False, None))

        init_stats   = getattr(enemy, "initial_stats",   {}) or {}
        init_bonuses = getattr(enemy, "initial_bonuses", {}) or {}

        # (стат, текущее, начальное, ключ_бонуса, зелёная_иконка, красная_иконка, бонус_в_процентах)
        stat_table = [
            ("atk",        enemy.atk,        init_stats.get("atk", 0),        "bonus_atk",       "atk_green_icon.png",       "atk_red_icon.png",       True),
            ("magic",      enemy.magic,      init_stats.get("magic", 0),      "bonus_magic",     "mag_green_icon.png",       "mag_red_icon.png",       True),
            ("defense",    enemy.defense,    init_stats.get("defense", 0),    "bonus_def",       "def_green_icon.png",       "def_red_icon.png",       True),
            ("dmgchance",  enemy.dmgchance,  init_stats.get("dmgchance", 0),  "bonus_dmgchance", "dmgchance_green_icon.png", "dmgchance_red_icon.png", True),
            ("critrate",   enemy.critrate,   init_stats.get("critrate", 0),   "bonus_critrate",  "critrate_green_icon.png",  "critrate_red_icon.png",  True),
            ("crit",       enemy.crit,       init_stats.get("crit", 1.0),     "bonus_crit",      "critdmg_green_icon.png",   "critdmg_red_icon.png",   True),
            ("total_tank", enemy.total_tank, init_stats.get("total_tank", 0), "bonus_tank",      "tank_green_icon.png",      "tank_red_icon.png",      False),
        ]

        for _stat_key, current_val, initial_val, bonus_key, green_icon, red_icon, is_pct in stat_table:
            try:
                curr = float(current_val)
                init = float(initial_val)
            except Exception:
                continue

            stat_diff = curr - init
            if abs(stat_diff) < 0.001:
                continue  # стат не менялся — иконки нет

            try:
                bonus_now  = float(getattr(enemy, bonus_key, 0.0))
                bonus_init = float(init_bonuses.get(bonus_key, 0.0))
            except Exception:
                bonus_now = bonus_init = 0.0
            bonus_diff = bonus_now - bonus_init

            # Цвет: приоритет — знак бонуса, если он ненулевой;
            # иначе — знак общего изменения стата.
            if abs(bonus_diff) >= 0.001:
                is_buff = bonus_diff > 0
            else:
                is_buff = stat_diff > 0

            icon = green_icon if is_buff else red_icon

            # Цифра — только если bonus ≠ 0
            bonus_text = enemydesc_bonus_text(bonus_diff, is_pct) if abs(bonus_diff) >= 0.001 else ""

            result.append((icon, is_buff, bonus_text if bonus_text else None))

        return result

    # ============================================================
    # СЛОЖНОСТЬ ДЕЙСТВИЯ (для attack_description)
    # ============================================================
    def get_action_difficulty_text(enemy, action_name, examine_level):
        """Возвращает строку «Сложность: N» или None, если её не видно.
        Видно: L3 — только для изученных действий; L4 — для всех."""
        if enemy is None or examine_level < 3:
            return None
        if action_name not in ACTS_CONFIG:
            return None

        mood = getattr(enemy, "mood", "neutral")
        if examine_level == 3:
            # Только для уже «изученных» действий текущего настроения
            used     = enemy.mood_action_used.get(mood, {}).get(action_name, False)
            revealed = enemy.mood_action_revealed.get(mood, {}).get(action_name, False)
            izzy     = False
            if getattr(store, "current_attacker", None) == 5:
                izzy = enemy.izzy_revealed_mood_actions.get(mood, {}).get(action_name, False) if hasattr(enemy, "izzy_revealed_mood_actions") else False
            if not (used or revealed or izzy):
                return None

        diff = calculate_action_difficulty(enemy, action_name)
        return f"Сложность: {diff}"

    # ============================================================
    # ГЛАВНАЯ ФУНКЦИЯ — ВЫЗЫВАЕТСЯ ИЗ ЭКРАНА ПРИ НАВЕДЕНИИ
    # ============================================================
    def describe_enemy_for_hover(enemy):
        """Собирает всю информацию для экрана enemydesc, уважая уровень осмотра."""
        if enemy is None:
            return None

        lvl = _examine_level(enemy)

        hp_text, hp_color = (None, "#ffffff")
        hp_res = describe_enemy_hp(enemy, lvl)
        if hp_res:
            hp_text, hp_color = hp_res

        perms, moods = get_enemy_passives_for_screen(enemy, lvl)

        
        mood_ru = MOOD_RU.get(getattr(enemy, "mood", "neutral"), "нейтрален") if lvl >= 1 else None
       

        return {
            "level":         lvl,
            "name":          getattr(enemy, "name", "?"),
            "nameeng":       getattr(enemy, "nameeng", "?"),
            "mood_key":      getattr(enemy, "mood", "neutral"),
            "mood_ru":       mood_ru,                       # ← теперь может быть None
            "hp_text":       hp_text,
            "hp_color":      hp_color,
            "hp_segments":   min(4, max(0, int(round((getattr(enemy, "current_hp", 0) / max(1, getattr(enemy, "max_hp", 1))) * 4)))),
            "stats":         get_enemy_stats_for_screen(enemy, lvl),
            "passives_perm": perms,
            "passives_mood": moods,
            "spare_percent": get_enemy_spare_for_screen(enemy, lvl),
            "shield":        get_enemy_shield_for_screen(enemy, lvl),
            "effects":       get_enemy_active_effects(enemy, lvl),
        }















transform enemydesc_slide_in:
    on show:
        alpha 0.0
        pause 1.5
        xoffset -40
        easeout 0.3 xoffset 0 alpha 1.0
    on hide:
        easein 0.3 xoffset -40 alpha 0.0


screen enemydesc():
    zorder 100

    if target_to_dis_enemy is None:
        timer 0.01 action Hide("enemydesc")
    else:
        $ e = target_to_dis_enemy
        $ d = describe_enemy_for_hover(e)

        # ============================================================
        # ОДИН ОБЩИЙ ФРЕЙМ — белая рамка, внутри чёрное поле
        # ============================================================
        frame at enemydesc_slide_in:
            xalign 0.5
            yalign 0.5
            xysize (1060, 690)          # ← было (900, 540)
            background "#ffffff"
            padding (5, 5)

            frame:
                #xfill True
                #yfill True
                xysize (1050, 680)
                xalign (0.5)
                yalign (0.5)
                background "#000000"
                #padding (14, 14)

                hbox:
                    spacing 20
                    # ========================================================
                    # ЛЕВАЯ КОЛОНКА — имя, портрет, состояние
                    # ========================================================
                    vbox:
                        xsize 300
                        spacing 8

                        # --- Имя ---
                        frame:
                            xfill True
                            ysize 48
                            background "#ffffff"
                            padding (3, 3)

                            frame:
                                xfill True yfill True
                                background "#000000"
                                text "[d['name']]":
                                    xalign 0.5 yalign 0.5
                                    size 30
                                    color "#ffffff"

                        # --- Портрет ---
                        $ _is_dummy = (
                            e is not None
                            and getattr(e, "name", None) == "Манекен"
                            and getattr(e, "nameeng", None) == "dummy"
                        )
                        frame:
                            xfill 270
                            ysize 400
                            padding (0, 0)
                            if _is_dummy:
                                add "dummyportrait.png" xysize (300, 400)
                            else:
                                background "#00cfd6"
                            # add "[d['nameeng']]fightsprite" xalign 0.5 yalign 0.5

                        # --- Щиты врага (жёлтые солиды) ---
                        # shield = 0  → блок не показывается
                        # shield > 0  → 4 слота, тёмный фон + яркая заливка поверх
                        if e.shield > 0:
                            hbox:
                                xalign 0.5
                                spacing 2
                                xfill True
                                for i in range(4):
                                    fixed:
                                        xysize (60, 3)
                                        # тёмно-жёлтая подложка
                                        add Solid("#2e2b00", xysize=(60, 3)) at damage_gradient_black
                                        # яркая заливка поверх — ровно по количеству щитов
                                        if i < e.shield:
                                            add Solid("#e1d22e", xysize=(60, 3)) at damage_gradient_gray

                        # --- HP текст ---
                        if d["hp_text"] is not None:
                            text "Здоровье: [d['hp_text']]":
                                size 20
                                color d["hp_color"]
                                xalign 0.0
                        else:
                            text "Здоровье: ???" size 20 color "#888888"

                        # --- Пощада ---
                        if d["spare_percent"] is not None:
                            frame:
                                xsize 250
                                ysize 40
                                background None
                                padding (0, 0)

                                fixed:
                                    xysize (300, 40)

                                    # 1) Фон — тёмно-красный
                                    add Solid("#550000", xysize=(300, 40))

                                    # 2) Заполнение — яркий жёлтый
                                    #    int(250 * percent / 100), минимум 1px, максимум 250px
                                    $ _spare_px = max(0, min(300, int(300 * d["spare_percent"] / 100)))
                                    if _spare_px > 0:
                                        add Solid("#e1d22e", xysize=(_spare_px, 40))

                                    # 3) Текст поверх
                                    text "[d['spare_percent']]%":
                                        size 20
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
                        else:
                            frame:
                                xsize 250
                                ysize 40
                                background None
                                padding (0, 0)

                                fixed:
                                    xysize (250, 40)
                                    add Solid("#550000", xysize=(250, 40))
                                    text "???":
                                        size 20
                                        color "#888888"
                                        xalign 0.5
                                        yalign 0.5

                        # --- Настроение ---
                        if d["mood_ru"]:
                            text "Настроение: [d['mood_ru']]":
                                size 20 color "#ffffff"
                        else:
                            text "Настроение: ???":
                                size 20 color "#888888"

                        # --- Активные эффекты (видно на L5) ---
                        if d["effects"]:
                            grid 5 3:
                                xalign 0.5
                                spacing 4
                                for icon, is_buff, bonus_text in d["effects"][:15]:
                                    hbox:
                                        spacing -10
                                        yalign 0.5
                                        if is_buff:
                                            add icon size (32, 32) yalign 0.5 at damage_gradient_green
                                        else:
                                            add icon size (32, 32) yalign 0.5 at damage_gradient

                                        if enemydesc_bonus_is_nonzero(bonus_text):
                                            text "[bonus_text]" size 20 color ("#00ff04" if is_buff else "#ff4444") yalign 0.5 outlines [(2, "#000000", 0, 0)] yoffset 10


                    # ========================================================
                    # ПРАВАЯ КОЛОНКА — статы и пассивки
                    # ========================================================
                    vbox:
                        xsize 600         # ← было 600
                        spacing 14

                        # --- Заголовок ---
                        text "Особенности":
                            size 34 color "#ffffff" xalign 0.5

                        # --- Статы (3 колонки × 2 строки) ---
                        grid 3 3:
                            spacing 2
                            use enemydesc_stat_cell("Атака",      d["stats"].get("atk"),      debuff_val=getattr(e, "atk_debuff", 0),      debuff_name_pos="Истощение", debuff_name_neg="Бодрость")
                            use enemydesc_stat_cell("Крит шанс",  d["stats"].get("critrate"), "%", debuff_val=getattr(e, "critrate_debuff", 0), debuff_name_pos="Сглаз",     debuff_name_neg="Удача")                        
                            use enemydesc_stat_cell("Точность",   d["stats"].get("accuracy"), "%", debuff_val=getattr(e, "accuracy_debuff", 0), debuff_name_pos="Страх",     debuff_name_neg="Концентрация")

                            use enemydesc_stat_cell("Защита",     d["stats"].get("def"),      debuff_val=getattr(e, "def_debuff", 0),      debuff_name_pos="Печаль",    debuff_name_neg="Вдохновение")
                            use enemydesc_stat_cell("Крит урон",  d["stats"].get("critdmg"),  "%", debuff_val=getattr(e, "critdmg_debuff", 0),  debuff_name_pos="Безразличие", debuff_name_neg="Гнев")
                            use enemydesc_stat_cell("Магия",      d["stats"].get("magic"),    "%", debuff_val=getattr(e, "magic_debuff", 0),    debuff_name_pos="Помутнение", debuff_name_neg="Просвещение")

                            use enemydesc_stat_cell("Скорость",   d["stats"].get("speed"),    "%", debuff_val=getattr(e, "tank_debuff", 0),     debuff_name_pos="Уязвимость", debuff_name_neg="Скрытность")
                            null width 200 height 52
                            null width 200 height 52

                        # --- Пассивки (постоянные и от настроения в едином vbox) ---
                        frame:
                            xfill True
                            xsize 650
                            ysize 508
                            background None #"#000000"
                            padding (10, 8)
                            vbox:
                                spacing 6
                                for pname, pdesc in d["passives_perm"]:
                                    vbox:
                                        spacing 2
                                        text "• [pname]" size 25 color "#ffffff"
                                        text "    [pdesc]" size 20 color "#cccccc" layout "greedy"
                                for pname, pdesc in d["passives_mood"]:
                                    vbox:
                                        spacing 2
                                        text "• [pname]" size 25 color "#fffb00"
                                        text "    [pdesc]" size 20 color "#cccccc" layout "greedy"

        # ============================================================
        # ДЕБАГ-ПАНЕЛЬ (отдельно от основного фрейма, снизу)
        # ============================================================
        #frame:
        #    xalign 0.5
        #    ypos 660
        #    xysize (900, 50)
        #    background "#000000DD"
        #    padding (8, 6)

        #    hbox:
        #        spacing 20
        #        text "DEBUG: [d['nameeng']]"      size 16 color "#ff00ff" yalign 0.5
        #        text "mood=[e.mood]"                size 14 color "#ffffff" yalign 0.5
        #        text "examine=[d['level']]"         size 14 color "#ffff00" yalign 0.5
        #        text "hp=[e.current_hp]/[e.max_hp]" size 14 color "#ffffff" yalign 0.5
        #        text "spare=[e.spare_progress]/[e.spare_max]" size 14 color "#ffff00" yalign 0.5
        #        text "shield=[e.shield]"            size 14 color "#ffffff" yalign 0.5
        #        text "turn=[e.turn]"                size 14 color "#ffffff" yalign 0.5


screen enemydesc_stat_cell(label_text, value, suffix="", debuff_val=0, debuff_name_pos="", debuff_name_neg=""):
    frame:
        background None
        xsize 200 ysize 30
        padding (6, 2)

        vbox:
            spacing 1
            yalign 0.5

            hbox:
                spacing 6
                yalign 0.5

                text "[label_text]:" size 20 color "#ffffff"
                if value is None:
                    text "???" size 20 color "#666666"
                else:
                    text "[value][suffix]" size 20 color "#ffffff"

            if debuff_val != 0 and value is not None:
                if debuff_val > 0:
                    $ debuff_txt = f"{debuff_name_pos}(х{debuff_val})" if debuff_name_pos else f"(+{debuff_val})"
                    text "[debuff_txt]" size 14 color "#8b0000"
                else:
                    $ debuff_txt = f"{debuff_name_neg}(х{-debuff_val})" if debuff_name_neg else f"({debuff_val})"
                    text "[debuff_txt]" size 14 color "#006400"
