
# Можно по attackindex и по state

# КРИС


























# Ren'Py: условный спрайт Криса по файлу "Крис 1"
# ВАЖНО:
# 1) Пути ниже предполагают, что кадры лежат как Kris_idle_up_1.png, Kris_idle_up_2.png и т.д.
# 2) Если у тебя sprite_style хранится как "up", а не "up", замени "up" на "up" в условиях.
# 3) Если HP-переменная у тебя называется current_hp, а не current_hp, замени .current_hp на .current_hp.
# 4) Там, где в файле не было указано время между кадрами, я поставил 0.064 как базовое значение.

transform falsh:
    alpha 0.0



# ------------------------------------------------------------
# IDLE
# ------------------------------------------------------------

image Kris_idle_up_anim:
    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    pause 0.2
    repeat

image Kris_idle_down_anim:
    "Kris_idle_down_1.png"
    pause 0.064
    "Kris_idle_down_2.png"
    pause 0.064
    "Kris_idle_down_3.png"
    pause 0.064
    "Kris_idle_down_4.png"
    pause 0.064
    "Kris_idle_down_5.png"
    pause 0.064
    repeat

image Kris_idle_down_mech_anim:
    "Kris_idle_down_mech_1.png"
    pause 0.064
    "Kris_idle_down_mech_2.png"
    pause 0.064
    "Kris_idle_down_mech_3.png"
    pause 0.064
    "Kris_idle_down_mech_4.png"
    pause 0.064
    "Kris_idle_down_mech_5.png"
    pause 0.064
    repeat

image Kris_idle_down_sword_anim:
    "kris_idle_down_sword1.png"
    pause 0.2
    "kris_idle_down_sword2.png"
    pause 0.2
    "kris_idle_down_sword3.png"
    pause 0.2
    "kris_idle_down_sword4.png"
    pause 0.2
    "kris_idle_down_sword5.png"
    pause 0.2
    repeat

image kris_idle_down_shield_anim:
    "kris_idle_down_shield1.png"
    pause 0.2
    "kris_idle_down_shield2.png"
    pause 0.2
    "kris_idle_down_shield3.png"
    pause 0.2
    "kris_idle_down_shield4.png"
    pause 0.2
    "kris_idle_down_shield5.png"
    pause 0.2
    repeat

image Kris_idle_up_none_anim:
    "kris_idle_up_none1.png"

image Kris_idle_down_none_anim:
    "kris_idle_down1.png"
    pause 0.2
    "kris_idle_down2.png"
    pause 0.2
    "kris_idle_down3.png"
    pause 0.2
    "kris_idle_down4.png"
    pause 0.2
    "kris_idle_down5.png"
    pause 0.2
    repeat

# ------------------------------------------------------------
# DEAD
# ------------------------------------------------------------

image Kris_dead_up_anim:
    "Kris_dead_up_1.png"
    pause 1.3
    "Kris_dead_up_2.png"
    pause 1.3
    repeat

image Kris_fall_up_anim:
    "kris_fall_up_1.png"
    pause 1.3
    "kris_fall_up_2.png"
    pause 1.3
    repeat 

image Kris_fall_down_anim:
    "kris_fall_down_1.png"
    pause 1.3
    "kris_fall_down_2.png"
    pause 1.3
    repeat 

image Kris_dead_down_anim:
    "Kris_dead_down_1.png"
    pause 1.3
    "Kris_dead_down_2.png"
    pause 1.3
    repeat

# ------------------------------------------------------------
# ACT
# ------------------------------------------------------------

image Kris_act_up_anim:
    "Kris_act_up_1.png"
    pause 0.064
    "Kris_act_up_2.png"
    pause 0.064
    "Kris_act_up_3.png"
    pause 0.064
    "Kris_act_up_4.png"
    pause 0.064
    "Kris_act_up_5.png"
    pause 0.064
    "Kris_act_up_6.png"
    pause 0.064
    "Kris_act_up_7.png"
    pause 0.064
    "Kris_act_up_8.png"
    pause 0.064
    "Kris_act_up_9.png"
    pause 0.064
    "Kris_act_up_10.png"
    pause 0.064
    "Kris_act_up_11.png"
    pause 0.064
    "Kris_act_up_12.png"
    pause 0.064
    "Kris_act_up_13.png"
    pause 0.064
    "Kris_act_up_14.png"
    pause 0.064
    "Kris_act_up_15.png"
    pause 0.064
    "Kris_act_up_16.png"

image Kris_act_down_anim:
    "Kris_act_down_1.png"
    pause 0.064
    "Kris_act_down_2.png"
    pause 0.064
    "Kris_act_down_3.png"
    pause 0.064
    "Kris_act_down_4.png"
    pause 0.064
    "Kris_act_down_5.png"
    pause 0.064
    "Kris_act_down_6.png"
    pause 0.064
    "Kris_act_down_7.png"
    pause 0.064
    "Kris_act_down_8.png"
    pause 0.064
    "Kris_act_down_9.png"
    pause 0.064
    "Kris_act_down_10.png"
    pause 0.064
    "Kris_act_down_11.png"
    pause 0.064
    "Kris_act_down_12.png"
    pause 0.064
    "Kris_act_down_13.png"
    pause 0.064
    "Kris_act_down_14.png"
    pause 0.064
    "Kris_act_down_15.png"
    pause 0.064
    "Kris_act_down_16.png"

image Kris_act_down_none_anim:
    "kris_act_down_none_1.png"
    pause 0.064
    "kris_act_down_none_2.png"
    pause 0.064
    "kris_act_down_none_3.png"
    pause 0.064
    "kris_act_down_none_4.png"
    pause 0.064
    "kris_act_down_none_5.png"
    pause 0.064
    "kris_act_down_none_6.png"
    pause 0.064
    "kris_act_down_none_7.png"
    pause 0.064
    "kris_act_down_none_8.png"
    pause 0.064
    "kris_act_down_none_9.png"
    pause 0.064
    "kris_act_down_none_10.png"
    pause 0.064
    "kris_act_down_none_11.png"
    pause 0.064
    "kris_act_down_none_12.png"
    pause 0.064
    "kris_act_down_none_13.png"
    pause 0.064
    "kris_act_down_none_14.png"
    pause 0.064
    "kris_act_down_none_15.png"
    pause 0.064
    "kris_act_down_none_16.png"
    pause 0.064

image Kris_act_down_sword_anim:
    "kris_act_down_sword_1.png"
    pause 0.064
    "kris_act_down_sword_2.png"
    pause 0.064
    "kris_act_down_sword_3.png"
    pause 0.064
    "kris_act_down_sword_4.png"
    pause 0.064
    "kris_act_down_sword_5.png"
    pause 0.064
    "kris_act_down_sword_6.png"
    pause 0.064
    "kris_act_down_sword_7.png"
    pause 0.064
    "kris_act_down_sword_8.png"
    pause 0.064
    "kris_act_down_sword_9.png"
    pause 0.064
    "kris_act_down_sword_10.png"
    pause 0.064
    "kris_act_down_sword_11.png"
    pause 0.064
    "kris_act_down_sword_12.png"
    pause 0.064
    "kris_act_down_sword_13.png"
    pause 0.064
    "kris_act_down_sword_14.png"
    pause 0.064
    "kris_act_down_sword_15.png"
    pause 0.064
    "kris_act_down_sword_16.png"
    pause 0.064
    "kris_act_down_sword_17.png"
    pause 0.064
    "kris_act_down_sword_18.png"
    pause 0.064

image Kris_act_down_mech_anim:
    "Kris_act_down_mech_1.png"
    pause 0.064
    "Kris_act_down_mech_2.png"
    pause 0.064
    "Kris_act_down_mech_3.png"
    pause 0.064
    "Kris_act_down_mech_4.png"
    pause 0.064
    "Kris_act_down_mech_5.png"
    pause 0.064
    "Kris_act_down_mech_6.png"
    pause 0.064
    "Kris_act_down_mech_7.png"
    pause 0.064
    "Kris_act_down_mech_8.png"
    pause 0.064
    "Kris_act_down_mech_9.png"
    pause 0.064
    "Kris_act_down_mech_10.png"
    pause 0.064
    "Kris_act_down_mech_11.png"
    pause 0.064
    "Kris_act_down_mech_12.png"
    pause 0.064
    "Kris_act_down_mech_13.png"
    pause 0.064
    "Kris_act_down_mech_14.png"
    pause 0.064
    "Kris_act_down_mech_15.png"
    pause 0.064
    "Kris_act_down_mech_16.png"
    pause 0.064
    "Kris_act_down_mech_17.png"
    pause 0.064
    "Kris_act_down_mech_18.png"

image Kris_act_down_shield_anim:
    "kris_act_down_shield_1.png"
    pause 0.064
    "kris_act_down_shield_2.png"
    pause 0.064
    "kris_act_down_shield_3.png"
    pause 0.064
    "kris_act_down_shield_4.png"
    pause 0.064
    "kris_act_down_shield_5.png"
    pause 0.064
    "kris_act_down_shield_6.png"
    pause 0.064
    "kris_act_down_shield_7.png"
    pause 0.064
    "kris_act_down_shield_8.png"
    pause 0.064
    "kris_act_down_shield_9.png"
    pause 0.064
    "kris_act_down_shield_10.png"
    pause 0.064
    "kris_act_down_shield_11.png"
    pause 0.064
    "kris_act_down_shield_12.png"
    pause 0.064
    "kris_act_down_shield_13.png"
    pause 0.064
    "kris_act_down_shield_14.png"
    pause 0.064
    "kris_act_down_shield_15.png"
    pause 0.064
    "kris_act_down_shield_16.png"
    pause 0.064

# ------------------------------------------------------------
# ACT2
# ------------------------------------------------------------

image Kris_act2_up_anim:
    "Kris_act_up_3.png"
    pause 0.064
    "Kris_act_up_2.png"
    pause 0.064
    "Kris_act_up_1.png"

image Kris_act2_down_anim:
    "Kris_act_down_3.png"
    pause 0.064
    "Kris_act_down_2.png"
    pause 0.064
    "Kris_act_down_1.png"

image Kris_act2_down_none_anim:
    "kris_act_down_none_3.png"
    pause 0.064
    "kris_act_down_none_2.png"
    pause 0.064
    "kris_act_down_none_1.png"

image Kris_act2_down_sword_anim:
    "kris_act_down_sword_3.png"
    pause 0.064
    "kris_act_down_sword_2.png"
    pause 0.064
    "kris_act_down_sword_1.png"

image Kris_act2_down_mech_anim:
    "Kris_act_down_mech_3.png"
    pause 0.064
    "Kris_act_down_mech_2.png"
    pause 0.064
    "Kris_act_down_mech_1.png"

image Kris_act2_down_shield_anim:
    "kris_act_down_shield_2.png"
    pause 0.064
    "kris_act_down_shield_1.png"
    pause 0.064

# ------------------------------------------------------------
# ITEM
# ------------------------------------------------------------

image Kris_item_up_anim:
    "kris_item_up_1.png"
    pause 0.064
    "kris_item_up_2.png"
    pause 0.064
    "kris_item_up_3.png"
    pause 0.064
    "kris_item_up_4.png"
    pause 0.064
    "kris_item_up_5.png"
    pause 0.064
    "kris_item_up_6.png"
    pause 0.064
    "kris_item_up_7.png"
    pause 0.064
    "kris_item_up_8.png"
    pause 0.064
    "kris_item_up_9.png"
    pause 0.064
    "kris_item_up_10.png"

image Kris_item_down_anim:
    "Kris_act_down_1.png"
    pause 0.064
    "Kris_act_down_2.png"
    pause 0.064
    "Kris_act_down_3.png"
    pause 0.064
    "Kris_act_down_4.png"
    pause 0.064
    "Kris_act_down_5.png"
    pause 0.064
    "Kris_act_down_6.png"
    pause 0.064
    "Kris_act_down_7.png"
    pause 0.064
    "Kris_act_down_8.png"
    pause 0.064
    "Kris_act_down_9.png"
    pause 0.064
    "Kris_act_down_10.png"

image Kris_item_down_sword_anim:
    "kris_item_down_sword_1.png"
    pause 0.064
    "kris_item_down_sword_2.png"
    pause 0.064
    "kris_item_down_sword_3.png"
    pause 0.064
    "kris_item_down_sword_4.png"
    pause 0.064
    "kris_item_down_sword_5.png"
    pause 0.064
    "kris_item_down_sword_6.png"
    pause 0.064
    "kris_item_down_sword_7.png"
    pause 0.064
    "kris_item_down_sword_8.png"
    pause 0.064
    "kris_item_down_sword_9.png"
    pause 0.064
    "kris_item_down_sword_10.png"
    pause 0.064

image Kris_item_down_mech_anim:
    "Kris_act_down_mech_1.png"
    pause 0.064
    "Kris_act_down_mech_2.png"
    pause 0.064
    "Kris_act_down_mech_3.png"
    pause 0.064
    "Kris_act_down_mech_4.png"
    pause 0.064
    "Kris_act_down_mech_5.png"
    pause 0.064
    "Kris_act_down_mech_6.png"
    pause 0.064
    "Kris_act_down_mech_7.png"
    pause 0.064
    "Kris_act_down_mech_8.png"
    pause 0.064
    "Kris_act_down_mech_9.png"
    pause 0.064
    "Kris_act_down_mech_10.png"

image Kris_item_down_shield_anim:
    "kris_item_down_shield_1.png"
    pause 0.064
    "kris_item_down_shield_2.png"
    pause 0.064
    "kris_item_down_shield_3.png"
    pause 0.064
    "kris_item_down_shield_4.png"
    pause 0.064
    "kris_item_down_shield_5.png"
    pause 0.064
    "kris_item_down_shield_6.png"
    pause 0.064
    "kris_item_down_shield_7.png"
    pause 0.064
    "kris_item_down_shield_8.png"
    pause 0.064
    "kris_item_down_shield_9.png"
    pause 0.064

# ------------------------------------------------------------
# ITEM2
# ------------------------------------------------------------

image Kris_item2_up_anim:
    "kris_item_up_3.png"
    pause 0.15
    "kris_item_up_2.png"
    pause 0.15
    "kris_item_up_1.png"

image Kris_item2_down_anim:
    "Kris_act_down_3.png"
    pause 0.15
    "Kris_act_down_2.png"
    pause 0.15
    "Kris_act_down_1.png"

image Kris_item2_down_sword_anim:
    "kris_item_down_sword_3.png"
    pause 0.15
    "kris_item_down_sword_2.png"
    pause 0.15
    "kris_item_down_sword_1.png"

image Kris_item2_down_mech_anim:
    "Kris_act_down_mech_3.png"
    pause 0.15
    "Kris_act_down_mech_2.png"
    pause 0.15
    "Kris_act_down_mech_1.png"

image Kris_item2_down_shield_anim:
    "kris_item_down_shield_2.png"
    pause 0.15
    "kris_item_down_shield_1.png"
    pause 0.15

