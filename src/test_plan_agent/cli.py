"""Interface de linha de comando do Test-Plan Agent."""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langgraph>=0.6.0",
#     "langchain-openai>=0.3.0",
#     "python-dotenv>=1.0.1",
# ]
# ///

import argparse
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from test_plan_agent.graph import run_agent
from test_plan_agent.llm import LLMError


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


def _clean_markdown_story_line(line: str) -> str:
    line = line.strip().rstrip("  ")
    line = re.sub(r"^[-*+]\s+", "", line)
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
    return line


def read_user_stories_file(file_path: str) -> list[str]:
    """Lê uma ou mais histórias de usuário a partir de um arquivo Markdown."""
    story_path = Path(file_path)

    if story_path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Informe um arquivo Markdown com extensão .md ou .markdown.")

    if not story_path.is_file():
        raise FileNotFoundError("Arquivo de história não encontrado.")

    stories: list[str] = []
    current_story_lines: list[str] = []

    for raw_line in story_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line in {"---", "***", "___"}:
            if current_story_lines:
                stories.append(" ".join(current_story_lines))
                current_story_lines = []
            continue

        if line.startswith("#"):
            continue

        cleaned_line = _clean_markdown_story_line(line)
        if cleaned_line:
            current_story_lines.append(cleaned_line)

    if current_story_lines:
        stories.append(" ".join(current_story_lines))

    return stories


def resolve_user_story(args: argparse.Namespace) -> str:
    """Resolve a entrada do agente a partir de argumento, arquivo ou exemplo padrão."""
    if args.user_story and args.story_file:
        raise ValueError("Use uma história no argumento ou --file, não ambos.")

    if args.story_file:
        return read_user_story_file(args.story_file)

    return args.user_story or DEFAULT_USER_STORY


def resolve_user_stories(args: argparse.Namespace) -> list[str]:
    """Resolve uma ou mais entradas do agente a partir de argumento, arquivo ou exemplo padrão."""
    if args.user_story and args.story_file:
        raise ValueError("Use uma história no argumento ou --file, não ambos.")

    if args.story_file:
        stories = read_user_stories_file(args.story_file)
        if not stories:
            raise ValueError("O arquivo informado não contém histórias de usuário para análise.")
        return stories

    return [args.user_story or DEFAULT_USER_STORY]


def _configure_stdout_encoding() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def _configure_stderr_encoding() -> None:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def _print_progress(message: str) -> None:
    print(f"[Test-Plan Agent] {message}", file=sys.stderr, flush=True)


def main() -> None:
    """Executa o agente e imprime o plano final em Markdown."""
    _configure_stdout_encoding()
    _configure_stderr_encoding()
    args = parse_args()
    user_stories = resolve_user_stories(args)

    try:
        if len(user_stories) == 1:
            _print_progress("Processando história 1/1...")
            final_state = run_agent(user_stories[0], progress_callback=_print_progress)
            print(final_state["final_answer"])
            return

        final_answers: list[str] = ["# Planos de Testes"]
        for index, user_story in enumerate(user_stories, start=1):
            _print_progress(f"Processando história {index}/{len(user_stories)}...")
            final_state = run_agent(user_story, progress_callback=_print_progress)
            final_answers.append(f"## História {index}\n\n" + final_state["final_answer"])
    except LLMError as error:
        raise SystemExit(str(error)) from error

    print("\n\n---\n\n".join(final_answers))


if __name__ == "__main__":
    main()