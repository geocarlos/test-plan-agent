"""Interface de linha de comando do Test-Plan Agent."""

import argparse
import json

from test_plan_agent.graph import run_agent


DEFAULT_USER_STORY = (
    "Como cliente autenticado, quero consultar meus pedidos recentes "
    "para acompanhar o status de entrega."
)


def parse_args() -> argparse.Namespace:
    """Lê argumentos informados pela linha de comando."""
    parser = argparse.ArgumentParser(description="Executa o fluxo mínimo do Test-Plan Agent.")
    parser.add_argument(
        "user_story",
        nargs="?",
        default=DEFAULT_USER_STORY,
        help="História de usuário, issue ou requisito funcional a ser analisado.",
    )
    return parser.parse_args()


def main() -> None:
    """Executa o fluxo mínimo do agente."""
    args = parse_args()
    final_state = run_agent(args.user_story)
    print(json.dumps(final_state["provisional_response"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()