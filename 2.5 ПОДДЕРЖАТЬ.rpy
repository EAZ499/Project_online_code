# =====================================================================
#  2.5_ПОДДЕРЖАТЬ.rpy — действие «Поддержать»
# =====================================================================




label support_hero_reaction(attacker_name, target):
    # «Пушистик» ур.1: поддержка Азриеля поднимает упавшего союзника
    # и даёт всей команде +2 комфорта.
    $ azri_on_support(attacker_name, target)
    # «Вперёд! Вперёд!» ур.1: при поддержке Арчи даёт союзнику
    # +10%+2*ур ко всем боевым статам и +1 комфорта.
    if attacker_name == "Арчи":
        $ archie_support_ally(target)
    if target.name == attacker_name:
        call support_hero_self(attacker_name, target) from _call_support_self
        return
    if target.name == "Крис":
        call support_hero_kris(attacker_name, target) from _call_support_kris
    elif target.name == "Азриель":
        call support_hero_azriel(attacker_name, target) from _call_support_az
    elif target.name == "Чара":
        call support_hero_chara(attacker_name, target) from _call_support_chara
    elif target.name == "Фриск":
        call support_hero_frisk(attacker_name, target) from _call_support_frisk
    elif target.name == "Иззи":
        call support_hero_izzy(attacker_name, target) from _call_support_izzy
    elif target.name == "Кловер":
        call support_hero_clover(attacker_name, target) from _call_support_clover
    elif target.name == "Седрик":
        call support_hero_sedric(attacker_name, target) from _call_support_sedric
    else:
        call support_hero_generic(attacker_name, target) from _call_support_hg
    return


label support_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис кладёт руку себе на грудь. «Ты справишься. Я с тобой.» И это помогает."
        else:
            "Крис пытается себя утешить, но слова звучат пусто."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель обнимает себя за плечи. «Я имею право на слабость.» И впервые верит."
        else:
            "Азриель пробует поддержать себя, но привычка держать лицо мешает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара неожиданно тихо говорит себе: «Ты не одна. Ты справишься.» И злость отступает."
        else:
            "Чара пробует себя успокоить, но злость сильнее."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск обнимает себя. «Я делаю достаточно. Я достаточно.» И трещинка затягивается."
        else:
            "Фриск пробует, но привычка быть сильной мешает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи сжимает себя за плечи. «Я справлюсь. Я справляюсь.» И впервые верит."
        else:
            "Иззи пробует себя поддержать, но сомнение заглушает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер неожиданно всерьёз говорит себе: «Ты справишься, снайпер. Правда.» И верит."
        else:
            "Кловер пробует, но шутка вылезает сама собой."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик кладёт руку себе на грудь. «Ты тоже важен. Ты тоже имеешь право устать.»"
        else:
            "Седрик не даёт себе минуты поддержки."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает себя."
        else:
            "[attacker_name] не может себя поддержать."
    return


label support_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель обнимает Криса. Тихо. Без слов. И Крис вдруг позволяет себе выдохнуть."
        else:
            "Азриель пытается поддержать, но Крис отстраняется."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом молча. Без колкостей. Просто рядом. И Крис чувствует — она понимает."
        else:
            "Чара пробует, но Крис закрывается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск кладёт руку на плечо Крису и молчит. Этого достаточно. Он выдыхает."
        else:
            "Фриск пробует, но Крис кивает и уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи тихо берёт Криса за руку. И он неожиданно сжимает её в ответ."
        else:
            "Иззи робеет и не решается."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер садится рядом без шуток. Просто молчит. И Крис это ценит."
        else:
            "Кловер пробует, но Крис отмахивается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик ставит перед Крисом тарелку супа и садится напротив. «Ешь. Я рядом.» И Крис слушается."
        else:
            "Седрик пробует, но Крис вежливо отказывается."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Криса."
        else:
            "[attacker_name] не может поддержать Криса."
    return


label support_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис обнимает Азриеля. И тот впервые позволяет себе расслабиться в чужих руках."
        else:
            "Крис пробует, но Азриель вежливо улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом молча. И Азриель вдруг понимает — она тоже видит его усталость."
        else:
            "Чара пробует, но Азриель держит маску."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск кладёт руку на плечо. «Я рядом.» И Азриель выдыхает."
        else:
            "Фриск пробует, но Азриель вежливо уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко обнимает Азриеля. И он улыбается искренне."
        else:
            "Иззи смущается, разговор глохнет."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер садится рядом без шуток. И Азриель впервые не отшучивается."
        else:
            "Кловер пробует, но Азриель улыбается вежливо."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик приносит Азриелю чай. «Пей. И расскажи. Или молчи. Как хочешь.»"
        else:
            "Седрик пробует, но Азриель уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Азриеля."
        else:
            "[attacker_name] не может поддержать Азриеля."
    return


