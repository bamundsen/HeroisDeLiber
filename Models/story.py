from Models.StoryLine.character_factory import Character_Factory
from abc import ABC, abstractclassmethod 
import json

class Story:
    def __init__(self) :
        self.hero = 0
        self.act_change = False
        self.has_chosen = False
        self.is_hero_alive = True
        self.hp_scoring = False
        self.is_history_finished = False
        self.current_act = 0
        self.choices = [0,0,0,0]
        self.current_choice = 0
        self.player_data = None
        self.new_choice = None
        self.from_refresh = False
    
    def get_main_text(self):
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
                self.current_act = len(self.player_data)
                self.act_change = True
            
    def get_current_choice(self):
        self.current_choice = int(0)
        for i in range(4):
            if self.player_data[self.current_act]['choices'][f"c_{i}"] != 0 and self.current_choice < 4:
                self.current_choice += int(1)
            else:
                break
            
    def set_choice_made(self):
        self.has_chosen = True

    def cookie_values_set(self):
        if self.player_data == 0:
            return self.to_json(self.new_choice, 1, self.choices)
        
        if self.new_choice != -1:
            print(self.current_act)
            print(self.current_choice)
            if self.act_change == True and self.current_act < 4:
                self.player_data[self.current_act-1]['choices'][f"c_{self.current_choice}"] = self.new_choice
                player_data_add = []
                for i in range(self.current_act):
                    player_data_add.append(self.player_data[i])
                
                player_data_add.append(self.to_json(self.player_data[0]['hero'],
                                                    self.current_act+1,
                                                    self.choices)[0])
                self.current_choice = int(0)
                self.player_data = player_data_add
                return json.dumps(self.player_data) 
            
            if self.current_act == 4 and self.current_choice == 3:
                self.player_data[self.current_act-1]['choices'][f"c_{self.current_choice}"] = self.new_choice
                self.is_history_finished = True
                return json.dumps(self.player_data)
            
            else:
                self.player_data[self.current_act]['choices'][f"c_{self.current_choice}"] = self.new_choice
                
                if self.current_choice < 3 :
                    self.current_choice += 1
                else:
                    self.current_choice = 0
                if self.act_change == True and self.current_act < 4:
                    self.current_act += 1

                return json.dumps(self.player_data)

    # MÉTODO PARA DEBUG
    def get_hero_stats(self):
        cf = Character_Factory()
        return cf.create(self.hero)
    
    # CONTEÚDOS DO FRONTEND
    def get_event_content(self):
        return StoryLoreStrategy(self).return_lore_dict()
    
    def get_consequence(self):
        return StoryLoreStrategy(self).return_lore_dict()

    def pack_content_consequence(self):
        if self.is_history_finished == True:
            # event content de final
            pass
        if self.is_hero_alive:
            event_content = {"event_content": self.get_event_content(), "hero_scores": self.damage_hp_and_score(), 
                     "consequence": self.get_consequence()}
        else:
            event_content = {"event_content": self.get_event_content(), "hero_scores": self.damage_hp_and_score(), 
                     "consequence": self.get_consequence()}
        return event_content

    def damage_hp_and_score(self):
        if self.hero != None and self.hero != 0:
            hero = Character_Factory.create(self.hero)
        self.hp_scoring = True
        for index, data in enumerate(self.player_data, start=1):
            if hero.hp < 1:
                break
            for count, choice in enumerate(data['choices'], start=0):   
                if data['choices'][choice] > 0:
                    contents = HpCounter(self, count, index, data['choices'][choice]).return_lore_dict()
                    if len(self.player_data) < 3:
                        if self.from_refresh:
                            self.current_act = int(len(self.player_data)-1)
                            self.get_current_choice()
                            if self.current_choice > 3:
                                self.current_choice = int(0)

                    damage = contents['damage']
                    score = contents['score']
                    hero.get_hp(damage)
                    hero.get_score(score)
                    if hero.hp < 1:
                        self.is_hero_alive = False
                        break
                else:
                    break
        self.set_choice_made()
        hero_scores = {"hp": hero.hp, "score": hero.score}
        return hero_scores
        

    def to_json(self, hero, act, c):
        player_data = [{"hero": hero,"act": act, "choices":{"c_0": c[0], 
                                                            "c_1": c[1], 
                                                            "c_2": c[2], 
                                                            "c_3": c[3]}}]
        return player_data
    
