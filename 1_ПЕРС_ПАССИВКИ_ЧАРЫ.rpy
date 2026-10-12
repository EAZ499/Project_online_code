# Пассивные способности и улучшения Чары.
# Все временные счётчики хранятся в store и сбрасываются в начале боя.

default chara_world_destroyer_chance = 0.01
default chara_misses = 0
default chara_next_attack_damage = 0.0
default chara_next_attack_crit_damage = 0.0
default chara_flesh_edge_penalty = 0.0

init python:
    CHARA_WORLD_DESTROYER_MAX = 0.10

    def chara_level():
        char = (getattr(store, "pers_dict", {}) or {}).get("Чара")
        return max(1, int(getattr(char, "level", 1) or 1)) if char else 1

    def chara_is_active():
        char = (getattr(store, "pers_dict", {}) or {}).get("Чара")
        return char is not None and getattr(char, "current_hp", 0) > 0

    def chara_reset_battle_passives():
        store.chara_misses = 0
        store.chara_next_attack_damage = 0.0
        store.chara_next_attack_crit_damage = 0.0
        store.chara_flesh_edge_penalty = 0.0
        store.chara_world_destroyer_chance = 0.01

    def chara_on_attack_result(hit, target=None, attack_name=None):
        """Обрабатывает промахи/попадания и одноразовые усиления атак."""
        if not chara_is_active():
            return
        level = chara_level()
        if not hit:
            store.chara_misses = int(getattr(store, "chara_misses", 0)) + 1
            # «Не двигайся!» и «Попался!» — только после открытия улучшений.
            if level >= 1:
                store.chara_next_attack_damage += 0.05
                store.chara_next_attack_crit_damage += 0.05
            return
        store.chara_misses = 0
        store.chara_next_attack_damage = 0.0
        store.chara_next_attack_crit_damage = 0.0
        # Базовый прогресс «Разрушителя миров» сохраняется только в бою;
        # его постоянное сохранение будет добавлено отдельным persistent-полем.
        store.chara_world_destroyer_chance = min(
            CHARA_WORLD_DESTROYER_MAX,
            float(getattr(store, "chara_world_destroyer_chance", 0.01)) + 0.002
        )

    def chara_prepare_next_attack(char):
        """Применяет одноразовый бонус «Псих» непосредственно к удару."""
        multiplier = float(getattr(char, "next_attack_damage_multiplier", 1.0) or 1.0)
        if multiplier != 1.0:
            char.bonus_atk *= multiplier
            char.next_attack_damage_multiplier = 1.0
            return multiplier
        return 1.0

    def chara_attack_bonus_damage():
        return float(getattr(store, "chara_next_attack_damage", 0.0) or 0.0)

    def chara_try_world_destroyer():
        chance = float(getattr(store, "chara_world_destroyer_chance", 0.01) or 0.01)
        if renpy.random.random() < chance:
            return True
        return False

    def chara_on_round_end():
        """Конец раунда: кровотечения и «Прекрасные алые виды»."""
        if not chara_is_active():
            return
        enemies = getattr(store, "enemies", {}) or {}
        total_bleeding = sum(max(0, int(getattr(e, "bloodshed_debuff", 0) or 0))
                             for e in enemies.values() if getattr(e, "current_hp", 0) > 0)
        char = store.pers_dict["Чара"]
        if chara_level() >= 5 and total_bleeding:
            char.current_mp = min(char.max_mp, char.current_mp + int(total_bleeding * char.max_mp * 0.01))
            char.bonus_crit += total_bleeding * 0.005
        # «Кровавые реки»: шанс удвоения следующего тика кровотечения.
        for enemy in enemies.values():
            if getattr(enemy, "current_hp", 0) > 0 and renpy.random.random() < 0.30:
                enemy.chara_double_bleeding = True
