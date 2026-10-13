# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# PBL Fase 6 — O Começo da Rede Neural: Visão Computacional com YOLO

## 👨‍🎓 Integrantes:
- Kaique Savi (RM 562072)

## 📜 Descrição

Projeto da **Fase 6 — FIAP IA**. A FarmTech Solutions está expandindo seus
serviços de IA para a visão computacional, e este trabalho é a demonstração
prática apresentada a um cliente que quer entender como funciona — e quão
confiável é — um sistema que reconhece objetos em imagens.

A partir de um dataset de **80 imagens de dois objetos — vaca e capacete** (32 de
treino, 4 de validação e 4 de teste por classe), montado com fotos do
[Open Images Dataset](https://storage.googleapis.com/openimages/web/index.html), conferido no
[Make Sense AI](https://www.makesense.ai/) e armazenado no Google Drive, o
projeto cobre as duas entregas obrigatórias:

- **Entrega 1** — customização do **YOLOv5** para as duas classes, com duas
  simulações de treino (30 e 60 épocas), validação, teste e imagens processadas.
- **Entrega 2** — comparação do YOLO customizado com o **YOLO padrão**
  (pré-treinado no COCO) e com uma **CNN treinada do zero**, em facilidade de uso,
  precisão, tempo de treino e tempo de inferência.

### 📓 Notebook

Todo o passo a passo, os resultados e as conclusões estão no notebook:

**[`KaiqueSavi_rm562072_pbl_fase6.ipynb`](./KaiqueSavi_rm562072_pbl_fase6.ipynb)**
&nbsp; [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KaiqueSavi/fiap-inteligencia-artificial/blob/main/SEM1/FASE06/PBL/KaiqueSavi_rm562072_pbl_fase6.ipynb)

| Seção do notebook | O que você encontra |
|-------------------|---------------------|
| 1–3. Dataset | Organização no Drive, rotulação no Make Sense e conferência dos rótulos. |
| 4–5. Treinamento | As duas simulações e as curvas de acurácia e erro por época. |
| 6–7. Validação e teste | Métricas do `best.pt` de cada simulação e imagens de teste processadas. |
| 8. Conclusões da Entrega 1 | Comparação entre as simulações, pontos fortes e limitações. |
| 9–11. Abordagens concorrentes | YOLO padrão (COCO) e CNN do zero na mesma base. |
| 12. Comparação final | Avaliação crítica das três abordagens. |

### 🎥 Vídeo demonstrativo

▶️ **[Assistir no YouTube (não listado)](COLE_AQUI_O_LINK_DO_VIDEO)**

## 📁 Estrutura de pastas

```
PBL/
├── assets/
│   └── logo-fiap.png                     # Logo da FIAP para o README
├── dataset/
│   ├── images/{train,val,test}/          # 64 + 8 + 8 imagens
│   ├── labels/{train,val,test}/          # um .txt (formato YOLO) por imagem
│   ├── labels.txt                        # nomes das classes, na ordem dos rótulos
│   └── creditos_imagens.csv              # autor, link e licença de cada imagem
├── KaiqueSavi_rm562072_pbl_fase6.ipynb   # Notebook da entrega (executado no Colab)
├── build_notebook.py                     # Script que gera o notebook via nbformat
├── .gitignore
└── README.md                             # Este arquivo
```

O notebook lê o dataset do Google Drive e grava lá os resultados dos treinos:

```
MyDrive/
├── fase6_dataset/
│   ├── images/{train,val,test}/          # 64 + 8 + 8 imagens
│   └── labels/{train,val,test}/          # um .txt (formato YOLO) por imagem
└── fase6_resultados/                     # best.pt, curvas e imagens processadas (gerado pelo notebook)
```

## 🔧 Como executar o código

1. Copie a pasta `dataset/` para o seu Google Drive com o nome `fase6_dataset`.
   Se você pular este passo, o notebook faz essa cópia sozinho na primeira execução.
2. Abra o notebook no Google Colab pelo botão acima.
3. Em **Ambiente de execução → Alterar o tipo de ambiente de execução**, selecione
   **GPU (T4)**.
4. **Ambiente de execução → Executar tudo** e autorize o acesso ao Drive.

Para usar outros objetos, altere apenas `CLASSES` e `COCO_EQUIV` na célula de
configuração.

## 🖼 Créditos das imagens

As imagens são do [Open Images Dataset V7](https://storage.googleapis.com/openimages/web/index.html)
e foram publicadas por seus autores sob licença
[CC BY 2.0](https://creativecommons.org/licenses/by/2.0/); foram apenas
redimensionadas. A autoria de cada uma está em
[`dataset/creditos_imagens.csv`](./dataset/creditos_imagens.csv). As caixas
delimitadoras do Open Images são distribuídas sob CC BY 4.0.

## 🗃 Histórico de lançamentos

* 0.1.0 - 13/10/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
