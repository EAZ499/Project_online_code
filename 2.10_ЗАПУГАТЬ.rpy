# =====================================================================
#  2.10_ЗАПУГАТЬ.rpy — действие «Запугать»
# =====================================================================




label scare_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call scare_hero_self(attacker_name, target) from _call_scare_self
        return
    if target.name == "Крис":
        call scare_hero_kris(attacker_name, target) from _call_scare_kris
    elif target.name == "Азриель":
        call scare_hero_azriel(attacker_name, target) from _call_scare_az
    elif target.name == "Чара":
        call scare_hero_chara(attacker_name, target) from _call_scare_chara
    elif target.name == "Фриск":
        call scare_hero_frisk(attacker_name, target) from _call_scare_frisk
    elif target.name == "Иззи":
        call scare_hero_izzy(attacker_name, target) from _call_scare_izzy
    elif target.name == "Кловер":
        call scare_hero_clover(attacker_name, target) from _call_scare_clover
    elif target.name == "Седрик":
        call scare_hero_sedric(attacker_name, target) from _call_scare_sedric
    else:
        call scare_hero_generic(attacker_name, target) from _call_scare_hg
    return


label scare_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис пугает себя мыслью о будущем. И понимает — страх можно использовать."
        else:
            "Крис пытается напугать себя, но уже и так напуган."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель пугает себя мыслью «а что если я не справлюсь». И вдруг решает: справлюсь."
        else:
            "Азриель пробует, но страх не работает как топливо."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара пугает себя тем, что может стать монстром. И злится — потому что не станет."
        else:
            "Чара пробует, но злость сильнее страха."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск пугает себя мыслью «а если не спасу». И вдруг понимает — не обязана."
        else:
            "Фриск пробует, но страх устал."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи пугает себя тем, что останется одна. И плачет. Но потом встаёт."
        else:
            "Иззи пугает себя, и ей становится только хуже."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер пугает себя мыслью о провале. И решает: не провалюсь."
        else:
            "Кловер пробует, но не верит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик пугает себя мыслью, что подведёт всех. И понимает — он не один."
        else:
            "Седрик пробует, но страх не помогает."
    else:
        if try_to_nego_result:
            "[attacker_name] пугает себя — и это работает."
        else:
            "[attacker_name] не может себя напугать."
    return


label scare_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель говорит сурово: «Крис, если ты продолжишь так — ты сломаешься.» И Крис впервые верит."
        else:
            "Азриель пробует, но Крис не реагирует."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Крис, если ты сейчас не остановишься, я найду способ тебя остановить.» И он замирает."
        else:
            "Чара пробует, но Крис отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Крис, я не переживу, если ты сдашься.» Он вздрагивает."
        else:
            "Фриск пробует, но Крис закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи шёпотом: «Крис… пожалуйста… не уходи…» И он неожиданно останавливается."
        else:
            "Иззи робеет, и Крис вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер без шуток: «Шеф, я найду тебя, где бы ты ни был. Держись.» И Крис кивает."
        else:
            "Кловер пробует, но Крис уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик сурово: «Крис, ты не ел неделю. Сядь. Сейчас.» И Крис садится."
        else:
            "Седрик пробует, но Крис отмахивается."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Криса — и работает."
        else:
            "[attacker_name] не может запугать Криса."
    return


label scare_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис сурово: «Аз, ты тоже сломаешься, если не остановишься.» И Азриель впервые кивает."
        else:
            "Крис пробует, но Азриель держит лицо."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Принц, ты либо улыбайся честно, либо сними корону. Так нельзя.» Он замирает."
        else:
            "Чара пробует, но Азриель улыбается вежливо."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Азриель, я не хочу потом искать тебя по кусочкам.» Он вздрагивает."
        else:
            "Фриск пробует, но Азриель уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи: «Азриель… пожалуйста… не исчезай…» И он неожиданно соглашается."
        else:
            "Иззи смущается, и Азриель вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер без шуток: «Принц, тебе конец, если ты продолжишь играть идеального.» Он слушает."
        else:
            "Кловер пробует, но Азриель улыбается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик: «Азриель, если ты сейчас же не сядешь — я лично тебя усажу.» Он садится."
        else:
            "Седрик пробует, но Азриель уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Азриеля."
        else:
            "[attacker_name] не может запугать Азриеля."
    return


label scare_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис сурово: «Чара, если ты продолжишь отталкивать всех — останешься одна. По-настоящему.» Она замирает."
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель: «Чара, злость тебя съест, если ты её не выплеснешь. Поговори.» Она слушает."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Чара, я не хочу смотреть, как ты сгораешь.» Она неожиданно вздрагивает."
        else:
            "Фриск пробует, но Чара холодна."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи: «Чара… не уходи… пожалуйста…» Она замирает — впервые."
        else:
            "Иззи смущается, и Чара отходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер без шуток: «Чара, если ты сейчас не остановишься — я тоже пойду с тобой. Но я хочу остаться.» Она слушает."
        else:
            "Кловер пробует, но Чара уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик: «Чара, если ты не поешь, я лично тебя накормлю.» Она смеётся — но соглашается."
        else:
            "Седрик пробует, но Чара отмахивается."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Чару."
        else:
            "[attacker_name] не может запугать Чару."
    return


