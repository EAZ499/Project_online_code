    
#                     @@@@        @@@        @@@@         @@@@@@@@@@@                                
#                      @@@@      @@@        @@@@@@        @@@                                        
#                       @@@@   @@@@        @@@ @@@        @@@                                        
#                         @@@ @@@@         @@@  @@@       @@@                                        
#                          @@@@@@         @@@   @@@@      @@@@@@@@@                                  
#                          @@@@@         @@@     @@@      @@@@@@@@@@@@                               
#                         @@@@@@@        @@@@@@@@@@@@     @@@      @@@@                              
#                        @@@   @@@      @@@@@@@@@@@@@@    @@@       @@@                              
#                       @@@     @@@    @@@@        @@@    @@@       @@@                              
#                      @@@       @@@   @@@          @@@   @@@@@@@@@@@@                               
#                     @@@         @@@ @@@           @@@@  @@@@@@@@@@                                 
                                                                        



init python:
    import os
    
    # Включаем логирование в файл
    config.log = os.path.join(config.savedir, "game_log.txt")


# Вы можете расположить сценарий своей игры в этом файле.

# Определение персонажей игры.
define e = Character('Эйлин', color="#c8ffc8")

default project = "rpg"
#default project = "choose"
#default project = "inventory"
#default project = "мышь"
#default project = "fight"

# Вместо использования оператора image можете просто
# складывать все ваши файлы изображений в папку images.
# Например, сцену bg room можно вызвать файлом "bg room.png",
# а eileen happy — "eileen happy.webp", и тогда они появятся в игре.
# Игра начинается здесь:


## Перед боем установите battlenumber
#$ battlenumber = "Арчи"

## После атаки игрока по врагу
#$ last_attacked_enemy = target_enemy
#$ last_enemy_damage_dealt = damage

## Показать экран
#call screen enemies_attacked_visual()

#init python:
#    config.underlay.append(
#      renpy.Keymap(
#            K_ESCAPE=save_and_open_artifacts2
#        )
#    )


label add_all:
    $ add_item("art1", 1)
    $ add_item("art2", 1)
    $ add_item("art3", 1)
    $ add_item("art4", 1)
    $ add_item("art5", 1)
    $ add_item("art6", 1)
    $ add_item("art7", 1)
    $ add_item("art8", 1)
    $ add_item("art9", 1)
    $ add_item("art10", 1)
    $ add_item("art11", 1)
    $ add_item("art12", 1)
    $ add_item("art13", 1)
    $ add_item("art14", 1)
    $ add_item("art15", 1)
    $ add_item("art16", 1)
    $ add_item("art17", 1)
    $ add_item("art18", 1)
    $ add_item("art19", 1)
    $ add_item("art20", 1)
    $ add_item("art21", 1)
    $ add_item("art22", 1)
    $ add_item("art23", 1)
    $ add_item("art24", 1)
    $ add_item("art25", 1)
    $ add_item("art26", 1)
    $ add_item("art27", 1)
    $ add_item("art28", 1)
    $ add_item("art29", 1)
    $ add_item("art30", 1)
    $ add_item("art31", 1)
    $ add_item("art32", 1)
    $ add_item("art33", 1)
    $ add_item("art34", 1)
    $ add_item("art35", 1)
    $ add_item("art36", 1)
    $ add_item("art37", 1)

    # даём все зелья в инвентарь
    #$ add_consumable("pot1", 1)
    #$ add_consumable("pot2", 1)
    #$ add_consumable("pot3", 1)
    #$ add_consumable("pot_atk_3", 1)
    #$ add_consumable("pot_atk_5", 1)
    #$ add_consumable("pot_def_3", 1)
    #$ add_consumable("pot_def_5", 1)
    #$ add_consumable("pot_crit_3", 1)
    #$ add_consumable("pot_crit_5", 1)
    #$ add_consumable("pot_acc_3", 1)
    #$ add_consumable("pot_acc_5", 1)
    #$ add_consumable("pot_all_3", 1)
    #$ add_consumable("pot_all_5", 1)

    # даём всю еду в инвентарь
    $ add_consumable("food_clubsandwich", 1)
    $ add_consumable("food_sans_sandwich", 1)
    $ add_consumable("food_banana", 1)
    $ add_consumable("food_lucky_monstercandy", 1)
    $ add_consumable("food_icecream", 1)
    $ add_consumable("food_readymeal_1", 1)
    $ add_consumable("food_readymeal_2", 1)
    $ add_consumable("food_readymeal_3", 1)
    $ add_consumable("food_cookiesharing", 1)
    $ add_consumable("food_pepperoni", 1)
    $ add_consumable("food_mint_gum", 1)
    $ add_consumable("food_lottery_candy", 1)
    $ add_consumable("food_colacoffee", 1)
    $ add_consumable("food_tonic", 1)
    $ add_consumable("food_crab_apple", 1)
    $ add_consumable("food_diet_salad", 1)
    $ add_consumable("food_broccoli", 1)
    $ add_consumable("food_noodles", 1)
    $ add_consumable("food_sparkling_water", 1)
    $ add_consumable("food_still_water", 1)
    $ add_consumable("food_frenchfries", 1)


    # даём всё одноразовое оружие в инвентарь
    $ add_consumable("wep_water_pistol", 3)
    $ add_consumable("wep_water_bomb", 3)
    $ add_consumable("wep_toothpick", 3)
    $ add_consumable("wep_rubber_band", 3)
    $ add_consumable("wep_paper_shooter", 3)
    $ add_consumable("wep_ruler", 3)
    $ add_consumable("wep_soap_bubbles", 3)
    $ add_consumable("wep_poetry_leaf", 3)
    $ add_consumable("wep_bath_bombs", 3)
    $ add_consumable("wep_constructor", 3)
    $ add_consumable("wep_flashlight", 3)

