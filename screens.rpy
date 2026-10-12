################################################################################
## Инициализация
################################################################################

init offset = -1

default _game_menu_screen = "load"
################################################################################
## Стили
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"

style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)




################################################################################
## Внутриигровые экраны
################################################################################


## Экран разговора #############################################################
##
## Экран разговора используется для показа диалога игроку. Он использует два
## параметра — who и what — что, соответственно, имя говорящего персонажа и
## показываемый текст. (Параметр who может быть None, если имя не задано.)
##
## Этот экран должен создать текст с id "what", чтобы Ren'Py могла показать
## текст. Здесь также можно создать наложения с id "who" и id "window", чтобы
## применить к ним настройки стиля.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    #zorder 1000
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## Если есть боковое изображение ("голова"), показывает её поверх текста.
    ## По стандарту не показывается на варианте для мобильных устройств — мало
    ## места.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Делает namebox доступным для стилизации через объект Character.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label



style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    
    background ConditionSwitch(
        "txt == 0", Image("gui/textbox.png", xalign=0.5, yalign=1.0),
        "txt == 1", Image("gui/textbox2.png", xalign=0.5, yalign=1.0),
        True, Image("gui/textbox2.png", xalign=0.5, yalign=1.0)  # Значение по умолчанию
    )


style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Экран ввода #################################################################
##
## Этот экран используется, чтобы показывать renpy.input. Это параметр запроса,
## используемый для того, чтобы дать игроку ввести в него текст.
##
## Этот экран должен создать наложение ввода с id "input", чтобы принять
## различные вводимые параметры.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Экран выбора ################################################################
##
## Этот экран используется, чтобы показывать внутриигровые выборы,
## представленные оператором menu. Один параметр, вложения, список объектов,
## каждый с заголовком и полями действия.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## Когда этот параметр True, заголовки меню будут проговариваться рассказчиком.
## Когда False, заголовки меню будут показаны как пустые кнопки.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Экран быстрого меню #########################################################
##
## Быстрое меню показывается внутри игры, чтобы обеспечить лёгкий доступ к
## внеигровым меню.

$ persistent.nuzhnofastmenu = 1

default persistent.pause = 1

screen quick_menu():
    textbutton _("")
    ## Гарантирует, что оно появляется поверх других экранов.
    #zorder 100
    
    if quick_menu:
        if persistent.nuzhnofastmenu == 1:      
            hbox:
                spacing 10
                style_prefix "quick"

                xalign 1.0
                yalign 0.0

                #textbutton _("Назад") action [Play("test_six", "button.ogg"),Rollback()]
                #textbutton _("История") action [Play("test_six", "button.ogg"),ShowMenu('history')]
                #textbutton _("Пропуск") action [Play("test_six", "button.ogg"),Skip()] alternate [Play("test_six", "button.ogg"),Skip(fast=True, confirm=True)]
                #textbutton _("Авто") action [Play("test_six", "button.ogg"),Preference("auto-forward", "toggle")]

                imagebutton:
                    action [Play("test_six", "button.ogg"),Skip()]
                    idle "propuskbel.png"
                    hover "propuskzh.png"
                    hovered Play("sound", "audio/buttonselected.mp3")

                imagebutton:
                    action [Play("test_six", "button.ogg"),ShowMenu('save')]
                    idle "glmenubel.png"
                    hover "glmenubel2.png"
                    hovered Play("sound", "audio/buttonselected.mp3")
                #textbutton _("Б.Сохр") action [Play("test_six", "button.ogg"),QuickSave()]
                #textbutton _("Б.Загр") action [Play("test_six", "button.ogg"),QuickLoad()]
                #textbutton _("Опции") action [Play("test_six", "button.ogg"),ShowMenu('preferences')]
        else:
            pass


## Данный код гарантирует, что экран быстрого меню будет показан в игре в любое
## время, если только игрок не скроет интерфейс.
init python:
    config.overlay_screens.append("quick_menu")


style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
## Экраны Главного и Игрового меню
################################################################################



## Экран навигации #############################################################
##
## Этот экран включает в себя главное и игровое меню, и обеспечивает навигацию к
## другим меню и к началу игры.


screen meow():
    if persistent.prolog_complete_meow == 1:
        if persistent.nepokas == 0:     
            imagebutton:
                action [Play("test_six", "button.ogg"), Jump("MEOW")] 
                xalign 0.505
                yalign 0.025   
                idle "meow.png"
                hover "meow2.png"
                hovered Play("sound", "audio/buttonselected.mp3")
        
    else:
        pass

screen Gasterarchiev:
    if persistent.prolog_complete_meow == 1:
        if persistent.nepokas == 0:
            vbox:
                xalign 0.05
                text "{color=#ffff00}{size=35}{a=https://drive.google.com/drive/folders/17xp3cXnUftAoDjp6Cqsj880vihIjtWew?usp=sharing}{font=Wingdings.ttf}My archive.{/a}"
    else:
        pass



