# ============================================================================
# ПАССИВКИ АРЧИ-ВРАГА (бой 1)
# ============================================================================

init python:
    def init_archie_battle_state(archie):
        if archie is None:
            return
        archie.mood = getattr(archie, "mood", "happy")
        archie.reaction_mode = "dodge"
        archie.down_turns = 0
        archie.was_missed_this_round = False
        archie.warmup_stacks = 0
        archie.dc_offset = 0
        archie.archie_passive_round = -1
        archie._archie_damage_guard = False

    def archie_enemy():
        # Пассивки Арчи работают только в его бою.
        if getattr(store, "battlenumber", 0) != 1:
            return None
        archie = (getattr(store, "enemies", {}) or {}).get("Арчи")
        if archie is not None and not hasattr(archie, "reaction_mode"):
            init_archie_battle_state(archie)
        return archie

    def archie_check_enemy_damage(archie, attacker, incoming_damage):
        if archie is None or incoming_damage <= 0:
            return incoming_damage
        if renpy.random.random() > float(getattr(archie, "critrate", 0.20)):
            return incoming_damage
        if getattr(archie, "reaction_mode", "dodge") == "dodge":
            archie.reaction_mode = "counter"
            renpy.notify("Арчи: Уворот!")
            return 0
        archie.reaction_mode = "dodge"
        if attacker is not None and getattr(attacker, "current_hp", 0) > 0:
            counter_dmg = max(1, int(float(getattr(archie, "atk", getattr(archie, "attack", 0))) * 0.75))
            attacker.current_hp = max(0, attacker.current_hp - counter_dmg)
            renpy.notify("Арчи: Контрудар! ({0} урона)".format(counter_dmg))
        return incoming_damage

    def archie_enemy_damage_hook(archie, old_hp, new_hp):
        if archie is None or getattr(archie, "name", None) != "Арчи":
            return new_hp
        incoming = max(0, int(old_hp - new_hp))
        if incoming <= 0 or getattr(archie, "_archie_damage_guard", False):
            return new_hp
        names = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"]
        current = getattr(store, "current_attacker", None)
        attacker = None
        if isinstance(current, int) and 0 < current <= len(names):
            attacker = (getattr(store, "pers_dict", {}) or {}).get(names[current - 1])
        return max(0, int(old_hp - archie_check_enemy_damage(archie, attacker, incoming)))

    def archie_mark_enemy_miss(target):
        if target is None or getattr(target, "name", None) != "Арчи":
            return
        target.was_missed_this_round = True
        if getattr(store, "current_attacker", None) == 1:
            kris = (getattr(store, "pers_dict", {}) or {}).get("Крис")
            if kris is not None and getattr(target, "mood", "happy") in ("happy", "cheerful"):
                kris.bonus_dmgchance = getattr(kris, "bonus_dmgchance", 0.0) + 0.04

    def archie_check_enemy_stand_up(archie):
        if getattr(archie, "prone_debuff", 0) <= 0:
            archie.down_turns = 0
            return
        archie.down_turns = int(getattr(archie, "down_turns", 0)) + 1
        if renpy.random.random() <= min(1.0, archie.down_turns * 0.20):
            archie.prone_debuff = 0
            archie.down_turns = 0
            renpy.notify("Арчи поднимается на ноги!")

    def archie_apply_enemy_breathing(archie):
        if getattr(archie, "was_missed_this_round", False):
            heal = max(1, int(float(archie.max_hp) * 0.05))
            archie.current_hp = min(archie.max_hp, archie.current_hp + heal)
            archie.was_missed_this_round = False
            renpy.notify("Правильное дыхание: Арчи восстановил {0} HP!".format(heal))

    def archie_enemy_attack_phase_hook():
        if getattr(store, "battlenumber", 0) != 1:
            return
        archie = archie_enemy()
        if archie is None or getattr(archie, "mood", "happy") != "angry":
            return
        round_no = int(getattr(store, "current_round", 0))
        if getattr(archie, "archie_passive_round", -1) == round_no:
            return
        archie.archie_passive_round = round_no
        if renpy.random.random() <= 0.20:
            kris = (getattr(store, "pers_dict", {}) or {}).get("Крис")
            if kris is not None and getattr(kris, "current_hp", 0) > 0:
                dmg = max(1, int(float(getattr(archie, "atk", getattr(archie, "attack", 0))) * 0.5))
                kris.current_hp = max(0, kris.current_hp - dmg)
                renpy.notify("Внезапный удар Арчи! Крис получает {0} урона.".format(dmg))

    def archie_on_battle_round_tick():
        archie = archie_enemy()
        if archie is None or getattr(archie, "current_hp", 0) <= 0:
            return
        archie_check_enemy_stand_up(archie)
        archie_apply_enemy_breathing(archie)
        kris = (getattr(store, "pers_dict", {}) or {}).get("Крис")
        mood = getattr(archie, "mood", "happy")
        if mood in ("happy", "cheerful"):
            if archie.warmup_stacks < 5:
                archie.warmup_stacks += 1
                archie.speed = store.clamp_enemy_speed(archie.speed + archie.warmup_stacks * 0.01)
            if kris is not None and kris.current_hp < kris.max_hp * 0.6:
                archie.bonus_atk = max(-0.5, getattr(archie, "bonus_atk", 0.0) - 0.10)
        elif mood == "angry" and kris is not None and kris.current_hp < kris.max_hp * 0.7:
            archie.bonus_atk = getattr(archie, "bonus_atk", 0.0) + 0.30
            archie.bonus_crit = getattr(archie, "bonus_crit", 0.0) + 0.30

    def archie_apply_social_passives(target, attacker, action_name, success, result):
        """Applies enemy-only Archie effects after an Acts check."""
        if target is None or getattr(target, "name", None) != "Арчи":
            return result
        mood = getattr(target, "mood", "happy")
        if mood == "neutral" and not success and result.get("rollback") and renpy.random.random() <= 0.25:
            result = dict(result)
            result.pop("rollback", None)
            renpy.notify("Арчи закрыл глаза на ошибку! Штраф отменен.")
        if getattr(attacker, "name", None) != "Крис":
            return result
        if mood in ("happy", "cheerful") and not success:
            target.dc_offset = int(getattr(target, "dc_offset", 0)) - 1
        elif mood == "neutral" and success:
            if action_name in ("Убеждение", "Поддержать", "Исполнение"):
                attacker.bonus_charm = getattr(attacker, "bonus_charm", 0) + 8
                renpy.notify("Крис получает +8% к очарованию!")
            elif action_name in ("Рассказать", "Играть", "Дразнить"):
                target.dc_offset = int(getattr(target, "dc_offset", 0)) - 1
                renpy.notify("Сложность бросков снижена на 1!")
        return result