# ------------------------------------------------------------
# ATTACKS / DEFEND
# ------------------------------------------------------------

image Kris_atk1_up_anim:
    "Kris_atk1_up_1.png"
    pause 0.064
    "Kris_atk1_up_2.png"
    pause 0.064
    "Kris_atk1_up_3.png"
    pause 0.064
    "Kris_atk1_up_4.png"
    pause 0.064
    "Kris_atk1_up_5.png"
    pause 0.064
    "Kris_atk1_up_6.png"
    pause 0.064
    "Kris_atk1_up_7.png"

image Kris_atk1_down_anim:
    "Kris_atk1_down_1.png"
    pause 0.064
    "Kris_atk1_down_2.png"
    pause 0.064
    "Kris_atk1_down_3.png"
    pause 0.064
    "Kris_atk1_down_4.png"
    pause 0.064
    "Kris_atk1_down_5.png"
    pause 0.064
    "Kris_atk1_down_6.png"
    pause 0.064
    "Kris_atk1_down_7.png"

image Kris_defend_up_anim:
    "Kris_atk2_up_1.png"
    pause 0.064
    "Kris_atk2_up_2.png"
    pause 0.064
    "Kris_atk2_up_3.png"
    pause 0.064
    "Kris_atk2_up_4.png"

image Kris_defend_down_anim:
    "Kris_atk2_down_1.png"
    pause 0.064
    "Kris_atk2_down_2.png"
    pause 0.064
    "Kris_atk2_down_3.png"
    pause 0.064
    "Kris_atk2_down_4.png"

image Kris_defend_down_mech_anim:
    "Kris_atk2_down_mech_1.png"
    pause 0.064
    "Kris_atk2_down_mech_2.png"
    pause 0.064
    "Kris_atk2_down_mech_3.png"
    pause 0.064
    "Kris_atk2_down_mech_4.png"

image Kris_defend_down_shield_anim:
    "Kris_atk2_down_shield_1.png"
    pause 0.064
    "Kris_atk2_down_shield_2.png"
    pause 0.064
    "Kris_atk2_down_shield_3.png"
    pause 0.064
    "Kris_atk2_down_shield_4.png"

image Kris_atk3_anim:
    pause 1.0
    "kris_down_fight3_1.png"
    pause 0.064
    "kris_down_fight3_2.png"
    pause 0.064
    "kris_down_fight3_3.png"
    pause 0.064
    "kris_down_fight3_4.png"
    pause 0.064
    "kris_down_fight3_5.png"
    pause 0.064
    "kris_down_fight3_6.png"
    pause 0.064
    "kris_down_fight3_7.png"
    pause 0.064
    "kris_down_fight3_8.png"
    pause 1.0
    "Kris_down_shield_damaged.png"


image Kris_atk4_anim:
    "Kris_atk4_1.png"
    pause 0.064
    "Kris_atk4_2.png"
    pause 0.064
    "Kris_atk4_3.png"
    pause 0.064
    "Kris_atk4_4.png"
    pause 0.064
    "Kris_atk4_5.png"
    pause 0.064
    "Kris_atk4_6.png"
    pause 0.064
    "Kris_atk4_7.png"
    pause 0.064
    "Kris_atk4_8.png"

# ------------------------------------------------------------
# MAGIC
# ------------------------------------------------------------

image Kris_mag1_up_anim:
    "Kris_mag1_up_1.png"
    pause 0.064
    "Kris_mag1_up_2.png"
    pause 0.064
    "Kris_mag1_up_3.png"
    pause 0.064
    "Kris_mag1_up_4.png"
    pause 0.064
    "Kris_mag1_up_5.png"
    pause 0.064
    "Kris_mag1_up_6.png"
    pause 0.064
    "Kris_mag1_up_7.png"
    pause 0.064
    "Kris_mag1_up_8.png"
    pause 0.064
    "Kris_mag1_up_9.png"
    pause 0.064
    "Kris_mag1_up_10.png"
    pause 0.064
    "Kris_mag1_up_11.png"
    pause 0.064
    "Kris_mag1_up_12.png"
    pause 0.064
    "Kris_mag1_up_13.png"
    pause 0.064
    "Kris_mag1_up_14.png"
    pause 0.064
    "Kris_mag1_up_15.png"
    pause 0.064
    "Kris_mag1_up_16.png"
    pause 0.064
    "Kris_mag1_up_17.png"
    pause 0.064
    "Kris_mag1_up_18.png"
    pause 0.064
    "Kris_mag1_up_19.png"
    pause 0.064
    "Kris_mag1_up_20.png"
    pause 0.064
    "Kris_mag1_up_21.png"

image Kris_mag1_up_shield_anim:
    "Kris_mag1_up_shield_1.png"
    pause 0.064
    "Kris_mag1_up_shield_2.png"
    pause 0.064
    "Kris_mag1_up_shield_3.png"
    pause 0.064
    "Kris_mag1_up_shield_4.png"
    pause 0.064
    "Kris_mag1_up_shield_5.png"
    pause 0.064
    "Kris_mag1_up_shield_6.png"
    pause 0.064
    "Kris_mag1_up_shield_7.png"
    pause 0.064
    "Kris_mag1_up_shield_8.png"
    pause 0.064
    "Kris_mag1_up_shield_9.png"
    pause 0.064
    "Kris_mag1_up_shield_10.png"
    pause 0.064
    "Kris_mag1_up_shield_11.png"
    pause 0.064
    "Kris_mag1_up_shield_12.png"
    pause 0.064
    "Kris_mag1_up_shield_13.png"
    pause 0.064
    "Kris_mag1_up_shield_14.png"
    pause 0.064
    "Kris_mag1_up_shield_15.png"
    pause 0.064
    "Kris_mag1_up_shield_16.png"
    pause 0.064
    "Kris_mag1_up_shield_17.png"
    pause 0.064
    "Kris_mag1_up_shield_18.png"
    pause 0.064
    "Kris_mag1_up_shield_19.png"
    pause 0.064
    "Kris_mag1_up_shield_20.png"
    pause 0.064
    "Kris_mag1_up_shield_21.png"
    pause 0.064
    "Kris_mag1_up_shield_22.png"
    pause 0.064
    "Kris_mag1_up_shield_23.png"
    pause 0.064
    "Kris_mag1_up_shield_24.png"
    pause 0.064
    "Kris_mag1_up_shield_25.png"

image Kris_mag2_up_anim:
    "Kris_mag2_up_1.png"
    pause 0.064
    "Kris_mag2_up_2.png"
    pause 0.064
    "Kris_mag2_up_3.png"
    pause 0.064
    "Kris_mag2_up_4.png"
    pause 0.064
    "Kris_mag2_up_5.png"
    pause 0.064
    "Kris_mag2_up_6.png"
    pause 0.064
    "Kris_mag2_up_7.png"
    pause 0.064
    "Kris_mag2_up_8.png"
    pause 0.064
    "Kris_mag2_up_9.png"
    pause 0.064
    "Kris_mag2_up_10.png"
    pause 0.064
    "Kris_mag2_up_11.png"
    pause 0.064
    "Kris_mag2_up_12.png"
    pause 0.064
    "Kris_mag2_up_13.png"
    pause 0.064
    "Kris_mag2_up_14.png"
    pause 0.064
    "Kris_mag2_up_15.png"
    pause 0.064
    "Kris_mag2_up_16.png"
    pause 0.064
    "Kris_mag2_up_17.png"
    pause 0.064
    "Kris_mag2_up_18.png"
    pause 0.064
    "Kris_mag2_up_19.png"
    pause 0.064
    "Kris_mag2_up_20.png"

image Kris_mag2_up_mech_anim:
    "Kris_mag2_up_mech_1.png"
    pause 0.064
    "Kris_mag2_up_mech_2.png"
    pause 0.064
    "Kris_mag2_up_mech_3.png"
    pause 0.064
    "Kris_mag2_up_mech_4.png"
    pause 0.064
    "Kris_mag2_up_mech_5.png"
    pause 0.064
    "Kris_mag2_up_mech_6.png"
    pause 0.064
    "Kris_mag2_up_mech_7.png"
    pause 0.064
    "Kris_mag2_up_mech_8.png"
    pause 0.064
    "Kris_mag2_up_mech_9.png"
    pause 0.064
    "Kris_mag2_up_mech_10.png"
    pause 0.064
    "Kris_mag2_up_mech_11.png"
    pause 0.064
    "Kris_mag2_up_mech_12.png"
    pause 0.064
    "Kris_mag2_up_mech_13.png"
    pause 0.064
    "Kris_mag2_up_mech_14.png"
    pause 0.064
    "Kris_mag2_up_mech_15.png"
    pause 0.064
    "Kris_mag2_up_mech_16.png"
    pause 0.064
    "Kris_mag2_up_mech_17.png"
    pause 0.064
    "Kris_mag2_up_mech_18.png"
    pause 0.064
    "Kris_mag2_up_mech_19.png"
    pause 0.064
    "Kris_mag2_up_mech_20.png"
    pause 0.064
    "Kris_mag2_up_mech_21.png"
    pause 0.064
    "Kris_mag2_up_mech_22.png"
    pause 0.064
    "Kris_mag2_up_mech_23.png"
    pause 0.064
    "Kris_mag2_up_mech_24.png"
    pause 0.064
    "Kris_mag2_up_mech_25.png"

image Kris_mag3_up_anim:
    "Kris_mag3_up1.png"
    pause 0.064
    "Kris_mag3_up2.png"
    pause 0.064
    "Kris_mag3_up3.png"
    pause 0.064
    "Kris_mag3_up4.png"
    pause 0.064
    "Kris_mag3_up5.png"
    pause 0.064
    "Kris_mag3_up6.png"
    pause 0.064
    "Kris_mag3_up7.png"
    pause 0.064
    "Kris_mag3_up8.png"
    pause 0.064
    "Kris_mag3_up9.png"
    pause 0.064
    "Kris_mag3_up10.png"
    pause 0.064
    "Kris_mag3_up11.png"
    pause 0.064
    "Kris_mag3_up12.png"


image Kris_mag3_None_anim:
    "Kris_mag3_None1.png"
    pause 0.064
    "Kris_mag3_None3.png"
    pause 0.064
    "Kris_mag3_None3.png"
    pause 0.064
    "Kris_mag3_None4.png"
    pause 0.064
    "Kris_mag3_None5.png"
    pause 0.064
    "Kris_mag3_None6.png"
    pause 0.064
    "Kris_mag3_None7.png"
    pause 0.064
    "Kris_mag3_None8.png"
    pause 0.064
    "Kris_mag3_None9.png"
    pause 0.064
    "Kris_mag3_None10.png"
    pause 0.064
    "Kris_mag3_None11.png"
    

image Kris_mag3_mech_anim:
    "Kris_mag3_sword1.png"
    pause 0.064
    "Kris_mag3_sword2.png"
    pause 0.064
    "Kris_mag3_sword3.png"
    pause 0.064
    "Kris_mag3_sword4.png"
    pause 0.064
    "Kris_mag3_sword5.png"
    pause 0.064
    "Kris_mag3_sword6.png"
    pause 0.064
    "Kris_mag3_sword7.png"
    pause 0.064
    "Kris_mag3_sword8.png"
    pause 0.064
    "Kris_mag3_sword9.png"
    pause 0.064
    "Kris_mag3_sword10.png"
    pause 0.064
    "Kris_mag3_sword11.png"
    pause 0.064
    "Kris_mag3_sword12.png"
    

image Kris_mag3_shield_anim:
    "Kris_mag3_shield1.png"
    pause 0.064
    "Kris_mag3_shield2.png"
    pause 0.064
    "Kris_mag3_shield3.png"
    pause 0.064
    "Kris_mag3_shield4.png"
    pause 0.064
    "Kris_mag3_shield5.png"
    pause 0.064
    "Kris_mag3_shield6.png"
    pause 0.064
    "Kris_mag3_shield7.png"
    pause 0.064
    "Kris_mag3_shield8.png"
    pause 0.064
    "Kris_mag3_shield9.png"
    pause 0.064
    "Kris_mag3_shield10.png"
    pause 0.064
    "Kris_mag3_shield11.png"
    pause 0.064
    "Kris_mag3_shield12.png"

# ------------------------------------------------------------
# ГЛАВНАЯ УСЛОВНАЯ КАРТИНКА
# ------------------------------------------------------------
# Логика порядка:
# - смерть ставится выше остальных состояний;
# - затем визуализация урона/лечения, чтобы она перебивала idle/act/item;
# - затем конкретные state-анимации;
# - в конце idle/fallback.

transform Hero_damaged_trans:
    xoffset 0
    linear 0.04 xoffset -8
    linear 0.04 xoffset 8
    linear 0.04 xoffset -8
    linear 0.04 xoffset 8
    linear 0.04 xoffset -8
    linear 0.04 xoffset 8
    linear 0.04 xoffset -8
    linear 0.04 xoffset 8
    linear 0.04 xoffset 0

transform Hero_healed_trans:
    matrixcolor TintMatrix("#00ff00")
    linear 0.50 matrixcolor TintMatrix("#ffffff")

transform shield_damaged:
    easein 0.4 matrixcolor TintMatrix("#eeff00")
    easeout 0.4 matrixcolor TintMatrix("#ffffff")


image Kris_fight2_anim0:
    "Kris_fight2_0_3.png"
    pause 0.3
    "Kris_fight2_0_2.png"
    pause 0.3
    "Kris_fight2_0_1.png"

image Kris_fight2_anim:
    "kris_fight2_1.png"
    pause 0.064
    "kris_fight2_2.png"
    pause 0.064
    "kris_fight2_3.png"
    pause 0.064
    "kris_fight2_4.png"
    pause 0.064
    "kris_fight2_5.png"
    pause 0.064
    "kris_fight2_6.png"
    pause 0.064
    "kris_fight2_7.png"
    pause 0.064

image Kris_fight2_anim2:
    "Kris_fight2_2_5.png"
    pause 0.1
    "Kris_fight2_2_4.png"
    pause 0.1
    "Kris_fight2_2_3.png"
    pause 0.1
    "Kris_fight2_2_2.png"
    pause 0.1
    "Kris_fight2_2_1.png"


image Kris_down_fight1_anim:
    "kris_down_fight1_1.png"
    pause 0.25
    "kris_down_fight1_2.png"
    pause 0.25
    "kris_down_fight1_3.png"
    pause 0.75


    "kris_down_fight1_4.png"
    pause 0.064316
    "kris_down_fight1_5.png"
    pause 0.064316
    "kris_down_fight1_6.png"
    pause 0.06416
    "kris_down_fight1_7.png"
    pause 1.5
    "kris_down_fight1_1.png"

    #"Kris_idle_down_1.png"
    #pause 0.2
    #"Kris_idle_down_2.png"
    #pause 0.2
    #"Kris_idle_down_3.png"
    #pause 0.2
    #"Kris_idle_down_4.png"
    #pause 0.2
    #"Kris_idle_down_5.png"


