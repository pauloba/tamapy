import os
from datetime import timedelta
from tamapy import Tamagotchi, SAVE_FILE


def cleanup():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


def test_initial_state():
    cleanup()
    t = Tamagotchi("Test")
    assert t.happy == 6
    assert t.full == 6
    assert t.clean == 6
    assert t.health == 6
    assert t.poo == 0
    assert t.age_years == 0


def test_medicine_cures_sickness():
    cleanup()
    t = Tamagotchi("Test")
    t.poo = 4  # sick
    t.health = 3

    t.take_medicine()

    assert t.health == 4  # healed
    assert t.poo == 0     # sickness cured


def test_age_increase():
    cleanup()
    t = Tamagotchi("Test")

    # simulate 10 minutes passing
    t.last_age_update -= timedelta(minutes=10)
    t.tick()

    assert t.age_years == 2


def test_save_load_resets_poo():
    cleanup()
    t = Tamagotchi("Test")
    t.poo = 5
    t.save()

    t2 = Tamagotchi.load()
    assert t2.poo == 0  # reset on load

    cleanup()