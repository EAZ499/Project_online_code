










#   ▄████████ ▀████    ▐████▀     ███        ▄████████    ▄████████ 
#  ███    ███   ███▌   ████▀  ▀█████████▄   ███    ███   ███    ███ 
#  ███    █▀     ███  ▐███       ▀███▀▀██   ███    ███   ███    ███ 
# ▄███▄▄▄        ▀███▄███▀        ███   ▀  ▄███▄▄▄▄██▀   ███    ███ 
#▀▀███▀▀▀        ████▀██▄         ███     ▀▀███▀▀▀▀▀   ▀███████████ 
#  ███    █▄    ▐███  ▀███        ███     ▀███████████   ███    ███ 
#  ███    ███  ▄███     ███▄      ███       ███    ███   ███    ███ 
#  ██████████ ████       ███▄    ▄████▀     ███    ███   ███    █▀  
#                                           ███    ███              



define prolog_complete_meow = 0







default extra_progress_type = "Записки"


init python:
    def hide_extra_progress_descriptions():
        for scr in (
            "achievkanulldes_new", "achievkanulldes1_new",
            "achievka01des_new", "achievka02des_new", "achievka03des_new",
            "achievka04des_new", "achievka05des_new", "achievka06des_new",
            "achievka07des_new", "achievka08des_new", "achievka09des_new",
            "achievka010des_new", "achievka011des_new", "achievka012des_new",
            "achievka1des_new", "achievka2des_new", "achievka3des_new",
            "achievka4des_new", "achievka5des_new", "achievka6des_new",
            "achievka6ades_new", "achievka7des_new", "achievka8des_new",
            "collected1des_new", "collected2des_new", "collected3des_new",
            "collected1description_new", "collected2description_new", "collected3description_new",

            "clue1des_new", "clue2des_new", "clue3des_new", "clue4des_new",
        ):
            renpy.hide_screen(scr)

    def hide_optional_progress_description(hover_screen, click_screen=None):
        if hover_screen:
            renpy.hide_screen(hover_screen)
        if click_screen:
            renpy.hide_screen(click_screen)


transform extra_progress_mini_appears:
    on show:
        alpha 0.0
        yoffset 90
        easeout 0.45 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        yoffset 0
        easein 0.35 alpha 0.0 yoffset 90


screen about2():
    style_prefix "battle_menu"
    zorder 99999

    timer 0.001 action SetVariable("main_section", "other")

    key "K_ESCAPE" action [
        Hide("extra_progress_mini_screen"),
        Hide("extra_all_screen"),
        Hide("about2"),
        SetVariable("extra_type", None),
        SetVariable("extra_section", "Пролог"),
        Show("main_vbox")
    ]

    vbox:
        yoffset 70
        xoffset 5
        at save_appears
        spacing -20

        vbox:
            xalign 0.0
            spacing 10
            add "main_label_3.png" xalign 0.5 yalign 0.3 zoom 0.3
            text "{font=8bitwonder.otf}{size=25}Экстра" xalign 0.5 yalign 0.3

        vbox:
            xoffset -10
            spacing 20

            vbox:
                yalign 1.0
                xalign 0.0
                xoffset -45
                yoffset 50

                button:
                    xsize 300
                    ysize 55
                    xalign 0.5
                    if extra_type == "Прогресс":
                        text _("Прогресс") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform2
                    else:
                        text _("Прогресс") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform
                    action [
                        Hide("extra_all_screen"),
                        Function(hide_extra_progress_descriptions),
                        SetVariable("extra_section", "Пролог"),
                        SetVariable("extra_type", "Прогресс"),
                        SetVariable("extra_progress_type", "Записки"),
                        Play("test_six", "button.ogg"),
                        Show("extra_progress_mini_screen")
                    ]

                button:
                    xsize 300
                    ysize 55
                    xalign 0.5
                    if extra_type == "Музыка":
                        text _("Музыка и фоны") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform2
                    else:
                        text _("Музыка и фоны") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform
                    action [
                        Hide("extra_progress_mini_screen"),
                        Function(hide_extra_progress_descriptions),
                        SetVariable("extra_section", "Пролог"),
                        SetVariable("extra_type", "Музыка"),
                        Play("test_six", "button.ogg"),
                        Show("extra_all_screen")
                    ]

                button:
                    xsize 300
                    ysize 55
                    xalign 0.5
                    if extra_type == "Об игре":
                        text _("Об игре") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform2
                    else:
                        text _("Об игре") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform
                    action [
                        Hide("extra_progress_mini_screen"),
                        Function(hide_extra_progress_descriptions),
                        SetVariable("extra_type", "Об игре"),
                        Play("test_six", "button.ogg"),
                        Show("extra_all_screen")
                    ]

                button:
                    xsize 300
                    ysize 55
                    xalign 0.5
                    text "Назад" size 30 xalign 0.5 yalign 0.5 at main_vbox_transform
                    if extra_type is None:
                        action [Hide("extra_progress_mini_screen"), Hide("extra_all_screen"), Hide("about2"), Show("main_vbox")]
                    else:
                        action [
                            Hide("extra_progress_mini_screen"),
                            Hide("extra_all_screen"),
                            Function(hide_extra_progress_descriptions),
                            SetVariable("extra_type", None),
                            SetVariable("extra_section", "Пролог")
                        ]


