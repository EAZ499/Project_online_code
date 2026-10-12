#       @@        @@@  @@@@@@@           @@@@@@       @@   @@@@@          @@@@@@      @@@@@@@@@@     
#       @@@      @@@   @@@@@@@@@@@     @@@@@@@@@@     @@@@@@@@@@@@      @@@@@@@@@@   @@@@@@@@@@@     
#       @@@      @@@   @@@     @@@   @@@@      @@@    @@@@      @@@   @@@@      @@@@     @@@         
#        @@@    @@@    @@@    @@@@   @@@        @@@   @@@        @@@  @@@        @@@     @@@         
#         @@@  @@@     @@@@@@@@@@    @@@        @@@   @@@        @@@ @@@@        @@@     @@@         
#         @@@  @@@     @@@     @@@   @@@        @@@   @@@       @@@   @@@        @@@     @@@         
#          @@@@@@      @@@      @@@  @@@@      @@@@   @@@@      @@@   @@@@      @@@@     @@@         
#           @@@@       @@@@@@@@@@@    @@@@@@@@@@@     @@@@@@@@@@@@     @@@@@@@@@@@       @@@         
#           @@@@       @@@@@@@@          @@@@@@       @@@ @@@@@@          @@@@@@         @@@         
#           @@@                                       @@@                                            
#         @@@@                                        @@@                                            
#       @@@@@                                         @@@                                            
                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                    
                                                                                                  
                                                                                                    
#        @@@@        @@@@    @@@          @@@    @@@     @@@     @@    @@@    @@@@   @@@      @@@@   
#        @@@@@      @@@@@    @@@          @@@    @@@     @@@     @@    @@@   @@@@    @@@     @@@@@   
#        @@@@@@    @@@@@@    @@@          @@@    @@@     @@@     @@    @@@ @@@@      @@@   @@@@@@@   
#        @@@ @@    @@ @@@    @@@@@@@@@@   @@@    @@@     @@@     @@    @@@@@@        @@@  @@@@ @@@   
#        @@@ @@@  @@@ @@@    @@@    @@@@  @@@    @@@     @@@     @@    @@@@@@@       @@@ @@@   @@@   
#        @@@  @@@@@@  @@@    @@@     @@@  @@@    @@@     @@@     @@    @@@  @@@@     @@@@@@    @@@   
#        @@@   @@@@   @@@    @@@   @@@@@  @@@    @@@     @@@     @@    @@@   @@@@@   @@@@@     @@@   
#        @@@   @@@@   @@@    @@@@@@@@@    @@@    @@@@@@@@@@@@@@@@@@    @@@     @@@@  @@@       @@@   
                                                                                                    



#                                                                                           Стиль мышки/Стиль курсора/Настройки курсора
default default_mouse = "default"
$ default_mouse = "default"
#Душа повреждённая
define dushadamaged = Movie(play="images/dushadamaged.avi", size=(40, 40), loop=1)
#Конфиги мыши. Конфиги курсора
define config.mouse = { }
define config.mouse['default0'] = [ ( "coursor0.png", 0, 0) ]
define config.mouse['default'] = [ ( "coursor1.png", 0, 0) ]
define config.mouse['default2'] = [ ( "heart1.png", 16, 16) ]
define config.mouse['damaged'] = [
    ( "heart1.png", 16, 16),
    ( "heart1.png", 16, 16),
    ( "heart2.png", 16, 16),
    ( "heart2.png", 16, 16),
]

#define config.mouse['damaged'] = Animation("heart1.png", 0.15, "heart2.png", 0.15, repeat=True)
#define config.mouse['Null'] = [("Nullcursor.png", 16, 16 )]
define config.mouse['Null'] = [("heart1.png", 16, 16 )]
#heart1.png



#                                                                       Переменные для пеоложения рамок и их размеров
default screenxpos = 515
default screenypos = 240
default xbord      = 250
default ybord      = 250
default borderthick= 10

default souloutrange = 0

# Переменные для отслеживания движения
default moving_up2 = False
default moving_down2 = False
default moving_left2 = False
default moving_right2 = False
default soul_speed = 6  # Скорость движения в пикселях за шаг
default keyboard_control = False  # Флаг управления с клавиатуры


default attack_mouse_x = 640
default attack_mouse_y = 360
default attack_mouse_initialized = False
default enemymonster = None
default move_step = 0.0

