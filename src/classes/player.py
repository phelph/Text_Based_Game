import sys
from classes.items import Item, Weapon
from classes.npcs import Enemy
from classes.stats import Stats


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.level: int = 1
        self.exp: int = 0
        self.max_exp: int = 100
        self.hp: int = 100
        self.max_hp: int = 100
        self.gold: int = 0
        self.stats: Stats = Stats()

        # Weapons and inventory
        self.equipped_weapon: Weapon = None
        self.inventory: list[Item] = []
        self.equipped_item_slot = 0

        # Usable weapon ranges and types
        self.usable_weapon_ranges = ["melee", "ranged"]
        self.usable_weapon_types = {
            "melee": ["Sword", "Axe"],
            "ranged": ["Bow", "Crossbow"],
        }

    def show_exp(self):
        print(f"{self.name} has {self.exp}/{self.max_exp - self.exp} exp to level up\n")

    def gain_exp(self, exp):
        self.exp += exp
        print(f"{self.name} gained {exp} experience!\n")
        if self.exp >= self.max_exp:
            self.level_up()
            self.exp = self.exp - self.max_exp
        self.show_exp()

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        print(f"{self.name} is now level {self.level}!\n")

    def attack(self, target: Enemy):
        dmg = self.equipped_weapon.get_power()

        killed_bool, target_hp, gained_gold = target.take_dmg(dmg)

        print(f"{self.name} attacks the {target.enemy_type} for {dmg} damage!\n")

        if killed_bool:
            print(f"{self.name} killed {target.enemy_type}!\n")
            print(f"{self.name} gained {gained_gold} gold!\n")
            self.gain_exp(target.exp)
        else:
            print(f"{target.name} has {target_hp} hp left!\n")

    def take_dmg(self, dmg: int):
        self.hp -= dmg

        if self.hp <= 0:
            print("OH NO! \nYou have died! \nBetter luck next time!")
            sys.exit(0)


class Warrior(Player):
    def __init__(self, name: str):
        super().__init__(name)

        # Warriors have higher base hp and strength, but less arcane knowledge than other classes
        self.max_hp += 20
        self.hp = self.max_hp

        self.stats.values["Strength"] += 5
        self.stats.values["Arcane"] -= 3

        # Usable weapon ranges and types
        # Warriors dont have access to pure ranged weapons
        # The only ranged weapon they can use is the Throwing Spear which can also be used as a melee weapon
        self.usable_weapon_ranges = ["melee", "hybrid"]
        self.usable_weapon_types = {
            "melee": ["Sword", "Axe"],
            "hybrid": ["Throwing Spear"],
        }

        self.equipped_weapon: Weapon = Weapon(
            name="Old Rusted Sword", power=5, weapon_range="melee", weapon_type="Sword"
        )


class Mage(Player):
    def __init__(self, name: str):
        super().__init__(name)

        # Mages have higher arcane and dex but less strength than other classes
        self.stats.values["Strength"] -= 3
        self.stats.values["Arcane"] += 10
        self.stats.values["Dexterity"] += 5

        # Usable weapon ranges and types
        # Mages dont have access to pure ranged weapons
        # The only ranged weapon they can use is the Throwing Spear which can also be used as a melee weapon
        self.usable_weapon_ranges = [
            "range",
        ]
        self.usable_weapon_types = {
            "range": [
                "Wand",
            ],
        }

        self.equipped_weapon: Weapon = Weapon(
            name="Simple Old Wand", power=5, weapon_range="range", weapon_type="Wand"
        )
