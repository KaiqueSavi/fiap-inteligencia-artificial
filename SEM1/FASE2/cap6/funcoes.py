"""
funcoes.py — Subalgoritmos e estruturas de dados (Caps. 3 e 4)

Este módulo concentra:
  * Funções de validação de entrada (robustas a erros de digitação).
  * Funções de cálculo de perdas e classificação do talhão.
  * Funções de exibição (dashboard colorido no terminal).
  * A tupla FAIXAS_CLASSIFICACAO — estrutura imutável (Cap. 4) que define
    as faixas de perda aceitável/atenção/crítico.
"""

# ---------------------------------------------------------------------------
# CONSTANTES — TUPLA IMUTÁVEL DE FAIXAS DE CLASSIFICAÇÃO (Cap. 4)
# ---------------------------------------------------------------------------
# Cada item é uma tupla (limite_superior_em_%, nome_da_faixa, codigo_ANSI_da_cor).
# A tupla externa é imutável propositalmente: faixas de classificação são
# parâmetros de negócio que não devem ser alterados em tempo de execução.
FAIXAS_CLASSIFICACAO = (
    (5.0,    "ACEITAVEL", "\033[92m"),   # Até 5% de perda -> verde (bom)
    (10.0,   "ATENCAO",   "\033[93m"),   # Entre 5% e 10%  -> amarelo (atenção)
    (999.0,  "CRITICO",   "\033[91m"),   # Acima de 10%    -> vermelho (crítico)
)

# Código ANSI para resetar a cor ao padrão do terminal após imprimir.
RESET_COR = "\033[0m"

# Conjunto de tipos de colheita válidos. Conjunto (set) permite "in" em O(1).
TIPOS_COLHEITA_VALIDOS = {"manual", "mecanica"}


# ---------------------------------------------------------------------------
# FUNÇÕES DE LEITURA DE INPUT COM VALIDAÇÃO (Cap. 3 — subalgoritmos)
# ---------------------------------------------------------------------------
def ler_str_nao_vazio(mensagem):
    """Lê uma string do teclado e só retorna quando o usuário digitar algo não-vazio."""
    # Laço que só termina quando o usuário fornecer uma entrada válida.
    while True:
        # Mostra a mensagem e captura o que o usuário digitou.
        valor = input(mensagem).strip()  # .strip() remove espaços nas pontas.
        # Se o usuário digitou algo (depois de remover espaços), devolvemos.
        if valor:
            return valor
        # Caso contrário, avisa e repete o loop.
        print("  [!] Entrada vazia. Digite um valor.")


def ler_float_positivo(mensagem):
    """Lê um número decimal >= 0. Repete até a entrada ser válida."""
    # Loop infinito que só quebra com return.
    while True:
        # Pegamos o texto digitado.
        texto = input(mensagem).strip()
        # Aceita vírgula como separador decimal (comum em pt-BR).
        texto = texto.replace(",", ".")
        try:
            # Tenta converter para float; pode lançar ValueError.
            valor = float(texto)
        except ValueError:
            # Se a conversão falhou, avisa e pede de novo.
            print("  [!] Valor inválido. Digite um número (ex.: 123.45).")
            continue  # Volta para o início do while.
        # Se o número for negativo, recusa.
        if valor < 0:
            print("  [!] Valor não pode ser negativo.")
            continue
        # Passou em todas as validações -> devolve.
        return valor


def ler_int_positivo(mensagem):
    """Lê um inteiro >= 0. Repete até a entrada ser válida."""
    while True:
        # Captura texto.
        texto = input(mensagem).strip()
        # Verifica se é composto apenas de dígitos (isdigit rejeita sinal e ponto).
        if not texto.isdigit():
            print("  [!] Digite um número inteiro não-negativo.")
            continue
        # Conversão segura (já sabemos que é só dígito).
        return int(texto)


def ler_opcao_menu(mensagem, minimo, maximo):
    """Lê um inteiro entre 'minimo' e 'maximo' (inclusivo). Útil para menus."""
    while True:
        # Reaproveitamos a leitura de inteiro.
        valor = ler_int_positivo(mensagem)
        # Checa faixa válida.
        if minimo <= valor <= maximo:
            return valor
        # Fora da faixa: avisa e pede de novo.
        print(f"  [!] Escolha uma opção entre {minimo} e {maximo}.")


