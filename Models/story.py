from Models.StoryLine.character_factory import Character_Factory
from flask import jsonify
from abc import ABC, abstractclassmethod 
import json

class Story:
    def __init__(self) :
        self.hero = 0
        self.act_change = False
        self.current_act = 0
        self.choices = [0,0,0,0]
        self.current_choice = 0
        self.player_data = None
        self.new_choice = None
        self.from_refresh = False
    
    def get_main_text(self):
        # if id == 0:
        #     with open("static/Resources/json/heroes.json", encoding='utf-8') as heroes_list_json:
        #         heroes_list = json.load(heroes_list_json)
        #     return heroes_list
                
        # if id == 1:
        #     with open("static/Resources/json/story_line.json", encoding='utf-8') as story_line_list_json:
        #         story_line_list = json.load(story_line_list_json)
        #     return story_line_list[0]['lore']
        
        with open("static/Resources/json/heroes.json", encoding='utf-8') as heroes_list_json:
                heroes_list = json.load(heroes_list_json)
        with open("static/Resources/json/story_line.json", encoding='utf-8') as story_line_list_json:
                story_line_list = json.load(story_line_list_json)
        main_content = {"heroes": heroes_list, "story": story_line_list}
        return main_content
    
    
    def get_current_choice_pick(self):
        if self.player_data != 0:
            self.current_act = len(self.player_data) - 1
            self.get_current_choice()
            
            if self.current_choice >= 3:
            # if self.current_choice > 3:
                # self.current_choice = int(0)
                self.current_act = len(self.player_data)
                self.act_change = True
            
    def get_current_choice(self):
        for i in range(4):
            if self.player_data[self.current_act]['choices'][f"c_{i}"] != 0 and self.current_choice < 4:
                self.current_choice += int(1)
            else:
                break

    def cookie_values_set(self):
        if self.player_data == 0:
            return self.to_json(self.new_choice, 1, self.choices)
        
        if self.new_choice != -1:
            if self.act_change:
                self.player_data[self.current_act-1]['choices'][f"c_{self.current_choice}"] = self.new_choice
                player_data_add = []
                for i in range(self.current_act):
                    player_data_add.append(self.player_data[i])
                
                player_data_add.append(self.to_json(self.player_data[0]['hero'],
                                                    self.current_act+1,
                                                    self.choices)[0])
                self.current_choice = int(0)
                print(f"SCA: {self.current_act} SCC: {self.current_choice-1} OPTION: {self.new_choice-1}")
                self.player_data = player_data_add
                return json.dumps(self.player_data) 
            
            else:
                self.player_data[self.current_act]['choices'][f"c_{self.current_choice}"] = self.new_choice
                
                if self.current_choice < 3 :
                    self.current_choice += 1
                else:
                    self.current_choice = 0
                if self.act_change == True:
                    self.current_act += 1

                return json.dumps(self.player_data)

    # degub method
    def get_hero_stats(self):
        cf = Character_Factory()
        return cf.create(self.hero)
    
    # CONTEÚDOS DO FRONTEND
    def get_event_content(self):

        if len(self.player_data) < 3:
            story_lore = StoryLore(NoBranchLore(self))
            
        if len(self.player_data) == 3:
            story_lore = StoryLore(BranchLore(self))
        
        return story_lore.return_content()
    
    def get_consequence(self):
     
        if len(self.player_data) < 3:
            story_lore = StoryLore(NoBranchLore(self))
            
        if len(self.player_data) == 3:
            story_lore = StoryLore(BranchLore(self))
        
        return story_lore.return_consequence()
    
    def to_json(self, hero, act, c):
        player_data = [{"hero": hero,"act": act, "choices":{"c_0": c[0], 
                                                            "c_1": c[1], 
                                                            "c_2": c[2], 
                                                            "c_3": c[3]}}]
        return player_data
    
    
class StoryFacade:
    def __init__(self, player_data, new_info, from_refresh):
        self.story = Story()
        self.character_factory = Character_Factory()
        self.story.player_data = player_data
        self.story.new_choice = new_info
        self.story.from_refresh = from_refresh
        if player_data != None and player_data != 0:
            self.story.hero = int(player_data[0]['hero'])
            
    def game_start(self):
        return self.story.get_main_text()
        
    def set_save(self):
        self.story.get_current_choice_pick()
        return self.story.cookie_values_set()
    
    def pick_choice(self):
        self.story.get_current_choice_pick()
        self.story.cookie_values_set()
        event_content = {"event_content": self.story.get_event_content(), 
                     "consequence": self.story.get_consequence()}
        return event_content
    
    def display_player_data(self):
        return json.dumps(self.story.player_data)
        
    #debugmethode
    def get_hero_status(self):
        print(self.story.hero)
        hero = self.character_factory.create(self.story.hero)
        return hero.ability_1
    
