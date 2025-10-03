def find_files_using_lib(files: list[str], lib_name: str) -> list[str]:
    """
    Retorna os arquivos que usam a biblioteca 'lib_name'
    """
    matching_files = []
    
    for f in files:
        # só considerar arquivos de código
        if not f.endswith((".js", ".ts", ".jsx", ".tsx", ".py")):
            continue
        
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file_data:
                content = file_data.read()
                # busca padrões de import/require
                if f'import {lib_name}' in content \
                   or f'require("{lib_name}")' in content \
                   or f'from {lib_name} import' in content:
                    matching_files.append(f)
        except Exception as e:
            print(f"Erro lendo {f}: {e}")
    
    return matching_files