screen extra_progress_mini_screen():
    zorder 999999

    key "K_ESCAPE" action [
        Hide("extra_progress_mini_screen"),
        Function(hide_extra_progress_descriptions),
        SetVariable("extra_type", None),
        SetVariable("extra_section", "Пролог")
    ]

    # ВНЕШНИЙ FRAME — белая рамка всего mini-окошка.
    frame:
        at extra_progress_mini_appears
        xpos 15
        ypos 15
        xsize 720
        ysize 660
        background "#ffffff"
        padding (7, 7)

        # ВНУТРЕННИЙ FRAME — чёрное тело mini-окна.
        frame:
            xfill True
            yfill True
            background "#000000"
            padding (18, 18)

            vbox:
                spacing 18
                xfill True
                yfill True

                # Верхняя сетка вкладок 4:2.
                # Здесь теперь 4 кнопки: Записки, Достижения, Collectibles, Улики.
                grid 3 2:
                    xalign 0.5
                    spacing 10

                    use extra_progress_tab_button("Записки", "Сюжетные\nзаписки")
                    use extra_progress_tab_button("Достижения", "Достижения")
                    use extra_progress_tab_button("Коллектаблсы", "Коллектаблсы")
                    use extra_progress_tab_button("Улики", "Улики")

                    
                    
                    null width 190 height 55
                    null width 190 height 55

                frame:
                    xfill True
                    yfill True
                    background None

                    viewport:
                        xfill True
                        yfill True
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            xfill True
                            spacing 22
                            at appears_left

                            if extra_progress_type == "Записки":
                                use extra_progress_story_content
                            elif extra_progress_type == "Достижения":
                                use extra_progress_achievements_content
                            elif extra_progress_type == "Коллектаблсы":
                                use extra_progress_collectibles_content
                            elif extra_progress_type == "Улики":
                                use extra_progress_clues_content


screen extra_progress_tab_button(tab_id, tab_text):
    button:
        xsize 190
        ysize 55
        xalign 0.5

        if extra_progress_type == tab_id:
            text _(tab_text) size 25 xalign 0.5 yalign 0.5 text_align 0.5 at main_vbox_transform2
        else:
            text _(tab_text) size 25 xalign 0.5 yalign 0.5 text_align 0.5 at main_vbox_transform

        action [
            Play("test_six", "button.ogg"),
            Function(hide_extra_progress_descriptions),
            SetVariable("extra_progress_type", tab_id),
            SetVariable("extra_section", "Пролог")
        ]


screen extra_progress_chapter_header(title):
    hbox:
        xalign 0.5
        spacing 18

        add Solid("#ffffff", xysize=(200, 4)) yalign 0.5
        text "{font=8bitwonder.otf}{size=25}[title]{/font}{/size}" xalign 0.5 yalign 0.5
        add Solid("#ffffff", xysize=(200, 4)) yalign 0.5


screen extra_progress_item_button(unlocked, unlocked_img, hover_screen, click_screen=None, null_hover_screen="achievkanulldes_new"):
    if unlocked:
        imagebutton:
            action If(click_screen, [Play("test_six", "button.ogg"), Show(click_screen)], NullAction())
            idle unlocked_img
            hover unlocked_img
            hovered [Play("sound", "audio/buttonselected.mp3"), Show(hover_screen)]
            unhovered Function(hide_optional_progress_description, hover_screen, click_screen)
    else:
        imagebutton:
            action NullAction()
            idle "achievment.png"
            hover "achievment1.png"
            hovered [Play("sound", "audio/buttonselected.mp3"), Show(null_hover_screen)]
            unhovered Hide(null_hover_screen)


screen extra_progress_story_content():
    use extra_progress_chapter_header("Пролог")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis1", 0) == 1:
                use extra_progress_item_button(True, "zapis1.png", "achievka01des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis2", 0) == 1:
                use extra_progress_item_button(True, "zapis2.png", "achievka02des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis3", 0) == 1:
                use extra_progress_item_button(True, "zapis3.png", "achievka03des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis4", 0) == 1:
                use extra_progress_item_button(True, "zapis4.png", "achievka04des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis5", 0) == 1:
                use extra_progress_item_button(True, "zapis5.png", "achievka05des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis6", 0) == 1:
                use extra_progress_item_button(True, "zapis6.png", "achievka06des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis7", 0) == 1:
                use extra_progress_item_button(True, "zapis7.png", "achievka07des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis8", 0) == 1:
                use extra_progress_item_button(True, "zapis8.png", "achievka08des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis9", 0) == 1:
                use extra_progress_item_button(True, "zapis9.png", "achievka09des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis10", 0) == 1:
                use extra_progress_item_button(True, "zapis10.png", "achievka010des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis11", 0) == 1:
                use extra_progress_item_button(True, "zapis11.png", "achievka011des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "zapis12", 0) == 1:
                use extra_progress_item_button(True, "zapis12.png", "achievka012des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes1_new")]
                    unhovered [Hide("achievkanulldes1_new"), Hide("achievkanulldes_bg")]

    use extra_progress_chapter_header("Глава 1")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5

            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")