class StoryLore:
    def __init__(self, branch_content):
        self.branch_content = branch_content
    
    def return_content(self):
        return self.branch_content.select_content()
        
    def return_consequence(self):
        return self.branch_content.select_consequence()

class Ilore(ABC):
    @abstractclassmethod
    def select_content(self):
        pass
    
    def select_consequence(self):
        pass

class NoBranchLore(Ilore):
    def __init__(self, story):
        self.story = story
        
    def select_content(self):
        if self.story.from_refresh:
            self.story.current_act = int(len(self.story.player_data)-1)
            self.story.get_current_choice()
            if self.story.current_choice > 3:
                self.story.current_choice = int(0)
            
        with open("static/Resources/json/stories/events.json", encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[int(self.story.player_data[self.story.current_act]['act'])]
        
        with open("static/Resources/json/stories/{hero}_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
            options = json.load(options_json)
            options = options[int(self.story.player_data[self.story.current_act]['act'])]['events'][self.story.current_choice]['options']
        
        options_texts = []
        for o in options:
            options_texts.append(o['text'])
            
        event_content = {"act_name": event['act_name'], 
                   "icon": event['lores'][self.story.current_choice]['icon'], 
                   "lore": event['lores'][self.story.current_choice]['lore'], 
                   "options": options_texts}

        return event_content
    
    def select_consequence(self):
        with open("static/Resources/json/stories/{hero}_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
            consequence = json.load(options_json)
            print(f"SCA: {self.story.current_act} SCC: {self.story.current_choice-1} OPTION: {self.story.new_choice-1}")
            if self.story.current_choice > 0:
                consequence = consequence[int(self.story.player_data[self.story.current_act]['act'])]['events'][self.story.current_choice-1]['options'][self.story.new_choice-1]['consequence']
            else:
                consequence = consequence[int(self.story.player_data[self.story.current_act-1]['act'])]['events'][3]['options'][self.story.new_choice-1]['consequence']
        
        return consequence
    
class BranchLore(Ilore):
    def __init__(self, story):
        self.story = story
        
    def select_content(self):
        if self.story.from_refresh:
            self.story.current_act = int(len(self.story.player_data)-1)
            self.story.get_current_choice()
            print(self.story.current_choice)
            if self.story.current_choice > 3:
                self.story.current_choice = int(0)
        
        branch_choice = int(self.story.player_data[1]['choices']['c_3']) -1
        
        with open("static/Resources/json/stories/0_events.json", encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[branch_choice]
            
        with open("static/Resources/json/stories/{hero}.0_hero.json".format(hero = int(self.story.player_data[0]['hero']), branch = branch_choice), encoding='utf-8') as options_json:
            options = json.load(options_json)
            options = options[branch_choice]['events'][self.story.current_choice]['options']
            
        options_texts = []
        for o in options:
            options_texts.append(o['text'])
                
        event_content = {"act_name": event['act_name'], 
                "icon": event['lores'][self.story.current_choice]['icon'], 
                "lore": event['lores'][self.story.current_choice]['lore'], 
                "options": options_texts}

        return event_content
    
    def select_consequence(self):
        branch_choice = int(self.story.player_data[1]['choices']['c_3']) -1
        
        with open("static/Resources/json/stories/{hero}.0_hero.json".format(hero = int(self.story.player_data[0]['hero']), branch = branch_choice), encoding='utf-8') as options_json:
            consequence = json.load(options_json)
            print(f"SCA: {self.story.current_act} SCC: {self.story.current_choice-1} OPTION: {self.story.new_choice-1}")
            if self.story.current_choice > 0:
                consequence = consequence[branch_choice]['events'][self.story.current_choice-1]['options'][self.story.new_choice-1]['consequence']
            else:
                consequence = consequence[branch_choice]['events'][3]['options'][self.story.new_choice-1]['consequence']
        
        return consequence
    
if __name__ == '__main__':
    pass