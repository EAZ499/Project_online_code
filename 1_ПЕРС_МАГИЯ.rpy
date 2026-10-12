screen Heromagics(): 
    timer 0.01 action Jump("Remove_screens")

    #if attackindex == "Krismag1":
    
    #elif attackindex == "greenheal":
    #    use green_choose_target_to_cook


    #imagebutton:
    #    idle "images/button_idle.png"
    #    hover "images/button_hover.png"
    #    action [Jump("atk1_is_done")]


#screen Heromagics2(): 
#    if attackindex == "greenheal":
#        if healindex == 1: # Посмотри список магии персонажей



# ============================================================================
# ФУНКЦИИ МАГИИ ПЕРСОНАЖЕЙ
# ============================================================================
# В этом модуле собраны функции применения магии для разных персонажей.
# Они используют систему бонусов/дебафов, уже принятую в проекте:
# - Мультипликативные бонусы: bonus_atk, bonus_magic, bonus_def (1.0 = 100%)
# - Аддитивные бонусы: bonus_dmgchance, bonus_critrate, bonus_crit (0 = 0%)
# - Спец-флаги на персонаже: next_ignore_armor, next_guaranteed_crit и др.
# Для логирования урона в общую систему используется add_attack_result(...).
# ============================================================================

init  python:

    import random

    # ------------------------------------------------------------------------
    # Вспомогательные функции
    # ------------------------------------------------------------------------
    def ensure_combat_flags(char):
        """Гарантирует наличие на персонаже временных боевых флагов."""
        if not hasattr(char, 'next_ignore_armor'):
            char.next_ignore_armor = False
        if not hasattr(char, 'next_guaranteed_crit'):
            char.next_guaranteed_crit = False
        if not hasattr(char, 'fear_state'):
            char.fear_state = False
        if not hasattr(char, 'magic_only_limit'):
            char.magic_only_limit = False
        if not hasattr(char, 'karma_reflect'):
            char.karma_reflect = False

    def log_magic_damage(attacker, target, dmg, is_crit=False):
        """Логирует магический урон в новую систему отображения."""
        if dmg > 0 and target is not None:
            try:
                store.add_attack_result(attacker.name, target.name, int(dmg), bool(is_crit), "magic")
            except Exception:
                # Безопасность на случай, если система ещё не инициализирована
                pass

    # ------------------------------------------------------------------------
    # ЧАРА — МАГИЯ
    # ------------------------------------------------------------------------
    def chara_mag_gnev(chara):
        """Гнев — увеличить атаку на 20%."""
        ensure_combat_flags(chara)
        chara.bonus_atk += 0.20
        renpy.log("Чара: +20% атака")

    def chara_mag_bezumie(chara):
        """Безумие — увеличить шанс крита на 20%."""
        ensure_combat_flags(chara)
        chara.bonus_critrate += 0.20
        renpy.log("Чара: +20% шанс крита")

    def chara_mag_sumasshestvie(chara):
        """Сумасшествие — увеличить крит. урон на 30%."""
        ensure_combat_flags(chara)
        chara.bonus_crit += 0.30
        renpy.log("Чара: +30% крит. урон")

    def chara_mag_psih_next_crit(chara):
        """Псих — следующая атака критует на 100%."""
        ensure_combat_flags(chara)
        chara.next_guaranteed_crit = True
        renpy.log("Чара: следующая атака — гарантированный крит")

    def chara_mag_moral_decomposition(chara):
        """Моральное разложение — броня цели игнорируется в следующей атаке."""
        ensure_combat_flags(chara)
        chara.next_ignore_armor = True
        renpy.log("Чара: следующая атака игнорирует броню")

    def chara_mag_awaken_past(chara, target):
        """Пробуждение прошлого — 1 удар ножом с повышенным шансом крита (гарантия)
        и усиленным крит.уроном. Игнорирует защиту. После — Чара умирает.
        """
        if target is None or target.current_hp <= 0:
            renpy.log("Цель не выбрана или уже повержена")
            return
        ensure_combat_flags(chara)
        # Временные бафы только на этот удар
        chara.next_guaranteed_crit = True
        chara.next_ignore_armor = True
        chara.bonus_crit += 0.50  # +50% крит.урона на удар
        # Удар
        dmg = int(chara.calculate_dmg(target))
        target.current_hp = max(0, target.current_hp - dmg)
        log_magic_damage(chara, target, dmg, is_crit=True)
        # Откатываем добавленный крит урон (на будущее)
        chara.bonus_crit = max(chara.bonus_crit - 0.50, 0)
        # Смерть Чары
        chara.change_hp(-chara.current_hp)
        renpy.log("Чара использует 'Пробуждение прошлого' и падает замертво")

    # ------------------------------------------------------------------------
    # ФРИСК — МАГИЯ
    # ------------------------------------------------------------------------
    def frisk_mag_potentia_intellectus(frisk, target_enemy):
        """Сила разума — снижает атаку на 5% себе и врагу."""
        frisk.bonus_atk = max(frisk.bonus_atk - 0.05, 0)
        if target_enemy:
            # Проще всего применить как постоянную модификацию базовой атаки врага
            target_enemy.attack = max(0, int(round(target_enemy.attack * 0.95)))
        renpy.log("Фриск: атака -5% себе и врагу")

    def frisk_mag_quod_licet(frisk, target_enemy):
        """Снижает броню врагу на 5% и повышает себе броню и урон на 5%."""
        frisk.bonus_def += 0.05
        frisk.bonus_atk += 0.05
        if target_enemy:
            target_enemy.armor = max(0, int(round(target_enemy.armor * 0.95)))
        renpy.log("Фриск: +5% защита, +5% атака; врагу -5% брони")

    def frisk_mag_foedus_icere(frisk, target_enemy):
        """Заключить договор — если степень договорённости >= 50%, поднять до 100%."""
        if not hasattr(store, 'agreement'): store.agreement = {}
        agreement_key = target_enemy.name if target_enemy else 'unknown'
        current = store.agreement.get(agreement_key, 0)
        if current >= 50:
            store.agreement[agreement_key] = 100
            renpy.log("Фриск: договорённость доведена до максимума")
        else:
            renpy.log("Фриск: договорённость слишком низкая")

    def frisk_mag_do_ut_des(frisk, target_enemy):
        """Я даю, чтобы ты дал — хилит врага на 200, всю команду на 400."""
        # Используем централизованную функцию для инициализации team_manager
        store.ensure_team_manager()
            
        # Враг
        if target_enemy:
            target_enemy.current_hp = min(target_enemy.max_hp, target_enemy.current_hp + 200)
        # Команда
        for slot in store.team_manager.team_slots:
            if slot and slot in store.characters:
                store.pers_dict[slot].change_hp(int(store.pers_dict[slot].max_hp * 0) + 400)  # плоско 400
        renpy.log("Фриск: враг +200 HP, команда +400 HP")

    def frisk_mag_save_determination(frisk):
        """Сохранение решимости — если кто-то из людей умер, воскресить на 150% HP."""
        revived = 0
        for name in ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер"]:
            if name in store.characters:
                c = store.pers_dict[name]
                if c.current_hp <= 0:
                    c.current_hp = int(c.max_hp * 1.5)
                    revived += 1
        renpy.log("Фриск: воскрешено: %d" % revived)

    # ------------------------------------------------------------------------
    # ИЗЗИ — МАГИЯ
    # ------------------------------------------------------------------------
    def izzy_mag_predvidenie(izzy):
        """Предвидение — уменьшает скорость пуль (стек), -20% HP."""
        izzy.change_hp(-int(izzy.max_hp * 0.20))
        if not hasattr(store, 'predvidenie_stacks'):
            store.predvidenie_stacks = 0
        store.predvidenie_stacks += 1
        renpy.log("Иззи: Предвидение (+стек), -20% HP")

    def izzy_mag_oskolok_sebya(izzy, target_enemy):
        """Осколок себя — запускает мини-игру саймон для усиления атаки."""
        if target_enemy is None:
            renpy.log("Цель не выбрана")
            return
        # Сохраняем цель для использования после мини-игры
        store.oskolok_sebya_target = target_enemy
        # Запускаем мини-игру саймон
        store.simon_game.start_game(3)  # Начинаем с сложности 3

    def izzy_mag_uspokoenie(izzy, ally_char):
        """Успокоение — снимает дебафы союзника. Стоимость: -5% HP Иззи."""
        if ally_char is None:
            renpy.log("Союзник не выбран")
            return
        ally_char.bloodshed_debuff = 0
        ally_char.prone_debuff = 0
        ally_char.atk_debuff = 0
        ally_char.def_debuff = 0
        ally_char.magic_debuff = 0
        ally_char.accuracy_debuff = 0
        ally_char.critrate_debuff = 0
        ally_char.critdmg_debuff = 0
        izzy.change_hp(-int(izzy.max_hp * 0.05))
        renpy.log("Иззи: Успокоение — дебафы сняты, -5% HP")

    def izzy_mag_meditaciya(izzy):
        """Медитация — +30% MP. С 2 ур. 40% шанс удвоить восстановление."""
        mp_gain = int(izzy.max_mp * 0.30)
        # Открытие чакр (ур.2): шанс х2
        if izzy.level >= 2 and random.random() < 0.40:
            mp_gain *= 2
        izzy.current_mp = min(izzy.max_mp, izzy.current_mp + mp_gain)
        renpy.log("Иззи: Медитация +%d MP" % mp_gain)

    def izzy_mag_karma(izzy, ally_char):
        """Карма — отражение 100% полученного союзником урона (с учётом брони врага).
        Стоимость: -40% HP Иззи."""
        if ally_char is None:
            renpy.log("Союзник не выбран")
            return
        ensure_combat_flags(ally_char)
        ally_char.karma_reflect = True
        izzy.change_hp(-int(izzy.max_hp * 0.40))
        renpy.log("Иззи: Карма наложена на %s" % ally_char.name)

    def izzy_mag_zacharovanie(izzy, ally_char):
        """Зачарование — увеличить силу атаки союзника. Стоимость: -40% HP Иззи.
        Формула упрощена: +20% мультипликативно."""
        if ally_char is None:
            renpy.log("Союзник не выбран")
            return
        ally_char.bonus_atk += 0.20
        izzy.change_hp(-int(izzy.max_hp * 0.40))
        renpy.log("Иззи: %s получает +20% атаки" % ally_char.name)

    def izzy_mag_probuzhdenie(izzy, target_enemy):
        """Пробуждение — 3 удара, гарант. крит, игнор брони; затем страх: только
        Медитация и Успокоение доступны пока страх не снят отдельными умениями."""
        if target_enemy is None:
            renpy.log("Цель не выбрана")
            return
        total = 0
        for i in range(3):
            izzy.next_ignore_armor = True
            izzy.next_guaranteed_crit = True
            # Усилим критический урон чуть выше
            izzy.bonus_crit += 0.30
            dmg = int(izzy.calculate_dmg(target_enemy))
            target_enemy.current_hp = max(0, target_enemy.current_hp - dmg)
            total += dmg
            log_magic_damage(izzy, target_enemy, dmg, True)
            izzy.bonus_crit = max(izzy.bonus_crit - 0.30, 0)
            if target_enemy.current_hp <= 0:
                break
        # Накладываем страх/ограничение
        izzy.fear_state = True
        izzy.magic_only_limit = True
        renpy.log("Иззи: Пробуждение — урон %d. Наложен страх (ограничение магии)." % total)

    # ------------------------------------------------------------------------
    # КЛОВЕР — МАГИЯ ОРУЖИЯ
    # ------------------------------------------------------------------------
    def clover_mag_set_caliber(clover, caliber):
        """Сменить калибр ('low'|'middle'|'high')."""
        if clover.name != "Кловер":
            return
        if caliber not in ('low', 'middle', 'high'):
            return
        clover.change_gun_caliber(caliber)
        renpy.log("Кловер: установлен калибр %s" % caliber)

    def clover_mag_dlinny_stvol(clover):
        """Длинный ствол — временно повышает точность и атаку."""
        clover.bonus_atk += 0.10
        clover.bonus_dmgchance += 0.10
        renpy.log("Кловер: Длинный ствол (+10% атака, +10% точность)")

    def clover_mag_wild_west(clover):
        """Дикий запад, Крошка! — повышенная точность и х2 число выстрелов (флаг)."""
        clover.bonus_dmgchance += 0.20
        if not hasattr(clover, 'extra_shots_mult'):
            clover.extra_shots_mult = 1
        clover.extra_shots_mult = 2
        renpy.log("Кловер: Дикий Запад — точность +20%, выстрелы x2")

    def clover_mag_russian_roulette(clover, target_enemy):
        """Русская рулетка — упрощённая заглушка: случайный урон или холостой."""
        if not target_enemy:
            renpy.log("Цель не выбрана")
            return
        bullet = random.random() < 0.33
        if bullet:
            dmg = int(clover.calculate_dmg(target_enemy) * 1.5)
            target_enemy.current_hp = max(0, target_enemy.current_hp - dmg)
            log_magic_damage(clover, target_enemy, dmg, False)
            renpy.log("Кловер: Рулетка — БАБАХ! Урон %d" % dmg)
        else:
            renpy.log("Кловер: Рулетка — щёлк... холостой")

    def clover_mag_hyper_beam(clover, target_enemy):
        """Гиперлуч — тратит все патроны (MP) и 50% HP. Наносит большой урон."""
        if not target_enemy:
            renpy.log("Цель не выбрана")
            return
        hp_cost = int(clover.max_hp * 0.50)
        clover.change_hp(-hp_cost)
        # Забираем все "пули" (MP как запас боеприпасов)
        clover.current_mp = 0
        dmg = int(max(0, clover.atk * 3.0 + clover.crit * 50 - target_enemy.armor))
        target_enemy.current_hp = max(0, target_enemy.current_hp - dmg)
        log_magic_damage(clover, target_enemy, dmg, False)
        renpy.log("Кловер: Гиперлуч — урон %d, -50%% HP, пули израсходованы" % dmg)

    def clover_mag_duel_noon(clover):
        """Дуэль в полдень — флаг контратаки при получении удара."""
        if not hasattr(clover, 'duel_counter'): clover.duel_counter = False
        clover.duel_counter = True
        renpy.log("Кловер: Дуэль в полдень — подготовка к контратаке")





