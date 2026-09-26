git add -- .gitignore README.md DOCUMENTACAO.md app/scripts/ingest.py app/services/data_cleaner.py tests/test_cleaner.py respostas.json
git commit -m "feat(ingest): deduplicate the provided response file" -m "Use respostas-exemplo.json as the ingestion source and remove its duplicate copy. Keep exact duplicate IDs once, reject conflicting records, and exclude the internal progress log from Git."# Documentacao do projeto

## O que estou construindo

Estou construindo o Brand Monitor para receber respostas de ferramentas de IA e identificar quando elas citam Acme, Zenith ou Nimbus. Depois, vou oferecer uma API para consultar a presenca dessas marcas e adicionar novas respostas.

## Como as pastas estao organizadas

- Separei `app/api` para receber requisicoes HTTP e devolver respostas.
- Coloquei em `app/domain` os formatos e regras centrais dos dados.
- Organizei em `app/services` a logica do produto: limpar dados, encontrar marcas e calcular metricas.
- Reservei `app/infrastructure` para conversar com o banco de dados.
- Coloquei em `app/scripts` tarefas como a ingestao inicial, separadas da API.
- Criei `tests` para verificar automaticamente os comportamentos importantes.

Fiz essa divisao para nao misturar, por exemplo, calculos de metricas com detalhes de HTTP ou SQL. A estrutura ja esta criada, mas ainda estou implementando a maior parte do codigo.

## Decisoes iniciais

- **FastAPI:** escolhi esse framework e ja o usei no ponto de entrada. Ele tambem facilita descrever os endpoints.
- **SQLite com SQLAlchemy:** planejo usar essa combinacao para guardar os dados localmente sem exigir um servidor de banco separado. Ainda falta implementar a persistencia.
- **Regras em servicos separados:** deixei deteccao, limpeza e metricas fora da API para poder testa-las de forma independente.
- **Arquivo de entrada:** vou usar `respostas-exemplo.json`, que contem os registros fornecidos para o desafio.

## Dados encontrados e dificuldades

Encontrei dados que exigem cuidado: o registro `r003` aparece duas vezes, algumas datas usam formatos diferentes, ha valores `null` e uma resposta tem texto vazio. Isso importa porque uma validacao rigida demais pode rejeitar dados que o sistema deveria conseguir tratar.

Para IDs repetidos, implementei esta regra: se os registros forem identicos, mantenho uma ocorrencia; se tiverem o mesmo ID mas dados diferentes, paro a ingestao com erro. Assim, nao descarto informacao silenciosamente. Tambem rejeito registros que nao sejam objetos ou nao tenham um ID de texto preenchido.

Ainda preciso definir o que fazer com datas que nao podem ser interpretadas e com texto vazio. Na deteccao, vou procurar marcas sem diferenciar maiusculas de minusculas e reconhecer variacoes como `A.C.M.E.`, sem confundir uma marca com parte de outra palavra.

O carregador em `app/scripts/ingest.py` le `respostas-exemplo.json` e aplica a regra de IDs antes de devolver os registros. Os endpoints, a persistencia, a deteccao e as metricas ainda nao estao funcionando.

## Testes e ambiente

Comecei testando a limpeza porque o arquivo ja tem um ID repetido. Os testes confirmam que duplicatas identicas sao removidas e conflitos de ID sao reportados. Tambem vou testar deteccao de marcas, validacao dos dados, metricas e endpoints.

O terminal nao tem o pacote `pytest`. Os testes desta etapa usam `unittest`, que faz parte do Python, e podem ser executados com `python -m unittest tests.test_cleaner -v`.