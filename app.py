import base64
from flask import Flask, g, render_template, redirect, request, url_for, session
from flask_talisman import Talisman
import os
import json

app = Flask(__name__, static_folder='static')

app.secret_key = "AHGDbfsajry4233dskdnmduh1232443dsajdjasjHJD"

def generate_nonce():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

@app.before_request
def set_nonce():
    g.nonce = generate_nonce()

@app.after_request
def add_nonce(response):
    if hasattr(g, 'nonce'):
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{g.nonce}' www.googletagmanager.com www.google-analytics.com; "
            "img-src 'self' www.google-analytics.com; "
            "connect-src 'self' www.google-analytics.com; "
            "style-src 'self' 'unsafe-inline' stackpath.bootstrapcdn.com; "
        )
        response.headers['Content-Security-Policy'] = csp
    return response

if 'DYNO' in os.environ:
    Talisman(app, content_security_policy=None)

with open(os.path.join(app.static_folder + '/json', 'cenarios.json'), 'r', encoding='utf-8') as f:
    cenarios = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    nonce = g.get('nonce', '')
    if request.method == 'POST':
        session['score'] = 0
        session['current_scenario'] = 0
        session['len'] = len(cenarios)
        return redirect(url_for('jogo'))
    return render_template('index.html', nonce=nonce)

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    nonce = g.get('nonce', '')
    if 'score' not in session:
        return redirect(url_for('index'), code=302)
    
    scenario = cenarios[session['current_scenario']]
    cenario_numero = session['current_scenario']

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
            return render_template('fim.html', score=final_score, nonce=nonce, cenario_numero=cenario_numero)

    if session['current_scenario'] < len(cenarios):
        return render_template('jogo.html', scenario=scenario, score=session['score'], nonce=nonce, cenario_numero=cenario_numero)
    else:
        final_score = session['score']
        session.clear()
        return render_template('fim.html', score=final_score, nonce=nonce, cenario_numero=cenario_numero)

@app.route('/fim')
def fim():
    nonce = g.get('nonce', '')
    if 'score' not in session:
        return redirect(url_for('index'))

    final_score = session['score']
    session.clear()
    return render_template('fim.html', score=final_score, nonce=nonce)

if __name__ == '__main__':
    app.run()