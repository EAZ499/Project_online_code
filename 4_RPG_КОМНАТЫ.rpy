#        @@    @@@    @@@@@@     @@@       @@@   @@@@@@@    @@@     @@  @@@@@@@@@ @@@        @@      
#        @@  @@@    @@@    @@@   @@@@     @@@@   @@    @@   @@@     @@     @@@    @@@        @@      
#        @@@@@@    @@@      @@@  @@@@@   @@@@@        @@@@  @@@     @@     @@@    @@@@@@     @@      
#        @@@@      @@       @@@  @@ @@   @@@@@   @@@@@@@@@  @@@@@@@@@@     @@@    @@@@@@@@@  @@      
#        @@ @@@    @@@      @@   @@  @@ @@ @@@  @@@    @@@  @@@     @@     @@@    @@@    @@@ @@      
#        @@   @@@   @@@@  @@@@   @@  @@@@  @@@  @@@   @@@@  @@@     @@     @@@    @@@@@@@@@  @@      
#        @@    @@@@   @@@@@@     @@   @@@  @@@    @@@@ @@@  @@@     @@     @@@    @@@@@@@    @@      
                                                                                                    
                                                                                                    
                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                    
#         @@@@@@@         @@@@@@@@   @@@@@@@@      @@@@@@@    @@@@@@@    @@@@@@@@@   @@@    @@   @@@@    @@    @@@@   @@@      @@@@   @@        @@@  @@@@      @@@  
#       @@@              @@@       @@@     @@@     @@  @@@   @@     @@   @@@     @@    @@@  @@  @@@      @@   @@@@@   @@@@    @@@@@   @@        @@@  @@@@@    @@@@
#       @@@             @@@        @@       @@    @@@  @@@  @@@@@@@@@@@  @@      @@@     @@@@@@@@        @@  @@@@@@   @@@@@  @@@@@@   @@@@@@@@  @@@  @@@@@@  @@ @@
#       @@@             @@@        @@       @@    @@   @@@  @@@          @@      @@@     @@@@@@@@        @@@@@  @@@   @@ @@@ @@ @@@   @@    @@@ @@@  @@@ @@ @@@ @@     
#       @@@              @@@       @@@     @@@   @@@   @@@   @@          @@@     @@    @@@  @@  @@@      @@@@   @@@   @@  @@@@  @@@   @@    @@  @@@  @@@  @@@@  @@       
#        @@@@@@@@         @@@@@@@@  @@@@@@@@@  @@@@@@@@@@@@  @@@@@@@@@   @@@@@@@@@   @@@    @@   @@@@    @@@    @@@   @@   @@   @@@   @@@@@@@@  @@@  @@@  @@@   @@   
#                                              @@        @@              @@                        
#                                              @@        @@              @@                          
#                                              @@        @@              @@                          
                                                                                                    
                                                                                                             

#                                                                                       ЛОГИКА ПЕРЕМЕЩЕНИЯ ПО ЭКРАНАМ!

#   1. Нас помещает в gamescreen, который использует экраны: 
#                   room: 
#                        - режим камеры. 0 - фиксированная. 1 - следует за игроком
#                        - solid логическими объектами с AABB коллизией
#                        - обычными логическими объектами которые ставят INTERACT равный своему hp в классе, то бишь при создании объекта для карты мне нужно будет указать хп.
#                        - таймеры, приписанные к хп и которые отправляют в нужный лейбл при нужном значении
#                   timers:
#                        - обновление функции отслеживания коллизий, нажатия кнопок движения, движения последователей
#                        - добавление последователей через условие picked. Имена последователей : имена их папок со спрайтами присваиваются через список char_defs. Названия спрайтов см. "аналогичные спрайты". Там idle и moving анимации
#                        - кнопки упраления игроком
#                        - сам игрок - физики и спрайты
#                   dynamic_entities:
#                        - игрок, последователи и декорации, отсортированные по точке на земле.
#   2. После приведения Interact в значение hp нужного объекта, нас бросает в лейбл, где может происходить всё, что угодно
#   3. Если перекидывает в другую комнату, то будет лейбл, связывающий два перехода и указывающий YVAR и XvAR для Криса







