
default xpos_transit= None
default ypos_transit= None
default dir_transit = None 

define blackbg3 = "blackbg3.png"


label transitions:
    
    #$ txt = 0
    
    show blackbg3 at transitions_black
    $renpy.pause(1.0, hard=True)
    hide screen game_screen with dissolve
    
    
    #$ renpy.pause(0.5, hard=True)
    #hide screen game_screen with dissolve
    $ room = fortransition
    $ set_spawn(xpos_transit, ypos_transit, dir_transit)
    $ interact = 0
    #call screen game_screen with dissolve
    #$ renpy.pause(0.5, hard=True)
    hide blackbg3
    call screen game_screen with dissolve
    #$ renpy.pause(9999, hard=True)    
    #call nolabel
    #return

default fortransition = None
transform transitions_black:
    on show:
        alpha 0.0 xoffset offset_y yoffset offset_y 
        easein 1.0 alpha 1.0 
    on hide:
        alpha 1.0 xoffset offset_y yoffset offset_y 
        easein 1.0 alpha 0.0