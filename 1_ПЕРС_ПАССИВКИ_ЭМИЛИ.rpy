# Способности Эмили. Все значения хранятся на объекте персонажа, поэтому
# корректно переживают смену цели и сохранения Ren'Py.

default emily_reputation = 0
default emily_hack_progress = {}
default emily_digital_shield = {}
default emily_disabled = {}
default emily_second_turn_chance = 0.0

init python:
    EMILY_ATTACKS = ("Вперёд, Мистер коготь!", "Назад, Мистер Коготь!")
    EMILY_ABILITIES = (
        "Викторина", "Гонка чисел", "Цифровой щит", "Блеснуть безупречностью",
        "Взлом сети", "Блокировка", "Левый аккаунт", "Заморозка репозитория",
        "Трансляция взлома", "Маленькая ошибка", "Доксиинг", "Взлом аккаунта",
        "Блэк аут", "Резервная копия", "Игра оптики",
    )

    def emily_level():
        return int(getattr((getattr(store, "pers_dict", {}) or {}).get("Эмили"), "level", 1) or 1)

    def emily_target_key(target):
        return getattr(target, "name", None) if target is not None else None

    def emily_add_debuff(target, name, turns=1, value=1):
        if target is None:
            return
        key = "emily_debuff_" + name
        setattr(target, key, max(int(getattr(target, key, 0) or 0), int(turns)))
        setattr(target, key + "_value", value)

    def emily_successful_action():
        """Пассивы, срабатывающие после успешного действия Эмили."""
        if getattr(store, "current_attacker", None) != 11:
            return
        store.emily_reputation = min(5, int(getattr(store, "emily_reputation", 0)) + 1)
        store.emily_second_turn_chance = min(1.0, float(getattr(store, "emily_second_turn_chance", 0.0)) + 0.003)

    def emily_on_damage_taken():
        store.emily_reputation = max(0, int(getattr(store, "emily_reputation", 0)) - 2)

    def emily_hack(target, amount=1):
        if target is None:
            return 0
        key = emily_target_key(target)
        progress = dict(getattr(store, "emily_hack_progress", {}) or {})
        progress[key] = min(4, int(progress.get(key, 0)) + amount)
        store.emily_hack_progress = progress
        if progress[key] >= 4:
            progress[key] = 0
            emily_add_debuff(target, "disabled", 2, 1)
        return progress[key]

    def emily_apply_ability(name, target):
        if target is None and name not in ("защита_Эмили", "Блеснуть безупречностью", "Блэк аут", "Игра оптики"):
            return False
        emily = (getattr(store, "pers_dict", {}) or {}).get("Эмили")
        if emily is None:
            return False
        if name == "защита_Эмили":
            emily.indefense = 1
            emily.bonus_def = max(getattr(emily, "bonus_def", 0), 0.10)
        elif name in EMILY_ATTACKS:
            damage = max(0, int(emily.calculate_dmg(target)))
            target.current_hp = max(0, target.current_hp - damage)
            target.damage_gain_for_vis = damage
            emily_hack(target, 1 if name == "Вперёд, Мистер коготь!" else 2)
        if name == "Вперёд, Мистер коготь!":
            emily_add_debuff(target, "bleed", 3, 1)
        elif name == "Назад, Мистер Коготь!":
            target.current_hp = min(getattr(target, "max_hp", target.current_hp), target.current_hp + max(1, int(emily.max_hp * 0.05)))
        elif name == "Викторина":
            emily_hack(target, 1); emily_add_debuff(target, "quiz", 2, 1)
        elif name == "Гонка чисел":
            emily_hack(target, 1); emily_add_debuff(target, "numbers", 2, 1)
        elif name == "Цифровой щит":
            store.emily_digital_shield[emily_target_key(target)] = 1
            emily_hack(target, 2)
        elif name == "Блеснуть безупречностью":
            emily.bonus_magic = getattr(emily, "bonus_magic", 1.0) + 0.08
            emily.bonus_perform = getattr(emily, "bonus_perform", 0.0) + 0.10
        elif name == "Взлом сети":
            emily_hack(target, 2)
            for enemy in (getattr(store, "enemies", {}) or {}).values():
                if enemy is not target: emily_hack(enemy, 1)
        elif name == "Блокировка":
            emily_add_debuff(target, "blocked", 3, 2)
        elif name == "Левый аккаунт":
            emily_add_debuff(target, "left_account", 2, 1)
        elif name == "Заморозка репозитория":
            emily_add_debuff(target, "frozen", 3, 1)
        elif name == "Трансляция взлома":
            emily_hack(target, 1); emily_add_debuff(target, "translation", 5, 1)
        elif name == "Маленькая ошибка":
            emily_add_debuff(target, "mistake", 3, 1)
        elif name == "Доксиинг":
            emily_add_debuff(target, "doxxing", 3, 1)
        elif name == "Взлом аккаунта":
            emily_add_debuff(target, "distracted", 1, 1); emily_hack(target, 2)
        elif name == "Блэк аут":
            for enemy in (getattr(store, "enemies", {}) or {}).values(): emily_add_debuff(enemy, "disabled", 2, 1)
        elif name == "Резервная копия":
            emily_add_debuff(target, "repository", 3, 1)
        elif name == "Игра оптики":
            for enemy in (getattr(store, "enemies", {}) or {}).values(): emily_add_debuff(enemy, "optics", 2, 1)
        emily_successful_action()
        return True

