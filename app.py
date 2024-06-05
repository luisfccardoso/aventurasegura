from flask import Flask, render_template, redirect, request, url_for, session
from flask_talisman import Talisman
import os

app = Flask(__name__, static_folder='static')

app.secret_key = os.urandom(24)

if 'DYNO' in os.environ:  
    Talisman(app, content_security_policy={
        'default-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',  # Permita fontes externas, se necessário
        ],
        'style-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
        ],
    })

# Lista de cenários
cenarios = [
    {
        'historia': 'Você encontrou um e-mail suspeito. O que você faz?',
        'opcao1': 'Excluir sem abrir',
        'opcao2': 'Abrir e clicar no link',
        'correto': 1
    },
    {
        'historia': 'Uma pessoa desconhecida te envia uma solicitação de amizade. O que você faz?',
        'opcao1': 'Aceitar',
        'opcao2': 'Ignorar',
        'correto': 0
    }
]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        selected_option = int(request.form['option'])
        scenario = cenarios[session['current_scenario']]
        if selected_option == scenario['correto']:
            session['score'] += 30
        else:
            session['score'] -= 10
            session['lives'] -= 1

        session['current_scenario'] += 1

        if session['lives'] <= 0 or session['current_scenario'] >= len(cenarios):
            final_score = session['score']
            session.clear()
            return render_template('end.html', score=final_score)

    if session['current_scenario'] < len(cenarios):
        scenario = cenarios[session['current_scenario']]
        return render_template('game.html', scenario=scenario, score=session['score'], lives=session['lives'])
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
    app.run(debug=True)
