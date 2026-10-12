
screen trader_screen():
    modal True
    text "Тут будет фон для торговца" xalign 0.5 yalign 0.5
    
    timer 0.001 action Show("trader_screen_options")





screen trader_screen_options:

    key "K_ESCAPE" action Jump("close_trader_screen_to_game_menu")
    
    # Затемнение фона
    #add Solid("#000a")
    
    frame:
        xsize 250 ysize 400
        align (0.95, 0.95)
        background "#ffffff"
        frame:
            align (0.5, 0.5)
            xsize 240 ysize 390
            background "#000000"
        
            vbox:
                spacing 15
                xalign 0.5
                
                label "Торговец" xalign 0.5
                
                textbutton "Поговорить":
                    xfill True
                    text_size 30
                    action [Hide("trader_screen_options"), Call("trader_dialogue")]
                
                textbutton "Торговать":
                    xfill True
                    text_size 30
                    action [Show("shop_screen"), Hide("trader_screen_options")]
                    # Предполагаем, что shop_screen уже существует
                
                textbutton "Опознать":
                    xfill True
                    text_size 30
                    action [Show("identify_screen"), Hide("trader_screen_options")]
                    # Предполагаем, что identify_screen уже существует
                
                textbutton "Уйти":
                    xfill True
                    text_size 30
                    action Jump("close_trader_screen_to_game_menu")


screen trader_screen_background:
    text "Тут будет фон для торговца" xalign 0.5 yalign 0.5


# Заглушка для диалога
label trader_dialogue:
    show screen trader_screen_background
    hide screen trader_screen_options
    "Торговец: Приветствую! Что тебя привело ко мне в такой час?"
    "Торговец: Впрочем, не отвечай. Мои товары говорят сами за себя."
    hide screen trader_screen_background
    call screen trader_screen
    #return
