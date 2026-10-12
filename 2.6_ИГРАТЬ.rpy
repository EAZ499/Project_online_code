# =====================================================================
#  2.6_ИГРАТЬ.rpy — действие «Играть»
# =====================================================================




label play_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call play_hero_self(attacker_name, target) from _call_play_self
        return
    if target.name == "Крис":
        call play_hero_kris(attacker_name, target) from _call_play_kris
    elif target.name == "Азриель":
        call play_hero_azriel(attacker_name, target) from _call_play_az
    elif target.name == "Чара":
        call play_hero_chara(attacker_name, target) from _call_play_chara
    elif target.name == "Фриск":
        call play_hero_frisk(attacker_name, target) from _call_play_frisk
    elif target.name == "Иззи":
        call play_hero_izzy(attacker_name, target) from _call_play_izzy
    elif target.name == "Кловер":
        call play_hero_clover(attacker_name, target) from _call_play_clover
    elif target.name == "Седрик":
        call play_hero_sedric(attacker_name, target) from _call_play_sedric
    else:
        call play_hero_generic(attacker_name, target) from _call_play_hg
    return


label play_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис вспоминает, как в детстве они с Азриелем играли в Super Star Fighters. Уголок рта дёргается вверх — впервые за день."
        else:
            "Крис пытается вспомнить что-то весёлое, но находит только пустоту."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель вспоминает, как раньше играл с Крисом. И улыбается искренне — не дежурно."
        else:
            "Азриель пробует отвлечься, но мысли не отпускают."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара вспоминает, как играла в снежки. И где-то внутри что-то оттаивает."
        else:
            "Чара пытается отвлечься, но раздражение сильнее."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск вспоминает любимую игру детства и мысленно улыбается."
        else:
            "Фриск пробует отвлечься, но привычка думать о других мешает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи вспоминает тамагочи, который у неё был. И улыбается."
        else:
            "Иззи пробует отвлечься, но тревога сильнее."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер вспоминает рекорды по тиру. И подмигивает себе: «Ещё побьём.»"
        else:
            "Кловер пробует отвлечься, но всё скатывается в шутку."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик вспоминает, как впервые приготовил что-то съедобное. Улыбается."
        else:
            "Седрик пробует отвлечься, но мысли о делах не отпускают."
    else:
        if try_to_nego_result:
            "[attacker_name] играет сам с собой и отвлекается."
        else:
            "[attacker_name] не может отвлечься."
    return


label play_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель вспоминает старую игру, в которую они играли детьми. И Крис впервые за день смеётся."
        else:
            "Азриель пробует, но Крис только вежливо улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает сыграть в «кто дольше промолчит». Крис неожиданно включается — и впервые расслабляется."
        else:
            "Чара пробует, но Крис не в настроении."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает простую словесную игру. И Крис включается."
        else:
            "Фриск пробует, но Крис только кивает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи предлагает поиграть в угадайку. И Крис включается, улыбаясь."
        else:
            "Иззи робеет, и Крис вежливо отказывается."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает игру в «кто придумает худший каламбур». Крис неожиданно выигрывает."
        else:
            "Кловер пробует, но Крис уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает Крису сыграть в «угадай блюдо по запаху». И Крис улыбается."
        else:
            "Седрик пробует, но Крис отмахивается."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Крисом."
        else:
            "[attacker_name] не может развеселить Криса."
    return


label play_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис вспоминает старую игру. И Азриель впервые смеётся без маски."
        else:
            "Крис пробует, но Азриель вежливо улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает сыграть в «найди у принца трещинку». Азриель сначала смущается, потом смеётся."
        else:
            "Чара пробует, но Азриель держит лицо."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает простую игру. И Азриель включается."
        else:
            "Фриск пробует, но Азриель вежливо уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи предлагает игру. И Азриель улыбается искренне."
        else:
            "Иззи смущается, и разговор не идёт."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает «кто придумает худший титул для принца». Азриель впервые хохочет."
        else:
            "Кловер пробует, но Азриель вежливо улыбается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает угадать блюдо. И Азриель включается."
        else:
            "Седрик пробует, но Азриель отмахивается."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Азриелем."
        else:
            "[attacker_name] не может развеселить Азриеля."
    return


