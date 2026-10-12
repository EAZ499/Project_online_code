# ============================================================
# complex_phone_screen.rpy
# v6: добавлен отдельный жёлтый маркер комнаты задания.
# Многоуровневый телефон / журнал / карта / сообщения / инфо.
# Плейсхолдерная версия: все картинки заменены Solid-квадратами.
# Подключение: положить файл в папку game/ и вызвать Show("complex_phone").
# ============================================================

# ------------------------------------------------------------
# БАЗОВОЕ СОСТОЯНИЕ ЭКРАНА
# ------------------------------------------------------------
default phone_panel = "home"                    # home / journal / contacts / info / party

default phone_map_location = "dorm_road"
default phone_map_sublocation = "dorm_road"
default phone_selected_quest = "pisa_1"
default phone_selected_route = "dorm_road"
default room = "DormRoad1"

default phone_selected_contact = "alphys"
default phone_chat_open = False

# Контакт появляется в мессенджере только если <id>_get_contacted == 1.
# Например: $ susie_get_contacted = 1 — открыть контакт Сьюзи.
default alphys_get_contacted = 1
default susie_get_contacted = 1
default noelle_get_contacted = 1
default phone_info_section = None
default phone_info_subsection = None
default phone_selected_character = "Крис"
default phone_character_info_tab = "info"
# Заметки персонажей для вкладки Инфо. Можно заполнить по сюжету/вручную.
default phone_character_notes = {}
default forming_team_selected_slot = 1

# Сюжетные переменные тем чата. Логика: [] — события нет, [1] — событие случилось,
# [1, None] — собеседник ждёт ответа, [1, 0] — проигнорировано, [1, 1/2/3] — отвечено.
default sport = []
default tea = []
default present = []
default susie_training = []
default susie_walk = []
default noelle_study = []
default noelle_library = []

# Возможность написать первыми. Эти флаги можно менять из сюжета.
default can_write_sport = 1
default can_write_tea = 1
default can_write_present = 1
default can_write_susie_training = 1
default can_write_susie_walk = 1
default can_write_noelle_study = 1
default can_write_noelle_library = 1

# Прогресс заданий: 0 — не взято, 1+ — стадии.
default phone_quest_progress = {
    "pisa_1": 3,
    "pisa_2": 1,
    "lost_badge": 1,
    "library_key": 3,
    "new_quest": 0,
    "new_quest_2": 1,
    "new_quest_3": 1,
    "new_quest_4": 1,
    "new_quest_5": 1,
    "new_quest_6": 0
}

# История сообщений и защита от повторной генерации одной и той же реплики.
default phone_chat_messages = {
    "alphys": [],
    "susie": [],
    "noelle": [],
}
default phone_chat_seen_events = []
















