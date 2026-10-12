# =====================================================================
#  2.8_УНИЖАТЬСЯ.rpy — действие «Унижаться»
# =====================================================================

label depressed_label:
    $ attacker_names = {1: "Крис", 2: "Азриель", 3: "Чара", 4: "Фриск",
                       5: "Иззи", 6: "Кловер", 7: "Седрик", 8: "Арчи", 9: "Сильвия", 10: "Фабри", 11: "Эмили", 12: "Сьюзи", 13: "Ральзей", 14: "Ноэлль", 15: "Санс", 16: "Бердли"}
    $ attacker_name = attacker_names.get(current_attacker)
    $ attacker = store.pers_dict.get(attacker_name) if attacker_name else None

    if target is None or attacker is None:
        jump finish_act

    $ target_is_hero  = any(target is h for h in store.pers_dict.values())
    $ target_is_enemy = any(target is e for e in store.enemies.values())

    if target_is_hero:
        call humiliate_hero_reaction(attacker_name, target) from _call_hum_hero
    elif target_is_enemy:
        if try_to_nego_result:
            $ apply_act_to_enemy(target, "Унижаться", True)
            $ target.action_progress["humiliate_progress"] += 1
            $ target.spare_progress = min(
                target.spare_progress + attacker.diplomacy * dip_multiply,
                target.spare_max
            )
            if target.spare_progress >= target.spare_max:
                $ renpy.notify("[target.name] готов(а) к пощаде!")
        call humiliate_enemy_reaction(attacker_name, target) from _call_hum_enemy

    jump finish_act


label humiliate_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call humiliate_hero_self(attacker_name, target) from _call_hum_self
        return
    if target.name == "Крис":
        call humiliate_hero_kris(attacker_name, target) from _call_hum_kris
    elif target.name == "Азриель":
        call humiliate_hero_azriel(attacker_name, target) from _call_hum_az
    elif target.name == "Чара":
        call humiliate_hero_chara(attacker_name, target) from _call_hum_chara
    elif target.name == "Фриск":
        call humiliate_hero_frisk(attacker_name, target) from _call_hum_frisk
    elif target.name == "Иззи":
        call humiliate_hero_izzy(attacker_name, target) from _call_hum_izzy
    elif target.name == "Кловер":
        call humiliate_hero_clover(attacker_name, target) from _call_hum_clover
    elif target.name == "Седрик":
        call humiliate_hero_sedric(attacker_name, target) from _call_hum_sedric
    else:
        call humiliate_hero_generic(attacker_name, target) from _call_hum_hg
    return


label humiliate_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит себе: «Ты не справляешься. Ты слабый.» И вдруг понимает — он не обязан быть сильным."
        else:
            "Крис пробует себя принизить, но даже это не работает — слишком устал."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель говорит себе: «Ты не идеален.» И впервые это не ранит."
        else:
            "Азриель пробует себя унизить, но маска не снимается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара шипит себе: «Ты монстр.» И вдруг понимает — нет."
        else:
            "Чара пробует себя принизить, но злость не работает в эту сторону."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск говорит себе: «Ты не справляешься.» И это неожиданно освобождает — можно не справляться."
        else:
            "Фриск пробует, но привычка держать лицо сильнее."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи говорит себе: «Ты бесполезная.» И вдруг слышит, как это глупо звучит."
        else:
            "Иззи верит себе на слово."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер говорит себе: «Ты просто шутка.» И тут же отвечает: «Нет. Я больше.»"
        else:
            "Кловер шутит и сама себя принижает."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит себе: «Ты никому не нужен.» И вдруг понимает — как это нелепо."
        else:
            "Седрик пробует, но не верит себе."
    else:
        if try_to_nego_result:
            "[attacker_name] принижает себя — и неожиданно находит силы."
        else:
            "[attacker_name] принижает себя."
    return


