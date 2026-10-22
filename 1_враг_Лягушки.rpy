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
        # Пассивки лягушек работают только в их собственном бою.
        if getattr(store, "battlenumber", 0) != 20:
            return None
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
    # «ИСКЛЮЧИТЕЛЬНАЯ УПЁРТОСТЬ» ФРОГЕСТЕРА
    # Шанс = крит-шанс Фрогестера превратить успех в провал.
    # ----------------------------------------------------------------
    def frog_try_pride_override(enemy):
        if enemy is None or getattr(enemy, "name", None) != "Фрогестер":
            return False
        chance = float(getattr(enemy, "critrate", 0.0) or 0.0)
        if renpy.random.random() < chance:
            renpy.notify("Фрогестер упёрся: успех превращён в провал!")
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
        enemy.bonus_dmgchance2 = max(-0.5, float(getattr(enemy, "bonus_dmgchance2", 0.0)) + delta)

    def frog_mod_critrate(enemy, delta):
        if enemy is None: return
        enemy.bonus_critrate2 = max(-0.5, float(getattr(enemy, "bonus_critrate2", 0.0)) + delta)

    def frog_mod_critdmg(enemy, delta):
        if enemy is None: return
        enemy.bonus_crit2 = max(-0.5, float(getattr(enemy, "bonus_crit2", 0.0)) + delta)

    def frog_mod_def_flat(enemy, delta):
        """Снижение итоговой защиты через bonus_def."""
        if enemy is None: return
        enemy.bonus_def = float(getattr(enemy, "bonus_def", 0.0)) - delta

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
            enemy.atk_debuff_got = int(getattr(enemy, "atk_debuff_got", 0) or 0) - (1 if result["atk"] > 0 else -1)
        if result.get("critrate"):
            frog_mod_critrate(enemy, result["critrate"])
            enemy.critrate_debuff_got = int(getattr(enemy, "critrate_debuff_got", 0) or 0) - (1 if result["critrate"] > 0 else -1)
        if result.get("critdmg"):
            frog_mod_critdmg(enemy, result["critdmg"])
            enemy.critdmg_debuff_got = int(getattr(enemy, "critdmg_debuff_got", 0) or 0) - (1 if result["critdmg"] > 0 else -1)
        if result.get("accuracy"):
            frog_mod_accuracy(enemy, result["accuracy"])
            enemy.accuracy_debuff_got = int(getattr(enemy, "accuracy_debuff_got", 0) or 0) - (1 if result["accuracy"] > 0 else -1)
        if result.get("def"):
            frog_mod_def_flat(enemy, result["def"])
            # frog_mod_def_flat вычитает delta из bonus_def -> положительный delta = дебафф
            enemy.def_debuff_got = int(getattr(enemy, "def_debuff_got", 0) or 0) + (1 if result["def"] > 0 else -1)
        if result.get("dmg_bonus"):
            frog_mod_atk(enemy, result["dmg_bonus"])
            enemy.atk_debuff_got = int(getattr(enemy, "atk_debuff_got", 0) or 0) - (1 if result["dmg_bonus"] > 0 else -1)

    # ----------------------------------------------------------------
    # ПАССИВКА «ИСКЛЮЧИТЕЛЬНАЯ УПЁРТОСТЬ» — вызывается из try_to_nego()
    # (см. задача 2.3 в файле 1_ПЕРС_ХАРАКТ.rpy)
    # ----------------------------------------------------------------
    # frog_try_pride_override уже определён выше.



