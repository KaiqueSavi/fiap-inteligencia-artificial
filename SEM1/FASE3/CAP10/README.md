# Cap. 10 — Análise e modelagem preditiva de culturas agrícolas

Atividade da Fase 3, Capítulo 10 — FIAP IA.

- **Aluno:** Kaique Savi
- **RM:** 562072
- **Fase / Capítulo:** 3 / 10
- **Notebook entregue:** [`KaiqueSavi_RM562072_fase3_cap10.ipynb`](./KaiqueSavi_RM562072_fase3_cap10.ipynb)

## Objetivo

A partir da base `Atividade_Cap10_produtos_agricolas.csv` (variação do *Crop
Recommendation Dataset*, com 2.200 amostras e 22 culturas perfeitamente
balanceadas), o trabalho tem quatro entregas:

1. Análise exploratória da base.
2. Análise descritiva com narrativa e, no mínimo, cinco gráficos.
3. Definição de um "perfil ideal" de solo/clima e comparação de três culturas
   escolhidas (`rice`, `mango`, `chickpea`).
4. Construção e comparação de cinco modelos preditivos que, dadas as condições
   de solo e clima, recomendam a melhor cultura.

## Base de dados

Arquivo: `Atividade_Cap10_produtos_agricolas.csv` (2.200 linhas × 8 colunas).

| Variável | Descrição |
|----------|-----------|
| `N`         | Nitrogênio no solo |
| `P`         | Fósforo no solo |
| `K`         | Potássio no solo |
| `temperature` | Temperatura média (°C) |
| `humidity`  | Umidade média do ar (%) |
| `ph`        | pH do solo |
| `rainfall`  | Precipitação (mm) |
| `label`     | Cultura plantada (22 classes, 100 amostras cada) |

Não há valores ausentes; a base está perfeitamente balanceada (100 amostras por
cultura).

## Estrutura do notebook

| Seção | Conteúdo |
|-------|----------|
| 1. Setup | Imports, semente fixa (`random_state=42`), tema visual. |
| 2. Análise exploratória | `shape`, `info`, `describe`, missing, contagem de classes. |
| 3. Análise descritiva (6 gráficos) | Countplot · Histogramas+KDE · Heatmap de correlação · Boxplots por cultura · Pairplot das 3 culturas · Radar normalizado. |
| 4. Perfil ideal | Médias globais vs médias por cultura, desvio em **z-score**, gráfico comparativo e narrativa para `rice`, `mango` e `chickpea`. |
| 5. Modelagem preditiva | Pipeline com `StandardScaler` + 5 algoritmos, CV estratificada 5-fold, *holdout* 20%, `classification_report`, matrizes de confusão e *feature importances*. |
| 6. Conclusões | Pontos fortes, limitações e próximos passos. |

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

| Modelo | CV Acc (média) | Test Acc | Test Macro F1 |
|--------|---------------:|---------:|--------------:|
| Random Forest        | 0,9938 | **0,9955** | **0,9955** |
| Gaussian NB          | 0,9949 | 0,9955 | 0,9954 |
| Decision Tree        | 0,9852 | 0,9795 | 0,9794 |
| KNN (k=5)            | 0,9653 | 0,9795 | 0,9793 |
| Logistic Regression  | 0,9682 | 0,9727 | 0,9725 |

Random Forest e Gaussian NB empatam virtualmente no topo. As variáveis mais
informativas, segundo o Random Forest, são `humidity`, `rainfall` e os
macronutrientes (`K`, `P`).

## Como reproduzir

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

## Conteúdo deste diretório

```
.
├── README.md                                 # este arquivo
├── KaiqueSavi_RM562072_fase3_cap10.ipynb     # notebook da entrega (executado)
├── Atividade_Cap10_produtos_agricolas.csv    # base de dados
├── build_notebook.py                         # script que gera o notebook via nbformat
└── .gitignore                                # ignora .venv e .ipynb_checkpoints
```

## Pontos fortes e limitações

**Pontos fortes:** pipeline reprodutível (semente fixa, split estratificado,
CV estratificada), pré-processamento dentro de `Pipeline` (sem *data leakage*),
comparação justa entre cinco famílias de algoritmos, análise estatística
(z-score) suportando a narrativa do perfil ideal.

**Limitações:** base sintética/limpa demais, sem outliers, missing values ou
ruído de campo; 100 amostras por classe é pouco para generalização; não há
variáveis geográficas, temporais nem econômicas; o classificador devolve um
único rótulo, embora na prática mais de uma cultura possa caber nas mesmas
condições.
