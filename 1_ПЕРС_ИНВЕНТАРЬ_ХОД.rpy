
init python:
    def compact_consumable_inventory_after_stack_depleted():
        """
        Пересобирает consumable_inventory без пустых/нулевых стаков,
        чтобы список предметов в боевом grid не оставлял «дырки».
        """
        inventory = getattr(store, "consumable_inventory", None)
        if not hasattr(inventory, "items"):
            return

        compacted = {}
        for item_id, count in inventory.items():
            if not item_id:
                continue

            try:
                normalized_count = int(count)
            except Exception:
                normalized_count = 0

            if normalized_count > 0:
                compacted[item_id] = normalized_count

        store.consumable_inventory = compacted


label perform_item:

    hide screen Heroattacks

    call item_dialogue

    $ attacker = current_attacker
    if isinstance(current_attacker, int):
        $ attacker_party_order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи", "Ральзей", "Ноэлль", "Санс", "Бердли"]
        if 0 < current_attacker <= len(attacker_party_order):
            $ attacker = store.pers_dict.get(attacker_party_order[current_attacker - 1], current_attacker)

    if hasattr(attacker, "state"):
        $ attacker.state = "item"

    $ current_attacker = attacker

    $ renpy.pause(1.0, hard=True)

    if target is not None and isinstance(attackindex, str):
        $ item_display_name = getattr(store, "consumable_names", {}).get(attackindex, attackindex)
        $ is_enemy_target = hasattr(store, "enemies") and target in getattr(store, "enemies", {}).values()
        if store.consumable_inventory.get(attackindex, 0) <= 0:
            pass
            #$ renpy.notify("Предмет [item_display_name] закончился.")
        elif hasattr(store, "is_weapon_consumable_item") and store.is_weapon_consumable_item(attackindex) and hasattr(attacker, "use_weapon_consumable"):
            $ attacker.use_weapon_consumable(attackindex, target)
            if attackindex != "wep_poetry_leaf":
                $ store.consumable_inventory[attackindex] = store.consumable_inventory.get(attackindex, 0) - 1
                if store.consumable_inventory.get(attackindex, 0) <= 0:
                    $ store.consumable_inventory.pop(attackindex, None)
        elif is_enemy_target and hasattr(store, "apply_consumable_all_effects"):
            $ item_used = store.apply_consumable_all_effects(target, attackindex)
            if item_used:
                $ store.consumable_inventory[attackindex] = store.consumable_inventory.get(attackindex, 0) - 1
                if store.consumable_inventory.get(attackindex, 0) <= 0:
                    $ store.consumable_inventory.pop(attackindex, None)
                # Пассивка Фроглин «Делёжка» должна срабатывать и тогда,
                # когда расходник с маной используют на враге (например,
                # мороженое на самой Фроглин), а не только на союзниках.
                if hasattr(store, "frog_on_consumable_used"):
                    $ _frog_item_fx = store.get_consumable_item_effects_level1(attackindex) if hasattr(store, "get_consumable_item_effects_level1") else {}
                    $ frog_on_consumable_used(attacker, attackindex, _frog_item_fx)
        elif hasattr(target, "use_consumable"):
            $ target.use_consumable(attackindex)
        else:
            pass
            #$ renpy.notify("Предмет [attackindex] нельзя применить к цели [getattr(target, 'name', target)].")
    else:
        if isinstance(attackindex, str) and store.consumable_inventory.get(attackindex, 0) > 0:
            $ store.consumable_inventory[attackindex] = store.consumable_inventory.get(attackindex, 0) - 1
            if store.consumable_inventory.get(attackindex, 0) <= 0:
                $ store.consumable_inventory.pop(attackindex, None)
        #$ renpy.notify("Не выбраны предмет или цель.")

    $ compact_consumable_inventory_after_stack_depleted()





    $ prepare_turn_effect_target(target)
    
        # ── ПРАВИЛЬНЫЙ ПОКАЗ ──
    # Сначала гарантированно убираем всё, что могло остаться
    hide screen heroes_attacked_visual
    hide screen attacked_compiled_heroturn
    hide screen clear_visual


    show screen attacked_compiled_heroturn
    #show screen heroes_attacked_visual
    #hide screen clear_visual
    
    $ renpy.pause(0.7, hard=True)
    if hasattr(attacker, "state"):
        $ attacker.state = "item2"
    $ renpy.pause(1 , hard=True)
    if hasattr(attacker, "state"):
        $ attacker.state = "idle"

    hide screen heroes_attacked_visual
    hide screen attacked_compiled_heroturn
    hide screen clear_visual

    $ attacker.turn = 1
    # «Причина ошибок»: использование предмета Крисом тоже может дать доп. ход.
    $ kris_apply_action_turn_for_current()


    $ attacker.step_forward = 2
    $ itemchoice = 0
    #$ target.damage_gain_for_vis = 0
    $ target = None

    
    call screen choose_attacker_screen()




