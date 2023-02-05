from flask import Flask, render_template, request, flash, redirect, make_response, url_for
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
  
    hero_picked = int(request.form.get('hero_picked'))
    resp = make_response(render_template('html/story_screen.html'))
    player_data = request.cookies.get('player_data')
    
    if player_data == None or player_data == "null":
        story_facade = StoryFacade(0, hero_picked, False)
        player_data = story_facade.set_save()
        resp.set_cookie('player_data', json.dumps(player_data), max_age=60*60*24*365*2)
            
    return resp

@app.route('/choose', methods=['GET','POST'])
def choose():
    option = request.get_json()
    option = int(option['option'])
    player_data = request.cookies.get('player_data')
    player_data = json.loads(player_data)
    story_facade = StoryFacade(player_data, option, False)
    content_response = story_facade.pick_choice()
  
    if story_facade.story.is_history_finished == False:
        resp = make_response(content_response)
        resp.set_cookie('player_data', story_facade.display_player_data(), max_age=60*60*24*365*2)
    
    else:
        print("RENDOU SQN")
        resp = make_response({'end': "yes"})
        resp.set_cookie('player_data', story_facade.display_player_data(), max_age=60*60*24*365*2)
        # resp = redirect("html/ending.html")
        # resp.delete_cookie('player_data')

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

@app.route('/storyend', methods=['GET'])
def story_end():
    # return redirect(url_for("html/ending.html"))
    try:
        player_data = json.loads(request.cookies.get('player_data'))
    except:
        return redirect("/")
    else:
        print(player_data)
        resp = make_response(render_template("html/ending.html"))
        resp.delete_cookie('player_data')
        return resp

app.run(debug=True)