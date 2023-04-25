#!/usr/bin/env python3
"""basic flask app"""
from typing import Dict
from flask import Flask, render_template, request, g
import flask
from flask_babel import Babel, _

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config(object):
    """config class that handles languages"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

def get_user() -> Dict:
  user_id = request.args.get('login_as')
  try:
        return users.get(int(user_id))
  except Exception:
    return None
    
@app.before_request
def before_request():
  logged_user = get_user()
  if logged_user:
    g.user = logged_user["name"]
  else:
    g.user = None

def get_locale()-> str:
  """get locale function"""
  preferred_lang = request.args.get('locale')
  # get the argument passed in locale
  if preferred_lang and preferred_lang in app.config["LANGUAGES"]:
    return preferred_lang  # return that preferred language. 
  # preffered language will be passed to the locale_selector.
  else:
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel = Babel(app, locale_selector=get_locale)


@app.route("/")
def index()-> str:
    """renders index.html"""
    return render_template("5-index.html", user=flask.g.user)

if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