default tab = 1  #0 - ничего,    1 - открывает save_and_open_artifacts 2 - вернуться в игру через Return_to_game_screen, сделать tab= 1




                                                                                                                        
                                                                    




screen bulletsrpg:
    #if getattr(store, "current_bullet_zone", None) is not None:
    $ bullets = store.active_room_objects.get("bullets", [])
    if getattr(store, "current_bullet_zone", None) is not None or len(bullets) > 0:
        add DynamicDisplayable(bullets_dd)


#default room = "Stadium"
#default room = None

default charicontimetodis = 0

screen pre_escape:
    key "K_ESCAPE" action Show("escape")




label check_point_for_save_and_open_artifacts:
    hide screen game_screen
    show screen artifacts_menu
    #call nolabel


#label check_point_for_save_and_open_artifacts2:
#    hide screen game_screen
#    show screen check_point
    #call nolabel


screen inventory_obertka:
    timer 0.00015 action Hide("inventory_obertka")
    timer 0.0001 action Call("open_inveintory")

screen inventory_obertka_close:
    timer 0.00015 action Hide("inventory_obertka_close")
    timer 0.0001 action Call("close_inveintory")


default Zaicev = 0
label open_inventory:
    $ store.sync_equipped_artifacts
    $store.Zaicev += 1
    hide screen game_screen
    call screen artifacts_menu


label close_inventory:
    hide screen artifacts_menu
    $ store.sync_equipped_artifacts
    $store.Zaicev += 1
    hide screen artifacts_menu
    call screen game_screen


init python:
    def equip_character_to_team(char_name, replace_slot_index=None):
        """Добавляет персонажа в свободный слот или заменяет в выбранном слоте."""
        store.ensure_team_manager()

        if char_name == "Крис":
            renpy.notify("Крис всегда в команде.")
            return

        if char_name not in store.characters:
            renpy.notify(f"Персонаж {char_name} недоступен.")
            return

        team_manager = store.team_manager

        if char_name in team_manager.team_slots:
            renpy.notify(f"{char_name} уже в команде.")
            return

        free_slot = None
        for i in range(1, team_manager.MAX_TEAM_SIZE):
            if team_manager.team_slots[i] is None:
                free_slot = i
                break

        if free_slot is not None:
            team_manager.team_slots[free_slot] = char_name
            team_manager.reorder_team_slots_by_current_attacker()
            team_manager.sync_picked_from_team()
            if hasattr(store, 'update_followers_from_picked'):
                store.update_followers_from_picked()
            renpy.notify(f"{char_name} добавлен(а) в команду.")
            return

        if replace_slot_index not in (1, 2, 3):
            renpy.notify("Команда заполнена. Сначала выберите слот 2-4 для замены.")
            return

        replaced_char = team_manager.team_slots[replace_slot_index]
        if replaced_char == "Крис":
            renpy.notify("Криса заменять нельзя.")
            return

        team_manager.team_slots[replace_slot_index] = char_name
        team_manager.reorder_team_slots_by_current_attacker()
        team_manager.sync_picked_from_team()
        if hasattr(store, 'update_followers_from_picked'):
            store.update_followers_from_picked()
        renpy.notify(f"{replaced_char} заменён(а) на {char_name}.")
        return


label open_forming_team:
    $ store.ensure_team_manager()
    hide screen game_screen
    call screen forming_team


label close_forming_team:
    hide screen forming_team
    $ forming_team_selected_slot = None
    call screen game_screen


