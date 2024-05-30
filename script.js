document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('start-btn');
    const playAgainBtn = document.getElementById('play-again-btn');

    const scenarios = [
        {
            historia: 'Você encontrou um e-mail suspeito. O que você faz?',
            opcao1: 'Excluir sem abrir',
            opcao2: 'Abrir e clicar no link',
            correto: 1
        },
        {
            historia: 'Uma pessoa desconhecida te envia uma solicitação de amizade. O que você faz?',
            opcao1: 'Aceitar',
            opcao2: 'Ignorar',
            correto: 0
        }
    ];

    let currentScenarioIndex = 0;
    let score = 0;
    let lives = 3;

    startBtn.addEventListener('click', function() {
        renderScenario();
    });

    playAgainBtn.addEventListener('click', function() {
        window.location.href = '/';
    });

    function renderScenario() {
        const scenario = scenarios[currentScenarioIndex];
        document.getElementById('scenario').textContent = scenario.historia;
        document.getElementById('option1').textContent = scenario.opcao1;
        document.getElementById('option2').textContent = scenario.opcao2;
        document.getElementById('score').textContent = 'Pontuação: ' + score;
        document.getElementById('lives').textContent = 'Vidas: ' + lives;

        document.getElementById('option1').addEventListener('click', function() {
            checkOption(0);
        });

        document.getElementById('option2').addEventListener('click', function() {
            checkOption(1);
        });
    }

    function checkOption(selectedOption) {
        const scenario = scenarios[currentScenarioIndex];
        if (selectedOption === scenario.correto) {
            score += 30;
        } else {
            score -= 10;
            lives -= 1;
        }

        currentScenarioIndex += 1;

        if (lives <= 0 || currentScenarioIndex >= scenarios.length) {
            document.getElementById('final-score').textContent = 'Sua pontuação final é: ' + score;
            return;
        }

        renderScenario();
    }
});
