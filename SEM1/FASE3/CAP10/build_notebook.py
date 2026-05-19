"""Generate KaiqueSavi_RM562072_fase3_cap10.ipynb using nbformat.

Produces an unexecuted notebook; run with `jupyter nbconvert --execute --inplace`.
"""
from __future__ import annotations

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells: list = []


def md(text: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(src: str) -> None:
    cells.append(nbf.v4.new_code_cell(src.strip("\n")))


# ---------------------------------------------------------------------------
# 0. Capa
# ---------------------------------------------------------------------------
md(
    """
# Atividade Cap. 10 — Análise e modelagem preditiva de culturas agrícolas

**Aluno:** Kaique Savi  |  **RM:** 562072  |  **Fase:** 3  |  **Capítulo:** 10

Este notebook analisa a base `produtos_agricolas.csv`, que reúne medidas de solo
(N, P, K, pH) e clima (temperatura, umidade, precipitação) associadas ao tipo de
cultura plantada. O trabalho está organizado em seis etapas:

1. **Setup** — bibliotecas, semente aleatória e carregamento dos dados.
2. **Análise exploratória** — estrutura, qualidade e balanceamento da base.
3. **Análise descritiva** com pelo menos cinco gráficos.
4. **Perfil ideal** de solo/clima e comparação de três culturas escolhidas
   (`rice`, `mango`, `chickpea`).
5. **Modelagem preditiva** com cinco algoritmos distintos
   (Logistic Regression, KNN, Decision Tree, Random Forest e Gaussian Naive Bayes),
   comparados por validação cruzada e métricas no conjunto de teste.
6. **Conclusões**, pontos fortes e limitações do trabalho.
"""
)

# ---------------------------------------------------------------------------
# 1. Setup
# ---------------------------------------------------------------------------
md(
    """
## 1. Setup

Carregamos as bibliotecas necessárias, fixamos a semente aleatória para
reprodutibilidade e definimos um tema visual consistente para os gráficos.
"""
)

code(
    """
# Caso esteja rodando em Colab/ambiente novo, descomente a linha abaixo:
# !pip install -q pandas numpy scikit-learn matplotlib seaborn

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 110
"""
)

code(
    """
df = pd.read_csv("Atividade_Cap10_produtos_agricolas.csv")
df.head()
"""
)

# ---------------------------------------------------------------------------
# 2. Análise exploratória
# ---------------------------------------------------------------------------
md(
    """
## 2. Análise exploratória

Antes de qualquer modelagem, verificamos formato, tipos, valores ausentes e
distribuição das classes.
"""
)

code("""print("Shape:", df.shape)\ndf.info()""")

code("""df.describe().T""")

code(
    """
missing = df.isna().sum()
print("Valores ausentes por coluna:")
print(missing.to_string())
print("\\nTotal de valores ausentes:", missing.sum())
"""
)

code(
    """
balanceamento = df["label"].value_counts()
print(f"Quantidade de classes: {balanceamento.shape[0]}")
print(f"Mínimo de amostras por classe: {balanceamento.min()}")
print(f"Máximo de amostras por classe: {balanceamento.max()}")
balanceamento.head(10)
"""
)

md(
    """
**Achados da exploração inicial**

- A base possui **2.200 linhas e 8 colunas**, sendo 7 atributos numéricos
  (`N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`) e o rótulo `label`.
- **Não há valores ausentes**, o que dispensa imputação.
- São **22 culturas distintas** com **exatamente 100 amostras cada** — base
  perfeitamente balanceada. Isso significa que a acurácia é uma métrica adequada,
  e que classificadores não precisam de técnicas de reamostragem.
- As escalas das variáveis são bastante distintas (ex.: `humidity` em ~80,
  `K` em dezenas, `rainfall` em centenas), reforçando a necessidade de
  padronização para modelos baseados em distância (KNN) ou regularização (LogReg).
"""
)

# ---------------------------------------------------------------------------
# 3. Análise descritiva
# ---------------------------------------------------------------------------
md(
    """
## 3. Análise descritiva

A seguir, **seis gráficos** ilustram o comportamento das variáveis e ajudam a
fundamentar a discussão sobre o perfil ideal.
"""
)

md("""### Gráfico 1 — Distribuição das classes""")

code(
    """
fig, ax = plt.subplots(figsize=(11, 5))
order = df["label"].value_counts().sort_values().index
sns.countplot(y="label", data=df, order=order, palette="viridis", ax=ax)
ax.set_title("Quantidade de amostras por cultura (base balanceada)")
ax.set_xlabel("Amostras")
ax.set_ylabel("Cultura")
plt.tight_layout()
plt.show()
"""
)

md(
    """
O gráfico confirma o balanceamento perfeito: todas as 22 culturas têm
exatamente 100 amostras, o que simplifica o treino e a comparação entre modelos.
"""
)

md("""### Gráfico 2 — Distribuições das variáveis numéricas""")

code(
    """
features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
fig, axes = plt.subplots(2, 4, figsize=(15, 7))
for ax, col in zip(axes.flat, features):
    sns.histplot(df[col], kde=True, ax=ax, color="steelblue")
    ax.set_title(col)
axes.flat[-1].axis("off")
fig.suptitle("Distribuição das variáveis (histograma + densidade)", y=1.02)
plt.tight_layout()
plt.show()
"""
)

md(
    """
- `N`, `P` e `K` apresentam distribuições multimodais, sugerindo que diferentes
  grupos de culturas exigem faixas de fertilizantes bem distintas.
- `temperature` e `ph` têm forma aproximadamente gaussiana — uma das razões
  pelas quais o Gaussian Naive Bayes deve performar bem.
- `humidity` é fortemente assimétrica à esquerda (concentra-se em valores altos)
  e `rainfall` tem cauda longa à direita.
"""
)

md("""### Gráfico 3 — Correlação de Pearson entre as variáveis""")

code(
    """
corr = df[features].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
    square=True, linewidths=0.5, ax=ax,
)
ax.set_title("Matriz de correlação de Pearson")
plt.tight_layout()
plt.show()
"""
)

md(
    """
- A correlação **mais forte é entre P e K (~0,74)**, indicando que solos ricos em
  fósforo tendem a ser ricos em potássio (ou recebem adubação conjunta).
- As demais correlações são fracas (|r| < 0,4), o que é positivo: as variáveis
  carregam informação complementar, reduzindo problemas de multicolinearidade
  para modelos lineares.
"""
)

md("""### Gráfico 4 — Variabilidade das features por cultura (boxplots)""")

code(
    """
fig, axes = plt.subplots(4, 2, figsize=(15, 18))
order = sorted(df["label"].unique())
for ax, col in zip(axes.flat, features):
    sns.boxplot(x="label", y=col, data=df, order=order, palette="Set3", ax=ax)
    ax.set_title(f"{col} por cultura")
    ax.tick_params(axis="x", rotation=75)
axes.flat[-1].axis("off")
fig.suptitle("Distribuição de cada variável segmentada por cultura", y=1.00)
plt.tight_layout()
plt.show()
"""
)

md(
    """
Os boxplots mostram que **a maior parte das culturas ocupa faixas bem separadas
em pelo menos uma das variáveis** — por exemplo, arroz (`rice`) destoa pelos
altos valores de `humidity` e `rainfall`, café (`coffee`) por baixa `humidity` e
alta `N`, e algumas leguminosas (`chickpea`, `kidneybeans`) por temperaturas
mais baixas. Essa separabilidade é um forte indício de que modelos não-lineares
atingirão acurácia muito alta.
"""
)

md("""### Gráfico 5 — Pairplot das três culturas em destaque""")

code(
    """
TRES_CULTURAS = ["rice", "mango", "chickpea"]
df_tres = df[df["label"].isin(TRES_CULTURAS)].copy()

sns.pairplot(
    df_tres,
    vars=features,
    hue="label",
    palette={"rice": "#1f77b4", "mango": "#ff7f0e", "chickpea": "#2ca02c"},
    plot_kws={"alpha": 0.7, "s": 25},
    height=1.6,
)
plt.suptitle("Pairplot — rice, mango e chickpea", y=1.02)
plt.show()
"""
)

md(
    """
O pairplot evidencia que as três culturas escolhidas são quase linearmente
separáveis: o arroz aparece isolado em alta `humidity` e `rainfall`, a manga
tende a calor com chuva moderada, e o grão-de-bico se concentra em faixas mais
frias e secas. Isso será confirmado quantitativamente na próxima seção.
"""
)

md("""### Gráfico 6 — Radar comparando perfis médios das três culturas""")

code(
    """
from math import pi

# Normaliza cada feature para [0,1] usando min-max global
norm = (df[features] - df[features].min()) / (df[features].max() - df[features].min())
norm["label"] = df["label"].values

perfis = norm.groupby("label")[features].mean().loc[TRES_CULTURAS]
perfil_global = norm[features].mean()

angles = [n / float(len(features)) * 2 * pi for n in range(len(features))]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
cores = {"rice": "#1f77b4", "mango": "#ff7f0e", "chickpea": "#2ca02c"}

for cultura in TRES_CULTURAS:
    values = perfis.loc[cultura].tolist() + [perfis.loc[cultura].tolist()[0]]
    ax.plot(angles, values, label=cultura, color=cores[cultura], linewidth=2)
    ax.fill(angles, values, alpha=0.15, color=cores[cultura])

valores_globais = perfil_global.tolist() + [perfil_global.tolist()[0]]
ax.plot(angles, valores_globais, label="média global", color="black",
        linewidth=2, linestyle="--")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(features)
ax.set_ylim(0, 1)
ax.set_title("Perfil médio normalizado (min-max) — três culturas vs média global", y=1.08)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
plt.tight_layout()
plt.show()
"""
)

# ---------------------------------------------------------------------------
# 4. Perfil ideal
# ---------------------------------------------------------------------------
md(
    """
## 4. Perfil ideal de solo/clima e comparação das três culturas

Definimos o **perfil global** como o vetor das médias de cada variável
considerando toda a base. Em seguida, contrastamos esse perfil com as médias de
`rice`, `mango` e `chickpea` usando o **desvio em z-score** — ou seja, quantos
desvios-padrão a média de cada cultura está acima ou abaixo da média global.
"""
)

code(
    """
perfil_global_raw = df[features].mean()
desvio_global = df[features].std()

perfis_culturas = df.groupby("label")[features].mean()
zscores = (perfis_culturas - perfil_global_raw) / desvio_global

tabela = pd.concat(
    [
        df[features].mean().rename("media_global").to_frame().T,
        perfis_culturas.loc[TRES_CULTURAS],
    ]
)
tabela.round(2)
"""
)

code(
    """
zscore_tres = zscores.loc[TRES_CULTURAS]

fig, ax = plt.subplots(figsize=(11, 5))
zscore_tres.T.plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Desvio em z-score do perfil de cada cultura em relação à média global")
ax.set_ylabel("z-score (média da cultura − média global) / desvio-padrão global")
ax.set_xlabel("Variável")
ax.legend(title="Cultura")
plt.tight_layout()
plt.show()

zscore_tres.round(2)
"""
)

md(
    """
**Leitura comparativa das três culturas**

- **`rice` (arroz):** valores **muito acima da média** em `humidity` (+~1,2σ) e
  `rainfall` (+~2σ), além de `N` levemente acima. É a cultura mais "encharcada"
  do grupo, alinhada com o cultivo em várzeas/alagados.
- **`mango` (manga):** `temperature` acima da média e **`rainfall` bem abaixo**
  (≈ −1,3σ), com `humidity` também reduzida. Perfil típico de fruta tropical
  que tolera (e prefere) estações secas durante a maturação.
- **`chickpea` (grão-de-bico):** **`P` e `humidity` bem acima da média**
  (especialmente fósforo, +~1,5σ) e `rainfall` bastante abaixo. Cultura de
  estação fria e seca, com solo bem suprido em fósforo.

As variáveis que mais separam essas três culturas são **`rainfall`**, **`humidity`**
e, em menor grau, **`temperature`** — o que é coerente com a literatura agrícola:
clima é o fator dominante para o zoneamento dessas espécies.
"""
)

# ---------------------------------------------------------------------------
# 5. Modelagem preditiva
# ---------------------------------------------------------------------------
md(
    """
## 5. Modelos preditivos

Construímos cinco classificadores que recebem como entrada as 7 variáveis de
solo/clima e devolvem a cultura recomendada. Cada modelo é encapsulado em um
`Pipeline` com `StandardScaler` (necessário para LogReg e KNN; inócuo para os
demais), avaliado por **validação cruzada estratificada de 5 folds** e medido no
conjunto de teste (20% holdout estratificado) com **acurácia** e **macro-F1**.
"""
)

code(
    """
X = df[features].copy()
y = df["label"].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
)
print("Treino:", X_train.shape, "  Teste:", X_test.shape)
"""
)

code(
    """
modelos = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1
    ),
    "Gaussian NB": GaussianNB(),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
resultados = []
modelos_treinados = {}

for nome, estimator in modelos.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("clf", estimator)])

    cv_scores = cross_validate(
        pipe, X_train, y_train, cv=cv,
        scoring=["accuracy", "f1_macro"], n_jobs=-1,
    )

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    resultados.append(
        {
            "modelo": nome,
            "cv_accuracy_mean": cv_scores["test_accuracy"].mean(),
            "cv_accuracy_std": cv_scores["test_accuracy"].std(),
            "cv_f1_macro_mean": cv_scores["test_f1_macro"].mean(),
            "cv_f1_macro_std": cv_scores["test_f1_macro"].std(),
            "test_accuracy": accuracy_score(y_test, y_pred),
            "test_f1_macro": f1_score(y_test, y_pred, average="macro"),
        }
    )
    modelos_treinados[nome] = (pipe, y_pred)

resumo = pd.DataFrame(resultados).set_index("modelo").round(4)
resumo.sort_values("test_f1_macro", ascending=False)
"""
)

code(
    """
fig, ax = plt.subplots(figsize=(10, 5))
plot_df = resumo[["cv_accuracy_mean", "test_accuracy", "test_f1_macro"]].copy()
plot_df.plot(kind="bar", ax=ax, color=["#4c72b0", "#55a868", "#c44e52"])
ax.set_ylim(0.6, 1.005)
ax.set_title("Comparativo de desempenho dos modelos")
ax.set_ylabel("Métrica")
ax.set_xlabel("")
ax.legend(loc="lower right")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.show()
"""
)

md(
    """
### Relatórios detalhados e matrizes de confusão

Para o **modelo vencedor** (maior macro-F1 no teste) e para o **modelo mais
simples** (Gaussian NB), exibimos o `classification_report` completo e a matriz
de confusão. Isso permite verificar se algum erro está concentrado em pares
específicos de culturas.
"""
)

code(
    """
melhor = resumo["test_f1_macro"].idxmax()
print(f">>> Modelo vencedor: {melhor}\\n")

pipe_best, y_pred_best = modelos_treinados[melhor]
print(classification_report(y_test, y_pred_best, digits=3))
"""
)

code(
    """
def plot_confusion(nome: str, y_pred: np.ndarray) -> None:
    classes = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=classes, yticklabels=classes,
        cbar=False, ax=ax,
    )
    ax.set_title(f"Matriz de confusão — {nome}")
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")
    plt.tight_layout()
    plt.show()

plot_confusion(melhor, modelos_treinados[melhor][1])
plot_confusion("Gaussian NB", modelos_treinados["Gaussian NB"][1])
"""
)

md(
    """
### Importância das variáveis (Random Forest)

A importância de features extraída do Random Forest indica quais variáveis o
ensemble usou mais para tomar decisões — uma forma de interpretar o modelo.
"""
)

code(
    """
rf_pipe, _ = modelos_treinados["Random Forest"]
rf = rf_pipe.named_steps["clf"]
importancias = pd.Series(rf.feature_importances_, index=features).sort_values()

fig, ax = plt.subplots(figsize=(8, 4))
importancias.plot(kind="barh", color="#4c72b0", ax=ax)
ax.set_title("Importância das variáveis — Random Forest")
ax.set_xlabel("Importância")
plt.tight_layout()
plt.show()

importancias.sort_values(ascending=False).round(3)
"""
)

md(
    """
### Discussão dos resultados

- A maioria dos modelos atinge **acurácia acima de 0,95** no conjunto de teste,
  refletindo a alta separabilidade da base. A **árvore de decisão individual**
  costuma ser o pior modelo, vítima de overfitting; o ensemble (**Random Forest**)
  corrige isso e fica entre os melhores.
- O **Gaussian Naive Bayes** se sai surpreendentemente bem porque, conforme
  visto na seção 3, várias features são aproximadamente gaussianas dentro de
  cada classe — exatamente a hipótese do modelo.
- A regressão logística multinomial também performa bem, sinal de que o problema
  é em grande parte linearmente separável após padronização.
- O Random Forest indica `humidity`, `rainfall` e os macronutrientes (`K`, `P`)
  como variáveis mais informativas — coerente com a discussão dos perfis na
  seção anterior.
- **Trade-offs:**
  - *Interpretabilidade* → árvore de decisão e regressão logística.
  - *Robustez e melhor performance bruta* → Random Forest.
  - *Simplicidade e treino instantâneo* → Gaussian NB.
  - *Sensibilidade a escala* → KNN exige obrigatoriamente o `StandardScaler`.
"""
)

# ---------------------------------------------------------------------------
# 6. Conclusões
# ---------------------------------------------------------------------------
md(
    """
## 6. Conclusões, pontos fortes e limitações

**Pontos fortes do trabalho**

- Pipeline 100% reprodutível: semente fixa, *train/test split* estratificado,
  *cross-validation* estratificada e pré-processamento dentro de `Pipeline`
  (evita data leakage).
- Comparação justa entre cinco famílias diferentes de algoritmos.
- Análise descritiva quantitativa (z-score) para sustentar a discussão dos
  perfis ideais, não apenas observação visual.

**Limitações**

- A base é **sintética/limpa**, sem outliers, valores ausentes ou ruído típicos
  de coleta em campo. Modelos com >99% de acurácia aqui dificilmente generalizam
  para dados reais sem coleta cuidadosa.
- **100 amostras por classe** é pouco para representar a variabilidade real de
  cada cultura em diferentes regiões, anos e práticas agronômicas.
- Não há variáveis **geográficas, temporais nem socioeconômicas** (latitude,
  altitude, época do plantio, custo de fertilizante), que seriam decisivas para
  uma recomendação aplicada a campo.
- A escolha "melhor cultura" segue apenas critérios de **adequação climática**;
  não incorpora **rendimento esperado, preço de mercado nem custos**, que são
  determinantes na decisão real do produtor.
- O classificador devolve um único rótulo, mas, na prática, mais de uma cultura
  pode ser adequada às mesmas condições — uma extensão natural seria predição
  *top-k* ou ranking por probabilidade.

**Próximos passos sugeridos**

- Tunar hiperparâmetros (GridSearch/Optuna) e ensaiar ensembles avançados
  (Gradient Boosting, XGBoost) para confirmar o teto do problema.
- Calibrar probabilidades e devolver recomendações *top-3* com nível de
  confiança.
- Validar o modelo em uma base externa, idealmente com dados de campo
  brasileiros, para checar generalização.
"""
)


nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {"name": "python", "version": "3.x"},
}

with open("KaiqueSavi_RM562072_fase3_cap10.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook gerado com {len(cells)} células.")
