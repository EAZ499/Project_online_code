#                                                                                                                                                                      @@@@@@ 
#                                                                                                                                                                   @@@@ 
#                                                                                                                                                                @@@ 
#                                                                                                                                                               @@@@@@ 
#                                                                                                                                                             @@@@                                                               
#               @@@@        @@@@   @@@@@@@@@@@@@@@@                @@@@        @@@@@               @@@@@           @@@@@      @@@@@@@@@@@@@@@@               @@@@   @@@@@@           @@@@@@@@@@@       @@@@ @@@@@@@@@            
#                @@@@     @@@@@    @@@@@@@@@@@@@@@@                @@@@       @@@@@@               @@@@@@         @@@@@@      @@@@@@@@@@@@@@@@               @@@@@@@@@@@@@@@@       @@@@@@@@@@@@@      @@@@@@@@@@@@@@@@          
#                 @@@@   @@@@      @@@@        @@@@                @@@@      @@@@@@@               @@@@@@@        @@@@@@      @@@@        @@@@               @@@@@@      @@@@@      @         @@@@     @@@@@        @@@@         
#                  @@@@ @@@@       @@@@        @@@@                @@@@    @@@@@@@@@               @@@@@@@       @@@@@@@      @@@@        @@@@               @@@@         @@@@@               @@@@     @@@@         @@@@@        
#                   @@@@@@@        @@@@        @@@@                @@@@   @@@@  @@@@               @@@@@@@@     @@@@ @@@      @@@@        @@@@               @@@@          @@@@       @@@@@@@@@@@@     @@@@          @@@@        
#                    @@@@@         @@@@        @@@@                @@@@  @@@@   @@@@               @@@@ @@@@    @@@  @@@      @@@@        @@@@               @@@@           @@@   @@@@@@@@@@@@@@@     @@@@          @@@@        
#                   @@@@@@@        @@@@        @@@@                @@@@@@@@@    @@@@               @@@@  @@@   @@@   @@@      @@@@        @@@@               @@@@           @@@   @@@@@       @@@@     @@@@          @@@@        
#                  @@@@ @@@@@      @@@@        @@@@                @@@@@@@@     @@@@               @@@@  @@@@ @@@@   @@@      @@@@        @@@@               @@@@           @@@@   @@@@        @@@@     @@@@          @@@@        
#                @@@@@   @@@@@     @@@@        @@@@                @@@@@@@      @@@@               @@@@   @@@@@@@    @@@      @@@@        @@@@                @@@@@      @@@@@    @@@@@     @@@@@@     @@@@@       @@@@@         
#               @@@@@     @@@@@    @@@@        @@@@                @@@@@        @@@@               @@@@    @@@@@     @@@      @@@@        @@@@                 @@@@@@@@@@@@@@      @@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@           
#              @@@@@        @@@@   @@@@        @@@@                @@@@         @@@@               @@@@      @@@      @@@      @@@@        @@@@                    @@@@@@@@@          @@@@@@@  @@@@     @@@@ @@@@@@@@             
#                                                                                                                                                                                                     
#                                                                                                                                                                                                     
#                                                                                                                                                                                                     
#                                                                                                                                                                                                     
#                                                                                                                                                                                                     
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
#                 @@@@            @@@@@         @@@@@@@@        @@@@         @@@      @@@@         @@@@@@@@@                    @@@@@@@@@@     @@@@@@@@@@@@@@@@    @@@@@@@@@@        @@@       @@@@@   @@@@         @@@@         
#                 @@@@@          @@@@@@      @@@@@@@@@@@@@      @@@@         @@@      @@@@      @@@@@@@@@@@@@@                 @@@@@@@@@@@@@   @@@@@@@@@@@@@@@@   @@@@@@@@@@@@@      @@@@     @@@@@    @@@@       @@@@@@         
#                 @@@@@@        @@@@@@@     @@@@@      @@@@     @@@@         @@@      @@@@     @@@@@       @@@@                @@       @@@@         @@@@         @@       @@@@      @@@@   @@@@@      @@@@      @@@@@@@         
#                 @@@@@@@       @@@@@@@    @@@@         @@@@    @@@@         @@@      @@@@     @@@@         @@@@                         @@@@        @@@@                   @@@@     @@@@ @@@@@        @@@@     @@@@@@@@         
#                 @@@ @@@      @@@ @@@@    @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@      @@@@@@@@@@@@          @@@@                   @@@@@@@@@@        @@@@            @@@@@@@@@@@     @@@@@@@@          @@@@   @@@@ @@@@         
#                 @@@ @@@@    @@@@ @@@@    @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@      @@@@@@@@@@@@          @@@@               @@@@@@@@@@@@@@        @@@@         @@@@@@@@@@@@@@     @@@@@@@@           @@@@   @@@@  @@@@         
#                 @@@  @@@@  @@@@  @@@@    @@@@                 @@@@         @@@      @@@@    @@@@          @@@@              @@@@@      @@@@        @@@@       @@@@@       @@@@     @@@@@@@@@         @@@@ @@@@@   @@@@         
#                 @@@   @@@@ @@@   @@@@    @@@@                 @@@@         @@@      @@@@     @@@@        @@@@             @@@@        @@@@        @@@@       @@@@        @@@@     @@@@ @@@@@        @@@@@@@@     @@@@         
#                 @@@    @@@@@@@   @@@@     @@@@          @     @@@@         @@@      @@@@     @@@@        @@@@              @@@@       @@@@@        @@@@       @@@@      @@@@@@     @@@@   @@@@@      @@@@@@@      @@@@         
#                 @@@    @@@@@@    @@@@      @@@@@@@@@@@@@@     @@@@         @@@      @@@@      @@@@@@@@@@@@@@                @@@@@@@@@@@@@@@        @@@@       @@@@@@@@@@@@@@@@     @@@@     @@@@@    @@@@@@       @@@@         
#                 @@@     @@@@     @@@@        @@@@@@@@@@@      @@@@         @@@      @@@@        @@@@@@@@@@                   @@@@@@@@@ @@@@        @@@@         @@@@@@@@  @@@@     @@@@      @@@@@@  @@@@@        @@@@         
#                                                                                                                                                                                                                                 
#                                                                                                                                                                                                                                 
#                                                                                                                                                                                                                                 
#                                                                                                                                                                                                                                 
#                                                                                                                                                                                                                                 
# 
# 

