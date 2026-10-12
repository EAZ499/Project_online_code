# Простейшие трансформы ATL для crossfade
transform save_zvezda_fade_out:
    # стартовый альфа 1.0, затем плавно исчезнуть за 3 секунды
    alpha 1.0
    
    #linear 3.0 alpha 0.0
    #pause 0.1
    #linear 0.01 alpha 1.0
    #repeat

transform save_zvezda_fade_in:
    # стартовый альфа 0.0, затем плавно появиться за 3 секунды
    alpha 0.0
    linear 1.5 alpha 1.0
    pause 1.5
    linear 1.5 alpha 0.0
    pause 1.5
    #linear 3.0 alpha 1.0
    repeat


transform par_layer(k=1.0, base_x=0, base_y=0):
    # k — коэффициент "глубины": 0.2 дальний, 1.0 ближний
    # base_x, base_y — базовые смещения
    xoffset parallax_x * k + base_x
    yoffset parallax_y * k + base_y



define strength = 40

transform black_big:
    on show:
        alpha 1.0
        linear 0.3 alpha 0.0
    on hide:
        linear 0.3 alpha 1.0


transform main_vbox:
    #matrixcolor ContrastMatrix(0.5)
    #matrixcolor BrightnessMatrix(0.01)
    alpha 0.0
    easein 2 alpha 1.0


transform main_vbox2:
    #matrixcolor ContrastMatrix(0.5)
    #matrixcolor BrightnessMatrix(0.01)
    on show:
        alpha 0.0
        easein 0.5 alpha 1.0
    on hide:
        easein 0.5 alpha 0.0








default main_menu_style = "new_game"



#screen check_point:
#    modal True
    #timer 0.001 action SetVariable("store.main_menu2_var", "preparing")

#    key "K_TAB" action None 
#    key "K_ESCAPE" action Return()
    #Call("Return_to_game_screen2")



#    timer 0.02 repeat True action Function(parallax_update, strength)

    
#    timer 0.0001 action SetVariable("main_menu_style", "in_game")
#    timer 0.01 action Show("main_vbox")

#    add "black_big.png" at black_big



#    vbox:
#        if store.main_menu2_var == "preparing":
#            #pass
#            at main_menu_up_to_down
#        elif store.main_menu2_var == "begun":
#            at just_alpha
#        else:
#            at bg_is_new_game

#

#        vbox:
#            at main_vbox2
#
#            if store.main_section == "Save" or  store.main_section == "Load": #Потом New_game
#

#                vbox:
#                    at main_vbox
#                    frame:
#                        background "#000000"
#                        
#                        add "Звезда_1.png" xsize 1280 ysize 720 at [save_zvezda_fade_out, par_layer(0.6)]
#                        add "Звезда_2.png" xsize 1280 ysize 720 at [save_zvezda_fade_in, par_layer(0.6)]
#
#            else:
#            #elif store.main_section == "Load": #Потом Save
#                vbox:
#                    at main_vbox
#                   frame:
#                        background "#000000"
#                        add "dusha" xsize 1280 ysize 720 xoffset -230 at par_layer(0.6)
#                        add "black_pol.png" at par_layer(0.6) xoffset -60




default main_section = "New_game"









screen bg_switcher:
    if store.main_section == "New_game":
        $renpy.show_screen("default_bg")
    elif store.main_section == "Save":
        $renpy.show_screen("default_bg_save")
        $renpy.hide_screen("default_bg")
    elif store.main_section == "other":
        $renpy.show_screen("default_bg")
        $renpy.hide_screen("default_bg_save")



transform main_svech_transform:
    alpha 0.0 xalign 0.5 zoom 0.15 yzoom 0.0 blur 10
    subpixel True
    on hover:
        block:
            easein 0.5 alpha 0.3 yzoom 0.1
            #easein 0.4 alpha 0.5 yzoom 0.6
            #easeout 1.2 alpha 0.0 yzoom 0.1
            #pause 0.3
            #repeat

    on idle:
        easein 1.0 alpha 0.0 yzoom 0.0
    
transform main_svech_transform2:
    alpha 0.0 xalign 0.5 yzoom 0.015 xzoom 0.010 blur 10
    subpixel True
    on hover:
        block:
            easein 0.5 alpha 0.3 yzoom 0.1 xzoom 0.005
            #easein 0.4 alpha 0.0 yzoom 0.6 xzoom 0.15
            #easeout 1.2 alpha 0.0 



    on idle:
        easein 1.0 alpha 0.0 yzoom 0.0
        #easein 1.0 alpha 0.0 yzoom 0.005 xzoom 0.01




transform main_svech_transform_bg:
    alpha 0.0 xalign 0.5 zoom 0.25 yzoom 0.0
    subpixel True
    on hover:
        block:
            easein 0.5 alpha 0.3 yzoom 0.15
            #easein 0.4 alpha 0.5 yzoom 0.6
            #easeout 1.2 alpha 0.0 yzoom 0.1
            #pause 0.3
            #repeat

    on idle:
        easein 1.0 alpha 0.0 yzoom 0.0
    
