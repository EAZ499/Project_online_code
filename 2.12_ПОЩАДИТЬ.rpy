# =====================================================================
#  2.12_ПОЩАДИТЬ.rpy — действие «Пощадить»
#  Особый случай: без проверок характеристик.
#  Если spare_progress >= spare_max — враг пощажён (target.spared = True).
#  Иначе — диалог по тому же паттерну, что и у остальных действий.
# =====================================================================

label perform_spare:
    hide screen hero_acts_perform
    hide screen Heroattacks

    $ attacker_names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск",
                       5: "Иззи", 6: "Кловер", 7: "Седрик", 8: "Арчи", 9: "Сильвия", 10: "Фабри", 11: "Эмили", 12: "Сьюзи", 13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
    $ attacker_name = attacker_names.get(current_attacker)
    $ attacker = store.pers_dict.get(attacker_name) if attacker_name else None

    if target is None or attacker is None:
        jump finish_act

    $ target_is_hero  = any(target is h for h in store.pers_dict.values())
    $ target_is_enemy = any(target is e for e in store.enemies.values())

    window show
    $ attacker.state = "act"

    if target_is_enemy:
        $ target.action_progress["spare_progress_action"] += 1

        if target.spare_progress >= target.spare_max:
            # Удачная пощада
            $ target.spared = True
            $ new_character_on_spare_success(attacker_name)
            $ renpy.notify("[target.name] пощажён(а)!")
            call spare_enemy_success_dialogue(attacker_name, target) from _call_spare_success
        else:
            # Пощады мало — полный диалог по паттерну остальных действий
            call spare_enemy_fail_reaction(attacker_name, target) from _call_spare_fail

    elif target_is_hero:
        call spare_hero_reaction(attacker_name, target) from _call_spare_hero

    jump finish_act


# ---------------------------------------------------------------------
#  Диалог при удачной пощаде врага
# ---------------------------------------------------------------------
label spare_enemy_success_dialogue(attacker_name, target):
    if attacker_name == "Крис":
        "Крис опускает руки и делает шаг назад. [target.name] смотрит на него — и впервые за весь бой не делает попытки напасть."
    elif attacker_name == "Азриель":
        "Азриель мягко улыбается: «Хватит. Ты свободен.» И [target.name] действительно останавливается."
    elif attacker_name == "Чара":
        "Чара щурится, но всё же отступает: «Живи пока.» [target.name] замирает — и не атакует."
    elif attacker_name == "Фриск":
        "Фриск складывает руки и говорит тихо: «Я тебя не трону.» [target.name] медленно опускает оружие."
    elif attacker_name == "Иззи":
        "Иззи дрожащим голосом: «Я… я не буду…» И [target.name] впервые за бой замирает без злобы."
    elif attacker_name == "Кловер":
        "Кловер отводит пистолет: «Всё, отбегался. Иди.» [target.name] не верит глазам, но не двигается."
    elif attacker_name == "Седрик":
        "Седрик вытирает руки о фартук: «Достаточно. Иди с миром.» [target.name] замирает — и кивает."
    else:
        "[attacker_name] щадит [target.name]."
    return


# ---------------------------------------------------------------------
#  Диалог при НЕДОСТАТОЧНОЙ пощаде — роутер по цели
# ---------------------------------------------------------------------
label spare_enemy_fail_reaction(attacker_name, target):
    if target.name == "Тревор":
        call spare_enemy_trevor(attacker_name, target) from _call_spare_trevor
    elif target.name == "Джевил":
        call spare_enemy_jevil(attacker_name, target) from _call_spare_jevil
    else:
        call spare_enemy_generic(attacker_name, target) from _call_spare_eg
    return


label spare_enemy_trevor(attacker_name, target):
    if attacker_name == "Крис":
        "Крис делает шаг назад и опускает руки: «Я не буду тебя бить.» Тревор фыркает: «И что, я должен поверить?» Он не нападает, но и не сдаётся."
    elif attacker_name == "Чара":
        "Чара отступает, но сжатые кулаки выдают её. «Пощадила бы, если б ты не был таким…» Тревор только щурится."
    elif attacker_name == "Азриель":
        "Азриель опускает оружие: «Я не хочу драться.» Тревор вздыхает: «А кто хочет?» — но не отступает."
    elif attacker_name == "Фриск":
        "Фриск делает шаг назад: «Я не буду.» Тревор смотрит недоверчиво, но замирает."
    elif attacker_name == "Иззи":
        "Иззи прячет руки за спину: «Я… я не буду тебя бить…» Тревор смотрит на неё, но не смягчается."
    elif attacker_name == "Кловер":
        "Кловер опускает пистолет: «Да ладно, не сейчас.» Тревор хмыкает: «Умно.»"
    elif attacker_name == "Седрик":
        "Седрик отступает: «Хватит с меня.» Тревор только качает головой."
    else:
        "[attacker_name] пытается пощадить [target.name], но этого мало."
    return