# character_picked_for_shift теперь будет свойством, которое автоматически вычисляется на основе количества персонажей в команде
init python:
    import math

    # === КЭШИРОВАНИЕ ДЛЯ character_status_card ===
    if not hasattr(store, "hp_mp_bar_cache"):
        store.hp_mp_bar_cache = {}
    if not hasattr(store, "char_status_cache"):
        store.char_status_cache = {}

    # Стоимость магии. Значения намеренно заданы централизованно: интерфейс,
    # проверка перед ходом и последующее списание используют одну таблицу.
    # Форматы стоимости:
    # {"mp": 10} — фиксированные 10 MP;
    # {"mp_percent": 0.20} — 20% от максимального MP героя;
    # {"mp": 5, "mp_percent": 0.10} — 5 MP + 10% от максимального MP.
    # Полученная сумма умножается на коэффициент персонажа:
    # mp_cost_multiplier + mpcostartifactmod, затем округляется вверх.
    ABILITY_RESOURCE_COSTS = {
        # Крис: 10 — Призвать меч; 11 — Призвать щит; 12 — Напрячься;
        # 13 — Позвать за щит; 14 — Правильный угол; 15 — Слабое место;
        # 16 — Концентрация; 17 — Поднять щиты!; 18 — Стремление вперёд;
        # 19 — Рывок защитника; 20 — Пробудиться.
        "Призвать меч": {"mp": 20}, "Призвать щит": {"mp": 4}, "Напрячься": {"mp": 6}, "Позвать за щит": {"mp": 6},
        "Правильный угол": {"mp": 8}, "Слабое место": {"mp": 8}, "Концентрация": {"mp": 10}, "Поднять щиты!": {"mp": 12},
        "Стремление вперёд": {"mp": 14}, "Рывок защитника (магия)": {"mp": 16}, "Пробудиться": {"mp": 18},
        # Азриель: 25 — Сменить облик; 26 — Шаг вперёд; 27 — Магия огня;
        # 28 — Горное равновесие; 29 — Клинки хаоса; 30 — За спиною принца;
        # 31 — Уничтожитель хаоса; 32 — Встать с колен; 33 — Звёздный блеск;
        # 34 — Боевой клич!; 35 — Луч Бога Гиперсмерти.
        # Стоимости — из ТЗ дизайнера.
        "Сменить облик": {"mp": 0},
        "Шаг вперёд": {"mp": 6}, "Магия огня": {"mp": 13}, "Горное равновесие": {"mp": 15}, "Клинки хаоса": {"mp": 19},
        "За спиною принца": {"mp": 24}, "Уничтожитель хаоса": {"mp": 30}, "Встать с колен": {"mp": 37}, "Звёздный блеск": {"mp": 47},
        "Боевой клич!": {"mp": 60},
        # «Луч Бога Гиперсмерти»: всё MP плюс 50% максимального HP.
        "Луч Бога Гиперсмерти": {"mp_all": True, "hp_percent": 0.5},
        # Чара: 42 — Гнев; 43 — Безумие; 44 — Сумасшествие;
        # 45 — Псих; 46 — Моральное разложение; 47 — Пробуждение прошлого.
        "Гнев": {"mp": 10}, "Безумие": {"mp": 14}, "Сумасшествие": {"mp": 21}, "Псих": {"mp": 25},
        "Моральное разложение": {"mp": 28}, "Пробуждение прошлого": {"mp_all": True},
        # Фриск: 49 — Potentia intellectus; 50 — Quod licet Iovi, non licet bovi;
        # 51 — Foedus icere; 52 — Do ut des; 53 — Сохранение решимости.
        "Potentia intellectus": {"mp": 12}, "Quod licet Iovi, non licet bovi": {"mp": 18}, "Проект договора": {"mp": 34}, "Foedus icere": {"mp": 38}, "Do ut des": {"mp": 44},
        "Вернуть в диалог": {"mp": 50},
        # Иззи: 54 — Осколок себя; 55 — Успокоение; 56 — Медитация;
        # 57 — Правильное дыхание; 58 — Благовония; 59 — Открытие пределов;
        # 60 — Воспрять дух; 61 — Карма; 62 — Предвиденье; 63 — Зачарование;
        # 64 — Усиление присутствия; 65 — Духовный лук; 66 — Пробуждение.
        # Стоимости — из ТЗ дизайнера.
        "Осколок себя": {"mp": 12}, "Успокоение": {"mp": 20}, "Медитация": {"mp": 0}, "Правильное дыхание": {"mp": 24},
        "Благовония": {"mp": 28}, "Открытие пределов": {"mp": 35}, "Воспрять дух": {"mp": 44}, "Карма": {"mp": 50},
        # «Предвиденье» стоит 20% максимального HP, «Духовный лук» — 70% MP,
        # «Пробуждение» — все MP.
        "Предвиденье": {"hp_percent": 0.20}, "Зачарование": {"mp": 0}, "Усиление присутствия": {"mp": 0},
        "Духовный лук": {"mp_percent": 0.70}, "Пробуждение": {"mp_all": True},
        # Кловер: 67 — Выбор калибра; 68 — Сыграем!; 69 — Помиловать;
        # 70 — Вафельный перерыв; 71 — Суд; 72 — Дробовик;
        # 73 — Метка разыскиваемого; 74 — Вызов на дуэль!;
        # 75 — Длинный ствол; 76 — От судьбы не уйдёшь;
        # 77 — Дикий запад, Крошка!; 78 — Гиперлуч.
        "Выбор калибра": {"mp": 0}, "Сыграем!": {"mp": 0}, "Помиловать": {"mp": 0}, "Вафельный перерыв": {"mp": 0},
        "Суд": {"mp": 0}, "Дробовик": {"mp": 0}, "Метка разыскиваемого": {"mp": 0}, "Вызов на дуэль!": {"mp": 0},
        # «Длинный ствол», «От судьбы не уйдёшь» и «Дикий запад» — магия,
        # расходующая ману; «Гиперлуч» тратит 80% максимального HP.
        "Длинный ствол": {"mp": 12}, "От судьбы не уйдёшь": {"mp": 18},
        "Дикий запад, Крошка!": {"mp": 24},
        "Гиперлуч": {"hp_percent": 0.8},
        # Арчи: 79 — Ладони чакры; 80 — Очищение Ци; 81 — Печати ниндзюцу;
        # 82 — Укрепление мышц; 83 — Рывок; 84 — Режим храбрости;
        # 85 — Реверс энергии; 86 — Травмирующие удары;
        # 87 — Вернуть отправителю; 88 — Храбрость!
        "Ладони чакры": {"mp": 10}, "Очищение Ци": {"mp": 12}, "Печати ниндзюцу": {"mp": 14},
        "Укрепление мышц": {"mp": 16}, "Рывок": {"mp": 18}, "Режим храбрости": {"mp": 20},
        "Реверс энергии": {"mp": 24}, "Травмирующие удары": {"mp": 26},
        "Вернуть отправителю": {"mp": 30}, "Храбрость!": {"mp": 36},
        # Седрик: вместо обычной маны использует ингредиенты (MP стоимость 0).
        "Сбегать за продуктами": {"mp": 0}, "Яичница на завтрак": {"mp": 0}, "Яичница с беконом": {"mp": 0},
        "Булочка": {"mp": 0}, "Салат Цезарь": {"mp": 0}, "Сэндвич": {"mp": 0},
        "Блинчики с кленовым сиропом": {"mp": 0}, "Бургер": {"mp": 0}, "Чизбургер": {"mp": 0},
        "Суши": {"mp": 0}, "Мясо на гриле": {"mp": 0}, "Пицца!": {"mp": 0},
        # Фабри: магия фамильяров (121..136). Призывы — это атаки, они
        # бесплатны и здесь не перечислены. Цены растут по уровню магии:
        # ур.1-2 — базовая поддержка, ур.5-7 — сильные эффекты,
        # ур.8-10 — ультимативные.
        "Спрятаться": {"mp": 8}, "Надеть панцирь": {"mp": 12},
        "Прикрепиться": {"mp": 18}, "Рикошет черепахи": {"mp": 24},
        "Орлиная зоркость": {"mp": 8}, "Небесные танцы": {"mp": 12},
        "Снести яичко": {"mp": 20}, "Перьевой ураган": {"mp": 30},
        "Ускориться": {"mp": 8}, "Не поймаешь": {"mp": 14},
        "Поделиться морковкой": {"mp": 16}, "Быстрее и дальше": {"mp": 36},
        "Боевой рёв": {"mp": 10}, "Неудержимость": {"mp": 14},
        "Бей сильнее!": {"mp": 18}, "Я покажу, как бить!": {"mp": 40},
        # Эмили (стоимости из ТЗ; проценты и специальные эффекты обрабатываются её пассивками).
        "Викторина": {"mp": 12}, "Гонка чисел": {"mp": 18}, "Цифровой щит": {"mp": 26},
        "Блеснуть безупречностью": {"mp": 5}, "Взлом сети": {"mp": 28}, "Блокировка": {"mp": 30},
        "Левый аккаунт": {"mp": 24}, "Заморозка репозитория": {"mp": 30}, "Трансляция взлома": {"mp": 28},
        "Маленькая ошибка": {"mp": 35}, "Доксиинг": {"mp": 42}, "Взлом аккаунта": {"mp": 60},
        "Блэк аут": {"mp": 70}, "Резервная копия": {"mp": 58}, "Игра оптики": {"mp": 76},
        "Пурпурная инфузия": {"mp_percent": 0.50}, "Зазывала": {"mp": 8}, "Rude Buster": {"mp": 16},
        "Зверский рык": {"mp": 18}, "Секираранг": {"mp": 26}, "Rude fissure": {"mp": 38},
        "Умиротворение": {"mp": 8}, "Лозы": {"mp": 12}, "Молитва исцеления": {"mp": 14},
        "Агрессивный пузырь": {"mp": 16}, "Пушистый страж": {"mp": 18}, "Лечение?...": {"mp": 20},
        "Рассеять!": {"mp": 22}, "Пламенная казнь": {"mp": 28}, "Перегной": {"mp": 30},
        "Убеждающий вид": {"mp": 18}, "Приумножить заслуги": {"mp": 24}, "Унизить слабого": {"mp": 26},
        "Песнь воскрешения": {"mp": 45}, "Спустить с небес": {"mp": 32}, "Концентрация зла": {"mp": 50},
        "Тёмный горящий сад": {"mp": 80},
        "Молитва исцеления Ноэлль": {"mp": 14}, "Ледяной шок": {"mp": 16}, "Сонный туман": {"mp": 22},
        "Морозная завеса": {"mp": 20}, "Ледяная буря": {"mp": 35}, "Оледенение чувств": {"mp": 45},
        "Морозная корка": {"mp": 25}, "Ледяной кокон": {"mp": 35}, "Аура холодного сердца": {"mp": 25},
        "Терновый сад": {"mp_percent": 0.65}, "Цветение бед": {"mp": 35},
        # «Снежная могила» списывает всю текущую MP здесь, а 30% текущего HP
        # применяет в собственном лейбле после подтверждения цели.
        "Снежная могила": {"mp_all": True},
        "Стена костей": {"mp": 10}, "Костяной дождь": {"mp": 18}, "Прижмись": {"mp": 12},
        "Поспать": {"mp": 2}, "Камнем вниз": {"mp": 16}, "Костяной щит": {"mp": 14},
        "Бластер": {"mp": 30}, "Пинг-понг": {"mp": 28}, "Костяная клетка": {"mp": 32},
        "Угрызения совести": {"mp": 25}, "Кара за грехи": {"mp": 40}, "Телекинез!": {"mp": 45},
        "Финальная атака": {"mp_all": True},
        "Гениальный план": {"mp": 10}, "Электрический клюв": {"mp": 14}, "Вихрь знаний": {"mp": 28},
    }

    # Нужны для определения самой дешёвой магии конкретного героя.
    CHARACTER_MAGIC_ABILITIES = {
        "Крис": ("Призвать меч", "Призвать щит", "Напрячься", "Позвать за щит", "Правильный угол", "Слабое место", "Концентрация", "Поднять щиты!", "Стремление вперёд", "Рывок защитника (магия)", "Пробудиться"),
        "Азриель": ("Шаг вперёд", "Магия огня", "Горное равновесие", "Клинки хаоса", "За спиною принца", "Уничтожитель хаоса", "Встать с колен", "Звёздный блеск", "Боевой клич!", "Луч Бога Гиперсмерти"),
        "Чара": ("Гнев", "Безумие", "Сумасшествие", "Псих", "Моральное разложение", "Пробуждение прошлого"),
        "Фриск": ("Potentia intellectus", "Quod licet Iovi, non licet bovi", "Проект договора", "Foedus icere", "Do ut des", "Вернуть в диалог"),
        "Иззи": ("Осколок себя", "Успокоение", "Медитация", "Правильное дыхание", "Благовония", "Открытие пределов", "Воспрять дух", "Карма", "Предвиденье", "Зачарование", "Усиление присутствия", "Духовный лук", "Пробуждение"),
        "Кловер": ("Выбор калибра", "Сыграем!", "Помиловать", "Вафельный перерыв", "Суд", "Дробовик", "Метка разыскиваемого", "Вызов на дуэль!", "Длинный ствол", "От судьбы не уйдёшь", "Дикий запад, Крошка!", "Гиперлуч"),
        "Арчи": ("Ладони чакры", "Очищение Ци", "Печати ниндзюцу", "Укрепление мышц", "Рывок", "Режим храбрости", "Реверс энергии", "Травмирующие удары", "Вернуть отправителю", "Храбрость!"),
        "Седрик": ("Сбегать за продуктами", "Яичница на завтрак", "Булочка", "Салат Цезарь", "Сэндвич", "Блинчики с кленовым сиропом", "Чизбургер", "Суши", "Мясо на гриле", "Пицца!"),
        # Фабри: 16 магий фамильяров (по 4 на каждого из 4 фамильяров).
        "Фабри": ("Спрятаться", "Надеть панцирь", "Прикрепиться", "Рикошет черепахи",
                  "Орлиная зоркость", "Небесные танцы", "Снести яичко", "Перьевой ураган",
                  "Ускориться", "Не поймаешь", "Поделиться морковкой", "Быстрее и дальше",
                  "Боевой рёв", "Неудержимость", "Бей сильнее!", "Я покажу, как бить!"),
        "Эмили": ("Викторина", "Гонка чисел", "Цифровой щит", "Блеснуть безупречностью",
                  "Взлом сети", "Блокировка", "Левый аккаунт", "Заморозка репозитория",
                  "Трансляция взлома", "Маленькая ошибка", "Доксиинг", "Взлом аккаунта",
                  "Блэк аут", "Резервная копия", "Игра оптики"),
        "Сьюзи": ("Пурпурная инфузия", "Зазывала", "Rude Buster", "Зверский рык", "Секираранг", "Rude fissure"),
        "Ральзей": ("Умиротворение", "Лозы", "Молитва исцеления", "Агрессивный пузырь", "Пушистый страж", "Лечение?...", "Рассеять!", "Пламенная казнь", "Перегной", "Убеждающий вид", "Приумножить заслуги", "Унизить слабого", "Песнь воскрешения", "Спустить с небес", "Концентрация зла", "Тёмный горящий сад"),
        "Ноэлль": ("Молитва исцеления Ноэлль", "Ледяной шок", "Сонный туман", "Морозная завеса", "Ледяная буря", "Оледенение чувств", "Морозная корка", "Ледяной кокон", "Аура холодного сердца", "Терновый сад", "Цветение бед", "Снежная могила"),
        "Санс": ("Стена костей", "Костяной дождь", "Прижмись", "Поспать", "Камнем вниз", "Костяной щит", "Бластер", "Пинг-понг", "Костяная клетка", "Угрызения совести", "Кара за грехи", "Телекинез!", "Финальная атака"),
        "Бердли": ("Гениальный план", "Электрический клюв", "Вихрь знаний"),
    }

    def get_current_battle_character():
        attacker = getattr(store, "current_attacker", None)
        # Арчи (8) — не игровой герой, поэтому его здесь нет.
        for attacker_id, char_name in (
            (1, "Крис"), (2, "Азриель"), (3, "Чара"), (4, "Фриск"),
            (5, "Иззи"), (6, "Кловер"), (7, "Седрик"),
            (9, "Сильвия"), (10, "Фабри"), (11, "Эмили"), (12, "Сьюзи"),
            (13, "Ральзей"), (14, "Ноэлль"), (15, "Санс"), (16, "Бердли"),
        ):
            if attacker == attacker_id:
                return store.pers_dict.get(char_name)
        return None

    def get_ability_resource_cost(ability_id, char=None):
        raw_cost = ABILITY_RESOURCE_COSTS.get(ability_id, {})
        if char is None:
            char = get_current_battle_character()

        mp_cost = float(raw_cost.get("mp", 0))
        hp_cost = int(math.ceil(float(raw_cost.get("hp", 0))))
        mp_percent = float(raw_cost.get("mp_percent", 0.0))

        if char is not None and mp_percent > 0.0:
            max_mp = max(0, getattr(char, "max_mp", 0))
            mp_cost += max_mp * mp_percent

        # «Луч Бога Гиперсмерти»: тратит всю текущую ману.
        if char is not None and raw_cost.get("mp_all"):
            mp_cost += max(0.0, float(getattr(char, "current_mp", 0)))

        if char is not None and getattr(char, "name", None) == "Ноэлль":
            mp_cost *= float(getattr(char, "noelle_next_magic_cost_multiplier", 1.0))

        # Часть максимального HP в стоимости («Луч Бога Гиперсмерти» — 50%).
        hp_percent = float(raw_cost.get("hp_percent", 0.0))
        if char is not None and hp_percent > 0.0:
            hp_cost += int(math.ceil(max(0, getattr(char, "max_hp", 0)) * hp_percent))

        if char is not None and mp_cost > 0:
            base_multiplier = float(getattr(char, "mp_cost_multiplier", 1.0))
            artifact_modifier = float(getattr(char, "mpcostartifactmod", 0.0))
            effective_multiplier = max(0.0, base_multiplier + artifact_modifier)
            mp_cost *= effective_multiplier

        # «Способности возвращаются» ур.2: призыв меча и щита стоит вдвое
        # меньше — множитель зависит от Pers.global_level.
        mp_cost *= kris_ability_cost_multiplier(ability_id)

        mp_cost = int(math.ceil(mp_cost))

        return {
            "mp": max(0, mp_cost),
            "hp": max(0, hp_cost),
        }

    def get_minimum_magic_mp_cost(char):
        """Возвращает актуальную минимальную стоимость магии героя."""
        ability_ids = CHARACTER_MAGIC_ABILITIES.get(getattr(char, "name", None), ())
        costs = [
            get_ability_resource_cost(ability_id, char).get("mp", 0)
            for ability_id in ability_ids
        ]
        positive_costs = [cost for cost in costs if cost > 0]
        return min(positive_costs) if positive_costs else 0

    def get_display_mp_fill(char, mp_value=None):
        """Считает заполнение MP только по проценту от максимума."""
        if char is None:
            return 0
        if mp_value is None:
            mp_value = getattr(char, "current_mp", 0)
        max_mp = getattr(char, "max_mp", 0)
        if mp_value <= 0 or max_mp <= 0:
            return 0
        return max(0, min(10, int(math.ceil((float(mp_value) / max_mp) * 10))))

    def can_pay_ability_cost(ability_id=None, char=None):
        if ability_id is None:
            ability_id = getattr(store, "attackindex", None)
        if char is None:
            char = get_current_battle_character()
        if char is None:
            return True
        if getattr(char, "name", None) == "Седрик" and ability_id != "Сбегать за продуктами":
            if hasattr(store, "can_cook_dish_single"):
                if not store.can_cook_dish_single(ability_id, char):
                    return False
        cost = get_ability_resource_cost(ability_id, char)
        return (
            getattr(char, "current_mp", 0) >= cost.get("mp", 0) and
            getattr(char, "current_hp", 0) > cost.get("hp", 0)
        )

    def set_ability_resource_preview(ability_id):
        char = get_current_battle_character()
        cost = get_ability_resource_cost(ability_id, char)
        store.resource_preview_ability = ability_id if cost.get("mp", 0) or cost.get("hp", 0) else None
        store.resource_preview_mp_cost = cost.get("mp", 0)
        store.resource_preview_hp_cost = cost.get("hp", 0)
        store.resource_preview_can_pay = can_pay_ability_cost(ability_id, char)
        renpy.restart_interaction()

    def clear_ability_resource_preview():
        store.resource_preview_ability = None
        store.resource_preview_mp_cost = 0
        store.resource_preview_hp_cost = 0
        # None — третье состояние: курсор больше не наведён на способность.
        # Оно принудительно возвращает HP/MP-бары к исходным трансформам.
        store.resource_preview_can_pay = None
        renpy.restart_interaction()

    def get_resource_preview_for_char(char):
        active_char = get_current_battle_character()
        # Стоимость и результат сравнения записываются непосредственно
        # hover-действием кнопки через set_ability_resource_preview.
        # MP-интерфейс только отображает уже рассчитанное состояние.
        if active_char is not char or store.resource_preview_ability is None:
            return 0, 0, None
        return (
            store.resource_preview_mp_cost,
            store.resource_preview_hp_cost,
            store.resource_preview_can_pay,
        )

    def pay_ability_cost(ability_id=None):
        if ability_id is None:
            ability_id = getattr(store, "attackindex", None)
        char = get_current_battle_character()
        if char is None or not can_pay_ability_cost(ability_id, char):
            return False
        cost = get_ability_resource_cost(ability_id, char)
        char.current_mp -= cost.get("mp", 0)
        char.current_hp -= cost.get("hp", 0)
        if getattr(char, "name", None) == "Ноэлль":
            char.noelle_next_magic_cost_multiplier = 1.0
        clear_ability_resource_preview()
        return True

    def get_character_picked_for_shift():
        """Возвращает количество персонажей в команде (кэшируется)"""
        if store.team_manager is not None:
            return store.team_manager.get_team_member_count()
        else:
            if hasattr(store, 'ensure_team_manager'):
                store.ensure_team_manager()
                if store.team_manager is not None:
                    return store.team_manager.get_team_member_count()
            return 1

    class CharacterPickedStore:
        def __get__(self, obj, objtype=None):
            return get_character_picked_for_shift()
        def __set__(self, obj, value):
            pass

    store.character_picked_for_shift = CharacterPickedStore()

    def get_hp_mp_bar_prev_values(char_key, current_hp, current_mp):
        cached = store.hp_mp_bar_cache.get(char_key)
        if cached is None:
            return current_hp, current_mp
        return cached

    def commit_hp_mp_bar_values(char_key, current_hp, current_mp):
        store.hp_mp_bar_cache[char_key] = (current_hp, current_mp)

    def commit_hp_mp_bar_values_for_all():
        if hasattr(store, "pers_dict") and store.pers_dict:
            for char in store.pers_dict.values():
                if hasattr(char, "name"):
                    commit_hp_mp_bar_values(char.name, char.current_hp, char.current_mp)
        if hasattr(store, "enemies") and store.enemies:
            for enemy_name, enemy in store.enemies.items():
                key = getattr(enemy, "name", enemy_name)
                commit_hp_mp_bar_values(key, enemy.current_hp, getattr(enemy, "current_mp", 0))

    def get_hp_mp_gain_flags(char):
        prev_hp, prev_mp = get_hp_mp_bar_prev_values(char.name, char.current_hp, char.current_mp)
        hp_gain = char.current_hp > prev_hp
        mp_gain = char.current_mp > prev_mp
        return hp_gain, mp_gain

    # === ОПТИМИЗИРОВАННЫЕ ФУНКЦИИ ДЛЯ character_status_card ===
    def get_char_status_offset():
        """Кэширует смещение для карточки персонажа"""
        count = get_character_picked_for_shift()
        offsets = {1: -320, 2: -640, 3: -960, 4: -1280}
        return offsets.get(count, -320)

    def get_char_order(char_name):
        """Возвращает порядок персонажа в команде (кэшируется)"""
        if not store.team_manager:
            return 1
        active_team_order = [slot for slot in store.team_manager.team_slots if slot]
        return active_team_order.index(char_name) + 1 if char_name in active_team_order else 1

    def get_char_hp_fill(char, prev_hp_value):
        """Вычисляет заполнение HP бара (1 иконка)"""
        if char.current_hp <= 0:
            return 0, 0
        if char.current_hp > char.max_hp:
            hp_overheal_percent = (char.current_hp - char.max_hp) / char.max_hp * 100
            overheal_icons = min(5, int(math.ceil(hp_overheal_percent / 10.0)))
            if prev_hp_value > char.max_hp:
                prev_hp_overheal_percent = (prev_hp_value - char.max_hp) / char.max_hp * 100
                prev_overheal_icons = min(5, int(math.ceil(prev_hp_overheal_percent / 10.0)))
            else:
                prev_overheal_icons = 0
            return overheal_icons, prev_overheal_icons
        hp_fill = int(math.ceil((char.current_hp / char.max_hp) * 10))
        hp_fill = max(0, min(10, hp_fill))
        prev_hp_fill = int(math.ceil((prev_hp_value / char.max_hp) * 10)) if char.max_hp else 0
        prev_hp_fill = max(0, min(10, prev_hp_fill))
        return hp_fill, prev_hp_fill

    def _mp_cell_count(amount, cells_per_full_bar):
        """Округляет количество ячеек без ошибки float на границе процента."""
        if amount <= 0:
            return 0
        return int(math.ceil(float(amount) * cells_per_full_bar - 1e-8))

    def _get_mp_layer_fills(char, mp_value):
        """Возвращает заполнение обычного и сверхманного слоёв для MP."""
        max_mp = max(0, getattr(char, "max_mp", 0))
        if max_mp <= 0 or mp_value <= 0:
            return 0, 0

        if mp_value > max_mp:
            normal_fill = 10.0
            over_fill = min(5, _mp_cell_count(mp_value - max_mp, 10.0 / max_mp))
        else:
            # Для предпросмотра используем только фактический процент MP,
            # не учитывая минимальную стоимость доступных заклинаний.
            normal_fill = min(10, _mp_cell_count(mp_value, 10.0 / max_mp))
            over_fill = 0

        return normal_fill, over_fill

    def get_char_mp_fill(char, prev_mp_value):
        """Вычисляет заполнение MP бара (1 иконка)"""
        if char.current_mp <= 0:
            return 0, 0
        if char.current_mp > char.max_mp:
            mp_overmana_percent = (char.current_mp - char.max_mp) / char.max_mp * 100
            # Сверхмана — отдельный слой: одна ячейка на каждые 5% сверх
            # max_mp, поверх десяти обычных ячеек.
            overmana_icons = min(5, _mp_cell_count(mp_overmana_percent, 1.0 / 10.0))
            if prev_mp_value > char.max_mp:
                prev_mp_overmana_percent = (prev_mp_value - char.max_mp) / char.max_mp * 100
                prev_overmana_icons = min(5, _mp_cell_count(prev_mp_overmana_percent, 1.0 / 10.0))
            else:
                prev_overmana_icons = 0
            return overmana_icons, prev_overmana_icons
        mp_fill = get_display_mp_fill(char)
        prev_mp_fill = int(math.ceil((prev_mp_value / char.max_mp) * 10)) if char.max_mp else 0
        prev_mp_fill = max(0, min(10, prev_mp_fill))
        return mp_fill, prev_mp_fill

    def get_char_hp_text_style(char):
        """Возвращает стиль текста HP: color, style_name"""
        if char.current_hp <= char.max_hp * 0.2:
            return "#ff0000", "damagetext2"
        elif char.current_hp > char.max_hp:
            return "#ffffff", "damagetext2"
        else:
            return "#ffffff", "damagetext2"

    def get_char_mp_text_style(char):
        """Возвращает стиль текста MP: color, style_name"""
        if char.current_mp <= char.max_mp * 0.2:
            return "#ffffffc2", "damagetext2"
        elif char.current_mp > char.max_mp:
            return "#3adeff", "damagetext2"
        else:
            return "#ffffff", "damagetext2"

    def get_char_hp_bar_transforms(char, hp_fill, prev_hp_fill, is_overheal):
        """Возвращает активные HP-ячейки с уже выбранными hover-трансформами."""
        result = []
        if is_overheal:
            for i in range(10):
                if i < hp_fill:
                    if i >= prev_hp_fill:
                        result.append(("hpactive_overheal.png", hp_mp_bar_app, damage_gradient_overheal))
                    else:
                        result.append(("hpactive_overheal.png", None, damage_gradient_overheal))
                elif i < prev_hp_fill:
                    result.append(("hpactive_overheal.png", hp_mp_bar_dis, damage_gradient_overheal))
        elif char.current_hp > 0 and char.current_hp <= char.max_hp * 0.2:
            for i in range(10):
                if i < hp_fill:
                    if i >= prev_hp_fill:
                        result.append(("hpactive.png", hp_mp_bar_app, damage_gradient_gray))
                    else:
                        result.append(("hpactive.png", None, damage_gradient_gray))
                elif i < prev_hp_fill:
                    result.append(("hpactive.png", hp_mp_bar_dis, damage_gradient_gray))
        else:
            for i in range(10):
                if i < hp_fill:
                    if i >= prev_hp_fill:
                        result.append(("hpactive.png", hp_mp_bar_app, damage_gradient_gray))
                    else:
                        result.append(("hpactive.png", None, damage_gradient_gray))
                elif i < prev_hp_fill:
                    result.append(("hpactive.png", hp_mp_bar_dis, damage_gradient_gray))

        preview_mp_cost, preview_hp_cost, preview_can_pay = get_resource_preview_for_char(char)
        preview_hp_slots = 0
        if preview_hp_cost and char.max_hp:
            preview_hp_slots = int(math.ceil((preview_hp_cost * 10.0) / char.max_hp))
            preview_hp_slots = max(0, min(10, preview_hp_slots))

        preview_hp_start = max(0, hp_fill - preview_hp_slots)
        decorated_result = []

        for i, (img, transition_transform, gradient_transform) in enumerate(result):
            preview_this_slot = (
                preview_hp_slots and
                (i >= preview_hp_start if preview_can_pay else i < preview_hp_slots)
            )
            preview_transform = None

            if preview_can_pay is None:
                preview_transform = resource_preview_none
            elif preview_this_slot:
                preview_transform = hp_enough if preview_can_pay else hp_not_enought

                # Красный hover содержит собственный градиентный shader.
                if not preview_can_pay:
                    gradient_transform = None

            transforms = [
                transform
                for transform in (
                    transition_transform,
                    gradient_transform,
                    preview_transform,
                )
                if transform is not None
            ]
            decorated_result.append((img, transforms))

        return decorated_result

    def get_char_hp_bar_transforms(char, hp_fill, prev_hp_fill, is_overheal, prev_hp_value=None):
        """Возвращает обычный и сверхнормальный HP-слои отдельно."""
        max_hp = max(0.0, float(getattr(char, "max_hp", 0)))
        if prev_hp_value is None:
            prev_hp_value = char.current_hp

        def layer_fills(value):
            if max_hp <= 0 or value <= 0:
                return 0.0, 0.0
            if value > max_hp:
                return 10, min(5, _mp_cell_count(value - max_hp, 10.0 / max_hp))
            return min(10, _mp_cell_count(value, 10.0 / max_hp)), 0

        normal_fill, over_fill = layer_fills(char.current_hp)
        normal_prev, over_prev = layer_fills(prev_hp_value)

        def filled_slots(fill, previous, image, gradient):
            result = []
            for i in range(int(math.ceil(max(fill, previous) - 1e-8))):
                if i < fill:
                    result.append((i, image, None,
                                   gradient, 12.0))
                elif i < previous:
                    result.append((i, image, hp_mp_bar_dis, None, 12.0))
            return result

        normal_result = filled_slots(normal_fill, normal_prev, "hpactive.png", damage_gradient_gray)
        over_result = filled_slots(
            over_fill,
            over_prev,
            Solid("#40d94a", xysize=(12, 22)),
            damage_gradient_green_bright,
        )

        _, preview_hp_cost, preview_can_pay = get_resource_preview_for_char(char)
        if preview_hp_cost:
            after_hp = max(0.0, char.current_hp - preview_hp_cost)
            after_normal, after_over = layer_fills(after_hp)
            normal_start, normal_end = after_normal, normal_fill
            over_start, over_end = after_over, over_fill
            if preview_can_pay:
                normal_result = filled_slots(after_normal, after_normal, "hpactive.png", damage_gradient_gray)
                over_result = filled_slots(
                    after_over,
                    after_over,
                    Solid("#40d94a", xysize=(12, 22)),
                    damage_gradient_green_bright,
                )
        else:
            normal_start = normal_end = over_start = over_end = 0.0

        def decorate(source, start, end, over=False, protected_prefix=0):
            decorated = []
            for i, img, transition, gradient, width in source:
                preview = (
                    preview_can_pay is not None and
                    i >= protected_prefix and
                    end > i and start < i + 1
                )
                transforms = [t for t in (transition, gradient) if t is not None]
                decorated.append((img, transforms, width))
            return decorated

        return (
            decorate(normal_result, normal_start, normal_end, False, over_fill),
            decorate(over_result, over_start, over_end, True),
        )

    def get_char_mp_bar_transforms(char, mp_fill, prev_mp_fill, is_overmana, is_dead, prev_mp_value=None):
        """Возвращает трансформы обычной и сверхманы отдельно.

        Раньше при сверхмане здесь строился только один список из over-mana
        ячеек. Из-за этого стоимость, пересекающая границу max_mp, не могла
        подсветить часть обычной маны.
        """
        normal_fill, over_fill = _get_mp_layer_fills(char, char.current_mp)
        if prev_mp_value is None:
            prev_mp_value = char.current_mp
        normal_prev_fill, over_prev_fill = _get_mp_layer_fills(char, prev_mp_value)

        def filled_slots(fill, previous_fill, image, gradient):
            result = []
            slot_count = int(math.ceil(max(fill, previous_fill) - 1e-8))
            for i in range(slot_count):
                if i < fill:
                    result.append((i, image, None, gradient, 12.0))
                elif i < previous_fill:
                    result.append((i, image, hp_mp_bar_dis, None, 12.0))
            return result

        gradient = damage_gradient if char.current_mp <= char.max_mp * 0.2 else damage_gradient_gray
        normal_result = filled_slots(
            normal_fill,
            normal_prev_fill,
            "mpactive.png",
            desaturate_dead3 if is_dead else gradient,
        )
        over_result = filled_slots(
            over_fill,
            over_prev_fill,
            Solid("#32eeff", xysize=(12, 22)),
            damage_gradient_semigray,
        )

        preview_mp_cost, preview_hp_cost, preview_can_pay = get_resource_preview_for_char(char)
        preview_normal_slots = 0
        preview_over_slots = 0
        if preview_mp_cost and char.max_mp:
            if preview_can_pay:
                # Предпросмотр повторяет фактическое списание MP. Считаем
                # разницу ячеек до и после, а не округляем стоимость отдельно.
                before_normal, before_over = _get_mp_layer_fills(char, char.current_mp)
                after_mp = max(0, char.current_mp - preview_mp_cost)
                after_normal, after_over = _get_mp_layer_fills(char, after_mp)
                preview_normal_start, preview_normal_end = after_normal, before_normal
                preview_over_start, preview_over_end = after_over, before_over
                normal_result = filled_slots(
                    after_normal,
                    after_normal,
                    "mpactive.png",
                    desaturate_dead3 if is_dead else gradient,
                )
                over_result = filled_slots(
                    after_over,
                    after_over,
                    Solid("#32eeff", xysize=(12, 22)),
                    damage_gradient_semigray,
                )
            else:
                # Для недоступной способности сохраняем прежний красный
                # предпросмотр доступного участка ресурса.
                available_over = max(0, char.current_mp - char.max_mp)
                over_cost = min(preview_mp_cost, available_over)
                normal_cost = max(0, preview_mp_cost - over_cost)
                normal_cost_cells = min(normal_fill, _mp_cell_count(normal_cost, 10.0 / char.max_mp))
                over_cost_cells = min(over_fill, _mp_cell_count(over_cost, 10.0 / char.max_mp))
                preview_normal_start = max(0, normal_fill - normal_cost_cells)
                preview_normal_end = normal_fill
                preview_over_start = max(0, over_fill - over_cost_cells)
                preview_over_end = over_fill
        else:
            preview_normal_start = preview_normal_end = 0.0
            preview_over_start = preview_over_end = 0.0

        def decorate(source, preview_start, preview_end, over=False, protected_prefix=0):
            decorated = []
            for slot_index, (i, img, transition_transform, gradient_transform, width) in enumerate(source):
                # i — настоящий индекс ячейки, а не позиция в укороченном
                # списке только заполненных ячеек.
                preview_this_slot = (
                    i >= protected_prefix and
                    preview_end > i and preview_start < i + 1
                )
                transforms = [transform for transform in (
                    transition_transform, gradient_transform
                ) if transform is not None]
                decorated.append((img, transforms, width))
            return decorated

        return (
            decorate(normal_result, preview_normal_start, preview_normal_end, False, over_fill),
            decorate(over_result, preview_over_start, preview_over_end, True),
        )

    def get_status_active_pixel_counts(char, resource):
        """Возвращает количество активных 1px-сегментов для двух слоёв."""
        if resource == "hp":
            value = float(getattr(char, "current_hp", 0))
            maximum = float(getattr(char, "max_hp", 0))
            _, cost, can_pay = get_resource_preview_for_char(char)
        else:
            value = float(getattr(char, "current_mp", 0))
            maximum = float(getattr(char, "max_mp", 0))
            cost, _, can_pay = get_resource_preview_for_char(char)

        if cost and can_pay:
            value = max(0.0, value - cost)
        if maximum <= 0:
            return 0, 0

        normal_pixels = min(100, _mp_cell_count(min(value, maximum), 100.0 / maximum))
        over_pixels = min(100, _mp_cell_count(max(0.0, value - maximum), 200.0 / maximum))
        return normal_pixels, over_pixels