screen navigation():
    $ persistent.navigation = 1
    use backtogame
    
    # Оптимизировано: один timer с复合 action вместо 27 отдельных
    timer 0.1 action [
        Hide("achievkanulldes"), Hide("achievkanulldes1"),
        Hide("achievka1des"), Hide("achievka2des"), Hide("achievka3des"),
        Hide("achievka4des"), Hide("achievka5des"), Hide("achievka6des"),
        Hide("achievka7des"), Hide("achievka8des"), Hide("achievka9des"),
        Hide("achievka10des"), Hide("achievka11des"), Hide("achievka12des"),
        Hide("achievka01des"), Hide("achievka02des"), Hide("achievka03des"),
        Hide("achievka04des"), Hide("achievka05des"), Hide("achievka06des"),
        Hide("achievka07des"), Hide("achievka08des"), Hide("achievka09des"),
        Hide("achievka010des"), Hide("achievka011des"), Hide("achievka012des"),
        Hide("collected1des"), Hide("collected2des"), Hide("collected3des"),
        Hide("collected1description"), Hide("collected2description"),
        Hide("collected3description")
    ]
    
    
 

    if main_menu:
        if persistent.prolog_complete == 1:
                use meow
    else:
        pass

    if main_menu:
        if persistent.gasterarchive == 1:
                use Gasterarchiev
    else:
        pass

    hbox spacing 0.2:
        style_prefix "navigation"

        xalign 0.5
        yalign 0.9

    

        if main_menu:

            textbutton _("Новая игра") action [Play("test_six", "button.ogg"), Start()] :
                hovered Play("sound", "audio/buttonselected.mp3")


        else:

            textbutton _("Сохранить") action [Play("test_six", "button.ogg"), Hide("relief"), ShowMenu("save")] :
                hovered Play("sound", "audio/buttonselected.mp3")

        textbutton _("Загрузить") action [Play("test_six", "button.ogg"),Hide("relief"), ShowMenu("load")]:
                hovered Play("sound", "audio/buttonselected.mp3")

        textbutton _("Настройки") action [Play("test_six", "button.ogg"), ShowMenu("preferences")]:
                hovered Play("sound", "audio/buttonselected.mp3")
        
        textbutton _("Экстра") action [Play("test_six", "button.ogg"), ShowMenu("about")]:
                hovered Play("sound", "audio/buttonselected.mp3")        

        if main_menu:
            textbutton _("Справка") action [Play("test_six", "button.ogg"), ShowMenu("help")]:
                hovered Play("sound", "audio/buttonselected.mp3")
            textbutton _("Выход") action [Play("test_six", "button.ogg"), Quit(confirm= main_menu)]:
                hovered Play("sound", "audio/buttonselected.mp3")

        else:
            textbutton _("Справка") action [Play("test_six", "button.ogg"),ShowMenu("help")]:
                hovered Play("sound", "audio/buttonselected.mp3")
            textbutton _("Гл.Меню") action [Play("test_six", "button.ogg"), MainMenu()]:
                hovered Play("sound", "audio/buttonselected.mp3")

    text "{size=999} СИСЯ!"

            


























































        


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    xalign 0.5


## Экран главного меню #########################################################
##
## Используется, чтобы показать главное меню после запуска игры.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

transform alpha_000:
    alpha 0.0 xpos 0.0 ypos 0.0

transform main_menu_trans1:
    subpixel True
    alpha 1.0

transform main_menu_trans2:
    subpixel True
    xalign 0.5 yalign 0.5
    easein 1 alpha 0.0 #zoom 3

transform label_shift:
    subpixel True
    parallel:
        easein 3 yoffset 15
    #pause 0.001
        #easeout 0.5 yoffset 30
    pause 1

    parallel:
        easein 4 yoffset -15
    #pause 0.001
        #easeout 0.5 yoffset -30
    pause 1

    repeat 

transform alpha_to_0:
    alpha 1.0
    easein 3 alpha 0.0




default main_menu_var = "to_start"

screen main_menu2():
    key "K_ESCAPE" action Show("escape")
    #key "K_ESCAPE" action NullAction()

    key "K_RETURN" action [Hide("Escape"), SetVariable("main_menu_var", "go")]

    ## Этот тег гарантирует, что любой другой экран с тем же тегом будет
    ## заменять этот.
    #tag menu

    #text "Фан игра по мотивам Undertale и Deltarune"
    vbox:
        if store.main_menu_var == "to_start":
            at main_menu_trans1
        else:
            at main_menu_trans2



        frame:
            background None

            imagebutton:
                at alpha_000
                idle "blackbg3.png"
                hover "blackbg3.png"

            vbox:
                xalign 0.5  yalign 0.9
                text "{size=40}Нажмите Enter" xalign 0.5 
                #text "{size=40}чтобы начать" xalign 0.5

            vbox:
                
                frame:
                    background None

                    #add gui.main_menu_background at label_shift 
                    add "gui/main_menu2.png" at label_shift
                    add "blackbg3.png" at alpha_to_0

    if store.main_menu_var == "to_start":
        pass
    else:
        timer 0.001 action Show("main_menu2")
        #timer 0.001 action Show("check_point") 




transform main_menu_up_to_down:
    subpixel True
    alpha 0.0 ypos 720
    #pause 2
    easein 5 alpha 1.0 ypos 0
    #alpha 0.0