# INÍCIO DO PADRÃO FACADE, PARA ENCAPSULAR A CRIAÇÃO DE STORY E STORYFACADE UTILIZADOS NO WEBVIEW
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
        return self.story.pack_content_consequence()
    
    def display_player_data(self):
        return json.dumps(self.story.player_data)
            
# FIM DO PADRÃO FACADE
    
# INÍCIO DO PADRÃO STRATEGY, FEITO PARA DISCRIMINAR A SELEÇÃO DE ARQUIVOS QUANDO HÁ BIFURCAÇÃO DA HISTÓRIA
# DIVIDIR EM DUAS CLASSES: SELECT CONTENT E SELECT CONSEQUENCE
# TRAZER A DECISÃO DA ESTRATÉGIA PARA O MÉTODO
class StoryLoreStrategy:
    def __init__(self, story):
        self.story = story
        
    def return_lore_dict(self):
        if self.story.has_chosen == False:
            if self.story.from_refresh or self.story.hp_scoring:
                self.story.current_act = int(len(self.story.player_data)-1) 
                self.story.get_current_choice()
            if self.story.current_choice > 3:
                self.story.current_choice = int(0)

            choice_to_pick = self.story.current_choice

            if len(self.story.player_data) < 3:
                contents = NoBranchLore(self.story).select_content()
                
            if len(self.story.player_data) == 3:
                contents = BranchLoreOne(self.story).select_content()
            
            if len(self.story.player_data) == 4:
                contents = BranchLoreTwo(self.story).select_content()

            if self.story.hp_scoring == False:
                options_texts = []
                for o in contents['options']:
                    options_texts.append(o['text'])

                        
                event_content = {"act_name": contents['event']['act_name'], 
                        "icon": contents['event']['lores'][choice_to_pick]['icon'], 
                        "lore": contents['event']['lores'][choice_to_pick]['lore'], 
                        "options": options_texts}
                return event_content
            
        if self.story.has_chosen == True:
                
            if len(self.story.player_data) < 3:
                story_lore = NoBranchLore(self.story).select_consequence()
                
            if len(self.story.player_data) == 3:
                story_lore = BranchLoreOne(self.story).select_consequence()
                
            if len(self.story.player_data) == 4:
                story_lore = BranchLoreTwo(self.story).select_consequence()
            
            return story_lore

class Ilore(ABC):
    @abstractclassmethod
    def select_content(self):
        pass
    
    def select_consequence(self):
        pass