init -999 python:
    # Максимальный приоритет - отключаем ВСЕ стандартные функции
    config.keymap['focus_up'] = []
    config.keymap['focus_down'] = []
    config.keymap['focus_left'] = []
    config.keymap['focus_right'] = []
    config.keymap['screenshot'] = []
    config.keymap['toggle_fullscreen'] = []
    config.keymap['toggle_music'] = []
    config.keymap['toggle_sound'] = []
    
    # Восстанавливаем КЛИК МЫШЬЮ и навигацию UI
    config.keymap['dismiss'] = ['K_SPACE', 'K_RETURN', 'mouseup_1']  # ← ДОБАВИЛИ mouseup_1 (клик мышью)
    config.keymap['game_menu'] = ['K_ESCAPE']

init python:

    # Инициализация player_collider, если он еще не инициализирован
    if not hasattr(store, 'player_collider') or store.player_collider is None:
        if hasattr(store, 'GameObject'):
            store.player_collider = store.GameObject(0, 64, 32, 32, None, solid=True)

    def clamp_soul_speed(value):
        return max(7, min(13, value))

    def clamp_enemy_speed(value):
        return max(0.7, min(1.3, value))

    def move_axis(pos, low, high, low_fix, high_fix,
                move_negative, move_positive,
                negative_speed, positive_speed, idle_speed):
        if pos > high:
            store.souloutrange = 1
            return high - high_fix

        if pos < low:
            store.souloutrange = 1
            return low + low_fix

        if move_negative:
            return pos - negative_speed * store.soul_speed * 0.025 * 1.3

        if move_positive:
            return pos + positive_speed * store.soul_speed * 0.025 * 1.3

        return pos + idle_speed

    def set_move2(direction, is_pressed):
        """
        Устанавливает или отменяет флаг движения в указанном направлении.
        
        Args:
            direction: "moving_up", "moving_down", "moving_left", "moving_right"
            is_pressed: True (клавиша нажата) или False (клавиша отпущена)
        """
        if hasattr(store, direction):
            setattr(store, direction, is_pressed)
        
        # Устанавливаем флаг управления с клавиатуры
        store.keyboard_control = any((
            store.moving_up2,
            store.moving_down2,
            store.moving_left2,
            store.moving_right2,
        ))

    def sync_attack_mouse_position():
        mx, my = renpy.get_mouse_pos()
        store.attack_mouse_x = mx
        store.attack_mouse_y = my
        store.attack_mouse_initialized = True


    def master_timer_logic(st, at):
        """
        Единый DynamicDisplayable, заменяющий timer'ы в mouse_restricted_area.
        • st: время, прошедшее с момента показа экрана.
        • at: время, прошедшее с момента последней отрисовки.
        """
        # 1. Обновление позиции мыши (вызываем каждый кадр для максимальной плавности)
        if hasattr(store, 'update_soul_position'):
            store.update_soul_position()
            
        # 2. Симуляция клика (эмулируем timer 0.05)
        if not hasattr(store, '_master_last_click'):
            store._master_last_click = st
            
        if st - store._master_last_click >= 0.05:
            if hasattr(store, 'click_soul'):
                store.click_soul()
            store._master_last_click = st
            
        # Возвращаем невидимый Null и задержку 0.01 сек (для отзывчивости UI)
        return Null(), 0.016