transform bg_is_new_game:
    subpixel True
    easein 2 xpos 200
    pause 0.001
    easein 3 alpha 0.0


transform fake_black:
    pause 8 alpha 0.0



transform just_alpha:
    on show:
        alpha 0.0
        easein 0.5 alpha 1.0
    on hide:
        easein 0.5 alpha 0.0



screen main_menu_prepare:
    
    #tag menu

    #timer 5 action ShowMenu()
    timer 7 action Hide("main_menu_prepare")

    #timer 0.02 repeat True action Function(parallax_update, strength)

    #timer 4.95 action Show("main_menu_parallax")
    #timer 5 action Show("main_vbox")


    vbox:
        if store.main_menu2_var == "preparing":
            vbox:

                at main_menu_up_to_down
                frame:
                    background "#000000"

                    add "dusha" xsize 1280 ysize 720 at par_layer(0.6, base_x=-230, base_y=0)
                    add "black_pol.png" at par_layer(0.6, base_x=-60, base_y=0)


screen main_menu():
    if store.started == 1:
        timer 0.001 action SetVariable("main_section", "Save")
    timer 0.02 repeat True action Function(parallax_update, strength)

    #timer 0.0001 action Show("main_menu_parallax")
    timer 0.0001 action Show("main_vbox")
    timer 2 action Hide("main_menu_prepare") 



##############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


transform save_zvezda_shine:
    alpha 0.0
    easein 1.0 alpha 1.0
    easeout 1.0 alpha 0.0
    repeat


transform main_vbox3:
    
    easein 2 alpha 1.0
    alpha 0.0


screen main_menu_parallax:


    #vbox:
    #    at main_vbox3
    #    frame:
    #        background "#000000"
    #        add "dusha" xsize 1280 ysize 720 at par_layer(0.6, base_x=-230, base_y=0)



    if store.main_section == "Save": #Потом New_game

        vbox:
            #at just_alpha
            at main_vbox
            frame:
                background "#000000"
                
                add "Звезда_1.png" xsize 1280 ysize 720 at [save_zvezda_fade_out, par_layer(0.6, base_x=0, base_y=0)]
                add "Звезда_2.png" xsize 1280 ysize 720 at [save_zvezda_fade_in, par_layer(0.6, base_x=0, base_y=0)]
                add "Звезда_3.png" xsize 1280 ysize 720 at [save_zvezda_shine, par_layer(0.6, base_x=0, base_y=0)]
                

    else:

        vbox:
            #at main_vbox
            #else:
            if store.bg_new_game == -1:
                vbox:
                    at main_vbox
                    frame:
                        background "#000000"
                        add "dusha" xsize 1280 ysize 720 at par_layer(0.6, base_x=-230, base_y=0)
                        add "black_pol.png" at par_layer(0.6, base_x=-60, base_y=0)
            else:
                vbox:
                    at bg_is_new_game
                    frame:
                        background "#000000"
                        add "dusha" xsize 1280 ysize 720 at par_layer(0.6, base_x=-230, base_y=0)
                        add "black_pol.png" at par_layer(0.6, base_x=-60, base_y=0)











transform shift_main_vbox_start:
    easein 1.0 alpha 0.0 xoffset 100




                  
default main_menu2_var = "preparing"                        
                    
default bg_new_game = -1

screen ok_lets_start:
    $ store.main_section == "New_game"
    timer 0.001 action SetVariable ("bg_new_game", 1)
    #timer 6.5 action SetVariable("bg_new_game", 0)


    zorder 999
    #add "dusha" at bg_is_new_game
    imagebutton:
        xpos 0 ypos 0
        at alpha_000
        idle "blackbg3.png"
        hover "blackbg3.png"
        action NullAction()

    timer 0.001 action SetVariable("main_menu2_var", "lets_go")
    timer 7 action Start()





























































style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

#style main_menu_frame:
    #xsize 280
    #yfill True

    # background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Экран игрового меню #########################################################
##
## Всё это показывает основную, обобщённую структуру экрана игрового меню. Он
## вызывается с экраном заголовка и показывает фон, заголовок и навигацию.
##
## Параметр scroll может быть None, или "viewport", или "vpgrid", когда этот
## экран предназначается для использования с более чем одним дочерним экраном,
## включённым в него.

default rot_ebal = 0



screen game_menu(title, scroll=None, yinitial=0.0):
    #timer 0.01 action SetVariable("rot_ebal", 1)

    #tag Menu

    style_prefix "game_menu"

    #if main_menu:
    #    add gui.main_menu_background
    #else:
    #    add gui.game_menu_background
    add "blackbg3.png"
    #timer 0.001 action Show("main_menu")
    #timer 0.001 action Show("main_vbox")

    timer 0.001 action Show("main_menu")
    
    #use main_menu
    #use main_vbox


    

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


