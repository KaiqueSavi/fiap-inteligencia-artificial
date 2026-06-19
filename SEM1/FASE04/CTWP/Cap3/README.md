# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Fase 4 / Cap. 3 — Da Terra ao Código: Classificação de Grãos de Trigo com Machine Learning

## 👨‍🎓 Integrantes:
- Willian Batista De Oliveira Silva
- Daniel Corrêa
- Kaique Savi (RM 562072)
- Pedro Henrique do Nascimento
- Vinícius Camargo

## 📜 Descrição

Atividade **IR ALÉM** da **Fase 4, Capítulo 3 (CTWP) — FIAP IA**.

Em cooperativas agrícolas de pequeno porte, a classificação dos grãos é feita
manualmente por especialistas — processo lento e sujeito a erro humano. O objetivo
deste trabalho é aplicar a metodologia **CRISP-DM** para construir um modelo de
*machine learning* que classifique três variedades de trigo (**Kama**, **Rosa** e
**Canadian**) a partir de 7 medidas físicas do grão.

Usamos o **Seeds Dataset** do *UCI Machine Learning Repository*
([dataset 236](https://archive.ics.uci.edu/dataset/236/seeds)), com 210 amostras.
A entrega cumpre as quatro tarefas do enunciado:

1. **Analisar e pré-processar** os dados (EDA, estatísticas, ausentes, escala).
2. **Implementar e comparar** pelo menos três algoritmos de classificação (usamos
   cinco).
3. **Otimizar** os modelos com `GridSearchCV`.
4. **Interpretar** os resultados e extrair *insights* no contexto agrícola.

Notebook entregue: [`KaiqueSavi_RM562072_fase4_cap3.ipynb`](./KaiqueSavi_RM562072_fase4_cap3.ipynb).

### Base de dados

Arquivo: `seeds_dataset.csv` (210 linhas × 9 colunas). Obtido do UCI e convertido
para CSV com cabeçalho em português.

| Variável             | Descrição |
|----------------------|-----------|
| `area`               | Área do grão |
| `perimetro`          | Comprimento do contorno do grão |
| `compacidade`        | Compacidade = 4·π·área / perímetro² |
| `comprimento_nucleo` | Comprimento do eixo principal da elipse equivalente |
| `largura_nucleo`     | Comprimento do eixo secundário da elipse |
| `coef_assimetria`    | Coeficiente de assimetria do grão |
| `comprimento_sulco`  | Comprimento do sulco central do grão |
| `classe`             | Código numérico (1=Kama, 2=Rosa, 3=Canadian) |
| `variedade`          | Rótulo textual da variedade — **alvo** (70 amostras por classe) |

Não há valores ausentes e a base é **perfeitamente balanceada** (70 amostras por
variedade).

### Estrutura do notebook (CRISP-DM)

| Seção                                   | Conteúdo |
|-----------------------------------------|----------|
| 1. Setup                                | Imports, semente fixa (`random_state=42`), tema visual. |
| 2. Entendimento dos dados               | `head`, `info`, estatísticas (média, **mediana**, desvio), ausentes, balanceamento. |
| 3. Análise descritiva (6 gráficos)      | Countplot · Histogramas+KDE · Boxplots por variedade · Heatmap de correlação · Pairplot · Dispersão área×sulco. |
| 4. Preparação dos dados                 | Tratamento de ausentes e padronização (`StandardScaler` em `Pipeline`, sem *data leakage*). |
| 5. Modelagem                            | *Split* estratificado 70/30, 5 algoritmos, CV 5-fold, acurácia/precisão/recall/F1 e matrizes de confusão. |
| 6. Otimização                           | `GridSearchCV` (KNN, SVM, Random Forest) e comparação **antes × depois**. |
| 7. Interpretação e conclusões           | Feature importances, *trade-offs*, pontos fortes, limitações e próximos passos. |

### Algoritmos avaliados

1. K-Nearest Neighbors (KNN)
2. Support Vector Machine (SVM, RBF)
3. Random Forest
4. Naive Bayes (Gaussian)
5. Logistic Regression

### Métricas usadas

- Acurácia (base balanceada, então é informativa).
- **Precisão, Recall e F1 macro** para leitura por classe.
- `classification_report` por variedade.
- Matriz de confusão para o melhor modelo e para o baseline (Naive Bayes).

### Resultados resumidos

Desempenho no conjunto de teste (30% holdout, 63 amostras) **antes** da otimização:

| Modelo               | CV Acc (média) | Test Acc | Test Precisão | Test Recall | Test F1 macro |
|----------------------|---------------:|---------:|--------------:|------------:|--------------:|
| Logistic Regression  | 0,9453         | **0,9048** | 0,9048      | 0,9048      | **0,9048**    |
| KNN (k=5)            | 0,9115         | 0,8889   | 0,8887        | 0,8889      | 0,8885        |
| SVM (RBF)            | 0,9391         | 0,8889   | 0,8887        | 0,8889      | 0,8885        |
| Random Forest        | 0,9317         | 0,8413   | 0,8415        | 0,8413      | 0,8402        |
| Naive Bayes          | 0,9320         | 0,8413   | 0,8415        | 0,8413      | 0,8402        |

Após a otimização com `GridSearchCV`:

| Modelo        | Test F1 (antes) | Test F1 (depois) | Melhores parâmetros |
|---------------|----------------:|-----------------:|---------------------|
| KNN           | 0,8885          | **0,9055**       | `n_neighbors=3, weights=uniform, p=1` |
| SVM (RBF)     | 0,8885          | 0,8885           | `C=1, gamma=scale, kernel=linear` |
| Random Forest | 0,8402          | 0,8402           | `n_estimators=400, max_depth=None, min_samples_split=5` |

A **Logistic Regression** lidera antes do tuning; o **KNN otimizado**
(`n_neighbors=3`, distância de Manhattan) passa a ser o melhor depois, atingindo
F1 macro ≈ 0,906. Os poucos erros concentram-se no par **Kama × Rosa**;
**Canadian** é classificada praticamente sem erro. As variáveis mais
discriminantes (Random Forest) são as medidas de **tamanho** — `area`,
`perimetro`, `comprimento_nucleo` e `comprimento_sulco`.

### Pontos fortes e limitações

**Pontos fortes:** pipeline reprodutível (semente fixa, *split* estratificado, CV
estratificada), pré-processamento dentro de `Pipeline` (sem *data leakage*),
comparação justa entre cinco famílias de algoritmos com múltiplas métricas, e
otimização explícita com `GridSearchCV` (comparação antes × depois).

**Limitações:** base pequena (210 amostras) eleva a variância das estimativas e
limita a generalização; só há medidas geométricas do grão (sem cor, peso ou
umidade); as amostras vêm de coleta controlada, sem grãos danificados ou variação
de safra/região.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto (`Cap3/`), definem-se:

```
Cap3/
├── assets/
│   └── logo-fiap.png                        # Logo da FIAP para o README
├── KaiqueSavi_RM562072_fase4_cap3.ipynb     # Notebook da entrega (executado)
├── seeds_dataset.csv                         # Base de dados UCI Seeds (210 × 9)
├── build_notebook.py                         # Script que gera o notebook via nbformat
├── .gitignore                                # Ignora .venv e .ipynb_checkpoints
└── README.md                                 # Arquivo de documentação (este arquivo)
```

## 🔧 Como executar o código

### Opção A — Google Colab

1. Faça upload de `KaiqueSavi_RM562072_fase4_cap3.ipynb` e `seeds_dataset.csv` em
   uma mesma sessão.
2. Descomente a primeira linha da célula de imports (`!pip install ...`) se
   necessário.
3. **Runtime → Run all**.

### Opção B — Local (venv)

```bash
cd SEM1/FASE04/CTWP/Cap3
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip jupyter nbconvert pandas numpy scikit-learn matplotlib seaborn

# Para abrir no Jupyter:
jupyter notebook KaiqueSavi_RM562072_fase4_cap3.ipynb

# Para regenerar o notebook a partir do script e executá-lo no terminal:
python build_notebook.py
jupyter nbconvert --to notebook --execute --inplace \
  KaiqueSavi_RM562072_fase4_cap3.ipynb \
  --ExecutePreprocessor.timeout=600
```

## 🗃 Histórico de lançamentos

* 0.1.0 - 16/06/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