label play_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис предлагает Чаре игру в молчанку. И она впервые участвует без колкостей."
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель предлагает лёгкую игру. И Чара впервые улыбается."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает игру. И Чара неожиданно включается."
        else:
            "Фриск пробует, но Чара холодно отказывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи предлагает игру. И Чара неожиданно смягчается."
        else:
            "Иззи робеет, и Чара отходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает «кто придумает худшую шутку». Чара смеётся — впервые за день."
        else:
            "Кловер пробует, но Чара не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает угадать блюдо. И Чара нехотя, но играет."
        else:
            "Седрик пробует, но Чара отказывается."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Чарой."
        else:
            "[attacker_name] не может развеселить Чару."
    return


label play_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис предлагает простую игру. И Фриск отвлекается — впервые за день."
        else:
            "Крис пробует, но Фриск улыбается и уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель предлагает игру. И Фриск смеётся."
        else:
            "Азриель пробует, но Фриск вежливо отказывается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает «кто дольше промолчит». И Фриск сдаётся первой с улыбкой."
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи предлагает игру. И Фриск включается искренне."
        else:
            "Иззи робеет, и Фриск улыбается вежливо."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает весёлую игру. И Фриск хохочет."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает угадать блюдо. И Фриск играет с удовольствием."
        else:
            "Седрик пробует, но Фриск вежливо отказывается."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Фриском."
        else:
            "[attacker_name] не может развеселить Фриска."
    return


label play_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис предлагает Иззи простую игру. И она впервые смеётся без стеснения."
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель предлагает игру. И Иззи смеётся."
        else:
            "Азриель пробует, но Иззи кивает из вежливости."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает «кто громче рычит». Иззи сначала смущается, потом хохочет."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает игру. И Иззи расслабляется."
        else:
            "Фриск пробует, но Иззи стесняется."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает весёлую игру. И Иззи смеётся искренне."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает игру. И Иззи играет с удовольствием."
        else:
            "Седрик пробует, но Иззи кивает и убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Иззи."
        else:
            "[attacker_name] не может развеселить Иззи."
    return


label play_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис предлагает игру. И Кловер включается без шуток."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель предлагает игру. И Кловер искренне веселится."
        else:
            "Азриель пробует, но Кловер улыбается и уходит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает игру. И Кловер включается без ехидства."
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает игру. И Кловер хохочет."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи предлагает игру. И Кловер впервые играет без шуток."
        else:
            "Иззи робеет, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает игру. И Кловер включается."
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Кловер."
        else:
            "[attacker_name] не может развеселить Кловер."
    return


label play_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис предлагает Седрику игру. И тот впервые за день садится."
        else:
            "Крис пробует, но Седрик уходит к делам."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель предлагает игру. И Седрик садится играть."
        else:
            "Азриель пробует, но Седрик вежливо отказывается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает игру. И Седрик неожиданно включается."
        else:
            "Чара пробует, но Седрик уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает игру. И Седрик улыбается искренне."
        else:
            "Фриск пробует, но Седрик отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи предлагает игру. И Седрик играет с удовольствием."
        else:
            "Иззи робеет, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает игру. И Седрик включается без дел."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Седриком."
        else:
            "[attacker_name] не может развеселить Седрика."
    return


label play_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] играет с [target.name]."
    else:
        "[attacker_name] не может развеселить [target.name]."
    return


label play_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                # Даёт прогресс пощады от социализации и +10% к бонус атаке и +15% к крит шансу
                $ _soc = getattr(attacker, "socialization", 0)
                $ _add = max(0, int(round(_soc * dip_multiply)))
                $ target.spare_progress = min(target.spare_progress + _add, target.spare_max)
                $ trevor_mod_stat(target, "attack", 0.10)
                $ trevor_mod_stat(target, "critrate", 0.15)
                $ renpy.notify("Игра увлекла Тревора: +10% атаки, +15% крит. шанса!")
            else:
                $ trevor_mod_stat(target, "attack", 0.10)
                $ trevor_mod_stat(target, "critrate", 0.15)
                $ renpy.notify("Тревор взвинчен: +10% атаки, +15% крит. шанса!")
        elif attacker_name == "Азриель" and ((_m == "neutral") or (_r == "peace" and _s >= 2) or (_r == "rivalry" and _m == "happy")):
            if try_to_nego_result:
                $ trevor_mod_stat(target, "speed", 0.10)
                $ renpy.notify("Тревор ускоряется: скорость +10%")
            else:
                $ trevor_mod_stat(target, "speed", 0.20)
                $ renpy.notify("Тревор ускоряется: скорость +20%")
        call play_enemy_trevor(attacker_name, target) from _call_play_trevor
    elif target.name == "Джевил":
        call play_enemy_jevil(attacker_name, target) from _call_play_jevil
    else:
        call play_enemy_generic(attacker_name, target) from _call_play_eg
    return