label scare_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис сурово: «Фриск, ты тоже имеешь право устать. Но ты не бессмертна.» Она кивает."
        else:
            "Крис пробует, но Фриск уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель: «Фриск, если ты продолжишь всех спасать — тебя не станет. Нас не станет.» Она вздрагивает."
        else:
            "Азриель пробует, но Фриск вежлива."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Фриск, ты не обязана. Если ты сдашься — это не предательство.» Она слушает."
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи: «Фриск… пожалуйста… не исчезай…» И Фриск неожиданно соглашается."
        else:
            "Иззи смущается, и Фриск вежлива."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер без шуток: «Фриск, ты не робот. Если продолжишь — сломаешься.» Она слушает."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик: «Фриск, ты поел(а)? Нет? Тогда я лично посажу тебя за стол.» И она садится."
        else:
            "Седрик пробует, но Фриск уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Фриска."
        else:
            "[attacker_name] не может запугать Фриска."
    return


label scare_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис: «Иззи, если ты продолжишь себя недооценивать — мир не узнает, какая ты.» Она вздрагивает."
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель: «Иззи, если ты не поверишь в себя — никто не поверит за тебя.» Она кивает."
        else:
            "Азриель пробует, но Иззи вежливо кивает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Иззи, если ты сейчас не перестанешь стесняться — я тебя заставлю говорить.» И она впервые смеётся."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Иззи, если ты не скажешь, что чувствуешь — никто не узнает.» Она неожиданно отвечает."
        else:
            "Фриск пробует, но Иззи стесняется."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер: «Солнце, если ты не перестанешь прятаться — я сама тебя вытащу.» Иззи смеётся."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик: «Иззи, если ты сейчас не съешь что-нибудь — я обижусь.» Она смеётся и ест."
        else:
            "Седрик пробует, но Иззи убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Иззи."
        else:
            "[attacker_name] не может запугать Иззи."
    return


label scare_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис: «Кловер, если ты продолжишь прятаться за шутками — ты потеряешь себя.» Она замирает."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель: «Кловер, если ты продолжишь всех развлекать — тебе не останется себя.» Она слушает."
        else:
            "Азриель пробует, но Кловер улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Кловер, если ты сейчас не скажешь правду — я тебя заставлю.» И Кловер вдруг говорит."
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Кловер, если ты не позволишь себе быть слабой — тебе будет плохо.» Она кивает."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи: «Кловер… пожалуйста… будь собой…» И Кловер впервые серьёзна."
        else:
            "Иззи смущается, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик: «Кловер, если ты сейчас же не сядешь и не поешь — я обижусь.» Она смеётся и садится."
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Кловер."
        else:
            "[attacker_name] не может запугать Кловер."
    return


label scare_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис: «Седрик, если ты продолжишь — я найду способ тебя остановить.» И он впервые садится."
        else:
            "Крис пробует, но Седрик отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель: «Седрик, если ты не сядешь — ты не сможешь никого накормить.» Он садится."
        else:
            "Азриель пробует, но Седрик уходит к делам."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Седрик, если ты сейчас не сядешь — я съем всё сама.» Он смеётся и садится."
        else:
            "Чара пробует, но Седрик уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Седрик, если ты не отдохнёшь — тебе нечем будет кормить.» Он вздрагивает."
        else:
            "Фриск пробует, но Седрик отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи: «Седрик… если ты не посидишь… тебе станет плохо…» И он садится."
        else:
            "Иззи смущается, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер: «Седрик, если ты сейчас не сядешь — я лично тебя усажу.» Он хохочет и садится."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Седрика."
        else:
            "[attacker_name] не может запугать Седрика."
    return


label scare_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] запугивает [target.name]."
    else:
        "[attacker_name] не может запугать [target.name]."
    return


label scare_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                $ trevor_mod_stat(target, "critdmg", 0.15)
                $ renpy.notify("Тревор готов дать сдачи: +15% крит. урона")
            else:
                $ trevor_mod_stat(target, "critdmg", 0.30)
                $ renpy.notify("Тревор разъярён: +30% крит. урона")
        elif _m == "neutral" and _r is None:
            if not try_to_nego_result:
                $ trevor_mod_stat(target, "attack", 0.05)
                $ trevor_mod_socialization(attacker_name, -1)
                $ renpy.notify("Неудачное запугивание: Тревор +5% атаки, социализация -1")
        elif (_r == "peace" and _s == 2) or (_r == "rivalry" and _m == "happy"):
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ trevor_mod_stat(target, "attack", 0.10)
                $ renpy.notify("Запугивание обозлило: пощада -0.5 дипл., атака +10%")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ trevor_mod_stat(target, "attack", 0.20)
                $ renpy.notify("Провал запугивания: пощада -1.0 дипл., атака +20%")
        elif _r == "peace" and _s >= 3:
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ renpy.notify("Тревор замкнулся: пощада -0.5 дипл.")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ renpy.notify("Тревор отстранился: пощада -1.0 дипл.")
        call scare_enemy_trevor(attacker_name, target) from _call_scare_trevor
    elif target.name == "Джевил":
        call scare_enemy_jevil(attacker_name, target) from _call_scare_jevil
    else:
        call scare_enemy_generic(attacker_name, target) from _call_scare_eg
    return


