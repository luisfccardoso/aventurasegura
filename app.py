import time
from flask import Flask, render_template, redirect, request, url_for, session
import os
import json

app = Flask(__name__, static_folder='static')

app.secret_key = os.urandom(24)

with open(os.path.join(app.static_folder + '/json', 'cenarios.json'), 'r', encoding='utf-8') as f:
    cenarios = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear()
        session['score'] = 0
        session['current_scenario'] = 0
        session['len'] = len(cenarios)
        return redirect(url_for('jogo'))
    return render_template('index.html')

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():

    if not all(key in session for key in ['score', 'current_scenario', 'len_cenarios']):
        return redirect(url_for('index'))
    
    current_scenario = session['current_scenario']
    if current_scenario >= session['len_cenarios']:
        return redirect(url_for('fim'))

    scenario = cenarios[current_scenario]

    if request.method == 'POST':
        selected_option = request.form['option']
        impact = scenario.get(selected_option + '_choice_impact', {})
        session['score'] += sum(impact.values())
        session['current_scenario'] += 1
        return redirect(url_for('jogo'))

    return render_template('jogo.html', scenario=scenario, score=session['score'])

@app.route('/fim')
def fim():
    if 'score' not in session:
        return redirect(url_for('index'))

    final_score = session['score']
    session.clear()
    return render_template('fim.html', score=final_score)

if __name__ == '__main__':
    app.run()