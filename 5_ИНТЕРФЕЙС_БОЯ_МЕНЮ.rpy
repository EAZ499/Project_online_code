# Шейдер (должен быть в init python блоке в начале файла)
init python:
    renpy.register_shader("vertical_gradient_outline", variables="""
    uniform vec4 u_gradient_color_top;
    uniform vec4 u_gradient_color_bottom;
    uniform vec2 u_model_size;
    varying float v_gradient_done;
    attribute vec4 a_position;
    """, vertex_300="""
    v_gradient_done = a_position.y / u_model_size.y;
    """, fragment_300="""
    float gradient_done = v_gradient_done;
    gl_FragColor *= mix(u_gradient_color_top, u_gradient_color_bottom, gradient_done);
    """)

# Трансформ для применения градиента
transform damage_gradient:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (1.0, 0.0, 0.0, 1.0)   # Красный снизу

# Градиент: Белый сверху - Серый снизу
transform damage_gradient_gray:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.7, 0.7, 0.7, 1.0)   # Серый снизу

transform damage_gradient_semigray:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.9, 0.9, 0.9, 1.0)   # Серый снизу

# Градиент: Чёрный сверху - Серый снизу
transform damage_gradient_black:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.4, 0.4, 0.4, 1.0)   # Серый снизу


# Градиент: Белый сверху - Зелёный снизу
transform damage_gradient_green:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.0, 0.8, 0.0, 0.8)   # Зелёный снизу

# Градиент: Белый сверху - Зелёный снизу
transform damage_gradient_green_bright:
    shader "vertical_gradient_outline"
    u_gradient_color_top (0.8, 1.0, 0.8, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.0, 1.0, 0.0, 1.0)   # Зелёный снизу



# Градиент: Сине-голубой снизу - Белый сверху
transform damage_gradient_cyan:
    shader "vertical_gradient_outline"
    u_gradient_color_top    (1.0, 1.0, 1.0, 1.0) # Белый снизу 
    u_gradient_color_bottom (0.0, 0.7, 1.0, 1.0) # Сине-голубой сверху

transform damage_gradient_yellow:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0) # Жёлтый сверху
    u_gradient_color_bottom (1.0, 1.0, 0.0, 1.0)

transform damage_gradient_overheal:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.5, 1.5, 1.5, 1.5)      # Белый сверху
    u_gradient_color_bottom (0.4, 0.4, 0.4, 1.0)   # Серый снизу

transform damage_gradient_for_lowhp:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.5, 1.5, 1.5, 1.5)      # Белый сверху
    u_gradient_color_bottom (0.8, 0.8, 0.8, 1.0)   # Серый снизу

transform damage_gradient_for_lowhp2:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 0.1, 0.1, 1.0)      # Белый сверху
    u_gradient_color_bottom (0.5, 0.1, 0.1, 0.5)   # Серый снизу


transform invisible:
    alpha 0.0

# Стиль текста с обводкой
style damage_text:
    outlines [ (2, "#000000", 0, 0) ]  # Чёрная обводка 2px






default attack = 1
default battle_ability_current_cds = {}

default attackindexdesc = None

default nextswitch_style = 0
default prevswitch_style = 0
# 0 - опущено
# 1 - поднято


default summoned = 0
# 0 - ничего
# 1 - меч
# 2 - щит
default battle_one_time_used = {}

# Боевые текстовые кнопки: selected-состояние не должно выглядеть как hover.
style battle_menu_button is button

style battle_menu_button_text is button_text:
    selected_idle_color gui.button_text_idle_color
    selected_hover_color gui.button_text_hover_color

