# =====================================================================
#  2.4_РАССКАЗАТЬ.rpy — действие «Рассказать»
# =====================================================================



label tell_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call tell_hero_self(attacker_name, target) from _call_tell_self
        return
    if target.name == "Крис":
        call tell_hero_kris(attacker_name, target) from _call_tell_kris
    elif target.name == "Азриель":
        call tell_hero_azriel(attacker_name, target) from _call_tell_az
    elif target.name == "Чара":
        call tell_hero_chara(attacker_name, target) from _call_tell_chara
    elif target.name == "Фриск":
        call tell_hero_frisk(attacker_name, target) from _call_tell_frisk
    elif target.name == "Иззи":
        call tell_hero_izzy(attacker_name, target) from _call_tell_izzy
    elif target.name == "Кловер":
        call tell_hero_clover(attacker_name, target) from _call_tell_clover
    elif target.name == "Седрик":
        call tell_hero_sedric(attacker_name, target) from _call_tell_sedric
    else:
        call tell_hero_generic(attacker_name, target) from _call_tell_hg
    return


label tell_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис мысленно рассказывает себе про свой день. Пара честных слов — и становится легче."
        else:
            "Крис пытается рассказать себе что-то, но слова путаются."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель проговаривает себе вслух: «Я имею право устать. Это не слабость.» И впервые слышит себя."
        else:
            "Азриель рассказывает себе о делах, но эмоции прячутся за словами."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара бормочет себе под нос: «Я не монстр. Я просто злюсь. Это не одно и то же.»"
        else:
            "Чара пытается сказать себе что-то, но злость перебивает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск тихо рассказывает себе историю дня. Честно. И понимает, что устал(а)."
        else:
            "Фриск привычно успокаивает себя «всё хорошо»."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шёпотом рассказывает себе о том, что тревожит. И легчает."
        else:
            "Иззи мнётся даже сама с собой."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает себе что-то без шуток. Тихо. И впервые звучит как правда."
        else:
            "Кловер переводит всё в шутку даже наедине с собой."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик вслух считает, что сделал за день. Понимает — слишком много."
        else:
            "Седрик не даёт себе даже минуты на рассказ — уже бежит к плите."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает себе что-то важное."
        else:
            "[attacker_name] не может собраться с мыслями."
    return


label tell_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает Крису о своих сомнениях. И Крис неожиданно раскрывается в ответ."
        else:
            "Азриель пробует рассказать, но Крис слушает только вполуха."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Крису, как однажды тоже не спала ночами. И он неожиданно признаётся в ответном."
        else:
            "Чара пытается, но Крис закрывается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Крису о себе. И Крис впервые слышит что-то похожее на его собственную боль."
        else:
            "Фриск пробует, но Крис вежливо слушает и молчит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко рассказывает Крису о своих страхах, и он неожиданно отвечает честно."
        else:
            "Иззи смущается и замолкает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает Крису что-то без шуток. И он отвечает без маски."
        else:
            "Кловер пробует, но Крис уходит от разговора."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает Крису о том, как тяжело бывает быть «тем, кто всех кормит». И Крис понимает."
        else:
            "Седрик пробует, но Крис отмахивается."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Крису что-то важное."
        else:
            "[attacker_name] не может достучаться до Криса."
    return


label tell_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Азриелю о своих ночах. И Азриель впервые отвечает чем-то личным."
        else:
            "Крис пробует, но Азриель улыбается вежливо."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Азриелю о том, как тяжело быть «злой». И он вдруг понимает."
        else:
            "Чара пробует, но Азриель держит маску."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Азриелю о том, как прячет усталость. Он кивает — знакомо."
        else:
            "Фриск пробует, но Азриель меняет тему."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко рассказывает, и Азриель неожиданно раскрывается."
        else:
            "Иззи смущается, и разговор не идёт."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает без шуток. И Азриель отвечает без маски."
        else:
            "Кловер пробует, но Азриель улыбается вежливо."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает Азриелю о своём. И они находят общее."
        else:
            "Седрик пробует, но Азриель вежливо уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Азриелю."
        else:
            "[attacker_name] не может рассказать Азриелю."
    return


label tell_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Чаре о том, что его тянет по ночам куда-то. И она вдруг отвечает чем-то похожим."
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает Чаре о своём страхе не быть идеальным. И она неожиданно соглашается."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Чаре о своих сомнениях. И Чара признаётся в ответном."
        else:
            "Фриск пробует, но Чара холодно уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи рассказывает, и Чара неожиданно смягчается."
        else:
            "Иззи смущается и замолкает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает Чаре без шуток. И Чара отвечает без колкостей."
        else:
            "Кловер пробует, но Чара не слушает."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает Чаре, как устаёт. И она понимает."
        else:
            "Седрик пробует, но Чара отворачивается."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Чаре."
        else:
            "[attacker_name] не может рассказать Чаре."
    return


