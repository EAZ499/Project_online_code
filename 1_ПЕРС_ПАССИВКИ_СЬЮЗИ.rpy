default susie_rage = 0
default susie_attack_bonus = 1.0
default susie_purple_infusion = 0
default susie_damage_taken = 0

init python:
    SUSIE_ATTACKS = ("Пинок ногой", "Удар Секирой", "Всем и сразу!", "Хвостовой хлыст", "Подручный снаряд", "Кусь!", "Об землю!", "Пурпурный локоть!", "Добивочная!", "Смести всё!")
    def susie_level():
        return int(getattr((getattr(store, "pers_dict", {}) or {}).get("Сьюзи"), "level", 1) or 1)
    def susie_apply_ability(name, target):
        s = (getattr(store, "pers_dict", {}) or {}).get("Сьюзи")
        if s is None: return False
        enemies = list((getattr(store, "enemies", {}) or {}).values())
        if name == "защита_Сьюзи":
            s.indefense = 1
            s.bonus_def = getattr(s, "bonus_def", 0) + 0.10
        elif name in SUSIE_ATTACKS and target is not None:
            mult = 1.0
            if name == "Пурпурный локоть!": mult = 2.1 if getattr(target, "prone_debuff", 0) else 0.8
            if name == "Добивочная!": mult = 3.0
            damage = max(0, int(s.calculate_dmg(target) * mult))
            target.current_hp = max(0, target.current_hp - damage)
            target.damage_gain_for_vis = damage
            if name == "Кусь!": setattr(target, "bloodshed_debuff", getattr(target, "bloodshed_debuff", 0) + 4)
            if name == "Об землю!": setattr(target, "def_debuff", getattr(target, "def_debuff", 0) + 10)
            if name == "Всем и сразу!":
                for e in enemies:
                    if e is not target: e.current_hp = max(0, e.current_hp - damage)
        elif name == "Пурпурная инфузия":
            store.susie_purple_infusion = min(5, int(getattr(store, "susie_purple_infusion", 0)) + 5)
        elif name == "Зазывала":
            s.bonus_tank = getattr(s, "bonus_tank", 0) + 2
            s.bonus_def = getattr(s, "bonus_def", 1.0) + 0.07
        elif name == "Rude Buster" and target is not None:
            damage = max(0, int(s.atk * 1.5 + s.magic * 2))
            target.current_hp = max(0, target.current_hp - damage); target.damage_gain_for_vis = damage
        elif name == "Зверский рык":
            for e in enemies: setattr(e, "fear_debuff", getattr(e, "fear_debuff", 0) + 1)
        elif name == "Секираранг":
            for e in enemies:
                e.current_hp = max(0, e.current_hp - int((s.atk + s.magic) * 1.5))
        elif name == "Rude fissure":
            for e in enemies: e.current_hp = max(0, e.current_hp - int(s.atk * 1.5 + s.magic * 2))
        store.susie_attack_bonus = 1.0
        return True

# Именованные точки входа для всех атак и магий Сьюзи.
label susie_defend_is_done:
    $ store.attackindex = "защита_Сьюзи"
    jump susie_ability_is_done
label susie_attack_1_is_done:
    $ store.attackindex = "Пинок ногой"
    jump susie_ability_is_done
label susie_attack_2_is_done:
    $ store.attackindex = "Удар Секирой"
    jump susie_ability_is_done
label susie_attack_3_is_done:
    $ store.attackindex = "Всем и сразу!"
    jump susie_ability_is_done
label susie_attack_4_is_done:
    $ store.attackindex = "Хвостовой хлыст"
    jump susie_ability_is_done
label susie_attack_5_is_done:
    $ store.attackindex = "Подручный снаряд"
    jump susie_ability_is_done
label susie_attack_6_is_done:
    $ store.attackindex = "Кусь!"
    jump susie_ability_is_done
label susie_attack_7_is_done:
    $ store.attackindex = "Об землю!"
    jump susie_ability_is_done
label susie_attack_8_is_done:
    $ store.attackindex = "Пурпурный локоть!"
    jump susie_ability_is_done
label susie_attack_9_is_done:
    $ store.attackindex = "Добивочная!"
    jump susie_ability_is_done
label susie_attack_10_is_done:
    $ store.attackindex = "Смести всё!"
    jump susie_ability_is_done
label susie_magic_1_is_done:
    $ store.attackindex = "Пурпурная инфузия"
    jump susie_ability_is_done
label susie_magic_2_is_done:
    $ store.attackindex = "Зазывала"
    jump susie_ability_is_done
label susie_magic_3_is_done:
    $ store.attackindex = "Rude Buster"
    jump susie_ability_is_done
label susie_magic_4_is_done:
    $ store.attackindex = "Зверский рык"
    jump susie_ability_is_done
label susie_magic_5_is_done:
    $ store.attackindex = "Секираранг"
    jump susie_ability_is_done
label susie_magic_6_is_done:
    $ store.attackindex = "Rude fissure"
    jump susie_ability_is_done

label susie_ability_is_done:
    $ susie_apply_ability(store.attackindex, store.target)
    $ store.pers_dict["Сьюзи"].turn = 0
    $ store.pers_dict["Сьюзи"].state = "idle"
    hide screen Heroattacks
    $ base_perform = 0
    jump afterheroattack