def ler_tipo_colheita(mensagem):
    """Lê o tipo de colheita e garante que seja 'manual' ou 'mecanica'."""
    while True:
        # Lê uma string e padroniza para minúsculas + sem acento em 'mecânica'.
        valor = ler_str_nao_vazio(mensagem).lower().replace("â", "a")
        # Normaliza variação comum com acento.
        if valor in TIPOS_COLHEITA_VALIDOS:
            return valor
        # Informa as opções aceitas.
        print(f"  [!] Tipo inválido. Use um destes: {sorted(TIPOS_COLHEITA_VALIDOS)}.")


# ---------------------------------------------------------------------------
# FUNÇÕES DE CÁLCULO (Cap. 3 — subalgoritmos com passagem de parâmetros)
# ---------------------------------------------------------------------------
def calcular_perda_toneladas(producao_esperada, producao_colhida):
    """Retorna quanto o produtor deixou de colher, em toneladas (>= 0)."""
    # Diferença entre esperado e colhido.
    perda = producao_esperada - producao_colhida
    # Se a colheita superou o esperado, tratamos como zero de perda (não negativa).
    return max(0.0, perda)


def calcular_percentual_perda(producao_esperada, producao_colhida):
    """Retorna a perda em percentual (0 a 100). Retorna 0 se esperada == 0."""
    # Proteção contra divisão por zero (talhão ainda sem expectativa).
    if producao_esperada <= 0:
        return 0.0
    # Calcula a perda em toneladas reaproveitando a função anterior.
    perda_t = calcular_perda_toneladas(producao_esperada, producao_colhida)
    # Regra de três simples: perda / esperada * 100.
    return (perda_t / producao_esperada) * 100.0


def classificar_talhao(percentual_perda):
    """Classifica o talhão conforme a tupla FAIXAS_CLASSIFICACAO.

    Retorna uma tupla (nome_da_faixa, cor_ansi).
    """
    # Itera nas faixas em ordem crescente de severidade.
    for limite, nome, cor in FAIXAS_CLASSIFICACAO:
        # A primeira faixa cujo limite não foi ultrapassado é a resposta.
        if percentual_perda <= limite:
            return (nome, cor)
    # Fallback defensivo (não deveria acontecer porque a última faixa é 999%).
    return ("CRITICO", "\033[91m")


# ---------------------------------------------------------------------------
# FUNÇÕES DE MONTAGEM DO DICIONÁRIO "talhao" (Cap. 4 — dicionário)
# ---------------------------------------------------------------------------
def criar_talhao(id_local, nome, area_ha, tipo_colheita,
                 producao_esperada_t, producao_colhida_t, safra):
    """Constrói um dicionário representando um talhão com campos derivados já calculados."""
    # Calcula perda absoluta em toneladas.
    perda_t = calcular_perda_toneladas(producao_esperada_t, producao_colhida_t)
    # Calcula perda percentual.
    perda_pct = calcular_percentual_perda(producao_esperada_t, producao_colhida_t)
    # Descobre a faixa de classificação a partir do percentual.
    nome_faixa, _cor = classificar_talhao(perda_pct)
    # Devolve um dicionário com todos os campos (brutos + derivados).
    return {
        "id_local": id_local,                    # ID sequencial atribuído na memória.
        "id_oracle": None,                       # Preenchido após sincronizar com Oracle.
        "nome": nome,                            # Nome amigável do talhão (ex.: "Talhão 12").
        "area_ha": area_ha,                      # Área em hectares.
        "tipo_colheita": tipo_colheita,          # 'manual' ou 'mecanica'.
        "producao_esperada_t": producao_esperada_t,  # Produção planejada (t).
        "producao_colhida_t": producao_colhida_t,    # Produção efetivamente colhida (t).
        "safra": safra,                          # Rótulo da safra (ex.: "2025/2026").
        "perda_t": perda_t,                      # Perda derivada em toneladas.
        "perda_pct": perda_pct,                  # Perda derivada em %.
        "classificacao": nome_faixa,             # Faixa: ACEITAVEL/ATENCAO/CRITICO.
    }


def recalcular_talhao(talhao):
    """Recalcula campos derivados (perda_t, perda_pct, classificacao) in-place.

    Usado após edição para manter o dicionário consistente.
    """
    # Recalcula perda em toneladas.
    talhao["perda_t"] = calcular_perda_toneladas(
        talhao["producao_esperada_t"], talhao["producao_colhida_t"]
    )
    # Recalcula perda em percentual.
    talhao["perda_pct"] = calcular_percentual_perda(
        talhao["producao_esperada_t"], talhao["producao_colhida_t"]
    )
    # Recalcula classificação conforme o novo percentual.
    nome_faixa, _cor = classificar_talhao(talhao["perda_pct"])
    talhao["classificacao"] = nome_faixa
    # Retorna o próprio dicionário (conveniência para encadear chamadas).
    return talhao