label humiliate_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается перед Крисом: «Я не тот, кем кажусь.» Крис неожиданно отвечает: «Я знаю. И это нормально.»"
        else:
            "Азриель пробует, но Крис видит, что это игра."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара резко принижается: «Я злая. Я ужасная.» Крис качает головой: «Нет. Ты просто устала.»"
        else:
            "Чара пробует, но Крис не верит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск говорит: «Я не справляюсь.» И Крис вдруг отвечает: «Я тоже.»"
        else:
            "Фриск пробует, но Крис отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шепчет: «Я бесполезная.» Крис мягко: «Нет, Иззи.»"
        else:
            "Иззи смущается и замолкает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Крис неожиданно понимает — она не шутит."
        else:
            "Кловер пробует, но Крис не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я никому не нужен.» И Крис отвечает: «Ты нужен. Как минимум мне.»"
        else:
            "Седрик пробует, но Крис уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Крисом."
        else:
            "[attacker_name] не может принизиться перед Крисом."
    return


label humiliate_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я не справляюсь.» И Азриель вдруг отвечает: «Я тоже.»"
        else:
            "Крис пробует, но Азриель вежливо отмахивается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара принижается. И Азриель впервые не утешает — просто соглашается."
        else:
            "Чара пробует, но Азриель держит лицо."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск говорит: «Я устал(а).» И Азриель вдруг понимает — знакомо."
        else:
            "Фриск пробует, но Азриель вежливо уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи говорит робко: «Я плохая.» И Азриель мягко: «Нет.»"
        else:
            "Иззи стесняется, и разговор глохнет."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Азриель впервые снимает маску."
        else:
            "Кловер пробует, но Азриель вежлив."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я не справляюсь.» И Азриель вдруг отвечает тем же."
        else:
            "Седрик пробует, но Азриель уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Азриелем."
        else:
            "[attacker_name] не может принизиться перед Азриелем."
    return


label humiliate_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я слабый.» И Чара вдруг отвечает: «Я тоже.»"
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается. И Чара впервые не язвит — соглашается."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск говорит: «Я устал(а).» И Чара вдруг признаётся в том же."
        else:
            "Фриск пробует, но Чара холодна."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шепчет: «Я плохая.» И Чара неожиданно мягко: «Нет. Ты добрая. Просто боишься.»"
        else:
            "Иззи робеет, и Чара уходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Чара неожиданно понимает."
        else:
            "Кловер пробует, но Чара не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я устал.» И Чара впервые не язвит."
        else:
            "Седрик пробует, но Чара уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Чарой."
        else:
            "[attacker_name] не может принизиться перед Чарой."
    return


label humiliate_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я не справляюсь.» И Фриск вдруг отвечает: «И я.»"
        else:
            "Крис пробует, но Фриск вежливо уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается. И Фриск впервые признаётся в собственном."
        else:
            "Азриель пробует, но Фриск вежлив."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара говорит: «Я ужасная.» И Фриск вдруг: «Ты не ужасная. И я не всегда справляюсь.»"
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шепчет: «Я плохая.» И Фриск мягко: «Нет.»"
        else:
            "Иззи робеет, и разговор не идёт."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Фриск впервые отвечает тем же."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я не справляюсь.» И Фриск вдруг отвечает: «И я тоже. Давай не справляться вместе.»"
        else:
            "Седрик пробует, но Фриск вежлив."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Фриском."
        else:
            "[attacker_name] не может принизиться перед Фриском."
    return


label humiliate_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я слабый.» И Иззи вдруг отвечает: «Я тоже боюсь.»"
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается. И Иззи впервые не пугается."
        else:
            "Азриель пробует, но Иззи кивает вежливо."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара говорит: «Я злая.» И Иззи вдруг: «Ты просто защищаешься.»"
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск говорит: «Я устал(а).» И Иззи впервые слышит взрослую усталость."
        else:
            "Фриск пробует, но Иззи стесняется."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Иззи неожиданно слушает без страха."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я не справляюсь.» И Иззи вдруг отвечает: «И я иногда тоже.»"
        else:
            "Седрик пробует, но Иззи убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Иззи."
        else:
            "[attacker_name] не может принизиться перед Иззи."
    return