## Экран Об игре ###############################################################
##
## Этот экран показывает авторскую информацию об игре и Ren'Py.
##
## В этом экране нет ничего особенного, и он служит только примером того, каким
## можно сделать свой экран.
define device = "historydiary"
screen about():
    $ persistent.meow = 0
    tag menu

    ## Этот оператор включает игровое меню внутрь этого экрана. Дочерний vbox
    ## включён в порт просмотра внутри экрана игрового меню.
    use game_menu(_("Экстра"), scroll="viewport"):

        style_prefix "about"

        vbox:
            spacing 30

            hbox:
                textbutton _("Сюжетные записки") action [Play("test_six", "button.ogg"), SetScreenVariable("device", "historydiary")]:
                    style "battle_menu_button"
                    text_style "battle_menu_button_text"
                    hovered Play("sound", "audio/buttonselected.mp3")
                textbutton _("Достижения") action [Play("test_six", "button.ogg"), SetScreenVariable("device", "achiev")]:
                    style "battle_menu_button"
                    text_style "battle_menu_button_text"
                    hovered Play("sound", "audio/buttonselected.mp3")
                textbutton _("Коллектаблсы") action [Play("test_six", "button.ogg"), SetScreenVariable("device", "collect")]:
                    style "battle_menu_button"
                    text_style "battle_menu_button_text"
                    hovered Play("sound", "audio/buttonselected.mp3")
                #textbutton _("Музыка") action [Play("test_six", "button.ogg"), SetScreenVariable("device", "music")]:
                #    hovered Play("sound", "audio/buttonselected.mp3")
                #textbutton _("Фоны") action [Play("test_six", "button.ogg"), SetScreenVariable("device", "background")]:
                #    hovered Play("sound", "audio/buttonselected.mp3")

            if device == "historydiary":
                use achievscreen0
            elif device == "achiev":
                use achievscreen
            elif device == "collect":
                use collectscreen
            #elif device == "music":
                #use musicscreen
            #elif device == "background":
                #use backgroundscreen
    use backtogame2

    if main_menu:
        $ persistent.nepokas = 1
    else:
        $ persistent.nepokas = 0



###################################### Сюжетные записки ##########################################

default device0 = 1
default pokazdes = 0


screen achievscreen0():
    
    # Начальное значение переменной
    
    $ persistent.hideafterprologue = 0
    # Use game menu

    style_prefix "about"

    vbox spacing 10:
        hbox spacing 30:
            xpos 0.02
            ypos 0

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device0", 1)]
                idle "1.png"
                hover "1hovered.png" 
                hovered Play("sound", "audio/buttonselected.mp3")

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device0", 2)]
                idle "2.png"
                hover "2hovered.png" 
                hovered Play("sound", "audio/buttonselected.mp3")

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device0", 3)]
                idle "3.png"
                hover "3hovered.png" 
                hovered Play("sound", "audio/buttonselected.mp3")

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device0", 4)]
                idle "deleteprogress.png"
                hover "deleteprogresshovered.png"            
                hovered Play("sound", "audio/buttonselected.mp3")
            
    if device0 == 1:
        use achievscreen01
    if device0 == 2:
        use achievscreen02
    if device0 == 3:
        use achievscreen03
    if device0 == 4:
        use deleteachiev0
    #elif device0 == "collect":
        #use collectscreen
    #elif device0 == "music":
        #use musicscreen
    #elif device0 == "background":
        #use backgroundscreen




#####Записки 1#####


screen achievkanulldes:
    add "achievpodscreen.png" xpos 0.525 ypos 0.385
    timer 1.0 action Hide("achievka1des") 

screen achievkanulldes1:
    add "achievpodscreen1.png" xpos 0.525 ypos 0.385 

screen achievka01des:
    add "zapis1des.png" xpos 0.525 ypos 0.385

screen achievka02des:
    add "zapis2des.png" xpos 0.525 ypos 0.385

screen achievka03des:
    add "zapis3des.png" xpos 0.525 ypos 0.385

screen achievka04des:
    add "zapis4des.png" xpos 0.525 ypos 0.385

screen achievka05des:
    add "zapis5des.png" xpos 0.525 ypos 0.385

screen achievka06des:
    add "zapis6des.png" xpos 0.525 ypos 0.385

screen achievka07des:
    add "zapis7des.png" xpos 0.525 ypos 0.385

screen achievka08des:
    add "zapis8des.png" xpos 0.525 ypos 0.385

screen achievka09des:
    add "zapis9des.png" xpos 0.525 ypos 0.385

screen achievka010des:
    add "zapis10des.png" xpos 0.525 ypos 0.385

screen achievka011des:
    add "zapis11des.png" xpos 0.525 ypos 0.385

screen achievka012des:
    add "zapis12des.png" xpos 0.525 ypos 0.385

screen deleteachiev0:
    add "Podtverdzapis.png" xpos 0.3 ypos 0.0
    hbox spacing 30:
        xpos 0.6125
        ypos 0
        textbutton "Да" action Jump("deletezapisi")
        textbutton "Нет" action SetVariable("device0", 1)

