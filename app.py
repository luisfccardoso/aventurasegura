from flask import Flask, render_template, redirect, request, url_for, session
from flask_talisman import Talisman
import os
import json

app = Flask(__name__, static_folder='static')

app.secret_key = "AHGDbfsajry4233dskdnmduh1232443dsajdjasjHJD"

if 'DYNO' in os.environ:
    Talisman(app, content_security_policy={
        'style-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
            'ajax.googleapis.com', 
            'fonts.googleapis.com',
            '*.gstatic.com'
        ],
        'script-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
            'www.googletagmanager.com',
            'code.jquery.com',
            'cdn.jsdelivr.net',
            'ajax.googleapis.com', 
            '*.googleanalytics.com ',
            '*.google-analytics.com'
        ],
        'default-src': [
            '\'self\'',
            '*.gstatic.com',
            'ajax.googleapis.com', 
            '*.googleanalytics.com ',
            '*.google-analytics.com'
            
        ],
        'font-src': [
            '\'self\'', 
            'themes.googleusercontent.com', 
            '*.gstatic.com'
        ],
        'frame-src': [
            '\'self\'', 
            'www.google.com',
            'www.youtube.com'
        ]
    })

with open(os.path.join(app.static_folder + '/json', 'cenarios.json'), 'r', encoding='utf-8') as f:
    cenarios = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['score'] = 0
        session['current_scenario'] = 0
        session['len'] = len(cenarios)
        return redirect(url_for('jogo'))
    return render_template('index.html')

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    if 'score' not in session:
        return redirect(url_for('index'), code=302)
    
    scenario = cenarios[session['current_scenario']]
    if request.method == 'POST':
        
        selected_option = request.form['option']
        if selected_option == 'left':
            impact = scenario['left_choice_impact']
        else:
            impact = scenario['right_choice_impact']

        session['score'] += sum(impact.values())
        session['current_scenario'] += 1

        if session['current_scenario'] >= len(cenarios):
            final_score = session['score']
            session.clear()
            return render_template('fim.html', score=final_score)

    if session['current_scenario'] < len(cenarios):
        return render_template('jogo.html', scenario=scenario, score=session['score'])
    else:
        final_score = session['score']
        session.clear()
        return render_template('fim.html', score=final_score)

@app.route('/fim')
def fim():
    if 'score' not in session:
        return redirect(url_for('index'))

    final_score = session['score']
    session.clear()
    return render_template('fim.html', score=final_score)

if __name__ == '__main__':
    app.run()