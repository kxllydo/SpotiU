from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template, jsonify, request
from dotenv import load_dotenv

test = Flask(__name__)

@test.route("/")
def start():
    return "Hello world"

if __name__ == "__main__":
    test.run()