screen achievscreen01():
    vbox spacing 10:
        box_wrap True
        xpos 0.0
        ypos 0.0
        if persistent.zapis1 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis1.png"
                hover "zapis1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), SetVariable("pokazdes", 1), Show("achievka01des")]
                unhovered Hide("achievka01des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.zapis2 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis2.png"
                hover "zapis2.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka02des")]
                unhovered Hide("achievka02des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered  [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.zapis3 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis3.png"
                hover "zapis3.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka03des")]
                unhovered Hide("achievka03des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

        if persistent.zapis4 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis4.png"
                hover "zapis4.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka04des")]
                unhovered Hide("achievka04des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")




screen achievscreen02():
    vbox spacing 10:
        box_wrap True
        xpos 0
        ypos 0
        if persistent.zapis5 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis5.png"
                hover "zapis5.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka05des")]
                unhovered Hide("achievka05des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.zapis6 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis6.png"
                hover "zapis6.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka06des")]
                unhovered Hide("achievka06des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.zapis7 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis7.png"
                hover "zapis7.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka07des")]
                unhovered Hide("achievka07des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

        if persistent.zapis8 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis8.png"
                hover "zapis8.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka08des")]
                unhovered Hide("achievka08des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

screen achievscreen03():
    vbox spacing 10:
        box_wrap True
        xpos 0
        ypos 0
        if persistent.zapis9 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis9.png"
                hover "zapis9.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka09des")]
                unhovered Hide("achievka09des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.zapis10 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis10.png"
                hover "zapis10.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka010des")]
                unhovered Hide("achievka010des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.zapis11 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis11.png"
                hover "zapis11.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka011des")]
                unhovered Hide("achievka011des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

        if persistent.zapis12 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "zapis12.png"
                hover "zapis12.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka012des")]
                unhovered Hide("achievka012des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes1")]
                unhovered Hide("achievkanulldes1")

if pokazdes == 0:
    hide achievkanulldes

###################################### АЧИВКИ ЭКРАН ##########################################

default device01 = 1

screen achievscreen():
    
    # Начальное значение переменной
    

    # Use game menu

    style_prefix "about"
    $ persistent.hideafterprologue = 0
    vbox spacing 10:
        hbox spacing 30:
            xpos 0.02
            ypos 0

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device01", 1)]
                idle "1.png"
                hover "1hovered.png" 
                hovered Play("sound", "audio/buttonselected.mp3")

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device01", 2)]
                idle "2.png"
                hover "2hovered.png" 
                hovered Play("sound", "audio/buttonselected.mp3")

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("device01", 3)]
                idle "deleteprogress.png"
                hover "deleteprogresshovered.png"            
                hovered Play("sound", "audio/buttonselected.mp3")
            
    if device01 == 1:
        use achievscreen001
    if device01 == 2:
        use achievscreen002
    if device01 == 3:
        use deleteachiev000

    #elif device0 == "collect":
        #use collectscreen
    #elif device0 == "music":
        #use musicscreen
    #elif device0 == "background":
        #use backgroundscreen

screen deleteachiev000:
    add "Podtverdzapis1.png" xpos 0.3 ypos 0.0
    hbox spacing 30:
        xpos 0.6125
        ypos 0
        textbutton "Да" action [Play("test_six", "button.ogg"),SetVariable("device01", 1), Jump("deleteachievki")] 
        textbutton "Нет" action [Play("test_six", "button.ogg"), SetVariable("device01", 1)] 


#####Записки 1#####


screen achievka1des:
    add "achievka1des.png" xpos 0.525 ypos 0.385
    

screen achievka2des:
    add "achievka2des.png" xpos 0.525 ypos 0.385

screen achievka3des:
    add "achievka3des.png" xpos 0.525 ypos 0.385

screen achievka4des:
    add "achievka4des.png" xpos 0.525 ypos 0.385

screen achievka5des:
    add "achievka5des.png" xpos 0.525 ypos 0.385

screen achievka6des:
    add "achievka6des.png" xpos 0.525 ypos 0.385

screen achievka6ades:
    add "achievka6ades.png" xpos 0.525 ypos 0.385

screen achievka7des:
    add "achievka7des.png" xpos 0.525 ypos 0.385

screen achievka8des:
    add "achievka8des.png" xpos 0.525 ypos 0.385








screen achievscreen001():
    
    vbox spacing 10:
        box_wrap True
        xpos 0.0
        ypos 0.0
        if persistent.achiev1 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka1.png"
                hover "achievka1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka1des")]
                unhovered Hide("achievka1des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.achiev2 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka2.png"
                hover "achievka2.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka2des")]
                unhovered Hide("achievka2des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.achiev3 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka3.png"
                hover "achievka3.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka3des")]
                unhovered Hide("achievka3des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

        if persistent.achiev4 == 1:
            imagebutton:
                action [Play("test_six", "button.ogg"), Hide("achievka4des"), Jump("sempat")]  # действие при нажатии
                idle "achievka4.png"
                hover "achievka4.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka4des")]
                unhovered Hide("achievka4des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


screen achievscreen002():
    vbox spacing 10:
        box_wrap True
        xpos 0
        ypos 0
        if persistent.screamer1 == 1 and persistent.screamer2 == 1 and persistent.screamer3 == 1 and persistent.screamer4 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka5.png"
                hover "achievka5.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka5des")]
                unhovered Hide("achievka5des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.sonhorosho == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka6.png"
                hover "achievka6.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka6des")]
                unhovered Hide("achievka6des")
        elif persistent.sonploho == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka6a.png"
                hover "achievka6a.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka6ades")]
                unhovered Hide("achievka6ades")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.achiev7 == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka7.png"
                hover "achievka7.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka7des")]
                unhovered Hide("achievka7des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

        if persistent.banani == 1 and persistent.tapki == 1 and persistent.ketchup == 1 and persistent.ecran == 1 and  persistent.scope == 1 and persistent.minisans == 1 and persistent.nosok == 1 and persistent.truba == 1:
            imagebutton:
                action NullAction()  # действие при нажатии
                idle "achievka8.png"
                hover "achievka8.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievka8des")]
                unhovered Hide("achievka8des")
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")
if pokazdes == 0:
    hide achievka5des



