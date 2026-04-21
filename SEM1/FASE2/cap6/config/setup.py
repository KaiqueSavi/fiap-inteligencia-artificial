from os.path import dirname, abspath, exists, join
from subprocess import run, CalledProcessError
from sys import executable
import os
from time import sleep

clear = lambda: print("\033c", end="")
clear()

BASE = dirname(abspath(__file__))


def get_input(
    question: str, options: tuple = ("s", "n"), answer_type: type = str
) -> int | str:
    is_range = len(options) == 2 and all(isinstance(i, (int, float)) for i in options)
    is_choice = options and all(isinstance(i, str) for i in options)

    hint = (
        f"[{'/'.join(options)}]"
        if is_choice
        else (f"[{options[0]}–{options[1]}]" if is_range else "")
    )

    while True:
        raw = input(f"\n  {question} {hint}: ").strip()
        try:
            value = answer_type(raw.lower() if answer_type is str else raw)
        except ValueError:
            clear()
            print("  ✗ Valor inválido, tente novamente.")
            continue

        if is_range and not (options[0] < value < options[1]):
            clear()
            print(f"  ✗ Digite um valor entre {options[0]} e {options[1]}.")
        elif is_choice and value not in options:
            clear()
            print(f"  ✗ Responda com: {' / '.join(options)}.")
        else:
            clear()
            return value


def ask(question: str) -> bool:
    return get_input(question, ("s", "n"), str) == "s"


def step(n: int, total: int, label: str, cls=True) -> None:
    if cls:
        clear()
    print(f"  [{n}/{total}] {label}")


def setup_venv() -> str:
    if not ask("Deseja criar um ambiente virtual (venv)?"):
        return executable

    venv_path = join(BASE, ".venv")
    print(f"\n  Criando venv em {venv_path}...")
    run([executable, "-m", "venv", venv_path], check=True)

    python = (
        join(venv_path, "Scripts", "python.exe")
        if os.name == "nt"
        else join(venv_path, "bin", "python")
    )

    print("  ✓ Venv criado.")
    return python


def install_requirements(python: str) -> None:
    req = join(BASE, "requirements.txt")
    if not exists(req):
        print("  ⚠ requirements.txt não encontrado, pulando instalação.")
        return

    print("\n  Instalando dependências...")
    try:
        run([python, "-m", "pip", "install", "-r", req], check=True)
        print("  ✓ Dependências instaladas.")
    except CalledProcessError:
        print("  ✗ Erro ao instalar dependências.")
        raise
    sleep(1)


def setup_oracle() -> None:
    if not ask("Você tem credenciais para a Oracle?"):
        return

    print("\n  Preencha as credenciais:\n")
    service_name = get_input("Nome do serviço", options=(), answer_type=str)
    host = get_input("Host", options=(), answer_type=str)
    port = get_input("Porta", options=(0, 65535), answer_type=int)
    user = get_input("Usuário", options=(), answer_type=str)
    password = get_input("Senha", options=(), answer_type=str)

    env_path = join(BASE, ".env")
    content = (
        f"DB_SERVICE_NAME={service_name}\n"
        f"DB_HOST={host}\n"
        f"DB_PORT={port}\n"
        f"DB_USER={user}\n"
        f"DB_PASSWORD={password}\n"
    )

    with open(env_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✓ Credenciais salvas em {env_path}")


def launch(python: str) -> None:
    main = join(BASE, "../main.py")
    if not exists(main):
        print("  ⚠ main.py não encontrado.")
        return
    print("\n  Iniciando o programa...\n" + "─" * 40)
    run([python, main])


def main() -> None:
    total = 3
    print("  ╔══════════════════════════════╗")
    print("  ║       Setup — Configuração   ║")
    print("  ╚══════════════════════════════╝\n")

    step(1, total, "Ambiente virtual", False)
    python = setup_venv()

    step(2, total, "Dependências")
    install_requirements(python)

    step(3, total, "Credenciais Oracle")
    setup_oracle()

    print("\n  ✓ Configuração concluída.\n")

    if ask("Deseja iniciar o programa agora?"):
        launch(python)


main()