transform hp_mp_bar_app:
    alpha 0.0
    easein 1.0 alpha 1.0

transform hp_mp_bar_dis:
    alpha 1.0
    easein 1.0 alpha 0.0

default resource_preview_ability = None
default resource_preview_mp_cost = 0
default resource_preview_hp_cost = 0
default resource_preview_can_pay = None

# Третье состояние предпросмотра. Оно применяется после unhovered и
# принудительно убирает промежуточный кадр мигающего matrixcolor.
transform resource_preview_none:
    alpha 1.0
    matrixcolor TintMatrix("#ffffff")

# Подсветка MP при наведении на магию.
transform mp_enough:
    matrixcolor TintMatrix("#ffffff")
    ease 0.65 matrixcolor TintMatrix("#151515")
    ease 0.65 matrixcolor TintMatrix("#ffffff")
    repeat

transform mp_not_enought:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)
    u_gradient_color_bottom (0.65, 0.15, 0.15, 1.0)

    # Одинаковая структура матриц в обеих фазах нужна Ren'Py
    # для плавной интерполяции matrixcolor через ease.
    matrixcolor (TintMatrix("#ffffff") * SaturationMatrix(1.0))
    ease 0.75 matrixcolor (TintMatrix("#ff3030") * SaturationMatrix(0.0))
    ease 0.75 matrixcolor (TintMatrix("#ffffff") * SaturationMatrix(1.0))
    repeat

# Подсветка HP при наведении на умение со стоимостью в здоровье.
transform hp_enough:
    matrixcolor TintMatrix("#ffffff")
    ease 0.65 matrixcolor TintMatrix("#151515")
    ease 0.65 matrixcolor TintMatrix("#ffffff")
    repeat

transform hp_not_enought:
    shader "vertical_gradient_outline"
    u_gradient_color_top (1.0, 1.0, 1.0, 1.0)
    u_gradient_color_bottom (0.65, 0.05, 0.05, 1.0)

    matrixcolor (TintMatrix("#ffffff") * SaturationMatrix(1.0))
    ease 0.75 matrixcolor (TintMatrix("#ff2020") * SaturationMatrix(0.0))
    ease 0.75 matrixcolor (TintMatrix("#ffffff") * SaturationMatrix(1.0))
    repeat

# Отдельные, но идентичные мигания для слоёв сверх нормы.
transform mp_enough_2:
    alpha 1.0
    ease 0.75 alpha 0.0

transform mp_not_enought_2:
    alpha 1.0
    ease 0.75 alpha 0.0

transform hp_enough_2:
    alpha 1.0
    ease 0.75 alpha 0.0

transform hp_not_enought_2:
    alpha 1.0
    ease 0.75 alpha 0.0

# Универсальный экран для отображения статуса одного персонажа
# ОПТИМИЗИРОВАНО: вычисление вынесено в Python функции


# переменные для отображения кнопок для выбора цели переменной target
default show_enemy_status = 1
default show_team_status = 1
# переменные для отображения спрайтов врагов и персонажей
default show_enemy_sprites = 1
default show_team_sprites = 1

transform savedspace_colour_red:
    matrixcolor TintMatrix("#ff0000")
    easeout savedspace*0.5 matrixcolor TintMatrix("#ffffff")

transform savedspace_colour_yellow:
    matrixcolor TintMatrix("#fff700")
    easeout savedspace*0.5 matrixcolor TintMatrix("#ffffff")

transform savedspace_colour_green:
    matrixcolor TintMatrix("#77ff00")
    easeout 1 matrixcolor TintMatrix("#ffffff")

transform savedspace_colour_cyan:
    matrixcolor TintMatrix("#00ffff")
    easeout 1 matrixcolor TintMatrix("#ffffff")

transform savedspace_colour_blue:
    matrixcolor TintMatrix("#639cff")
    easeout 1 matrixcolor TintMatrix("#ffffff")

transform savedspace_colour_red_pulse:
    #matrixcolor TintMatrix("#ff0000")
    block:
        easein 0.9 matrixcolor TintMatrix("#ffffff")
        pause 0.5
        easeout 0.9 matrixcolor TintMatrix("#ff7878")
        repeat

transform desaturate_dead:
    easein 0.5 matrixcolor SaturationMatrix(0.0) matrixcolor TintMatrix("#400c0c")

transform desaturate_dead2:
    easein 0.5 matrixcolor SaturationMatrix(0.0) matrixcolor TintMatrix("#292929")

transform desaturate_dead3:
    easein 0.5 matrixcolor SaturationMatrix(0.0) matrixcolor TintMatrix("#000000")