image Kris_down_fight1_anim_part2:
    "kris_up_fight1_3.png"
    pause 1.2
    "kris_down_fight1_4.png"
    pause 0.064316
    "kris_down_fight1_5.png"
    pause 0.064316
    "kris_down_fight1_6.png"
    pause 0.06416
    "kris_down_fight1_7.png"
    pause 1.5
    "kris_down_fight1_1.png"



image Kris_up_fight1_anim_part1:
    "kris_up_fight1_1.png"
    pause 0.25
    "kris_up_fight1_2.png"
    pause 0.25
    "kris_up_fight1_3.png"
    pause 5


    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    
    
image Kris_up_fight1_anim_part2:
    "kris_up_fight1_3.png"
    pause 1.2
    "kris_up_fight1_4.png"
    pause 0.064316
    "kris_up_fight1_5.png"
    pause 0.064316
    "kris_up_fight1_6.png"
    pause 0.06416
    "kris_up_fight1_7.png"
    pause 1.5
    "kris_up_fight1_1.png"


image Kris_up_fight1_anim_part2_complex = ConditionSwitch(
    "store.pers_dict['Крис'].prone_debuff > 0", "Kris_fall_up_anim",
    "True", "Kris_up_fight1_anim_part2"
)

image Kris_up_magic1_anim:
    "kris_up_magic1_1.png"
    pause 0.064
    "kris_up_magic1_2.png"
    pause 0.064
    "kris_up_magic1_3.png"
    pause 0.064
    "kris_up_magic1_4.png"
    pause 0.064
    "kris_up_magic1_5.png"
    pause 0.064
    "kris_up_magic1_6.png"
    pause 0.064
    "kris_up_magic1_7.png"
    pause 0.064
    "kris_up_magic1_8.png"
    pause 0.064
    "kris_up_magic1_9.png"
    pause 0.064
    "kris_up_magic1_10.png"
    pause 0.064
    "kris_up_magic1_11.png"
    pause 0.064
    "kris_up_magic1_12.png"
    pause 0.064
    "kris_up_magic1_13.png"
    pause 0.064
    "kris_up_magic1_14.png"
    pause 0.064
    "kris_up_magic1_15.png"
    pause 0.064
    "kris_up_magic1_16.png"
    pause 0.064
    "kris_up_magic1_17.png"
    pause 0.064
    "kris_up_magic1_18.png"
    pause 0.064
    "kris_up_magic1_19.png"
    pause 0.064
    "kris_up_magic1_20.png"
    pause 0.064

image Kris_down_magic1_anim:
    "kris_down_magic1_1.png"
    pause 0.064
    "kris_down_magic1_2.png"
    pause 0.064
    "kris_down_magic1_3.png"
    pause 0.064
    "kris_down_magic1_4.png"
    pause 0.064
    "kris_down_magic1_5.png"
    pause 0.064
    "kris_down_magic1_6.png"
    pause 0.064
    "kris_down_magic1_7.png"
    pause 0.064
    "kris_down_magic1_8.png"
    pause 0.064
    "kris_down_magic1_9.png"
    pause 0.064
    "kris_down_magic1_10.png"
    pause 0.064
    "kris_down_magic1_11.png"
    pause 0.064
    "kris_down_magic1_12.png"
    pause 0.064
    "kris_down_magic1_13.png"
    pause 0.064
    "kris_down_magic1_14.png"
    pause 0.064
    "kris_down_magic1_15.png"
    pause 0.064
    "kris_down_magic1_16.png"
    pause 0.064
    "kris_down_magic1_17.png"
    pause 0.064
    "kris_down_magic1_18.png"
    pause 0.064
    "kris_down_magic1_19.png"
    pause 0.064

image Kris_down_magic1_shield_anim:
    "kris_down_magic1_shield1.png"
    pause 0.064
    "kris_down_magic1_shield2.png"
    pause 0.064
    "kris_down_magic1_shield3.png"
    pause 0.064
    "kris_down_magic1_shield4.png"
    pause 0.064
    "kris_down_magic1_shield5.png"
    pause 0.064
    "kris_down_magic1_shield6.png"
    pause 0.064
    "kris_down_magic1_shield7.png"
    pause 0.064
    "kris_down_magic1_shield8.png"
    pause 0.064
    "kris_down_magic1_shield9.png"
    pause 0.064
    "kris_down_magic1_shield10.png"
    pause 0.064
    "kris_down_magic1_shield11.png"
    pause 0.064
    "kris_down_magic1_shield12.png"
    pause 0.064
    "kris_down_magic1_shield13.png"
    pause 0.064
    "kris_down_magic1_shield14.png"
    pause 0.064
    "kris_down_magic1_shield15.png"
    pause 0.064
    "kris_down_magic1_shield16.png"
    pause 0.064
    "kris_down_magic1_shield17.png"
    pause 0.064
    "kris_down_magic1_shield18.png"
    pause 0.064
    "kris_down_magic1_shield19.png"
    pause 0.064
    "kris_down_magic1_shield20.png"
    pause 0.064
    "kris_down_magic1_shield21.png"
    pause 0.064
    "kris_down_magic1_shield22.png"
    pause 0.064
    "kris_down_magic1_shield23.png"
    pause 0.064
    "kris_down_magic1_shield24.png"
    pause 0.064
    "kris_down_magic1_shield25.png"
    pause 0.064
    "kris_down_magic1_shield26.png"
    pause 0.064
    "kris_down_magic1_shield27.png"
    pause 0.064
    "kris_down_magic1_shield28.png"
    pause 0.064
    "kris_down_magic1_shield29.png"
    pause 0.064
    "kris_down_magic1_shield30.png"
    pause 0.064

image Kris_up_magic2_anim:
    "kris_up_magic2_1.png"
    pause 0.064
    "kris_up_magic2_2.png"
    pause 0.064
    "kris_up_magic2_3.png"
    pause 0.064
    "kris_up_magic2_4.png"
    pause 0.064
    "kris_up_magic2_5.png"
    pause 0.064
    "kris_up_magic2_6.png"
    pause 0.064
    "kris_up_magic2_7.png"
    pause 0.064
    "kris_up_magic2_8.png"
    pause 0.064
    "kris_up_magic2_9.png"
    pause 0.064
    "kris_up_magic2_10.png"
    pause 0.064
    "kris_up_magic2_11.png"
    pause 0.064
    "kris_up_magic2_12.png"
    pause 0.064
    "kris_up_magic2_13.png"
    pause 0.064
    "kris_up_magic2_14.png"
    pause 0.064
    "kris_up_magic2_15.png"
    pause 0.064
    "kris_up_magic2_16.png"
    pause 0.064
    "kris_up_magic2_17.png"
    pause 0.064
    "kris_up_magic2_18.png"
    pause 0.064
    "kris_up_magic2_19.png"
    pause 0.064
    "kris_up_magic2_20.png"
    pause 0.064

image Kris_down_magic2_none_anim:
    "kris_down_magic2_none_1.png"
    pause 0.064
    "kris_down_magic2_none_2.png"
    pause 0.064
    "kris_down_magic2_none_3.png"
    pause 0.064
    "kris_down_magic2_none_4.png"
    pause 0.064
    "kris_down_magic2_none_5.png"
    pause 0.064
    "kris_down_magic2_none_6.png"
    pause 0.064
    "kris_down_magic2_none_7.png"
    pause 0.064
    "kris_down_magic2_none_8.png"
    pause 0.064
    "kris_down_magic2_none_9.png"
    pause 0.064
    "kris_down_magic2_none_10.png"
    pause 0.064
    "kris_down_magic2_none_11.png"
    pause 0.064
    "kris_down_magic2_none_12.png"
    pause 0.064
    "kris_down_magic2_none_13.png"
    pause 0.064
    "kris_down_magic2_none_14.png"
    pause 0.064
    "kris_down_magic2_none_15.png"
    pause 0.064
    "kris_down_magic2_none_16.png"
    pause 0.064
    "kris_down_magic2_none_17.png"
    pause 0.064
    "kris_down_magic2_none_18.png"
    pause 0.064
    "kris_down_magic2_none_19.png"
    pause 0.064
    "kris_down_magic2_none_20.png"
    pause 0.064

image Kris_down_magic2_sword_anim:
    "kris_down_magic2_shield_1.png"
    pause 0.064
    "kris_down_magic2_shield_2.png"
    pause 0.064
    "kris_down_magic2_shield_3.png"
    pause 0.064
    "kris_down_magic2_shield_4.png"
    pause 0.064
    "kris_down_magic2_shield_5.png"
    pause 0.064
    "kris_down_magic2_shield_6.png"
    pause 0.064
    "kris_down_magic2_shield_7.png"
    pause 0.064
    "kris_down_magic2_shield_8.png"
    pause 0.064
    "kris_down_magic2_shield_9.png"
    pause 0.064
    "kris_down_magic2_shield_10.png"
    pause 0.064
    "kris_down_magic2_shield_11.png"
    pause 0.064
    "kris_down_magic2_shield_12.png"
    pause 0.064
    "kris_down_magic2_shield_13.png"
    pause 0.064
    "kris_down_magic2_shield_14.png"
    pause 0.064
    "kris_down_magic2_shield_15.png"
    pause 0.064
    "kris_down_magic2_shield_16.png"
    pause 0.064
    "kris_down_magic2_shield_17.png"
    pause 0.064
    "kris_down_magic2_shield_18.png"
    pause 0.064
    "kris_down_magic2_shield_19.png"
    pause 0.064
    "kris_down_magic2_shield_20.png"
    pause 0.064
    "kris_down_magic2_shield_21.png"
    pause 0.064
    "kris_down_magic2_shield_22.png"
    pause 0.064
    "kris_down_magic2_shield_23.png"
    pause 0.064
    "kris_down_magic2_shield_24.png"
    pause 0.064
    "kris_down_magic2_shield_25.png"
    pause 0.064
    "kris_down_magic2_shield_26.png"
    pause 0.064
    "kris_down_magic2_shield_27.png"
    pause 0.064
    "kris_down_magic2_shield_28.png"
    pause 0.064
    "kris_down_magic2_shield_29.png"
    pause 0.064
    "kris_down_magic2_shield_30.png"
    pause 0.064
    "kris_down_magic2_shield_31.png"
    pause 0.064
    "kris_down_magic2_shield_32.png"
    pause 0.064

image Kris_fight6_anim:
    "kris_fight6_1.png"
    pause 0.064
    "kris_fight6_2.png"
    pause 0.064
    "kris_fight6_3.png"
    pause 0.064
    "kris_fight6_4.png"
    pause 0.064
    "kris_fight6_5.png"
    pause 0.064
    "kris_fight6_6.png"
    pause 0.064
    "kris_fight6_7.png"
    pause 0.064
    "kris_fight6_8.png"
    pause 0.064
    "kris_fight6_9.png"
    pause 0.064
    "kris_fight6_10.png"
    pause 0.064
    "kris_fight6_11.png"
    pause 0.064
    "kris_fight6_12.png"
    pause 0.064
    "kris_fight6_13.png"
    pause 0.064
    "kris_fight6_14.png"
    pause 0.064
    "kris_fight6_15.png"
    pause 0.064

image Kris_defense_up_anim:
    "kris_defense_up_1.png"
    pause 0.064
    "kris_defense_up_2.png"
    pause 0.064
    "kris_defense_up_3.png"
    pause 0.064
    "kris_defense_up_4.png"
    pause 0.064

image Kris_defense_down_none_anim:
    "kris_defense_down_none_1.png"
    pause 0.064
    "kris_defense_down_none_2.png"
    pause 0.064
    "kris_defense_down_none_3.png"
    pause 0.064
    "kris_defense_down_none_4.png"
    pause 0.064

image Kris_defense_down_sword_anim:
    "kris_defense_down_sword_1.png"
    pause 0.064
    "kris_defense_down_sword_2.png"
    pause 0.064
    "kris_defense_down_sword_3.png"
    pause 0.064
    "kris_defense_down_sword_4.png"
    pause 0.064
    "kris_defense_down_sword_5.png"
    pause 0.064

image Kris_defense_down_shield_anim:
    "kris_defense_down_shield_1.png"
    pause 0.064
    "kris_defense_down_shield_2.png"
    pause 0.064
    "kris_defense_down_shield_3.png"
    pause 0.064
    "kris_defense_down_shield_4.png"
    pause 0.064

