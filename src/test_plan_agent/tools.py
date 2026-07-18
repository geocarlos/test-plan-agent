"""Ferramentas controladas para apoio ao agente."""

from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
ALLOWED_EXTENSIONS = {".md", ".txt"}
MAX_FILE_SIZE_BYTES = 50_000


class LocalFileReadError(ValueError):
    """Erro controlado para falhas de leitura da base local."""


def read_local_data_file(relative_path: str) -> dict[str, Any]:
    """Lê arquivos permitidos dentro da pasta data/."""
    requested_path = Path(relative_path)
    data_dir = DATA_DIR.resolve()
    target_path = (data_dir / requested_path).resolve()

    if not target_path.is_relative_to(data_dir):
        raise LocalFileReadError("Acesso negado: o arquivo deve estar dentro da pasta data/.")

    if target_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise LocalFileReadError("Extensão inválida: use apenas arquivos .md ou .txt.")

    if not target_path.is_file():
        raise LocalFileReadError("Arquivo não encontrado na base local.")

    file_size = target_path.stat().st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise LocalFileReadError("Arquivo grande demais para leitura controlada.")

    return {
        "source": f"data/{target_path.relative_to(data_dir).as_posix()}",
        "content": target_path.read_text(encoding="utf-8"),
        "size_bytes": file_size,
    }


def prepare_minimal_context(user_story: str) -> dict[str, Any]:
    """Prepara um contexto local mínimo sem acessar recursos externos."""
    normalized_story = " ".join(user_story.strip().split())
    template_data = read_local_data_file("test_templates.md")

    return {
        "source": template_data["source"],
        "summary": normalized_story[:160],
        "template_reference": template_data["content"],
        "template_size_bytes": template_data["size_bytes"],
        "next_step": "usar a base local para estruturar planos de teste nas próximas etapas",
    }