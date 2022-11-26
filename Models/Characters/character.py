class Character:
    def __init__(self, name, hp, defense, attack_1, attack_2, ability_1, ability_2, quintessence, icon):
        self.name = name
        self.hp = hp
        self.defense = defense
        self.attack_1 = attack_1
        self.attack_2 = attack_2
        self.ability_1 = ability_1
        self.ability_2 = ability_2
        self.quintessence = quintessence
        self.icon = icon

    def attack(self, defense_enemy):
        pass
    
    def get_damagge(self, attack_enemy):
        pass
    
    def healing(self, healing_source):
        pass
    