init python:
    # --- БЫСТРЫЕ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ (вне store) ---
    # Инициализируем их один раз при старте
    _soul_physics_active = False
    _soul_mx = 640.0
    _soul_my = 360.0
    _soul_initialized = False
    
    # Флаги движения (локальные, доступ к ним мгновенный)
    _move_up = False
    _move_down = False
    _move_left = False
    _move_right = False
    
    # Таймер для клика
    _last_click_time = 0.0
    # Глобальные переменные для фиксированного timestep
    _physics_accumulator = 0.0
    _fixed_dt = 1.0 / 60.0  # 60 обновлений физики в секунду

    def sync_soul_pos():
        """Синхронизирует внутренние координаты с реальной мышью"""
        global _soul_mx, _soul_my, _soul_initialized
        mx, my = renpy.get_mouse_pos()
        _soul_mx = float(mx)
        _soul_my = float(my)
        _soul_initialized = True



    def reset_soul_state():
        """
        Полная остановка физики души и очистка ВСЕХ координат.
        Вызывать ПЕРЕД force_release_mouse().
        """
        global _soul_initialized, _soul_physics_active
        global _soul_mx, _soul_my
        global _move_up, _move_down, _move_left, _move_right
        global _physics_accumulator, _last_click_time
        
        # Останавливаем физику ПЕРВЫМ ДЕЛОМ
        _soul_physics_active = False
        _soul_initialized = False
        
        # Очищаем координаты
        _soul_mx = 640.0
        _soul_my = 360.0
        
        # Сбрасываем флаги движения
        _move_up = False
        _move_down = False
        _move_left = False
        _move_right = False
        
        # КРИТИЧНО: Сбрасываем аккумулятор физики
        _physics_accumulator = 0.0
        _last_click_time = 0.0
        
        # Очищаем сохранённые координаты атаки
        store.attack_mouse_x = 640
        store.attack_mouse_y = 360
        store.attack_mouse_initialized = False



    def activate_soul_physics():
        """Активирует физику души при начале фазы уворота."""
        global _soul_physics_active, _soul_initialized, _physics_accumulator
        
        _soul_physics_active = True
        _soul_initialized = False
        _physics_accumulator = 0.0





    def set_move_flag(direction, is_pressed):
        """Быстрая установка флагов движения"""
        global _move_up, _move_down, _move_left, _move_right
        if direction == "up": _move_up = is_pressed
        elif direction == "down": _move_down = is_pressed
        elif direction == "left": _move_left = is_pressed
        elif direction == "right": _move_right = is_pressed
        
        # Синхронизируем флаг keyboard_control в store для совместимости с другими системами
        store.keyboard_control = _move_up or _move_down or _move_left or _move_right



    def update_soul_physics(at):
        global _soul_mx, _soul_my, _soul_initialized
        global _physics_accumulator, _fixed_dt, _soul_physics_active
        
        # Защита: если физика остановлена — не делаем ничего
        if not _soul_physics_active:
            return
        
        if not _soul_initialized:
            sync_soul_pos()
            return

        # Уменьшенная защита от телепортации: 0.05 сек вместо 0.25
        # Это максимум 3 кадра физики, что предотвращает прыжки
        if at > 0.25:
            at = 0.25

        _physics_accumulator += at

        left = store.screenxpos
        top = store.screenypos
        right = left + store.xbord - 4
        bottom = top + store.ybord - 5
        
        move_step = store.soul_speed * 0.02#0.02
        store.move_step = move_step
        
        dx = 0.0
        dy = 0.0
        
        if _move_up: dy -= 1.0
        if _move_down: dy += 1.0
        if _move_left: dx -= 1.0
        if _move_right: dx += 1.0
        
        length = (dx*dx + dy*dy) ** 0.5
        if length > 0:
            dx = (dx / length) * move_step
            dy = (dy / length) * move_step

        while _physics_accumulator >= _fixed_dt:
            _soul_mx += dx
            _soul_my += dy
            
            if _soul_mx < left: _soul_mx = left
            elif _soul_mx > right: _soul_mx = right
            
            if _soul_my < top: _soul_my = top
            elif _soul_my > bottom: _soul_my = bottom
            
            _physics_accumulator -= _fixed_dt

        target_x = int(_soul_mx)
        target_y = int(_soul_my)
        
        store.attack_mouse_x = target_x
        store.attack_mouse_y = target_y
        
        renpy.set_mouse_pos(target_x, target_y)










    def click_soul_fast(st):
        """Симуляция клика. Вызывается внутри DynamicDisplayable."""
        global _last_click_time
        
        # Эмуляция таймера 0.1 сек
        if st - _last_click_time >= 0.1:
            mx = int(_soul_mx)
            my = int(_soul_my)
            
            # Создаем событие Pygame
            pygame.event.post(pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, 
                {'pos': (mx, my), 'button': 1}
            ))
            _last_click_time = st

    def soul_master_logic(st, at):
        """Единая точка входа для обновления каждый кадр"""
        update_soul_physics(at)
        # Если физика остановлена — не делаем ничего
        if not _soul_physics_active:
            return Null(), 1.0  # Редкий опрос, чтобы не грузить

        click_soul_fast(st)
        
        # Возвращаем Null и просим перерисовать через 0.016 сек (60 FPS)
        return Null(), 0.008

    # Экспорт функций для использования в экране
    globals()['set_move_flag'] = set_move_flag
    globals()['soul_master_logic'] = soul_master_logic