transform main_svech_transform2_bg:
    alpha 0.0 xalign 0.5 yzoom 0.005 xzoom 0.010 blur 10
    subpixel True
    on hover:
        block:
            easein 0.5 alpha 0.3 yzoom 0.15 xzoom 0.0075
            #easein 0.4 alpha 0.0 yzoom 0.6 xzoom 0.15
            #easeout 1.2 alpha 0.0 



    on idle:
        easein 1.0 alpha 0.0 yzoom 0.0
        #easein 1.0 alpha 0.0 yzoom 0.005 xzoom 0.01





transform main_svech_transform_bg_auto:
    alpha 0.0 xalign 0.5 zoom 0.25 yzoom 0.0
    subpixel True

    easein 0.5 alpha 0.3 yzoom 0.15
    #easein 0.4 alpha 0.5 yzoom 0.6
    #easeout 1.2 alpha 0.0 yzoom 0.1
    #pause 0.3
    #repeat

    on idle:
        easein 1.0 alpha 0.0 yzoom 0.0






















transform main_vbox_transform2:
    zoom 1.2
    easein 0.5  zoom 1.4
    on hover:
        matrixcolor TintMatrix("#ffff00") zoom 1.4
        #easein 0.5 zoom 1.4
    on idle:
        matrixcolor TintMatrix("#ffff00") zoom 1.4
        #zoom 1.4


transform main_vbox_transform:
    subpixel False
    on hover:
        matrixcolor TintMatrix("#ffff00")
        easein 0.5 zoom 1.2
    on idle:
        matrixcolor TintMatrix("#ffffff")
        easein 0.5 zoom 1.0

transform main_vbox_transform3:
    on hover:
        matrixcolor TintMatrix("#ffffff")
    on idle:
        matrixcolor TintMatrix("#ffffff")



screen main_vbox:
    style_prefix "battle_menu"
    zorder 999999

    timer 0.01 action Show("main_menu_parallax")




    timer 0.1 action SetVariable("main_menu2_var", "begun")
    #style_prefix "game_menu"
    vbox:
        #if store.main_menu2_var == "preparing":
        #    at main_vbox
        if store.main_menu2_var == "begun":
            at just_alpha       
        else:
            at shift_main_vbox_start

        #at par_layer(0.1)
        xalign 0.95
        yalign 0.35
        spacing 20
        
        yoffset 20

        vbox:
            xalign 0.5
            spacing 30
           
            vbox:
                spacing 10
                add "main_label_3.png" xalign 0.5 yalign 0.3 zoom 0.3
                text "{font=8bitwonder.otf}{size=25}Deltafatetale" xalign 0.5 yalign 0.3

            vbox:
                xalign 0.5
                spacing 10
                textbutton "reset" action Start()
                if store.started == 0:
                    button:
                        xsize 300 ysize 55 xalign 0.5
                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform2_bg
                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform2

                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform_bg
                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform
                        text _("Начать игру") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform 
                        action [Play("test_six", "button.ogg"),SetVariable("main_section", "New_game"), Show("ok_lets_start")] 
                else:
                    button:
                        xsize 300 ysize 55 xalign 0.5

                        text _("Вернуться в игру") size 30 xalign 0.5 yalign 0.5 at main_vbox_transform                             
                        action [Hide("main_vbox"), Hide("main_menu"), Return()]
                    #Call("Return_to_game_screen2") xalign 0.5
                #imagebutton:
                #    idle "left0.png"
                #    hover "left1.png"
                #    action [SetVariable("persistent.loading", 0), Call("Return_to_game_screen4")]
                #textbutton "save" action Show("load_slots")
                if store.started == 1:
                    button:
                        xsize 300 ysize 55 xalign 0.5
                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform2_bg
                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform2

                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform_bg
                        #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform
                        text "Сохранить" size 30 xalign 0.5 yalign 0.5 at main_vbox_transform 
                        action [
                            
                            Function(set_spawn, player_x, player_y, dir="down", reset_followers=False),
                            Hide("game_screen"),
                            Show("game_screen"),
                            Hide("game_screen"),
                            #SetVariable("main_section", "Save"),
                            Hide("main_vbox"),
                            Show("save_slots")
                        ]
                    
                button:
                    xsize 300 ysize 55 xalign 0.5
                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform2_bg
                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform2

                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform_bg
                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform

                    text "Загрузить" size 30 xalign 0.5 yalign 0.5 at main_vbox_transform  
                    action [
                        Function(set_spawn, store.player_x, store.player_y, dir="down", reset_followers=False),
                        Hide("game_screen"),
                        Show("game_screen"),
                        Hide("game_screen"),
                        Hide("main_vbox"),
                        #SetVariable("persistent.loading", 0),
                        #SetVariable("main_section", "Save"),
                        Show("load_slots")
                    ]
                    

                button:
                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform
                    text "Настройки" size 30 xalign 0.5 yalign 0.5 at main_vbox_transform 
                    xsize 300 ysize 55 xalign 0.5
                    action [
                        Function(set_spawn, store.player_x, store.player_y, dir="down", reset_followers=False),
                        Hide("game_screen"),
                        Show("game_screen"),
                        Hide("game_screen"),
                        Hide("main_vbox"),
                        #SetVariable("main_section", "Pref"),
                        Hide("main_vbox"),
                        Show("preferences_new2")
                    ]
                    
                button:
                    xsize 300 ysize 55 xalign 0.5
                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform
                    text "{size=30}Экстра" size 30 xalign 0.5 yalign 0.5 at main_vbox_transform 
                    action [Hide("main_vbox"), Show("about2")]                    

                button:
                    #add "svech_for_button.png" xalign 0.5 yalign 0.5 yoffset 3 at main_svech_transform
                    xsize 300 ysize 55 xalign 0.5
                    text "Выход" size 30 xalign 0.5 yalign 0.5 at main_vbox_transform 
                    action Quit() 
                    

    if store.main_menu2_var == "begun":
        pass
    else:
        imagebutton:
            xpos 0 ypos 0 
            at alpha_000
            idle "blackbg3.png"
            hover "blackbg3.png"
            action NullAction()



        