class NoBranchLore(Ilore):
    def __init__(self, story):
        self.story = story
        self.act = self.story.current_act
        self.current_choice = self.story.current_choice
        
    def select_content(self):
        act_to_pick = int(self.story.player_data[self.act]['act'])
        choice_to_pick = self.story.current_choice
        with open("static/Resources/json/stories/events.json", encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[act_to_pick]
        
        with open("static/Resources/json/stories/{hero}_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
            options = json.load(options_json)
            options = options[act_to_pick]['events'][choice_to_pick]['options']
        
        contents = {"event": event, "options": options}
        return contents
    
    def select_consequence(self):
        with open("static/Resources/json/stories/{hero}_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
            consequence = json.load(options_json)
            if self.current_choice > 0:
                consequence = consequence[int(self.story.player_data[self.story.current_act]['act'])]['events'][self.current_choice-1]['options'][self.story.new_choice-1]['consequence']
            else:
                consequence = consequence[int(self.story.player_data[self.story.current_act-1]['act'])]['events'][3]['options'][self.story.new_choice-1]['consequence']
        
        return consequence
    
class BranchLoreOne(Ilore):
    def __init__(self, story):
        self.story = story
        self.current_choice = self.story.current_choice
        
    def select_content(self):
        branch_choice = int(self.story.player_data[1]['choices']['c_3']) -1
        
        with open("static/Resources/json/stories/0_events.json", encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[branch_choice]
            
        with open("static/Resources/json/stories/{hero}.0_hero.json".format(hero = int(self.story.player_data[0]['hero']), branch = branch_choice), encoding='utf-8') as options_json:
            options = json.load(options_json)
            options = options[branch_choice]['events'][self.current_choice]['options']
        
        contents = {"event": event, "options": options}
        return contents
    
    def select_consequence(self):
        branch_choice = int(self.story.player_data[1]['choices']['c_3']) -1
        
        with open("static/Resources/json/stories/{hero}.0_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
            consequence = json.load(options_json)
            
            if self.current_choice > 0:
                consequence = consequence[branch_choice]['events'][self.current_choice-1]['options'][self.story.new_choice-1]['consequence']
            else:
                consequence = consequence[branch_choice]['events'][3]['options'][self.story.new_choice-1]['consequence']
        
        return consequence

    
class BranchLoreTwo(Ilore):
    def __init__(self, story):
        self.story = story
        self.current_choice = self.story.current_choice
        
    def select_content(self):
        branch_choice_one = int(self.story.player_data[1]['choices']['c_3']) -1
        branch_choice_two = int(self.story.player_data[2]['choices']['c_3']) -1
        
        with open("static/Resources/json/stories/0.{bc1}_events.json".format(bc1 = branch_choice_one), encoding='utf-8') as events_json:
            event = json.load(events_json)
            event = event[branch_choice_two]
            
        with open("static/Resources/json/stories/{hero}.0.{bc1}_hero.json".format(hero = int(self.story.player_data[0]['hero']), bc1 = branch_choice_one), encoding='utf-8') as options_json:
            options = json.load(options_json)
            options = options[branch_choice_two]['events'][self.current_choice]['options']
            
        contents = {"event": event, "options": options}
        return contents
    
    def select_consequence(self):
        branch_choice_one = int(self.story.player_data[1]['choices']['c_3']) -1
        branch_choice_two = int(self.story.player_data[2]['choices']['c_3']) -1
        
        with open("static/Resources/json/stories/{hero}.0.{bc1}_hero.json".format(hero = int(self.story.player_data[0]['hero']), bc1 = branch_choice_one), encoding='utf-8') as options_json:
            consequence = json.load(options_json)

            if self.current_choice > 0:
                consequence = consequence[branch_choice_two]['events'][self.current_choice-1]['options'][self.story.new_choice-1]['consequence']
            else:
                consequence = consequence[branch_choice_two]['events'][3]['options'][self.story.new_choice-1]['consequence']
        
        return consequence
# FIM DO PADRÃO STRATEGY

class HpCounter:
    def __init__(self, story, choice, act, chosen):
        self.story = story
        self.choice = choice
        self.act = act
        self.chosen = chosen - 1
        
    def return_lore_dict(self):
        
        if self.act < 3:
            with open("static/Resources/json/stories/{hero}_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
                consequence = json.load(options_json)
            damage = consequence[self.act]['events'][self.choice]['options'][self.chosen]['damage']
            score = consequence[self.act]['events'][self.choice]['options'][self.chosen]['score']
            
        if self.act == 3:
            branch_choice = int(self.story.player_data[1]['choices']['c_3']) -1
            with open("static/Resources/json/stories/{hero}.0_hero.json".format(hero = int(self.story.player_data[0]['hero'])), encoding='utf-8') as options_json:
                consequence = json.load(options_json)
            damage = consequence[branch_choice]['events'][self.choice]['options'][self.chosen]['damage']
            score = consequence[branch_choice]['events'][self.choice]['options'][self.chosen]['score']
        
        if self.act == 4:
            branch_choice_one = int(self.story.player_data[1]['choices']['c_3']) -1
            branch_choice_two = int(self.story.player_data[2]['choices']['c_3']) -1
            with open("static/Resources/json/stories/{hero}.0.{bc1}_hero.json".format(hero = int(self.story.player_data[0]['hero']), bc1 = branch_choice_one), encoding='utf-8') as options_json:
                consequence = json.load(options_json)
            damage = consequence[branch_choice_two]['events'][self.choice]['options'][self.chosen]['damage']
            score = consequence[branch_choice_two]['events'][self.choice]['options'][self.chosen]['score']
                
        numbers = {"damage": damage,
                "score": score}
        return numbers

if __name__ == '__main__':
    pass