init python:
    # Глобальный флаг: активна ли физика души
    _soul_physics_active = False


    def force_release_mouse():
        """
        Освобождает мышь от перехвата боевой системой.
        Вызывается ПОСЛЕ reset_soul_state().
        """
        global _soul_physics_active
        
        # Фиксируем позицию ДО любых изменений
        current_mx, current_my = renpy.get_mouse_pos()
        
        # Гарантируем остановку физики
        _soul_physics_active = False
        
        # Скрываем экран уворота
        renpy.hide_screen("mouse_restricted_area")
        
        # Сбрасываем флаги
        store.keyboard_control = False
        store.soul_keyboard_moving = False
        store.moving_up2 = False
        store.moving_down2 = False
        store.moving_left2 = False
        store.moving_right2 = False
        
        # Удаляем границы
        if hasattr(store, 'remove_borders'):
            store.remove_borders()
        if hasattr(store, 'remove_attack_borders'):
            store.remove_attack_borders()
        
        # Восстанавливаем курсор
        store.default_mouse = "default"
        
        # Восстанавливаем keymap
        config.keymap['screenshot'] = ['K_s']
        config.keymap['focus_up'] = ['K_UP', 'K_w']
        config.keymap['focus_down'] = ['K_DOWN', 'K_s']
        
        # Устанавливаем мышь в зафиксированную позицию
        renpy.set_mouse_pos(current_mx, current_my)
        
        # Перезапускаем взаимодействие
        renpy.restart_interaction()




    def activate_soul_physics():
        """Активирует физику души при начале фазы уворота."""
        global _soul_physics_active, _soul_initialized
        
        _soul_physics_active = True
        _soul_initialized = False  # Заставит sync_soul_pos() прочитать реальную позицию мыши





    #def update_soul_position():
    #    """Обновляет позицию сердца (БЕЗ рекурсии!)"""
    #    if not store.attack_mouse_initialized:
    #        sync_attack_mouse_position()

    #    mx = store.attack_mouse_x
    #    my = store.attack_mouse_y
        
        ## Проверяем переменные
        #if not (hasattr(store, 'screenxpos') and hasattr(store, 'screenypos') and
        #        hasattr(store, 'xbord') and hasattr(store, 'ybord')):
        #    return
            
        #if not (hasattr(store, 'moving_up2') and hasattr(store, 'moving_down2') and
        #        hasattr(store, 'moving_left2') and hasattr(store, 'moving_right2')):
        #    return
            
        #if not hasattr(store, 'soul_speed'):
        #    store.soul_speed = 1
            
    #    left = store.screenxpos
    #    right = left + store.xbord - 4
    #    top = store.screenypos
    #    bottom = top + store.ybord - 5

        # Обработка движения по вертикали
    #    my = move_axis(
    #        my, top, bottom,
    #        1, 1,
    #        store.moving_up2, store.moving_down2,
    #        12, 12, 0#.5
    #    )

        # Обработка движения по горизонтали
    #    mx = move_axis(
    #        mx, left, right,
    #        1, 4,
    #        store.moving_left2, store.moving_right2,
    #        12, 12, 0#.5
    #    )

        # Устанавливаем позицию мыши
        #renpy.set_mouse_pos(mx, my)
        
        # Обновляем коллайдер
        #if hasattr(store, 'player_collider') and store.player_collider is not None:
        #    store.player_collider.x = mx - 16
        #    store.player_collider.y = my - 16
        


    #    store.attack_mouse_x = mx
    #    store.attack_mouse_y = my
    #    renpy.set_mouse_pos(int(mx), int(my))#,duration = 0.016)





################################################### Мышка

#transform follow_mouse:
#    xpos mouse_x  # Горизонтальная позиция мыши
#    ypos mouse_y  # Вертикальная позиция мыши
#    subpixel True  # Для плавного перемещения
#    pause 0.01     # Частота обновления (в секундах)
#    repeat         # Повторять бесконечно



#                                                                                                  Режим управления
default control = "keyboard" #или keyboard или phone
image soul = "heart1.png"