label humiliate_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я слабый.» И Кловер впервые не шутит: «И я.»"
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается. И Кловер неожиданно соглашается без шуток."
        else:
            "Азриель пробует, но Кловер улыбается и уходит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара говорит: «Я ужасная.» И Кловер вдруг: «А я прячусь за шутками.»"
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск принижается. И Кловер впервые признаётся в собственном."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шепчет: «Я плохая.» И Кловер мягко: «Нет. И я не всегда весёлая.»"
        else:
            "Иззи робеет, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я устал.» И Кловер неожиданно отвечает: «И я прячусь от этого.»"
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Кловер."
        else:
            "[attacker_name] не может принизиться перед Кловер."
    return


label humiliate_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я слабый.» И Седрик вдруг отвечает: «И я. Мне тоже нужна помощь.»"
        else:
            "Крис пробует, но Седрик отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается. И Седрик неожиданно соглашается."
        else:
            "Азриель пробует, но Седрик уходит к делам."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара говорит: «Я злая.» И Седрик вдруг: «И я прячусь от усталости.»"
        else:
            "Чара пробует, но Седрик улыбается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск принижается. И Седрик впервые говорит о своём."
        else:
            "Фриск пробует, но Седрик меняет тему."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шепчет: «Я не справляюсь.» И Седрик вдруг: «И я иногда.»"
        else:
            "Иззи робеет, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Седрик впервые отвечает тем же."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Седриком."
        else:
            "[attacker_name] не может принизиться перед Седриком."
    return


label humiliate_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] принижается перед [target.name]."
    else:
        "[attacker_name] не может принизиться перед [target.name]."
    return


label humiliate_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        if _r == "peace" and _s >= 3:
            if not try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.2)
                $ renpy.notify("Неудачное унижение: пощада снизилась")
        call humiliate_enemy_trevor(attacker_name, target) from _call_hum_trevor
    elif target.name == "Джевил":
        call humiliate_enemy_jevil(attacker_name, target) from _call_hum_jevil
    else:
        call humiliate_enemy_generic(attacker_name, target) from _call_hum_eg
    return