label tell_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Фриску о том, что не может уснуть. И она отвечает чем-то похожим."
        else:
            "Крис пробует, но Фриск мягко меняет тему."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает Фриску о своём страхе. И она признаётся в ответном."
        else:
            "Азриель пробует, но Фриск вежливо улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Фриску как это — носить всё в себе. И Фриск впервые соглашается."
        else:
            "Чара пробует, но Фриск уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко рассказывает, и Фриск открывается в ответ."
        else:
            "Иззи смущается, разговор глохнет."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает Фриску всерьёз. И Фриск отвечает без маски."
        else:
            "Кловер пробует, но Фриск не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает Фриску о своей усталости. И Фриск понимает."
        else:
            "Седрик пробует, но Фриск благодарит и уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Фриску."
        else:
            "[attacker_name] не может рассказать Фриску."
    return


label tell_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Иззи что-то личное. И она перестаёт бояться говорить сама."
        else:
            "Крис пробует, но Иззи только смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает Иззи о своих сомнениях, и она перестаёт стесняться."
        else:
            "Азриель пробует, но Иззи кивает из вежливости."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Иззи что-то настоящее. И Иззи неожиданно отвечает."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Иззи о своих слабостях. И Иззи перестаёт бояться собственных."
        else:
            "Фриск пробует, но Иззи только слушает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает Иззи без шуток. И Иззи улыбается."
        else:
            "Кловер пробует, но Иззи не решается ответить."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает Иззи, как тяжело бывает. И она оживает."
        else:
            "Седрик пробует, но Иззи молчит."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Иззи."
        else:
            "[attacker_name] не может рассказать Иззи."
    return


label tell_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Кловер что-то настоящее. И она отвечает без шутки."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает Кловер о своих тревогах. И она слушает серьёзно."
        else:
            "Азриель пробует, но Кловер переводит в шутку."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Кловер о том, как прячется за злостью. И та понимает."
        else:
            "Чара пробует, но Кловер уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Кловер о своём. И Кловер отвечает без шуток."
        else:
            "Фриск пробует, но Кловер улыбается и уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко рассказывает, и Кловер впервые слушает всерьёз."
        else:
            "Иззи смущается, разговор не идёт."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает Кловер о своей усталости. И она вдруг понимает."
        else:
            "Седрик пробует, но Кловер отшучивается."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Кловер."
        else:
            "[attacker_name] не может рассказать Кловер."
    return


label tell_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Седрику о своей усталости. И тот впервые признаётся в ответном."
        else:
            "Крис пробует, но Седрик отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает Седрику о своих сомнениях. И тот понимает."
        else:
            "Азриель пробует, но Седрик уходит к делам."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Седрику о злости. И тот неожиданно отвечает честно."
        else:
            "Чара пробует, но Седрик улыбается и уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Седрику о том, как тяжело быть «сильным». И он понимает."
        else:
            "Фриск пробует, но Седрик меняет тему."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи рассказывает Седрику что-то настоящее, и он открывается в ответ."
        else:
            "Иззи робеет, и разговор глохнет."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает Седрику без шуток. И он удивлённо слушает."
        else:
            "Кловер пробует, но Седрик не реагирует."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Седрику."
        else:
            "[attacker_name] не может рассказать Седрику."
    return


label tell_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] рассказывает [target.name] что-то важное."
    else:
        "[attacker_name] не может рассказать [target.name]."
    return


label tell_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                $ trevor_mod_stat(target, "critdmg", -0.10)
                $ trevor_mod_stat(target, "attack", -0.05)
                $ renpy.notify("Тревор остывает: -10% крит. урона, -5% атаки")
            else:
                $ trevor_mod_stat(target, "critdmg", -0.20)
                $ trevor_mod_stat(target, "attack", -0.10)
                $ renpy.notify("Тревор: -20% крит. урона, -10% атаки")
        elif attacker_name == "Азриель" and ((_m == "neutral") or (_r == "peace" and _s >= 2) or (_r == "rivalry" and _m == "happy")):
            if try_to_nego_result:
                $ trevor_mod_stat(target, "speed", 0.10)
                $ renpy.notify("Тревор ускоряется: скорость +10%")
            else:
                $ trevor_mod_stat(target, "speed", 0.20)
                $ renpy.notify("Тревор ускоряется: скорость +20%")
        call tell_enemy_trevor(attacker_name, target) from _call_tell_trevor
    elif target.name == "Джевил":
        call tell_enemy_jevil(attacker_name, target) from _call_tell_jevil
    else:
        call tell_enemy_generic(attacker_name, target) from _call_tell_eg
    return