init  python:

    def follow_mouse_soul(st, at):
        """
        • Берём координаты курсора.
        • Сдвигаем коллайдер души (32×32 → −16/−16 = центр).
        • Возвращаем спрайт 'soul' в ту же позицию.
        """
        mx, my = renpy.get_mouse_pos()

        # Обновляем коллайдер, если он существует и нет управления с клавиатуры
        if (hasattr(store, 'player_collider') and store.player_collider is not None and
            not (hasattr(store, 'keyboard_control') and store.keyboard_control)):
            store.player_collider.x = mx - 16
            store.player_collider.y = my - 16

        return Transform("soul",
                        xpos = mx - 16,
                        ypos = my - 16), 0      # 0 → перерисовывать каждый кадр




    def white_bar_cursor(st, at):
        """
        Функция DynamicDisplayable для white_bar, которая следует за курсором.
        Использует текущие координаты мыши и обновляет их каждый кадр.
        """
        mx, my = renpy.get_mouse_pos()
        
        # Если управление с клавиатуры, используем позицию из player_collider
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            if hasattr(store, 'player_collider') and store.player_collider is not None:
                mx = store.player_collider.x + 16
                my = store.player_collider.y + 16
        
        # Создаём белый бар с центром в позиции курсора
        # xsize 20, ysize 3 - как в оригинальном трансформе
        # alpha 1.0 - полная прозрачность
        return Transform(
            Solid("#ffffff"),
            xpos=mx - 10,  # Центрируем по X (20/2 = 10)
            ypos=my - 1.5,  # Центрируем по Y (3/2 = 1.5)
            xsize=20,
            ysize=3,
            alpha=1.0
        ), 0  # 0 → перерисовывать каждый кадр
    
    def white_bar_animated(st, at, duration=2.0):
        """
        Функция DynamicDisplayable для white_bar с анимацией появления.
        Параметр duration - длительность анимации в секундах (по умолчанию 2.0).
        Анимация: xsize от 0 до 20, alpha от 0.0 до 1.0 за указанное время.
        """
        mx, my = renpy.get_mouse_pos()
        
        # Если управление с клавиатуры, используем позицию из player_collider
        if hasattr(store, 'keyboard_control') and store.keyboard_control:
            if hasattr(store, 'player_collider') and store.player_collider is not None:
                mx = store.player_collider.x + 16
                my = store.player_collider.y + 16
        
        # Вычисляем прогресс анимации на основе времени
        progress = min(st / duration, 1.0)
        
        # Анимируем xsize от 0 до 20 и alpha от 0.0 до 1.0
        current_xsize = int(20 * progress)
        current_alpha = progress
        
        # Создаём белый бар с центром в позиции курсора
        return Transform(
            Solid("#ffffff"),
            xpos=mx - current_xsize / 2,  # Центрируем по X
            ypos=my - 1.5,  # Центрируем по Y (3/2 = 1.5)
            xsize=current_xsize,
            ysize=3,
            alpha=current_alpha
        ), 0  # 0 → перерисовывать каждый кадр


transform mousetocenter:
    xpos (renpy.get_mouse_pos()[0]-16) ypos (renpy.get_mouse_pos()[1]-16)
    linear 0.3 xpos 720 ypos 360

#                                                                                                                                               Экран с областью уворота от атак    
transform savedspace_colour:
    matrixcolor TintMatrix("#ff0000")
    easeout savedspace matrixcolor TintMatrix("#ffffff")

#                                                                                                     Экран для мышки. Чтоб её возвращать                        
screen mouse_restricted_area:
    
    #$ mx, my = renpy.get_mouse_pos()

    zorder 99999
    on "show" action SetVariable("default_mouse", "default2")   # прячем системный курсор
    on "hide" action SetVariable("default_mouse", "default")# возвращаем обратно
    on "show" action Function(add_borders)
    on "hide" action Function(remove_borders)
    # Старый вариант (оставлен по просьбе):
    on "show" action [SetVariable("keyboard_control", False), SetVariable("moving_up2", False), SetVariable("moving_down2", False), SetVariable("moving_left2", False), SetVariable("moving_right2", False)]
    on "hide" action [SetVariable("keyboard_control", False), SetVariable("moving_up2", False), SetVariable("moving_down2", False), SetVariable("moving_left2", False), SetVariable("moving_right2", False)]
    #on "show" action [SetVariable("keyboard_control", False), SetVariable("moving_up", False), SetVariable("moving_down", False), SetVariable("moving_left", False), SetVariable("moving_right", False)]  # сбрасываем все флаги при показе
    #on "hide" action [SetVariable("keyboard_control", False), SetVariable("moving_up", False), SetVariable("moving_down", False), SetVariable("moving_left", False), SetVariable("moving_right", False)]  # сбрасываем все флаги при скрытии
    
    on "show" action [
        Function(activate_soul_physics),
        Function(restrict_mouse_to_area),
        SetVariable("default_mouse", "Null"),
        SetVariable("keyboard_control", False),
        SetVariable("moving_up2", False),
        SetVariable("moving_down2", False),
        SetVariable("moving_left2", False),
        SetVariable("moving_right2", False),
    ]

    on "hide" action [
        Function(reset_soul_state),
        Function(force_release_mouse),
        SetVariable("default_mouse", "default"),
        Function(remove_borders),
    ]




    # Управление (keyboard)

    #key "K_UP" action Function(set_move2, "moving_up2", True)
    #key "keyup_K_UP" action Function(set_move2, "moving_up2", False)
    #key "K_DOWN" action Function(set_move2, "moving_down2", True)
    #key "keyup_K_DOWN" action Function(set_move2, "moving_down2", False)
    #key "K_LEFT" action Function(set_move2, "moving_left2", True)
    #key "keyup_K_LEFT" action Function(set_move2, "moving_left2", False)
    #key "K_RIGHT" action Function(set_move2, "moving_right2", True)
    #key "keyup_K_RIGHT" action Function(set_move2, "moving_right2", False)

    # Управление (keyboard)
    # При нажатии устанавливаем флаг И сразу обновляем позицию
