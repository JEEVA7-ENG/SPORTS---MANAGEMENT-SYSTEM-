# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    with sqlite3.connect('sports.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS teams 
                    (id INTEGER PRIMARY KEY, name TEXT, sport TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS athletes 
                    (id INTEGER PRIMARY KEY, name TEXT, team_id INTEGER, 
                     position TEXT, health_status TEXT, 
                     FOREIGN KEY(team_id) REFERENCES teams(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS coaches 
                    (id INTEGER PRIMARY KEY, name TEXT, team_id INTEGER, 
                     specialization TEXT,
                     FOREIGN KEY(team_id) REFERENCES teams(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS leagues 
                    (id INTEGER PRIMARY KEY, name TEXT, season TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS matches 
                    (id INTEGER PRIMARY KEY, league_id INTEGER, team1_id INTEGER, 
                     team2_id INTEGER, date TEXT, result TEXT,
                     FOREIGN KEY(league_id) REFERENCES leagues(id),
                     FOREIGN KEY(team1_id) REFERENCES teams(id),
                     FOREIGN KEY(team2_id) REFERENCES teams(id))''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

# Team Management
@app.route('/teams')
def teams():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('SELECT * FROM teams')
    teams = c.fetchall()
    conn.close()
    return render_template('teams.html', teams=teams)

@app.route('/add_team', methods=['POST'])
def add_team():
    name = request.form['name']
    sport = request.form['sport']
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('INSERT INTO teams (name, sport) VALUES (?, ?)', (name, sport))
    conn.commit()
    conn.close()
    return redirect(url_for('teams'))

# Athlete Management
@app.route('/athletes')
def athletes():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('SELECT a.*, t.name as team_name FROM athletes a LEFT JOIN teams t ON a.team_id = t.id')
    athletes = c.fetchall()
    c.execute('SELECT id, name FROM teams')
    teams = c.fetchall()
    conn.close()
    return render_template('athletes.html', athletes=athletes, teams=teams)

@app.route('/add_athlete', methods=['POST'])
def add_athlete():
    name = request.form['name']
    team_id = request.form['team_id']
    position = request.form['position']
    health_status = request.form['health_status']
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('INSERT INTO athletes (name, team_id, position, health_status) VALUES (?, ?, ?, ?)', 
              (name, team_id, position, health_status))
    conn.commit()
    conn.close()
    return redirect(url_for('athletes'))

# Coach Management
@app.route('/coaches')
def coaches():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('SELECT c.*, t.name as team_name FROM coaches c LEFT JOIN teams t ON c.team_id = t.id')
    coaches = c.fetchall()
    c.execute('SELECT id, name FROM teams')
    teams = c.fetchall()
    conn.close()
    return render_template('coaches.html', coaches=coaches, teams=teams)

@app.route('/add_coach', methods=['POST'])
def add_coach():
    name = request.form['name']
    team_id = request.form['team_id']
    specialization = request.form['specialization']
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('INSERT INTO coaches (name, team_id, specialization) VALUES (?, ?, ?)', 
              (name, team_id, specialization))
    conn.commit()
    conn.close()
    return redirect(url_for('coaches'))

# League Management
@app.route('/leagues')
def leagues():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('SELECT * FROM leagues')
    leagues = c.fetchall()
    conn.close()
    return render_template('leagues.html', leagues=leagues)

@app.route('/add_league', methods=['POST'])
def add_league():
    name = request.form['name']
    season = request.form['season']
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('INSERT INTO leagues (name, season) VALUES (?, ?)', (name, season))
    conn.commit()
    conn.close()
    return redirect(url_for('leagues'))

# Match Management
@app.route('/matches')
def matches():
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('SELECT m.*, l.name as league_name, t1.name as team1_name, t2.name as team2_name '
              'FROM matches m '
              'JOIN leagues l ON m.league_id = l.id '
              'JOIN teams t1 ON m.team1_id = t1.id '
              'JOIN teams t2 ON m.team2_id = t2.id')
    matches = c.fetchall()
    c.execute('SELECT id, name FROM leagues')
    leagues = c.fetchall()
    c.execute('SELECT id, name FROM teams')
    teams = c.fetchall()
    conn.close()
    return render_template('matches.html', matches=matches, leagues=leagues, teams=teams)

@app.route('/add_match', methods=['POST'])
def add_match():
    league_id = request.form['league_id']
    team1_id = request.form['team1_id']
    team2_id = request.form['team2_id']
    date = request.form['date']
    result = request.form['result']
    conn = sqlite3.connect('sports.db')
    c = conn.cursor()
    c.execute('INSERT INTO matches (league_id, team1_id, team2_id, date, result) VALUES (?, ?, ?, ?, ?)', 
              (league_id, team1_id, team2_id, date, result))
    conn.commit()
    conn.close()
    return redirect(url_for('matches'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)