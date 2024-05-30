from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Initialize the database object globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    
    # Configuração do banco de dados SQLite em um arquivo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogo_seguranca.db'
    
    # Initialize the database with the app
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        # Adiciona cenários ao banco de dados se não existirem
        if Cenario.query.count() == 0:
            cenarios = [
                Cenario(imagem=url_for('static', filename='images/image1.jpg'), historia='Você encontrou um e-mail suspeito. O que você faz?',
                        opcao1='Excluir sem abrir', opcao2='Abrir e clicar no link', correto=0),
                Cenario(imagem=url_for('static', filename='images/image2.jpg'), historia='Uma pessoa desconhecida te envia uma solicitação de amizade. O que você faz?',
                        opcao1='Aceitar', opcao2='Ignorar', correto=1)
            ]
            db.session.bulk_save_objects(cenarios)
            db.session.commit()
    
    return app

# Modelo do Jogador
class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pontuacao = db.Column(db.Integer, nullable=False)
    vidas = db.Column(db.Integer, nullable=False)

# Modelo do Cenário
class Cenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(255), nullable=False)
    historia = db.Column(db.Text, nullable=False)
    opcao1 = db.Column(db.String(255), nullable=False)
    opcao2 = db.Column(db.String(255), nullable=False)
    correto = db.Column(db.Integer, nullable=False)

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['score'] = 0
        session['lives'] = 3
        session['current_scenario'] = 0
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'name' not in session:
        return redirect(url_for('index'))

    scenarios = Cenario.query.all()
    if request.method == 'POST':
        selected_option = int(request.form['option'])
        scenario = scenarios[session['current_scenario']]
        if selected_option == scenario.correto:
            session['score'] += 30
        else:
            session['score'] -= 10
            session['lives'] -= 1

        session['current_scenario'] += 1

        if session['lives'] <= 0 or session['current_scenario'] >= len(scenarios):
            jogador = Jogador(nome=session['name'], pontuacao=session['score'], vidas=session['lives'])
            db.session.add(jogador)
            db.session.commit()
            return redirect(url_for('end'))

    if session['current_scenario'] < len(scenarios):
        scenario = scenarios[session['current_scenario']]
        return render_template('game.html', scenario=scenario, score=session['score'], lives=session['lives'])
    else:
        jogador = Jogador(nome=session['name'], pontuacao=session['score'], vidas=session['lives'])
        db.session.add(jogador)
        db.session.commit()
        return redirect(url_for('end'))

@app.route('/end')
def end():
    if 'name' not in session:
        return redirect(url_for('index'))

    final_score = session['score']
    session.clear()
    return render_template('end.html', score=final_score)

if __name__ == '__main__':
    app.run(debug=True)
