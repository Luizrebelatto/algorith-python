import os
import hashlib

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
        right = hashes[i+1] if i+1 < len(hashes) else left
        combined = hash_data((left + right).encode())
        new_level.append(combined)

    return build_merkle_tree(new_level)

def generate_project_merkle_root(project_path: str):
    files = get_all_files(project_path)
    file_hashes = []
    for f in files:
        with open(f, "rb") as file_data:
            content = file_data.read()
            file_hashes.append(hash_data(content))
    merkle_root = build_merkle_tree(file_hashes)
    return merkle_root, list(zip(files, file_hashes))
