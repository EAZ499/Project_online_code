default xp = 0
# XP за конкретную битву.
default future_xp = 0
default pending_xp_to_apply = 0

default battle_enemy_statuses = {}
default battle_fully_resolved = False
default xp_animation_finished = False
default kris_bad_way_completed = False

init python:
    MAX_GLOBAL_LEVEL = 10

    def get_xp_for_next_level(current_level):
        """XP, нужный для перехода с current_level на следующий. На 10 уровне рост останавливается."""
        if current_level >= MAX_GLOBAL_LEVEL:
            return None
        return current_level * 90

    def sync_owner_lvl_xp(owner):
        """Синхронизирует owner.lvl_xp с текущим глобальным уровнем."""
        if owner is None:
            return
        required_xp = get_xp_for_next_level(Pers.global_level)
        owner.lvl_xp = 0 if required_xp is None else required_xp

    def _active_enemy_names():
        """Возвращает список активных врагов для текущего battlenumber."""
        if 'get_active_enemies' in globals():
            try:
                return list(get_active_enemies())
            except Exception:
                pass

        # Fallback, если get_active_enemies ещё не загружен.
        mapping = {
            1: ["Арчи"],
            2: ["Тревор"],
            3: ["ДжевилV1"],
            4: ["Психолог"],
            5: ["Спамтон"],
            10: ["Арчи", "Тревор", "ДжевилV1", "Психолог"],
            11: ["dummy"],
            13: ["dummy2"],
        }
        return mapping.get(store.battlenumber, [])

    def _active_enemy_objects():
        """Список активных enemy-объектов."""
        result = []
        if not hasattr(store, 'enemies') or not isinstance(store.enemies, dict):
            return result

        for enemy_name in _active_enemy_names():
            enemy_obj = store.enemies.get(enemy_name)
            if enemy_obj is not None:
                result.append(enemy_obj)
        return result

    def get_main_xp_owner():
        """Единый объект персонажа, в котором хранится xp (одна переменная)."""
        if hasattr(store, 'pers_dict') and isinstance(store.pers_dict, dict):
            if "Крис" in store.pers_dict:
                return store.pers_dict["Крис"]
            for p in store.pers_dict.values():
                return p
        return None

    def update_enemy_resolution_flags():
        """Обновляет флаги spared/dead у врагов по их текущему состоянию."""
        for enemy in _active_enemy_objects():
            # Пощажённый враг: либо уже есть флаг, либо набран spare_progress.
            if getattr(enemy, 'spared', False) or getattr(enemy, 'spare_progress', 0) >= getattr(enemy, 'spare_max', 100):
                enemy.spared = True

            # Мёртвый враг определяется по HP.
            enemy.dead = enemy.current_hp <= 0

    def is_battle_resolved():
        """Битва завершена, если каждый враг либо убит, либо пощажён."""
        enemies = _active_enemy_objects()
        if not enemies:
            return False

        update_enemy_resolution_flags()
        return all(enemy.dead or enemy.spared for enemy in enemies)

    def calculate_future_xp():
        """Общий XP за бой: сумма xp всех активных врагов."""
        total = 0
        for enemy in _active_enemy_objects():
            total += int(getattr(enemy, 'xp', 0))
        return max(0, total)

    def reset_active_enemies_for_new_battle():
        """Сбрасывает состояние активных врагов перед стартом нового боя."""
        for enemy in _active_enemy_objects():
            enemy.current_hp = enemy.max_hp
            enemy.spared = False
            enemy.dead = False
            enemy.spare_progress = 0

            # Сбрасываем прогресс ACT-действий (если словарь уже создан).
            if hasattr(enemy, 'action_progress') and isinstance(enemy.action_progress, dict):
                for key in enemy.action_progress:
                    enemy.action_progress[key] = 0

    def prepare_post_battle_xp():
        """Готовит значения опыта перед экраном после боя."""
        store.future_xp = calculate_future_xp()
        store.pending_xp_to_apply = store.future_xp
        store.xp_animation_finished = False
        sync_owner_lvl_xp(get_main_xp_owner())

    def apply_xp_step(step=1):
        """Пошаговое начисление XP для экрана после боя."""
        owner = get_main_xp_owner()
        if owner is None:
            store.xp_animation_finished = True
            return

        if store.pending_xp_to_apply <= 0:
            store.xp_animation_finished = True
            return

        gain = min(int(step), int(store.pending_xp_to_apply))
        owner.xp += gain
        store.pending_xp_to_apply -= gain

        sync_owner_lvl_xp(owner)

        # Левел-ап: на 10 уровне прогресс по уровням останавливается.
        while owner.lvl_xp > 0 and owner.xp >= owner.lvl_xp:
            owner.xp -= owner.lvl_xp
            owner.set_level(owner.level + 1)
            sync_owner_lvl_xp(owner)

            # Как только достигнут 10 уровень — прерываем дальнейшие расчёты анимации опыта.
            if Pers.global_level >= MAX_GLOBAL_LEVEL:
                store.pending_xp_to_apply = 0
                store.xp_animation_finished = True
                return

        store.xp_animation_finished = store.pending_xp_to_apply <= 0

    def _battle_enemy_objects_by_number(battle_number=None):
        """Словарь врагов текущей битвы, привязанный к battlenumber."""
        bn = store.battlenumber if battle_number is None else battle_number

        # Временная подмена для повторного использования _active_enemy_names
        original_bn = store.battlenumber
        store.battlenumber = bn
        names = _active_enemy_names()
        store.battlenumber = original_bn

        result = {}
        if hasattr(store, 'enemies') and isinstance(store.enemies, dict):
            for name in names:
                if name in store.enemies:
                    result[name] = store.enemies[name]
        return result

    def bad_way():
        """
        Проверяет «плохой путь»:
        - создаёт словарь объектов врагов по battlenumber,
        - если у врага current_hp == 0, помечает его dead,
        - возвращает True, когда все враги в этом словаре имеют статус dead.
        """
        enemies_by_battle = _battle_enemy_objects_by_number(store.battlenumber)
        store.battle_enemy_statuses[store.battlenumber] = {}

        for enemy_name, enemy in enemies_by_battle.items():
            enemy.dead = enemy.current_hp <= 0
            store.battle_enemy_statuses[store.battlenumber][enemy_name] = "dead" if enemy.dead else "alive"

        statuses = store.battle_enemy_statuses[store.battlenumber].values()
        return bool(statuses) and all(status == "dead" for status in statuses)

    def reset_zero_hp_bonus_stats(char):
        """Сбрасывает бонусы и только отрицательные дебаффы у бойца с 0 HP."""
        if char is None or getattr(char, "current_hp", 0) > 0:
            return

        # Павший участник связи «Позвать за щит» не должен оставлять
        # партнёру бонус защиты.
        clear_kris_shield_link(char)

        hero_bonus_defaults = {
            "bonus_atk": 1.0,
            "bonus_magic": 1.0,
            "bonus_def": 1.0,
            "bonus_crit": 0.0,
            "bonus_critrate": 0.0,
            "bonus_dmgchance": 0.0,
            "bonus_tank": 0.0,
            "bonus_perform": 0.0,
            "bonus_socialization": 0.0,
            "bonus_diplomacy": 0.0,
            "bonus_charm": 0.0,
            "bonus_perception": 0.0,
            "bonus_rhetoric": 0.0,
            "bonus_artistry": 0.0,
            "bonus_comfort": 0.0,
            "bonus_power": 0.0,
        }
        enemy_bonus_defaults = {
            "bonus_atk": 1.0,
            "bonus_magic": 1.0,
            "bonus_def": 1.0,
            "bonus_magic_armor": 0.0,
            "bonus_crit": 0.0,
            "bonus_critrate": 0.0,
            "bonus_dmgchance": 0.0,
            "bonus_tank": 0.0,
            "bonus_perform": 1.0,
        }
        enemy_debuff_var_defaults = {
            "atk_debuff_var2": 1.0,
            "def_debuff_var2": 1.0,
            "magic_debuff_var2": 1.0,
            "accuracy_debuff_var2": 0.0,
            "critrate_debuff_var2": 0.0,
            "critdmg_debuff_var2": 0.0,
        }
        negative_counter_defaults = {
            "bloodshed_debuff": 0,
            "prone_debuff": 0,
            "atk_debuff": 0,
            "def_debuff": 0,
            "magic_debuff": 0,
            "accuracy_debuff": 0,
            "critrate_debuff": 0,
            "critdmg_debuff": 0,
            "tank_debuff": 0,
        }
        negative_indicator_defaults = {
            "bloodshed_debuff_got": 0,
            "prone_debuff_got": 0,
            "atk_debuff_got": 0,
            "def_debuff_got": 0,
            "magic_debuff_got": 0,
            "accuracy_debuff_got": 0,
            "critrate_debuff_got": 0,
            "critdmg_debuff_got": 0,
            "tank_debuff_got": 0,
            "overheal_debuff_got": 0,
            "overcritrate_debuff_indic": 0,
            "overdmgrate_debuff_indic": 0,
        }
        is_hero = hasattr(char, "bonus_socialization")
        stat_defaults = hero_bonus_defaults if is_hero else enemy_bonus_defaults

        # Для мёртвого героя bloodshed всегда полностью сбрасывается.
        if is_hero and hasattr(char, "bloodshed_debuff"):
            char.bloodshed_debuff = 0

        for stat_name, default_value in stat_defaults.items():
            if hasattr(char, stat_name):
                setattr(char, stat_name, default_value)

        for stat_name, default_value in negative_counter_defaults.items():
            if hasattr(char, stat_name) and getattr(char, stat_name) < 0:
                setattr(char, stat_name, default_value)

        for stat_name, default_value in negative_indicator_defaults.items():
            if hasattr(char, stat_name) and getattr(char, stat_name) < 0:
                setattr(char, stat_name, default_value)

        if not is_hero:
            for stat_name, default_value in enemy_debuff_var_defaults.items():
                if hasattr(char, stat_name) and getattr(char, stat_name) < default_value:
                    setattr(char, stat_name, default_value)







