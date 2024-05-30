let pontos = 0;
let desafioAtual = 0;

function startGame() {
    window.location.href = "desafios.html";
}

function loadChallenge() {
    fetch('desafios.json')
    .then(response => response.json())
    .then(data => {
        const desafio = data[desafioAtual];
        const pergunta = document.getElementById('pergunta');
        const opcoes = document.getElementById('opcoes');

        pergunta.textContent = desafio.pergunta;

        opcoes.innerHTML = '';
        desafio.opcoes.forEach((opcao, index) => {
            const button = document.createElement('button');
            button.textContent = opcao;
            button.onclick = () => checkAnswer(index);
            opcoes.appendChild(button);
        });
    });
}

function checkAnswer(resposta) {
    fetch('desafios.json')
    .then(response => response.json())
    .then(data => {
        const desafio = data[desafioAtual];
        if (resposta === desafio.resposta) {
            pontos += 30;
            alert("Resposta correta! Você ganhou 30 pontos.");
        } else {
            pontos -= 30;
            alert("Resposta incorreta! Você perdeu 30 pontos.");
        }
        desafioAtual++;
        if (desafioAtual < data.length) {
            loadChallenge();
        } else {
            alert(`Fim do jogo! Pontuação final: ${pontos}`);
            window.location.href = "index.html";
        }
    });
}