label scare_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис сурово: «Тревор, если ты продолжишь так — я не смогу тебе помочь.» И Тревор неожиданно кивает."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара: «Тревор, если ты сейчас не скажешь правду — я найду её сама.» Он замирает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель: «Тревор, если ты не остановишься — я не смогу тебя защитить.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск: «Тревор, если ты не скажешь — я не смогу помочь.» Он неожиданно отвечает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи: «Тревор… не уходи… пожалуйста…» Он замирает."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер: «Тревор, если ты сейчас не заговоришь — я буду стрелять шутками без остановки.» Он смеётся, но говорит."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик: «Тревор, если ты не поешь — я тебя накормлю насильно.» Он смеётся и ест."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] запугивает Тревора."
            else:
                "[attacker_name] не может запугать Тревора."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис сурово: «Тревор, если ты продолжишь так — я не смогу тебе помочь.» И Тревор неожиданно кивает."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара: «Тревор, если ты сейчас не скажешь правду — я найду её сама.» Он замирает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель: «Тревор, если ты не остановишься — я не смогу тебя защитить.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск: «Тревор, если ты не скажешь — я не смогу помочь.» Он неожиданно отвечает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи: «Тревор… не уходи… пожалуйста…» Он замирает."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер: «Тревор, если ты сейчас не заговоришь — я буду стрелять шутками без остановки.» Он смеётся, но говорит."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик: «Тревор, если ты не поешь — я тебя накормлю насильно.» Он смеётся и ест."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] запугивает Тревора."
            else:
                "[attacker_name] не может запугать Тревора."


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
                "Крис сурово: «Тревор, если ты продолжишь так — я не смогу тебе помочь.» И Тревор неожиданно кивает."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара: «Тревор, если ты сейчас не скажешь правду — я найду её сама.» Он замирает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель: «Тревор, если ты не остановишься — я не смогу тебя защитить.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск: «Тревор, если ты не скажешь — я не смогу помочь.» Он неожиданно отвечает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи: «Тревор… не уходи… пожалуйста…» Он замирает."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер: «Тревор, если ты сейчас не заговоришь — я буду стрелять шутками без остановки.» Он смеётся, но говорит."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик: «Тревор, если ты не поешь — я тебя накормлю насильно.» Он смеётся и ест."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] запугивает Тревора."
            else:
                "[attacker_name] не может запугать Тревора."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис сурово: «Тревор, если ты продолжишь так — я не смогу тебе помочь.» И Тревор неожиданно кивает."
            else:
                "Крис пробует, но Тревор фыркает."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара: «Тревор, если ты сейчас не скажешь правду — я найду её сама.» Он замирает."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель: «Тревор, если ты не остановишься — я не смогу тебя защитить.» Он слушает."
            else:
                "Азриель пробует, но Тревор не реагирует."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск: «Тревор, если ты не скажешь — я не смогу помочь.» Он неожиданно отвечает."
            else:
                "Фриск пробует, но Тревор закрывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи: «Тревор… не уходи… пожалуйста…» Он замирает."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер: «Тревор, если ты сейчас не заговоришь — я буду стрелять шутками без остановки.» Он смеётся, но говорит."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик: «Тревор, если ты не поешь — я тебя накормлю насильно.» Он смеётся и ест."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] запугивает Тревора."
            else:
                "[attacker_name] не может запугать Тревора."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label scare_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис сурово: «Джевил, если ты продолжишь прятаться за загадками — ты никогда не найдёшь себя.» Он замирает."
        else:
            "Крис пробует, но Джевил исчезает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара: «Джевил, если ты не ответишь прямо — я найду способ заставить.» Он впервые отвечает без загадки."
        else:
            "Чара пробует, но Джевил кружится."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель: «Джевил, если ты не сбросишь маску — она срастётся с тобой.» Он слушает."
        else:
            "Азриель пробует, но Джевил уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск: «Джевил, если ты не скажешь, что болит — я не смогу помочь.» Он неожиданно говорит."
        else:
            "Фриск пробует, но Джевил исчезает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи: «Джевил… не уходи…» И он не уходит."
        else:
            "Иззи смущается, и Джевил уходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер: «Джевил, если ты сейчас не заговоришь по-человечески — я расскажу всем, что ты добрый.» Он хохочет, но говорит."
        else:
            "Кловер пробует, но Джевил уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик: «Джевил, если ты сейчас не сядешь и не поешь — я обижусь.» Он садится."
        else:
            "Седрик пробует, но Джевил исчезает."
    else:
        if try_to_nego_result:
            "[attacker_name] запугивает Джевила."
        else:
            "[attacker_name] не может запугать Джевила."
    return


label scare_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] запугивает [target.name]."
    else:
        "[attacker_name] не может запугать [target.name]."
    return