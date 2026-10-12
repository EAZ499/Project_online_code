# ============================================================
# СИЛЬВИЯ — эффекты танцев
# ============================================================
#
# Здесь собраны функции эффектов десяти танцев. Лейблы в
# 1_ПЕРС_АТАКИ_ЛЕЙБЛЫ.rpy вызывают эти функции, чтобы не
# дублировать формулы между диспетчером, меню и подсказками.
#
# Общие правила проекта, которые здесь соблюдаются:
#   - дебаффы накладываются через entity.debuff(prefix, value);
#   - массовые эффекты идут только по живым активным врагам
#     текущего боя (store.active_enemies), не по всему store.enemies;
#   - урон не вычитается дважды: там, где используется общий
#     механизм, HP меняет только он.
# ============================================================

init python:

    # ------------------------------------------------------------
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ------------------------------------------------------------

    def sylvia_living_enemies():
        """
        Живые активные противники текущего боя.

        В проекте участвующие враги определяются функцией
        get_active_enemies() (1_ВЫБОР_ЦЕЛИ.rpy); store.active_enemies
        не существует, поэтому обращаемся именно к функции.
        """
        if "get_active_enemies" not in globals():
            return []
        enemies_dict = getattr(store, "enemies", None) or {}
        result = []
        for enemy_name in get_active_enemies():
            enemy = enemies_dict.get(enemy_name)
            if enemy is None:
                continue
            if getattr(enemy, "dead", False):
                continue
            if getattr(enemy, "current_hp", 0) <= 0:
                continue
            result.append(enemy)
        return result

    def sylvia_party_members():
        """Живые участники команды."""
        result = []
        pers = getattr(store, "pers_dict", None) or {}
        for char in pers.values():
            if getattr(char, "picked", 0) != 1:
                continue
            if getattr(char, "current_hp", 0) <= 0:
                continue
            result.append(char)
        return result

    def _sylvia_heal(char, percent):
        """Восстанавливает процент от максимального HP персонажу."""
        if char is None:
            return 0
        max_hp = int(getattr(char, "max_hp", 0) or 0)
        heal = int(max_hp * percent)
        if heal <= 0:
            return 0
        before = int(getattr(char, "current_hp", 0) or 0)
        char.current_hp = min(max_hp, before + heal)
        return int(char.current_hp) - before

    def _sylvia_team_def_buff(char, percent):
        """
        Выдаёт процент защиты участнику команды.
        bonus_def — МНОЖИТЕЛЬ к базовой защите (Pers.defense:
        base_def * bonus_def), поэтому проценты переводим в доли.
        Для Сильвии применяется «Искусство для себя» (ур.9): она
        получает собственный бафф на 30% сильнее.
        """
        if char is None:
            return
        share = percent / 100.0
        if getattr(char, "name", None) == "Сильвия":
            extra = sylvia_self_buff_multiplier()
            if extra > 0.0:
                share *= extra
        char.bonus_def = float(getattr(char, "bonus_def", 0.0) or 0.0) + share

    def _sylvia_restore_mp(char, percent):
        """Восстанавливает процент от максимальной маны персонажу."""
        if char is None:
            return 0
        max_mp = int(getattr(char, "max_mp", 0) or 0)
        restore = int(max_mp * percent)
        if restore <= 0:
            return 0
        before = int(getattr(char, "current_mp", 0) or 0)
        char.current_mp = min(max_mp, before + restore)
        return int(char.current_mp) - before

    def sylvia_apply_effects_twice(effect_func):
        """
        Обёртка «Громкого финала» (ур.10): с шансом, равным крит-шансу,
        эффекты танца применяются дважды.
        """
        effect_func()
        if sylvia_roll_loud_finale():
            effect_func()


    # ------------------------------------------------------------
    # 1) «КАПРИЗ КИТРИ»
    #    Plié -> Relevé -> Dégagé -> Фуэте
    #    Даёт Сильвии +1 щит.
    # ------------------------------------------------------------

    def sylvia_dance_kitri():
        char = sylvia_char()
        if char is None:
            return
        char.shield = int(getattr(char, "shield", 0) or 0) + 1
        renpy.log("Сильвия: «Каприз Китри» — +1 щит")

    # ------------------------------------------------------------
    # 2) «ВИДЕНИЕ ДУЛЬСИНЕИ»
    #    Tombé -> Chassé -> Saut de basque -> Grand jeté
    #    Следующая атака всех союзников нанесёт на 30% больше.
    # ------------------------------------------------------------

    def sylvia_dance_dulcinea():
        for char in sylvia_party_members():
            # Используем СУЩЕСТВУЮЩИЙ механизм проекта:
            # Pers.next_attack_multiplier сам расходуется в calculate_dmg
            # и сбрасывается в 1.0 после удара. Второй флаг не нужен —
            # это был бы второй источник истины для одного состояния.
            char.next_attack_multiplier = 1.30
            # «Искусство для себя» (ур.9): Сильвия получает свой бафф на 30% сильнее.
            if getattr(char, "name", None) == "Сильвия":
                extra = sylvia_self_buff_multiplier()
                if extra > 0.0:
                    char.next_attack_multiplier = 1.30 * extra
        renpy.log("Сильвия: «Видение Дульсинеи» — +30% к следующей атаке команды")

    def sylvia_wings_bonus(char):
        """
        «Крылья птицы» (x3): атаки команды наносят дополнительно 50%
        урона от магии. Возвращает добавку к урону, не расходуя стак.
        """
        if char is None:
            return 0
        if int(getattr(char, "sylvia_wings", 0) or 0) <= 0:
            return 0
        return int(float(getattr(char, "magic", 0) or 0) * 0.50)

    def sylvia_amur_flame_damage(char):
        """
        «Пламя Амура» (x4): 40% урона от магии по всем противникам.
        Возвращает величину урона за одно срабатывание.
        """
        if char is None:
            return 0
        if int(getattr(char, "sylvia_amur_flame", 0) or 0) <= 0:
            return 0
        return int(float(getattr(char, "magic", 0) or 0) * 0.40)

    # ------------------------------------------------------------
    # 3) «ТЕНЬ СОЛОРА»
    #    Tombé -> Passé -> Developpé -> Attitude
    #    Бафф «Тень Солора» (x2). Персонажи не могут ходить, но
    #    восстанавливают 20% HP и маны за ход. Их танк = 0.
    # ------------------------------------------------------------

    def sylvia_dance_solor():
        for char in sylvia_party_members():
            char.sylvia_solor_shadow = 2
            # Персонаж не может действовать.
            char.turn = 0
            # Танк обнуляется на время эффекта.
            char.sylvia_solor_saved_tank = float(getattr(char, "bonus_tank", 0) or 0)
            char.bonus_tank = 0
        renpy.log("Сильвия: «Тень Солора» — команда обездвижена, но regenerates 20%")

    def sylvia_solor_tick():
        """Тик «Тени Солора»: восстановление HP/MP и снятие эффекта."""
        for char in sylvia_party_members():
            stacks = int(getattr(char, "sylvia_solor_shadow", 0) or 0)
            if stacks <= 0:
                continue
            _sylvia_heal(char, 0.20)
            _sylvia_restore_mp(char, 0.20)
            stacks -= 1
            char.sylvia_solor_shadow = stacks
            if stacks <= 0:
                # Возвращаем танк, когда эффект спадает.
                saved = float(getattr(char, "sylvia_solor_saved_tank", 0.0) or 0.0)
                char.bonus_tank = int(getattr(char, "bonus_tank", 0) or 0) + int(saved)
                char.sylvia_solor_saved_tank = 0.0

    # ------------------------------------------------------------
    # 4) «СИНЯЯ ПТИЦА»
    #    Plié -> Glissade -> Échappé sauté -> Brisé
    #    «Крылья птицы» (x3). Атаки команды наносят дополнительно
    #    50% урона от магии.
    # ------------------------------------------------------------

    def sylvia_dance_bluebird():
        for char in sylvia_party_members():
            char.sylvia_wings = 3
        # «Искусство для себя» (ур.9): Сильвия получает собственный
        # командный бафф сильнее на 30%.
        _sylvia = sylvia_char()
        if _sylvia is not None:
            extra = sylvia_self_buff_multiplier()
            if extra > 0.0:
                _sylvia.sylvia_wings = int(round(3 * extra))
        renpy.log("Сильвия: «Синяя птица» — «Крылья птицы» x3")

    # ------------------------------------------------------------
    # 5) «ДЫХАНИЕ ЖИЗЕЛИ»
    #    Plié -> Relevé -> Developpé -> Arabesque
    #    Снимает дебаффы страха, восстанавливает 15% HP,
    #    даёт команде 20% защиты.
    # ------------------------------------------------------------

    def sylvia_dance_gisele():
        for char in sylvia_party_members():
            # Страх в проекте — положительный accuracy_debuff.
            if getattr(char, "accuracy_debuff", 0) > 0:
                char.accuracy_debuff = 0
            _sylvia_heal(char, 0.15)
            # +20% защиты команде; для Сильвии — сильнее (ур.9).
            _sylvia_team_def_buff(char, 20.0)
        renpy.log("Сильвия: «Дыхание Жизели» — снят страх, +15% HP, +20% защиты")

    # ------------------------------------------------------------
    # 6) «КАВАЛЕРСКИЙ КРУГ ДЕЗИРЕ»
    #    Tombé -> Chassé -> Saut de basque -> Tour en l'air
    #    Умножает бонусный крит-урон персонажа с самым высоким
    #    значением на 1.5.
    # ------------------------------------------------------------

    def sylvia_dance_desire():
        members = sylvia_party_members()
        if not members:
            return
        best = max(members, key=lambda c: float(getattr(c, "crit", 1.0) or 1.0))
        # У Pers свойство crit доступно только для чтения, поэтому
        # множитель применяем через bonus_crit — отдельный аддитивный
        # вклад в крит-урон, у которого есть сеттер.
        current = float(getattr(best, "crit", 1.0) or 1.0)
        best.bonus_crit = float(getattr(best, "bonus_crit", 0.0) or 0.0) + (current * 0.5)
        renpy.log(f"Сильвия: «Кавалерский круг Дезире» — крит-урон {best.name} x1.5")

    # ------------------------------------------------------------
    # 7) «ИСКРЫ АМУРА»
    #    Plié -> Glissade -> Changement de pieds -> Temps levé
    #    «Пламя Амура» (x4). Каждый персонаж наносит всем
    #    противникам 40% урона от своей магии.
    # ------------------------------------------------------------

    def sylvia_dance_amur():
        members = sylvia_party_members()
        enemies = sylvia_living_enemies()
        # «Важность исполнения»: эффекты движения делятся на 2 при провале
        # точности и умножаются на 1.5 при крите.
        perf = sylvia_performance_modifier()
        for char in members:
            char.sylvia_amur_flame = 4
            magic = float(getattr(char, "magic", 0) or 0)
            damage = int(magic * 0.40 * perf)
            if damage <= 0:
                continue
            for enemy in enemies:
                # Проект вычитает HP напрямую; общего take_damage нет.
                enemy.current_hp = max(0, int(getattr(enemy, "current_hp", 0) or 0) - damage)
                add_attack_result(char.name, enemy.name, damage, False, "normal")
        renpy.log("Сильвия: «Искры Амура» — «Пламя Амура» x4")

    # ------------------------------------------------------------
    # 8) «ВИНТ СПАРТАКА»
    #    Tombé -> Chassé -> Jeté entrelacé -> Pirouette à la seconde
    #    Прибавка к бонусной атаке команде. Все персонажи наносят
    #    всем противникам урон = 30% от текущей атаки.
    # ------------------------------------------------------------

    def sylvia_dance_spartacus():
        members = sylvia_party_members()
        enemies = sylvia_living_enemies()
        # «Важность исполнения» применяется к эффекту движения.
        perf = sylvia_performance_modifier()
        for char in members:
            atk = float(getattr(char, "atk", 0) or 0)
            # bonus_atk — МНОЖИТЕЛЬ к базовой атаке (Pers.atk:
            # base_atk * bonus_atk), поэтому прибавку 30% пишем как 0.30,
            # а не как абсолютные очки (иначе атака выросла бы в 30 раз).
            char.bonus_atk = float(getattr(char, "bonus_atk", 0.0) or 0.0) + (0.30 * perf)
            damage = int(atk * 0.30 * perf)
            if damage <= 0:
                continue
            for enemy in enemies:
                enemy.current_hp = max(0, int(getattr(enemy, "current_hp", 0) or 0) - damage)
                add_attack_result(char.name, enemy.name, damage, False, "normal")
        renpy.log("Сильвия: «Винт Спартака» — +30% атаки и массовый урон")

    # ------------------------------------------------------------
    # 9) «ДИНАМИКА ГАМЗАТТИ»
    #    Tombé -> Glissade -> Échappé sauté -> Cabriole
    #    Накладывает всем персонажам точность x4.
    # ------------------------------------------------------------

    def sylvia_dance_gamzatti():
        for char in sylvia_party_members():
            char.sylvia_precision_stacks = 4
            base = float(getattr(char, "dmgchance", 0.0) or 0.0)
            char.dmgchance_mod = float(getattr(char, "dmgchance_mod", 0.0) or 0.0) + base * 3.0
        renpy.log("Сильвия: «Динамика Гамзатти» — точность x4")

    # ------------------------------------------------------------
    # 10) «КАНТИЛЕНА БЕЛОГО ЛЕБЕДЯ»
    #     Plié -> Relevé -> Battement fondu -> Temps lié
    #     Сбрасывает штрафные характеристики и дебаффы,
    #     восстанавливает 30% HP всей команде.
    # ------------------------------------------------------------

    def sylvia_dance_swan():
        for char in sylvia_party_members():
            # Снятие всех дебаффов-штрафов по допустимым префиксам.
            for prefix in ("bloodshed", "prone", "atk", "def", "magic",
                           "accuracy", "critrate", "critdmg", "tank"):
                attr = prefix + "_debuff"
                if getattr(char, attr, 0):
                    setattr(char, attr, 0)
            # Сброс штрафных бонусных характеристик, если они отрицательные.
            for attr in ("bonus_atk", "bonus_def", "bonus_magic", "bonus_dmgchance",
                         "bonus_critrate", "bonus_crit", "bonus_tank"):
                value = getattr(char, attr, 0)
                if isinstance(value, (int, float)) and value < 0:
                    setattr(char, attr, 0)
            _sylvia_heal(char, 0.30)
        renpy.log("Сильвия: «Кантилена Белого лебедя» — сняты дебаффы, +30% HP")


    # ------------------------------------------------------------
    # РЕЕСТР: id танца -> функция эффекта
    # ------------------------------------------------------------

    SYLVIA_DANCE_EFFECTS = {
        "kitri":     sylvia_dance_kitri,
        "dulcinea":  sylvia_dance_dulcinea,
        "solor":     sylvia_dance_solor,
        "bluebird":  sylvia_dance_bluebird,
        "gisele":    sylvia_dance_gisele,
        "desire":    sylvia_dance_desire,
        "amur":      sylvia_dance_amur,
        "spartacus": sylvia_dance_spartacus,
        "gamzatti":  sylvia_dance_gamzatti,
        "swan":      sylvia_dance_swan,
    }

    def sylvia_run_dance_effect(dance_id):
        """
        Запускает эффект танца. Учитывает:
          - «Важность исполнения» (ур.1): множитель эффектов от проверки
            точности/крита, выполненной при выборе движения;
          - «Громкий финал» (ур.10): с шансом, равным крит-шансу,
            эффекты танца применяются дважды.
        Возвращает True, если эффект был выполнен.
        """
        effect = SYLVIA_DANCE_EFFECTS.get(dance_id)
        if effect is None:
            renpy.log(f"Сильвия: неизвестный танец '{dance_id}'")
            return False
        sylvia_apply_effects_twice(effect)
        return True


    # ------------------------------------------------------------
    # ТИК ДЛИТЕЛЬНЫХ ЭФФЕКТОВ СИЛЬВИИ
    # ------------------------------------------------------------
    # «Крылья птицы» (x3), «Пламя Амура» (x4) и точность (x4) держатся
    # заданное число ходов. Уменьшаем счётчики в конце раунда, иначе
    # флаги остались бы навсегда (и были бы «мёртвыми» переменными).

    def sylvia_tick_team_effects():
        """Уменьшает счётчики длительных баффов команды на 1 за раунд."""
        for char in sylvia_party_members():
            # Точность x4: убираем выданную ранее добавку к dmgchance_mod.
            stacks = int(getattr(char, "sylvia_precision_stacks", 0) or 0)
            if stacks > 0:
                base = float(getattr(char, "base_dmgchance", 0.0) or 0.0)
                # За каждый ход снимаем одну «базовую» долю добавки.
                char.dmgchance_mod = max(0.0,
                    float(getattr(char, "dmgchance_mod", 0.0) or 0.0) - base)
                char.sylvia_precision_stacks = stacks - 1

            # «Пламя Амура» (x4): пока бафф активен, персонаж наносит
            # всем противникам 40% урона от своей магии за раунд.
            if int(getattr(char, "sylvia_amur_flame", 0) or 0) > 0:
                _burn = sylvia_amur_flame_damage(char)
                if _burn > 0:
                    for enemy in sylvia_living_enemies():
                        enemy.current_hp = max(0, int(getattr(enemy, "current_hp", 0) or 0) - _burn)
                        add_attack_result(char.name, enemy.name, _burn, False, "magic")

            for field in ("sylvia_wings", "sylvia_amur_flame"):
                value = int(getattr(char, field, 0) or 0)
                if value > 0:
                    setattr(char, field, value - 1)