###################################### Коллектаблсы ##########################################

screen collected1des:
    add "collectpodscreen1.png" xpos 0.525 ypos 0.385
    
screen collected2des:
    add "collectpodscreen2.png" xpos 0.525 ypos 0.385

screen collected3des:
    add "collectpodscreen3.png" xpos 0.525 ypos 0.385

screen collected1description:
    add "collected1description.png" xpos 0.525 ypos 0.385 
    timer 30 action Hide("collected1description")  

screen collected2description:
    add "collected2description.png" xpos 0.525 ypos 0.385 
    timer 30 action Hide("collected2description") 

screen collected3description:
    add "collected3description.png" xpos 0.525 ypos 0.385 
    timer 30 action Hide("collected3description") 



default collectdevice = 1
screen collectscreen():
    $ persistent.hideafterprologue = 0

    # Начальное значение переменной

    # Use game menu
    style_prefix "about"  # This line should not be indented

    vbox spacing 10:
        hbox spacing 30:
            xpos 0.02
            ypos 0

            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("collectdevice", 1)]
                idle "1.png"
                hover "1hovered.png" 
                hovered Play("sound", "audio/buttonselected.mp3")


            imagebutton:
                action [Play("test_six", "button.ogg"), SetVariable("collectdevice", 2)]
                idle "deleteprogress.png"
                hover "deleteprogresshovered.png"            
                hovered Play("sound", "audio/buttonselected.mp3")
            
    if collectdevice == 1:
        use collectables1
    elif collectdevice == 2:
        use deletecollectables

    #elif device0 == "collect":
    #use collectscreen
    #elif device0 == "music":
    #use musicscreen
    #elif device0 == "background":
    #use backgroundscreen

screen deletecollectables:
    add "Podtverdzapis2.png" xpos 0.3 ypos 0.0
    hbox spacing 30:
        xpos 0.6125
        ypos 0
        textbutton "Да" action [Play("test_six", "button.ogg"), SetVariable("collectdevice", 1), Jump("deletecollectables")] 
        textbutton "Нет" action [Play("test_six", "button.ogg"), SetVariable("collectdevice", 1)]



screen collectables1():
    
    vbox spacing 10:
        box_wrap True
        xpos 0.0
        ypos 0.0
        if persistent.collected1 == 1:
            imagebutton:
                action [Play("test_six", "button.ogg"), Show("collected1description")]    # действие при нажатии
                idle "collected1.png"
                hover "collected1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("collected1des")]
                unhovered [Hide("collected1des"), Hide("collected1description")] 
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


        if persistent.collected2 == 1:
            imagebutton:
                action [Play("test_six", "button.ogg"), Show("collected2description")]   # действие при нажатии
                idle "collected2.png"
                hover "collected2.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("collected2des")]
                unhovered [Hide("collected2des"), Hide("collected2description")]
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")

        if persistent.collected3 == 1:
            imagebutton:
                action [Play("test_six", "button.ogg"), Show("collected3description")]    # действие при нажатии
                idle "collected3.png"
                hover "collected3.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("collected3des")]
                unhovered [Hide("collected3des"), Hide("collected3description")]
        else:
            imagebutton:
                action NullAction()
                idle "achievment.png"
                hover "achievment1.png"
                hovered [Play("sound", "audio/buttonselected.mp3"), Show("achievkanulldes")]
                unhovered Hide("achievkanulldes")


###################################### Музыка ##########################################

#screen musicscreen():

###################################### Фоны ##########################################

#screen backgroundscreen():
                

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Экраны загрузки и сохранения ################################################
##
## Эти экраны ответственны за возможность сохранять и загружать игру. Так
## как они почти одинаковые, оба реализованы по правилам третьего экрана —
## file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save

screen save():
    $ persistent.hideafterprologue = 0
    tag menu
    
    use file_slots(_("Сохранить"))


screen load():
    
    $ persistent.hideafterprologue = 0
    tag menu

    use file_slots(_("Загрузить"))
    use backtogame2