screen forming_team():
    modal True
    key "K_q" action Call("close_forming_team")
    key "K_ESCAPE" action Call("close_forming_team")

    $ store.ensure_team_manager()
    $ team_slots = store.team_manager.team_slots
    $ is_team_full = all(team_slots[i] is not None for i in range(1, 4))
    $ available_chars = [name for name in store.characters if name != "Крис"]

    add "#000000AA"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1100
        ysize 620

        vbox:
            spacing 18
            xalign 0.5
            yalign 0.5

            text "forming_team — менеджер команды" size 42 xalign 0.5
            text "Q / Esc — закрыть" size 24 xalign 0.5

            hbox:
                spacing 80
                xalign 0.5

                vbox:
                    spacing 10
                    text "Персонажи" size 30
                    for char_name in available_chars:
                        textbutton char_name:
                            xminimum 300
                            action [
                                Function(store.equip_character_to_team, char_name, forming_team_selected_slot),
                                SetVariable("forming_team_selected_slot", None)
                            ]

                vbox:
                    spacing 10
                    text "Слоты team_manager" size 30
                    text "Слот 1: Крис (не заменяется)" size 24

                    for i in range(1, 4):
                        $ slot_name = team_slots[i] if team_slots[i] else "Пусто"
                        textbutton "Слот [i+1]: [slot_name]":
                            xminimum 450
                            action SetVariable("forming_team_selected_slot", i)
                            sensitive is_team_full

                    if is_team_full:
                        if forming_team_selected_slot in (1, 2, 3):
                            text "Выбран слот [forming_team_selected_slot+1] для замены." size 22 color "#66ff66"
                        else:
                            text "Команда заполнена: выберите слот 2-4, затем нажмите персонажа." size 22 color "#ffff66"
                    else:
                        text "Есть свободные слоты: персонажи добавляются автоматически." size 22 color "#66ff66"
    
















default game_type = "rpg" #или dialogue

screen to_escape:
    if store.game_type == "dialogue":
        timer 0.01 action ShowMenu()
    else:
        timer 0.01 action Jump("to_escape_label")


label open_wash_screen_from_game_menu:
    hide screen game_menu
    call screen wash_screen
    

label close_wash_screen_to_game_menu:
    hide screen wash_screen
    call screen game_screen()
    

label open_trader_screen_from_game_menu:
    hide screen game_menu
    call screen trader_screen
    

label close_trader_screen_to_game_menu:
    hide screen trader_screen
    hide screen trader_screen_options
    call screen game_screen()
    

label to_escape_label:
    $ set_spawn(store.player_x, store.player_y, dir="down", reset_followers=False)
    hide screen game_screen
    show screen game_screen
    hide screen game_screen
    $ ShowMenu()



















#init python:
#    z_pressed = 0
#    def set_z_pressed_true():
#        z_pressed = 1
#    
#    def set_z_pressed_false():
#        z_pressed = 0

default z_pressed = 0
default is_saving = 0

screen z_pressed_1:
    timer 0.001 action SetVariable("z_pressed", 1)
    timer 0.5 action [SetVariable("z_pressed", 0), Hide("z_pressed_1")]


screen keytest_escape():
    zorder 999999999
    #key "K_ESCAPE" action [Notify("ESC пойман оверлеем"), ShowMenu("preferences")]

init python:
    #config.overlay_screens.append("keytest_escape")
    config.keymap['save_screen'] = ['K_F1', 'K_RETURN']    

