import os
import json
import sqlite3
from flask import g
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="./server/build")
CORS(app)

DATABASE = './igm.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
@app.route('/player')
def player():
    players = query_db("SELECT * FROM player LIMIT 0,30", one=False)
    labels = ["player_id", "player_name", "belong_id"]
    players_dict = [dict(zip(labels, player)) for player in players]
    return jsonify(players_dict)

@app.route('/team')
def team():
    teams = query_db("SELECT * FROM team LIMIT 0,30", one=False)
    labels = ["team_id", "team_name"]
    teams_dict = [dict(zip(labels, team)) for team in teams]
    return jsonify(teams_dict)

@app.route('/transaction')
def transaction():
    transactions = query_db("SELECT * FROM event LIMIT 0,30", one=False)
    labels = ["transaction_id", "year", "month", "weekday", "monthday", "description", "source_id", "dest_id", "player"]
    transactions_dict = [dict(zip(labels, transaction)) for transaction in transactions]
    return jsonify(transactions_dict)

if __name__ == '__main__':
    app.run(debug=True, port=3000)