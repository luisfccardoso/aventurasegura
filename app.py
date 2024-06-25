import base64
import random
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

titulo_feedback = ''
mensagem_feedback = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    nonce = g.get('nonce', '')
    if request.method == 'POST':
        return redirect(url_for('historia'))
    return render_template('index.html', nonce=nonce)

@app.route('/historia', methods=['GET', 'POST'])
def historia():
    nonce = g.get('nonce', '')    
    if request.method == 'POST':
        session['score'] = 0
        session['current_scenario'] = 1
        random.shuffle(cenarios)

        return redirect(url_for('jogo'))
    return render_template('historia.html', nonce=nonce)

@app.route('/consequencia', methods=['GET', 'POST'])
def consequencia():
    nonce = g.get('nonce', '')  

    if request.method == 'POST':
        return redirect(url_for('jogo'))
    return render_template('consequencia.html', nonce=nonce)

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    nonce = g.get('nonce', '')
    if 'score' not in session:
        return redirect(url_for('historia'), code=302)
    
    cenario_numero = session['current_scenario']
    scenario = cenarios[cenario_numero]

    if cenario_numero > 10:
        final_score = session['score']
        session.clear()
        return render_template('fim.html', score=final_score, nonce=nonce, cenario_numero=cenario_numero)

    if request.method == 'POST':
        scenario = cenarios[cenario_numero]
        selected_option = request.form['option']
        
        if selected_option == 'left':
            impact = scenario['impacto_esquerda']
            if impact == 1:
                mensagem_feedback = scenario['consequencia_esquerda']
                titulo_feedback = "Acertou"
            else:
                mensagem_feedback = scenario['consequencia_esquerda']
                titulo_feedback = "Tente de novo!"
        else:
            impact = scenario['impacto_direita']
            if impact == 1:
                mensagem_feedback = scenario['consequencia_direita']
                titulo_feedback = "Acertou"
            else:
                mensagem_feedback = scenario['consequencia_direita']
                titulo_feedback = "Tente de novo!"
        
        session['score'] += impact
        session['current_scenario'] += 1

        return render_template('consequencia.html', nonce=nonce, titulo_feedback=titulo_feedback, mensagem_feedback=mensagem_feedback, cenario_numero=cenario_numero)

    return render_template('jogo.html', scenario=scenario, score=session['score'], nonce=nonce, cenario_numero=cenario_numero)

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