#                                                       @@@  @@@                                     
#                                                       @@   @@                                      
#                    @@@@@@@@             @@@@@@@@     @@@@@@@@@@                @@@@@@@@            
#                    @@@@@@@@@@@       @@@@@@@@@@@@   @@@@@@@@@@@             @@@@@@@@@@@@           
#                    @@@     @@@@     @@@@            @@@                    @@@@                    
#                    @@@     @@@@   @@@@              @@@                   @@@                      
#                    @@@    @@@@    @@@               @@@                  @@@                       
#                    @@@@@@@@@      @@@               @@@@@@@@@@           @@@                       
#                    @@@   @@@@@@   @@@               @@@@@@@@@@           @@@                       
#                    @@@      @@@@  @@@               @@@                  @@@                       
#                    @@@      @@@@  @@@@              @@@                  @@@@                      
#                    @@@     @@@@    @@@@@            @@@                   @@@@@                    
#                   @@@@@@@@@@@       @@@@@@@@@@@@   @@@@@@@@@@@             @@@@@@@@@@@@           
#                    @@@@@@@              @@@@@@@      @@@@@@@@@@                @@@@@@@                                                                                                                                                                                                                                                                                                                
                                                                                              
                                                                                                                                                                                               
                                                                                                    
#                    @@@@@@@@@@@    @@@@@@@@@@@@@@@@     @@@@@@@@@@                                  
#                    @@@     @@@@   @@@@         @@@     @@@                                         
#                    @@@      @@@@  @@@@         @@@     @@@                                         
#                    @@@      @@@@  @@@@         @@@     @@@                                         
#                    @@@      @@@   @@@@         @@@     @@@                                         
#                    @@@@@@@@@@@    @@@@         @@@     @@@                                         
#                    @@@@@@@@       @@@@         @@@     @@@                                         
#                    @@@            @@@@         @@@     @@@                                         
#                    @@@            @@@@         @@@     @@@                                         
#                    @@@            @@@@         @@@     @@@                                         
#                    @@@            @@@@         @@@     @@@                                         
                                                                                                    
                                                                   





#                                                                       Функции отслеживания переменещения мышки
# --- константа ---
# NOTE(qodo): test write marker — безопасный комментарий, не влияющий на игру
define THRESHOLD = 10          # "хочу реагировать, если мышь сдвинулась ≥10 px"
define THR2 = THRESHOLD**2     # 100  – храним сразу квадрат порога

# --- переменные ---
default last_mouse_pos = None
default mouse_moved    = False


default current_bullet_zone = None
default bulletcollided = 0
default green_bullet_collisions = []
default collision_cooldown_end_time = 0

# Переменные для цикла создания пуль в зоне 2
default zone2_cycle_timer = 0.0
default zone2_cycle_state = 0  # 0 = создание пуль, 1 = пауза 0.5 сек, 2 = создание пуль, 3 = пауза 5 сек
default zone2_last_update_time = 0.0



##                                                               2. Графика игрока (idle + walk)

default spritestyle = "above"
default sprite_suffix = ""



image player_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "up0.png",
    "spritestyle == 'under'", "up0b.png")
image player_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "down0.png",
    "spritestyle == 'under'", "down0b.png")
image player_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "left0.png",
    "spritestyle == 'under'", "left0b.png")
image player_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "right0.png",
    "spritestyle == 'under'", "right0b.png")



image player_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("up0.png",0.15,"up1.png",0.15,"up2.png",0.15,"up3.png",0.15, repeat=True),
    "under",
    Animation("up0b.png",0.15,"up1b.png",0.15,"up2b.png",0.15, "up3b.png",0.15, repeat=True))
image player_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("down0.png",0.15,"down1.png",0.15,"down2.png",0.15, "down3.png",0.15, repeat=True),
    "under",
    Animation("down0b.png",0.15,"down1b.png",0.15,"down2b.png",0.15, "down3b.png",0.15, repeat=True))

image player_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("left0.png",0.15,"left1.png",0.15,"left2.png",0.15, 'left3.png', 0.15, repeat=True),
    "under",
    Animation("left0b.png",0.15,"left1b.png",0.15,"left2b.png",0.15, "left3b.png",0.15, repeat=True))
image player_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("right0.png",0.15,"right1.png",0.15,"right2.png",0.15, "right3.png",0.15, repeat=True),
    "under",
    Animation("right0b.png",0.15,"right1b.png",0.15,"right2b.png",0.15, "right3b.png",0.15, repeat=True))



















#                                                                                                                     Душа




# player_collider будет инициализирован позже, после определения класса GameObject
default player_collider = None

default soul_x = 640        # стартовая позиция по центру вашей 600×600 области
default soul_y = 360




default soulstate = "default"

image soul = ConditionSwitch(
    "soulstate == 'default'",
    "heart1.png",
    "damaged",
    Animation("heart1.png",0.15,"heart2.png",0.15, repeat=True))


























#                                                                     Спутники — аналогичные спрайты


image follower_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "up0.png",
    "spritestyle == 'under'", "up0b.png")
image follower_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "down0.png",
    "spritestyle == 'under'", "down0b.png")
image follower_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "left0.png",
    "spritestyle == 'under'", "left0b.png")
image follower_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "right0.png",
    "spritestyle == 'under'", "right0b.png")


define speedframe = 1


image follower_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("up0.png",0.15,"up1.png",0.15,"up2.png",0.15,"up3.png",0.15, repeat=True),
    "under",
    Animation("up0b.png",0.15,"up1b.png",0.15,"up2b.png",0.15, "up3b.png",0.15, repeat=True))
image follower_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("down0.png",0.15,"down1.png",0.15,"down2.png",0.15, "down3.png",0.15, repeat=True),
    "under",
    Animation("down0b.png",0.15,"down1b.png",0.15,"down2b.png",0.15, "down3b.png",0.15, repeat=True))

image follower_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("left0.png",0.15,"left1.png",0.15,"left2.png",0.15, 'left3.png', 0.15, repeat=True),
    "under",
    Animation("left0b.png",0.15,"left1b.png",0.15,"left2b.png",0.15, "left3b.png",0.15, repeat=True))
image follower_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("right0.png",0.15,"right1.png",0.15,"right2.png",0.15, "right3.png",0.15, repeat=True),
    "under",
    Animation("right0b.png",0.15,"right1b.png",0.15,"right2b.png",0.15, "right3b.png",0.15, repeat=True))


image none_idle_down  = Null()
image none_idle_up    = Null()
image none_idle_left  = Null()
image none_idle_right = Null()
image none_walk_right = Null() 
image none_walk_left  = Null()
image none_walk_up    = Null()
image none_walk_down  = Null()

















# Спрайты для Asriel
image asriel_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "asriel_up1.png",
    "spritestyle == 'under'", "asriel_up1b.png")
image asriel_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "asriel_down1.png",
    "spritestyle == 'under'", "asriel_down1b.png")
image asriel_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "asriel_left1.png",
    "spritestyle == 'under'", "asriel_left1b.png")
image asriel_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "asriel_right1.png",
    "spritestyle == 'under'", "asriel_right1b.png")

image asriel_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("asriel_up1.png", 0.15, "asriel_up2.png", 0.15, "asriel_up1.png", 0.15, "asriel_up3.png", 0.15, repeat=True),
    "under",
    Animation("asriel_up1b.png", 0.15, "asriel_up2b.png", 0.15, "asriel_up1b.png", 0.15, "asriel_up3b.png", 0.15, repeat=True))
image asriel_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("asriel_down1.png", 0.15, "asriel_down2.png", 0.15, "asriel_down1.png", 0.15, "asriel_down3.png", 0.15, repeat=True),
    "under",
    Animation("asriel_down1b.png", 0.15, "asriel_down2b.png", 0.15, "asriel_down1b.png", 0.15, "asriel_down3b.png", 0.15, repeat=True))
image asriel_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("asriel_left1.png", 0.15, "asriel_left2.png", 0.15, "asriel_left1.png", 0.15, "asriel_left3.png", 0.15, repeat=True),
    "under",
    Animation("asriel_left1b.png", 0.15, "asriel_left2b.png", 0.15, "asriel_left1b.png", 0.15, "asriel_left3b.png", 0.15, repeat=True))
image asriel_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("asriel_right1.png", 0.15, "asriel_right2.png", 0.15, "asriel_right1.png", 0.15, "asriel_right3.png", 0.15, repeat=True),
    "under",
    Animation("asriel_right1b.png", 0.15, "asriel_right2b.png", 0.15, "asriel_right1b.png", 0.15, "asriel_right3b.png", 0.15, repeat=True))























# Спрайты для Chara
image chara_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "chara_up1.png",
    "spritestyle == 'under'", "chara_up1b.png")
image chara_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "chara_down1.png",
    "spritestyle == 'under'", "chara_down1b.png")
image chara_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "chara_left1.png",
    "spritestyle == 'under'", "chara_left1b.png")
image chara_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "chara_right1.png",
    "spritestyle == 'under'", "chara_right1b.png")

image chara_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("chara_up1.png", 0.15, "chara_up2.png", 0.15, "chara_up1.png", 0.15, "chara_up3.png", 0.15, repeat=True),
    "under",
    Animation("chara_up1b.png", 0.15, "chara_up2b.png", 0.15, "chara_up1b.png", 0.15, "chara_up3b.png", 0.15, repeat=True))
image chara_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("chara_down1.png", 0.15, "chara_down2.png", 0.15, "chara_down1.png", 0.15, "chara_down3.png", 0.15, repeat=True),
    "under",
    Animation("chara_down1b.png", 0.15, "chara_down2b.png", 0.15, "chara_down1b.png", 0.15, "chara_down3b.png", 0.15, repeat=True))
image chara_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("chara_left1.png", 0.15, "chara_left2.png", 0.15, "chara_left1.png", 0.15, "chara_left3.png", 0.15, repeat=True),
    "under",
    Animation("chara_left1b.png", 0.15, "chara_left2b.png", 0.15, "chara_left1b.png", 0.15, "chara_left3b.png", 0.15, repeat=True))
image chara_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("chara_right1.png", 0.15, "chara_right2.png", 0.15, "chara_right1.png", 0.15, "chara_right3.png", 0.15, repeat=True),
    "under",
    Animation("chara_right1b.png", 0.15, "chara_right2b.png", 0.15, "chara_right1b.png", 0.15, "chara_right3b.png", 0.15, repeat=True))





















# Спрайты для Frisk
image frisk_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "frisk_up1.png",
    "spritestyle == 'under'", "frisk_up1b.png")
image frisk_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "frisk_down1.png",
    "spritestyle == 'under'", "frisk_down1b.png")
image frisk_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "frisk_left1.png",
    "spritestyle == 'under'", "frisk_left1b.png")
image frisk_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "frisk_right1.png",
    "spritestyle == 'under'", "frisk_right1b.png")

image frisk_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("frisk_up1.png", 0.15, "frisk_up2.png", 0.15, "frisk_up1.png", 0.15, "frisk_up3.png", 0.15, repeat=True),
    "under",
    Animation("frisk_up1b.png", 0.15, "frisk_up2b.png", 0.15, "frisk_up1b.png", 0.15, "frisk_up3b.png", 0.15, repeat=True))
image frisk_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("frisk_down1.png", 0.15, "frisk_down2.png", 0.15, "frisk_down1.png", 0.15, "frisk_down3.png", 0.15, repeat=True),
    "under",
    Animation("frisk_down1b.png", 0.15, "frisk_down2b.png", 0.15, "frisk_down1b.png", 0.15, "frisk_down3b.png", 0.15, repeat=True))
image frisk_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("frisk_left1.png", 0.15, "frisk_left2.png", 0.15, "frisk_left1.png", 0.15, "frisk_left3.png", 0.15, repeat=True),
    "under",
    Animation("frisk_left1b.png", 0.15, "frisk_left2b.png", 0.15, "frisk_left1b.png", 0.15, "frisk_left3b.png", 0.15, repeat=True))
image frisk_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("frisk_right1.png", 0.15, "frisk_right2.png", 0.15, "frisk_right1.png", 0.15, "frisk_right3.png", 0.15, repeat=True),
    "under",
    Animation("frisk_right1b.png", 0.15, "frisk_right2b.png", 0.15, "frisk_right1b.png", 0.15, "frisk_right3b.png", 0.15, repeat=True))











# Спрайты для Кловера
image clover_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "clover_up1.png",
    "spritestyle == 'under'", "clover_up1b.png")
image clover_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "clover_down1.png",
    "spritestyle == 'under'", "clover_down1b.png")
image clover_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "clover_left1.png",
    "spritestyle == 'under'", "clover_left1b.png")
image clover_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "clover_right1.png",
    "spritestyle == 'under'", "clover_right1b.png")

image clover_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("clover_up1.png", 0.15, "clover_up2.png", 0.15, "clover_up1.png", 0.15, "clover_up3.png", 0.15, repeat=True),
    "under",
    Animation("clover_up1b.png", 0.15, "clover_up2b.png", 0.15, "clover_up1b.png", 0.15, "clover_up3b.png", 0.15, repeat=True))
image clover_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("clover_down1.png", 0.15, "clover_down2.png", 0.15, "clover_down1.png", 0.15, "clover_down3.png", 0.15, repeat=True),
    "under",
    Animation("clover_down1b.png", 0.15, "clover_down2b.png", 0.15, "clover_down1b.png", 0.15, "clover_down3b.png", 0.15, repeat=True))
image clover_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("clover_left1.png", 0.15, "clover_left2.png", 0.15, "clover_left1.png", 0.15, "clover_left3.png", 0.15, repeat=True),
    "under",
    Animation("clover_left1b.png", 0.15, "clover_left2b.png", 0.15, "clover_left1b.png", 0.15, "clover_left3b.png", 0.15, repeat=True))
image clover_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("clover_right1.png", 0.15, "clover_right2.png", 0.15, "clover_right1.png", 0.15, "clover_right3.png", 0.15, repeat=True),
    "under",
    Animation("clover_right1b.png", 0.15, "clover_right2b.png", 0.15, "clover_right1b.png", 0.15, "clover_right3b.png", 0.15, repeat=True))












# Спрайты для Иззи
image izzy_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "izzy_up1.png",
    "spritestyle == 'under'", "izzy_up1b.png")
image izzy_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "izzy_down1.png",
    "spritestyle == 'under'", "izzy_down1b.png")
image izzy_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "izzy_left1.png",
    "spritestyle == 'under'", "izzy_left1b.png")
