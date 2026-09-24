import re
import os

padroes = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"ghp_[0-9A-Za-z]{36}",
}


def escanear_pasta(caminho_pasta):
    todos_achados = []

    for pasta_atual, subpastas, arquivos in os.walk(caminho_pasta):
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(pasta_atual, nome_arquivo)
            achados = escanear_documentos(caminho_completo)
            todos_achados.extend(achados)

    return todos_achados


def escanear_documentos(caminho_documento):
    achados = []

    with open(caminho_documento, "r", encoding="utf-8", errors="ignore") as documento:
        for numero_linha, linha in enumerate(documento, start=1):
            for nome_segredo, padrao in padroes.items():
                resultado = re.search(padrao, linha)
                if resultado:
                    achados.append({
                        "documento": caminho_documento,
                        "linha": numero_linha,
                        "tipo": nome_segredo,
                        "trecho": resultado.group()
                    })

    return achados


if __name__ == "__main__":
    resultados = escanear_pasta(r"C:\Users\silva\OneDrive\Desktop\projetos\verificador de senhas\Analisador-de-senha")
    if resultados:
        for achado in resultados:
            tipo = achado['tipo']
            doc = achado['documento']
            linha = achado['linha']
            trecho = achado['trecho']
            print(f"[{tipo}]: {doc}:{linha} -> {trecho}")
    else:
        print("Nenhum segredo encontrado.")