screen file_slots(title):
    
    style_prefix "navigation"
    add "images/dark.jpg" xpos 0.5 ypos 0.5
    default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))

    use game_menu(title):
        fixed:

            ## Это гарантирует, что ввод будет принимать enter перед остальными
            ## кнопками.
            order_reverse True

            ## Номер страницы, который может быть изменён посредством клика на
            ## кнопку.
            button:
                style "page_label"
                key_events True
                xalign 9.0
                yalign 9.9
                action [Play("test_six", "button.ogg"),page_name_value.Toggle()]
             

                input:
                    style "page_label_text"
                    value page_name_value

            ## Таблица слотов.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.2
                yalign 0.2

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action [Play("test_six", "button.ogg"),FileAction(slot)]
                        hovered Play("test_six", "audio/buttonselected.mp3")

                        has vbox spacing 10

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M"), empty=_("Пустой слот")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action [Play("test_six", "button.ogg"),FileDelete(slot)]
                        
                        
                        

            ## Кнопки для доступа к другим страницам.
            vbox spacing 0:
                style_prefix "page"

                xalign 0.95
                yalign 0.1

                
                if config.has_autosave:
                    textbutton _("{#auto_page}Автосохр.") action [Play("test_six", "button.ogg"),FilePage("auto")]:
                        hovered Play("sound", "audio/buttonselected.mp3")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Быстр.сохр.") action [Play("test_six", "button.ogg"),FilePage("quick")]:
                        hovered Play("sound", "audio/buttonselected.mp3")
                
                ## range(1, 10) задаёт диапазон значений от 1 до 9.
                for page in range(1, 8):
                    textbutton "[page] страница" action [Play("test_six", "button.ogg"),FilePage(page)]:
                        hovered Play("sound", "audio/buttonselected.mp3")


                if config.has_quicksave:
                    textbutton _("{#quick_page}{color=#ff0000}Сотри всех") action [Play("test_six", "button.ogg"), Hide("navigation"), Hide("save"), Hide("load"), Show("deletealltimelines")]:
                        hovered Play("sound", "audio/buttonselected.mp3")




style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Экран настроек ##############################################################
##
## Экран настроек позволяет игроку настраивать игру под себя.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():
    
    $ persistent.hideafterprologue = 0
    tag menu    
    use game_menu(_("Настройки"), scroll="viewport"):

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
                            bar value Preference("music volume") xsize 200
                        

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
                    textbutton _("Без звука"):
                        action [Jump('screamer10'), Preference("all mute", "toggle")]
                        hovered Play("sound", "audio/buttonselected.mp3")
                        style "mute_all_button"
                textbutton "{color=#020202}{size=15}{font=Wingdings.ttf}You won't get anywhere by covering your ears." action NullAction()
    use backtogame2


transform ears:
    alpha 0.0
    pause 2
    easein 1 alpha 1.0
    pause 4
    easein 2 alpha 0.0

transform ears2:
    pause 5.0
    alpha 0.0
    easein 2 alpha 1.0


screen message_for_you:
    zorder 99999999
    add "blackbg3.png" xalign 0.5 yalign 0.5 
    text"{color=#ffffff}{size=45}{font=Wingdings.ttf}YOU WON'T ESCAPE BY COVERING YOUR EARS.{/font}*" xalign 0.5 yalign 0.5 at ears

screen scream_screen:
    zorder 99999999
    add "scream"

label screamer10:
    hide screen check_point
    hide screen main_vbox
    $ config.skipping = False
    $ persistent.screamer1 = 1
    hide ship2
    hide ship3
    hide rukasleva
    hide rukasprava 
    stop music
    play sound "scream.mp3"
    show screen scream_screen
    $ renpy.pause (1.0, hard=True)
    stop sound
    hide screen scream_screen
    show screen message_for_you
    $ renpy.pause (7.0, hard=True)
    pause 7
    $ renpy.full_restart()

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450


