from Models.Characters.character import Character
from Models.Characters.warrior import Warrior
from Models.Characters.wizard import Wizard
from Models.Characters.rogue import Rogue
from Models.Characters.cleric import Cleric
from enum import Enum
import json

class Character_Type(Enum):
    GUERREIRO = 1
    MAGO = 2
    LADINO = 3
    CLERIGO = 4
    
class Character_Factory:
    
    @staticmethod
    def create(character_type) -> Character:
        
        with open("static/Resources/json/heroes.json", encoding='utf-8') as heroes_list_json:
            heroes_list = json.load(heroes_list_json)
        
        if character_type == Character_Type.GUERREIRO:
            return Warrior(heroes_list[0]['name'], heroes_list[0]['hp'], heroes_list[0]['defense'], heroes_list[0]['attack_1'], heroes_list[0]['attack_2'], heroes_list[0]['ability_1'], heroes_list[0]['ability_2'], heroes_list[0]['quintessence'], heroes_list[0]['icon'])
        if character_type == Character_Type.MAGO:
            return Wizard(heroes_list[1]['name'], heroes_list[1]['hp'], heroes_list[1]['defense'], heroes_list[1]['attack_1'], heroes_list[1]['attack_2'], heroes_list[1]['ability_1'], heroes_list[1]['ability_2'], heroes_list[1]['quintessence'], heroes_list[1]['icon'])
        if character_type == Character_Type.LADINO:
            return Rogue(heroes_list[2]['name'], heroes_list[2]['hp'], heroes_list[2]['defense'], heroes_list[2]['attack_1'], heroes_list[2]['attack_2'], heroes_list[2]['ability_1'], heroes_list[2]['ability_2'], heroes_list[2]['quintessence'], heroes_list[2]['icon'])
        if character_type == Character_Type.CLERIGO:
            return Cleric(heroes_list[3]['name'], heroes_list[3]['hp'], heroes_list[3]['defense'], heroes_list[3]['attack_1'], heroes_list[3]['attack_2'], heroes_list[3]['ability_1'], heroes_list[3]['ability_2'], heroes_list[3]['quintessence'], heroes_list[3]['icon'])
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
        