# Каждая способность имеет отдельную точку входа. Это сохраняет тот же
# контракт, что и у боевых лейблов Криса: кнопка меню всегда прыгает в
# именованный лейбл, а общий исполнитель занимается только применением.
label emily_defend_is_done:
    $ store.attackindex = "защита_Эмили"
    jump emily_ability_is_done
label emily_attack_1_is_done:
    $ store.attackindex = "Вперёд, Мистер коготь!"
    jump emily_ability_is_done
label emily_attack_2_is_done:
    $ store.attackindex = "Назад, Мистер Коготь!"
    jump emily_ability_is_done
label emily_magic_1_is_done:
    $ store.attackindex = "Викторина"
    jump emily_ability_is_done
label emily_magic_2_is_done:
    $ store.attackindex = "Гонка чисел"
    jump emily_ability_is_done
label emily_magic_3_is_done:
    $ store.attackindex = "Цифровой щит"
    jump emily_ability_is_done
label emily_magic_4_is_done:
    $ store.attackindex = "Блеснуть безупречностью"
    jump emily_ability_is_done
label emily_magic_5_is_done:
    $ store.attackindex = "Взлом сети"
    jump emily_ability_is_done
label emily_magic_6_is_done:
    $ store.attackindex = "Блокировка"
    jump emily_ability_is_done
label emily_magic_7_is_done:
    $ store.attackindex = "Левый аккаунт"
    jump emily_ability_is_done
label emily_magic_8_is_done:
    $ store.attackindex = "Заморозка репозитория"
    jump emily_ability_is_done
label emily_magic_9_is_done:
    $ store.attackindex = "Трансляция взлома"
    jump emily_ability_is_done
label emily_magic_10_is_done:
    $ store.attackindex = "Маленькая ошибка"
    jump emily_ability_is_done
label emily_magic_11_is_done:
    $ store.attackindex = "Доксиинг"
    jump emily_ability_is_done
label emily_magic_12_is_done:
    $ store.attackindex = "Взлом аккаунта"
    jump emily_ability_is_done
label emily_magic_13_is_done:
    $ store.attackindex = "Блэк аут"
    jump emily_ability_is_done
label emily_magic_14_is_done:
    $ store.attackindex = "Резервная копия"
    jump emily_ability_is_done
label emily_magic_15_is_done:
    $ store.attackindex = "Игра оптики"
    jump emily_ability_is_done

label emily_ability_is_done:
    $ emily_apply_ability(store.attackindex, store.target)
    # Возврат когтя по спецификации не расходует ход.
    $ store.pers_dict["Эмили"].turn = 1 if store.attackindex == "Назад, Мистер Коготь!" else 0
    $ store.pers_dict["Эмили"].state = "idle"
    hide screen Heroattacks
    $ base_perform = 0
    jump afterheroattack

