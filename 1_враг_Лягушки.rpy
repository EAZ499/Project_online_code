# ============================================================================
# ПАССИВКИ ЛЯГУШЕК-ВРАГОВ (Фроглин, Фрогетта, Фрогестер, Фрогис)
# Файл-аналог 1_враг_Арчи.rpy. Все хуки вызываются из общих боевых точек.
# ============================================================================

init python:

    FROG_NAMES = ("Фроглин", "Фрогетта", "Фрогестер", "Фрогис")

    def frog_act_key(action_name):
        """Убедить → Убеждение, Исполнить → Исполнение (ключи ACTS_CONFIG)."""
        return {"Убедить": "Убеждение", "Исполнить": "Исполнение"}.get(action_name, action_name)

    def frog_enemy_by_name(enemy_name):
        enemies = getattr(store, "enemies", {}) or {}
        enemy = enemies.get(enemy_name)
        if enemy is not None and getattr(enemy, "current_hp", 0) > 0:
            return enemy
        return None

    # ----------------------------------------------------------------
    # ИНИЦИАЛИЗАЦИЯ
    # ----------------------------------------------------------------
    def init_frog_battle_state(enemy):
        if enemy is None:
            return
        enemy.frog_warmup_stacks = getattr(enemy, "frog_warmup_stacks", 0)
        enemy.frog_dmg_bonus = getattr(enemy, "frog_dmg_bonus", 0.0)
        enemy.action_difficulties = getattr(enemy, "action_difficulties", {})

    def init_all_frogs_battle_state():
        enemies = getattr(store, "enemies", {}) or {}
        for name in FROG_NAMES:
            if name in enemies:
                init_frog_battle_state(enemies[name])

    # ----------------------------------------------------------------
    # СЛОЖНОСТИ
    # ----------------------------------------------------------------
    def frog_difficulty(enemy, action_name):
        """Возвращает фиксированную сложность действия или None."""
        if enemy is None or getattr(enemy, "name", None) not in FROG_NAMES:
            return None
        diffs = getattr(enemy, "action_difficulties", {}) or {}
        key = frog_act_key(action_name)
        if key in diffs:
            return int(diffs[key])
        return None

    # ----------------------------------------------------------------
    # «ИСКЛЮЧИТЕЛЬНАЯ УПЁРТОСТЬ» ФРОГИСА
    # Шанс = крит-шанс Фрогиса превратить успех в провал.
    # ----------------------------------------------------------------
    def frog_try_pride_override(enemy):
        if enemy is None or getattr(enemy, "name", None) != "Фрогис":
            return False
        chance = float(getattr(enemy, "critrate", 0.0) or 0.0)
        if renpy.random.random() < chance:
            renpy.notify("Фрогис упёрся: успех превращён в провал!")
            return True
        return False

    # ----------------------------------------------------------------
    # МОДИФИКАТОРЫ ХАРАКТЕРИСТИК
    # ----------------------------------------------------------------
    def frog_mod_atk(enemy, delta):
        if enemy is None: return
        enemy.bonus_atk = max(-0.9, float(getattr(enemy, "bonus_atk", 0.0)) + delta)

    def frog_mod_accuracy(enemy, delta):
        if enemy is None: return
        enemy.accuracy_debuff_var = max(-0.5, float(getattr(enemy, "accuracy_debuff_var", 0.0)) + delta)

    def frog_mod_critrate(enemy, delta):
        if enemy is None: return
        enemy.critrate_debuff_var = max(-0.5, float(getattr(enemy, "critrate_debuff_var", 0.0)) + delta)

    def frog_mod_critdmg(enemy, delta):
        if enemy is None: return
        enemy.critdmg_debuff_var = max(-0.5, float(getattr(enemy, "critdmg_debuff_var", 0.0)) + delta)

    def frog_mod_def_flat(enemy, delta):
        """Снижение итоговой защиты через def_debuff_var (множитель)."""
        if enemy is None: return
        enemy.def_debuff_var = max(0.0, float(getattr(enemy, "def_debuff_var", 1.0)) - delta)

    def frog_rollback_spare(enemy, attacker_name, multiplier):
        """Откатывает spare_progress на multiplier * diplomacy атакующего."""
        attacker = _rollback_resolve_attacker(attacker_name) if "_rollback_resolve_attacker" in globals() else None
        if attacker is None or enemy is None:
            return 0
        dip = int(getattr(attacker, "diplomacy", 0) or 0)
        if dip <= 0: return 0
        delta = int(round(dip * multiplier))
        if delta <= 0: delta = 1
        old = int(getattr(enemy, "spare_progress", 0) or 0)
        enemy.spare_progress = max(0, old - delta)
        return old - enemy.spare_progress

    # ----------------------------------------------------------------
    # ТАБЛИЦА ЭФФЕКТОВ ДЕЙСТВИЙ
    # "spare"      — добавить diplomacy*dip_multiply к spare_progress (успех)
    # "rollback"   — откатить spare_progress на X * diplomacy
    # "atk"        — изменить bonus_atk на X (множитель, 0.1 = +10%)
    # "critrate"   — изменить critrate_debuff_var на X
    # "critdmg"    — изменить critdmg_debuff_var на X
    # "accuracy"   — изменить accuracy_debuff_var на X
    # "def"        — уменьшить def_debuff_var на X
    # "dmg_bonus"  — добавить bonus_atk на X (учтено отдельно для читаемости)
    # ----------------------------------------------------------------
    frog_act_effects = {
        "Фроглин": {
            "Убеждение":  {"success": {"spare": 1.0}, "failure": {}},
            "Рассказать": {"success": {"spare": 1.0}, "failure": {}},
            "Поддержать": {"success": {}, "failure": {}},
            "Играть":     {"success": {"spare": 1.0}, "failure": {}},
            "Запугать":   {"success": {"rollback": 0.5, "atk":  0.20},
                           "failure": {"rollback": 1.0, "atk":  0.40}},
            "Грубить":    {"success": {"rollback": 0.5, "atk":  0.20},
                           "failure": {"atk": 0.40}},
            "Исполнение": {"success": {}, "failure": {}},
            "Дразнить":   {"success": {}, "failure": {}},
        },
        "Фрогетта": {
            "Убеждение":  {"success": {}, "failure": {}},
            "Рассказать": {"success": {}, "failure": {}},
            "Поддержать": {"success": {"spare": 1.0, "atk": 0.10},
                           "failure": {"atk": 0.20}},
            "Играть":     {"success": {"spare": 1.0, "critrate": 0.05},
                           "failure": {"spare": 1.0, "critrate": 0.10}},
            "Запугать":   {"success": {"rollback": 0.5, "critdmg":  0.08},
                           "failure": {"rollback": 1.0, "critdmg":  0.15}},
            "Грубить":    {"success": {"rollback": 0.5, "dmg_bonus": 0.08},
                           "failure": {"rollback": 1.0, "dmg_bonus": 0.16}},
            "Исполнение": {"success": {}, "failure": {}},
            "Дразнить":   {"success": {"spare": 1.0, "accuracy": 0.05},
                           "failure": {"accuracy": 0.10}},
        },
        "Фрогестер": {
            "Убеждение":  {"success": {}, "failure": {}},
            "Рассказать": {"success": {}, "failure": {}},
            "Поддержать": {"success": {"spare": 1.0}, "failure": {}},
            "Играть":     {"success": {"spare": 1.0}, "failure": {}},
            "Запугать":   {"success": {"def": 0.05}, "failure": {"def": 0.10}},
            "Грубить":    {"success": {"rollback": 0.5}, "failure": {"rollback": 1.0}},
            "Исполнение": {"success": {"spare": 1.0}, "failure": {}},
            "Дразнить":   {"success": {"accuracy": 0.05}, "failure": {"accuracy": 0.15}},
        },
        "Фрогис": {
            "Убеждение":  {"success": {}, "failure": {"atk": 0.05}},
            "Рассказать": {"success": {}, "failure": {}},
            "Поддержать": {"success": {}, "failure": {}},
            "Играть":     {"success": {}, "failure": {}},
            "Запугать":   {"success": {}, "failure": {}},
            "Грубить":    {"success": {"atk": 0.15}, "failure": {"atk": 0.30}},
            "Исполнение": {"success": {}, "failure": {}},
            "Дразнить":   {"success": {"rollback": 0.5}, "failure": {"rollback": 1.0}},
        },
    }

    def frog_apply_act(enemy, attacker, action_name, success):
        """Единая точка применения эффекта действия на лягушку."""
        if enemy is None or getattr(enemy, "name", None) not in FROG_NAMES:
            return
        key = frog_act_key(action_name)
        spec = (frog_act_effects.get(enemy.name, {}) or {}).get(key, {})
        result = spec.get("success" if success else "failure", {})
        dip = int(getattr(attacker, "diplomacy", 0) or 0) if attacker is not None else 0
        dip_mult = int(getattr(store, "dip_multiply", 1) or 1)
        if result.get("spare") and success:
            enemy.spare_progress = min(
                int(getattr(enemy, "spare_max", 100)),
                int(getattr(enemy, "spare_progress", 0)) + dip * dip_mult,
            )
        if result.get("rollback"):
            frog_rollback_spare(enemy, getattr(attacker, "name", None), result["rollback"])
        if result.get("atk"):
            frog_mod_atk(enemy, result["atk"])
        if result.get("critrate"):
            frog_mod_critrate(enemy, result["critrate"])
        if result.get("critdmg"):
            frog_mod_critdmg(enemy, result["critdmg"])
        if result.get("accuracy"):
            frog_mod_accuracy(enemy, result["accuracy"])
        if result.get("def"):
            frog_mod_def_flat(enemy, result["def"])
        if result.get("dmg_bonus"):
            frog_mod_atk(enemy, result["dmg_bonus"])

    # ----------------------------------------------------------------
    # ПАССИВКА «ИСКЛЮЧИТЕЛЬНАЯ УПЁРТОСТЬ» — вызывается из try_to_nego()
    # (см. задача 2.3 в файле 1_ПЕРС_ХАРАКТ.rpy)
    # ----------------------------------------------------------------
    # frog_try_pride_override уже определён выше.

    # ----------------------------------------------------------------
    # ПАССИВКА «МАГИЧЕСКАЯ АУРА» ФРОГЛИН — вызывается в начале боя
    # ----------------------------------------------------------------
    def frog_apply_magic_aura_on_battle_start():
        """-5% bonus_magic всем героям, +5% самой Фроглин."""
        f = frog_enemy_by_name("Фроглин")
        if f is None: return
        f.bonus_magic = float(getattr(f, "bonus_magic", 0.0)) + 0.05
        for char in (getattr(store, "pers_dict", {}) or {}).values():
            if getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0:
                char.bonus_magic = max(0.0, float(getattr(char, "bonus_magic", 0.0)) - 0.05)

    # ----------------------------------------------------------------
    # ПАССИВКА «МАГИЧЕСКАЯ ВРЕДНОСТЬ» ФРОГЛИН
    # Каждый ход −2 MP всем персонажам.
    # ----------------------------------------------------------------
    def frog_magic_harm_tick():
        f = frog_enemy_by_name("Фроглин")
        if f is None: return
        for char in (getattr(store, "pers_dict", {}) or {}).values():
            if getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0:
                char.current_mp = max(0, int(getattr(char, "current_mp", 0)) - 2)

    # ----------------------------------------------------------------
    # ПАССИВКА «ДЕЛЁЖКА» ФРОГЛИН
    # Если персонаж использует расходник с mp_heal — Фроглин получает +10% магии.
    # ----------------------------------------------------------------
    def frog_on_consumable_used(user, item_id, effects=None):
        f = frog_enemy_by_name("Фроглин")
        if f is None: return
        effects = effects or {}
        if int(effects.get("mp_heal", 0) or 0) > 0:
            f.bonus_magic = float(getattr(f, "bonus_magic", 0.0)) + 0.10
            renpy.notify("Фроглин: +10% магии за расходник маны")

    # ----------------------------------------------------------------
    # ПАССИВКА «А Я МОГУ СИЛЬНЕЕ!» ФРОГЕТТЫ
    # Каждый раз, когда она получает урон — +20% атаки.
    # ----------------------------------------------------------------
    def frog_on_damage_taken(enemy, old_hp, new_hp):
        if enemy is None: return new_hp
        if new_hp < old_hp:
            if getattr(enemy, "name", None) == "Фрогетта":
                enemy.bonus_atk = float(getattr(enemy, "bonus_atk", 0.0)) + 0.20
            elif getattr(enemy, "name", None) == "Фрогис":
                # «Видите? Они злодеи!» — сам Фрогис и все его атакующие
                enemy.atk_debuff = int(getattr(enemy, "atk_debuff", 0)) + 2
                enemy.critdmg_debuff_var = float(getattr(enemy, "critdmg_debuff_var", 0.0)) + 0.10
                attacker = None
                cur = getattr(store, "current_attacker", None)
                order = ["Крис","Азриель","Чара","Фриск","Иззи","Кловер","Седрик","Арчи","Сильвия","Фабри","Эмили","Сьюзи","Ральзей","Ноэлль","Санс","Бердли"]
                if isinstance(cur, int) and 0 < cur <= len(order):
                    attacker = (getattr(store, "pers_dict", {}) or {}).get(order[cur - 1])
                if attacker is not None and getattr(attacker, "current_hp", 0) > 0:
                    attacker.bonus_atk = float(getattr(attacker, "bonus_atk", 0.0)) + 0.05
                    attacker.bonus_crit = float(getattr(attacker, "bonus_crit", 0.0)) + 0.05
            elif getattr(enemy, "name", None) == "Фрогестер":
                # «Милое пузеко» — -10% атаки атакующему
                cur = getattr(store, "current_attacker", None)
                order = ["Крис","Азриель","Чара","Фриск","Иззи","Кловер","Седрик","Арчи","Сильвия","Фабри","Эмили","Сьюзи","Ральзей","Ноэлль","Санс","Бердли"]
                if isinstance(cur, int) and 0 < cur <= len(order):
                    att = (getattr(store, "pers_dict", {}) or {}).get(order[cur - 1])
                    if att is not None:
                        att.bonus_atk = max(0.0, float(getattr(att, "bonus_atk", 0.0)) - 0.10)
        return new_hp

    # ----------------------------------------------------------------
    # ПАССИВКА «БОЛЬНО НЕ БУДЕТ!» ФРОГЕТТЫ
    # Шанс = critrate нанести смертельный урон. Вызывается после успешного
    # calculate_dmg_to_hero.
    # ----------------------------------------------------------------
    def frog_try_lethal_on_attack(target_hero):
        f = frog_enemy_by_name("Фрогетта")
        if f is None or target_hero is None:
            return False
        if getattr(target_hero, "current_hp", 0) <= 0:
            return False
        chance = float(getattr(f, "critrate", 0.0) or 0.0)
        if renpy.random.random() < chance:
            target_hero.current_hp = 0
            renpy.notify("Фрогетта: «Больно не будет!»")
            return True
        return False

    # ----------------------------------------------------------------
    # ПАССИВКА «НАТОЧЕННЫЕ СТРЕЛЫ» ФРОГЕСТЕРА
    # Каждое попадание снарядом — +1 стак кровотечения.
    # ----------------------------------------------------------------
    def frog_frogster_bleed_on_hit(target_hero):
        f = frog_enemy_by_name("Фрогестер")
        if f is None or target_hero is None: return
        target_hero.bloodshed_debuff = int(getattr(target_hero, "bloodshed_debuff", 0)) + 1
        if hasattr(target_hero, "bloodshed_debuff_got"):
            target_hero.bloodshed_debuff_got += 1

    # ----------------------------------------------------------------
    # ТИК КОНЦА РАУНДА
    # ----------------------------------------------------------------
    def frog_on_battle_round_tick():
        enemies = getattr(store, "enemies", {}) or {}

        # «Не задобришь!» Фрогис — каждый ход −15% от spare_max
        frogis = frog_enemy_by_name("Фрогис")
        if frogis is not None:
            rollback = max(1, int(getattr(frogis, "spare_max", 40) * 0.15))
            frogis.spare_progress = max(0, int(getattr(frogis, "spare_progress", 0)) - rollback)

        # «Не особо-то и хотелось» Фрогестер — +15% от spare_max в конце хода
        frogster = frog_enemy_by_name("Фрогестер")
        if frogster is not None:
            regen = max(1, int(getattr(frogster, "spare_max", 30) * 0.15))
            frogster.spare_progress = min(
                int(getattr(frogster, "spare_max", 30)),
                int(getattr(frogster, "spare_progress", 0)) + regen,
            )

        # «Готовка к удару» Фрогетта — +5% accuracy/critrate себе, +2% союзникам
        froggette = frog_enemy_by_name("Фрогетта")
        if froggette is not None:
            froggette.frog_warmup_stacks = int(getattr(froggette, "frog_warmup_stacks", 0)) + 1
            frog_mod_accuracy(froggette, 0.05)
            frog_mod_critrate(froggette, 0.05)
            for name in ("Фроглин", "Фрогестер", "Фрогис"):
                ally = frog_enemy_by_name(name)
                if ally is None: continue
                frog_mod_accuracy(ally, 0.02)
                frog_mod_critrate(ally, 0.02)