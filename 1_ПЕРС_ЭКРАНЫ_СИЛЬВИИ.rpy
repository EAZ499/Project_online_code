# ============================================================
# СИЛЬВИЯ — ЭКРАНЫ
# ============================================================
#
# 1) sylvia_repertoire_screen — выбор до 3 танцев в начале боя
#    (только если уровень персонажа >= SYLVIA_REPERTOIRE_CHOICE_LEVEL).
# 2) sylvia_movement_screen   — выбор одного движения танца.
#
# Оба экрана используют данные из 1_ПЕРС_ПАССИВКИ_СИЛЬВИИ.rpy,
# чтобы не дублировать списки движений и танцев.
# ============================================================


# ------------------------------------------------------------
# ЭКРАН ВЫБОРА РЕПЕРТУАРА
# ------------------------------------------------------------
# Показывается один раз на первом ходу Сильвии, если её уровень
# не ниже порога. Игрок выбирает до трёх танцев; повтор танца в
# бою запрещён, поэтому выбранный набор — это её «программа».

screen sylvia_repertoire_screen():
    modal True
    zorder 999999999

    default _selected = []

    add Solid("#000000cc")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 12

        text "Выберите репертуар танца":
            size 42
            color "#ffffff"
            xalign 0.5

        text "До %d танцев. Выбранный танец исполняется один раз за бой." % SYLVIA_REPERTOIRE_SIZE:
            size 22
            color "#aaaaaa"
            xalign 0.5

        null height 10

        # Сетка танцев: название и комбинация движений.
        grid 2 5:
            spacing 10
            xalign 0.5

            for _dance_id in sylvia_all_dance_ids():
                $ _dance = SYLVIA_DANCES[_dance_id]
                $ _combo_text = " → ".join([sylvia_movement_name(m) for m in _dance["combo"]])
                $ _is_selected = _dance_id in _selected

                button:
                    xysize (560, 84)
                    background ("#3a5a8a" if _is_selected else "#1a1a2a")
                    action If(
                        _is_selected,
                        SetScreenVariable("_selected", [d for d in _selected if d != _dance_id]),
                        If(
                            len(_selected) < SYLVIA_REPERTOIRE_SIZE,
                            SetScreenVariable("_selected", _selected + [_dance_id]),
                            NullAction(),
                        ),
                    )

                    vbox:
                        spacing 2
                        xpos 10
                        ypos 6

                        $ _mark = "[✓] " if _is_selected else ""
                        text _mark + _dance["name"]:
                            size 24
                            color ("#ffffff" if _is_selected else "#cccccc")
                        text _combo_text:
                            size 16
                            color "#9fd4ff"
                        text _dance["desc"]:
                            size 14
                            color "#999999"

        null height 12

        hbox:
            spacing 20
            xalign 0.5

            textbutton "Подтвердить":
                text_size 28
                sensitive (len(_selected) > 0)
                action [
                    Function(_sylvia_confirm_repertoire, _selected),
                    Hide("sylvia_repertoire_screen"),
                ]

            text "выбрано: [len(_selected)] / %d" % SYLVIA_REPERTOIRE_SIZE:
                size 22
                color "#aaaaaa"
                yalign 0.5


init python:

    def _sylvia_confirm_repertoire(selected):
        """Сохраняет выбранный репертуар в объект персонажа."""
        char = sylvia_char()
        if char is None:
            return
        char.sylvia_repertoire = list(selected)
        char.sylvia_repertoire_chosen = True
        renpy.log("Сильвия: репертуар выбран — {}".format(
            ", ".join([sylvia_dance_name(d) for d in selected])))

    def sylvia_ensure_repertoire():
        """
        Гарантирует, что репертуар задан.
        Если уровень ниже порога — берётся автоматический набор
        (танцы первых трёх уровней), как требует спецификация.
        Возвращает True, если нужно показать экран выбора.
        """
        char = sylvia_char()
        if char is None:
            return False

        if getattr(char, "sylvia_repertoire_chosen", False):
            return False

        if sylvia_level() >= SYLVIA_REPERTOIRE_CHOICE_LEVEL:
            # Игрок выбирает сам — показываем экран.
            return True

        # Уровень ниже порога: набор берётся автоматически.
        char.sylvia_repertoire = sylvia_dances_for_level(sylvia_level())
        char.sylvia_repertoire_chosen = True
        renpy.log("Сильвия: репертуар задан автоматически (уровень ниже порога)")
        return False


# ------------------------------------------------------------
# ЭКРАН ВЫБОРА ДВИЖЕНИЯ
# ------------------------------------------------------------
# Доступны все движения текущего открытого уровня и ниже.
# Показывает очередь, текущий танец-кандидат и стоимость маны.

screen sylvia_movement_screen():
    modal True
    zorder 99999998

    $ _char = sylvia_char()
    $ _queue = sylvia_queue_names()
    $ _available = sylvia_available_movements()
    $ _cost = sylvia_movement_cost()
    $ _mp = int(getattr(_char, "current_mp", 0) or 0) if _char else 0
    $ _tier = sylvia_current_tier()

    add Solid("#000000dd")

    vbox:
        xalign 0.5
        ypos 40
        spacing 8

        text "Движение танца":
            size 36
            color "#ffffff"
            xalign 0.5

        text "Уровень движений: %d  |  Мана: %d (движение — %d)  |  Ходов до сброса прогресса: %d" % (
                _tier, _mp, _cost, SYLVIA_TIER_PROGRESS_MAX - int(sylvia_get("sylvia_progress_steps", 0) or 0)):
            size 20
            color "#aaaaaa"
            xalign 0.5

        # Очередь движений: что игрок уже набрал.
        text "Очередь: " + (" → ".join(_queue) if _queue else "(пусто)"):
            size 22
            color ("#9fd4ff" if _queue else "#666666")
            xalign 0.5

        null height 6

        # Сетка доступных движений.
        # vpgrid с фиксированным числом колонок допускает ЛЮБОЕ число
        # детей: на ур.1 движений 2, на ур.4 — 30. Обычный grid 4 4
        # требовал бы ровно 16 и падал бы на низких уровнях.
        vpgrid:
            cols 4
            spacing 10
            xalign 0.5
            ysize 340
            draggable True
            mousewheel True

            for _mid in _available:
                $ _mname = sylvia_movement_name(_mid)

                button:
                    xysize (280, 60)
                    background "#1a1a2a"
                    hover_background "#2a3a5a"
                    sensitive (_mp >= _cost)
                    action [
                        SetVariable("sylvia_pending_move", _mid),
                        Hide("sylvia_movement_screen"),
                        Jump("sylvia_movement_is_done"),
                    ]

                    text _mname:
                        size 20
                        color "#ffffff"
                        xalign 0.5
                        yalign 0.5

        null height 8

        # Подсказка про репертуар.
        text "Репертуар: " + ", ".join([sylvia_dance_name(d) for d in (sylvia_get("sylvia_repertoire", []) or [])]):
            size 18
            color "#88aa88"
            xalign 0.5

        textbutton "Назад":
            text_size 24
            xalign 0.5
            action [Hide("sylvia_movement_screen"), Jump("playerturn2")]
