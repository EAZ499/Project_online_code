# 1_ВРАГ_МАНЕКЕН.rpy
# Пассивки врага «Манекен» (dummy)

init python:
    # ------------------------------------------------------------
    # ПАССИВКА «ЭТО ПРОСТО МАНЕКЕН» — без изменений
    # ------------------------------------------------------------
    DUMMY_BOREDOM_CHANCE = 0.20
    DUMMY_BOREDOM_STACKS = 3
    DUMMY_SEAM_DEF_LOSS = 0.10

    # ------------------------------------------------------------
    # РУТ МАНЕКЕНА
    # ------------------------------------------------------------
    # Стартовое настроение — «neutral» (в отличие от Арчи, у которого
    # старт «happy»). Мирные действия при накоплении пощады >= 12
    # переводят в «happy», агрессивные при >= 19 — в «angry».
    #
    # Успех/провал действия двигает spare_progress на «дипломатия
    # атакующего * dip_multiply» (для progress) или откатывает на
    # «дипломатия * rollback» (для rollback). Бонусы atk/crit/critrate/
    # def/speed идут напрямую в bonus_atk/bonus_crit/bonus_critrate/
    # bonus_def/speed врага. Поле route в спеке означает, что успешное
    # действие этого типа учитывается в счётчике taunt_actions
    # (для агрессивных) и в счётчике peace_actions (для мирных).

    DUMMY_PEACE_THRESHOLD = 12
    DUMMY_TAUNT_THRESHOLD = 19

    # Действия, повышающие «мирный» счётчик.
    DUMMY_PEACE_ACTIONS = {"Рассказать", "Поддержать", "Играть"}

    # Действия, повышающие «дразнящий» счётчик.
    DUMMY_TAUNT_ACTIONS = {"Грубить", "Дразнить"}

    dummy_mood_tree = {
        # --------------------------------------------------------
        # НЕЙТРАЛЬНОЕ — стартовое
        # --------------------------------------------------------
        "neutral": {
            "Оценить":    {"difficulty": -5},
            "Вопрос":     {"difficulty": -5},
            "Убеждение":  {"difficulty": -3, "success": {"progress": 1.0},
                            "failure": {"atk": -.05}},
            "Рассказать": {"difficulty": -2},
            "Поддержать": {"difficulty": -2, "success": {"progress": 1.0},
                            "failure": {"atk": -.10}},
            "Играть":     {"difficulty": 0},
            "Запугать":   {"difficulty": -2, "success": {"rollback": .5},
                            "failure": {"rollback": 1.0}},
            "Грубить":    {"difficulty": -1, "success": {"rollback": .5, "atk": .05},
                            "failure": {"rollback": 1.0, "atk": .10}},
            "Исполнение": {"difficulty": -1, "success": {"progress": 1.0, "critrate": .05},
                            "failure": {"critrate": .10}},
            "Дразнить":   {"difficulty": 0},
            "Унижаться":  {"difficulty": 0, "success": {"progress": 1.0}},
        },
        # --------------------------------------------------------
        # ВЕСЁЛОЕ — мирный рут (порог 12)
        # --------------------------------------------------------
        "happy": {
            "Оценить":    {"difficulty": -5},
            "Вопрос":     {"difficulty": -5},
            "Убеждение":  {"difficulty": 2, "success": {"rollback": .5},
                            "failure": {"rollback": 1.0}},
            "Рассказать": {"difficulty": -2, "success": {"progress": 1.0}},
            "Поддержать": {"difficulty": -3, "success": {"progress": 1.0}},
            "Играть":     {"difficulty": -1, "success": {"progress": 1.0}},
            "Запугать":   {"difficulty": -3},
            "Грубить":    {"difficulty": -1, "route": "taunt",
                            "success": {"progress": 1.0, "atk": .10},
                            "failure": {"atk": .20}},
            "Исполнение": {"difficulty": 0},
            "Дразнить":   {"difficulty": -2, "route": "taunt",
                            "success": {"progress": 1.0, "atk": .06, "crit": .10},
                            "failure": {"atk": .10, "crit": .15}},
            "Унижаться":  {"difficulty": 0},
        },
        # --------------------------------------------------------
        # ЗЛОЕ — рут Дразнилки (порог 19)
        # --------------------------------------------------------
        "angry": {
            "Оценить":    {"difficulty": -5},
            "Вопрос":     {"difficulty": -5},
            "Убеждение":  {"difficulty": -2},
            "Рассказать": {"difficulty": -2},
            "Поддержать": {"difficulty": -2, "success": {"rollback": .5, "def": 1},
                            "failure": {"rollback": 1.0, "def": 2}},
            "Играть":     {"difficulty": -1, "success": {"rollback": .5, "speed": .05},
                            "failure": {"rollback": 1.0, "speed": .10}},
            "Запугать":   {"difficulty": -3},
            "Грубить":    {"difficulty": -1, "success": {"progress": 1.0, "atk": .10},
                            "failure": {"atk": .20}},
            "Исполнение": {"difficulty": 0},
            "Дразнить":   {"difficulty": -2, "success": {"progress": 1.0, "atk": .10, "crit": .15},
                            "failure": {"atk": .15, "crit": .20}},
            "Унижаться":  {"difficulty": 0},
        },
    }

    def dummy_difficulty(target, action_name):
        """Сложность действия по текущему настроению манекена."""
        if target is None:
            return 0
        action_name = {"Убедить": "Убеждение", "Исполнить": "Исполнение"}.get(action_name, action_name)
        mood = getattr(target, "mood", "neutral")
        return dummy_mood_tree.get(mood, {}).get(action_name, {}).get("difficulty", -5)

    def dummy_apply_act(target, attacker, action_name, success):
        """Применяет успех/провал действия к манекену.

        Вся механика рута (spare_progress, откаты, бонусы, счётчики
        peace/taunt и переходы между настроениями) делается ЗДЕСЬ.
        Поэтому в get_act_spare_effect() манекен должен возвращать 0,
        чтобы apply_act_to_enemy() не накладывал spare_progress второй раз.
        """
        if target is None:
            return
        if not (getattr(target, "nameeng", None) == "dummy"
                or getattr(target, "name", None) == "Манекен"):
            return

        action_name = {"Убедить": "Убеждение", "Исполнить": "Исполнение"}.get(action_name, action_name)
        mood = getattr(target, "mood", "neutral")
        spec = dummy_mood_tree.get(mood, {}).get(action_name, {})
        result = spec.get("success" if success else "failure", {})

        diplomacy = int(getattr(attacker, "diplomacy", 0) or 0)
        dip_mult = int(getattr(store, "dip_multiply", 1) or 1)

        if result.get("progress"):
            target.spare_progress = min(
                int(getattr(target, "spare_max", 100)),
                int(getattr(target, "spare_progress", 0)) + diplomacy * dip_mult,
            )
        if result.get("rollback"):
            target.spare_progress = max(
                0,
                int(getattr(target, "spare_progress", 0))
                - int(round(diplomacy * result["rollback"])),
            )

        target.bonus_atk       = float(getattr(target, "bonus_atk", 0.0))       + result.get("atk", 0.0)
        target.bonus_crit      = float(getattr(target, "bonus_crit", 0.0))      + result.get("crit", 0.0)
        target.bonus_critrate  = float(getattr(target, "bonus_critrate", 0.0))  + result.get("critrate", 0.0)
        target.bonus_def       = float(getattr(target, "bonus_def", 0.0))       + result.get("def", 0.0)
        if result.get("speed"):
            new_speed = float(getattr(target, "speed", 1.0)) + result["speed"]
            target.speed = store.clamp_enemy_speed(new_speed) if hasattr(store, "clamp_enemy_speed") else max(.5, min(1.5, new_speed))

        # Счётчики для перехода между рутами.
        if action_name in DUMMY_PEACE_ACTIONS:
            target.dummy_peace_actions = int(getattr(target, "dummy_peace_actions", 0)) + 1
        if action_name in DUMMY_TAUNT_ACTIONS or spec.get("route") == "taunt":
            target.dummy_taunt_actions = int(getattr(target, "dummy_taunt_actions", 0)) + 1

        # Переход между рутами — общая функция из 0.0_РУТЫ_ВРАГОВ.rpy.
        if "process_enemy_routes" in globals():
            process_enemy_routes(target, action_name)

    def dummy_is_maneken(enemy):
        """Строгая проверка именно основного Манекена, не dummy2."""
        return (
            enemy is not None
            and getattr(enemy, "name", None) == "Манекен"
            and getattr(enemy, "nameeng", None) == "dummy"
        )

    def dummy_active_enemy():
        """Возвращает живого Манекена, если он участвует в текущем бою.

        Fallback на store.enemies.get("dummy") убран: он возвращал манекена
        и в тех боях, где манекен не участвует, из-за чего пассивка
        «Это просто манекен» накладывала Усталость/Безразличие героям
        в каждом раунде любого боя.
        """
        if "get_active_enemies" not in globals():
            return None
        enemies = getattr(store, "enemies", {}) or {}
        for key in get_active_enemies():
            enemy = enemies.get(key)
            if dummy_is_maneken(enemy) and getattr(enemy, "current_hp", 0) > 0:
                return enemy
        return None

    def dummy_find_enemy_by_display_name(name):
        """Ищет активного врага по отображаемому имени."""
        enemies = getattr(store, "enemies", {}) or {}
        keys = get_active_enemies() if "get_active_enemies" in globals() else list(enemies.keys())

        for key in keys:
            enemy = enemies.get(key)
            if enemy is not None and getattr(enemy, "name", None) == name:
                return enemy

        return None

    def dummy_prevent_bleeding(enemy):
        """«Бескровный, безмагии»: манекен не получает кровотечение."""
        if not dummy_is_maneken(enemy):
            return False

        enemy.bloodshed_debuff = 0
        enemy.bloodshed_debuff_got = 0
        return True

    def dummy_on_crit(target_name):
        """«Рвущиеся швы»: крит по манекену снижает бонусную защиту на 10%."""
        enemy = dummy_find_enemy_by_display_name(target_name)
        if not dummy_is_maneken(enemy):
            return

        # Для Enemy bonus_def — коэффициент в armor:
        # armor = base_def * bonus_def + ...
        # Поэтому -0.10 реально снижает защиту.
        enemy.bonus_def = float(getattr(enemy, "bonus_def", 0.0) or 0.0) - DUMMY_SEAM_DEF_LOSS

        renpy.log(
            "[Манекен][Рвущиеся швы] bonus_def теперь {}".format(
                enemy.bonus_def
            )
        )

    def dummy_apply_boredom():
        """«Это просто манекен»: 20% шанс каждому герою получить Усталость x3 и Безразличие x3."""
        if dummy_active_enemy() is None:
            return

        pers = getattr(store, "pers_dict", {}) or {}

        for char in pers.values():
            if getattr(char, "picked", 0) != 1:
                continue
            if getattr(char, "current_hp", 0) <= 0:
                continue

            if renpy.random.random() >= DUMMY_BOREDOM_CHANCE:
                continue

            # Усталость = положительный atk_debuff
            char.debuff("atk", DUMMY_BOREDOM_STACKS)

            # Безразличие = положительный critdmg_debuff
            char.debuff("critdmg", DUMMY_BOREDOM_STACKS)

            renpy.notify(
                "Манекен навеял скуку: {} получает Усталость x3 и Безразличие x3".format(
                    getattr(char, "name", "?")
                )
            )
