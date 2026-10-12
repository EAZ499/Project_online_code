# ============================================================================
# «СЫГРАЕМ!» — МИНИ-ИГРЫ КЛОВЕРА
# ----------------------------------------------------------------------------
# Магия «Сыграем!» ур.1 даёт сыграть на выбор в одну из игр, где Кловер обязан
# поставить ставку в виде своих бонусных характеристик.
#
#   Покер           — Техасский покер, максимальная ставка 25%.
#   Слоты           — до 7 монет по 3% от случайной характеристики.
#   Русская рулетка — Кловер выбирает число пуль (до 6), урон =
#                     магия * 40% * кол-во пуль.
#   Рулетка         — ставка до 12% от двух характеристик, двойной выигрыш.
#   Дайсы           — угадать значения на 3 кубах d6, ставка до 20%.
#   КНБ             — камень-ножницы-бумага до 3 побед, ставка до 40%.
#
# Ставка списывается из бонусных характеристик (bonus_*). При проигрыше
# характеристика уходит в минус — это и есть «потеря бонусных характеристик».
# ============================================================================

default clover_gamble_game = None
default clover_gamble_stake = 0.0
default clover_gamble_log = ""
default clover_gamble_done = False
default clover_gamble_dice = []
default clover_gamble_guess = []
default clover_gamble_rps_score = [0, 0]
default clover_gamble_rps_round = 0
default clover_gamble_coin_count = 0
default clover_gamble_bullets = 3
default clover_gamble_shot_result = None

init python:
    # Ставка выражается долей выбранной характеристики.
    CLOVER_GAMBLE_STAT_FIELDS = {
        "атака": "bonus_atk",
        "защита": "bonus_def",
        "магия": "bonus_magic",
        "точность": "bonus_dmgchance",
        "крит шанс": "bonus_critrate",
        "крит урон": "bonus_crit",
    }

    def clover_gamble_stat_names():
        return list(CLOVER_GAMBLE_STAT_FIELDS.keys())

    def clover_gamble_stake_field(stat_name):
        return CLOVER_GAMBLE_STAT_FIELDS.get(stat_name, "bonus_dmgchance")

    def clover_gamble_get(stat_name):
        char = clover_char()
        if char is None:
            return 0.0
        field = clover_gamble_stake_field(stat_name)
        return float(getattr(char, field, 0.0) or 0.0)

    def clover_gamble_take(stat_name, amount):
        """Списывает ставку из бонусной характеристики."""
        char = clover_char()
        if char is None:
            return 0.0
        field = clover_gamble_stake_field(stat_name)
        current = float(getattr(char, field, 0.0) or 0.0)
        setattr(char, field, current - amount)
        return amount

    def clover_gamble_give(stat_name, amount):
        """Начисляет выигрыш в бонусную характеристику."""
        char = clover_char()
        if char is None:
            return 0.0
        field = clover_gamble_stake_field(stat_name)
        current = float(getattr(char, field, 0.0) or 0.0)
        setattr(char, field, current + amount)
        return amount

    def clover_gamble_money_stake(stat_name, max_ratio):
        """Считает денежный эквивалент максимальной ставки (для казино)."""
        return int(abs(clover_gamble_get(stat_name)) * max_ratio * 100)

    def clover_gamble_finish(won, stat_name, stake_amount, message):
        """Завершает игру: применяет результат, удачу/сглаз и долю казино."""
        store.clover_gamble_log = message
        store.clover_gamble_done = True
        # «Делу - время, потехе - час»: игра сыграна — дебафф «игроман» снят.
        clover_clear_gambler_debuff()
        # «Ставка на удачу» ур.4: выигрыш 3 удачи, проигрыш 4 сглаза.
        clover_apply_bet_result(won)
        # «Проценты с казино» ур.3: команда делит 25% от игр.
        money = clover_gamble_money_stake(stat_name, abs(stake_amount))
        clover_casino_share(money if won else -money)
        renpy.restart_interaction()
        return won


