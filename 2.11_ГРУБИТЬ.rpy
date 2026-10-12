# =====================================================================
#  2.11_ГРУБИТЬ.rpy — действие «Грубить»
# =====================================================================




label rude_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call rude_hero_self(attacker_name, target) from _call_rude_self
        return
    if target.name == "Крис":
        call rude_hero_kris(attacker_name, target) from _call_rude_kris
    elif target.name == "Азриель":
        call rude_hero_azriel(attacker_name, target) from _call_rude_az
    elif target.name == "Чара":
        call rude_hero_chara(attacker_name, target) from _call_rude_chara
    elif target.name == "Фриск":
        call rude_hero_frisk(attacker_name, target) from _call_rude_frisk
    elif target.name == "Иззи":
        call rude_hero_izzy(attacker_name, target) from _call_rude_izzy
    elif target.name == "Кловер":
        call rude_hero_clover(attacker_name, target) from _call_rude_clover
    elif target.name == "Седрик":
        call rude_hero_sedric(attacker_name, target) from _call_rude_sedric
    else:
        call rude_hero_generic(attacker_name, target) from _call_rude_hg
    return


label rude_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо бросает себе: «Соберись, тряпка.» И — работает."
        else:
            "Крис ругает себя, но это не помогает."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Хватит притворяться.» И впервые слышит себя."
        else:
            "Азриель пробует, но маска держится."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Хватит ныть, ты не слабая.» И злится — но правильно."
        else:
            "Чара пробует, но саможалость сильнее."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо себе: «Ты не спасательный круг.» И выдыхает."
        else:
            "Фриск пробует, но привычка держать лицо мешает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо себе: «Хватит бояться!» И впервые не боится."
        else:
            "Иззи пробует, но страх сильнее."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо себе: «Хватит прятаться за шутками!» И впервые молчит без неловкости."
        else:
            "Кловер пробует, но шутка вырывается сама."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо себе: «Сядь. Отдохни. Немедленно.» И садится."
        else:
            "Седрик пробует, но дела сильнее."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит себе — и работает."
        else:
            "[attacker_name] не может на себя надавить."
    return


label rude_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель резко: «Крис, ты выглядишь как труп. Иди спать.» Крис впервые слушается."
        else:
            "Азриель пробует, но Крис вежлив."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Крис, ты выглядишь ужасно. Иди спать, идиот.» Крис усмехается."
        else:
            "Чара пробует, но Крис отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск неожиданно грубо: «Крис, хватит себя жалеть.» Он вздрагивает."
        else:
            "Фриск пробует, но Крис закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Крис, ты… ты должен спать!» Он улыбается."
        else:
            "Иззи смущается, и Крис вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Шеф, ты вообще себя видел? Иди спать, кому говорю.» Крис хохочет."
        else:
            "Кловер пробует, но Крис уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Крис, если ты сейчас не сядешь — я лично уложу тебя.» Крис садится."
        else:
            "Седрик пробует, но Крис уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Крису — и работает."
        else:
            "[attacker_name] не может надавить на Криса."
    return


label rude_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Аз, хватит изображать идеального. Сними маску.» Азриель слушает."
        else:
            "Крис пробует, но Азриель улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Принц, ты либо живой, либо картинка. Выбирай.» Он впервые не улыбается."
        else:
            "Чара пробует, но Азриель держит лицо."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо: «Азриель, хватит спасать всех, кроме себя.» Он замирает."
        else:
            "Фриск пробует, но Азриель уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Азриель… ты… ты устал! Отдохни!» Он смеётся."
        else:
            "Иззи смущается, и Азриель вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Принц, снимай корону. Отдохни. Или сломаешься.» Он слушает."
        else:
            "Кловер пробует, но Азриель уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Азриель, сядь. Поешь. Молчи. Это приказ.» Он хохочет и садится."
        else:
            "Седрик пробует, но Азриель уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Азриелю."
        else:
            "[attacker_name] не может надавить на Азриеля."
    return


label rude_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Чара, хватит всех отталкивать. Ты не одна.» Она замирает."
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Чара, злость не заменит тебе близких.» Она слушает."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо: «Чара, хватит строить из себя монстра. Ты не монстр.» Она вздрагивает."
        else:
            "Фриск пробует, но Чара холодна."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Чара… не уходи… пожалуйста!» Она замирает."
        else:
            "Иззи смущается, и Чара отходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Чара, хватит язвить. Скажи уже, что болит.» Она впервые говорит."
        else:
            "Кловер пробует, но Чара уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Чара, сядь. Поешь. Потом злись.» Она смеётся и садится."
        else:
            "Седрик пробует, но Чара уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Чаре."
        else:
            "[attacker_name] не может надавить на Чару."
    return


