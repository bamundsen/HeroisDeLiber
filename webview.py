from flask import Flask, render_template, request, flash, redirect, make_response, jsonify
from Models.story import StoryFacade
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def first_page():
    story_facade = StoryFacade(None, None, None)
    
    player_data = request.cookies.get('player_data')
    if player_data == None or player_data == "null":
        resp = make_response(render_template("html/form.html", main_story=story_facade.game_start()))
    else:    
        resp = make_response(render_template("html/story_screen.html"))
    
    return resp

@app.route('/', methods=['POST'])
def pick_hero():
    # story = Story()
    
    # hero_picked = int(request.form.get('hero_picked'))
    
    # resp = make_response(render_template('html/story_screen.html'))
    
    # player_data = request.cookies.get('player_data')
    # if player_data == None or player_data == "null":
    #     player_data = story.cookie_values_set(0,hero_picked)
    #     resp.set_cookie('player_data', json.dumps(player_data), max_age=60*60*24*365*2)
        
    
    hero_picked = int(request.form.get('hero_picked'))
    resp = make_response(render_template('html/story_screen.html'))
    player_data = request.cookies.get('player_data')
    
    if player_data == None or player_data == "null":
        story_facade = StoryFacade(0, hero_picked, False)
        player_data = story_facade.set_save()
        resp.set_cookie('player_data', json.dumps(player_data), max_age=60*60*24*365*2)
            
    return resp

@app.route('/choose', methods=['POST'])
def choose():
    option = request.get_json()
    option = int(option['option'])
    player_data = request.cookies.get('player_data')
    player_data = json.loads(player_data)
    print(type(player_data))
    story_facade = StoryFacade(player_data, option, False)
  
    resp = make_response(story_facade.pick_choice())
    hero = story_facade.get_hero_damage()
    if hero.hp < 100:
        print ("hero is dying")
    resp.set_cookie('player_data', story_facade.display_player_data(), max_age=60*60*24*365*2)
    return resp

@app.route('/loadcookies', methods=['GET'])
def loadcookies():
    player_data = json.loads(request.cookies.get('player_data'))
    
    if player_data == None or player_data == "null":
        return redirect("/")
    else:
        story_facade = StoryFacade(player_data, -1, True)
        resp = make_response(story_facade.pick_choice())
        return resp
    
app.run(debug=True)