label tell_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис рассказывает Тревору о своих бессонных ночах. И Тревор впервые смотрит без насмешки."
            else:
                "Крис пробует, но Тревор отмахивается: «Да всем тяжело»."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара рассказывает Тревору о том, как сложно дома. И он неожиданно отвечает похожим."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель рассказывает Тревору о своём страхе. И Тревор слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск рассказывает Тревору о своей усталости. И он кивает."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи рассказывает что-то робкое. И Тревор неожиданно отвечает."
            else:
                "Иззи смущается, и разговор глохнет."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер рассказывает Тревору без шуток. И он слышит."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик рассказывает Тревору о своей усталости. И Тревор удивляется — впервые видит его не только «поваром»."
            else:
                "Седрик пробует, но Тревор отмахивается."
        else:
            if try_to_nego_result:
                "[attacker_name] рассказывает Тревору."
            else:
                "[attacker_name] не может рассказать Тревору."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис рассказывает Тревору о своих бессонных ночах. И Тревор впервые смотрит без насмешки."
            else:
                "Крис пробует, но Тревор отмахивается: «Да всем тяжело»."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара рассказывает Тревору о том, как сложно дома. И он неожиданно отвечает похожим."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель рассказывает Тревору о своём страхе. И Тревор слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск рассказывает Тревору о своей усталости. И он кивает."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи рассказывает что-то робкое. И Тревор неожиданно отвечает."
            else:
                "Иззи смущается, и разговор глохнет."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер рассказывает Тревору без шуток. И он слышит."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик рассказывает Тревору о своей усталости. И Тревор удивляется — впервые видит его не только «поваром»."
            else:
                "Седрик пробует, но Тревор отмахивается."
        else:
            if try_to_nego_result:
                "[attacker_name] рассказывает Тревору."
            else:
                "[attacker_name] не может рассказать Тревору."

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
                "Крис рассказывает Тревору о своих бессонных ночах. И Тревор впервые смотрит без насмешки."
            else:
                "Крис пробует, но Тревор отмахивается: «Да всем тяжело»."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара рассказывает Тревору о том, как сложно дома. И он неожиданно отвечает похожим."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель рассказывает Тревору о своём страхе. И Тревор слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск рассказывает Тревору о своей усталости. И он кивает."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи рассказывает что-то робкое. И Тревор неожиданно отвечает."
            else:
                "Иззи смущается, и разговор глохнет."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер рассказывает Тревору без шуток. И он слышит."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик рассказывает Тревору о своей усталости. И Тревор удивляется — впервые видит его не только «поваром»."
            else:
                "Седрик пробует, но Тревор отмахивается."
        else:
            if try_to_nego_result:
                "[attacker_name] рассказывает Тревору."
            else:
                "[attacker_name] не может рассказать Тревору."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис рассказывает Тревору о своих бессонных ночах. И Тревор впервые смотрит без насмешки."
            else:
                "Крис пробует, но Тревор отмахивается: «Да всем тяжело»."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара рассказывает Тревору о том, как сложно дома. И он неожиданно отвечает похожим."
            else:
                "Чара пробует, но Тревор закрывается."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель рассказывает Тревору о своём страхе. И Тревор слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск рассказывает Тревору о своей усталости. И он кивает."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи рассказывает что-то робкое. И Тревор неожиданно отвечает."
            else:
                "Иззи смущается, и разговор глохнет."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер рассказывает Тревору без шуток. И он слышит."
            else:
                "Кловер пробует, но Тревор не слушает."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик рассказывает Тревору о своей усталости. И Тревор удивляется — впервые видит его не только «поваром»."
            else:
                "Седрик пробует, но Тревор отмахивается."
        else:
            if try_to_nego_result:
                "[attacker_name] рассказывает Тревору."
            else:
                "[attacker_name] не может рассказать Тревору."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label tell_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис рассказывает Джевилу о своём. И Джевил впервые замирает и слушает."
        else:
            "Крис пробует, но Джевил исчезает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара рассказывает Джевилу о своей злости. И он понимает."
        else:
            "Чара пробует, но Джевил хохочет."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель рассказывает о своём страхе. И Джевил неожиданно кивает."
        else:
            "Азриель пробует, но Джевил кружится."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск рассказывает Джевилу что-то настоящее. И он замирает."
        else:
            "Фриск пробует, но Джевил исчезает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи рассказывает робко, но Джевил впервые слушает до конца."
        else:
            "Иззи смущается, и Джевил уходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер рассказывает без шуток. И Джевил отвечает без загадок."
        else:
            "Кловер пробует, но Джевил улыбается и исчезает."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик рассказывает о своём. И Джевил садится рядом."
        else:
            "Седрик пробует, но Джевил только хихикает."
    else:
        if try_to_nego_result:
            "[attacker_name] рассказывает Джевилу."
        else:
            "[attacker_name] не может рассказать Джевилу."
    return


label tell_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] рассказывает [target.name] что-то важное."
    else:
        "[attacker_name] не может рассказать [target.name]."
    return
