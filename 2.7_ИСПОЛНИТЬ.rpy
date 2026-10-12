# =====================================================================
#  2.7_ИСПОЛНИТЬ.rpy — действие «Исполнение»
# =====================================================================



label perform_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call perform_hero_self(attacker_name, target) from _call_perform_self
        return
    if target.name == "Крис":
        call perform_hero_kris(attacker_name, target) from _call_perform_kris
    elif target.name == "Азриель":
        call perform_hero_azriel(attacker_name, target) from _call_perform_az
    elif target.name == "Чара":
        call perform_hero_chara(attacker_name, target) from _call_perform_chara
    elif target.name == "Фриск":
        call perform_hero_frisk(attacker_name, target) from _call_perform_frisk
    elif target.name == "Иззи":
        call perform_hero_izzy(attacker_name, target) from _call_perform_izzy
    elif target.name == "Кловер":
        call perform_hero_clover(attacker_name, target) from _call_perform_clover
    elif target.name == "Седрик":
        call perform_hero_sedric(attacker_name, target) from _call_perform_sedric
    else:
        call perform_hero_generic(attacker_name, target) from _call_perform_hg
    return


label perform_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис вполголоса напевает что-то. Странно, но это помогает отвлечься."
        else:
            "Крис пытается что-то изобразить, но голос срывается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет короткую мелодию на воображаемом пианино. И улыбается."
        else:
            "Азриель пытается, но фальшивит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара напевает что-то агрессивное, но с настоящей душой."
        else:
            "Чара пытается выступить, но злость мешает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск тихо напевает колыбельную — и сама успокаивается."
        else:
            "Фриск пытается, но голос слабый."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи неуверенно напевает. И впервые не боится, что услышат."
        else:
            "Иззи стесняется даже собственного голоса."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает ковбойское шоу. Сама себе аплодирует."
        else:
            "Кловер пробует, но выходит натянуто."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает кухонную песенку — и правда становится легче."
        else:
            "Седрик пытается, но мысли о делах мешают."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает сам перед собой и отвлекается."
        else:
            "[attacker_name] не может выступить."
    return


label perform_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет старую мелодию. Крис вспоминает детство и впервые за день расслабляется."
        else:
            "Азриель пробует, но Крис только вежливо улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет что-то агрессивное и честное. Крис неожиданно включается."
        else:
            "Чара пробует, но Крис не в настроении."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт колыбельную. И Крис выдыхает."
        else:
            "Фриск пробует, но Крис отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи неуверенно напевает. И Крис неожиданно улыбается."
        else:
            "Иззи стесняется, и Крис вежливо отказывается."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает ковбойское шоу. Крис смеётся."
        else:
            "Кловер пробует, но Крис не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает кухонную песенку. И Крис улыбается."
        else:
            "Седрик пробует, но Крис уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Крисом."
        else:
            "[attacker_name] не может впечатлить Криса."
    return


label perform_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис напевает что-то простое. И Азриель искренне улыбается."
        else:
            "Крис пробует, но Азриель вежливо улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет что-то резкое. И Азриель впервые смеётся без маски."
        else:
            "Чара пробует, но Азриель держит лицо."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт. И Азриель слушает заворожённо."
        else:
            "Фриск пробует, но Азриель вежливо уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи поёт. И Азриель улыбается искренне."
        else:
            "Иззи стесняется, и Азриель вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает шоу. Азриель хохочет."
        else:
            "Кловер пробует, но Азриель улыбается вежливо."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает. И Азриель расслабляется."
        else:
            "Седрик пробует, но Азриель уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Азриелем."
        else:
            "[attacker_name] не может впечатлить Азриеля."
    return


label perform_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис напевает что-то. И Чара неожиданно улыбается."
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет мелодию. И Чара замирает."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт. И Чара неожиданно включается."
        else:
            "Фриск пробует, но Чара холодна."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи поёт. И Чара неожиданно смягчается."
        else:
            "Иззи робеет, и Чара отходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает шоу. Чара смеётся — впервые за день."
        else:
            "Кловер пробует, но Чара не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает. И Чара нехотя улыбается."
        else:
            "Седрик пробует, но Чара отказывается."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Чарой."
        else:
            "[attacker_name] не может впечатлить Чару."
    return


label perform_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис поёт. И Фриск искренне улыбается."
        else:
            "Крис пробует, но Фриск вежливо уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет. И Фриск слушает заворожённо."
        else:
            "Азриель пробует, но Фриск вежливо отказывается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет резкую песню. Фриск неожиданно включается."
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи поёт. И Фриск улыбается искренне."
        else:
            "Иззи робеет, и Фриск вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает шоу. Фриск хохочет."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает. И Фриск расслабляется."
        else:
            "Седрик пробует, но Фриск вежливо уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Фриском."
        else:
            "[attacker_name] не может впечатлить Фриска."
    return