label rude_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Фриск, ты не спасательный круг. Отдохни.» Она кивает."
        else:
            "Крис пробует, но Фриск уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Фриск, ты не обязана всех вытаскивать.» Она слушает."
        else:
            "Азриель пробует, но Фриск вежлива."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Фриск, хватит быть святой. Ты тоже живая.» Она вздрагивает."
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Фриск… отдохни… пожалуйста!» Она улыбается."
        else:
            "Иззи смущается, и Фриск вежлива."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Фриск, ты тоже человек. Хватит геройствовать.» Она слушает."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Фриск, ешь. Сейчас. Иначе обижусь.» Она смеётся и ест."
        else:
            "Седрик пробует, но Фриск уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Фриску."
        else:
            "[attacker_name] не может надавить на Фриска."
    return


label rude_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Иззи, хватит себя недооценивать. Ты не хуже других.» Она вздрагивает."
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Иззи, хватит прятаться. Ты достойна.» Она кивает."
        else:
            "Азриель пробует, но Иззи вежливо кивает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Иззи, хватит краснеть! Говори!» Она неожиданно говорит."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо: «Иззи, хватит себя жалеть.» Она неожиданно отвечает."
        else:
            "Фриск пробует, но Иззи стесняется."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Солнце, хватит прятаться. Ты классная. Точка.» Она смеётся."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Иззи, ешь. Сейчас. Иначе обижусь.» Она смеётся и ест."
        else:
            "Седрик пробует, но Иззи убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Иззи."
        else:
            "[attacker_name] не может надавить на Иззи."
    return


label rude_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Кловер, хватит шутить. Скажи правду.» Она замирает."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Кловер, шутки не заменят тебе настоящих чувств.» Она слушает."
        else:
            "Азриель пробует, но Кловер улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Кловер, хватит прятаться за шутками. Говори.» И Кловер говорит."
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо: «Кловер, хватит всех развлекать. Позаботься о себе.» Она кивает."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Кловер… будь собой… пожалуйста!» Кловер впервые серьёзна."
        else:
            "Иззи смущается, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Кловер, сядь и поешь. Без шуток.» Она смеётся и садится."
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Кловер."
        else:
            "[attacker_name] не может надавить на Кловер."
    return


label rude_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Седрик, сядь. Отдохни. Иначе развалишься.» Он садится."
        else:
            "Крис пробует, но Седрик отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Седрик, ты человек, а не машина. Сядь.» Он слушает."
        else:
            "Азриель пробует, но Седрик уходит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Седрик, сядь, пока я не съела всё сама.» Он смеётся и садится."
        else:
            "Чара пробует, но Седрик уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо: «Седрик, если ты не отдохнёшь — тебе нечем будет кормить.» Он садится."
        else:
            "Фриск пробует, но Седрик отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Седрик… сядь… пожалуйста!» Он садится."
        else:
            "Иззи смущается, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Седрик, сядь, или я усажу.» Он хохочет и садится."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Седрику."
        else:
            "[attacker_name] не может надавить на Седрика."
    return


label rude_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] грубит [target.name]."
    else:
        "[attacker_name] не может надавить на [target.name]."
    return


label rude_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                $ trevor_mod_stat(target, "accuracy", 0.15)
                $ renpy.notify("Тревор предельно собран: +15% точности")
            else:
                $ trevor_mod_stat(target, "accuracy", 0.30)
                $ renpy.notify("Тревор в ярости: +30% точности")
        elif _m == "neutral" and _r is None:
            if not try_to_nego_result:
                $ trevor_mod_stat(target, "attack", 0.05)
                $ trevor_mod_socialization(attacker_name, -1)
                $ renpy.notify("Неудачная грубость: Тревор +5% атаки, социализация -1")
        elif (_r == "peace" and _s == 2) or (_r == "rivalry" and _m == "happy"):
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ trevor_mod_stat(target, "attack", 0.10)
                $ renpy.notify("Грубость обозлила: пощада -0.5 дипл., атака +10%")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ trevor_mod_stat(target, "attack", 0.20)
                $ renpy.notify("Провал грубости: пощада -1.0 дипл., атака +20%")
        elif _r == "peace" and _s >= 3:
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ renpy.notify("Тревор оскорблён: пощада -0.5 дипл.")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ renpy.notify("Тревор отвернулся: пощада -1.0 дипл.")
        call rude_enemy_trevor(attacker_name, target) from _call_rude_trevor
    elif target.name == "Джевил":
        call rude_enemy_jevil(attacker_name, target) from _call_rude_jevil
    else:
        call rude_enemy_generic(attacker_name, target) from _call_rude_eg
    return