image izzy_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "izzy_right1.png",
    "spritestyle == 'under'", "izzy_right1b.png")

image izzy_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("izzy_up1.png", 0.15, "izzy_up2.png", 0.15, "izzy_up1.png", 0.15, "izzy_up3.png", 0.15, repeat=True),
    "under",
    Animation("izzy_up1b.png", 0.15, "izzy_up2b.png", 0.15, "izzy_up1b.png", 0.15, "izzy_up3b.png", 0.15, repeat=True))
image izzy_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("izzy_down1.png", 0.15, "izzy_down2.png", 0.15, "izzy_down1.png", 0.15, "izzy_down3.png", 0.15, repeat=True),
    "under",
    Animation("izzy_down1b.png", 0.15, "izzy_down2b.png", 0.15, "izzy_down1b.png", 0.15, "izzy_down3b.png", 0.15, repeat=True))
image izzy_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("izzy_left1.png", 0.15, "izzy_left2.png", 0.15, "izzy_left1.png", 0.15, "izzy_left3.png", 0.15, repeat=True),
    "under",
    Animation("izzy_left1b.png", 0.15, "izzy_left2b.png", 0.15, "izzy_left1b.png", 0.15, "izzy_left3b.png", 0.15, repeat=True))
image izzy_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("izzy_right1.png", 0.15, "izzy_right2.png", 0.15, "izzy_right1.png", 0.15, "izzy_right3.png", 0.15, repeat=True),
    "under",
    Animation("izzy_right1b.png", 0.15, "izzy_right2b.png", 0.15, "izzy_right1b.png", 0.15, "izzy_right3b.png", 0.15, repeat=True))





















# Спрайты для Седрика
image sedric_idle_up = ConditionSwitch(
    "spritestyle == 'above'", "sedric_up1.png",
    "spritestyle == 'under'", "sedric_up1b.png")
image sedric_idle_down = ConditionSwitch(
    "spritestyle == 'above'", "sedric_down1.png",
    "spritestyle == 'under'", "sedric_down1b.png")
image sedric_idle_left = ConditionSwitch(
    "spritestyle == 'above'", "sedric_left1.png",
    "spritestyle == 'under'", "sedric_left1b.png")
image sedric_idle_right = ConditionSwitch(
    "spritestyle == 'above'", "sedric_right1.png",
    "spritestyle == 'under'", "sedric_right1b.png")

image sedric_walk_up = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("sedric_up1.png", 0.15, "sedric_up2.png", 0.15, "sedric_up1.png", 0.15, "sedric_up3.png", 0.15, repeat=True),
    "under",
    Animation("sedric_up1b.png", 0.15, "sedric_up2b.png", 0.15, "sedric_up1b.png", 0.15, "sedric_up3b.png", 0.15, repeat=True))
image sedric_walk_down = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("sedric_down1.png", 0.15, "sedric_down2.png", 0.15, "sedric_down1.png", 0.15, "sedric_down3.png", 0.15, repeat=True),
    "under",
    Animation("sedric_down1b.png", 0.15, "sedric_down2b.png", 0.15, "sedric_down1b.png", 0.15, "sedric_down3b.png", 0.15, repeat=True))
image sedric_walk_left = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("sedric_left1.png", 0.15, "sedric_left2.png", 0.15, "sedric_left1.png", 0.15, "sedric_left3.png", 0.15, repeat=True),
    "under",
    Animation("sedric_left1b.png", 0.15, "sedric_left2b.png", 0.15, "sedric_left1b.png", 0.15, "sedric_left3b.png", 0.15, repeat=True))
image sedric_walk_right = ConditionSwitch(
    "spritestyle == 'above'",
    Animation("sedric_right1.png", 0.15, "sedric_right2.png", 0.15, "sedric_right1.png", 0.15, "sedric_right3.png", 0.15, repeat=True),
    "under",
    Animation("sedric_right1b.png", 0.15, "sedric_right2b.png", 0.15, "sedric_right1b.png", 0.15, "sedric_right3b.png", 0.15, repeat=True))


















#                                                                   Поля приключений
image class_enchanced = "class_enchanced.png"






























#                                                                              0. Перменные для всего рпг перемещении
default camera_mode = 1  # 0 - фиксированная, 1 - X/Y следуют, 2 - следует X, 3 - следует Y
default current_camera_zone = None
default current_camera_zone_data = None
default camera_target_x = None
default camera_target_y = None
default camera_axis_state = "follow_xy"
default current_dir = "down"
# Список удерживаемых направлений (левый – раньше, правый – последний)
default pressed_dirs  = []
# Параметры экрана и игрока
default SCREEN_WIDTH   = 1280
default SCREEN_HEIGHT  = 720
default SPEED          = 5
default player_w       = 32
default player_h       = 32
default character_hitbox_offset_x = -16
default character_hitbox_offset_y = 33
default COLLISION_MARGIN = 10  # Допуск коллизии: персонаж может зайти на 4 px в край объекта.
default INTERACT = 0
default FOLLOW_DISTANCE = 64  # можно подбирать опытным путём
default followers = []
default STEP_DELAY = 5  # Временное значение, будет пересчитано позже







# История позиций главного героя
default position_history = []  # будет содержать кортежи (x, y)
## 3. Глобальные переменные и флаги
default moving_up    = False
default moving_down  = False
default moving_left  = False
default moving_right = False
default is_moving    = False

default interact   = INTERACT

# Переменные для сохранения координат игрока и последователей
default saved_player_x = None
default saved_player_y = None
default saved_followers = []






init python:
    def get_follow_distance_by_speed():
        speed = getattr(store, "SPEED", 5)

        if speed <= 5:
            return 25

        if speed >= 8:
            return 50

        # Плавный переход между 5 и 8:
        # 5 = 25 px
        # 6 = примерно 33 px
        # 7 = примерно 42 px
        # 8 = 50 px
        return int(25 + (speed - 5) * (25.0 / 3.0))












init python:
    # Если какие-то размеры ещё не определены, ставим безопасные дефолты.
    sw = globals().get("SCREEN_WIDTH", 1280)
    sh = globals().get("SCREEN_HEIGHT", 720)
    pw = globals().get("player_w", 0)
    ph = globals().get("player_h", 0)

    if not hasattr(store, "player_x"):
        store.player_x = (sw - pw) // 2
    if not hasattr(store, "player_y"):
        store.player_y = (sh - ph) // 2

    # (опционально) чтобы больше не ловить NameError на room
    if not hasattr(store, "room"):
        store.room = None


    # --- Bullet zone: гарантируем наличие current_bullet_zone ---
    if not hasattr(store, "current_bullet_zone"):
        # если у тебя уже есть desired_bullet_zone — логично стартовать от него
        if hasattr(store, "desired_bullet_zone"):
            store.current_bullet_zone = store.desired_bullet_zone
        else:
            # поставь то, что у тебя означает "нет зоны" (часто None или 0)
            store.current_bullet_zone = None

    # --- Camera zone: состояние работает по той же схеме, что и bullet zone ---
    if not hasattr(store, "current_camera_zone"):
        store.current_camera_zone = None
    if not hasattr(store, "current_camera_zone_data"):
        store.current_camera_zone_data = None
    if not hasattr(store, "camera_target_x"):
        store.camera_target_x = None
    if not hasattr(store, "camera_target_y"):
        store.camera_target_y = None
    if not hasattr(store, "camera_axis_state"):
        store.camera_axis_state = "follow_xy"











#                                                                                                                                                           # 1. Списки игровых объектов

#                                                                                                                          Списки
default solid_objects = []      # ← ПУСТО!
default pickups       = []




#                                                                                                                        Рамки уворота

# Объекты будут инициализированы позже, после определения класса GameObject
#default rock1  = rock1
#default rock2  = None
#default pick1  = None























init -9999 python:
    # Глобальные контейнеры, которые используются движком комнат
    if not hasattr(store, "solid_objects"):
        store.solid_objects = []
    if not hasattr(store, "pickups"):
        store.pickups = []
    if not hasattr(store, "enemies"):
        store.enemies = []
    if not hasattr(store, "bullets"):
        store.bullets = []

    if not hasattr(store, "active_room_objects"):
        store.active_room_objects = {"solid": [], "pickups": [], "enemies": [], "bullets": []}



#                                                                                                                  Твёрдые и интерактивы

# Враги будут инициализированы позже, после определения класса GameObject
default enemiess = store.enemiess




define char_defs = {
    "Chara": "chara",
    "Asriel" : "asriel",
    "Frisk": "frisk",
    "Clover": "clover",
    "Izzy": "izzy",
    "Sedric": "sedric",
}

default accel_for_bullet_x = 1
default accel_for_bullet_y = 6