image Krisfightsprite = ConditionSwitch(

    # DEAD
    "(store.pers_dict['Крис'].current_hp <= 0 or store.pers_dict['Крис'].prone_debuff > 1) and store.pers_dict['Крис'].sprite_style == 'up'", At("Kris_fall_up_anim", Hero_damaged_trans),
    "(store.pers_dict['Крис'].current_hp <= 0 or store.pers_dict['Крис'].prone_debuff > 1) and store.pers_dict['Крис'].sprite_style == 'down'", At("Kris_fall_down_anim",Hero_damaged_trans),

    # HEALED + ITEM
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'up'", At("kris_item_up_10.png", Hero_healed_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", At("Kris_act_down_10.png", Hero_healed_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", At("kris_item_down_sword_10.png", Hero_healed_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", At("kris_item_down_shield_9.png", Hero_healed_trans),

    # DAMAGED + TRANSFORM
    "store.pers_dict['Крис'].damage_gain_for_vis >= 10 and store.pers_dict['Крис'].sprite_style == 'up'", At("kris_damaged_up.png", Hero_damaged_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis >= 10 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", At ("kris_damaged_down_none.png",Hero_damaged_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis >= 10 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", At("kris_damaged_down_sword.png", Hero_damaged_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis >= 10 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", At("kris_down_shield_damaged.png", Hero_damaged_trans),

    # SHIELD DAMAGED + TRANSFORM (СПРАЙТЫ ЗАМЕНЕНЫ НА IDLE АНИМАЦИИ)
    "store.pers_dict['Крис'].damage_gain_for_vis > 0 and store.pers_dict['Крис'].sprite_style == 'up'", At("Kris_idle_up_anim", shield_damaged),
    "store.pers_dict['Крис'].damage_gain_for_vis > 0 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", At("Kris_idle_down_none_anim", shield_damaged),
    "store.pers_dict['Крис'].damage_gain_for_vis > 0 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", At("Kris_idle_down_sword_anim", shield_damaged),
    "store.pers_dict['Крис'].damage_gain_for_vis > 0 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", At("kris_idle_down_shield_anim", shield_damaged),


    # ITEM
    "store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_item_up_anim",
    "store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_item_down_anim",
    "store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_item_down_sword_anim",
    "store.pers_dict['Крис'].state == 'item' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_item_down_shield_anim",

    # ITEM2
    "store.pers_dict['Крис'].state == 'item2' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_item2_up_anim",
    "store.pers_dict['Крис'].state == 'item2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_item2_down_anim",
    "store.pers_dict['Крис'].state == 'item2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_item2_down_sword_anim",
    "store.pers_dict['Крис'].state == 'item2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_item2_down_shield_anim",

    # HEALED + TRANSFORM
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].sprite_style == 'up'", At("Kris_idle_up_anim", Hero_healed_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", At("Kris_idle_down_none_anim", Hero_healed_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", At("Kris_idle_down_sword_anim", Hero_healed_trans),
    "store.pers_dict['Крис'].damage_gain_for_vis <= -2 and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", At("kris_idle_down_shield_anim", Hero_healed_trans),

    # ACT
    "store.pers_dict['Крис'].state == 'act' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_act_up_anim",
    "store.pers_dict['Крис'].state == 'act' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_act_down_none_anim",
    "store.pers_dict['Крис'].state == 'act' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_act_down_sword_anim",
    "store.pers_dict['Крис'].state == 'act' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_act_down_shield_anim",

    # ACT2
    "store.pers_dict['Крис'].state == 'act2' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_act2_up_anim",
    "store.pers_dict['Крис'].state == 'act2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_act2_down_none_anim",
    "store.pers_dict['Крис'].state == 'act2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_act2_down_sword_anim",
    "store.pers_dict['Крис'].state == 'act2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_act2_down_shield_anim",

    #Удар неудачника
    # Видимая fight1-анимация выводится отдельным экранным overlay,
    # чтобы её xpos/ypos были абсолютными координатами экрана, а не hbox.
    "store.pers_dict['Крис'].state == 'fight1' and store.pers_dict['Крис'].sprite_style == 'up'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Крис'].state == 'fight1' and store.pers_dict['Крис'].sprite_style == 'down'", At("Kris_idle_up_none_anim", falsh),
    # Взмах мечом
    "store.pers_dict['Крис'].state == 'fight2_0'", "Kris_fight2_anim0",
    "store.pers_dict['Крис'].state == 'fight2'", "Kris_fight2_anim",
    "store.pers_dict['Крис'].state == 'fight2_2'", "Kris_fight2_anim2",

    # Удар щитом / С разворота! / Бонк! / Отчаянное комбо / Рывок защитника
    "store.pers_dict['Крис'].state == 'fight3_0'", "Kris_down_shield_damaged.png",
    "store.pers_dict['Крис'].state == 'fight3'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Крис'].state == 'fight3_2'", At("Kris_down_shield_damaged.png", kris_fight3_screen_team_target_trans_back),


    "store.pers_dict['Крис'].state == 'fight4'", "Kris_fight2_anim",
    "store.pers_dict['Крис'].state == 'fight5'", "Kris_atk4_anim",
    "store.pers_dict['Крис'].state == 'fight10'", "Kris_fight2_anim",
    "store.pers_dict['Крис'].state == 'fight11'", "Kris_atk4_anim",

    # Колотый удар
    "store.pers_dict['Крис'].state == 'fight6'", "Kris_fight6_anim",
    "store.pers_dict['Крис'].state == 'fight7'", "Kris_atk3_anim",

    # ATTACK_RUKA_1
    "store.pers_dict['Крис'].state == 'attack_ruka_1' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_atk1_up_anim",
    "store.pers_dict['Крис'].state == 'attack_ruka_1' and store.pers_dict['Крис'].sprite_style == 'down'", "Kris_atk1_down_anim",

    # Защищаться
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_defense_up_anim",
    # Защищаться внизу без меча
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_defense_down_none_anim",
    # Защищаться внизу с мечом
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_defense_down_sword_anim",
    # Защищаться
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_defense_down_shield_anim",


    
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_defend_down_anim",
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_defend_down_mech_anim",
    "store.pers_dict['Крис'].state == 'defend' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_defend_down_shield_anim",

    # ATTACK_MECH_3 / ATTACK_SHIELD_4
    "store.pers_dict['Крис'].state == 'attack_mech_3' and store.pers_dict['Крис'].sprite_style == 'down'", "Kris_atk3_anim",
    "store.pers_dict['Крис'].state == 'attack_shield_4' and store.pers_dict['Крис'].sprite_style == 'down'", "Kris_atk4_anim",

    # MAGIC 1
    "store.pers_dict['Крис'].state == 'magic1' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_up_magic1_anim",
    "store.pers_dict['Крис'].state == 'magic1' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_down_magic1_anim",
    "store.pers_dict['Крис'].state == 'magic1' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_down_magic1_anim",
    "store.pers_dict['Крис'].state == 'magic1' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_down_magic1_shield_anim",

    # MAGIC 2
    "store.pers_dict['Крис'].state == 'magic2' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_up_magic2_anim",
    "store.pers_dict['Крис'].state == 'magic2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_down_magic2_none_anim",
    "store.pers_dict['Крис'].state == 'magic2' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_down_magic2_sword_anim",
    
    "store.pers_dict['Крис'].state == 'magic4' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_mag2_up_anim",
    "store.pers_dict['Крис'].state == 'magic4' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_mag2_up_anim",
    "store.pers_dict['Крис'].state == 'magic4' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_mag2_up_mech_anim",

    # MAGIC 3
    "store.pers_dict['Крис'].state == 'magic3' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_mag3_up_anim",
    "store.pers_dict['Крис'].state == 'magic3' and summoned == 0", "Kris_mag3_None_anim",
    "store.pers_dict['Крис'].state == 'magic3' and summoned == 1", "Kris_mag3_mech_anim",
    "store.pers_dict['Крис'].state == 'magic3' and summoned == 2", "Kris_mag3_shield_anim",


    "store.pers_dict['Крис'].state in ('magic5', 'magic6', 'magic7', 'magic8', 'magic9', 'magic10', 'magic11') and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_mag3_Noneanim",
    "store.pers_dict['Крис'].state in ('magic5', 'magic6', 'magic7', 'magic8', 'magic9', 'magic10', 'magic11') and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_mag3_Noneanim",
    "store.pers_dict['Крис'].state in ('magic5', 'magic6', 'magic7', 'magic8', 'magic9', 'magic10', 'magic11') and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_mag3_swordanim",
    "store.pers_dict['Крис'].state in ('magic5', 'magic6', 'magic7', 'magic8', 'magic9', 'magic10', 'magic11') and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "Kris_mag3_shieldanim",

    # IDLE / FALLBACK
    "store.pers_dict['Крис'].state == 'idle' and store.pers_dict['Крис'].sprite_style == 'up' and store.summoned == 0", "Kris_idle_up_anim",
    "store.pers_dict['Крис'].state == 'idle' and store.pers_dict['Крис'].sprite_style == 'up'", "Kris_idle_up_anim",
    "store.pers_dict['Крис'].state == 'idle' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 0", "Kris_idle_down_none_anim",
    "store.pers_dict['Крис'].state == 'idle' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 1", "Kris_idle_down_sword_anim",
    "store.pers_dict['Крис'].state == 'idle' and store.pers_dict['Крис'].sprite_style == 'down' and store.summoned == 2", "kris_idle_down_shield_anim",

    "True", "Kris_idle_down_anim"
)
# Пример использования в screen:
#
# screen battle_screen():
#     add "Krisfightsprite" xpos 500 ypos 300






# ЧАРА
#
# Доступные боевые изображения:
# Kris_pisya3.png — основной верхний спрайт,
# chara_down1.png — нижний спрайт,
# Charaatk1.png — спрайт атаки.
# Разные действия пока анимируются ATL поверх этих изображений. Отдельные
# кадры позже можно заменить внутри image-блоков, не меняя Charafightsprite.

# IDLE / COMMON STATES


image Chara_fight_begun_anim:
    "chara_fight_begun1.png"
    pause 0.064
    "chara_fight_begun2.png"
    pause 0.064
    "chara_fight_begun3.png"
    pause 0.064
    "chara_fight_begun4.png"
    pause 0.064
    "chara_fight_begun5.png"
    pause 0.064
    "chara_fight_begun6.png"
    pause 0.064
    "chara_fight_begun7.png"
    pause 0.064
    "chara_fight_begun8.png"
    pause 0.064
    "chara_fight_begun9.png"
    pause 0.064
    "chara_fight_begun10.png"
    pause 0.064
    "chara_fight_begun11.png"
    pause 0.064
    "chara_fight_begun12.png"
    pause 0.064
    "chara_fight_begun13.png"
    pause 0.064
    "chara_fight_begun14.png"
    pause 0.064
    "chara_fight_begun15.png"
    pause 0.064
    "chara_fight_begun16.png"
    pause 0.064
    "chara_fight_begun17.png"
    pause 0.064
    "chara_fight_begun18.png"
    pause 0.064
    "chara_fight_begun19.png"
    pause 0.064
    "chara_fight_begun20.png"
    pause 0.064
    "chara_fight_begun21.png"
    pause 0.064
    "chara_fight_begun22.png"
    pause 0.064
    "chara_fight_begun23.png"
    pause 0.064
    "chara_fight_begun24.png"
    pause 0.064
    "chara_fight_begun25.png"
    pause 0.064
    "chara_fight_begun26.png"
    pause 0.064
    "chara_fight_begun27.png"
    pause 0.064
    "chara_fight_begun28.png"
    pause 0.064
    "chara_fight_begun29.png"
    pause 0.064
    "chara_fight_begun30.png"
    pause 0.064
    "chara_fight_begun31.png"
    pause 0.064
    "chara_fight_begun32.png"
    pause 0.064
    "chara_fight_begun33.png"
    pause 0.064
    "chara_fight_begun34.png"
    pause 0.064
    "chara_fight_begun35.png"
    pause 0.064
    "chara_fight_begun36.png"
    pause 0.064
    "chara_fight_begun37.png"
    pause 0.064
    "chara_fight_begun38.png"
    pause 0.064
    "chara_fight_begun39.png"
    pause 0.064
    "chara_fight_begun40.png"
    pause 0.064
    "chara_fight_begun41.png"
    pause 0.064
    "chara_fight_begun42.png"
    pause 0.064
    "chara_fight_begun43.png"
    pause 0.064
    

image Chara_idle_up_anim:
    "chara_fight_idle1.png"
    pause 0.2
    "chara_fight_idle2.png"
    pause 0.2
    "chara_fight_idle3.png"
    pause 0.2
    "chara_fight_idle4.png"
    pause 0.2
    "chara_fight_idle5.png"
    pause 0.2
    "chara_fight_idle6.png"
    pause 0.2
    "chara_fight_idle7.png"
    pause 0.2
    "chara_fight_idle8.png"
    pause 0.2
    "chara_fight_idle9.png"
    pause 0.2
    "chara_fight_idle10.png"
    pause 0.2
    "chara_fight_idle11.png"
    pause 0.2
    "chara_fight_idle12.png"
    pause 0.2
    repeat

image Chara_idle_down_anim:
    "chara_down1.png"
    pause 0.45
    yoffset -2
    pause 0.15
    yoffset 0
    repeat

image Chara_dead_up_anim:
    "Kris_pisya3.png"
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.35)
    alpha 0.75

image Chara_dead_down_anim:
    "chara_down1.png"
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.35)
    alpha 0.75

image Chara_defend_up_anim:
    "Kris_pisya3.png"
    ease 0.15 zoom 0.94 xoffset -4
    ease 0.20 zoom 1.0 xoffset 0
    repeat

image Chara_defend_down_anim:
    "chara_down1.png"
    ease 0.15 zoom 0.94 xoffset -4
    ease 0.20 zoom 1.0 xoffset 0
    repeat

# ATTACKS 35–41

# 35 — Удар бунтарки
image chara_fight_fight1:
    "chara_fight_fight1_1.png"
    pause 0.064
    "chara_fight_fight1_2.png"
    pause 0.064
    "chara_fight_fight1_3.png"
    pause 0.064
    "chara_fight_fight1_4.png"
    pause 0.064
    "chara_fight_fight1_5.png"
    pause 0.064
    "chara_fight_fight1_6.png"
    pause 0.064
    "chara_fight_fight1_7.png"
    pause 0.064
    "chara_fight_fight1_8.png"
    pause 0.064
    "chara_fight_fight1_9.png"
    pause 0.064
    "chara_fight_fight1_10.png"
    pause 0.064
    "chara_fight_fight1_11.png"
    pause 0.064
    "chara_fight_fight1_12.png"
    pause 0.064
    "chara_fight_fight1_13.png"
    pause 0.064
    "chara_fight_fight1_14.png"
    pause 0.064
    "chara_fight_fight1_15.png"
    pause 0.064
    "chara_fight_fight1_16.png"
    pause 0.064
    "chara_fight_fight1_17.png"
    pause 0.064
    "chara_fight_fight1_18.png"
    pause 0.064
    "chara_fight_fight1_19.png"
    pause 0.064
    "chara_fight_fight1_20.png"
    pause 0.064
    "chara_fight_fight1_21.png"
    pause 0.064
    "chara_fight_fight1_22.png"
    pause 0.064
    "chara_fight_fight1_23.png"
    pause 0.064
    "chara_fight_fight1_24.png"
    pause 0.064
    "chara_fight_fight1_25.png"
    pause 0.064
    "chara_fight_fight1_26.png"
    pause 0.064
    "chara_fight_fight1_27.png"
    pause 0.064
    "chara_fight_fight1_28.png"
    pause 0.064
    "chara_fight_fight1_29.png"
    pause 0.064
    "chara_fight_fight1_30.png"
    pause 0.064
    "chara_fight_fight1_31.png"
    pause 0.064
    "chara_fight_fight1_32.png"
    pause 0.064
    "chara_fight_fight1_33.png"
    pause 0.064
    "chara_fight_fight1_34.png"
    pause 0.064
    "chara_fight_fight1_35.png"
    pause 0.064
    "chara_fight_fight1_36.png"
    pause 0.064
    "chara_fight_fight1_37.png"
    pause 0.064
    "chara_fight_fight1_38.png"
    pause 0.064
    "chara_fight_fight1_39.png"
    pause 0.064
    "chara_fight_fight1_40.png"
    pause 0.064
    "chara_fight_fight1_41.png"
    pause 0.064
    "chara_fight_fight1_42.png"
    pause 0.064
    "chara_fight_fight1_43.png"
    pause 0.064



image chara_fight1_effect:
    "chara_fight1_effect1.png"
    pause 1.0
    "chara_fight1_effect2.png"
    pause 0.03201
    "chara_fight1_effect3.png"
    pause 0.03201
    "chara_fight1_effect4.png"
    pause 0.03201
    "chara_fight1_effect5.png"
    pause 0.03201
    "chara_fight1_effect6.png"
    pause 0.03201
    "chara_fight1_effect7.png"
    pause 0.03201
    "chara_fight1_effect8.png"
    pause 0.03201
    "chara_fight1_effect9.png"
    pause 0.03201
    "chara_fight1_effect10.png"
    pause 0.03201
    "chara_fight1_effect1.png"


image chara_fight2_effect:
    "chara_fight2_effect1.png"
    pause 4.0
    "chara_fight2_effect2.png"
    pause 0.03201
    "chara_fight2_effect3.png"
    pause 0.03201
    "chara_fight2_effect4.png"
    pause 0.03201
    "chara_fight2_effect5.png"
    pause 0.03201
    "chara_fight2_effect6.png"
    pause 0.03201
    "chara_fight2_effect7.png"
    pause 0.03201
    "chara_fight2_effect8.png"
    pause 0.03201
    "chara_fight2_effect9.png"
    pause 0.03201
    "chara_fight2_effect10.png"
    pause 0.03201
    "chara_fight2_effect1.png"

transform fight3_xzoom:
    xzoom 1.5

image chara_fight3_effect:
    "chara_fight3_effect1.png"
    pause 1.5
    "chara_fight3_effect2.png"
    pause 0.03201
    "chara_fight3_effect3.png"
    pause 0.03201
    "chara_fight3_effect4.png"
    pause 0.03201
    "chara_fight3_effect5.png"
    pause 0.03201
    "chara_fight3_effect6.png"
    pause 0.03201
    "chara_fight3_effect7.png"
    pause 0.03201
    "chara_fight3_effect8.png"
    pause 0.03201
    "chara_fight3_effect9.png"
    pause 0.03201
    "chara_fight3_effect10.png"
    pause 0.03201
    "chara_fight3_effect1.png"

transform chara_fight_fight1_transform:
    xanchor 0.5
    yanchor 0.5
    subpixel True
    xpos store.turn_effect_source[0]
    ypos store.turn_effect_source[1]
    easeout 0.35 xpos store.turn_effect_target[0] ypos store.turn_effect_target[1]




transform chara_fight2_trans_dis:
    pause 2.9
    parallel:
        easeout 0.3 xoffset 400
    parallel:
        easeout 0.25 alpha 0.0




# Часть 1: Кадры 1-37
image Chara_fight2_anim_part1:
    "chara_fight_fight2_1.png"
    pause 0.06403
    "chara_fight_fight2_2.png"
    pause 0.06403
    "chara_fight_fight2_3.png"
    pause 0.06403
    "chara_fight_fight2_4.png"
    pause 0.06403
    "chara_fight_fight2_5.png"
    pause 0.06403
    "chara_fight_fight2_6.png"
    pause 0.06403
    "chara_fight_fight2_7.png"
    pause 0.06403
    "chara_fight_fight2_8.png"
    pause 0.06403
    "chara_fight_fight2_9.png"
    pause 0.06403
    "chara_fight_fight2_10.png"
    pause 0.06403
    "chara_fight_fight2_11.png"
    pause 0.06403
    "chara_fight_fight2_12.png"
    pause 0.06403
    "chara_fight_fight2_13.png"
    pause 0.06403
    "chara_fight_fight2_14.png"
    pause 0.06403
    "chara_fight_fight2_15.png"
    pause 0.06403
    "chara_fight_fight2_16.png"
    pause 0.06403
    "chara_fight_fight2_17.png"
    pause 0.06403
    "chara_fight_fight2_18.png"
    pause 0.06403
    "chara_fight_fight2_19.png"
    pause 0.06403
    "chara_fight_fight2_20.png"
    pause 0.06403
    "chara_fight_fight2_21.png"
    pause 0.06403
    "chara_fight_fight2_22.png"
    pause 0.06403
    "chara_fight_fight2_23.png"
    pause 0.06403
    "chara_fight_fight2_24.png"
    pause 0.06403
    "chara_fight_fight2_25.png"
    pause 0.06403
    "chara_fight_fight2_26.png"
    pause 0.801
    "chara_fight_fight2_27.png"
    pause 0.06403
    "chara_fight_fight2_28.png"
    pause 0.06403
    "chara_fight_fight2_29.png"
    pause 0.06403
    "chara_fight_fight2_30.png"
    pause 0.06403
    "chara_fight_fight2_31.png"
    pause 0.06403
    "chara_fight_fight2_32.png"
    pause 0.06403
    "chara_fight_fight2_33.png"
    pause 0.06403
    "chara_fight_fight2_34.png"
    pause 0.06403
    "chara_fight_fight2_35.png"
    pause 0.06403
    "chara_fight_fight2_36.png"
    pause 0.06403
    "chara_fight_fight2_37.png"
    pause 0.06403
    repeat False



transform chara_fight2_screen_target_trans(target_x=0, target_y=0):
    # Вторая часть находится в корне effect-экрана, поэтому получает
    # абсолютные экранные координаты выбранной цели.
    xanchor 0.5
    yanchor 0.5
    subpixel True
    xpos target_x
    ypos target_y
    xoffset -75
    alpha 0.0
    pause 3.5
    
    easein 0.4 xoffset 0 yoffset -125 alpha 1.0
    ease 0.4 xoffset 50 yoffset -140
    easeout 0.3 yoffset 0 xoffset 100
        
    pause 1.0
    parallel:
        easein 1.0 xoffset -100
    parallel:
        easein 1.5 alpha 0.0


# Часть 2: Кадры 41-102
image Chara_fight2_anim_part2:
    "chara_fight_fight2.2_1.png"
    pause 3.5
    "chara_fight_fight2.2_1.png"
    pause 0.06401
    "chara_fight_fight2.2_2.png"
    pause 0.06401
    "chara_fight_fight2.2_3.png"
    pause 0.06401
    "chara_fight_fight2.2_4.png"
    pause 0.06401
    "chara_fight_fight2.2_5.png"
    pause 0.06401
    "chara_fight_fight2.2_6.png"
    pause 0.06401
    "chara_fight_fight2.2_7.png"
    pause 0.06401
    "chara_fight_fight2.2_8.png"
    pause 0.06401
    "chara_fight_fight2.2_9.png"
    pause 0.06401
    "chara_fight_fight2.2_10.png"
    pause 0.06401
    "chara_fight_fight2.2_11.png"
    pause 0.06401
    "chara_fight_fight2.2_12.png"
    pause 0.06401
    "chara_fight_fight2.2_13.png"
    pause 0.06401
    "chara_fight_fight2.2_14.png"
    pause 0.06401
    "chara_fight_fight2.2_15.png"
    pause 0.06401
    "chara_fight_fight2.2_16.png"
    pause 0.06401
    "chara_fight_fight2.2_17.png"
    pause 0.06401
    "chara_fight_fight2.2_18.png"
    pause 0.06401
    "chara_fight_fight2.2_19.png"
    pause 0.06401
    "chara_fight_fight2.2_20.png"
    pause 0.06401
    "chara_fight_fight2.2_21.png"
    pause 0.06401
    "chara_fight_fight2.2_22.png"
    pause 0.06401
    "chara_fight_fight2.2_23.png"
    pause 0.06401
    "chara_fight_fight2.2_24.png"
    pause 0.06401
    "chara_fight_fight2.2_25.png"
    pause 0.06401
    "chara_fight_fight2.2_26.png"
    pause 0.06401
    "chara_fight_fight2.2_27.png"
    pause 0.06401
    "chara_fight_fight2.2_28.png"
    pause 0.06401
    "chara_fight_fight2.2_29.png"
    pause 0.06401
    "chara_fight_fight2.2_30.png"
    pause 0.06401
    "chara_fight_fight2.2_31.png"
    pause 0.06401
    "chara_fight_fight2.2_32.png"
    pause 0.06401
    "chara_fight_fight2.2_33.png"
    pause 0.06401
    "chara_fight_fight2.2_34.png"
    pause 0.06401
    "chara_fight_fight2.2_35.png"
    pause 0.06401
    "chara_fight_fight2.2_37.png"
    pause 0.06401
    "chara_fight_fight2.2_38.png"
    pause 0.06401
    "chara_fight_fight2.2_39.png"
    pause 0.06401
    "chara_fight_fight2.2_40.png"
    pause 0.06401
    "chara_fight_fight2.2_41.png"
    pause 0.06401
    "chara_fight_fight2.2_42.png"
    pause 0.06401
    "chara_fight_fight2.2_43.png"
    pause 0.06401
    "chara_fight_fight2.2_44.png"
    pause 0.06401
    "chara_fight_fight2.2_45.png"
    pause 0.06401
    "chara_fight_fight2.2_46.png"
    pause 0.06401
    "chara_fight_fight2.2_47.png"
    pause 0.06401
    "chara_fight_fight2.2_48.png"
    pause 0.06401
    "chara_fight_fight2.2_49.png"
    pause 0.06401
    "chara_fight_fight2.2_50.png"
    pause 0.06401
    "chara_fight_fight2.2_51.png"
    pause 0.06401
    "chara_fight_fight2.2_52.png"
    pause 0.06401
    "chara_fight_fight2.2_53.png"
    pause 0.06401
    "chara_fight_fight2.2_54.png"
    pause 0.06401
    "chara_fight_fight2.2_55.png"
    pause 0.06401
    "chara_fight_fight2.2_56.png"
    pause 0.06401
    "chara_fight_fight2.2_57.png"
    pause 0.06401
    "chara_fight_fight2.2_58.png"
    pause 0.06401
    "chara_fight_fight2.2_59.png"
    pause 0.06401
    "chara_fight_fight2.2_60.png"
    pause 0.06401
    "chara_fight_fight2.2_61.png"
    pause 0.06401
    repeat False











image Chara_fight3_anim_part1:
    "chara_fight3_part1_1.png"
    pause 0.06401
    "chara_fight3_part1_2.png"
    pause 0.06401
    "chara_fight3_part1_3.png"
    pause 0.06401
    "chara_fight3_part1_4.png"
    pause 0.06401
    "chara_fight3_part1_5.png"
    pause 0.06401
    "chara_fight3_part1_6.png"
    pause 0.06401
    "chara_fight3_part1_7.png"
    pause 0.06401
    "chara_fight3_part1_8.png"
    pause 0.06401
    "chara_fight3_part1_9.png"
    pause 0.06401
    "chara_fight3_part1_10.png"
    pause 0.06401
    "chara_fight3_part1_11.png"
    pause 0.06401
    "chara_fight3_part1_12.png"
    pause 0.06401
    "chara_fight3_part1_13.png"
    pause 0.06401
    repeat False




image Chara_fight3_anim_part2:
    "chara_fight3_part2_1.png"
    pause 1.5
    "chara_fight3_part2_1.png"
    pause 0.06401
    "chara_fight3_part2_2.png"
    pause 0.06401
    "chara_fight3_part2_3.png"
    pause 0.06401
    "chara_fight3_part2_4.png"
    pause 0.06401
    "chara_fight3_part2_5.png"
    pause 1.0
    "chara_fight3_part2_6.png"
    pause 0.08401
    "chara_fight3_part2_7.png"
    pause 0.08401
    "chara_fight3_part2_8.png"
    pause 0.12401
    "chara_fight3_part2_9.png"
    pause 0.12401
    "chara_fight3_part2_10.png"
    pause 0.12401
    "chara_fight3_part2_11.png"
    pause 0.12401
    "chara_fight3_part2_12.png"
    pause 0.08401
    "chara_fight3_part2_13.png"
    pause 0.08401
    "chara_fight3_part2_14.png"
    pause 0.08401
    "chara_fight3_part2_15.png"
    pause 0.08401
    "chara_fight3_part2_16.png"
    pause 0.08401
    "chara_fight3_part2_17.png"
    pause 0.08401
    "chara_fight3_part2_18.png"
    pause 0.08401
    "chara_fight3_part2_19.png"
    pause 0.08401
    repeat False










transform chara_fight3_trans_dis:
    pause 1.0
    parallel:
        easeout 0.3 xoffset 300
    parallel:
        easeout 0.25 alpha 0.0


transform trans_checked:
    ease 0.5 xoffset -120 alpha 0.0


transform darker_trans:
    matrixcolor BrightnessMatrix(-0.5)  # или любой другой эффект затемнения
    xalign 0.5 yalign 0.5

transform chara_fight3_screen_target_trans(target_x=0, target_y=0):
    # Вторая часть находится в корне effect-экрана, поэтому получает
    # абсолютные экранные координаты выбранной цели.
    xanchor 0.5
    yanchor 0.5
    subpixel True
    xpos target_x
    ypos target_y
    xoffset -60
    alpha 0.0
    pause 1.5
    easeout 0.25 xoffset 100 alpha 1.0
    ease 0.3 xoffset 150
    pause 1.9
    ease 0.5 xoffset -30 alpha 0.0


transform chara_atk3_prog_10:
    zoom 1.0
    easein 0.2 zoom 1.5
    easeout 0.5 zoom 1.2

transform chara_atk3_prog_20:
    zoom 1.2
    easein 0.2 zoom 1.7
    easeout 0.5 zoom 1.4

transform chara_atk3_prog_30:
    zoom 1.4
    easein 0.2 zoom 1.9
    easeout 0.5 zoom 1.6

transform chara_atk3_prog_40:
    zoom 1.6
    easein 0.2 zoom 2.1
    easeout 0.5 zoom 1.8

transform chara_atk3_prog_50:
    zoom 1.8
    easein 0.2 zoom 2.3
    easeout 0.5 zoom 2.0

transform chara_atk3_prog_60:
    zoom 2.0
    easein 0.2 zoom 2.5
    easeout 0.5 zoom 2.2

transform chara_atk3_prog_70:
    zoom 2.2
    easein 0.2 zoom 2.7
    easeout 0.5 zoom 2.4

transform chara_atk3_prog_80:
    zoom 2.4
    easein 0.2 zoom 2.9
    easeout 0.5 zoom 2.6

transform chara_atk3_prog_85:
    zoom 2.6
    easein 0.2 zoom 3.1
    easeout 0.5 zoom 2.8

transform chara_atk3_prog_90:
    zoom 2.8
    easein 0.2 zoom 3.3
    easeout 0.5 zoom 3.0

transform chara_atk3_prog_95:
    zoom 3.0
    easein 0.2 zoom 3.5
    easeout 0.5 zoom 3.2

transform chara_atk3_prog_100:
    zoom 3.2
    easein 0.2 zoom 3.7
    easeout 0.5 zoom 3.4










image Chara_atk1_anim:
    "Charaatk1.png"
    xoffset 0
    easeout 0.12 xoffset 42
    easein 0.18 xoffset 0

# 36 — Удар ножом
image Chara_atk2_anim:
    "Charaatk1.png"
    xoffset 0
    rotate 0
    easeout 0.10 xoffset 55 rotate 7
    easein 0.16 xoffset 0 rotate 0

# 37 — Удар шпагой
image Chara_atk3_anim:
    "Charaatk1.png"
    xoffset 0
    zoom 1.0
    easeout 0.14 xoffset 70 zoom 1.05
    easein 0.20 xoffset 0 zoom 1.0

# Спрайты Чары для анимации ударов 1/2/3 (Удар бунтарки / Удар ножом / Удар шпагой),
# построенные по образу fight1 Криса и использующие те же transform'ы.
# Сейчас алиасуются на существующие кадры chara_fight_fight1_*; при наличии
# выделенных ассетов (chara_down_fight1_*.png / chara_up_fight1_*.png) замените ими.


image Chara_up_fight1_anim_part1:
    "chara_fight_fight1_1.png"
    pause 0.105
    "chara_fight_fight1_2.png"
    pause 0.105
    "chara_fight_fight1_3.png"
    pause 0.105
    "chara_fight_fight1_4.png"
    pause 0.105
    "chara_fight_fight1_5.png"
    pause 0.105
    "chara_fight_fight1_6.png"
    pause 0.105
    "chara_fight_fight1_7.png"
    pause 0.105
    "chara_fight_fight1_8.png"

transform chara_fight1_trans_dis:
    easeout 1.5 alpha 0.0



transform chara_fight1_screen_target_trans(target_x=0, target_y=0):
    # Вторая часть находится в корне effect-экрана, поэтому получает
    # абсолютные экранные координаты выбранной цели.
    xanchor 0.5
    yanchor 0.5
    subpixel True
    xpos target_x
    ypos target_y
    xoffset -200
    alpha 0.0
    easein 0.4 alpha 1.0
    pause 0.01
    parallel:
        easeout 0.9 xoffset 100 yoffset -100 alpha 1.0 
    parallel:
        pause 0.6
        easeout 0.3 yoffset 10
        
    pause 1.0
    parallel:
        easein 1.0 xoffset -100
    parallel:
        easein 1.5 alpha 0.0







image Chara_up_fight1_anim_part2:
    pause 0.55
    "chara_fight_fight1_8.png"
    pause 0.05011
    "chara_fight_fight1_9.png"
    pause 0.05011
    "chara_fight_fight1_10.png"
    pause 0.05011
    "chara_fight_fight1_11.png"
    pause 0.05011
    "chara_fight_fight1_12.png"
    pause 0.05011
    "chara_fight_fight1_13.png"
    pause 0.05011
    "chara_fight_fight1_14.png"
    pause 0.05011
    "chara_fight_fight1_15.png"
    pause 0.05011
    "chara_fight_fight1_16.png"
    pause 0.05011
    "chara_fight_fight1_17.png"
    pause 0.05011
    "chara_fight_fight1_18.png"
    pause 0.05011
    "chara_fight_fight1_19.png"
    pause 0.05011
    "chara_fight_fight1_20.png"
    pause 0.05011
    "chara_fight_fight1_21.png"
    pause 0.05011
    "chara_fight_fight1_22.png"
    pause 0.05011
    "chara_fight_fight1_23.png"
    pause 0.05011
    "chara_fight_fight1_24.png"
    pause 0.05011
    "chara_fight_fight1_25.png"
    pause 0.05011
    "chara_fight_fight1_26.png"
    pause 0.05011
    "chara_fight_fight1_27.png"
    pause 1.0
    "chara_fight_fight1_28.png"
    pause 0.1601
    "chara_fight_fight1_29.png"
    pause 0.1601
    "chara_fight_fight1_30.png"
    pause 0.1601
    "chara_fight_fight1_31.png"
    pause 0.1601
    "chara_fight_fight1_32.png"
    pause 0.1601
    "chara_fight_fight1_33.png"
    pause 0.1601
    "chara_fight_fight1_34.png"
    pause 0.1601
    "chara_fight_fight1_35.png"
    pause 0.1601
    "chara_fight_fight1_36.png"
    pause 0.1601
    "chara_fight_fight1_37.png"
    pause 0.1601
    "chara_fight_fight1_38.png"
    pause 0.1601
    "chara_fight_fight1_39.png"
    pause 0.1601
    "chara_fight_fight1_40.png"
    pause 0.1601
    "chara_fight_fight1_41.png"

# 38 — Удар из-за спины
image Chara_atk4_anim:
    "Charaatk1.png"
    alpha 1.0
    xoffset -35
    ease 0.10 alpha 0.15
    xoffset 65
    ease 0.10 alpha 1.0
    easein 0.18 xoffset 0

# 39 — Решето
image Chara_atk5_anim:
    "Charaatk1.png"
    xoffset 0
    linear 0.06 xoffset 35
    linear 0.06 xoffset 5
    linear 0.06 xoffset 45
    linear 0.06 xoffset 0

# 40 — Ножевой снаряд
image Chara_atk6_anim:
    "Charaatk1.png"
    alpha 1.0
    xoffset 0
    easeout 0.22 xoffset 90 alpha 0.25
    alpha 1.0
    xoffset 0

# 41 — Реки крови
image Chara_atk7_anim:
    "Charaatk1.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.12 matrixcolor TintMatrix("#ff3030") zoom 1.07
    ease 0.18 matrixcolor TintMatrix("#ffffff") zoom 1.0
    repeat

# MAGIC 42–47

# 42 — Гнев
image Chara_mag1_anim:
    "Kris_pisya3.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.18 matrixcolor TintMatrix("#ff5038") zoom 1.05
    ease 0.22 matrixcolor TintMatrix("#ffffff") zoom 1.0
    repeat

# 43 — Безумие
image Chara_mag2_anim:
    "Kris_pisya3.png"
    rotate 0
    matrixcolor TintMatrix("#ffffff")
    ease 0.12 rotate -3 matrixcolor TintMatrix("#d659ff")
    ease 0.12 rotate 3 matrixcolor TintMatrix("#ff4f84")
    ease 0.12 rotate 0 matrixcolor TintMatrix("#ffffff")
    repeat

# 44 — Сумасшествие
image Chara_mag3_anim:
    "Kris_pisya3.png"
    xoffset 0
    matrixcolor TintMatrix("#ffffff")
    linear 0.07 xoffset -5 matrixcolor TintMatrix("#ff3030")
    linear 0.07 xoffset 5 matrixcolor TintMatrix("#7f30ff")
    linear 0.07 xoffset 0 matrixcolor TintMatrix("#ffffff")
    repeat

# 45 — Психоз
image Chara_mag4_anim:
    "Kris_pisya3.png"
    alpha 1.0
    matrixcolor SaturationMatrix(1.0)
    ease 0.14 alpha 0.55 matrixcolor SaturationMatrix(0.0)
    ease 0.14 alpha 1.0 matrixcolor SaturationMatrix(1.0)
    repeat

# 46 — Моральное разложение
image Chara_mag5_anim:
    "Kris_pisya3.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.22 matrixcolor TintMatrix("#71345f") yoffset 3
    ease 0.22 matrixcolor TintMatrix("#ffffff") yoffset 0
    repeat

# 47 — Пробуждение прошлого
image Chara_mag6_anim:
    "Charaatk1.png"
    alpha 0.35
    zoom 0.92
    matrixcolor TintMatrix("#ff2020")
    ease 0.30 alpha 1.0 zoom 1.10 matrixcolor TintMatrix("#ffffff")
    ease 0.18 zoom 1.0

# У Чары её state пока не устанавливается в лейблах атак и магии.
# Поэтому уникальные действия переключаются по attackindex, а общие
# состояния — по полям самого персонажа.
image chara_fight_act:
    "chara_fight_act1.png"
    pause 0.064
    "chara_fight_act2.png"
    pause 0.064
    "chara_fight_act3.png"
    pause 0.064
    "chara_fight_act4.png"
    pause 0.064
    "chara_fight_act5.png"
    pause 0.064
    "chara_fight_act6.png"
    pause 0.064
    "chara_fight_act7.png"
    pause 0.064
    "chara_fight_act8.png"
    pause 0.064
    "chara_fight_act9.png"
    pause 0.064
    "chara_fight_act10.png"
    pause 0.064
    "chara_fight_act11.png"
    pause 0.064
    "chara_fight_act12.png"
    pause 0.064
    "chara_fight_act13.png"
    pause 0.064
    "chara_fight_act14.png"
    pause 0.064
    "chara_fight_act15.png"
    pause 0.064
    "chara_fight_act16.png"
    pause 0.064
    "chara_fight_act17.png"
    pause 0.064
    "chara_fight_act18.png"
    pause 0.064
    "chara_fight_act19.png"
    pause 0.064
    "chara_fight_act20.png"
    pause 0.064
    "chara_fight_act21.png"
    pause 0.064
    "chara_fight_act22.png"
    pause 0.064
    "chara_fight_act23.png"
    pause 0.064



image chara_fight_act2:
    "chara_fight_act24.png"
    pause 0.064
    "chara_fight_act25.png"
    pause 0.064
    "chara_fight_act26.png"
    pause 0.064
    "chara_fight_act27.png"
    pause 0.064
    "chara_fight_act28.png"
    pause 0.064
    "chara_fight_act29.png"
    pause 0.064
    "chara_fight_act30.png"
    pause 0.064
    "chara_fight_act31.png"
    pause 0.064
    "chara_fight_act32.png"
    pause 0.064
    "chara_fight_act33.png"
    pause 0.064
    "chara_fight_act34.png"
    pause 0.064
    "chara_fight_act35.png"
    pause 0.064
    "chara_fight_act36.png"
    pause 0.064
    "chara_fight_act37.png"
    pause 0.064
    "chara_fight_act38.png"
    pause 0.064
    "chara_fight_act39.png"
    pause 0.064
    "chara_fight_act40.png"
    pause 0.064
    "chara_fight_act41.png"
    pause 0.064
    "chara_fight_act42.png"
    pause 0.064
    "chara_fight_act43.png"
    pause 0.064
    "chara_fight_act44.png"
    pause 0.064
    "chara_fight_act45.png"
    pause 0.064

image chara_fight_item:
    "chara_fight_item1.png"
    pause 0.064
    "chara_fight_item2.png"
    pause 0.064
    "chara_fight_item3.png"
    pause 0.064
    "chara_fight_item4.png"
    pause 0.064
    "chara_fight_item5.png"
    pause 0.064
    "chara_fight_item6.png"
    pause 0.064
    "chara_fight_item7.png"
    pause 0.064
    "chara_fight_item8.png"
    pause 0.064
    "chara_fight_item9.png"
    pause 0.064
    "chara_fight_item10.png"
    pause 0.064
    "chara_fight_item11.png"
    pause 0.064
    "chara_fight_item12.png"
    pause 0.064
    "chara_fight_item13.png"
    pause 0.064
    "chara_fight_item14.png"
    

image chara_fight_item2:
    "chara_fight_item20.png"
    pause 0.038
    "chara_fight_item21.png"
    pause 0.038
    "chara_fight_item22.png"
    pause 0.038
    "chara_fight_item23.png"
    pause 0.038
    "chara_fight_item24.png"
    pause 0.038
    "chara_fight_item25.png"
    pause 0.038
    "chara_fight_item26.png"
    pause 0.038
    "chara_fight_item27.png"
    pause 0.038
    "chara_fight_item28.png"
    pause 0.038
    "chara_fight_item29.png"
    pause 0.038
    "chara_fight_item30.png"
    pause 0.038
    "chara_fight_item31.png"
    pause 0.038
    "chara_fight_item32.png"
    pause 0.038
    "chara_fight_item33.png"
    pause 0.038
    "chara_fight_item34.png"
    pause 0.038
    "chara_fight_item35.png"
    pause 0.038
    "chara_fight_item36.png"
    pause 0.038
    "chara_fight_item37.png"
    pause 0.038
    "chara_fight_item38.png"
    pause 0.038
    "chara_fight_item39.png"
    pause 0.038
    "chara_fight_item40.png"


image chara_gnev_anim:
    "chara_gnev_1.png"
    pause 0.064
    "chara_gnev_2.png"
    pause 0.064
    "chara_gnev_3.png"
    pause 0.064
    "chara_gnev_4.png"
    pause 0.064
    "chara_gnev_5.png"
    pause 0.064
    "chara_gnev_6.png"
    pause 0.064
    "chara_gnev_7.png"
    pause 0.064
    "chara_gnev_8.png"
    pause 0.064
    "chara_gnev_9.png"
    pause 0.064
    "chara_gnev_10.png"
    pause 0.064
    "chara_gnev_11.png"
    pause 0.064
    "chara_gnev_12.png"
    pause 0.064
    "chara_gnev_13.png"
    pause 0.064
    "chara_gnev_14.png"
    pause 0.064
    "chara_gnev_15.png"
    pause 0.064
    "chara_gnev_16.png"
    pause 0.064
    "chara_gnev_17.png"
    pause 0.064
    "chara_gnev_18.png"
    pause 0.064
    "chara_gnev_19.png"
    pause 0.064
    "chara_gnev_20.png"
    pause 0.064
    "chara_gnev_21.png"
    pause 0.064
    "chara_gnev_22.png"
    pause 0.064
    "chara_gnev_23.png"
    pause 0.064
    "chara_gnev_24.png"
    pause 0.064
    "chara_gnev_25.png"
    pause 0.064
    "chara_gnev_26.png"
    pause 0.064
    "chara_gnev_27.png"
    pause 0.064
    "chara_gnev_28.png"
    pause 0.064
    "chara_gnev_29.png"
    pause 0.064
    "chara_gnev_30.png"
    pause 0.064
    "chara_gnev_31.png"
    pause 0.064
    "chara_gnev_32.png"
    pause 0.064
    "chara_gnev_33.png"
    pause 0.064
    "chara_gnev_34.png"
    pause 0.064
    "chara_gnev_35.png"
    pause 0.064
    "chara_gnev_36.png"
    pause 0.1281
    "chara_gnev_37.png"
    pause 0.1281
    "chara_gnev_38.png"
    pause 0.1281
    "chara_gnev_39.png"
    pause 0.1281
    "chara_gnev_40.png"
    pause 0.1281


image chara_fight_magic1:
    "chara_fight_magic1_1.png"
    pause 0.064
    "chara_fight_magic1_2.png"
    pause 0.064
    "chara_fight_magic1_3.png"
    pause 0.064
    "chara_fight_magic1_4.png"
    pause 0.064
    "chara_fight_magic1_5.png"
    pause 0.064
    "chara_fight_magic1_6.png"
    pause 0.064
    "chara_fight_magic1_7.png"
    pause 0.064
    "chara_fight_magic1_8.png"
    pause 0.064
    "chara_fight_magic1_9.png"
    pause 0.064
    "chara_fight_magic1_10.png"
    pause 0.064
    "chara_fight_magic1_11.png"
    pause 0.064
    "chara_fight_magic1_12.png"
    pause 0.064
    "chara_fight_magic1_13.png"
    pause 0.064
    "chara_fight_magic1_14.png"
    pause 0.064
    "chara_fight_magic1_15.png"
    pause 0.064
    "chara_fight_magic1_16.png"
    pause 0.064
    "chara_fight_magic1_17.png"
    pause 0.064
    "chara_fight_magic1_18.png"
    pause 0.064
    "chara_fight_magic1_19.png"
    pause 0.064
    "chara_fight_magic1_20.png"
    pause 0.064
    "chara_fight_magic1_21.png"
    pause 0.064
    "chara_fight_magic1_22.png"
    pause 0.064
    "chara_fight_magic1_23.png"
    pause 0.064
    "chara_fight_magic1_24.png"
    pause 0.064
    "chara_fight_magic1_25.png"
    pause 0.064
    "chara_fight_magic1_26.png"
    pause 0.064
    "chara_fight_magic1_27.png"
    pause 0.064
    "chara_fight_magic1_28.png"
    pause 0.064
    "chara_fight_magic1_29.png"
    pause 0.064
    "chara_fight_magic1_30.png"
    pause 0.064
    "chara_fight_magic1_31.png"
    pause 0.064
    "chara_fight_magic1_32.png"
    pause 0.064
    "chara_fight_magic1_33.png"
    pause 0.064
    "chara_fight_magic1_34.png"
    pause 0.064
    "chara_fight_magic1_35.png"
    pause 0.064
    "chara_fight_magic1_36.png"
    pause 0.064
    "chara_fight_magic1_37.png"
    pause 0.064
    "chara_fight_magic1_38.png"
    pause 0.064
    "chara_fight_magic1_39.png"
    pause 0.064
    "chara_fight_magic1_40.png"
    pause 0.064
    "chara_fight_magic1_41.png"
    pause 0.064
    "chara_fight_magic1_42.png"
    pause 0.064

image chara_fight_fight2:
    "chara_fight_fight2_1.png"
    pause 0.064
    "chara_fight_fight2_2.png"
    pause 0.064
    "chara_fight_fight2_3.png"
    pause 0.064
    "chara_fight_fight2_4.png"
    pause 0.064
    "chara_fight_fight2_5.png"
    pause 0.064
    "chara_fight_fight2_6.png"
    pause 0.064
    "chara_fight_fight2_7.png"
    pause 0.064
    "chara_fight_fight2_8.png"
    pause 0.064
    "chara_fight_fight2_9.png"
    pause 0.064
    "chara_fight_fight2_10.png"
    pause 0.064
    "chara_fight_fight2_11.png"
    pause 0.064
    "chara_fight_fight2_12.png"
    pause 0.064
    "chara_fight_fight2_13.png"
    pause 0.064
    "chara_fight_fight2_14.png"
    pause 0.064
    "chara_fight_fight2_15.png"
    pause 0.064
    "chara_fight_fight2_16.png"
    pause 0.064
    "chara_fight_fight2_17.png"
    pause 0.064
    "chara_fight_fight2_18.png"
    pause 0.064
    "chara_fight_fight2_19.png"
    pause 0.064
    "chara_fight_fight2_20.png"
    pause 0.064
    "chara_fight_fight2_21.png"
    pause 0.064
    "chara_fight_fight2_22.png"
    pause 0.064
    "chara_fight_fight2_23.png"
    pause 0.064
    "chara_fight_fight2_24.png"
    pause 0.064
    "chara_fight_fight2_25.png"
    pause 0.064
    "chara_fight_fight2_26.png"
    pause 0.064
    "chara_fight_fight2_27.png"
    pause 0.064
    "chara_fight_fight2_28.png"
    pause 0.064
    "chara_fight_fight2_29.png"
    pause 0.064
    "chara_fight_fight2_30.png"
    pause 0.064
    "chara_fight_fight2_31.png"
    pause 0.064
    "chara_fight_fight2_32.png"
    pause 0.064
    "chara_fight_fight2_33.png"
    pause 0.064
    "chara_fight_fight2_34.png"
    pause 0.064
    "chara_fight_fight2_35.png"
    pause 0.064
    "chara_fight_fight2_36.png"
    pause 0.064
    "chara_fight_fight2_37.png"
    pause 0.064
    "chara_fight_fight2_38.png"
    pause 0.064
    "chara_fight_fight2_39.png"
    pause 0.064
    "chara_fight_fight2_40.png"
    pause 0.064
    "chara_fight_fight2_41.png"
    pause 0.064
    "chara_fight_fight2_42.png"
    pause 0.064
    "chara_fight_fight2_43.png"
    pause 0.064
    "chara_fight_fight2_44.png"
    pause 0.064
    "chara_fight_fight2_45.png"
    pause 0.064
    "chara_fight_fight2_46.png"
    pause 0.064
    "chara_fight_fight2_47.png"
    pause 0.064
    "chara_fight_fight2_48.png"
    pause 0.064
    "chara_fight_fight2_49.png"
    pause 0.064
    "chara_fight_fight2_50.png"
    pause 0.064
    "chara_fight_fight2_51.png"
    pause 0.064
    "chara_fight_fight2_52.png"
    pause 0.064
    "chara_fight_fight2_53.png"
    pause 0.064
    "chara_fight_fight2_54.png"
    pause 0.064
    "chara_fight_fight2_55.png"
    pause 0.064
    "chara_fight_fight2_56.png"
    pause 0.064
    "chara_fight_fight2_57.png"
    pause 0.064
    "chara_fight_fight2_58.png"
    pause 0.064
    "chara_fight_fight2_59.png"
    pause 0.064
    "chara_fight_fight2_60.png"
    pause 0.064
    "chara_fight_fight2_61.png"
    pause 0.064
    "chara_fight_fight2_62.png"
    pause 0.064
    "chara_fight_fight2_63.png"
    pause 0.064
    "chara_fight_fight2_64.png"
    pause 0.064
    "chara_fight_fight2_65.png"
    pause 0.064
    "chara_fight_fight2_66.png"
    pause 0.064
    "chara_fight_fight2_67.png"
    pause 0.064
    "chara_fight_fight2_68.png"
    pause 0.064
    "chara_fight_fight2_69.png"
    pause 0.064
    "chara_fight_fight2_70.png"
    pause 0.064
    "chara_fight_fight2_71.png"
    pause 0.064
    "chara_fight_fight2_72.png"
    pause 0.064
    "chara_fight_fight2_73.png"
    pause 0.064
    "chara_fight_fight2_74.png"
    pause 0.064
    "chara_fight_fight2_75.png"
    pause 0.064
    "chara_fight_fight2_76.png"
    pause 0.064
    "chara_fight_fight2_77.png"
    pause 0.064
    "chara_fight_fight2_78.png"
    pause 0.064
    "chara_fight_fight2_79.png"
    pause 0.064
    "chara_fight_fight2_80.png"
    pause 0.064
    "chara_fight_fight2_81.png"
    pause 0.064
    "chara_fight_fight2_82.png"
    pause 0.064
    "chara_fight_fight2_83.png"
    pause 0.064
    "chara_fight_fight2_84.png"
    pause 0.064
    "chara_fight_fight2_85.png"
    pause 0.064
    "chara_fight_fight2_86.png"
    pause 0.064
    "chara_fight_fight2_87.png"
    pause 0.064
    "chara_fight_fight2_88.png"
    pause 0.064
    "chara_fight_fight2_89.png"
    pause 0.064
    "chara_fight_fight2_90.png"
    pause 0.064
    "chara_fight_fight2_91.png"
    pause 0.064
    "chara_fight_fight2_92.png"
    pause 0.064
    "chara_fight_fight2_93.png"
    pause 0.064
    "chara_fight_fight2_94.png"
    pause 0.064
    "chara_fight_fight2_95.png"
    pause 0.064
    "chara_fight_fight2_96.png"
    pause 0.064
    "chara_fight_fight2_97.png"
    pause 0.064
    "chara_fight_fight2_98.png"
    pause 0.064
    "chara_fight_fight2_99.png"
    pause 0.064
    "chara_fight_fight2_100.png"
    pause 0.064
    "chara_fight_fight2_101.png"
    pause 0.064
    "chara_fight_fight2_102.png"
    pause 0.064

image chara_fight_fight3:
    "chara_fight_fight3_1.png"
    pause 0.064
    "chara_fight_fight3_2.png"
    pause 0.064
    "chara_fight_fight3_3.png"
    pause 0.064
    "chara_fight_fight3_4.png"
    pause 0.064
    "chara_fight_fight3_5.png"
    pause 0.064
    "chara_fight_fight3_6.png"
    pause 0.064
    "chara_fight_fight3_7.png"
    pause 0.064
    "chara_fight_fight3_8.png"
    pause 0.064
    "chara_fight_fight3_9.png"
    pause 0.064
    "chara_fight_fight3_10.png"
    pause 0.064
    "chara_fight_fight3_11.png"
    pause 0.064
    "chara_fight_fight3_12.png"
    pause 0.064
    "chara_fight_fight3_13.png"
    pause 0.064
    "chara_fight_fight3_14.png"
    pause 0.064
    "chara_fight_fight3_15.png"
    pause 0.064
    "chara_fight_fight3_16.png"
    pause 0.064
    "chara_fight_fight3_17.png"
    pause 0.064
    "chara_fight_fight3_18.png"
    pause 0.064
    "chara_fight_fight3_19.png"
    pause 0.064
    "chara_fight_fight3_20.png"
    pause 0.064
    "chara_fight_fight3_21.png"
    pause 0.064
    "chara_fight_fight3_22.png"
    pause 0.064
    "chara_fight_fight3_23.png"
    pause 0.064
    "chara_fight_fight3_24.png"
    pause 0.064
    "chara_fight_fight3_25.png"
    pause 0.064
    "chara_fight_fight3_26.png"
    pause 0.064
    "chara_fight_fight3_27.png"
    pause 0.064
    "chara_fight_fight3_28.png"
    pause 0.064
    "chara_fight_fight3_29.png"
    pause 0.064
    "chara_fight_fight3_30.png"
    pause 0.064
    "chara_fight_fight3_31.png"
    pause 0.064
    "chara_fight_fight3_32.png"
    pause 0.064

image Charafightsprite = ConditionSwitch(

    # FALLEN / DEAD
    "store.pers_dict['Чара'].prone_debuff > 0 or store.pers_dict['Чара'].current_hp <= 0", At("chara_fight_fall.png", Hero_damaged_trans),

    # FIGHT BEGUN
    "store.pers_dict['Чара'].state == 'fight_begun_state'", "Chara_fight_begun_anim",

    # ACT
    "store.pers_dict['Чара'].state == 'act'", "chara_fight_act",

    # ACT2
    "store.pers_dict['Чара'].state == 'act2'", "chara_fight_act2",

    # HEALED + ITEM
    "store.pers_dict['Чара'].damage_gain_for_vis <= -2 and store.pers_dict['Чара'].state == 'item'", At("chara_fight_item15.png", Hero_healed_trans),

    # ITEM
    "store.pers_dict['Чара'].state == 'item'", "chara_fight_item",

    # ITEM2
    "store.pers_dict['Чара'].state == 'item2'", "chara_fight_item2",

    # DAMAGED / HEALED
    "store.pers_dict['Чара'].damage_gain_for_vis >= 10 and store.pers_dict['Чара'].state != 'item'", At("chara_fight_damaged.png", Hero_damaged_trans),
    "store.pers_dict['Чара'].damage_gain_for_vis <= -2", At("Chara_idle_up_anim", Hero_healed_trans),

    # DEFEND
    "store.pers_dict['Чара'].state == 'defend'", "Chara_defend_up_anim",

    # ATTACKS
    "store.pers_dict['Чара'].state == 'fight1'", At("Kris_idle_up_none_anim", falsh),

    "store.pers_dict['Чара'].state == 'fight2'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Чара'].state == 'fight3'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Чара'].state == 'fight4'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Чара'].state == 'fight5'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Чара'].state == 'fight6'", At("Kris_idle_up_none_anim", falsh),
    "store.pers_dict['Чара'].state == 'fight7'", At("Kris_idle_up_none_anim", falsh),

    # MAGIC
    "store.pers_dict['Чара'].state == 'magic1'", "chara_gnev_anim",
    "store.pers_dict['Чара'].state == 'magic2'", "chara_fight_magic1",
    "store.pers_dict['Чара'].state == 'magic3'", "Chara_mag3_anim",
    "store.pers_dict['Чара'].state == 'magic4'", "Chara_mag4_anim",
    "store.pers_dict['Чара'].state == 'magic5'", "Chara_mag5_anim",
    "store.pers_dict['Чара'].state == 'magic6'", "Chara_mag6_anim",

    # IDLE / FALLBACK
    "True", "Chara_idle_up_anim"
)

# АЗРИЕЛЬ
# Доступные боевые изображения: asriel s.png, asriel_down1.png и Asrielatk1.png.

image Asriel_idle_up_anim:
    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    pause 0.2
    repeat

image Asriel_idle_down_anim:
    "asriel_down1.png"
    pause 0.45
    yoffset -2
    pause 0.15
    yoffset 0
    repeat

image Asriel_dead_up_anim:
    "asriel s.png"
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.35)
    alpha 0.75

