# =====================================================================
#  2.9_ДРАЗНИТЬ.rpy — действие «Дразнить»
# =====================================================================




label tease_hero_reaction(attacker_name, target):
    if target.name == attacker_name:
        call tease_hero_self(attacker_name, target) from _call_tease_self
        return
    if target.name == "Крис":
        call tease_hero_kris(attacker_name, target) from _call_tease_kris
    elif target.name == "Азриель":
        call tease_hero_azriel(attacker_name, target) from _call_tease_az
    elif target.name == "Чара":
        call tease_hero_chara(attacker_name, target) from _call_tease_chara
    elif target.name == "Фриск":
        call tease_hero_frisk(attacker_name, target) from _call_tease_frisk
    elif target.name == "Иззи":
        call tease_hero_izzy(attacker_name, target) from _call_tease_izzy
    elif target.name == "Кловер":
        call tease_hero_clover(attacker_name, target) from _call_tease_clover
    elif target.name == "Седрик":
        call tease_hero_sedric(attacker_name, target) from _call_tease_sedric
    else:
        call tease_hero_generic(attacker_name, target) from _call_tease_hg
    return


label tease_hero_self(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает сам себя: «Ну что, герой, опять спать не будешь?» И неожиданно улыбается."
        else:
            "Крис пытается себя развеселить, но грусть сильнее."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает себя: «Ну, ваше высочество, опять всех спасли?» И смеётся над собой."
        else:
            "Азриель пробует, но маска держится."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара зло шутит над собой: «Злюка, опять всех разогнала.» И впервые смеётся."
        else:
            "Чара пробует, но злость гасит шутку."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает себя: «Ну что, спасатель, кого сегодня вытащил?» И улыбается."
        else:
            "Фриск пробует, но привычка держать лицо мешает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко подкалывает себя: «Ну что, вечно краснеешь…» И впервые смеётся."
        else:
            "Иззи не получается себя развеселить."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает себя: «Снайпер, ты вообще попадаешь?» И сама хохочет."
        else:
            "Кловер шутит, но не весело."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает себя: «Ну что, шеф, опять всё на себе тащишь?» И улыбается."
        else:
            "Седрик пробует, но мысли о делах перебивают."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит себя."
        else:
            "[attacker_name] не может развеселить себя."
    return


label tease_hero_kris(attacker_name, target):
    if attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает Криса: «Спать не пробовал? Говорят, помогает.» Крис фыркает — и впервые за день смеётся."
        else:
            "Азриель пробует, но Крис не реагирует."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Ну что, зомби, до рассвета опять?» Крис усмехается."
        else:
            "Чара пробует, но Крис закрывается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает мягко: «Ты вообще отдыхаешь, или ты робот?» Крис улыбается."
        else:
            "Фриск пробует, но Крис не реагирует."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко подкалывает: «Крис… ты… спишь хоть иногда?..» И он смеётся."
        else:
            "Иззи смущается, и Крис вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Шеф, а ты вообще видел свою кровать за последнюю неделю?» Крис хохочет."
        else:
            "Кловер пробует, но Крис уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Крис, ты поел хоть раз сегодня, или всё грустишь?» Крис улыбается."
        else:
            "Седрик пробует, но Крис отмахивается."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Криса."
        else:
            "[attacker_name] не может развеселить Криса."
    return


label tease_hero_azriel(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает: «Принц, а улыбку на ночь снимаешь?» Азриель смеётся."
        else:
            "Крис пробует, но Азриель вежлив."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Ну что, принц, корона не жмёт?» Азриель фыркает."
        else:
            "Чара пробует, но Азриель держит лицо."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает: «Ты когда последний раз отдыхал, ваше высочество?» Азриель смеётся."
        else:
            "Фриск пробует, но Азриель вежлив."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко подкалывает: «Азриель… ты… ты не устал улыбаться?..» И он смеётся."
        else:
            "Иззи смущается, и Азриель вежлив."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Ваше высочество, а принц вообще спит? Или вы так — по расписанию?» Азриель хохочет."
        else:
            "Кловер пробует, но Азриель вежлив."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Азриель, ты поел хоть раз не из вежливости?» И тот смеётся."
        else:
            "Седрик пробует, но Азриель уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Азриеля."
        else:
            "[attacker_name] не может развеселить Азриеля."
    return


label tease_hero_chara(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает: «Чара, ты улыбаться умеешь, или это не по уставу?» Она фыркает и впервые смеётся."
        else:
            "Крис пробует, но Чара отмахивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает мягко: «Чара, а ты вообще когда-нибудь расслабляешься?» Она неожиданно улыбается."
        else:
            "Азриель пробует, но Чара фыркает."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает: «Чара, а ты бываешь не злая? Хоть иногда?» И Чара смеётся."
        else:
            "Фриск пробует, но Чара холодна."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко подкалывает: «Чара… ты… ты не такая страшная, как хочешь казаться…» Чара фыркает, но не злится."
        else:
            "Иззи смущается, и Чара отходит."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Чара, а ты умеешь улыбаться или только щуриться?» Чара хохочет."
        else:
            "Кловер пробует, но Чара не реагирует."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Чара, ты злая, потому что голодная. Я знаю.» Она смеётся."
        else:
            "Седрик пробует, но Чара уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Чару."
        else:
            "[attacker_name] не может развеселить Чару."
    return


label tease_hero_frisk(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает: «Фриск, ты вообще отдыхаешь, или ты тоже робот?» И она смеётся."
        else:
            "Крис пробует, но Фриск уходит."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает мягко: «Фриск, а у тебя вообще есть режим «не спасать»?» Она смеётся."
        else:
            "Азриель пробует, но Фриск вежлива."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Фриск, а ты вообще бываешь слабой? Или только для других?» Фриск хохочет."
        else:
            "Чара пробует, но Фриск закрывается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи подкалывает робко: «Фриск… ты… ты не устал(а) быть сильным?..» Фриск смеётся."
        else:
            "Иззи смущается, и Фриск вежлива."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Фриск, а ты вообще отдыхаешь или только спасаешь мир?» Фриск хохочет."
        else:
            "Кловер пробует, но Фриск уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Фриск, ты поел(а) или опять забыл(а)?» И она смеётся."
        else:
            "Седрик пробует, но Фриск вежлива."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Фриска."
        else:
            "[attacker_name] не может развеселить Фриска."
    return


label tease_hero_izzy(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает мягко: «Иззи, ты вообще когда-нибудь перестаёшь стесняться?» Она смеётся."
        else:
            "Крис пробует, но Иззи смущается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает: «Иззи, а ты вообще бываешь не милой?» Она хохочет."
        else:
            "Азриель пробует, но Иззи вежливо кивает."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Иззи, ну сколько можно краснеть!» Иззи неожиданно хохочет."
        else:
            "Чара пробует, но Иззи зажимается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает: «Иззи, ты вообще умеешь злиться? Или только стесняться?» Иззи смеётся."
        else:
            "Фриск пробует, но Иззи стесняется."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Солнце, ты краснеешь даже когда спишь?» Иззи хохочет."
        else:
            "Кловер пробует, но Иззи смущается."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Иззи, чай будешь, или опять убежишь?» Она смеётся."
        else:
            "Седрик пробует, но Иззи убегает."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Иззи."
        else:
            "[attacker_name] не может развеселить Иззи."
    return


label tease_hero_clover(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает: «Кловер, ты вообще серьёзной бываешь?» Она фыркает и смеётся."
        else:
            "Крис пробует, но Кловер отшучивается."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает: «Кловер, а что если шутки закончатся?» Она хохочет."
        else:
            "Азриель пробует, но Кловер улыбается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Кловер, а под шутками что?» Кловер сначала смеётся, потом задумывается."
        else:
            "Чара пробует, но Кловер отмахивается."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает: «Кловер, а ты грустить умеешь?» Она неожиданно перестаёт улыбаться и кивает."
        else:
            "Фриск пробует, но Кловер уходит."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко подкалывает: «Кловер… ты… ты устаёшь шутить?..» Кловер мягко улыбается: «Иногда.»"
        else:
            "Иззи смущается, и Кловер шутит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Кловер, ты хоть когда-нибудь без пистолета ходишь?» Она смеётся."
        else:
            "Седрик пробует, но Кловер уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Кловер."
        else:
            "[attacker_name] не может развеселить Кловер."
    return


label tease_hero_sedric(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает: «Седрик, ты вообще отдыхаешь, или только кормишь?» Седрик смеётся."
        else:
            "Крис пробует, но Седрик уходит к плите."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает: «Седрик, а ты вообще ешь то, что готовишь?» Седрик хохочет."
        else:
            "Азриель пробует, но Седрик отмахивается."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Седрик, а фартук вообще снимаешь?» Он смеётся."
        else:
            "Чара пробует, но Седрик уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает: «Седрик, а ты вообще когда-нибудь садишься?» Он смеётся и садится."
        else:
            "Фриск пробует, но Седрик отмахивается."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи подкалывает: «Седрик… ты… ты вообще спишь?..» И он смеётся, а потом задумывается."
        else:
            "Иззи смущается, и Седрик успокаивает её."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Седрик, а ты по ночам не готовишь во сне?» Он хохочет."
        else:
            "Кловер пробует, но Седрик уходит."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Седрика."
        else:
            "[attacker_name] не может развеселить Седрика."
    return


label tease_hero_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] дразнит [target.name]."
    else:
        "[attacker_name] не может развеселить [target.name]."
    return


label tease_enemy_reaction(attacker_name, target):
    if target.name == "Тревор":
        $ _r = getattr(target, "route", None)
        $ _s = getattr(target, "route_stage", 1)
        $ _m = getattr(target, "mood", "neutral")
        if _r == "rivalry" and _m == "angry":
            if try_to_nego_result:
                $ trevor_mod_stat(target, "speed", 0.10)
                $ renpy.notify("Тревор подстёгнут: скорость +10%")
            else:
                $ trevor_mod_stat(target, "speed", 0.20)
                $ renpy.notify("Тревор разъярён: скорость +20%")
        elif _m == "neutral" and _r is None:
            if try_to_nego_result:
                $ trevor_mod_stat(target, "critdmg", 0.10)
                $ trevor_mod_stat(target, "attack", 0.10)
                $ renpy.notify("Тревор задет: +10% крит. урона, +10% атаки")
            else:
                $ trevor_mod_stat(target, "critdmg", 0.20)
                $ trevor_mod_stat(target, "attack", 0.20)
                $ renpy.notify("Тревор зол: +20% крит. урона, +20% атаки")
        elif (_r == "peace" and _s == 2) or (_r == "rivalry" and _m == "happy"):
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ trevor_mod_stat(target, "attack", 0.10)
                $ renpy.notify("Дразнить разозлило: пощада -0.5 дипл., атака +10%")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ trevor_mod_stat(target, "attack", 0.20)
                $ renpy.notify("Провал издёвки: пощада -1.0 дипл., атака +20%")
        elif _r == "peace" and _s >= 3:
            if try_to_nego_result:
                $ trevor_rollback_spare(target, attacker_name, 0.5)
                $ renpy.notify("Тревор уходит в себя: пощада -0.5 дипл.")
            else:
                $ trevor_rollback_spare(target, attacker_name, 1.0)
                $ renpy.notify("Тревор закрывается: пощада -1.0 дипл.")
        call tease_enemy_trevor(attacker_name, target) from _call_tease_trevor
    elif target.name == "Джевил":
        call tease_enemy_jevil(attacker_name, target) from _call_tease_jevil
    else:
        call tease_enemy_generic(attacker_name, target) from _call_tease_eg
    return


label tease_enemy_trevor(attacker_name, target):
    if target.mood == "neutral":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис подкалывает Тревора: «Прогулы — это твоя новая специальность?» Тревор фыркает, но впервые без агрессии."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара подкалывает: «Тревор, а ты вообще на парах бываешь, или ты миф?» Он неожиданно смеётся."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель подкалывает мягко: «Тревор, а ты вообще умеешь улыбаться?» Он фыркает, но улыбается."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск подкалывает: «Тревор, а ты ночуешь-то где?» Он неожиданно смеётся."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко подкалывает: «Тревор… ты… ты вообще ешь?..» И он смеётся."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер подкалывает: «Мистер Тревор, вы вообще бываете в институте?» Он хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик подкалывает: «Тревор, ты поел хоть раз за неделю?» Он улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] дразнит Тревора."
            else:
                "[attacker_name] не может развеселить Тревора."

    elif target.mood == "angry":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис подкалывает Тревора: «Прогулы — это твоя новая специальность?» Тревор фыркает, но впервые без агрессии."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара подкалывает: «Тревор, а ты вообще на парах бываешь, или ты миф?» Он неожиданно смеётся."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель подкалывает мягко: «Тревор, а ты вообще умеешь улыбаться?» Он фыркает, но улыбается."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск подкалывает: «Тревор, а ты ночуешь-то где?» Он неожиданно смеётся."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко подкалывает: «Тревор… ты… ты вообще ешь?..» И он смеётся."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер подкалывает: «Мистер Тревор, вы вообще бываете в институте?» Он хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик подкалывает: «Тревор, ты поел хоть раз за неделю?» Он улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] дразнит Тревора."
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
                "Крис подкалывает Тревора: «Прогулы — это твоя новая специальность?» Тревор фыркает, но впервые без агрессии."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара подкалывает: «Тревор, а ты вообще на парах бываешь, или ты миф?» Он неожиданно смеётся."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель подкалывает мягко: «Тревор, а ты вообще умеешь улыбаться?» Он фыркает, но улыбается."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск подкалывает: «Тревор, а ты ночуешь-то где?» Он неожиданно смеётся."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко подкалывает: «Тревор… ты… ты вообще ешь?..» И он смеётся."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер подкалывает: «Мистер Тревор, вы вообще бываете в институте?» Он хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик подкалывает: «Тревор, ты поел хоть раз за неделю?» Он улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] дразнит Тревора."
            else:
                "[attacker_name] не может развеселить Тревора."

    elif target.mood == "happy":
        if attacker_name == "Крис":
            if try_to_nego_result:
                "Крис подкалывает Тревора: «Прогулы — это твоя новая специальность?» Тревор фыркает, но впервые без агрессии."
            else:
                "Крис пробует, но Тревор отмахивается."
        elif attacker_name == "Чара":
            if try_to_nego_result:
                "Чара подкалывает: «Тревор, а ты вообще на парах бываешь, или ты миф?» Он неожиданно смеётся."
            else:
                "Чара пробует, но Тревор уходит."
        elif attacker_name == "Азриель":
            if try_to_nego_result:
                "Азриель подкалывает мягко: «Тревор, а ты вообще умеешь улыбаться?» Он фыркает, но улыбается."
            else:
                "Азриель пробует, но Тревор закрывается."
        elif attacker_name == "Фриск":
            if try_to_nego_result:
                "Фриск подкалывает: «Тревор, а ты ночуешь-то где?» Он неожиданно смеётся."
            else:
                "Фриск пробует, но Тревор уходит."
        elif attacker_name == "Иззи":
            if try_to_nego_result:
                "Иззи робко подкалывает: «Тревор… ты… ты вообще ешь?..» И он смеётся."
            else:
                "Иззи смущается, и Тревор уходит."
        elif attacker_name == "Кловер":
            if try_to_nego_result:
                "Кловер подкалывает: «Мистер Тревор, вы вообще бываете в институте?» Он хохочет."
            else:
                "Кловер пробует, но Тревор не реагирует."
        elif attacker_name == "Седрик":
            if try_to_nego_result:
                "Седрик подкалывает: «Тревор, ты поел хоть раз за неделю?» Он улыбается."
            else:
                "Седрик пробует, но Тревор уходит."
        else:
            if try_to_nego_result:
                "[attacker_name] дразнит Тревора."
            else:
                "[attacker_name] не может развеселить Тревора."

    else:
        if try_to_nego_result:
            "[attacker_name] действует на Тревора."
        else:
            "[attacker_name] не находит в Треворе отклика."

    return


label tease_enemy_jevil(attacker_name, target):
    if attacker_name == "Крис":
        if try_to_nego_result:
            "Крис подкалывает: «Джевил, а ты вообще умеешь не хихикать?» И тот впервые фыркает по-человечески."
        else:
            "Крис пробует, но Джевил кружится."
    elif attacker_name == "Чара":
        if try_to_nego_result:
            "Чара подкалывает: «Джевил, а загадки — это твоя работа или ты просто боишься прямых вопросов?» Он замирает, потом смеётся."
        else:
            "Чара пробует, но Джевил хохочет."
    elif attacker_name == "Азриель":
        if try_to_nego_result:
            "Азриель подкалывает: «Джевил, а серьёзным быть пробовал?» Он фыркает, но не исчезает."
        else:
            "Азриель пробует, но Джевил уходит."
    elif attacker_name == "Фриск":
        if try_to_nego_result:
            "Фриск подкалывает: «Джевил, а ты вообще умеешь не исчезать?» Он неожиданно отвечает прямо."
        else:
            "Фриск пробует, но Джевил исчезает."
    elif attacker_name == "Иззи":
        if try_to_nego_result:
            "Иззи робко подкалывает: «Джевил… ты… ты вообще умеешь просто стоять?..» И он смеётся по-доброму."
        else:
            "Иззи смущается, и Джевил исчезает."
    elif attacker_name == "Кловер":
        if try_to_nego_result:
            "Кловер подкалывает: «Джевил, а у тебя в контракте прописано «только загадками»?» Он хохочет и отвечает прямо."
        else:
            "Кловер пробует, но Джевил уходит."
    elif attacker_name == "Седрик":
        if try_to_nego_result:
            "Седрик подкалывает: «Джевил, а ты голодный, или просто так кружишься?» Он смеётся и садится."
        else:
            "Седрик пробует, но Джевил исчезает."
    else:
        if try_to_nego_result:
            "[attacker_name] дразнит Джевила."
        else:
            "[attacker_name] не может развеселить Джевила."
    return


label tease_enemy_generic(attacker_name, target):
    if try_to_nego_result:
        "[attacker_name] дразнит [target.name]."
    else:
        "[attacker_name] не может развеселить [target.name]."
    return