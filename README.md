# scanner-de-senhas

# CODE SCANNER

Ferramenta em Python que varre arquivos, repositórios e o histórico de commits do Git em busca de credenciais expostas no código-fonte — chaves de API, tokens de acesso e outros segredos que não deveriam estar versionados.

## O problema

Vazamento de credenciais em repositórios de código é uma das causas mais comuns de incidentes de segurança reais. É comum um desenvolvedor colocar uma chave de API "temporariamente" no código pra testar, esquecer de remover, e a credencial ficar exposta publicamente.

O que muita gente não percebe: **remover a credencial do código não é suficiente**. O Git guarda o histórico completo de cada arquivo desde o primeiro commit — então mesmo que a chave tenha sido apagada na versão atual, ela continua existindo, visível, em qualquer commit antigo que a tenha incluído.

## O que o scanner faz

- Varre recursivamente uma pasta e todas as suas subpastas
- Usa expressões regulares para identificar padrões conhecidos de credenciais (ex: chaves AWS, tokens do GitHub)
- **Varre também todo o histórico de commits do Git**, encontrando segredos que já foram removidos do código atual mas continuam expostos em versões antigas
- Ignora automaticamente pastas irrelevantes (`.git`, `node_modules`, `__pycache__`, `venv`) e o próprio relatório gerado, evitando falsos positivos
- Reporta o arquivo (ou commit), a linha e o tipo de segredo encontrado
- Salva os resultados em um relatório estruturado (`relatorio.json`)

## Como usar

```bash
python code_scanner.py
```

Por padrão, escaneia a pasta atual (estado atual + histórico completo do Git, se houver um repositório `.git` presente). Para escanear outro diretório, edite os caminhos passados para `escanear_pasta()` e `escanear_historico_git()`.

## Dependências

```bash
pip install gitpython
```

O restante usa apenas bibliotecas padrão do Python (`re`, `os`, `json`).

## Exemplo de saída

[AWS Key]: .\config.py:12 -> AKIA1234567890ABCDEF
[GitHub Token]: teste.txt (commit 8b71974):2 -> ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


Repare que o histórico mostra o hash do commit onde o segredo foi encontrado — permitindo rastrear exatamente quando a credencial foi introduzida.

## Segurança do próprio projeto

O `relatorio.json` gerado contém, em texto puro, qualquer credencial encontrada — por isso ele está listado no `.gitignore` e também na lista de arquivos ignorados pelo próprio scanner, evitando que seja enviado ao repositório ou reescaneado indevidamente.

## Próximos passos

- Adicionar mais padrões de detecção (chaves privadas SSH, strings de conexão de banco de dados)
- Detecção por entropia, para identificar segredos sem formato conhecido
- Gerar relatório em formato HTML, além do JSON
- Transformar em ferramenta de linha de comando (CLI) com argumentos configuráveis

## Tecnologias

Python 3, módulo `re`, `os`, `json` (biblioteca padrão) e `GitPython`