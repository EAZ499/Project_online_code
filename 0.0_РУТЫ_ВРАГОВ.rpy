# =====================================================================
#  ТРЕВОР — данные и эффекты; универсальная система рутов ниже.
# =====================================================================

define TREVOR_PEACE_THRESHOLD        = 24
define TREVOR_RIVALRY_THRESHOLD      = 18
define TREVOR_RIVALRY_HAPPY_PROGRESS = 27
define TREVOR_PEACE_TARGET           = 50
define TREVOR_RIVALRY_TARGET         = 50

define TREVOR_PEACEFUL_ACTIONS = {"Вопрос", "Поддержать", "Унижаться"}
define TREVOR_RIVALRY_ACTIONS  = {"Запугать", "Грубить", "Дразнить"}

default trevor_act_effects = {
    "neutral": {
        "Оценить":     {"default":  0},
        "Вопрос":      {"default":  1},
        "Убеждение":   {"default":  0, "Азриель": -1},
        "Рассказать":  {"default":  0, "Азриель": -1},
        "Поддержать":  {"default":  1, "Азриель":  0},
        "Играть":      {"default":  0, "Азриель": -1},
        "Запугать":    {"default":  1},
        "Грубить":     {"default":  1},
        "Исполнение":  {"default":  0},
        "Дразнить":    {"default": -1},
        "Унижаться":   {"default":  1},
    },
    "angry": {
        "Оценить":     {"default":  0},
        "Вопрос":      {"default":  0},
        "Убеждение":   {"default":  0},
        "Рассказать":  {"default": -1},
        "Поддержать":  {"default": -1},
        "Играть":      {"default":  1},
        "Запугать":    {"default":  1},
        "Грубить":     {"default":  1},
        "Исполнение":  {"default": -1},
        "Дразнить":    {"default":  1},
        "Унижаться":   {"default":  0, "Азриель":  1},
    },
    "thoughtful": {
        "Оценить":     {"default":  0},
        "Вопрос":      {"default":  0},
        "Убеждение":   {"default":  0},
        "Рассказать":  {"default":  0},
        "Поддержать":  {"default":  1},
        "Играть":      {"default":  0},
        "Запугать":    {"default": -1},
        "Грубить":     {"default": -1},
        "Исполнение":  {"default":  0},
        "Дразнить":    {"default": -1},
        "Унижаться":   {"default":  1},
    },
    "tired": {
        "Оценить":     {"default":  0},
        "Вопрос":      {"default":  0},
        "Убеждение":   {"default":  0},
        "Рассказать":  {"default":  0},
        "Поддержать":  {"default":  1},
        "Играть":      {"default":  0},
        "Запугать":    {"default": -1},
        "Грубить":     {"default": -1},
        "Исполнение":  {"default":  0},
        "Дразнить":    {"default": -1},
        "Унижаться":   {"default":  1},
    },
    "happy": {
        "Оценить":     {"default":  0},
        "Вопрос":      {"default":  1},
        "Убеждение":   {"default": -1},
        "Рассказать":  {"default":  0, "Азриель": -1},
        "Поддержать":  {"default":  1, "Азриель":  0},
        "Играть":      {"default":  0, "Азриель": -1},
        "Запугать":    {"default": -1},
        "Грубить":     {"default": -1},
        "Исполнение":  {"default":  0},
        "Дразнить":    {"default": -1},
        "Унижаться":   {"default":  0, "Азриель":  1},
    },
}

