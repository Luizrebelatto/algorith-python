import os
import hashlib
import json

CACHE_FILE = ".merkle_cache.json"


def hash_data(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_all_files(directory: str, ignore=("node_modules", ".git")) -> list[str]:
    files = []
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            files.append(filepath)
    return sorted(files)


def build_merkle_tree(hashes: list[str]) -> str:
    if not hashes:
        return None
    if len(hashes) == 1:
        return hashes[0]

    new_level = []
    for i in range(0, len(hashes), 2):
        left = hashes[i]
        right = hashes[i + 1] if i + 1 < len(hashes) else left
        combined = hash_data((left + right).encode())
        new_level.append(combined)

    return build_merkle_tree(new_level)


def load_cache() -> dict:
    """Carrega cache de hashes antigos do disco."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data: dict):
    """Salva hashes atuais no cache."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def chunk_text(text: str, max_chars=2000) -> list[str]:
    """Divide texto em pedaços menores para mandar para a IA."""
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def generate_project_merkle_root(project_path: str):
    """Gera Merkle Root e identifica arquivos modificados desde o último run."""
    files = get_all_files(project_path)
    file_hashes = {}
    modified_files = []

    # carregar cache
    cache = load_cache()

    for f in files:
        with open(f, "rb") as file_data:
            content = file_data.read()
            file_hash = hash_data(content)
            file_hashes[f] = file_hash

            # detecta mudanças
            if cache.get(f) != file_hash:
                modified_files.append(f)

    # salva novo estado no cache
    save_cache(file_hashes)

    merkle_root = build_merkle_tree(list(file_hashes.values()))

    return merkle_root, file_hashes, modified_files


def prepare_for_ai(modified_files: list[str], max_chunk_size=2000):
    """Divide arquivos modificados em chunks para enviar à IA."""
    chunks = []
    for f in modified_files:
        with open(f, "r", encoding="utf-8", errors="ignore") as file_data:
            content = file_data.read()
            file_chunks = chunk_text(content, max_chunk_size)
            for i, chunk in enumerate(file_chunks):
                chunks.append({
                    "file": f,
                    "part": i + 1,
                    "total_parts": len(file_chunks),
                    "content": chunk
                })
    return chunks
