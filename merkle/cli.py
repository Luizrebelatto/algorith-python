import argparse
from merkle.core import generate_project_merkle_root

def main():
    parser = argparse.ArgumentParser(description="Calcula a Merkle Root de um projeto.")
    parser.add_argument("path", help="Caminho do projeto")
    args = parser.parse_args()

    root, files = generate_project_merkle_root(args.path)

    print(f"\n📂 Merkle Root: {root}\n")
    print("Arquivos e hashes:")
    for f, h in files:
        print(f"{f} -> {h}")