label start2:

    $ add_item("art1", 1)
    $ add_item("art2", 1)
    $ add_item("art3", 1)
    $ add_item("art4", 1)
    $ add_item("art5", 1)
    $ add_item("art6", 1)
    $ add_item("art7", 1)
    $ add_item("art8", 1)
    $ add_item("art9", 1)
    $ add_item("art10", 1)
    $ add_item("art11", 1)
    $ add_item("art12", 1)
    $ add_item("art13", 1)
    $ add_item("art14", 1)
    $ add_item("art15", 1)
    $ add_item("art16", 1)
    $ add_item("art17", 1)
    $ add_item("art18", 1)
    $ add_item("art19", 1)
    $ add_item("art20", 1)
    $ add_item("art21", 1)
    $ add_item("art22", 1)
    $ add_item("art23", 1)
    $ add_item("art24", 1)
    $ add_item("art25", 1)
    $ add_item("art26", 1)
    $ add_item("art27", 1)
    $ add_item("art28", 1)
    $ add_item("art29", 1)
    $ add_item("art30", 1)
    $ add_item("art31", 1)
    $ add_item("art32", 1)
    $ add_item("art33", 1)
    $ add_item("art34", 1)
    $ add_item("art35", 1)
    $ add_item("art36", 1)
    $ add_item("art37", 1)

    # даём все зелья в инвентарь
    #$ add_consumable("pot1", 1)
    #$ add_consumable("pot2", 1)
    #$ add_consumable("pot3", 1)
    #$ add_consumable("pot_atk_3", 1)
    #$ add_consumable("pot_atk_5", 1)
    #$ add_consumable("pot_def_3", 1)
    #$ add_consumable("pot_def_5", 1)
    #$ add_consumable("pot_crit_3", 1)
    #$ add_consumable("pot_crit_5", 1)
    #$ add_consumable("pot_acc_3", 1)
    #$ add_consumable("pot_acc_5", 1)
    #$ add_consumable("pot_all_3", 1)
    #$ add_consumable("pot_all_5", 1)

    # даём всю еду в инвентарь
    $ add_consumable("food_clubsandwich", 1)
    $ add_consumable("food_sans_sandwich", 1)
    $ add_consumable("food_banana", 1)
    $ add_consumable("food_lucky_monstercandy", 1)
    $ add_consumable("food_icecream", 1)
    $ add_consumable("food_readymeal_1", 1)
    $ add_consumable("food_readymeal_2", 1)
    $ add_consumable("food_readymeal_3", 1)
    $ add_consumable("food_cookiesharing", 1)
    $ add_consumable("food_pepperoni", 1)
    $ add_consumable("food_mint_gum", 1)
    $ add_consumable("food_lottery_candy", 1)
    $ add_consumable("food_colacoffee", 1)
    $ add_consumable("food_tonic", 1)
    $ add_consumable("food_crab_apple", 1)
    $ add_consumable("food_diet_salad", 1)
    $ add_consumable("food_broccoli", 1)
    $ add_consumable("food_noodles", 1)
    $ add_consumable("food_sparkling_water", 1)
    $ add_consumable("food_still_water", 1)
    $ add_consumable("food_frenchfries", 1)


    # даём всё одноразовое оружие в инвентарь
    $ add_consumable("wep_water_pistol", 3)
    $ add_consumable("wep_water_bomb", 3)
    $ add_consumable("wep_toothpick", 3)
    $ add_consumable("wep_rubber_band", 3)
    $ add_consumable("wep_paper_shooter", 3)
    $ add_consumable("wep_ruler", 3)
    $ add_consumable("wep_soap_bubbles", 3)
    $ add_consumable("wep_poetry_leaf", 3)
    $ add_consumable("wep_bath_bombs", 3)
    $ add_consumable("wep_constructor", 3)
    $ add_consumable("wep_flashlight", 3)


    $ quick_menu = True


    stop music # музыка заебёт

    #show screen pre_escape #для выхода из игры 

    $ followers = followers or []
    # Создаем новое состояние игры (персонажи, враги, менеджеры)
    $ reset_game_state()
    #$ grant_story_party_bonus_stats()







    #store.enemies["dummy"].armor

    $ store.enemies["dummy"].bloodshed_debuff = 4
    $ store.enemies["dummy"].prone_debuff = 1
    $ store.enemies["dummy"].atk_debuff = -4
    $ store.enemies["dummy"].def_debuff = -60
    $ store.enemies["dummy"].critdmg_debuff = -4
    $ store.enemies["dummy"].shield = 2
    $ store.enemies["dummy"].bonus_atk2 += 0.2
    $ store.enemies["dummy"].bonus_magic2 += 0.2
    $ store.enemies["dummy"].bonus_def2 -= 0.2
    $ store.enemies["dummy"].bonus_crit2 += 0.2
    $ store.enemies["dummy"].bonus_critrate2 += 0.2
    
    $ store.enemies["dummy"].bonus_dmgchance2 += 0.2
    $ store.enemies["dummy"].bonus_perform2 += 0.2
    $ store.enemies["dummy"].bonus_tank2 += 0.2




    $ store.enemies["dummy"].ask_checked = 1
    $ store.enemies["dummy"].persuade_checked = 1
    $ store.enemies["dummy"].tell_checked = 1
    $ store.enemies["dummy"].support_checked = 1
    $ store.enemies["dummy"].play_checked = 1
    $ store.enemies["dummy"].perform_checked = 1
    $ store.enemies["dummy"].humiliate_checked = 1
    $ store.enemies["dummy"].tease_checked = 1
    $ store.enemies["dummy"].scare_checked = 1


    #$ store.enemies["dummy"].speed = 2


    # store.enemies.get["Джевил"].bonus_def2 += 0.2













    # Устанавливаем глобальный уровень персонажей
    $ Pers.global_level = 9

    # Перезарядки способностей выставляются по initial_cooldown на старте боя
    # (reset_battle_ability_cooldowns в лейбле fightbegin12).
    # Чтобы протестировать способности в первом раунде, во время боя вызови
    # zero_battle_ability_cooldowns() — обнулит текущие перезарядки.
    # Посмотреть таблицу: report_battle_ability_cooldowns().

    # Устанавливаем текущие HP и MP равными максимальным для каждого персонажа
    $ store.pers_dict["Крис"].current_hp = 120
    $ store.pers_dict["Крис"].current_mp = 70   
    $ store.pers_dict["Крис"].shield = 4
    #store.pers_dict["Крис"].max_mp
    $ store.pers_dict["Азриель"].shield = 0
    $ store.pers_dict["Чара"].shield = 0  
    $ change_reltns(-100)
    
    
    
    
    #$ store.enemies["ДжевилV1"].shield = 4def clear_followers
    
    
    
    # store.enemies["ДжевилV1"].current_hp

    #$ store.enemies["ДжевилV1"].bloodshed_debuff =2


    
    #$ store.pers_dict["Крис"].bonus_dmgchance = 1

    # Устанавливаем дебафы для Криса
    #$ store.pers_dict["Крис"].bloodshed_debuff = 4
    #$ store.pers_dict["Чара"].bloodshed_debuff = 1
    #$ store.pers_dict["Фриск"].bloodshed_debuff = 3
    #$ store.pers_dict["Азриель"].bloodshed_debuff = 1
    





    #$ store.pers_dict["Крис"].prone_debuff = 1
    #$ store.pers_dict["Крис"].atk_debuff = -1
    #$ store.pers_dict["Крис"].def_debuff = 2
    #$ store.pers_dict["Крис"].magic_debuff = 2
    
    #$ store.pers_dict["Крис"].accuracy_debuff = -10
    
    #$ store.pers_dict["Крис"].critrate_debuff = 2
    #$ store.pers_dict["Крис"].critdmg_debuff = 2





    ## Устанавливаем бонусы для Азри и Криса
    ## Бонусы для Криса
    #$ store.pers_dict["Крис"].base_atk_mod = 5
    









    #$ store.pers_dict["Крис"].bonus_atk = 1.2
    







    $ store.pers_dict["Крис"].sprite_style = "down"




    #$ store.pers_dict["Крис"].bonus_atk_mod = 0.1
    #$ store.pers_dict["Крис"].bonus_crit = 0.3
    #$ store.pers_dict["Крис"].crit_mod = 0.2
    #$ store.pers_dict["Крис"].overkrit_bonus = 0.1
    #$ store.pers_dict["Крис"].bonus_critrate = 0.15
    #$ store.pers_dict["Крис"].critrate_mod = 0.1
    #$ store.pers_dict["Крис"].bonus_dmgchance = 0.2
    #$ store.pers_dict["Крис"].dmgchance_mod = 0.1
    #$ store.pers_dict["Крис"].base_magic_mod = 3
    #$ store.pers_dict["Крис"].bonus_magic = 1.1
    #$ store.pers_dict["Крис"].bonus_magic_mod = 0.05
    #$ store.pers_dict["Крис"].base_def_mod = 4
    #$ store.pers_dict["Крис"].bonus_def = 1.15
    #$ store.pers_dict["Крис"].bonus_def_mod = 0.08
    #$ store.pers_dict["Крис"].bonus_tank = 5
    #$ store.pers_dict["Крис"].bonus_tank_mod = 0.1
    #$ store.pers_dict["Крис"].bonus_perform = 0.2
    #$ store.pers_dict["Крис"].perform_mod = 0.1
    ## Специальные бонусы для Криса
    #$ store.summoned = 1
    #$ store.pers_dict["Крис"].dodge_projectiles = True
    #$ store.pers_dict["Крис"].next_attack_triple_damage = True
    
    ## Бонусы для Азри
    #$ store.pers_dict["Азриель"].base_atk_mod = 3
    #$ store.pers_dict["Азриель"].bonus_atk = 1.1
    #$ store.pers_dict["Азриель"].bonus_atk_mod = 0.05
    #$ store.pers_dict["Азриель"].bonus_crit = 0.2
    #$ store.pers_dict["Азриель"].crit_mod = 0.1
    #$ store.pers_dict["Азриель"].overkrit_bonus = 0.05
    #$ store.pers_dict["Азриель"].bonus_critrate = 0.1
    #$ store.pers_dict["Азриель"].critrate_mod = 0.05
    #$ store.pers_dict["Азриель"].bonus_dmgchance = 0.15
    #$ store.pers_dict["Азриель"].dmgchance_mod = 0.05
    #$ store.pers_dict["Азриель"].base_magic_mod = 8
    #$ store.pers_dict["Азриель"].bonus_magic = 1.3
    #$ store.pers_dict["Азриель"].bonus_magic_mod = 0.15
    #$ store.pers_dict["Азриель"].base_def_mod = 6
    #$ store.pers_dict["Азриель"].bonus_def = 1.2
    #$ store.pers_dict["Азриель"].bonus_def_mod = 0.1
    #$ store.pers_dict["Азриель"].bonus_tank = 3
    #$ store.pers_dict["Азриель"].bonus_tank_mod = 0.05
    #$ store.pers_dict["Азриель"].bonus_perform = 0.15
    #$ store.pers_dict["Азриель"].perform_mod = 0.08
    ## Специальные бонусы для Азри
    #$ store.pers_dict["Азриель"].damage_reflect = True
    #$ store.pers_dict["Азриель"].chaos_blades = True


    #$ store.pers_dict["Азриель"].critdmg_debuff = 2

    call debug_trevor_all_effects
    


    ## Бонусы для фриск

    $ store.pers_dict["Фриск"].bonus_atk = 1.2
    $ store.pers_dict["Фриск"].bonus_crit = 0.6
    $ store.pers_dict["Фриск"].bonus_critrate = 1

    #$ store.pers_dict["Фриск"].prone_debuff = 1
    $ store.pers_dict["Фриск"].bloodshed_debuff = 3
    $ store.pers_dict["Фриск"].critdmg_debuff = 5
    




    $ store.pers_dict["Крис"].current_hp = 50

    $ store.pers_dict["Азриель"].current_hp = 1200#store.pers_dict["Азриель"].max_hp
    $ store.pers_dict["Азриель"].current_mp = store.pers_dict["Азриель"].max_mp
    
    $ store.pers_dict["Чара"].current_hp = 97000#store.pers_dict["Чара"].max_hp#store.pers_dict["Чара"].max_hp
    $ store.pers_dict["Чара"].current_mp = store.pers_dict["Чара"].max_mp
    
    $ store.pers_dict["Фриск"].current_hp -= 43 #store.pers_dict["Фриск"].max_hp
    #$ store.pers_dict["Фриск"].max_hp = 2000
    $ store.pers_dict["Фриск"].current_mp = store.pers_dict["Фриск"].max_mp
    
    $ store.pers_dict["Иззи"].current_hp = store.pers_dict["Иззи"].max_hp
    $ store.pers_dict["Иззи"].current_mp = store.pers_dict["Иззи"].max_mp
    
    $ store.pers_dict["Кловер"].current_hp = store.pers_dict["Кловер"].max_hp
    $ store.pers_dict["Кловер"].current_mp = store.pers_dict["Кловер"].max_mp
    
    $ store.pers_dict["Седрик"].current_hp = store.pers_dict["Седрик"].max_hp
    $ store.pers_dict["Седрик"].current_mp = store.pers_dict["Седрик"].max_mp
    
    $ store.ensure_team_manager()
    # Добавляем персонажей в команду
    $ store.pers_dict["Азриель"].picked = 1
    $ store.pers_dict["Чара"].picked = 1
    $ store.pers_dict["Фриск"].picked = 1
    
    # Логирование для диагностики
    $ renpy.log(f"Азриель picked: {store.pers_dict['Азриель'].picked}")
    $ renpy.log(f"Чара picked: {store.pers_dict['Чара'].picked}")
    $ renpy.log(f"Фриск picked: {store.pers_dict['Фриск'].picked}")
    
    # Восстанавливаем команду из переменных picked
    $ store.team_manager.rebuild_team_from_picked()
    $ renpy.log(f"Команда после rebuild: {store.team_manager.team_slots}")
    
    # Дополнительно обновляем followers на основе picked
    if hasattr(store, 'update_followers_from_picked'):
        $store.update_followers_from_picked()
        $ renpy.log("Вызвана update_followers_from_picked() после установки picked")
        pause 2.0
    
    # Дополнительно синхронизируем turn переменные
    #$ store.pers_dict["Крис"].turn
    $ store.pers_dict["Азриель"].turn = 1
    $ store.pers_dict["Чара"].turn = 1
    $ store.pers_dict["Фриск"].turn = 1
    #$ battlenumber = 13

    # getattr(store.pers_dict["Крис"], "next_attack_damage_multiplier", 1.0)

    # Устанавливаем начального атакующего как объект
    $ char = store.pers_dict["Крис"]

    $ mx, my = renpy.get_mouse_pos()
    $ sx, sy = store.screenxpos, store.screenypos
    $ sync_restricted_boundaries()

    if project == "fight": 
        label fightstarts:
            # показать
            #"amgus"
            # убрать

            
            #label Underrunefight:
            "щас будет атака"
            #$ persistent.hp = 20
            # show screen mouse_restricted_area  # Показываем экран с ограниченной областью
            $ default_mouse = 'damaged'
            $ renpy.pause(0.7, hard=True)
            $ default_mouse = "default2"
            #$ renpy.pause(2, hard=True)
            #$ MouseMove(640, 360, duration=0.3)
            #$ renpy.pause(2, hard=True)
            #$ default_mouse = "Null"

            call screen fightbegin



    elif project == "rpg":
       


        # Бонус отношения торговцев
        $ merchant_relation_bonus += 5
        $ merchants_personal_relation["merchant2"] += 7






        show screen consume_trade_relation






        #label Underrunemove:
        # followers теперь инициализируется в 1_RPG_ДВИЖЕНИЕ.rpy после init python блока
        $ interact = INTERACT
        #scene class_enhanced

        # Добавляем всех последователей на основе picked
        if hasattr(store, 'update_followers_from_picked'):
            $ store.update_followers_from_picked()

        
        #show screen inventory

        #$ txt = 0
        # Устанавливаем спавн только при новой игре, не при загрузке

        $ set_spawn(500, 400, "down")


        #$store.battlenumber = 1 #11
        #jump fightbegin12


        $ room = "proba"
        call screen game_screen

        jump pisya















    elif project == "choose":
        show enemyanimation with dissolve
        call screen enemyanimation
        #call screen switchedcheck

    
    elif project == "мышь":
        jump enemyattacklabel

    elif project == "inventory":

        # Устанавливаем уровень 5 для всех персонажей
        python:
            for char_name in store.pers_dict:
                store.pers_dict[char_name].level = 10

            #call init_all_chars
        # даём артефакты в инвентарь (по 1 каждого типа)
        


        # открываем меню

        call screen artifacts_menu
    


    return