init python:

    # Арчи: полное дерево переговоров. Имена действий совпадают с ACTS_CONFIG.
    archie_mood_tree = {
        "happy": {
            "Убеждение": {"difficulty": 2, "success": {"rollback": .5}, "failure": {"rollback": 1.0}},
            "Рассказать": {"difficulty": -2, "success": {"progress": 1.0}},
            "Поддержать": {"difficulty": -3, "success": {"progress": 1.0}},
            "Играть": {"difficulty": -1, "success": {"progress": 1.0}},
            "Запугать": {"difficulty": -3},
            "Грубить": {"difficulty": -1, "route": "taunt", "success": {"progress": 1.0, "atk": .10}, "failure": {"atk": .20}},
            "Исполнение": {"difficulty": 0},
            "Дразнить": {"difficulty": -2, "route": "taunt", "success": {"progress": 1.0, "atk": .06, "crit": .10}, "failure": {"atk": .10, "crit": .15}},
        },
        "neutral": {
            "Убеждение": {"difficulty": -3, "success": {"progress": 1.0}, "failure": {"atk": -.05}},
            "Рассказать": {"difficulty": -2},
            "Поддержать": {"difficulty": -2, "success": {"progress": 1.0}, "failure": {"atk": -.10}},
            "Играть": {"difficulty": 0},
            "Запугать": {"difficulty": -2, "success": {"rollback": .5}, "failure": {"rollback": 1.0}},
            "Грубить": {"difficulty": -1, "success": {"rollback": .5, "atk": .05}, "failure": {"rollback": 1.0, "atk": .10}},
            "Исполнение": {"difficulty": -1, "success": {"progress": 1.0, "critrate": .05}, "failure": {"critrate": .10}},
            "Дразнить": {"difficulty": 0},
        },
        "angry": {
            "Убеждение": {"difficulty": -2}, "Рассказать": {"difficulty": -2},
            "Поддержать": {"difficulty": -2, "success": {"rollback": .5, "def": 1}, "failure": {"rollback": 1.0, "def": 2}},
            "Играть": {"difficulty": -1, "success": {"rollback": .5, "speed": .05}, "failure": {"rollback": 1.0, "speed": .10}},
            "Запугать": {"difficulty": -3},
            "Грубить": {"difficulty": -1, "success": {"progress": 1.0, "atk": .10}, "failure": {"atk": .20}},
            "Исполнение": {"difficulty": 0},
            "Дразнить": {"difficulty": -2, "success": {"progress": 1.0, "atk": .10, "crit": .15}, "failure": {"atk": .15, "crit": .20}},
        },
    }

    def archie_apply_act(target, attacker, action_name, success):
        if target is None or getattr(target, "name", None) != "Арчи":
            return
        action_name = {"Убедить": "Убеждение", "Исполнить": "Исполнение"}.get(action_name, action_name)
        tree = archie_mood_tree.get(getattr(target, "mood", "happy"), {})
        spec = tree.get(action_name, {})
        result = spec.get("success" if success else "failure", {})
        # Пассивка «Думай, Крис!» иногда отменяет откат пощады.
        if (not success and getattr(target, "mood", "happy") == "neutral" and
                result.get("rollback") and renpy.random.random() <= 0.25):
            result = dict(result)
            result.pop("rollback", None)
            renpy.notify("Арчи закрыл глаза на ошибку! Штраф отменен.")
        diplomacy = int(getattr(attacker, "diplomacy", 0) or 0)
        if result.get("progress"):
            target.spare_progress = min(target.spare_max, target.spare_progress + diplomacy * int(getattr(store, "dip_multiply", 1) or 1))
        if result.get("rollback"):
            target.spare_progress = max(0, target.spare_progress - int(round(diplomacy * result["rollback"])))
        target.bonus_atk = target.bonus_atk + result.get("atk", 0)
        target.bonus_crit = target.bonus_crit + result.get("crit", 0)
        target.bonus_critrate = target.bonus_critrate + result.get("critrate", 0)
        target.bonus_def = target.bonus_def + result.get("def", 0)
        if result.get("speed"):
            target.speed = store.clamp_enemy_speed(target.speed + result["speed"]) if hasattr(store, "clamp_enemy_speed") else max(.5, min(1.5, target.speed + result["speed"]))
        if spec.get("route"):
            target.archie_taunt_actions = int(getattr(target, "archie_taunt_actions", 0)) + 1
        if action_name in ("Рассказать", "Поддержать", "Играть"):
            target.archie_peace_actions = int(getattr(target, "archie_peace_actions", 0)) + 1
        if getattr(target, "mood", "happy") == "happy" and not success:
            target.dc_offset = int(getattr(target, "dc_offset", 0)) - 1
        elif getattr(target, "mood", "happy") == "neutral" and success:
            if action_name in ("Убеждение", "Поддержать", "Исполнение") and getattr(attacker, "name", None) == "Крис":
                attacker.bonus_charm = getattr(attacker, "bonus_charm", 0) + 8
                renpy.notify("Крис получает +8% к очарованию!")
            elif action_name in ("Рассказать", "Играть", "Дразнить"):
                target.dc_offset = int(getattr(target, "dc_offset", 0)) - 1
                renpy.notify("Сложность бросков снижена на 1!")
        process_enemy_routes(target, action_name)

    def archie_difficulty(target, action_name):
        action_name = {"Убедить": "Убеждение", "Исполнить": "Исполнение"}.get(action_name, action_name)
        return archie_mood_tree.get(getattr(target, "mood", "happy"), {}).get(action_name, {}).get("difficulty", 0)

    def trevor_get_effect(enemy, action_name, attacker_name=None):
        if enemy is None or getattr(enemy, "name", None) != "Тревор":
            return 0
        route = getattr(enemy, "route", None)
        stage = getattr(enemy, "route_stage", 1)
        # Если Тревор на этапе 2 рута Умиротворения (порог 24, настроение neutral),
        # то Убеждение даёт негативный эффект (-1) для всех!
        if route == "peace" and stage >= 2:
            if action_name == "Убеждение":
                return -1
            if action_name in ("Запугать", "Грубить", "Дразнить"):
                return -1

        mood = getattr(enemy, "mood", "neutral")
        per_mood = trevor_act_effects.get(mood, {})
        per_action = per_mood.get(action_name, {})
        if attacker_name and attacker_name in per_action:
            return per_action[attacker_name]
        return per_action.get("default", 0)

    def trevor_mod_stat(enemy, stat_name, percent_delta):
        """Изменяет процентную характеристику врага Тревора."""
        if enemy is None:
            return
        if stat_name == "attack":
            cur = float(getattr(enemy, "bonus_atk2", 0.0) or 0.0)
            enemy.bonus_atk2 = max(-0.9, cur + percent_delta)
        elif stat_name == "critdmg":
            cur = float(getattr(enemy, "critdmg_debuff_var2", 0.0) or 0.0)
            enemy.critdmg_debuff_var2 = max(-0.5, cur + percent_delta)
        elif stat_name == "critrate":
            cur = float(getattr(enemy, "critrate_debuff_var2", 0.0) or 0.0)
            enemy.critrate_debuff_var2 = max(-0.5, cur + percent_delta)
        elif stat_name == "accuracy":
            cur = float(getattr(enemy, "accuracy_debuff_var2", 0.0) or 0.0)
            enemy.accuracy_debuff_var2 = max(-0.5, cur + percent_delta)
        elif stat_name == "speed":
            cur = float(getattr(enemy, "speed", 1.0) or 1.0)
            new_speed = cur * (1.0 + percent_delta)
            if hasattr(store, "clamp_enemy_speed"):
                enemy.speed = store.clamp_enemy_speed(new_speed)
            else:
                enemy.speed = max(0.5, min(1.5, new_speed))

    def trevor_mod_socialization(attacker_or_name, delta):
        """Изменяет бонус социализации атакующего персонажа."""
        attacker = _rollback_resolve_attacker(attacker_or_name)
        if attacker is None:
            return
        cur = getattr(attacker, "bonus_socialization", 0)
        attacker.bonus_socialization = cur + delta

    def trevor_rollback_spare(enemy, attacker_or_name, multiplier=0.5):
        """Откатывает прогресс пощады Тревора на multiplier * дипломатия атакующего."""
        attacker = _rollback_resolve_attacker(attacker_or_name)
        if attacker is None or enemy is None:
            return 0
        diplomacy = int(getattr(attacker, "diplomacy", 0) or 0)
        if diplomacy <= 0:
            return 0
        delta = int(round(diplomacy * multiplier))
        if delta <= 0:
            delta = 1
        old = int(getattr(enemy, "spare_progress", 0) or 0)
        effective_floor = 0
        new_val = max(effective_floor, old - delta)
        enemy.spare_progress = new_val
        return old - new_val

    def trevor_switch_to_peace_route(enemy):
        """Переключает Тревора на рут Умиротворения (при действии Поддержать в Соперничестве)."""
        if enemy is None or getattr(enemy, "name", None) != "Тревор":
            return
        enemy.route = "peace"
        spare_prog = int(getattr(enemy, "spare_progress", 0) or 0)
        if spare_prog >= 38:
            enemy.route_stage = 3
            set_enemy_mood(enemy, "thoughtful")
            renpy.notify("Тревор: смена рута на «Умиротворение» (этап 3, задумчивый)")
        elif spare_prog >= 24:
            enemy.route_stage = 2
            set_enemy_mood(enemy, "neutral")
            renpy.notify("Тревор: смена рута на «Умиротворение» (этап 2, нейтральный)")
        else:
            enemy.route_stage = 1
            set_enemy_mood(enemy, "neutral")
            renpy.notify("Тревор: смена рута на «Умиротворение»")

    def _rollback_resolve_attacker(attacker_or_name):
        if attacker_or_name is None:
            return None
        if hasattr(attacker_or_name, "diplomacy"):
            return attacker_or_name
        if isinstance(attacker_or_name, str):
            return getattr(store, "pers_dict", {}).get(attacker_or_name)
        return None

    def get_enemy_route_stage_floor(enemy):
        if enemy is None:
            return 0
        route = getattr(enemy, "route", None)
        stage = int(getattr(enemy, "route_stage", 1) or 1)
        if route is None or stage <= 1:
            return 0
        config = enemy_route_config.get(getattr(enemy, "name", None))
        if not config:
            return 0
        route_data = config.get("routes", {}).get(route)
        if not route_data:
            return 0
        stage_data = route_data.get("stages", {}).get(stage)
        if not stage_data:
            return 0
        return int(stage_data.get("threshold", 0))

    def rollback_spare_progress(attacker_or_name, target, multiplier=0.3):
        attacker = _rollback_resolve_attacker(attacker_or_name)
        if attacker is None or target is None:
            return 0
        diplomacy = int(getattr(attacker, "diplomacy", 0) or 0)
        if diplomacy <= 0:
            return 0
        delta = int(round(diplomacy * multiplier))
        if delta <= 0:
            return 0
        old = int(getattr(target, "spare_progress", 0) or 0)
        effective_floor = min(get_enemy_route_stage_floor(target), old)
        new_value = max(old - delta, effective_floor, 0)
        target.spare_progress = new_value
        return old - new_value

    def _resolve_attacker_obj(attacker_or_name):
        if attacker_or_name is None:
            return None
        if hasattr(attacker_or_name, "diplomacy"):
            return attacker_or_name
        if isinstance(attacker_or_name, str):
            return getattr(store, "pers_dict", {}).get(attacker_or_name)
        if isinstance(attacker_or_name, int):
            order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик"]
            if 1 <= attacker_or_name <= len(order):
                return getattr(store, "pers_dict", {}).get(order[attacker_or_name - 1])
        return None

    def _resolve_target_obj(target_or_name):
        if target_or_name is None:
            return None
        if hasattr(target_or_name, "spare_progress"):
            return target_or_name
        if isinstance(target_or_name, str):
            enemies = getattr(store, "enemies", {}) or {}
            if target_or_name in enemies:
                return enemies[target_or_name]
            return (getattr(store, "pers_dict", {}) or {}).get(target_or_name)
        return None

    def _sync_spare_max(enemy):
        config = enemy_route_config.get(getattr(enemy, "name", None), {})
        if "spare_max" in config:
            enemy.spare_max = int(config["spare_max"])

    def add_spare_progress(attacker, target, action_name, apply_effect=True):
        attacker_obj = _resolve_attacker_obj(attacker)
        target_obj = _resolve_target_obj(target)
        if attacker_obj is None or target_obj is None:
            return 0

        _sync_spare_max(target_obj)
        old_progress = int(getattr(target_obj, "spare_progress", 0) or 0)

        if apply_effect:
            apply_act_to_enemy(target_obj, action_name, True)

        diplomacy = int(getattr(attacker_obj, "diplomacy", 0) or 0)
        dip_multiply = int(getattr(store, "dip_multiply", 1) or 1)
        target_obj.spare_progress = min(
            target_obj.spare_progress + max(0, diplomacy) * dip_multiply,
            target_obj.spare_max
        )

        cfg = getattr(store, "ACTS_CONFIG", {}).get(action_name, {})
        progress_key = cfg.get("progress_key")
        if progress_key and progress_key in getattr(target_obj, "action_progress", {}):
            target_obj.action_progress[progress_key] += 1

        process_enemy_routes(target_obj, action_name)

        if action_name == "Оценить":
            revealed = reveal_random_acts_to_enemy(target_obj, 2)
            if revealed:
                renpy.notify("Осмотр выявил: " + ", ".join(revealed))

        if target_obj.spare_progress >= target_obj.spare_max:
            renpy.notify("%s готов(а) к пощаде!" % getattr(target_obj, "name", "?"))
        return int(target_obj.spare_progress - old_progress)