label support_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис молча садится рядом. И Чара впервые не отталкивает."
        else:
            "Крис пробует, но Чара шипит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель кладёт руку Чаре на плечо. Она щурится, но не уходит."
        else:
            "Азриель пробует, но Чара отворачивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск обнимает Чару. И та неожиданно позволяет себе прижаться."
        else:
            "Фриск пробует, но Чара холодно отстраняется."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко протягивает Чаре руку. И та сжимает её в ответ."
        else:
            "Иззи робеет, и Чара отходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер садится рядом без шуток. И Чара это принимает."
        else:
            "Кловер пробует, но Чара не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик ставит перед Чарой чашку чая. Без слов. И она берёт."
        else:
            "Седрик пробует, но Чара отталкивает."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Чару."
        else:
            "[attacker_name] не может поддержать Чару."
    return


label support_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис обнимает Фриска. И она впервые позволяет себе прижаться и выдохнуть."
        else:
            "Крис пробует, но Фриск мягко уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель кладёт руку Фриску на плечо. «Я рядом. Всегда.» Она кивает."
        else:
            "Азриель пробует, но Фриск улыбается и уходит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом без колкостей. Молча. И Фриск расслабляется."
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи обнимает Фриска. И та впервые позволяет себе побыть слабой."
        else:
            "Иззи робеет и не решается."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер садится рядом без шуток. И Фриск улыбается искренне."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик приносит Фриску поесть и садится напротив. «Я рядом, пока ты ешь.»"
        else:
            "Седрик пробует, но Фриск благодарит и уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Фриска."
        else:
            "[attacker_name] не может поддержать Фриска."
    return


label support_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис обнимает Иззи. И она впервые позволяет себе расплакаться."
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель обнимает Иззи. «Всё хорошо. Ты справишься.» И она верит."
        else:
            "Азриель пробует, но Иззи кивает из вежливости."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом молча. И Иззи неожиданно начинает говорить."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск обнимает Иззи. И та успокаивается."
        else:
            "Фриск пробует, но Иззи только кивает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер обнимает Иззи. Без шуток. И Иззи расслабляется."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик обнимает Иззи и приносит какао. И она впервые улыбается искренне."
        else:
            "Седрик пробует, но Иззи кивает и убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Иззи."
        else:
            "[attacker_name] не может поддержать Иззи."
    return


label support_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис садится рядом без шуток. И Кловер впервые позволяет себе молчать."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель кладёт руку Кловер на плечо. И она не отстраняется."
        else:
            "Азриель пробует, но Кловер улыбается и уходит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом. Молча. И Кловер это принимает."
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск обнимает Кловер. И та впервые не отшучивается."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи обнимает Кловер. И та неожиданно позволяет себе улыбнуться искренне."
        else:
            "Иззи робеет, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик приносит Кловер булочку и садится рядом. Без шуток. И она понимает."
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Кловер."
        else:
            "[attacker_name] не может поддержать Кловер."
    return


label support_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис молча садится рядом. И Седрик впервые позволяет себе не вставать к плите."
        else:
            "Крис пробует, но Седрик отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель садится рядом и кладёт руку на плечо. И Седрик выдыхает."
        else:
            "Азриель пробует, но Седрик уходит к делам."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом молча. И Седрик впервые не спешит."
        else:
            "Чара пробует, но Седрик отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск обнимает Седрика. И он впервые позволяет себе прижаться."
        else:
            "Фриск пробует, но Седрик мягко уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи обнимает Седрика. И он улыбается искренне."
        else:
            "Иззи робеет, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер садится рядом без шуток. И Седрик впервые не отмахивается."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Седрика."
        else:
            "[attacker_name] не может поддержать Седрика."
    return


label support_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] поддерживает [target.name]."
    else:
        "[attacker_name] не может поддержать [target.name]."
    return


label support_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                $ trevor_mod_stat(target, "critdmg", -0.10)
                $ renpy.notify("Тревор: -10% крит. урона")
            else:
                $ trevor_mod_stat(target, "critdmg", -0.20)
                $ renpy.notify("Тревор: -20% крит. урона")
        elif _r == "peace" and _s >= 3:
            if not try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.2)
                $ renpy.notify("Тревор закрывается: пощада снизилась")
        elif attacker_name != "Азриель":
            # Нейтрал, Умиротворение 24, или Соперничество 27
            if try_to_nego_result:
                $ trevor_mod_stat(target, "attack", -0.10)
                $ trevor_mod_stat(target, "critdmg", -0.20)
                $ renpy.notify("Тревор смягчается: -10% атаки, -20% крит. урона")
                if _r == "rivalry":
                    $ trevor_switch_to_peace_route(target)
            else:
                pass
        call support_enemy_trevor(attacker_name, target) from _call_support_trevor
    elif target.name == "Джевил":
        call support_enemy_jevil(attacker_name, target) from _call_support_jevil
    else:
        call support_enemy_generic(attacker_name, target) from _call_support_eg
    return


