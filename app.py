import base64
import random
from flask import Flask, g, render_template, redirect, request, url_for, session
from flask_talisman import Talisman
import os
import json

app = Flask(__name__, static_folder='static')

app.secret_key = "AHGDbfsajry4233dskdnmduh1232443dsajdjasjHJD"

def gerar_nonce():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

@app.before_request
def set_nonce():
    g.nonce = gerar_nonce()

@app.after_request
def add_nonce(resposta):
    if hasattr(g, 'nonce'):
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{g.nonce}' www.googletagmanager.com www.google-analytics.com; "
            "img-src 'self' www.google-analytics.com; "
            "connect-src 'self' www.google-analytics.com; "
            "style-src 'self' 'unsafe-inline' stackpath.bootstrapcdn.com; "
        )
        resposta.headers['Content-Security-Policy'] = csp
    return resposta

if 'DYNO' in os.environ:
    Talisman(app, content_security_policy=None)

with open(os.path.join(app.static_folder + '/json', 'cenarios.json'), 'r', encoding='utf-8') as f:
    cenarios = json.load(f)
with open(os.path.join(app.static_folder + '/json', 'perfis.json'), 'r', encoding='utf-8') as f:
    perfis = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    nonce = g.get('nonce', '')
    if request.method == 'POST':
        return redirect(url_for('historia'))
    return render_template('index.html', nonce=nonce)

@app.route('/historia', methods=['GET', 'POST'])
def historia():
    nonce = g.get('nonce', '')  
    session.clear()
      
    if request.method == 'POST':
        return redirect(url_for('jogos'))
    return render_template('historia.html', nonce=nonce)

@app.route('/jogos', methods=['GET', 'POST'])
def jogos():
    nonce = g.get('nonce', '')  

    if request.method == 'POST':
        cenario = cenarios[1]

        if request.form['opcao'] == 'esquerda':
            impacto = cenario['impacto_esquerda']
            if impacto == 1:
                mensagem_feedback = cenario['consequencia_esquerda']
                titulo_feedback = "Acertou"
            else:
                mensagem_feedback = cenario['consequencia_esquerda']
                titulo_feedback = "Tente de novo!"
        else:
            impacto = cenario['impacto_direita']
            if impacto == 1:
                mensagem_feedback = cenario['consequencia_direita']
                titulo_feedback = "Acertou"
            else:
                mensagem_feedback = cenario['consequencia_direita']
                titulo_feedback = "Tente de novo!"
                
        session['pontuacao'] += impacto
        session['cenario_atual'] += 1
        
        return render_template('consequencia.html', cenario=cenario, nonce=nonce, cenario_numero=session['cenario_atual']-1,mensagem_feedback=mensagem_feedback,titulo_feedback=titulo_feedback)
    
    session['pontuacao'] = 0
    session['cenario_atual'] = 1
    random.shuffle(cenarios)
    cenario = cenarios[1]
    print('print 2')
    return render_template('jogo.html', cenario=cenario, pontuacao=session['pontuacao'], nonce=nonce, cenario_numero=session['cenario_atual'])

@app.route('/consequencia', methods=['GET', 'POST'])
def consequencia():
    nonce = g.get('nonce', '')  

    if request.method == 'POST':
        return redirect(url_for('jogo'))

    return render_template('consequencia.html', nonce=nonce)

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    nonce = g.get('nonce', '')
    if 'pontuacao' not in session:
        return redirect(url_for('historia'), code=302)
    
    cenario = cenarios[session['cenario_atual']]

    if session['cenario_atual'] > 10:
        pontuacao = session['pontuacao']
        for contador in range(11):
            if pontuacao == contador:
                perfil = perfis[contador]
                break
        return render_template('fim.html', pontuacao=pontuacao, nonce=nonce, perfil=perfil)

    if request.method == 'POST':
        if request.form['opcao'] == 'esquerda':
            impacto = cenario['impacto_esquerda']
            if impacto == 1:
                mensagem_feedback = cenario['consequencia_esquerda']
                titulo_feedback = "Acertou"
            else:
                mensagem_feedback = cenario['consequencia_esquerda']
                titulo_feedback = "Tente de novo!"
        else:
            impacto = cenario['impacto_direita']
            if impacto == 1:
                mensagem_feedback = cenario['consequencia_direita']
                titulo_feedback = "Acertou"
            else:
                mensagem_feedback = cenario['consequencia_direita']
                titulo_feedback = "Tente de novo!"
        
        session['pontuacao'] += impacto
        session['cenario_atual'] += 1

        return render_template('consequencia.html', cenario=cenario, nonce=nonce, cenario_numero=session['cenario_atual']-1,mensagem_feedback=mensagem_feedback,titulo_feedback=titulo_feedback)

    return render_template('jogo.html', cenario=cenario, pontuacao=session['pontuacao'], nonce=nonce, cenario_numero=session['cenario_atual'])

@app.route('/fim')
def fim():
    nonce = g.get('nonce', '')

    for contador in range(11):
        if session['pontuacao'] == contador:
            perfil = perfis[contador]
            break

    return render_template('fim.html', pontuacao=session['pontuacao'], nonce=nonce, perfil=perfil)

@app.route('/obrigado')
def obrigado():
    nonce = g.get('nonce', '')
    return render_template('obrigado.html', nonce=nonce)

if __name__ == '__main__':
    app.run()