import re
import os
import json
import git

padroes = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"ghp_[0-9A-Za-z]{36}",
}

PASTAS_IGNORADAS = {".git", "node_modules", "__pycache__", "venv"}
ARQUIVOS_IGNORADOS = {"relatorio.json"}


def testar_conteudo(texto, nome_referencia):
    achados = []
    for numero_linha, linha in enumerate(texto.splitlines(), start=1):
        for nome_segredo, padrao in padroes.items():
            resultado = re.search(padrao, linha)
            if resultado:
                achados.append({
                    "documento": nome_referencia,
                    "linha": numero_linha,
                    "tipo": nome_segredo,
                    "trecho": resultado.group()
                })
    return achados


def escanear_documentos(caminho_documento):
    with open(caminho_documento, "r", encoding="utf-8", errors="ignore") as documento:
        texto = documento.read()
    return testar_conteudo(texto, caminho_documento)


def escanear_pasta(caminho_pasta):
    todos_achados = []

    for pasta_atual, subpastas, arquivos in os.walk(caminho_pasta):
        subpastas[:] = [pasta for pasta in subpastas if pasta not in PASTAS_IGNORADAS]

        for nome_arquivo in arquivos:
            if nome_arquivo in ARQUIVOS_IGNORADOS:
                continue

            caminho_completo = os.path.join(pasta_atual, nome_arquivo)
            achados = escanear_documentos(caminho_completo)
            todos_achados.extend(achados)

    return todos_achados


def escanear_historico_git(caminho_repositorio):
    todos_achados = []
    repositorio = git.Repo(caminho_repositorio)

    for commit in repositorio.iter_commits():
        for item in commit.tree.traverse():
            if item.type == "blob":
                try:
                    conteudo_bytes = item.data_stream.read()
                    conteudo_texto = conteudo_bytes.decode("utf-8", errors="ignore")
                except Exception:
                    continue

                referencia = f"{item.path} (commit {commit.hexsha[:7]})"
                achados = testar_conteudo(conteudo_texto, referencia)
                todos_achados.extend(achados)

    return todos_achados


def salvar_relatorio(achados, caminho_saida="relatorio.json"):
    with open(caminho_saida, "w", encoding="utf-8") as arquivo_saida:
        json.dump(achados, arquivo_saida, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    resultados = escanear_pasta(".")
    resultados_historico = escanear_historico_git(".")
    todos_resultados = resultados + resultados_historico

    salvar_relatorio(todos_resultados)

    if todos_resultados:
        for achado in todos_resultados:
            tipo = achado['tipo']
            doc = achado['documento']
            linha = achado['linha']
            trecho = achado['trecho']
            print(f"[{tipo}]: {doc}:{linha} -> {trecho}")
    else:
        print("Nenhum segredo encontrado.")