screen check_enemy_status:
    for char in store.pers_dict.values():
        if char.current_hp <= 0:
            timer 0.01 action Function(reset_zero_hp_bonus_stats, char)

    for enemy in _active_enemy_objects():
        if enemy.current_hp <= 0:
            timer 0.01 action Function(reset_zero_hp_bonus_stats, enemy)
    # Проверяем завершение боя (все враги либо убиты, либо пощажены).
    timer 0.5 repeat True action [
        Function(update_enemy_resolution_flags),
        SetVariable("battle_fully_resolved", is_battle_resolved())
    ]

    if battle_fully_resolved:
        timer 0.5 action Jump("after_fight")

    # Game over, если все выбранные персонажи мертвы.
    if all((char.picked == 0 or char.current_hp <= 0) for char in store.pers_dict.values()):
        timer 0.02 action Jump("game_over")


screen post_battle_xp_screen():
    modal True
    zorder 100

    # Плавное начисление опыта.
    if not xp_animation_finished:
        timer 0.03 repeat True action Function(apply_xp_step, 1)

    if Pers.global_level >= MAX_GLOBAL_LEVEL:
        timer 0.05 action Return()

    add Solid("#000000CC")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        ysize 360
        background Solid("#1B1B1BE6")
        padding (35, 30)

        vbox:
            spacing 18
            xfill True

            $ owner = get_main_xp_owner()

            text "ОПЫТ ПОСЛЕ БОЯ" size 46 xalign 0.5
            text "Получено за бой: [future_xp]" size 34 xalign 0.5
            #text "Гено: [bad_way]"
            $ geno_route = bad_way()
            text "Гено: [\"Да\" if geno_route else \"Нет\"]" size 30 xalign 0.5

            #text "Уровень: [owner.level]"

            if owner is not None:
                if Pers.global_level >= MAX_GLOBAL_LEVEL:
                    text "Уровень: макс.ур." size 30 xalign 0.5
                else:
                    text "Уровень: [Pers.global_level]" size 30 xalign 0.5
                    text "Текущий опыт: [owner.xp] / [owner.lvl_xp]" size 30 xalign 0.5
                    bar:
                        xalign 0.5
                        xmaximum 620
                        value AnimatedValue(value=owner.xp, range=max(1, owner.lvl_xp), delay=0.08)

            if xp_animation_finished:
                textbutton "Продолжить":
                    xalign 0.5
                    text_size 34
                    action Return()
            else:
                text "Начисление опыта..." size 28 xalign 0.5











