# Brand Monitor

Servico para analisar mencoes de marcas em respostas de ferramentas de IA. A ingestao, a validacao dos dados, a deteccao de marcas e a persistencia SQLite ja estao implementadas. A API e as metricas ainda estao em desenvolvimento.

## Estrutura

- `app/api`: endpoints HTTP. Mantem a camada web separada das regras do produto.
- `app/domain`: formatos dos dados e contratos usados pelas outras camadas.
- `app/services`: regras de negocio, como limpeza, deteccao de marcas e metricas.
- `app/infrastructure`: acesso ao banco e implementacoes de persistencia.
- `app/scripts`: tarefas executadas fora da API, como a ingestao inicial.
- `tests`: testes das regras e dos comportamentos importantes.

Essa separacao ajuda a testar as regras sem depender diretamente da API ou do banco.

## Dados de exemplo

`respostas-exemplo.json` e o arquivo de entrada da ingestao. Ele contem casos sujos importantes para o projeto, como um identificador repetido, datas em formatos diferentes, valores nulos e texto vazio.

## Documentacao

As decisoes e dificuldades estao explicadas em [DOCUMENTACAO.md](DOCUMENTACAO.md).

## Desenvolvimento

As dependencias estao listadas em `requirements.txt`. A ingestao grava as respostas em `brand_monitor.sqlite3` usando SQLite e SQLAlchemy. Esse banco local e ignorado pelo Git.

Execute a ingestao com `python -m app.scripts.ingest` e rode todos os testes com `python -m unittest discover -v`.