default enemy_route_config = {
    "Тревор": {
        "spare_max": 50,
        "routes": {
            "peace": {
                "name": "Умиротворение",
                "stages": {
                    2: {
                        "threshold": 24,
                        "entry_actions": {"Вопрос", "Поддержать", "Унижаться"},
                        "mood": "neutral",
                    },
                    3: {
                        "threshold": 38,
                        "entry_actions": {"Вопрос", "Поддержать", "Унижаться"},
                        "mood": "thoughtful",
                    },
                },
            },
            "rivalry": {
                "name": "Соперничество",
                "stages": {
                    2: {
                        "threshold": 18,
                        "entry_actions": {"Запугать", "Грубить", "Дразнить"},
                        "mood": "angry",
                    },
                    3: {
                        "threshold": 27,
                        "entry_actions": {"Запугать", "Грубить", "Дразнить"},
                        "mood": "happy",
                    },
                },
            },
        },
    },
}


init python:

    def get_enemy_spare_max(enemy):
        if getattr(enemy, "name", None) == "Тревор":
            return 50
        config = enemy_route_config.get(getattr(enemy, "name", None), {})
        return config.get("spare_max", getattr(enemy, "spare_max", 100))

    def ensure_enemy_route_fields(enemy):
        if "route" not in enemy.__dict__:
            enemy.route = None
        if "route_stage" not in enemy.__dict__:
            enemy.route_stage = 1

    def process_enemy_routes(enemy, action_name):
        if enemy is None:
            return

        ensure_enemy_route_fields(enemy)

        if getattr(enemy, "name", None) == "Арчи":
            peace = int(getattr(enemy, "archie_peace_actions", 0))
            taunt = int(getattr(enemy, "archie_taunt_actions", 0))
            if enemy.route is None and enemy.spare_progress >= 12 and peace > taunt:
                enemy.route, enemy.route_stage = "peace", 2
                set_enemy_mood(enemy, "neutral")
                renpy.notify("Арчи: рут «Мирный», настроение «Нейтральный».")
            elif enemy.route is None and enemy.spare_progress >= 19 and taunt > peace:
                enemy.route, enemy.route_stage = "taunt", 2
                set_enemy_mood(enemy, "angry")
                renpy.notify("Арчи: рут «Дразнилки», настроение «Злой».")
            return

        config = enemy_route_config.get(getattr(enemy, "name", None))
        if not config:
            return

        enemy.spare_max = get_enemy_spare_max(enemy)
        spare_progress = int(getattr(enemy, "spare_progress", 0))
        routes = config.get("routes", {})

        if enemy.route is None:
            for route_key, route_data in routes.items():
                stage2 = route_data.get("stages", {}).get(2)
                if (stage2 and spare_progress >= stage2["threshold"]
                        and action_name in stage2["entry_actions"]):
                    enemy.route = route_key
                    enemy.route_stage = 2
                    enemy.spare_max = get_enemy_spare_max(enemy)
                    set_enemy_mood(enemy, stage2["mood"])
                    renpy.notify("%s: рут «%s», этап 2." % (enemy.name, route_data["name"]))
                    return
            return

        route_data = routes.get(enemy.route)
        if enemy.route_stage != 2 or not route_data:
            return
        stage3 = route_data.get("stages", {}).get(3)
        advances_without_entry_action = (
            getattr(enemy, "name", None) == "Тревор" and enemy.route == "peace"
        )
        if (stage3 and spare_progress >= stage3["threshold"]
                and (advances_without_entry_action or action_name in stage3["entry_actions"])):
            enemy.route_stage = 3
            set_enemy_mood(enemy, stage3["mood"])
            renpy.notify("%s: этап 3 рута «%s»." % (enemy.name, route_data["name"]))