#                                                                           Экран с логикой и отрисовкой
screen game_screen():
    use keytest_escape()
    key "K_ESCAPE" action ShowMenu("save_screen")

    # Фоновая логика стирки (пока идёт стирка) во время геймплея
    timer 0.1 repeat True action Function(store.wash_background_update)

    if store.is_saving == 1:
        timer 0.001 action [SetVariable("is_saving", 0), ShowMenu()]

    $ feedness_delay = getattr(store, "feedness_tick_delay", 0) or schedule_next_feedness_tick()
    if feedness_delay:
        timer feedness_delay action Function(start_feedness_tick_cycle)

    if getattr(store, "feedness_tick_active", False):
        timer 0.2 action Function(process_next_feedness_tick_target) repeat True

    timer 0.1 action SetVariable("xpos_transit", player_x) repeat True

    #key "K_ESCAPE" action [Notify("ESC пойман оверлеем"), ShowMenu("preferences")]
    timer 0.1 action ShowMenu()
    #Show("escape")
    
    #key "K_ESCAPE" action ShowMenu("preferences")
    key "K_TAB" action [Function(save_and_open_artifacts2), Call("open_inventory")]
    key "K_q" action [Function(save_and_open_artifacts2), Call("open_forming_team")]
    key "K_w" action [Function(stop_movement), Function(save_and_open_artifacts2), SetVariable("control_Kris", 0), SetVariable("phone_panel", "home"), Show("complex_phone")]
    
    #key "K_ESCAPE" action MainMenu()
    #key "K_p" action ShowMenu()
    #key "K_ESCAPE" action ShowMenu()
    #key "K_ESCAPE" action Show("to_escape")
    


    #Function(save_and_open_artifacts2)]



        #If(
        #    tab == 2,
        #    [Call("Return_to_game_screen2"), SetVariable("tab", 1)],
        #    NullAction()
    #    )
    #)

    #В будущем для мобилок:

        #textbutton "AAAa" xpos 500 ypos 500 action Show ("artifacts_menu")  
        #textbutton "Открыть инвентарь" xpos 500 ypos 550 action Function(store.save_and_open_artifacts)
        #textbutton "Открыть инвентарь2" xpos 500 ypos 600 action Function(store.save_and_open_artifacts2)

    timer 0.1 action SetVariable("quick_menu", False)
    $ offset_x, offset_y = get_camera_offset()

    use room
    use timers
    use dynamic_entities
    use bulletsrpg
    













#                                                                                   Универсальный лейбл

label nolabel:
    #window hide
    #"{alpha=0}1{/alpha}"
    window hide
    $ renpy.pause(9999, hard=True)
    jump nolabel
    #return

transform rpgbullet1:
    #on show:
        xpos 300 
        ypos 600
        linear 5 xpos 925 ypos 1225



screen rpgdamaged:
    

    timer 0.01 action [Function(store.team_manager.apply_damage_to_team), Function(remove_green_bullet)]
    timer 2.0 action Function(add_green_bullet)
    #timer 0.01 action SetVariable("rect_collision_works", 0)
    timer 0.01 action SetVariable ("charicontimetodis", 0)
    timer 0.01 action Show ("team_status_display")
    #timer 1.501 action Hide("team_status_display")
    timer 1.5 action SetVariable ("charicontimetodis", 1)
    #timer 1.503 action Show("team_status_display")
    #timer 2.001 action SetVariable("rect_collision_works", 1)
    timer 2.0012 action Hide ("rpgdamaged")
    text "{font=determination.otf}{size=40}[raw_damage_for_vis]" at rpgdamaged style "damage_text"
    
transform rpgdamaged:
    alpha 0.0 xpos 500 ypos 400
    easein 0.5 xpos 585 alpha 1.0
    pause 0.5
    easeout 0.5 xpos 700 alpha 0.0

screen interact_check:
    zorder 999999
    text "{font=determination.otf}{size=40}[interact]"



screen suka:
    zorder 999999
    imagebutton:
        xpos 0 ypos 0
        at alpha_000
        idle "blackbg3.png"
        hover "blackbg3.png"
        action NullAction()



























