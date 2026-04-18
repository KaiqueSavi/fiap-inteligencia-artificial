"""
main.py — Ponto de entrada da aplicação CLI

Orquestra:
  * O menu principal (loop com match/case).
  * A tabela em memória: lista de dicionários (Cap. 4).
  * Delega cálculos/validação para funcoes.py (Cap. 3/4).
  * Delega persistência em arquivos para arquivos.py (Cap. 5).
  * Delega CRUD com Oracle para banco.py (Cap. 6).

Na inicialização tenta conectar ao Oracle. Se a rede da FIAP não estiver
acessível, segue em "modo offline" — apenas as opções de Oracle ficam
bloqueadas. Todas as demais continuam funcionando.
"""

# os: utilizado para limpar a tela de forma portátil entre Windows e Unix.
import os

# Importamos apenas o que vamos usar, com nomes explícitos para legibilidade.
from funcoes import (
    ler_str_nao_vazio,
    ler_float_positivo,
    ler_opcao_menu,
    ler_tipo_colheita,
    criar_talhao,
    recalcular_talhao,
    exibir_dashboard,
)
from arquivos import (
    salvar_backup_json,
    carregar_backup_json,
    exportar_relatorio_txt,
)
# O módulo banco inteiro é importado com alias para deixar claro quando
# estamos tocando o banco vs. a lógica local.
import banco