label humiliate_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис говорит Тревору: «Я не справляюсь.» И Тревор неожиданно смягчается — он тоже."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара говорит: «Я ужасная.» И Тревор вдруг: «Не ты одна.»"
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель принижается. И Тревор впервые смотрит без насмешки."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск говорит: «Я не справляюсь.» И Тревор вдруг отвечает тем же."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи шепчет: «Я плохая.» И Тревор вдруг: «Нет. Я тоже себя так чувствую.»"
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер принижается всерьёз. И Тревор впервые снимает колючки."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик говорит: «Я устал.» И Тревор вдруг отвечает: «Я тоже.»"
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] принижается перед Тревором."
            else:
                "[attacker_name] не может принизиться перед Тревором."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис говорит Тревору: «Я не справляюсь.» И Тревор неожиданно смягчается — он тоже."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара говорит: «Я ужасная.» И Тревор вдруг: «Не ты одна.»"
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель принижается. И Тревор впервые смотрит без насмешки."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск говорит: «Я не справляюсь.» И Тревор вдруг отвечает тем же."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи шепчет: «Я плохая.» И Тревор вдруг: «Нет. Я тоже себя так чувствую.»"
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер принижается всерьёз. И Тревор впервые снимает колючки."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик говорит: «Я устал.» И Тревор вдруг отвечает: «Я тоже.»"
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] принижается перед Тревором."
            else:
                "[attacker_name] не может принизиться перед Тревором."


    elif target.mood == "thoughtful":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис спрашивает мягко, и Тревор — впервые за бой — отвечает без сарказма. Ему самому странно, что хочется сказать больше."
            else:
                "Крис пробует заговорить, но Тревор молча смотрит в сторону."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара рубит прямо — и Тревор отвечает так же прямо. Задумчивость делает его честнее, чем обычно."
            else:
                "Чара давит, но Тревор молчит — но не от злобы, а потому что не готов."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель пробует задать вопрос, но Тревор смотрит мимо. Что-то в принце задевает его — не в эту секунду."
            else:
                "Тревор не отвечает Азриелю. Он не злится — просто закрыт."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск садится рядом и не спешит. И Тревор говорит сам — медленно, будто впервые формулируя свои мысли вслух."
            else:
                "Тревор молчит. Фриск не давит — просто ждёт."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи спрашивает робко. Тревор смотрит на неё внимательно и отвечает так мягко, как сам от себя не ожидал."
            else:
                "Иззи стесняется, и Тревор её не торопит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер шутит без нажима, и Тревор фыркает — но уже не зло. Он отвечает."
            else:
                "Кловер пытается разговорить, но Тревор задумчиво отводит взгляд."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик протягивает еду и молчит. Тревор благодарно кивает — и говорит сам."
            else:
                "Седрик не давит, но и Тревор не отвечает."
        else:
            if try_to_nego_result:
                "[attacker_name] смог задать вопрос задумчивому Тревору."
            else:
                "[attacker_name] не смог пробить задумчивость Тревора."

    elif target.mood == "tired":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис говорит Тревору: «Я не справляюсь.» И Тревор неожиданно смягчается — он тоже."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара говорит: «Я ужасная.» И Тревор вдруг: «Не ты одна.»"
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель принижается. И Тревор впервые смотрит без насмешки."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск говорит: «Я не справляюсь.» И Тревор вдруг отвечает тем же."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи шепчет: «Я плохая.» И Тревор вдруг: «Нет. Я тоже себя так чувствую.»"
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер принижается всерьёз. И Тревор впервые снимает колючки."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик говорит: «Я устал.» И Тревор вдруг отвечает: «Я тоже.»"
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] принижается перед Тревором."
            else:
                "[attacker_name] не может принизиться перед Тревором."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис говорит Тревору: «Я не справляюсь.» И Тревор неожиданно смягчается — он тоже."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара говорит: «Я ужасная.» И Тревор вдруг: «Не ты одна.»"
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель принижается. И Тревор впервые смотрит без насмешки."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск говорит: «Я не справляюсь.» И Тревор вдруг отвечает тем же."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи шепчет: «Я плохая.» И Тревор вдруг: «Нет. Я тоже себя так чувствую.»"
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер принижается всерьёз. И Тревор впервые снимает колючки."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик говорит: «Я устал.» И Тревор вдруг отвечает: «Я тоже.»"
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] принижается перед Тревором."
            else:
                "[attacker_name] не может принизиться перед Тревором."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label humiliate_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис говорит: «Я не справляюсь.» И Джевил замирает — он тоже."
        else:
            "Крис пробует, но Джевил кружится."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара говорит: «Я злая.» И Джевил вдруг: «Я тоже прячусь.»"
        else:
            "Чара пробует, но Джевил хохочет."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель принижается. И Джевил впервые слушает."
        else:
            "Азриель пробует, но Джевил исчезает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск говорит: «Я не справляюсь.» И Джевил не исчезает."
        else:
            "Фриск пробует, но Джевил уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шепчет: «Я плохая.» И Джевил вдруг замирает."
        else:
            "Иззи смущается, и Джевил исчезает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер принижается всерьёз. И Джевил вдруг отвечает тем же."
        else:
            "Кловер пробует, но Джевил уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик говорит: «Я не справляюсь.» И Джевил садится рядом."
        else:
            "Седрик пробует, но Джевил исчезает."
    else:
        if try_to_nego_result:
            "[attacker_name] принижается перед Джевилом."
        else:
            "[attacker_name] не может принизиться перед Джевилом."
    return


label humiliate_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] принижается перед [target.name]."
    else:
        "[attacker_name] не может принизиться перед [target.name]."
    return