# === ОПТИМИЗИРОВАННЫЕ ФУНКЦИИ ДЛЯ choose_attack_screen ===
init python:
    # Перезарядки боевых кнопок задаются в ходах.
    # initial_cooldown — значение при начале боя,
    # cooldown_after_use — сколько ходов ждать после применения.
    # Пока не настроенные значения оставлены равными 0.
    BATTLE_ABILITY_COOLDOWNS = {
        name: {"initial_cooldown": 0, "cooldown_after_use": 0, "current_cd": 0}
        for name in (
            # Крис — атаки
            "Удар неудачника", "Удар мечом", "C разворота!", "Пронзить",
            "Отчаянное комбо", "Удар щитом", "Бонк!", "Отбить руки",
            "Рывок защитника (атака)",
            # Азриель — атаки
            "Удар принца", "Взмах мечом", "Щитовой удар", "Удар лбом",
            # Чара — атаки
            "Удар бунтарки", "Удар ножом", "Удар шпагой", "Удар из-за спины",
            "Решето", "Ножевой снаряд", "Реки крови",
            # Фриск, Кловер и Седрик — атаки/действия в меню атаки
            "Si vis pacem, para bellum", "Навскидку", "Прицельный", "Лассо",
            "Хлыст", "Клеймо", "Скорострел", "Удар сковородкой", "Пощёчина от шефа",
            # Крис — магия
            "Призвать меч", "Призвать щит", "Напрячься", "Позвать за щит",
            "Правильный угол", "Слабое место", "Концентрация", "Поднять щиты!",
            "Стремление вперёд", "Рывок защитника (магия)", "Пробудиться",
            # Азриель — магия
            "Шаг вперёд", "Магия огня", "Горное равновесие", "Клинки хаоса",
            "За спиною принца", "Уничтожитель хаоса", "Встать с колен",
            "Звёздный блеск", "Боевой клич!", "Луч Бога Гиперсмерти",
            # Чара — магия
            "Гнев", "Безумие", "Сумасшествие", "Псих", "Моральное разложение",
            "Пробуждение прошлого",
            # Фриск — магия
            "Potentia intellectus", "Quod licet Iovi, non licet bovi", "Foedus icere",
            "Do ut des", "Сохранение решимости",
            # Иззи — магия
            "Осколок себя", "Успокоение", "Медитация", "Карма", "Зачарование",
            "Предвидение", "Пробуждение", "Гнев", "Безумие", "Сумасшествие", "Псих",
            # Кловер — магия
            "Мелкий калибр", "Средний калибр", "Крупный калибр", "Длинный ствол",
            "Русская рулетка", "Дикий запад, Крошка!", "Уровень-геноцид",
            # Седрик — кнопки экрана магии (кулинарные действия)
            "Сбегать за продуктами", "Яичница на завтрак", "Булочка", "Салат Цезарь",
            "Сэндвич", "Блинчики с кленовым сиропом", "Чизбургер", "Суши",
            "Мясо на гриле", "Пицца!",
            # Фабри — призывы (меню атаки)
            "Призвать М-ра Панцыря", "Призвать М-с Пёрышко",
            "Призвать М-с Морковку", "Призвать М-с Манки",
            # Фабри — магия фамильяров
            "Спрятаться", "Надеть панцирь", "Прикрепиться", "Рикошет черепахи",
            "Орлиная зоркость", "Небесные танцы", "Снести яичко", "Перьевой ураган",
            "Ускориться", "Не поймаешь", "Поделиться морковкой", "Быстрее и дальше",
            "Боевой рёв", "Неудержимость", "Бей сильнее!", "Я покажу, как бить!",
        )
    }

    # Единый реестр кнопок боевого меню.
    # position — порядковый номер внутри секции, column — колонка vbox.
    # action и hover хранят описание действий кнопки, а не дублируются в screen-блоках.
    BATTLE_ABILITY_DEFINITIONS = []

    def _battle_ability(name, owner, menu, section, position, label=None, column=1,
                        level=0, requirements=None, action=None, hover=None,
                        initial_cooldown=0, cooldown_after_use=0, one_time=False,
                        cooldown_reduction=0, cooldown_reduction_level=0):
        ability = {
            "name": name,
            "label": label or name,
            "owner": owner,
            "owner_id": {"Крис": 1, "Азриель": 2, "Чара": 3, "Фриск": 4,
                         "Иззи": 5, "Кловер": 6, "Седрик": 7, "Арчи": 8,
                         "Сильвия": 9, "Фабри": 10, "Эмили": 11, "Сьюзи": 12,
                         "Ральзей": 13, "Ноэлль": 14, "Санс": 15, "Бердли": 16}.get(owner),
            "menu": menu,
            "section": section,
            "position": position,
            "column": column,
            "level": level,
            "requirements": requirements or {},
            "action": action or {},
            "hover": hover or {"description": True},
            "initial_cooldown": initial_cooldown,
            "cooldown_after_use": cooldown_after_use,
            "current_cd": 0,
            "one_time": one_time,
            "cooldown_reduction": cooldown_reduction,
            "cooldown_reduction_level": cooldown_reduction_level,
        }
        BATTLE_ABILITY_DEFINITIONS.append(ability)
        BATTLE_ABILITY_COOLDOWNS[name] = {
            "initial_cooldown": initial_cooldown,
            "cooldown_after_use": cooldown_after_use,
            "current_cd": 0,
            "cooldown_reduction": cooldown_reduction,
            "cooldown_reduction_level": cooldown_reduction_level,
        }

    def _battle_attack(name, owner, section, position, column=1, level=0,
                       label=None, requirements=None, turntype="totarget",
                       set_defend=False, set_defend_target=False, self_target=False,
                       initial_cooldown=0, cooldown_after_use=0, one_time=False,
                       cooldown_reduction=0, cooldown_reduction_level=0):
        action = {
            "turntype": turntype,
            "set_defend": set_defend,
            "set_defend_target": set_defend_target,
            "self_target": self_target,
            "show_target": True,
            "show_name": True,
        }
        _battle_ability(
            name, owner, "attack", section, position, label=label, column=column,
            level=level, requirements=requirements, action=action,
            initial_cooldown=initial_cooldown,
            cooldown_after_use=cooldown_after_use,
            one_time=one_time,
            cooldown_reduction=cooldown_reduction,
            cooldown_reduction_level=cooldown_reduction_level,
        )

    def _battle_magic(name, owner, section, position, column=1, level=0,
                      label=None, requirements=None, turntype="totarget",
                      set_defend_target=False, self_target=False,
                      initial_cooldown=0, cooldown_after_use=0, one_time=False,
                      cooldown_reduction=0, cooldown_reduction_level=0):
        action = {
            "turntype": turntype,
            "set_defend_target": set_defend_target,
            "self_target": self_target,
            "show_target": True,
            "show_name": True,
        }
        _battle_ability(
            name, owner, "magic", section, position, label=label, column=column,
            level=level, requirements=requirements, action=action,
            hover={"description": True, "resource_preview": True},
            initial_cooldown=initial_cooldown,
            cooldown_after_use=cooldown_after_use,
            one_time=one_time,
            cooldown_reduction=cooldown_reduction,
            cooldown_reduction_level=cooldown_reduction_level,
        )

    # Атаки. Пустой requirements означает, что дополнительных условий нет.
    _battle_attack("Удар неудачника", "Крис", 1, 1, turntype="toenemy")
    _battle_attack("защита_Крис", "Крис", 1, 2, label="Защищаться", set_defend=True)
    _battle_attack("Удар мечом", "Крис", 1, 1, column=2, requirements={"summoned": 1})
    _battle_attack("Удар щитом", "Крис", 1, 1, column=2, requirements={"summoned": 2})
    # «Привычка к вращению» ур.6: перезарядка «С разворота!» уменьшена на 2.
    _battle_attack("C разворота!", "Крис", 1, 2, column=2, level=3, requirements={"summoned": 1}, initial_cooldown=3, cooldown_after_use=3,
                   cooldown_reduction=2, cooldown_reduction_level=6)
    _battle_attack("Бонк!", "Крис", 1, 2, column=2, level=4, requirements={"summoned": 2}, initial_cooldown=1, cooldown_after_use=2)
    _battle_attack("Пронзить", "Крис", 2, 1, level=5, requirements={"summoned": 1}, initial_cooldown=2, cooldown_after_use=2)
    _battle_attack("Отбить руки", "Крис", 2, 1, level=6, requirements={"summoned": 2}, initial_cooldown=2, cooldown_after_use=3)
    _battle_attack("Отчаянное комбо", "Крис", 2, 2, level=8, requirements={"summoned": 1}, initial_cooldown=5, cooldown_after_use=6)
    _battle_attack("Рывок защитника (атака)", "Крис", 2, 2, label="Рывок защитника", level=9, requirements={"summoned": 2}, initial_cooldown=3, cooldown_after_use=3)

    _battle_attack("Удар принца", "Азриель", 1, 1)
    _battle_attack("защита_Азриель", "Азриель", 1, 2, label="Защищаться", set_defend=True)
    _battle_attack("Взмах мечом", "Азриель", 1, 1, column=2)
    _battle_attack("Щитовой удар", "Азриель", 1, 2, column=2, level=3, initial_cooldown=1, cooldown_after_use=3)
    _battle_attack("Удар лбом", "Азриель", 2, 1, level=5, initial_cooldown=3, cooldown_after_use=2)

    _battle_attack("Удар бунтарки", "Чара", 1, 1)
    _battle_attack("защита_Чара", "Чара", 1, 2, label="Защищаться", set_defend=True)
    _battle_attack("Удар ножом", "Чара", 1, 1, column=2, initial_cooldown=0, cooldown_after_use=1)
    _battle_attack("Удар шпагой", "Чара", 1, 2, column=2, initial_cooldown=0, cooldown_after_use=1)
    _battle_attack("Удар из-за спины", "Чара", 2, 1, level=3, initial_cooldown=1, cooldown_after_use=2)
    _battle_attack("Решето", "Чара", 2, 2, level=5, initial_cooldown=3, cooldown_after_use=4)
    _battle_attack("Ножевой снаряд", "Чара", 2, 1, column=2, level=7, initial_cooldown=1, cooldown_after_use=2)
    _battle_attack("Реки крови", "Чара", 2, 2, column=2, level=10, initial_cooldown=6, cooldown_after_use=4)

    _battle_attack("защита_Фриск", "Фриск", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Para bellum", "Фриск", 1, 2,
                   requirements={"hp_state": "any"},
                   one_time=True, initial_cooldown=0)
    # Кловер. Атаки: перезарядки и уровни — из ТЗ дизайнера.
    _battle_attack("защита_Кловер", "Кловер", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Навскидку", "Кловер", 1, 2, initial_cooldown=0, cooldown_after_use=1)
    _battle_attack("Прицельный", "Кловер", 1, 1, column=2, level=3, initial_cooldown=0, cooldown_after_use=1)
    _battle_attack("Лассо", "Кловер", 1, 2, column=2, level=5, initial_cooldown=2, cooldown_after_use=4)
    _battle_attack("Разрушительный хлыст", "Кловер", 2, 1, level=7, initial_cooldown=2, cooldown_after_use=7)
    _battle_attack("Клеймо", "Кловер", 2, 2, level=7, initial_cooldown=1, cooldown_after_use=8)
    _battle_attack("Скорострел", "Кловер", 2, 3, column=2, level=9, initial_cooldown=0, cooldown_after_use=0)

    # Арчи. Атаки: уровни и перезарядки — из ТЗ дизайнера.
    _battle_attack("защита_Арчи", "Арчи", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Боксёрское комбо", "Арчи", 1, 2, initial_cooldown=0, cooldown_after_use=1)
    _battle_attack("По полочкам", "Арчи", 1, 1, column=2, initial_cooldown=0, cooldown_after_use=2)
    _battle_attack("Удары богомола", "Арчи", 1, 2, column=2, level=2, initial_cooldown=0, cooldown_after_use=2)
    _battle_attack("Удар орла", "Арчи", 1, 3, column=2, level=3, initial_cooldown=4, cooldown_after_use=4)
    _battle_attack("Апперкот", "Арчи", 2, 1, level=4, initial_cooldown=2, cooldown_after_use=5)
    _battle_attack("Ураган", "Арчи", 2, 2, level=5, initial_cooldown=5, cooldown_after_use=7)
    _battle_attack("Мягкая ладонь", "Арчи", 2, 3, level=6, initial_cooldown=6, cooldown_after_use=4)
    _battle_attack("Oma yi wa mou", "Арчи", 2, 1, column=2, level=8, initial_cooldown=9, one_time=True)
    _battle_attack("защита_Седрик", "Седрик", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Удар сковородкой", "Седрик", 1, 2, initial_cooldown=0, cooldown_after_use=0, turntype="toenemy")
    _battle_attack("Пощёчина от шефа", "Седрик", 1, 1, column=2, level=10, initial_cooldown=6, cooldown_after_use=8, turntype="toenemy")

    # Сильвия: собственных атак у неё нет (атака «очень плохо»), весь её ход —
    # это движения танца. В меню атаки остаётся базовая защита; движения
    # регистрируются как магия ниже и не имеют перезарядки («Репертуар»).
    _battle_attack("защита_Сильвия", "Сильвия", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Плие", "Сильвия", 1, 2, initial_cooldown=0, cooldown_after_use=0)
    _battle_attack("Томбе", "Сильвия", 1, 3, initial_cooldown=0, cooldown_after_use=0)

    # Фабри: собственных атак нет (атака «очень плохо»), весь её ход — призыв
    # фамильяра. В меню атаки остаётся базовая защита, четыре призыва
    # бесплатны (это не магия, поэтому записи в ABILITY_RESOURCE_COSTS нет).
    _battle_attack("защита_Фабри", "Фабри", 1, 5, label="Защищаться", set_defend=True)
    _battle_attack("Призвать М-ра Панцыря", "Фабри", 1, 1, level=1, turntype="toally")
    _battle_attack("Призвать М-с Пёрышко", "Фабри", 1, 2, level=1, turntype="toally")
    _battle_attack("Призвать М-с Морковку", "Фабри", 1, 3, level=1, turntype="toally")
    _battle_attack("Призвать М-с Манки", "Фабри", 1, 4, level=1, turntype="toally")

    # Эмили — атаки и магия аналитика/взломщика.
    _battle_attack("Вперёд, Мистер коготь!", "Эмили", 1, 1, level=1, initial_cooldown=0, cooldown_after_use=0)
    _battle_attack("Назад, Мистер Коготь!", "Эмили", 1, 2, level=1, initial_cooldown=0, cooldown_after_use=1)
    _battle_attack("защита_Эмили", "Эмили", 1, 5, label="Защищаться", set_defend=True)
    _battle_magic("Викторина", "Эмили", 1, 1, level=1, initial_cooldown=0, cooldown_after_use=1)
    _battle_magic("Гонка чисел", "Эмили", 1, 2, level=1, initial_cooldown=0, cooldown_after_use=1)
    _battle_magic("Цифровой щит", "Эмили", 1, 3, level=1, initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Блеснуть безупречностью", "Эмили", 1, 4, level=1, initial_cooldown=2, cooldown_after_use=4, self_target=True)
    _battle_magic("Взлом сети", "Эмили", 2, 1, level=2, initial_cooldown=2, cooldown_after_use=4)
    _battle_magic("Блокировка", "Эмили", 2, 2, level=3, initial_cooldown=3, cooldown_after_use=5)
    _battle_magic("Левый аккаунт", "Эмили", 2, 3, level=4, initial_cooldown=5, cooldown_after_use=6)
    _battle_magic("Заморозка репозитория", "Эмили", 2, 4, level=5, initial_cooldown=2, cooldown_after_use=7)
    _battle_magic("Трансляция взлома", "Эмили", 3, 1, level=5, initial_cooldown=2, cooldown_after_use=7)
    _battle_magic("Маленькая ошибка", "Эмили", 3, 2, level=6, initial_cooldown=3, cooldown_after_use=5)
    _battle_magic("Доксиинг", "Эмили", 3, 3, level=7, initial_cooldown=4, cooldown_after_use=8)
    _battle_magic("Взлом аккаунта", "Эмили", 3, 4, level=8, initial_cooldown=8, cooldown_after_use=6)
    _battle_magic("Блэк аут", "Эмили", 4, 1, level=9, initial_cooldown=3, cooldown_after_use=7)
    _battle_magic("Резервная копия", "Эмили", 4, 2, level=9, initial_cooldown=5, cooldown_after_use=8)
    _battle_magic("Игра оптики", "Эмили", 4, 3, level=10, initial_cooldown=8, cooldown_after_use=5)

    _battle_attack("защита_Сьюзи", "Сьюзи", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Пинок ногой", "Сьюзи", 1, 2, level=1, cooldown_after_use=1)
    _battle_attack("Удар Секирой", "Сьюзи", 1, 3, level=1, cooldown_after_use=1)
    _battle_attack("Всем и сразу!", "Сьюзи", 1, 4, level=1, cooldown_after_use=1)
    _battle_attack("Хвостовой хлыст", "Сьюзи", 1, 5, level=1, cooldown_after_use=4)
    _battle_attack("Подручный снаряд", "Сьюзи", 2, 1, level=2, cooldown_after_use=2)
    _battle_attack("Кусь!", "Сьюзи", 2, 2, level=3, initial_cooldown=2, cooldown_after_use=3)
    _battle_attack("Об землю!", "Сьюзи", 2, 3, level=4, cooldown_after_use=3)
    _battle_attack("Пурпурный локоть!", "Сьюзи", 2, 4, level=5, cooldown_after_use=4)
    _battle_attack("Добивочная!", "Сьюзи", 3, 1, level=6, cooldown_after_use=4)
    _battle_attack("Смести всё!", "Сьюзи", 3, 2, level=8, initial_cooldown=4, cooldown_after_use=5)
    _battle_magic("Пурпурная инфузия", "Сьюзи", 1, 1, level=1, cooldown_after_use=7, self_target=True)
    _battle_magic("Зазывала", "Сьюзи", 1, 2, level=2)
    _battle_magic("Rude Buster", "Сьюзи", 1, 3, level=3, cooldown_after_use=2)
    _battle_magic("Зверский рык", "Сьюзи", 2, 1, level=5, cooldown_after_use=3)
    _battle_magic("Секираранг", "Сьюзи", 2, 2, level=7, cooldown_after_use=4)
    _battle_magic("Rude fissure", "Сьюзи", 2, 3, level=9, cooldown_after_use=6)

    # Магия. mana=True включает проверку can_pay_ability_cost и preview MP/HP.
    magic_req = {"mana": True}
    _battle_magic("Призвать меч", "Крис", 1, 1, requirements={"mana": True, "summoned_not": 1}, self_target=True)
    _battle_magic("Призвать щит", "Крис", 1, 1, column=2, requirements={"mana": True, "summoned_not": 2}, self_target=True)
    _battle_magic("Напрячься", "Крис", 1, 2, requirements={"mana": True, "level": 3, "summoned_not": 3}, self_target=True)
    _battle_magic("Позвать за щит", "Крис", 1, 2, column=2, requirements={"mana": True, "level": 3, "summoned": 2}, turntype="toally", initial_cooldown=3, one_time=True)
    # «Правильный угол» и «Слабое место» требуют накопленных действий
    # (actions_min); «Гибкое терпение» ур.8 снижает порог у «Слабого места».
    _battle_magic("Правильный угол", "Крис", 1, 3, column=2, requirements={"mana": True, "level": 5, "summoned": 2, "actions_min": 4}, self_target=True, initial_cooldown=4, cooldown_after_use=3)
    _battle_magic("Слабое место", "Крис", 1, 4, requirements={"mana": True, "level": 4, "summoned": 1, "actions_min": 3}, self_target=True, initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Концентрация", "Крис", 2, 1, requirements={"mana": True, "level": 7, "summoned": 1}, self_target=True, initial_cooldown=3, cooldown_after_use=4)
    _battle_magic("Поднять щиты!", "Крис", 2, 1, column=2, requirements={"mana": True, "level": 8, "summoned": 2}, self_target=True, initial_cooldown=5, cooldown_after_use=4)
    _battle_magic("Стремление вперёд", "Крис", 2, 2, requirements={"mana": True, "level": 9, "summoned": 2}, self_target=True, initial_cooldown=9, cooldown_after_use=8)
    _battle_magic("Рывок защитника (магия)", "Крис", 2, 3, column=2, requirements={"mana": True, "level": 10, "summoned": 2}, self_target=True, initial_cooldown=8, cooldown_after_use=7)
    _battle_magic("Пробудиться", "Крис", 2, 4, requirements={"mana": True, "level": 10, "summoned": 1}, self_target=True, initial_cooldown=7, one_time=True)

    # Азриель. «Размножение личности»: доступность магии зависит от облика
    # (requirements form), перезарядки — из ТЗ дизайнера.
    _battle_magic("Сменить облик", "Азриель", 1, 3, requirements={}, self_target=True, initial_cooldown=0, cooldown_after_use=1)
    _battle_magic("Шаг вперёд", "Азриель", 1, 1, requirements={"mana": True, "form": "fluffy"}, initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Магия огня", "Азриель", 1, 2, requirements={"mana": True, "level": 2, "form": "echo"}, initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Горное равновесие", "Азриель", 1, 1, column=2, level=3, requirements={"mana": True, "level": 3, "form": "fluffy"}, turntype="toenemy", initial_cooldown=4, cooldown_after_use=0, one_time=True)
    _battle_magic("Клинки хаоса", "Азриель", 1, 2, column=2, requirements={"mana": True, "level": 4, "form": "echo"}, turntype="toenemy", initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("За спиною принца", "Азриель", 2, 1, level=5, requirements={"mana": True, "level": 5, "form": "fluffy"}, turntype="toally", initial_cooldown=3, cooldown_after_use=6)
    _battle_magic("Уничтожитель хаоса", "Азриель", 2, 2, level=6, requirements={"mana": True, "level": 6, "form": "echo"}, initial_cooldown=3, cooldown_after_use=3)
    _battle_magic("Встать с колен", "Азриель", 2, 1, column=2, level=7, requirements={"mana": True, "level": 7, "form": "fluffy"}, initial_cooldown=5, cooldown_after_use=6)
    _battle_magic("Звёздный блеск", "Азриель", 2, 2, column=2, level=8, requirements={"mana": True, "level": 8, "form": "echo"}, initial_cooldown=4, cooldown_after_use=5)
    _battle_magic("Боевой клич!", "Азриель", 3, 1, level=9, requirements={"mana": True, "level": 9, "form": "fluffy"}, initial_cooldown=3, cooldown_after_use=5)
    _battle_magic("Луч Бога Гиперсмерти", "Азриель", 3, 2, level=10, requirements={"mana": True, "level": 10, "form": "echo"}, initial_cooldown=7, cooldown_after_use=6)

    _battle_magic("Гнев", "Чара", 1, 1, requirements={"mana": True}, set_defend_target=True)
    _battle_magic("Безумие", "Чара", 1, 2, requirements={"mana": True}, set_defend_target=True)
    _battle_magic("Сумасшествие", "Чара", 1, 1, column=2, requirements={"mana": True, "level": 5}, initial_cooldown=3, cooldown_after_use=4)
    _battle_magic("Псих", "Чара", 1, 2, column=2, requirements={"mana": True, "level": 7}, initial_cooldown=0, cooldown_after_use=6)
    _battle_magic("Моральное разложение", "Чара", 2, 1, requirements={"mana": True, "level": 7}, initial_cooldown=2, cooldown_after_use=5)
    _battle_magic("Пробуждение прошлого", "Чара", 2, 2, requirements={"mana": True, "level": 10}, initial_cooldown=8, one_time=True)

    _battle_magic("Potentia intellectus", "Фриск", 1, 1, requirements={"mana": True, "level": 1}, initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Quod licet Iovi, non licet bovi", "Фриск", 1, 2, requirements={"mana": True, "level": 2}, initial_cooldown=1, cooldown_after_use=3)
    _battle_magic("Проект договора", "Фриск", 1, 1, column=2, requirements={"mana": True, "level": 4}, initial_cooldown=5, one_time=True)
    _battle_magic("Foedus icere", "Фриск", 2, 1, requirements={"mana": True, "level": 6}, initial_cooldown=5, cooldown_after_use=3)
    _battle_magic("Do ut des", "Фриск", 2, 2, requirements={"mana": True, "level": 8}, initial_cooldown=6, cooldown_after_use=4)
    _battle_magic("Вернуть в диалог", "Фриск", 2, 3, column=2, requirements={"mana": True, "level": 10}, initial_cooldown=4, cooldown_after_use=8)

    _battle_magic("Осколок себя", "Иззи", 1, 1, requirements={"mana": True, "level": 1}, initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Успокоение", "Иззи", 1, 2, requirements={"mana": True, "level": 1}, turntype="toally", initial_cooldown=1, cooldown_after_use=4)
    _battle_magic("Медитация", "Иззи", 1, 1, column=2, requirements={"mana": True, "level": 1}, turntype="tochar", initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Правильное дыхание", "Иззи", 1, 2, column=2, requirements={"mana": True, "level": 1}, turntype="tochar", initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Благовония", "Иззи", 1, 1, requirements={"mana": True, "level": 2}, initial_cooldown=3, cooldown_after_use=4)
    _battle_magic("Открытие пределов", "Иззи", 1, 2, requirements={"mana": True, "level": 3}, turntype="tochar", initial_cooldown=2, cooldown_after_use=8)
    _battle_magic("Воспрять дух", "Иззи", 2, 1, requirements={"mana": True, "level": 4}, turntype="toally", initial_cooldown=2, cooldown_after_use=6)
    _battle_magic("Карма", "Иззи", 2, 2, requirements={"mana": True, "level": 5}, turntype="toally", initial_cooldown=4, cooldown_after_use=5)
    _battle_magic("Предвиденье", "Иззи", 2, 1, column=2, requirements={"mana": True, "level": 6}, turntype="tochar", initial_cooldown=6, cooldown_after_use=3)
    _battle_magic("Зачарование", "Иззи", 2, 2, column=2, requirements={"mana": True, "level": 7}, turntype="toally", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Усиление присутствия", "Иззи", 3, 1, requirements={"mana": True, "level": 8}, self_target=True, initial_cooldown=7, one_time=True)
    _battle_magic("Духовный лук", "Иззи", 3, 2, requirements={"mana": True, "level": 9}, initial_cooldown=8, cooldown_after_use=4)
    _battle_magic("Пробуждение", "Иззи", 3, 1, column=2, requirements={"mana": True, "level": 10}, initial_cooldown=9, one_time=True)

    # Кловер. Магия: уровни и перезарядки — из ТЗ дизайнера.
    # «Сыграем!» всегда имеет перезарядку 0.
    _battle_magic("Выбор калибра", "Кловер", 1, 1, requirements={"mana": True, "level": 1}, initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Сыграем!", "Кловер", 1, 2, requirements={"mana": True, "level": 1}, initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Помиловать", "Кловер", 1, 1, column=2, requirements={"mana": True, "level": 1}, initial_cooldown=1, cooldown_after_use=3)
    _battle_magic("Вафельный перерыв", "Кловер", 1, 2, column=2, requirements={"mana": True, "level": 2}, initial_cooldown=4, cooldown_after_use=5, one_time=True)
    _battle_magic("Суд", "Кловер", 2, 1, requirements={"mana": True, "level": 3}, initial_cooldown=5, cooldown_after_use=10)
    _battle_magic("Дробовик", "Кловер", 2, 2, requirements={"mana": True, "level": 4}, initial_cooldown=3, cooldown_after_use=2)
    _battle_magic("Метка разыскиваемого", "Кловер", 2, 1, column=2, requirements={"mana": True, "level": 4}, initial_cooldown=2, cooldown_after_use=4)
    _battle_magic("Вызов на дуэль!", "Кловер", 2, 2, column=2, requirements={"mana": True, "level": 5}, initial_cooldown=0, cooldown_after_use=3)
    _battle_magic("Длинный ствол", "Кловер", 3, 1, requirements={"mana": True, "level": 6}, initial_cooldown=3, cooldown_after_use=2)
    _battle_magic("От судьбы не уйдёшь", "Кловер", 3, 2, requirements={"mana": True, "level": 8}, initial_cooldown=5, cooldown_after_use=7)
    _battle_magic("Дикий запад, Крошка!", "Кловер", 3, 1, column=2, requirements={"mana": True, "level": 9}, initial_cooldown=6, cooldown_after_use=6)
    # «Гиперлуч» одноразовый и доступен только на руте GENO.
    _battle_magic("Гиперлуч", "Кловер", 3, 2, column=2, requirements={"geno_route": True, "level": 10}, initial_cooldown=8, one_time=True)

    # Арчи. Магия: базовые заклинания и стойки, уровни и КД — из ТЗ.
    _battle_magic("Ладони чакры", "Арчи", 1, 1, requirements={"mana": True, "level": 1}, initial_cooldown=0, cooldown_after_use=5)
    _battle_magic("Очищение Ци", "Арчи", 1, 2, requirements={"mana": True, "level": 1}, self_target=True, initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Печати ниндзюцу", "Арчи", 1, 1, column=2, requirements={"mana": True, "level": 2}, self_target=True, initial_cooldown=1, cooldown_after_use=3)
    _battle_magic("Укрепление мышц", "Арчи", 1, 2, column=2, requirements={"mana": True, "level": 3}, self_target=True, initial_cooldown=2, cooldown_after_use=4)
    _battle_magic("Рывок", "Арчи", 1, 3, column=2, requirements={"mana": True, "level": 4}, self_target=True, initial_cooldown=1, cooldown_after_use=2)
    _battle_magic("Режим храбрости", "Арчи", 2, 1, requirements={"mana": True, "level": 4}, self_target=True, initial_cooldown=3, cooldown_after_use=6)
    _battle_magic("Реверс энергии", "Арчи", 2, 2, requirements={"mana": True, "level": 5}, self_target=True, initial_cooldown=5, cooldown_after_use=4)
    _battle_magic("Травмирующие удары", "Арчи", 2, 1, column=2, requirements={"mana": True, "level": 6}, self_target=True, initial_cooldown=0, cooldown_after_use=7)
    _battle_magic("Вернуть отправителю", "Арчи", 2, 2, column=2, requirements={"mana": True, "level": 7}, self_target=True, initial_cooldown=2, cooldown_after_use=5)
    _battle_magic("Храбрость!", "Арчи", 2, 3, column=2, requirements={"mana": True, "level": 9}, self_target=True, initial_cooldown=7, cooldown_after_use=5)

    _battle_magic("Сбегать за продуктами", "Седрик", 1, 1, requirements={"mana": True}, self_target=True, initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Яичница на завтрак", "Седрик", 1, 2, requirements={"mana": True}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Булочка", "Седрик", 1, 1, column=2, requirements={"mana": True}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Салат Цезарь", "Седрик", 1, 2, column=2, requirements={"mana": True, "level": 2}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Сэндвич", "Седрик", 2, 1, requirements={"mana": True, "level": 3}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Блинчики с кленовым сиропом", "Седрик", 2, 2, requirements={"mana": True, "level": 4}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Чизбургер", "Седрик", 2, 1, column=2, requirements={"mana": True, "level": 5}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Суши", "Седрик", 2, 2, column=2, requirements={"mana": True, "level": 6}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Мясо на гриле", "Седрик", 3, 1, requirements={"mana": True, "level": 7}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)
    _battle_magic("Пицца!", "Седрик", 3, 2, requirements={"mana": True, "level": 9}, turntype="cook", initial_cooldown=0, cooldown_after_use=0)

    # Фабри: магия фамильяров. Секция = владелец-фамильяр:
    # 1 — М-р Панцырь, 2 — М-с Пёрышко, 3 — М-с Морковка, 4 — М-с Манки.
    # Требование "familiar" проверяет, призван ли нужный фамильяр
    # (см. battle_ability_condition_is_met / battle_ability_should_appear).
    # Уровни и перезарядки — из спеки _FABRI_SPEC.md, раздел 6.

    # --- М-р Панцырь (sec 1) ---
    _battle_magic("Спрятаться", "Фабри", 1, 1, level=1, requirements={"mana": True, "familiar": "shell"},
                  turntype="tochar", initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Надеть панцирь", "Фабри", 1, 2, level=2, requirements={"mana": True, "familiar": "shell"},
                  turntype="tochar", initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Прикрепиться", "Фабри", 1, 3, level=5, requirements={"mana": True, "familiar": "shell"},
                  turntype="tochar", initial_cooldown=4, cooldown_after_use=5)
    _battle_magic("Рикошет черепахи", "Фабри", 1, 4, level=7, requirements={"mana": True, "familiar": "shell"},
                  turntype="toenemy", initial_cooldown=5, cooldown_after_use=6)

    # --- М-с Пёрышко (sec 2) ---
    _battle_magic("Орлиная зоркость", "Фабри", 2, 1, level=1, requirements={"mana": True, "familiar": "feather"},
                  turntype="tochar", initial_cooldown=0, cooldown_after_use=2)
    _battle_magic("Небесные танцы", "Фабри", 2, 2, level=2, requirements={"mana": True, "familiar": "feather"},
                  turntype="tochar", initial_cooldown=1, cooldown_after_use=3)
    # «Снести яичко»: кладка одна за бой, после применения КД 1.
    _battle_magic("Снести яичко", "Фабри", 2, 3, level=6, requirements={"mana": True, "familiar": "feather"},
                  turntype="totarget", initial_cooldown=3, cooldown_after_use=1, one_time=True)
    _battle_magic("Перьевой ураган", "Фабри", 2, 4, level=8, requirements={"mana": True, "familiar": "feather"},
                  turntype="toenemy", initial_cooldown=5, cooldown_after_use=5)

    # --- М-с Морковка (sec 3) ---
    _battle_magic("Ускориться", "Фабри", 3, 1, level=1, requirements={"mana": True, "familiar": "carrot"},
                  turntype="tochar", initial_cooldown=0, cooldown_after_use=1)
    _battle_magic("Не поймаешь", "Фабри", 3, 2, level=3, requirements={"mana": True, "familiar": "carrot"},
                  turntype="tochar", initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Поделиться морковкой", "Фабри", 3, 3, level=4, requirements={"mana": True, "familiar": "carrot"},
                  turntype="toally", initial_cooldown=3, cooldown_after_use=4)
    _battle_magic("Быстрее и дальше", "Фабри", 3, 4, level=9, requirements={"mana": True, "familiar": "carrot"},
                  turntype="toally", initial_cooldown=7, cooldown_after_use=6)

    # --- М-с Манки (sec 4) ---
    _battle_magic("Боевой рёв", "Фабри", 4, 1, level=1, requirements={"mana": True, "familiar": "monkey"},
                  turntype="toenemy", initial_cooldown=0, cooldown_after_use=3)
    _battle_magic("Неудержимость", "Фабри", 4, 2, level=3, requirements={"mana": True, "familiar": "monkey"},
                  turntype="tochar", initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Бей сильнее!", "Фабри", 4, 3, level=5, requirements={"mana": True, "familiar": "monkey"},
                  turntype="toally", initial_cooldown=3, cooldown_after_use=3)
    _battle_magic("Я покажу, как бить!", "Фабри", 4, 4, level=10, requirements={"mana": True, "familiar": "monkey"},
                  turntype="toally", initial_cooldown=8, cooldown_after_use=6)

    # Полный реестр из спецификации. Ральзей намеренно не получает обычных
    # атак: это его пассивка «Чистые руки», но общая защита доступна.
    _battle_attack("защита_Ральзей", "Ральзей", 1, 1, label="Защищаться", set_defend=True)
    _battle_magic("Умиротворение", "Ральзей", 1, 1, level=1, requirements={"mana": True}, turntype="toenemy")
    _battle_magic("Лозы", "Ральзей", 1, 2, level=1, requirements={"mana": True})
    _battle_magic("Молитва исцеления", "Ральзей", 1, 3, level=1, requirements={"mana": True}, turntype="toally")
    _battle_magic("Агрессивный пузырь", "Ральзей", 1, 4, level=1, requirements={"mana": True}, turntype="toally")
    _battle_magic("Пушистый страж", "Ральзей", 1, 5, level=2, requirements={"mana": True}, turntype="toally")
    _battle_magic("Лечение?...", "Ральзей", 2, 1, level=2, requirements={"mana": True})
    _battle_magic("Рассеять!", "Ральзей", 2, 2, level=3, requirements={"mana": True})
    _battle_magic("Пламенная казнь", "Ральзей", 2, 3, level=3, requirements={"mana": True}, initial_cooldown=1, cooldown_after_use=2)
    _battle_magic("Перегной", "Ральзей", 2, 4, level=4, requirements={"mana": True})
    _battle_magic("Убеждающий вид", "Ральзей", 2, 5, level=4, requirements={"mana": True})
    _battle_magic("Приумножить заслуги", "Ральзей", 3, 1, level=5, requirements={"mana": True}, turntype="toally")
    _battle_magic("Унизить слабого", "Ральзей", 3, 2, level=6, requirements={"mana": True}, turntype="toally")
    _battle_magic("Песнь воскрешения", "Ральзей", 3, 3, level=7, requirements={"mana": True}, turntype="toally")
    _battle_magic("Спустить с небес", "Ральзей", 3, 4, level=8, requirements={"mana": True}, turntype="toally")
    _battle_magic("Концентрация зла", "Ральзей", 3, 5, level=9, requirements={"mana": True}, self_target=True)
    _battle_magic("Тёмный горящий сад", "Ральзей", 3, 6, level=10, requirements={"mana": True}, one_time=True, initial_cooldown=9)

    _battle_attack("защита_Ноэлль", "Ноэлль", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Неуверенный взмах", "Ноэлль", 1, 2, level=1, cooldown_after_use=1)
    _battle_attack("Ледяная катана", "Ноэлль", 1, 3, level=1, cooldown_after_use=2)
    _battle_attack("Снежок", "Ноэлль", 1, 4, level=3, cooldown_after_use=2)
    _battle_magic("Молитва исцеления Ноэлль", "Ноэлль", 1, 1, level=1, label="Молитва исцеления", requirements={"mana": True}, turntype="toally", cooldown_after_use=1)
    _battle_magic("Ледяной шок", "Ноэлль", 1, 2, level=1, requirements={"mana": True}, cooldown_after_use=2)
    _battle_magic("Сонный туман", "Ноэлль", 1, 3, level=2, requirements={"mana": True}, initial_cooldown=1, cooldown_after_use=3)
    _battle_magic("Морозная завеса", "Ноэлль", 2, 1, level=3, requirements={"mana": True}, self_target=True, initial_cooldown=2, cooldown_after_use=4)
    _battle_magic("Ледяная буря", "Ноэлль", 2, 2, level=4, requirements={"mana": True}, initial_cooldown=3, cooldown_after_use=4)
    _battle_magic("Оледенение чувств", "Ноэлль", 2, 3, level=5, requirements={"mana": True}, initial_cooldown=4, cooldown_after_use=5)
    _battle_magic("Морозная корка", "Ноэлль", 2, 4, level=6, requirements={"mana": True}, initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Ледяной кокон", "Ноэлль", 3, 1, level=7, requirements={"mana": True}, turntype="toally", initial_cooldown=3, cooldown_after_use=5)
    _battle_magic("Аура холодного сердца", "Ноэлль", 3, 2, level=8, requirements={"mana": True}, self_target=True, initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Терновый сад", "Ноэлль", 3, 3, level=9, requirements={"mana": True}, one_time=True, initial_cooldown=6)
    _battle_magic("Цветение бед", "Ноэлль", 3, 4, level=9, requirements={"mana": True})
    _battle_magic("Снежная могила", "Ноэлль", 3, 5, level=10, requirements={"mana": True}, one_time=True, initial_cooldown=9)

    _battle_attack("защита_Санс", "Санс", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Удар костью", "Санс", 1, 2, level=1)
    _battle_attack("Преподать урок", "Санс", 1, 3, level=3)
    _battle_attack("Подойди сюда", "Санс", 1, 4, level=5)
    _battle_magic("Стена костей", "Санс", 1, 1, level=1, requirements={"mana": True})
    _battle_magic("Костяной дождь", "Санс", 1, 2, level=1, requirements={"mana": True})
    _battle_magic("Прижмись", "Санс", 1, 3, level=1, requirements={"mana": True})
    _battle_magic("Поспать", "Санс", 1, 4, level=1, requirements={"mana": True}, self_target=True, initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Камнем вниз", "Санс", 1, 5, level=1, requirements={"mana": True})
    _battle_magic("Костяной щит", "Санс", 2, 1, level=2, requirements={"mana": True}, turntype="toally", cooldown_after_use=2)
    _battle_magic("Бластер", "Санс", 2, 2, level=3, requirements={"mana": True}, initial_cooldown=3, cooldown_after_use=4)
    _battle_magic("Пинг-понг", "Санс", 2, 3, level=4, requirements={"mana": True}, initial_cooldown=2, cooldown_after_use=3)
    _battle_magic("Костяная клетка", "Санс", 2, 4, level=5, requirements={"mana": True}, initial_cooldown=2, cooldown_after_use=4)
    _battle_magic("Угрызения совести", "Санс", 2, 5, level=5, requirements={"mana": True}, initial_cooldown=2, cooldown_after_use=4)
    _battle_magic("Кара за грехи", "Санс", 3, 1, level=6, requirements={"mana": True}, initial_cooldown=3, cooldown_after_use=5)
    _battle_magic("Телекинез!", "Санс", 3, 2, level=8, requirements={"mana": True}, initial_cooldown=3, cooldown_after_use=5)
    _battle_magic("Финальная атака", "Санс", 3, 3, level=10, requirements={"mana": True}, one_time=True, initial_cooldown=9)

    _battle_attack("защита_Бердли", "Бердли", 1, 1, label="Защищаться", set_defend=True)
    _battle_attack("Клювом!", "Бердли", 1, 2)
    _battle_magic("Гениальный план", "Бердли", 1, 1, level=1, requirements={"mana": True}, self_target=True)
    _battle_magic("Электрический клюв", "Бердли", 1, 2, level=2, requirements={"mana": True}, initial_cooldown=1, cooldown_after_use=2)
    _battle_magic("Вихрь знаний", "Бердли", 2, 1, level=6, requirements={"mana": True}, initial_cooldown=3, cooldown_after_use=4)

    BATTLE_MENU_RULES = {
        "attack": {
            1: {"sections": 2, "next_levels": {1: 5}},
            2: {"sections": 2, "next_levels": {1: 5}},
            3: {"sections": 2, "next_levels": {1: 3}},
            4: {"sections": 1, "next_levels": {}},
            5: {"sections": 1, "next_levels": {}},
            6: {"sections": 2, "next_levels": {1: 7}},
            7: {"sections": 1, "next_levels": {}},
            10: {"sections": 1, "next_levels": {}},
            11: {"sections": 1, "next_levels": {}},
            12: {"sections": 3, "next_levels": {1: 1, 2: 2}},
            13: {"sections": 1, "next_levels": {}},
            14: {"sections": 1, "next_levels": {}},
            15: {"sections": 1, "next_levels": {}},
            16: {"sections": 1, "next_levels": {}},
        },
        "magic": {
            1: {"sections": 2, "next_levels": {1: 7}},
            2: {"sections": 3, "next_levels": {1: 5, 2: 9}},
            3: {"sections": 2, "next_levels": {1: 6}},
            4: {"sections": 2, "next_levels": {1: 6}},
            5: {"sections": 3, "next_levels": {1: 0, 2: 7}},
            6: {"sections": 2, "next_levels": {1: 7}},
            7: {"sections": 3, "next_levels": {1: 3, 2: 7}},
            9: {"sections": 1, "next_levels": {}},
            # Фабри: 4 секции — по одной на фамильяра (1 Панцырь, 2 Пёрышко,
            # 3 Морковка, 4 Манки). Навигация последовательная: доступ к
            # секции N открывает next_levels[N] через уровень Фабри, а
            # отсутствие записи для N делает переход «запертым» навсегда.
            # Поэтому заданы ВСЕ переходы 1..3 и порог = 1: у каждого
            # фамильяра есть магия 1-го уровня («Спрятаться», «Орлиная
            # зоркость», «Ускориться», «Боевой рёв»), и порог >1 сделал бы
            # её недостижимой в начале игры. Видимость способностей внутри
            # секции регулирует требование "familiar": без призванного
            # фамильяра кнопок нет вовсе.
            10: {"sections": 4, "next_levels": {1: 1, 2: 1, 3: 1}},
            11: {"sections": 4, "next_levels": {1: 1, 2: 2, 3: 5}},
            12: {"sections": 2, "next_levels": {1: 1}},
            13: {"sections": 3, "next_levels": {1: 3, 2: 5}},
            14: {"sections": 3, "next_levels": {1: 3, 2: 7}},
            15: {"sections": 3, "next_levels": {1: 3, 2: 6}},
            16: {"sections": 2, "next_levels": {1: 4}},
        },
    }

    def get_battle_abilities(menu, attacker, section):
        return sorted(
            [a for a in BATTLE_ABILITY_DEFINITIONS
             if a["menu"] == menu and a["owner_id"] == attacker and a["section"] == section],
            key=lambda a: (a["column"], a["position"]),
        )

    def get_battle_menu_navigation(menu, attacker, section):
        rules = BATTLE_MENU_RULES.get(menu, {}).get(attacker, {"sections": 1, "next_levels": {}})
        global_level = getattr(getattr(store, "Pers", None), "global_level", 0)
        next_level = rules["next_levels"].get(section)
        return {
            "show_prev": section > 1,
            "show_next": section < rules["sections"] and next_level is not None and global_level >= next_level,
            "next_locked": section < rules["sections"] and next_level is not None and global_level < next_level,
        }

    def _battle_ability_owner(ability_name):
        """Имя владельца способности по её внутреннему имени.

        Нужно для скидок перезарядки: «Привычка к вращению» — пассивка
        КРИСА, поэтому её уровень нельзя применять к способностям других
        персонажей.
        """
        for ability in BATTLE_ABILITY_DEFINITIONS:
            if ability["name"] == ability_name:
                return ability["owner"]
        return None

    def _battle_owner_level(owner):
        """Уровень владельца способности.

        У каждого персонажа своя функция уровня (kris_passive_level,
        fabri_level и т.д.); неизвестный владелец получает уровень 1,
        чтобы чужие пассивки не «протекали».
        """
        readers = {
            "Крис": kris_passive_level,
            "Азриель": azri_level,
            "Чара": chara_level,
            "Фриск": frisk_level,
            "Иззи": izzy_level,
            "Кловер": clover_level,
            "Арчи": archie_level,
            "Сильвия": sylvia_level,
            "Эмили": emily_level,
            "Сьюзи": susie_level,
        }
        if owner in ("Ральзей", "Ноэлль", "Санс", "Бердли"):
            return int(getattr((getattr(store, "pers_dict", {}) or {}).get(owner), "level", 1) or 1)
        if owner == "Фабри":
            return fabri_level()
        reader = readers.get(owner)
        if reader is None:
            return 1
        return int(reader())

    def _effective_battle_cooldown(ability_name, kind="cooldown_after_use"):
        """Перезарядка способности с учётом улучшений по уровню.

        В реестре у способности может быть задана скидка
        (cooldown_reduction) и уровень, с которого она действует
        (cooldown_reduction_level). Например, «Привычка к вращению» ур.6
        (пассивка Криса) уменьшает перезарядку «С разворота!» на 2.

        Скидка принадлежит владельцу способности, поэтому сравниваем
        уровень владельца, а не всегда уровень Криса.
        """
        data = BATTLE_ABILITY_COOLDOWNS.get(ability_name, {}) or {}
        value = int(data.get(kind, 0) or 0)
        reduction = int(data.get("cooldown_reduction", 0) or 0)
        required_level = int(data.get("cooldown_reduction_level", 0) or 0)
        if reduction and required_level:
            owner = _battle_ability_owner(ability_name)
            if owner is not None and _battle_owner_level(owner) >= required_level:
                value = max(0, value - reduction)
        return value

    def get_battle_ability_current_cd(ability):
        name = ability["name"] if isinstance(ability, dict) else ability
        cds = getattr(store, "battle_ability_current_cds", {})
        if name not in cds:
            cds[name] = _effective_battle_cooldown(name, "initial_cooldown")
        return cds[name]

    def set_battle_ability_current_cd(ability_name, value):
        if not hasattr(store, "battle_ability_current_cds"):
            store.battle_ability_current_cds = {}
        store.battle_ability_current_cds[ability_name] = max(0, int(value))

    def tick_battle_ability_cooldowns(step=1):
        """Уменьшает текущую перезарядку всех способностей на step.

        Вызывается в конце раунда (после атак врага) вместе со снятием
        стаков дебафов.
        """
        cds = getattr(store, "battle_ability_current_cds", None)
        if not cds:
            return
        for ability_name in list(cds.keys()):
            cds[ability_name] = max(0, int(cds[ability_name]) - step)

    def reset_battle_ability_cooldowns():
        """Возвращает перезарядки к изначальным значениям (начало боя).

        initial_cooldown — это значение на начало боя, поэтому словарь
        заполняется заново для всех известных способностей. Дальше каждую
        способность с перезарядкой в конце раунда уменьшает
        tick_battle_ability_cooldowns.

        Для теста способностей в первом раунде есть
        zero_battle_ability_cooldowns().
        """
        store.battle_ability_current_cds = {
            name: _effective_battle_cooldown(name, "initial_cooldown")
            for name in BATTLE_ABILITY_COOLDOWNS
        }

    def reset_battle_one_time_abilities():
        """Одноразовые способности снова доступны (один раз за бой)."""
        store.battle_one_time_used = {}

    def report_battle_ability_cooldowns(owner=None):
        """Возвращает таблицу текущих перезарядок (для консоли и log.txt).

        owner — имя персонажа ("Крис") или его id (1). По умолчанию берётся
        текущий атакующий, owner="all" — все способности.
        """
        cds = getattr(store, "battle_ability_current_cds", {}) or {}
        if owner is None:
            owner = getattr(store, "current_attacker", None)
        if isinstance(owner, str) and owner != "all":
            owner = {"Крис": 1, "Азриель": 2, "Чара": 3, "Фриск": 4,
                     "Иззи": 5, "Кловер": 6, "Седрик": 7, "Арчи": 8,
                     "Сильвия": 9, "Фабри": 10, "Эмили": 11, "Сьюзи": 12,
                     "Ральзей": 13, "Ноэлль": 14, "Санс": 15, "Бердли": 16}.get(owner)
        show_all = owner == "all"

        lines = []
        for ability in BATTLE_ABILITY_DEFINITIONS:
            if not show_all and owner and ability["owner_id"] != owner:
                continue
            name = ability["name"]
            current = cds.get(name, ability.get("initial_cooldown", 0))
            lines.append(
                "{}: сейчас {}, старт {}, после применения {}".format(
                    name, current,
                    ability.get("initial_cooldown", 0),
                    ability.get("cooldown_after_use", 0),
                )
            )
        report = "\n".join(lines) if lines else "нет данных"
        renpy.log("[COOLDOWNS] " + report.replace("\n", " | "))
        return report

    def zero_battle_ability_cooldowns():
        """Тест: обнуляет текущие перезарядки всех способностей.

        Вызывать во время боя (например, из консоли), чтобы проверить
        способности в первом раунде.
        """
        store.battle_ability_current_cds = {
            name: 0 for name in BATTLE_ABILITY_COOLDOWNS
        }
        renpy.log("[COOLDOWNS] все текущие перезарядки обнулены")
        renpy.notify("Перезарядки способностей обнулены (тест).")
        return store.battle_ability_current_cds

    def start_battle_ability_cooldown(ability_name):
        cooldown = _effective_battle_cooldown(ability_name, "cooldown_after_use")
        # «Дробовик» и «Длинный ствол» Кловера: если ствол взорвался,
        # способность уходит на перезарядку вдвое дольше.
        if ability_name == "Дробовик" and bool(getattr(store, "clover_shotgun_exploded", False)):
            cooldown *= 2
            store.clover_shotgun_exploded = False
        if ability_name == "Длинный ствол" and bool(getattr(store, "clover_winchester_exploded", False)):
            cooldown *= 2
            store.clover_winchester_exploded = False
        set_battle_ability_current_cd(ability_name, cooldown)

    def battle_mark_one_time_used(ability_name):
        if not hasattr(store, "battle_one_time_used"):
            store.battle_one_time_used = {}
        store.battle_one_time_used[ability_name] = True

    def battle_one_time_is_used(ability):
        name = ability["name"] if isinstance(ability, dict) else ability
        return getattr(store, "battle_one_time_used", {}).get(name, False)

    def battle_ability_condition_is_met(ability):
        requirements = ability.get("requirements", {})

        # Одноразовые способности: либо доступны, либо «сгорели» навсегда.
        if ability.get("one_time") and battle_one_time_is_used(ability):
            return False
        if get_battle_ability_current_cd(ability) > 0:
            return False

        global_level = getattr(getattr(store, "Pers", None), "global_level", 0)
        if global_level < max(ability.get("level", 0), requirements.get("level", 0)):
            return False
        if "summoned" in requirements and getattr(store, "summoned", 0) != requirements["summoned"]:
            return False
        if "summoned_not" in requirements and getattr(store, "summoned", 0) == requirements["summoned_not"]:
            return False
        # «Размножение личности» Азриеля: магия зависит от текущего облика.
        form_req = requirements.get("form")
        if form_req and azri_current_form() != form_req:
            return False
        char = store.pers_dict.get(ability["owner"])
        # Накопленные действия: «Правильный угол» и «Слабое место» становятся
        # доступны только после нужного количества действий (без перезарядки).
        actions_min = int(requirements.get("actions_min", 0) or 0)
        if actions_min:
            needed = kris_actions_required(ability["name"], actions_min)
            if int(getattr(char, "actions_count", 0) or 0) < needed:
                return False
        hp_state = requirements.get("hp_state")
        if hp_state == "low" and (char is None or char.current_hp > 0.5 * char.max_hp):
            return False
        if hp_state == "high" and (char is None or char.current_hp <= 0.5 * char.max_hp):
            return False
        if requirements.get("mana") and not can_pay_ability_cost(ability["name"], char):
            return False
        # «Гиперлуч» Кловера: доступен только на руте GENO.
        if requirements.get("geno_route") and not clover_geno_route_available():
            return False
        # Фабри: магия фамильяров доступна, только если фамильяр призван.
        fam = requirements.get("familiar")
        if fam and not fabri_familiar_is_summoned(fam):
            return False
        return True

    def battle_ability_button_color(ability):
        return "#ffffff" if battle_ability_condition_is_met(ability) else "#777777"

    def battle_ability_level_is_met(ability):
        requirements = ability.get("requirements", {})
        global_level = getattr(getattr(store, "Pers", None), "global_level", 0)
        return global_level >= max(ability.get("level", 0), requirements.get("level", 0))

    def battle_ability_should_appear(ability):
        """Проверяет, должна ли способность отображаться в меню."""
        if not battle_ability_level_is_met(ability):
            return False

        requirements = ability.get("requirements", {})
        if "summoned" in requirements:
            if getattr(store, "summoned", 0) != requirements["summoned"]:
                return False

        # «Размножение личности»: в меню видны только магии текущего облика.
        form_req = requirements.get("form")
        if form_req and azri_current_form() != form_req:
            return False

        # «Гиперлуч» Кловера: в меню появляется только на руте GENO.
        if requirements.get("geno_route") and not clover_geno_route_available():
            return False

        # Фабри: секция фамильяра видна, только пока он призван; иначе
        # была бы кнопка без эффекта (её скрывает и _condition_is_met).
        fam = requirements.get("familiar")
        if fam and not fabri_familiar_is_summoned(fam):
            return False

        return True

    def battle_ability_action(ability):
        if not battle_ability_condition_is_met(ability):
            return NullAction()
        action_data = ability.get("action", {})
        actions = []
        # Одноразовость и перезарядка фиксируются только в
        # Heroperformsturn после подтверждения цели и успешной оплаты.
        if action_data.get("turntype"):
            actions.append(SetVariable("turntype", action_data["turntype"]))
        actions.append(SetVariable("atk_ind_ratio", 1))
        if action_data.get("set_defend"):
            actions.append(Function(set_defend_action))
        else:
            actions.extend([
                SetVariable("attackindex", ability["name"]),
                SetVariable("attackindexdesc", ability["name"]),
            ])
        if action_data.get("set_defend_target"):
            actions.append(Function(set_defend_target))
        if action_data.get("self_target"):
            actions.append(SetVariable("target", store.pers_dict.get(ability["owner"])))
        if action_data.get("show_target"):
            actions.append(Show("turntarget"))
        if action_data.get("show_name"):
            actions.append(Show("attack_name_display"))
        return actions

    def commit_battle_ability(ability_name):
        ability = next((a for a in BATTLE_ABILITY_DEFINITIONS if a.get("name") == ability_name), None)
        if not ability:
            return
        if ability.get("one_time"):
            battle_mark_one_time_used(ability_name)
        else:
            start_battle_ability_cooldown(ability_name)

    def battle_ability_hover(ability):
        hover = [
            Function(clear_ability_resource_preview),
            SetVariable("attackindexdesc", ability["name"]),
        ]
        if ability.get("hover", {}).get("resource_preview"):
            hover.append(Function(set_ability_resource_preview, ability["name"]))
        hover.append(Show("attack_description"))
        return hover

    def battle_menu_transform(state):
        name = {
            "forward": "from_right_to_left",
            "backward": "from_left_to_right",
            "dissappear_forward": "from_right_to_left2",
            "dissappear_back": "from_left_to_right2",
        }.get(state, "appear")
        return getattr(store, name)

    def get_attack_buttons(attacker, section, summoned, global_level):
        """Возвращает список кнопок атак для текущего атакующего и секции"""
        buttons = []
        
        if attacker == 1:  # Крис
            if section == 1:
                buttons.append({
                    'label': "Удар неудачника",
                    'action': ["turntype", "toenemy", "atk_ind_ratio", 0.6, "attackindex", "Удар неудачника", "attackindexdesc", "Удар неудачника"],
                    'desc': "Удар неудачника"
                })
                buttons.append({
                    'label': "Защищаться",
                    'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "защита_Крис", "attackindexdesc", "защита_Крис"],
                    'desc': "защита_Крис"
                })
                
                # Оружие
                if summoned == 1:
                    buttons.append({'label': "Удар мечом", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар мечом", "attackindexdesc", "Удар мечом"], 'desc': "Удар мечом"})
                    if global_level >= 3:
                        buttons.append({'label': "C разворота!", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "C разворота!", "attackindexdesc", "C разворота!"], 'desc': "C разворота!"})
                elif summoned == 2:
                    buttons.append({'label': "Удар щитом", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар щитом", "attackindexdesc", "Удар щитом"], 'desc': "Удар щитом"})
                    if global_level >= 4:
                        buttons.append({'label': "Бонк!", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Бонк!", "attackindexdesc", "Бонк!"], 'desc': "Бонк!"})
                        
            elif section == 2:
                if summoned == 1:
                    if global_level >= 5:
                        buttons.append({'label': "Пронзить", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Пронзить", "attackindexdesc", "Пронзить"], 'desc': "Пронзить"})
                    if global_level >= 10:
                        buttons.append({'label': "Отчаянное комбо", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Отчаянное комбо", "attackindexdesc", "Отчаянное комбо"], 'desc': "Отчаянное комбо"})
                elif summoned == 2:
                    if global_level >= 6:
                        buttons.append({'label': "Отбить руки", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Отбить руки", "attackindexdesc", "Отбить руки"], 'desc': "Отбить руки"})
                    if global_level >= 10:
                        buttons.append({'label': "Рывок защитника", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Рывок защитника (атака)", "attackindexdesc", "Рывок защитника (атака)"], 'desc': "Рывок защитника (атака)"})
        
        elif attacker == 2:  # Азриель
            if section == 1:
                buttons.append({'label': "Удар принца", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар принца", "attackindexdesc", "Удар принца"], 'desc': "Удар принца"})
                buttons.append({'label': "Защищаться", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "защита_Азриель", "attackindexdesc", "защита_Азриель"], 'desc': "защита_Азриель"})
                buttons.append({'label': "Взмах мечом", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Взмах мечом", "attackindexdesc", "Взмах мечом"], 'desc': "Взмах мечом"})
                buttons.append({'label': "Щитовой удар", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Щитовой удар", "attackindexdesc", "Щитовой удар"], 'desc': "Щитовой удар"})
            elif section == 2:
                if global_level >= 5:
                    buttons.append({'label': "Удар лбом", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар лбом", "attackindexdesc", "Удар лбом"], 'desc': "Удар лбом"})
        
        elif attacker == 3:  # Чара
            if section == 1:
                buttons.append({'label': "Удар бунтарки", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар бунтарки", "attackindexdesc", "Удар бунтарки"], 'desc': "Удар бунтарки"})
                buttons.append({'label': "Защищаться", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "защита_Чара", "attackindexdesc", "защита_Чара"], 'desc': "защита_Чара"})
                buttons.append({'label': "Удар ножом", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар ножом", "attackindexdesc", "Удар ножом"], 'desc': "Удар ножом"})
                buttons.append({'label': "Удар шпагой", 'action': ["turntype", "totarget", "atk_ind_ratio", 1, "attackindex", "Удар шпагой", "attackindexdesc", "Удар шпагой"], 'desc': "Удар шпагой"})
        
        return buttons
    
    def set_defend_action():
        """Устанавливает attackindex и attackindexdesc в зависимости от current_attacker"""
        attacker = store.current_attacker
        names = {1: "защита_Крис", 2: "защита_Азриель", 3: "защита_Чара", 4: "защита_Фриск",
                 5: "защита_Иззи", 6: "защита_Кловер", 7: "защита_Седрик",
                 9: "защита_Сильвия", 10: "защита_Фабри", 11: "защита_Эмили", 12: "защита_Сьюзи",
                 13: "защита_Ральзей", 14: "защита_Ноэлль", 15: "защита_Санс", 16: "защита_Бердли"}
        name = names.get(attacker, "Защищаться")
        store.attackindex = name
        store.attackindexdesc = name
        set_defend_target()

    def set_defend_target():
        """Выбирает текущего персонажа целью собственной защиты."""
        # Индекс = current_attacker - 1, поэтому список обязан совпадать
        # с нумерацией ATTACKER_ORDER (Арчи=8 не игровой, Фабри=10).
        attacker_names = ["Крис", "Азриель", "Чара", "Фриск", "Иззи", "Кловер",
                          "Седрик", "Арчи", "Сильвия", "Фабри", "Эмили", "Сьюзи",
                          "Ральзей", "Ноэлль", "Санс", "Бердли"]
        if isinstance(store.current_attacker, int) and 1 <= store.current_attacker <= len(attacker_names):
            store.target = store.pers_dict[attacker_names[store.current_attacker - 1]]

    def set_defend_desc():
        """Устанавливает attackindexdesc в зависимости от current_attacker (для hovered)"""
        attacker = store.current_attacker
        names = {1: "защита_Крис", 2: "защита_Азриель", 3: "защита_Чара", 4: "защита_Фриск",
                 5: "защита_Иззи", 6: "защита_Кловер", 7: "защита_Седрик",
                 9: "защита_Сильвия", 10: "защита_Фабри", 11: "защита_Эмили", 12: "защита_Сьюзи",
                 13: "защита_Ральзей", 14: "защита_Ноэлль", 15: "защита_Санс", 16: "защита_Бердли"}
        name = names.get(attacker, "Защищаться")
        store.attackindexdesc = name

    def get_switch_button_state(current_section, global_level, min_level_for_next=5):
        """Возвращает состояние кнопок переключения секций"""
        can_go_next = global_level >= min_level_for_next
        is_first_section = current_section == 1
        return {
            'show_prev': not is_first_section,
            'show_next': is_first_section and can_go_next,
            'next_disabled': is_first_section and not can_go_next
        }



############################################################################################################ МЕНЮ ВЫБОР АТАКИ 

# === ДВУХЭТАПНАЯ АНИМАЦИЯ ПЕРЕКЛЮЧЕНИЯ СЕКЦИЙ ===

# Новая секция входит справа и останавливается в центре.
transform from_right_to_left:
    alpha 0.0
    xoffset 200
    ease 0.2 alpha 1.0 xoffset 0

# Новая секция входит слева и останавливается в центре.
transform from_left_to_right:
    alpha 0.0
    xoffset -200
    ease 0.2 alpha 1.0 xoffset 0

# Первое появление содержимого.
transform appear:
    alpha 0.0
    ease 0.2 alpha 1.0

# Содержимое, пришедшее справа, продолжает движение из центра влево.
transform from_right_to_left2:
    alpha 1.0
    xoffset 0
    ease 0.2 alpha 0.0 xoffset -200

# Содержимое, пришедшее слева, продолжает движение из центра вправо.
transform from_left_to_right2:
    alpha 1.0
    xoffset 0
    ease 0.2 alpha 0.0 xoffset 200


# Отдельные переменные для каждого экрана.
default attack_section_switch = None
default attack_section_switch_locked = False
default attack_pending_section = None
default attack_pending_direction = None

default magic_section_switch = None
default magic_section_switch_locked = False
default magic_pending_section = None
default magic_pending_direction = None

default act_section_switch = None
default act_section_switch_locked = False
default act_pending_section = None
default act_pending_direction = None


init python:
    def begin_battle_menu_section_switch(menu_name, target_section, direction):
        """
        Первый этап: текущая section остаётся прежней, а её содержимое уезжает.
        """
        lock_name = menu_name + "_section_switch_locked"

        if getattr(store, lock_name, False):
            return

        setattr(store, menu_name + "_pending_section", target_section)
        setattr(store, menu_name + "_pending_direction", direction)
        setattr(store, lock_name, True)
        renpy.show_screen("stop_switch")

        if direction == "forward":
            setattr(store, menu_name + "_section_switch", "dissappear_forward")

        if direction == "backward":
            setattr(store, menu_name + "_section_switch", "dissappear_back")

        renpy.restart_interaction()


    def finish_battle_menu_section_switch(menu_name):
        """
        Второй этап: через 0.25 секунды меняется section и входит новое содержимое.
        """
        target_section = getattr(store, menu_name + "_pending_section", None)
        direction = getattr(store, menu_name + "_pending_direction", None)

        if target_section is not None:
            store.section = target_section

        if direction == "forward":
            setattr(store, menu_name + "_section_switch", "forward")

        if direction == "backward":
            setattr(store, menu_name + "_section_switch", "backward")

        setattr(store, menu_name + "_pending_section", None)
        setattr(store, menu_name + "_pending_direction", None)
        setattr(store, menu_name + "_section_switch_locked", False)

        renpy.restart_interaction()


screen stop_switch:
    zorder 1000
    timer 0.6 action Hide("stop_switch")

    button:
        xsize 1280
        ysize 720
        background None
        action NullAction()


screen battle_ability_button(ability):
    if battle_ability_level_is_met(ability):
        $ _enabled = battle_ability_condition_is_met(ability)
        $ _color = "#ffffff" if _enabled else "#777777"
        $ _label = ability["label"]

        # Одноразовая использованная способность: серая, БЕЗ «(x N)».
        $ _is_one_time = ability.get("one_time", False)
        $ _one_time_used = _is_one_time and battle_one_time_is_used(ability)

        # Счётчик показывается и у одноразовых способностей, пока они ещё
        # не применены: иначе непонятно, почему кнопка серая в начале боя.
        $ _current_cd = 0 if _one_time_used else get_battle_ability_current_cd(ability)
        $ _button_label = "{} (x{})".format(_label, _current_cd) if _current_cd > 0 else _label

        $ _init_cd  = _effective_battle_cooldown(ability["name"], "initial_cooldown")
        $ _after_cd = _effective_battle_cooldown(ability["name"], "cooldown_after_use")
        $ _show_cd  = (not _is_one_time) and ((_init_cd != 0) or (_after_cd != 0))
        $ _cd_text  = "Перезарядка ({}/{})".format(_init_cd, _after_cd)

        button:
            xsize 345
            ysize 50
            xalign 0.5
            background None
            action [battle_ability_action(ability), Function(clear_ability_resource_preview)]
            hovered battle_ability_hover(ability)
            unhovered [
                Function(clear_ability_resource_preview),
                Hide("attack_description"),
            ]

            text "{font=determination.otf}{size=35}{color=[_color]}[_button_label]":
                xalign 0.5
                text_align 0.5
                yalign 0.5

screen battle_ability_block(attacker, current_section, menu, switch_state):
    $ _abilities = get_battle_abilities(menu, attacker, current_section)
    $ _visible_abilities = [_a for _a in _abilities if battle_ability_should_appear(_a)]
    if _visible_abilities:
        hbox:
            at battle_menu_transform(switch_state)
            xpos 0.2125
            ypos 0.7125
            spacing 20

            for _column in sorted(set(a["column"] for a in _visible_abilities)):
                vbox:
                    spacing 20
                    for _ability in [_a for _a in _visible_abilities if _a["column"] == _column]:
                        use battle_ability_button(_ability)


screen battle_menu_switches(menu):
    $ _navigation = get_battle_menu_navigation(menu, current_attacker, section)

    if _navigation["show_prev"]:
        if prevswitch_style == 0:
            imagebutton:
                idle "images/switchprevous.png"
                at pdu
                action Function(begin_battle_menu_section_switch, menu, section - 1, "backward")
            timer 0.7 action SetVariable("prevswitch_style", 1)
        else:
            imagebutton:
                idle "images/switchprevous.png"
                at pu
                action Function(begin_battle_menu_section_switch, menu, section - 1, "backward")
            timer 0.7 action SetVariable("prevswitch_style", 1)
    else:
        if prevswitch_style == 1:
            imagebutton:
                idle "images/switchprevous.png"
                at pud
                action NullAction()
            timer 0.7 action SetVariable("prevswitch_style", 0)
        else:
            timer 0.7 action SetVariable("prevswitch_style", 0)

    $ _has_next = section < BATTLE_MENU_RULES.get(menu, {}).get(current_attacker, {}).get("sections", 1)
    $ _hide_next_switch = current_attacker == 1 and getattr(store, "summoned", 0) == 0
    if _navigation["show_next"] and not _hide_next_switch:
        if nextswitch_style == 0:
            imagebutton:
                idle "images/switchnext2.png"
                at ndu
                action Function(begin_battle_menu_section_switch, menu, section + 1, "forward")
        else:
            imagebutton:
                idle "images/switchnext2.png"
                at nu
                action Function(begin_battle_menu_section_switch, menu, section + 1, "forward")
        timer 0.7 action SetVariable("nextswitch_style", 1)
    elif _has_next and not _hide_next_switch:
        if nextswitch_style == 0:
            imagebutton:
                idle "images/switchnext2.png"
                at nd
                action NullAction()
        else:
            imagebutton:
                idle "images/switchnext2.png"
                at nud
                action NullAction()
        timer 0.7 action SetVariable("nextswitch_style", 0)
    elif not _hide_next_switch:
        imagebutton:
            idle "images/switchnext2.png"
            at nud
            action NullAction()
        timer 0.7 action SetVariable("nextswitch_style", 0)
    else:
        timer 0.7 action SetVariable("nextswitch_style", 0)


screen choose_attack_screen():

    style_prefix "battle_menu"

    if attack_section_switch_locked:
        timer 0.25 action Function(finish_battle_menu_section_switch, "attack") repeat False

    use battle_menu_switches("attack")
    use battle_ability_block(current_attacker, section, "attack", attack_section_switch)



############################################################################################################### МЕНЮ ВЫБОРА МАГИИ 1
screen choose_magic_screen():

    style_prefix "battle_menu"

    if magic_section_switch_locked:
        timer 0.25 action Function(finish_battle_menu_section_switch, "magic") repeat False

    use battle_menu_switches("magic")
    use battle_ability_block(current_attacker, section, "magic", magic_section_switch)






############################################################################################################ МЕНЮ ВЫБОР ПРЕДМЕТОВ 

transform invapp:
    xpos 300 ypos -900
    easein 0.7 ypos 0
transform invapp2:
    xpos 310 ypos -900
    easein 0.7 ypos 0

image inventory = "inventory.png"

default battle_inventory_type = "consumerables"













init python:
    battle_weapon_name_fallbacks = {
        "wep_water_pistol": "Водяной пистолет",
        "wep_water_bomb": "Водяная бомба",
        "wep_toothpick": "Зубочистка",
        "wep_rubber_band": "Резинка",
        "wep_paper_shooter": "Трубочка с бумажкой",
        "wep_ruler": "Линейка",
        "wep_soap_bubbles": "Мыльные пузыри",
        "wep_poetry_leaf": "Сомнительные стихи",
        "wep_bath_bombs": "Бомбочки для ванной",
        "wep_constructor": "Конструктор",
        "wep_flashlight": "Фонарик",
    }

    def get_battle_item_name(item_id, name_map):
        """Возвращает локализованное имя предмета в боевом инвентаре."""
        if item_id in name_map:
            return name_map[item_id]

        if item_id in battle_weapon_name_fallbacks:
            return battle_weapon_name_fallbacks[item_id]

        if isinstance(item_id, str) and item_id.startswith("wep_"):
            cleaned = item_id.replace("wep_", "").replace("_", " ")
            return cleaned[:1].upper() + cleaned[1:]

        return item_id

    def get_inventory_desc_lines(item_id):
        """Собирает описание эффектов расходника по уровням (1/2/3)."""
        if not item_id:
            return []

        def has_effect(value):
            return value not in (0, 0.0, None, False, "", [])

        def as_percent(value):
            return int(round(value * 100)) if isinstance(value, float) else value

        def pretty_number(value):
            if isinstance(value, float):
                rounded = round(value)
                if abs(value - rounded) < 0.000001:
                    return int(rounded)
            return value

        def append_line_if_has(lines_list, effects, key, line_builder):
            value = effects.get(key, 0)
            if has_effect(value):
                lines_list.append(line_builder(value))

        def resolve_debuff_name(debuff_type, value):
            fallback_names = {
                "atk": (u"Истощение", u"Бодрость"),
                "def": (u"Печаль", u"Вдохновение"),
                "magic": (u"Помутнение", u"Просвещение"),
                "accuracy": (u"Страх", u"Концентрация"),
                "critrate": (u"Сглаз", u"Удача"),
                "critdmg": (u"Безразличие", u"Гнев"),
                "sad": (u"Грусть", u"Грусть"),
                "apatia": (u"Апатия", u"Апатия"),
                "happy": (u"Радость", u"Радость"),
            }

            if debuff_type == "critdmg":
                pair = fallback_names.get(debuff_type)
                if pair:
                    return pair[0] if value > 0 else pair[1]

            if hasattr(store, "get_debuff_name"):
                name = store.get_debuff_name(debuff_type, value)
                if name:
                    return name

            pair = fallback_names.get(debuff_type)
            if pair:
                return pair[0] if value > 0 else pair[1]

            return debuff_type.upper()

        def build_universal_debuff_line(effect_key, value):
            if not isinstance(effect_key, str) or "_debuff" not in effect_key:
                return None

            target_label = u""
            key_name = effect_key

            if key_name.startswith("enemy_"):
                target_label = u" "
                key_name = key_name[len("enemy_"):]

            if key_name.endswith("_all_picked"):
                target_label = u" всем"
                key_name = key_name[:-len("_all_picked")]

            if not key_name.endswith("_debuff"):
                return None

            debuff_type = key_name[:-len("_debuff")]
            if not debuff_type:
                return None

            debuff_name = resolve_debuff_name(debuff_type, value)

            if not debuff_name:
                fallback_names = {
                    "sad": u"Грусть",
                    "apatia": u"Апатия",
                    "happy": u"Радость",
                }
                debuff_name = fallback_names.get(debuff_type, debuff_type.upper())

            return u"{}{}: x{}".format(debuff_name, target_label, abs(int(value)))

        level_specs = [
            (
                1,
                #"{size=1}{color=#000000}Свойства{/color}{/size}",
                #"{size=35}{color=#ffffff}{b}Свойства{/b}{/color}{/size}",
                "{size=30}{color=#ffffff}Свойства{/color}{/size}",
                [
                    ("hp_heal", lambda v: u"HP: {}".format(pretty_number(v))),
                    ("hp_percent", lambda v: u"HP: {}%".format(pretty_number(as_percent(v)))),
                    ("mp_heal", lambda v: u"MP: {}".format(pretty_number(v))),
                    ("shield_heal", lambda v: u"Щит: {}".format(pretty_number(v))),
                    ("hp_regen", lambda v: u"HP реген: {}".format(pretty_number(v))),
                    ("hp_heal_all_picked", lambda v: u"HP всем: {}".format(pretty_number(v))),
                    ("hp_percent_all_picked", lambda v: u"HP команде:{}%".format(pretty_number(as_percent(v)))),
                    ("over_heal", lambda v: u"Сверхлечение"),
                    ("damage", lambda v: u"Урон: {}".format(pretty_number(v))),
                    ("damage_single", lambda v: u"Урон: {}".format(pretty_number(v))),
                    ("damage_allies", lambda v: u"Урон союзникам: {}".format(pretty_number(v))),
                    ("revive", lambda v: u"Поднимает павшего"),
                ],
            ),
            (
                2,
                "{size=30}{color=#ffffff}Дебаффы/баффы{u}{/u}{/color}{/size}",
                [
                    ("bleeding", lambda v: u"Кровотечение: x{}".format(pretty_number(v))),
                    ("enemy_atk_debuff", lambda v: u"{} цели: x{}".format(resolve_debuff_name(u"atk", v), pretty_number(abs(v * 1)))),
                    ("enemy_def_debuff", lambda v: u"{} цели: x{}".format(resolve_debuff_name(u"def", v), pretty_number(abs(v * 1)))),
                    ("enemy_magic_debuff", lambda v: u"{} цели: x{}".format(resolve_debuff_name(u"magic", v), pretty_number(abs(v * 1)))),
                    ("enemy_accuracy_debuff", lambda v: u"{} цели: x{}".format(resolve_debuff_name(u"accuracy", v), pretty_number(abs(v * 1)))),
                    ("enemy_critrate_debuff", lambda v: u"{} цели: x{}".format(resolve_debuff_name(u"critrate", v), pretty_number(abs(v * 1)))),
                    ("enemy_critdmg_debuff", lambda v: u"{} цели: x{}".format(resolve_debuff_name(u"critdmg", v), pretty_number(abs(v * 1)))),
                ],
            ),
            (
                3,
                "{size=30}{color=#ffffff}Бонусы/штрафы{u}{/u}{/color}{/size}",
                [
                    ("enemy_bonus_atk_debuff", lambda v: u"Атака цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_atk", lambda v: u"Атака цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_magic_debuff", lambda v: u"Магия цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_magic", lambda v: u"Магия цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_accuracy_debuff", lambda v: u"Точность цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_accuracy", lambda v: u"Точность цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_critrate_debuff", lambda v: u"Критшанс цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_critrate", lambda v: u"Критшанс цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_critdmg_debuff", lambda v: u"Критурон цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_critdmg", lambda v: u"Критурон цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_speed_debuff", lambda v: u"Скорость цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_def_debuff", lambda v: u"Защита цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_bonus_def", lambda v: u"Защита цели: {}%".format(pretty_number(-v * 100))),
                    ("enemy_base_atk_debuff", lambda v: u"Атака цели: {}".format(pretty_number(-v))),
                    ("enemy_base_atk", lambda v: u"Атака цели: {}".format(pretty_number(-v))),
                    ("enemy_base_def_debuff", lambda v: u"Защита цели: {}".format(pretty_number(-v))),
                    ("enemy_base_def", lambda v: u"Защита цели: {}".format(pretty_number(-v))),

                    ("bonus_atk", lambda v: u"Атака: {}%".format(pretty_number(v * 100))),
                    ("bonus_def", lambda v: u"Защита: {}%".format(pretty_number(v * 100))),
                    ("bonus_magic", lambda v: u"Магия: {}%".format(pretty_number(v * 100))),
                    ("bonus_accuracy", lambda v: u"Точность: {}%".format(pretty_number(v * 100))),
                    ("bonus_critrate", lambda v: u"Критшанс: {}%".format(pretty_number(v * 100))),
                    ("bonus_critdmg", lambda v: u"Критурон: {}%".format(pretty_number(v * 100))),
                    ("bonus_tank", lambda v: u"Танк: {}".format(pretty_number(v))),
                    ("bonus_perform", lambda v: u"Выступление: {}".format(pretty_number(v))),
                    ("bonus_socialization", lambda v: u"Социализация: {}".format(pretty_number(v))),
                    ("bonus_diplomacy", lambda v: u"Дипломатия: {}".format(pretty_number(v))),
                    ("bonus_charm", lambda v: u"Очарование: {}".format(pretty_number(v))),
                    ("bonus_perception", lambda v: u"Восприятие: {}".format(pretty_number(v))),
                    ("bonus_rhetoric", lambda v: u"Риторика: {}".format(pretty_number(v))),
                    ("bonus_artistry", lambda v: u"Артистизм: {}".format(pretty_number(v))),
                    ("bonus_comfort", lambda v: u"Комфорт: {}".format(pretty_number(v))),
                    ("bonus_power", lambda v: u"Власть: {}".format(pretty_number(v))),
                    ("bonus_socialization_all_picked", lambda v: u"Социализация всех: {}".format(pretty_number(v))),
                    ("merchant_relation_bonus", lambda v: u"Торговля: {}%".format(pretty_number(v))),
                    ("soul_speed", lambda v: u"Скорость цели: {:+}%".format(pretty_number(v * 10))),

                    #("ordinarynumber", lambda v: u"• ordinarynumber: +{}".format(v)),
                ],
            ),
        ]

        lines = []
        for level, title, checks in level_specs:
            getter_name = "get_consumable_item_effects_level{}".format(level)
            effects = getattr(store, getter_name)(item_id) if hasattr(store, getter_name) else {}
            level_lines = []
            rendered_keys = set()
            for key, builder in checks:
                value = effects.get(key, 0)
                if has_effect(value):
                    level_lines.append(builder(value))
                    rendered_keys.add(key)

            if level == 2:
                for effect_key in sorted(effects.keys()):
                    effect_value = effects.get(effect_key, 0)
                    if not has_effect(effect_value):
                        continue
                    if effect_key in rendered_keys:
                        continue

                    debuff_line = build_universal_debuff_line(effect_key, effect_value)
                    if debuff_line:
                        level_lines.append(debuff_line)

            if level_lines:
                lines.append(title)
                lines.extend(level_lines)

        if hasattr(store, "consumable_prices") and item_id in store.consumable_prices:
            #lines.append(u"Цена: {}".format(store.consumable_prices[item_id]))
            pass
        return lines

    def build_battle_item_stacks(items_source):
        """Собирает стакнутый список предметов для боевого инвентаря."""
        stacks = {}
        order = []

        def add_item(item_id, count=1):
            if not item_id:
                return

            try:
                count = int(count)
            except Exception:
                count = 1

            if count <= 0:
                return

            if item_id not in stacks:
                stacks[item_id] = 0
                order.append(item_id)
            stacks[item_id] += count

        if hasattr(items_source, "items"):
            for item_id, count in items_source.items():
                add_item(item_id, count)
        elif isinstance(items_source, (list, tuple)):
            for item in items_source:
                if isinstance(item, dict):
                    add_item(item.get("id"), item.get("count", 1))
                elif isinstance(item, (list, tuple)) and len(item) >= 2:
                    add_item(item[0], item[1])
                else:
                    add_item(item, 1)

        return [(item_id, stacks[item_id]) for item_id in order]

style battle_inventory_hbar is scrollbar:
    ysize 50
    base_bar Solid("#000000")
    thumb Solid("#ffffff")
    unscrollable "hide"

screen inventory_desc:
    zorder 120

    #if hovered_artifact_id:
    $ item_id = attackindexdesc
    $ inv_name_map = getattr(store, "consumable_names", {})
    $ inv_item_name = get_battle_item_name(item_id, inv_name_map)
    $ inv_desc_lines = get_inventory_desc_lines(item_id)
    #if attackindexdesc == "food_lucky_monstercandy":
    #    $ visible_inv_desc_lines = ["случайный эффект"]
    #else:
    $ visible_inv_desc_lines = inv_desc_lines[:10]
    $ inv_desc_height = max(120, 80 + (len(visible_inv_desc_lines) * 47))

    hbox:
        at invent_1
        #xalign 0.01
        #ypos 110
        #spacing 24

        frame:
            background "#ffffff"
            xsize 340
            ysize 350
            padding (4, 4)

            frame:
                background "#000000"
                xfill True
                yfill True
                padding (16, 16)

                vbox:
                    spacing 12
                    xalign 0.5
                    yalign 0.0

                    text "{font=determination.otf}{size=28}[inv_item_name]{/size}{/font}" color "#ffffff" xalign 0.5 text_align 0.5
                    
                    #text "{font=determination.otf}{size=28}[attackindexdesc]{/size}{/font}" color "#ffffff" xalign 0.5 text_align 0.5

                    frame:
                        background "#ffffff"
                        xsize 220
                        ysize 220
                        padding (3, 3)
                        xalign 0.5

                        frame:
                            background "#000000"
                            xfill True
                            yfill True

                            if item_id:
                                add f"{inv_item_name}.png" xysize (80, 80) xalign 0.5 yalign 0.5

    hbox:
        at invent_2
        #xalign 0.99
        #ypos 110
        #spacing 24
        frame:
            background "#ffffff"
            xsize 340
            if attackindexdesc == "food_lucky_monstercandy":
                ysize 300
            elif attackindexdesc == "wep_poetry_leaf":
                ysize 200
            elif attackindexdesc == "wep_flashlight":
                ysize 390
            elif attackindexdesc == "wep_bath_bombs":
                ysize 250
            else:
                ysize inv_desc_height - 20
            padding (4, 4)

            frame:
                background "#000000"
                xfill True
                yfill True
                padding (16, 16)

                vbox:
                    spacing 20
                    xfill True

                    #text "{font=determination.otf}{size=28}Свойства{/size}{/font}" color "#ffffff"

                    if attackindexdesc == "food_lucky_monstercandy":
                        vbox:
                            spacing 20
                            xalign 0.5 
                            text "{font=determination.otf}{size=30}Случайный эффект \nот 1 из 6 вкусов:{/size}{/font}" text_align 0.5
                            vbox:
                                xalign 0.5 
                                text "{font=determination.otf}{size=25}Ириска{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Кофе{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Чистая вода{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Слиток золота{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Острый чили{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Сточная канава{/size}{/font}" text_align 0.5 xalign 0.5
                    elif attackindexdesc == "wep_bath_bombs":
                        vbox:
                            spacing 20
                            xalign 0.5
                            text "{font=determination.otf}{size=35}Свойства{/size}{/font}" text_align 0.5 xalign 0.5
                            vbox:
                                spacing 25
                                xalign 0.5 
                                text "{font=determination.otf}{size=25}Урон цели: 40{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Урон всем остальным в бою: 20{/size}{/font}" text_align 0.5 xalign 0.5
                    elif attackindexdesc == "wep_flashlight":
                        vbox:
                            spacing 40
                            xalign 0.5 
                            text "{font=determination.otf}{size=35}Бонусы/штрафы{/size}{/font}" text_align 0.5
                            vbox:
                                spacing 25
                                xalign 0.5 
                                text "{font=determination.otf}{size=25}Критшанс цели: -5%{/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=35}Танк от цели:{/size}{/font}" text_align 0.5 xalign 0.5
                                vbox:
                                    spacing 15
                                    xalign 0.5 
                                    text "{font=determination.otf}{size=25}Если цель - враг:\n +5 у применившего{/size}{/font}" text_align 0.5 xalign 0.5
                                    text "{font=determination.otf}{size=25}Если цель - друг:\n +5 у цели{/size}{/font}" text_align 0.5 xalign 0.5
                                
                    elif attackindexdesc == "wep_poetry_leaf":
                        vbox:
                            spacing 20
                            xalign 0.5 
                            text "{font=determination.otf}{size=30}Эффект слабеет с \nкаждым разом:{/size}{/font}" text_align 0.5 
                            vbox:
                                xalign 0.5 
                                text "{font=determination.otf}{size=25}Базовая атака: -3 {/size}{/font}" text_align 0.5 xalign 0.5
                                text "{font=determination.otf}{size=25}Базовая защита: -3 {/size}{/font}" text_align 0.5 xalign 0.5                    

                    else:
                        for line in visible_inv_desc_lines:
                            text "{font=determination.otf}{size=25}[line]{/size}{/font}" color "#ffffff" xalign 0.5
                        


transform invent_1:
    on show:
        xpos -300 ypos 100 alpha 0.0
        pause 0.5
        easein 0.5 xpos 10 alpha 1.0
    on hide:
        easein 0.5 xoffset -50 alpha 0.0

transform invent_2:
    on show:
        xpos 1580 ypos 100
        pause 0.5
        easein 0.5 xpos 930 alpha 1.0
    on hide:
        easein 0.5 xoffset 50 alpha 0.0























screen itemchoice2:
    zorder 1

    $ all_battle_items = build_battle_item_stacks(getattr(store, "consumable_inventory", {}))
    $ consumable_items = [(item_id, count) for item_id, count in all_battle_items if not item_id.startswith("wep_")]
    $ weapon_items = [(item_id, count) for item_id, count in all_battle_items if item_id.startswith("wep_")]
    $ shown_items = consumable_items if battle_inventory_type == "consumerables" else weapon_items

    $ name_map = getattr(store, "consumable_names", {})

    $ items_per_column = 4
    $ column_count = max((len(shown_items) + items_per_column - 1) // items_per_column, 1)
    $ item_columns = [shown_items[i * items_per_column:(i + 1) * items_per_column] for i in range(column_count)]



    frame:
        background "#ffffff"
        xalign 0.5
        ypos 100
        xsize 560
        ysize 360
        padding (4, 4)

        frame:
            
            background "#000000"
            xfill True
            yfill True
            padding (24, 24)

            vbox:
                spacing 40
                xfill True
                yfill True

                frame:
                    background "#000000"
                    xfill True
                    yfill True

                    #side "c b":
                    viewport:
                        id "itemchoice2_grid_viewport"
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True

                        hbox:
                            spacing 10

                            for column_items in item_columns:
                                vbox:
                                    spacing 10

                                    for item_id, count in column_items:
                                        textbutton "{font=determination.otf}{size=30}[get_battle_item_name(item_id, name_map)] ([int(count)]){/size}{/font}":
                                            text_color "#ffffff"
                                            text_layout "nobreak"
                                            action [
                                                SetVariable("itemchoice", 1),
                                                SetVariable("turntype", "totarget"),
                                                SetVariable("attackindex", item_id),
                                                SetVariable("attackindexdesc", item_id),
                                                SetVariable("hovered_artifact_id", item_id),
                                                Show("turntarget"),
                                                Show("attack_name_display"),
                                            ]
                                            hovered [
                                                SetVariable("attackindexdesc", item_id),
                                                #SetVariable("hovered_artifact_id", item_id),
                                                #Show("attack_description"),
                                                Show("inventory_desc"),
                                            ]
                                            unhovered [
                                                #SetVariable("hovered_artifact_id", None),
                                                Hide("attack_description"),
                                                Hide("inventory_desc"),
                                            ]

                frame:
                    xsize 757
                    ysize 60
                    yoffset 40+30
                    xoffset -138
                    background "#ffffff"
                    bar:
                        xalign 0.5 yalign 0.5
                        xsize 747
                        #yoffset 60
                        #xoffset -100
                        style "battle_inventory_hbar"
                        value XScrollValue("itemchoice2_grid_viewport")

    #hbox:
    #    spacing 28
    #    xalign 0.5
    
    #frame:
    #    xysize(170,120)
    #    xalign 0.05
    #    yalign 0.9
    



    #    textbutton "{font=determination.otf}{size=34}Расходники{/size}{/font}":
    #        action SetVariable("battle_inventory_type", "consumerables")

    #    textbutton "{font=determination.otf}{size=34}Оружие{/size}{/font}":
    #        action SetVariable("battle_inventory_type", "weapon")



screen act_action_button(action_name):
    button:
        xsize 345
        ysize 50
        xalign 0.5
        background None

        text "{font=determination.otf}{size=35}[action_name]":
            xalign 0.5
            text_align 0.5
            yalign 0.5
            color get_act_button_color(action_name)

        action (make_act_action_list(action_name) if target is not None else Show("please_choose_target"))

        hovered [
            SetVariable("attackindexdesc", action_name),
            Show("attack_description"),
        ]
        unhovered [Hide("attack_description")]


############################################################################################################ МЕНЮ ВЫБОРА ДЕЙСТВИЯ 1


screen actchoice1():
    style_prefix "battle_menu"

    # Меняем section только после завершения выходной анимации.
    if act_section_switch_locked:
        timer 0.25 action Function(finish_battle_menu_section_switch, "act") repeat False

    # ==========================================================
    # СЕКЦИЯ 1
    # ==========================================================
    if section == 1:
        # Крайняя секция — кнопка "назад" неактивна
        if prevswitch_style == 0:
            imagebutton:
                idle "images/switchprevous.png"
                at pd
                action NullAction()
            timer 0.5 action SetVariable("prevswitch_style", 0)
        if prevswitch_style == 1:
            imagebutton:
                idle "images/switchprevous.png"
                at pud
                action NullAction()
            timer 0.5 action SetVariable("prevswitch_style", 0)

        if nextswitch_style == 1:
            imagebutton:
                idle "images/switchnext2.png"
                at nu
                action Function(begin_battle_menu_section_switch, "act", 2, "forward")
            timer 0.5 action SetVariable("nextswitch_style", 1)
        if nextswitch_style == 0:
            imagebutton:
                idle "images/switchnext2.png"
                at ndu
                action Function(begin_battle_menu_section_switch, "act", 2, "forward")
            timer 0.5 action SetVariable("nextswitch_style", 1)

        if act_section_switch == "forward":
            hbox:
                at from_right_to_left
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Оценить")
                    use act_action_button("Вопрос")
                vbox:
                    spacing 20
                    use act_action_button("Убеждение")
                    use act_action_button("Рассказать")

        if act_section_switch == "backward":
            hbox:
                at from_left_to_right
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Оценить")
                    use act_action_button("Вопрос")
                vbox:
                    spacing 20
                    use act_action_button("Убеждение")
                    use act_action_button("Рассказать")

        if act_section_switch is None:
            hbox:
                at appear
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Оценить")
                    use act_action_button("Вопрос")
                vbox:
                    spacing 20
                    use act_action_button("Убеждение")
                    use act_action_button("Рассказать")

        if act_section_switch == "dissappear_forward":
            hbox:
                at from_right_to_left2
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Оценить")
                    use act_action_button("Вопрос")
                vbox:
                    spacing 20
                    use act_action_button("Убеждение")
                    use act_action_button("Рассказать")

        if act_section_switch == "dissappear_back":
            hbox:
                at from_left_to_right2
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Оценить")
                    use act_action_button("Вопрос")
                vbox:
                    spacing 20
                    use act_action_button("Убеждение")
                    use act_action_button("Рассказать")

    # ==========================================================
    # СЕКЦИЯ 2
    # ==========================================================
    if section == 2:
        if prevswitch_style == 0:
            imagebutton:
                idle "images/switchprevous.png"
                at pdu
                action [Function(begin_battle_menu_section_switch, "act", 1, "backward"), SetVariable("prevswitch_style", 1), SetVariable("nextswitch_style", 1)]
        if prevswitch_style == 1:
            imagebutton:
                idle "images/switchprevous.png"
                at pu
                action [Function(begin_battle_menu_section_switch, "act", 1, "backward"), SetVariable("prevswitch_style", 1), SetVariable("nextswitch_style", 1)]
            timer 0.5 action SetVariable("prevswitch_style", 1)

        if nextswitch_style == 0:
            timer 0.5 action SetVariable("nextswitch_style", 1)
            imagebutton:
                idle "images/switchnext2.png"
                at ndu
                action Function(begin_battle_menu_section_switch, "act", 3, "forward")
        if nextswitch_style == 1:
            timer 0.5 action SetVariable("nextswitch_style", 1)
            imagebutton:
                idle "images/switchnext2.png"
                at nu
                action Function(begin_battle_menu_section_switch, "act", 3, "forward")

        if act_section_switch == "forward":
            hbox:
                at from_right_to_left
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Поддержать")
                    use act_action_button("Играть")
                vbox:
                    spacing 20
                    use act_action_button("Запугать")
                    use act_action_button("Грубить")

        if act_section_switch == "backward":
            hbox:
                at from_left_to_right
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Поддержать")
                    use act_action_button("Играть")
                vbox:
                    spacing 20
                    use act_action_button("Запугать")
                    use act_action_button("Грубить")

        if act_section_switch is None:
            hbox:
                at appear
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Поддержать")
                    use act_action_button("Играть")
                vbox:
                    spacing 20
                    use act_action_button("Запугать")
                    use act_action_button("Грубить")

        if act_section_switch == "dissappear_forward":
            hbox:
                at from_right_to_left2
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Поддержать")
                    use act_action_button("Играть")
                vbox:
                    spacing 20
                    use act_action_button("Запугать")
                    use act_action_button("Грубить")

        if act_section_switch == "dissappear_back":
            hbox:
                at from_left_to_right2
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Поддержать")
                    use act_action_button("Играть")
                vbox:
                    spacing 20
                    use act_action_button("Запугать")
                    use act_action_button("Грубить")

    # ==========================================================
    # СЕКЦИЯ 3
    # ==========================================================
    if section == 3:
        imagebutton:
            idle "images/switchprevous.png"
            at pu
            action Function(begin_battle_menu_section_switch, "act", 2, "backward")
        timer 0.5 action SetVariable("prevswitch_style", 1)

        imagebutton:
            idle "images/switchnext2.png"
            at nud
            action NullAction()
        timer 0.5 action SetVariable("nextswitch_style", 0)

        if act_section_switch == "forward":
            hbox:
                at from_right_to_left
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Исполнение")
                    use act_action_button("Унижаться")
                vbox:
                    spacing 20
                    use act_action_button("Дразнить")
                    use act_action_button("Пощадить")

        if act_section_switch == "backward":
            hbox:
                at from_left_to_right
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Исполнение")
                    use act_action_button("Унижаться")
                vbox:
                    spacing 20
                    use act_action_button("Дразнить")
                    use act_action_button("Пощадить")

        if act_section_switch is None:
            hbox:
                at appear
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Исполнение")
                    use act_action_button("Унижаться")
                vbox:
                    spacing 20
                    use act_action_button("Дразнить")
                    use act_action_button("Пощадить")

        if act_section_switch == "dissappear_forward":
            hbox:
                at from_right_to_left2
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Исполнение")
                    use act_action_button("Унижаться")
                vbox:
                    spacing 20
                    use act_action_button("Дразнить")
                    use act_action_button("Пощадить")

        if act_section_switch == "dissappear_back":
            hbox:
                at from_left_to_right2
                xpos 0.2125 ypos 0.7125
                spacing 20
                vbox:
                    spacing 20
                    use act_action_button("Исполнение")
                    use act_action_button("Унижаться")
                vbox:
                    spacing 20
                    use act_action_button("Дразнить")
                    use act_action_button("Пощадить")
