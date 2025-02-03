document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tab-group li a");
    const tabContents = document.querySelectorAll(".tab-content > div");
    const signupButton = document.getElementById("signup-button");  // Certifique-se de que existe um elemento com id "signup-button"
    const telefoneInput = document.getElementById("telefone-cadastro");  // Corrigido para usar o novo id
    const placaInputs = document.querySelectorAll("#placa, #placa-cadastro");
    const modeloInput = document.getElementById("modelo");
    const nomeInput = document.getElementById("nome");
    const nomeEntradaSaidaInput = document.getElementById("nome-entrada-saida");
    const formCadastro = document.querySelector("#signup form");
    const formEntradaSaida = document.querySelector("#login form");
    const listarButtons = document.querySelectorAll(".forgot a");
  
    function showMessage(input, message) {
      let messageElement = input.parentNode.querySelector('.message');
      if (!messageElement) {
        messageElement = document.createElement('div');
        messageElement.classList.add('message');
        input.parentNode.appendChild(messageElement);
      }
      messageElement.textContent = message;
    }
  
    function clearMessage(input) {
      let messageElement = input.parentNode.querySelector('.message');
      if (messageElement) {
        messageElement.textContent = '';
      }
    }
  
    function validateForm(inputs) {
      let isValid = true;
      inputs.forEach(input => {
        if (input.value.trim() === '') {
          showMessage(input, 'Este campo é obrigatório');
          isValid = false;
        } else if (input.id === 'nome' || input.id === 'modelo') {
          if (input.value.trim().length < 3) {
            showMessage(input, 'Mínimo de 3 caracteres');
            isValid = false;
          } else {
            clearMessage(input);
          }
        } else {
          clearMessage(input);
        }
      });
      return isValid;
    }
  
    // Adicionar evento de clique para alternar entre as abas
    tabs.forEach(tab => {
        tab.addEventListener("click", function(e) {
            e.preventDefault();
  
            document.querySelectorAll(".tab-group li").forEach(li => li.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));
  
            this.parentElement.classList.add("active");
            const target = document.querySelector(this.getAttribute("href"));
            target.classList.add("active");
        });
    });
  
    // Adicionar evento de entrada para formatar o campo de telefone
    telefoneInput.addEventListener("input", function(e) {
        let value = e.target.value.replace(/\D/g, "");
  
        if (value.length > 11) {
          value = value.slice(0, 11); // Limita a 11 caracteres
          showMessage(telefoneInput, "Limite de caracteres atingido");
        } else {
          clearMessage(telefoneInput);
        }
  
        if (value.length > 6) {
            value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
        } else if (value.length > 2) {
            value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
        } else if (value.length > 0) {
            value = `(${value}`;
        }
  
        e.target.value = value;
    });
  
    telefoneInput.addEventListener("blur", function(e) {
      const value = e.target.value;
      const regex = /^\(\d{2}\) \d{5}-\d{4}$/;
      if (!regex.test(value)) {
        showMessage(telefoneInput, "Telefone Inválido");
      } else {
        clearMessage(telefoneInput);
      }
    });
  
    // Adicionar evento de entrada para limitar o campo de placa a 7 dígitos e converter para maiúsculas
    placaInputs.forEach(input => {
      input.addEventListener("input", function(e) {
        let value = e.target.value.replace(/\W/g, ""); // Remove todos os caracteres não alfanuméricos
        if (value.length > 7) {
          value = value.slice(0, 7); // Limita a 7 caracteres
          showMessage(input, "Limite de caracteres atingido");
        } else {
          clearMessage(input);
        }
        e.target.value = value.toUpperCase(); // Converte para maiúsculas
  
        if (value.length === 7) {
          const regex = /^[A-Z]{3}[0-9][A-Z][0-9]{2}$|^[A-Z]{3}[0-9]{4}$/;
          if (!regex.test(value)) {
            showMessage(input, "Placa inválida");
          } else {
            clearMessage(input);
          }
        } else if (value.length < 7 && value.length > 0) {
          clearMessage(input);
        }
      });
  
      input.addEventListener("blur", function(e) {
        const value = e.target.value;
        if (value.length === 0) {
          clearMessage(input);
          return;
        }
        const regex = /^[A-Z]{3}[0-9][A-Z][0-9]{2}$|^[A-Z]{3}[0-9]{4}$/;
        if (!regex.test(value)) {
          showMessage(input, "Placa inválida");
        } else {
          clearMessage(input);
        }
      });
  
      input.addEventListener("keydown", function(e) {
        if (e.target.value.length >= 7 && e.key !== "Backspace" && e.key !== "Delete") {
          showMessage(input, "Limite de caracteres atingido");
          e.preventDefault();
        }
      });
    });
  
    // Adicionar evento de entrada para limitar o campo de modelo do carro a 20 caracteres
    modeloInput.addEventListener("input", function(e) {
      let value = e.target.value;
      if (value.length > 20) {
        value = value.slice(0, 20); // Limita a 20 caracteres
        showMessage(modeloInput, "Limite de caracteres atingido");
      } else if (value.length < 3) {
        showMessage(modeloInput, "Mínimo de 3 caracteres");
      } else {
        clearMessage(modeloInput);
      }
      e.target.value = value; // Atualiza o valor do input
    });
  
    // Adicionar evento de entrada para limitar o campo de nome a 20 caracteres
    nomeInput.addEventListener("input", function(e) {
      let value = e.target.value;
      if (value.length > 20) {
        value = value.slice(0, 20); // Limita a 20 caracteres
        showMessage(nomeInput, "Limite de caracteres atingido");
      } else if (value.length < 3) {
        showMessage(nomeInput, "Mínimo de 3 caracteres");
      } else {
        clearMessage(nomeInput);
      }
      e.target.value = value; // Atualiza o valor do input
    });
  
    function normalizeString(str) {
      return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }
  
    formCadastro.addEventListener("submit", function(e) {
      e.preventDefault();
      const nome = document.getElementById("nome");
      const telefone = document.getElementById("telefone-cadastro");
      const placa = document.getElementById("placa-cadastro");
      const modelo = document.getElementById("modelo");
  
      if (!validateForm([nome, telefone, placa, modelo])) {
        return;
      }
  
      const telefoneRegex = /^\(\d{2}\) \d{5}-\d{4}$/;
      if (!telefoneRegex.test(telefone.value)) {
        showMessage(telefone, "Telefone Inválido");
        return;
      }
  
      const placaRegex = /^[A-Z]{3}[0-9][A-Z][0-9]{2}$|^[A-Z]{3}[0-9]{4}$/;
      if (!placaRegex.test(placa.value)) {
        showMessage(placa, "Placa inválida");
        return;
      }
  
      const dataHora = new Date().toISOString();
      const nomeNormalizado = normalizeString(nome.value);
  
      // Verificar se a placa já existe no banco de dados
      fetch(`/api/verificar_placa?placa=${placa.value}`)
        .then(response => response.json())
        .then(data => {
          if (data.exists) {
            showMessage(placa, "Placa já cadastrada");
          } else {
            // Verificar se o nome já existe no banco de dados
            fetch(`/api/verificar_nome?nome=${nomeNormalizado}`)
              .then(response => response.json())
              .then(data => {
                if (data.exists) {
                  showMessage(nome, "Nome já cadastrado");
                } else {
                  // Se o nome e a placa não existirem, prosseguir com o cadastro
                  fetch('/api/inserir_cliente_carro', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ nome: nomeNormalizado, telefone: telefone.value, placa: placa.value, marca: modelo.value, dataHora: dataHora })
                  })
                  .then(response => response.json())
                  .then(data => {
                    alert(data.message);
                  });
                }
              });
          }
        });
    });
  
    formEntradaSaida.addEventListener("submit", function(e) {
      e.preventDefault();
      const nome = document.getElementById("nome-entrada-saida");
      const placa = document.getElementById("placa");
      const transacao = document.getElementById("transacao");
  
      if (!validateForm([nome, placa, transacao])) {
        return;
      }
  
      const dataHora = new Date().toISOString();
      const nomeNormalizado = normalizeString(nome.value);
  
      // Verificar se o nome e a placa já estão cadastrados juntos
      fetch(`/api/verificar_nome_placa?nome=${nomeNormalizado}&placa=${placa.value}`)
        .then(response => response.json())
        .then(data => {
          if (!data.exists) {
            // Verificar se o nome está cadastrado
            fetch(`/api/verificar_nome?nome=${nomeNormalizado}`)
              .then(response => response.json())
              .then(nomeData => {
                if (nomeData.exists) {
                  showMessage(placa, "Placa não cadastrada");
                } else {
                  // Verificar se a placa está cadastrada
                  fetch(`/api/verificar_placa?placa=${placa.value}`)
                    .then(response => response.json())
                    .then(placaData => {
                      if (placaData.exists) {
                        showMessage(nome, "Nome não cadastrado");
                      } else {
                        showMessage(nome, "Inválido");
                        showMessage(placa, "Inválido");
                      }
                    });
                }
              });
          } else {
            // Verificar se o nome e a placa estão cadastrados juntos
            fetch(`/api/verificar_nome_placa?nome=${nomeNormalizado}&placa=${placa.value}`)
              .then(response => response.json())
              .then(nomePlacaData => {
                if (!nomePlacaData.exists) {
                  showMessage(nome, "Inválido");
                  showMessage(placa, "Inválido");
                } else {
                  // Verificar se a entrada está cadastrada antes de permitir a saída
                  if (transacao.value === "saida") {
                    fetch(`/api/verificar_entrada?placa=${placa.value}`)
                      .then(response => response.json())
                      .then(entradaData => {
                        if (!entradaData.exists) {
                          showMessage(placa, "Entrada não cadastrada");
                        } else {
                          // Se a entrada estiver cadastrada, prosseguir com o registro da saída
                          fetch('/api/registrar_entrada_saida', {
                            method: 'POST',
                            headers: {
                              'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ nome: nomeNormalizado, placa: placa.value, transacao: transacao.value, dataHora: dataHora })
                          })
                          .then(response => response.json())
                          .then(data => {
                            alert(data.message);
                          });
                        }
                      });
                  } else if (transacao.value === "entrada") {
                    // Verificar se há um registro de saída antes de permitir a entrada
                    fetch(`/api/verificar_saida?placa=${placa.value}`)
                      .then(response => response.json())
                      .then(saidaData => {
                        if (!saidaData.exists) {
                          showMessage(placa, "O veículo não tem registro de saída");
                        } else {
                          // Se houver um registro de saída, prosseguir com o registro da entrada
                          fetch('/api/registrar_entrada_saida', {
                            method: 'POST',
                            headers: {
                              'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ nome: nomeNormalizado, placa: placa.value, transacao: transacao.value, dataHora: dataHora })
                          })
                          .then(response => response.json())
                          .then(data => {
                            alert(data.message);
                          });
                        }
                      });
                  } else {
                    // Se for uma entrada, prosseguir com o registro
                    fetch('/api/registrar_entrada_saida', {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json'
                      },
                      body: JSON.stringify({ nome: nomeNormalizado, placa: placa.value, transacao: transacao.value, dataHora: dataHora })
                    })
                    .then(response => response.json())
                    .then(data => {
                      alert(data.message);
                    });
                  }
                }
              });
          }
        });
    });
  
    const listarButtonCadastro = document.querySelector("#signup .forgot a");
    const listarButtonEntradaSaida = document.querySelector("#login .forgot a");
  
    listarButtonCadastro.addEventListener("click", function(e) {
      e.preventDefault();
      fetch('/api/listar_dados')
        .then(response => response.json())
        .then(data => {
          const uniqueData = [];
          const seen = new Set();
  
          data.entradas_saidas.forEach(item => {
            const key = `${item.NOME}-${item.PLACA}-${item.MARCA}`;
            if (!seen.has(key)) {
              seen.add(key);
              uniqueData.push(item);
            }
          });
  
          // Ordenar os dados para que os mais recentes apareçam primeiro
          uniqueData.sort((a, b) => new Date(b.DT_HORA_ENTRADA) - new Date(a.DT_HORA_ENTRADA));
  
          const newTab = window.open();
          newTab.document.write(`
            <html>
              <head>
                <title>Dados Cadastrados</title>
                <style>
                  body {
                    background-color: rgba(19, 35, 47, 0.9);
                    color: white;
                    font-family: 'Titillium Web', sans-serif;
                  }
                  h1 {
                    text-align: center;
                    font-size: 24px;
                    margin: 20px 0;
                  }
                  table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                  }
                  th, td {
                    padding: 10px;
                    text-align: left;
                  }
                  th {
                    background-color: #1ab188; /* Cor do botão Voltar */
                    color: #ffffff;
                    font-size: 20px;
                    font-weight: bold;
                  }
                  td {
                    background-color: rgba(19, 35, 47, 0.9);
                    color: white;
                    font-size: 16px;
                  }
                  tr:nth-child(even) {
                    background-color: rgba(160, 179, 176, 0.25);
                  }
                  .button {
                    border: 0;
                    outline: none;
                    border-radius: 25px;
                    padding: 15px 30px; /* Aumentar o padding */
                    font-size: 1rem; /* Diminuir o tamanho da fonte */
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: .1em;
                    background: #1ab188;
                    color: #ffffff;
                    transition: all 0.5s ease;
                    appearance: none;
                    cursor: pointer;
                    margin-top: 20px;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    position: absolute;
                    bottom: 20px; /* Posicionar no fim da janela */
                    left: 50%;
                    transform: translateX(-50%);
                  }
                  .button:hover, .button:focus {
                    background: #179b77; /* Cor um pouco mais escura */
                  }
                </style>
              </head>
              <body>
                <h1>Dados Cadastrados</h1>
                <table border="1">
                  <tr>
                    <th>Nome</th>
                    <th>Telefone</th>
                    <th>Placa</th>
                    <th>Marca</th>
                  </tr>
          `);
          uniqueData.forEach(item => {
            newTab.document.write(`
              <tr>
                <td>${item.NOME}</td>
                <td>${item.TELEFONE}</td>
                <td>${item.PLACA}</td>
                <td>${item.MARCA}</td>
              </tr>
            `);
          });
          newTab.document.write(`
                </table>
                <button class="button" id="voltar-button">Voltar</button>
                <script>
                  document.getElementById('voltar-button').addEventListener('click', function() {
                    const cadastroTab = window.open('/', '_blank');
                    cadastroTab.focus();
                    window.close();
                  });
                </script>
              </body>
            </html>
          `);
          newTab.document.close();
          window.close(); // Fecha a janela principal após abrir a de listagem
        });
    });
  
    listarButtonEntradaSaida.addEventListener("click", function(e) {
      e.preventDefault();
      fetch('/api/listar_dados')
        .then(response => response.json())
        .then(data => {
          // Ordenar os dados para que os mais recentes apareçam primeiro
          data.entradas_saidas.sort((a, b) => new Date(b.DT_HORA_ENTRADA) - new Date(a.DT_HORA_ENTRADA));
  
          const newTab = window.open();
          newTab.document.write(`
            <html>
              <head>
                <title>Dados Cadastrados</title>
                <style>
                  body {
                    background-color: rgba(19, 35, 47, 0.9);
                    color: white;
                    font-family: 'Titillium Web', sans-serif;
                  }
                  h1 {
                    text-align: center;
                    font-size: 24px;
                    margin: 20px 0;
                  }
                  table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                  }
                  th, td {
                    padding: 10px;
                    text-align: left;
                  }
                  th {
                    background-color: #1ab188; /* Cor do botão Voltar */
                    color: #ffffff;
                    font-size: 20px;
                    font-weight: bold;
                  }
                  td {
                    background-color: rgba(19, 35, 47, 0.9);
                    color: white;
                    font-size: 16px;
                  }
                  tr:nth-child(even) {
                    background-color: rgba(160, 179, 176, 0.25);
                  }
                  .button {
                    border: 0;
                    outline: none;
                    border-radius: 25px;
                    padding: 15px 30px; /* Aumentar o padding */
                    font-size: 1rem; /* Diminuir o tamanho da fonte */
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: .1em;
                    background: #1ab188;
                    color: #ffffff;
                    transition: all 0.5s ease;
                    appearance: none;
                    cursor: pointer;
                    margin-top: 20px;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    position: absolute;
                    bottom: 20px; /* Posicionar no fim da janela */
                    left: 50%;
                    transform: translateX(-50%);
                  }
                  .button:hover, .button:focus {
                    background: #179b77; /* Cor um pouco mais escura */
                  }
                </style>
              </head>
              <body>
                <h1>Dados Cadastrados</h1>
                <table border="1">
                  <tr>
                    <th>Nome</th>
                    <th>Placa</th>
                    <th>Data/Hora Entrada</th>
                    <th>Data/Hora Saída</th>
                  </tr>
          `);
          data.entradas_saidas.forEach(item => {
            newTab.document.write(`
              <tr>
                <td>${item.NOME}</td>
                <td>${item.PLACA}</td>
                <td>${item.DT_HORA_ENTRADA}</td>
                <td>${item.DT_HORA_SAIDA}</td>
              </tr>
            `);
          });
          newTab.document.write(`
                </table>
                <button class="button" id="voltar-button">Voltar</button>
                <script>
                  document.getElementById('voltar-button').addEventListener('click', function() {
                    const cadastroTab = window.open('/', '_blank');
                    cadastroTab.focus();
                    window.close();
                  });
                </script>
              </body>
            </html>
          `);
          newTab.document.close();
          window.close(); // Fecha a janela principal após abrir a de listagem
        });
    });
  
    // ...existing code...
  });
  