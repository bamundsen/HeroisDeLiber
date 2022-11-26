from Models.StoryLine.character_factory import Character_Factory
from flask import jsonify   
import json

class Story:
    def __init__(self) :
        self.hero = 0
        self.act_change = False
        self.current_act = 0
        self.choices = [0,0,0,0]
        self.current_choice = 0
    
    def get_main_text(self, id):
        if id == 0:
            with open("static/Resources/json/heroes.json", encoding='utf-8') as heroes_list_json:
                self.heroes_list = json.load(heroes_list_json)
                return self.heroes_list
                
        if id == 1:
            with open("static/Resources/json/story_line.json", encoding='utf-8') as story_line_list_json:
                self.story_line_list = json.load(story_line_list_json)
                return self.story_line_list[0]['lore']
    
    def get_current_choice(self, player_data):
        
        self.current_act = len(player_data) - 1
        for i in range(4):
            if player_data[self.current_act]['choices'][f"c_{i}"] != 0:
                self.current_choice += int(1)
            else:
                break  
        if self.current_choice > 3:
            self.current_choice = int(0)
            self.current_act = len(player_data)
            self.act_change = True

    def cookie_values_set(self, player_data, new_info):
        if player_data == 0:
            return self.to_json(new_info, 1, self.choices)
        
        else:
            self.get_current_choice(player_data)
            if self.act_change == True:
                player_data_add = []
                for i in range(self.current_act):
                    player_data_add.append(player_data[i])
                
                player_data_add.append(self.to_json(player_data[0]['hero'],
                                                    self.current_act+1,
                                                    self.choices)[0])
                return json.dumps(player_data_add) 
            
            else:
                player_data[self.current_act]['choices'][f"c_{self.current_choice}"] = new_info
                # espaguete
                if self.current_choice <3 :
                    self.current_choice += 1
                else:
                    self.current_choice = 0
                return json.dumps(player_data)

    # degub methode
    def get_hero_stats(self):
        cf = Character_Factory()
        return cf.create(self.hero)
    
    def get_event_content(self, player_data):
        
        with open("static/Resources/json/stories/events.json", encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[int(player_data[self.current_act]['act'])]
        
        with open("static/Resources/json/stories/{hero}_hero.json".format(hero = int(player_data[0]['hero'])), encoding='utf-8') as options_json:
            options = json.load(options_json)
            print(f"SELF CURRENT ACT {self.current_act} SELF CURRENT CHOICE: {self.current_choice}")
            options = options[int(player_data[self.current_act]['act'])]['events'][self.current_choice]['options']
            
        event_content = [event['act_name'], 
                         event['icon'], 
                         event['lores'][self.current_choice]['lore']]
        for o in options:
            event_content.append(o['text'])
            
        return event_content
    
    def to_json(self, hero, act, c):
        player_data = [{"hero": hero,"act": act, "choices":{"c_0": c[0], 
                                                            "c_1": c[1], 
                                                            "c_2": c[2], 
                                                            "c_3": c[3]}}]
        return player_data
    
    
if __name__ == '__main__':
    pass