# НОВЫЙ экран для отображения кнопок выбора противника и союзника
screen character_status_card(char):
    timer 1.05 repeat False action Function(commit_hp_mp_bar_values, char.name, char.current_hp, char.current_mp)

    $ prev_hp_value, prev_mp_value = get_hp_mp_bar_prev_values(char.name, char.current_hp, char.current_mp)
    $ char_order = get_char_order(char.name)
    $ status_offset = get_char_status_offset()

    $ hp_fill, prev_hp_fill = get_char_hp_fill(char, prev_hp_value)
    $ mp_fill, prev_mp_fill = get_char_mp_fill(char, prev_mp_value)
    $ hp_color, hp_style = get_char_hp_text_style(char)
    $ mp_color, mp_style = get_char_mp_text_style(char)
    $ is_dead     = char.current_hp <= 0
    $ is_overheal = char.current_hp > char.max_hp
    $ is_overmana = char.current_mp > char.max_mp
    $ hp_normal_bar_transforms, hp_over_bar_transforms = get_char_hp_bar_transforms(char, hp_fill, prev_hp_fill, is_overheal, prev_hp_value)
    $ mp_normal_bar_transforms, mp_over_bar_transforms = get_char_mp_bar_transforms(char, mp_fill, prev_mp_fill, is_overmana, is_dead, prev_mp_value)

    # Портерт НЕ рисуем — он уже нарисован в team_status_display через herobox.png
    # Карточка начинается сразу от правого края портрета.
    # Ширина подобрана так, чтобы всё укладывалось в spacing=157 в team_status_display.
    fixed:
        xysize (157, 130)
        xoffset status_offset - 50
        yoffset -50

        # ============================================================
        # ИМЯ (высота фикс. 30px, ширина ограничена 145)
        # ============================================================
        fixed:
            xpos -5
            ypos 31 
            xysize (145, 30)
            text char.name:
                font "determination.otf"
                size 30
                color "#ffffff"
                xalign 0.0
                yalign 0.5
                outlines [(3, "#000000", 0, 0)]
                if is_dead:
                    at desaturate_dead
                else:
                    at damage_gradient_gray

        # ============================================================
        # ПАЙ-ЧАРТ ЕДЫ (правый верхний угол)
        # ============================================================
        fixed:
            xalign 1.0
            #xpos 125
            xoffset 72
            ypos 31
            xysize (32, 32)
            if is_dead:
                add FeednessPieChart(char, size=25) at desaturate_dead3
            else:
                add FeednessPieChart(char, size=25)

        # ============================================================
        # ЩИТ (только когда есть, иначе пропускаем)
        # ============================================================
        if char.shield > 0:
            fixed:
                xoffset 25
                xpos 25
                ypos 46
                xysize (70, 12)
                #background "#000000"

                # Фон щита — 4 позиции лесенкой
                fixed:
                    hbox:
                        xalign 0.0 yalign 1.0
                        spacing 2
                        for i in range(1, 5):
                            add Solid("#27250d", xysize=(37, int(10 * i * 0.10))) yalign 1.0 xalign 1.0 at damage_gradient_black

                # Заполнение щита — текущее значение
                fixed:
                    hbox:
                        yoffset 3
                        xalign 0.0 yalign 1.0
                        spacing 2
                        if char.shield >= 4:
                            for i in range(1, 5):
                                add Solid("#ffea00", xysize=(37, int(10 * i * 0.10))) yalign 1.0 xalign 1.0 at damage_gradient_semigray
                        else:
                            for i in range(1, min(char.shield + 1, 5)):
                                add Solid("#e1d22e", xysize=(37, int(10 * i * 0.10))) yalign 1.0 xalign 1.0 at damage_gradient_gray

        # ============================================================
        # HP
        # ============================================================
        fixed:

            xpos 0
            ypos 50
            yoffset 5
            xysize (157, 30)
            if is_dead:
                at desaturate_dead2

            $ hp_transform = damage_gradient_for_lowhp if hp_color == "#ff0000" else damage_gradient_green_bright if char.current_hp > char.max_hp else damage_gradient_gray
            $ hp_text_size = 30 if char.current_hp < 1000 else (24 if char.current_hp < 10000 else 20)

            # Текст HP — своя зона 50px, прижат вправо
            fixed:
                xpos 0
                ypos 4
                xysize (50, 30)
                text "{font=determination.otf}{size=[hp_text_size]}[int(char.current_hp)]{/font}{/size}":
                    color hp_color
                    style hp_style
                    xalign 0.0
                    yalign 0.5
                    at hp_transform

            # Полоска HP — жёстко на позиции xpos 52
            fixed:
                xpos 52
                ypos 9
                xysize (102, 12)
                hbox:
                    spacing 4
                    for i in range(10):
                        add "hppassive.png" at damage_gradient_black
                hbox:
                    spacing 4
                    for img, transforms, width in hp_normal_bar_transforms:
                        if img is not None:
                            fixed:
                                xysize (12, 22)
                                if transforms:
                                    add img xzoom (width / 12.0) yzoom 1.0 at transforms
                                else:
                                    add img xzoom (width / 12.0) yzoom 1.0
                if is_overheal:
                    hbox:
                        spacing 4
                        for img, transforms, width in hp_over_bar_transforms:
                            if img is not None:
                                fixed:
                                    xysize (12, 22)
                                    if transforms:
                                        add img xzoom (width / 12.0) yzoom 1.0 at transforms
                                    else:
                                        add img xzoom (width / 12.0) yzoom 1.0

        # ============================================================
        # MP
        # ============================================================
        fixed:
            xpos 0
            ypos 85
            xysize (157, 30)
            if is_dead:
                at desaturate_dead2

            $ mp_transform = damage_gradient_black if mp_color == "#ffffffc2" else damage_gradient_semigray if mp_color == "#3adeff" else damage_gradient_gray
            $ mp_text_size = 30 if char.current_mp < 1000 else (24 if char.current_mp < 10000 else 20)

            fixed:
                xpos 0
                ypos 4
                xysize (50, 30)
                text "{font=determination.otf}{size=[mp_text_size]}[char.current_mp]{/font}{/size}":
                    color mp_color
                    style mp_style
                    xalign 0.0
                    yalign 0.5
                    at mp_transform

            fixed:
                xpos 52
                ypos 9
                xysize (102, 12)
                hbox:
                    spacing 4
                    for i in range(10):
                        add "mppassive.png" at damage_gradient_black
                hbox:
                    spacing 4
                    for img, transforms, width in mp_normal_bar_transforms:
                        if img is not None:
                            fixed:
                                xysize (12, 22)
                                if transforms:
                                    add img xzoom (width / 12.0) yzoom 1.0 at transforms
                                else:
                                    add img xzoom (width / 12.0) yzoom 1.0
                if is_overmana:
                    hbox:
                        spacing 4
                        for img, transforms, width in mp_over_bar_transforms:
                            if img is not None:
                                fixed:
                                    xysize (12, 22)
                                    if transforms:
                                        add img xzoom (width / 12.0) yzoom 1.0 at transforms
                                    else:
                                        add img xzoom (width / 12.0) yzoom 1.0


screen team_status_display():
    zorder 3

    if show_team_status == 1:
        hbox:
            if get_character_picked_for_shift() == 4:
                xoffset 0
            elif get_character_picked_for_shift() == 3:
                xoffset 150
            elif get_character_picked_for_shift() == 2:
                xoffset 300
            else:
                xoffset 450

            # ============================================================
            # ВЕРХНИЙ РЯД: портреты с цветными трансформами
            # ============================================================
            hbox:
                xoffset 8
                spacing 0
                if charicontimetodis == 1:
                    at charicondis
                else:
                    at chariconapp

                # Крис
                vbox:
                    $ kris_hp_gain, kris_mp_gain = get_hp_mp_gain_flags(store.pers_dict["Крис"])
                    if store.pers_dict["Крис"].damage_gain_for_vis == 1:
                        add "Крисherobox.png" at savedspace_colour_yellow
                    elif kris_hp_gain and kris_mp_gain:
                        add "Крисherobox.png" at savedspace_colour_cyan
                    elif kris_mp_gain:
                        add "Крисherobox.png" at savedspace_colour_blue
                    elif store.pers_dict["Крис"].damage_gain_for_vis >= 10:
                        add "Крисherobox.png" at savedspace_colour_red
                    elif store.pers_dict["Крис"].damage_gain_for_vis <= -2:
                        add "Крисherobox.png" at savedspace_colour_green
                    elif store.pers_dict["Крис"].current_hp <= 0:
                        add "Крисherobox.png" at desaturate_dead
                    elif store.pers_dict["Крис"].current_hp <= store.pers_dict["Крис"].max_hp * 0.2:
                        add "Крисherobox.png" at savedspace_colour_red_pulse
                    else:
                        add "Крисherobox.png"

                # Остальные члены команды
                if store.team_manager is not None:
                    for char_name in store.team_manager.team_slots[1:]:
                        if char_name:
                            vbox:
                                $ hp_gain, mp_gain = get_hp_mp_gain_flags(store.pers_dict[char_name])
                                if store.pers_dict[char_name].damage_gain_for_vis == 1:
                                    add "[char_name]herobox.png" at savedspace_colour_yellow
                                elif hp_gain and mp_gain:
                                    add "[char_name]herobox.png" at savedspace_colour_cyan
                                elif mp_gain:
                                    add "[char_name]herobox.png" at savedspace_colour_blue
                                elif store.pers_dict[char_name].damage_gain_for_vis >= 10:
                                    add "[char_name]herobox.png" at savedspace_colour_red
                                elif store.pers_dict[char_name].damage_gain_for_vis <= -2:
                                    add "[char_name]herobox.png" at savedspace_colour_green
                                elif store.pers_dict[char_name].current_hp <= 0:
                                    add "[char_name]herobox.png" at desaturate_dead
                                elif store.pers_dict[char_name].current_hp <= store.pers_dict[char_name].max_hp * 0.2:
                                    add "[char_name]herobox.png" at savedspace_colour_red_pulse
                                else:
                                    add "[char_name]herobox.png"

            # ============================================================
            # НИЖНИЙ РЯД: карточки HP/MP/имя/еда
            # ============================================================
            hbox:
                ypos 20
                if charicontimetodis == 1:
                    at charnamedis
                else:
                    at charnameappfast

                spacing 163#157 - 0.5 * get_character_picked_for_shift()

                if "Крис" in store.pers_dict:
                    use character_status_card(store.pers_dict["Крис"])

                if store.team_manager is not None:
                    for char_name in store.team_manager.team_slots[1:]:
                        if char_name and char_name in store.pers_dict:
                            use character_status_card(store.pers_dict[char_name])


# Переменные для управления ходом боя
default current_attacker = 1 # Номер персонажа, который сейчас атакует (1-Крис, 2-Азриель, 3-Чара, 4-Фриск, 5-Иззи, 6-Кловер, 7-Седрик)
default current_target = None    # Объект врага, которого выбрали целью
default attack_type = None       # Тип атаки (например, 2)

# Словарь для соответствия ID персонажей их именам
default pers_names = {
    1: "Крис",
    2: "Азриель",
    3: "Чара",
    4: "Фриск",
    5: "Седрик",
    6: "Кловер",
    7: "Иззи",
    8: "Арчи"
}

# Словарь для соответствия имен персонажей их ID
default pers_ids = {
    "Крис": 1,
    "Азриель": 2,
    "Чара": 3,
    "Фриск": 4,
    "Седрик": 5,
    "Кловер": 6,
    "Иззи": 7,
    "Арчи": 8
}

default switched = 0
default section = 1
default global_level = 10
default turntype = 0

default asrimaxhp = 100

# Переменные для отслеживания состояния кнопок между секциями
default previous_global_level_to_compare = 0  # Предыдущий уровень для сравнения
default current_global_level_to_compare = 0   # Текущий уровень для сравнения
default switchnextisup = 0  # Флаг, что кнопка "вперед" была поднята
default switchprevup = 0    # Флаг, что кнопка "назад" была поднята


#                                                                                                       Стиль окна для перемещения и битв
default txt = 0

# Заменить в итоговом файле
    #style window:
    #xalign 0.5
    #xfill True
    #yalign gui.textbox_yalign
    #ysize gui.textbox_height
    #
    #background ConditionSwitch(
    #    "txt == '0'", Image("gui/textbox.png", xalign=0.5, yalign=1.0),
    #    "txt == '1'", Image("gui/textbox2.png", xalign=0.5, yalign=1.0),
    #    True, Image("gui/textbox2.png", xalign=0.5, yalign=1.0)  # Значение по умолчанию
    #)

    #!!!!!! НЕ ЗАБЫТЬ ЗАСУНУТЬ gui/textbox2.png



########################################### ПЕРЕМЕННЫЕ ДЛЯ ДОБАВЛЕНИЯ ДОП ЭКРАНОВ МЕНЮ КНОПОК


default perekluch = 0

default act2 = 1
default actswitch = 0

default magic = 1
default magic2 =  1
default magic_switch = 0

default item2 = 1
default item_switch = 0



label buttoms:


    $ show_enemy_status = 1
    # Сбрасываем состояние кнопок перед началом нового хода персонажа,
    # чтобы не оставались экраны прошлой анимации (например atob/abackdis).
    $ fightchoice = 0
    $ actchoice = 0
    $ magicchoice = 0
    $ itemchoice = 0

    hide screen choose_attack_screen
    hide screen actchoice1
    hide screen choose_magic_screen
    hide screen itemchoice2

    hide screen ftoc
    hide screen atoc
    hide screen mtoc
    hide screen itoc

    hide screen ftob
    hide screen atob
    hide screen mtob
    hide screen itob

    hide screen fbackapp
    hide screen abackapp
    hide screen mbackapp
    hide screen ibackapp

    hide screen fbackdis
    hide screen abackdis
    hide screen mbackdis
    hide screen ibackdis




    
    $ store.show_enemy_status = 1
    show screen fvapp
    show screen ivapp
    show screen avapp
    show screen mvapp
    #"{alpha=0.0}Этот текст невидим{/alpha}"
    #window hide

    $ target = None
    $ attackindex = None
    $ renpy.pause(9999, hard=True)
    jump buttoms




default turn_type_for_switchers = 0
# 1 для атаки
# 2 для предметов
# 3 для магии
# 4 для предмета

###############################################################################################################______ТРАНСФОРМЫ____________######################################################################################################################################################################


################################################################################################################################################################   ТРАНСФОРМЫ ЗДОРОВЬЯ И МАНЫ 



######################################################################################################## ДИАЛОГОВОЕ ОКНО

transform ddu:
    xpos 0.19 ypos 1.5
    easein 0.5 ypos 475

transform dud:
    xpos 0.19 ypos 475
    easein 0.5 ypos 1.5
transform du:
    xpos 0.19 ypos 475






################################################################################################# ТРАНСФОРМЫ ДЛЯ ПЕРЕКЛЮЧАТЕЛЕЙ
transform ndu: 
    xpos 0.8 ypos 1.2
    easein 0.4 ypos 0.66
transform nud:
    xpos 0.8 ypos 0.66
    easein 0.4 ypos 1.2
transform nu:
    xpos 0.8 ypos 0.66
transform nd:
    xpos 0.8 ypos 1.2


transform pdu:
    xpos 0.085 ypos 1.2
    easein 0.4 ypos 0.66
transform pud:
    xpos 0.085 ypos 0.66
    easein 0.4 ypos 1.2
transform pu:
    xpos 0.085 ypos 0.66
transform pd:
    xpos 0.085 ypos 1.2








###################################################################################################################### Появление кнопок сверхку

transform fapp:
    xoffset 78 yoffset 28
    subpixel True
    yanchor 0.5 xanchor 0.5
    xpos 280 ypos 900
    easein 0.6 xpos 280 ypos 650

    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0


transform aapp:
    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True
    xpos 460 ypos 900 
    easein 0.6 xpos 460 ypos 650

    
    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0


transform mapp:
    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True
    xpos 640 ypos 900
    easein 0.6 xpos 640 ypos 650
    
    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0


transform iapp:
    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True

    xpos 820 ypos 900                                                                                                                       #
    easein 0.6 xpos 820 ypos 650 
    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0
                                                                                                        
                                                                                                                                             
                                                                                                                                            
                                                                                                                                            
###################################################################################################################### Появление кнопок сбоку     

transform fapph:
    xpos 280  ypos 900
    easein 0.6 xpos 280  ypos 650
transform aapph:
    xpos 460 ypos 900 
    easein 0.6 xpos 460 ypos 650
transform mapph:
    xpos 640 ypos 900
    easein 0.6 xpos 640 ypos 650
transform iapph:
    xpos 820 ypos 900
    easein 0.6 xpos 820 ypos 650


###################################################################################################################### съёб кнопок сбоку


transform fdis:
    xpos 280  ypos 650
    easein 0.6 xpos 280  ypos 900
transform adis:
    xpos 460 ypos 650
    easein 0.6 xpos 460 ypos 900 
transform mdis:
    xpos 640 ypos 650
    easein 0.6 xpos 640 ypos 900
transform idis:
    xpos 820 ypos 650
    easein 0.6 xpos 820 ypos 900

#transform buttomcenter:
#    easein 0.6 xpos 0.050 ypos 600

###################################################################################################################### съёб кнопок на место

#transform toc:
#    easein 0.6 xpos 550 ypos 450


transform ftoc:
    subpixel True
    #zoom 1.1
    xpos 280  ypos 650
    easein 0.6 xpos 550 ypos 450 #zoom 1.0
transform atoc:
    subpixel True
    xpos 460 ypos 650
    easein 0.6 xpos 550 ypos 450
transform mtoc:
    subpixel True
    xpos 640 ypos 650
    easein 0.6 xpos 550 ypos 450
transform itoc:
    subpixel True
    xpos 820 ypos 650
    easein 0.6 xpos 550 ypos 450





transform goapp:
    xpos 530 ypos 900
    easein 0.5 ypos 460

transform godis:
    ypos 460 xpos 530
    easein 0.5 xpos 530 ypos 900


transform goappcook:
    xpos 600 ypos 900
    easein 0.5 ypos 600








transform tof:

    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True

    xpos 550 ypos 450
    easein 0.6 xpos 280  ypos 650

    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0

transform toa:

    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True
     

    xpos 550 ypos 450
    easein 0.6 xpos 460 ypos 650

    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0

transform tom:
    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True
     

    xpos 550 ypos 450
    easein 0.6 xpos 640 ypos 650

    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0


transform toi:

    xoffset 78 yoffset 28 yanchor 0.5 xanchor 0.5
    subpixel True


    xpos 550 ypos 450
    easein 0.6 xpos 820 ypos 650

    on hover:
        easein 0.2 zoom 1.1
    on idle:
        easeout 0.2 zoom 1.0













###############################################################################################################_______ИЗОБРАЖЕНИЯ___________######################################################################################################################################################################

#################################################### АНИМАЦИИ
image enemyanimation = Movie(play="images/best_gif.webm", size=(1280, 720), loop=0, xpos=640, ypos=720)

#################################################### КНОПКИ
image fightbuttom = "fightor.png"
image fightbuttomback = "backor1.png"

image actbuttom = "actor.png"
image actbuttomback = "backor1.png"

image magicbuttom = "magicor.png"
image magicbuttomback = "backor1.png"

image itembuttom = "itemor.png"
image itembuttomback = "backor1.png"
################################################### ДИАЛОГИ МЕЖДУ ХОДАМИ
image dialogue1round = "dialogue1round.png"
image dialogue = "dialogueuni.png"

##################################################  КНОПКИ ПЕРЕКЛЮЧЕНИЯ 
image switchnext = "switchnext2.png"
image switchprev = "switchprevous.png"

##################################################  ТЕЛО ПРОТИВНИКА
image imageenemyhead = "golova.png"
image imageenemybody = "tulov.png"
image imageenemylegs = "nog.png"




######################################################################################################## ГУСЕНИЧКА 

#№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№   Качание гусенички

transform enemyheadmove:
    #xpos 0.445 ypos 0.2

    linear 0.35 xpos 0.45 ypos 0.2
    linear 0.35 xpos 0.445 ypos 0.195 
    linear 0.35 xpos 0.44 ypos 0.2
    linear 0.35 xpos 0.445 ypos 0.195 
    repeat