screen green_choose_target_to_cook:
    $ max_port = store.cooking_manager.max_allowed_portions() if hasattr(store, 'cooking_manager') else 1
    $ cur_port = store.cooking_manager.get_total_feed_multiply() if hasattr(store, 'cooking_manager') else 0
    $ dish = getattr(store, 'attackindex', 'Блюдо')

    vbox:
        spacing 10
        xalign 0.5
        ypos 80

        text "{size=32}{color=#ffffff}Приготовление: [dish]{/color}{/size}" xalign 0.5
        text "{size=22}{color=#ffffaa}Порции: [cur_port] / [max_port]{/color}{/size}" xalign 0.5

        null height 5

        hbox:
            spacing 40
            xalign 0.5
            vbox:
                spacing 4
                text "{color=#ffffff}Животное: [store.cooking_manager.current_animal_ing] -> [store.cooking_manager.future_current_animal_ing]{/color}" size 20
                text "{color=#ffffff}Фрукты/овощи: [store.cooking_manager.current_plant_ing] -> [store.cooking_manager.future_current_plant_ing]{/color}" size 20
            vbox:
                spacing 4
                text "{color=#ffffff}Мучное: [store.cooking_manager.current_bread_ing] -> [store.cooking_manager.future_current_bread_ing]{/color}" size 20
                text "{color=#ffffff}Приправы: [store.cooking_manager.current_spices_ing] -> [store.cooking_manager.future_current_spices_ing]{/color}" size 20