label after_fight:
    # Подготовка данных опыта для экрана после боя.
    $ prepare_post_battle_xp()

    call screen post_battle_xp_screen()

    # После завершения начисления можно проверить bad_way().
    if bad_way():
        $ kris_bad_way_completed = True
        $ renpy.notify("BAD WAY: все враги в текущей битве мертвы.")

    hide screen team_status_display
    hide screen Heroattacks
    hide screen targettochoose_sprites
    hide screen check_enemy_status

    # Бой окончен — снимаем связь «Позвать за щит» и её бонус защиты.
    $ clear_all_kris_shield_links()

    $ current_attacker = None
    $ selected_targets = []
    $ target = None
    $ actionid = None

    # Возвращаем всех персонажей в исходную позицию перед началом боя.
    python:
        for _char in store.pers_dict.values():
            _char.step_forward = 0

    # Сбрасываем состояние кнопок перед началом нового хода персонажа,
    # чтобы не оставались экраны прошлой анимации (например atob/abackdis).
    $ fightchoice = 0
    $ actchoice = 0
    $ magicchoice = 0
    $ itemchoice = 0

    hide screen choose_attack_screen
    hide screen actchoice1
    hide screen choose_magic_screen
    hide screen itemchoice2

    hide screen ftoc
    hide screen atoc
    hide screen mtoc
    hide screen itoc

    hide screen ftob
    hide screen atob
    hide screen mtob
    hide screen itob

    hide screen fbackapp
    hide screen abackapp
    hide screen mbackapp
    hide screen ibackapp

    hide screen fbackdis
    hide screen abackdis
    hide screen mbackdis
    hide screen ibackdis

    #call

    call screen game_screen()
    #return
