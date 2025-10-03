import argparse
from merkle.core import generate_project_merkle_root, prepare_for_ai


def main():
    parser = argparse.ArgumentParser(description="Calcula a Merkle Root e prepara arquivos para IA.")
    parser.add_argument("path", help="Caminho do projeto")
    args = parser.parse_args()

    root, file_hashes, modified_files = generate_project_merkle_root(args.path)

    print(f"\n📂 Merkle Root: {root}\n")
    print("Arquivos e hashes:")
    for f, h in file_hashes.items():
        print(f"{f} -> {h}")

    if modified_files:
        print("\n📌 Arquivos modificados desde o último run:")
        for f in modified_files:
            print(f" - {f}")

        # preparar chunks para IA
        chunks = prepare_for_ai(modified_files)
        print("\n✂️ Chunks para IA:")
        for c in chunks:
            print(f"\n{c['file']} (parte {c['part']}/{c['total_parts']}):\n{c['content'][:100]}...")
    else:
        print("\n✅ Nenhum arquivo foi modificado desde o último run.")
