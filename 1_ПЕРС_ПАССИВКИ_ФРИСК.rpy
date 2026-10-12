# Пассивки Фриск и боевое состояние дипломатии.
default frisk_si_vis_ready = False
default frisk_round_social_bonus = 0
default frisk_saved_peace_battles = 0
default frisk_last_hp = 0
default frisk_foedus_used = False

init python:
    FRISK_SOCIAL_ATTRS = ("socialization", "diplomacy", "charm", "perception", "rhetoric", "artistry", "power")

    def frisk_char():
        return (getattr(store, "pers_dict", {}) or {}).get("Фриск")

    def frisk_level():
        char = frisk_char()
        return max(1, int(getattr(char, "level", 1) or 1)) if char else 1

    def frisk_reset_battle_passives():
        char = frisk_char()
        store.frisk_si_vis_ready = False
        store.frisk_round_social_bonus = 0
        store.frisk_foedus_used = False
        store.frisk_last_hp = getattr(char, "current_hp", 0) if char else 0

    def frisk_on_damage_received(old_hp=None):
        char = frisk_char()
        if char is None or char.current_hp <= 0:
            return False
        if old_hp is None or char.current_hp < old_hp:
            store.frisk_si_vis_ready = True
            return True
        return False

    def frisk_round_strategy():
        char = frisk_char()
        if char is None:
            return
        attr = renpy.random.choice(FRISK_SOCIAL_ATTRS)
        setattr(char, attr, getattr(char, attr, 0) + 1)

    def frisk_prepare_round_end():
        frisk_round_strategy()
        char = frisk_char()
        if char is not None:
            store.frisk_last_hp = getattr(char, "current_hp", 0)

    def frisk_peace_reward():
        """Награда за бой, законченный пощадой."""
        store.frisk_saved_peace_battles = int(getattr(store, "frisk_saved_peace_battles", 0)) + 1
        char = frisk_char()
        if char is not None:
            char.bonus_charm = getattr(char, "bonus_charm", 0) + 0.01
            char.diplomacy = getattr(char, "diplomacy", 0) + 1

    def frisk_si_vis_damage_bonus():
        """Сумма недостающего HP команды, ограниченная 100%."""
        chars = getattr(store, "pers_dict", {}) or {}
        missing = 0.0
        for char in chars.values():
            if getattr(char, "is_ally", True) and getattr(char, "max_hp", 0):
                missing += max(0.0, 1.0 - char.current_hp / float(char.max_hp))
        return min(1.0, missing / max(1, len(chars)))