label perform_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис напевает. И Иззи смеётся без стеснения."
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет. И Иззи слушает с восхищением."
        else:
            "Азриель пробует, но Иззи кивает вежливо."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет что-то громкое. Иззи сначала смущается, потом хохочет."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт. И Иззи расслабляется."
        else:
            "Фриск пробует, но Иззи стесняется."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает шоу. Иззи смеётся искренне."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает. И Иззи поёт вместе с ним."
        else:
            "Седрик пробует, но Иззи убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Иззи."
        else:
            "[attacker_name] не может впечатлить Иззи."
    return


label perform_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис напевает. И Кловер подхватывает."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет. И Кловер заворожённо слушает."
        else:
            "Азриель пробует, но Кловер улыбается и уходит."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет резкую песню. Кловер включается."
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт. И Кловер хохочет."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи поёт. И Кловер впервые слушает без шуток."
        else:
            "Иззи робеет, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает. И Кловер подхватывает."
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Кловер."
        else:
            "[attacker_name] не может впечатлить Кловер."
    return


label perform_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис напевает. И Седрик впервые присаживается."
        else:
            "Крис пробует, но Седрик уходит к делам."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет. И Седрик садится слушать."
        else:
            "Азриель пробует, но Седрик вежливо отказывается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет что-то громкое. Седрик включается."
        else:
            "Чара пробует, но Седрик уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт. И Седрик улыбается искренне."
        else:
            "Фриск пробует, но Седрик отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи поёт. И Седрик поёт вместе с ней."
        else:
            "Иззи робеет, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает шоу. Седрик смеётся."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Седриком."
        else:
            "[attacker_name] не может впечатлить Седрика."
    return


label perform_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] выступает перед [target.name]."
    else:
        "[attacker_name] не может впечатлить [target.name]."
    return


label perform_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ renpy.notify("Тревор раздражён выступлением: пощада -0.5 дипломатии")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ renpy.notify("Ужасное выступление: пощада -1.0 дипломатии")
        call perform_enemy_trevor(attacker_name, target) from _call_perform_trevor
    elif target.name == "Джевил":
        call perform_enemy_jevil(attacker_name, target) from _call_perform_jevil
    else:
        call perform_enemy_generic(attacker_name, target) from _call_perform_eg
    return


label perform_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис напевает что-то простое. И Тревор неожиданно слушает."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара исполняет резкое. И Тревор впервые улыбается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель играет мелодию. И Тревор замирает."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск поёт. И Тревор слушает."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи поёт робко. И Тревор неожиданно улыбается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер изображает шоу. Тревор хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик напевает кухонную. И Тревор улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] выступает перед Тревором."
            else:
                "[attacker_name] не может впечатлить Тревора."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис напевает что-то простое. И Тревор неожиданно слушает."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара исполняет резкое. И Тревор впервые улыбается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель играет мелодию. И Тревор замирает."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск поёт. И Тревор слушает."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи поёт робко. И Тревор неожиданно улыбается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер изображает шоу. Тревор хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик напевает кухонную. И Тревор улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] выступает перед Тревором."
            else:
                "[attacker_name] не может впечатлить Тревора."


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
                "Крис напевает что-то простое. И Тревор неожиданно слушает."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара исполняет резкое. И Тревор впервые улыбается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель играет мелодию. И Тревор замирает."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск поёт. И Тревор слушает."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи поёт робко. И Тревор неожиданно улыбается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер изображает шоу. Тревор хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик напевает кухонную. И Тревор улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] выступает перед Тревором."
            else:
                "[attacker_name] не может впечатлить Тревора."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис напевает что-то простое. И Тревор неожиданно слушает."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара исполняет резкое. И Тревор впервые улыбается."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель играет мелодию. И Тревор замирает."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск поёт. И Тревор слушает."
            else:
                "Фриск пробует, но Тревор отказывается."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи поёт робко. И Тревор неожиданно улыбается."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер изображает шоу. Тревор хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик напевает кухонную. И Тревор улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] выступает перед Тревором."
            else:
                "[attacker_name] не может впечатлить Тревора."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label perform_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис напевает. И Джевил неожиданно замирает."
        else:
            "Крис пробует, но Джевил исчезает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара исполняет резкое. И Джевил хохочет — но не зло."
        else:
            "Чара пробует, но Джевил уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель играет. И Джевил впервые слушает."
        else:
            "Азриель пробует, но Джевил кружится."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск поёт. И Джевил не исчезает."
        else:
            "Фриск пробует, но Джевил уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи поёт робко. И Джевил улыбается искренне."
        else:
            "Иззи смущается, и Джевил исчезает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер изображает шоу. И Джевил отвечает тем же."
        else:
            "Кловер пробует, но Джевил отмахивается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик напевает. И Джевил садится слушать."
        else:
            "Седрик пробует, но Джевил уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] выступает перед Джевилом."
        else:
            "[attacker_name] не может впечатлить Джевила."
    return


label perform_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] выступает перед [target.name]."
    else:
        "[attacker_name] не может впечатлить [target.name]."
    return