screen extra_progress_achievements_content():
    use extra_progress_chapter_header("Пролог")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5
            if getattr(persistent, "achiev1", 0) == 1:
                use extra_progress_item_button(True, "achievka1.png", "achievka1des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "achiev2", 0) == 1:
                use extra_progress_item_button(True, "achievka2.png", "achievka2des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "achiev3", 0) == 1:
                use extra_progress_item_button(True, "achievka3.png", "achievka3des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "achiev4", 0) == 1:
                use extra_progress_item_button(True, "achievka4.png", "achievka4des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            $ _achiev5_unlocked = getattr(persistent, "screamer1", 0) == 1 and getattr(persistent, "screamer2", 0) == 1 and getattr(persistent, "screamer3", 0) == 1 and getattr(persistent, "screamer4", 0) == 1
            if _achiev5_unlocked:
                use extra_progress_item_button(True, "achievka5.png", "achievka5des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "sonhorosho", 0) == 1:
                use extra_progress_item_button(True, "achievka6.png", "achievka6des_new")
            elif getattr(persistent, "sonploho", 0) == 1:
                use extra_progress_item_button(True, "achievka6a.png", "achievka6ades_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "achiev7", 0) == 1:
                use extra_progress_item_button(True, "achievka7.png", "achievka7des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            $ _achiev8_unlocked = getattr(persistent, "banani", 0) == 1 and getattr(persistent, "tapki", 0) == 1 and getattr(persistent, "ketchup", 0) == 1 and getattr(persistent, "ecran", 0) == 1 and getattr(persistent, "scope", 0) == 1 and getattr(persistent, "minisans", 0) == 1 and getattr(persistent, "nosok", 0) == 1 and getattr(persistent, "truba", 0) == 1
            if _achiev8_unlocked:
                use extra_progress_item_button(True, "achievka8.png", "achievka8des_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

    use extra_progress_chapter_header("Глава 1")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5

            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")


screen extra_progress_collectibles_content():
    use extra_progress_chapter_header("Пролог")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5
            if getattr(persistent, "collected1", 0) == 1:
                use extra_progress_item_button(True, "collected1.png", "collected1des_new", "collected1description_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "collected2", 0) == 1:
                use extra_progress_item_button(True, "collected2.png", "collected2des_new", "collected2description_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

        vbox:
            xalign 0.5
            if getattr(persistent, "collected3", 0) == 1:
                use extra_progress_item_button(True, "collected3.png", "collected3des_new", "collected3description_new")
            else:
                imagebutton:
                    action NullAction()
                    idle "achievment.png"
                    hover "achievment1.png"
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_bg"), Show("achievkanulldes_new")]
                    unhovered [Hide("achievkanulldes_new"), Hide("achievkanulldes_bg")]

    use extra_progress_chapter_header("Глава 1")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5

            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")


screen extra_progress_clues_content():
    use extra_progress_chapter_header("Пролог")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")

        vbox:
            xalign 0.5
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")

        vbox:
            xalign 0.5
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")

    use extra_progress_chapter_header("Глава 1")

    vbox:
        xalign 0.5
        spacing 12

        vbox:
            xalign 0.5
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                unhovered Hide("achievkanulldes_new")













































######################################   Экран                 ##########################################

transform zapiski_title_appears:
    xpos 0


transform appears_left:
    #on show:
    alpha 0.0 yoffset -25
    easein 1 yoffset 0 alpha 1.0
    #on hide:
    #    easeout 5 xoffset 0



transform appears_left_for_all:
    on show:
        yoffset 0
    on hide:
        easein 1 yoffset 20 alpha 0.0

transform bright_to_normal:
    matrixcolor BrightnessMatrix(1.0)
    easein 1.3 matrixcolor BrightnessMatrix(0.0)



transform zoom05:
    zoom 0.70


default extra_type = None
default extra_sectiom = "Пролог"











screen extra_all_screen():

    zorder 999999

    key "K_ESCAPE" action [Hide("extra_all_screen"), SetVariable("extra_section", "Пролог")]






    vbox:
        at appears_left_for_all
        frame:
            background None

            # ЗАПИСКИ



            
            if extra_type == "Записки":



            
                vbox:
                    xoffset -10
                    xpos 930
                    ypos 210
                    at appears_left
                    frame:
                        xalign 0.6
                        yalign 0.6
                        xsize 305
                        ysize 55
                        background None #"#ffffff"

                        frame:
                            xalign 0.5
                            yalign 0.5
                            background "#000000"
                            ysize 45
                            hbox:
                                xalign 0.5
                                yalign 0.5
                                xsize 290
                                ysize 40

                                if extra_section == "Пролог":
                                    button:
                                        
                                        at appears_left
                                        xalign 0.0
                                        text "x"
                                        action None
                                else:
                                    button:
                                        at appears_left
                                        xalign 0.0
                                        text "<"
                                        action SetVariable("extra_section", "Пролог")


                    

                                if extra_section == "Пролог":
                                    button:
                                        at appears_left
                                        xalign 1.0
                                        text ">"
                                        action SetVariable("extra_section", "1")
                                else:
                                    textbutton "{color=#000000}1{/color}" action None
                                
                            hbox:
                                xalign 0.45 yalign 0.5 xoffset 10
                                frame:
                                    background "#000000"
                                    xalign 0.5
                                    if extra_section == "Пролог":
                                        hbox:
                                            at appears_left
                                            text "{font=8bitwonder.otf}{size=25}Пролог" xalign 0.5 yalign 0.5
                                    else:
                                        hbox:
                                            at appears_left
                                            text "{font=8bitwonder.otf}{size=25}Глава 1" xalign 0.5 yalign 0.5

                



                viewport:
                    xpos 20 ypos 20
                    xysize (500, 1000)
                    #scrollbars "vertical"
                    #mousewheel True
                    vbox:
                        spacing 20
                        at appears_left
                        vbox:

                            at zoom05
                            spacing 10
                            box_wrap True
                            xpos 0.0
                            ypos 0.0


                            if extra_section == "Пролог":
                                if persistent.zapis1 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis1.png"
                                        hover "zapis1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), SetVariable("pokazdes_new", 1), Show("achievka01des_new")]
                                        unhovered Hide("achievka01des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis2 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis2.png"
                                        hover "zapis2.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka02des_new")]
                                        unhovered Hide("achievka02des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered  [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis3 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis3.png"
                                        hover "zapis3.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka03des_new")]
                                        unhovered Hide("achievka03des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")

                                if persistent.zapis4 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis4.png"
                                        hover "zapis4.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka04des_new")]
                                        unhovered Hide("achievka04des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis5 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis5.png"
                                        hover "zapis5.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka05des_new")]
                                        unhovered Hide("achievka05des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis6 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis6.png"
                                        hover "zapis6.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka06des_new")]
                                        unhovered Hide("achievka06des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis7 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis7.png"
                                        hover "zapis7.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka07des_new")]
                                        unhovered Hide("achievka07des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")

                                if persistent.zapis8 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis8.png"
                                        hover "zapis8.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka08des_new")]
                                        unhovered Hide("achievka08des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis9 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis9.png"
                                        hover "zapis9.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka09des_new")]
                                        unhovered Hide("achievka09des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis10 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis10.png"
                                        hover "zapis10.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka010des_new")]
                                        unhovered Hide("achievka010des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.zapis11 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis11.png"
                                        hover "zapis11.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka011des_new")]
                                        unhovered Hide("achievka011des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")

                                if persistent.zapis12 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "zapis12.png"
                                        hover "zapis12.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka012des_new")]
                                        unhovered Hide("achievka012des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes1_new")]
                                        unhovered Hide("achievkanulldes1_new")
                            else:
                                pass










            elif extra_type == "Достижения":

                vbox:   
                        xoffset -10
                        xpos 930
                        ypos 210
                        at appears_left
                        frame:
                            xalign 0.6
                            yalign 0.6
                            xsize 305
                            ysize 55
                            background None #"#ffffff"

                            frame:
                                xalign 0.5
                                yalign 0.5
                                background "#000000"
                                ysize 45
                                hbox:
                                    xalign 0.5
                                    yalign 0.5
                                    xsize 290
                                    ysize 40

                                    if extra_section == "Пролог":
                                        button:
                                            
                                            at appears_left
                                            xalign 0.0
                                            text "x"
                                            action None
                                    else:
                                        button:
                                            at appears_left
                                            xalign 0.0
                                            text "<"
                                            action SetVariable("extra_section", "Пролог")


                        

                                    if extra_section == "Пролог":
                                        button:
                                            at appears_left
                                            xalign 1.0
                                            text ">"
                                            action SetVariable("extra_section", "1")
                                    else:
                                        textbutton "{color=#000000}1{/color}" action None
                                    
                                hbox:
                                    xalign 0.45 yalign 0.5 xoffset 10
                                    frame:
                                        background "#000000"
                                        xalign 0.5
                                        if extra_section == "Пролог":
                                            hbox:
                                                at appears_left
                                                text "{font=8bitwonder.otf}{size=25}Пролог" xalign 0.5 yalign 0.5
                                        else:
                                            hbox:
                                                at appears_left
                                                text "{font=8bitwonder.otf}{size=25}Глава 1" xalign 0.5 yalign 0.5




                viewport:
                    xpos 20 ypos 20
                    xysize (500, 1000)
                    #scrollbars "vertical"
                    #mousewheel True
                    vbox:
                        yalign 0.5
                        spacing 20
                        at appears_left
                        vbox:

                            at zoom05
                            spacing 10
                            box_wrap True
                            xpos 0.0
                            ypos 0.0

                            if extra_section == "Пролог":
                                if persistent.achiev1 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka1.png"
                                        hover "achievka1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka1des_new")]
                                        unhovered Hide("achievka1des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.achiev2 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka2.png"
                                        hover "achievka2.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka2des_new")]
                                        unhovered Hide("achievka2des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.achiev3 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka3.png"
                                        hover "achievka3.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka3des_new")]
                                        unhovered Hide("achievka3des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")

                                if persistent.achiev4 == 1:
                                    imagebutton:
                                        action [Play("test_six", "button.ogg"), Hide("achievka4des_new"), Jump("sempat")]  # действие при нажатии
                                        idle "achievka4.png"
                                        hover "achievka4.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka4des_new")]
                                        unhovered Hide("achievka4des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")
                            
                                if persistent.screamer1 == 1 and persistent.screamer2 == 1 and persistent.screamer3 == 1 and persistent.screamer4 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka5.png"
                                        hover "achievka5.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka5des_new")]
                                        unhovered Hide("achievka5des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.sonhorosho == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka6.png"
                                        hover "achievka6.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka6des_new")]
                                        unhovered Hide("achievka6des_new")
                                elif persistent.sonploho == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka6a.png"
                                        hover "achievka6a.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka6ades_new")]
                                        unhovered Hide("achievka6ades_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")


                                if persistent.achiev7 == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka7.png"
                                        hover "achievka7.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka7des_new")]
                                        unhovered Hide("achievka7des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")

                                if persistent.banani == 1 and persistent.tapki == 1 and persistent.ketchup == 1 and persistent.ecran == 1 and  persistent.scope == 1 and persistent.minisans == 1 and persistent.nosok == 1 and persistent.truba == 1:
                                    imagebutton:
                                        action NullAction()  # действие при нажатии
                                        idle "achievka8.png"
                                        hover "achievka8.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka8des_new")]
                                        unhovered Hide("achievka8des_new")
                                else:
                                    imagebutton:
                                        action NullAction()
                                        idle "achievment.png"
                                        hover "achievment1.png"
                                        hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                        unhovered Hide("achievkanulldes_new")



            elif extra_type == "Коллектаблсы":



                vbox:
                    xoffset -10
                    xpos 930
                    ypos 210
                    at appears_left
                    frame:
                        xalign 0.6
                        yalign 0.6
                        xsize 305
                        ysize 55
                        background None #"#ffffff"

                        frame:
                            xalign 0.5
                            yalign 0.5
                            background None#"#000000"
                            ysize 45
                            hbox:
                                xalign 0.5
                                yalign 0.5
                                xsize 290
                                ysize 40

                                if extra_section == "Пролог":
                                    button:
                                        at appears_left
                                        xalign 0.0
                                        text "x"
                                        action None
                                else:
                                    button:
                                        at appears_left
                                        xalign 0.0
                                        text "<"
                                        action SetVariable("extra_section", "Пролог")

                                if extra_section == "Пролог":
                                    button:
                                        at appears_left
                                        xalign 1.0
                                        text ">"
                                        action SetVariable("extra_section", "1")
                                else:
                                    textbutton "{color=#000000}2{/color}" action None
                                
                            hbox:
                                xalign 0.45 yalign 0.5 xoffset 10
                                frame:
                                    background "#000000"
                                    xalign 0.5
                                    if extra_section == "Пролог":
                                        hbox:
                                            at appears_left
                                            text "{font=8bitwonder.otf}{size=25}Пролог" xalign 0.5 yalign 0.5
                                    else:
                                        hbox:
                                            at appears_left
                                            text "{font=8bitwonder.otf}{size=25}Глава 1" xalign 0.5 yalign 0.5


                viewport:
                    xpos 20 ypos 20
                    xysize (500, 1000)
                    #scrollbars "vertical"
                    #mousewheel True
                    vbox:
                        yalign 0.5
                        spacing 20
                        at appears_left
                        vbox:

                            at zoom05
                            spacing 10
                            box_wrap True
                            xpos 0.0
                            ypos 0.0

                            #xalign 0.5

                            if persistent.collected1 == 1:
                                imagebutton:
                                    action [Play("test_six", "button.ogg"), Show("collected1description_new")]    # действие при нажатии
                                    idle "collected1.png"
                                    hover "collected1.png"
                                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("collected1des_new")]
                                    unhovered [Hide("collected1des_new"), Hide("collected1description_new")]
                            else:
                                imagebutton:
                                    action NullAction()
                                    idle "achievment.png"
                                    hover "achievment1.png"
                                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                    unhovered Hide("achievkanulldes_new")

                            if persistent.collected2 == 1:
                                imagebutton:
                                    action [Play("test_six", "button.ogg"), Show("collected2description_new")]   # действие при нажатии
                                    idle "collected2.png"
                                    hover "collected2.png"
                                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("collected2des_new")]
                                    unhovered [Hide("collected2des_new"), Hide("collected2description_new")]
                            else:
                                imagebutton:
                                    action NullAction()
                                    idle "achievment.png"
                                    hover "achievment1.png"
                                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                    unhovered Hide("achievkanulldes_new")

                            if persistent.collected3 == 1:
                                imagebutton:
                                    action [Play("test_six", "button.ogg"), Show("collected3description_new")]    # действие при нажатии
                                    idle "collected3.png"
                                    hover "collected3.png"
                                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("collected3des_new")]
                                    unhovered [Hide("collected3des_new"), Hide("collected3description_new")]
                            else:
                                imagebutton:
                                    action NullAction()
                                    idle "achievment.png"
                                    hover "achievment1.png"
                                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes_new")]
                                    unhovered Hide("achievkanulldes_new")


            elif extra_type == "Об игре":
                frame:
                    at appears_left
                    xsize 800
                    ysize 700
                    background "#ffffff"

                    viewport:
                        xfill True
                        yfill True
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vscrollbar_xsize 20

                        vbox:
                            spacing 20
                            xfill True
                            at bright_to_normal

                            frame:
                                xfill True
                                background "#000000"
                                padding (20, 20)

                                vbox:
                                
                                    spacing 0
                                    xfill True
                                    

                                    text "Об игре":
                                        xalign 0.4
                                        size 40

                                    vbox:
                                        
                                        spacing 25
                                        # без ysize у блока текста
                                        text "Версия игры: xxxx2026. Глава 1":
                                            xmaximum 750
                                            size 25

                                        text "Проект основан по мотивам игр Toby Fox и фанатского творчества":
                                            xmaximum 750
                                            size 25

                                        text "Соцальные сети: {a=https://vk.com/deltafatetale}Группа во Вконтакте{/a} и {a=https://gamejolt.com/games/deltafatetale/703117}страница на Gamejolt{/a}":
                                            xmaximum 750
                                            size 25

                                        text "Озвучка в прологе сделана при поддержке {a=https://vk.com/wbacompany}Клиффорда Крауна{/a} и {a=https://vk.com/ourlittleplanet}Misato{/a}.":
                                            xmaximum 750
                                            size 25

                                    #add Solid("#ffffff", xysize=(900, 5)) xalign 0.0 xoffset -20

                                    #add "slide2_1.JPG":
                                    #    zoom 0.7
                                    #    xalign 0.0
                                    #    xoffset -20
                                    #    #at bright_to_normal

                                    add Solid("#ffffff", xysize=(900, 5)) xalign 0.0 xoffset -20 

                                    #add "titri2" xalign 0.5
                                    # если у titri2 лишняя пустота — режь

                                    add Transform("titri2", crop=(0, 0, 1000, 1500)):
                                        xalign 0.5 zoom 0.8

                                    add Solid("#ffffff", xysize=(900, 5)) xalign 0.0 xoffset -20

                                    text " - Были использованы ИИ инструменты \n{size=25}{a=https://drive.google.com/drive/folders/17xp3cXnUftAoDjp6Cqsj880vihIjtWew?usp=sharing} - {font=Wingdings.ttf}MY ARCHIVE.{/a}{/size}":
                                        xmaximum 830
                                        size 25
                                    #vbox:
                                    #    xsize 300 ysize 55 xalign 0.0
                                    #    text "{size=20}{a=https://drive.google.com/drive/folders/17xp3cXnUftAoDjp6Cqsj880vihIjtWew?usp=sharing} -{font=Wingdings.ttf}MY ARCHIVE.{/a}{/size}" xalign 0.5 yalign 0.5 color "#ffffff" at main_vbox_transform3 
                                #add Solid("#ffffff", xysize=(900, 700)) at to_alpha0000