################################################################################
## Лейблы переходов
################################################################################

#сохранение
#label Return_to_game_screen_save:
#
#    #if store.window_locked != 1:
#    #    $ txt = 0
#
#
#    if room != None:
#        $ set_spawn(player_x,player_y,dir="down", reset_followers=False)
#        hide screen game_screen
#        show screen game_screen
#        hide screen game_screen
#    hide screen main_vbox
#    #pause 0.1
#    show screen load_slots()
#    #call nolabel

#загрузка
#label Return_to_game_screen_load:
#    #window hide
#    #if store.window_locked !=1:
#    #    $ txt = 0
#
#    #if room != None:
#    $ set_spawn(store.player_x, store.player_y,dir="down", reset_followers=False)
#    hide screen game_screen
#    show screen game_screen
#    hide screen game_screen
#    hide screen main_vbox
#
#    $ persistent.loading = 0
#    $store.main_section= "Save"
#    show screen save_slots()
#    #call nolabel


# Настройки
#label Return_to_game_screen_Pref:
#    #window hide
#    #if store.window_locked !=1:
#    #    $ txt = 0
#
#    #if room != None:
#    $ set_spawn(store.player_x,store.player_y,dir="down", reset_followers=False)
#    hide screen game_screen
#    show screen game_screen
#    hide screen game_screen
#
#    hide screen main_vbox
#
#    $store.main_section = "Pref"
#    hide screen main_vbox
#    show screen preferences_new2




label Return_to_game_screen3:
    #window hide
    #$ txt = 0
    $ rpg_save = 0
    hide screen save_slots
    if room != None:
        $ store.sync_equipped_artifacts()
        hide screen check_point
        call screen game_screen
    #call nolabel

label Return_to_game_screen2:
    #window hide
    #   $ txt = 0
    if room !=None:
        $ store.sync_equipped_artifacts()
    hide screen check_point
    hide screen main_vbox
    #if invent == "opened":
        #hide screen artifacts_menu
    #    $ store.invent = "closed"
    #else:
    ## Синхронизируем экипированные артефакты перед выходом
    if room !=None:
        call screen game_screen
    #call nolabel











########## parallax

init python:
    parallax_x = 0.0
    parallax_y = 0.0

    def parallax_update(strength):
        global parallax_x, parallax_y
        w = float(renpy.config.screen_width)
        h = float(renpy.config.screen_height)
        mx, my = renpy.get_mouse_pos()
        # нормируем в -1..1
        nx = (mx / w) * 2.0 - 1.0
        ny = (my / h) * 2.0 - 1.0
        parallax_x = nx * strength
        parallax_y = ny * strength




















################################################################################
## Экран выхода из игры
################################################################################


default escape_hold_time = 0.0

init python:

    def quit_game():
        renpy.quit()

    def check_escape_hold():
        import pygame

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            store.escape_hold_time += 0.1
            if store.escape_hold_time >= 3.0:
                quit_game()
        else:
            store.escape_hold_time = 0.0
            renpy.hide_screen("escape")

screen escape():
    tag escape

    ## фон
    frame:
        xysize (1280, 720)
        background "#000000"

    ## таймер на 0.1 секунды — проверяет удержание клавиши
    timer 0.1 action Function(check_escape_hold) repeat True

    ## текстовое информирование
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20

        text "ВЫХОД ИЗ ИГРЫ" size 40 bold True
        text "Удерживайте ESC для выхода" size 28

        ## обратный отсчёт
        #text "{size=32}{color=#ffffff}" \
        #    "[max(0, 3.0 - escape_hold_time):.1f] сек." / "{/color}{/size}"
