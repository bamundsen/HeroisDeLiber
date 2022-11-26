from Models.Characters.character import Character
from Models.StoryLine.character_factory import Character_Factory
from Models.StoryLine.character_factory import Character_Type
import json
import math

class Story:
    def __init__(self) :
        self.hero_value = 100000
        self.act_value = 10000
        self.choice_one_value = 1000
        self.choice_two_value = 100
        self.choice_three_value = 10
        self.choice_four_value = 1
        self.hero = 0
        self.act = 0
        self.choices = []
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
        for data in player_data['choices']:
            if data != 0:
                self.current_choice += int(1)
            else:
                break

        # self.hero = int(player_data/self.hero_value)
        # self.act = int((player_data%self.hero_value)/self.act_value)
        # if self.act == 0:
        #     self.act = int(1)
        # choices_mult = 10000
        # self.choices = []
        # for i in range(4):
        #     self.choices.append((int(player_data%choices_mult)/self.choice_one_value))
        #     if self.choices[i] > 0:
        #         self.current_choice += int(1)  
        #     choices_mult = int(choices_mult/10)
            
        # if self.current_choice >= 4:
        #         self.act += int(1)
    
    def cookie_values_set(self, player_data, new_info):
        if player_data == 0:
            return self.to_json(new_info, 1, 0, 0, 0, 0)

    def cookie_create(self, new_info):
        # setting new hero
        self.story_values_set(new_info*self.hero_value)
    
        player_data = int(self.hero*self.hero_value + self.act*self.act_value)
        counter = int(1000)
        for data in self.choices:
            player_data += int(data*counter)
            counter /= 10
        
    
        return player_data


    def get_hero_stats(self):
        cf = Character_Factory()
        return cf.create(self.hero)
    
    def get_event_content(self, player_data):
        with open("static/Resources/json/stories/events.json", encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[int(player_data[0]['act'])]
        
        if player_data[0]['hero'] == 1:
             with open("static/Resources/json/stories/options_knight.json", encoding='utf-8') as options_json:
                options = json.load(options_json)
                options = options[int(player_data[0]['act'])]['events'][self.current_choice]['options']
            
        event_content = [event['act_name'], event['icon'], event['lores'][self.current_choice]['lore']]
        for o in options:
            event_content.append(o['text'])
            
        return event_content
        # with open("static/Resources/json/stories/events.json", encoding='utf-8') as events_json:
        #     event = json.load(events_json)
        #     event = event[self.act]
            
        # for i in range(4):
        #     event_content = [event['act_name'], event['icon'], event['events'][int(i+1)]['lore']]
        #     if self.choices[i+1] == 0:
        #         break
        # return event_content
    
    def get_options_content(self):
        if self.hero == 1:
            with open("static/Resources/json/stories/options_knight.json", encoding='utf-8') as options_json:
                options = json.load(options_json)
                options = options[self.act]['event'][self.current_choice]['options']
        
        options_text = []   
        for option in options:
            if option['id'] != 0:
                options_text.append(option['text'])
    
        return options_text
    
    def to_json(self, hero, act, c_one, c_two, c_three, c_four):
        player_data = [{"hero": hero,"act": act, "choices":[{"c_one": c_one, "c_two": c_two, "c_three": c_three, "c_four": c_four}]}]
        return player_data
    
if __name__ == '__main__':
    pass