# ----------------------------------------------------------------
# ПАССИВКА «МАГИЧЕСКАЯ АУРА» ФРОГЛИН 
# ----------------------------------------------------------------
    def frog_magic_aura_round_tick():
        """«Магическая аура» в конце раунда.

        Фактический эффект (накопительно): +15% bonus_magic Фроглин,
        -5% bonus_magic героям.
        Визуал:
          - heroes_attacked_visual смотрит на *_got
            (<0 -> зелёная иконка, >0 -> красная);
          - enemydesc (если он смотрит на magic_debuff) —
            выставляем magic_debuff = -1.
        Возвращает True, если эффект применён.
        """
        f = frog_enemy_by_name("Фроглин")
        if f is None:
            return False

        # 1) Реальный накопительный эффект для Фроглин
        f.bonus_magic = float(getattr(f, "bonus_magic", 0.0)) + 0.08

        # 2) Визуал Фроглин: зелёная иконка магии
        f.magic_debuff_got = int(getattr(f, "magic_debuff_got", 0) or 0) - 3
        # и для enemydesc, если он смотрит на magic_debuff
        f.magic_debuff = int(getattr(f, "magic_debuff", 0) or 0) - 1

        # 3) Герои: реальный упадок + красная иконка
        for char in (getattr(store, "pers_dict", {}) or {}).values():
            if getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0:
                char.bonus_magic = float(getattr(char, "bonus_magic", 0.0)) - 0.05
                char.magic_debuff_got = int(getattr(char, "magic_debuff_got", 0) or 0) + 1
                renpy.notify("{}: magic_debuff_got={}".format(char.name, char.magic_debuff_got))  # отладка

        return True

    # ----------------------------------------------------------------
    # ПАССИВКА «МАГИЧЕСКАЯ ВРЕДНОСТЬ» ФРОГЛИН
    # Каждый ход −6 MP всем персонажам.
    # ----------------------------------------------------------------
    def frog_magic_harm_tick():
        f = frog_enemy_by_name("Фроглин")
        if f is None: return
        for char in (getattr(store, "pers_dict", {}) or {}).values():
            if getattr(char, "picked", 0) == 1 and getattr(char, "current_hp", 0) > 0:
                char.current_mp = max(0, int(getattr(char, "current_mp", 0)) - 6)

    # ----------------------------------------------------------------
    # ПАССИВКА «ДЕЛЁЖКА» ФРОГЛИН
    # Если персонаж использует расходник с mp_heal — Фроглин получает +10% магии.
    # ----------------------------------------------------------------
    def frog_on_consumable_used(user, item_id, effects=None):
        f = frog_enemy_by_name("Фроглин")
        if f is None: return
        effects = effects or {}
        if int(effects.get("mp_heal", 0) or 0) > 0:
            f.bonus_magic = float(getattr(f, "bonus_magic", 0.0)) + 0.15
            # Визуал как у «Магической ауры»: зелёная иконка магии
            # в бою и бафф магии в ENEMYDESC.
            f.magic_debuff_got = int(getattr(f, "magic_debuff_got", 0) or 0) - 3
            f.magic_debuff = int(getattr(f, "magic_debuff", 0) or 0) - 1
            renpy.notify("Фроглин: +10% магии за расходник маны")

    # ----------------------------------------------------------------
    # ПАССИВКА «А Я МОГУ СИЛЬНЕЕ!» ФРОГЕТТЫ
    # Каждый раз, когда она получает урон — +20% атаки.
    # ----------------------------------------------------------------
    def frog_on_damage_taken(enemy, old_hp, new_hp):
        if enemy is None:
            return new_hp
        if new_hp < old_hp:
            name = getattr(enemy, "name", None)

            if name == "Фрогетта":
                # «А я могу сильнее!» — +20% атаки при получении урона
                enemy.bonus_atk = float(getattr(enemy, "bonus_atk", 0.0)) + 0.20
                # бафф атаки — зелёная иконка
                enemy.atk_debuff_got = int(getattr(enemy, "atk_debuff_got", 0) or 0) - 1

            elif name == "Фрогестер":
                # «Видите? Они злодеи!»
                # Фрогестер: +2 стака истощения, +10% крит-урона
                enemy.atk_debuff = int(getattr(enemy, "atk_debuff", 0)) - 2
                # +2 дебаффа атаки — красная ×2
                enemy.atk_debuff_got = int(getattr(enemy, "atk_debuff_got", 0) or 0) - 2
                enemy.bonus_crit2 = float(getattr(enemy, "bonus_crit2", 0.0)) + 0.10
                # +10% крит-урона — зелёная
                enemy.critdmg_debuff_got = int(getattr(enemy, "critdmg_debuff_got", 0) or 0) - 1

                # Атакующий: +5% атаки, +5% крит-урона
                cur = getattr(store, "current_attacker", None)
                order = ["Крис","Азриель","Чара","Фриск","Иззи","Кловер","Седрик",
                         "Арчи","Сильвия","Фабри","Эмили","Сьюзи","Ральзей","Ноэлль","Санс","Бердли"]
                if isinstance(cur, int) and 0 < cur <= len(order):
                    attacker = (getattr(store, "pers_dict", {}) or {}).get(order[cur - 1])
                    if attacker is not None and getattr(attacker, "current_hp", 0) > 0:
                        attacker.bonus_atk = float(getattr(attacker, "bonus_atk", 0.0)) + 0.05
                        attacker.atk_debuff_got = int(getattr(attacker, "atk_debuff_got", 0) or 0) - 1
                        attacker.bonus_crit = float(getattr(attacker, "bonus_crit", 0.0)) + 0.05
                        attacker.critdmg_debuff_got = int(getattr(attacker, "critdmg_debuff_got", 0) or 0) - 1

            elif name == "Фрогис":
                # «Милое пузеко» — −10% атаки атакующему
                cur = getattr(store, "current_attacker", None)
                order = ["Крис","Азриель","Чара","Фриск","Иззи","Кловер","Седрик",
                         "Арчи","Сильвия","Фабри","Эмили","Сьюзи","Ральзей","Ноэлль","Санс","Бердли"]
                if isinstance(cur, int) and 0 < cur <= len(order):
                    att = (getattr(store, "pers_dict", {}) or {}).get(order[cur - 1])
                    if att is not None:
                        att.bonus_atk = max(0.0, float(getattr(att, "bonus_atk", 0.0)) - 0.10)
                        # −10% атаки — красная
                        att.atk_debuff_got = int(getattr(att, "atk_debuff_got", 0) or 0) + 1

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
            target_hero.shield = 0
            renpy.notify("Фрогетта: «Больно не будет!»")
            return True
        return False

    # ----------------------------------------------------------------
    # ПАССИВКА «НАТОЧЕННЫЕ СТРЕЛЫ» ФРОГИСА
    # Каждое попадание снарядом — +1 стак кровотечения.
    # ----------------------------------------------------------------
    def frog_frogster_bleed_on_hit(target_hero):
        f = frog_enemy_by_name("Фрогис")
        if f is None or target_hero is None: return
        target_hero.bloodshed_debuff = int(getattr(target_hero, "bloodshed_debuff", 0)) + 1
        if hasattr(target_hero, "bloodshed_debuff_got"):
            target_hero.bloodshed_debuff_got += 1

    # ----------------------------------------------------------------
    # ТИК КОНЦА РАУНДА
    # ----------------------------------------------------------------
    def frog_on_battle_round_tick():
        enemies = getattr(store, "enemies", {}) or {}

        # «Не задобришь!» — ФРОГЕСТЕР. Каждый ход −15% от spare_max.
        frogster = frog_enemy_by_name("Фрогестер")
        if frogster is not None:
            rollback = max(1, int(getattr(frogster, "spare_max", 40) * 0.15))
            frogster.spare_progress = max(0, int(getattr(frogster, "spare_progress", 0)) - rollback)

        # «Не особо-то и хотелось» — ФРОГИС. Каждый ход +15% от spare_max.
        frogis = frog_enemy_by_name("Фрогис")
        if frogis is not None:
            regen = max(1, int(getattr(frogis, "spare_max", 30) * 0.15))
            frogis.spare_progress = min(
                int(getattr(frogis, "spare_max", 30)),
                int(getattr(frogis, "spare_progress", 0)) + regen,
            )

        # «Готовка к удару» — Фрогетта. +5% accuracy/critrate себе, +2% союзникам.
        froggette = frog_enemy_by_name("Фрогетта")
        if froggette is not None:
            froggette.frog_warmup_stacks = int(getattr(froggette, "frog_warmup_stacks", 0)) + 1
            frog_mod_accuracy(froggette, 0.05)
            froggette.accuracy_debuff_got = int(getattr(froggette, "accuracy_debuff_got", 0) or 0) - 1
            frog_mod_critrate(froggette, 0.05)
            froggette.critrate_debuff_got = int(getattr(froggette, "critrate_debuff_got", 0) or 0) - 1
            for name in ("Фроглин", "Фрогестер", "Фрогис"):
                ally = frog_enemy_by_name(name)
                if ally is None:
                    continue
                frog_mod_accuracy(ally, 0.02)
                ally.accuracy_debuff_got = int(getattr(ally, "accuracy_debuff_got", 0) or 0) - 1
                frog_mod_critrate(ally, 0.02)
                ally.critrate_debuff_got = int(getattr(ally, "critrate_debuff_got", 0) or 0) - 1

    # ----------------------------------------------------------------
    # ПРЕДВАРИТЕЛЬНЫЙ ОСМОТР ЛЯГУШЕК (battlenumber == 20)
    # Ставит всем живым лягушкам «Осмотрено 5 раз», как будто игрок
    # пять раз успешно применил «Оценить» ещё до первого хода.
    #
    # Три штуки, которые читает UI/боёвка:
    #   1) evaluate_success_count = 5  — уровень осмотра в ENEMYDESC:
    #      раскрывает пассивки и точный HP (потолок 5 стоит в apply_act_to_enemy);
    #   2) action_progress["evaluate_progress"] = 5 — прогресс самого действия;
    #   3) mood_action_revealed[mood][act] = True + mood_action_used["Оценить"]
    #      — get_act_button_color() рисует кнопки ACT цветом эффекта,
    #      а не белым «как будто не нажимали».
    #
    # spare_progress НЕ трогается: предосмотр не приближает пощаду.
    # Перебор идёт по "store.ACTS_CONFIG" — так же, как в
    # reveal_random_acts_to_enemy(), поэтому набор раскрытых действий
    # совпадает с реальным осмотром.
    # ----------------------------------------------------------------
    FROG_EVALUATE_TARGET = 5   # = кэп evaluate_success_count в apply_act_to_enemy

    def mark_frogs_checked_from_start():
        enemies = getattr(store, "enemies", {}) or {}
        checked = []
        # list(): словари намеренно не создаём/не меняем структуру на ходу.
        for fname in list(FROG_NAMES):
            frog = enemies.get(fname)
            if frog is None or getattr(frog, "current_hp", 0) <= 0:
                continue

            # 1) Счётчик успешных осмотров (максимум).
            frog.evaluate_success_count = FROG_EVALUATE_TARGET

            # 2) Прогресс действия «Оценить».
            if not isinstance(getattr(frog, "action_progress", None), dict):
                frog.action_progress = {}
            frog.action_progress["evaluate_progress"] = FROG_EVALUATE_TARGET

            # 3) Журналы настроений: гарантируем все 8 настроений.
            #    Лягушки стартуют в "happy" (см. блок _frogs в make_enemies),
            #    но если настроение уже сменилось — красим текущее.
            _ensure_mood_action_used(frog)
            mood = getattr(frog, "mood", "happy")
            frog.mood_action_used.setdefault(mood, {})["Оценить"] = True
            for _act in list(store.ACTS_CONFIG.keys()):
                if _act in ("Оценить", "Пощадить"):
                    continue
                frog.mood_action_revealed.setdefault(mood, {})[_act] = True

            checked.append(fname)
        return checked

    def change_frogs_evaluate_level(delta):
        enemies = getattr(store, "enemies", {}) or {}
        last_val = 0
        targets = []
        if "get_active_enemies" in globals():
            try:
                for name in get_active_enemies():
                    if name in enemies:
                        targets.append(enemies[name])
            except Exception:
                pass
        if not targets:
            targets = list(enemies.values())
        t = getattr(store, "target", None)
        if t is not None and t not in targets:
            targets.append(t)
        for e in targets:
            cur = int(getattr(e, "evaluate_success_count", 0))
            new_val = max(0, min(5, cur + delta))
            e.evaluate_success_count = new_val
            if hasattr(e, "action_progress") and isinstance(e.action_progress, dict):
                e.action_progress["evaluate_progress"] = new_val
            if hasattr(e, "evaluate_progress"):
                e.evaluate_progress = new_val
            last_val = new_val
        renpy.notify("Осмотр: %d" % last_val)
        renpy.restart_interaction()

    def get_frogs_evaluate_display():
        enemies = getattr(store, "enemies", {}) or {}
        targets = []
        if "get_active_enemies" in globals():
            try:
                for name in get_active_enemies():
                    if name in enemies:
                        targets.append(enemies[name])
            except Exception:
                pass
        if not targets:
            targets = list(enemies.values())
        if targets:
            vals = [str(getattr(e, "evaluate_success_count", 0)) for e in targets]
            return vals[0] if len(set(vals)) == 1 else "/".join(vals)
        t = getattr(store, "target", None)
        if t is not None:
            return str(getattr(t, "evaluate_success_count", 0))
        return "0"


# Лейбл для вызова из боя: call mark_frogs_checked_from_start
label mark_frogs_checked_from_start:
    if battlenumber == 20:
        $ _frog_checked = mark_frogs_checked_from_start()
    return