transform to_alpha0000:
    matrixcolor BrightnessMatrix(2.0) alpha 1.0
    easein 1.3 matrixcolor BrightnessMatrix(0.0) alpha 0.0
    


###################################### АЧИВКИ ЭКРАН NEW ##########################################

default device01_new = 1
default extra_section = "Пролог"




screen deletecollectables_new:

    add "Podtverdzapis2.png" xpos 0.3 ypos 0.0
    hbox spacing 30:
        xpos 0.6125
        ypos 0
        textbutton "Да" action [Play("test_six", "button.ogg"), SetVariable("collectdevice_new", 1), Jump("deletecollectables")]
        textbutton "Нет" action [Play("test_six", "button.ogg"), SetVariable("collectdevice_new", 1)]







#####Записки#####


transform zapiski:
    on show:
        alpha 0.0 xpos 1280 ypos 100 xzoom 0.9 #yzoom 2
        easein 0.5 alpha 1.0 xpos 750
    on hide:
        #xzoom 0.9 yzoom 2
        easein 0.5 alpha 0.0 xpos 1280 ypos 100

transform achiev_des_bg_fade:
    
    on show:
        xoffset 50 yoffset -40
        alpha 0.0
        easein 0.35 alpha 1.0

    on hide:
        xoffset 50 yoffset -40
        alpha 1.0
        easein 0.35 alpha 0.0