# Все определения физических объектов режима приключений собраны здесь,
# чтобы комнаты и зоны можно было копировать одним блоком без риска задеть функции.
define room_object_definitions = {
    "Stadium": {
        "solid": [
            {"x": 300, "y": 200, "w": 32, "h": 32, "image": "object.png", "name": "rock1"},
            {"x": 900, "y": 500, "w": 100, "h": 50, "image": "object_big.png", "name": "rock2"},
            {"x": -500, "y": -500, "w": 50, "h": 150, "image": "wood.png", "name": "wood_solid"},
        ],
        "pickups": [
            {"x": 600, "y": 150, "w": 40, "h": 40, "image": "object2.png", "hp": "дерево", "name": "pick1"},
            {"x": 2270, "y": 400, "w": 60, "h": 20, "image": "object2.png", "hp": "переход", "name": "pick2"},
            {"x": 200, "y": 200, "w": 50, "h": 50, "image": "object2.png", "hp": "магазин", "name": "shopsans"},
            {"x": 200, "y": 500, "w": 50, "h": 50, "image": "object2.png", "hp": "стиралка", "name": "washingmachine"},
            {"x": 200, "y": 700, "w": 50, "h": 50, "image": "object2.png", "hp": "опознание", "name": "check_table"},
            {"x": 1000, "y": 600, "w": 50, "h": 50, "image": "object2.png", "hp": "для_диалога_1", "name": "dialog_pick_7"},
            {"x": 1200, "y": 650, "w": 50, "h": 50, "image": "object2.png", "hp": "для_диалога_2", "name": "dialog_pick_8"},
            {"x": 1400, "y": 700, "w": 50, "h": 50, "image": "object2.png", "hp": "для_диалога_3", "name": "dialog_pick_9"},
            {"x": 1000, "y": 150, "w": 50, "h": 50, "image": "object2.png", "hp": "торговец", "name": "trader"},
            {"x": -200, "y": -200, "w": 50, "h": 50, "image": "object2.png", "hp": "dummy_fight", "name": "dummy_pickup"},
            {"x": 1600, "y": 820, "w": 50, "h": 50, "image": "object2.png", "hp": "dummy2_fight", "name": "dummy2_pickup"},
        ],
        "enemies": [
            {"x": 400, "y": 300, "w": 50, "h": 70, "image": "enemy.png", "name": "enemy1"},
            {"x": 700, "y": 400, "w": 50, "h": 70, "image": "enemy.png", "name": "enemy2"},
        ],
        "bullets": [
            {"x": 300, "y": 300, "w": 30, "h": 30, "image": "object2.png", "name": "bullet1", "dx_per_tick": 6.0, "dy_per_tick": 2.0},
        ],
    },

    "proba": {
        "solid":[
            {"x": 802, "y": 18, "w": 181, "h": 15, "image": None, "name": "solid_1"},
            {"x": 157, "y": 293, "w": 165, "h": 89, "image": None, "name": "solid_2"},
            {"x": 115, "y": 319, "w": 40, "h": 60, "image": None, "name": "solid_3"},
            {"x": 6, "y": 287, "w": 105, "h": 71, "image": None, "name": "solid_4"},
            {"x": 326, "y": 293, "w": 297, "h": 32, "image": None, "name": "solid_5"},
            {"x": 491, "y": 337, "w": 156, "h": 39, "image": None, "name": "solid_6"},
            {"x": 577, "y": 1, "w": 47, "h": 369, "image": None, "name": "solid_7"},
            {"x": 776, "y": 4, "w": 34, "h": 480, "image": None, "name": "solid_8"},
            {"x": 775, "y": 441, "w": 313, "h": 41, "image": None, "name": "solid_9"},
            {"x": 1265, "y": 439, "w": 302, "h": 43, "image": None, "name": "solid_10"},
            {"x": 1549, "y": 3, "w": 20, "h": 426, "image": None, "name": "solid_11"},
            {"x": 4, "y": 301, "w": 8, "h": 1719, "image": None, "name": "solid_12"},
            {"x": 19, "y": 1975, "w": 4058, "h": 45, "image": None, "name": "solid_13"},
            {"x": 1577, "y": 228, "w": 496, "h": 61, "image": None, "name": "solid_14"},
            {"x": 2070, "y": 183, "w": 365, "h": 142, "image": None, "name": "solid_15"},
            {"x": 2437, "y": 197, "w": 1108, "h": 88, "image": None, "name": "solid_16"},
            {"x": 3508, "y": 292, "w": 182, "h": 91, "image": None, "name": "solid_17"},
            {"x": 3844, "y": 292, "w": 173, "h": 89, "image": None, "name": "solid_18"},
            {"x": 3981, "y": 194, "w": 99, "h": 94, "image": None, "name": "solid_19"},
            {"x": 3696, "y": 294, "w": 143, "h": 39, "image": None, "name": "solid_20"},
            {"x": 3, "y": 945, "w": 1490, "h": 296, "image": None, "name": "solid_21"},
            {"x": 167, "y": 1247, "w": 486, "h": 119, "image": None, "name": "solid_22"},
            {"x": 1051, "y": 1241, "w": 218, "h": 123, "image": None, "name": "solid_23"},
            {"x": 1336, "y": 1241, "w": 77, "h": 99, "image": None, "name": "solid_24"},
            {"x": 1272, "y": 1242, "w": 214, "h": 59, "image": None, "name": "solid_25"},
            {"x": 1924, "y": 1204, "w": 44, "h": 134, "image": None, "name": "solid_27"},
            {"x": 1922, "y": 905, "w": 149, "h": 388, "image": None, "name": "solid_28"},
            {"x": 2079, "y": 907, "w": 1998, "h": 279, "image": None, "name": "solid_29"},
            {"x": 2067, "y": 1192, "w": 39, "h": 204, "image": None, "name": "solid_30"},
            {"x": 2185, "y": 1183, "w": 269, "h": 214, "image": None, "name": "solid_31"},
            {"x": 2111, "y": 1228, "w": 71, "h": 136, "image": None, "name": "solid_32"},
            {"x": 2065, "y": 313, "w": 32, "h": 66, "image": None, "name": "solid_33"},
            {"x": 2195, "y": 330, "w": 238, "h": 42, "image": None, "name": "solid_34"},
            {"x": 2831, "y": 1158, "w": 317, "h": 202, "image": None, "name": "solid_35"},
            {"x": 3518, "y": 1183, "w": 317, "h": 160, "image": None, "name": "solid_36"},
            {"x": 4064, "y": 19, "w": 13, "h": 1994, "image": None, "name": "solid_38"},
            {"x": 627, "y": 1, "w": 189, "h": 37, "image": None, "name": "solid_39"},
            {"x": 969, "y": 13, "w": 415, "h": 314, "image": None, "name": "solid_41"},
            {"x": 1389, "y": 175, "w": 157, "h": 153, "image": None, "name": "solid_42"},
            {"x": 1379, "y": 43, "w": 52, "h": 88, "image": None, "name": "solid_43"},
            #Столбы
            {"x": 1828, "y": 871, "w": 40, "h": 100, "image": None, "name": "Столб с движ"},
            {"x": 1923, "y": 1260, "w": 45, "h": 100, "image": None, "name": "Вперёд1"},
            {"x": 1839, "y": 1490, "w": 47, "h": 100, "image": None, "name": "Автовниз"},
            {"x": 17, "y": 1794, "w": 41, "h": 100, "image": None, "name": "Вперёдвниз"},
            {"x": 2692, "y": 390, "w": 40, "h": 100, "image": None, "name": "Автобусверх"},
        ],
        "pickups": [
            {"x": 406, "y": 326, "w": 72, "h": 25, "image": None, "hp": "Izzy", "name": "Дверь иззи"},
            {"x": 1179, "y": 333, "w": 80, "h": 43, "image": None, "hp": "Нормис1вход", "name": "pickups_41"},
            {"x": 898, "y": 40, "w": 171, "h": 33, "image": None, "hp": "Нормис1лужайка", "name": "pickups_42"},
            {"x": 2256, "y": 348, "w": 326, "h": 74, "image": None, "hp": "Остановка", "name": "pickups_43"},
            {"x": 3194, "y": 258, "w": 111, "h": 101, "image": None, "hp": "Папсмагаз", "name": "pickups_44"},
            {"x": 2717, "y": 450, "w": 59, "h": 71, "image": None, "hp": "Остановка", "name": "pickups_45"},
            {"x": 1867, "y": 1547, "w": 85, "h": 56, "image": None, "hp": "Остановка", "name": "pickups_46"},
            {"x": 2262, "y": 1370, "w": 373, "h": 68, "image": None, "hp": "Остановка", "name": "pickups_47"},
            {"x": 234, "y": 377, "w": 138, "h": 41, "image": None, "hp": "Кустиззи1", "name": "pickups_48"},
            {"x": 569, "y": 370, "w": 128, "h": 44, "image": None, "hp": "Кустиззи2", "name": "pickups_49"},
            {"x": 701, "y": 33, "w": 136, "h": 44, "image": None, "hp": "ДворИззи", "name": "pickups_50"},
            {"x": 1455, "y": 325, "w": 162, "h": 71, "image": None, "hp": "Нормис1подвал", "name": "pickups_51"},
            {"x": 1612, "y": 273, "w": 37, "h": 54, "image": None, "hp": "Цветик", "name": "pickups_52"},
            {"x": 620, "y": 207, "w": 26, "h": 93, "image": None, "hp": "Окноиззи", "name": "pickups_53"},
            {"x": 2959, "y": 271, "w": 132, "h": 92, "image": None, "hp": "Папсокно", "name": "pickups_54"},
            {"x": 3076, "y": 292, "w": 78, "h": 51, "image": None, "hp": "Папсцветы", "name": "pickups_55"},
            {"x": 3506, "y": 337, "w": 32, "h": 64, "image": None, "hp": "Нормис2кусты", "name": "pickups_56"},
            {"x": 2580, "y": 288, "w": 184, "h": 47, "image": None, "hp": "За остановкой", "name": "pickups_57"},
            {"x": 3768, "y": 344, "w": 78, "h": 59, "image": None, "hp": "Нормис2", "name": "pickups_58"},
            {"x": 3929, "y": 375, "w": 140, "h": 30, "image": None, "hp": "Нормис2окно", "name": "pickups_59"},
            {"x": 4042, "y": 298, "w": 32, "h": 59, "image": None, "hp": "Нормис2лут", "name": "pickups_60"},
            {"x": 243, "y": 1374, "w": 75, "h": 39, "image": None, "hp": "Фроггитокно1", "name": "pickups_61"},
            {"x": 412, "y": 1385, "w": 119, "h": 75, "image": None, "hp": "Фрггит", "name": "pickups_62"},
            {"x": 576, "y": 1376, "w": 99, "h": 59, "image": None, "hp": "Фрогитокно2", "name": "pickups_63"},
            {"x": 1176, "y": 1370, "w": 71, "h": 39, "image": None, "hp": "Напста", "name": "pickups_64"},
            {"x": 1028, "y": 1272, "w": 38, "h": 49, "image": None, "hp": "Напстамусор", "name": "pickups_65"},
            {"x": 2958, "y": 1390, "w": 112, "h": 70, "image": None, "hp": "Морозики", "name": "pickups_66"},
            {"x": 464, "y": 1940, "w": 59, "h": 40, "image": None, "hp": "белый", "name": "pickups_67"},
            {"x": 1219, "y": 1937, "w": 53, "h": 28, "image": None, "hp": "красный", "name": "pickups_68"},
            {"x": 1701, "y": 1943, "w": 43, "h": 35, "image": None, "hp": "Жёлтый", "name": "pickups_69"},
            {"x": 1859, "y": 1948, "w": 35, "h": 34, "image": None, "hp": "Жёлтый", "name": "pickups_70"},
            {"x": 2416, "y": 1951, "w": 41, "h": 34, "image": None, "hp": "Фиолетовый", "name": "pickups_71"},
            {"x": 3046, "y": 1942, "w": 41, "h": 30, "image": None, "hp": "Синий", "name": "pickups_72"},
            {"x": 3533, "y": 1944, "w": 33, "h": 30, "image": None, "hp": "Зелёный", "name": "pickups_73"},
            {"x": 3165, "y": 1218, "w": 33, "h": 64, "image": None, "hp": None, "name": "pickups_74"},
            {"x": 3677, "y": 1363, "w": 91, "h": 38, "image": None, "hp": "Папилла", "name": "pickups_75"},
            {"x": 3596, "y": 1369, "w": 31, "h": 34, "image": None, "hp": "Кустпапилла1", "name": "pickups_76"},
            {"x": 3748, "y": 1365, "w": 35, "h": 25, "image": None, "hp": "Кустапапилла2", "name": "pickups_77"},
        ],
        "enemies": [],
        "bullets": [],
    },

    "sport_1floor_right": {
        "solid": [],
        "pickups": [
            {"x": 2020, "y": 1600, "w": 40, "h": 20, "image": "object2.png", "hp": "переход", "name": "pick3"},
            {"x": 1200, "y": 900, "w": 50, "h": 50, "image": "object2.png", "hp": "dummy_fight", "name": "dummy_pickup"},
        ],
        "enemies": [],
        "bullets": [],
    },
}

define room_bullet_zone_definitions = {
    "Stadium": [
        # зона 1
        {"id": "Stadium_z1", "x0": 0, "x1": 1000, "y0": 300, "y1": 2000},
        # зона 2 (пример, поменяй под себя)
        {"id": "Stadium_z2", "x0": 1100, "x1": 2100, "y0": 300, "y1": 2000},
    ],
    "proba": [
        {"id": "Pipka", "x0": 956, "x1": 1149, "y0": 1116, "y1": 1187},
    ],
}

# Зоны камеры работают как bulletzone: текущая комната -> список зон -> первая подходящая зона.
# x0/x1/y0/y1 — рамки в мировых координатах игрока.
# Пока координата игрока внутри рамки по оси, камера следует по этой оси;
# когда координата выходит за рамку, цель камеры зажимается на ближайшей границе.
define room_camera_zone_definitions = {
    "Stadium": [
        {"id": "Stadium_cam", "x0": 0, "x1": 2100, "y0": 300, "y1": 2000},
    ],
    "proba": [
        {"id": "Stadium_camera_zone", "x0": 640, "x1": 3440, "y0": 360, "y1": 1656},
    ],
}