# --- УПРАВЛЕНИЕ ---
    # Теперь мы просто меняем флаги, а физика считается в master_logic
    key "K_UP" action Function(set_move_flag, "up", True)
    key "keyup_K_UP" action Function(set_move_flag, "up", False)
    
    key "K_DOWN" action Function(set_move_flag, "down", True)
    key "keyup_K_DOWN" action Function(set_move_flag, "down", False)
    
    key "K_LEFT" action Function(set_move_flag, "left", True)
    key "keyup_K_LEFT" action Function(set_move_flag, "left", False)
    
    key "K_RIGHT" action Function(set_move_flag, "right", True)
    key "keyup_K_RIGHT" action Function(set_move_flag, "right", False)

    # --- ГЛАВНЫЙ ДВИГАТЕЛЬ ---
    # Вместо множества таймеров используем один DynamicDisplayable.
    # Он вызывает soul_master_logic каждый кадр (60+ раз в секунду).
    add DynamicDisplayable(soul_master_logic)




    # Старый вариант (оставлен по просьбе):
    #timer 0.017 repeat True action Function(update_soul_position)
    #timer 0.05 action Function(click_soul) repeat True


    #timer 0.015 repeat True action Function(update_soul_position)
    #timer 0.1 action Function(click_soul) repeat True

    #add DynamicDisplayable(master_timer_logic)


    #timer 0.032 action Function(click_soul) repeat True
    #timer 0.03 repeat True action Function(check_mouse_shift)


    # ПОТОМ ПОПРОБОВАТЬ ЗАМЕНИТЬ ТАЙМЕР НА ИСПОЛЬЗОВАНИЕ ФУНКЦИИ
    #timer 0.016 repeat True action Function(click_physics_object3)
    
    # Отладочная информация
    # Старый вариант (оставлен по просьбе):
    # text "up:[moving_up2] down:[moving_down2] left:[moving_left2] right:[moving_right2]" xpos 500 ypos 500
    text "up:[moving_up] down:[moving_down] left:[moving_left] right:[moving_right]" xpos 500 ypos 500
    text "keyboard_control:[keyboard_control]" xpos 500 ypos 520
    $ mx, my = renpy.get_mouse_pos()
    text "mouse: ([mx], [my])" xpos 500 ypos 540
    text "За пределами: [souloutrange]"xpos 500 ypos 560
    text "move_step [move_step]" xpos 500 ypos 580


define config.keymap['developer'] = []

init -100 python:
    config.framerate = 72

    if hasattr(config, "gl_vsync"):
        config.gl_vsync = True #False






