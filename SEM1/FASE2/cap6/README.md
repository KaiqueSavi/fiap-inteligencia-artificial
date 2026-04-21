# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# **Monitoramento de Perdas na Colheita de Cana-de-Açúcar**

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/willian-batista-de-oliveira-silva/">Willian Batista De Oliveira Silva</a>
- <a href="https://www.linkedin.com/in/danielcorrea-printerx/">Daniel Corrêa</a>
- <a href="https://www.linkedin.com/in/kaique-s-16ba47206/">Kaique Savi</a>
- <a href="https://www.linkedin.com/in/pedro-henrique-do-nascimento-b86083348">Pedro Henrique do Nascimento Souza</a> 
- <a href="https://www.linkedin.com/visnowden">Vinícius Camargo</a>

## 📜 Descrição

# 🌱 Projeto PBL – Monitoramento de Perdas na Colheita de Cana-de-Açúcar

## 📌 Contexto

O agronegócio é um dos pilares da economia brasileira, envolvendo toda a cadeia produtiva — desde insumos até o consumo final. Dentro desse cenário, a cana-de-açúcar se destaca, com o Brasil liderando a produção mundial, atingindo cerca de **620 milhões de toneladas por safra**.

Apesar desse alto volume, um problema relevante impacta diretamente a produtividade: **as perdas na colheita**, especialmente na mecanizada, que podem chegar a **15%**, enquanto na manual ficam em torno de 5%. Esse desperdício representa prejuízos significativos, como cerca de **R$ 20 milhões anuais apenas no estado de São Paulo**.

---

## ❗ Problema

O produtor rural, na maioria das vezes, não possui ferramentas adequadas para:

- Identificar **onde ocorrem as maiores perdas**
- Entender **os motivos dessas perdas**
- Comparar o desempenho entre diferentes talhões
- Tomar decisões baseadas em dados

Isso dificulta a otimização do processo produtivo e reduz a eficiência da colheita.

---

## 💡 Solução Proposta

Desenvolvimento de um sistema em Python (via terminal) com foco em **gestão e análise de perdas na colheita**, atuando como uma solução no conceito de **Agrotech**.

O sistema permite:

- 📊 Cadastro de talhões com:
  - Área
  - Tipo de colheita (manual ou mecanizada)
  - Produção esperada
  - Produção real

- 📉 Cálculo automático de perdas:
  - Em toneladas
  - Em percentual

- 🚦 Classificação das perdas:
  - 🟢 Aceitável  
  - 🟡 Atenção  
  - 🔴 Crítico  

- 🖥️ Exibição de um mini-dashboard no terminal com cores ANSI

- 📄 Geração de relatórios em `.txt`

---

## 💾 Persistência de Dados

O sistema utiliza uma abordagem híbrida:

- JSON local → funcionamento offline
- Banco de dados Oracle → armazenamento estruturado e consolidação

Essa estratégia permite flexibilidade e integração com ambientes maiores.

---

## 🧠 Validação e Consistência

Todas as entradas do usuário são validadas para garantir:

- Integridade dos dados
- Evitar erros de digitação
- Confiabilidade das análises

---

## ⚙️ Tecnologias e Conceitos Aplicados

O projeto atende aos requisitos técnicos do PBL, utilizando:

- 🔹 Subalgoritmos (funções com parâmetros)
- 🔹 Estruturas de dados (listas, tuplas e dicionários)
- 🔹 Manipulação de arquivos (TXT e JSON)
- 🔹 Conexão com banco de dados Oracle

---

## 🚀 Diferencial

O sistema não se limita ao cadastro de dados — ele atua como ferramenta de apoio à decisão:

- Identifica automaticamente o **talhão com maior perda**
- Permite comparação entre áreas
- Transforma dados em informações úteis

---

## 🎯 Objetivo

Auxiliar o produtor rural a:

- Reduzir perdas na colheita
- Melhorar a tomada de decisão
- Aumentar a eficiência produtiva

---

## 📈 Conclusão

O projeto se encaixa no contexto de inovação do agronegócio, trazendo uma solução simples, mas eficiente, alinhada ao conceito de Agrotech. Ao transformar dados operacionais em insights, contribui diretamente para a melhoria da produtividade e redução de desperdícios no setor sucroenergético.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto (cap6/), definem-se:

```
cap6/
┬
├── assets
│   └── logo-fiap.png       # Logo da FIAP para README
├── config
│   ├── requirements.txt    # Dependências (oracledb)
│   └── setup.py            # Assistente de configuração
├── output
│   └── relatório.txt       # Arquivo de relatório (TXT)
├── src
│   ├── backup_talhoes.json # Arquivo de backup (JSON) — Cap. 5
│   ├── arquivos.py         # JSON (backup) e TXT (relatório) — Cap. 5
│   ├── banco.py            # CRUD Oracle e sincronização — Cap. 6
│   └── funcoes.py          # Validação, cálculo, classificação, exibição (Caps. 3 e 4)
├── main.py                 # Menu CLI e orquestração (Cap. 4: lista de dicts)
└── README.md               # Arquivo de documentação
```

## 🔧 Como executar o código

Primeiramente, rode o arquivo de setup
```
python /config/setup.py # Windows
python3 /config/setup.py # Linux
```
Uma vez configurado, execute main.py
```
python /main.py # Windows
python3 /main.py # Linux
```


## 🗃 Histórico de lançamentos

* 0.1.0 - 21/04/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