# Словарь определений пуль для зон (за пределами init python для доступа к переменным default)
default room_objects_bullets = {
    "Stadium_z1": [
        {"x": 0, "y": 0, "w": 16, "h": 16, "image": "greenbullet.png", "name": "green_bullet", "dx_per_tick": 0*accel_for_bullet_x, "dy_per_tick": 0*accel_for_bullet_y, "hp": "damaged"},


        {"x": 300, "y": 600, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b1", "dx_per_tick": 1.0*accel_for_bullet_x, "dy_per_tick": 1.0*accel_for_bullet_y, "hp": "damaged"},
        {"x": 300, "y": 600, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b1", "dx_per_tick": 1.0*accel_for_bullet_x, "dy_per_tick": 1.0*accel_for_bullet_y, "hp": "damaged"},
        {"x": 150, "y": 100, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b1", "dx_per_tick": 0.5*accel_for_bullet_x, "dy_per_tick": 1.2*accel_for_bullet_y, "hp": "damage"},
        {"x": 200, "y": 150, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b2", "dx_per_tick": 1.5*accel_for_bullet_x, "dy_per_tick": 0.3*accel_for_bullet_y, "hp": "damage"},
        {"x": 250, "y": 200, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b3", "dx_per_tick": 2.0*accel_for_bullet_x, "dy_per_tick": 0.8*accel_for_bullet_y, "hp": "damage"},
        {"x": 300, "y": 250, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b4", "dx_per_tick": 0.2*accel_for_bullet_x, "dy_per_tick": 2.5*accel_for_bullet_y, "hp": "damage"},
        {"x": 350, "y": 300, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b5", "dx_per_tick": 1.8*accel_for_bullet_x, "dy_per_tick": 1.0*accel_for_bullet_y, "hp": "damage"},
        {"x": 400, "y": 350, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b6", "dx_per_tick": 0.7*accel_for_bullet_x, "dy_per_tick": 0.9*accel_for_bullet_y, "hp": "damage"},
        {"x": 450, "y": 400, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b7", "dx_per_tick": 2.8*accel_for_bullet_x, "dy_per_tick": 0.4*accel_for_bullet_y, "hp": "damage"},
        {"x": 500, "y": 450, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b8", "dx_per_tick": 0.3*accel_for_bullet_x, "dy_per_tick": 2.0*accel_for_bullet_y, "hp": "damage"},
        {"x": 550, "y": 500, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b9", "dx_per_tick": 1.2*accel_for_bullet_x, "dy_per_tick": 1.5*accel_for_bullet_y, "hp": "damage"},
        {"x": 600, "y": 550, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b10", "dx_per_tick": 0.9*accel_for_bullet_x, "dy_per_tick": 0.6*accel_for_bullet_y, "hp": "damage"},
        {"x": 180, "y": 580, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b11", "dx_per_tick": 2.2*accel_for_bullet_x, "dy_per_tick": 1.8*accel_for_bullet_y, "hp": "damage"},
        {"x": 230, "y": 520, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b12", "dx_per_tick": 0.4*accel_for_bullet_x, "dy_per_tick": 0.7*accel_for_bullet_y, "hp": "damage"},
        {"x": 280, "y": 470, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b13", "dx_per_tick": 1.6*accel_for_bullet_x, "dy_per_tick": 2.3*accel_for_bullet_y, "hp": "damage"},
        {"x": 330, "y": 420, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b14", "dx_per_tick": 2.5*accel_for_bullet_x, "dy_per_tick": 0.5*accel_for_bullet_y, "hp": "damage"},
        {"x": 380, "y": 370, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b15", "dx_per_tick": 0.8*accel_for_bullet_x, "dy_per_tick": 1.9*accel_for_bullet_y, "hp": "damage"},
        {"x": 430, "y": 320, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b16", "dx_per_tick": 1.4*accel_for_bullet_x, "dy_per_tick": 0.2*accel_for_bullet_y, "hp": "damage"},
        {"x": 480, "y": 270, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b17", "dx_per_tick": 0.6*accel_for_bullet_x, "dy_per_tick": 2.7*accel_for_bullet_y, "hp": "damage"},
        {"x": 530, "y": 220, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b18", "dx_per_tick": 2.9*accel_for_bullet_x, "dy_per_tick": 1.1*accel_for_bullet_y, "hp": "damage"},
        {"x": 580, "y": 170, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b19", "dx_per_tick": 1.0*accel_for_bullet_x, "dy_per_tick": 0.8*accel_for_bullet_y, "hp": "damage"},
        {"x": 630, "y": 120, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b20", "dx_per_tick": 0.5*accel_for_bullet_x, "dy_per_tick": 2.1*accel_for_bullet_y, "hp": "damage"},
        ],
    "Stadium_z2": [
        {"x": 0, "y": 0, "w": 16, "h": 16, "image": "greenbullet.png", "name": "green_bullet", "dx_per_tick": 0, "dy_per_tick": 0, "hp": "damaged"},
    ],

    "Pipka": [
        {"x": 0, "y": 0, "w": 16, "h": 16, "image": "greenbullet.png", "name": "green_bullet", "dx_per_tick": 0, "dy_per_tick": 0, "hp": "damaged"},
        {"x": 1669, "y": 828, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": -5.26, "dy_per_tick": 2.89, "hp": "damage", "name": "bullet_11", "despawn": True},
        {"x": 861, "y": 986, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": 4.3, "dy_per_tick": 4.18, "hp": "damage", "name": "bullet_12", "despawn": True},
        {"x": 927, "y": 1236, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": 3.22, "dy_per_tick": -5.06, "hp": "damage", "name": "bullet_13", "despawn": True},
        {"x": 1170, "y": 959, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": -1.19, "dy_per_tick": 5.88, "hp": "damage", "name": "bullet_14", "despawn": True},
    ],
}






# Инициализация объектов после определения класса GameObject
# === 1. Boundary + управление стенками (без pygame) ============================






transform text1:
    xpos 650 ypos 1000
    easein 1 ypos 200
    pause 2.0
    easein 2 ypos 1000

label piska:
    hide screen game_screen
    "СТОЯТЬ КОВБОЙ, СЭНДНЮДЕС"
    "ИЛИ ПРОХОД НЕ БУДЕТ ОТКРЫТ"
    return























#                                                               Фукнкции для перемещения по экранам. Позже создать условия в зависимости от комнат

screen camera_zone_tracker:
    # Отдельный экран-датчик камеры: каждый кадр сравнивает координаты игрока
    # с рамками room_camera_zone_definitions текущей комнаты.
    timer 0.016 repeat True action Function(sync_camera_zone)

screen timers:
    # Таймеры
    # Проверяем, что функции определены перед использованием
    #if hasattr(store, 'update_movement'):
    #    timer 0.016 repeat True action Function(update_movement)
    #if hasattr(store, 'check_touches'):
    #    timer 0.2 repeat True action Function(check_touches)
    #if hasattr(store, 'update_followers'):
    #    timer 0.016 repeat True action Function(update_followers)
    #if hasattr(store, 'update_bullet'):
    #    timer 0.016 repeat True action Function(update_bullet)

    use camera_zone_tracker
    timer 0.016 repeat True action [Function(update_bullet), Function(update_followers), Function(check_touches), Function(update_movement)]
    #timer 2.0 repeat True action Function(save_coordinates_before_save)
    











# ==============================================================================
# ОБЪЕДИНЕННЫЙ INIT PYTHON БЛОК - все функции и классы в правильном порядке
# ==============================================================================

init python:
    
    # Импорты
    import pygame
    import time
    import copy
    from collections import deque
    
    rect_collision_works = 1

    # ==================== КЛАССЫ ====================
    
    # Универсальный класс для всех объектов
    class GameObject(object):
        def __init__(self, x, y, w, h, image, solid=False, hp=None):
            self.x, self.y = x, y
            self.w, self.h = w, h
            self.image  = image
            self.solid  = solid
            self.hp     = hp
            # ⬇⬇ добавляем "спрайтовые" поля
            self.dir        = "down"   # текущее направление кадра
            self.is_moving  = False    # герой/спутник стоит или идёт
        
        # Методы для сериализации
        def __getstate__(self):
            """Метод для получения состояния объекта при сериализации"""
            state = self.__dict__.copy()
            return state
        
        def __setstate__(self, state):
            """Метод для восстановления состояния объекта при десериализации"""
            self.__dict__.update(state)
            
        # Дополнительные методы сериализации для совместимости с Ren'Py
        def _pers_getstate(self):
            """Метод для получения состояния объекта при сериализации в Ren'Py"""
            return self.__getstate__()
        
        def _pers_setstate(self, state):
            """Метод для восстановления состояния объекта при десериализации в Ren'Py"""
            self.__setstate__(state)
    
    # Класс пули на основе pygame.Rect
    class Bullet:
        """Класс пули на основе pygame.Rect для коллизий и движения"""
        def __init__(self, x, y, w, h, image, dx_per_tick=0.0, dy_per_tick=0.0, hp="damaged", name=""):
            self.rect = pygame.Rect(x, y, w, h)
            self.image = image
            self.dx_per_tick = dx_per_tick
            self.dy_per_tick = dy_per_tick
            self.hp = hp
            self.name = name

        def move(self):
            """Перемещает пулю на dx_per_tick и dy_per_tick"""
            self.rect.x += self.dx_per_tick
            self.rect.y += self.dy_per_tick

        def collider(self):
            """Возвращает pygame.Rect для проверки коллизий"""
            return self.rect

        # Методы для сериализации
        def __getstate__(self):
            """Метод для получения состояния объекта при сериализации"""
            return {
                'rect': self.rect,
                'image': self.image,
                'dx_per_tick': self.dx_per_tick,
                'dy_per_tick': self.dy_per_tick,
                'hp': self.hp,
                'name': self.name
            }
        
        def __setstate__(self, state):
            """Метод для восстановления состояния объекта при десериализации"""
            self.rect = state['rect']
            self.image = state['image']
            self.dx_per_tick = state['dx_per_tick']
            self.dy_per_tick = state['dy_per_tick']
            self.hp = state['hp']
            self.name = state['name']
        
        # Дополнительные методы сериализации для совместимости с Ren'Py
        def _pers_getstate(self):
            """Метод для получения состояния объекта при сериализации в Ren'Py"""
            return self.__getstate__()
        
        def _pers_setstate(self, state):
            """Метод для восстановления состояния объекта при десериализации в Ren'Py"""
            self.__setstate__(state)

    # Класс игрока на основе pygame.Rect для коллизий
    class PlayerRect:
        """Класс игрока на основе pygame.Rect для проверки коллизий"""
        def __init__(self, x, y, w, h):
            self.rect = pygame.Rect(x, y, w, h)

        def update_position(self, x, y):
            """Обновляет позицию игрока"""
            self.rect.x = x
            self.rect.y = y

        def collider(self):
            """Возвращает pygame.Rect для проверки коллизий"""
            return self.rect

        # Методы для сериализации
        def __getstate__(self):
            """Метод для получения состояния объекта при сериализации"""
            return {
                'rect': self.rect
            }
        
        def __setstate__(self, state):
            """Метод для восстановления состояния объекта при десериализации"""
            self.rect = state['rect']
        
        # Дополнительные методы сериализации для совместимости с Ren'Py
        def _pers_getstate(self):
            """Метод для получения состояния объекта при сериализации в Ren'Py"""
            return self.__getstate__()
        
        def _pers_setstate(self, state):
            """Метод для восстановления состояния объекта при десериализации в Ren'Py"""
            self.__setstate__(state)























    # ГЛОБАЛЬНЫЙ класс EmptyFollower (не внутри функции!)
    class EmptyFollower:
        def __init__(self):
            self.x = getattr(store, 'player_x', 640)
            self.y = getattr(store, 'player_y', 360)
            self.w = getattr(store, 'player_w', 64)
            self.h = getattr(store, 'player_h', 64)
            self.kind = None
            self.prefix = "none"
            self.dir = "down"
            self.is_moving = False
        
        # Методы для сериализации
        def __getstate__(self):
            """Метод для получения состояния объекта при сериализации"""
            state = self.__dict__.copy()
            return state
        
        def __setstate__(self, state):
            """Метод для восстановления состояния объекта при десериализации"""
            self.__dict__.update(state)
            
        # Дополнительные методы сериализации для совместимости с Ren'Py
        def _pers_getstate(self):
            """Метод для получения состояния объекта при сериализации в Ren'Py"""
            return self.__getstate__()
        
        def _pers_setstate(self, state):
            """Метод для восстановления состояния объекта при десериализации в Ren'Py"""
            self.__setstate__(state)
            
        # Дополнительные методы сериализации для совместимости с Ren'Py
        def _pers_getstate(self):
            """Метод для получения состояния объекта при сериализации в Ren'Py"""
            return self.__getstate__()
        
        def _pers_setstate(self, state):
            """Метод для восстановления состояния объекта при десериализации в Ren'Py"""
            self.__setstate__(state)
    










    # Класс для границ
    class Boundary(python_object):
        """AABB‑прямоугольник с поддержкой отката Ren'Py."""
        __slots__ = ("x", "y", "w", "h")
        def __init__(self, x, y, w, h):
            self.x, self.y, self.w, self.h = x, y, w, h
        def __repr__(self):
            return f"<Boundary ({self.x},{self.y}) {self.w}×{self.h}>"
        
        # Методы для сериализации
        def __getstate__(self):
            """Метод для получения состояния объекта при сериализации"""
            return {
                'x': self.x,
                'y': self.y,
                'w': self.w,
                'h': self.h
            }
        
        def __setstate__(self, state):
            """Метод для восстановления состояния объекта при десериализации"""
            self.x, self.y, self.w, self.h = state['x'], state['y'], state['w'], state['h']
    
    
    
    
    
    
    
    
    
    
    # ==================== ФУНКЦИИ ====================
    
    # Функции отслеживания перемещения мышки
    def check_mouse_shift():
        # Проверяем, не управляется ли мышь с клавиатуры
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            return  # Не отслеживаем движение при управлении с клавиатуры
            
        mx, my = renpy.get_mouse_pos()

        # первый кадр – просто запоминаем позицию
        if hasattr(store, 'last_mouse_pos') and store.last_mouse_pos is None:
            store.last_mouse_pos = (mx, my)
            if hasattr(store, 'mouse_moved'):
                store.mouse_moved    = False
            return

        # Проверяем, что переменные определены
        if hasattr(store, 'last_mouse_pos') and store.last_mouse_pos is not None:
            lx, ly = store.last_mouse_pos           # предыдущие координаты
            dx, dy = mx - lx, my - ly               # сдвиг по осям
            dist2  = dx*dx + dy*dy                  # КВАДРАТ евклидовой дистанции

            if hasattr(store, 'mouse_moved'):
                store.mouse_moved = dist2 >= THR2       # True/False
            store.last_mouse_pos = (mx, my)         # обновляем память
    
    def follow_mouse_soul2(st, at):
        mx, my = renpy.get_mouse_pos()          # позиция курсора
        # Проверяем, инициализирован ли player_collider
        if hasattr(store, 'player_collider') and store.player_collider is not None:
            store.player_collider.x = mx - 16       # 32×32 → –16/–16 = центр по курсору
            store.player_collider.y = my - 16
        return Transform("soul", xpos=mx-16, ypos=my-16), 0
        # 0 → перерисовывать каждый кадр
        
    def soul_cursor(st, at):
        mx, my = renpy.get_mouse_pos()
        # 32×32 → хотим, чтобы "heart1.png" была центром под курсором
        # Если управление с клавиатуры, используем позицию из player_collider
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            if hasattr(store, 'player_collider') and store.player_collider is not None:
                mx = store.player_collider.x + 16
                my = store.player_collider.y + 16
        return Transform("soul", xpos=mx-16, ypos=my-16), 0

    def white_bar_func(st, at):
        mx, my = renpy.get_mouse_pos()
        # 32×32 → хотим, чтобы "heart1.png" была центром под курсором
        # Если управление с клавиатуры, используем позицию из player_collider
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            if hasattr(store, 'player_collider') and store.player_collider is not None:
                mx = store.player_collider.x + 16
                my = store.player_collider.y + 16
        return Transform("white_bar", xpos=mx-16, ypos=my-16), 0
    
    # Функции для рамок уворота
    def make_borders():
        # Проверяем, что переменные определены
        if (hasattr(store, 'screenxpos') and hasattr(store, 'screenypos') and
            hasattr(store, 'xbord') and hasattr(store, 'ybord')):
            sx, sy = store.screenxpos, store.screenypos
            w,  h  = store.xbord,      store.ybord
            # Проверяем, определен ли класс GameObject
            if hasattr(store, 'GameObject'):
                return [
                    GameObject(sx,     sy,     w, 5, None, solid=True),
                    GameObject(sx,     sy,     5, h, None, solid=True),
                    GameObject(sx,     sy+h,   w, 5, None, solid=True),
                    GameObject(sx+w,   sy,     5, h, None, solid=True),
                ]
            else:
                # Возвращаем пустой список, если GameObject еще не определен
                return []
        else:
            return []

    def add_borders():
        # создаём и запоминаем
        store.current_borders = make_borders()
        
    def remove_borders():
        # Проверяем, что current_borders и solid_objects инициализированы
        if (hasattr(store, 'current_borders') and store.current_borders is not None and
            hasattr(store, 'solid_objects') and store.solid_objects is not None):
            for b in store.current_borders:
                if b in store.solid_objects:
                    store.solid_objects.remove(b)
            store.current_borders = []
    
    # Функции для управления игроком
    def update_player_collider(mx, my):
        # Проверяем, инициализирован ли player_collider
        if hasattr(store, 'player_collider') and store.player_collider is not None:
            store.player_collider.x = mx - 16
            store.player_collider.y = my - 16

    def follow_mouse_player(st, at):
        mx, my = renpy.get_mouse_pos()

        # двигаем твёрдый объект-"кубик"
        update_player_collider(mx, my)

        # Проверяем, что переменные определены
        if hasattr(store, 'is_moving') and hasattr(store, 'current_dir'):
            # какой тег спрайта нужен именно сейчас
            tag = ("player_walk_" if store.is_moving else "player_idle_") + store.current_dir
        else:
            # Используем значения по умолчанию, если переменные еще не определены
            tag = "player_idle_down"

        # возвращаем Displayable и задержку 0 → перерисовывать каждый кадр
        return Transform(tag, xpos=mx-16, ypos=my-16), 0
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Соответствие «противоположных» стрелок
    opposite_dirs = {"up": "down", "down": "up", "left": "right", "right": "left"}

    def set_move(var_name, value):
        """Обработчик нажатий/отжатий стрелок.
        • Перезаписывает флаг moving_*;
        • Поддерживает список pressed_dirs;
        • Вычисляет is_moving и current_dir.
        """
        dir_name = var_name.replace("moving_", "")
        opp_dir  = opposite_dirs[dir_name]
        setattr(store, var_name, value)
        # — 2. key‑down ——————————————————————————————
        if value:
            # Проверяем, что переменные определены
            if hasattr(store, 'pressed_dirs') and store.pressed_dirs is not None:
                # выключаем противоположный флаг и убираем его из списка
                setattr(store, f"moving_{opp_dir}", False)
                if opp_dir in store.pressed_dirs:
                    store.pressed_dirs.remove(opp_dir)

                # добавляем направление в конец списка
                if dir_name not in store.pressed_dirs:
                    store.pressed_dirs.append(dir_name)
        # — 3. key‑up ————————————————————————————————
        else:
            if hasattr(store, 'pressed_dirs') and store.pressed_dirs is not None:
                if dir_name in store.pressed_dirs:
                    store.pressed_dirs.remove(dir_name)
        # --- агрегаты ---
        # Проверяем, что переменные определены
        if (hasattr(store, 'is_moving') and hasattr(store, 'moving_up') and
            hasattr(store, 'moving_down') and hasattr(store, 'moving_left') and
            hasattr(store, 'moving_right')):
            store.is_moving = (
                store.moving_up or store.moving_down or
                store.moving_left or store.moving_right)
        
        # Текущее направление — первый элемент списка (первая нажатая клавиша),
        # или прежнее значение, если список пуст (стояние)
        if (hasattr(store, 'current_dir') and hasattr(store, 'pressed_dirs') and
            store.pressed_dirs):
            store.current_dir = store.pressed_dirs[0]
    
    # Автоклик для регистрации получения пули
    def simulate_click():
        # Проверяем, не управляется ли мышь с клавиатуры
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            return  # Не генерируем клики при управлении с клавиатуры
            
        # Получаем текущую позицию мыши
        mx, my = renpy.get_mouse_pos()
        # Создаем событие клика мыши через pygame
        mousedown_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                        {'pos': (mx, my), 'button': 1})
        mouseup_event = pygame.event.Event(pygame.MOUSEBUTTONUP,
                                        {'pos': (mx, my), 'button': 1})
        
        # Добавляем события в очередь
        pygame.event.post(mousedown_event)
        #renpy.timeout(0.0000000001)
        pygame.event.post(mouseup_event)

    def follow_mouse(st, at):
        mx, my = renpy.get_mouse_pos()
        # Сдвигаем картинку, чтобы курсор был по центру,
        # возвращаем (дисплейбл, время до следующего кадра)
        return Transform("heartdamaged", xpos=mx-16, ypos=my-16), 0   
        # 0 = перерисовать в следующий кадр
        # если хотите ровно 60 fps, замените 0 на 1.0/60.0

    # Ограничения для мыши
    def restrict_mouse_to_area():
        # Проверяем, не управляется ли мышь с клавиатуры
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            return  # Не ограничиваем мышь при управлении с клавиатуры
            
        mx, my = renpy.get_mouse_pos()
        #sw, sh = config.screen_width, config.screen_height

        # Проверяем, что переменные определены
        if (hasattr(store, 'screenxpos') and hasattr(store, 'screenypos') and
            hasattr(store, 'xbord') and hasattr(store, 'ybord')):
            # Границы разрешенной области
            left = store.screenxpos
            right = left + store.xbord
            top = store.screenypos
            bottom = top + store.ybord

            new_x = mx
            new_y = my

            # Проверка каждой стороны отдельно
            if mx < left:
                new_x = left + 8
            elif mx >= right:
                new_x = right - 5
            elif my < top:
                new_y = top + 5
            elif my >= bottom:
                new_y = bottom - 5

            # Переместить мышь, если нужно
            if (mx != new_x or my != new_y):
                renpy.set_mouse_pos(new_x, new_y)

    # Прямоугольная AABB-коллизия
    def rect_collision(o1, o2):
        return (o1.x <  o2.x + o2.w and
                o1.x + o1.w > o2.x and
                o1.y <  o2.y + o2.h and
                o1.y + o1.h > o2.y)

    def make_collision_box(x, y, w, h):
        """Создаёт уменьшенный физический хитбокс персонажа.

        Координаты x/y здесь — координаты персонажа, а не левый верхний
        угол хитбокса. Визуальный спрайт и отладочная отрисовка не меняются.
        """
        margin = max(0, int(getattr(store, "COLLISION_MARGIN", 0) or 0))
        offset_x = getattr(store, "character_hitbox_offset_x", 0)
        offset_y = getattr(store, "character_hitbox_offset_y", 0)
        return GameObject(
            x + offset_x + margin,
            y + offset_y + margin,
            max(1, w - margin * 2),
            max(1, h - margin * 2),
            None
        )

    def try_axis(dx, dy, flag_name, dir_str):
        """
        Пытается сдвинуть игрока на (dx,dy).
        Если путь закрыт – отпускает клавишу flag_name.
        Возвращает True, если сдвиг удался.
        """
        if not getattr(store, flag_name):
            return False            # эта клавиша сейчас не зажата

        # Проверяем, что переменные определены
        if (hasattr(store, 'player_x') and hasattr(store, 'player_y') and
            hasattr(store, 'player_w') and hasattr(store, 'player_h')):
            nx = store.player_x + dx
            ny = store.player_y + dy
            # Проверяем, определен ли класс GameObject
            if hasattr(store, 'GameObject'):
                probe = make_collision_box(
                    nx, ny, store.player_w, store.player_h)
            else:
                probe = None

            if probe is not None and hasattr(store, 'solid_objects') and store.solid_objects is not None:
                if any(rect_collision(probe, o) for o in store.solid_objects):
                    return False
            store.player_x, store.player_y = nx, ny
            return True
        return False

    def aabb(obj, x, y):
        """Быстро создаёт временный прямоугольник того же размера."""
        # Проверяем, определен ли класс GameObject
        if hasattr(store, 'GameObject'):
            return make_collision_box(x, y, obj.w, obj.h)
        else:
            return None

    # Обновление движения игрока с учётом твёрдых объектов
    def update_movement():
        moved = False

        # Проверяем, что переменная SPEED определена
        if hasattr(store, 'SPEED'):
            # 1) сначала — вертикаль (↑/↓)
            #    (вверх проверяем раньше, чтобы при одновременных клавишах
            #     приоритет остался тем же, что был у вас в коде)
            moved |= try_axis(0, -store.SPEED, "moving_up",    "up")
            moved |= try_axis(0,  store.SPEED, "moving_down",  "down")

            # 2) потом — горизонталь (←/→)
            moved |= try_axis(-store.SPEED, 0, "moving_left",  "left")
            moved |= try_axis( store.SPEED, 0, "moving_right", "right")
        
        # Проверяем, что переменная is_moving определена
        if hasattr(store, 'is_moving'):
            store.is_moving = moved
        
        # Синхронизация player_rect с позицией игрока
        if hasattr(store, 'player_rect') and store.player_rect is not None:
            store.player_rect.update_position(store.player_x, store.player_y)
        
        # Проверка и синхронизация зон при движении игрока
        if hasattr(store, 'sync_camera_zone'):
            store.sync_camera_zone()
        if hasattr(store, 'sync_bullet_zone'):
            store.sync_bullet_zone()
    
    def step_once(obj, tx, ty):
        dx, dy = tx - obj.x, ty - obj.y
        if dx == dy == 0:
            return 0, 0

        # Проверяем, что переменная SPEED определена
        if hasattr(store, 'SPEED'):
            # берём максимум ±SPEED, но не перескакиваем цель
            step_x = max(-store.SPEED, min(store.SPEED, dx))
            step_y = max(-store.SPEED, min(store.SPEED, dy))
        else:
            # Используем значение по умолчанию, если SPEED еще не определена
            step_x = max(-5, min(5, dx))
            step_y = max(-5, min(5, dy))

        return step_x, step_y

    # Переменные связанные с движением и спрайтами
    def dir_by_delta(dx, dy, fallback="down"):
        """Возвращает 'up'/'down'/'left'/'right' в зависимости от вектора."""
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        elif dy != 0:
            return "down" if dy > 0 else "up"
        else:
            return fallback      # стоим на месте — оставляем прошлый спрайт

    # Функции для управления последователями
    def history_index_by_distance(total_dist):
        """
        Возвращает такой индекс в position_history,
        на котором накопленный путь героя ≥ total_dist пикселей.
        Если дистанции ещё не набралось – возвращает None.
        """
        if not hasattr(store, 'position_history') or not store.position_history:
            return None
        walked = 0
        for idx in range(len(store.position_history) - 1):
            x1, y1 = store.position_history[idx][:2]
            x2, y2 = store.position_history[idx + 1][:2]
            walked += abs(x1 - x2) + abs(y1 - y2)   # манхэттен; быстрее sqrt
            if walked >= total_dist:
                return idx + 1
        return None









    def update_followers():
        # Динамически пересчитываем STEP_DELAY для изменения расстояния без перезапуска
        if hasattr(store, 'FOLLOW_DISTANCE') and hasattr(store, 'SPEED'):
            store.STEP_DELAY = 10# (store.FOLLOW_DISTANCE + store.SPEED - 1) // store.SPEED
        
        # Проверяем, что переменные определены
        if (hasattr(store, 'player_x') and hasattr(store, 'player_y') and
            hasattr(store, 'current_dir') and hasattr(store, 'is_moving') and
            hasattr(store, 'position_history') and store.position_history is not None):
            # пишем кадр героя
            store.position_history.appendleft((
                store.player_x, store.player_y,
                store.current_dir, store.is_moving))
        else:
            return
            
        # 1) если герой СТОИТ – хвост тоже стоит
        if not store.is_moving:
            if hasattr(store, 'followers') and store.followers is not None:
                for f in store.followers:
                    if f is not None:
                        f.is_moving = False      # сохраняем направление, позиции
            return

        # 2) герой ДВИЖЕТСЯ – каждый делает ровно один шаг
        if hasattr(store, 'followers') and store.followers is not None and hasattr(store, 'STEP_DELAY'):
            for i, f in enumerate(store.followers):
                if f is None:
                    continue
                delay_frames = store.STEP_DELAY * (i + 1)
                if delay_frames >= len(store.position_history):
                    f.is_moving = False
                    continue
                # точка, где был герой delay кадров назад
                tx, ty, target_dir, _ = store.position_history[delay_frames]
                step_x, step_y = step_once(f, tx, ty)
                if step_x == step_y == 0:
                    f.is_moving = False
                    continue
                # Проверяем, что followers не пустой и i > 0
                if i > 0 and store.followers and i-1 < len(store.followers):
                    front_rect = aabb(
                        f,
                        store.followers[i-1].x,
                        store.followers[i-1].y)
                else:
                    front_rect = aabb(
                        f,
                        store.player_x,
                        store.player_y)

                # Последователь тоже не должен цепляться за край препятствия.
                # Используем тот же уменьшенный хитбокс, что и для игрока.
                follower_probe = aabb(f, f.x + step_x, f.y + step_y)
                if (follower_probe is not None and
                        hasattr(store, 'solid_objects') and
                        store.solid_objects is not None and
                        any(rect_collision(follower_probe, obj)
                            for obj in store.solid_objects)):
                    f.is_moving = False
                    continue

                # шаг прошёл – двигаем
                f.x += step_x
                f.y += step_y
                # Используем направление из истории позиций игрока
                f.dir = target_dir
                f.is_moving = True

    # Функция empty_follower - теперь определена ДО использования
    def empty_follower():
        """Функция для получения пустого последователя"""
        if (hasattr(store, 'GameObject') and
            hasattr(store, 'player_x') and hasattr(store, 'player_y') and
            hasattr(store, 'player_w') and hasattr(store, 'player_h')):
            g = store.GameObject(
                store.player_x, store.player_y,
                store.player_w, store.player_h,
                None
            )
            g.kind = None
            g.prefix = "none"
            return g
        else:
            # Используем глобальный класс EmptyFollower
            return EmptyFollower()

    def add_follower(name):
        # Проверяем, что переменные определены
        if not hasattr(store, 'followers') or store.followers is None:
            store.followers = []

        if not hasattr(store, 'char_defs'):
            return False

        # уже есть такой?
        if any(f and f.kind == name for f in store.followers):
            return False

        # ищем пустой слот
        for f in store.followers:
            if f is not None and getattr(f, "kind", None) is None:
                f.kind = name
                f.prefix = store.char_defs.get(name, "none")
                return True

        # если слота нет — создаём новый
        nf = store.empty_follower()
        nf.kind = name
        nf.prefix = store.char_defs.get(name, "none")
        store.followers.append(nf)
        return True

    def remove_follower(name):
        if not (hasattr(store, 'followers') and store.followers is not None and
                hasattr(store, 'current_dir')):
            return False
            
        for f in store.followers:
            if f is not None and f.kind == name:
                f.kind   = None
                f.prefix = "none"
                # сбросим состояние, если нужно:
                f.is_moving = False
                f.dir       = store.current_dir
                return True
        return False
    
    def update_followers_from_picked():
        """
        Обновляет список followers на основе атрибута picked персонажей.
        Вызывается при изменении состава команды.
        """
        # Проверяем, что pers_dict и followers инициализированы
        if not hasattr(store, 'pers_dict') or not hasattr(store, 'followers'):
            return
        
        # Создаем маппинг локально прямо в функции
        character_follower_map = {
            "Азриель": "Asriel",
            "Чара": "Chara",
            "Фриск": "Frisk",
            "Кловер": "Clover",
            "Иззи": "Izzy",
            "Седрик": "Sedric"
        }
        
        if store.pers_dict is None:
            return

        char_defs = getattr(store, 'char_defs', {})

        desired_order = []

        # 1) Приоритетно берём порядок из team_manager.team_slots,
        #    где очередь уже выстроена по current_attacker.
        if (hasattr(store, 'team_manager') and store.team_manager is not None and
            hasattr(store.team_manager, 'team_slots')):
            for char_name in store.team_manager.team_slots[1:]:
                if char_name in character_follower_map:
                    desired_order.append(character_follower_map[char_name])
        else:
            # 2) Фолбэк: строим по picked и фиксированному attacker order.
            attacker_order = ["Азриель", "Чара", "Фриск", "Иззи", "Кловер", "Седрик"]
            for char_name in attacker_order:
                if char_name in store.pers_dict:
                    character = store.pers_dict[char_name]
                    if hasattr(character, 'picked') and character.picked == 1:
                        desired_order.append(character_follower_map[char_name])

        desired_signature = tuple(desired_order)
        current_order = tuple(
            f.kind for f in (store.followers or [])
            if f is not None and getattr(f, 'kind', None) is not None
        )

        # Если состав и порядок не изменился, не трогаем координаты.
        if (current_order == desired_signature and
            isinstance(store.followers, list) and len(store.followers) >= 3):
            return

        # Переорганизация очереди followers: пересобираем в правильном порядке.
        previous_by_kind = {}
        for follower in store.followers or []:
            if follower is not None and getattr(follower, 'kind', None) is not None:
                previous_by_kind[follower.kind] = follower

        rebuilt_followers = []
        for sprite_key in desired_order:
            follower = previous_by_kind.get(sprite_key)
            if follower is None:
                follower = store.empty_follower()

            follower.kind = sprite_key
            follower.prefix = char_defs.get(sprite_key, 'none')
            follower.x = getattr(store, 'player_x', getattr(follower, 'x', 0))
            follower.y = getattr(store, 'player_y', getattr(follower, 'y', 0))
            follower.w = getattr(store, 'player_w', 32)
            follower.h = getattr(store, 'player_h', 32)
            follower.dir = getattr(store, 'current_dir', 'down')
            follower.is_moving = False
            rebuilt_followers.append(follower)

        # Держим постоянный размер списка followers (3 слота).
        while len(rebuilt_followers) < 3:
            empty = store.empty_follower()
            empty.kind = None
            empty.prefix = 'none'
            empty.x = getattr(store, 'player_x', getattr(empty, 'x', 0))
            empty.y = getattr(store, 'player_y', getattr(empty, 'y', 0))
            empty.w = getattr(store, 'player_w', 32)
            empty.h = getattr(store, 'player_h', 32)
            empty.dir = getattr(store, 'current_dir', 'down')
            empty.is_moving = False
            rebuilt_followers.append(empty)

        store.followers = rebuilt_followers

    def stop_movement():
        """Останавливает движение игрока - сбрасывает все флаги движения"""
        # Сбрасываем флаги движения
        store.moving_up = False
        store.moving_down = False
        store.moving_left = False
        store.moving_right = False
        store.is_moving = False
        # Очищаем список нажатых направлений
        store.pressed_dirs = []

    # Проверка попаданий на «плюшки» и пули, сброс HP к дефолту
    def check_touches():
        # Проверяем, что переменные определены
        if hasattr(store, 'INTERACT'):
            store.interact = store.INTERACT
        
        # Сбрасываем bulletcollided в 0 перед проверкой
        store.bulletcollided = 0
        
        # Проверяем коллизии с пулями через player_hitbox_rect (отдельный pygame.Rect 32x32 для коллизий)
        if hasattr(store, 'player_hitbox_rect') and store.player_hitbox_rect is not None:
            player_collider = store.player_hitbox_rect
            
            # Проверяем коллизии с пулями
            if hasattr(store, 'active_room_objects') and 'bullets' in store.active_room_objects:
                for bullet in store.active_room_objects["bullets"]:
                    if player_collider.colliderect(bullet.collider()):
                        if hasattr(bullet, 'hp'):
                            store.interact = bullet.hp
                            store.bulletcollided = 1
                        return
        
        # Проверяем коллизии с pickups (для совместимости со старой системой)
        if (hasattr(store, 'GameObject') and
            hasattr(store, 'player_x') and hasattr(store, 'player_y') and
            hasattr(store, 'player_w') and hasattr(store, 'player_h')):
            player = GameObject(
                store.player_x + store.character_hitbox_offset_x,
                store.player_y + store.character_hitbox_offset_y,
                store.player_w,
                store.player_h,
                None)
            
            if player is not None:
                # Проверяем коллизии с pickups
                if hasattr(store, 'pickups') and store.pickups is not None:
                    for pu in store.pickups:
                        if rect_collision(player, pu):
                            if hasattr(pu, 'hp'):
                                store.interact = pu.hp
                            return
    
    # Функция проверки коллизий между зелёной пулей и другими пулями
    def check_green_bullet_collisions():
        """
        Проверяет коллизии между зелёной пулей (green_bullet) и всеми остальными пулями.
        Использует pygame.Rect.colliderect для точной проверки пересечения 16x16.
        Возвращает список пуль, с которыми столкнулась зелёная пуля.
        """
        collided_bullets = []
        
        # Получаем список активных пуль
        if not hasattr(store, 'active_room_objects') or 'bullets' not in store.active_room_objects:
            return collided_bullets
        
        bullets = store.active_room_objects["bullets"]
        if not bullets:
            return collided_bullets
        
        # Находим зелёную пулю
        green_bullet = None
        for bullet  in bullets:
            if hasattr(bullet, 'name') and bullet.name == "green_bullet":
                green_bullet = bullet
                break
        
        # Если зелёная пуля не найдена, возвращаем пустой список
        if green_bullet is None:
            return collided_bullets
        
        # Проверяем коллизии зелёной пули со всеми остальными пулями
        for bullet in bullets:
            # Пропускаем саму зелёную пулю
            if bullet is green_bullet:
                continue
            
            # Используем pygame.Rect.colliderect для точной проверки коллизии 16x16
            if hasattr(green_bullet, 'rect') and hasattr(bullet, 'rect'):
                if green_bullet.rect.colliderect(bullet.rect):
                    collided_bullets.append(bullet)
        
        return collided_bullets
 
    # Функция получения смещения камеры
    def get_camera_offset():
        # Проверяем, что переменные определены и не равны None
        has_camera_data = (
            hasattr(store, 'camera_mode') and
            hasattr(store, 'SCREEN_WIDTH') and hasattr(store, 'SCREEN_HEIGHT') and
            hasattr(store, 'player_x') and store.player_x is not None and
            hasattr(store, 'player_y') and store.player_y is not None and
            hasattr(store, 'player_w') and store.player_w is not None and
            hasattr(store, 'player_h') and store.player_h is not None
        )

        if not has_camera_data:
            return 0, 0

        # Если активна camerazone, берём не сырые координаты игрока, а цель камеры.
        # sync_camera_zone() каждый кадр зажимает цель в рамках зоны по каждой оси.
        target_x = getattr(store, 'camera_target_x', None)
        target_y = getattr(store, 'camera_target_y', None)
        if getattr(store, 'current_camera_zone_data', None) is not None and target_x is not None and target_y is not None:
            return (
                store.SCREEN_WIDTH // 2 - target_x - store.player_w // 2,
                store.SCREEN_HEIGHT // 2 - target_y - store.player_h // 2
            )

        # Старый режим остаётся запасным вариантом для комнат без camerazone.
        # Считаем смещение отдельно по каждой оси.
        centered_offset_x = store.SCREEN_WIDTH // 2 - store.player_x - store.player_w // 2
        centered_offset_y = store.SCREEN_HEIGHT // 2 - store.player_y - store.player_h // 2

        if store.camera_mode == 1:
            # 1 - центрированная камера по горизонтали и вертикали.
            offset_x = centered_offset_x
            offset_y = centered_offset_y
        elif store.camera_mode == 2:
            # 2 - центрированная только по горизонтали: X следует за игроком, Y фиксирован.
            offset_x = centered_offset_x
            offset_y = 0
        elif store.camera_mode == 3:
            # 3 - центрированная только по вертикали: Y следует за игроком, X фиксирован.
            offset_x = 0
            offset_y = centered_offset_y
        else:
            # 0 и любые неизвестные значения - фиксированная камера.
            offset_x = 0
            offset_y = 0

        return offset_x, offset_y
    # Функция сохранения координат игрока и последователей и открытия меню артефактов
    def save_and_open_artifacts():
        """
        Сохраняет xyoffset игрока и всех последователей,
        скрывает экран game_screen и открывает экран artifacts_menu
        """
        # Сохраняем координаты игрока
        if hasattr(store, 'player_x') and hasattr(store, 'player_y'):
            store.saved_player_x = store.player_x
            store.saved_player_y = store.player_y
        
        # Сохраняем координаты всех последователей
        if hasattr(store, 'followers') and store.followers is not None:
            store.saved_followers = []
            for f in store.followers:
                if f is not None and hasattr(f, 'x') and hasattr(f, 'y'):
                    store.saved_followers.append({
                        'x': f.x,
                        'y': f.y,
                        'kind': getattr(f, 'kind', None),
                        'prefix': getattr(f, 'prefix', 'none'),
                        'dir': getattr(f, 'dir', 'down'),
                        'is_moving': getattr(f, 'is_moving', False)
                    })
                else:
                    store.saved_followers.append(None)
        else:
            store.saved_followers = []
        
        # Скрываем экран game_screen и открываем artifacts_menu
        #renpy.hide_screen("game_screen")
        #renpy.show_screen("artifacts_menu")
        renpy.call_in_new_context("check_point_for_save_and_open_artifacts")
    

    def save_and_open_artifacts2():
        """
        Сохраняет xyoffset игрока и всех последователей,
        скрывает экран game_screen и открывает экран artifacts_menu
        """
        # Сохраняем координаты игрока
        if hasattr(store, 'player_x') and hasattr(store, 'player_y'):
            store.saved_player_x = store.player_x
            store.saved_player_y = store.player_y
        
        # Сохраняем координаты всех последователей
        if hasattr(store, 'followers') and store.followers is not None:
            store.saved_followers = []
            for f in store.followers:
                if f is not None and hasattr(f, 'x') and hasattr(f, 'y'):
                    store.saved_followers.append({
                        'x': f.x,
                        'y': f.y,
                        'kind': getattr(f, 'kind', None),
                        'prefix': getattr(f, 'prefix', 'none'),
                        'dir': getattr(f, 'dir', 'down'),
                        'is_moving': getattr(f, 'is_moving', False)
                    })
                else:
                    store.saved_followers.append(None)
        else:
            store.saved_followers = []
        
        # Скрываем экран game_screen и открываем artifacts_menu
        #renpy.hide_screen("game_screen")
        #renpy.show_screen("check_point")
        store.main_section = "New_game"
        store.main_section = "Save"
        #store.
        #renpy.call_in_new_context("check_point_for_save_and_open_artifacts2")



    
    # Функция для сохранения координат перед сохранением игры
    def save_coordinates_before_save():
        """
        Сохраняет координаты игрока и последователей
        перед сохранением игры через слоты сохранения Ren'Py.
        Также сохраняет координаты в xpos_transit и ypos_transit.
        """
        # Сохраняем координаты игрока в xpos_transit и ypos_transit
        if hasattr(store, 'player_x') and hasattr(store, 'player_y'):
            store.xpos_transit = store.player_x
            store.ypos_transit = store.player_y
        
        # Сохраняем координаты игрока
        if hasattr(store, 'player_x') and hasattr(store, 'player_y'):
            store.saved_player_x = store.player_x
            store.saved_player_y = store.player_y
        
        # Сохраняем координаты всех последователей
        if hasattr(store, 'followers') and store.followers is not None:
            store.saved_followers = []
            for f in store.followers:
                if f is not None and hasattr(f, 'x') and hasattr(f, 'y'):
                    store.saved_followers.append({
                        'x': f.x,
                        'y': f.y,
                        'kind': getattr(f, 'kind', None),
                        'prefix': getattr(f, 'prefix', 'none'),
                        'dir': getattr(f, 'dir', 'down'),
                        'is_moving': getattr(f, 'is_moving', False)
                    })
                else:
                    store.saved_followers.append(None)
        else:
            store.saved_followers = []


    # Функция для восстановления координат после загрузки игры
    def load_coordinates_after_load():
        """
        Восстанавливает координаты игрока и последователей
        после загрузки игры из сохранения.
        """
        # Восстанавливаем координаты игрока из сохранённых значений
        if (hasattr(store, 'saved_player_x') and hasattr(store, 'saved_player_y') and
            store.saved_player_x is not None and store.saved_player_y is not None):
            store.player_x = store.saved_player_x
            store.player_y = store.saved_player_y
        
        # Восстанавливаем координаты последователей
        if (hasattr(store, 'saved_followers') and store.saved_followers is not None and
            hasattr(store, 'followers') and store.followers is not None):
            for i, saved_f in enumerate(store.saved_followers):
                if i < len(store.followers):
                    if saved_f is not None and store.followers[i] is not None:
                        store.followers[i].x = saved_f.get('x', store.player_x)
                        store.followers[i].y = saved_f.get('y', store.player_y)
                        if hasattr(store.followers[i], 'dir'):
                            store.followers[i].dir = saved_f.get('dir', 'down')
                        if hasattr(store.followers[i], 'is_moving'):
                            store.followers[i].is_moving = saved_f.get('is_moving', False)
        
        # Обновляем позицию игрока в player_rect, если он существует
        if (hasattr(store, 'player_rect') and store.player_rect is not None and
            hasattr(store, 'player_x') and hasattr(store, 'player_y')):
            store.player_rect.update_position(store.player_x, store.player_y)
        
        # Обновляем историю позиций для последователей
        if (hasattr(store, 'position_history') and hasattr(store, 'player_x') and
            hasattr(store, 'player_y') and hasattr(store, 'current_dir') and
            hasattr(store, 'is_moving')):
            from collections import deque
            store.position_history = deque([
                (store.player_x, store.player_y, store.current_dir, store.is_moving)
            ] * 50, maxlen=50)


    # Функция для вызова set_spawn с сохранёнными координатами после загрузки
    def load_spawn_after_load():
        """
        Вызывает set_spawn с сохранёнными координатами
        после загрузки игры из сохранения.
        """
        if (hasattr(store, 'saved_player_x') and hasattr(store, 'saved_player_y') and
            store.saved_player_x is not None and store.saved_player_y is not None and
            hasattr(store, 'set_spawn')):
            store.set_spawn(store.saved_player_x, store.saved_player_y,
                        getattr(store, 'current_dir', 'down'), reset_followers=False)


    # Функции для границ
    def build_restricted_boundaries():
        # Проверяем, что переменные определены
        if (hasattr(store, 'screenxpos') and hasattr(store, 'screenypos') and
            hasattr(store, 'xbord') and hasattr(store, 'ybord')):
            sx, sy = store.screenxpos, store.screenypos
            w,  h  = store.xbord,      store.ybord
            left   = Boundary(sx - 1, sy, 1, h)
            right  = Boundary(sx + w, sy, 1, h)
            top    = Boundary(sx, sy - 1, w, 1)
            bottom = Boundary(sx, sy + h, w, 1)
            return left, right, top, bottom
        else:
            # Возвращаем пустые границы, если переменные еще не определены
            return None, None, None, None

    def sync_restricted_boundaries():
        left, right, top, bottom = build_restricted_boundaries()
        if left is not None and right is not None and top is not None and bottom is not None:
            (
                store.wall_left,
                store.wall_right,
                store.wall_top,
                store.wall_bottom,
            ) = left, right, top, bottom
    
    
    
    
    
    
    
    
    
    
    
    
    























    
    
    
    # ==================== СИСТЕМА УПРАВЛЕНИЯ ОБЪЕКТАМИ КОМНАТ ====================
    
    # Словарь для хранения всех объектов комнат.
    # Данные берутся из room_object_definitions выше, рядом с room_objects_bullets.
    room_objects = copy.deepcopy(store.room_object_definitions)
    for room_data in room_objects.values():
        room_data.setdefault("solid", [])
        room_data.setdefault("pickups", [])
        room_data.setdefault("enemies", [])
        room_data.setdefault("depth_solids", [])
        room_data.setdefault("front_decors", [])
        room_data.setdefault("bullets", [])

    # Хранит активные GameObject для текущей комнаты
    active_room_objects = {
        "solid": [],
        "pickups": [],
        "enemies": [],
        "bullets": []
    }

    # Зоны пуль тоже лежат в общем блоке определений физических объектов.
    bullet_zone_defs = copy.deepcopy(store.room_bullet_zone_definitions)
    camera_zone_defs = copy.deepcopy(store.room_camera_zone_definitions)

    def _in_rect(px, py, z):
        # Проверяем, что координаты прямоугольника определены и не равны None
        if z.get("x0") is None or z.get("x1") is None or z.get("y0") is None or z.get("y1") is None:
            return False
        return (z["x0"] <= px <= z["x1"]) and (z["y0"] <= py <= z["y1"])

    def _clamp(value, low, high):
        return max(low, min(high, value))

    def desired_camera_zone(room_id, px, py):
        """
        Возвращает словарь camerazone для комнаты.
        В отличие от bulletzone, зона камеры остаётся активной и за рамками x0/x1/y0/y1:
        рамки нужны не для выхода из зоны, а для остановки камеры по соответствующей оси.
        Поэтому обычно хватает одной зоны на комнату. Если зон несколько — берётся первая.
        """
        zones = getattr(store, "camera_zone_defs", {}).get(room_id, [])
        if not zones:
            return None

        for z in zones:
            if _in_rect(px, py, z):
                return z

        return zones[0]

    def sync_camera_zone():
        """
        Обновляет режим камеры по координатам игрока так же часто, как sync_bullet_zone().
        Формат зоны: {"id": str, "x0": int, "x1": int, "y0": int, "y1": int}.
        - внутри x0..x1 камера следует по X; вне рамки X цель зажимается на x0 или x1;
        - внутри y0..y1 камера следует по Y; вне рамки Y цель зажимается на y0 или y1.
        camera_mode выставляется для совместимости со старой логикой:
        1 = follow X/Y, 2 = follow X, 3 = follow Y, 0 = обе оси зажаты.
        """
        if not (hasattr(store, "room") and hasattr(store, "player_x") and hasattr(store, "player_y")):
            return

        room_id = store.room
        px = store.player_x
        py = store.player_y
        zone = desired_camera_zone(room_id, px, py)

        if zone is None:
            store.current_camera_zone = None
            store.current_camera_zone_data = None
            store.camera_target_x = None
            store.camera_target_y = None
            store.camera_mode = 1
            store.camera_axis_state = "legacy"
            return

        store.current_camera_zone = zone.get("id")
        store.current_camera_zone_data = zone

        x0, x1 = zone["x0"], zone["x1"]
        y0, y1 = zone["y0"], zone["y1"]
        store.camera_target_x = _clamp(px, x0, x1)
        store.camera_target_y = _clamp(py, y0, y1)

        follow_x = (x0 <= px <= x1)
        follow_y = (y0 <= py <= y1)

        if follow_x and follow_y:
            store.camera_mode = 1
            store.camera_axis_state = "follow_xy"
        elif follow_x:
            store.camera_mode = 2
            store.camera_axis_state = "follow_x_lock_y"
        elif follow_y:
            store.camera_mode = 3
            store.camera_axis_state = "lock_x_follow_y"
        else:
            store.camera_mode = 0
            store.camera_axis_state = "lock_xy"

    def desired_bullet_zone(room_id, px, py):
        """
        Возвращает id зоны (например Stadium_z1), либо None.
        Важно: порядок зон в списке = приоритет (как else-if).
        """
        for z in store.bullet_zone_defs.get(room_id, []):
            if _in_rect(px, py, z):
                return z["id"]
        return None

    def sync_bullet_zone():
        """
        1) Смотрит где игрок.
        2) Если зона изменилась — чистит текущие пули и создаёт новый список из room_objects_bullets[zone_id].
        3) Если игрок вне зон — удаляет все пули.
        """
        room_id = store.room
        px, py = store.player_x, store.player_y

        zone_id = desired_bullet_zone(room_id, px, py)

        current = getattr(store, "current_bullet_zone", None)

        if zone_id == store.current_bullet_zone:
            return

        store.current_bullet_zone = zone_id

        # удаляем активные пули
        store.active_room_objects["bullets"].clear()

        # если вне зоны — всё
        if zone_id is None:

            # Создаём зелёную пулю, если её не было
            add_green_bullet()
            
            return

        # Сбрасываем состояние цикла для зоны 2 при входе
        if zone_id == "Stadium_z2":
            store.zone2_cycle_state = 0
            store.zone2_cycle_timer = 0.0
            store.zone2_last_update_time = 0.0

        # создаём пули зоны заново (с начальными координатами из словаря)
        for obj_data in store.room_objects_bullets.get(zone_id, []):
            # Если это green_bullet, используем текущую позицию игрока со смещением
            if obj_data.get("name") == "green_bullet":
                # Размер пули 16x16, поэтому смещаем на -16 для центрирования
                bullet_x = store.player_x - 8
                bullet_y = store.player_y - 8
            else:
                bullet_x = obj_data["x"]
                bullet_y = obj_data["y"]
            
            b = store.Bullet(
                bullet_x, bullet_y,
                obj_data["w"], obj_data["h"],
                obj_data["image"],
                dx_per_tick=obj_data.get("dx_per_tick", 0.0),
                dy_per_tick=obj_data.get("dy_per_tick", 0.0),
                hp=obj_data.get("hp", "damaged"),
                name=obj_data.get("name", "")
            )
            store.active_room_objects["bullets"].append(b)






    





    # Отдельный словарь для пуль (если нужен отдельно)
    #добавь каждому отдельное смещение
#    room_objects_bullets = {}
#    room_objects_bullets["Stadium_z1"] = [
#        {"x": 300, "y": 600, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b1", "dx_per_tick": 1.0, "dy_per_tick": 1.0, "hp": "damaged"},
#        {"x": 330, "y": 600, "w": 16, "h": 16, "image": "dynamobullet.png", "name": "b1", "dx_per_tick": 0.0, "dy_per_tick": 0.0, "hp": "damaged"},
#        {"x": store.player_x, "y": store.player_y, "w": 32, "h": 32, "image": "dynamobullet.png", "name": "green_bullet", "dx_per_tick": 0, "dy_per_tick": 0, "hp": "damaged"}
#    ]

#    room_objects_bullets["Stadium_z2"] = [
#        {"x": 800, "y": 250, "w": 20, "h": 20, "image": "dynamobullet.png", "name": "b2", "dx_per_tick": -5.0, "dy_per_tick": 1.0},
#    ]
    








    
    def remove_room_objects2(room):
        active_room_objects["bullets"].clear()

    def load_room_objects(room_id):
        """Загружает объекты указанной комнаты в активные списки."""
        room_data = room_objects.get(room_id, {})
        
        # Очищаем активные списки
        active_room_objects["solid"].clear()
        active_room_objects["pickups"].clear()
        active_room_objects["enemies"].clear()
        
        
        # Создаём GameObject для твёрдых объектов
        for obj_data in room_data.get("solid", []):
            obj = GameObject(
                obj_data["x"], obj_data["y"],
                obj_data["w"], obj_data["h"],
                obj_data["image"],
                solid=True
            )
            obj.name = obj_data.get("name", "")
            active_room_objects["solid"].append(obj)
        
        # Создаём GameObject для pickups
        for obj_data in room_data.get("pickups", []):
            obj = GameObject(
                obj_data["x"] - obj_data["w"] // 2,
                obj_data["y"] - obj_data["h"] // 2,
                obj_data["w"], obj_data["h"],
                obj_data["image"],
                solid=False,
                hp=obj_data.get("hp")
            )
            obj.name = obj_data.get("name", "")
            active_room_objects["pickups"].append(obj)
        
        # Создаём GameObject для врагов
        for obj_data in room_data.get("enemies", []):
            obj = GameObject(
                obj_data["x"], obj_data["y"],
                obj_data["w"], obj_data["h"],
                obj_data["image"],
                solid=False
            )
            obj.name = obj_data.get("name", "")
            active_room_objects["enemies"].append(obj)
        
        # Пули загружаются через sync_bullet_zone() при входе в зону
        
        # Обновляем глобальные списки для коллизий
        store.solid_objects.extend(active_room_objects["solid"])
        store.pickups.extend(active_room_objects["pickups"])
        store.enemiess = active_room_objects["enemies"][:]
    
    def clear_room_objects():
        """Очищает все активные списки объектов."""
        # Удаляем объекты из глобальных списков
        for obj in active_room_objects["solid"]:
            if obj in store.solid_objects:
                store.solid_objects.remove(obj)
        
        for obj in active_room_objects["pickups"]:
            if obj in store.pickups:
                store.pickups.remove(obj)
        
        # Очищаем активные списки
        active_room_objects["solid"].clear()
        active_room_objects["pickups"].clear()
        active_room_objects["enemies"].clear()
        active_room_objects["bullets"].clear()
        
        # Очищаем глобальный список врагов
        store.enemiess = []
    
    def get_bullet_pos(bullet_index=0):
        """
        Возвращает координаты пули по индексу, аналогично renpy.get_mouse_pos().
        Если пуля с указанным индексом не существует, возвращает (0, 0).
        
        Параметры:
            bullet_index - индекс пули в списке active_room_objects["bullets"] (по умолчанию 0)
        
        Возвращает:
            Кортеж (x, y) - координаты пули
        """
        bullets = store.active_room_objects.get("bullets", [])
        if 0 <= bullet_index < len(bullets):
            bullet = bullets[bullet_index]
            if hasattr(bullet, 'rect'):
                return (bullet.rect.x, bullet.rect.y)
        return (0, 0)
    
    def spawn_zone2_bullets():
        """Создаёт пули для зоны 2."""
        # Создаём несколько пулей в зоне 2
        bullets_to_spawn = [
            {"x": 800, "y": 250, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": -5.0, "dy_per_tick": 1.0},
            {"x": 850, "y": 300, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": -4.0, "dy_per_tick": 1.5},
            {"x": 900, "y": 350, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": -3.0, "dy_per_tick": 2.0},
            {"x": 950, "y": 400, "w": 20, "h": 20, "image": "dynamobullet.png", "dx_per_tick": -2.0, "dy_per_tick": 2.5},
        ]
        
        for b_data in bullets_to_spawn:
            b = store.Bullet(
                b_data["x"], b_data["y"],
                b_data["w"], b_data["h"],
                b_data["image"],
                dx_per_tick=b_data.get("dx_per_tick", 0.0),
                dy_per_tick=b_data.get("dy_per_tick", 0.0),
                hp="damaged",
                name="zone2_bullet"
            )
            store.active_room_objects["bullets"].append(b)
    
    def update_zone2_cycle():
        """Управляет циклом создания пуль в зоне 2.
        Цикл: создание пуль -> пауза 0.5 сек -> создание пуль -> пауза 5 сек -> повторение."""
        # Проверяем, находимся ли мы в зоне 2
        if store.current_bullet_zone != "Stadium_z2":
            # Сбрасываем состояние цикла если вышли из зоны
            store.zone2_cycle_state = 0
            store.zone2_cycle_timer = 0.0
            return
        
        import time
        current_time = time.time()
        
        # Инициализация времени при первом вызове
        if store.zone2_last_update_time == 0.0:
            store.zone2_last_update_time = current_time
        
        delta_time = current_time - store.zone2_last_update_time
        store.zone2_last_update_time = current_time
        
        # Обновляем таймер
        store.zone2_cycle_timer += delta_time
        
        # Состояние 0: создание пуль
        if store.zone2_cycle_state == 0:
            spawn_zone2_bullets()
            store.zone2_cycle_state = 1
            store.zone2_cycle_timer = 0.0
        
        # Состояние 1: пауза 0.5 сек
        elif store.zone2_cycle_state == 1:
            if store.zone2_cycle_timer >= 0.2:
                store.zone2_cycle_state = 2
                store.zone2_cycle_timer = 0.0
        
        # Состояние 2: создание пуль
        elif store.zone2_cycle_state == 2:
            spawn_zone2_bullets()
            store.zone2_cycle_state = 3
            store.zone2_cycle_timer = 0.0
        
        # Состояние 3: пауза 5 сек
        elif store.zone2_cycle_state == 3:
            if store.zone2_cycle_timer >= 2.0:
                store.zone2_cycle_state = 0
                store.zone2_cycle_timer = 0.0
    
    
    
    
    
    
    
    
    def update_bullet():
        """Обновляет координаты всех пуль, используя метод move() класса Bullet.
        Пуля green_bullet следует за игроком."""
        # Обновляем цикл зоны 2 если мы в ней
        if hasattr(store, 'current_bullet_zone') and store.current_bullet_zone == "Stadium_z2":
            update_zone2_cycle()
        
        # Получаем смещение камеры для расчета границ экрана
        ox, oy = get_camera_offset()
        
        # Границы экрана с учетом смещения камеры и дополнительного отступа
        # Экран: 1280x720, отступ: +640 по X, +360 по Y
        screen_left = -ox - 640
        screen_right = 1280 - ox + 640
        screen_top = -oy - 360
        screen_bottom = 720 - oy + 360
        
        # Удаляем пули, которые вышли за пределы экрана
        active_room_objects["bullets"] = [
            bullet for bullet in active_room_objects["bullets"]
            if not (bullet.rect.x < screen_left or bullet.rect.x > screen_right or
                    bullet.rect.y < screen_top or bullet.rect.y > screen_bottom)
        ]
        
        for bullet in active_room_objects["bullets"]:
            # Если это green_bullet, обновляем её позицию на позицию игрока со смещением
            if hasattr(bullet, 'name') and bullet.name == "green_bullet":
                if hasattr(store, 'player_x') and hasattr(store, 'player_y'):
                    # Позиционируем прямоугольник пули в позиции игрока со смещением -16
                    bullet.rect.x = store.player_x #- 16
                    bullet.rect.y = store.player_y #- 16
            else:
                # Для остальных пуль используем обычное движение
                bullet.move()
        
        # Проверяем коллизии зелёной пули с другими пулями
        if hasattr(store, 'check_green_bullet_collisions'):
            store.green_bullet_collisions = store.check_green_bullet_collisions()
        
        #renpy.restart_interaction()
    
    def remove_green_bullet():
        """Удаляет зелёную пулю из списка активных пуль."""
        if hasattr(store, 'active_room_objects') and 'bullets' in store.active_room_objects:
            store.active_room_objects["bullets"] = [b for b in store.active_room_objects["bullets"] if not (hasattr(b, 'name') and b.name == "green_bullet")]
    
    def add_green_bullet():
        """Добавляет зелёную пулю на позицию игрока."""
        if hasattr(store, 'player_x') and hasattr(store, 'player_y') and store.player_x is not None and store.player_y is not None:
            from store import Bullet
            # Преобразуем координаты в целые числа для pygame.Rect
            bullet = Bullet(
                int(store.player_x), int(store.player_y),
                16, 16,
                "greenbullet.png",
                dx_per_tick=0, dy_per_tick=0,
                hp="damaged",
                name="green_bullet"
            )
            store.active_room_objects["bullets"].append(bullet)
    
    def bullet_single_dd(st, at, bullet_index=0):
        """
        DynamicDisplayable для отображения одной пули с динамическими координатами.
        Аналогично renpy.get_mouse_pos() но для пули.
        """
        bullets = store.active_room_objects.get("bullets", [])
        if 0 <= bullet_index < len(bullets):
            b = bullets[bullet_index]
            ox, oy = store.get_camera_offset()
            # Возвращаем Transform с текущими координатами пули
            # Задержка 0 означает перерисовку каждый кадр
            return Transform(
                Solid("#ff0000", xysize=(b.rect.w, b.rect.h)),
                xpos=b.rect.x + ox,
                ypos=b.rect.y + oy,
                xanchor=0.5,
                yanchor=0.5
            ), 0
        return Null(), 0
    
    def bullets_dd(st, at):
            # если зоны нет — ничего не рисуем
            #if getattr(store, "current_bullet_zone", None) is None:
            #    return Null(), 0

            bullets = store.active_room_objects.get("bullets", [])
            if not bullets:
                return Null(), 0

            # Смещение камеры: если пули "в мире" и должны ездить вместе с камерой — оставь это.
            ox, oy = store.get_camera_offset()

            children = []
            for b in bullets:
                # ВАЖНО: берём b.image и его b.rect.x/b.rect.y каждый кадр
                # Используем xanchor=0.5 и yanchor=0.5 для центрирования пули относительно её rect
                # Это обеспечивает соответствие между визуальным отображением и логикой коллизий
                children.append(
                    Transform(
                        Solid("#ff0000", xysize=(b.rect.w, b.rect.h)),
                        xpos=b.rect.x + ox,
                        ypos=b.rect.y + oy,
                        xanchor=0.5,
                        yanchor=0.5
                    )
                )

            # Fixed собирает все объекты в один слой
            # DynamicDisplayable автоматически перерисовывается каждый кадр (задержка 0)
            # restart_interaction() вызывается в update_bullet(), поэтому здесь не нужен
            return Fixed(*children), 0


    def add_room_object(room_id, obj_type, obj_data):
        """Добавляет объект в комнату динамически."""
        if room_id not in room_objects:
            room_objects[room_id] = {"solid": [], "pickups": [], "enemies": [], "bullets": []}
        room_objects[room_id].setdefault(obj_type, [])
        
        room_objects[room_id][obj_type].append(obj_data)
        
        # Если это текущая комната, сразу добавляем в активные списки
        if room_id == store.room:
            load_room_objects(room_id)
    
    def remove_room_object(room_id, obj_type, obj_name):
        """Удаляет объект из комнаты."""
        if room_id not in room_objects or obj_type not in room_objects[room_id]:
            return False
        
        room_objects[room_id][obj_type] = [
            obj for obj in room_objects[room_id][obj_type]
            if obj.get("name") != obj_name
        ]
        
        # Если это текущая комната, перезагружаем
        if room_id == store.room:
            load_room_objects(room_id)
        
        return True

    def set_spawn(x, y, dir="down", reset_followers=True):
        if dir not in ("up", "down", "left", "right"):
            dir = "down"    
        # 1) игрок
        store.player_x = x
        store.player_y = y
        store.current_dir = dir
        store.is_moving = False

        # Сброс всех флагов движения и списка нажатых клавиш
        store.moving_up = False
        store.moving_down = False
        store.moving_left = False
        store.moving_right = False
        store.pressed_dirs = []

        # 2) очистим историю, иначе followers потянутся к старым координатам
        store.position_history = deque([(x, y, dir, False)] * 50, maxlen=50)

        # 3) followers: либо ровно на игрока, либо "в линию"
        if reset_followers and hasattr(store, "followers") and store.followers:
            for f in store.followers:
                if f is None:
                    continue
                f.x = x
                f.y = y
                f.dir = dir
                f.is_moving = False
        
        # 4) синхронизация player_rect с новой позицией
        if hasattr(store, 'player_rect') and store.player_rect is not None:
            store.player_rect.update_position(x, y)
        
        # 5) синхронизация зон с новой позицией игрока
        if hasattr(store, 'sync_camera_zone'):
            store.sync_camera_zone()
        if hasattr(store, 'sync_bullet_zone'):
            store.sync_bullet_zone()




    # ==================== ИНИЦИАЛИЗАЦИЯ ====================
    
    # Проверяем, что current_borders и solid_objects инициализированы
    if (hasattr(store, 'current_borders') and store.current_borders is not None and
        hasattr(store, 'solid_objects') and store.solid_objects is not None):
        store.solid_objects.extend(store.current_borders)
    
    # Пересчитываем STEP_DELAY после инициализации coffeвсех переменных
    if hasattr(store, 'SPEED'):
        store.FOLLOW_DISTANCE = get_follow_distance_by_speed()
        store.STEP_DELAY = int((store.FOLLOW_DISTANCE + store.SPEED - 1) // store.SPEED)

    # Инициализация position_history как deque для оптимизации
    if not hasattr(store, 'position_history') or not isinstance(store.position_history, deque):
        store.position_history = deque(maxlen=50)

    # Инициализация списка последователей - теперь empty_follower() уже определена!
    if not hasattr(store, 'followers') or store.followers is None:
        # Создаем пустой список последователей
        store.followers = []
    
    # ДОБАВИТЬ: если слотов меньше 3 — дозаполняем
    while len(store.followers) < 3:
        store.followers.append(store.empty_follower())
    
    # Инициализация current_borders
    if hasattr(store, 'make_borders'):
        if not hasattr(store, 'current_borders') or store.current_borders is None:
            store.current_borders = store.make_borders()
        else:
            store.current_borders = store.make_borders()
    
    # Инициализация solid_objects
    if hasattr(store, 'current_borders') and store.current_borders is not None:
        if hasattr(store, 'solid_objects') and store.solid_objects is not None:
            store.solid_objects.extend(store.current_borders)
    
    # Инициализация объектов после определения классов GameObject, Bullet, PlayerRect
    if hasattr(store, 'GameObject') and hasattr(store, 'Bullet') and hasattr(store, 'PlayerRect'):
        store.player_collider = GameObject(0, 32, 2, 2, None, solid=True)
        store.rock1 = GameObject(300, 200,  60, 60, "object.png",     solid=True)
        store.rock2 = GameObject(900, 500, 100, 50, "object_big.png", solid=True)
        store.pick1 = GameObject(600, 150,  40, 40, "object2.png",    hp="дерево")
        store.enemiess = [
            GameObject(400, 300, 50, 70, "enemy.png"),
            GameObject(700, 400, 50, 70, "enemy.png"),
        ]
        
        # Инициализация player_rect в центре экрана для коллизий с пулями
        if hasattr(store, 'SCREEN_WIDTH') and hasattr(store, 'SCREEN_HEIGHT'):
            center_x = store.SCREEN_WIDTH // 2
            center_y = store.SCREEN_HEIGHT // 2
            player_w = getattr(store, 'player_w', 32)
            player_h = getattr(store, 'player_h', 32)
            store.player_rect = PlayerRect(center_x, center_y, player_w, player_h)
        
        # Инициализация player_center_rect - отдельный pygame.Rect для коллизий в центре экрана
        if hasattr(store, 'SCREEN_WIDTH') and hasattr(store, 'SCREEN_HEIGHT'):
            center_x = store.SCREEN_WIDTH // 2
            center_y = store.SCREEN_HEIGHT // 2
            store.player_center_rect = pygame.Rect(center_x, center_y, player_w, player_h)
        
        # Инициализация player_hitbox_rect - отдельный pygame.Rect 32x32 для коллизий с пулями
        if hasattr(store, 'SCREEN_WIDTH') and hasattr(store, 'SCREEN_HEIGHT'):
            center_x = store.SCREEN_WIDTH // 2
            center_y = store.SCREEN_HEIGHT // 2
            store.player_hitbox_rect = pygame.Rect(center_x - 16, center_y - 16, 32, 32)
        
        # Инициализация переменной bulletcollided
        store.bulletcollided = 0
        
        # Инициализация зон при запуске игры (если room уже определён)
        if hasattr(store, 'room') and hasattr(store, 'sync_camera_zone'):
            store.sync_camera_zone()
        if hasattr(store, 'room') and hasattr(store, 'sync_bullet_zone'):
            store.sync_bullet_zone()
  
    # Проверяем, что pers_dict инициализирован
    if hasattr(store, 'pers_dict') and store.pers_dict is not None:
        # Используем новую функцию для обновления followers на основе picked
        if hasattr(store, 'update_followers_from_picked'):
            store.update_followers_from_picked()
    
    
    # Получаем смещение камеры
    # Проверяем, что функция get_camera_offset определена
    if hasattr(store, 'get_camera_offset'):
        offset_x, offset_y = get_camera_offset()
    else:
        offset_x, offset_y = 0, 0
    
    # Проверяем, что followers инициализирован
    if hasattr(store, 'followers') and store.followers is not None:
        for f in store.followers:
            # Проверяем, что f не None
            if f is not None:
                # Проверяем, что атрибуты определены
                if hasattr(f, 'x') and hasattr(f, 'y') and hasattr(f, 'is_moving') and hasattr(f, 'dir') and hasattr(f, 'prefix'):
                    fx, fy = f.x + offset_x, f.y + offset_y
                    state  = "walk" if f.is_moving else "idle"
                    f_sprite = f"{f.prefix}_{state}_{f.dir}"
                    # Удалено: add f_sprite xpos fx ypos fy (это Ren'Py DSL, не Python)


# ==============================================================================
# SCREEN БЛОК - здесь должен быть Ren'Py DSL синтаксис
# ==============================================================================

screen dynamic_entities:
    zorder 1
    $ update_followers_from_picked()
    # Получаем смещение камеры
    $ offset_x, offset_y = get_camera_offset()
    $ render_queue = get_sorted_render_queue()

    # Все спрайты рисуются в одном цикле, строго по глубине.
    for item in render_queue:
        if item["type"] == "solid":
            add Solid(item["color"], xysize=(item["w"], item["h"])):
                xpos item["x"] + offset_x
                ypos item["y"] + offset_y
                anchor item["anchor"]
        elif item.get("xsize") is not None and item.get("ysize") is not None:
            add item["image"]:
                xpos item["x"] + offset_x
                ypos item["y"] + offset_y
                xsize item["xsize"]
                ysize item["ysize"]
                anchor item["anchor"]
        else:
            add item["image"]:
                xpos item["x"] + offset_x
                ypos item["y"] + offset_y
                anchor item["anchor"]

        if item["type"] in ("follower", "player"):
            # Сохраняем существующую отладочную отрисовку хитбоксов.
            $ hx, hy, hw, hh = item["hitbox"]
            add Solid("#ff000080", xysize=(hw, hh)) xpos hx + offset_x ypos hy + offset_y

        if item["type"] == "player":
            if item.get("interact"):
                add "vosklic.png" xpos item["x"] + offset_x + 15 ypos item["y"] + offset_y - 80 xsize 32 ysize 28

            add Solid("#ff0000", xysize=(2, 2)) xpos item["x"] + offset_x ypos item["y"] + offset_y anchor (0.5, 0.5)

    $ flw = getattr(store, "followers", None) or []


    $ pd = getattr(store, "pers_dict", None)


    text "followers len=[len(flw)]" xpos 20 ypos 20

    # Отображение координат игрока
    text "player_xy=[store.player_x], [store.player_y]" xpos 20 ypos 170
    
    if pd is None:
        text "pers_dict = None" xpos 20 ypos 50
    else:
        text "pers_dict keys=[list(pd.keys())]" xpos 20 ypos 50

        if "Азриель" in pd:
            text "Азриель picked=[getattr(pd['Азриель'],'picked', 'NOATTR')]" xpos 20 ypos 80
        if "Чара" in pd:
            text "Чара picked=[getattr(pd['Чара'],'picked', 'NOATTR')]" xpos 20 ypos 110
        if "Фриск" in pd:
            text "Фриск picked=[getattr(pd['Фриск'],'picked', 'NOATTR')]" xpos 20 ypos 140

    text "zone=[getattr(store,'current_bullet_zone',None)]  player=[player_x],[player_y]" xpos 20 ypos 200
    text "camera_zone=[getattr(store,'current_camera_zone',None)] mode=[getattr(store,'camera_mode',None)] axis=[getattr(store,'camera_axis_state',None)]" xpos 20 ypos 215
    text "camera_target=[getattr(store,'camera_target_x',None)], [getattr(store,'camera_target_y',None)]" xpos 20 ypos 245

    text "bullets=[len(active_room_objects['bullets'])]" xpos 20 ypos 275

    if len(active_room_objects["bullets"]) > 0:
        text "xybullet: [active_room_objects['bullets'][0].rect.x], [active_room_objects['bullets'][0].rect.y]" xpos 20 ypos 260
    else:
        text "xybullet: None" xpos 20 ypos 260

    text "bulletcollided: [bulletcollided]" xpos 20 ypos 290

    text "green_bullet_collisions: [len(green_bullet_collisions)]" xpos 20 ypos 350
    text "[store.z_pressed]" xpos 20 ypos 420
    text "[interact]" xpos 20 ypos 450
    text "[speedframe]" xpos 20 ypos 480





    text "[xpos_transit], [ypos_transit]" xpos 20 ypos 390

    if store.control_Kris == 1:

        # Кнопка для отслеживания нажатия клавиши Z
        key "Z" action Show("z_pressed_1")
        key "Я" action Show("z_pressed_1")
        key "z" action Show("z_pressed_1")
        key "я" action Show("z_pressed_1")

        #    key "x" action [SetVariable("sprint", 1), Show ("sprint")]


        key "K_x"       action SetVariable("SPEED", 8)
        key "keyup_K_x" action SetVariable("SPEED", 5)
        
        

        # Управление (keyboard)
        key "K_UP"          action Function(set_move, "moving_up",    True)
        key "keyup_K_UP"    action Function(set_move, "moving_up",    False)
        key "K_DOWN"        action Function(set_move, "moving_down",  True)
        key "keyup_K_DOWN"  action Function(set_move, "moving_down",  False)
        key "K_LEFT"        action Function(set_move, "moving_left",  True)
        key "keyup_K_LEFT"  action Function(set_move, "moving_left",  False)
        key "K_RIGHT"       action Function(set_move, "moving_right", True)
        key "keyup_K_RIGHT" action Function(set_move, "moving_right", False)

default control_Kris = 1
#default sprint = 0
#screen
