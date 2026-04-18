"""
arquivos.py — Manipulação de arquivos (Cap. 5)

Este módulo implementa:
  * Backup/carga em JSON -> permite trabalhar offline e recuperar a sessão.
  * Exportação de relatório gerencial em TXT -> texto puro sem cores ANSI,
    pronto para ser aberto em qualquer editor ou impresso.
"""

# json: serialização/deserialização de estruturas Python <-> texto.
import json
# os.path.exists: checagem da existência do arquivo de backup.
import os
# datetime: carimbo de data/hora no cabeçalho do relatório TXT.
from datetime import datetime


# ---------------------------------------------------------------------------
# JSON (backup local, permite trabalho offline)
# ---------------------------------------------------------------------------
def salvar_backup_json(talhoes, caminho="backup_talhoes.json"):
    """Grava a lista de talhões em um arquivo JSON indentado."""
    # Abre (ou cria) o arquivo em modo de escrita, sobrescrevendo o conteúdo.
    # encoding='utf-8' garante que acentos sejam gravados corretamente.
    with open(caminho, "w", encoding="utf-8") as arquivo:
        # json.dump serializa a lista para JSON no arquivo.
        # indent=2 deixa legível para humanos.
        # ensure_ascii=False preserva caracteres acentuados (ex.: "Talhão 1").
        json.dump(talhoes, arquivo, indent=2, ensure_ascii=False)
    # Mensagem de confirmação para o usuário.
    print(f"  [OK] Backup salvo em '{caminho}' ({len(talhoes)} talhão(ões)).")


def carregar_backup_json(caminho="backup_talhoes.json"):
    """Lê o arquivo JSON e devolve a lista de talhões.

    Se o arquivo não existir, devolve uma lista vazia (situação normal
    na primeira execução).
    """
    # Primeiro checa se o arquivo existe -> evita lançar exceção por algo esperado.
    if not os.path.exists(caminho):
        # Arquivo ausente: começa com lista vazia e avisa.
        print(f"  [i] Arquivo '{caminho}' não encontrado. Começando do zero.")
        return []

    # Tenta abrir e ler o JSON.
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            # json.load deserializa o JSON para uma lista de dicts.
            talhoes = json.load(arquivo)
    except json.JSONDecodeError as erro:
        # Arquivo corrompido: informa o usuário e devolve lista vazia.
        print(f"  [!] Arquivo de backup corrompido ({erro}). Começando do zero.")
        return []

    # Avisa quantos registros foram carregados.
    print(f"  [OK] {len(talhoes)} talhão(ões) carregado(s) de '{caminho}'.")
    return talhoes


# ---------------------------------------------------------------------------
# TXT (relatório gerencial em texto puro)
# ---------------------------------------------------------------------------
def exportar_relatorio_txt(talhoes, caminho="relatorio.txt"):
    """Gera um relatório gerencial em TXT sem códigos ANSI (texto puro)."""
    # Carimbo de data/hora formatado: 18/04/2026 10:45:23.
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Abre o arquivo para escrita em UTF-8.
    with open(caminho, "w", encoding="utf-8") as arquivo:
        # --- Cabeçalho ---
        arquivo.write("=" * 98 + "\n")
        arquivo.write("RELATÓRIO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR\n")
        arquivo.write(f"Gerado em: {agora}\n")
        arquivo.write(f"Total de talhões: {len(talhoes)}\n")
        arquivo.write("=" * 98 + "\n\n")

        # --- Sem talhões: já encerra ---
        if not talhoes:
            arquivo.write("(Nenhum talhão cadastrado.)\n")
            print(f"  [OK] Relatório gerado em '{caminho}' (vazio).")
            return

        # --- Tabela ---
        # Cabeçalho da tabela (mesmas colunas do dashboard, sem cor).
        arquivo.write(f"{'ID':<6}{'NOME':<20}{'ÁREA(ha)':>10}{'TIPO':>12}"
                      f"{'ESP.(t)':>10}{'COL.(t)':>10}"
                      f"{'PERDA(t)':>10}{'PERDA(%)':>10}{'CLASSE':>10}\n")
        arquivo.write("-" * 98 + "\n")

        # Uma linha por talhão.
        for t in talhoes:
            # Decide qual ID mostrar (Oracle se sincronizado, senão local).
            id_mostrado = (f"O{t['id_oracle']}" if t.get("id_oracle") is not None
                           else f"L{t['id_local']}")
            arquivo.write(
                f"{id_mostrado:<6}{t['nome'][:19]:<20}"
                f"{t['area_ha']:>10.2f}{t['tipo_colheita']:>12}"
                f"{t['producao_esperada_t']:>10.2f}{t['producao_colhida_t']:>10.2f}"
                f"{t['perda_t']:>10.2f}{t['perda_pct']:>10.2f}"
                f"{t['classificacao']:>10}\n"
            )

        arquivo.write("-" * 98 + "\n")

        # --- Totais ---
        total_area = sum(t["area_ha"] for t in talhoes)
        total_esperado = sum(t["producao_esperada_t"] for t in talhoes)
        total_colhido = sum(t["producao_colhida_t"] for t in talhoes)
        total_perda = sum(t["perda_t"] for t in talhoes)
        pct_medio = (total_perda / total_esperado * 100.0) if total_esperado > 0 else 0.0

        arquivo.write("\nTOTAIS:\n")
        arquivo.write(f"  Área total.............: {total_area:.2f} ha\n")
        arquivo.write(f"  Produção esperada......: {total_esperado:.2f} t\n")
        arquivo.write(f"  Produção colhida.......: {total_colhido:.2f} t\n")
        arquivo.write(f"  Perda total............: {total_perda:.2f} t\n")
        arquivo.write(f"  Perda média ponderada..: {pct_medio:.2f}%\n")

        # --- Destaque: pior talhão ---
        pior = max(talhoes, key=lambda t: t["perda_pct"])
        arquivo.write("\nTALHÃO COM MAIOR PERDA PERCENTUAL:\n")
        arquivo.write(f"  {pior['nome']} -> {pior['perda_pct']:.2f}% "
                      f"(classificação: {pior['classificacao']})\n")

        # --- Contagem por classificação ---
        aceitaveis = sum(1 for t in talhoes if t["classificacao"] == "ACEITAVEL")
        atencoes   = sum(1 for t in talhoes if t["classificacao"] == "ATENCAO")
        criticos   = sum(1 for t in talhoes if t["classificacao"] == "CRITICO")
        arquivo.write("\nDISTRIBUIÇÃO POR FAIXA:\n")
        arquivo.write(f"  Aceitáveis (<=5%)........: {aceitaveis}\n")
        arquivo.write(f"  Atenção    (5%-10%)......: {atencoes}\n")
        arquivo.write(f"  Críticos   (>10%)........: {criticos}\n")

        # --- Rodapé ---
        arquivo.write("\n" + "=" * 98 + "\n")
        arquivo.write("FIAP · IA · Python — Gestão do Agronegócio\n")
        arquivo.write("=" * 98 + "\n")

    # Mensagem ao usuário após fechar o arquivo.
    print(f"  [OK] Relatório gerado em '{caminho}'.")
