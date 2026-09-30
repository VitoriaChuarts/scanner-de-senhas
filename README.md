# CODE SCANNER

Ferramenta em Python que varre arquivos, repositórios e o histórico de commits do Git em busca de credenciais expostas no código-fonte — chaves de API, tokens de acesso e outros segredos que não deveriam estar versionados.

## O problema

Vazamento de credenciais em repositórios de código é uma das causas mais comuns de incidentes de segurança reais. É comum um desenvolvedor colocar uma chave de API "temporariamente" no código pra testar, esquecer de remover, e a credencial ficar exposta publicamente.

O que muita gente não percebe: **remover a credencial do código não é suficiente**. O Git guarda o histórico completo de cada arquivo desde o primeiro commit — então mesmo que a chave tenha sido apagada na versão atual, ela continua existindo, visível, em qualquer commit antigo que a tenha incluído.

## O que o scanner faz

- Varre recursivamente uma pasta e todas as suas subpastas
- Usa expressões regulares para identificar padrões conhecidos de credenciais (chaves de acesso da AWS e tokens do GitHub)
- **Varre também o histórico de commits do Git**, encontrando segredos que já foram removidos do código atual mas continuam expostos em versões antigas
- Reporta o arquivo (ou o commit), o número da linha e o tipo de segredo encontrado
- **Mascara os segredos** no terminal e no relatório: só os 4 primeiros caracteres aparecem
- Ignora pastas irrelevantes (`.git`, `node_modules`, `__pycache__`, `venv`, `.venv`) e o próprio relatório gerado, evitando falsos positivos
- Salva os resultados em um relatório estruturado (`relatorio.json`)

## Como usar

Requisitos: Python 3 e Git instalados. Não há nada para instalar com `pip`.

```
python code_scanner.py                 # escaneia a pasta atual
python code_scanner.py C:\meu\projeto  # escaneia outra pasta
python code_scanner.py --help          # mostra a ajuda
```

Se a pasta informada não existir, o programa avisa e encerra, em vez de dizer que está tudo limpo. Se a pasta não for um repositório Git, ele mostra um aviso e escaneia só os arquivos.

O `relatorio.json` é gravado na pasta onde o comando foi executado.

## Exemplo de saída

```
[AWS Key]: .\teste.txt:1 -> AKIA********
[GitHub Token]: .\teste.txt:2 -> ghp_********
[AWS Key]: teste.txt (commit f7d2897):1 -> AKIA********
[GitHub Token]: teste.txt (commit f7d2897):2 -> ghp_********
```

As duas primeiras linhas vêm da varredura dos arquivos atuais; as duas últimas, do histórico, com o hash do commit onde o segredo foi introduzido. O `teste.txt` do repositório contém chaves falsas, só para demonstração.

## Como o histórico é varrido

O scanner executa `git log -p -U0`, que mostra, para cada commit, apenas as linhas que ele **adicionou**. Ele lê essa saída linha por linha, guardando o commit e o arquivo atuais, e procura segredos só nas linhas adicionadas. Usa também os marcadores `@@` do Git para calcular o número correto da linha.

Com isso, cada segredo aparece **uma única vez**, no commit em que entrou. Uma versão anterior olhava o conteúdo completo de todos os arquivos em cada commit, e o mesmo segredo se repetia em todos os commits em que existia.

## Segurança do próprio projeto

- Os segredos aparecem mascarados (`AKIA********`) no terminal e no `relatorio.json`, para que a própria ferramenta não vaze o que encontrou.
- O `relatorio.json` está no `.gitignore` e na lista de arquivos ignorados pelo scanner, evitando que seja enviado ao repositório ou reescaneado.

## Limitações

- Só reconhece dois padrões (chave de acesso da AWS e token do GitHub)
- Varre o histórico da branch atual
- Não sabe diferenciar segredo real de exemplo: um valor de teste com o formato certo também é marcado
- Não verifica se a credencial ainda está ativa; todo achado deve ser tratado como comprometido e rotacionado

## Próximos passos

- Adicionar mais padrões de detecção (chaves privadas SSH, strings de conexão de banco de dados)
- Varrer o histórico de todas as branches
- Detecção por entropia, para identificar segredos sem formato conhecido
- Testes automatizados
- Gerar relatório em formato HTML, além do JSON

## Tecnologias

Python 3 (biblioteca padrão: `re`, `os`, `json`, `subprocess`, `argparse`) e Git.