screen achiev_des_panel(img):
    zorder 99999999

    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"

    add img at zapiski


screen achievkanulldes_new:
    zorder 99999999

    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievpodscreen.png" at zapiski


screen achievkanulldes1_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievpodscreen1.png" at zapiski

screen achievka01des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis1des.png" at zapiski

screen achievka02des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis2des.png" at zapiski

screen achievka03des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis3des.png" at zapiski

screen achievka04des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis4des.png" at zapiski

screen achievka05des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis5des.png" at zapiski

screen achievka06des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis6des.png" at zapiski

screen achievka07des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis7des.png" at zapiski

screen achievka08des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis8des.png" at zapiski

screen achievka09des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis9des.png" at zapiski

screen achievka010des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis10des.png" at zapiski

screen achievka011des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis11des.png" at zapiski

screen achievka012des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "zapis12des.png" at zapiski

screen deleteachiev0_new:
    zorder 99999999
    add "Podtverdzapis.png" xpos 0.3 ypos 0.0
    hbox spacing 30:
        xpos 0.6125
        ypos 0
        textbutton "Да" action Jump("deletezapisi")
        textbutton "Нет" action SetVariable("device0_new", 1)

##### Ачивки #####


screen achievka1des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka1des.png" at zapiski


screen achievka2des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka2des.png" at zapiski

