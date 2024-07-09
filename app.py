import base64
from random import randint, choice
from flask import Flask, g, render_template, redirect, request, url_for, session
from flask_talisman import Talisman
import os
import json 

app = Flask(__name__, static_folder='static')

app.secret_key = "sajdjsuad08y37qww67685D%!afewjrh37rt7%¨dsda"

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

def get_cenario(cenarios):
    cenario = cenarios[session['cenario_atual']]

    session['id'] = cenario['id']
    session['personagem'] = cenario['personagem']
    session['imagem'] = cenario['imagem']
    session['texto'] = cenario['texto']
    session['texto_escolha_esquerda'] = cenario['texto_escolha_esquerda']
    session['texto_escolha_direita'] = cenario['texto_escolha_direita']
    session['consequencia_esquerda'] = cenario['consequencia_esquerda']
    session['consequencia_direita'] = cenario['consequencia_direita']
    session['impacto_direita'] = cenario['impacto_direita']
    session['impacto_esquerda'] = cenario['impacto_esquerda']

@app.route('/', methods=['GET', 'POST'])
def index():
    nonce = g.get('nonce', '')
    # Escolhe aleatoriamente entre as versões A e B
    versao = choice(['a', 'b'])
    session['versao_index'] = versao  # Armazena a versão na sessão

    if request.method == 'POST':
        return redirect(url_for('historia'))
   
    return render_template(f'index_{versao}.html', nonce=nonce)


@app.route('/historia', methods=['GET', 'POST'])
def historia():
    nonce = g.get('nonce', '')  
    session.clear()
    session['cenario_atual'] = randint(1, 30)
    get_cenario(cenarios)
      
    if request.method == 'POST':
        return redirect(url_for('jogos'))
    return render_template('historia.html', nonce=nonce)

@app.route('/jogos', methods=['GET', 'POST'])
def jogos():
    nonce = g.get('nonce', '')  

    if request.method == 'POST':

        if request.form['opcao'] == 'esquerda':
            if session['impacto_esquerda'] == 1:
                session['pontuacao'] += 1
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_esquerda'],titulo_feedback="Acertou!")

            else:
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_esquerda'],titulo_feedback="Tente novamente!")

        else:
            if session['impacto_direita'] == 1:
                session['pontuacao'] += 1
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_direita'],titulo_feedback="Acertou!")

            else:
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_direita'],titulo_feedback="Tente Novamente!")

    session['pontuacao'] = 0
    session['cenario_atual'] = randint(1, 30)
    session['cenarios'] = 1

    return render_template('jogo.html', texto_escolha_direita=session['texto_escolha_direita'], texto_escolha_esquerda=session['texto_escolha_esquerda'], texto=session['texto'], imagem=session['imagem'], personagem=session['personagem'], pontuacao=session['pontuacao'], nonce=nonce, cenario_numero=session['cenarios'])

@app.route('/consequencia', methods=['GET', 'POST'])
def consequencia():
    if request.method == 'POST':
        return redirect(url_for('jogo'))

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    nonce = g.get('nonce', '')
    get_cenario(cenarios)

    if 'pontuacao' not in session:
        return redirect(url_for('historia'), code=302)
    
    if session['cenarios'] > 10:
        for contador in range(11):
            if session['pontuacao'] == contador:
                perfil = perfis[contador]
                break
        return render_template('fim.html', pontuacao=session['pontuacao'], nonce=nonce, perfil=perfil)

    if request.method == 'POST':
        if request.form['opcao'] == 'esquerda':
            if session['impacto_esquerda'] == 1:
                session['pontuacao'] += 1
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_esquerda'],titulo_feedback="Acertou!")

            else:
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_esquerda'],titulo_feedback="Tente novamente!")

        else:
            if session['impacto_direita'] == 1:
                session['pontuacao'] += 1
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_direita'],titulo_feedback="Acertou!")

            else:
                session['cenario_atual'] += 1
                session['cenarios'] += 1
                
                return render_template('consequencia.html', nonce=nonce, cenario_numero=session['cenarios']-1,mensagem_feedback=session['consequencia_direita'],titulo_feedback="Tente Novamente!")
        
    return render_template('jogo.html', texto_escolha_direita=session['texto_escolha_direita'], texto_escolha_esquerda=session['texto_escolha_esquerda'], texto=session['texto'], imagem=session['imagem'], personagem=session['personagem'], pontuacao=session['pontuacao'], nonce=nonce, cenario_numero=session['cenarios'])

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