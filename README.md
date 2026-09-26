# Brand Monitor

Servico para analisar mencoes de marcas em respostas de ferramentas de IA. O projeto esta sendo desenvolvido por etapas; por enquanto, a estrutura existe, mas a API, a ingestao, a persistencia e as metricas ainda precisam ser implementadas.

## Estrutura

- `app/api`: endpoints HTTP. Mantem a camada web separada das regras do produto.
- `app/domain`: formatos dos dados e contratos usados pelas outras camadas.
- `app/services`: regras de negocio, como limpeza, deteccao de marcas e metricas.
- `app/infrastructure`: acesso ao banco e implementacoes de persistencia.
- `app/scripts`: tarefas executadas fora da API, como a ingestao inicial.
- `tests`: testes das regras e dos comportamentos importantes.

Essa separacao ajuda a testar as regras sem depender diretamente da API ou do banco. Os arquivos ainda estao em grande parte como esqueletos.

## Dados de exemplo

`respostas-exemplo.json` e o arquivo de entrada da ingestao. Ele contem casos sujos importantes para o projeto, como um identificador repetido, datas em formatos diferentes, valores nulos e texto vazio.

## Documentacao

As decisoes e dificuldades estao explicadas em [DOCUMENTACAO.md](DOCUMENTACAO.md).

## Desenvolvimento

As dependencias estao listadas em `requirements.txt`. A aplicacao usa FastAPI; SQLite com SQLAlchemy esta previsto para persistencia, mas essa parte ainda nao foi implementada.

Execute os testes atuais com `python -m unittest tests.test_cleaner -v`.