image Asriel_dead_down_anim:
    "asriel_down1.png"
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.35)
    alpha 0.75

image Asriel_defend_up_anim:
    "asriel s.png"
    ease 0.15 zoom 0.94 xoffset -4
    ease 0.20 zoom 1.0 xoffset 0
    repeat

image Asriel_defend_down_anim:
    "asriel_down1.png"
    ease 0.15 zoom 0.94 xoffset -4
    ease 0.20 zoom 1.0 xoffset 0
    repeat

# Атаки 21–24
image Asriel_atk1_anim:
    "Asrielatk1.png"
    easeout 0.12 xoffset 42
    easein 0.18 xoffset 0

image Asriel_atk2_anim:
    "Asrielatk1.png"
    easeout 0.10 xoffset 55 rotate 7
    easein 0.16 xoffset 0 rotate 0

image Asriel_atk3_anim:
    "Asrielatk1.png"
    easeout 0.14 xoffset 65 zoom 1.05
    easein 0.20 xoffset 0 zoom 1.0

image Asriel_atk4_anim:
    "Asrielatk1.png"
    xoffset -35
    ease 0.10 alpha 0.15
    xoffset 65
    ease 0.10 alpha 1.0
    easein 0.18 xoffset 0

# Магия 25–34
image Asriel_mag1_anim:
    "asriel s.png"
    ease 0.18 xoffset 25 zoom 1.05
    ease 0.22 xoffset 0 zoom 1.0
    repeat

