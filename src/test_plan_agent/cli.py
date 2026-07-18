"""Interface de linha de comando do Test-Plan Agent."""

import argparse

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
        default=DEFAULT_USER_STORY,
        help="História de usuário, issue ou requisito funcional a ser analisado.",
    )
    return parser.parse_args()


def main() -> None:
    """Executa o agente e imprime o plano final em Markdown."""
    args = parse_args()
    final_state = run_agent(args.user_story)
    print(final_state["final_answer"])


if __name__ == "__main__":
    main()