transform enemybodymove:
    #0.445 ypos 0.25
    #xpos 0.5 ypos 0.65

    linear 0.34 xpos 0.45 ypos 0.25
    linear 0.34 xpos 0.445 ypos 0.245 
    linear 0.34 xpos 0.44 ypos 0.25
    linear 0.34 xpos 0.445 ypos 0.245 
    repeat

transform enemylegsmove:
    #xpos 0.5 ypos 0.7
    #xpos 0.45 ypos 0.3

    linear 0.33 xpos 0.45 ypos 0.3
    linear 0.33 xpos 0.445 ypos 0.295 
    linear 0.33 xpos 0.44 ypos 0.3
    linear 0.33 xpos 0.445 ypos 0.295 
    repeat

######################################### Появление гусенички

transform enemyheadappear:
    xpos 0.445 ypos 0.2
transform enemybodyappear:
    xpos 0.445 ypos 0.25
transform enemylegsappear:
    xpos 0.45 ypos 0.3

##################         ПОЯВЛЕНИЕ ТЕЛА ГУСЕНИЧКИ В БОЮ
screen enemyanimation:
    timer 1.0 action Jump("afterenemyanimation")

label afterenemyanimation:
    pause 1
    hide enemyanimation
    
    #тут будет атака

    show imageenemylegs at enemylegsappear
    show imageenemybody at enemybodyappear
    show imageenemyhead at enemyheadappear
    pause 0.3
    show imageenemylegs at enemylegsmove
    show imageenemybody at enemybodymove
    show imageenemyhead at enemyheadmove
    show screen pause
    jump playerturn







###############################################################################################################______ЛЕЙБЛЫ____________######################################################################################################################################################################








############################################################################################# ПЕРЕХОДЫ ПРИ НАЖАТИИ КНОПОК


################################################   ПЕРЕХОДЫ АТАКИ

default fightchoice = 0
default actchoice = 0
default magicchoice = 0
default itemchoice = 0
default chosenstyle = 1
#chosen_style: 1=Атака, 2=действие, 3=магия, 4=инвентарь





label backchosen:
    
    hide turntarget
    hide screen attack_name_display  # Добавляем скрытие экрана с анимацией
    #для переключателей меню
    $ section = 1
    $ target = None
    $ turntype2 = 0

    if nextswitch_style == 1:
        show switchnext at nud
        $ nextswitch_style = 0
        
    if prevswitch_style == 1:
        show switchprev at pud
        $ prevswitch_style = 0
    hide dialogue

    hide dialogue1round
    show dialogue1round at du

    call buttomcentercheck

    $ fightchoice = 0
    $ actchoice = 0
    $ magicchoice = 0
    $ itemchoice = 0





    
    
    $ renpy.pause(999999, hard=True)  
    return



label fightchosen:
    
    show screen attack_name_display
    $ store.attack_section_switch = None
    $ store.attackindex=None
    $ turntype2 = 1

    $ section = 1

    hide dialogue1round
    
    hide screen fvapp
    hide screen ftob
    show screen ftoc
    
    hide screen fbackdis
    hide screen fbackapp
    show screen fbackapp
     
    show dialogue at du
    #call check_switchers
    show screen choose_attack_screen



    

    call buttomcentercheck


    $ fightchoice = 1
    $ actchoice = 0
    $ magicchoice = 0
    $ itemchoice = 0    
    # show screen pause
    
    #$ renpy.pause(999999, hard=True)     

    jump nolabel
    



label actchosen:

    $ store.pokaz_poshad = 1
    hide screen abackapp
    hide screen abackdis
    hide screen atob

    show screen attack_name_display
    $ store.act_section_switch = None

    
    $ attackindex = None
    #call check_switchers
    $ section = 1

    $ turntype2 = 1


    hide dialogue1round
    
    hide screen avapp
    hide screen atob
    show screen atoc

    hide screen abackdis
    hide screen abackapp
    show screen abackapp
  
    #show dialogue1round at du
    show dialogue at du
    show screen actchoice1


    call buttomcentercheck


    $ fightchoice = 0
    $ actchoice = 1
    $ magicchoice = 0
    $ itemchoice = 0    
    # show screen pause

    
    $ renpy.pause(999999, hard=True)    
    jump actchosen




label magicchosen:

    

    show screen attack_name_display
    
    $ store.magic_section_switch = None
    
    $ attackindex = None

    $ section = 1

    $ turntype2 = 1


    hide dialogue1round
    
    hide screen mvapp
    hide screen mtob
    show screen mtoc

    show screen mbackapp    
    hide screen mbackdis


    show dialogue at du
    
    show screen choose_magic_screen
    #show screen switchdis

    #show dialogue1round at du

    call buttomcentercheck



    $ fightchoice = 0
    $ actchoice = 0
    $ magicchoice = 1
    $ itemchoice = 0  
    # show screen pause



    $ renpy.pause(999999, hard=True)
    jump magicchosen    



default itemtype = 1 # 1-выбрали инвентарь. Стандарт - расходники, 2 - свапнули на оружку, 3 - свап на расходники, 4 - нажали бэк

label itemchosen:
    show screen attack_name_display

    $ itemtype = 1 
    $ target = None
    $ attackindex = None
    $ itemchoice = 0

    $ section = 1
    
    $ turntype2 = 1

    hide dialogue1round
    
    hide screen ivapp
    hide screen itob
    show screen itoc

    show screen ibackapp    
    hide screen ibackdis

    hide image "dialogue1round.png"
    #show image "dialogue1round.png" at dud

    
    #show dialogue at du
    
    hide dialogue
    hide dialogue1round
    #show screen switchdis

    #show dialogue1round at du
    #hide screen attack_name_display
    show screen itemchoice2


    call buttomcentercheck


    


    $ fightchoice = 0
    $ actchoice = 0
    $ magicchoice = 0
    $ itemchoice = 1    
    # show screen pause
    
    $ renpy.pause(999999, hard=True)
    jump itemchosen    



label gameover:
    # DECAYING: смерть через этот путь тоже портит тело Криса.
    # Вызов идемпотентен — двойного списания за один game over не будет.
    $ kris_decaying_register_death()
    # «Подсознательная память» Азриеля (тоже идемпотентно).
    $ azri_register_battle_lost()
    "Ты проиграл"




label buttomcentercheck:
    if fightchoice == 1:
        hide screen choose_attack_screen


        hide screen ftoc
        show screen ftob

        hide screen fbackapp
        show screen fbackdis
        show screen pause
        pause 0.5


    elif actchoice == 1:
        hide screen actchoice1

        hide screen atoc
        show screen atob
        hide screen abackapp
        show screen abackdis
        show screen pause
        pause 0.5
       

    elif magicchoice == 1:
        hide screen choose_magic_screen

        hide screen mtoc
        show screen mtob

        hide screen mbackapp
        show screen mbackdis
        show screen pause
        pause 0.5
    elif itemchoice == 1:
        hide screen itemchoice2

        hide screen itoc

        hide screen ibackapp
        
        hide screen ibackapp
        show screen ibackdis
        show screen itob
        show screen pause
        pause 0.5



############################################################################################################______________ЭКРАНЫ____________######################################################################################################################################################################

#######################################################################________Экраны атаки


##############################___Приход вертикал

screen fvapp:
    zorder 3
    vbox:
        
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                imagebutton:
                    idle "fight_kris_up1.png"
                    hover "fight_kris_up1.png"
                    at fapp
                    action Call("fightchosen")
            else:
                if summoned == 0:
                    imagebutton:
                        idle "fight_kris_down1.png"
                        hover "fight_kris_down1.png"
                        at fapp
                        action Call("fightchosen")
                
                if summoned == 1:
                    imagebutton:
                        idle "fight_kris_mech_back17.png"
                        hover "fight_kris_mech_back17.png"
                        at fapp
                        action Call("fightchosen")

                if summoned == 2:
                    imagebutton:
                        idle "fight_kris_shit_back17.png"
                        hover "fight_kris_shit_back17.png"
                        at fapp
                        action Call("fightchosen")

        else:
            imagebutton:
                idle "fightor.png"
                hover "fightor.png"
                at fapp
                action Call("fightchosen")


#############################____приход центр 

screen ftoc:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                add "fight_kris_up" at ftoc

            else:
                if summoned == 0:
                    add "fight_kris_down" at ftoc
                if summoned == 1:
                    add "fight_kris_mech" at ftoc
                if summoned == 2:
                    add "fight_kris_shit" at ftoc                        
        else:
            imagebutton:
                idle "fightor.png"
                hover "fightor.png"
                at ftoc
                action NullAction()


############################_____Уход из центра

screen ftob:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                imagebutton:
                    idle "fight_kris_up_back"
                    hover "fight_kris_up_back"
                    at tof
                    action Jump("fightchosen")
            else:
                if summoned == 0:
                    imagebutton:
                        idle "fight_kris_down_back"
                        hover "fight_kris_down_back"
                        at tof
                        action Jump("fightchosen")
                if summoned == 1:
                    imagebutton:
                        idle "fight_kris_mech_back"
                        hover "fight_kris_mech_back"
                        at tof
                        action Jump("fightchosen")
                if summoned == 2:
                    imagebutton:
                        idle "fight_kris_shit_back"
                        hover "fight_kris_shit_back"
                        at tof
                        action Jump("fightchosen")
        else:
            imagebutton:
                idle "fightor.png"
                hover "fightor.png"
                at tof
                action Jump("fightchosen")










#######################################################################________Экраны действия


##############################___Экран назад

screen fbackapp:
    zorder 3
    vbox:
        if fightchoice == 1:
            imagebutton:
                idle "backor1.png"
                hover "backor1.png"
                at fapph
                action [Hide("choose_attack_screen"), Show("fbackdis"), SetVariable("attackindex", None),  Jump("backchosen"), SetVariable("target", None)]
    #Show("switchdis")
screen abackapp:
    zorder 3
    if actchoice == 1:
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at aapph
            action [SetVariable("attackindex", None), Jump("backchosen"), SetVariable("target", None)]
screen ibackapp:
    zorder 3
    if itemchoice == 1:
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at iapph
            action [SetVariable("attackindex", None), Jump("backchosen"), SetVariable("target", None)]
screen mbackapp:
    zorder 3
    if magic == 1:
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at mapph
            action [SetVariable("attackindex", None), Jump("backchosen"), SetVariable("target", None)]










screen fbackdis:
    zorder 3
    vbox:
        if fightchoice == 1:
            if current_attacker == 1:
                if pers_dict["Крис"].sprite_style == "up":
                    imagebutton:
                        idle "backor1.png"
                        hover "backor1.png"
                        at fdis
                        action NullAction()
                else:
                    if summoned == 0:
                        imagebutton:
                            idle "backor1.png"
                            hover "backor1.png"
                            at fdis
                            action NullAction()
                    if summoned == 1:
                        imagebutton:
                            idle "backor1.png"
                            hover "backor1.png"
                            at fdis
                            action NullAction()
                    if summoned == 2:
                        imagebutton:
                            idle "backor1.png"
                            hover "backor1.png"
                            at fdis
                            action NullAction()
            else:
                imagebutton:
                    idle "backor1.png"
                    hover "backor1.png"
                    at fdis
                    action NullAction()
screen abackdis:
    zorder 3
    if actchoice == 1:
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at adis
            action NullAction()
screen ibackdis:
    zorder 3
    if itemchoice == 1:
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at idis
            action NullAction()
screen mbackdis:  
    zorder 3   
    if magic == 1:
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at mdis
            action NullAction()

##############################___Приход вертикал

screen avapp:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                imagebutton:
                    idle "Kris_act_up_toc1.png"
                    hover "Kris_act_up_toc1.png"
                    at aapp
                    action [Jump("actchosen"), SetVariable("target", None)]
            else:
                imagebutton:
                    idle "Kris_act_down_toc1.png"
                    hover "Kris_act_down_toc1.png"
                    at aapp
                    action [Jump("actchosen"), SetVariable("target", None)]
                
        else:
            imagebutton:
                idle "actor.png"
                hover "actor.png"
                at aapp
                action [Jump("actchosen"), SetVariable("target", None)]



#############################____приход центр 

screen atoc:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                add "Kris_act_up_toc"  at atoc
            else:
                add "Kris_act_down_toc"  at atoc
        else:
            imagebutton:
                idle "actor.png"
                hover "actor.png"
                at atoc
                action NullAction()


############################_____Уход из центра

screen atob:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                imagebutton:
                    idle "Kris_act_up_tob"
                    hover "Kris_act_up_tob"
                    at toa
                    action [Jump("actchosen"),SetVariable("target", None)]
            else:
                imagebutton:
                    idle "Kris_act_down_tob"
                    hover "Kris_act_down_tob"
                    at toa
                    action [Jump("actchosen"),SetVariable("target", None)]
        else:
            imagebutton:
                idle "actor.png"
                hover "actor.png"
                at toa
                action [Jump("actchosen"),SetVariable("target", None)]











#######################################################################________Экраны предмета








##############################___Приход вертикал

screen ivapp:
    zorder 3
    vbox:
        if current_attacker == 1:
            imagebutton:
                idle "Kris_item_toc1.png"
                hover "Kris_item_toc1.png"
                at iapp
                action [Jump("itemchosen"),SetVariable("target", None)]
        else:
                
            imagebutton:
                idle "itemor.png"
                hover "itemor.png"
                at iapp
                action [Jump("itemchosen"),SetVariable("target", None)]



#############################____приход центр 

transform itemtype1:
    alpha 0.0
    easein 0.2 alpha 1.0


transform itemtype2_icon_dis:
    anchor (0.5, 0.5) xoffset 95 yoffset 70
    parallel:
        easein 0.5 xoffset -50 rotate -200 alpha 0.0
    parallel:
        ease 0.45 yoffset 170 

transform itemtype2_icon_app:
    anchor (0.5, 0.5)
    xoffset 275 yoffset 170 alpha 0.0 rotate 200
    parallel:
        easein 0.5 xoffset 95 rotate -0 alpha 1.0
    parallel:
        ease 0.45 yoffset 70 

    


transform switcher_turn:
    
    xoffset -7 yoffset -27
    easein 0.2 rotate -200     
    easeout 0.05 rotate -180


transform text_switch_itemtype1:
    matrixcolor ColorizeMatrix("#FFFFff", "#FFFFff")
    easein 0.8 matrixcolor ColorizeMatrix("#FFFF00", "#FFFF00")


transform text_switch_app:
    yoffset -10 alpha 0.0
    easein 0.5 alpha 1.0 yoffset 0

transform text_switch_dis:
    easein 0.5 alpha 0.0 yoffset 10




screen itoc:
    zorder 3
    if current_attacker == 1:
        add "Kris_anim_toc" at itoc #at idis
    else:
        vbox:
            imagebutton:
                idle "itemor.png"
                hover "itemor.png"
                at idis
                action NullAction()

    if itemtype == 1:
        
        # фрейм для бг текста
        frame:
            xoffset 60 yoffset 2
            background "#000000"
            xsize 94
            ysize 52
            at itoc
        
        add "cons.png" yoffset 2 xoffset 60 at itoc,  text_switch_itemtype1 
        imagebutton:
            xpos 1025 ypos 508
            idle "switcher_idle.png"
            hover "switcher_hover.png"
            at itemtype1
            action [SetVariable("itemtype", 2), SetVariable("battle_inventory_type", "weapon")]

        add "switcher.png" xpos 1025 ypos 508 xoffset 20 at itemtype1

        add "wep_item.png" xpos 1025 ypos 508 xoffset 10 at itemtype1

        


        # xpos 1025 ypos 508


    if itemtype == 2:


        # фрейм для бг текста
        frame:
            xoffset 60 yoffset 2
            background "#000000"
            xsize 94
            ysize 52
            xpos 550 ypos 450
        
        add "cons.png" yoffset 2 xoffset 60 xpos 550 ypos 450 at text_switch_dis
        add "weap.png" yoffset 2 xoffset 60 xpos 550 ypos 450 at text_switch_app



        imagebutton:
            xpos 1025 ypos 508
            idle "switcher_idle.png"
            hover "switcher_hover.png"

            action [SetVariable("itemtype", 3), SetVariable("battle_inventory_type", "consumerables")]

        add "switcher.png" xpos 1025 ypos 508 at switcher_turn

        
        add "con_item.png" xpos 1025 ypos 508 at itemtype2_icon_app
        add "wep_item.png" xpos 1025 ypos 508 at itemtype2_icon_dis



    if itemtype == 3:
        # фрейм для бг текста
        # фрейм для бг текста
        frame:
            xoffset 60 yoffset 2
            background "#000000"
            xsize 94
            ysize 52
            xpos 550 ypos 450
        
        add "weap.png" yoffset 2 xoffset 60 xpos 550 ypos 450 at text_switch_dis
        add "cons.png" yoffset 2 xoffset 60 xpos 550 ypos 450 at text_switch_app

        imagebutton:
            xpos 1025 ypos 508
            idle "switcher_idle.png"
            hover "switcher_hover.png"

            action [SetVariable("itemtype", 2), SetVariable("battle_inventory_type", "weapon")]

        add "switcher.png" xpos 1025 ypos 508 at switcher_turn

        add "con_item.png" xpos 1025 ypos 508 at itemtype2_icon_dis
        add "wep_item.png" xpos 1025 ypos 508 at itemtype2_icon_app

    if itemtype == 4:
        frame:
            xoffset 60 yoffset 2
            background "#ff0000"
            xsize 94
            ysize 52
            xpos 820 ypos 650
    