# Функция для применения штрафа ко всей команде
init python:
    def apply_penalty_to_team():
        """
        Отнимает 5% HP у всех активных персонажей в команде
        """
        if store.team_manager is not None:
            for slot in store.team_manager.team_slots:
                if slot and slot in store.pers_dict:
                    char = store.pers_dict[slot]
                    if char.current_hp > 0:  # Применяем только к живым персонажам
                        damage = int(char.max_hp * 0.05)  # 5% от максимального HP
                        char.change_hp(-damage)


    # отметим рамки флажком, чтобы потом легко удалить
    def make_border(x, y, w, h):
        g = GameObject(x, y, w, h, None, solid=True)
        g.is_border = True
        return g

    def add_attack_borders():
        # если уже добавлены — ничего не делаем
        if any(getattr(o, "is_border", False) for o in store.solid_objects):
            return

        sx, sy   = store.screenxpos, store.screenypos
        w, h     = store.xbord,      store.ybord
        borders = [
            make_border(sx,       sy,       w, 5),  # верх
            make_border(sx,       sy,       5, h),  # лево
            make_border(sx,       sy + h,   w, 5),  # низ
            make_border(sx + w,   sy,       5, h),  # право
        ]
        store.solid_objects.extend(borders)

    def remove_attack_borders():
        store.solid_objects = [
            o for o in store.solid_objects
            if not getattr(o, "is_border", False)
        ]






























#                                                                                                                                              Экран когда ударили
#   Переменные времени неуязвимости
default savedspace = 2
default savedtimer = savedspace
# Изображение сердца когда ударили
image heartdamaged = Animation("heart1.png", 0.15, "heart2.png", 0.15, repeat=True)

screen attacked_compiled_heroturn:

    timer 0.01 action Show("heroes_attacked_visual")
    timer 1.3 action Show("clear_visual")
    timer 1.35 action Hide("clear_visual")
    timer 1.5 action Hide("attacked_compiled")

screen attacked_compiled:
    timer 0.01 action Show ("protected_screen")
    timer 0.01 action Show("heroes_attacked_visual")
    timer 1.3 action Show("clear_visual")
    timer 1.35 action Hide("clear_visual")
    timer 1.5 action Hide("attacked_compiled")





screen clear_visual:
    timer 0.1 action Function(commit_hp_mp_bar_values_for_all)
    timer 0.1 action Function(reset_debuff_flags_for_all)
    timer 0.1 action Hide("clear_visual")


label asdasd:
    $ default_mouse = "Null"

default box_style = None
screen protected_screen:
    $ store.box_style = getattr(store, "last_protected_box_style", "damaged")

    #timer 0.01 action Call("asdasd")
    #timer 0.01 action SetVariable("default_mouse", "Null")
    #on "hide" action SetVariable("default_mouse", "default2")

    # === ГЛАВНОЕ ИЗМЕНЕНИЕ ===
    # Эта строка выполняется в момент показа экрана
   
   
    #timer 0.01 action Function(lambda: store.enemymonster.calculate_dmg_to_hero(store.team_manager.get_character_to_hit()))

    #timer 2.0 action Show("clear_visual")

    #timer 0.1 action [Show("attacked_compiled")]
    #timer 0.1 action [Show("heroes_attacked_visual")]

    #timer 1.0 action SetVariable("default_mouse", 'default2') repeat True
    #timer 0.5 action SetVariable("default_mouse", 'Null') repeat True


    timer 0.1 action SetVariable("savedtimer", savedspace)
    timer 1.0 action SetVariable("savedtimer", savedtimer-1) repeat True
    text "savedtimer: [savedtimer]" xpos 0 ypos 40
    zorder 99999999999
    
    
    imagebutton:
        xalign 0.5 yalign 0.5
        idle "saved.png"
        hover "saved.png"
        action NullAction()
    
    # Контейнер для горизонтального расположения изображений
    hbox:
        xpos 0.35 ypos 0.15  # Центрируем по горизонтали и вертикали
        hbox:
            xalign 0.1
            spacing 10  # Расстояние между изображениями
            if savedtimer >= 1:
                add "savedtimer.png"
            if savedtimer >= 2:
                add "savedtimer.png"
            if savedtimer >= 3:
                add "savedtimer.png"
            if savedtimer >= 4:
                add "savedtimer.png"
            if savedtimer >= 5:
                add "savedtimer.png"

    #timer (savedspace) action SetVariable("savedtimer", (savedspace))
    timer savedspace action [SetVariable ("box_style", None), Hide("protected_screen")]  # Скрытие автоматически вызовет on "hide"

    #кастомный курсор на экране
    #python:
    #    mx, my = renpy.get_mouse_pos()
    #add "heartdamaged" xpos (mx-16) ypos (my-16)

label damaged:
    #$ default_mouse = 'damaged'
    #pause 4.8
    #$ default_mouse = 'default2'
    $ renpy.pause(99999, hard=True)
    #call nolabel