label support_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис садится рядом с Тревором и говорит: «Я не знаю, что у тебя там. Но ты не один.» Тревор долго молчит, но не уходит."
            else:
                "Крис пробует, но Тревор отворачивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара садится рядом молча. И Тревор вдруг понимает — она правда понимает."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель садится рядом и просто молчит. И Тревор впервые не отталкивает."
            else:
                "Азриель пробует, но Тревор уходит."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск кладёт руку Тревору на плечо. И он неожиданно расслабляется."
            else:
                "Фриск пробует, но Тревор отстраняется."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко садится рядом. И Тревор впервые не отгоняет."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер садится рядом без шуток. И Тревор принимает."
            else:
                "Кловер пробует, но Тревор отшучивается."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик приносит Тревору поесть и садится рядом. И Тревор впервые не отказывается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] поддерживает Тревора."
            else:
                "[attacker_name] не может поддержать Тревора."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис садится рядом с Тревором и говорит: «Я не знаю, что у тебя там. Но ты не один.» Тревор долго молчит, но не уходит."
            else:
                "Крис пробует, но Тревор отворачивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара садится рядом молча. И Тревор вдруг понимает — она правда понимает."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель садится рядом и просто молчит. И Тревор впервые не отталкивает."
            else:
                "Азриель пробует, но Тревор уходит."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск кладёт руку Тревору на плечо. И он неожиданно расслабляется."
            else:
                "Фриск пробует, но Тревор отстраняется."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко садится рядом. И Тревор впервые не отгоняет."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер садится рядом без шуток. И Тревор принимает."
            else:
                "Кловер пробует, но Тревор отшучивается."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик приносит Тревору поесть и садится рядом. И Тревор впервые не отказывается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] поддерживает Тревора."
            else:
                "[attacker_name] не может поддержать Тревора."


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
                "Крис садится рядом с Тревором и говорит: «Я не знаю, что у тебя там. Но ты не один.» Тревор долго молчит, но не уходит."
            else:
                "Крис пробует, но Тревор отворачивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара садится рядом молча. И Тревор вдруг понимает — она правда понимает."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель садится рядом и просто молчит. И Тревор впервые не отталкивает."
            else:
                "Азриель пробует, но Тревор уходит."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск кладёт руку Тревору на плечо. И он неожиданно расслабляется."
            else:
                "Фриск пробует, но Тревор отстраняется."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко садится рядом. И Тревор впервые не отгоняет."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер садится рядом без шуток. И Тревор принимает."
            else:
                "Кловер пробует, но Тревор отшучивается."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик приносит Тревору поесть и садится рядом. И Тревор впервые не отказывается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] поддерживает Тревора."
            else:
                "[attacker_name] не может поддержать Тревора."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис садится рядом с Тревором и говорит: «Я не знаю, что у тебя там. Но ты не один.» Тревор долго молчит, но не уходит."
            else:
                "Крис пробует, но Тревор отворачивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара садится рядом молча. И Тревор вдруг понимает — она правда понимает."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель садится рядом и просто молчит. И Тревор впервые не отталкивает."
            else:
                "Азриель пробует, но Тревор уходит."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск кладёт руку Тревору на плечо. И он неожиданно расслабляется."
            else:
                "Фриск пробует, но Тревор отстраняется."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко садится рядом. И Тревор впервые не отгоняет."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер садится рядом без шуток. И Тревор принимает."
            else:
                "Кловер пробует, но Тревор отшучивается."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик приносит Тревору поесть и садится рядом. И Тревор впервые не отказывается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] поддерживает Тревора."
            else:
                "[attacker_name] не может поддержать Тревора."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label support_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис садится рядом с Джевилом. И тот впервые не исчезает."
        else:
            "Крис пробует, но Джевил кружится."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара садится рядом молча. И Джевил вдруг замирает."
        else:
            "Чара пробует, но Джевил хохочет."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель садится рядом и говорит: «Я не буду тебя ловить. Я просто рядом.» И Джевил верит."
        else:
            "Азриель пробует, но Джевил исчезает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск садится рядом с Джевилом. И он впервые позволяет себе молчать."
        else:
            "Фриск пробует, но Джевил уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко садится рядом. И Джевил неожиданно улыбается искренне."
        else:
            "Иззи смущается, и Джевил уходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер садится рядом без шуток. И Джевил слышит."
        else:
            "Кловер пробует, но Джевил отмахивается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик приносит Джевилу еду. И тот садится рядом."
        else:
            "Седрик пробует, но Джевил исчезает."
    else:
        if try_to_nego_result:
            "[attacker_name] поддерживает Джевила."
        else:
            "[attacker_name] не может поддержать Джевила."
    return


label support_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] поддерживает [target.name]."
    else:
        "[attacker_name] не может поддержать [target.name]."
    return