# ---------------------------------------------------------------------------
# FUNÇÕES DE EXIBIÇÃO (Cap. 3 — procedimentos, sem retorno)
# ---------------------------------------------------------------------------
def _cor_para_faixa(nome_faixa):
    """Função auxiliar: a partir do nome da faixa devolve o código ANSI da cor."""
    # Itera a mesma tupla e procura o nome.
    for _limite, nome, cor in FAIXAS_CLASSIFICACAO:
        if nome == nome_faixa:
            return cor
    # Se não encontrar, usa sem cor.
    return ""


def exibir_cabecalho_tabela():
    """Imprime o cabeçalho da tabela do dashboard. Procedimento puro (sem retorno)."""
    # Linha superior.
    print("-" * 98)
    # Cabeçalho alinhado em colunas de largura fixa.
    print(f"{'ID':<4}{'NOME':<20}{'ÁREA(ha)':>10}{'TIPO':>12}"
          f"{'ESP.(t)':>10}{'COL.(t)':>10}{'PERDA(t)':>10}{'PERDA(%)':>10}{'CLASSE':>12}")
    # Linha inferior do cabeçalho.
    print("-" * 98)


def exibir_talhao(talhao):
    """Imprime uma linha do dashboard com a cor da classificação."""
    # Busca a cor correspondente à classificação armazenada.
    cor = _cor_para_faixa(talhao["classificacao"])
    # Usa id_oracle se sincronizado; caso contrário, id_local com prefixo L.
    id_mostrado = (f"O{talhao['id_oracle']}" if talhao.get("id_oracle") is not None
                   else f"L{talhao['id_local']}")
    # Monta a linha com as mesmas larguras do cabeçalho.
    linha = (f"{id_mostrado:<4}{talhao['nome'][:19]:<20}"
             f"{talhao['area_ha']:>10.2f}{talhao['tipo_colheita']:>12}"
             f"{talhao['producao_esperada_t']:>10.2f}{talhao['producao_colhida_t']:>10.2f}"
             f"{talhao['perda_t']:>10.2f}{talhao['perda_pct']:>10.2f}"
             f"{talhao['classificacao']:>12}")
    # Imprime aplicando cor de abertura e reset no final (para não "vazar" cor).
    print(f"{cor}{linha}{RESET_COR}")


def exibir_dashboard(talhoes):
    """Imprime o dashboard completo com todos os talhões + totalizadores."""
    # Caso de lista vazia: apenas avisa.
    if not talhoes:
        print("  (Nenhum talhão cadastrado ainda.)")
        return

    # Cabeçalho.
    exibir_cabecalho_tabela()
    # Linha por talhão.
    for t in talhoes:
        exibir_talhao(t)
    # Divisor antes dos totais.
    print("-" * 98)

    # Calcula totais agregados.
    total_area = sum(t["area_ha"] for t in talhoes)
    total_esperado = sum(t["producao_esperada_t"] for t in talhoes)
    total_colhido = sum(t["producao_colhida_t"] for t in talhoes)
    total_perda = sum(t["perda_t"] for t in talhoes)
    # Percentual médio ponderado: perda_total / esperado_total.
    pct_medio = (total_perda / total_esperado * 100.0) if total_esperado > 0 else 0.0

    # Identifica o pior talhão (maior perda_pct) para destaque gerencial.
    pior = max(talhoes, key=lambda t: t["perda_pct"])

    # Imprime totais.
    print(f"TOTAIS: área={total_area:.2f} ha | esperado={total_esperado:.2f} t | "
          f"colhido={total_colhido:.2f} t | perda={total_perda:.2f} t | "
          f"% médio={pct_medio:.2f}%")
    # Destaca o pior talhão (com cor da classificação dele).
    cor_pior = _cor_para_faixa(pior["classificacao"])
    print(f"PIOR TALHÃO: {cor_pior}{pior['nome']} "
          f"({pior['perda_pct']:.2f}% - {pior['classificacao']}){RESET_COR}")
    # Rodapé final.
    print("-" * 98)