#                                                                                    Экран со списком комнат   
screen room:


    if len(green_bullet_collisions) > 0 and getattr(store, 'current_bullet_zone', None) is not None:
    # Наносим урон всем персонажам в команде
        
        timer 0.0016 action Show("rpgdamaged")
        


    $ safe_dir = current_dir if current_dir in ("up","down","left","right") else "down"
    $ sprite_name = ("player_walk_" if is_moving else "player_idle_") + safe_dir
    #timer 0.000001 action Show("suka")


    use interact_check

    # Автоматическая загрузка объектов при показе
    on "show" action Function(load_room_objects, room)
    
    # Автоматическая очистка при скрытии
    on "hide" action Function(clear_room_objects)


    # 1) часто проверяем — в какой зоне игрок (дёшево, можно хоть 0.05)
    if hasattr(store, 'sync_bullet_zone'):
        timer 0.05 repeat True action Function(sync_bullet_zone)

    # 2) если зона активна — двигаем пули
    if getattr(store, "current_bullet_zone", None) is not None and hasattr(store, "update_bullet"):
        timer 0.016 repeat True action Function(update_bullet)





    if room == "proba":
        add "fon2.png" xpos 0 + offset_x ypos 0 + offset_y xanchor 0 yanchor 0
        timer 0.1 action SetVariable("camera_mode", 1)





    if room == "Stadium":
        add "fon2.png" xpos 0 + offset_x ypos 0 + offset_y xanchor 0 yanchor 0
        timer 0.1 action SetVariable("camera_mode", 1)


        # Добавлять вс
        if store.z_pressed == 1 and interact == "дерево":
            textbutton "ВСПЛЫЛА КНОПКА ВЗАИМОДЕЙСТВИЯ!!!!" at text1 action SetVariable("interact", "стиралка")
        
        # shopsans - открывает экран shop_screen через таймер
        if store.z_pressed == 1 and interact == "магазин":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action Show("shop_screen")
        
        # washingmachine - открывает экран wash_screen через таймер
        if store.z_pressed == 1 and interact == "стиралка":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action Jump("open_wash_screen_from_game_menu")
        
        # check_table - открывает экран identify_screen через таймер
        if store.z_pressed == 1 and interact == "опознание":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action Show("identify_screen")
        
        # dialog_pick_7 - устанавливает dialogue_id = 7 через таймер
        if store.z_pressed == 1 and interact == "для_диалога_1":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action [SetVariable("dialogue_id", 7), Call("rpg_dialogues")]
        
        # dialog_pick_8 - устанавливает dialogue_id = 8 через таймер
        if store.z_pressed == 1 and interact == "для_диалога_2":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action [SetVariable("dialogue_id", 8), Jump("rpg_dialogues")]
        
        # dialog_pick_9 - устанавливает dialogue_id = 9 через таймер
        if store.z_pressed == 1 and interact == "для_диалога_3":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action [SetVariable("dialogue_id", 9), Jump("rpg_dialogues")]
        
        # trader - открывает экран торговца через таймер
        if store.z_pressed == 1 and interact == "торговец":
            timer 0.001 action Function(stop_movement)
            timer 0.01 action Jump("open_trader_screen_from_game_menu")
        
        if store.z_pressed == 1 and interact == "переход":
            timer 0.01 action [SetVariable("fortransition", "sport_1floor_right"), SetVariable("xpos_transit", 2020), SetVariable("ypos_transit", 1450), SetVariable("dir_transit","up"), Jump("transitions")]  #Screen("Transitionscreen")

        if store.z_pressed == 1 and len(green_bullet_collisions) > 0 and getattr(store, 'current_bullet_zone', None) is not None:
            # Наносим урон всем персонажам в командe
            
            timer 0.0016 action Show("rpgdamaged")










        if store.z_pressed == 1 and interact == "dummy_fight" and store.enemies["dummy"].spared == 0 and store.enemies["dummy"].current_hp > 0:
            timer 0.00001 action [Hide("game_screen")]
            timer 0.00005 action [SetVariable("battlenumber", 11), MouseMove(640, 360, duration=0.3), Jump("fightbegin12")]

           
        if store.z_pressed == 1 and interact == "dummy2_fight":
            timer 0.00001 action [Hide("game_screen")]
            timer 0.00005 action [SetVariable("battlenumber", 13), MouseMove(640, 360, duration=0.3), Jump("fightbegin12")]


        
































    elif room == "sport_1floor_right":

        timer 0.1 action SetVariable("camera_mode", 1)
        

        

        #Добавлять объекты и изображения от первого до последнего
        #add "classs" xpos 0 + offset_x ypos 0 + offset_y xanchor 0 yanchor 0
        add "sportkorridor1right.png" xpos 0 + offset_x ypos 0 + offset_y


        # Добавлять вс
        if store.z_pressed == 1 and interact == "дерево":
            textbutton "ВСПЛЫЛА КНОПКА ВЗАИМОДЕЙСТВИЯ!!!!" at text1 action SetVariable("interact", "стиралка")


        if store.z_pressed == 1 and interact == "переход":
            timer 0.01 action [SetVariable("fortransition", "Stadium"), SetVariable("xpos_transit", 2290), SetVariable("ypos_transit", 480), SetVariable("dir_transit","down"), Jump("transitions")]  #Screen("Transitionscreen")

        if store.z_pressed == 1 and interact == "dummy_fight":
            timer 0.00001 action [Hide("game_screen")]
            timer 0.00005 action [SetVariable("battlenumber", 11), MouseMove(640, 360, duration=0.3), Jump("fightbegin12")]

           
        if store.z_pressed == 1 and interact == "dummy2_fight":
            timer 0.00001 action [Hide("game_screen")]
            timer 0.00005 action [SetVariable("battlenumber", 13), MouseMove(640, 360, duration=0.3), Jump("fightbegin12")]





    # ФИЗИЧЕСКОЕ ТЕЛО ФИЗИЧЕСКАЯ ОБОЛОЧКА ЦВЕТ ФИЗИЧЕСКИХ ОБЪЕКТОВ

    # --- bullet zones ---
    #for z in store.bullet_zone_defs.get(room, []):
    #    add Solid("#003b00cc", xysize=(z["x1"] - z["x0"], z["y1"] - z["y0"])) xpos z["x0"] + offset_x ypos z["y0"] + offset_y #xanchor 0 yanchor 0

    # --- твёрдые объекты ---
    #for obj in active_room_objects["solid"]:
    #    add Solid("#0000ff", xysize=(obj.w, obj.h)) xpos obj.x + offset_x ypos obj.y + offset_y #xanchor 0.5 yanchor 0.5

    # --- противники ---
    #for obj in active_room_objects["enemies"]:
    #    add Solid("#ffff00", xysize=(obj.w, obj.h)) xpos obj.x + offset_x ypos obj.y + offset_y #xanchor 0.5 yanchor 0.5

    # --- pickup ---
    #for obj in active_room_objects["pickups"]:
    #    add Solid("#00ff00", xysize=(obj.w, obj.h)) xpos obj.x + offset_x ypos obj.y + offset_y xanchor 0 yanchor 0
    
    # --- пули отображаются через DynamicDisplayable(bullets_dd) в экране bulletsrpg ---
    # чтобы избежать дублирования, здесь пули не отображаем
    # for obj in active_room_objects["bullets"]:
    #     add obj.image xpos obj.x + offset_x ypos obj.y + offset_y xanchor 0 yanchor 0
    
    