screen achievka3des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka3des.png" at zapiski

screen achievka4des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka4des.png" at zapiski

screen achievka5des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka5des.png" at zapiski

screen achievka6des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka6des.png" at zapiski

screen achievka6ades_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka6ades.png" at zapiski

screen achievka7des_new:
    zorder 99999999
    frame:
        at achiev_des_bg_fade
        xpos 700
        ypos 100
        xsize 500
        ysize 700
        background "#000000"
    add "achievka7des.png" at zapiski

screen achievka8des_new:
    zorder 99999999
    add "achievka8des.png" at zapiski



###################################### Коллектаблсы NEW ##########################################

screen collected1des_new:
    zorder 99999999
    add "collectpodscreen1.png" at zapiski
    
screen collected2des_new:
    zorder 99999999
    add "collectpodscreen2.png" at zapiski

screen collected3des_new:
    zorder 99999999
    add "collectpodscreen3.png" at zapiski

screen collected1description_new:
    zorder 99999999
    add "collected1description.png" at zapiski
    timer 30 action Hide("collected1description_new")

screen collected2description_new:
    zorder 99999999
    add "collected2description.png" at zapiski
    timer 30 action Hide("collected2description_new")

screen collected3description_new:
    zorder 99999999
    add "collected3description.png" at zapiski
    timer 30 action Hide("collected3description_new")












































