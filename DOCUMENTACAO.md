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
- **Pydantic:** vou usa-lo para validar os campos recebidos e normalizar datas antes de calcular as metricas ou salvar respostas.
- **SQLite com SQLAlchemy:** planejo usar essa combinacao para guardar os dados localmente sem exigir um servidor de banco separado. Ainda falta implementar a persistencia.
- **Regras em servicos separados:** deixei deteccao, limpeza e metricas fora da API para poder testa-las de forma independente.
- **Arquivo de entrada:** vou usar `respostas-exemplo.json`, que contem os registros fornecidos para o desafio.

## Dados encontrados e dificuldades

Encontrei dados que exigem cuidado: o registro `r003` aparece duas vezes, algumas datas usam formatos diferentes, ha valores `null` e uma resposta tem texto vazio. Isso importa porque uma validacao rigida demais pode rejeitar dados que o sistema deveria conseguir tratar.

Para IDs repetidos, implementei esta regra: se os registros forem identicos, mantenho uma ocorrencia; se tiverem o mesmo ID mas dados diferentes, paro a ingestao com erro. Assim, nao descarto informacao silenciosamente. Tambem rejeito registros que nao sejam objetos ou nao tenham um ID de texto preenchido.

Implementei a leitura de datas ISO, no formato `dia/mes/ano` e no formato `ano/mes/dia`, convertendo os valores reconhecidos para ISO. Uma data impossivel ou em outro formato interrompe a ingestao com o numero do registro e o campo que falhou. Mantive os valores `null` permitidos e a resposta vazia, porque os encontrei no arquivo e eles podem ser resultado da coleta.

Implementei a deteccao em `app/services/brand_detector.py`. Ela ignora maiusculas e minusculas, reconhece `A.C.M.E.` e exige limites de palavra para nao tratar, por exemplo, `Acmeish` como mencao. O resultado usa os nomes padronizados `Acme`, `Zenith` e `Nimbus`, sem repetir a mesma marca se ela aparecer varias vezes.

O carregador em `app/scripts/ingest.py` le `respostas-exemplo.json`, valida e normaliza os registros, e por fim aplica a regra de IDs. A deteccao ja esta disponivel como servico; ainda falta usa-la nos calculos e endpoints. Os endpoints, a persistencia e as metricas ainda nao estao funcionando.

## Testes e ambiente

Comecei testando a limpeza porque o arquivo ja tem um ID repetido e datas em formatos diferentes. Os testes confirmam o tratamento das duplicatas, a normalizacao das datas, a preservacao dos nulos e do texto vazio, e a rejeicao de campos ausentes e datas impossiveis. Tambem testei a deteccao de maiusculas, grafia pontuada, repeticoes e limites de palavra. Ainda vou testar metricas e endpoints.

O terminal nao tem o pacote `pytest`. Os testes desta etapa usam `unittest`, que faz parte do Python, e podem ser executados com `python -m unittest tests.test_cleaner -v`.