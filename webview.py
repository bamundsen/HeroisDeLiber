from flask import Flask, render_template, request, flash, redirect, make_response, jsonify
from Models.StoryLine.character_factory import Character_Type, Character_Factory
from Models.story import Story
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def first_page():
    story = Story()
    player_data = request.cookies.get('player_data')
    if player_data == None or player_data == "null":
        resp = make_response(render_template("html/form.html", main_story=story.get_main_text()))
    else:    
        resp = make_response(render_template("html/story_screen.html"))
    
    return resp

@app.route('/', methods=['POST'])
def pick_hero():
    story = Story()
    
    hero_picked = int(request.form.get('hero_picked'))
    
    resp = make_response(render_template('html/story_screen.html'))
    
    player_data = request.cookies.get('player_data')
    if player_data == None or player_data == "null":
        player_data = story.cookie_values_set(0,hero_picked)
        resp.set_cookie('player_data', json.dumps(player_data), max_age=60*60*24*365*2)
            
    return resp

@app.route('/choose', methods=['POST'])
def choose():
    
    # IMPLEMENTAR BIFURCAÇÃO NOS ATOS 2, 3 E 4
    # DANO EM TODAS AS OPÇÕES, IMPLEMENTAR CÁLCULO DE SCORE + DANO EM CADA ESCOLHA
    story = Story()
    option = request.get_json()
    option = int(option['option'])
    
    
    player_data = request.cookies.get('player_data')
    player_data = json.loads(player_data)
    player_data = story.cookie_values_set(player_data, option)
    event_content = {"event_content": story.get_event_content(json.loads(player_data), False), 
                     "consequence": story.get_consequence(json.loads(player_data), option)}
    print(event_content['consequence'])
    resp = make_response(event_content)
    resp.set_cookie('player_data', player_data, max_age=60*60*24*365*2)
    return resp

@app.route('/loadcookies', methods=['GET'])
def loadcookies():
    story = Story()
    player_data = request.cookies.get('player_data')

    if player_data == None or player_data == "null":
        return redirect("/")
    else:
        player_data = json.loads(player_data)
        event_content = {"event_content": story.get_event_content(player_data, True), 
                         "consequence": 0}
        resp = make_response(event_content)
        return resp

app.run(debug=True)