init python:
    def get_sorted_render_queue():
        """Собирает сущности в мировых координатах и сортирует от задних к передним."""
        queue = []

        if store.room == "Stadium":
            queue.append({
                "type": "image",
                "image": "wood2.png",
                "x": -550,
                "y": -700,
                "anchor": (0.0, 0.0),
                # Декорация переднего плана: всегда перекрывает персонажей.
                "sort_y": float("inf"),
            })
            queue.append({
                "type": "image",
                "image": "player_idle_down",
                "x": 300,
                "y": 300,
                "anchor": (0.0, 0.0),
                "sort_y": 300 + 141,  # Низ down0.png (69x141).
            })
        elif store.room == "proba":
            queue.append({
                "type": "image",
                "image": "fon3.png",
                "x": 0,
                "y": 0,
                "anchor": (0.0, 0.0),
                # Передний слой карты: рисуется после остальных декораций.
                "sort_y": float("inf"),
                "sort_priority": 100,
            })
            queue.append({
                "type": "solid",
                "color": "#1769e8",
                # Центр тестовой комнаты: дверь находится на пути игрока.
                "x": 480,
                "y": 260,
                "w": 80,
                "h": 180,
                "anchor": (0.0, 0.0),
                # Нижняя граница двери — её точка соприкосновения с землёй.
                "sort_y": 260 + 180,
            })

        # Визуальные объекты из редактора с автоматической Y-сортировкой.
        # Их x/y — левый верхний угол, а sort_y — основание объекта.
        room_data = getattr(store, "room_object_definitions", {}).get(store.room, {})
        for obj in room_data.get("depth_solids", []):
            obj_x = obj.get("x", 0)
            obj_y = obj.get("y", 0)
            obj_w = obj.get("w", 1)
            obj_h = obj.get("h", 1)
            queue.append({
                "type": "solid",
                "color": obj.get("color", "#1769e8"),
                "x": obj_x,
                "y": obj_y,
                "w": obj_w,
                "h": obj_h,
                "anchor": (0.0, 0.0),
                "sort_y": obj.get("sort_y", obj_y + obj_h),
            })

        # Декорации переднего плана всегда рисуются после персонажей.
        # Их положение не участвует в Y-сортировке.
        for obj in room_data.get("front_decors", []):
            image_name = obj.get("image")
            if not image_name:
                continue
            queue.append({
                "type": "image",
                "image": image_name,
                "x": obj.get("x", 0),
                "y": obj.get("y", 0),
                "xsize": obj.get("w"),
                "ysize": obj.get("h"),
                "anchor": (0.0, 0.0),
                "sort_y": float("inf"),
            })

        flw = getattr(store, "followers", None) or []
        # При одинаковой глубине сохраняем прежний порядок спутников.
        for f in reversed(flw):
            if f is None or getattr(f, "kind", None) is None:
                continue
            if getattr(f, "x", None) is None or getattr(f, "y", None) is None:
                continue

            state = "walk" if getattr(f, "is_moving", False) else "idle"
            prefix = getattr(f, "prefix", None)
            direction = getattr(f, "dir", "down")
            if not prefix:
                continue
            follower_w = getattr(f, "w", 0) or 0
            follower_h = getattr(f, "h", 0) or 0
            queue.append({
                "type": "follower",
                "image": "{}_{}_{}".format(prefix, state, direction),
                "x": f.x,
                "y": f.y,
                "anchor": (0.5, 0.5),
                "hitbox": (f.x + getattr(store, "character_hitbox_offset_x", 0),
                           f.y + getattr(store, "character_hitbox_offset_y", 0),
                           follower_w, follower_h),
                # Точка сортировки относительно центра персонажа.
                "sort_y": f.y + (follower_h // 2),
            })

        player_x = getattr(store, "player_x", 0)
        player_y = getattr(store, "player_y", 0)
        player_w = getattr(store, "player_w", 0) or 0
        player_h = getattr(store, "player_h", 0) or 0
        player_sprite = ("player_walk_" if getattr(store, "is_moving", False) else "player_idle_") + getattr(store, "current_dir", "down")
        queue.append({
            "type": "player",
            "image": player_sprite,
            "x": player_x,
            "y": player_y,
            "anchor": (0.5, 0.5),
            "hitbox": (player_x + getattr(store, "character_hitbox_offset_x", 0),
                       player_y + getattr(store, "character_hitbox_offset_y", 0),
                       player_w, player_h),
            "interact": getattr(store, "interact", 0) != 0,
            "sort_y": player_y + (player_h // 2),
        })

        # Сначала учитываем глубину, затем явный приоритет слоя.
        # fon3.png имеет максимальный приоритет и оказывается самым верхним.
        queue.sort(key=lambda item: (item["sort_y"], item.get("sort_priority", 0)))
        return queue

#                                                                                       Списки лейблов






#transform Transitionscreen_transform:
#    on show:
#        alpha 0.0
#        easein 0.5 alpha 1.0
#    on hide:
#        alpha 1.0
#        easein 0.5 alpha 0.0


#screen Transitionscreen:
#    at Transitionscreen_transform
#    timer 0.55 action Setvariable("room", fortransition)