image Asriel_mag2_anim:
    "asriel s.png"
    matrixcolor TintMatrix("#ff6338")
    ease 0.25 matrixcolor TintMatrix("#ffffff")
    repeat

image Asriel_mag3_anim:
    "asriel s.png"
    matrixcolor TintMatrix("#58a6ff")
    ease 0.15 yoffset -8
    ease 0.20 yoffset 0
    repeat

image Asriel_mag4_anim:
    "asriel s.png"
    rotate 0
    ease 0.12 rotate -4
    ease 0.12 rotate 4
    ease 0.12 rotate 0
    repeat

image Asriel_mag5_anim:
    "asriel s.png"
    matrixcolor TintMatrix("#d659ff")
    ease 0.22 zoom 1.08 matrixcolor TintMatrix("#ffffff")
    ease 0.22 zoom 1.0
    repeat

image Asriel_mag6_anim:
    "Asrielatk1.png"
    alpha 0.35
    zoom 0.92
    ease 0.30 alpha 1.0 zoom 1.10
    ease 0.18 zoom 1.0

image Asriel_mag7_anim:
    "asriel s.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.18 matrixcolor TintMatrix("#f1dc68") zoom 1.05
    ease 0.22 matrixcolor TintMatrix("#ffffff") zoom 1.0
    repeat