label play_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис предлагает Тревору сыграть в простую игру на телефоне. И Тревор неожиданно соглашается."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара предлагает «кто дальше плюнет». Тревор фыркает и включается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель предлагает лёгкую игру. И Тревор неожиданно играет."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск предлагает игру. И Тревор включается."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко предлагает игру. И Тревор неожиданно соглашается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер предлагает игру. И Тревор фыркает, но играет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик предлагает угадать блюдо. И Тревор нехотя включается."
            else:
                "Седрик пробует, но Тревор отказывается."
        else:
            if try_to_nego_result:
                "[attacker_name] играет с Тревором."
            else:
                "[attacker_name] не может развеселить Тревора."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис предлагает Тревору сыграть в простую игру на телефоне. И Тревор неожиданно соглашается."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара предлагает «кто дальше плюнет». Тревор фыркает и включается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель предлагает лёгкую игру. И Тревор неожиданно играет."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск предлагает игру. И Тревор включается."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко предлагает игру. И Тревор неожиданно соглашается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер предлагает игру. И Тревор фыркает, но играет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик предлагает угадать блюдо. И Тревор нехотя включается."
            else:
                "Седрик пробует, но Тревор отказывается."
        else:
            if try_to_nego_result:
                "[attacker_name] играет с Тревором."
            else:
                "[attacker_name] не может развеселить Тревора."


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
                "Крис предлагает Тревору сыграть в простую игру на телефоне. И Тревор неожиданно соглашается."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара предлагает «кто дальше плюнет». Тревор фыркает и включается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель предлагает лёгкую игру. И Тревор неожиданно играет."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск предлагает игру. И Тревор включается."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко предлагает игру. И Тревор неожиданно соглашается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер предлагает игру. И Тревор фыркает, но играет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик предлагает угадать блюдо. И Тревор нехотя включается."
            else:
                "Седрик пробует, но Тревор отказывается."
        else:
            if try_to_nego_result:
                "[attacker_name] играет с Тревором."
            else:
                "[attacker_name] не может развеселить Тревора."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис предлагает Тревору сыграть в простую игру на телефоне. И Тревор неожиданно соглашается."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара предлагает «кто дальше плюнет». Тревор фыркает и включается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель предлагает лёгкую игру. И Тревор неожиданно играет."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск предлагает игру. И Тревор включается."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко предлагает игру. И Тревор неожиданно соглашается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер предлагает игру. И Тревор фыркает, но играет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик предлагает угадать блюдо. И Тревор нехотя включается."
            else:
                "Седрик пробует, но Тревор отказывается."
        else:
            if try_to_nego_result:
                "[attacker_name] играет с Тревором."
            else:
                "[attacker_name] не может развеселить Тревора."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label play_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис предлагает Джевилу игру. И он впервые играет без загадок."
        else:
            "Крис пробует, но Джевил кружится."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара предлагает Джевилу «кто громче хохочет». И он неожиданно участвует."
        else:
            "Чара пробует, но Джевил исчезает."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель предлагает игру. И Джевил замирает, но участвует."
        else:
            "Азриель пробует, но Джевил хохочет."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск предлагает игру. И Джевил включается без исчезновений."
        else:
            "Фриск пробует, но Джевил уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко предлагает игру. И Джевил неожиданно соглашается."
        else:
            "Иззи смущается, и Джевил исчезает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер предлагает игру. И Джевил участвует без загадок."
        else:
            "Кловер пробует, но Джевил хохочет."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик предлагает угадать блюдо. И Джевил садится играть."
        else:
            "Седрик пробует, но Джевил уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] играет с Джевилом."
        else:
            "[attacker_name] не может развеселить Джевила."
    return


label play_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] играет с [target.name]."
    else:
        "[attacker_name] не может развеселить [target.name]."
    return