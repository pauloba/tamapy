import json
import os
from datetime import datetime, timedelta

SAVE_FILE = "tamapy_state.json"


def print_squares(stat_value, stat_name):
    """
    Render a bar from 0–6 for a given stat name.
    stat_value: int in [0,6]
    stat_name: one of "happy", "full", "clean", "health"
    """
    stat_value = max(0, min(6, stat_value))

    label_map = {
        "happy": "HAPPY",
        "full": "FULL",
        "clean": "CLEAN",
        "health": "HEALTHY",
    }
    label = label_map.get(stat_name, stat_name.upper())

    filled = "■" * stat_value
    empty = "□" * (6 - stat_value)

    if stat_value == 0:
        icon = "💀"
    elif stat_value <= 2:
        icon = "🔴"
    elif stat_value <= 4:
        icon = "🟠"
    else:
        icon = "🟢"

    print(f"{icon} {label:<7} {filled}{empty}")


class Tamagotchi:
    """
    Tick-based Tamagotchi with slow decay.

    Stats:
      happy, full, clean, health: 0–6

    Hidden stat:
      poo: 0–6 (NOT shown to user, NOT saved)

    Death condition:
      happy == 0 AND health == 0 AND full == 0 AND clean == 0

    Age:
      +1 pet year every 5 minutes of real time (only while game is running)
    """

    def __init__(self, name: str):
        self.name = name
        self.start = datetime.now()
        self.now = self.start

        # Stats
        self.happy = 6
        self.full = 6
        self.clean = 6
        self.health = 6

        # Hidden stat
        self.poo = 0

        # Age system
        self.age_years = 0
        self.last_age_update = self.start

        # Tick counter
        self.tick_count = 0

    @property
    def is_dead(self):
        return (
            self.happy == 0
            and self.health == 0
            and self.full == 0
            and self.clean == 0
        )

    def _dec_stat(self, attr):
        value = getattr(self, attr)
        if value > 0:
            setattr(self, attr, value - 1)

    def _inc_stat(self, attr):
        value = getattr(self, attr)
        if value < 6:
            setattr(self, attr, value + 1)

    # Actions

    def feed(self):
        if not self.is_dead:
            self._inc_stat("full")

    def clean_poo(self):
        if not self.is_dead:
            if self.poo > 0:
                self.poo -= 1
            self._inc_stat("clean")

    def take_medicine(self):
        """
        Medicine heals AND cures sickness by resetting poo.
        """
        if not self.is_dead:
            self._inc_stat("health")
            self.poo = 0  # cure sickness source

    def play(self):
        if not self.is_dead:
            self._inc_stat("happy")

    # Age system

    def update_age(self):
        now = datetime.now()
        elapsed_minutes = (now - self.last_age_update).total_seconds() / 60

        if elapsed_minutes >= 5:
            gained_years = int(elapsed_minutes // 5)
            self.age_years += gained_years
            self.last_age_update = now

    # Tick logic

    def tick(self):
        if self.is_dead:
            return

        self.tick_count += 1
        self.now = datetime.now()

        # Update age
        self.update_age()

        # Poo increases every 2 ticks (hidden)
        if self.tick_count % 2 == 0 and self.poo < 6:
            self.poo += 1

        # Natural sickness: poo >= 3
        if self.poo >= 3:
            self._dec_stat("health")

        # Slow decay: rotate stats
        order = ["happy", "full", "clean", "health"]
        idx = (self.tick_count - 1) % len(order)
        target = order[idx]

        if target == "health":
            if self.health <= 2 and self.health > 0:
                self._dec_stat("health")
        else:
            self._dec_stat(target)

        # If poo maxed, cleanliness drops
        if self.poo == 6 and self.clean > 0:
            self._dec_stat("clean")

    # Persistence

    def to_dict(self):
        return {
            "name": self.name,
            "start": self.start.isoformat(),
            "now": self.now.isoformat(),
            "happy": self.happy,
            "full": self.full,
            "clean": self.clean,
            "health": self.health,
            "tick_count": self.tick_count,
            "age_years": self.age_years,
            "last_age_update": self.last_age_update.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(data["name"])
        obj.start = datetime.fromisoformat(data["start"])
        obj.now = datetime.fromisoformat(data["now"])
        obj.happy = data["happy"]
        obj.full = data["full"]
        obj.clean = data["clean"]
        obj.health = data["health"]
        obj.tick_count = data.get("tick_count", 0)
        obj.age_years = data.get("age_years", 0)
        obj.last_age_update = datetime.fromisoformat(
            data.get("last_age_update", data["now"])
        )

        # Hidden stat resets on load
        obj.poo = 0

        return obj

    def save(self, path: str = SAVE_FILE):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @staticmethod
    def load(path: str = SAVE_FILE):
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Tamagotchi.from_dict(data)

    # UI

    def print_status(self):
        print(f"\n=== {self.name}'s status ===")
        print(f"Age: {self.age_years} 🐾")
        print_squares(self.happy, "happy")
        print_squares(self.full, "full")
        print_squares(self.clean, "clean")
        print_squares(self.health, "health")

        if self.is_dead:
            print("\n💀 Your Tamapy has died. Game over.\n")


def main():
    print("🐣 Welcome to Tamapy!\n")

    tama = Tamagotchi.load()
    if tama:
        print(f"Loaded existing Tamapy: {tama.name}")
    else:
        name = input("Choose a name for your Tamapy: ").strip()
        if not name:
            name = "Tamapy"
        tama = Tamagotchi(name)
        tama.save()

    while True:
        tama.print_status()
        if tama.is_dead:
            break

        print("What do you want to do?")
        print("[f]eed  [p]lay  [c]lean  [m]edicine  [q]uit")
        choice = input("> ").strip().lower()

        if choice == "f":
            tama.feed()
        elif choice == "p":
            tama.play()
        elif choice == "c":
            tama.clean_poo()
        elif choice == "m":
            tama.take_medicine()
        elif choice == "q":
            print("Saving and quitting...")
            tama.save()
            break
        else:
            print("Unknown action.")
            continue

        tama.tick()
        tama.save()


if __name__ == "__main__":
    main()