# ---------------------------------------------------------------------------
# UTILIDADES DE UI
# ---------------------------------------------------------------------------
def limpar_tela():
    """Limpa a tela do terminal de forma compatível com Windows e Unix (macOS/Linux)."""
    # No Windows o comando é 'cls'; nos demais Unix é 'clear'.
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa até o usuário apertar Enter. Útil entre ações do menu."""
    # input devolve a linha digitada; aqui só queremos o "Enter".
    input("\nPressione ENTER para voltar ao menu...")


def mostrar_menu(conn_ativa):
    """Imprime o cabeçalho e as opções do menu principal.

    'conn_ativa' indica se há conexão com o Oracle. As opções de sincronização
    ficam marcadas como indisponíveis quando não há conexão.
    """
    print("=" * 60)
    print("  FIAP · IA · PYTHON — GESTÃO DO AGRONEGÓCIO")
    print("  Perdas na colheita mecanizada de cana-de-açúcar")
    print("=" * 60)
    # Sufixo que aparece nas opções 8 e 9 quando não há conexão.
    sufixo_oracle = "" if conn_ativa else "  [indisponível - sem conexão Oracle]"
    print("""
  1 - Cadastrar talhão
  2 - Listar talhões / Dashboard
  3 - Editar talhão
  4 - Excluir talhão
  5 - Exportar relatório TXT
  6 - Salvar backup JSON
  7 - Carregar backup JSON""")
    # As duas opções de Oracle são impressas com o sufixo indicativo.
    print(f"  8 - Sincronizar: memória -> Oracle{sufixo_oracle}")
    print(f"  9 - Sincronizar: Oracle -> memória{sufixo_oracle}")
    print("  0 - Sair")
    print("=" * 60)


# ---------------------------------------------------------------------------
# AÇÕES DO MENU (cada opção em uma função separada — Cap. 3: procedimentos)
# ---------------------------------------------------------------------------
def acao_cadastrar(talhoes, proximo_id_local):
    """Coleta os dados do usuário e adiciona um novo talhão à lista em memória.

    Retorna o novo valor de proximo_id_local (incrementado).
    """
    print("\n-- Cadastro de Talhão --")
    # Lê cada campo usando as funções validadas de funcoes.py.
    nome = ler_str_nao_vazio("  Nome do talhão: ")
    area_ha = ler_float_positivo("  Área (ha): ")
    tipo = ler_tipo_colheita("  Tipo de colheita (manual/mecanica): ")
    prod_esp = ler_float_positivo("  Produção esperada (t): ")
    prod_col = ler_float_positivo("  Produção colhida (t): ")
    safra = ler_str_nao_vazio("  Safra (ex.: 2025/2026): ")

    # Cria o dict já com campos derivados calculados.
    novo = criar_talhao(
        id_local=proximo_id_local,
        nome=nome,
        area_ha=area_ha,
        tipo_colheita=tipo,
        producao_esperada_t=prod_esp,
        producao_colhida_t=prod_col,
        safra=safra,
    )
    # Adiciona à lista em memória (nossa "tabela" — Cap. 4).
    talhoes.append(novo)
    print(f"\n  [OK] Talhão '{nome}' cadastrado com id_local L{proximo_id_local} "
          f"(perda: {novo['perda_pct']:.2f}% - {novo['classificacao']}).")
    # Próximo id é o atual + 1.
    return proximo_id_local + 1


def acao_listar(talhoes):
    """Mostra o dashboard com todos os talhões e totais."""
    print("\n-- Dashboard de Talhões --\n")
    exibir_dashboard(talhoes)


def _selecionar_talhao(talhoes):
    """Ajuda a escolher um talhão pela posição na lista. Retorna o índice ou None."""
    # Mostra a lista primeiro para o usuário ver as opções.
    exibir_dashboard(talhoes)
    # Se não há nada, já retorna.
    if not talhoes:
        return None
    # Pede o id_local (L<n>) para selecionar.
    print()
    id_local = ler_opcao_menu(
        f"  Digite o id_local (1..{len(talhoes)}) do talhão: ",
        1, max(t["id_local"] or 0 for t in talhoes)
    )
    # Busca o índice na lista correspondente ao id_local escolhido.
    for indice, t in enumerate(talhoes):
        if t["id_local"] == id_local:
            return indice
    # Não achou — situação improvável, mas tratada.
    print("  [!] Talhão não encontrado.")
    return None


def acao_editar(talhoes, conn):
    """Edita um talhão existente. Se estiver sincronizado, atualiza também o Oracle."""
    print("\n-- Edição de Talhão --")
    # Escolhe qual registro editar.
    indice = _selecionar_talhao(talhoes)
    if indice is None:
        return

    # Pega referência ao dict escolhido.
    talhao = talhoes[indice]
    print(f"\n  Editando '{talhao['nome']}' — deixe em branco para manter o valor atual.\n")

    # Para cada campo editável, perguntamos; entrada vazia mantém o valor antigo.
    # (Aqui usamos input direto porque precisamos detectar "vazio" — as funções
    # de funcoes.py recusam vazio propositalmente.)
    novo_nome = input(f"  Nome [{talhao['nome']}]: ").strip() or talhao["nome"]

    texto_area = input(f"  Área ha [{talhao['area_ha']}]: ").strip().replace(",", ".")
    nova_area = float(texto_area) if texto_area else talhao["area_ha"]

    novo_tipo = input(f"  Tipo [{talhao['tipo_colheita']}] (manual/mecanica): ").strip().lower()
    novo_tipo = novo_tipo.replace("â", "a") or talhao["tipo_colheita"]
    # Se digitou algo inválido, mantém o valor antigo para não corromper dado.
    if novo_tipo not in {"manual", "mecanica"}:
        print(f"  [!] Tipo inválido; mantendo '{talhao['tipo_colheita']}'.")
        novo_tipo = talhao["tipo_colheita"]

    texto_esp = input(f"  Produção esperada t [{talhao['producao_esperada_t']}]: ").strip().replace(",", ".")
    nova_esp = float(texto_esp) if texto_esp else talhao["producao_esperada_t"]

    texto_col = input(f"  Produção colhida t [{talhao['producao_colhida_t']}]: ").strip().replace(",", ".")
    nova_col = float(texto_col) if texto_col else talhao["producao_colhida_t"]

    nova_safra = input(f"  Safra [{talhao['safra']}]: ").strip() or talhao["safra"]

    # Aplica as alterações no dicionário.
    talhao["nome"] = novo_nome
    talhao["area_ha"] = nova_area
    talhao["tipo_colheita"] = novo_tipo
    talhao["producao_esperada_t"] = nova_esp
    talhao["producao_colhida_t"] = nova_col
    talhao["safra"] = nova_safra

    # Recalcula os campos derivados (perda_t, perda_pct, classificação).
    recalcular_talhao(talhao)

    # Se o talhão está sincronizado com Oracle, atualiza também no banco.
    if talhao.get("id_oracle") is not None and conn is not None:
        try:
            afetadas = banco.atualizar_talhao(conn, talhao["id_oracle"], talhao)
            print(f"\n  [OK] Alterações salvas (memória + Oracle, {afetadas} linha afetada).")
        except Exception as erro:
            # Se falhou o UPDATE no Oracle, avisa mas mantém a edição em memória.
            print(f"\n  [!] Editado em memória, mas falhou no Oracle: {erro}")
    else:
        print("\n  [OK] Alterações salvas em memória.")


def acao_excluir(talhoes, conn):
    """Remove um talhão da memória e, se aplicável, do Oracle."""
    print("\n-- Exclusão de Talhão --")
    indice = _selecionar_talhao(talhoes)
    if indice is None:
        return

    # Pega referência antes de remover.
    talhao = talhoes[indice]
    # Confirmação textual do usuário (segurança contra exclusão acidental).
    print(f"\n  Confirma exclusão de '{talhao['nome']}'? (digite 'sim' para confirmar)")
    if input("  > ").strip().lower() != "sim":
        print("  [i] Exclusão cancelada.")
        return

    # Se está sincronizado com Oracle, remove lá primeiro.
    if talhao.get("id_oracle") is not None and conn is not None:
        try:
            banco.excluir_talhao(conn, talhao["id_oracle"])
            print(f"  [OK] Excluído do Oracle (id={talhao['id_oracle']}).")
        except Exception as erro:
            print(f"  [!] Falha ao excluir do Oracle: {erro}")
            return  # Interrompe para não deixar inconsistência.

    # Remove da memória.
    talhoes.pop(indice)
    print("  [OK] Excluído da memória.")


def acao_exportar_txt(talhoes):
    """Gera o arquivo relatorio.txt com resumo gerencial."""
    print("\n-- Exportar Relatório TXT --")
    exportar_relatorio_txt(talhoes)


def acao_salvar_json(talhoes):
    """Salva o estado atual em backup_talhoes.json."""
    print("\n-- Salvar Backup JSON --")
    salvar_backup_json(talhoes)


def acao_carregar_json():
    """Lê backup_talhoes.json e devolve a lista + próximo id_local."""
    print("\n-- Carregar Backup JSON --")
    # Lê do arquivo.
    talhoes = carregar_backup_json()
    # Se o backup veio vazio, próximo id é 1; senão, maior id existente + 1.
    if talhoes:
        proximo_id = max((t.get("id_local") or 0) for t in talhoes) + 1
    else:
        proximo_id = 1
    # Devolve para main substituir o estado atual pelo carregado.
    return talhoes, proximo_id


def acao_sync_local_para_oracle(talhoes, conn):
    """Envia para o Oracle os talhões ainda não sincronizados."""
    print("\n-- Sincronizar: memória -> Oracle --")
    # Sem conexão, não há o que fazer.
    if conn is None:
        print("  [!] Sem conexão com Oracle. Tente reiniciar o programa.")
        return
    try:
        enviados = banco.sincronizar_local_para_oracle(conn, talhoes)
        print(f"  [OK] {enviados} talhão(ões) enviado(s) ao Oracle.")
    except Exception as erro:
        print(f"  [!] Falha na sincronização: {erro}")


def acao_sync_oracle_para_local(conn):
    """Puxa todos os talhões do Oracle e devolve como nova lista."""
    print("\n-- Sincronizar: Oracle -> memória --")
    if conn is None:
        print("  [!] Sem conexão com Oracle. Tente reiniciar o programa.")
        return None, None
    try:
        talhoes = banco.sincronizar_oracle_para_local(conn)
        proximo_id = (len(talhoes) + 1) if talhoes else 1
        print(f"  [OK] {len(talhoes)} talhão(ões) carregado(s) do Oracle.")
        return talhoes, proximo_id
    except Exception as erro:
        print(f"  [!] Falha na sincronização: {erro}")
        return None, None


# ---------------------------------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    """Ponto de entrada. Inicializa estado, conecta, roda o menu até o usuário sair."""
    # Estado em memória — lista de dicts (Cap. 4).
    talhoes = []
    # Contador de id_local sequencial. Começa em 1.
    proximo_id_local = 1

    # Tenta conectar ao Oracle. Se falhar, segue em modo offline.
    conn = None
    print("Conectando ao Oracle da FIAP...")
    try:
        conn = banco.conectar()
        # Garante a tabela no primeiro uso (idempotente).
        banco.garantir_tabela(conn)
        print("  [OK] Conectado.\n")
    except Exception as erro:
        # Aviso — mas não impede o uso local.
        print(f"  [!] Sem conexão Oracle (modo offline). Detalhe: {erro}\n")

    # Loop principal do menu.
    while True:
        # Limpa a tela a cada volta para manter a UI organizada.
        limpar_tela()
        # Mostra o menu (com ou sem Oracle).
        mostrar_menu(conn_ativa=(conn is not None))
        # Lê a escolha (0 a 9).
        escolha = ler_opcao_menu("  Escolha -> ", 0, 9)

        # Limpa novamente antes de executar a ação para destacar a saída dela.
        limpar_tela()

        # Despacha a ação escolhida usando match/case (Python 3.10+).
        match escolha:
            case 1:
                proximo_id_local = acao_cadastrar(talhoes, proximo_id_local)
                pausar()
            case 2:
                acao_listar(talhoes)
                pausar()
            case 3:
                acao_editar(talhoes, conn)
                pausar()
            case 4:
                acao_excluir(talhoes, conn)
                pausar()
            case 5:
                acao_exportar_txt(talhoes)
                pausar()
            case 6:
                acao_salvar_json(talhoes)
                pausar()
            case 7:
                carregados, novo_proximo = acao_carregar_json()
                # Substitui o estado atual pelo carregado.
                talhoes = carregados
                proximo_id_local = novo_proximo
                pausar()
            case 8:
                acao_sync_local_para_oracle(talhoes, conn)
                pausar()
            case 9:
                carregados, novo_proximo = acao_sync_oracle_para_local(conn)
                # Só substitui se a sincronização teve sucesso.
                if carregados is not None:
                    talhoes = carregados
                    proximo_id_local = novo_proximo
                pausar()
            case 0:
                # Saída: fecha a conexão se existir.
                print("Encerrando...")
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass  # Fechar conexão não deve quebrar saída.
                # break encerra o while e consequentemente o programa.
                break


# Ponto de entrada padrão: só roda main() se o arquivo foi chamado diretamente.
if __name__ == "__main__":
    main()