image Asriel_mag8_anim:
    "asriel s.png"
    alpha 1.0
    ease 0.12 alpha 0.45
    ease 0.12 alpha 1.0
    repeat

image Asriel_mag9_anim:
    "asriel s.png"
    matrixcolor TintMatrix("#7d5cff")
    ease 0.20 matrixcolor TintMatrix("#ffffff") yoffset -4
    ease 0.20 yoffset 0
    repeat

image Asriel_mag10_anim:
    "Asrielatk1.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.12 matrixcolor TintMatrix("#ffdf55") zoom 1.08
    ease 0.18 matrixcolor TintMatrix("#ffffff") zoom 1.0
    repeat

image Asriel_act_up_anim:
    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    pause 0.2
    repeat

image Asriel_act2_up_anim:
    "Kris_idle_up_3.png"
    pause 0.064
    "Kris_idle_up_2.png"
    pause 0.064
    "Kris_idle_up_1.png"

image Asriel_act_down_anim:
    "asriel_down1.png"
    pause 0.45
    yoffset -2
    pause 0.15
    yoffset 0
    repeat

image Asriel_act2_down_anim:
    "asriel_down1.png"

image Asriel_item_up_anim:
    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    pause 0.2
    repeat

image Asriel_item_down_anim:
    "asriel_down1.png"
    pause 0.45
    yoffset -2
    pause 0.15
    yoffset 0
    repeat

