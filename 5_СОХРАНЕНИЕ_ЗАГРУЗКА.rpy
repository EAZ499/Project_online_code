################################################################################
## Экраны сохранения и загрузки игры
################################################################################



################################################################################
## Экран сохранения ###########################################################
##
## Этот экран позволяет игроку сохранить игру в один из слотов.

default rpg_save = 0

transform save_appears:
    on show:
        yoffset 800 xalign 0.99 yalign 0.01
        easein 0.5 yoffset 0
    on hide:
        xalign 0.99 yalign 0.01
        easein 0.5 yoffset 800 






screen save_slots:
    zorder 999999999999999999
    #on "show" action Show("default_bg_save")
    #on "hide" action Hide("default_bg_save")

    #vbox:
    #    at main_vbox
    #    frame:
    #        background "#000000"
    #    
    #        add "Звезда_1.png" xsize 1280 ysize 720 at [save_zvezda_fade_out, par_layer(0.6, base_x=0, base_y=0)]
    #        add "Звезда_2.png" xsize 1280 ysize 720 at [save_zvezda_fade_in, par_layer(0.6, base_x=0, base_y=0)]

    timer 0.001 action SetVariable("main_section", "Save")

    key "K_ESCAPE" action [Hide("save_slots"), Show("main_vbox")]

    

    timer 0.02 repeat True action Function(parallax_update, strength)

    #timer 5 action Show("main_vbox")




    #if persistent.loading == 1:
    #    pass
    #else:
    vbox:
        
        at save_appears

        frame:
            xalign 0.5
            yalign 0.5
            xsize 405
            ysize 710
            background None # "#ffffff"
    
            frame:
                background None # "#000000"
                vbox:
                    xalign 0.5
                    yalign 0.5
                    xsize 390
                    ysize 590

                    spacing 10
                    add "main_label_3.png" xalign 0.5 yalign 0.3 zoom 0.3
                    #text "{font=8bitwonder.otf}{size=25}Deltafatetale" xalign 0.5 yalign 0.3

                    vbox:
                        spacing 20
                        xalign 0.5
                        yalign 0.5
                        
                        text "{font=8bitwonder.otf}{size=25}Сохранить":
                            #text_size 40
                            xalign 0.5
                            #text_color "#ffffff"
                            
                        grid 2 4:
                            spacing 20
                            xalign 0.5
                            
                            for i in range(8):
                                $ slot = i + 1
                                
                                button:
                                    xsize 190
                                    ysize 90
                                    background Frame("gui/button/slot_idle_background.png", 10, 10)
                                    hover_background Frame("gui/button/slot_hover_background.png", 10, 10)
                                    action [FileSave(slot), Hide("save_slots"), Show("main_vbox")]
                                    
                                    vbox:
                                        xalign 0.5
                                        yalign 0.5
                                        spacing 5
                                        
                                        #text "Слот [slot]":
                                            #text_size 20
                                            #text_color "#ffffff"
                                        #    xalign 0.5
                                        
                                        text FileTime(slot, format="%d.%m.%Y %H:%M", empty="---"):
                                            size 14
                                            #text_color "#aaaaaa"
                                            xalign 0.5 yalign 0.5 yoffset 15
                                        
                                        text FileSaveName(slot):
                                            #text_size 14
                                            #text_color "#888888"
                                            xalign 0.5
                                            #max_width 300
                                        if FileSaveName(slot):
                                            textbutton "Удалить":
                                                #text_size 12
                                                #text_color "#ff6666"
                                                #hover_text_color "#ff4444"
                                                action FileDelete(slot)
                                                xalign 0.5
                        
                        hbox:
                            spacing 20
                            xalign 0.5
                            
                            textbutton "Назад":
                                xalign 0.5
                                #text_size 20
                                #text_color "#ffffff"
                                action [Hide("save_slots"), Show("main_vbox")]
                                #xysize 150, 50


################################################################################
## Экран загрузки ##############################################################
##
## Этот экран позволяет игроку загрузить игру из одного из слотов.

screen load_slots():
    zorder 99999
    

    #tag menu
    timer 0.001 action SetVariable("main_section", "Save")

    key "K_ESCAPE" action [Hide("load_slots"), Show("main_vbox")]


    timer 0.02 repeat True action Function(parallax_update, strength)



    

    vbox:
        at save_appears

        frame:
            xalign 0.5
            yalign 0.5
            xsize 405
            ysize 710
            background None # "#ffffff"
    
            frame:
                background None # "#000000"
                vbox:
                    xalign 0.5
                    yalign 0.5
                    xsize 390
                    ysize 590

                    spacing 10
                    add "main_label_3.png" xalign 0.5 yalign 0.3 zoom 0.3
                    #text "{font=8bitwonder.otf}{size=25}Deltafatetale" xalign 0.5 yalign 0.3

                    vbox:
                        spacing 20
                        xalign 0.5
                        yalign 0.5
                        
                        text "{font=8bitwonder.otf}{size=25}Загрузить":
                            #text_size 40
                            xalign 0.5
                            #text_color "#ffffff"
                            
                        grid 2 4:
                            spacing 20
                            xalign 0.5
                            
                            for i in range(8):
                                $ slot = i + 1
                                
                                button:
                                    xsize 190
                                    ysize 90
                                    background Frame("gui/button/slot_idle_background.png", 10, 10)
                                    hover_background Frame("gui/button/slot_hover_background.png", 10, 10)
                                    action [Hide("save_slots"), SetVariable("persistent.loading", 1), FileLoad(slot)]
                                    
                                    vbox:
                                        xalign 0.5
                                        yalign 0.5
                                        spacing 5
                                        
                                        #text "Слот [slot]":
                                            #text_size 20
                                            #text_color "#ffffff"
                                        #    xalign 0.5
                                        
                                        text FileTime(slot, format="%d.%m.%Y %H:%M", empty="---"):
                                            size 14
                                            #text_color "#aaaaaa"
                                            xalign 0.5 yalign 0.5 yoffset 15
                                        
                                        text FileSaveName(slot):
                                            #text_size 14
                                            #text_color "#888888"
                                            xalign 0.5
                                            #max_width 300
                                        if FileSaveName(slot):
                                            textbutton "Удалить":
                                                #text_size 12
                                                #text_color "#ff6666"
                                                #hover_text_color "#ff4444"
                                                action FileDelete(slot)
                                                xalign 0.5
                        
                        hbox:
                            spacing 20
                            xalign 0.5
                            
                            textbutton "Назад":
                                xalign 0.5
                                #text_size 20
                                #text_color "#ffffff"
                                action [Hide("load_slots"), Show("main_vbox")]
                                #xysize 150, 50

screen hide_after_load:
    timer 0.5 action Hide("save_slots")
    timer 0.51 action Hide("hide_after_load")
    