init python:
    # ---------- РОЛИ ПЕРСОНАЖА ----------
    PHONE_ROLE_ATTRS = [
        ("damager_role",  "Урон",       "#3A0102", "#EA4245"),
        ("debuffer_role", "Дебаффы",    "#3A1901", "#EA8542"),
        ("tank_role",     "Стойкость",  "#393A01", "#EAE342"),
        ("support_role",  "Поддержка",  "#293A01", "#B9EA42"),
        ("nego_role",     "Переговоры", "#0E3A01", "#5FEA42"),
    ]

    def phone_get_role_value(char_name, role_attr):
        char = phone_get_character_object(char_name)
        if char is None: return 0
        try: value = getattr(char, role_attr)
        except: value = None
        if value is None: return 0
        try: return max(0, min(4, int(value)))
        except: return 0

    # ---------- ОПЫТ ПЕРСОНАЖА ----------
    def phone_get_xp_fraction(char_name=None):
        char = phone_get_character_object(char_name)
        if char is None: return 0.0
        xp = getattr(char, "xp", 0)
        mxp = getattr(char, "lvl_xp", 1)
        if mxp <= 0: return 0.0
        return max(0.0, min(1.0, float(xp) / float(mxp)))

    def phone_get_xp_text(char_name=None):
        char = phone_get_character_object(char_name)
        if char is None: return "0/0"
        return "%s/%s" % (getattr(char, "xp", 0), getattr(char, "lvl_xp", 0))

    # ---------- ИТОГОВЫЕ ХАРАКТЕРИСТИКИ ----------
    
    # Таблицы порогов (12 уровней: индексы 0-11)
    # Значения: very_poor (1 палка), poor (2), medium (3), good (4), very_good (5)
    PHONE_STATS_TABLES = {
        "hp": {
            "very_poor": [50, 72, 94, 117, 139, 161, 183, 206, 228, 250, 272, 294],
            "poor":      [75, 101, 128, 154, 181, 207, 233, 260, 286, 313, 339, 365],
            "medium":    [100, 131, 161, 192, 222, 253, 283, 314, 344, 375, 406, 436],
            "good":      [125, 160, 194, 229, 264, 299, 333, 368, 403, 438, 472, 507],
            "very_good": [150, 189, 228, 267, 306, 344, 383, 422, 461, 500, 539, 578],
        },
        "mp": {
            "very_poor": [20, 24, 29, 33, 38, 42, 47, 51, 56, 60, 64, 69],
            "poor":      [27, 32, 38, 43, 49, 54, 60, 65, 71, 76, 82, 87],
            "medium":    [33, 40, 46, 53, 59, 66, 73, 79, 86, 93, 99, 106],
            "good":      [40, 47, 55, 63, 70, 78, 86, 93, 101, 109, 116, 124],
            "very_good": [46, 55, 64, 72, 81, 90, 98, 107, 116, 125, 134, 143],
        },
        "atk": {
            "very_poor": [12, 15, 18, 21, 24, 29, 34, 38, 43, 48, 53, 58],
            "poor":      [15, 19, 23, 26, 30, 35, 40, 45, 50, 55, 60, 65],
            "medium":    [18, 23, 27, 32, 36, 41, 46, 51, 56, 61, 66, 71],
            "good":      [21, 26, 32, 37, 42, 47, 52, 58, 63, 68, 73, 78],
            "very_good": [24, 30, 36, 42, 48, 53, 58, 64, 69, 74, 79, 84],
        },
        "magic": {
            "very_poor": [18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84],
            "poor":      [23, 30, 37, 43, 50, 57, 64, 71, 78, 85, 92, 99],
            "medium":    [27, 35, 43, 51, 59, 67, 75, 82, 90, 98, 106, 114],
            "good":      [32, 41, 50, 58, 67, 76, 85, 93, 102, 111, 120, 129],
            "very_good": [36, 46, 56, 65, 75, 85, 95, 104, 114, 124, 134, 144],
        },
        "defense": {
            "very_poor": [1, 4, 6, 9, 11, 14, 16, 19, 21, 24, 26, 29],
            "poor":      [2, 6, 8, 12, 14, 18, 20, 24, 26, 30, 32, 36],
            "medium":    [3, 8, 11, 16, 19, 24, 27, 32, 35, 40, 43, 48],
            "good":      [4, 10, 13, 19, 22, 28, 31, 37, 40, 46, 49, 55],
            "very_good": [5, 12, 15, 22, 25, 32, 45, 52, 55, 62, 65, 72],
        },
        "tank": {
            "very_poor": [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
            "poor":      [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
            "medium":    [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35],
            "good":      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
            "very_good": [45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45],
        },
        "dmgchance": {
            "very_poor": [20, 23, 27, 30, 33, 37, 40, 43, 47, 50, 53, 57],
            "poor":      [30, 34, 37, 41, 44, 48, 52, 55, 59, 63, 66, 70],
            "medium":    [40, 45, 48, 52, 56, 59, 63, 67, 71, 75, 79, 83],
            "good":      [50, 56, 58, 63, 67, 71, 75, 79, 83, 88, 92, 96],
            "very_good": [60, 64, 69, 73, 78, 82, 87, 91, 96, 100, 104, 109],
        },
        "critrate": {
            "very_poor": [1, 3, 5, 7, 9, 11, 13, 15, 17, 20, 22, 24],
            "poor":      [5, 7, 10, 12, 15, 18, 21, 24, 27, 30, 33, 36],
            "medium":    [10, 12, 16, 18, 22, 25, 29, 32, 36, 40, 44, 48],
            "good":      [15, 17, 21, 24, 28, 32, 36, 40, 44, 50, 55, 60],
            "very_good": [20, 24, 28, 32, 36, 40, 44, 48, 52, 60, 64, 68],
        },
        "crit": {
            "very_poor": [5, 8, 11, 14, 17, 20, 23, 26, 30, 33, 36, 39],
            "poor":      [10, 13, 17, 21, 25, 29, 33, 37, 42, 50, 54, 58],
            "medium":    [15, 19, 23, 28, 33, 38, 43, 48, 54, 66, 72, 77],
            "good":      [20, 24, 29, 34, 40, 46, 52, 58, 65, 83, 90, 96],
            "very_good": [25, 33, 41, 49, 57, 65, 73, 82, 90, 99, 107, 115],
        },
            
            
            
            
            
            "diplomacy": {
            "very_poor": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "poor":      [9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 25, 26],
            "medium":    [10, 12, 13, 15, 17, 18, 20, 22, 23, 25, 27, 28],
            "good":      [12, 14, 16, 18, 20, 23, 25, 27, 29, 31, 33, 36],
            "very_good": [14, 17, 20, 23, 26, 29, 32, 35, 38, 40, 43, 46],
        },
        "charm": {
            "very_poor": [0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17],
            "poor":      [5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22],
            "medium":    [10, 12, 13, 15, 16, 18, 19, 21, 22, 24, 25, 27],
            "good":      [15, 17, 18, 20, 21, 23, 24, 26, 27, 29, 30, 32],
            "very_good": [20, 22, 23, 25, 26, 28, 29, 31, 32, 34, 35, 37],
        },
        "social": {
            "very_poor": [-8, -7, -6, -5, -4, -2, -1, 0, 1, 2, 3, 4],
            "poor":      [-7, -6, -4, -3, -2, 0, 1, 2, 4, 5, 6, 7],
            "medium":    [-4, -3, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10],
            "good":      [-1, 0, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13],
            "very_good": [2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16],
        },
    }
  

    # Сопоставление атрибутов экрана с ключами таблиц
    PHONE_STAT_MAP = {
        "hp": "hp", "max_hp": "hp",
        "mp": "mp", "max_mp": "mp",
        "atk": "atk", "attack": "atk",
        "magic": "magic",
        "defense": "defense", "def": "defense",
        "tank": "tank", "total_tank": "tank",
        "dmgchance": "dmgchance", "accuracy": "dmgchance",
        "critrate": "critrate",
        "crit": "crit", "critdmg": "crit",
        # Социальные характеристики
        "diplomacy": "diplomacy",
        "charm": "charm",
        "socialization": "social",
        "perception": "social",
        "rhetoric": "social",
        "artistry": "social",
        "comfort": "social",
        "power": "social",
    }

    PHONE_RATING_STRIP_COLORS = ["#370000", "#462206", "#5F6700", "#73B400", "#3AFF00"]

    # Списки атрибутов для отрисовки полосок
    PHONE_MAIN_STAT_ATTRS = [
        "hp", "mp",
        "atk", "magic",
        "dmgchance", "critrate", "crit",
        "defense", "tank",
    ]
    
    PHONE_SOCIAL_STAT_ATTRS = [
        "diplomacy", "charm", "socialization", "perception", 
        "rhetoric", "artistry", "comfort", "power"
    ]

    # --- ФУНКЦИЯ ПОЛУЧЕНИЯ ЗНАЧЕНИЯ ХАРАКТЕРИСТИКИ ---
    def phone_get_total_stat(char, attr):
        if char is None: return None
        
        # 1. Прямая попытка получить атрибут (например, atk, magic, defense)
        # В Pers свойства atk, magic, defense уже возвращают итоговое значение
        val = getattr(char, attr, None)
        
        # 2. Если не нашли, пробуем варианты написания
        if val is None:
            if attr == "hp": val = getattr(char, "max_hp", None)
            elif attr == "mp": val = getattr(char, "max_mp", None)
            elif attr == "tank": val = getattr(char, "total_tank", None)
            elif attr == "dmgchance": val = getattr(char, "dmgchance", None) # Свойство в Pers
            elif attr == "critrate": val = getattr(char, "critrate", None) # Свойство в Pers
            elif attr == "crit": val = getattr(char, "crit", None) # Свойство в Pers (множитель)
        
        # 3. Если значение - список (уровни), берем текущий уровень (не должно случаться для свойств, но на всякий случай)
        if isinstance(val, (list, tuple)):
            lvl = int(getattr(char, "level", 1)) - 1
            if 0 <= lvl < len(val): return val[lvl]
            return val[-1] if val else 0
            
        return val

    # --- ФУНКЦИЯ РАСЧЕТА РЕЙТИНГА (ПОЛОСОК) ---
    def phone_stat_rating(char_name, attr):
        char = phone_get_character_object(char_name)
        if char is None:
            return 0

        # Уровень (1-12) -> индекс (0-11)
        level = int(getattr(char, "level", 1))
        level = max(1, min(12, level))
        idx = level - 1

        # Получаем значение
        value = phone_get_total_stat(char, attr)
        
        # Если характеристики нет (None), возвращаем 0 полосок
        if value is None:
            return 0
            
        try:
            value = float(value)
        except:
            return 0

        # Определяем ключ таблицы
        table_key = PHONE_STAT_MAP.get(attr)
        if not table_key or table_key not in PHONE_STATS_TABLES:
            # Если нет таблицы (например, для соц. навыков без таблиц), 
            # но значение есть, дадим 1 полоску просто за наличие? 
            # Или 0. Пусть будет 0, если нет таблицы.
            return 0 

        table = PHONE_STATS_TABLES[table_key]

        # Нормализация значений под формат таблицы
        if table_key in ("dmgchance", "critrate"):
            value = value * 100.0
            
        if table_key == "crit":
            if value < 5.0: 
                value = (value - 1.0) * 100.0

        # --- ЛОГИКА РЕЙТИНГА ---
        # Сверху вниз: чем выше порог, тем больше полосок.
        if value >= table["very_good"][idx]:
            return 5
        if value >= table["good"][idx]:
            return 4
        if value >= table["medium"][idx]:
            return 3
        if value >= table["poor"][idx]:
            return 2

        # very_poor — минимальный ненулевой рейтинг.
        # Для боевых характеристик порог положительный, для социальных — отрицательный,
        # поэтому здесь корректно работают оба случая.
        if value >= table.get("very_poor", [0] * 12)[idx]:
            return 1

        # На всякий случай: если боевое значение между 0 и very_poor,
        # но строго положительное — тоже даём 1 полоску (старое поведение).
        if value > 0:
            return 1

        # Социальные характеристики всегда показывают хотя бы одну полоску,
        # даже если значение ниже минимального порога таблицы (например, власть -12).
        if table_key in ("diplomacy", "charm", "social"):
            return 1

        return 0

    # --- ФУНКЦИИ ФОРМАТИРОВАНИЯ ТЕКСТА СТАТОВ ---
    def phone_safe_attr(obj, attr, default="—"):
        if obj is None: return default
        val = getattr(obj, attr, default)
        return default if val is None else val

    def phone_fmt_stat(value):
        try:
            # Целые числа и близкие к ним — без десятых.
            # Только настоящее дробное значение (1.07) показываем как есть.
            if isinstance(value, float):
                if value.is_integer():
                    return str(int(value))
                return "%.2f" % value
            return str(value)
        except Exception:
            return "—"

    def phone_fmt_percent(value):
        try: return "%d%%" % int(round(float(value) * 100))
        except: return phone_fmt_stat(value)

    # --- СПИСКИ СТАТИСТИКИ ДЛЯ ОТОБРАЖЕНИЯ ---
    def phone_character_main_stats(char_name=None):
        char = phone_get_character_object(char_name)
        if char is None:
            return [(n, "—") for n in ["HP", "MP", "Атака", "Магия", "Защита", "Танк", "Точность", "Крит. шанс", "Крит. урон"]]

        hp = "%s/%s" % (phone_fmt_stat(getattr(char, "current_hp", 0)), phone_fmt_stat(getattr(char, "max_hp", 0)))
        mp = "%s/%s" % (phone_fmt_stat(getattr(char, "current_mp", 0)), phone_fmt_stat(getattr(char, "max_mp", 0)))


        return [
            ("HP", hp),
            ("MP", mp),
            ("Атака", "%d" % int(round(float(getattr(char, "atk", 0))))),
            ("Магия", "%d" % int(round(float(getattr(char, "magic", 0))))),
            ("Защита", "%d" % int(round(float(getattr(char, "defense", 0))))),
            ("Танк", "%d" % int(round(float(getattr(char, "total_tank", 0))))),
            ("Точность", phone_fmt_percent(getattr(char, "dmgchance", 0))),
            ("Крит. шанс", phone_fmt_percent(getattr(char, "critrate", 0))),
            ("Крит. урон", "%d%%" % int(round(float(getattr(char, "crit", 1.0)) * 100))),
        ]

    def phone_character_social_stats(char_name=None):
        char = phone_get_character_object(char_name)
        if char is None:
            return [(n, "—") for n in ["Дипломатия", "Очарование", "Социализация", "Восприятие", "Риторика", "Артистизм", "Комфорт", "Власть"]]
             
        return [
            ("Дипломатия", phone_fmt_stat(getattr(char, "diplomacy", 0))),
            ("Очарование", phone_fmt_stat(getattr(char, "charm", 0)) + "%"),
            ("Социализация", phone_fmt_stat(getattr(char, "socialization", 0))),
            ("Восприятие", phone_fmt_stat(getattr(char, "perception", 0))),
            ("Риторика", phone_fmt_stat(getattr(char, "rhetoric", 0))),
            ("Артистизм", phone_fmt_stat(getattr(char, "artistry", 0))),
            ("Комфорт", phone_fmt_stat(getattr(char, "comfort", 0))),
            ("Власть", phone_fmt_stat(getattr(char, "power", 0))),
        ]
    
    # Вспомогательные функции для других частей телефона (чтобы не сломать)
    def phone_get_character_object(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        pd = getattr(store, "pers_dict", None)
        if isinstance(pd, dict) and char_name in pd: return pd[char_name]
        chars = getattr(store, "characters", None)
        if isinstance(chars, dict) and char_name in chars: return chars[char_name]
        return None





    def get_stat_display_data(char_name, stat_type="main"):
        """
        Возвращает список кортежей: (label, value, rating)
        stat_type: "main" или "social"
        """
        result = []
        
        # Получаем значения (имя, значение)
        if stat_type == "main":
            stats_list = phone_character_main_stats(char_name)
            attrs_list = PHONE_MAIN_STAT_ATTRS
        else:
            stats_list = phone_character_social_stats(char_name)
            attrs_list = PHONE_SOCIAL_STAT_ATTRS
            
        # Получаем рейтинги
        # Нам нужно сопоставить порядок stats_list с attrs_list
        # В текущей реализации phone_character_main_stats возвращает фиксированный порядок
        
        # Маппинг для красивых названий в блоках
        label_map = {
            "HP": "HP", "MP": "MP", "Сытость": "FD", "Атака": "ATK", "Магия": "MAG",
            "Точность": "HIT", "Крит. шанс": "CRT%", "Крит. урон": "CRTx",
            "Защита": "DEF", "Танк": "TNK", "Отношение": "REL", "Уровень": "LVL",
            "В команде": "IN", # На всякий случай
            
            "Дипломатия": "DIP", "Очарование": "CHM", "Социализация": "SOC",
            "Восприятие": "PER", "Риторика": "RHT", "Артистизм": "ART",
            "Комфорт": "CMF", "Власть": "PWR"
        }
        
        # Маппинг для получения рейтинга (нужен ключ атрибута)
        # Порядок в stats_list должен соответствовать порядку в attrs_list, 
        # но в phone_character_main_stats есть "Уровень", "Сытость", "В команде", которых нет в PHONE_MAIN_STAT_ATTRS
        # Поэтому будем искать рейтинг по имени, если возможно, или пропускать
        
        attr_map_reverse = {
            "HP": "hp", "MP": "mp", "Атака": "atk", "Магия": "magic",
            "Точность": "dmgchance", "Крит. шанс": "critrate", "Крит. урон": "crit",
            "Защита": "defense", "Танк": "tank", "Отношение": "reltns",
            
            "Дипломатия": "diplomacy", "Очарование": "charm", "Социализация": "socialization",
            "Восприятие": "perception", "Риторика": "rhetoric", "Артистизм": "artistry",
            "Комфорт": "comfort", "Власть": "power"
        }

        for name, value in stats_list:
            short_label = label_map.get(name, name[:3].upper())
            
            # Пытаемся найти рейтинг
            attr_key = attr_map_reverse.get(name)
            rating = 0
            if attr_key:
                rating = phone_stat_rating(char_name, attr_key)
            
            result.append((short_label, value, rating))
            
        return result














# ------------------------------------------------------------
# ДАННЫЕ, ФУНКЦИИ КАРТЫ, КВЕСТОВ И ЧАТА
# ------------------------------------------------------------
init python:
    # ---------- маленькие утилиты ----------
    def _phone_safe_restart():
        try:
            renpy.restart_interaction()
        except Exception:
            pass

    def _phone_set_store_var(var_name, value):
        setattr(store, var_name, value)
        _phone_safe_restart()

    def _phone_get_list_var(var_name):
        value = getattr(store, var_name, [])
        if value is None:
            value = []
            setattr(store, var_name, value)
        return value

    def _phone_set_topic_state(topic_key, value):
        setattr(store, topic_key, list(value))
        _phone_safe_restart()

    # ---------- настройки прокрутки списка заданий ----------
    PHONE_QUEST_ROW_HEIGHT = 70
    PHONE_QUEST_ROW_SPACING = 8
    PHONE_QUEST_VIEWPORT_HEIGHT = 540

    def phone_active_quest_count_for_scroll():
        return len([qid for qid in PHONE_QUESTS.keys() if phone_get_quest_progress(qid) > 0])

    def phone_should_show_quest_vbar():
        count = phone_active_quest_count_for_scroll()
        if count <= 0:
            return False
        content_h = count * PHONE_QUEST_ROW_HEIGHT + max(0, count - 1) * PHONE_QUEST_ROW_SPACING
        return content_h > PHONE_QUEST_VIEWPORT_HEIGHT

    def phone_set_panel(panel_name):
        store.phone_panel = panel_name
        if panel_name == "contacts":
            store.phone_chat_open = False
        if panel_name == "info" and store.phone_info_section == "characters":
            store.phone_info_section = "battle"
        _phone_safe_restart()

    # ---------- данные карты ----------
    # Новая логика:
    # location     = большая зона:      pemchik / chris_street / dorm_road
    # sublocation  = подзона/корпус:    physic / main / gum / empty
    # room         = конкретная комната: PemchkPhysic1, PemchkMain2 и т.д.
    #
    # Пример: room = "PemchkPhysic1"
    # Это читается как: ПЕМЧК -> физкорпус -> 1 этаж.

    PHONE_LOCATIONS = {
        "pemchik": {
            "name": "ПЕМЧК",
            "sublocations": ["physic", "main", "gum", "empty"],
        },
        "chris_street": {
            "name": "Улица Криса",
            "sublocations": ["chris_street"],
        },
        "dorm_road": {
            "name": "Дорога в общежитие",
            "sublocations": ["dorm_road"],
        }
    }

    PHONE_SUBLOCATIONS = {
        "physic": {
            "location": "pemchik",
            "name": "Физико-математический корпус",
            "rooms": [
                ("PemchkPhysic3", "3 этаж"),
                ("PemchkPhysic2", "2 этаж"),
                ("PemchkPhysic1", "1 этаж"),
                ("PemchkPhysic0", "0 этаж"),
            ],
        },
        "main": {
            "location": "pemchik",
            "name": "Главный корпус",
            "rooms": [
                ("PemchkMain3", "3 этаж"),
                ("PemchkMain2", "2 этаж"),
                ("PemchkMain1", "1 этаж"),
                (None, "пусто"),
            ],
        },
        "gum": {
            "location": "pemchik",
            "name": "ГУМ корпус",
            "rooms": [
                ("PemchkGum2", "2 этаж"),
                ("PemchkGum1", "1 этаж"),
                ("PemchkGum0", "0 этаж"),
                (None, "пусто"),
            ],
        },
        "empty": {
            "location": "pemchik",
            "name": "Пустая вкладка",
            "rooms": [
                (None, "пусто"),
                (None, "пусто"),
                (None, "пусто"),
                (None, "пусто"),
            ],
        },
        "chris_street": {
            "location": "chris_street",
            "name": "Улица Криса",
            "rooms": [
                ("ChrisStreet1", "начало улицы"),
                ("ChrisStreet2", "середина улицы"),
                ("ChrisStreet3", "конец улицы"),
                (None, "пусто"),
            ],
        },
        "dorm_road": {
            "location": "dorm_road",
            "name": "Дорога в общежитие",
            "rooms": [
                ("DormRoad1", "остановка"),
                ("DormRoad2", "поворот"),
                ("DormRoad3", "общежитие"),
                (None, "пусто"),
            ],
        }
    }

    # Визуальное расположение голубых кнопок комнат/этажей на центральной карте.
    # Формат: [{"room": str|None, "name": str, "x": int, "y": int, "w": int, "h": int}, ...]
    PHONE_ROOM_UI_LAYOUTS = {
        "physic": [
            {"room": "PemchkPhysic3", "name": "3 этаж", "x": 72, "y": 48, "w": 440, "h": 70},
            {"room": "PemchkPhysic2", "name": "2 этаж", "x": 72, "y": 134, "w": 440, "h": 70},
            {"room": "PemchkPhysic1", "name": "1 этаж", "x": 72, "y": 220, "w": 440, "h": 70},
            {"room": "PemchkPhysic0", "name": "0 этаж", "x": 72, "y": 306, "w": 440, "h": 70},
        ],
        "main": [
            {"room": "PemchkMain3", "name": "3 этаж", "x": 72, "y": 48, "w": 440, "h": 70},
            {"room": "PemchkMain2", "name": "2 этаж", "x": 72, "y": 134, "w": 440, "h": 70},
            {"room": "PemchkMain1", "name": "1 этаж", "x": 72, "y": 220, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 306, "w": 440, "h": 70},
        ],
        "gum": [
            {"room": "PemchkGum2", "name": "2 этаж", "x": 72, "y": 48, "w": 440, "h": 70},
            {"room": "PemchkGum1", "name": "1 этаж", "x": 72, "y": 134, "w": 440, "h": 70},
            {"room": "PemchkGum0", "name": "0 этаж", "x": 72, "y": 220, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 306, "w": 440, "h": 70},
        ],
        "empty": [
            {"room": None, "name": "пусто", "x": 72, "y": 48, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 134, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 220, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 306, "w": 440, "h": 70},
        ],
        "chris_street": [
            {"room": "ChrisStreet1", "name": "начало улицы", "x": 72, "y": 48, "w": 440, "h": 70},
            {"room": "ChrisStreet2", "name": "середина улицы", "x": 72, "y": 134, "w": 440, "h": 70},
            {"room": "ChrisStreet3", "name": "конец улицы", "x": 72, "y": 220, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 306, "w": 440, "h": 70},
        ],
        "dorm_road": [
            {"room": "DormRoad1", "name": "остановка", "x": 72, "y": 48, "w": 440, "h": 70},
            {"room": "DormRoad2", "name": "поворот", "x": 72, "y": 134, "w": 440, "h": 70},
            {"room": "DormRoad3", "name": "общежитие", "x": 72, "y": 220, "w": 440, "h": 70},
            {"room": None, "name": "пусто", "x": 72, "y": 306, "w": 440, "h": 70},
        ]
    }

    # Фон подлокаций на центральной карте.
    # "type": "solid" — сплошной цвет; "type": "image" — PNG-изображение.
    PHONE_SUBLOCATION_BACKGROUNDS = {

    }

    # Связь room-переменной с маркером игрока на карте.
    # Формат: "room": (location, sublocation, подпись, x, y)
    # x/y — координаты коричневого квадратика на центральной карте.
    PHONE_ROOM_BINDINGS = {
        "PemchkPhysic0": ("pemchik", "physic", "Физмат, 0 этаж", 500, 340),
        "PemchkPhysic1": ("pemchik", "physic", "Физмат, 1 этаж", 500, 260),
        "PemchkPhysic2": ("pemchik", "physic", "Физмат, 2 этаж", 430, 144),
        "PemchkPhysic3": ("pemchik", "physic", "Физмат, 3 этаж", 500, 100),
        "PemchkMain1": ("pemchik", "main", "Главкорпус, 1 этаж", 500, 300),
        "PemchkMain2": ("pemchik", "main", "Главкорпус, 2 этаж", 500, 205),
        "PemchkMain3": ("pemchik", "main", "Главкорпус, 3 этаж", 500, 110),
        "PemchkGum0": ("pemchik", "gum", "ГУМ, 0 этаж", 500, 315),
        "PemchkGum1": ("pemchik", "gum", "ГУМ, 1 этаж", 500, 210),
        "PemchkGum2": ("pemchik", "gum", "ГУМ, 2 этаж", 500, 115),
        "ChrisStreet1": ("chris_street", "chris_street", "Улица Криса, начало", 150, 150),
        "ChrisStreet2": ("chris_street", "chris_street", "Улица Криса, середина", 300, 245),
        "ChrisStreet3": ("chris_street", "chris_street", "Улица Криса, конец", 465, 350),
        "DormRoad1": ("dorm_road", "dorm_road", "Дорога, остановка", 130, 145),
        "DormRoad2": ("dorm_road", "dorm_road", "Дорога, поворот", 300, 250),
        "DormRoad3": ("dorm_road", "dorm_road", "Общежитие", 470, 350)
    }

    PHONE_QUESTS = {
        "pisa_1": {
            "name": "ПИСА I 1111111111111111111",
            "desc": "Найти первую точку задания.",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 92, 67),
                2: ("pemchik", "physic", "PemchkPhysic2", 360, 185),
                3: ("pemchik", "main", "PemchkMain2", 310, 240),
            },
        },
        "pisa_2": {
            "name": "ПИСА II 1111111111111111111 ",
            "desc": "Появится после взятия задания.",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic1", 470, 345),
            },
        },
        "lost_badge": {
            "name": "Потерянный пропуск 1111111111111",
            "desc": "Найти пропуск около корпуса.",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic0", 68, 520),
                2: ("pemchik", "gum", "PemchkGum0", 320, 440),
            },
        },
        "library_key": {
            "name": "Ключ библиотеки 1111111111111",
            "desc": "Проверить аудитории и библиотеку.",
            "targets": {
                1: ("pemchik", "main", "PemchkMain1", 150, 410),
                2: ("pemchik", "main", "PemchkMain3", 420, 150),
                3: ("pemchik", "gum", "PemchkGum2", 225, 170),
            },
        },
        "new_quest": {
            "name": "Новое задание 1111111111",
            "desc": "",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 40, 40),
            },
        },
        "new_quest_2": {
            "name": "Новое задание 11111111111",
            "desc": "",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 40, 40),
            },
        },
        "new_quest_3": {
            "name": "Новое задание 11111111111",
            "desc": "",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 40, 40),
            },
        },
        "new_quest_4": {
            "name": "Новое задание 11111111111",
            "desc": "",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 40, 40),
            },
        },
        "new_quest_5": {
            "name": "Новое задание 11111111111",
            "desc": "",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 40, 40),
            },
        },
        "new_quest_6": {
            "name": "Новое задание 11111111111",
            "desc": "",
            "targets": {
                1: ("pemchik", "physic", "PemchkPhysic3", 40, 40),
            },
        }
    }

    
    PHONE_ROOM_MARKERS_DISABLED = []
    PHONE_QUEST_MARKERS_DISABLED = {}

    # Правая часть телефона в журнале — это крупные зоны навигации.
    PHONE_ROUTE_NAV = [
        ("pemchik", "ПЕМЧК"),
        ("chris_street", "Улица Криса"),
        ("dorm_road", "Дорога в общежитие"),
    ]

    def phone_location_items():
        return [(key, PHONE_LOCATIONS[key]) for key, _name in PHONE_ROUTE_NAV if key in PHONE_LOCATIONS]

    def phone_sublocation_items(location_key=None):
        location_key = location_key or getattr(store, "phone_map_location", "pemchik")
        loc = PHONE_LOCATIONS.get(location_key, PHONE_LOCATIONS["pemchik"])
        result = []
        for sub_key in loc.get("sublocations", []):
            if sub_key in PHONE_SUBLOCATIONS:
                result.append((sub_key, PHONE_SUBLOCATIONS[sub_key]))
        return result

    def phone_get_sublocation_rooms(sublocation_key=None):
        sublocation_key = sublocation_key or getattr(store, "phone_map_sublocation", "physic")
        return PHONE_SUBLOCATIONS.get(sublocation_key, PHONE_SUBLOCATIONS["empty"]).get("rooms", [])

    def phone_get_sublocation_room_objects(sublocation_key=None):
        sublocation_key = sublocation_key or getattr(store, "phone_map_sublocation", "physic")
        if sublocation_key in PHONE_ROOM_UI_LAYOUTS:
            return PHONE_ROOM_UI_LAYOUTS[sublocation_key]
        return []

    def phone_get_sublocation_background(sublocation_key=None):
        sublocation_key = sublocation_key or getattr(store, "phone_map_sublocation", "physic")
        return PHONE_SUBLOCATION_BACKGROUNDS.get(sublocation_key, {
            "type": "solid",
            "color": "#1b1b1b",
        })

    def phone_set_route(route_key):
        store.phone_selected_route = route_key
        store.phone_map_location = route_key
        subs = phone_sublocation_items(route_key)
        valid_subs = [key for key, _data in subs]
        if store.phone_map_sublocation not in valid_subs:
            store.phone_map_sublocation = valid_subs[0] if valid_subs else None
        _phone_safe_restart()

    def phone_get_route_name(route_key=None):
        route_key = route_key or getattr(store, "phone_selected_route", "pemchik")
        for key, name in PHONE_ROUTE_NAV:
            if key == route_key:
                return name
        return route_key

    def phone_route_has_quest_marker(route_key):
        qtarget = phone_selected_quest_target()
        return bool(qtarget and qtarget.get("location") == route_key)

    def phone_route_has_player_marker(route_key):
        pmarker = phone_get_player_marker()
        return bool(pmarker and pmarker.get("location") == route_key)

    def phone_get_location_name(location_key=None):
        location_key = location_key or getattr(store, "phone_map_location", "pemchik")
        return PHONE_LOCATIONS.get(location_key, {}).get("name", location_key)

    def phone_get_sublocation_name(sublocation_key=None):
        sublocation_key = sublocation_key or getattr(store, "phone_map_sublocation", "physic")
        return PHONE_SUBLOCATIONS.get(sublocation_key, {}).get("name", sublocation_key or "пусто")

    def phone_get_sublocation_short(sublocation_key=None):
        # Compatibility alias: short deprecated, use name.
        return phone_get_sublocation_name(sublocation_key)

    def phone_set_map_location(location_key):
        # Это выбор большой зоны. Он НЕ является room.
        store.phone_map_location = location_key
        store.phone_selected_route = location_key
        subs = phone_sublocation_items(location_key)
        valid_subs = [key for key, _data in subs]
        if store.phone_map_sublocation not in valid_subs:
            store.phone_map_sublocation = valid_subs[0] if valid_subs else None
        _phone_safe_restart()

    def phone_set_map_sublocation(sublocation_key):
        # Это нижняя вкладка корпуса/подлокации.
        # Стадия задания тоже может выставлять эту переменную автоматически через phone_select_quest().
        if sublocation_key is not None:
            store.phone_map_sublocation = sublocation_key
            sub = PHONE_SUBLOCATIONS.get(sublocation_key, {})
            if sub.get("location"):
                store.phone_map_location = sub["location"]
                store.phone_selected_route = sub["location"]
        _phone_safe_restart()

    def phone_set_room(room_key):
        # Центральные синие кнопки теперь меняют ТОЛЬКО комнату.
        # Они не меняют phone_map_sublocation.
        if room_key is not None:
            store.room = room_key
        _phone_safe_restart()

    def phone_parse_room_components(room_key):
        # Фолбэк для новых строковых room без записи в PHONE_ROOM_BINDINGS.
        # Добавляй точные комнаты в PHONE_ROOM_BINDINGS, если нужны свои координаты.
        if not isinstance(room_key, str):
            return None
        if room_key.startswith("PemchkPhysic"):
            return ("pemchik", "physic", "Физмат, " + room_key.replace("PemchkPhysic", "") + " этаж", 40, 40)
        if room_key.startswith("PemchkMain"):
            return ("pemchik", "main", "Главкорпус, " + room_key.replace("PemchkMain", "") + " этаж", 40, 40)
        if room_key.startswith("PemchkGum"):
            return ("pemchik", "gum", "ГУМ, " + room_key.replace("PemchkGum", "") + " этаж", 40, 40)
        if room_key.startswith("ChrisStreet"):
            return ("chris_street", "chris_street", "Улица Криса", 40, 40)
        if room_key.startswith("DormRoad"):
            return ("dorm_road", "dorm_road", "Дорога в общежитие", 40, 40)
        return None

    def phone_get_player_marker():
        room_key = getattr(store, "room", "PemchkPhysic1")
        if room_key in PHONE_ROOM_MARKERS_DISABLED:
            return None
        marker = PHONE_ROOM_BINDINGS.get(room_key)
        if marker is None:
            marker = phone_parse_room_components(room_key)
        if marker is None:
            return {
                "room": room_key,
                "location": getattr(store, "phone_map_location", "pemchik"),
                "sublocation": getattr(store, "phone_map_sublocation", "physic"),
                "label": room_key,
                "x": 40,
                "y": 40,
            }
        loc, sub, label, x, y = marker
        return {"room": room_key, "location": loc, "sublocation": sub, "label": label, "x": x, "y": y}

    def phone_get_quest_progress(quest_id):
        return int(store.phone_quest_progress.get(quest_id, 0))

    def phone_set_quest_progress(quest_id, progress):
        store.phone_quest_progress[quest_id] = max(0, int(progress))
        _phone_safe_restart()

    def phone_add_quest_progress(quest_id, delta):
        phone_set_quest_progress(quest_id, phone_get_quest_progress(quest_id) + delta)

    def phone_unpack_quest_target(raw_target):
        if len(raw_target) == 5:
            loc, sub, room_key, map_x, map_y = raw_target
            button_x = 36
            button_y = 25
        elif len(raw_target) == 7:
            loc, sub, room_key, map_x, map_y, button_x, button_y = raw_target
        else:
            raise Exception("Quest target must be 5 or 7 values")
        return {
            "location": loc,
            "sublocation": sub,
            "room": room_key,
            "x": map_x,
            "y": map_y,
            "map_x": map_x,
            "map_y": map_y,
            "marker_x": map_x,
            "marker_y": map_y,
            "button_x": button_x,
            "button_y": button_y,
        }

    def phone_get_quest_target(quest_id):
        progress = phone_get_quest_progress(quest_id)
        if progress <= 0:
            return None
        if progress in PHONE_QUEST_MARKERS_DISABLED.get(quest_id, []):
            return None
        quest = PHONE_QUESTS.get(quest_id)
        if not quest:
            return None
        targets = quest.get("targets", {})
        if progress in targets:
            raw_target = targets[progress]
        else:
            available = [stage for stage in targets if stage <= progress and stage not in PHONE_QUEST_MARKERS_DISABLED.get(quest_id, [])]
            if not available:
                return None
            raw_target = targets[max(available)]
        return phone_unpack_quest_target(raw_target)

    def phone_select_quest(quest_id):
        store.phone_selected_quest = quest_id
        target = phone_get_quest_target(quest_id)
        if target:
            # Подлокация карты прикреплена к выбранному заданию/стадии.
            store.phone_map_location = target["location"]
            store.phone_selected_route = target["location"]
            store.phone_map_sublocation = target["sublocation"]
        _phone_safe_restart()

    def phone_selected_quest_target():
        return phone_get_quest_target(store.phone_selected_quest)

    def phone_room_has_quest_marker(room_key):
        # Отдельная проверка именно комнаты задания.
        # Используется для жёлтого квадрата прямо на кнопке комнаты/этажа.
        qtarget = phone_selected_quest_target()
        return bool(qtarget and room_key is not None and qtarget.get("room") == room_key)

    def phone_player_in_quest_room():
        # True, если текущая переменная room совпадает с room цели задания.
        qtarget = phone_selected_quest_target()
        return bool(qtarget and getattr(store, "room", None) == qtarget.get("room"))

    def phone_get_selected_quest_room():
        qtarget = phone_selected_quest_target()
        if not qtarget:
            return "нет цели"
        return qtarget.get("room", "нет room")

    def phone_active_quests():
        return [(qid, q) for qid, q in PHONE_QUESTS.items() if phone_get_quest_progress(qid) > 0]

    # ---------- данные инфо/персонажей ----------
    PHONE_INFO_SECTIONS = [
        ("intro", "Для тебя, Крис"),
        ("battle", "Бой"),
        ("items", "Предметы"),
        ("trade", "Торговля"),
        ("mechanics", "и др. механики"),
        ("characters", "Персонажи"),
    ]

    # Подразделы верхнего уровня: ключ раздела -> [(sub_key, sub_name), ...]
    PHONE_INFO_SUBSECTIONS = {
        "intro": [
            ("intro_text", "Для тебя, Крис"),
        ],
        "battle": [
            ("battle_intro",   "Основы боя"),
            ("battle_stats",   "Характеристики"),
            ("battle_damage",  "Нанесение урона"),
            ("battle_damage_taken", "Получение урона"),
            ("battle_social",  "Действие"),
            ("battle_items",   "Применение предметов"),
            ("battle_tables",  "Подробные формулы"),
        ],
        "items": [
            ("items_inventory",     "Инвентарь"),
            ("items_wash_identify", "Стирка и опознание"),
            ("items_sets",          "Сеты"),
        ],
        "trade": [
            ("trade_main", "Торговля"),
        ],
        "mechanics": [],
        "characters": [],
    }

    # Содержимое разделов. Показывается, когда выбран конкретный подраздел.
    PHONE_INFO_CONTENT = {
        "intro_text": (
            "Для тебя, Крис.\n\n"
            "Крис, надеюсь, ты это читаешь не прямо во время боя, а когда нашлась "
            "свободная минута. Я попросила Эмили сделать для тебя приложение по тому, "
            "как правильно нужно драться. Всяко лучше, чем таскать с собой книжку в "
            "полкило. Мне кажется, внутри себя ты давно уже знаешь, как постоять за "
            "себя, просто тебе нужно немного вспомнить как это делается."
        ),
        "battle_intro": (

            "Бой делится на раунды. А в раунде, как у всего в этой жизни, наступает "
            "свой черёд. Сначала очередь врага, если он решается атаковать, а затем "
            "твоей команды.\n\n"
            "Выбирает, кто будет ходить первым... Согласованность? Вы же в своей "
            "команде думаете, как будете действовать, верно? Но иногда есть те, кто "
            "лезет нарожон и те, кто хотел бы завершить этот раунд, сходив последним. "
            "Бой закончится, когда ты убедишь противника, что между вами больше "
            "общего, чем он думает. Или убьёшь его. Не знаю, хватит ли тебе решимости "
            "сделать такое.\n\n"
            "--- В свой ход ты можешь: ---\n\n"
            "- наносить урон одним из нескольких вариантов атак. Как по врагам, так "
            "и по своим сокомандникам.\n"
            "- применить магию на кого хочешь. Это может быть как огненный шар, так "
            "и лечение.\n"
            "- действовать.\n"
            "- использовать предмет как на себя, так и на союзника или врага.\n\n"
            "В большинстве случаев ты должен навестись SOUL OBJECT и кликнуть по "
            "противнику вариантом атаки/магии/действия/предмета.\n\n"
            "Когда ты сделаешь свой ход, другие члены твоей компании тоже смогут его "
            "сделать. Раунд заканчивается, когда все сделали свой ход."
        ),
        "battle_stats": (
            "У всего есть характеристики, Крис.\n\n"
            "Базовая характеристика (база) даётся тебе с рождения и увеличивается по "
            "мере твоего развития.\n\n"
            "Характеристики от артефактов даются, когда ты надеваешь артефакты на "
            "себя.\n\n"
            "Бонусная характеристика — значение, на которое умножается в % базовая "
            "характеристика.\n\n"
            "Дебафы — это состояние, в котором ты можешь находиться, настроение. Они "
            "увеличивают или уменьшают значение базовой характеристики в зависимости "
            "от количества стаков. Дебафы снимаются по одному стаку в конце каждого "
            "раунда.\n\n"
            "--- Итоговая формула ---\n\n"
            "Если характеристика в числах:\n"
            "(база + артефакты) + (база * бонус%) + (5% * дебафф)\n\n"
            "Если характеристика в процентах:\n"
            "база + артефакты + бонус% + 5% * дебафф"
        ),
        "battle_damage": (
            "Помимо атаки и магии (которой ты тоже можешь наносить урон), есть "
            "точность, крит. шанс и крит. урон.\n\n"
            "Некоторые атаки и магия имеют перезарядку — как изначальную, так и "
            "промежуточную после использования.\n\n"
            "Точность — шанс того, что ты попадёшь по противнику.\n"
            "Критический урон — насколько вся твоя атака умножается при срабатывании "
            "критического шанса.\n\n"
            "Дополнительные переменные:\n"
            "- Исполнение — множитель от точности выполнения MINIGAME. Изначально 0, "
            "обычно не больше 100%.\n"
            "- Множитель следующей атаки — редкий модификатор.\n"
            "- Индивидуальный множитель атаки — у каждой атаки свои особенности. "
            "Стандарт 100%.\n\n"
            "Урон = атака * исполнение * Индивидуальный множитель * Множитель "
            "следующей атаки * крит.урон - защита цели\n\n"
        ),
        "battle_damage_taken": (
            "Урон по тебе работает так же, как и твоё нанесениение урона. Если урон направлен на одиночную цель, "
            "каждый раз при пересечении SOUL OBJECT с вражеским снарядом выбирается "
            "случайная жертва на основании Танк. Танк имеет ограничение от 25 до 50.\n\n"
            "Когда персонаж или противник имеет щит, при попадании атакой урон "
            "не наносится.\n\n"
            "У противника тоже есть свои боевые характеристики, включающие шанс попадания, Крит шанс и Крит урон. \n\n"
            "Скорость противника отвечает за то, с какой скоростью будут лететь его снаряды. "
            "Максимальные и минимальные скорости у вас и противника - от 50% до 150%\n\n"
            "Магия у противника не отвечает за урон изначально. Она отвечает за то, с каким шансом "
            "противник запустит в вас при увороте дополнительные снаряды\n\n"
            "У каждого противника есть свои пассивные способности. Часть из них постоянная. "
            "Часть из них зависит от настроения."
        ),
        "battle_social": (
            "У тебя 12 универсальных действий, чтобы прийти к мирному решению.\n\n"
            "Осмотреть. Позволяет определить, какие у противника есть характеристики "
            "и какие варианты какой имеют эффект: негативный (откатывает "
            "договорённости), нейтральный (ничего не произойдёт) или позитивный.\n\n"
            "Следующие 10 действий выбирают твой подход к противнику. Каждое "
            "действие на каждом противнике имеет свою сложность и требует броска "
            "кубика д20, значение которого должно быть больше сложности действия.\n\n"
            "Формула твоих социальных характеристик:\n"
            "Итог = база + артефакты + дебафф\n\n"
            "Когда ты успешно совершишь бросок, ты узнаешь, эффективное это действие "
            "или нет. Сложность броска зависит от настроения противника и действий "
            "по отношению к нему.\n\n"
            "Когда прогресс пощады при успешных действиях дойдёт до определённого "
            "значения, настроение врага поменяется. Тогда ты перестанешь знать, что "
            "дают действия, и придётся снова находить подход.\n\n"
            "Прогресс засчитывается в зависимости от «дипломатии» — чем её больше, "
            "тем быстрее прогресс пощады накапливается. Очарование — это шанс, когда "
            "прогресс пощады при удачном действии будет двойной."
        ),
        "battle_items": (            
            "В предметах можно использовать 3 группы: расходники, одноразовое "
            "оружие и сеты.\n\n"
            "- Расходники поддерживают тебя физически. Ты не сможешь использовать "
            "их больше, чем в тебя влезет. Для определения места существует шкала "
            "аппетита в виде кружочка. Кружочек заполняется цветами в зависимости "
            "от вида еды: полезная (зелёный), фастфуд (красный), сладости (жёлтый), "
            "напитки (синий), прочие (белый). Учитывай предпочтения друзей — "
            "эффективность еды в бою зависит от соблюдения их вкусов.\n\n"
            "Расходники можно использовать и в открытом мире. Аппетит персонажей "
            "сбрасывается раз в ход и в случайное время при прогулке.\n\n"
            "- Одноразовое оружие используется, чтобы нанести урон противнику или "
            "наложить эффекты. При нанесении урона учитывает щиты противника, но не "
            "учитывает его броню.\n\n"
            "- Если ты собрал на себе набор из артефактов, то можешь использовать "
            "его активную способность."
        ),
        "battle_tables": (

            "Эмили почему-то решила, что будет важным написать подробные формулы под каждую характеристику. "
            "Не думаю, что ты будешь в это сильно углубляться. Но пускай будет. Не лишнее.\n\n"
            
            "ОБЩАЯ СТРУКТУРА ПАРАМЕТРОВ:\n"
                "  База       — базовый показатель от уровней;\n"
                "  Арт        — суммарная прибавка от артефактов и активных сетов;\n"
                "  Бонус%     — бонусное значение в %;\n"
                "  Бафф/дебаф — текущее количество стаков эффекта. Отрицальное \n"
                "  значение стаков даёт дебафф \n\n"

            "  === БОЕВЫЕ ХАРАКТЕРИСТИКИ ===\n\n"

            "1. ЗДОРОВЬЕ И МАНА: \n"
            "    Макс HP/Макс MP = База + Артефакт\n\n"

            "2. АТАКА И МАГИЯ: \n"
            "    Атака = (База + Арт) + (База * Бонус%) + (База * 10%*Бафф)\n"
            "    Бафф:   Бодрость.\n"
            "    Дебафф: Истощение.\n"

            "    Магия = (База + Арт) + (База * Бонус%) + (База * 15%*Бафф )\n"
            "    Бафф:   Просвещение \n"
            "    Дебафф: Помутнение \n\n"


            "3. ТОЧНОСТЬ И КРИТИЧЕСКИЕ УДАРЫ:\n"
            "    Точность = База + Арт + Бонус% + 5%*Бафф\n"
            "    Бафф:   Концентрация.\n"
            "    Дебафф: Страх.\n\n"
            
            "    Крит.шанс = База + Арт + Бонус% + 5%*Бафф + Сверхточность\n"
            "    Сверхточность = точность - 100%. При 115% = 15%. При значениях \n"
            "       ниже 100% = 0.\n"
            "    Бафф:   Удача.\n"
            "    Дебафф: Сглаз.\n\n"

            "    Крит.урон = База + Арт + Бонус% + 5%*бафф + Сверхкрит\n"
            "    Сверхкрит = 50%(точность - 100%). При 115% = 7,5%. При значениях \n"
            "       ниже 100% = 0.\n"
            "    Бафф:   Гнев.\n"
            "    Дебафф: Безразличие.\n\n"

            "4. ЗАЩИТА:\n"
            "    Защита = (База + Арт) + (База * Бонус%) + (База * 15%*Бафф)\n"
            "    Бафф:   Печаль.\n"
            "    Дебафф: Вдохновение.\n\n"


            "5. ТАНК:\n"
            "   Танк = База + Бонус + штраф с 'упал' + 5*Бафф\n"
            "   Значения от 25 до 50.\n"
            "   Если персонаж упал, то = 10\n"
            "   Бафф:   Уязвимость.\n"
            "   Дебафф: Скрытность.\n\n"

            "6. РАСЧЁТ УРОНА: \n"    
            "  Урон = Атака * Крит. урон (при срабатывании) * исполнение \n"
            "         * множитель след. атаки * множитель индивид. атаки\n"
            "         - Защита цели)\n\n"


            "  Исполнение = База + Арт + бонус\n"
            "      База = 0. Набирается каждый раз при исполнении атаки.\n"                
            "      Максимальное значение 120% \n"
            "  \n\n"

            "Снижение урона при высоких значениях (пороги штрафов):\n"
            "  до 400 (x1.0) | 400–500 (x0.97) | 500–600 (x0.94) | 600–700 (x0.9)\n"
            "  700–800 (x0.86) | 800–900 (x0.83) | 900–1000 (x0.8) | 1000–1100 (x0.77)\n"
            "  >1100 (x0.75)\n\n"

            "=== СОЦИАЛЬНЫЕ ХАРАКТЕРИСТИКИ ===\n\n"
        
            "  СОЦИАЛИЗАЦИЯ = База + Бонус + Арт\n"
            "  ДИПЛОМАТИЯ   = База + Бонус + Арт\n"
            "  ОЧАРОВАНИЕ   = База + Бонус + Арт + 3*Удача(Сглаз)\n"
            "  ВОСПРИЯТИЕ   = База + Бонус + Арт + Помутнение(Просвещение)\n"
            "  РИТОРИКА     = База + Бонус + Арт + Концентрация(Страх)\n"
            "  АРТИСТИЗМ    = База + Бонус + Арт + Уязвимость(Скрытность)\n"
            "  КОМФОРТ      = База + Бонус + Арт + Вдохновение(Печаль)\n"
            "  ВЛАСТЬ       = База + Бонус + Арт + Гнев(Безразличие)\n\n"

        ),
        "items_inventory": (
            "В левой части находится раздел с предметами. Где можно "
            "экипировать или использовать артефакты, расходники и "
            "одноразовое оружие.\n\n"
            "Наведя на них SOUL OBJECT, ты можешь увидеть их описание. "
            "Нажав на кнопку лупы, ты можешь настроить 3 режима "
            "отображения:\n"
            "- будет ли показываться тебе только боевые характеристики;\n"
            "- будет ли показываться полное описание;\n"
            "- не будет показываться ничего.\n\n"
            "Среднюю часть занимают базовые характеристики + "
            "характеристики от артефактов у выбранного тобой персонажа "
            "и текущий аппетит. Сверху имеется переключатель для выбора "
            "персонажа. Для показа более подробных текущих персонажей "
            "можно навестись на. Кнопкой бой и соц ты выбираешь, какие "
            "характеристики будут отображаться.\n\n"
            "Последняя часть — это надетые артефакты выбранного "
            "персонажа. Наведя на них, ты получаешь описание. Нажимая — "
            "снимаешь. Кнопка «Сеты» показывает справочник наборов "
            "артефактов, которые ты собрал. В справочнике сетов при "
            "наведении на артефакт показывается его описание и боевые "
            "характеристики."
        ),
        "items_wash_identify": (
            "Каждый артефакт имеет свой эффект после стирки. Он может "
            "улучшиться, получив дополнительный эффект; ничего не "
            "получить или уничтожиться, превратившись в мусор. Поэтому... "
            "Делай всё на свой страх и риск.\n\n"
            "Поскольку ты живёшь в общежитии, стирка у тебя бесплатная. "
            "Можешь засунуть до 4 артефактов. И подождать 7 мин. Или "
            "заняться своими делами?..\n\n"
            "Опознанию поддаются лишь некоторые артефакты. У каждого "
            "артефакта есть своя цена и шанс опознания. При удачном "
            "опознании появляются дополнительные эффекты.\n\n"
            "Эффекты у артефактов при опознании и стирке обычно "
            "улучшают боевые или социальные характеристики."
        ),
        "items_sets": (
            "Справочник сетов показывает все наборы артефактов, которые "
            "ты собирал хотя бы раз.\n\n"
            "Когда кто-то экипирует или снимает сет, характеристики от "
            "сета будет видно в центральной части экрана. А активная "
            "способность, если она имеется у сета, показана в "
            "справочниках сетов.\n\n"
            "Слева — список открытых сетов. В центре — состав сета и "
            "описание. Справа — характеристики, которые сет даёт. "
            "Наведись на артефакт в составе, чтобы увидеть его описание "
            "и боевые характеристики."
        ),
        "trade_main": (
            "Экран торговли делится на три части:\n"
            "- предметы и деньги твоей команды;\n"
            "- предметы на обмен;\n"
            "- предметы на продажу у торговца и его отношение к нам.\n\n"
            "Наведя на предметы, ты можешь получить их описание, точно "
            "как в инвентаре. Нажав на них, ты помещаешь их в обмен или "
            "обратно в инвентарь/торговцу.\n\n"
            "Цены у торговца зависят от его отношения, которое зависит "
            "от твоей репутации и баффов от расходников, баффов и прочих "
            "возможных эффектов."
        ),
    }
    

    PHONE_CHARACTER_NAMES = [
        "Крис", "Азриель", "Чара",
        "Фриск", "Кловер", "Арчи",
        "Иззи", "Седрик", "Сильвия",
        "Фабри", "Эмили", "Ральзей",
        "Сьюзи", "Ноэлль", "Санс", "Бердли",
        "Перс 17",
    ]

    def phone_get_character_names():
        if hasattr(store, "pers_dict") and store.pers_dict:
            names = list(store.pers_dict.keys())
            result = []
            for n in PHONE_CHARACTER_NAMES:
                if n in names and n not in result:
                    result.append(n)
            for n in names:
                if n not in result:
                    result.append(n)
            while len(result) < 17:
                result.append("Пусто %d" % (len(result) + 1))
            return result[:17]
        return PHONE_CHARACTER_NAMES[:]

    def phone_select_info_section(section_key):
        store.phone_info_section = section_key
        store.phone_info_subsection = None
        if section_key == "characters":
            store.phone_panel = "party"
        else:
            store.phone_panel = "info"
            # Если у раздела только один подраздел — открываем его сразу,
            # чтобы не заставлять кликать дважды (актуально для «Для тебя, Крис»).
            subs = PHONE_INFO_SUBSECTIONS.get(section_key, [])
            if len(subs) == 1:
                store.phone_info_subsection = subs[0][0]
        _phone_safe_restart()

    def phone_select_info_subsection(sub_key):
        store.phone_info_subsection = sub_key
        _phone_safe_restart()

    def phone_info_back():
        # Назад: сначала с подраздела на список подразделов,
        # затем с подразделов на список верхних разделов.
        if store.phone_info_subsection is not None:
            store.phone_info_subsection = None
        else:
            store.phone_info_section = None
        _phone_safe_restart()

    def phone_info_go_home():
        store.phone_info_section = None
        store.phone_info_subsection = None
        _phone_safe_restart()

    def phone_info_section_name(section_key):
        for key, name in PHONE_INFO_SECTIONS:
            if key == section_key:
                return name
        return section_key or ""

    def phone_info_subsection_name(sub_key):
        if not sub_key:
            return ""
        subs = PHONE_INFO_SUBSECTIONS.get(getattr(store, "phone_info_section", None), [])
        for key, name in subs:
            if key == sub_key:
                return name
        return sub_key

    def phone_info_breadcrumb():
        # Строит строку, начиная с названия выбранного раздела.
        # Уровень 2 (только раздел): "бой"
        # Уровень 3 (раздел + подраздел): "бой → основы боя"
        parts = []
        sec = getattr(store, "phone_info_section", None)
        sub = getattr(store, "phone_info_subsection", None)
        if sec and sec != "characters":
            parts.append(phone_info_section_name(sec).lower())
        if sub:
            parts.append(phone_info_subsection_name(sub).lower())
        return " —> ".join(parts) if parts else ""

    def phone_info_get_content(sub_key):
        if not sub_key:
            return ""
        return PHONE_INFO_CONTENT.get(sub_key, "Содержимое раздела пока не заполнено.")

    # Кэш измеренных высот текста для подразделов.
    # Содержимое PHONE_INFO_CONTENT статично, поэтому считать нужно один раз.
    _phone_info_height_cache = {}

    def phone_info_content_height(sub_key):
        """Приблизительная высота текста подраздела в пикселях."""
        if sub_key in _phone_info_height_cache:
            return _phone_info_height_cache[sub_key]

        text_value = PHONE_INFO_CONTENT.get(sub_key, "")
        if not text_value:
            _phone_info_height_cache[sub_key] = 0
            return 0

        height = 0
        try:
            # Реальное измерение через рендер Ren'Py.
            from renpy.display.text import Text as RText
            t = RText(text_value, size=22)
            # 810 — ширина viewport без vbar; по высоте не ограничиваем.
            r = renpy.render(t, 810, 100000, 0, 0)
            height = r.height
        except Exception:
            # Резервная оценка, если рендер недоступен.
            avg_char_w = 12.0
            line_h = 30.0
            chars_per_line = max(1, int(810 / avg_char_w))
            total_lines = 0
            for line in text_value.split("\n"):
                if not line:
                    total_lines += 1
                else:
                    total_lines += max(1, (len(line) + chars_per_line - 1) // chars_per_line)
            height = int(total_lines * line_h)

        _phone_info_height_cache[sub_key] = height
        return height

    def phone_info_needs_vbar(sub_key):
        """True, если содержимое подраздела не помещается во viewport (высота 590)."""
        return phone_info_content_height(sub_key) > 590

    def phone_select_character(char_name):
        store.phone_selected_character = char_name
        store.phone_info_section = "characters"
        store.phone_panel = "party"
        _phone_safe_restart()

    def phone_select_character_tab(tab_key):
        store.phone_character_info_tab = tab_key
        _phone_safe_restart()

    def phone_get_character_object(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        pd = getattr(store, "pers_dict", None)
        if isinstance(pd, dict) and char_name in pd:
            return pd[char_name]
        chars = getattr(store, "characters", None)
        if isinstance(chars, dict) and char_name in chars:
            return chars[char_name]
        return None

    def phone_safe_attr(obj, attr, default="—"):
        if obj is None:
            return default
        try:
            value = getattr(obj, attr)
        except Exception:
            return default
        if value is None:
            return default
        return value

    def phone_fmt_stat(value):
        try:
            if isinstance(value, float):
                return "%.2f" % value
            return str(value)
        except Exception:
            return "—"

    def phone_fmt_percent(value):
        try:
            return "%d%%" % int(round(float(value) * 100))
        except Exception:
            return phone_fmt_stat(value)

    def phone_character_main_stats(char_name=None):
        char = phone_get_character_object(char_name)
        if char is None:
            return [
                ("HP", "—"),
                ("MP", "—"),
                ("Атака", "—"),
                ("Магия", "—"),
                ("Защита", "—"),
                ("В команде", "—"),
            ]

        hp = "%s/%s" % (phone_fmt_stat(phone_safe_attr(char, "current_hp")), phone_fmt_stat(phone_safe_attr(char, "max_hp")))
        mp = "%s/%s" % (phone_fmt_stat(phone_safe_attr(char, "current_mp")), phone_fmt_stat(phone_safe_attr(char, "max_mp")))

        return [
            ("Уровень", phone_fmt_stat(phone_safe_attr(char, "level"))),
            ("HP", hp),
            ("MP", mp),
            ("Атака", phone_fmt_stat(phone_safe_attr(char, "atk"))),
            ("Магия", phone_fmt_stat(phone_safe_attr(char, "magic"))),
            ("Защита", phone_fmt_stat(phone_safe_attr(char, "defense"))),
            ("Крит. шанс", phone_fmt_percent(phone_safe_attr(char, "critrate"))),
            ("Крит. урон", phone_fmt_stat(phone_safe_attr(char, "crit"))),
            ("Точность", phone_fmt_percent(phone_safe_attr(char, "dmgchance"))),
            ("Отношение", phone_fmt_stat(phone_safe_attr(char, "reltns"))),
            ("Сытость", "%s/%s" % (phone_fmt_stat(phone_safe_attr(char, "current_feedness")), phone_fmt_stat(phone_safe_attr(char, "max_feedness")))),
            ("В команде", phone_fmt_stat(phone_safe_attr(char, "picked"))),
        ]

    def phone_character_social_stats(char_name=None):
        char = phone_get_character_object(char_name)
        return [
            ("Социализация", phone_fmt_stat(phone_safe_attr(char, "socialization"))),
            ("Дипломатия", phone_fmt_stat(phone_safe_attr(char, "diplomacy"))),
            ("Очарование", phone_fmt_stat(phone_safe_attr(char, "charm")) + "%"),
            ("Восприятие", phone_fmt_stat(phone_safe_attr(char, "perception"))),
            ("Риторика", phone_fmt_stat(phone_safe_attr(char, "rhetoric"))),
            ("Артистизм", phone_fmt_stat(phone_safe_attr(char, "artistry"))),
            ("Комфорт", phone_fmt_stat(phone_safe_attr(char, "comfort"))),
            ("Власть", phone_fmt_stat(phone_safe_attr(char, "power"))),
        ]

    def phone_character_notes_text(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        notes = getattr(store, "phone_character_notes", {})
        if isinstance(notes, dict):
            return notes.get(char_name, "Место для будущих записей.\nМожно позже вывести сюда биографию, заметки, отношения или сюжетные факты.")
        return "Место для будущих записей."

    PHONE_CHARACTER_DESCRIPTIONS = {
        "Крис": "Крис — игрок. Использует меч и щит. Сбалансированный персонаж с хорошей защитой и атакой. Стремится защищать друзей.",
        "Чара": "Чара — таинственная фигура. Высокая атака и критический урон. Способна наносить огромный урон за один удар.",
        "Азриель": "Азриель — наследник Дреммуров. Сбалансированная магия и атака. Может использовать как магию, так и физическую атаку.",
        "Фриск": "Фриск — решительный персонаж. Очень высокая точность и критический шанс. Атакует быстро и эффективно.",
        "Иззи": "Иззи — маг-бояк. Специализируется на магии и социальных навыках. Имеет на один уровень больше остальных.",
        "Кловер": "Кловер — стрелок. Использует оружие с калибром. Высокая защита и атака.",
        "Седрик": "Седрик — мудрый персонаж. Сбалансированная атака и защита. Имеет высокие социальные характеристики.",
        "Фабри": "Фабри — созидатель, а не разрушитель. У неё нет активных атак: она призывает рукодельных друзей (до двух) и управляет их магией. Фамильяры дают команде ауры и делят с ней урон.",
        "Арчи": "Арчи — противник, временно доступный в списке персонажей.",
        "Сильвия": "Сильвия — персонаж с высокой точностью и социальными навыками.",
        "Эмили": "Эмили — аналитик и контроллер. Высокая магия и точность.",
        "Ральзей": "Ральзей — маг поддержки. Сильная магия и полезные эффекты для команды.",
        "Ноэлль": "Ноэлль — поддержка. Высокая магия и социальные навыки.",
        "Сьюзи": "Сьюзи — агрессивный персонаж. Очень высокая атака и критический шанс.",
        "Санс": "Санс — хрупкий маг с высокой точностью и сильными заклинаниями.",
        "Бердли": "Бердли — самоуверенный стратег. Сочетает физические и магические атаки, усиливая себя и ослабляя противников.",
        "Перс 17": "Дополнительный слот персонажа.",
    }

    def phone_character_description(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        return PHONE_CHARACTER_DESCRIPTIONS.get(char_name, "Описание персонажа пока недоступно.")

    PHONE_STAT_RATING_THRESHOLDS = {
        "atk": [15, 28, 40, 52],
        "magic": [5, 15, 25, 40],
        "defense": [5, 12, 18, 26],
        "critrate": [5, 12, 20, 28],
        "dmgchance": [55, 62, 68, 75],
        "socialization": [0, 3, 6, 9],
        "diplomacy": [10, 20, 35, 50],
        "charm": [5, 12, 20, 28],
        "perception": [0, 3, 6, 9],
        "rhetoric": [0, 3, 6, 9],
        "artistry": [0, 3, 6, 9],
        "comfort": [0, 3, 6, 9],
        "power": [0, 3, 6, 9],
    }

    PHONE_STAT_PERCENT_THRESHOLD = {"critrate", "dmgchance"}

    def phone_character_rating_for_stat(char, attr_name):
        if char is None:
            return 0
        thresholds = PHONE_STAT_RATING_THRESHOLDS.get(attr_name)
        if not thresholds:
            return 0
        try:
            current_value = getattr(char, attr_name)
        except Exception:
            return 0
        if attr_name in PHONE_STAT_PERCENT_THRESHOLD:
            try:
                current_value = float(current_value) * 100
            except Exception:
                return 0
        if not isinstance(current_value, (int, float)):
            try:
                current_value = float(current_value)
            except Exception:
                return 0
        rating = 0
        for i, threshold in enumerate(thresholds):
            if current_value >= threshold:
                rating = i + 1
            else:
                break
        if current_value >= thresholds[3]:
            rating = 5
        return rating

    def phone_get_xp_info(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        char = phone_get_character_object(char_name)
        if char is None:
            return 0, 1
        xp = phone_safe_attr(char, "xp", 0)
        try:
            xp = int(xp)
        except Exception:
            xp = 0
        max_xp = phone_safe_attr(char, "lvl_xp", 0)
        try:
            max_xp = int(max_xp)
        except Exception:
            max_xp = 0
        if max_xp <= 0:
            Pers_class = getattr(store, "Pers", None) or globals().get("Pers", None)
            if Pers_class is not None:
                gl = getattr(Pers_class, "global_level", 1)
                next_xp_fn = getattr(store, "get_xp_for_next_level", None)
                if next_xp_fn is not None:
                    try:
                        next_xp = next_xp_fn(gl)
                        if next_xp is not None and next_xp > 0:
                            max_xp = int(next_xp)
                    except Exception:
                        pass
        if max_xp <= 0:
            max_xp = 1
        return xp, max_xp

    def phone_get_role_bars(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        char = phone_get_character_object(char_name)
        if char is None:
            return 0, 0, 0, 0, 0
        damager = int(phone_safe_attr(char, "damager_role", 0))
        debuffer = int(phone_safe_attr(char, "debuffer_role", 0))
        tank = int(phone_safe_attr(char, "tank_role", 0))
        support = int(phone_safe_attr(char, "support_role", 0))
        nego = int(phone_safe_attr(char, "nego_role", 0))
        return damager, debuffer, tank, support, nego








    def phone_extract_named_items(obj, attr_names):
        if obj is None:
            return []
        for attr in attr_names:
            try:
                value = getattr(obj, attr)
            except Exception:
                value = None
            if not value:
                continue
            if isinstance(value, dict):
                result = []
                for key, data in value.items():
                    if isinstance(data, dict):
                        title = data.get("name", data.get("title", key))
                        desc = data.get("desc", data.get("description", ""))
                    else:
                        title = key
                        desc = data
                    result.append((str(title), str(desc)))
                return result
            if isinstance(value, (list, tuple)):
                result = []
                for item in value:
                    if isinstance(item, dict):
                        title = item.get("name", item.get("title", item.get("id", "Без названия")))
                        desc = item.get("desc", item.get("description", ""))
                    else:
                        title = str(item)
                        desc = ""
                    result.append((str(title), str(desc)))
                return result
        return []

    def _phone_ability_card(name, data=None, owner=None, category=""):
        data = data or {}
        desc = data.get("description", data.get("desc", ""))
        effects = data.get("effects", data.get("effect", ""))
        if effects and effects != desc:
            desc = "%s\n\n%s" % (desc, effects) if desc else effects
        cost = (getattr(store, "ABILITY_RESOURCE_COSTS", {}) or {}).get(name, {})
        resource = []
        if cost.get("mp") is not None:
            resource.append("Мана: %s MP" % cost.get("mp"))
        elif cost.get("mp_percent"):
            resource.append("Мана: %s%% от максимума" % int(float(cost["mp_percent"]) * 100))
        elif cost.get("mp_all"):
            resource.append("Мана: вся текущая мана")
        if cost.get("hp"):
            resource.append("HP: %s" % cost.get("hp"))
        if cost.get("hp_percent"):
            resource.append("HP: %s%% от максимума" % int(float(cost["hp_percent"]) * 100))
        cooldown = (getattr(store, "BATTLE_ABILITY_COOLDOWNS", {}) or {}).get(name, {})
        if cooldown:
            resource.append("Перезарядка:\n    Изначальная: %s\n    После использования: %s" % (
                cooldown.get("initial_cooldown", 0), cooldown.get("cooldown_after_use", 0)))
        level = data.get("level", data.get("unlock_level", ""))
        level = (PHONE_ABILITY_LEVELS.get(owner, {}) or {}).get(name, level)
        if not level and category in ("attacks", "magic", "passive"):
            level = 1
        return {"name": str(name), "description": str(desc or "Описание пока не заполнено."),
                "level": level,
                "resource": "\n".join(resource),
                "upgrade": data.get("upgrade", data.get("improvement", "")),
                "category": category or data.get("type", ""), "owner": owner}

    # Индексы открытия из спецификации. Реестр боя содержит не все уровни
    # (часть способностей создаётся как базовая), поэтому телефон использует
    # эту таблицу как источник истины.
    PHONE_ABILITY_LEVELS = {
        "Крис": {
            "Удар неудачника": 1, "защита_Крис": 1, "Удар мечом": 1, "Удар щитом": 1,
            "C разворота!": 3, "Бонк!": 4, "Пронзить": 5, "Отбить руки": 6,
            "Отчаянное комбо": 8, "Рывок защитника (атака)": 9,
            "Призвать меч": 1, "Призвать щит": 1, "Напрячься": 3, "Позвать за щит": 3,
            "Слабое место": 4, "Правильный угол": 5, "Концентрация": 7,
            "Поднять щиты!": 8, "Стремление вперёд": 9, "Рывок защитника (магия)": 9,
            "Пробудиться": 10, "Поднять щиты!!!": 10,
        },
        "Азриель": {
            "Удар принца": 1, "Взмах мечом": 1, "Щитовой удар": 3, "Удар лбом": 5,
            "Сменить облик": 1, "Шаг вперёд": 1, "Магия огня": 1, "Горное равновесие": 3,
            "Клинки хаоса": 4, "За спиною принца": 5, "Уничтожитель хаоса": 6,
            "Встать с колен": 7, "Звездный блеск": 8, "Звёздный блеск": 8,
            "Боевой клич!": 9, "Луч Бога Гиперсмерти": 10,
        },
        "Чара": {
            "Удар шпагой": 1, "Удар ножом": 1, "Удар бунтарки": 1, "Почесать спинку": 3,
            "Решето": 5, "Ножевой снаряд": 7, "Реки крови": 10,
            "Гнев": 1, "Заточить клинки": 2, "Безумие": 3, "Сумасшествие": 5,
            "Псих": 7, "Моральное разложение": 7, "Пробуждение прошлого": 10,
        },
        "Фриск": {
            "Para bellum": 1, "Potentia intellectus": 1, "Quod licet Iovi, non licet bovi": 2,
            "Проект договора": 4, "Foedus icere": 6, "Do ut des": 8, "Вернуть в диалог": 10,
        },
        "Кловер": {
            "Навскидку": 1, "Прицельный": 3, "Лассо": 5, "Разрушительный хлыст": 7,
            "Клеймо": 7, "Скорострел": 9,
            "Выбор калибра": 1, "Мелкий калибр": 1, "Средний калибр": 1, "Крупный калибр": 1,
            "Сыграем!": 1, "Помиловать": 1, "Вафельный перерыв": 2, "Суд": 3,
            "Дробовик": 4, "Метка разыскиваемого": 4, "Вызов на дуэль!": 5,
            "Длинный ствол": 6, "От судьбы не уйдёшь": 8, "Дикий запад, Крошка!": 9,
            "Гиперлуч": 10,
        },
        "Арчи": {
            "Боксёрское комбо": 1, "По полочкам": 1, "Удары богомола": 2, "Удар орла": 3,
            "Апперкот": 4, "Ураган": 5, "Мягкая ладонь": 6, "Oma yi wa mou": 8,
            "Ладони чакры": 1, "Очищение Ци": 1, "Печати ниндзюцу": 2, "Укрепление мышц": 3,
            "Рывок": 4, "Режим храбрости": 4, "Реверс энергии": 5,
            "Травмирующие удары": 6, "Вернуть отправителю": 7, "Храбрость!": 9,
        },
        "Иззи": {
            "Осколок себя": 1, "Успокоение": 1, "Медитация": 1, "Правильное дыхание": 1,
            "Благовония": 2, "Открытие пределов": 3, "Воспрять дух": 4, "Карма": 5,
            "Предвиденье": 6, "Предвидение": 6, "Зачарование": 7, "Усиление присутствия": 8,
            "Духовный лук": 9, "Пробуждение": 10,
        },
        "Седрик": {
            "Удар сковородкой": 1, "Пощёчина от шефа": 10,
            "Сбегать за продуктами": 1, "Булочка": 1, "Яичница на завтрак": 1,
            "Салат Цезарь": 2, "Сэндвич": 3, "Блинчики с кленовым сиропом": 4,
            "Бургер": 5, "Чизбургер": 5, "Суши": 6, "Мясо на гриле": 7, "Пицца!": 9,
        },
        "Сильвия": {
            "защита_Сильвия": 1, "Плие": 1, "Томбе": 1, "Glissade": 1, "Changement de pieds": 1,
            "Temps levé": 1, "Brisé": 1, "Échappé sauté": 1, "Assemblé": 1, "Sissonne": 1,
            "Chassé": 1, "Jeté entrelacé": 1, "Grand jeté": 1, "Cabriole": 1,
            "Saut de basque": 1, "Tour en l'air": 1, "Pirouette à la seconde": 1,
            "II Plié": 1, "Плие": 1, "Passé": 1, "Developpé": 1, "Arabesque": 1,
            "Attitude": 1, "Dégagé": 1, "Tour lent": 1, "Фуэте": 1, "Relevé": 1,
            "Sus-sus": 1, "Па-де-бурре": 1, "Battement soutenu": 1, "Batman fondu": 1,
            "Temps lié": 1, "Rond de jambe en l'air": 1,
        },
        "Фабри": {
            "Призвать М-ра Панцыря": 1, "Призвать М-с Пёрышко": 1,
            "Призвать М-с Морковку": 1, "Призвать М-с Манки": 1,
            "Спрятаться": 1, "Надеть панцирь": 2, "Прикрепиться": 5, "Рикошет черепахи": 7,
            "Орлиная зоркость": 1, "Небесные танцы": 2, "Снести яичко": 6, "Перьевой ураган": 8,
            "Ускориться": 1, "Не поймаешь": 3, "Поделиться морковкой": 4, "Быстрее и дальше": 9,
            "Боевой рёв": 1, "Неудержимость": 3, "Бей сильнее!": 5, "Я покажу, как бить!": 10,
        },
        "Эмили": {
            "защита_Эмили": 1, "Вперёд, Мистер коготь!": 1, "Назад, Мистер Коготь!": 1,
            "Викторина": 1, "Гонка чисел": 1, "Цифровой щит": 1, "Блеснуть безупречностью": 1,
            "Взлом сети": 2, "Блокировка": 3, "Левый аккаунт": 4, "Заморозка репозитория": 5,
            "Трансляция взлома": 5, "Маленькая ошибка": 6, "Доксиинг": 7,
            "Взлом аккаунта": 8, "Блэк аут": 9, "Резервная копия": 9, "Игра оптики": 10,
        },
        "Ральзей": {
            "защита_Ральзей": 1, "Умиротворение": 1, "Лозы": 1, "Молитва исцеления": 1,
            "Агрессивный пузырь": 1, "Пушистый страж": 2, "Лечение?...": 2, "Рассеять!": 3,
            "Пламенная казнь": 3, "Перегной": 4, "Убеждающий вид": 4, "Приумножить заслуги": 5,
            "Унизить слабого": 6, "Песнь воскрешения": 7, "Спустить с небес": 8,
            "Концентрация зла": 9, "Тёмный горящий сад": 10,
        },
        "Сьюзи": {
            "защита_Сьюзи": 1, "Пинок ногой": 1, "Удар Секирой": 1, "Всем и сразу!": 1,
            "Хвостовой хлыст": 1, "Подручный снаряд": 2, "Кусь!": 3, "Об землю!": 4,
            "Пурпурный локоть!": 5, "Добивочная!": 6, "Смести всё!": 8,
            "Пурпурная инфузия": 1, "Зазывала": 2, "Rude Buster": 3, "Зверский рык": 5,
            "Секираранг": 7, "Rude fissure": 9,
        },
        "Ноэлль": {
            "защита_Ноэлль": 1, "Неуверенный взмах": 1, "Ледяная катана": 1, "Снежок": 3,
            "Молитва исцеления Ноэлль": 1, "Ледяной шок": 1, "Сонный туман": 2,
            "Морозная завеса": 3, "Ледяная буря": 4, "Оледенение чувств": 5,
            "Морозная корка": 6, "Ледяной кокон": 7, "Аура холодного сердца": 8,
            "Терновый сад": 9, "Цветение бед": 9, "Снежная могила": 10,
        },
        "Санс": {
            "Удар костью": 1, "Преподать урок": 3, "Подойди сюда": 5,
            "Стена костей": 1, "Костяной дождь": 1, "Прижмись": 1, "Поспать": 1,
            "Камнем вниз": 1, "Костяной щит": 2, "Бластер": 3, "Пинг-понг": 4,
            "Костяная клетка": 5, "Угрызения совести": 5, "Кара за грехи": 6,
            "Телекинез!": 8, "Финальная атака": 10,
        },
        "Бердли": {
            "защита_Бердли": 1, "Клювом!": 1, "Гениальный план": 1,
            "Электрический клюв": 3, "Вихрь знаний": 5,
        },
    }

    # Улучшения из документа дизайна: ключ способности -> записи
    # (уровень, название, описание); у одной способности может быть несколько улучшений.
    PHONE_ABILITY_UPGRADES = {
        "Крис": {
            "Призвать меч": (2, "Способности возвращаются", "Призыв меча и щита требует в два раза меньше маны."),
            "Призвать щит": (2, "Способности возвращаются", "Призыв меча и щита требует в два раза меньше маны."),
            "Напрячься": (3, "Направить фокус", "С шансом 20% магия даёт двойной бонус, но расходует вдвое больше маны."),
            "Позвать за щит": (4, "Удачные прятки", "Накладывает 1 щит на союзника."),
            "защита_Крис": (5, "Правильный угол", "При защите Крис имеет 10% шанс наложить на себя 1 щит."),
            "C разворота!": (6, "Привычка к вращению", "Перезарядка снижена на 2; дополнительный урон повышен до 150%, шанс задеть остальных врагов уроном 50%."),
            "Слабое место": (8, "Гибкое терпение", "Можно использовать после первого действия; каждое действие добавляет следующей атаке +50% урона."),
        },
        "Азриель": {
            "Шаг вперёд": (2, "2 шага вперёд", "Шаг вперёд даёт вдвое больше танка, но перезаряжается вдвое дольше."),
            "Пляшущие огоньки": (4, "Перегрев", "Получение урона от огоньков может поджечь врага и нанести остальным противникам урон от магии."),
            "Магия огня": [(3, "Пламенная инфузия", "Пламенные огоньки и обычные атаки могут вызвать дополнительный огненный урон; шанс растёт при провалах, максимум 80%."), (5, "Пиромания", "Попадания повышают шанс Пламенной инфузии и Перегрева при призыве огоньков.")],
            "Клинки хаоса": (6, "Хаос в огне", "Каждое попадание клинков хаоса может вызвать Пламенную инфузию и Перегрев."),
            "Уничтожитель хаоса": (7, "Плавящий луч", "Луч имеет шанс 25% снизить броню цели на 20%."),
            "Звёздный блеск": (9, "Осколки звёзд", "Малые звёзды имеют 30% шанс нанести другим врагам 20% урона."),
            "Звездный блеск": (9, "Осколки звёзд", "Малые звёзды имеют 30% шанс нанести другим врагам 20% урона."),
            "Пиромания": (5, "Пусть всё горит", "Пиромания и Пламенная инфузия вызывают друг друга поочерёдно, продолжая цепочку до первого провала."),
            "Пламенная инфузия": (8, "Пусть всё горит", "Пиромания и Пламенная инфузия вызывают друг друга поочерёдно, продолжая цепочку до первого провала."),
            "Столбы огня": (10, "Столбы огня", "Пламенная инфузия может вызвать ещё одну Пламенную инфузию на ту же цель."),
        },
        "Чара": {
            "Гнев": (2, "Прилив адреналина", "Гнев даёт 3 заряда Бодрости и Ярости."),
            "Удар шпагой": (3, "Сквозной рывок", "Удар шпагой может пронзить две цели в ряду."),
            "Удар ножом": (4, "Точный надрез", "Удар может наложить дополнительное кровотечение и повысить критический урон Чары."),
            "Удар из-за спины": (5, "Массаж спинки", "Есть шанс нанести 150% урона и добавить 2 кровотечения."),
            "Безумие": (7, "Расшатанная психика", "Каждая магия даёт +3 к ярости и +4% критического урона."),
            "Ножевой снаряд": (8, "Ножевой рикошет", "Ножевой снаряд может отскочить в дополнительную цель."),
            "Моральное разложение": (9, "Глубже плоти", "Урон по цели дополнительно снижает её бонусную защиту на 100."),
            "Удар из-за спины": (5, "Массаж спинки", "Есть шанс нанести 150% урона и добавить 2 кровотечения."),
            "Критический урон": (6, "Кара из тени", "Чем ниже танк Чары, тем сильнее Удар ножом и Удар из-за спины."),
            "Кровотечение": (10, "Кровавые реки", "В конце раунда враги могут получить двойной урон от кровотечения."),
        },
        "Фриск": {
            "Сила разума": (2, "Взвешенные доводы", "С шансом 50% Сила разума даёт от 5% до 10% Очарования."),
            "Potentia intellectus": (3, "Уверенность в аргументах", "Сила разума даёт Фриск +1 к Социализации."),
            "Quod licet Iovi, non licet bovi": (4, "Чувство вседозволенности", "Повышает Власть Фриск на 3 при применении заклинания."),
            "Foedus icere": (7, "Быстрая сделка", "Автоматически щадит цель и даёт Фриск +10% Очарования."),
            "Поправки в договоре": (8, "Поправки в договоре", "Снимает штрафы характеристик союзников."),
            "Что дозволено Юпитеру": (6, "Повиновение", "Что дозволено Юпитеру снижает сложность броска цели на 2."),
            "Сила разума": (5, "Коллективный разум", "Сила разума может примениться ко всем врагам с шансом, равным Очарованию Фриск."),
            "Вернуть в диалог": (10, "Увилистые формулировки", "Успешное заключение договора повышает прогресс пощады остальных врагов на 15%."),
        },
        "Кловер": {
            "Навскидку": (2, "Ловкие пальчики", "Стрельба навскидку может сделать на один выстрел больше."),
            "Лассо": (4, "Правильное перевоспитание", "После полной отсидки цель получает 2 стака Безразличия и 2 стака Слабости."),
            "Сыграем!": (4, "Ставка на удачу", "При выигрыше Кловер получает 3 заряда Удачи, при проигрыше — 4 Сглаза."),
            "Суд": (6, "Допрос с пристрастием", "Проверки Восприятия и Власти по разыскиваемой цели совершаются с преимуществом, если у неё есть преступления."),
            "Помиловать": (8, "Лучше живым, чем мёртвым", "Цель, посаженная за решётку под меткой охотника, получает 100% прогресса пощады."),
        },
        "Арчи": {
            "Боксёрское комбо": (2, "И ещё один!", "К боксёрскому комбо добавляется ещё один удар."),
            "Печати ниндзюцу": (3, "Быстрые комбинации", "Есть шанс сложить четыре печати и снять штраф к бонусной характеристике."),
            "Укрепление мышц": (4, "Твёрдые мускулы", "Арчи может наложить на себя второй щит от Укрепления мышц."),
            "Рывок": (5, "Движение жизнь!", "Рывок может полностью снять случайный дебафф."),
            "Удар орла": (6, "Далеко и надолго!", "Удар орла и Ураган выбрасывают цель на один ход дольше."),
            "Мягкая ладонь": (7, "Нежное перенаправление силы", "После Мягкой ладони случайный союзник получает 40% магии Арчи."),
            "Очищение Ци": (8, "Новые каналы энергии", "Очищение Ци и Реверс энергии изменяют на один дебафф или штраф больше."),
            "Режим храбрости": (9, "Быстрое восстановление", "Режим открывается быстрее, а заряды восстанавливаются каждые 9 секунд."),
            "Храбрость!": (10, "Ради других!", "Количество ходов действия Храбрости увеличивается до пяти."),
        },
        "Иззи": {
            "Медитация": [(2, "Открытие чакр", "Медитация даёт 2 стака Просвещения."), (3, "Потоки чакр", "Медитация с шансом 40% восстанавливает вдвое больше маны.")],
            "Успокоение": (4, "Правильное дыхание", "Успокоение союзника повышает его точность на 10%."),
            "Осколок себя": (5, "Аккуратное деление", "Есть шанс 30% не потерять HP при использовании Осколка себя."),
            "Благовония": (7, "Целебное благовоние", "Пока Благовония на перезарядке, Правильное дыхание восстанавливает Иззи 20% HP."),
            "Зачарование": (8, "Духовный диалог", "С шансом 50% восстанавливает Иззи 10% MP и повышает уровень её магии на 10%."),
        },
        "Фабри": {
            "Спрятаться": (2, "Всем прятаться!", "М-р Панцырь снижает танк Фабри на 3 при применении Спрятаться."),
            "Ускориться": (3, "Не сбавляя скорости", "Ускорение М-с Морковки даёт бонус скорости 15%, который снижается на 5% в течение 3 ходов."),
            "Неудержимость": (4, "Сорваться с цепи", "М-с Манки дополнительно даёт цели +5% бонусной атаки и +20% критического урона."),
            "Небесные танцы": (5, "Разминающие танцы", "Откатывает все атаки и магию цели на 1."),
            "Не поймаешь": (7, "Выносливее хищника", "Эффект уклонения действует на 1 ход дольше."),
            "Бей сильнее!": (8, "Я тоже бей сильнее!", "Добавляет к урону М-с Манки 20% магии Фабри."),
            "Рикошет черепахи": (9, "Закаляя панцирь", "М-р Панцырь получает +10% бонусной защиты за каждую задетую цель."),
        },
        "Эмили": {
            "Цифровой щит": (2, "Взрыв цифровой заразы", "При взрыве щита взламывает ещё одного случайного противника."),
            "Гонка чисел": (3, "Математическое унижение", "Победа в гонке накладывает на противника Печаль x2."),
            "Блеснуть безупречностью": (4, "На колени!", "Может дать врагам прогресс пощады, равный дипломатии Эмили, делённой на число оставшихся врагов."),
            "Взлом сети": (5, "Сконцентрированный хакер", "Повышает шанс критического успеха во Взломе сети на 14%."),
            "Блокировка": (7, "Тотальный бан", "Отключает дополнительно две случайные пассивные способности цели на 2 хода."),
            "Заморозка репозитория": (8, "Репозиторное лечение", "Снимает с цели дебаффы, сохраняя баффы; применяет лечение и бонусы."),
            "Взлом аккаунта": (10, "Взлом по всем фронтам", "С шансом критического успеха отвлекает цель на 2 хода вместо 1."),
        },
        "Сьюзи": {
            "Удар секирой": (2, "Внезапная инфузия", "Удар секирой может нанести дополнительный урон магией."),
            "Зазывала": (3, "Привлекая внимание", "Даёт Сьюзи +3 танка и +7% защиты; может снизить скорость врагов."),
            "Кусь!": (4, "Зубы монстра", "При попадании может наложить на цель 2 стака Страха."),
            "Подручный снаряд": (5, "Страйк!", "С шансом 30% наносит остальным противникам 30% урона."),
            "Пурпурный локоть!": (7, "Следующий!", "Добивание даёт Сьюзи Бодрость x3."),
            "Секираранг": (9, "Пурпурное накопление", "Каждое попадание Секирарангом даёт Сьюзи стак Пурпурной инфузии."),
        },
        "Ноэлль": {
            "Молитва исцеления Ноэлль": (2, "Нежная прохлада", "На союзнике с HP ниже 30% дополнительно лечит и накладывает Вдохновение x1."),
            "Ледяной шок": (3, "Леденея кровь", "Ледяной шок накладывает Мороз x2, если у цели уже есть этот дебафф."),
            "Сонный туман": (4, "Сонный дурман", "Снимает Бодрость и Гнев у врагов, а также Страх, если он есть."),
            "Морозная завеса": (5, "Аура морозной стали", "Накладывает на противников Мороз x2."),
            "Ледяная буря": (6, "Буря сгущается", "Накладывает Обморожение x2 с повышенным шансом."),
            "Оледенение чувств": (7, "Массовый холод", "Может распространиться на двух стоящих рядом противников."),
        },
        "Санс": {
            "Костяной щит": (2, "Стойкая стена", "С шансом критического удара пронзает вторую цель, нанося 70% урона."),
            "Костяной дождь": (3, "Концентрированные осадки", "Выбранная цель получает дополнительно 15% урона и 2 стака Кармы."),
            "Камнем вниз": (4, "Стук об парту", "Снижает атаку противника и накладывает Страх; может напугать остальных врагов."),
            "Преподать урок": (5, "Понятно и без слов", "Даёт прогресс пощады цели: 10% плюс половина дипломатии Санса."),
            "Прижмись": (6, "Давайте без фокусов", "Снижает бонусную магию противника на 15%."),
            "Угрызения совести": (7, "Коллективная ответственность", "Может умножить Карму остальных противников на 120%."),
            "Костяной щит (союзник)": (9, "Кармический щит", "Щит можно накладывать на союзников; при разрушении противник получает Карму x3."),
        },
        "Седрик": {
            "Сбегать за продуктами": (2, "С мыслями о рецепте", "Повышает критический шанс и критический урон Седрика."),
            "Булочка": (3, "Двойная порция", "Булочка может создать дополнительную бесплатную порцию для случайного союзника."),
            "Удар сковородкой": (4, "Хрустящая корочка", "Повышает шанс опрокинуть врага и гарантированно накладывает Слабость x1."),
            "Яичница на завтрак": (5, "Белковый заряд", "Повышает бонус атаки союзника до 7% и даёт ему +5% критического урона."),
            "Салат Цезарь": (6, "Фирменная заправка", "Дополнительно восстанавливает союзникам 15% MP."),
            "Сэндвич": (7, "Свежая нарезка", "Сильнее замедляет снаряды и снимает один случайный дебафф."),
            "Блинчики с кленовым сиропом": (8, "Сладкий сироп", "Даёт Просвещение x2 и дополнительно повышает бонусную защиту."),
            "Мясо на гриле": (9, "Королевский банкет", "С шансом критического удара Седрик приготовит мясо и себе."),
            "Пощёчина от шефа": (10, "Авторитет шефа", "Дополнительно снижает атаку врага и накладывает Истощение x2."),
        },
        "Сильвия": {
            "Пластика и выносливость": (3, "Пластика и выносливость", "Есть шанс не потратить ману при выполнении элемента танца."),
            "Не сбиваясь с Ритма": (4, "Не сбиваясь с Ритма", "Урон может не сбить текущую комбинацию."),
            "Диалог культур": (5, "Диалог культур", "Выполненное движение может повысить прогресс пощады."),
            "Вдохновение танцем": (7, "Вдохновение танцем", "Успешное уклонение восстанавливает 20% маны."),
            "Искусство для себя": (9, "Искусство для себя", "Сильвия получает собственные союзные баффы, усиленные на 30%."),
            "Громкий финал": (10, "Громкий финал", "С шансом критического удара применяет эффекты танца дважды."),
        },
        "Ральзей": {
            "Агрессивный пузырь": (2, "Упругое зеркало", "После взрыва пузырь возвращает снаряд противнику с уроном 250%."),
            "Лозы": (3, "Горючие лозы", "Лозы могут наложить дебафф Горючее."),
            "Молитва исцеления": (4, "Парное лечение", "Лечит вторую цель с самым маленьким процентом HP на 40% силы молитвы."),
            "Пламенная казнь": (5, "Массовое разбирательство", "При добивании применяется к другой цели с уроном 120%."),
            "Пушистый страж": (6, "Отпуская боль", "Следующее уклонение цели возвращает ей 25% полученного урона."),
            "Приумножить заслуги": (7, "Взаимное приумножение", "Использование способности повышает магию Ральзея на 20%."),
            "Перегной": (8, "Внутренний коллапс", "Сначала удваивает все дебаффы цели, затем добавляет к ним ещё два."),
            "Песнь воскрешения": (9, "Не требуй заботы, в бой!", "После воскрешения цель сразу получает Молитву исцеления."),
            "Концентрация зла": (10, "Королевское распределение", "Собранные дебаффы превращаются в урон врагам и лечение союзников."),
        },
    }

    PHONE_PASSIVE_CATALOG = {
        "Крис": [("VESSEL CONTROL", 1, "Возможность контролировать Криса зависит от отношений. При увороте душа сопротивляется управлению."), ("DECAYING", 1, "После каждой смерти максимальное HP Криса уменьшается на 1."), ("Двоестилие", 1, "Даёт бонус к защите или атаке до 50% от базового значения в зависимости от отношений с PLAYER."), ("Причина ошибок", 1, "Каждый ход Крис может получить дополнительный ход; шанс растёт с ходами и зависит от уровня."), ("Привыкший к общажной жизни", 1, "Вредная еда накладывает на Криса кровотечение и повышает комфорт."), ("Следы на мече", 3, "Каждый добитый Крисом противник навсегда повышает его критический урон и атаку."), ("Вмятины на щите", 7, "Получение урона со щитом повышает бонусную защиту."), ("Желание жить", 9, "Один раз за бой восстанавливает 20% HP, если здоровье Криса упало до 0.")],
        "Азриель": [("Размножение личности?", 1, "Магия зависит от обликов «Отзвуки прошлого» и «Пушистый принц»."), ("Строя оборону", 1, "Каждая защита повышает бонусную защиту на 5%."), ("Образ принца", 1, "В начале боя даёт бонусы к Социализации и Власти; провалы уменьшают их."), ("Лоб в лоб", 1, "Получение урона может повысить танк и бонусную броню."), ("Пушистик", 1, "Поддержка поднимает упавшего союзника и повышает комфорт команды."), ("Подсознательная память", 1, "Поражение команды навсегда повышает базовую магию Азриеля."), ("Стойкий", 2, "Азриеля невозможно повалить; требует 20 MP."), ("Голубая кровь", 3, "Может дважды снять с себя негативные эффекты, но кровотечение наносит больше HP-урона."), ("Рука помощи", 4, "Поднимает упавшего союзника ограниченное число раз; требует 20 MP."), ("Свита голубых кровей", 6, "Распространяет Голубую кровь на команду с уменьшенным шансом."), ("Стойкий", 8, "Невозможно повалить; при 0 HP или падении получает бонус защиты.")],
        "Чара": [("Агрессивная поддержка", 1, "Поддержка даёт союзнику заряды Бодрости; грубость снижает комфорт и повышает критический урон."), ("Хрупкая острота", 1, "Каждая атака накладывает кровотечение, но снижает бонусную атаку Чары."), ("Несчастный случай", 1, "Атаки имеют шанс удвоить кровотечение."), ("Не двигайся!", 1, "Промах повышает точность и Ярость; бонус сбрасывается при попадании."), ("Разрушитель миров", 1, "Атаки получают растущий шанс нанести большой дополнительный урон."), ("Маленькая топка", 1, "Сладости в аппетите повышают Бодрость и критический урон, но могут опустошить аппетит."), ("Попался!", 3, "Промах усиливает следующую атаку; бонус сбрасывается после попадания."), ("Прекрасные алые виды", 5, "Кровотечения врагов восстанавливают Чаре ману и повышают критический урон."), ("Аура смерти", 7, "Повышает критический урон Чары и её союзников.")],
        "Фриск": [("Legatus", 1, "Фриск не наносит физический вред; кнопка атаки изначально отсутствует."), ("Si vis pacem, para bellum", 1, "Получив урон, Фриск может совершить мощную атаку, усиливаемую недостающим HP команды."), ("Подбор стратегии переговоров", 1, "Каждый раунд повышает случайный социальный навык."), ("Разговор за бизнес-ланчем", 1, "Здоровая еда повышает Очарование, Дипломатию и случайную характеристику."), ("Уточнить позицию члена делегации", 1, "Может перехватить проваленную союзником социальную проверку."), ("Молодой, но прилежный", 1, "Каждый мирно завершённый бой повышает Очарование и Дипломатию."), ("Concordia civium murus urbium", 3, "Совместные действия команды восстанавливают HP и могут дать защиту и социальный бонус."), ("Suaviter in modo, fortiter in re", 3, "Каждое действие повышает броню Фриск."), ("Pacta sunt servanda", 4, "Пощажённые враги начинают следующий бой с повышенным прогрессом пощады."), ("Amor vincit omnia", 10, "Пощада восстанавливает части отряда 40% HP.")],
        "Кловер": [("Ковбой", 1, "Количество патронов и урон обычной атаки зависят от калибра."), ("Зоркий глаз — зоркий ум", 1, "Высокие боевые характеристики повышают соответствующие социальные навыки."), ("Делу — время, потехе — час", 1, "Если Кловер не играет, игроман заставляет его сыграть с противником."), ("Расследование дела", 1, "Действия и урон заполняют шкалу виновности; преступления приводят к суду и тюремному сроку."), ("Поправка на ветер", 1, "Максимальное исполнение атаки повышено; постоянный бонус зависит от уровня."), ("Всем в салуне за мой счёт!", 1, "Напитки дают боевые бонусы команде, но Кловер теряет точность и падает."), ("Инструктор по бою", 2, "Каждый выстрел повышает точность случайного союзника."), ("Проценты с казино", 3, "Команда делит часть выигрыша и проигрыша Кловера в играх."), ("Перестрелка в полдень", 5, "При атаке противника Кловер отвечает выстрелом, расходуя патроны."), ("Рикошет", 7, "Выстрел может отскочить к дополнительным случайным противникам."), ("Внезапная заначка", 9, "При окончании патронов Кловер может восстановить половину обоймы."), ("Смертельная удача", 10, "Получая Удачу, Кловер получает её вдвое больше.")],
        "Арчи": [("Удар! Удар!", 1, "Критический шанс Арчи может дать ему дополнительный ход."), ("Не медля!", 1, "Арчи всегда ходит первым."), ("Уворот! Контрудар!", 1, "Арчи попеременно уворачивается и контратакует при получении урона."), ("Вперёд! Вперёд!", 1, "Поддержка союзника даёт ему боевые бонусы и комфорт."), ("Не считайте до десяти!", 1, "После падения Арчи может подняться с 10% HP."), ("Правильное дыхание.", 2, "Арчи каждый ход восстанавливает HP и ману."), ("Эй! Я здесь!", 4, "Удары могут повышать танк Арчи."), ("Боевое зеркало", 6, "Может отражать наложенные на него снарядами дебаффы."), ("Запаха достаточно!", 8, "Арчи может получить часть эффекта расходника союзника."), ("Прости, но это мне!", 10, "Может забрать половину полученного союзником баффа себе.")],
        "Иззи": [("Равновесие", 1, "Магия с шансом 45% не отнимает у Иззи HP."), ("Посвящённая", 1, "Иззи всегда на один уровень выше команды."), ("Я тоже...", 1, "Заклинания отнимают HP, но не могут опустить его ниже 1."), ("Таинство вместо мечей", 1, "Иззи не может атаковать, но имеет базовые заклинания."), ("Адаптация к диете", 1, "Пустые места очереди аппетита восстанавливают HP и MP."), ("Подозрительная проницательность", 1, "Осмотр раскрывает эффекты четырёх действий и повышает социальные характеристики для полезных действий."), ("Подавление инородной ауры", 3, "Магия Иззи по врагу снижает его магию."), ("Успокоение близкого", 5, "Каждый ход повышает шанс, что Крис подчинится."), ("Случайное провиденье", 7, "Может получать Просвещение x2 каждый ход."), ("Магия сверху", 9, "Может применить магию дважды.")],
        "Седрик": [("Продукты для рецептов", 1, "Вместо маны Седрик расходует четыре вида ингредиентов; запасы растут каждые два уровня."), ("Перфекционизм или ничего!", 1, "Блюдо, не прошедшее проверку точности, выбрасывается."), ("Разогрев сковороды", 1, "Приготовление блюда повышает силу следующего удара сковородкой."), ("Уточнение рецептуры", 1, "Приготовление блюда для себя повышает точность следующей готовки этого блюда."), ("Массовая готовка", 1, "Каждые три уровня позволяет приготовить за ход на одно блюдо больше."), ("Долг перед голодными", 3, "Пустые ячейки аппетита команды повышают точность Седрика."), ("Выше кулинарного искусства", 5, "Блюда могут критически усилиться на основе характеристик Седрика."), ("Сытный дух", 7, "Заполненный аппетит даёт персонажу Бодрость x2."), ("Экономия продуктов", 9, "При приготовлении есть шанс не потратить ингредиенты.")],
        "Сильвия": [("Раскрываясь в свете прожекторов", 1, "Движения повышают танк Сильвии; каждый удар сбрасывает этот бонус."), ("Антракт", 1, "При исчерпании маны Сильвия пропускает ходы, восстанавливая запас."), ("Важность исполнения", 1, "Точность и критический шанс определяют силу эффекта танцевальных движений."), ("Репертуар", 1, "Танцы расходуют 10% максимальной маны; урон сбивает комбинацию, один танец можно исполнить раз за бой."), ("Ловкость в бою", 1, "Получение урона может дать шанс полностью увернуться от снаряда."), ("Своя очередь", 1, "Первый или последний ход в раунде даёт Сильвии защиту или критический шанс."), ("Пластика требует диеты", 1, "Здоровая еда может дать дополнительный ход; пустые ячейки аппетита лечат HP."), ("Диалог культур", 5, "Выполненное движение может повысить прогресс пощады врагов."), ("Вдохновение танцем", 7, "Успешное уклонение восстанавливает ману."), ("Искусство для себя", 9, "Сильвия получает собственные баффы, которые раздаёт союзникам, усиленными на 30%."), ("Громкий финал", 10, "Может применить эффекты танца дважды.")],
        "Фабри": [("Созидатель, а не разрушитель", 1, "У Фабри нет активных атак; она призывает и поддерживает фамильяров."), ("Рукодельные друзья", 1, "Фабри может призвать до двух фамильяров; они делят с ней урон и лечение."), ("Передышка, чтоб вернуться", 1, "После получения урона душа Фабри возвращается дольше в зависимости от уровня."), ("Разнообразие — лучшее вдохновение", 1, "Разная еда повышает бонусную магию и критический шанс."), ("Энтузиазм и усердие", 3, "Фабри может не потратить ману при создании фамильяра."), ("Сотворить наспех", 5, "Позволяет создать сразу двух фамильяров."), ("Творчество будет жить...", 7, "Критический шанс даёт Фабри дополнительный урон и защищает фамильяров от смертельного урона."), ("Радующее творчество", 9, "Создание фамильяров даёт союзникам Вдохновение x3.")],
        "Эмили": [("Поиск уязвимостей", 1, "Успешные действия и магия дают прогресс взлома и снижают бонусную защиту врага."), ("Авторитет с мозгами", 1, "Успехи дают Репутацию, повышающую Социализацию; неудачи снимают заряды."), ("Быстрая энергия", 1, "Сладости, вредная еда и жидкости повышают разные боевые и социальные характеристики."), ("Усиление взлома системы", 1, "Находясь в команде, Эмили постепенно повышает шанс Криса на дополнительный ход."), ("Ответить в Интернете", 1, "Потеря Репутации повышает критический шанс Эмили."), ("Накопление знаний", 2, "Успешные действия команды повышают максимальную ману Эмили."), ("Анализ ошибок", 5, "Ошибка союзника повышает требуемую социальную характеристику до смены настроения врага."), ("Второе я", 7, "Действия и магия накапливают прогресс цифрового клона, который принимает следующую атаку."), ("Бит за битом. Байт за байтом.", 9, "Успешная магия снижает защиту цели и может снизить её дополнительно.")],
        "Ральзей": [("Облегчающие переговоры", 1, "Пощада врага лечит союзника на основе магии Ральзея; его собственная пощада лечит сильнее."), ("Энергия вещей", 1, "Ральзей может применить предмет дважды."), ("Чистые руки", 1, "Ральзей не использует атаки."), ("Убедительные аргументы", 1, "Применение магии снижает сложности некоторых социальных взаимодействий."), ("Переговоры за королевским столом", 1, "Кормление Ральзея повышает две его социальные характеристики."), ("Отрицание милоты", 3, "Срабатывание Очарования повышает критические характеристики и Власть Ральзея."), ("Кончая с формальностями", 5, "Смена настроения противника может вызвать дополнительное действие Ральзея."), ("Принятие доброты", 7, "Лечение цели также частично лечит Ральзея."), ("Подчинись моей воле", 9, "Очарование продвигает пощаду сильнее благодаря Дипломатии Ральзея.")],
        "Сьюзи": [("Ну сколько можно?!!", 1, "Выбор другого персонажа повышает бонусную атаку Сьюзи до конца раунда."), ("Жди ответку!", 1, "Получение урона даёт Гнев и может дать Бодрость."), ("Вопросы?..", 1, "Получение урона может наложить Страх на атакующего."), ("Большая печка", 1, "Сброс аппетита Сьюзи срабатывает дважды за ход."), ("Собиратель бед", 1, "Защита, получение урона и атаки восстанавливают Сьюзи ману."), ("А по-другому не получится", 1, "Использование атак и магии повышает соответствующие бонусные характеристики."), ("Прости, что не сразу", 3, "Урон по цели повышается в зависимости от недостающего у неё HP."), ("Диноустойчивость", 5, "Дебаффы Сьюзи снимаются дважды, баффы — один раз."), ("Отражающая чешуя", 7, "Сьюзи может отразить дебафф обратно во врага."), ("Слабаки!", 9, "Падение союзника даёт Сьюзи Бодрость x4.")],
        "Ноэлль": [("Хрупкое сердце", 1, "Получение урона может наложить Страх, но снижает стоимость следующей магии."), ("Ледяная могила", 1, "Атакующая магия накладывает Мороз; накопление пяти стаков замораживает врага."), ("Снежный заклинатель", 1, "При запасе маны выше 60% может наложить два стака Обморожения."), ("Защитный рефлекс", 1, "Защищаясь, восстанавливает ману и повышает критический шанс."), ("Сладкоежка", 1, "Сладости и салаты снимают страх и восстанавливают HP."), ("Становясь сильнее...", 2, "Убийство или заморозка врага навсегда повышают магию и критический шанс."), ("Треснутая от льда броня", 4, "Обмороженные противники теряют защиту за каждый стак."), ("Робкая забота", 6, "Лечение ослабленного союзника может снять дебафф и передать ему ману.")],
        "Санс": [("Я думал, мы со своим...", 1, "Санс использует d30 вместо d20 для проверок характеристик."), ("Альтернативное HP", 1, "У Санса 1 HP и четыре гарантированных уклонения, восстанавливаемых сном."), ("Карма", 1, "Магия накапливает Карму; стаки наносят урон, но не могут убить врага."), ("Профессорские навыки", 1, "Осмотр имеет преимущество, а поддержка снимает больше дебаффов."), ("Объяснение препода", 1, "После успешного действия Санс может снизить сложность проверки союзникам."), ("Ответственность старшего", 1, "Принимает на себя смертельный удар, предназначенный союзнику."), ("Очаровательный сеньор", 3, "Очарование сильнее продвигает пощаду."), ("Груз ответственности на плечах", 5, "Атаки противника накапливают ему стаки Кармы."), ("Решить за чашкой чая", 7, "Угощение противника снижает сложности социальных проверок Санса."), ("Обучение очарованию", 9, "Успешное Очарование при первом ходе повышает его бонус у команды.")],
        "Бердли": [("Самоуверенный стратег", 1, "Бердли сочетает физические и магические атаки, усиливая себя и ослабляя противников.")],
    }

    def phone_character_attack_items(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        char = phone_get_character_object(char_name)
        items = phone_extract_named_items(char, ["attacks", "attack_list", "attack_items", "acts", "skills"])
        if items:
            registry = globals().get("ABILITY_DESCRIPTIONS", {}) or {}
            return _phone_append_upgrades(char_name, [_phone_ability_card(name, dict(registry.get(name, {}), description=desc), char_name, "attacks") for name, desc in items])
        definitions = getattr(store, "BATTLE_ABILITY_DEFINITIONS", []) or []
        registry = globals().get("ABILITY_DESCRIPTIONS", {}) or {}
        registered = [a for a in definitions if a.get("owner") == char_name and a.get("menu") == "attack"]
        if registered:
            items = [_phone_ability_card(a.get("name"), dict(a, **registry.get(a.get("name"), {})), char_name, "attacks") for a in registered]
            return _phone_append_upgrades(char_name, items)
        return _phone_append_upgrades(char_name, [_phone_ability_card("Обычная атака", {"description": "Базовая атака персонажа."}, char_name, "attacks")])

    def _phone_append_upgrades(char_name, items):
        upgrades = PHONE_ABILITY_UPGRADES.get(char_name, {})
        expanded = []
        for item in items:
            expanded.append(item)
            upgrade_entries = upgrades.get(item["name"], [])
            if upgrade_entries and not isinstance(upgrade_entries, list):
                upgrade_entries = [upgrade_entries]
            for unlock_level, upgrade_name, upgrade_desc in upgrade_entries:
                expanded.append({"name": upgrade_name, "description": upgrade_desc,
                                 "level": "", "resource": "", "upgrade": "",
                                 "category": "upgrade", "owner": char_name,
                                 "is_upgrade": True, "unlock_level": unlock_level})
        return expanded

    def phone_unlocked_ability_items(items, char_name=None):
        """Only return abilities and upgrades available at the character level."""
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        char = phone_get_character_object(char_name)
        try:
            current_level = int(getattr(char, "level", 1)) if char is not None else 1
        except Exception:
            current_level = 1
        result = []
        for item in items or []:
            if not isinstance(item, dict):
                result.append(item)
                continue
            required_level = item.get("unlock_level", item.get("level", 1))
            try:
                required_level = int(required_level or 1)
            except Exception:
                required_level = 1
            if required_level <= current_level:
                result.append(item)
        return result

    def phone_character_magic_items(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        names = list((globals().get("CHARACTER_MAGIC_ABILITIES", {}) or {}).get(char_name, ()))
        registered = [a for a in (getattr(store, "BATTLE_ABILITY_DEFINITIONS", []) or [])
                      if a.get("owner") == char_name and a.get("menu") == "magic"]
        if registered:
            names = [a.get("name") for a in registered]
        registry = globals().get("ABILITY_DESCRIPTIONS", {}) or {}
        if names:
            cards = []
            definitions = {a.get("name"): a for a in registered}
            for name in names:
                data = dict(registry.get(name, {}))
                if name in definitions:
                    data.update(definitions[name])
                cards.append(_phone_ability_card(name, data, char_name, "magic"))
            return _phone_append_upgrades(char_name, cards)
        char = phone_get_character_object(char_name)
        items = phone_extract_named_items(char, ["magic_list", "spells", "magic_skills", "magic_items"])
        return [_phone_ability_card(name, {"description": desc}, char_name, "magic") for name, desc in items]

    def phone_character_passive_items(char_name=None):
        char_name = char_name or getattr(store, "phone_selected_character", "Крис")
        char = phone_get_character_object(char_name)
        items = phone_extract_named_items(char, ["passives", "passive_list", "traits", "perks"])
        if items:
            registry = globals().get("ABILITY_DESCRIPTIONS", {}) or {}
            return [_phone_ability_card(name, dict(registry.get(name, {}), description=desc), char_name, "passive") for name, desc in items]
        levels = PHONE_ABILITY_LEVELS.get(char_name, {})
        return [{"name": name, "description": desc, "level": levels.get(name, level), "resource": "",
                 "upgrade": "", "category": "passive", "owner": char_name}
                for name, level, desc in PHONE_PASSIVE_CATALOG.get(char_name, [])]

    def phone_character_summary(char_name):
        stats = phone_character_main_stats(char_name)
        return "\n".join(["%s: %s" % (name, value) for name, value in stats])

    # ---------- чат ----------
    # Настройки прокрутки списка контактов внутри телефона.
    PHONE_CONTACT_ROW_HEIGHT = 66
    PHONE_CONTACT_ROW_SPACING = 8
    PHONE_CONTACT_VIEWPORT_HEIGHT = 455

    PHONE_CONTACTS = {
        "alphys": {
            "name": "Альфис",
            "topics": ["sport", "tea", "present"],
        },
        "susie": {
            "name": "Сьюзи",
            "topics": ["susie_training", "susie_walk"],
        },
        "noelle": {
            "name": "Ноэль",
            "topics": ["noelle_study", "noelle_library"],
        },
    }

    PHONE_TOPIC_DATA = {
        "sport": {
            "title": "заняться спортом",
            "incoming": "Пойдём заниматься спортом?",
            "ignored": "Ладно, забей на спорт.",
            "player_start": "Пойдём заниматься спортом?",
            "npc_after_player_start": "Да, давай. Только не опаздывай.",
            "answers": [
                (1, "Да, пошли", "Отлично, встречаемся у зала."),
                (2, "Не сейчас", "Окей, тогда позже."),
                (3, "Я подумаю", "Хорошо, но не тяни."),
            ],
        },
        "tea": {
            "title": "попить чай",
            "incoming": "Попьём чай после пар?",
            "ignored": "Ладно, забей на чай.",
            "player_start": "Может, попьём чай?",
            "npc_after_player_start": "Хорошая идея. Я как раз свободна.",
            "answers": [
                (1, "Да", "Тогда я займу столик."),
                (2, "Нет", "Поняла."),
                (3, "Позже", "Хорошо, напомню позже."),
            ],
        },
        "present": {
            "title": "купить подарок",
            "incoming": "Нужно купить подарок. Поможешь?",
            "ignored": "Ладно, со старой темой всё ясно.",
            "player_start": "Давай купим подарок.",
            "npc_after_player_start": "Да! Я уже думала об этом.",
            "answers": [
                (1, "Помогу", "Спасибо! Тогда идём вместе."),
                (2, "Не могу", "Жаль, но я справлюсь."),
                (3, "А кому?", "Расскажу при встрече."),
            ],
        },
        "susie_training": {
            "title": "тренировка",
            "incoming": "Эй, пойдём тренироваться?",
            "ignored": "Ладно, без тренировки.",
            "player_start": "Пойдём тренироваться?",
            "npc_after_player_start": "Ха, наконец-то нормальная идея.",
            "answers": [
                (1, "Идём", "Вот это настрой."),
                (2, "Позже", "Не тяни."),
                (3, "Я пас", "Слабак."),
            ],
        },
        "susie_walk": {
            "title": "прогулка",
            "incoming": "Пойдём проветримся?",
            "ignored": "Ладно, забудь.",
            "player_start": "Может, прогуляемся?",
            "npc_after_player_start": "Ну... можно.",
            "answers": [
                (1, "Да", "Тогда шевелись."),
                (2, "Не могу", "Пф, ясно."),
                (3, "Куда?", "По дороге решим."),
            ],
        },
        "noelle_study": {
            "title": "учёба",
            "incoming": "Поможешь мне с учёбой?",
            "ignored": "Ничего, я попробую сама.",
            "player_start": "Давай позанимаемся?",
            "npc_after_player_start": "Да, спасибо! Мне это правда поможет.",
            "answers": [
                (1, "Конечно", "Спасибо, я подготовлю тетради."),
                (2, "Позже", "Хорошо, я подожду."),
                (3, "Что именно?", "Покажу при встрече."),
            ],
        },
        "noelle_library": {
            "title": "библиотека",
            "incoming": "Сходим в библиотеку?",
            "ignored": "Ладно, тогда в другой раз.",
            "player_start": "Пойдём в библиотеку?",
            "npc_after_player_start": "Да! Я как раз хотела туда зайти.",
            "answers": [
                (1, "Пойдём", "Отлично, встретимся у входа."),
                (2, "Не сейчас", "Поняла."),
                (3, "Зачем?", "Мне нужно найти одну книгу."),
            ],
        },
    }

    def phone_contact_name(contact_id):
        return PHONE_CONTACTS.get(contact_id, {}).get("name", contact_id or "")

    def phone_contact_flag_name(contact_id):
        return "%s_get_contacted" % contact_id

    def phone_contact_is_available(contact_id):
        # Контакт доступен только если существует/задан флаг: <id>_get_contacted == 1.
        # Пример: alphys_get_contacted, susie_get_contacted, noelle_get_contacted.
        return int(getattr(store, phone_contact_flag_name(contact_id), 0)) == 1

    def phone_available_contacts():
        return [(cid, cdata) for cid, cdata in PHONE_CONTACTS.items() if phone_contact_is_available(cid)]

    def phone_contact_count_for_scroll():
        return len(phone_available_contacts())

    def phone_should_show_contact_vbar():
        count = phone_contact_count_for_scroll()
        if count <= 0:
            return False
        content_h = count * PHONE_CONTACT_ROW_HEIGHT + max(0, count - 1) * PHONE_CONTACT_ROW_SPACING
        return content_h > PHONE_CONTACT_VIEWPORT_HEIGHT

    def phone_contact_topics(contact_id=None):
        contact_id = contact_id or getattr(store, "phone_selected_contact", None)
        if not phone_contact_is_available(contact_id):
            return []
        return PHONE_CONTACTS.get(contact_id, {}).get("topics", [])

    def phone_open_chat(contact_id):
        if not phone_contact_is_available(contact_id):
            renpy.notify("Контакт ещё не получен.")
            return
        store.phone_selected_contact = contact_id
        store.phone_chat_open = True
        store.phone_panel = "contacts"
        phone_refresh_chat_queue(contact_id)
        _phone_safe_restart()

    def phone_close_chat():
        store.phone_chat_open = False
        _phone_safe_restart()

    def phone_add_chat_message(contact_id, who, text, event_id=None):
        if not hasattr(store, "phone_chat_messages") or store.phone_chat_messages is None:
            store.phone_chat_messages = {}
        for cid in PHONE_CONTACTS.keys():
            if cid not in store.phone_chat_messages:
                store.phone_chat_messages[cid] = []
        if contact_id not in store.phone_chat_messages:
            store.phone_chat_messages[contact_id] = []
        if event_id is not None:
            if event_id in store.phone_chat_seen_events:
                return
            store.phone_chat_seen_events.append(event_id)
        store.phone_chat_messages[contact_id].append({"who": who, "text": text})

    def phone_close_waiting_topics_before(contact_id, new_topic_key):
        contact = PHONE_CONTACTS.get(contact_id, {})
        topics = contact.get("topics", [])
        for topic_key in topics:
            if topic_key == new_topic_key:
                break
            state = _phone_get_list_var(topic_key)
            if len(state) >= 2 and state[0] == 1 and state[1] is None:
                state[1] = 0
                setattr(store, topic_key, state)
                phone_add_chat_message(contact_id, "npc", PHONE_TOPIC_DATA[topic_key]["ignored"], "%s:%s:ignored" % (contact_id, topic_key))

    def phone_refresh_chat_queue(contact_id=None):
        contact_id = contact_id or getattr(store, "phone_selected_contact", None)
        if not phone_contact_is_available(contact_id):
            return
        contact = PHONE_CONTACTS.get(contact_id, {})
        for topic_key in contact.get("topics", []):
            state = _phone_get_list_var(topic_key)
            if len(state) == 0:
                continue
            if state[0] != 1:
                continue

            # [1] превращаем в [1, None]: событие случилось, NPC написал, ждёт ответа.
            if len(state) == 1:
                phone_close_waiting_topics_before(contact_id, topic_key)
                state.append(None)
                setattr(store, topic_key, state)
                phone_add_chat_message(contact_id, "npc", PHONE_TOPIC_DATA[topic_key]["incoming"], "%s:%s:incoming" % (contact_id, topic_key))
                continue

            # [1, None] уже ждёт ответа, ничего не добавляем.
            # [1, 0/1/2/3] уже закрыто/отвечено.

    def phone_select_contact(contact_id):
        # Старое имя функции оставлено как алиас. Теперь оно открывает конкретный чат.
        phone_open_chat(contact_id)

    def phone_get_waiting_topic(contact_id):
        contact = PHONE_CONTACTS.get(contact_id, {})
        for topic_key in contact.get("topics", []):
            state = _phone_get_list_var(topic_key)
            if len(state) >= 2 and state[0] == 1 and state[1] is None:
                return topic_key
        return None

    def phone_answer_topic(contact_id, topic_key, answer_id):
        state = _phone_get_list_var(topic_key)
        if not (len(state) >= 2 and state[0] == 1 and state[1] is None):
            return
        answer_text = None
        reaction_text = None
        for aid, player_text, npc_text in PHONE_TOPIC_DATA[topic_key]["answers"]:
            if aid == answer_id:
                answer_text = player_text
                reaction_text = npc_text
                break
        if answer_text is None:
            return
        state[1] = answer_id
        setattr(store, topic_key, state)
        phone_add_chat_message(contact_id, "player", answer_text, "%s:%s:answer:%s:player" % (contact_id, topic_key, answer_id))
        phone_add_chat_message(contact_id, "npc", reaction_text, "%s:%s:answer:%s:npc" % (contact_id, topic_key, answer_id))
        _phone_safe_restart()

    def phone_can_player_start_topic(topic_key):
        # Писать первыми можно только если сюжетный флаг can_write_* == 1 и тема ещё не начата.
        if int(getattr(store, "can_write_" + topic_key, 0)) != 1:
            return False
        state = _phone_get_list_var(topic_key)
        return len(state) == 0

    def phone_player_start_topic(contact_id, topic_key):
        if not phone_can_player_start_topic(topic_key):
            return
        setattr(store, topic_key, [2, 1])
        phone_add_chat_message(contact_id, "player", PHONE_TOPIC_DATA[topic_key]["player_start"], "%s:%s:player_start:player" % (contact_id, topic_key))
        phone_add_chat_message(contact_id, "npc", PHONE_TOPIC_DATA[topic_key]["npc_after_player_start"], "%s:%s:player_start:npc" % (contact_id, topic_key))
        _phone_safe_restart()

    def phone_get_player_start_topics(contact_id):
        contact = PHONE_CONTACTS.get(contact_id, {})
        return [topic_key for topic_key in contact.get("topics", []) if phone_can_player_start_topic(topic_key)]

    def phone_dev_trigger_topic(topic_key):
        # Инструмент разработчика: имитирует, что событие уже случилось.
        state = _phone_get_list_var(topic_key)
        if len(state) == 0:
            setattr(store, topic_key, [1])
        elif state[0] != 1:
            state[0] = 1
            setattr(store, topic_key, state)
        phone_refresh_chat_queue(getattr(store, "phone_selected_contact", None))
        _phone_safe_restart()

    def phone_dev_reset_chats():
        for topic_key in PHONE_TOPIC_DATA.keys():
            setattr(store, topic_key, [])
        store.phone_chat_messages = {}
        for cid in PHONE_CONTACTS.keys():
            store.phone_chat_messages[cid] = []
        store.phone_chat_seen_events = []
        store.phone_chat_open = False
        _phone_safe_restart()


# ============================================================
# PATCH: ГОЛУБЫЕ КОМНАТЫ/ЭТАЖИ В ЦЕНТРЕ ОТКЛЮЧЕНЫ
# Комнаты остаются только логическими room id.
# Жёлтый маркер задания и коричневый маркер игрока стоят свободно по x/y.
# ============================================================
init python:
    PHONE_ROOM_UI_LAYOUTS = {}

    def phone_get_sublocation_room_objects(sublocation_key=None):
        return []

# ------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ СТИЛИ/ПЛЕЙСХОЛДЕРЫ
# ------------------------------------------------------------
style phone_text:
    size 22
    color "#ffffff"

style phone_tiny:
    size 16
    color "#ffffff"

style phone_button_text:
    size 22
    color "#b000ff"
    hover_color "#ffffff"

style phone_button:
    background Solid("#38df26")
    hover_background Solid("#50ff40")
    insensitive_background Solid("#555555")
    padding (8, 6)

style phone_black_button:
    background Solid("#000000")
    hover_background Solid("#222222")
    insensitive_background Solid("#333333")
    padding (8, 6)

style phone_black_button_text:
    size 26
    color "#ffffff"
    hover_color "#ffff00"


# ------------------------------------------------------------
# ГЛАВНЫЙ ЭКРАН ТЕЛЕФОНА
# ------------------------------------------------------------
screen complex_phone():
    modal True
    zorder 200
    
    key "K_ESCAPE" action [Function(phone_info_reset), SetVariable("control_Kris", 1), Hide("complex_phone")]
    key "K_p" action [Function(phone_info_reset), Hide("complex_phone")]
    
    add Solid("#00000066")
    add "Vsechat_template.png"
    fixed:
        xysize (1280, 720)

        # Левая зона зависит от открытого приложения.
        if phone_panel == "journal":
            use phone_journal_left_panel
        elif phone_panel == "contacts":
            use phone_contacts_left_panel
        elif phone_panel == "info":
            use phone_info_left_panel
        elif phone_panel == "party":
            use phone_party_left_panel
        else:
            text "Телефон" xpos 70 ypos 60 size 42 color "#ffffff"
            text "Нажми приложение на телефоне справа.\nEsc / P — закрыть телефон." xpos 70 ypos 120 size 26 color "#ffffff"

        # Сам телефон справа всегда виден, кроме перехода в менеджер команды.
        use phone_body

default phone_time = "9:32"
default wifi = "good"
default phonepercent = 100

screen phone_body():
    
    frame:
        xpos 913
        ypos 64
        xsize 305
        ysize 610
        background None#Solid("#08060f")
        #padding (14, 22)

        frame:
            xfill True
            yfill True
            background "standart.jpg" #Solid("#ad9bb4")
            padding (10, 12)

            if phone_panel == "home":
                use phone_home_apps
            elif phone_panel == "journal":
                use phone_journal_phone_side
            elif phone_panel == "contacts":
                use phone_contacts_phone_side
            elif phone_panel == "info":
                use phone_info_phone_side
            elif phone_panel == "party":
                use phone_party_phone_side
    frame:
        xsize 305
        ysize 30
        xpos 915
        ypos 60
        background "#000000"
        hbox:

            spacing 40

            text "[phone_time]" size 15 yoffset 3 xoffset 10 color "#b8b8b8"

            add "camera.png" zoom 0.61 xoffset 60 

            if wifi == "good":
                add "good_connect.png" zoom 2 yoffset 3 xoffset 70
            if wifi == "mid":
                add "mid_connect.png" zoom 2 yoffset 3 xoffset 70
            if wifi == "bad":
                add "no_connect.png" zoom 2 yoffset 3 xoffset 70
            
            text "[phonepercent]%" size 15 yoffset 3 xalign 0.5 xoffset 35  color "#b8b8b8"


    # нижние кнопки телефона-плейсхолдеры
    frame:
        xsize 305
        ysize 60
        xpos 915
        ypos 620
        background "#000000"

    hbox:
        xpos 965
        ypos 630
        spacing 55
        textbutton "{size=28}{color=#ffffff}≡{/color}":
            action Function(phone_go_home)
        textbutton "{size=28}{color=#ffffff}⌂{/color}":
            action Function(phone_close_phone)
        if phone_panel == "home":
            textbutton "{size=28}{color=#ffffff}↩{/color}" action [SetVariable("control_Kris", 1), Hide("complex_phone")]
        elif phone_panel == "info" and phone_info_section is not None:
            textbutton "{size=28}{color=#ffffff}↩{/color}" action Function(phone_info_back)
        else:
            textbutton "{size=28}{color=#ffffff}↩{/color}" action SetVariable("phone_panel", "home")

transform icon_phone:
    xanchor 0.5 yanchor 0.5 xpos 40 ypos 45
    on idle:
        linear 0.1 zoom 1.0 
    on hover:
        linear 0.1 zoom 0.9


screen phone_home_apps():
    vbox:
        spacing 16
        xalign 0.5
        yalign 0.1

        grid 3 4:
            yoffset 10
            spacing 14

            button:
                at icon_phone
                background "journal.png"
                text "Журнал" size 15 yalign 1.0 xalign 0.5 yoffset 10
                style "phone_button"
                #text_style "phone_button_text"
                xsize 74
                ysize 90
                action Function(phone_set_panel, "journal")
            button:
                at icon_phone
                background "messages.png"
                text "Контакты" size 15 yalign 1.0 xalign 0.5 yoffset 10
                style "phone_button"
                xsize 74
                ysize 90
                action Function(phone_set_panel, "contacts")
            button:
                at icon_phone
                background "info.png"
                text "Инфо" size 15 yalign 1.0 xalign 0.5 yoffset 10
                style "phone_button"
                xsize 74
                ysize 90
                action Function(phone_set_panel, "info")

            #textbutton "Персы":
            #    style "phone_button"
            #    text_style "phone_button_text"
            #    xsize 74
            #    ysize 90
            #    action [SetVariable("phone_info_section", "characters"), Function(phone_set_panel, "party")]
            
            button:
                at icon_phone
                background "team.png"
                text "Команда" size 15 yalign 1.0 xalign 0.5 yoffset 10
                style "phone_button"
                xsize 74
                ysize 90
                action [Hide("complex_phone"), 
                        Function (phone_try_ensure_team_manager),
                        Hide ("complex_phone"),
                        Show ("phone_team_fallback_manager")
                ]
                #Call("phone_open_team_manager")]

            
            null width 74 height 62
            null width 74 height 62

            null width 74 height 62
            null width 74 height 62
            null width 74 height 62
            null width 74 height 62
            null width 74 height 62
            null width 74 height 62




# ------------------------------------------------------------
# ТРАНСФОРМЫ МАРКЕРОВ КАРТЫ
# ------------------------------------------------------------
transform phone_bottom_tab_quest_marker:
    # Маркер задания на нижней вкладке локации.
    # Положение задаётся трансформом, а не xpos/ypos в add.
    xpos 45
    ypos -12
    alpha 1.0
    ease 0.35 yoffset -3
    ease 0.35 yoffset 0
    repeat

transform phone_sublocation_select_marker:
    # Небольшой маркер выбранного этажа/подлокации.
    xpos 10
    ypos 8
    alpha 1.0

transform phone_room_button_quest_marker:
    # Жёлтый квадрат на кнопке комнаты/этажа.
    # Координаты задаются через xpos/ypos в add, трансформ только моргание.
    alpha 1.0
    ease 0.35 alpha 0.45
    ease 0.35 alpha 1.0
    repeat

transform phone_room_match_marker:
    # Большой индикатор совпадения текущей комнаты игрока с комнатой цели.
    alpha 1.0
    ease 0.35 alpha 0.45
    ease 0.35 alpha 1.0
    repeat

transform phone_map_quest_pulse:
    # Сам жёлтый квадратик цели внутри карты задаётся координатами qtarget["x"], qtarget["y"].
    alpha 1.0
    ease 0.45 alpha 0.45
    ease 0.45 alpha 1.0
    repeat

# ------------------------------------------------------------
# ЖУРНАЛ / КАРТА
# ------------------------------------------------------------
screen phone_journal_left_panel():
    fixed:
        xpos 5
        ypos 35
        xysize (870, 650)

        # --------------------------------------------------------
        # ЛЕВАЯ ПАНЕЛЬ: список заданий
        # --------------------------------------------------------
        frame:
            xpos 0
            ypos 0
            xsize 225
            ysize 615
            background Solid("#ffffff")
            padding (10, 10)

            frame:
                xalign 0.5
                xsize 215
                ysize 605
                yalign 0.5
                background Solid("#000000")


                vbox:
                    spacing 8
                    text "Задания" size 34 color "#ffffff" xalign 0.5
                    add Solid("#ffffff", xysize=(205, 3))

                    viewport id "phone_quest_viewport":
                        xsize 210
                        ysize PHONE_QUEST_VIEWPORT_HEIGHT
                        mousewheel True 
                        draggable True

                        vbox:
                            spacing 8
                            

                            for qid, quest in PHONE_QUESTS.items():
                                $ prog = phone_get_quest_progress(qid)

                                # В скролл и vbar попадают только взятые задания: progress 1+.
                                if prog > 0:
                                    $ is_selected = phone_selected_quest == qid
                                    $ quest_text_color = "#ffff00" if is_selected else "#ffffff"

                                    button:
                                        
                                        style "phone_black_button"
                                        xfill True
                                        ysize PHONE_QUEST_ROW_HEIGHT
                                        selected is_selected
                                        #hovered Show("quest_desc")
                                        #unhovered Hide("quest_desc")
                                        #action Function(phone_select_quest, qid)
                                        action Function(handle_quest_click, qid)

                                        hbox:
                                            spacing 6
                                            yalign 0.5

                                            if is_selected:
                                                add "orientir.png" xysize (15, 15) yalign 0.5
                                            else:
                                                null width 18 height 18

                                            text "[quest['name']]":
                                                size 20
                                                xmaximum 165
                                                layout "subtitle"
                                                color quest_text_color
                                                hover_color "#ffff00"
                                                selected_color "#ffff00"
                                                yalign 0.5

        # Отдельный scrollbar списка заданий — стоит между списком и картой.
        # Появляется только когда активные задания не помещаются во viewport.
        if phone_should_show_quest_vbar():
            vbar value YScrollValue("phone_quest_viewport"):
                xpos 230
                ypos 60
                xsize 20
                ysize 550
                base_bar Solid("#222222")
                thumb Solid("#ffffff")

        # --------------------------------------------------------
        # ЦЕНТР: карта выбранной подлокации/корпуса
        # --------------------------------------------------------
        frame:
            xpos 255
            ypos 0
            xsize 590
            ysize 610
            background Solid("#ffffff")
            padding (10, 10)

            frame:
                xalign 0.5
                yalign 0.5
            
                xsize 580
                ysize 600
                background Solid("#000000")
                padding (10, 10)

                fixed:
                    xysize (566, 590)

                    text "[phone_get_location_name()]":
                        xsize 566
                        text_align 0.5
                        size 30
                        color "#ffffff"
                        xalign 0.5
                        yalign 0.00
                        yoffset -5
                    
                    add Solid ("#ffffff", xysize=(585, 5)) xalign 0.5 yoffset 35 xoffset -5

                    # Фон подлокации.
                    $ bg = phone_get_sublocation_background(phone_map_sublocation)
                    if bg.get("type") == "image":
                        add Transform(bg.get("image"), size=(566, 440)) xpos 0 ypos 42
                    else:
                        add Solid(bg.get("color", "#1b1b1b"), xysize=(580, 442)) xpos -10 ypos 40

                    add Solid ("#ffffff", xysize=(585, 5)) xalign 0.5 ypos 480 xoffset -5

                    # Нижние вкладки подлокаций/корпусов — вынесены из vbox комнат
                    # для стабильной позиции, не зависящей от количества комнат.
                    hbox:
                        xpos 0
                        ypos 480
                        spacing 14

                        for sub_key, sub_data in phone_sublocation_items(phone_map_location):
                            fixed:
                                xysize (130, 62)

                                frame:
                                    xpos -5
                                    ypos 10
                                    xsize 137
                                    ysize 57
                                    background Solid("#ffffff")
                                    padding (5, 5)
                                    $ is_selected_sub = phone_map_sublocation == sub_key

                                    textbutton sub_data.get("name", sub_key):
                                        style "phone_black_button"
                                        xsize 127
                                        ysize 47
                                        text_size 14
                                        text_xmaximum 110
                                        text_text_align 0.5
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        text_layout "subtitle"
                                        text_color "#ffffff"
                                        text_hover_color "#ffff00"
                                        text_selected_color "#ffff00"
                                        selected is_selected_sub
                                        action Function(phone_set_map_sublocation, sub_key)

                                    $ qtarget = phone_selected_quest_target()
                                    if qtarget and qtarget["location"] == phone_map_location and qtarget["sublocation"] == sub_key:
                                        add Solid("#ffff00", xysize=(137, 5)) yoffset -5 xoffset -5 #at phone_map_quest_pulse 
                                        add Solid("#ffff00", xysize=(5, 57)) yoffset -5 xoffset -5 #at phone_map_quest_pulse 
                                        add Solid("#ffff00", xysize=(5, 57)) yoffset -5 xoffset 127 #at phone_map_quest_pulse 
                                        add Solid("#ffff00", xysize=(137, 5))  yoffset 47 xoffset -5 #at phone_map_quest_pulse
                                        #at phone_bottom_tab_quest_marker

                                    $ pmarker = phone_get_player_marker()
                                    if pmarker and pmarker["location"] == phone_map_location and pmarker["sublocation"] == sub_key:
                                        add "Krisheadcolored.png" xysize(43, 43) xpos 40 ypos 50

                    # Жёлтый маркер задания на карте — overlay поверх центральной области.
                    # Координаты идут из marker_x/marker_y, а не из кнопок комнат.
                    $ qtarget = phone_selected_quest_target()
                    if qtarget and qtarget["location"] == phone_map_location and qtarget["sublocation"] == phone_map_sublocation:
                        #add "orientir.png" at phone_map_quest_pulse
                        add "map_mark.png" xysize(20, 20) xpos qtarget.get("marker_x", qtarget.get("map_x", qtarget["x"])) ypos qtarget.get("marker_y", qtarget.get("map_y", qtarget["y"])) at phone_map_quest_pulse2

                        #add Solid("#ffff00", xysize=(20, 20)) xpos qtarget.get("marker_x", qtarget.get("map_x", qtarget["x"])) ypos qtarget.get("marker_y", qtarget.get("map_y", qtarget["y"])) at phone_map_quest_pulse2

                    # Коричневый маркер игрока.
                    # Положение идёт через PHONE_ROOM_BINDINGS по текущему store.room.
                    $ pmarker = phone_get_player_marker()
                    if pmarker and pmarker["location"] == phone_map_location and pmarker["sublocation"] == phone_map_sublocation:
                        add "Krisheadcolored.png" xysize(45, 45) xpos pmarker["x"]-10 ypos pmarker["y"]-10
                        #add Solid("#8a4b19", xysize=(24, 24)) xpos pmarker["x"] ypos pmarker["y"]

                # Отдельная проверка комнаты: если room игрока совпал с room цели,
                # показываем большой жёлтый квадрат и подпись. Это НЕ координатный маркер карты,
                # а именно индикатор «персонаж в нужной комнате».
                #if phone_player_in_quest_room():
                #    frame:
                #        xpos 392
                #        ypos 430
                #        xsize 155
                #        ysize 42
                #        background Solid("#000000CC")
                #        padding (6, 5)
                #        hbox:
                #            spacing 7
                #            add Solid("#ffff00", xysize=(22, 22)) at phone_room_match_marker
                #            text "комната цели" size 17 color "#ffff00" yalign 0.5

                # Нижние вкладки корпусов/подлокаций текущей большой локации.
                # Жёлтый маркер на вкладке — через transform phone_bottom_tab_quest_marker.
               
        use phone_dev_tool

transform phone_map_quest_pulse2:
    ease 0.35 yoffset -3
    ease 0.35 yoffset 0
    repeat

screen phone_journal_phone_side():
    frame:
        xoffset -10
        yoffset -10
        background "journalbg.png"
        padding (0, 0)
    
        vbox:
            xoffset 10
            yoffset 25
            spacing 0
            text "Локации" size 38 color "#998a55" xalign 0.5
            #add Solid("#ffffff", xysize=(235, 3))
            vbox:
                spacing 4
                # Правая часть телефона: крупные зоны.
                # Маркеры стоят в hbox: жёлтый = цель задания, коричневый = игрок.
                for route_key, route_name in PHONE_ROUTE_NAV:
                    hbox:
                        yoffset 5
                        
                        ysize 65
                        spacing -2
                        xfill True


                        if phone_route_has_player_marker(route_key):
                            add "Krisheadcolored.png"
                            #add Solid("#8a4b19", xysize=(14, 14)) yalign 0.5
                        else:
                            null width 65 height 65

                        button:
                            #background "#ffffff"
                            xsize 200
                            ysize 65
                            xfill True
                            #style "phone_black_button"
                            action Function(phone_set_route, route_key)

                            hbox:
                                yalign 0.5
                                spacing 0

                                text "[route_name]" size 25 color "#998a55"

                                if phone_route_has_quest_marker(route_key):
                                    add "orientir.png" xysize(9,9) at phone_map_quest_pulse 
                                    #add Solid("#ffff00", xysize=(14, 14)) yalign 0.5















            add Solid("#ffffff66", xysize=(235, 2))

            $ selected_q = PHONE_QUESTS.get(phone_selected_quest, {})
            $ pmarker = phone_get_player_marker()
            text "Выбрано: [selected_q.get('name', phone_selected_quest)]" size 17 color "#ffff00"
            text "Зона: [phone_get_route_name()]" size 15 color "#ffffff"
            text "Подлокация: [phone_get_sublocation_name()]" size 15 color "#ffffff"
            text "room: [getattr(store, 'room', 'нет room')]" size 15 color "#ffffff"
            text "цель room: [phone_get_selected_quest_room()]" size 15 color "#ffff00"
            text "player: [pmarker.get('label', '')]" size 15 color "#ffffff"

            if phone_player_in_quest_room():
                hbox:
                    spacing 8
                    add Solid("#ffff00", xysize=(18, 18)) at phone_room_match_marker
                    text "В НУЖНОЙ КОМНАТЕ" size 16 color "#ffff00" yalign 0.5
            else:
                text "не та комната" size 15 color "#aaaaaa"


screen phone_dev_tool():
    frame:
        xpos 5
        ypos 650
        xsize 840
        ysize 45
        background Solid("#111111DD")
        padding (5, 3)

        hbox:
            spacing 8

            text "DEV QUEST" size 15 color "#ff00ff" yalign 0.5

            text "selected: [phone_selected_quest]" size 14 color "#ffffff" yalign 0.5

            textbutton "-":
                text_size 16
                action Function(phone_add_quest_progress, phone_selected_quest, -1)

            text "stage: [phone_get_quest_progress(phone_selected_quest)]" size 14 color "#ffff00" yalign 0.5

            textbutton "+":
                text_size 16
                action Function(phone_add_quest_progress, phone_selected_quest, 1)

            textbutton "0":
                text_size 16
                action Function(phone_set_quest_progress, phone_selected_quest, 0)

            textbutton "1":
                text_size 16
                action Function(phone_set_quest_progress, phone_selected_quest, 1)

            textbutton "2":
                text_size 16
                action Function(phone_set_quest_progress, phone_selected_quest, 2)

            textbutton "3":
                text_size 16
                action Function(phone_set_quest_progress, phone_selected_quest, 3)

            text "target room: [phone_get_selected_quest_room()]" size 13 color "#ffff00" yalign 0.5


# ------------------------------------------------------------
# КОНТАКТЫ / ЧАТ
# ------------------------------------------------------------
transform phone_topics_slide_in:
    xoffset -35
    alpha 0.0
    ease 0.20 xoffset 0 alpha 1.0


screen phone_contacts_left_panel():
    if phone_chat_open and phone_contact_is_available(phone_selected_contact):
        timer 0.25 repeat True action Function(phone_refresh_chat_queue, phone_selected_contact)

    fixed:
        xpos 70
        ypos 55
        xysize (740, 600)

        #if not phone_chat_open:
        #    frame:
        #        xpos 0
        #        ypos 0
        #        xsize 740
        #        ysize 600
        #        background Solid("#000000")
        #        padding (25, 20)

        #        vbox:
        #            spacing 18
        #            xalign 0.5
        #            yalign 0.5
        #            text "Сообщения" size 42 color "#ffffff" xalign 0.5
        #            text "Выбери контакт на телефоне, чтобы открыть чат." size 24 color "#aaaaaa" xalign 0.5

        if phone_chat_open and phone_contact_is_available(phone_selected_contact):
            frame at phone_topics_slide_in:
                xpos 0
                ypos 0
                xsize 740
                ysize 600
                background Solid("#000000")
                padding (25, 20)

                vbox:
                    spacing 18
                    text "Темы: [phone_contact_name(phone_selected_contact)]" size 38 color "#ffffff" xalign 0.5

                    $ waiting_topic = phone_get_waiting_topic(phone_selected_contact)
                    if waiting_topic:
                        text "Собеседник ждёт ответа:" size 24 color "#ffff00"
                        text "[PHONE_TOPIC_DATA[waiting_topic]['incoming']]" size 22 color "#ffffff"
                        hbox:
                            spacing 12
                            for aid, player_text, npc_text in PHONE_TOPIC_DATA[waiting_topic]["answers"]:
                                textbutton player_text:
                                    style "phone_black_button"
                                    text_style "phone_black_button_text"
                                    action Function(phone_answer_topic, phone_selected_contact, waiting_topic, aid)
                    else:
                        $ start_topics = phone_get_player_start_topics(phone_selected_contact)
                        if start_topics:
                            text "Можно написать первыми:" size 24 color "#ffffff"
                            grid 2 3:
                                spacing 30
                                for topic_key in start_topics:
                                    textbutton PHONE_TOPIC_DATA[topic_key]["title"]:
                                        style "phone_black_button"
                                        text_style "phone_black_button_text"
                                        xsize 300
                                        ysize 65
                                        action Function(phone_player_start_topic, phone_selected_contact, topic_key)
                                for i in range(max(0, 6 - len(start_topics))):
                                    null width 300 height 65
                        else:
                            text "У этого персонажа сейчас нет доступных тем." size 24 color "#777777"

                    add Solid("#ffffff", xysize=(690, 2))
                    text "DEV темы текущего чата" size 18 color "#ff00ff"
                    hbox:
                        spacing 10
                        for topic_key in phone_contact_topics(phone_selected_contact):
                            textbutton PHONE_TOPIC_DATA[topic_key]["title"]:
                                text_size 16
                                action Function(phone_dev_trigger_topic, topic_key)
                        textbutton "reset":
                            text_size 16
                            action Function(phone_dev_reset_chats)


screen phone_contacts_phone_side():
    fixed:
        xysize (285, 586)

        if not phone_chat_open:
            text "Сообщения" xpos 0 ypos 10 xsize 265 text_align 0.5 size 30 color "#ffffff"
            add Solid("#ffffff66", xysize=(265, 2)) xpos 0 ypos 48

            viewport id "phone_contacts_viewport":
                xpos 0
                ypos 62
                xsize 265
                ysize PHONE_CONTACT_VIEWPORT_HEIGHT
                mousewheel True
                draggable True

                vbox:
                    spacing PHONE_CONTACT_ROW_SPACING

                    $ available_contacts = phone_available_contacts()
                    if not available_contacts:
                        text "Нет доступных контактов." size 16 color "#999999" xalign 0.5

                    for cid, cdata in available_contacts:
                        button:
                            style "phone_black_button"
                            xsize 255
                            ysize PHONE_CONTACT_ROW_HEIGHT
                            action Function(phone_open_chat, cid)

                            hbox:
                                spacing 8
                                yalign 0.5

                                frame:
                                    xsize 52
                                    ysize 52
                                    background Solid("#333333")
                                    padding (2, 2)

                                    text "[cid]" size 8 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5

                                frame:
                                    xsize 175
                                    ysize 52
                                    background Solid("#111111")
                                    padding (8, 5)

                                    vbox:
                                        spacing 2
                                        text cdata.get("name", cid) size 20 color "#ffffff"
                                        $ topic_count = len(cdata.get("topics", []))
                                        text "тем: [topic_count]" size 13 color "#999999"

            if phone_should_show_contact_vbar():
                vbar value YScrollValue("phone_contacts_viewport"):
                    xpos 268
                    ypos 62
                    xsize 8
                    ysize PHONE_CONTACT_VIEWPORT_HEIGHT
                    base_bar Solid("#222222")
                    thumb Solid("#ffffff")

        elif phone_contact_is_available(phone_selected_contact):
            hbox:
                xpos 0
                ypos 6
                spacing 6

                textbutton "←":
                    text_size 22
                    action Function(phone_close_chat)

                frame:
                    xsize 36
                    ysize 36
                    background Solid("#333333")
                    padding (2, 2)
                    text "[phone_selected_contact]" size 7 color "#ffffff" xalign 0.5 yalign 0.5 text_align 0.5

                text "[phone_contact_name(phone_selected_contact)]" size 22 color "#ffffff" yalign 0.5

            add Solid("#ffffff66", xysize=(265, 2)) xpos 0 ypos 48

            frame:
                xpos 0
                ypos 58
                xsize 265
                ysize 430
                background Solid("#927198")
                padding (6, 6)

                viewport:
                    mousewheel True
                    draggable True
                    xfill True
                    yfill True

                    vbox:
                        spacing 8
                        $ messages = phone_chat_messages.get(phone_selected_contact, [])
                        if not messages:
                            text "Пока нет сообщений." size 15 color "#ffffff" xalign 0.5
                        for msg in messages:
                            if msg["who"] == "player":
                                frame:
                                    xalign 1.0
                                    xmaximum 180
                                    background Solid("#b06ab9")
                                    padding (6, 4)
                                    text msg["text"] size 14 color "#ffffff"
                            else:
                                frame:
                                    xalign 0.0
                                    xmaximum 190
                                    background Solid("#6f4d75")
                                    padding (6, 4)
                                    text msg["text"] size 14 color "#ffffff"

            hbox:
                xpos 0
                ypos 500
                spacing 5
                add Solid("#ffffff", xysize=(205, 28))
                text ":)" size 18 color "#ffffff"
                text "▷" size 18 color "#ffffff"

        else:
            text "Контакт недоступен" xpos 0 ypos 250 xsize 265 text_align 0.5 size 18 color "#999999"
            textbutton "← к контактам":
                xpos 55
                ypos 285
                text_size 16
                action Function(phone_close_chat)


# ------------------------------------------------------------
# СПРАВОЧНИК / ИНФО
# ------------------------------------------------------------
screen phone_info_left_panel():
    # Экран рисуется только когда выбран конкретный подраздел
    # (например, «Основы боя» внутри «Боя»).
    if phone_info_section and phone_info_subsection:
        $ _info_sub = phone_info_subsection
        $ _needs_vbar = phone_info_needs_vbar(_info_sub)
        # Если нужен vbar — отдаём ему 30 px справа, иначе viewport на всю ширину.
        $ _vp_width = 780 if _needs_vbar else 810

        vbox:
            spacing 10
            xpos 10
            ypos 10
            xysize (820, 640)

            # Полоса с названием текущего подраздела.
            frame:
                xpos 0
                ypos 0
                xsize 870
                ysize 60

                frame:
                    xsize 860
                    ysize 50
                    xalign 0.5
                    yalign 0.5
                    background Solid("#000000")
                    text "[phone_info_subsection_name(_info_sub)]":
                        xalign 0.5
                        yalign 0.5
                        size 30
                        color "#ffff00"
                    
                    #textbutton "закрыть":
                    #    xalign 1.0 
                    #    action Function(phone_info_back)


            # Тело раздела.
            frame:
                xpos 0
                ypos 0
                xsize 870
                ysize 640

                frame:
                    xpos 0
                    ypos 0
                    xsize 860
                    ysize 630
                    background Solid("#000000")
                    padding (25, 20)

                    hbox:
                        spacing 10

                        viewport id "phone_info_viewport":
                            xsize _vp_width
                            ysize 590
                            mousewheel True
                            draggable True

                            vbox:
                                text "[phone_info_get_content(_info_sub)]":
                                    size 22
                                    color "#ffffff"

                        # vbar появляется только если текст не помещается.
                        if _needs_vbar:
                            vbar value YScrollValue("phone_info_viewport"):
                                xsize 20
                                ysize 590
                                base_bar Solid("#222222")
                                thumb Solid("#ffffff")


screen phone_info_phone_side():
    vbox:
        yoffset 10
        spacing 10
        xalign 0.5
        yalign 0.03

        # --- Хлебные крошки над кнопками ---
        # Фрейм присутствует ВСЕГДА, чтобы не сдвигать кнопки.
        # Для intro текст не выводим — остаётся пустое место того же размера.
        frame:
            xsize 260
            ysize 46
            background None
            padding (6, 4)
            if phone_info_section != "intro":
                text "[phone_info_breadcrumb()]":
                    size 20
                    color "#ffffff"
                    xalign 0.5
                    yalign 0.5
                    text_align 0.5
                    layout "subtitle"
                    xmaximum 250
                    ymaximum 38

        # --- Кнопки: либо разделы, либо подразделы текущего раздела ---
        # Список верхних разделов остаётся видимым, если:
        #   - раздел ещё не выбран (None);
        #   - это «Персонажи» (там своя навигация);
        #   - у выбранного раздела только ОДИН подраздел — тогда он открывается
        #     автоматически и промежуточный список кнопок-подразделов не нужен.
        $ _cur_subs = PHONE_INFO_SUBSECTIONS.get(phone_info_section, []) if phone_info_section else []
        $ _single_sub = (len(_cur_subs) == 1)

        if phone_info_section is None or phone_info_section == "characters" or _single_sub:
            for sec_key, sec_name in PHONE_INFO_SECTIONS:
                if sec_key != "characters":
                    textbutton sec_name:
                        style "phone_button"
                        text_style "phone_button_text"
                        xsize 250
                        ysize 55
                        # Подсветим выбранный раздел (актуально для "intro").
                        selected phone_info_section == sec_key
                        action Function(phone_select_info_section, sec_key)
                else:
                    textbutton "Персонажи":
                        style "phone_button"
                        text_style "phone_button_text"
                        xsize 250
                        ysize 55
                        action Function(phone_select_info_section, "characters")
        else:
            # Уровень 2: подразделы выбранного раздела (только для многосоставных разделов вроде «Бой»).
            $ _subs = PHONE_INFO_SUBSECTIONS.get(phone_info_section, [])
            if _subs and len(_subs) > 1:
                for sub_key, sub_name in _subs:
                    textbutton sub_name:
                        style "phone_black_button"
                        text_style "phone_black_button_text"
                        xsize 250
                        ysize 48
                        text_size 17
                        text_xmaximum 250
                        text_text_align 0.5
                        text_xalign 0.5
                        text_yalign 0.5
                        text_layout "subtitle"
                        text_selected_color "#ffff00"
                        selected phone_info_subsection == sub_key
                        action Function(phone_select_info_subsection, sub_key)

            textbutton "← назад":
                text_size 16
                action Function(phone_info_back)

        textbutton "домой":
            text_size 16
            action Function(phone_info_go_home)


#


# ------------------------------------------------------------
# ПЕРСОНАЖИ / ПАРТИЯ (v7: два фрейма, увеличенный размер, роли, опыт)
# ------------------------------------------------------------
screen phone_party_left_panel():
    fixed:
        xpos 30
        ypos 15
        xysize (900, 690)

        # --------------------------------------------------------
        # ФРЕЙМ 1: кнопки переключения вкладок
        # --------------------------------------------------------
        frame:
            xpos 0
            ypos 0
            xsize 840
            ysize 82
            background Solid("#ffffff")
            padding (10, 10)
            frame:
                xalign 0.5
                yalign 0.5
                xsize 830
                ysize 72
                background Solid("#000000")


                hbox:
                    spacing 10
                    xalign 0.5
                    yalign 0.5
                    for tab_key, tab_name in [("info", "Инфо"), ("stats", "Характеристики"),
                                            ("attacks", "Атаки"), ("magic", "Магия"),
                                            ("passive", "Пассив")]:
                        textbutton tab_name:
                            style "phone_black_button"
                            text_style "phone_black_button_text"
                            text_selected_color "#ffff00"
                            selected phone_character_info_tab == tab_key
                            xsize 150
                            ysize 58
                            text_size 26
                            text_xalign 0.5
                            text_yalign 0.5
                            action [SetVariable("phone_character_info_tab", tab_key), Function(phone_select_character_tab, tab_key)]

        # --------------------------------------------------------
        # ФРЕЙМ 2: вся остальная информация о персонаже
        # --------------------------------------------------------
        frame:
            xpos 0
            ypos 92
            xsize 840
            ysize 590
            background Solid("#ffffff")
            padding (5, 5)
            frame:
                xalign 0.5
                yalign 0.5
                xsize 830
                ysize 580
                background Solid("#000000")


                vbox:
                    spacing 12

                    if phone_character_info_tab == "info":
                        use phone_party_tab_info
                    elif phone_character_info_tab == "stats":
                        use phone_party_tab_stats
                    elif phone_character_info_tab == "attacks":
                        use phone_party_tab_list("Атаки", phone_character_attack_items(phone_selected_character))
                    elif phone_character_info_tab == "magic":
                        use phone_party_tab_list("Магия", phone_character_magic_items(phone_selected_character))
                    elif phone_character_info_tab == "passive":
                        use phone_party_tab_list("Пассив", phone_character_passive_items(phone_selected_character))
                    else:
                        use phone_party_tab_info


screen phone_party_tab_info():
    $ char_obj = phone_get_character_object(phone_selected_character)
    $ xp_frac = phone_get_xp_fraction(phone_selected_character)
    $ xp_fill = int(40 * xp_frac)

    vbox:
        spacing 12

        # Текущий уровень + маленькая полоска опыта:
        # база серая, заполнение белое, ширина = доля xp от максимума.
        fixed:
            xysize (840, 26)
            vbox:
                xpos 760
                ypos 2
                text "Ур.[phone_fmt_stat(phone_safe_attr(char_obj, 'level'))]" size 20 color "#ffffff" xalign 0.2 #xalign 1.0 xoffset -146 yoffset 0
                fixed:
                    xysize (40, 8)
                    add Solid("#555555", xysize=(40, 4))
                    if xp_fill > 0:
                        add Solid("#ffffff", xysize=(xp_fill, 4))

        frame:
            yoffset -40
            xsize 840
            ysize 330
            background None#Solid("#111111")
            padding (12, 10)

            vbox:
                spacing 10

                hbox:
                    spacing 20

                    vbox:
                        spacing 8
                        xsize 240
                        # текст имени персонажа
                        text "[phone_selected_character]" size 26 color "#ffffff" xalign 0.5
                        # изображение души персонажа
                        # (замени Solid на add "soul_имя.png", когда появятся картинки)
                        add Solid("#5f63d9", xysize=(230, 380)) xalign 0.5
                        

                        hbox:
                            spacing 16
                            yalign 0.5

                            vbox:
                                spacing 5
                                for role_attr, role_label, base_c, fill_c in PHONE_ROLE_ATTRS:
                                    text "[role_label]" size 22 color "#ffffff" xalign 0.0

                            vbox:
                                yoffset 4
                                spacing 15
                                for role_attr, role_label, base_c, fill_c in PHONE_ROLE_ATTRS:
                                    $ role_val = phone_get_role_value(phone_selected_character, role_attr)
                                    hbox:
                                        spacing 4
                                        for i in range(4):
                                            fixed:
                                                xysize (44, 14)
                                                add Solid(base_c, xysize=(44, 14))
                                                if i < role_val:
                                                    add Solid(fill_c, xysize=(44, 14))

                    # текст описания персонажа
                    text "[phone_character_notes_text(phone_selected_character)]" yoffset 20 size 20 color "#ffffff" #xmaximum 840

        # Характеристики + дополнительный vbox оценочных полосок (1..5)
        #use phone_party_stats_block


# ------------------------------------------------------------
# БЛОК ХАРАКТЕРИСТИК + ДОПОЛНИТЕЛЬНЫЙ VBOX ПОЛОСОК ОЦЕНКИ
# ------------------------------------------------------------
screen phone_party_stats_block():
    $ char_obj = phone_get_character_object(phone_selected_character)
    $ xp_frac = phone_get_xp_fraction(phone_selected_character)
    $ xp_fill = int(40 * xp_frac)
    
    # Словарь переводов для отображения
    $ stat_names_ru = {
        "hp": "Здоровье",
        "mp": "Мана",
        "atk": "Атака",
        "magic": "Магия",
        "defense": "Защита",
        "tank": "Танк",
        "dmgchance": "Точность",
        "critrate": "Крит. шанс",
        "crit": "Крит. урон",
        "feedness": "Сытость",
        "reltns": "Отношение",
        
        "diplomacy": "Дипломатия",
        "charm": "Очарование",
        "socialization": "Социализация",
        "perception": "Восприятие",
        "rhetoric": "Риторика",
        "artistry": "Артистизм",
        "comfort": "Комфорт",
        "power": "Власть"
    }

    vbox:
        spacing 12

        # ---------------------------------------------------------
        # ВЕРХНЯЯ ЧАСТЬ: Уровень, Опыт, Имя, Портрет
        # ---------------------------------------------------------
        frame:
            background None
            vbox:
                xpos 760
                ypos 2
                text "Ур.[phone_fmt_stat(phone_safe_attr(char_obj, 'level'))]" size 20 color "#ffffff" xalign 0.2
                fixed:
                    xysize (40, 8)
                    add Solid("#555555", xysize=(40, 4))
                    if xp_fill > 0:
                        add Solid("#ffffff", xysize=(xp_fill, 4))

        frame:
            yoffset -40
            background None
            padding (12, 10)

            vbox:
                spacing 10
                hbox:
                    spacing 20
                    vbox:
                        spacing 8
                        xsize 240
                        text "[phone_selected_character]" size 26 color "#ffffff" xalign 0.5
                        add Solid("#5f63d9", xysize=(230, 380)) xalign 0.5

    # ---------------------------------------------------------
    # ОСНОВНАЯ ЧАСТЬ: БЛОКИ ХАРАКТЕРИСТИК
    # ---------------------------------------------------------
    hbox:
        yoffset -470 
        xoffset 250
        spacing 30 
        
        # --- КОЛОНКА 1: БОЕВЫЕ ХАРАКТЕРИСТИКИ ---
        vbox:
            spacing 10
            text "Боевые" size 24 color "#ffffff" xalign 0.5
            add Solid("#727272", xysize=(250, 2))
            
            for stat_attr in PHONE_MAIN_STAT_ATTRS:
                $ rating = phone_stat_rating(phone_selected_character, stat_attr)
                
                # Получаем числовое значение для отображения справа
                $ raw_val = phone_get_total_stat(char_obj, stat_attr)
                $ display_val = "—"
                if raw_val is not None:
                    if stat_attr in ["dmgchance", "critrate"]:
                        $ display_val = "%d%%" % int(round(float(raw_val) * 100))
                    elif stat_attr == "crit":
                        # Крит. урон показываем как процент: 1.07 -> 107%
                        $ display_val = "%d%%" % int(round(float(raw_val) * 100))
                    elif stat_attr in ["atk", "magic", "defense", "tank"]:
                        # Целое без десятых
                        $ display_val = "%d" % int(round(float(raw_val)))
                    elif stat_attr in ["hp", "mp"]:
                        $ cur_hp = getattr(char_obj, "current_" + stat_attr, 0)
                        $ display_val = "%s/%s" % (phone_fmt_stat(cur_hp), phone_fmt_stat(raw_val))
                    else:
                        $ display_val = phone_fmt_stat(raw_val)

                # Получаем русское название
                $ ru_name = stat_names_ru.get(stat_attr, stat_attr.upper())

                # БЛОК ХАРАКТЕРИСТИКИ
                frame:
                    background Solid("#000000")
                    padding (8, 5)
                    xsize 260
                    ysize 30
                    
                    vbox:
                        # Верхняя строка: Название слева, Значение справа
                        hbox:
                            xfill True
                            yalign 0.5
                            text "[ru_name]" size 18 color "#aaaaaa"
                            text "[display_val]" size 18 color "#ffffff" xalign 1.0
                        
                        # Нижняя строка: Полоски рейтинга
                        hbox:
                            spacing 3
                            yalign 1.0 
                            for i in range(rating):
                                add Solid(PHONE_RATING_STRIP_COLORS[i], xysize=(47, 3))
                            for i in range(5 - rating):
                                add Solid("#000000", xysize=(40, 6))
                # --- Отступы между группами ---
                if stat_attr in ["mp", "magic", "crit"]:
                    null height 10

# --- КОЛОНКА 2: СОЦИАЛЬНЫЕ ХАРАКТЕРИСТИКИ ---
        vbox:
            spacing 10
            text "Социальные" size 24 color "#ffffff" xalign 0.5
            add Solid("#727272", xysize=(250, 2))

            for stat_attr in PHONE_SOCIAL_STAT_ATTRS:
                $ rating = phone_stat_rating(phone_selected_character, stat_attr)

                # Получаем числовое значение для отображения справа
                $ raw_val = phone_get_total_stat(char_obj, stat_attr)
                $ display_val = "—"
                if raw_val is not None:
                    $ display_val = phone_fmt_stat(raw_val)

                # Получаем русское название
                $ ru_name = stat_names_ru.get(stat_attr, stat_attr.upper())

                # БЛОК ХАРАКТЕРИСТИКИ
                frame:
                    background Solid("#000000")
                    padding (8, 5)
                    xsize 260
                    ysize 30

                    vbox:
                        # Верхняя строка: Название слева, Значение справа
                        hbox:
                            xfill True
                            yalign 0.5
                            text "[ru_name]" size 18 color "#aaaaaa"
                            text "[display_val]" size 18 color "#ffffff" xalign 1.0

                        # Нижняя строка: Полоски рейтинга
                        hbox:
                            spacing 3
                            yalign 1.0
                            for i in range(rating):
                                add Solid(PHONE_RATING_STRIP_COLORS[i], xysize=(47, 3))
                            for i in range(5 - rating):
                                add Solid("#000000", xysize=(40, 6))

                if stat_attr == "socialization":
                    null height 10
            hbox:
                spacing 8
                xalign 0.5
                yoffset 6

                textbutton "− ур":
                    style "phone_black_button"
                    text_style "phone_black_button_text"
                    text_size 20
                    xsize 120
                    ysize 34
                    action Function(_phone_level_minus)

                textbutton "+ ур":
                    style "phone_black_button"
                    text_style "phone_black_button_text"
                    text_size 20
                    xsize 120
                    ysize 34
                    action Function(_phone_level_plus)




init python:
    def _phone_level_minus():
        Pers.global_level = max(1, Pers.global_level - 1)
        renpy.restart_interaction()

    def _phone_level_plus():
        Pers.global_level = min(12, Pers.global_level + 1)
        renpy.restart_interaction()




screen phone_party_tab_stats():
    use phone_party_stats_block

screen phone_party_tab_list(tab_title, items):
    frame:
        xsize 825
        ysize 560
        background Solid("#000000")
        padding (18, 14)

        vbox:
            spacing 12
            text "[tab_title]: [phone_selected_character]" size 34 color "#ffff00" xalign 0.5
            add Solid("#ffffff66", xysize=(800, 2))

            hbox:
                spacing 8
                viewport id "phone_party_ability_viewport":
                    xsize 780
                    ysize 490
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 12
                        for item in phone_unlocked_ability_items(items, phone_selected_character):
                            $ item_name = item.get("name", "Без названия") if isinstance(item, dict) else item[0]
                            $ item_desc = item.get("description", "") if isinstance(item, dict) else item[1]
                            $ item_level = item.get("level", "") if isinstance(item, dict) else ""
                            $ item_resource = item.get("resource", "") if isinstance(item, dict) else ""
                            $ item_upgrade = item.get("upgrade", "") if isinstance(item, dict) else ""
                            $ item_is_upgrade = item.get("is_upgrade", False) if isinstance(item, dict) else False
                            frame:
                                xsize 750
                                background Solid("#000000")
                                padding (12, 10)

                                vbox:
                                    spacing 6
                                    fixed:
                                        xfill True
                                        ysize 34
                                        text "[item_name]" size (21 if item_is_upgrade else 25) color ("#fffb00" if item_is_upgrade else "#ffffff") xalign 0.5 yalign 0.5 text_align 0.5
                                        if item_level and not item_is_upgrade and int(item_level) > 1:
                                            text "ур. [item_level]" size 20 color "#ffffff" xalign 1.0 yalign 0.5
                                    if item_desc:
                                        text "[item_desc]" size 18 color "#aaaaaa"
                                    else:
                                        text "Описание пока не заполнено." size 18 color "#666666"
                                    if item_resource:
                                        text "[item_resource]" size 18 color "#66ccff"
                                    if item_upgrade:
                                        text "Улучшение способности:\n[item_upgrade]" size 18 color "#99ff99"
                                if isinstance(item, dict) and item.get("separator_after", False):
                                    add Solid("#777777", xysize=(730, 2))

                vbar value YScrollValue("phone_party_ability_viewport"):
                    xsize 18
                    ysize 490
                    base_bar Solid("#333333")
                    thumb Solid("#ffffff")
                    thumb_offset 0

default phone_role_mode = {}

init python:
    # Наборы ролей для переключения по ПКМ.
    # Добавляй сюда других персонажей, когда понадобится.
    PHONE_ROLE_SETS = {
        "pacifist": {
            "Крис":    {"damager_role": 2, "debuffer_role": 2, "tank_role": 3, "support_role": 2, "nego_role": 3},
            "Азриель": {"damager_role": 1, "debuffer_role": 1, "tank_role": 3, "support_role": 3, "nego_role": 3},
        },
        "geno": {
            "Крис":    {"damager_role": 4, "debuffer_role": 3, "tank_role": 3, "support_role": 1, "nego_role": 1},
            "Азриель": {"damager_role": 4, "debuffer_role": 3, "tank_role": 2, "support_role": 1, "nego_role": 1},
        },
    }

    # Кто поддерживает переключение.
    PHONE_ROLE_TOGGLE_CHARS = ("Крис", "Азриель")

    def phone_toggle_role_set(char_name):
        if char_name not in PHONE_ROLE_TOGGLE_CHARS:
            # Для остальных персонажей ПКМ просто ничего не делает.
            return

        char = phone_get_character_object(char_name)
        if char is None:
            return

        if not isinstance(store.phone_role_mode, dict):
            store.phone_role_mode = {}

        current = store.phone_role_mode.get(char_name)
        # Первое нажатие — pacifist. Второе — geno. Третье снова pacifist. И т.д.
        new_mode = "geno" if current == "pacifist" else "pacifist"

        roles = PHONE_ROLE_SETS.get(new_mode, {}).get(char_name)
        if not roles:
            return

        for attr_name, value in roles.items():
            setattr(char, attr_name, value)

        store.phone_role_mode[char_name] = new_mode
        renpy.notify(f"{char_name}: {new_mode}")
        renpy.restart_interaction()





screen phone_party_phone_side():
    vbox:
        spacing 13
        text "Персонажи" size 26 color "#ffffff" xalign 0.5
        grid 3 6:
            spacing 8
            for cname in phone_get_character_names():
                vbox:
                    spacing 2
                    button:
                        style "phone_black_button"
                        xsize 75
                        ysize 60
                        selected phone_selected_character == cname
                        action Function(phone_select_character, cname)
                        alternate Function(phone_toggle_role_set, cname)
                        add Solid("#5f4035", xysize=(38, 38)) xalign 0.5 yalign 0.5
                    text "[cname[:6]]" size 13 color "#ffffff" xalign 0.5
        textbutton "домой":
            text_size 16
            action Function(phone_set_panel, "home")


# ------------------------------------------------------------
# УДОБНЫЕ ЛЕЙБЛЫ ДЛЯ ТЕСТА
# ------------------------------------------------------------

default quest_click_qid = None     # qid кнопки, получившей «первый клик»
default quest_click_count = 0      # счётчик кликов по этой кнопке

init python:
    def handle_quest_click(qid):
        # --- Нажата ДРУГАЯ кнопка ---
        # Первый клик сбрасывается; описание, если открыто, закрывается.
        if store.quest_click_qid != qid:
            store.quest_click_qid = qid
            store.quest_click_count = 1
            renpy.hide_screen("quest_desc")
            phone_select_quest(qid)            # 1-й клик по новой кнопке — выбор квеста
            _phone_safe_restart()
            return

        # --- Нажата ТА ЖЕ кнопка ---
        store.quest_click_count += 1

        if store.quest_click_count == 2:
            renpy.show_screen("quest_desc")    # 2-й клик — открыть описание
        elif store.quest_click_count >= 3:
            renpy.hide_screen("quest_desc")    # 3-й клик — закрыть описание
            store.quest_click_count = 0
            store.quest_click_qid = None
        _phone_safe_restart()


    def phone_set_panel(panel_name):
        old_panel = store.phone_panel
        # Сбрасываем навигацию по «Инфо» при входе в него и при выходе из него.
        if panel_name == "info" or old_panel == "info":
            store.phone_info_section = None
            store.phone_info_subsection = None
        store.phone_panel = panel_name
        if panel_name == "contacts":
            store.phone_chat_open = False
        if panel_name != "journal":
            renpy.hide_screen("quest_desc")
            store.quest_click_qid = None
            store.quest_click_count = 0
        _phone_safe_restart()

    def phone_info_reset():
        store.phone_info_section = None
        store.phone_info_subsection = None

    def phone_go_home():
        """≡ — возвращает телефон в главное меню приложений из любого раздела/подраздела."""
        store.phone_panel = "home"
        store.phone_chat_open = False
        store.phone_info_section = None
        store.phone_info_subsection = None
        store.quest_click_qid = None
        store.quest_click_count = 0
        renpy.hide_screen("quest_desc")
        _phone_safe_restart()

    def phone_close_phone():
        """⌂ — закрывает телефон целиком и возвращает в мир (как Esc)."""
        store.control_Kris = 1
        store.phone_panel = "home"
        store.phone_chat_open = False
        store.phone_info_section = None
        store.phone_info_subsection = None
        store.quest_click_qid = None
        store.quest_click_count = 0
        renpy.hide_screen("quest_desc")
        renpy.hide_screen("complex_phone")
        _phone_safe_restart()


label open_complex_phone:
    show screen complex_phone
    #return

label test_complex_phone:
    call screen complex_phone
    return

transform amogus:
    yoffset -700 xoffset 200
    easein 0.4 yoffset 0



screen quest_desc():
    key "K_ESCAPE" action [Hide("quest_desc"), SetVariable("quest_click_qid", None), SetVariable("quest_click_count", 0)]
    zorder 201       # выше complex_phone
    modal False       # не блокирует клики по телефону

    $ q = PHONE_QUESTS.get(store.phone_selected_quest, {})

    frame at amogus:
        xsize 700
        ysize 700
        background Solid("#000000DD")
        padding (20, 20)
        vbox:
            spacing 12
            text q.get("name", "Задание") size 34 color "#ffff00"
            text q.get("desc", "Описания нет.") size 24 color "#ffffff"

# ------------------------------------------------------------
# МЕНЕДЖЕР КОМАНДЫ
# ------------------------------------------------------------
# Логика:
# 1) слоты команды показаны слева большими портретами-плейсхолдерами;
# 2) клик по портрету выбирает слот;
# 3) в телефоне справа появляются кнопки персонажей, которыми заменяется выбранный слот.

init python:
    PHONE_TEAM_CHAR_ROW_HEIGHT = 48
    PHONE_TEAM_CHAR_ROW_SPACING = 6
    PHONE_TEAM_CHAR_VIEWPORT_HEIGHT = 350

    def phone_try_ensure_team_manager():
        if hasattr(store, "ensure_team_manager"):
            store.ensure_team_manager()
            return
        if getattr(store, "team_manager", None) is None and "TeamManager" in globals():
            store.team_manager = TeamManager()
            if hasattr(store.team_manager, "rebuild_team_from_picked"):
                store.team_manager.rebuild_team_from_picked()
        if getattr(store, "characters", None) is None and getattr(store, "pers_dict", None) is not None:
            store.characters = store.pers_dict

    def phone_team_slots_ref():
        phone_try_ensure_team_manager()
        tm = getattr(store, "team_manager", None)

        if tm is not None and hasattr(tm, "team_slots"):
            max_size = int(getattr(tm, "MAX_TEAM_SIZE", 4))
            while len(tm.team_slots) < max_size:
                tm.team_slots.append(None)
            if len(tm.team_slots) > 0 and tm.team_slots[0] is None:
                tm.team_slots[0] = "Крис"
            return tm.team_slots

        # Фолбэк, если в проекте ещё нет team_manager.
        # Позволяет экрану работать как визуальный менеджер, но лучше подключить настоящий TeamManager.
        if not hasattr(store, "phone_fallback_team_slots") or store.phone_fallback_team_slots is None:
            store.phone_fallback_team_slots = ["Крис", None, None, None]
        while len(store.phone_fallback_team_slots) < 4:
            store.phone_fallback_team_slots.append(None)
        if store.phone_fallback_team_slots[0] is None:
            store.phone_fallback_team_slots[0] = "Крис"
        return store.phone_fallback_team_slots

    def phone_team_slots():
        return list(phone_team_slots_ref())

    def phone_team_available_characters():
        characters = getattr(store, "characters", None) or getattr(store, "pers_dict", {}) or {}
        if characters:
            names = list(characters.keys())
        else:
            names = phone_get_character_names()

        result = []
        for name in names:
            if not name:
                continue
            if str(name).startswith("Пусто"):
                continue
            if name == "Крис":
                continue
            if name not in result:
                result.append(name)
        return result

    def phone_team_should_show_char_vbar():
        count = len(phone_team_available_characters())
        if count <= 0:
            return False
        content_h = count * PHONE_TEAM_CHAR_ROW_HEIGHT + max(0, count - 1) * PHONE_TEAM_CHAR_ROW_SPACING
        return content_h > PHONE_TEAM_CHAR_VIEWPORT_HEIGHT

    def phone_team_select_slot(slot_index):
        store.forming_team_selected_slot = int(slot_index)
        _phone_safe_restart()

    def phone_team_sync_after_change():
        tm = getattr(store, "team_manager", None)
        if tm is not None:
            if hasattr(tm, "reorder_team_slots_by_current_attacker"):
                tm.reorder_team_slots_by_current_attacker()
            if hasattr(tm, "sync_picked_from_team"):
                tm.sync_picked_from_team()
            elif getattr(store, "pers_dict", None):
                slots = phone_team_slots_ref()
                for n, ch in store.pers_dict.items():
                    if hasattr(ch, "picked"):
                        ch.picked = 1 if n in slots else 0

        if hasattr(store, "update_followers_from_picked"):
            store.update_followers_from_picked()

    def phone_team_set_slot_character(slot_index, char_name):
        slots = phone_team_slots_ref()
        slot_index = int(slot_index)

        if slot_index <= 0:
            renpy.notify("Крис закреплён в первом слоте.")
            return
        if slot_index >= len(slots):
            renpy.notify("Такого слота нет.")
            return
        if not char_name or char_name == "Крис":
            return

        characters = getattr(store, "characters", None) or getattr(store, "pers_dict", {}) or {}
        if characters and char_name not in characters:
            renpy.notify("Персонаж {} недоступен.".format(char_name))
            return

        # Если персонаж уже стоял в другом слоте — переносим его в выбранный слот.
        for i, existing_name in enumerate(slots):
            if i != slot_index and existing_name == char_name:
                slots[i] = None

        slots[slot_index] = char_name
        store.forming_team_selected_slot = slot_index
        phone_team_sync_after_change()
        renpy.notify("Слот {}: {}".format(slot_index + 1, char_name))
        renpy.restart_interaction()

    def phone_team_clear_slot(slot_index):
        slots = phone_team_slots_ref()
        slot_index = int(slot_index)

        if slot_index <= 0:
            renpy.notify("Криса убрать нельзя.")
            return
        if slot_index >= len(slots):
            return

        slots[slot_index] = None
        store.forming_team_selected_slot = slot_index
        phone_team_sync_after_change()
        renpy.restart_interaction()

    # Старые функции оставлены как алиасы, чтобы другие части проекта не сломались.
    def phone_fallback_team_add(char_name, replace_slot_index=None):
        slot_index = replace_slot_index
        if slot_index is None:
            slot_index = getattr(store, "forming_team_selected_slot", 1)
        phone_team_set_slot_character(slot_index, char_name)

    def phone_fallback_team_remove(char_name):
        slots = phone_team_slots_ref()
        if char_name in slots:
            phone_team_clear_slot(slots.index(char_name))

label phone_open_team_manager:
    $ phone_try_ensure_team_manager()
    hide screen complex_phone
    show screen phone_team_fallback_manager
    return

screen phone_team_fallback_manager():
    modal True
    zorder 200

    key "K_ESCAPE" action Return()
    key "K_q" action Return()

    $ phone_try_ensure_team_manager()
    $ team_slots = phone_team_slots()
    $ max_size = len(team_slots)
    $ selected_slot = getattr(store, "forming_team_selected_slot", 1)
    if selected_slot is None or selected_slot < 0 or selected_slot >= max_size:
        $ selected_slot = 1 if max_size > 1 else 0
    $ can_replace_selected_slot = selected_slot > 0
    $ available_chars = phone_team_available_characters()

    add "#00000099"
    add "Vsechat_template.png"

    fixed:
        xysize (1280, 720)

        # --------------------------------------------------------
        # ЛЕВАЯ ЧАСТЬ: слоты команды крупными портретами
        # --------------------------------------------------------
        frame:
            xpos 45
            ypos 70
            xsize 820
            ysize 560
            background Solid("#000000CC")
            padding (24, 22)

            vbox:
                spacing 18

                text "Команда" size 42 color "#ffffff" xalign 0.5
                add Solid("#ffffff66", xysize=(760, 3)) xalign 0.5

                hbox:
                    spacing 20
                    xalign 0.5
                    yoffset 10

                    for i in range(max_size):
                        $ slot_name = team_slots[i] if i < len(team_slots) and team_slots[i] else "Пусто"
                        $ is_selected_slot = selected_slot == i
                        $ slot_bg = "#25364a" if is_selected_slot else "#111111"
                        $ slot_border = "#ffff00" if is_selected_slot else "#ffffff"

                        vbox:
                            spacing 8
                            xsize 175

                            $ slot_name_color = "#ffffff" if slot_name != "Пусто" else "#888888"
                            text "[slot_name]":
                                xsize 175
                                text_align 0.5
                                size 24
                                color slot_name_color

                            button:
                                xsize 175
                                ysize 350
                                background Solid(slot_border)
                                hover_background Solid("#ffff00")
                                padding (4, 4)
                                action Function(phone_team_select_slot, i)

                                frame:
                                    xfill True
                                    yfill True
                                    background Solid(slot_bg)
                                    padding (10, 10)

                                    vbox:
                                        spacing 8
                                        xalign 0.5
                                        yalign 0.5

                                        # Портрет-плейсхолдер. Потом заменишь на add "имя_портрета.png".
                                        $ portrait_bg = "#5f63d9" if slot_name != "Пусто" else "#151515"
                                        $ portrait_text_color = "#ffffff" if slot_name != "Пусто" else "#555555"
                                        $ slot_label_color = "#ffff00" if is_selected_slot else "#aaaaaa"
                                        frame:
                                            xsize 125
                                            ysize 235
                                            background Solid(portrait_bg)
                                            padding (5, 5)

                                            text "[slot_name]":
                                                size 18
                                                color portrait_text_color
                                                xalign 0.5
                                                yalign 0.5
                                                text_align 0.5

                                        text "Слот [i + 1]":
                                            xsize 150
                                            text_align 0.5
                                            size 18
                                            color slot_label_color

                hbox:
                    spacing 12
                    xalign 0.5
                    yoffset 20

                    text "Выбран слот: [selected_slot + 1]" size 22 color "#ffff00"

                    if selected_slot == 0:
                        text "Крис фиксирован" size 22 color "#aaaaaa"
                    elif selected_slot > 0:
                        textbutton "очистить слот":
                            text_size 18
                            action Function(phone_team_clear_slot, selected_slot)

        # --------------------------------------------------------
        # ПРАВАЯ ЧАСТЬ: телефон с кнопками замены персонажа
        # --------------------------------------------------------
        frame:
            xpos 913
            ypos 64
            xsize 305
            ysize 610
            background None

            frame:
                xfill True
                yfill True
                background "standart.jpg"
                padding (12, 18)

                fixed:
                    xysize (281, 574)

                    text "Команда":
                        xpos 0
                        ypos 10
                        xsize 281
                        text_align 0.5
                        size 32
                        color "#ffffff"

                    add Solid("#ffffff66", xysize=(255, 2)) xpos 13 ypos 52

                    frame:
                        xpos 10
                        ypos 66
                        xsize 261
                        ysize 76
                        background Solid("#00000099")
                        padding (8, 8)

                        vbox:
                            spacing 4
                            text "Выбран слот [selected_slot + 1]" size 18 color "#ffff00" xalign 0.5
                            if selected_slot < len(team_slots):
                                $ current_slot_name = team_slots[selected_slot] if team_slots[selected_slot] else "Пусто"
                                text "Сейчас: [current_slot_name]" size 16 color "#ffffff" xalign 0.5

                    if not can_replace_selected_slot:
                        text "Первый слот закреплён за Крисом.":
                            xpos 20
                            ypos 175
                            xsize 240
                            text_align 0.5
                            size 18
                            color "#aaaaaa"
                    else:
                        viewport id "phone_team_char_viewport":
                            xpos 10
                            ypos 158
                            xsize 246
                            ysize PHONE_TEAM_CHAR_VIEWPORT_HEIGHT
                            mousewheel True
                            draggable True

                            vbox:
                                spacing PHONE_TEAM_CHAR_ROW_SPACING

                                if not available_chars:
                                    text "Нет доступных персонажей." size 16 color "#aaaaaa" xalign 0.5

                                for char_name in available_chars:
                                    $ is_current_char = selected_slot < len(team_slots) and team_slots[selected_slot] == char_name
                                    $ is_in_other_slot = char_name in team_slots and not is_current_char
                                    $ char_button_text = char_name + (" ✓" if is_current_char else (" •" if is_in_other_slot else ""))
                                    $ char_button_color = "#ffff00" if is_current_char else "#ffffff"

                                    textbutton char_button_text:
                                        style "phone_black_button"
                                        xsize 238
                                        ysize PHONE_TEAM_CHAR_ROW_HEIGHT
                                        text_size 17
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        text_color char_button_color
                                        text_hover_color "#ffff00"
                                        action Function(phone_team_set_slot_character, selected_slot, char_name)

                        if phone_team_should_show_char_vbar():
                            vbar value YScrollValue("phone_team_char_viewport"):
                                xpos 262
                                ypos 158
                                xsize 8
                                ysize PHONE_TEAM_CHAR_VIEWPORT_HEIGHT
                                base_bar Solid("#222222")
                                thumb Solid("#ffffff")

                    textbutton "закрыть":
                        xpos 75
                        ypos 520
                        xsize 130
                        ysize 38
                        text_size 18
                        action Return()

        # Нижняя панель кнопок телефона, чтобы экран был похож на остальные приложения.
        frame:
            xsize 305
            ysize 60
            xpos 915
            ypos 620
            background "#000000"

        hbox:
            xpos 965
            ypos 630
            spacing 55
            textbutton "{size=28}{color=#ffffff}≡{/color}":
                action [Function(phone_go_home), Hide("phone_team_fallback_manager"), Show("complex_phone")]
            textbutton "{size=28}{color=#ffffff}⌂{/color}":
                action [Function(phone_close_phone), Hide("phone_team_fallback_manager")]
            textbutton "{size=28}{color=#ffffff}↩{/color}":
                action [SetVariable("phone_panel", "home"), Hide("phone_team_fallback_manager"), Show("complex_phone")]