image Asriel_item2_up_anim:
    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    pause 0.2
    repeat

image Asriel_item2_down_anim:
    "asriel_down1.png"
    pause 0.45
    yoffset -2
    pause 0.15
    yoffset 0
    repeat

image Asrielfightsprite = ConditionSwitch(
    # DEAD
    "store.pers_dict['Азриель'].current_hp <= 0 and store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_dead_up_anim",
    "store.pers_dict['Азриель'].current_hp <= 0 and store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_dead_down_anim",

    # ACT
    "store.pers_dict['Азриель'].state == 'act' and store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_act_up_anim",
    "store.pers_dict['Азриель'].state == 'act' and store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_act_down_anim",

    # ACT2
    "store.pers_dict['Азриель'].state == 'act2' and store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_act2_up_anim",
    "store.pers_dict['Азриель'].state == 'act2' and store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_act2_down_anim",

    # HEALED + ITEM
    "store.pers_dict['Азриель'].damage_gain_for_vis <= -2 and store.pers_dict['Азриель'].state == 'item' and store.pers_dict['Азриель'].sprite_style == 'up'", At("Asriel_item_up_anim", Hero_healed_trans),
    "store.pers_dict['Азриель'].damage_gain_for_vis <= -2 and store.pers_dict['Азриель'].state == 'item' and store.pers_dict['Азриель'].sprite_style == 'down'", At("Asriel_item_down_anim", Hero_healed_trans),

    # DAMAGED / HEALED
    "store.pers_dict['Азриель'].damage_gain_for_vis >= 10 and store.pers_dict['Азриель'].sprite_style == 'up'", At("asriel s.png", Hero_damaged_trans),
    "store.pers_dict['Азриель'].damage_gain_for_vis >= 10 and store.pers_dict['Азриель'].sprite_style == 'down'", At("asriel_down1.png", Hero_damaged_trans),
    "store.pers_dict['Азриель'].damage_gain_for_vis <= -2 and store.pers_dict['Азриель'].sprite_style == 'up'", At("asriel s.png", Hero_healed_trans),
    "store.pers_dict['Азриель'].damage_gain_for_vis <= -2 and store.pers_dict['Азриель'].sprite_style == 'down'", At("asriel_down1.png", Hero_healed_trans),

    # ITEM
    "store.pers_dict['Азриель'].state == 'item' and store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_item_up_anim",
    "store.pers_dict['Азриель'].state == 'item' and store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_item_down_anim",

    # ITEM2
    "store.pers_dict['Азриель'].state == 'item2' and store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_item2_up_anim",
    "store.pers_dict['Азриель'].state == 'item2' and store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_item2_down_anim",

    # DEFEND
    "store.pers_dict['Азриель'].state == 'defend' and store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_defend_up_anim",
    "store.pers_dict['Азриель'].state == 'defend' and store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_defend_down_anim",

    # ATTACKS 21–24
    "store.pers_dict['Азриель'].state == 'fight1'", "Asriel_atk1_anim",
    "store.pers_dict['Азриель'].state == 'fight2'", "Asriel_atk2_anim",
    "store.pers_dict['Азриель'].state == 'fight3'", "Asriel_atk3_anim",
    "store.pers_dict['Азриель'].state == 'fight4'", "Asriel_atk4_anim",

    # MAGIC 25–34
    "store.pers_dict['Азриель'].state == 'magic1'", "Asriel_mag1_anim",
    "store.pers_dict['Азриель'].state == 'magic2'", "Asriel_mag2_anim",
    "store.pers_dict['Азриель'].state == 'magic3'", "Asriel_mag3_anim",
    "store.pers_dict['Азриель'].state == 'magic4'", "Asriel_mag4_anim",
    "store.pers_dict['Азриель'].state == 'magic5'", "Asriel_mag5_anim",
    "store.pers_dict['Азриель'].state == 'magic6'", "Asriel_mag6_anim",
    "store.pers_dict['Азриель'].state == 'magic7'", "Asriel_mag7_anim",
    "store.pers_dict['Азриель'].state == 'magic8'", "Asriel_mag8_anim",
    "store.pers_dict['Азриель'].state == 'magic9'", "Asriel_mag9_anim",
    "store.pers_dict['Азриель'].state == 'magic10'", "Asriel_mag10_anim",

    # IDLE / FALLBACK
    "store.pers_dict['Азриель'].sprite_style == 'up'", "Asriel_idle_up_anim",
    "store.pers_dict['Азриель'].sprite_style == 'down'", "Asriel_idle_down_anim",
    "True", "Asriel_idle_up_anim"
)


# ФРИСК
# Временные изображения используют PNG Криса. Имена Frisk_* оставлены
# отдельными, чтобы позднее заменить кадры без изменения Friskfightsprite.

# IDLE / COMMON STATES

image Frisk_idle_up_anim:
    "Kris_idle_up_1.png"
    pause 0.2
    "Kris_idle_up_2.png"
    pause 0.2
    "Kris_idle_up_3.png"
    pause 0.2
    "Kris_idle_up_4.png"
    pause 0.2
    "Kris_idle_up_5.png"
    pause 0.2
    repeat

image Frisk_idle_down_anim:
    "Kris_idle_down_1.png"
    pause 0.064
    "Kris_idle_down_2.png"
    pause 0.064
    "Kris_idle_down_3.png"
    pause 0.064
    "Kris_idle_down_4.png"
    pause 0.064
    "Kris_idle_down_5.png"
    pause 0.064
    repeat

image Frisk_dead_up_anim:
    "Kris_dead_up_1.png"
    pause 0.3
    "Kris_dead_up_2.png"
    pause 0.3
    repeat

image Frisk_dead_down_anim:
    "Kris_dead_down_1.png"
    pause 0.3
    "Kris_dead_down_2.png"
    pause 0.3
    repeat

image Frisk_defend_up_anim:
    "Kris_atk2_up_1.png"
    ease 0.15 zoom 0.94 xoffset -4
    ease 0.20 zoom 1.0 xoffset 0
    repeat

image Frisk_defend_down_anim:
    "Kris_atk2_down_1.png"
    ease 0.15 zoom 0.94 xoffset -4
    ease 0.20 zoom 1.0 xoffset 0
    repeat

image Frisk_act_up_anim:
    "Kris_act_up_1.png"
    pause 0.064
    "Kris_act_up_2.png"
    pause 0.064
    "Kris_act_up_3.png"
    pause 0.064
    "Kris_act_up_4.png"

image Frisk_act_down_anim:
    "Kris_act_down_1.png"
    pause 0.064
    "Kris_act_down_2.png"
    pause 0.064
    "Kris_act_down_3.png"
    pause 0.064
    "Kris_act_down_4.png"

image Frisk_item_up_anim:
    "Kris_act_up_1.png"
    pause 0.10
    "Kris_act_up_2.png"
    pause 0.10
    "Kris_act_up_3.png"

image Frisk_item_down_anim:
    "Kris_act_down_1.png"
    pause 0.10
    "Kris_act_down_2.png"
    pause 0.10
    "Kris_act_down_3.png"

image Frisk_act2_up_anim:
    "Kris_act_up_3.png"
    pause 0.064
    "Kris_act_up_2.png"
    pause 0.064
    "Kris_act_up_1.png"

image Frisk_act2_down_anim:
    "Kris_act_down_3.png"
    pause 0.064
    "Kris_act_down_2.png"
    pause 0.064
    "Kris_act_down_1.png"

image Frisk_item2_up_anim:
    "Kris_act_up_1.png"
    pause 0.10
    "Kris_act_up_2.png"
    pause 0.10
    "Kris_act_up_3.png"

image Frisk_item2_down_anim:
    "Kris_act_down_1.png"
    pause 0.10
    "Kris_act_down_2.png"
    pause 0.10
    "Kris_act_down_3.png"

# ATTACK 48 — Si vis pacem, para bellum

image Frisk_atk1_anim:
    "Kris_atk1_up_1.png"
    xoffset 0
    easeout 0.12 xoffset 55 zoom 1.05
    easein 0.18 xoffset 0 zoom 1.0

# MAGIC 49–53

image Frisk_mag1_anim:
    "Kris_idle_up_1.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.20 matrixcolor TintMatrix("#65a8ff") zoom 1.05
    ease 0.24 matrixcolor TintMatrix("#ffffff") zoom 1.0
    repeat

image Frisk_mag2_anim:
    "Kris_idle_up_1.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.18 matrixcolor TintMatrix("#ffd45c") yoffset -5
    ease 0.22 matrixcolor TintMatrix("#ffffff") yoffset 0
    repeat

image Frisk_mag3_anim:
    "Kris_idle_up_1.png"
    alpha 1.0
    ease 0.15 alpha 0.45
    ease 0.15 alpha 1.0
    repeat

image Frisk_mag4_anim:
    "Kris_idle_up_1.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.25 matrixcolor TintMatrix("#64ff8a") zoom 1.08
    ease 0.25 matrixcolor TintMatrix("#ffffff") zoom 1.0
    repeat

image Frisk_mag5_anim:
    "Kris_idle_up_1.png"
    matrixcolor TintMatrix("#ffffff")
    ease 0.18 matrixcolor TintMatrix("#ffdf55") yoffset -8
    ease 0.22 matrixcolor TintMatrix("#ffffff") yoffset 0
    repeat

image Friskfightsprite = ConditionSwitch(

    # DEAD
    "store.pers_dict['Фриск'].current_hp <= 0 and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_dead_up_anim",
    "store.pers_dict['Фриск'].current_hp <= 0 and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_dead_down_anim",

    # HEALED + ITEM
    "store.pers_dict['Фриск'].damage_gain_for_vis <= -2 and store.pers_dict['Фриск'].state == 'item' and store.pers_dict['Фриск'].sprite_style == 'up'", At("Frisk_item_up_anim", Hero_healed_trans),
    "store.pers_dict['Фриск'].damage_gain_for_vis <= -2 and store.pers_dict['Фриск'].state == 'item' and store.pers_dict['Фриск'].sprite_style == 'down'", At("Frisk_item_down_anim", Hero_healed_trans),

    # ITEM
    "store.pers_dict['Фриск'].state == 'item' and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_item_up_anim",
    "store.pers_dict['Фриск'].state == 'item' and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_item_down_anim",

    # ITEM2
    "store.pers_dict['Фриск'].state == 'item2' and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_item2_up_anim",
    "store.pers_dict['Фриск'].state == 'item2' and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_item2_down_anim",

    # DAMAGED / HEALED
    "store.pers_dict['Фриск'].damage_gain_for_vis >= 10 and store.pers_dict['Фриск'].state != 'item' and store.pers_dict['Фриск'].sprite_style == 'up'", At("Kris_damaged_up_1.png", Hero_damaged_trans),
    "store.pers_dict['Фриск'].damage_gain_for_vis >= 10 and store.pers_dict['Фриск'].state != 'item' and store.pers_dict['Фриск'].sprite_style == 'down'", At("Kris_damaged_down_1.png", Hero_damaged_trans),
    "store.pers_dict['Фриск'].damage_gain_for_vis <= -2 and store.pers_dict['Фриск'].sprite_style == 'up'", At("Kris_healed_up_1.png", Hero_healed_trans),
    "store.pers_dict['Фриск'].damage_gain_for_vis <= -2 and store.pers_dict['Фриск'].sprite_style == 'down'", At("Kris_healed_down_1.png", Hero_healed_trans),

    # DEFEND / ACT / ITEM
    "store.pers_dict['Фриск'].state == 'defend' and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_defend_up_anim",
    "store.pers_dict['Фриск'].state == 'defend' and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_defend_down_anim",
    "store.pers_dict['Фриск'].state == 'act' and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_act_up_anim",
    "store.pers_dict['Фриск'].state == 'act' and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_act_down_anim",
    "store.pers_dict['Фриск'].state == 'act2' and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_act2_up_anim",
    "store.pers_dict['Фриск'].state == 'act2' and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_act2_down_anim",
    # ATTACK 48
    "store.pers_dict['Фриск'].state == 'fight1'", "Frisk_atk1_anim",

    # MAGIC 49–53
    "store.pers_dict['Фриск'].state == 'magic1'", "Frisk_mag1_anim",
    "store.pers_dict['Фриск'].state == 'magic2'", "Frisk_mag2_anim",
    "store.pers_dict['Фриск'].state == 'magic3'", "Frisk_mag3_anim",
    "store.pers_dict['Фриск'].state == 'magic4'", "Frisk_mag4_anim",
    "store.pers_dict['Фриск'].state == 'magic5'", "Frisk_mag5_anim",

    # IDLE / FALLBACK
    "store.pers_dict['Фриск'].state == 'idle' and store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_idle_up_anim",
    "store.pers_dict['Фриск'].state == 'idle' and store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_idle_down_anim",
    "store.pers_dict['Фриск'].sprite_style == 'up'", "Frisk_idle_up_anim",
    "store.pers_dict['Фриск'].sprite_style == 'down'", "Frisk_idle_down_anim",
    "True", "Frisk_idle_up_anim"
)
