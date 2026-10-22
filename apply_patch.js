const fs = require('fs');

let s = fs.readFileSync('5_ENEMYDESC_ЭКРАН.rpy', 'utf8');

// 1. Add "Манекен" to ENEMY_PASSIVES if not present
const dummyPassives = `        "Манекен": {
            "permanent": [
                ("Это просто манекен",       "Скучающий кусок дерева и старой ткани, набитый соломой. Атак у него нет — но от скуки каждый герой в конце хода может получить Усталость ×3 и Безразличие ×3 с шансом 20%."),
                ("Бескровный, безмагии",     "Ни крови, ни магии — только дерево, ткань и нитки. Манекен не может получить кровотечение."),
                ("Рвущиеся швы",             "Старые швы не выдерживают натиска. Каждый критический удар по манекену снижает его бонусную защиту на 10%."),
            ],
            "mood": {
                "neutral": [
                    ("Полностью поддатливый", "Проверки социальных характеристик при действиях против манекена имеют очень низкую сложность."),
                    ("Закончим, когда захотим", "Любое успешное социальное действие сразу повышает пощаду манекена до 100%."),
                    ("Это... Просто манекен. Не думай на нём фармить", "После победы не даёт ни опыта, ни кромеров."),
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

        # Дженерик:`;

if (!s.includes('"Манекен":')) {
    s = s.replace('        # Дженерик:', dummyPassives);
}

// 2. Update get_enemy_active_effects
const targetOld = `        # Изначальные значения бонусов (по умолчанию 0.0)
        init_bonuses = getattr(enemy, "initial_bonuses", {}) or {}

        # Таблица бонусов: (ключ, текущее_значение, green_icon, red_icon, в_процентах)
        bonus_table = [
            ("bonus_atk",       getattr(enemy, "bonus_atk", 0.0),       "atk_green_icon.png",       "atk_red_icon.png",       True),
            ("bonus_magic",     getattr(enemy, "bonus_magic", 0.0),     "mag_green_icon.png",       "mag_red_icon.png",       True),
            ("bonus_def",       getattr(enemy, "bonus_def", 0.0),       "def_green_icon.png",       "def_red_icon.png",       True),
            ("bonus_dmgchance", getattr(enemy, "bonus_dmgchance", 0.0), "dmgchance_green_icon.png", "dmgchance_red_icon.png", True),
            ("bonus_critrate",  getattr(enemy, "bonus_critrate", 0.0),  "critrate_green_icon.png",  "critrate_red_icon.png",  True),
            ("bonus_crit",      getattr(enemy, "bonus_crit", 0.0),      "critdmg_green_icon.png",   "critdmg_red_icon.png",   True),
            ("bonus_tank",      getattr(enemy, "bonus_tank", 0.0),      "tank_green_icon.png",      "tank_red_icon.png",      False),
        ]

        for key, curr_val, green_icon, red_icon, is_pct in bonus_table:
            base_val = init_bonuses.get(key, 0.0)
            diff = curr_val - base_val

            if abs(diff) >= 0.001:
                is_buff = diff > 0
                icon = green_icon if is_buff else red_icon
                if is_pct:
                    text = "%+d%%" % int(round(diff * 100))
                else:
                    text = "%+d" % int(round(diff))
                result.append((icon, is_buff, text))`;

const targetNew = `        # Изначальные значения бонусов и характеристик
        init_bonuses = getattr(enemy, "initial_bonuses", {}) or {}
        init_stats = getattr(enemy, "initial_stats", {}) or {}

        # Таблица бонусов: (ключ_бонуса, текущее_значение_бонуса, green_icon, red_icon, в_процентах, ключ_характеристики, текущее_значение_характеристики)
        bonus_table = [
            ("bonus_atk",       getattr(enemy, "bonus_atk", 0.0),       "atk_green_icon.png",       "atk_red_icon.png",       True,  "atk",        getattr(enemy, "atk", 0)),
            ("bonus_magic",     getattr(enemy, "bonus_magic", 0.0),     "mag_green_icon.png",       "mag_red_icon.png",       True,  "magic",      getattr(enemy, "magic", 0)),
            ("bonus_def",       getattr(enemy, "bonus_def", 0.0),       "def_green_icon.png",       "def_red_icon.png",       True,  "defense",    getattr(enemy, "defense", 0)),
            ("bonus_dmgchance", getattr(enemy, "bonus_dmgchance", 0.0), "dmgchance_green_icon.png", "dmgchance_red_icon.png", True,  "dmgchance",  getattr(enemy, "dmgchance", 0.0)),
            ("bonus_critrate",  getattr(enemy, "bonus_critrate", 0.0),  "critrate_green_icon.png",  "critrate_red_icon.png",  True,  "critrate",   getattr(enemy, "critrate", 0)),
            ("bonus_crit",      getattr(enemy, "bonus_crit", 0.0),      "critdmg_green_icon.png",   "critdmg_red_icon.png",   True,  "crit",       getattr(enemy, "crit", 0.0)),
            ("bonus_tank",      getattr(enemy, "bonus_tank", 0.0),      "tank_green_icon.png",      "tank_red_icon.png",      False, "total_tank", getattr(enemy, "total_tank", 0)),
        ]

        for key, curr_val, green_icon, red_icon, is_pct, stat_key, curr_stat in bonus_table:
            base_val = init_bonuses.get(key, 0.0)
            diff = curr_val - base_val

            if abs(diff) >= 0.001:
                is_buff = diff > 0
                icon = green_icon if is_buff else red_icon
                if is_pct:
                    text = "%+d%%" % int(round(diff * 100))
                else:
                    text = "%+d" % int(round(diff))
                result.append((icon, is_buff, text))
            elif abs(curr_val) < 0.001:
                init_stat_val = init_stats.get(stat_key, None)
                if init_stat_val is not None and curr_stat > init_stat_val:
                    result.append((green_icon, True, None))`;

const normalize = (t) => t.replace(/\r\n/g, '\n');

if (!normalize(s).includes(normalize(targetOld))) {
    console.error('Target old block not found');
    process.exit(1);
}

s = normalize(s).replace(normalize(targetOld), targetNew);
fs.writeFileSync('5_ENEMYDESC_ЭКРАН.rpy', s, 'utf8');
console.log('Update complete');