label item_dialogue:


    if attackindex == "food_clubsandwich":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_sans_sandwich":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_banana":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_lucky_monstercandy":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_icecream":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_readymeal_1":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_readymeal_2":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_readymeal_3":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_cookiesharing":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_pepperoni":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_mint_gum":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_lottery_candy":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_colacoffee":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_tonic":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_crab_apple":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_diet_salad":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_broccoli":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_noodles":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_sparkling_water":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_still_water":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "food_frenchfries":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_water_pistol":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_water_bomb":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_toothpick":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_rubber_band":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_paper_shooter":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_ruler":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_soap_bubbles":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_poetry_leaf":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_bath_bombs":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_constructor":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."

    elif attackindex == "wep_flashlight":
        $ item_dialogue_item_name = attackindex
        if target == store.pers_dict["Крис"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Крис."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Крис."
            else:
                "Предмет [item_dialogue_item_name] использован на Крис."
        elif target == store.pers_dict["Азриель"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Азриель."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Азриель."
            else:
                "Предмет [item_dialogue_item_name] использован на Азриель."
        elif target == store.pers_dict["Чара"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Чара."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Чара."
            else:
                "Предмет [item_dialogue_item_name] использован на Чара."
        elif target == store.pers_dict["Фриск"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Фриск."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Фриск."
            else:
                "Предмет [item_dialogue_item_name] использован на Фриск."
        elif target == store.pers_dict["Иззи"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Иззи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Иззи."
            else:
                "Предмет [item_dialogue_item_name] использован на Иззи."
        elif target == store.pers_dict["Кловер"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Кловер."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Кловер."
            else:
                "Предмет [item_dialogue_item_name] использован на Кловер."
        elif target == store.pers_dict["Седрик"]:
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Седрик."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Седрик."
            else:
                "Предмет [item_dialogue_item_name] использован на Седрик."
        elif target == store.enemies.get("Арчи"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Арчи."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Арчи."
            else:
                "Предмет [item_dialogue_item_name] использован на Арчи."
        elif target == store.enemies.get("Тревор"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Тревор."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Тревор."
            else:
                "Предмет [item_dialogue_item_name] использован на Тревор."
        elif target == store.enemies.get("ДжевилV1"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на ДжевилV1."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на ДжевилV1."
            else:
                "Предмет [item_dialogue_item_name] использован на ДжевилV1."
        elif target == store.enemies.get("Психолог"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Психолог."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Психолог."
            else:
                "Предмет [item_dialogue_item_name] использован на Психолог."
        elif target == store.enemies.get("Спамтон"):
            if current_attacker == store.pers_dict["Крис"]:
                "Крис использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Азриель"]:
                "Азриель использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Чара"]:
                "Чара использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Фриск"]:
                "Фриск использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Иззи"]:
                "Иззи использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Кловер"]:
                "Кловер использует [item_dialogue_item_name] на Спамтон."
            elif current_attacker == store.pers_dict["Седрик"]:
                "Седрик использует [item_dialogue_item_name] на Спамтон."
            else:
                "Предмет [item_dialogue_item_name] использован на Спамтон."
        else:
            "Цель для предмета не выбрана."
    else:
        "Для этого предмета нет отдельного диалога."

    return
