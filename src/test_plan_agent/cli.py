"""Interface de linha de comando do Test-Plan Agent."""

import argparse
from pathlib import Path

from test_plan_agent.graph import run_agent


DEFAULT_USER_STORY = (
    "Como cliente autenticado, quero consultar meus pedidos recentes "
    "para acompanhar o status de entrega."
)


def parse_args() -> argparse.Namespace:
    """Lê argumentos informados pela linha de comando."""
    parser = argparse.ArgumentParser(description="Gera um plano de testes com o Test-Plan Agent.")
    parser.add_argument(
        "user_story",
        nargs="?",
        help="História de usuário, issue ou requisito funcional a ser analisado.",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="story_file",
        help="Caminho para um arquivo Markdown com a história de usuário a ser analisada.",
    )
    return parser.parse_args()


def read_user_story_file(file_path: str) -> str:
    """Lê uma história de usuário a partir de um arquivo Markdown."""
    story_path = Path(file_path)

    if story_path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Informe um arquivo Markdown com extensão .md ou .markdown.")

    if not story_path.is_file():
        raise FileNotFoundError("Arquivo de história não encontrado.")

    lines = story_path.read_text(encoding="utf-8").splitlines()
    story_lines = [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]

    return "\n".join(story_lines)


def resolve_user_story(args: argparse.Namespace) -> str:
    """Resolve a entrada do agente a partir de argumento, arquivo ou exemplo padrão."""
    if args.user_story and args.story_file:
        raise ValueError("Use uma história no argumento ou --file, não ambos.")

    if args.story_file:
        return read_user_story_file(args.story_file)

    return args.user_story or DEFAULT_USER_STORY


def main() -> None:
    """Executa o agente e imprime o plano final em Markdown."""
    args = parse_args()
    user_story = resolve_user_story(args)
    final_state = run_agent(user_story)
    print(final_state["final_answer"])


if __name__ == "__main__":
    main()