## Экран истории ###############################################################
##
## Этот экран показывает игроку историю диалогов. Хотя в этом экране нет ничего
## особенного, он имеет доступ к истории диалогов, хранимом в _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Избегайте предсказывания этого экрана, так как он может быть очень
    ## массивным.
    predict False

    use game_menu(_("История"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

        style_prefix "history"

        for h in _history_list:

            window:

                ## Это всё правильно уравняет, если history_height будет
                ## установлен на None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Берёт цвет из who параметра персонажа, если он
                        ## установлен.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("История диалогов пуста.")


## Это определяет, какие теги могут отображаться на экране истории.

define gui.history_allow_tags = { "alt", "noalt" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Экран помощи ################################################################
##
## Экран, дающий информацию о клавишах управления. Он использует другие экраны
## (keyboard_help, mouse_help, и gamepad_help), чтобы показывать актуальную
## помощь.

define persistent.nepokas = 0

screen help():
    timer 0.001 action Return()
#    $ persistent.hideafterprologue = 0
#    tag menu
#    
#    default device = "keyboard"
#    #use game_menu("Справка")
#    #use backtogame2
#    vbox spacing 40:
#        xpos 50
#        ypos 120
#    
#        hbox:
#            image "gui/button/check_selected_foreground.png"
#            text "Версия игры 12112024(Пролог)"
#        hbox:
#            image "gui/button/check_selected_foreground.png"
#            text "Спасибо всем участникам проекта за энтузиазм и безвозмездно оказанную помощь! Благодарим всех, кто проявлял интерес к \nпроекту и ждал его выхода."#

#        vbox spacing 30:
#            hbox:
#                image "gui/button/check_selected_foreground.png"
#                text "По {a=https://swipe.vg/ru/p/2598}мультиссылке{/a} можно найти игру в ВК, Gamejolt и Itch.io."
#            hbox:
#                image "gui/button/check_selected_foreground.png"
#                text "В группе ВК можно найти {a=https://vk.com/audios-210855366?z=audio_playlist-210855366_1}саундрек{/a} и рассмотреть {a=https://vk.com/album-210855366_293370494}фоны{/a}."
#            hbox:
#                image "gui/button/check_selected_foreground.png"
#                text "Озвучка сделана при поддержке {a=https://vk.com/wbacompany}Клиффорда Крауна{/a} и {a=https://vk.com/ourlittleplanet}Misato{/a}."
#            hbox:
#                xpos -10
#                ypos -20
#                image "gui/button/check_selected_foreground2.png"
#                textbutton "{size=35}{color=#ffff00}Посмотреть титры" action Jump("justtitri")   
        
                
        

default persistent.MainMenunavigation = "0"

        
screen backtogame():
    if main_menu:
        pass
    else:
        vbox:
            at alpha_000
            imagebutton:
                xalign 1.0
                #action [Play("test_six", "button.ogg"), Return()]
                action None #NullАction()
                idle "backbuttonbel.png"
                hover "backbuttonzh.png" 
                hovered Play("sound", "audio/buttonselected.mp3")    

screen backtogame2():
    vbox:
        at alpha_000
        imagebutton:
            xalign 1.0
            #action [Play("test_six", "button.ogg"), SetVariable("persistent.nepokas", 0), Return()]
            action None#NullАction()
            idle "backbuttonbel.png"
            hover "backbuttonzh.png" 
            hovered Play("sound", "audio/buttonselected.mp3")  

################################################################################
## Дополнительные экраны
################################################################################


## Экран подтверждения #########################################################
##
## Экран подтверждения вызывается, когда Ren'Py хочет спросить у игрока вопрос
## Да или Нет.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

default persistent.loading = 0

screen confirm(message, yes_action, no_action):

    ## Гарантирует, что другие экраны будут недоступны, пока показан этот экран.
    modal True

    zorder 9999999999999999

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                #if store.loading == True: 
                #    textbutton _("Да") action [Play("test_six", "button.ogg"),yes_action, Show("hide_after_load"), SetVariable("loading", False)]
                #else:
                textbutton _("Да") action [Play("test_six", "button.ogg"),yes_action]
                
                textbutton _("Нет") action [Play("test_six", "button.ogg"),no_action]

    ## Правый клик и esc, как ответ "Нет".
    key "K_ESCAPE" action [Play("test_six", "button.ogg"),no_action]


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Экран индикатора пропуска ###################################################
##
## Экран индикатора пропуска появляется для того, чтобы показать, что идёт
## пропуск.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 6

            text _("Пропускаю")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Эта трансформация используется, чтобы мигать стрелками одна за другой.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Нам надо использовать шрифт, имеющий в себе символ U+25B8 (стрелку выше).
    font "DejaVuSans.ttf"


## Экран уведомлений ###########################################################
##
## Экран уведомлений используется, чтобы показать игроку оповещение. (Например,
## когда игра автосохранилась, или был сделан скриншот)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Экран NVL ###################################################################
##
## Этот экран используется в диалогах и меню режима NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Показывает диалог или в vpgrid, или в vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Показывает меню, если есть. Меню может показываться некорректно, если
        ## config.narrator_menu установлено на True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Это контролирует максимальное число строк NVL, могущих показываться за раз.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Мобильные варианты
################################################################################

style pref_vbox:
    variant "medium"
    xsize 450

## Раз мышь может не использоваться, мы заменили быстрое меню версией,
## использующей меньше кнопок, но больших по размеру, чтобы их было легче
## касаться.
define quick_menu = False

screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Назад") action [Play("test_six", "button.ogg"),Rollback()]
            textbutton _("Пропуск") action [Play("test_six", "button.ogg"),Skip()] alternate [Play("test_six", "button.ogg"),Skip(fast=True, confirm=True)]
            textbutton _("Авто") action [Play("test_six", "button.ogg"),Preference("auto-forward", "toggle")]
            textbutton _("Меню") action [Play("test_six", "button.ogg"),ShowMenu()]


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 340

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 400

#style bar:
#    variant "small"
#    ysize gui.bar_size
#    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
#    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

#style vbar:
#    variant "small"
#    xsize gui.bar_size
#    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
#    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 600

init python:
    renpy.music.register_channel("test_one", "sfx", False)
    renpy.music.register_channel("test_two", "sfx", False)
    renpy.music.register_channel("test_three", "sfx", False)
    renpy.music.register_channel("test_four", "sfx", False)
    renpy.music.register_channel("test_five", "sfx", False)
    renpy.music.register_channel("test_six", "sfx", False)
