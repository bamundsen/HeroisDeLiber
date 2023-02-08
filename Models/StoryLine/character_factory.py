from enum import Enum
import json

class Character_Type(Enum):
    GUERREIRO = 1
    MAGO = 2
    LADINO = 3
    CLERIGO = 4

class Character:
    def __init__(self, hero_json):
        self.name = hero_json['name']
        self.hp = hero_json['hp']
        self.defense = hero_json['defense']
        self.attack_1 = hero_json['attack_1']
        self.attack_2 = hero_json['attack_2']
        self.ability_1 = hero_json['ability_1']
        self.ability_2 = hero_json['ability_2']
        self.quintessence = hero_json['quintessence']
        self.icon = hero_json['icon']
        self.score = 100

    def attack(self, defense_enemy):
        pass
    
    def get_hp(self, damage):
        damage -= damage*(self.defense/200)
        self.hp -= damage
        return self.hp
    
    def get_score(self, score):
        self.score += score
        return self.score

class Cleric(Character):
    pass

class Rogue(Character):
    pass

class Warrior(Character):
    pass

class Wizard(Character):
    pass
    
# INÍCIO DO PADRÃO FACTORY
class Character_Factory:
    
    @staticmethod
    def create(character_type) -> Character:
        
        with open("static/Resources/json/heroes.json", encoding='utf-8') as heroes_list_json:
            heroes_list = json.load(heroes_list_json)
        
        if character_type == Character_Type.GUERREIRO.value:
            return Warrior(heroes_list[0])
        if character_type == Character_Type.MAGO.value:
            return Wizard(heroes_list[1])
        if character_type == Character_Type.LADINO.value:
            return Rogue(heroes_list[2])
        if character_type == Character_Type.CLERIGO.value:
            return Cleric(heroes_list[3])
        else:
            return None
    
    def to_enum(index) -> Character_Type:
        if index == 1:
            return Character_Type.GUERREIRO
        if index == 2:
            return Character_Type.MAGO
        if index == 3:
            return Character_Type.LADINO
        if index == 4:
            return Character_Type.CLERIGO


        