label rude_enemy_trevor(attacker_name, target):


    

    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис грубо: «Тревор, хватит прятаться. Говори как есть.» Он замирает и правда говорит."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара грубо: «Тревор, хватит врать себе. Что дома?» Он неожиданно отвечает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель грубо: «Тревор, хватит притворяться. Я вижу.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск грубо: «Тревор, хватит всё держать в себе.» Он замирает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи грубо (для неё): «Тревор… скажи правду…» Он неожиданно говорит."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер грубо: «Тревор, хватит отмалчиваться. Говори.» Он усмехается и говорит."
            else:
                "Кловер пробует, но Тревор уходит."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик грубо: «Тревор, сядь и поешь. И заодно расскажи.» Он садится."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] грубит Тревору."
            else:
                "[attacker_name] не может надавить на Тревора."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис грубо: «Тревор, хватит прятаться. Говори как есть.» Он замирает и правда говорит."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара грубо: «Тревор, хватит врать себе. Что дома?» Он неожиданно отвечает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель грубо: «Тревор, хватит притворяться. Я вижу.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск грубо: «Тревор, хватит всё держать в себе.» Он замирает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи грубо (для неё): «Тревор… скажи правду…» Он неожиданно говорит."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер грубо: «Тревор, хватит отмалчиваться. Говори.» Он усмехается и говорит."
            else:
                "Кловер пробует, но Тревор уходит."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик грубо: «Тревор, сядь и поешь. И заодно расскажи.» Он садится."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] грубит Тревору."
            else:
                "[attacker_name] не может надавить на Тревора."


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
                "Крис грубо: «Тревор, хватит прятаться. Говори как есть.» Он замирает и правда говорит."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара грубо: «Тревор, хватит врать себе. Что дома?» Он неожиданно отвечает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель грубо: «Тревор, хватит притворяться. Я вижу.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск грубо: «Тревор, хватит всё держать в себе.» Он замирает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи грубо (для неё): «Тревор… скажи правду…» Он неожиданно говорит."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер грубо: «Тревор, хватит отмалчиваться. Говори.» Он усмехается и говорит."
            else:
                "Кловер пробует, но Тревор уходит."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик грубо: «Тревор, сядь и поешь. И заодно расскажи.» Он садится."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] грубит Тревору."
            else:
                "[attacker_name] не может надавить на Тревора."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис грубо: «Тревор, хватит прятаться. Говори как есть.» Он замирает и правда говорит."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара грубо: «Тревор, хватит врать себе. Что дома?» Он неожиданно отвечает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель грубо: «Тревор, хватит притворяться. Я вижу.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск грубо: «Тревор, хватит всё держать в себе.» Он замирает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи грубо (для неё): «Тревор… скажи правду…» Он неожиданно говорит."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер грубо: «Тревор, хватит отмалчиваться. Говори.» Он усмехается и говорит."
            else:
                "Кловер пробует, но Тревор уходит."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик грубо: «Тревор, сядь и поешь. И заодно расскажи.» Он садится."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] грубит Тревору."
            else:
                "[attacker_name] не может надавить на Тревора."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label rude_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис грубо: «Джевил, хватит прятаться за загадками.» Он замирает."
        else:
            "Крис пробует, но Джевил исчезает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара грубо: «Джевил, хватит цирка. Говори прямо.» Он впервые говорит прямо."
        else:
            "Чара пробует, но Джевил хохочет."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель грубо: «Джевил, сними маску. Я не враг.» Он слушает."
        else:
            "Азриель пробует, но Джевил исчезает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск грубо: «Джевил, хватит загадок. Скажи как есть.» Он неожиданно говорит."
        else:
            "Фриск пробует, но Джевил уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи грубо (для неё): «Джевил… не прячься…» Он не исчезает."
        else:
            "Иззи смущается, и Джевил уходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер грубо: «Джевил, хватит клоунады. Говори по-человечески.» Он хохочет и говорит."
        else:
            "Кловер пробует, но Джевил уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик грубо: «Джевил, сядь и поешь. Без загадок.» Он садится."
        else:
            "Седрик пробует, но Джевил исчезает."
    else:
        if try_to_nego_result:
            "[attacker_name] грубит Джевилу."
        else:
            "[attacker_name] не может надавить на Джевила."
    return


label rude_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] грубит [target.name]."
    else:
        "[attacker_name] не может надавить на [target.name]."
    return