###################################### Музыка NEW ##########################################

#screen musicscreen_new():

###################################### Фоны NEW ##########################################

#screen backgroundscreen_new():










































###################################### Экран настроек (preferences) ##########################################

default pref_section = None







transform alpha_okno_pred:
    yoffset -200 alpha 0.0 xoffset 10
    on show:
        easein 0.5 yoffset 10 alpha 1.0
    on hide:
        easeout 0.5 yoffset 20 alpha 0.0

screen okno_pred:
    frame:
        xysize(560, 310)
        at alpha_okno_pred
        background "#ffffff"
        frame:
            xysize (550, 300)
            xalign 0.5
            yalign 0.5
            background "#000000"
            padding (10, 10)
            vbox:
                xysize (540, 295)
                xfill True
                spacing 10
                text "Внимание!" size 40 xalign 0.5
                text " Оконный режим негативно влияет на стабильность в бою\n Во время уворота от атак координаты сердцевидного объекта могут отображаться некорректно\n Рекомендуется играть в полноэкранном режиме или растянуть окно на всю высоту экрана":
                    
                    size 25
                    xmaximum 540
                    xfill True
                    text_align 0.0   # влево


screen preferences_new2():
    zorder 99999



    timer 0.001 action SetVariable("main_section", "other")
    key "K_ESCAPE" action [Hide("preferences_new2"), Show("main_vbox")]
    vbox:
        at save_appears
        #at par_layer(0.1)
        xoffset 0
        yoffset 50
        xalign 0.5
        yalign 0.5
        spacing 20
        vbox:
            xalign 0.5
            spacing 10
            add "main_label_3.png" xalign 0.5 yalign 0.3 zoom 0.3
            text "{font=8bitwonder.otf}{size=25}Настройки" xalign 0.5 yalign 0.3
        
        

            hbox:
                xalign 0.5 
                

                text "{font=determination.otf}{size=20}Режим экрана" xalign 0.5 yalign 0.5
                textbutton _("{size=20}Оконный") action [Play("test_six", "button.ogg"),Hide("okno_pred"),Preference("display", "window")]:
                    hovered [Play("sound", "audio/buttonselected.mp3"), Show("okno_pred")]
                    unhovered [Hide("okno_pred")]
                    
                textbutton _("{size=20}Полный*") action [Play("test_six", "button.ogg"),Preference("display", "fullscreen")]:
                    hovered Play("sound", "audio/buttonselected.mp3")

            #text "{font=determination.otf}{size=20}Звук" xalign 0.5 yalign 0.5
            
            grid 2 4:
                xalign 0.5 
                spacing 20
                

                text "{font=determination.otf}{size=20}Громкость звука" xalign 0.0 yalign 0.5
                bar value Preference("sound volume") xsize 180 xalign 1.0 yalign 0.5

        
                text "{font=determination.otf}{size=20}Громкость музыки" xalign 0.0 yalign 0.5
                bar value Preference("music volume") xsize 180 xalign 1.0 yalign 0.5
            
            
                text "{font=determination.otf}{size=20}Громкость Озвучки" xalign 0.0 yalign 0.5
                bar value Preference("voice volume") xsize 180 xalign 1.0 yalign 0.5


            
                text "{font=determination.otf}{size=20}Скорость текста" xalign 0.0 yalign 0.5
                bar value Preference("text speed") xsize 180 xalign 1.0 yalign 0.5

            vbox spacing 20:
                xalign 0.5
                if config.has_music or config.has_sound or config.has_voice:
                    null height gui.pref_spacing
                    textbutton _("{size=20}Играть без звука*"):
                        xalign 0.5
                        action [Jump('screamer10'), Preference("all mute", "toggle")]
                        hovered Play("sound", "audio/buttonselected.mp3")
                        style "mute_all_button"
                #textbutton"{color=#ffffff}{size=15}{font=Wingdings.ttf}YOU WON'T ESCAPE BY COVERING YOUR EARS." action NullAction()
            
            text "{font=determination.otf}{size=20}*Рекомендуется" xalign 0.5 yalign 0.5

            textbutton "Назад" action [Hide("preferences_new2"), Show("main_vbox")] xalign 0.5