screen cooking_interface():
    use green_choose_target_to_cook

    $ char_order = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик", "Сильвия"]

    vbox:
        spacing 12
        xalign 0.5
        ypos 270

        for char_name in char_order:
            if char_name in store.pers_dict and getattr(store.pers_dict[char_name], "picked", 0) == 1 and getattr(store.pers_dict[char_name], "current_hp", 0) > 0:
                $ char = store.pers_dict[char_name]
                $ amount = store.cooking_manager.feed_amount.get(char_name, 0)
                $ can_add = store.cooking_manager.can_add_portion(char_name, store.attackindex)

                hbox:
                    spacing 15
                    xalign 0.5

                    text "{size=22}[char_name]{/size}" min_width 120 xalign 0.0

                    if amount > 0:
                        textbutton "<" action Function(store.cooking_manager.remove_portion, char_name, store.attackindex):
                            text_size 24
                    else:
                        textbutton "<" action NullAction():
                            text_size 24
                            text_color "#555555"

                    text "{size=20}Сытость: [char.current_feedness]/[char.max_feedness] (+[amount]){/size}" min_width 230 xalign 0.5

                    if can_add:
                        textbutton ">" action Function(store.cooking_manager.add_portion, char_name, store.attackindex):
                            text_size 24
                    else:
                        textbutton ">" action NullAction():
                            text_size 24
                            text_color "#555555"

        null height 20

        hbox:
            spacing 50
            xalign 0.5

            if store.cooking_manager.get_total_feed_multiply() > 0:
                textbutton "Приготовить!" action [Hide("cooking_interface"), Hide("turntarget"), Jump("sedric_cook_action")]:
                    text_size 26
                    text_color "#00ff00"
            else:
                textbutton "Приготовить!" action NullAction():
                    text_size 26
                    text_color "#555555"

            textbutton "Отмена" action [Function(store.cooking_manager.cancel_cooking), Hide("cooking_interface"), Hide("turntarget"), Jump("playerturn2")]:
                text_size 26
                text_color "#ff5555"