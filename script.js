let currentScenarioIndex = 0;
let scenarios;

fetch('cenarios.json')
  .then(response => response.json())
  .then(data => {
    scenarios = data;
    displayScenario();
  });

function displayScenario() {
  const scenario = scenarios[currentScenarioIndex];
  document.getElementById('scenario-title').textContent = scenario.titulo;
  document.getElementById('scenario-description').textContent = scenario.descricao;

  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';

  scenario.opcoes.forEach(opcao => {
    const button = document.createElement('button');
    button.textContent = opcao.texto;
    button.onclick = () => checkAnswer(opcao.id);
    optionsDiv.appendChild(button);
  });
}

function checkAnswer(opcaoId) {
  const scenario = scenarios[currentScenarioIndex];
  const opcao = scenario.opcoes.find(opcao => opcao.id === opcaoId);

  if (opcaoId === scenario.resposta_correta) {
    displayFeedback(scenario.resposta_feedback.correta);
  } else {
    displayFeedback(scenario.resposta_feedback.incorreta);
  }
}

function displayFeedback(feedback) {
  document.getElementById('screen').innerHTML = `
    <h1>Resultado</h1>
    <p>${feedback}</p>
    <button onclick="nextScenario()">Próximo Cenário</button>
  `;
}

function nextScenario() {
  currentScenarioIndex++;
  if (currentScenarioIndex < scenarios.length) {
    displayScenario();
  } else {
    document.getElementById('screen').innerHTML = `
      <h1>Parabéns!</h1>
      <p>Você completou todos os cenários.</p>
    `;
  }
}