screen preferences_new_all():


    

    if store.pref_section == "Звук":
    
    #elif store.pref_section == "Экран":
    
    #elif store.pref_section == "Текст":

        hbox spacing 20:

            vbox spacing 100:
                box_wrap False

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox spacing 1:
                        style_prefix "radio"
                        label _("Режим экрана")
                        textbutton _("Оконный") action [Play("test_six", "button.ogg"),Preference("display", "window")]:
                            hovered Play("sound", "audio/buttonselected.mp3")
                        textbutton _("Полный") action [Play("test_six", "button.ogg"),Preference("display", "fullscreen")]:
                            hovered Play("sound", "audio/buttonselected.mp3")


                vbox:
                    style_prefix "check"
                    label _("Пропуск")
                    textbutton _("Всего текста") action [Play("test_six", "button.ogg"),Preference("skip", "toggle")]:
                        hovered Play("sound", "audio/buttonselected.mp3")
                    textbutton _("После выборов") action [Play("test_six", "button.ogg"),Preference("after choices", "toggle")]:
                        hovered Play("sound", "audio/buttonselected.mp3")
                    textbutton _("Переходов") action [Play("test_six", "button.ogg"),InvertSelected(Preference("transitions", "toggle"))]:
                        hovered Play("sound", "audio/buttonselected.mp3")



                ## Дополнительные vbox'ы типа "radio_pref" или "check_pref"
                ## могут быть добавлены сюда для добавления новых настроек.

            null height (4 * gui.pref_spacing)

            vbox spacing 50:
                style_prefix "slider"
                box_wrap False

                vbox:

                    if config.has_music:
                        label _("Громкость музыки")
                        
                        hbox:
                            bar value Preference("music volume") xsize 120
                        

                    if config.has_sound:

                        label _("Громкость звуков")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Тест") action Play("sound", config.sample_sound)

                    if config.has_voice:
                            label _("Громкость голоса")

                            hbox:
                                bar value Preference("voice volume")

                                if config.sample_voice:
                                    textbutton _("Тест") action Play("voice", config.sample_voice)
                vbox:
                        label _("Скорость текста")
                        hbox:
                            bar value Preference("text speed")

                        label _("Скорость авточтения")
                        hbox:
                            bar value Preference("auto-forward time")
                         
                         
            vbox spacing 20:
                if config.has_music or config.has_sound or config.has_voice:
                    null height gui.pref_spacing
                    textbutton _("Играть без звука"):
                        action [Jump('screamer10'), Preference("all mute", "toggle")]
                        hovered Play("sound", "audio/buttonselected.mp3")
                        style "mute_all_button"
                textbutton "{color=#020202}{size=15}{font=Wingdings.ttf}You won't get anywhere by covering your ears." action NullAction()
    use backtogame2
                 

default player_y = 0
default player_x = 0
default py = player_x
