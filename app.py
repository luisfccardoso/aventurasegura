from flask import Flask, render_template, redirect, request, url_for, session
from flask_talisman import Talisman
import os
import json

app = Flask(__name__, static_folder='static')

app.secret_key = os.urandom(24)

# Configurar Talisman se estiver no Heroku
if 'DYNO' in os.environ:
    Talisman(app, content_security_policy={
        'default-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
        ],
        'style-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
        ],
    })

# Carregar cenários do arquivo JSON
with open(os.path.join(app.static_folder, 'cenarios.json'), 'r', encoding='utf-8') as f:
    cenarios = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['score'] = 0
        session['current_scenario'] = 0
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        selected_option = request.form['option']
        scenario = cenarios[session['current_scenario']]
        if selected_option == 'left':
            impact = scenario['left_choice_impact']
        else:
            impact = scenario['right_choice_impact']

        session['score'] += sum(impact.values())
        session['current_scenario'] += 1

        if session['current_scenario'] >= len(cenarios):
            final_score = session['score']
            session.clear()
            return render_template('end.html', score=final_score)

    if session['current_scenario'] < len(cenarios):
        scenario = cenarios[session['current_scenario']]
        return render_template('game.html', scenario=scenario, score=session['score'])
    else:
        final_score = session['score']
        session.clear()
        return render_template('end.html', score=final_score)

@app.route('/end')
def end():
    if 'score' not in session:
        return redirect(url_for('index'))

    final_score = session['score']
    session.clear()
    return render_template('end.html', score=final_score)

if __name__ == '__main__':
    app.run()