# ============================================================================
# ЭКРАН ВЫБОРА ИГРЫ
# ============================================================================

screen clover_gamble_screen():
    modal True
    zorder 100

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 640
        background "#1a1a1aee"

        vbox:
            spacing 12
            xalign 0.5
            yalign 0.5

            text "Сыграем!" size 44 color "#ffd700" xalign 0.5
            text "Бонусные характеристики Кловера — это ставка." size 22 color "#aaaaaa" xalign 0.5

            null height 8

            if clover_gamble_game is None:
                # ------------------ ВЫБОР ИГРЫ ------------------
                text "Выбери игру:" size 28 color "#ffffff" xalign 0.5

                for _game, _max in CLOVER_GAME_STAKES.items():
                    textbutton "[_game]  (макс. ставка [int(_max * 100)]%)":
                        text_size 26
                        xalign 0.5
                        action [
                            SetVariable("clover_gamble_game", _game),
                            SetVariable("clover_gamble_log", ""),
                            SetVariable("clover_gamble_done", False),
                            SetVariable("clover_gamble_stake", _max),
                            SetVariable("clover_gamble_dice", []),
                            SetVariable("clover_gamble_guess", []),
                            SetVariable("clover_gamble_rps_score", [0, 0]),
                            SetVariable("clover_gamble_rps_round", 0),
                            SetVariable("clover_gamble_coin_count", 0),
                            SetVariable("clover_gamble_shot_result", None),
                        ]

                null height 10
                textbutton "Выйти":
                    text_size 24
                    xalign 0.5
                    action Return(None)

            elif clover_gamble_game == "Русская рулетка":
                # ------------------ РУССКАЯ РУЛЕТКА ------------------
                text "Русская рулетка" size 32 color "#ff4444" xalign 0.5
                text "Выбери, сколько пуль будет в револьвере (макс. 6)." size 22 color "#cccccc" xalign 0.5
                text "Урон = магия Кловера * 40% * кол-во пуль" size 20 color "#888888" xalign 0.5

                hbox:
                    xalign 0.5
                    spacing 10
                    for _b in range(1, 7):
                        textbutton "[_b]":
                            text_size 28
                            action SetVariable("clover_gamble_bullets", _b)

                text "Пули: [clover_gamble_bullets]" size 24 color "#ffd700" xalign 0.5

                if clover_gamble_shot_result is None:
                    textbutton "Крутить барабан!":
                        text_size 28
                        xalign 0.5
                        action Function(clover_russian_roulette_play)
                else:
                    text "[clover_gamble_log]" size 24 color "#ffffff" xalign 0.5

                null height 10
                textbutton "Назад":
                    text_size 22
                    xalign 0.5
                    action [SetVariable("clover_gamble_game", None), SetVariable("clover_gamble_shot_result", None)]

            elif clover_gamble_game == "Слоты":
                # ------------------ СЛОТЫ ------------------
                text "Слоты" size 32 color "#ffd700" xalign 0.5
                text "Каждая монета — ставка 3% от случайной характеристики." size 22 color "#cccccc" xalign 0.5
                text "Можно кинуть до 7 монет." size 20 color "#888888" xalign 0.5

                text "Монет: [clover_gamble_coin_count] / 7" size 24 color "#ffd700" xalign 0.5

                if clover_gamble_coin_count < 7 and not clover_gamble_done:
                    textbutton "Кинуть монету":
                        text_size 26
                        xalign 0.5
                        action Function(clover_slots_drop_coin)

                if clover_gamble_coin_count > 0 and not clover_gamble_done:
                    textbutton "Крутить слоты!":
                        text_size 28
                        xalign 0.5
                        action Function(clover_slots_spin)

                if clover_gamble_done:
                    text "[clover_gamble_log]" size 24 color "#ffffff" xalign 0.5

                null height 10
                textbutton "Назад":
                    text_size 22
                    xalign 0.5
                    action [SetVariable("clover_gamble_game", None), SetVariable("clover_gamble_coin_count", 0), SetVariable("clover_gamble_done", False)]

            elif clover_gamble_game == "Дайсы":
                # ------------------ ДАЙСЫ ------------------
                text "Дайсы" size 32 color "#ffd700" xalign 0.5
                text "Угадай значения на 3 кубах d6. Ставка до 20%." size 22 color "#cccccc" xalign 0.5

                if not clover_gamble_dice:
                    text "Кубы: не брошены" size 22 color "#888888" xalign 0.5
                    textbutton "Бросить кубы":
                        text_size 26
                        xalign 0.5
                        action Function(clover_dice_roll)
                else:
                    text "Кубы: [clover_gamble_dice[0]] [clover_gamble_dice[1]] [clover_gamble_dice[2]]" size 30 color "#ffffff" xalign 0.5
                    if not clover_gamble_guess:
                        text "Твоя ставка на значения:" size 22 color "#cccccc" xalign 0.5
                        hbox:
                            xalign 0.5
                            spacing 8
                            for _g in range(1, 7):
                                textbutton "[_g]":
                                    text_size 24
                                    action Function(clover_dice_guess, _g)
                    else:
                        text "Твой выбор: [clover_gamble_guess]" size 24 color "#ffd700" xalign 0.5
                        text "[clover_gamble_log]" size 24 color "#ffffff" xalign 0.5

                null height 10
                textbutton "Назад":
                    text_size 22
                    xalign 0.5
                    action [SetVariable("clover_gamble_game", None), SetVariable("clover_gamble_dice", []), SetVariable("clover_gamble_guess", []), SetVariable("clover_gamble_done", False)]

            elif clover_gamble_game == "КНБ":
                # ------------------ КАМЕНЬ-НОЖНИЦЫ-БУМАГА ------------------
                text "Камень-ножницы-бумага" size 32 color "#ffd700" xalign 0.5
                text "Игра до 3 побед. Ставка до 40% от выбранной характеристики." size 22 color "#cccccc" xalign 0.5
                text "Счёт: Кловер [clover_gamble_rps_score[0]] — Противник [clover_gamble_rps_score[1]]" size 24 color "#ffffff" xalign 0.5

                if not clover_gamble_done:
                    hbox:
                        xalign 0.5
                        spacing 12
                        textbutton "Камень":
                            text_size 26
                            action Function(clover_rps_play, "камень")
                        textbutton "Ножницы":
                            text_size 26
                            action Function(clover_rps_play, "ножницы")
                        textbutton "Бумага":
                            text_size 26
                            action Function(clover_rps_play, "бумага")
                else:
                    text "[clover_gamble_log]" size 24 color "#ffffff" xalign 0.5

                null height 10
                textbutton "Назад":
                    text_size 22
                    xalign 0.5
                    action [SetVariable("clover_gamble_game", None), SetVariable("clover_gamble_rps_score", [0, 0]), SetVariable("clover_gamble_done", False)]

            elif clover_gamble_game == "Рулетка":
                # ------------------ РУЛЕТКА ------------------
                text "Рулетка" size 32 color "#ffd700" xalign 0.5
                text "Ставка до 12% от двух выбранных характеристик. Двойной выигрыш." size 22 color "#cccccc" xalign 0.5

                if not clover_gamble_done:
                    hbox:
                        xalign 0.5
                        spacing 12
                        textbutton "Красное":
                            text_size 26
                            action Function(clover_roulette_play, "красное")
                        textbutton "Чёрное":
                            text_size 26
                            action Function(clover_roulette_play, "чёрное")
                    hbox:
                        xalign 0.5
                        spacing 12
                        textbutton "Чёт":
                            text_size 26
                            action Function(clover_roulette_play, "чёт")
                        textbutton "Нечет":
                            text_size 26
                            action Function(clover_roulette_play, "нечет")
                else:
                    text "[clover_gamble_log]" size 24 color "#ffffff" xalign 0.5

                null height 10
                textbutton "Назад":
                    text_size 22
                    xalign 0.5
                    action [SetVariable("clover_gamble_game", None), SetVariable("clover_gamble_done", False)]

            elif clover_gamble_game == "Покер":
                # ------------------ ПОКЕР ------------------
                text "Покер" size 32 color "#ffd700" xalign 0.5
                text "Техасский покер. Максимальная ставка — 25% бонусных характеристик." size 22 color "#cccccc" xalign 0.5
                text "Противники ставят свои характеристики; победитель забирает банк." size 20 color "#888888" xalign 0.5

                if not clover_gamble_done:
                    textbutton "Раздать карты":
                        text_size 28
                        xalign 0.5
                        action Function(clover_poker_play)
                else:
                    text "[clover_gamble_log]" size 24 color "#ffffff" xalign 0.5

                null height 10
                textbutton "Назад":
                    text_size 22
                    xalign 0.5
                    action [SetVariable("clover_gamble_game", None), SetVariable("clover_gamble_done", False)]

            null height 6

            if clover_gamble_done:
                textbutton "Закончить":
                    text_size 26
                    xalign 0.5
                    action Return(True)


