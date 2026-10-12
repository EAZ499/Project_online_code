
default dialogue_id = None



    


label rpg_dialogues:
    show screen game_screen
    # Проверка dialogue_id для pickups с hp 7, 8, 9
    if dialogue_id == 7:
        "Диалог для pickup с hp 7"
        "Сохранение"
        $ dialogue_id = None
        $ set_spawn (store.player_x, store.player_y, dir="down", reset_followers=False)
        #$ set_spawn(store.player_x, store.player_y, current_dir)
        hide screen game_screen
        $ set_spawn (store.player_x, store.player_y, dir="down", reset_followers=False)
        call screen game_screen
        
        
    elif dialogue_id == 8:
        "Диалог для pickup с hp 8"
        $ dialogue_id = None
    
    elif dialogue_id == 9:
        "Диалог для pickup с hp 9"
        $ dialogue_id = None
        
    else:
        # Обычный RPG диалог
        "Обычный RPG диалог"

    #hide screen game_screen with dissolve
    #show screen game_screen
    #show "blackbg3.png" at transitions_black
    
    #$ renpy.pause(0.5, hard=True)
    #hide screen game_screen with dissolve
    #$ room = fortransition
    #$ xpos_transit = store.player_x
    #$ ypos_transit = store.player_y
    #$ dir_transit = current_dir
    #$ set_spawn(xpos_transit, ypos_transit, dir_transit)

    #$ set_spawn(store.player_x, store.player_y, current_dir)
    #$ interact = 0
    call screen game_screen with dissolve