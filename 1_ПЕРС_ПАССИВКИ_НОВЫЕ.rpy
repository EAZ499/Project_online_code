# Полные боевые лейблы персонажей из спецификации.
# До добавления отдельных портретов новые участники используют нейтральную
# карточку Криса. Это сохраняет существующий team_status_display рабочим:
# динамический image-tag вида «[char_name]herobox.png» не падает с ошибкой.
image Ральзейherobox = "Крисherobox.png"
image Ноэлльherobox = "Крисherobox.png"
image Сансherobox = "Крисherobox.png"
image Бердлиherobox = "Крисherobox.png"

init python:
    NEW_CHARACTER_NAMES = {13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
    NEW_CHARACTER_LABELS = {
        "защита_Ральзей": "ralsei_defend_is_done", "Умиротворение": "ralsei_magic_1_is_done", "Лозы": "ralsei_magic_2_is_done",
        "Молитва исцеления": "ralsei_magic_3_is_done", "Агрессивный пузырь": "ralsei_magic_4_is_done",
        "Пушистый страж": "ralsei_magic_5_is_done", "Лечение?...": "ralsei_magic_6_is_done",
        "Рассеять!": "ralsei_magic_7_is_done", "Пламенная казнь": "ralsei_magic_8_is_done",
        "Перегной": "ralsei_magic_9_is_done", "Убеждающий вид": "ralsei_magic_10_is_done",
        "Приумножить заслуги": "ralsei_magic_11_is_done", "Унизить слабого": "ralsei_magic_12_is_done",
        "Песнь воскрешения": "ralsei_magic_13_is_done", "Спустить с небес": "ralsei_magic_14_is_done",
        "Концентрация зла": "ralsei_magic_15_is_done", "Тёмный горящий сад": "ralsei_magic_16_is_done",
        "защита_Ноэлль": "noelle_defend_is_done", "Неуверенный взмах": "noelle_attack_1_is_done",
        "Ледяная катана": "noelle_attack_2_is_done", "Снежок": "noelle_attack_3_is_done",
        "Молитва исцеления Ноэлль": "noelle_magic_1_is_done", "Ледяной шок": "noelle_magic_2_is_done",
        "Сонный туман": "noelle_magic_3_is_done", "Морозная завеса": "noelle_magic_4_is_done",
        "Ледяная буря": "noelle_magic_5_is_done", "Оледенение чувств": "noelle_magic_6_is_done",
        "Морозная корка": "noelle_magic_7_is_done", "Ледяной кокон": "noelle_magic_8_is_done",
        "Аура холодного сердца": "noelle_magic_9_is_done", "Терновый сад": "noelle_magic_10_is_done",
        "Цветение бед": "noelle_magic_11_is_done", "Снежная могила": "noelle_magic_12_is_done",
        "защита_Санс": "sans_defend_is_done", "Удар костью": "sans_attack_1_is_done",
        "Преподать урок": "sans_attack_2_is_done", "Подойди сюда": "sans_attack_3_is_done",
        "Стена костей": "sans_magic_1_is_done", "Костяной дождь": "sans_magic_2_is_done",
        "Прижмись": "sans_magic_3_is_done", "Поспать": "sans_magic_4_is_done",
        "Камнем вниз": "sans_magic_5_is_done", "Костяной щит": "sans_magic_6_is_done",
        "Бластер": "sans_magic_7_is_done", "Пинг-понг": "sans_magic_8_is_done",
        "Костяная клетка": "sans_magic_9_is_done", "Угрызения совести": "sans_magic_10_is_done",
        "Кара за грехи": "sans_magic_11_is_done", "Телекинез!": "sans_magic_12_is_done",
        "Финальная атака": "sans_magic_13_is_done", "защита_Бердли": "berdly_defend_is_done",
        "Клювом!": "berdly_attack_1_is_done", "Гениальный план": "berdly_magic_1_is_done",
        "Электрический клюв": "berdly_magic_2_is_done", "Вихрь знаний": "berdly_magic_3_is_done",
    }

    def new_character_jump_to_label():
        renpy.jump(NEW_CHARACTER_LABELS.get(getattr(store, "attackindex", None), "generic_character_ability_is_done"))

    def new_character_actor():
        attacker = getattr(store, "current_attacker", None)
        if getattr(attacker, "name", None) in NEW_CHARACTER_NAMES.values():
            return attacker
        return (getattr(store, "pers_dict", {}) or {}).get(NEW_CHARACTER_NAMES.get(attacker))

    def new_character_enemies():
        return [e for e in (getattr(store, "enemies", {}) or {}).values()
                if getattr(e, "current_hp", 0) > 0 and not getattr(e, "spared", False)]

    def new_character_is_enemy(entity):
        return entity is not None and not getattr(entity, "is_ally", False)

    def new_character_damage(entity, amount, damage_type="magic"):
        if entity is None:
            return 0
        amount = max(0, int(amount))
        if getattr(entity, "noelle_ice_tomb", False):
            amount = int(amount * (2.0 if damage_type == "fire" else 1.7 if damage_type == "physical" else 1.0))
        if damage_type == "fire" and getattr(entity, "ralsei_fuel", 0):
            ralsei = (getattr(store, "pers_dict", {}) or {}).get("Ральзей")
            fuel = int(getattr(entity, "ralsei_fuel", 0) or 0)
            entity.ralsei_fuel = 0
            entity.ralsei_burning = int(getattr(entity, "ralsei_burning", 0) or 0) + fuel
            if ralsei is not None:
                entity.ralsei_burning_power = new_character_magic(ralsei)
        if getattr(entity, "shield", 0) > 0:
            entity.shield = max(0, int(entity.shield) - 1)
            return 0
        before = int(getattr(entity, "current_hp", 0) or 0)
        entity.current_hp = max(0, before - amount)
        entity.damage_gain_for_vis = before - entity.current_hp
        return before - entity.current_hp

    def new_character_heal(entity, amount, trigger_ralsei=True):
        if entity is None:
            return 0
        before = int(getattr(entity, "current_hp", 0) or 0)
        entity.current_hp = min(int(getattr(entity, "max_hp", before) or before), before + max(0, int(amount)))
        healed = entity.current_hp - before
        # «Принятие доброты» (ур.7): Ральзей получает 30% от лечения цели.
        ralsei = (getattr(store, "pers_dict", {}) or {}).get("Ральзей")
        if (trigger_ralsei and healed > 0 and ralsei is not None and
                getattr(ralsei, "level", 1) >= 7 and entity is not ralsei):
            new_character_heal(ralsei, healed * 0.30, trigger_ralsei=False)
        return healed

    def new_character_on_damage_taken(victim, amount, source=None):
        """Событие урона для пассивов Ноэлль и Санса."""
        if victim is None or amount <= 0:
            return
        if getattr(victim, "name", None) == "Ноэлль":
            # «Хрупкое сердце»: страх x2 и скидка на следующую магию.
            if renpy.random.random() < 0.35:
                victim.fear_debuff = max(getattr(victim, "fear_debuff", 0), 2)
                victim.fear_state = True
                victim.noelle_next_magic_cost_multiplier = 0.80
        if getattr(victim, "ralsei_guard", 0) and source is not None:
            ralsei = (getattr(store, "pers_dict", {}) or {}).get("Ральзей")
            if ralsei is not None:
                new_character_damage(source, new_character_magic(ralsei, 0.30))
            victim.ralsei_guard = 0
        sans = (getattr(store, "pers_dict", {}) or {}).get("Санс")
        if sans is not None and getattr(sans, "level", 1) >= 5 and source is not None:
            new_character_add_status(source, "sans_karma", 2)

    def new_character_bubble_burst(victim):
        """Взрыв «Агрессивного пузыря» при первом полученном ударе."""
        if victim is None or not getattr(victim, "ralsei_bubble", 0):
            return
        ralsei = (getattr(store, "pers_dict", {}) or {}).get("Ральзей")
        if ralsei is None:
            victim.ralsei_bubble = 0
            return
        for enemy in new_character_enemies():
            new_character_damage(enemy, new_character_magic(ralsei, 0.15))
            status = renpy.random.choice(("bloodshed_debuff", "atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff"))
            new_character_add_status(enemy, status, 1)
        victim.ralsei_bubble = 0

    def new_character_on_spare_success(attacker_name=None):
        """Ральзей: «Облегчающие переговоры» — лечение после пощады."""
        ralsei = (getattr(store, "pers_dict", {}) or {}).get("Ральзей")
        if ralsei is None:
            return
        amount = new_character_magic(ralsei) * 0.20
        if attacker_name == "Ральзей":
            amount *= 2.0
        for ally in (getattr(store, "pers_dict", {}) or {}).values():
            if getattr(ally, "is_ally", True) and getattr(ally, "current_hp", 0) > 0:
                new_character_heal(ally, amount)

    def new_character_clear_frost(entity):
        if entity is None:
            return
        if hasattr(entity, "_noelle_base_speed"):
            entity.speed = entity._noelle_base_speed
            delattr(entity, "_noelle_base_speed")
        entity.noelle_frost = 0
        entity.noelle_frost_accuracy = 0
        entity.noelle_frost_social_penalty = 0
        entity.noelle_ice_tomb = False

    def new_character_add_status(entity, name, stacks=1):
        if entity is None:
            return 0
        if name == "noelle_frost":
            old_value = int(getattr(entity, "noelle_frost", 0) or 0)
            new_value = min(5, max(0, old_value + int(stacks)))
            if new_value > old_value:
                if not hasattr(entity, "_noelle_base_speed"):
                    entity._noelle_base_speed = float(getattr(entity, "speed", 1.0))
                entity.speed = max(0.05, entity._noelle_base_speed * (1.0 - 0.02 * new_value))
            entity.noelle_frost = new_value
            entity.noelle_frost_accuracy = new_value * 0.01
            entity.noelle_frost_social_penalty = new_value
            if new_value >= 5:
                entity.noelle_ice_tomb = True
            return new_value
        value = max(0, int(getattr(entity, name, 0) or 0) + int(stacks))
        setattr(entity, name, value)
        return value

    def new_character_clear_debuffs(entity):
        if entity is None:
            return
        for name in ("bloodshed_debuff", "prone_debuff", "atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff", "critrate_debuff", "critdmg_debuff", "fear_debuff", "speed_debuff", "sans_prone", "noelle_frost_crust", "sans_karma"):
            if hasattr(entity, name):
                setattr(entity, name, 0)
        new_character_clear_frost(entity)
        entity.fear_state = False

    def new_character_magic(actor, coefficient=1.0):
        return max(1, int(float(getattr(actor, "magic", 1)) * coefficient))

    def new_character_apply(ability_name):
        actor = new_character_actor()
        target = getattr(store, "target", None)
        if actor is None:
            return
        enemies = new_character_enemies()
        allies = [c for c in (getattr(store, "pers_dict", {}) or {}).values()
                  if getattr(c, "is_ally", True) and getattr(c, "current_hp", 0) > 0]
        magic = new_character_magic(actor)

        if ability_name.startswith("защита_"):
            actor.indefense = 1
            actor.bonus_def = max(getattr(actor, "bonus_def", 0), 1)
            if actor.name == "Ноэлль":
                actor.current_mp = min(actor.max_mp, actor.current_mp + int(actor.max_mp * 0.15))
                actor.bonus_tank = max(0, getattr(actor, "bonus_tank", 0) - 2)
                if not getattr(actor, "noelle_defense_reflex_active", False):
                    actor.bonus_critrate2 = getattr(actor, "bonus_critrate2", 0) + 0.12
                    actor.noelle_defense_critrate_bonus = 0.12
                    actor.noelle_defense_reflex_active = True
            elif actor.name == "Санс":
                actor.sans_dodge_charges = 4
            return

        # Ральзей.
        if ability_name == "Умиротворение":
            if new_character_is_enemy(target):
                target.spare_progress = max(getattr(target, "spare_progress", 0), 85)
                if target.current_hp <= target.max_hp * 0.10 or target.spare_progress >= 85:
                    target.spared = True
                    new_character_on_spare_success("Ральзей")
        elif ability_name == "Лозы":
            if new_character_is_enemy(target):
                new_character_damage(target, magic * 0.70)
                new_character_add_status(target, "ralsei_fuel", 1)
                new_character_clear_frost(target)
        elif ability_name == "Молитва исцеления":
            healed = new_character_heal(target, magic * 1.30)
            if getattr(actor, "level", 1) >= 4:
                candidates = [ally for ally in allies if ally is not target]
                if candidates:
                    second_target = min(candidates, key=lambda ally: float(getattr(ally, "current_hp", 0)) / max(1, getattr(ally, "max_hp", 1)))
                    new_character_heal(second_target, magic * 1.30 * 0.40)
            if getattr(actor, "level", 1) >= 7:
                new_character_heal(actor, healed * 0.30)
        elif ability_name == "Агрессивный пузырь":
            if target is not None:
                target.shield = getattr(target, "shield", 0) + 1
                target.ralsei_bubble = 1
        elif ability_name == "Пушистый страж":
            if target is not None:
                target.ralsei_guard = 1
        elif ability_name == "Лечение?...":
            if target is not None:
                new_character_add_status(target, "bloodshed_debuff" if new_character_is_enemy(target) else "ralsei_reverse_heal", 3)
        elif ability_name == "Рассеять!":
            new_character_clear_debuffs(target)
            if target is not None:
                for name in ("bonus_atk2", "bonus_magic2", "bonus_def2", "bonus_dmgchance2"):
                    if hasattr(target, name):
                        setattr(target, name, 0)
        elif ability_name == "Пламенная казнь":
            if new_character_is_enemy(target):
                if target.current_hp <= magic * 2.5:
                    target.current_hp = 0
                else:
                    new_character_damage(target, magic * 1.5, "fire")
                if target.current_hp <= 0:
                    set_battle_ability_current_cd(ability_name, 0)
        elif ability_name == "Перегной":
            if target is not None:
                multiplier = 2 if getattr(actor, "level", 1) >= 8 else 1
                for name in ("bloodshed_debuff", "prone_debuff", "atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff"):
                    if hasattr(target, name):
                        setattr(target, name, getattr(target, name, 0) * multiplier + 2)
        elif ability_name == "Убеждающий вид":
            if new_character_is_enemy(target):
                target.spare_progress = min(getattr(target, "spare_max", 100), getattr(target, "spare_progress", 0) + int(magic * getattr(actor, "diplomacy", 1) * 0.15))
        elif ability_name == "Приумножить заслуги":
            if target is not None:
                for name in ("bonus_atk2", "bonus_magic2", "bonus_def2", "bonus_dmgchance2", "bonus_crit2"):
                    if hasattr(target, name):
                        setattr(target, name, getattr(target, name, 0) * 1.30)
                if getattr(actor, "level", 1) >= 7:
                    actor.bonus_magic2 = getattr(actor, "bonus_magic2", 0) + 0.20
        elif ability_name in ("Унизить слабого", "Спустить с небес"):
            if target is not None:
                stacks = sum(max(0, int(getattr(target, n, 0) or 0)) for n in ("bloodshed_debuff", "prone_debuff", "atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff"))
                new_character_clear_debuffs(target)
                if enemies:
                    destination = max(enemies, key=lambda e: sum(max(0, int(getattr(e, n, 0) or 0)) for n in ("bloodshed_debuff", "prone_debuff", "atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff")))
                    new_character_add_status(destination, "bloodshed_debuff", stacks)
        elif ability_name == "Песнь воскрешения":
            if target is not None and getattr(target, "current_hp", 0) <= 0:
                target.current_hp = max(1, int(target.max_hp * 0.01))
                if getattr(actor, "level", 1) >= 9:
                    new_character_heal(target, new_character_magic(actor) * 1.30)
        elif ability_name == "Концентрация зла":
            total = 0
            for entity in list(enemies) + allies:
                total += sum(max(0, int(getattr(entity, n, 0) or 0)) for n in ("bloodshed_debuff", "prone_debuff", "atk_debuff", "def_debuff", "magic_debuff", "accuracy_debuff"))
                new_character_clear_debuffs(entity)
            actor.bonus_magic2 = getattr(actor, "bonus_magic2", 0) + total * 0.50
            for enemy in enemies:
                new_character_damage(enemy, magic * total * 0.03)
            for ally in allies:
                new_character_heal(ally, magic * total * 0.03)
        elif ability_name == "Тёмный горящий сад":
            for enemy in enemies:
                for _ in range(3):
                    new_character_add_status(enemy, "ralsei_fuel", 1)
                    new_character_clear_frost(enemy)
                    new_character_damage(enemy, magic * 0.70, "fire")
                new_character_damage(enemy, magic * 3.0, "fire")

        # Ноэлль.
        elif ability_name == "Неуверенный взмах":
            new_character_damage(target, max(0, getattr(actor, "atk", 1) - getattr(target, "defense", 0)), "physical")
            if renpy.random.random() < 0.20:
                actor.prone_debuff = max(getattr(actor, "prone_debuff", 0), 1)
        elif ability_name == "Ледяная катана":
            new_character_damage(target, max(0, getattr(actor, "atk", 1) - getattr(target, "defense", 0)), "physical")
            new_character_add_status(target, "noelle_frost", 1)
        elif ability_name == "Снежок":
            new_character_damage(target, max(1, int(getattr(actor, "atk", 1) * 0.50)), "physical")
            new_character_add_status(target, "noelle_frost", 1)
            new_character_add_status(target, "accuracy_debuff", 2)
        elif ability_name == "Молитва исцеления Ноэлль":
            ratio = float(getattr(target, "current_hp", 0)) / max(1, getattr(target, "max_hp", 1)) if target else 1
            new_character_heal(target, magic * 1.30)
            if getattr(actor, "level", 1) >= 2 and ratio < 0.30:
                new_character_heal(target, target.max_hp * 0.15)
                new_character_add_status(target, "noelle_inspiration", 1)
            if getattr(actor, "level", 1) >= 6 and ratio < 0.25:
                new_character_clear_debuffs(target)
                target.current_mp = min(target.max_mp, target.current_mp + 10)
        elif ability_name == "Ледяной шок":
            new_character_damage(target, max(0, magic * 1.40 - getattr(target, "defense", 0)))
            already_frosted = bool(getattr(target, "noelle_frost", 0))
            frost_stacks = 2 if getattr(actor, "level", 1) >= 3 and already_frosted else 1
            if (getattr(actor, "current_mp", 0) > getattr(actor, "max_mp", 1) * 0.60 and
                    renpy.random.random() < float(getattr(actor, "critrate", 0.0))):
                frost_stacks += 1
            new_character_add_status(target, "noelle_frost", frost_stacks)
            if getattr(target, "current_hp", 1) <= 0:
                target.noelle_ice_tomb = True
        elif ability_name == "Сонный туман":
            for enemy in enemies:
                ratio = float(enemy.current_hp) / max(1, enemy.max_hp)
                if enemy.spare_progress >= 85 or ratio <= 0.15:
                    enemy.spare_progress = max(enemy.spare_progress, 100)
                    enemy.spared = True
                    new_character_on_spare_success("Ноэлль")
                else:
                    new_character_add_status(enemy, "atk_debuff", 1)
                    enemy.speed = max(0.5, getattr(enemy, "speed", 1.0) * 0.95)
                    enemy.spare_progress = min(getattr(enemy, "spare_max", 100), enemy.spare_progress + int(magic * 0.60))
        elif ability_name == "Морозная завеса":
            for ally in allies:
                ally.bonus_def2 = getattr(ally, "bonus_def2", 0) + 0.10
            if getattr(actor, "level", 1) >= 5:
                for enemy in enemies:
                    new_character_add_status(enemy, "noelle_frost", 2)
        elif ability_name == "Ледяная буря":
            for enemy in enemies:
                new_character_damage(enemy, magic * 0.70)
                extra_frost = (getattr(actor, "level", 1) >= 6 and
                               renpy.random.random() < min(1.0, float(getattr(actor, "critrate", 0.0)) + 0.50))
                new_character_add_status(enemy, "noelle_frost", 2 if extra_frost else 1)
        elif ability_name == "Оледенение чувств":
            new_character_add_status(target, "accuracy_debuff", 4)
            new_character_add_status(target, "def_debuff", 2)
            new_character_add_status(target, "noelle_frost", 2)
            target.prone_debuff = max(getattr(target, "prone_debuff", 0), 1)
        elif ability_name == "Морозная корка":
            setattr(target, "noelle_frost_crust", 2)
        elif ability_name == "Ледяной кокон":
            if target is not None:
                target.noelle_cocoon = 2
                target.shield = getattr(target, "shield", 0) + 2
                target.turn = 0
        elif ability_name == "Аура холодного сердца":
            actor.current_hp = max(1, actor.current_hp - int(actor.current_hp * 0.10))
            for ally in allies:
                ally._next_attack_multiplier_temp = max(getattr(ally, "_next_attack_multiplier_temp", 1.0), 1.30 if ally.name == "Крис" else 1.20)
        elif ability_name == "Терновый сад":
            for enemy in enemies:
                enemy.noelle_thorn_garden = 2
                new_character_add_status(enemy, "bloodshed_debuff", 2)
                new_character_add_status(enemy, "noelle_frost", 2)
                new_character_add_status(enemy, "accuracy_debuff", 2)
        elif ability_name == "Цветение бед":
            for enemy in enemies:
                stacks = int(getattr(enemy, "noelle_thorn_garden", 0) or 0)
                enemy.noelle_thorn_garden = 0
                new_character_damage(enemy, magic * 0.80 * stacks)
        elif ability_name == "Снежная могила":
            actor.current_hp = max(1, actor.current_hp - int(actor.current_hp * 0.30))
            actor.current_mp = 0
            for enemy in enemies:
                new_character_damage(enemy, magic * (4.0 if enemy is target else 1.3))
                new_character_add_status(enemy, "noelle_frost", 5 if enemy is target else 2)
                if enemy is target and getattr(enemy, "noelle_ice_tomb", False):
                    new_character_damage(enemy, magic * 3.0)
                if getattr(enemy, "noelle_frost", 0) >= 5:
                    enemy.noelle_ice_tomb = True

        # Санс.
        elif ability_name == "Удар костью":
            new_character_damage(target, max(0, getattr(actor, "atk", 1) - getattr(target, "defense", 0)))
            new_character_add_status(target, "sans_karma", 4)
            new_character_add_status(target, "atk_debuff", 1)
        elif ability_name == "Преподать урок":
            new_character_damage(target, new_character_magic(actor, 0.60))
            new_character_add_status(target, "sans_karma", 5)
            target.sans_karma_no_tick = 1
            if getattr(actor, "level", 1) >= 5 and new_character_is_enemy(target):
                target.spare_progress = min(getattr(target, "spare_max", 100),
                                            getattr(target, "spare_progress", 0) + 10 + getattr(actor, "diplomacy", 0) * 0.50)
        elif ability_name == "Подойди сюда":
            new_character_damage(target, magic)
            new_character_add_status(target, "sans_karma", 7)
        elif ability_name == "Стена костей":
            new_character_damage(target, magic * 0.80)
            new_character_add_status(target, "sans_karma", 4)
            if getattr(actor, "level", 1) >= 2 and renpy.random.random() < getattr(actor, "critrate", 0):
                for enemy in enemies:
                    if enemy is not target:
                        new_character_damage(enemy, magic * 0.56)
                        break
        elif ability_name == "Костяной дождь":
            for enemy in enemies:
                new_character_damage(enemy, magic * 0.30)
                new_character_add_status(enemy, "sans_karma", 4)
                if enemy is target and getattr(actor, "level", 1) >= 3:
                    new_character_damage(enemy, magic * 0.15)
                    new_character_add_status(enemy, "sans_karma", 2)
        elif ability_name == "Прижмись":
            new_character_add_status(target, "sans_prone", 1)
            new_character_add_status(target, "speed_debuff", 2)
            if getattr(actor, "level", 1) >= 6:
                new_character_add_status(target, "magic_debuff", 2)
        elif ability_name == "Поспать":
            actor.sans_dodge_charges = 4
            actor.current_mp = min(actor.max_mp, actor.current_mp + int(actor.max_mp * 0.40))
            actor.bonus_tank = getattr(actor, "bonus_tank", 0) + 3
        elif ability_name == "Камнем вниз":
            new_character_damage(target, magic + getattr(target, "defense", 0))
            new_character_add_status(target, "atk_debuff", 3 if getattr(actor, "level", 1) >= 4 else 2)
            new_character_add_status(target, "accuracy_debuff", 3)
            if getattr(actor, "level", 1) >= 4:
                new_character_add_status(target, "fear_debuff", 3)
                for enemy in enemies:
                    if enemy is not target and renpy.random.random() < float(getattr(actor, "critrate", 0.0)):
                        new_character_add_status(enemy, "fear_debuff", 2)
        elif ability_name == "Костяной щит":
            if target is not None:
                target.shield = getattr(target, "shield", 0) + 1
                target.sans_bone_shield = 1
        elif ability_name == "Бластер":
            if getattr(actor, "sans_dodge_charges", 0) > 0:
                actor.sans_dodge_charges -= 1
                for enemy in enemies:
                    karma_multiplier = (getattr(enemy, "sans_karma", 0) * 4
                                        if getattr(actor, "level", 1) >= 8 else
                                        1 + getattr(enemy, "sans_karma", 0) * 0.04)
                    new_character_damage(enemy, magic * max(1, karma_multiplier))
                    new_character_add_status(enemy, "sans_karma", 9)
        elif ability_name == "Пинг-понг":
            actor.sans_dodge_charges = max(0, getattr(actor, "sans_dodge_charges", 0) - 2)
            new_character_damage(target, magic + getattr(target, "defense", 0))
            new_character_add_status(target, "sans_karma", 3)
        elif ability_name == "Костяная клетка":
            actor.sans_dodge_charges = max(0, getattr(actor, "sans_dodge_charges", 0) - 2)
            new_character_add_status(target, "sans_karma", 5)
            new_character_add_status(target, "atk_debuff", 3)
            new_character_add_status(target, "accuracy_debuff", 2)
        elif ability_name == "Угрызения совести":
            actor.sans_dodge_charges = max(0, getattr(actor, "sans_dodge_charges", 0) - 2)
            for enemy in enemies:
                enemy.sans_karma = int(getattr(enemy, "sans_karma", 0) * 1.5)
                if getattr(actor, "level", 1) >= 7 and renpy.random.random() < float(getattr(actor, "critrate", 0.0)):
                    for other in enemies:
                        if other is not enemy:
                            other.sans_karma = int(getattr(other, "sans_karma", 0) * 1.2)
        elif ability_name == "Кара за грехи":
            actor.sans_dodge_charges = max(0, getattr(actor, "sans_dodge_charges", 0) - 3)
            for enemy in enemies:
                stacks = getattr(enemy, "sans_karma", 0)
                multiplier = 1.50
                if getattr(actor, "level", 1) >= 10 and renpy.random.random() < float(getattr(actor, "critrate", 0.0)):
                    multiplier *= max(1.0, float(getattr(actor, "crit", 1.0)) * 1.30)
                new_character_damage(enemy, magic * stacks * 0.05 * multiplier)
                enemy.sans_karma = 0
        elif ability_name == "Телекинез!":
            actor.sans_dodge_charges = max(0, getattr(actor, "sans_dodge_charges", 0) - 3)
            new_character_damage(target, magic * 1.20)
            new_character_add_status(target, "sans_karma", 4)
        elif ability_name == "Финальная атака":
            charges = max(0, int(getattr(actor, "sans_dodge_charges", 0) or 0))
            actor.sans_dodge_charges = 0
            for enemy in enemies:
                # Костяной дождь.
                new_character_damage(enemy, magic * 0.30)
                new_character_add_status(enemy, "sans_karma", 4)
                # Пинг-понг: выбранная цель получает полный урон, остальные
                # — 70% от броска по полю.
                if enemy is target:
                    new_character_damage(enemy, magic + getattr(enemy, "defense", 0))
                else:
                    new_character_damage(enemy, (magic + getattr(enemy, "defense", 0)) * 0.70)
                new_character_add_status(enemy, "sans_karma", 3)
                # Три бластера на линию за каждый оставшийся заряд уклонения.
                for _ in range(charges * 3):
                    multiplier = max(1.0, 1.0 + getattr(enemy, "sans_karma", 0) * 0.04)
                    new_character_damage(enemy, magic * multiplier)
                    new_character_add_status(enemy, "sans_karma", 9)

        # Бердли: в документе есть только заголовок, поэтому его лейблы
        # используют согласованные базовые эффекты до появления ТЗ.
        elif ability_name == "Клювом!":
            new_character_damage(target, max(0, getattr(actor, "atk", 1) - getattr(target, "defense", 0)))
        elif ability_name == "Гениальный план":
            actor.bonus_magic2 = getattr(actor, "bonus_magic2", 0) + 0.20
            actor.bonus_dmgchance2 = getattr(actor, "bonus_dmgchance2", 0) + 0.10
        elif ability_name == "Электрический клюв":
            new_character_damage(target, magic * 1.20)
            new_character_add_status(target, "accuracy_debuff", 2)
        elif ability_name == "Вихрь знаний":
            for enemy in enemies:
                new_character_damage(enemy, magic * 0.80)
                new_character_add_status(enemy, "def_debuff", 2)

    def generic_character_ability_is_done():
        new_character_apply(getattr(store, "attackindex", None))
        actor = new_character_actor()
        if actor is not None:
            actor.turn = 0
            actor.state = "idle"

    def new_character_round_end_effects():
        """Тики длительных эффектов новых персонажей перед ходом врага."""
        enemies = new_character_enemies()
        noelle = (getattr(store, "pers_dict", {}) or {}).get("Ноэлль")
        sans = (getattr(store, "pers_dict", {}) or {}).get("Санс")
        if noelle is not None:
            # «Сладкоежка»: сладости и свежий салат в очереди снимают страх
            # и восстанавливают 5% HP в конце раунда.
            food_queue = list(getattr(noelle, "feedness_queue", []) or [])
            if any(item in ("sweets", "healthy") for item in food_queue):
                noelle.fear_debuff = max(0, int(getattr(noelle, "fear_debuff", 0) or 0) - 1)
                noelle.accuracy_debuff = max(0, int(getattr(noelle, "accuracy_debuff", 0) or 0) - 1)
                new_character_heal(noelle, noelle.max_hp * 0.05, trigger_ralsei=False)
            thorn_targets = [e for e in enemies if getattr(e, "noelle_thorn_garden", 0) > 0 and getattr(e, "bloodshed_debuff", 0) > 0]
            noelle.current_mp = min(noelle.max_mp, noelle.current_mp + 6 * len(thorn_targets))
            for enemy in thorn_targets:
                enemy.noelle_thorn_garden = min(4, enemy.noelle_thorn_garden + 1)
            for ally in (getattr(store, "pers_dict", {}) or {}).values():
                cocoon = int(getattr(ally, "noelle_cocoon", 0) or 0)
                if cocoon > 0:
                    new_character_heal(ally, ally.max_hp * 0.30)
                    ally.noelle_cocoon = max(0, cocoon - 1)
                    if ally.noelle_cocoon == 0:
                        new_character_clear_debuffs(ally)
            # «Становясь сильнее»: убийство или полная заморозка навсегда
            # повышают магию и критшанс Ноэлль.
            for enemy in (getattr(store, "enemies", {}) or {}).values():
                if getattr(enemy, "current_hp", 0) <= 0 and not getattr(enemy, "noelle_rewarded", False):
                    noelle.bonus_magic2 = getattr(noelle, "bonus_magic2", 0) + 0.0025
                    noelle.bonus_critrate2 = getattr(noelle, "bonus_critrate2", 0) + 0.0015
                    enemy.noelle_rewarded = True
        if sans is not None:
            for enemy in enemies:
                stacks = int(getattr(enemy, "sans_karma", 0) or 0)
                no_tick = bool(getattr(enemy, "sans_karma_no_tick", False))
                if stacks > 0 and not no_tick:
                    damage = min(max(0, enemy.current_hp - 1), int(sans.magic * 0.05 * stacks))
                    enemy.current_hp = max(1, enemy.current_hp - damage)
                # Если Санс действовал по цели в этом раунде, вся её карма
                # сбрасывается без тика урона; иначе снимаются обычные 3 стака.
                enemy.sans_karma = 0 if no_tick else max(0, stacks - 3)
                enemy.sans_karma_no_tick = 0
        for enemy in enemies:
            fuel = int(getattr(enemy, "ralsei_fuel", 0) or 0)
            if fuel > 0:
                ralsei = (getattr(store, "pers_dict", {}) or {}).get("Ральзей")
                if ralsei is not None and not getattr(enemy, "ralsei_burning", 0):
                    enemy.ralsei_burning_power = new_character_magic(ralsei)
                enemy.ralsei_burning = int(getattr(enemy, "ralsei_burning", 0) or 0) + fuel
                enemy.ralsei_fuel = 0
            burning = int(getattr(enemy, "ralsei_burning", 0) or 0)
            if burning > 0:
                snap_magic = int(getattr(enemy, "ralsei_burning_power", 0) or 0)
                if snap_magic > 0:
                    new_character_damage(enemy, snap_magic * 0.10 * burning)

    def new_character_reset_battle_state():
        for name in ("Ральзей", "Ноэлль", "Санс", "Бердли"):
            char = (getattr(store, "pers_dict", {}) or {}).get(name)
            if char is None:
                continue
            char.turn = 1
            char.state = "idle"
            char.sans_dodge_charges = 4 if name == "Санс" else 0
            char.noelle_cocoon = 0
            char.noelle_thorn_garden = 0
            if name == "Ноэлль":
                previous_bonus = float(getattr(char, "noelle_defense_critrate_bonus", 0.12) if getattr(char, "noelle_defense_reflex_active", False) else 0.0)
                if previous_bonus:
                    char.bonus_critrate2 = max(0, getattr(char, "bonus_critrate2", 0) - previous_bonus)
                char.noelle_defense_reflex_active = False
                char.noelle_next_magic_cost_multiplier = 1.0
            char.ralsei_bubble = 0
            char.ralsei_guard = 0
        for enemy in (getattr(store, "enemies", {}) or {}).values():
            new_character_clear_frost(enemy)
            for attr in ("ralsei_fuel", "ralsei_burning", "noelle_frost", "noelle_ice_tomb",
                         "ralsei_burning_power", "noelle_thorn_garden", "noelle_frost_crust", "sans_karma", "sans_karma_no_tick"):
                if hasattr(enemy, attr):
                    setattr(enemy, attr, 0)

label generic_character_ability_is_done:
    $ generic_character_ability_is_done()
    hide screen Heroattacks
    $ base_perform = 0
    jump afterheroattack

# Стабильный отдельный лейбл на каждую способность.
label ralsei_defend_is_done:
    $ store.attackindex = 'защита_Ральзей'
    jump generic_character_ability_is_done
label ralsei_magic_1_is_done:
    $ store.attackindex = 'Умиротворение'
    jump generic_character_ability_is_done
label ralsei_magic_2_is_done:
    $ store.attackindex = 'Лозы'
    jump generic_character_ability_is_done
label ralsei_magic_3_is_done:
    $ store.attackindex = 'Молитва исцеления'
    jump generic_character_ability_is_done
label ralsei_magic_4_is_done:
    $ store.attackindex = 'Агрессивный пузырь'
    jump generic_character_ability_is_done
label ralsei_magic_5_is_done:
    $ store.attackindex = 'Пушистый страж'
    jump generic_character_ability_is_done
label ralsei_magic_6_is_done:
    $ store.attackindex = 'Лечение?...'
    jump generic_character_ability_is_done
label ralsei_magic_7_is_done:
    $ store.attackindex = 'Рассеять!'
    jump generic_character_ability_is_done
label ralsei_magic_8_is_done:
    $ store.attackindex = 'Пламенная казнь'
    jump generic_character_ability_is_done
label ralsei_magic_9_is_done:
    $ store.attackindex = 'Перегной'
    jump generic_character_ability_is_done
label ralsei_magic_10_is_done:
    $ store.attackindex = 'Убеждающий вид'
    jump generic_character_ability_is_done
label ralsei_magic_11_is_done:
    $ store.attackindex = 'Приумножить заслуги'
    jump generic_character_ability_is_done
label ralsei_magic_12_is_done:
    $ store.attackindex = 'Унизить слабого'
    jump generic_character_ability_is_done
label ralsei_magic_13_is_done:
    $ store.attackindex = 'Песнь воскрешения'
    jump generic_character_ability_is_done
label ralsei_magic_14_is_done:
    $ store.attackindex = 'Спустить с небес'
    jump generic_character_ability_is_done
label ralsei_magic_15_is_done:
    $ store.attackindex = 'Концентрация зла'
    jump generic_character_ability_is_done
label ralsei_magic_16_is_done:
    $ store.attackindex = 'Тёмный горящий сад'
    jump generic_character_ability_is_done

label noelle_defend_is_done:
    $ store.attackindex = 'защита_Ноэлль'
    jump generic_character_ability_is_done
label noelle_attack_1_is_done:
    $ store.attackindex = 'Неуверенный взмах'
    jump generic_character_ability_is_done
label noelle_attack_2_is_done:
    $ store.attackindex = 'Ледяная катана'
    jump generic_character_ability_is_done
label noelle_attack_3_is_done:
    $ store.attackindex = 'Снежок'
    jump generic_character_ability_is_done
label noelle_magic_1_is_done:
    $ store.attackindex = 'Молитва исцеления Ноэлль'
    jump generic_character_ability_is_done
label noelle_magic_2_is_done:
    $ store.attackindex = 'Ледяной шок'
    jump generic_character_ability_is_done
label noelle_magic_3_is_done:
    $ store.attackindex = 'Сонный туман'
    jump generic_character_ability_is_done
label noelle_magic_4_is_done:
    $ store.attackindex = 'Морозная завеса'
    jump generic_character_ability_is_done
label noelle_magic_5_is_done:
    $ store.attackindex = 'Ледяная буря'
    jump generic_character_ability_is_done
label noelle_magic_6_is_done:
    $ store.attackindex = 'Оледенение чувств'
    jump generic_character_ability_is_done
label noelle_magic_7_is_done:
    $ store.attackindex = 'Морозная корка'
    jump generic_character_ability_is_done
label noelle_magic_8_is_done:
    $ store.attackindex = 'Ледяной кокон'
    jump generic_character_ability_is_done
label noelle_magic_9_is_done:
    $ store.attackindex = 'Аура холодного сердца'
    jump generic_character_ability_is_done
label noelle_magic_10_is_done:
    $ store.attackindex = 'Терновый сад'
    jump generic_character_ability_is_done
label noelle_magic_11_is_done:
    $ store.attackindex = 'Цветение бед'
    jump generic_character_ability_is_done
label noelle_magic_12_is_done:
    $ store.attackindex = 'Снежная могила'
    jump generic_character_ability_is_done

label sans_defend_is_done:
    $ store.attackindex = 'защита_Санс'
    jump generic_character_ability_is_done
label sans_attack_1_is_done:
    $ store.attackindex = 'Удар костью'
    jump generic_character_ability_is_done
label sans_attack_2_is_done:
    $ store.attackindex = 'Преподать урок'
    jump generic_character_ability_is_done
label sans_attack_3_is_done:
    $ store.attackindex = 'Подойди сюда'
    jump generic_character_ability_is_done
label sans_magic_1_is_done:
    $ store.attackindex = 'Стена костей'
    jump generic_character_ability_is_done
label sans_magic_2_is_done:
    $ store.attackindex = 'Костяной дождь'
    jump generic_character_ability_is_done
label sans_magic_3_is_done:
    $ store.attackindex = 'Прижмись'
    jump generic_character_ability_is_done
label sans_magic_4_is_done:
    $ store.attackindex = 'Поспать'
    jump generic_character_ability_is_done
label sans_magic_5_is_done:
    $ store.attackindex = 'Камнем вниз'
    jump generic_character_ability_is_done
label sans_magic_6_is_done:
    $ store.attackindex = 'Костяной щит'
    jump generic_character_ability_is_done
label sans_magic_7_is_done:
    $ store.attackindex = 'Бластер'
    jump generic_character_ability_is_done
label sans_magic_8_is_done:
    $ store.attackindex = 'Пинг-понг'
    jump generic_character_ability_is_done
label sans_magic_9_is_done:
    $ store.attackindex = 'Костяная клетка'
    jump generic_character_ability_is_done
label sans_magic_10_is_done:
    $ store.attackindex = 'Угрызения совести'
    jump generic_character_ability_is_done
label sans_magic_11_is_done:
    $ store.attackindex = 'Кара за грехи'
    jump generic_character_ability_is_done
label sans_magic_12_is_done:
    $ store.attackindex = 'Телекинез!'
    jump generic_character_ability_is_done
label sans_magic_13_is_done:
    $ store.attackindex = 'Финальная атака'
    jump generic_character_ability_is_done

label berdly_defend_is_done:
    $ store.attackindex = 'защита_Бердли'
    jump generic_character_ability_is_done
label berdly_attack_1_is_done:
    $ store.attackindex = 'Клювом!'
    jump generic_character_ability_is_done
label berdly_magic_1_is_done:
    $ store.attackindex = 'Гениальный план'
    jump generic_character_ability_is_done
label berdly_magic_2_is_done:
    $ store.attackindex = 'Электрический клюв'
    jump generic_character_ability_is_done
label berdly_magic_3_is_done:
    $ store.attackindex = 'Вихрь знаний'
    jump generic_character_ability_is_done

init 10 python:
    # Описания хранятся рядом с лейблами, чтобы карточка способности и
    # фактический исполнитель никогда не расходились по именам.
    _new_ability_text = {
        "защита_Ральзей": "Ральзей принимает защитную стойку и снижает входящий урон.",
        "Умиротворение": "Щадит врага с малым запасом здоровья или высоким прогрессом пощады.",
        "Лозы": "Наносит 70% магии, замедляет врага и накладывает Горючее.",
        "Молитва исцеления": "Восстанавливает союзнику 130% текущей магии.",
        "Агрессивный пузырь": "Даёт союзнику щит, который готов отразить урон.",
        "Пушистый страж": "Защищает союзника и готовит ответный удар по обидчику.",
        "Лечение?...": "Накладывает кровотечение на врага или обратное кровотечение на союзника.",
        "Рассеять!": "Снимает с цели дебаффы и боевые бонусы.",
        "Пламенная казнь": "Добивает врага с низким запасом здоровья или наносит 150% магии.",
        "Перегной": "Увеличивает стаки дебаффов цели на два.",
        "Убеждающий вид": "Повышает прогресс пощады цели.",
        "Приумножить заслуги": "Увеличивает бонусные характеристики выбранного союзника.",
        "Унизить слабого": "Переносит дебаффы союзника на врага с наибольшим числом дебаффов.",
        "Песнь воскрешения": "Возвращает павшего союзника с 1% здоровья.",
        "Спустить с небес": "Снимает дебаффы союзника и переносит их на врага.",
        "Концентрация зла": "Собирает дебаффы, усиливает магию Ральзея, лечит союзников и наносит урон врагам.",
        "Тёмный горящий сад": "Трижды применяет Лозы и дважды Пламенную казнь ко всем врагам.",
        "защита_Ноэлль": "Снижает входящий урон, восстанавливает 12% максимальной маны и уменьшает танк.",
        "Неуверенный взмах": "Слабый физический удар с шансом уронить Ноэлль.",
        "Ледяная катана": "Физический удар и один стак Мороза.",
        "Снежок": "Низкий урон, Мороз и штраф точности врага.",
        "Молитва исцеления Ноэлль": "Лечит союзника на 130% магии Ноэлль.",
        "Ледяной шок": "Наносит 140% магии за вычетом защиты и накладывает Мороз.",
        "Сонный туман": "Щадит ослабленных врагов, остальных замедляет и ослабляет.",
        "Морозная завеса": "Повышает защиту всей команды.",
        "Ледяная буря": "Наносит урон всем врагам и накладывает Мороз.",
        "Оледенение чувств": "Парализует цель, накладывает Страх, снижает защиту и даёт Мороз.",
        "Морозная корка": "Накладывает на врага морозную корку на два хода.",
        "Ледяной кокон": "Даёт союзнику два щита и запрещает ему действовать.",
        "Аура холодного сердца": "Жертвует здоровьем и усиливает следующие атаки команды.",
        "Терновый сад": "Накладывает на всех врагов кровотечение, Мороз и штраф точности.",
        "Цветение бед": "Снимает Терновый сад и наносит урон за каждый снятый ход.",
        "Снежная могила": "Тратит ману и здоровье, нанося огромный урон всем врагам.",
        "защита_Санс": "Восстанавливает четыре гарантированных уклонения.",
        "Удар костью": "Физический удар, снижает атаку и даёт четыре стака Кармы.",
        "Преподать урок": "Наносит урон и даёт пять стаков Кармы.",
        "Подойди сюда": "Магический удар и семь стаков Кармы.",
        "Стена костей": "Наносит урон и даёт четыре стака Кармы.",
        "Костяной дождь": "Бьёт всех врагов и даёт им Карму.",
        "Прижмись": "Прижимает врага и снижает его скорость.",
        "Поспать": "Восстанавливает уклонения и часть маны.",
        "Камнем вниз": "Наносит урон магией и защитой врага, снижает атаку и точность.",
        "Костяной щит": "Ставит щит, принимающий один удар.",
        "Бластер": "Бьёт врагов в линии и даёт им Карму за заряд уклонения.",
        "Пинг-понг": "Бросает цель по полю за два заряда уклонения.",
        "Костяная клетка": "Даёт Карму, снижает атаку и точность цели.",
        "Угрызения совести": "Умножает Карму врагов за два заряда уклонения.",
        "Кара за грехи": "Наносит урон за всю Карму и снимает её.",
        "Телекинез!": "Наносит удар и Карму за три заряда уклонения.",
        "Финальная атака": "Костяной дождь, Пинг-понг и бластеры за все уклонения.",
        "защита_Бердли": "Бердли принимает защитную стойку и снижает входящий урон.",
        "Клювом!": "Физический удар Бердли.",
        "Гениальный план": "Повышает магию и точность Бердли.",
        "Электрический клюв": "Наносит магический урон и снижает точность цели.",
        "Вихрь знаний": "Наносит урон всем врагам и снижает их защиту.",
    }
    if "ABILITY_DESCRIPTIONS" in globals():
        for _name, _description in _new_ability_text.items():
            ABILITY_DESCRIPTIONS.setdefault(_name, {"type": "Магия", "level": 1, "description": _description, "effects": _description, "weapon": None})