label spare_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        "Крис делает шаг назад: «Хватит.» Джевил замирает, но тут же хихикает: «Не сейчас, не сейчас!»"
    elif attacker_name == "Чара":
        "Чара отступает: «Живи пока.» Джевил хохочет: «Пока — это не сейчас!»"
    elif attacker_name == "Азриель":
        "Азриель опускает руки: «Я не буду.» Джевил кружится: «Хочешь — не бей, а я всё равно уйду!»"
    elif attacker_name == "Фриск":
        "Фриск тихо: «Не буду.» Джевил смотрит долго — и исчезает, не ответив."
    elif attacker_name == "Иззи":
        "Иззи лепечет: «Я… не буду…» Джевил замирает на секунду — и снова хохочет."
    elif attacker_name == "Кловер":
        "Кловер отводит пистолет: «Хватит цирка.» Джевил хихикает: «Цирк только начинается!»"
    elif attacker_name == "Седрик":
        "Седрик говорит устало: «Иди с миром.» Джевил смотрит на него внимательно — но не отвечает."
    else:
        "[attacker_name] пытается пощадить [target.name], но этого недостаточно."
    return


label spare_enemy_generic(attacker_name, target):
    "[attacker_name] пытается пощадить [target.name], но тот ещё не готов. Пощада: [target.spare_progress]/[target.spare_max]."
    return


# ---------------------------------------------------------------------
#  Пощада героя (диалог по паттерну остальных действий)
# ---------------------------------------------------------------------
label spare_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call spare_hero_self(attacker_name, target) from _call_spare_self
        return
    if target.name == "Крис":
        call spare_hero_kris(attacker_name, target) from _call_spare_kris
    elif target.name == "Азриель":
        call spare_hero_azriel(attacker_name, target) from _call_spare_az
    elif target.name == "Чара":
        call spare_hero_chara(attacker_name, target) from _call_spare_chara
    elif target.name == "Фриск":
        call spare_hero_frisk(attacker_name, target) from _call_spare_frisk
    elif target.name == "Иззи":
        call spare_hero_izzy(attacker_name, target) from _call_spare_izzy
    elif target.name == "Кловер":
        call spare_hero_clover(attacker_name, target) from _call_spare_clover
    elif target.name == "Седрик":
        call spare_hero_sedric(attacker_name, target) from _call_spare_sedric
    else:
        call spare_hero_generic(attacker_name, target) from _call_spare_hg
    return


label spare_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        "Крис мысленно прощает себя за то, что не спал. И это неожиданно помогает."
    elif attacker_name == "Азриель":
        "Азриель говорит себе: «Ты имеешь право не быть идеальным.» И впервые верит."
    elif attacker_name == "Чара":
        "Чара шепчет себе: «Ты не монстр.» И не спорит."
    elif attacker_name == "Фриск":
        "Фриск прощает себя за то, что устал(а). И это освобождает."
    elif attacker_name == "Иззи":
        "Иззи говорит себе: «Ты достаточно.» И не краснеет."
    elif attacker_name == "Кловер":
        "Кловер неожиданно всерьёз прощает себя. Без шуток."
    elif attacker_name == "Седрик":
        "Седрик говорит себе: «Ты тоже имеешь право на отдых.» И садится."
    else:
        "[attacker_name] прощает себя."
    return


label spare_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        "Азриель мягко: «Крис, я тебя не виню. Иди отдохни.» Крис кивает."
    elif attacker_name == "Чара":
        "Чара бурчит: «Хватит себя грызть. Иди поспи.» Крис улыбается."
    elif attacker_name == "Фриск":
        "Фриск тихо: «Ты не виноват.» И Крис впервые верит."
    elif attacker_name == "Иззи":
        "Иззи шепчет: «Крис… ты не плохой…» И он выдыхает."
    elif attacker_name == "Кловер":
        "Кловер без шуток: «Ты не сломан, шеф. Иди спать.» И Крис слушается."
    elif attacker_name == "Седрик":
        "Седрик: «Крис, поешь и поспи. Мир подождёт.» И Крис соглашается."
    else:
        "[attacker_name] щадит Криса."
    return