# Label для восстановления координат после загрузки игры
label after_load:
    # Устанавливаем флаг, что игра загружена из сохранения
    $ is_loaded_from_save = True
    # Восстанавливаем координаты игрока и последователей
    if hasattr(store, 'load_spawn_after_load'):
        $ load_spawn_after_load()
    return


#screen inventory:


label pisya:
    pause 10
    $store.player_x = player_x
    $store.player_y = player_y
    $store.save_and_open_artifacts
    show artifacts_menu
    hide artifacts_menu
    
    #show screen check_point
    #$ renpy.pause(9999, hard=True)
    #call nolabel
    return






label debug_trevor_all_effects:
    $ trevor = store.enemies.get("Тревор")
    
    # Positive debuffs (positive values) and negative (buffs)
    # For each debuff, set both the counter and the _got flag
    
    # Bloodshed (bleeding)
    $ trevor.bloodshed_debuff = 3
    $ trevor.bloodshed_debuff_got = 3
    
    # Prone (lying down)
    $ trevor.prone_debuff = 2
    $ trevor.prone_debuff_got = 2
    
    # Attack - истощение (positive = debuff/red icon)
    $ trevor.atk_debuff = 3
    $ trevor.atk_debuff_got = 3
    
    # Defense - печаль (positive = debuff/red icon)
    $ trevor.def_debuff = 3
    $ trevor.def_debuff_got = 3
    
    # Magic - помутнение (positive = debuff/red icon)
    $ trevor.magic_debuff = 3
    $ trevor.magic_debuff_got = 3
    
    # Accuracy - страх (positive = debuff/red icon)
    $ trevor.accuracy_debuff = 3
    $ trevor.accuracy_debuff_got = 3
    
    # Critrate - сглаз (positive = debuff/red icon)
    $ trevor.critrate_debuff = 3
    $ trevor.critrate_debuff_got = 3
    
    # Critdmg - безразличие (positive = debuff/red icon)
    $ trevor.critdmg_debuff = 3
    $ trevor.critdmg_debuff_got = 3
    
    # Tank - уязвимость (positive = red)
    $ trevor.tank_debuff = 3
    $ trevor.tank_debuff_got = 2
    $ trevor.spare_progress  = 10
    
    # Shield
    $ trevor.shield = 2
    
    # Damage for visualization
    $ trevor.damage_gain_for_vis = 25
    $ trevor.got_crit_for_visual = 0
    $ store.enemies["Тревор"].evaluate_success_count = 5
    
    return
