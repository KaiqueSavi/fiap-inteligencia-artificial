# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Cap. 10 — Análise e modelagem preditiva de culturas agrícolas

## 👨‍🎓 Integrantes:
- Willian Batista De Oliveira Silva
- Daniel Corrêa
- Kaique Savi (RM 562072)
- Pedro Henrique do Nascimento
- Vinícius Camargo

## 📜 Descrição

Atividade da **Fase 3, Capítulo 10 — FIAP IA**.

A partir da base `Atividade_Cap10_produtos_agricolas.csv` (variação do *Crop
Recommendation Dataset*, com 2.200 amostras e 22 culturas perfeitamente
balanceadas), o trabalho tem quatro entregas:

1. Análise exploratória da base.
2. Análise descritiva com narrativa e, no mínimo, cinco gráficos.
3. Definição de um "perfil ideal" de solo/clima e comparação de três culturas
   escolhidas (`rice`, `mango`, `chickpea`).
4. Construção e comparação de cinco modelos preditivos que, dadas as condições
   de solo e clima, recomendam a melhor cultura.

Notebook entregue: [`KaiqueSavi_RM562072_fase3_cap10.ipynb`](./KaiqueSavi_RM562072_fase3_cap10.ipynb).

### Base de dados

Arquivo: `Atividade_Cap10_produtos_agricolas.csv` (2.200 linhas × 8 colunas).

| Variável      | Descrição |
|---------------|-----------|
| `N`           | Nitrogênio no solo |
| `P`           | Fósforo no solo |
| `K`           | Potássio no solo |
| `temperature` | Temperatura média (°C) |
| `humidity`    | Umidade média do ar (%) |
| `ph`          | pH do solo |
| `rainfall`    | Precipitação (mm) |
| `label`       | Cultura plantada (22 classes, 100 amostras cada) |

Não há valores ausentes; a base está perfeitamente balanceada (100 amostras por
cultura).

### Estrutura do notebook

| Seção                              | Conteúdo |
|------------------------------------|----------|
| 1. Setup                           | Imports, semente fixa (`random_state=42`), tema visual. |
| 2. Análise exploratória            | `shape`, `info`, `describe`, missing, contagem de classes. |
| 3. Análise descritiva (6 gráficos) | Countplot · Histogramas+KDE · Heatmap de correlação · Boxplots por cultura · Pairplot das 3 culturas · Radar normalizado. |
| 4. Perfil ideal                    | Médias globais vs médias por cultura, desvio em **z-score**, gráfico comparativo e narrativa para `rice`, `mango` e `chickpea`. |
| 5. Modelagem preditiva             | Pipeline com `StandardScaler` + 5 algoritmos, CV estratificada 5-fold, *holdout* 20%, `classification_report`, matrizes de confusão e *feature importances*. |
| 6. Conclusões                      | Pontos fortes, limitações e próximos passos. |

### Algoritmos avaliados

1. Logistic Regression (multinomial)
2. K-Nearest Neighbors (k=5)
3. Decision Tree
4. Random Forest (200 árvores)
5. Gaussian Naive Bayes

### Métricas usadas

- Acurácia (base é balanceada, então é informativa).
- **Macro F1** como métrica principal de comparação.
- `classification_report` por classe.
- Matriz de confusão para o melhor modelo e para o Gaussian NB.

### Resultados resumidos

| Modelo               | CV Acc (média) | Test Acc   | Test Macro F1 |
|----------------------|---------------:|-----------:|--------------:|
| Random Forest        | 0,9938         | **0,9955** | **0,9955**    |
| Gaussian NB          | 0,9949         | 0,9955     | 0,9954        |
| Decision Tree        | 0,9852         | 0,9795     | 0,9794        |
| KNN (k=5)            | 0,9653         | 0,9795     | 0,9793        |
| Logistic Regression  | 0,9682         | 0,9727     | 0,9725        |

Random Forest e Gaussian NB empatam virtualmente no topo. As variáveis mais
informativas, segundo o Random Forest, são `humidity`, `rainfall` e os
macronutrientes (`K`, `P`).

### Pontos fortes e limitações

**Pontos fortes:** pipeline reprodutível (semente fixa, split estratificado,
CV estratificada), pré-processamento dentro de `Pipeline` (sem *data leakage*),
comparação justa entre cinco famílias de algoritmos, análise estatística
(z-score) suportando a narrativa do perfil ideal.

**Limitações:** base sintética/limpa demais, sem outliers, missing values ou
ruído de campo; 100 amostras por classe é pouco para generalização; não há
variáveis geográficas, temporais nem econômicas; o classificador devolve um
único rótulo, embora na prática mais de uma cultura possa caber nas mesmas
condições.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto (`CAP10/`), definem-se:

```
CAP10/
├── assets/
│   └── logo-fiap.png                         # Logo da FIAP para o README
├── KaiqueSavi_RM562072_fase3_cap10.ipynb     # Notebook da entrega (executado)
├── Atividade_Cap10_produtos_agricolas.csv    # Base de dados (2.200 × 8)
├── build_notebook.py                         # Script que gera o notebook via nbformat
├── .gitignore                                # Ignora .venv e .ipynb_checkpoints
└── README.md                                 # Arquivo de documentação (este arquivo)
```

## 🔧 Como executar o código

### Opção A — Google Colab

1. Faça upload de `KaiqueSavi_RM562072_fase3_cap10.ipynb` e
   `Atividade_Cap10_produtos_agricolas.csv` em uma mesma sessão.
2. Descomente a primeira linha da célula de imports (`!pip install ...`) se
   necessário.
3. **Runtime → Run all**.

### Opção B — Local (venv)

```bash
cd SEM1/FASE3/CAP10
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip jupyter nbconvert pandas numpy scikit-learn matplotlib seaborn

# Para abrir no Jupyter:
jupyter notebook KaiqueSavi_RM562072_fase3_cap10.ipynb

# Para executar tudo no terminal:
jupyter nbconvert --to notebook --execute --inplace \
  KaiqueSavi_RM562072_fase3_cap10.ipynb \
  --ExecutePreprocessor.timeout=600
```

## 🗃 Histórico de lançamentos

* 0.1.0 - 19/05/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