label spare_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        "Крис: «Аз, ты не обязан быть идеальным.» И Азриель кивает."
    elif attacker_name == "Чара":
        "Чара: «Принц, отдохни уже.» И Азриель впервые не спорит."
    elif attacker_name == "Фриск":
        "Фриск: «Ты имеешь право устать.» Азриель выдыхает."
    elif attacker_name == "Иззи":
        "Иззи: «Азриель… отдохни…» И он садится."
    elif attacker_name == "Кловер":
        "Кловер: «Принц, сними корону на денёк.» И он смеётся и снимает."
    elif attacker_name == "Седрик":
        "Седрик: «Азриель, сядь, поешь.» Он садится."
    else:
        "[attacker_name] щадит Азриеля."
    return


label spare_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        "Крис: «Чара, ты не злая. Правда.» Она замирает."
    elif attacker_name == "Азриель":
        "Азриель: «Чара, я знаю, что под злостью — боль.» Она кивает."
    elif attacker_name == "Фриск":
        "Фриск: «Чара, ты можешь не защищаться. Мы рядом.» Она выдыхает."
    elif attacker_name == "Иззи":
        "Иззи: «Чара… ты добрая…» Чара впервые не огрызается."
    elif attacker_name == "Кловер":
        "Кловер: «Чара, снимай броню. Здесь своих не бьют.» Она улыбается."
    elif attacker_name == "Седрик":
        "Седрик: «Чара, сядь, поешь.» Она садится."
    else:
        "[attacker_name] щадит Чару."
    return


label spare_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        "Крис: «Фриск, ты не обязана всех спасать.» Она кивает."
    elif attacker_name == "Азриель":
        "Азриель: «Фриск, ты тоже человек.» Она выдыхает."
    elif attacker_name == "Чара":
        "Чара: «Фриск, хватит геройствовать.» Она смеётся."
    elif attacker_name == "Иззи":
        "Иззи: «Фриск… отдохни…» И она садится."
    elif attacker_name == "Кловер":
        "Кловер: «Фриск, ты не робот.» Она слушает."
    elif attacker_name == "Седрик":
        "Седрик: «Фриск, поешь и отдохни.» Она соглашается."
    else:
        "[attacker_name] щадит Фриска."
    return


label spare_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        "Крис: «Иззи, ты достаточно.» И она улыбается."
    elif attacker_name == "Азриель":
        "Азриель: «Иззи, ты не мешаешь.» Она выдыхает."
    elif attacker_name == "Чара":
        "Чара: «Иззи, хватит себя грызть.» Она кивает."
    elif attacker_name == "Фриск":
        "Фриск: «Иззи, ты классная.» Она краснеет, но верит."
    elif attacker_name == "Кловер":
        "Кловер: «Солнце, ты лучшая.» Иззи смеётся."
    elif attacker_name == "Седрик":
        "Седрик: «Иззи, ты не обязана быть удобной.» Она улыбается."
    else:
        "[attacker_name] щадит Иззи."
    return


label spare_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        "Крис: «Кловер, ты не только шутки.» Она слушает."
    elif attacker_name == "Азриель":
        "Азриель: «Кловер, ты имеешь право на грусть.» Она кивает."
    elif attacker_name == "Чара":
        "Чара: «Кловер, сними маску.» И она снимает."
    elif attacker_name == "Фриск":
        "Фриск: «Кловер, будь собой.» Она улыбается искренне."
    elif attacker_name == "Иззи":
        "Иззи: «Кловер… ты хорошая…» И Кловер впервые не шутит."
    elif attacker_name == "Седрик":
        "Седрик: «Кловер, сядь, поешь, без шуток.» Она садится."
    else:
        "[attacker_name] щадит Кловер."
    return


label spare_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        "Крис: «Седрик, сядь. Мир не рухнет.» Он садится."
    elif attacker_name == "Азриель":
        "Азриель: «Седрик, ты не обязан всех кормить.» Он выдыхает."
    elif attacker_name == "Чара":
        "Чара: «Седрик, сядь, я сама поем.» Он смеётся и садится."
    elif attacker_name == "Фриск":
        "Фриск: «Седрик, отдохни.» Он соглашается."
    elif attacker_name == "Иззи":
        "Иззи: «Седрик… отдохни… пожалуйста…» Он садится."
    elif attacker_name == "Кловер":
        "Кловер: «Шеф, привал.» И он смеётся."
    else:
        "[attacker_name] щадит Седрика."
    return


label spare_hero_generic(attacker_name, target):
    "[attacker_name] щадит [target.name]."
    return