############################_____Уход из центра



screen itob:
    zorder 3
    if current_attacker == 1:
        imagebutton:
            idle "Kris_anim_tob"
            hover "Kris_anim_tob"
            at toi
            #at iapph
            action [Jump("itemchosen"),SetVariable("target", None)]


    else:
        vbox:
            imagebutton:
                idle "itemor.png"
                hover "itemor.png"
                at iapph
                action [Jump("itemchosen"),SetVariable("target", None)]





#######################################################################________Экраны магии








##############################___Приход вертикал

screen mvapp:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                imagebutton:
                    idle "Kris_magic_up_toc1.png"
                    hover "Kris_magic_up_toc1.png"
                    at mapp
                    action [Jump("magicchosen"),SetVariable("target", None)]
            else:
                imagebutton:
                    idle "Kris_magic_down_toc1.png"
                    hover "Kris_magic_down_toc1.png"
                    at mapp
                    action [Jump("magicchosen"),SetVariable("target", None)]
               
        else:
            imagebutton:
                idle "magicor.png"
                hover "magicor.png"
                at mapp
                action [Jump("magicchosen"),SetVariable("target", None)]



#############################____приход центр 

screen mtoc:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                add "Kris_magic_up_toc" at mtoc
            else:
                add "Kris_magic_down_toc" at mtoc

        else:
            imagebutton:
                idle "magicor.png"
                hover "magicor.png"
                at mtoc
                action NullAction()


############################_____Уход из центра

screen mtob:
    zorder 3
    vbox:
        if current_attacker == 1:
            if pers_dict["Крис"].sprite_style == "up":
                imagebutton:
                    idle "Kris_magic_up_toc"
                    hover "Kris_magic_up_toc"
                    at tom
                    action [Jump("magicchosen"),SetVariable("target", None)]

            else:
                imagebutton:
                    idle "Kris_magic_down_tob"
                    hover "Kris_magic_down_tob"
                    at tom
                    action [Jump("magicchosen"),SetVariable("target", None)]


        else:
            imagebutton:
                idle "magicor.png"
                hover "magicor.png"
                at tom
                action [Jump("magicchosen"),SetVariable("target", None)]










################################################################################################################################################################ МЕНЮ ВЫБОРА ПОСЛЕ НАЖАТИЯ


###############################################################################################################  МЕНЮ ВЫБОРА АТАКИ 1




default enemytoatkchosen = 0

default attackindex = None
default battlenumber = 20
default enemycombatsubject = None
default enemycount = None




# Старый PNG-вариант описаний отключён. Теперь содержимое формируется
# непосредственно внутри screen attack_description:
# image attack_description = ConditionSwitch(...)


# Убрали current_attackerturn, так как теперь используем current_attacker (номер)

transform desc_position:
    on show:
        xpos 1280 ypos 95 alpha 0.0
        pause 0.7
        easein 0.5 xpos 350 alpha 1.0
    on hide:
        easein 0.5 xpos 1280 alpha 0.0








####################################################################################################################################################  НАЧАЛЬНЫЙ ЭКРАН С КНОПКАМИ

################################################################################## ЭКРАНЫ С КНОПКОЙ АТАКИ

screen fightbuttom:
    vbox:
        xpos 0.05 ypos 0.05
        spacing 10
        imagebutton:
            idle "fightor.png"
            hover "fightor.png"
            #hovered Play("sound", "audio/buttonselected.mp3")
            action [SetVariable("attackindex", None),  Jump("screenfight")]

screen fightbackbuttom:
    vbox:
        xpos 0.05 ypos 0.05
        spacing 10
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            #at fightbuttompos
            #hovered Play("sound", "audio/buttonselected.mp3")
            action [SetVariable("attackindex", None),  Jump("fightbuttomback")]

################################################################################## ЭКРАНЫ С КНОПКОЙ ДЕЙСТВИЯ

screen actbuttom:
    vbox:
        xpos 0.05 ypos 0.2
        spacing 10
        imagebutton:
            idle "actor.png"
            hover "actor.png"  # Добавьте hover-состояние
            action [SetVariable("attackindex", None),  Jump("screenact")]
            #Play("sound", "audio/select.wav")
            #hovered Play("sound", "audio/hover.wav")

screen actbackbuttom():
    vbox:
        xpos 0.05 ypos 0.2
        spacing 10
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"  # Добавьте hover-изображение
            at actbackappear
            action [
                #Play("sound", "audio/click.wav"),
                SetVariable("attackindex", None),
                
                Jump("actbuttomback")
            ]
            hovered Play("sound", "audio/hover.wav")

################################################################################## ЭКРАНЫ С КНОПКОЙ МАГИИ

screen magicbuttom:
    vbox:
        xpos 0.05 ypos 0.35
        spacing 10
        imagebutton:
            idle "magicor.png"
            hover "magicor.png"
            #hovered Play("sound", "audio/buttonselected.mp3")
            action [SetVariable("attackindex", None),  Jump("screenmagic")]


screen magicbackbuttom():
    imagebutton:
        idle "backor1.png"
        hover "backor1.png"
        action [Hide("magicbackbuttom"), SetVariable("attackindex", None),  Jump("magicbuttomback")]
        xpos 0.05 ypos 0.35


################################################################################## ЭКРАНЫ С КНОПКОЙ ПРЕДМЕТОВ

screen itembuttom:
    vbox:
        xpos 0.05 ypos 0.5
        spacing 10
        imagebutton:
            idle "itemor.png"
            hover "itemor.png"
            #hovered Play("sound", "audio/buttonselected.mp3")
            action [SetVariable("attackindex", None),  Jump("screenitem")]

screen itembackbuttom():  # ДОБАВЛЕН НЕДОСТАЮЩИЙ ЭКРАН
    imagebutton:
        idle "backor1.png"
        hover "backor1.png"
        action [Hide("itembackbuttom"), SetVariable("attackindex", None),  Jump("itembuttomback")]
        xpos 0.05 ypos 0.5




#######################################################################  Экран ухода переключ
#screen switchdis:
#    if switched > 0: #если уже переключ
#        imagebutton:
#            idle "images/switchnext2.png" 
#            hover "images/switchnext2.png" 
#            at nud # Применяем трансформацию
#            action NullAction()         # Используем imagebutton вместо add + timer
#        imagebutton:
#            idle "images/switchprevous.png" 
#            hover "images/switchnext2.png" 
#            at pud  # Применяем трансформацию
#            action NullAction()   
#    else:
#        imagebutton:
#            idle "images/switchnext2.png" 
#            hover "images/switchnext2.png" 
#            at nud # Применяем трансформацию
#            action NullAction()      



######################################################## Экран паузы

screen pause:
    zorder 9999
    imagebutton:
            xalign 0.0 yalign 0.0
            idle "images/saved.png" 
            hover "images/saved.png" 
            action NullAction() 
    timer 0.5 action Hide("pause")