# ============================================================================
# ЛОГИКА ИГР
# ============================================================================

init python:
    def clover_poker_play():
        """Покер: Кловер и противники разыгрывают бонусные характеристики.

        Максимальная ставка — 25%. Если Кловер выиграл, он получает всё, что
        ставили противники. Если проиграл, не спасовавшие противники делят его
        ставку: 50% получает сильнейшая комбинация, остальные 50% делят между
        собой не спасовавшие.
        """
        stat = renpy.random.choice(clover_gamble_stat_names())
        stake_ratio = CLOVER_GAME_STAKES["Покер"]
        stake = abs(clover_gamble_get(stat)) * stake_ratio
        if stake <= 0:
            stake = 1.0
        clover_gamble_take(stat, stake)

        # Противники: часть пасует, остальные ставят.
        opponents = [e for e in (getattr(store, "enemies", {}) or {}).values()
                     if e is not None and getattr(e, "current_hp", 0) > 0]
        if not opponents:
            opponents = [None, None]  # абстрактные соперники за столом

        pot = stake
        active = []
        for index, _opp in enumerate(opponents[:4]):
            if renpy.random.random() < 0.25:
                continue  # спасовал
            active.append(index)
            pot += stake * 0.5  # противник ставит сопоставимо

        clover_hand = renpy.random.randint(1, 100)
        best_opp = max([renpy.random.randint(1, 100) for _ in active], default=0)

        if clover_hand > best_opp:
            clover_gamble_give(stat, pot)
            msg = ("Покер: комбинация {}. Ты выиграл банк {:.1f} ({})!"
                   .format(clover_hand, pot, stat))
            return clover_gamble_finish(True, stat, stake, msg)

        # Проигрыш: 50% сильнейшему, 50% между не спасовавшими.
        winners = max(1, len(active))
        msg = ("Покер: комбинация {} против {}. Ставка {:.1f} ({}) уходит "
               "{} противникам.".format(clover_hand, best_opp, stake, stat, winners))
        return clover_gamble_finish(False, stat, stake, msg)

    def clover_slots_drop_coin():
        """Слоты: монета делает ставку 3% от случайной характеристики."""
        stat = renpy.random.choice(clover_gamble_stat_names())
        stake = abs(clover_gamble_get(stat)) * 0.03
        if stake <= 0:
            stake = 1.0
        clover_gamble_take(stat, stake)
        store.clover_gamble_coin_count = int(store.clover_gamble_coin_count or 0) + 1
        store.clover_gamble_log = "Монета {}: ставка {:.1f} ({})".format(
            store.clover_gamble_coin_count, stake, stat)
        renpy.restart_interaction()

    def clover_slots_spin():
        """Прокрутка слотов: три символа, совпадение = выигрыш."""
        coins = int(getattr(store, "clover_gamble_coin_count", 0) or 0)
        if coins <= 0:
            return False
        symbols = ["7", "BAR", "cherry", "lemon", "bell"]
        spin = [renpy.random.choice(symbols) for _ in range(3)]
        stat = renpy.random.choice(clover_gamble_stat_names())
        stake = abs(clover_gamble_get(stat)) * 0.03 * coins

        if spin[0] == spin[1] == spin[2]:
            # Крупный выигрыш: возврат x5 от ставки.
            win = stake * 5
            clover_gamble_give(stat, win)
            msg = "Слоты: {} {} {} — КРУПНЫЙ ВЫИГРЫШ {:.1f} ({})!".format(spin[0], spin[1], spin[2], win, stat)
            return clover_gamble_finish(True, stat, stake, msg)
        if spin[0] == spin[1] or spin[1] == spin[2]:
            win = stake * 1.5
            clover_gamble_give(stat, win)
            msg = "Слоты: {} {} {} — малый выигрыш {:.1f} ({})".format(spin[0], spin[1], spin[2], win, stat)
            return clover_gamble_finish(True, stat, stake, msg)

        msg = "Слоты: {} {} {} — мимо. Потеряно {:.1f} ({})".format(spin[0], spin[1], spin[2], stake, stat)
        return clover_gamble_finish(False, stat, stake, msg)

    def clover_russian_roulette_play():
        """Русская рулетка: урон = магия Кловера * 40% * кол-во пуль."""
        char = clover_char()
        if char is None:
            return False
        bullets = max(1, min(6, int(getattr(store, "clover_gamble_bullets", 3) or 3)))
        damage = int(float(getattr(char, "magic", 0)) * 0.40 * bullets)
        # Кто-то застрелится: 1 из 6 шансов на пулю.
        fired = renpy.random.randint(1, 6)
        store.clover_gamble_shot_result = fired

        if fired <= bullets:
            # Застрелился противник — урон по случайному врагу.
            enemies_alive = [e for e in (getattr(store, "enemies", {}) or {}).values()
                             if e is not None and getattr(e, "current_hp", 0) > 0]
            if enemies_alive:
                victim = renpy.random.choice(enemies_alive)
                victim.current_hp = max(0, victim.current_hp - damage)
                add_attack_result("Кловер", victim.name, damage, False, "normal")
                msg = "Русская рулетка: БАБАХ! {} получает {} урона ({} пуль).".format(
                    victim.name, damage, bullets)
            else:
                msg = "Русская рулетка: БАБАХ! Но противников нет."
            store.clover_gamble_log = msg
            store.clover_gamble_done = True
            clover_clear_gambler_debuff()
            renpy.restart_interaction()
            return True

        # Осечка: Кловер теряет 40% от магии.
        stat = "магия"
        stake = abs(clover_gamble_get(stat)) * 0.40
        msg = "Русская рулетка: щёлк... холостой. Потеряно {:.1f} ({})".format(stake, stat)
        return clover_gamble_finish(False, stat, stake, msg)

    def clover_roulette_play(bet):
        """Рулетка: ставка до 12% от двух характеристик, двойной выигрыш."""
        stats = renpy.random.sample(clover_gamble_stat_names(), 2)
        stake = sum(abs(clover_gamble_get(s)) * CLOVER_GAME_STAKES["Рулетка"] for s in stats)
        if stake <= 0:
            stake = 1.0
        for s in stats:
            clover_gamble_take(s, abs(clover_gamble_get(s)) * CLOVER_GAME_STAKES["Рулетка"])

        number = renpy.random.randint(0, 36)
        color = "красное" if number % 2 == 1 else "чёрное"
        parity = "чёт" if number % 2 == 0 else "нечет"
        won = (bet == color) or (bet == parity) or (bet in ("красное", "чёрное") and bet == color)

        if won:
            for s in stats:
                clover_gamble_give(s, abs(clover_gamble_get(s)) * CLOVER_GAME_STAKES["Рулетка"] * 2)
            msg = "Рулетка: выпало {} ({}). Ставка «{}» сыграла — двойной выигрыш!".format(number, color, bet)
            return clover_gamble_finish(True, stats[0], stake, msg)

        msg = "Рулетка: выпало {} ({}). Ставка «{}» проиграла ({:.1f}).".format(number, color, bet, stake)
        return clover_gamble_finish(False, stats[0], stake, msg)

    def clover_dice_roll():
        """Дайсы: бросок 3 кубов d6."""
        store.clover_gamble_dice = [renpy.random.randint(1, 6) for _ in range(3)]
        store.clover_gamble_guess = []
        store.clover_gamble_log = ""
        renpy.restart_interaction()

    def clover_dice_guess(value):
        """Кловер угадывает значение на кубах."""
        guess = list(getattr(store, "clover_gamble_guess", []) or [])
        guess.append(int(value))
        store.clover_gamble_guess = guess
        if len(guess) < 3:
            renpy.restart_interaction()
            return False

        stat = renpy.random.choice(clover_gamble_stat_names())
        stake = abs(clover_gamble_get(stat)) * CLOVER_GAME_STAKES["Дайсы"]
        if stake <= 0:
            stake = 1.0
        clover_gamble_take(stat, stake)

        dice = list(getattr(store, "clover_gamble_dice", []) or [])
        hits = sum(1 for a, b in zip(guess, dice) if a == b)
        if hits == 3:
            win = stake * 4
            clover_gamble_give(stat, win)
            msg = "Дайсы: {} — все три угаданы! Выигрыш {:.1f} ({})".format(dice, win, stat)
            return clover_gamble_finish(True, stat, stake, msg)
        if hits >= 1:
            win = stake * hits
            clover_gamble_give(stat, win)
            msg = "Дайсы: {} — угадано {}. Выигрыш {:.1f} ({})".format(dice, hits, win, stat)
            return clover_gamble_finish(True, stat, stake, msg)

        msg = "Дайсы: {} — не угадано. Потеряно {:.1f} ({})".format(dice, stake, stat)
        return clover_gamble_finish(False, stat, stake, msg)

    def clover_rps_play(player_choice):
        """КНБ до 3 побед, ставка до 40% от выбранной характеристики."""
        if bool(getattr(store, "clover_gamble_done", False)):
            return False
        options = ["камень", "ножницы", "бумага"]
        beats = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}
        enemy_choice = renpy.random.choice(options)

        score = list(getattr(store, "clover_gamble_rps_score", [0, 0]) or [0, 0])
        if player_choice == enemy_choice:
            result = "ничья"
        elif beats[player_choice] == enemy_choice:
            score[0] += 1
            result = "победа"
        else:
            score[1] += 1
            result = "поражение"
        store.clover_gamble_rps_score = score
        store.clover_gamble_rps_round = int(getattr(store, "clover_gamble_rps_round", 0) or 0) + 1

        # Партия идёт до 3 побед.
        if score[0] >= 3 or score[1] >= 3:
            stat = renpy.random.choice(clover_gamble_stat_names())
            stake = abs(clover_gamble_get(stat)) * CLOVER_GAME_STAKES["КНБ"]
            if stake <= 0:
                stake = 1.0
            won = score[0] >= 3
            if won:
                clover_gamble_give(stat, stake * 2)
            else:
                clover_gamble_take(stat, stake)
            msg = "КНБ: {} — счёт {}:{}. {}".format(
                result, score[0], score[1],
                "Кловер победил!" if won else "Кловер проиграл ({:.1f}).".format(stake))
            return clover_gamble_finish(won, stat, stake, msg)

        store.clover_gamble_log = "КНБ: {} (счёт {}:{})".format(result, score[0], score[1])
        renpy.restart_interaction()
        return True