screen turnchoose_analogue:
    zorder 3

    default turnchoose_selected = None
    default turnchoose_return_from = None
    default turnchoose_back_from = None

    if turnchoose_return_from is not None:
        timer 0.6 action SetScreenVariable("turnchoose_return_from", None)

    if turnchoose_back_from is not None:
        timer 0.6 action SetScreenVariable("turnchoose_back_from", None)

    # FIGHT
    imagebutton:
        idle "fightor.png"
        hover "fightor.png"
        if turnchoose_selected == "fight":
            at ftoc
        elif turnchoose_return_from == "fight":
            at tof
        else:
            at fapp
        action [
            SetVariable("attackindex", None),
            SetVariable("section", 1),
            SetVariable("turntype2", 1),
            SetVariable("fightchoice", 1),
            SetVariable("actchoice", 0),
            SetVariable("magicchoice", 0),
            SetVariable("itemchoice", 0),
            Show("attack_name_display"),
            Hide("dialogue1round"),
            Show("dialogue"),
            Hide("actchoice1"),
            Hide("choose_magic_screen"),
            Hide("itemchoice2"),
            Show("choose_attack_screen"),
            SetScreenVariable("turnchoose_back_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "fight" else None),
            SetScreenVariable("turnchoose_return_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "fight" else None),
            SetScreenVariable("turnchoose_selected", "fight"),
        ]

    # ACT
    imagebutton:
        idle "actor.png"
        hover "actor.png"
        if turnchoose_selected == "act":
            at atoc
        elif turnchoose_return_from == "act":
            at toa
        else:
            at aapp
        action [
            SetVariable("target", None),
            SetVariable("attackindex", None),
            SetVariable("section", 1),
            SetVariable("turntype2", 1),
            SetVariable("fightchoice", 0),
            SetVariable("actchoice", 1),
            SetVariable("magicchoice", 0),
            SetVariable("itemchoice", 0),
            Show("attack_name_display"),
            Hide("dialogue1round"),
            Show("dialogue"),
            Hide("choose_attack_screen"),
            Hide("choose_magic_screen"),
            Hide("itemchoice2"),
            Show("actchoice1"),
            SetScreenVariable("turnchoose_back_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "act" else None),
            SetScreenVariable("turnchoose_return_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "act" else None),
            SetScreenVariable("turnchoose_selected", "act"),
        ]

    # MAGIC
    imagebutton:
        idle "magicor.png"
        hover "magicor.png"
        if turnchoose_selected == "magic":
            at mtoc
        elif turnchoose_return_from == "magic":
            at tom
        else:
            at mapp
        action [
            SetVariable("target", None),
            SetVariable("attackindex", None),
            SetVariable("section", 1),
            SetVariable("turntype2", 1),
            SetVariable("fightchoice", 0),
            SetVariable("actchoice", 0),
            SetVariable("magicchoice", 1),
            SetVariable("itemchoice", 0),
            Show("attack_name_display"),
            Hide("dialogue1round"),
            Show("dialogue"),
            Hide("choose_attack_screen"),
            Hide("actchoice1"),
            Hide("itemchoice2"),
            Show("choose_magic_screen"),
            SetScreenVariable("turnchoose_back_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "magic" else None),
            SetScreenVariable("turnchoose_return_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "magic" else None),
            SetScreenVariable("turnchoose_selected", "magic"),
        ]

    # ITEM
    imagebutton:
        idle "itemor.png"
        hover "itemor.png"
        if turnchoose_selected == "item":
            at itoc
        elif turnchoose_return_from == "item":
            at toi
        else:
            at iapp
        action [
            SetVariable("target", None),
            SetVariable("attackindex", None),
            SetVariable("section", 1),
            SetVariable("turntype2", 1),
            SetVariable("fightchoice", 0),
            SetVariable("actchoice", 0),
            SetVariable("magicchoice", 0),
            SetVariable("itemchoice", 1),
            Show("attack_name_display"),
            Hide("dialogue1round"),
            Hide("dialogue"),
            Hide("choose_attack_screen"),
            Hide("actchoice1"),
            Hide("choose_magic_screen"),
            Show("itemchoice2"),
            SetScreenVariable("turnchoose_back_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "item" else None),
            SetScreenVariable("turnchoose_return_from", turnchoose_selected if turnchoose_selected and turnchoose_selected != "item" else None),
            SetScreenVariable("turnchoose_selected", "item"),
        ]

    # BACK на месте выбранной кнопки
    if turnchoose_selected == "fight":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at fapph
            action [
                SetVariable("target", None),
                SetVariable("attackindex", None),
                SetVariable("fightchoice", 0),
                SetVariable("actchoice", 0),
                SetVariable("magicchoice", 0),
                SetVariable("itemchoice", 0),
                Hide("attack_name_display"),
                Hide("choose_attack_screen"),
                Hide("actchoice1"),
                Hide("choose_magic_screen"),
                Hide("itemchoice2"),
                Hide("dialogue"),
                Show("dialogue1round"),
                SetScreenVariable("turnchoose_back_from", "fight"),
                SetScreenVariable("turnchoose_return_from", "fight"),
                SetScreenVariable("turnchoose_selected", None),
            ]
    elif turnchoose_selected == "act":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at aapph
            action [
                SetVariable("target", None),
                SetVariable("attackindex", None),
                SetVariable("fightchoice", 0),
                SetVariable("actchoice", 0),
                SetVariable("magicchoice", 0),
                SetVariable("itemchoice", 0),
                Hide("attack_name_display"),
                Hide("choose_attack_screen"),
                Hide("actchoice1"),
                Hide("choose_magic_screen"),
                Hide("itemchoice2"),
                Hide("dialogue"),
                Show("dialogue1round"),
                SetScreenVariable("turnchoose_back_from", "act"),
                SetScreenVariable("turnchoose_return_from", "act"),
                SetScreenVariable("turnchoose_selected", None),
            ]
    elif turnchoose_selected == "magic":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at mapph
            action [
                SetVariable("target", None),
                SetVariable("attackindex", None),
                SetVariable("fightchoice", 0),
                SetVariable("actchoice", 0),
                SetVariable("magicchoice", 0),
                SetVariable("itemchoice", 0),
                Hide("attack_name_display"),
                Hide("choose_attack_screen"),
                Hide("actchoice1"),
                Hide("choose_magic_screen"),
                Hide("itemchoice2"),
                Hide("dialogue"),
                Show("dialogue1round"),
                SetScreenVariable("turnchoose_back_from", "magic"),
                SetScreenVariable("turnchoose_return_from", "magic"),
                SetScreenVariable("turnchoose_selected", None),
            ]
    elif turnchoose_selected == "item":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at iapph
            action [
                SetVariable("target", None),
                SetVariable("attackindex", None),
                SetVariable("fightchoice", 0),
                SetVariable("actchoice", 0),
                SetVariable("magicchoice", 0),
                SetVariable("itemchoice", 0),
                Hide("attack_name_display"),
                Hide("choose_attack_screen"),
                Hide("actchoice1"),
                Hide("choose_magic_screen"),
                Hide("itemchoice2"),
                Hide("dialogue"),
                Show("dialogue1round"),
                SetScreenVariable("turnchoose_back_from", "item"),
                SetScreenVariable("turnchoose_return_from", "item"),
                SetScreenVariable("turnchoose_selected", None),
            ]

    # Анимация ухода BACK вниз на предыдущем месте
    if turnchoose_back_from == "fight":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at fdis
            action NullAction()
    elif turnchoose_back_from == "act":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at adis
            action NullAction()
    elif turnchoose_back_from == "magic":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at mdis
            action NullAction()
    elif turnchoose_back_from == "item":
        imagebutton:
            idle "backor1.png"
            hover "backor1.png"
            at idis
            action NullAction()



################################################# Всё появляется
transform barsapp:
    xalign 0.98 ypos -900
    easein 0.8 xalign 0.98 ypos 33

transform chariconapp:
    xpos -7 ypos -100
    easein 0.5 xpos -7 ypos -5

transform charicondis:
    xpos -7 ypos -5
    easein 0.5 xpos -7 ypos -100

transform charnameapp:
    xpos 140 ypos -900
    easein 0.8 xpos 140 ypos 20

transform charnameappfast:
    xpos 140 ypos -900
    easein 0.4 xpos 140 ypos 20

transform charnamedis:
    xpos 140 ypos 20
    easein 0.5 xpos 140 ypos -100


transform charhpnapp:
    xalign 0.11 ypos -900
    easein 0.8 xalign 0.11 ypos 53








# Экран для отображения названия атаки в зависимости от attackindex
transform attackinfoapp:
    on show:
        ypos 450 xpos -500
        easein 0.7 xpos 250 ypos 450
    on hide:
        xpos 250 ypos 450
        easein 0.7 ypos 450 xpos -500

transform targetinfoapp:

    on show:
        ypos 450 xpos 1500
        easein 0.7 xpos 725 ypos 450
    on hide:
        xpos 725 ypos 450
        easein 0.7 ypos 450 xpos 1500


default turntype2 = 0

transform name_display_to_down:
    on show:
        ypos 800 xpos 250
        easein 0.7 yoffset -200
    on hide:
        easein 0.7 offset 200

transform name_display_to_down2:
    on show:
        ypos 800 xpos 725
        easein 0.7 yoffset -200
    on hide:
        easein 0.7 offset 200



screen attack_name_display():
    zorder 2

    $ inv_name_map = getattr(store, "consumable_names", {})
    $ inv_item_name = get_battle_item_name(hovered_artifact_id, inv_name_map)
    $ inv_desc_lines = get_inventory_desc_lines(hovered_artifact_id)


    #if attackindex is not None:
    #    add "attackinfobg.png" at attackinfoapp
    
    frame:
        background "#ffff00"          # белая рамка
        padding (7, 7, 5, 5)        # толщина рамки


        at attackinfoapp
        xsize 280
        ysize 56

        frame:
            xsize 274
            ysize 50
            background "#000000"     # чёрный фон внутри
            #xpadding 10
            #ypadding 10
            xalign 0.5
            yalign 0.5

            vbox:
                xalign 0.5
                yalign 0.5

                # Крис - Атаки (0-9)
                if attackindex == None:
                    text"{font=determination.otf}{size=30}---" color "#ffff00" 
                elif attackindex and attackindex.startswith("защита_"):
                    text"{font=determination.otf}{size=30}Защищаться" color "#ffff00" 
                elif attackindex == "Удар неудачника":
                    text"{font=determination.otf}{size=30}Удар неудачника"  color "#ffff00"
                elif attackindex == "Удар мечом":
                    text"{font=determination.otf}{size=30}Удар мечом"  color "#ffff00" 
                elif attackindex == "Удар щитом":
                    text"{font=determination.otf}{size=30}Удар щитом"  color "#ffff00" 
                elif attackindex == "C разворота!":
                    text"{font=determination.otf}{size=30}C разворота!"  color "#ffff00" 
                elif attackindex == "Бонк!":
                    text"{font=determination.otf}{size=30}Бонк!"  color "#ffff00" 
                elif attackindex == "Пронзить":
                    text"{font=determination.otf}{size=30}Пронзить"  color "#ffff00" 
                elif attackindex == "Отбить руки":
                    text"{font=determination.otf}{size=30}Отбить глаз"  color "#ffff00" 
                elif attackindex == "Отчаянное комбо":
                    text"{font=determination.otf}{size=30}Отчаянное комбо"  color "#ffff00" 
                elif attackindex == "Рывок защитника (атака)":
                    text"{font=determination.otf}{size=30}Рывок защитника"  color "#ffff00" 
                    
                # Крис - Магия (10-20)
                elif attackindex == "Призвать меч":
                    text"{font=determination.otf}{size=30}Призвать меч"  color "#ffff00" 
                elif attackindex == "Призвать щит":
                    text"{font=determination.otf}{size=30}Призвать щит"  color "#ffff00" 
                elif attackindex == "Напрячься":
                    text"{font=determination.otf}{size=30}Напрячься"  color "#ffff00" 
                elif attackindex == "Позвать за щит":
                    text"{font=determination.otf}{size=30}Позвать за щит"  color "#ffff00" 
                elif attackindex == "Правильный угол":
                    text"{font=determination.otf}{size=30}Правильный угол"  color "#ffff00" 
                elif attackindex == "Слабое место":
                    text"{font=determination.otf}{size=30}Слабое место"  color "#ffff00" 
                elif attackindex == "Концентрация":
                    text"{font=determination.otf}{size=30}Концентрация"  color "#ffff00" 
                elif attackindex == "Поднять щиты!":
                    text"{font=determination.otf}{size=30}Поднять щиты!"  color "#ffff00" 
                elif attackindex == "Стремление вперёд":
                    text"{font=determination.otf}{size=30}Стремление вперёд"  color "#ffff00" 
                elif attackindex == "Рывок защитника (магия)":
                    text"{font=determination.otf}{size=30}Рывок защитника"  color "#ffff00" 
                elif attackindex == "Пробудиться":
                    text"{font=determination.otf}{size=30}Пробудиться"  color "#ffff00" 
                    
                # Азриель - Атаки (0, 21-24)
                elif attackindex == "Удар принца":
                    text"{font=determination.otf}{size=30}Удар принца"  color "#ffff00" 
                elif attackindex == "Взмах мечом":
                    text"{font=determination.otf}{size=30}Взмах мечом"  color "#ffff00" 
                elif attackindex == "Щитовой удар":
                    text"{font=determination.otf}{size=30}Щитовой удар"  color "#ffff00" 
                elif attackindex == "Удар лбом":
                    text"{font=determination.otf}{size=30}Удар лбом"  color "#ffff00" 
                    
                # Азриель - Магия (25-35)
                elif attackindex == "Сменить облик":
                    text"{font=determination.otf}{size=30}Сменить облик"  color "#ffff00" 
                elif attackindex == "Шаг вперёд":
                    text"{font=determination.otf}{size=30}Шаг вперёд"  color "#ffff00" 
                elif attackindex == "Магия огня":
                    text"{font=determination.otf}{size=30}Магия огня"  color "#ffff00" 
                elif attackindex == "Горное равновесие":
                    text"{font=determination.otf}{size=30}Горное равновесие"  color "#ffff00" 
                elif attackindex == "Клинки хаоса":
                    text"{font=determination.otf}{size=30}Клинки хаоса"  color "#ffff00" 
                elif attackindex == "За спиною принца":
                    text"{font=determination.otf}{size=30}За спиною принца"  color "#ffff00" 
                elif attackindex == "Уничтожитель хаоса":
                    text"{font=determination.otf}{size=30}Уничтожитель хаоса"  color "#ffff00" 
                elif attackindex == "Встать с колен":
                    text"{font=determination.otf}{size=30}Встать с колен"  color "#ffff00" 
                elif attackindex == "Звёздный блеск":
                    text"{font=determination.otf}{size=30}Звёздный блеск"  color "#ffff00" 
                elif attackindex == "Боевой клич!":
                    text"{font=determination.otf}{size=30}Боевой клич!"  color "#ffff00" 
                elif attackindex == "Луч Бога Гиперсмерти":
                    text"{font=determination.otf}{size=30}Луч Бога Гиперсмерти"  color "#ffff00" 
                    
                # Чара - Атаки (0, 35-41)
                elif attackindex == "Удар бунтарки":
                    text"{font=determination.otf}{size=30}Удар бунтарки"  color "#ffff00" 
                elif attackindex == "Удар ножом":
                    text"{font=determination.otf}{size=30}Удар ножом"  color "#ffff00" 
                elif attackindex == "Удар шпагой":
                    text"{font=determination.otf}{size=30}Удар шпагой"  color "#ffff00" 
                elif attackindex == "Удар из-за спины":
                    text"{font=determination.otf}{size=30}Удар из-за спины"  color "#ffff00" 
                elif attackindex == "Решето":
                    text"{font=determination.otf}{size=30}Решето"  color "#ffff00" 
                elif attackindex == "Ножевой снаряд":
                    text"{font=determination.otf}{size=30}Ножевой снаряд"  color "#ffff00" 
                elif attackindex == "Реки крови":
                    text"{font=determination.otf}{size=30}Реки крови"  color "#ffff00" 
                    
                # Чара - Магия (42-47)
                elif attackindex == "Гнев":
                    text"{font=determination.otf}{size=30}Гнев"  color "#ffff00" 
                elif attackindex == "Безумие":
                    text"{font=determination.otf}{size=30}Безумие"  color "#ffff00" 
                elif attackindex == "Сумасшествие":
                    text"{font=determination.otf}{size=30}Сумасшествие"  color "#ffff00" 
                elif attackindex == "Псих":
                    text"{font=determination.otf}{size=30}Псих"  color "#ffff00" 
                elif attackindex == "Моральное разложение":
                    text"{font=determination.otf}{size=30}Моральное разложение"  color "#ffff00" 
                elif attackindex == "Пробуждение прошлого":
                    text"{font=determination.otf}{size=30}Пробуждение прошлого"  color "#ffff00" 
                    
                # Фриск - Атаки (0, 48)
                elif attackindex == "Para bellum":
                    text"{font=determination.otf}{size=30}Para bellum"  color "#ffff00"
                    
                # Фриск - Магия (49-53)
                elif attackindex == "Potentia intellectus":
                    text"{font=determination.otf}{size=30}Potentia intellectus"  color "#ffff00" 
                elif attackindex == "Quod licet Iovi, non licet bovi":
                    text"{font=determination.otf}{size=30}Quod licet Iovi, non licet bovi"  color "#ffff00" 
                elif attackindex == "Foedus icere":
                    text"{font=determination.otf}{size=30}Foedus icere"  color "#ffff00" 
                elif attackindex == "Do ut des":
                    text"{font=determination.otf}{size=30}Do ut des"  color "#ffff00" 
                elif attackindex == "Сохранение решимости":
                    text"{font=determination.otf}{size=30}Сохранение решимости"  color "#ffff00" 
                    
                # Иззи - Магия (54-60)
                elif attackindex == "Осколок себя":
                    text"{font=determination.otf}{size=30}Осколок себя"  color "#ffff00" 
                elif attackindex == "Успокоение":
                    text"{font=determination.otf}{size=30}Успокоение"  color "#ffff00" 
                elif attackindex == "Медитация":
                    text"{font=determination.otf}{size=30}Медитация"  color "#ffff00" 
                elif attackindex == "Карма":
                    text"{font=determination.otf}{size=30}Карма"  color "#ffff00" 
                elif attackindex == "Зачарование":
                    text"{font=determination.otf}{size=30}Зачарование"  color "#ffff00" 
                elif attackindex == "Предвидение":
                    text"{font=determination.otf}{size=30}Предвидение"  color "#ffff00" 
                elif attackindex == "Пробуждение":
                    text"{font=determination.otf}{size=30}Пробуждение"  color "#ffff00" 
                    
                # Кловер - Атаки (0, 61-66)
                elif attackindex == "Навскидку":
                    text"{font=determination.otf}{size=30}Навскидку"  color "#ffff00" 
                elif attackindex == "Прицельный":
                    text"{font=determination.otf}{size=30}Прицельный"  color "#ffff00" 
                elif attackindex == "Лассо":
                    text"{font=determination.otf}{size=30}Лассо"  color "#ffff00" 
                elif attackindex == "Хлыст":
                    text"{font=determination.otf}{size=30}Хлыст"  color "#ffff00" 
                elif attackindex == "Клеймо":
                    text"{font=determination.otf}{size=30}Клеймо"  color "#ffff00" 
                elif attackindex == "Скорострел":
                    text"{font=determination.otf}{size=30}Скорострел"  color "#ffff00" 
                    
                # Кловер - Магия (67-73)
                elif attackindex == "Выбор калибра":
                    text"{font=determination.otf}{size=30}мелкий калибр"  color "#ffff00" 
                elif attackindex == "Сыграем!":
                    text"{font=determination.otf}{size=30}средний калибр"  color "#ffff00" 
                elif attackindex == "Помиловать":
                    text"{font=determination.otf}{size=30}крупный калибр"  color "#ffff00" 
                elif attackindex == "Длинный ствол":
                    text"{font=determination.otf}{size=30}длинный ствол"  color "#ffff00" 
                elif attackindex == "Суд":
                    text"{font=determination.otf}{size=30}Суд"  color "#ffff00"
                elif attackindex == "Дикий запад, Крошка!":
                    text"{font=determination.otf}{size=30}Дикий запад, Крошка!"  color "#ffff00" 
                elif attackindex == "Гиперлуч":
                    text"{font=determination.otf}{size=30}уровень-геноцид"  color "#ffff00" 
                    
                # Седрик - Атаки (0, 74-75)
                elif attackindex == "Удар сковородкой":
                    text"{font=determination.otf}{size=30}Удар сковородкой"  color "#ffff00" 
                elif attackindex == "Пощёчина от шефа":
                    text"{font=determination.otf}{size=30}Пощёчина от шефа"  color "#ffff00" 
                    
                # Седрик - Магия (76-85)
                elif attackindex == "Сбегать за продуктами":
                    text"{font=determination.otf}{size=30}Сбегать за продуктами"  color "#ffff00" 
                elif attackindex == "Яичница на завтрак":
                    text"{font=determination.otf}{size=30}Яичница на завтрак"  color "#ffff00" 
                elif attackindex == "Булочка":
                    text"{font=determination.otf}{size=30}Булочка"  color "#ffff00" 
                elif attackindex == "Салат Цезарь":
                    text"{font=determination.otf}{size=30}салат Цезарь"  color "#ffff00" 
                elif attackindex == "Сэндвич":
                    text"{font=determination.otf}{size=30}Сэндвич"  color "#ffff00" 
                elif attackindex == "Блинчики с кленовым сиропом":
                    text"{font=determination.otf}{size=30}Блинчики с кленовым сиропом"  color "#ffff00" 
                elif attackindex == "Чизбургер":
                    text"{font=determination.otf}{size=30}Чизбургер"  color "#ffff00" 
                elif attackindex == "Суши":
                    text"{font=determination.otf}{size=30}Суши"  color "#ffff00" 
                elif attackindex == "Мясо на гриле":
                    text"{font=determination.otf}{size=30}Мясо на гриле"  color "#ffff00" 
                elif attackindex == "Пицца!":
                    text"{font=determination.otf}{size=30}Пицца!"  color "#ffff00" 
                    
                # Атаки врагов (86-90)
                elif attackindex == "Атака Джевила":
                    text"{font=determination.otf}{size=30}Атака Джевила"  color "#ffff00" 
                elif attackindex == "Атака Арчи":
                    text"{font=determination.otf}{size=30}Атака Арчи"  color "#ffff00" 
                elif attackindex == "Атака Тревора":
                    text"{font=determination.otf}{size=30}Атака Тревора"  color "#ffff00" 
                elif attackindex == "Атака Психолога":
                    text"{font=determination.otf}{size=30}Атака Психолога"  color "#ffff00" 
                elif attackindex == "Атака Спамтона":
                    text"{font=determination.otf}{size=30}Атака Спамтона"  color "#ffff00" 
                
                elif isinstance(attackindex, str) and (attackindex.startswith("wep_") or attackindex.startswith("food_") ):
                    text "{font=determination.otf}{size=30}[inv_item_name]{/size}{/font}" color "#ffff00" xalign 0.5 text_align 0.5 xmaximum 250
                else:
                    #text"{font=determination.otf}{size=30}[inv_item_name]"  color "#ffff00"
                    text"{font=determination.otf}{size=30}[attackindex]"  color "#ffff00"                  





    frame:
        background "#ffff00"          # белая рамка
        padding (7, 7, 5, 5)        # толщина рамки

        at targetinfoapp
        xsize 280
        ysize 56

        frame:
            xsize 274
            ysize 50
            background "#000000"     # чёрный фон внутри
            #xpadding 10
            #ypadding 10
            xalign 0.5
            yalign 0.5

            vbox:
                xalign 0.5
                yalign 0.5
                if target is None:
                    text"{font=determination.otf}{size=30}---"  color "#ffff00" 
                else:
                    text"{font=determination.otf}{size=30}[target.name]" color "#ffff00" 
###############################################################################################################______ПЕРЕКЛЮЧАТЕЛИ____________######################################################################################################################################################################












################# _________________________________ИНДИВИДУАЛЬНЫЕ КНОПКИ___________________##################

image fight_kris_mech_back:
    "fight_kris_mech_back1.png"
    pause 0.06411
    "fight_kris_mech_back2.png"
    pause 0.06411
    "fight_kris_mech_back3.png"
    pause 0.06411
    "fight_kris_mech_back4.png"
    pause 0.06411
    "fight_kris_mech_back5.png"
    pause 0.06411
    "fight_kris_mech_back6.png"
    pause 0.06411
    "fight_kris_mech_back7.png"
    pause 0.06411
    "fight_kris_mech_back8.png"
    pause 0.06411
    "fight_kris_mech_back9.png"
    pause 0.06411
    "fight_kris_mech_back10.png"
    pause 0.06411
    "fight_kris_mech_back11.png"
    pause 0.06411
    "fight_kris_mech_back12.png"
    pause 0.06411
    "fight_kris_mech_back13.png"
    pause 0.06411
    "fight_kris_mech_back14.png"
    pause 0.06411
    "fight_kris_mech_back15.png"
    pause 0.06411
    "fight_kris_mech_back16.png"
    pause 0.06411
    "fight_kris_mech_back17.png"
    pause 0.06411
    


image fight_kris_shit_back:
    "fight_kris_shit_back1.png"
    pause 0.06412
    "fight_kris_shit_back2.png"
    pause 0.06412
    "fight_kris_shit_back3.png"
    pause 0.06412
    "fight_kris_shit_back4.png"
    pause 0.06412
    "fight_kris_shit_back5.png"
    pause 0.06412
    "fight_kris_shit_back6.png"
    pause 0.06412
    "fight_kris_shit_back7.png"
    pause 0.06412
    "fight_kris_shit_back8.png"
    pause 0.06412
    "fight_kris_shit_back9.png"
    pause 0.06412
    "fight_kris_shit_back10.png"
    pause 0.06412
    "fight_kris_shit_back11.png"
    pause 0.06412
    "fight_kris_shit_back12.png"
    pause 0.06412
    "fight_kris_shit_back13.png"
    pause 0.06412
    "fight_kris_shit_back14.png"
    pause 0.06412
    "fight_kris_shit_back15.png"
    pause 0.06412
    "fight_kris_shit_back16.png"
    pause 0.06412
    "fight_kris_shit_back17.png"
    pause 0.06412
    



image fight_kris_up_back:
    "fight_kris_up_back1.png"
    pause 0.06413
    "fight_kris_up_back2.png"
    pause 0.06413
    "fight_kris_up_back3.png"
    pause 0.06413
    "fight_kris_up_back4.png"
    pause 0.06413
    "fight_kris_up_back5.png"
    pause 0.06413
    "fight_kris_up_back6.png"
    pause 0.06413
    "fight_kris_up_back7.png"
    pause 0.06413
    "fight_kris_up_back8.png"
    pause 0.06413
    "fight_kris_up_back9.png"
    pause 0.06413
    "fight_kris_up_back10.png"
    pause 0.06413
    "fight_kris_up_back11.png"
    pause 0.06413
    "fight_kris_up_back12.png"
    pause 0.06413
    "fight_kris_up_back13.png"
    pause 0.06413
    "fight_kris_up_back14.png"
    pause 0.06413
    "fight_kris_up_back15.png"
    pause 0.06413
    "fight_kris_up_back16.png"
    pause 0.06413
    "fight_kris_up_back17.png"
    pause 0.06413
    



image fight_kris_down_back:
    "fight_kris_down_back1.png"
    pause 0.06414
    "fight_kris_down_back2.png"
    pause 0.06414
    "fight_kris_down_back3.png"
    pause 0.06414
    "fight_kris_down_back4.png"
    pause 0.06414
    "fight_kris_down_back5.png"
    pause 0.06414
    "fight_kris_down_back6.png"
    pause 0.06414
    "fight_kris_down_back7.png"
    pause 0.06414
    "fight_kris_down_back8.png"
    pause 0.06414
    "fight_kris_down_back9.png"
    pause 0.06414
    "fight_kris_down_back10.png"
    pause 0.06414
    "fight_kris_down_back11.png"
    pause 0.06414
    "fight_kris_down_back12.png"
    pause 0.06414
    "fight_kris_down_back13.png"
    pause 0.06414
    "fight_kris_down_back14.png"
    pause 0.06414
    "fight_kris_down_back15.png"
    pause 0.06414
    "fight_kris_down_back16.png"
    pause 0.06414
    "fight_kris_down_back17.png"
    pause 0.06414
    



image fight_kris_shit:
    "fight_kris_shit1.png"
    pause 0.06415
    "fight_kris_shit2.png"
    pause 0.06415
    "fight_kris_shit3.png"
    pause 0.06415
    "fight_kris_shit4.png"
    pause 0.06415
    "fight_kris_shit5.png"
    pause 0.06415
    "fight_kris_shit6.png"
    pause 0.06415
    "fight_kris_shit7.png"
    pause 0.06415
    "fight_kris_shit8.png"
    pause 0.06415
    "fight_kris_shit9.png"
    pause 0.06415
    "fight_kris_shit10.png"
    pause 0.06415
    "fight_kris_shit11.png"
    pause 0.06415
    "fight_kris_shit12.png"
    pause 0.06415
    "fight_kris_shit13.png"
    pause 0.06415
    "fight_kris_shit14.png"
    pause 0.06415
    "fight_kris_shit15.png"
    pause 0.06415
    "fight_kris_shit16.png"
    pause 0.06415
    "fight_kris_shit17.png"
    pause 0.06415


image fight_kris_mech:
    "fight_kris_mech1.png"
    pause 0.064116
    "fight_kris_mech2.png"
    pause 0.064116
    "fight_kris_mech3.png"
    pause 0.064116
    "fight_kris_mech4.png"
    pause 0.064116
    "fight_kris_mech5.png"
    pause 0.064116
    "fight_kris_mech6.png"
    pause 0.064116
    "fight_kris_mech7.png"
    pause 0.064116
    "fight_kris_mech8.png"
    pause 0.064116
    "fight_kris_mech9.png"
    pause 0.064116
    "fight_kris_mech10.png"
    pause 0.064116
    "fight_kris_mech11.png"
    pause 0.064116
    "fight_kris_mech12.png"
    pause 0.064116
    "fight_kris_mech13.png"
    pause 0.064116
    "fight_kris_mech14.png"
    pause 0.064116
    "fight_kris_mech15.png"
    pause 0.064116
    "fight_kris_mech16.png"
    pause 0.064116
    "fight_kris_mech17.png"
    



image fight_kris_up:
    "fight_kris_up1.png"
    pause 0.1005064117
    "fight_kris_up2.png"
    pause 0.064117
    "fight_kris_up3.png"
    pause 0.064117
    "fight_kris_up4.png"
    pause 0.064117
    "fight_kris_up5.png"
    pause 0.064117
    "fight_kris_up6.png"
    pause 0.064117
    "fight_kris_up7.png"
    pause 0.064117
    "fight_kris_up8.png"
    pause 0.064117
    "fight_kris_up9.png"
    pause 0.064117
    "fight_kris_up10.png"
    pause 0.064117
    "fight_kris_up11.png"
    pause 0.064117
    "fight_kris_up12.png"
    pause 0.064117
    "fight_kris_up13.png"
    pause 0.064117
    "fight_kris_up14.png"
    pause 0.064117
    "fight_kris_up15.png"
    pause 0.064117
    "fight_kris_up16.png"
    pause 0.064117
    "fight_kris_up17.png"
    pause 0.064117
    



image fight_kris_down:
    "fight_kris_down1.png"
    pause 0.10064118
    "fight_kris_down2.png"
    pause 0.064118
    "fight_kris_down3.png"
    pause 0.064118
    "fight_kris_down4.png"
    pause 0.064118
    "fight_kris_down5.png"
    pause 0.064118
    "fight_kris_down6.png"
    pause 0.064118
    "fight_kris_down7.png"
    pause 0.064118
    "fight_kris_down8.png"
    pause 0.064118
    "fight_kris_down9.png"
    pause 0.064118
    "fight_kris_down10.png"
    pause 0.064118
    "fight_kris_down11.png"
    pause 0.064118
    "fight_kris_down12.png"
    pause 0.064118
    "fight_kris_down13.png"
    pause 0.064118
    "fight_kris_down14.png"
    pause 0.064118
    "fight_kris_down15.png"
    pause 0.064118
    "fight_kris_down16.png"
    pause 0.064118
    "fight_kris_down17.png"
    pause 0.064118
    











    # 1. Kris magic up tob (пауза 0.064003101)
image Kris_magic_up_tob:
    "Kris_magic_up_tob1.png"
    pause 0.064003101
    "Kris_magic_up_tob2.png"
    pause 0.064003101
    "Kris_magic_up_tob3.png"
    pause 0.064003101
    "Kris_magic_up_tob4.png"
    pause 0.064003101
    "Kris_magic_up_tob5.png"
    pause 0.064003101
    "Kris_magic_up_tob6.png"
    pause 0.064003101
    "Kris_magic_up_tob7.png"
    pause 0.064003101
    "Kris_magic_up_tob8.png"
    pause 0.064003101
    "Kris_magic_up_tob9.png"
    pause 0.064003101
    "Kris_magic_up_tob10.png"
    pause 0.064003101
    "Kris_magic_up_tob11.png"
    pause 0.064003101
    "Kris_magic_up_tob12.png"
    pause 0.064003101
    "Kris_magic_up_tob13.png"
    pause 0.064003101
    "Kris_magic_up_tob14.png"
    pause 0.064003101
    "Kris_magic_up_tob15.png"
    pause 0.064003101
    "Kris_magic_up_tob16.png"
    pause 0.064003101
    "Kris_magic_up_tob17.png"
    pause 0.064003101
    

# 2. Kris magic down tob (пауза 0.064003102)
image Kris_magic_down_tob:
    "Kris_magic_down_tob1.png"
    pause 0.064003102
    "Kris_magic_down_tob2.png"
    pause 0.064003102
    "Kris_magic_down_tob3.png"
    pause 0.064003102
    "Kris_magic_down_tob4.png"
    pause 0.064003102
    "Kris_magic_down_tob5.png"
    pause 0.064003102
    "Kris_magic_down_tob6.png"
    pause 0.064003102
    "Kris_magic_down_tob7.png"
    pause 0.064003102
    "Kris_magic_down_tob8.png"
    pause 0.064003102
    "Kris_magic_down_tob9.png"
    pause 0.064003102
    "Kris_magic_down_tob10.png"
    pause 0.064003102
    "Kris_magic_down_tob11.png"
    pause 0.064003102
    "Kris_magic_down_tob12.png"
    pause 0.064003102
    "Kris_magic_down_tob13.png"
    pause 0.064003102
    "Kris_magic_down_tob14.png"
    pause 0.064003102
    "Kris_magic_down_tob15.png"
    pause 0.064003102
    "Kris_magic_down_tob16.png"
    pause 0.064003102
    "Kris_magic_down_tob17.png"
    pause 0.064003102
    

# 3. Kris magic up toc (пауза 0.064003103)
image Kris_magic_up_toc:
    "Kris_magic_up_toc1.png"
    pause 0.064003103
    "Kris_magic_up_toc2.png"
    pause 0.064003103
    "Kris_magic_up_toc3.png"
    pause 0.064003103
    "Kris_magic_up_toc4.png"
    pause 0.064003103
    "Kris_magic_up_toc5.png"
    pause 0.064003103
    "Kris_magic_up_toc6.png"
    pause 0.064003103
    "Kris_magic_up_toc7.png"
    pause 0.064003103
    "Kris_magic_up_toc8.png"
    pause 0.064003103
    "Kris_magic_up_toc9.png"
    pause 0.064003103
    "Kris_magic_up_toc10.png"
    pause 0.064003103
    "Kris_magic_up_toc11.png"
    pause 0.064003103
    "Kris_magic_up_toc12.png"
    pause 0.064003103
    "Kris_magic_up_toc13.png"
    pause 0.064003103
    "Kris_magic_up_toc14.png"
    pause 0.064003103
    "Kris_magic_up_toc15.png"
    pause 0.064003103
    "Kris_magic_up_toc16.png"
    pause 0.064003103
    "Kris_magic_up_toc17.png"
    pause 0.064003103
    

# 4. Kris magic down toc (пауза 0.045003104)
image Kris_magic_down_toc:
    "Kris_magic_down_toc1.png"
    pause 0.045003104
    "Kris_magic_down_toc2.png"
    pause 0.045003104
    "Kris_magic_down_toc3.png"
    pause 0.045003104
    "Kris_magic_down_toc4.png"
    pause 0.045003104
    "Kris_magic_down_toc5.png"
    pause 0.045003104
    "Kris_magic_down_toc6.png"
    pause 0.045003104
    "Kris_magic_down_toc7.png"
    pause 0.045003104
    "Kris_magic_down_toc8.png"
    pause 0.045003104
    "Kris_magic_down_toc9.png"
    pause 0.045003104
    "Kris_magic_down_toc10.png"
    pause 0.045003104
    "Kris_magic_down_toc11.png"
    pause 0.045003104
    "Kris_magic_down_toc12.png"
    pause 0.045003104
    "Kris_magic_down_toc13.png"
    pause 0.045003104
    "Kris_magic_down_toc14.png"
    pause 0.045003104
    "Kris_magic_down_toc15.png"
    pause 0.045003104
    "Kris_magic_down_toc16.png"
    pause 0.045003104
    "Kris_magic_down_toc17.png"
    pause 0.045003104
    




# 1. Kris act up tob (пауза 0.064002101)
image Kris_act_up_tob:
    "Kris_act_up_tob1.png"
    pause 0.064002101
    "Kris_act_up_tob2.png"
    pause 0.064002101
    "Kris_act_up_tob3.png"
    pause 0.064002101
    "Kris_act_up_tob4.png"
    pause 0.064002101
    "Kris_act_up_tob5.png"
    pause 0.064002101
    "Kris_act_up_tob6.png"
    pause 0.064002101
    "Kris_act_up_tob7.png"
    pause 0.064002101
    "Kris_act_up_tob8.png"
    pause 0.064002101
    "Kris_act_up_tob9.png"
    pause 0.064002101
    "Kris_act_up_tob10.png"
    pause 0.064002101
    "Kris_act_up_tob11.png"
    pause 0.064002101
    "Kris_act_up_tob12.png"
    pause 0.064002101
    "Kris_act_up_tob13.png"
    pause 0.064002101
    "Kris_act_up_tob14.png"
    pause 0.064002101
    "Kris_act_up_tob15.png"
    pause 0.064002101
    "Kris_act_up_tob16.png"
    pause 0.064002101
    "Kris_act_up_tob17.png"
    pause 0.064002101
    

# 2. Kris act down tob (пауза 0.064002102)
image Kris_act_down_tob:
    "Kris_act_down_tob1.png"
    pause 0.064002102
    "Kris_act_down_tob2.png"
    pause 0.064002102
    "Kris_act_down_tob3.png"
    pause 0.064002102
    "Kris_act_down_tob4.png"
    pause 0.064002102
    "Kris_act_down_tob5.png"
    pause 0.064002102
    "Kris_act_down_tob6.png"
    pause 0.064002102
    "Kris_act_down_tob7.png"
    pause 0.064002102
    "Kris_act_down_tob8.png"
    pause 0.064002102
    "Kris_act_down_tob9.png"
    pause 0.064002102
    "Kris_act_down_tob10.png"
    pause 0.064002102
    "Kris_act_down_tob11.png"
    pause 0.064002102
    "Kris_act_down_tob12.png"
    pause 0.064002102
    "Kris_act_down_tob13.png"
    pause 0.064002102
    "Kris_act_down_tob14.png"
    pause 0.064002102
    "Kris_act_down_tob15.png"
    pause 0.064002102
    "Kris_act_down_tob16.png"
    pause 0.064002102
    "Kris_act_down_tob17.png"
    pause 0.064002102
    

# 3. Kris act up toc (пауза 0.064002103)
image Kris_act_up_toc:
    "Kris_act_up_toc1.png"
    pause 0.274002103
    "Kris_act_up_toc2.png"
    pause 0.074002103
    "Kris_act_up_toc3.png"
    pause 0.074002103
    "Kris_act_up_toc4.png"
    pause 0.074002103
    "Kris_act_up_toc5.png"
    pause 0.074002103
    "Kris_act_up_toc6.png"
    pause 0.074002103
    "Kris_act_up_toc7.png"
    pause 0.074002103
    "Kris_act_up_toc8.png"
    pause 0.074002103
    "Kris_act_up_toc9.png"
    pause 0.074002103
    "Kris_act_up_toc10.png"
    pause 0.074002103
    "Kris_act_up_toc11.png"
    pause 0.074002103
    "Kris_act_up_toc12.png"
    pause 0.074002103
    "Kris_act_up_toc13.png"
    pause 0.074002103
    "Kris_act_up_toc14.png"
    pause 0.074002103
    "Kris_act_up_toc15.png"
    pause 0.074002103
    "Kris_act_up_toc16.png"
    pause 0.074002103
    "Kris_act_up_toc17.png"
    pause 0.074002103
    

# 4. Kris act down toc (пауза 0.064002104)
image Kris_act_down_toc:
    "Kris_act_down_toc1.png"
    pause 0.274002104
    "Kris_act_down_toc2.png"
    pause 0.074002104
    "Kris_act_down_toc3.png"
    pause 0.074002104
    "Kris_act_down_toc4.png"
    pause 0.074002104
    "Kris_act_down_toc5.png"
    pause 0.074002104
    "Kris_act_down_toc6.png"
    pause 0.074002104
    "Kris_act_down_toc7.png"
    pause 0.074002104
    "Kris_act_down_toc8.png"
    pause 0.074002104
    "Kris_act_down_toc9.png"
    pause 0.074002104
    "Kris_act_down_toc10.png"
    pause 0.074002104
    "Kris_act_down_toc11.png"
    pause 0.074002104
    "Kris_act_down_toc12.png"
    pause 0.074002104
    "Kris_act_down_toc13.png"
    pause 0.074002104
    "Kris_act_down_toc14.png"
    pause 0.074002104
    "Kris_act_down_toc15.png"
    pause 0.074002104
    "Kris_act_down_toc16.png"
    pause 0.074002104
    "Kris_act_down_toc17.png"
    pause 0.074002104
    



# Анимация 1 (набор tob)
image Kris_anim_tob:
    "Kris_item_tob1.png"
    pause 0.064004101
    "Kris_item_tob2.png"
    pause 0.064004101
    "Kris_item_tob3.png"
    pause 0.064004101
    "Kris_item_tob4.png"
    pause 0.064004101
    "Kris_item_tob5.png"
    pause 0.064004101
    "Kris_item_tob6.png"
    pause 0.064004101
    "Kris_item_tob7.png"
    pause 0.064004101
    "Kris_item_tob8.png"
    pause 0.064004101
    "Kris_item_tob9.png"
    pause 0.064004101
    "Kris_item_tob10.png"
    pause 0.064004101
    "Kris_item_tob11.png"
    pause 0.064004101
    "Kris_item_tob12.png"
    pause 0.064004101
    "Kris_item_tob13.png"
    pause 0.064004101
    "Kris_item_tob14.png"
    pause 0.064004101
    "Kris_item_tob15.png"
    pause 0.064004101
    "Kris_item_tob16.png"
    pause 0.064004101
    "Kris_item_tob17.png"
    pause 0.064004101   # последняя пауза – анимация останавливается на этом кадре

# Анимация 2 (набор toc)
image Kris_anim_toc:
    "Kris_item_toc1.png"
    pause 0.064004102
    "Kris_item_toc2.png"
    pause 0.064004102
    "Kris_item_toc3.png"
    pause 0.064004102
    "Kris_item_toc4.png"
    pause 0.064004102
    "Kris_item_toc5.png"
    pause 0.064004102
    "Kris_item_toc6.png"
    pause 0.064004102
    "Kris_item_toc7.png"
    pause 0.064004102
    "Kris_item_toc8.png"
    pause 0.064004102
    "Kris_item_toc9.png"
    pause 0.064004102
    "Kris_item_toc10.png"
    pause 0.064004102
    "Kris_item_toc11.png"
    pause 0.064004102
    "Kris_item_toc12.png"
    pause 0.064004102
    "Kris_item_toc13.png"
    pause 0.064004102
    "Kris_item_toc14.png"
    pause 0.064004102
    "Kris_item_toc15.png"
    pause 0.064004102
    "Kris_item_toc16.png"
    pause 0.064004102
    "Kris_item_toc17.png"
    pause 0.064004102
