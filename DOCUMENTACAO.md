# Documentacao do projeto

## O que estou construindo

Estou construindo o Brand Monitor para receber respostas de ferramentas de IA e identificar quando elas citam Acme, Zenith ou Nimbus. A API permite consultar a presenca das marcas, ver as respostas com mais citacoes e adicionar novas respostas.

## Como organizei o projeto

- Separei `app/api` para receber requisicoes HTTP e devolver respostas.
- Coloquei em `app/domain` os formatos centrais dos dados.
- Organizei em `app/services` a limpeza, a deteccao de marcas e as metricas.
- Reservei `app/infrastructure` para a conexao com o banco e a persistencia.
- Coloquei em `app/scripts` tarefas que podem ser executadas separadamente da API.
- Criei `tests` para verificar automaticamente os comportamentos importantes.

Fiz essa divisao para nao misturar calculos de metricas com detalhes de HTTP ou SQL.

## Decisoes tecnicas

- **FastAPI:** escolhi esse framework para criar os endpoints e documentar a API.
- **Pydantic:** uso-o para validar os campos e normalizar datas antes de salvar as respostas.
- **SQLite com SQLAlchemy:** escolhi essa combinacao para persistir dados localmente sem exigir um servidor de banco separado.
- **Regras separadas da API:** deixei deteccao e metricas em servicos para poder testa-las sem fazer requisicoes HTTP.
- **Arquivo de entrada:** uso `respostas.json`, o arquivo fornecido para o desafio.

## Dados e dificuldades

Encontrei o registro `r003` duplicado, datas em formatos diferentes, valores `null` e uma resposta vazia. Para IDs repetidos, implementei esta regra: se os registros forem iguais, mantenho uma ocorrencia; se o mesmo ID vier com conteudo diferente, rejeito a carga para nao descartar informacao silenciosamente.

Aceito datas ISO, `dia/mes/ano` e `ano/mes/dia`, convertendo as datas reconhecidas para ISO. Datas impossiveis ou em formatos desconhecidos interrompem a ingestao com o numero do registro e o campo que falhou. Mantenho valores nulos e resposta vazia quando o formato do campo permite.

Tambem guardo campos extras do scraping em JSON no banco, para nao descarta-los durante a persistencia. Ao iniciar, normalizo aliases de plataforma que ja estejam salvos, para que uma reingestao nao encontre conflitos causados apenas por caixa ou hifen.

## Deteccao e metricas

Implementei a deteccao em `app/services/brand_detector.py`. Ela ignora maiusculas e minusculas, reconhece `A.C.M.E.` e exige limites de palavra para nao tratar `Acmeish` como mencao. O resultado usa nomes padronizados e nao repete a mesma marca na resposta.

Implementei tres endpoints: `GET /share-of-voice?marca=Acme`, `GET /top-citacoes?n=5` e `POST /respostas`. A marca no share of voice aceita diferencas entre maiusculas e minusculas, mas precisa ser uma das marcas monitoradas.

No share of voice, conto respostas unicas que citam a marca e divido pelo total de respostas persistidas. Agrupo variacoes conhecidas como `ChatGPT`, `chatgpt`, `Chat-GPT` e `chat-gpt` sob o nome `ChatGPT`; faco o mesmo com caixa diferente para Gemini e Perplexity. Arredondo os percentuais para duas casas decimais. Para o ranking, considero mais forte uma resposta que cita mais marcas distintas; em caso de empate, ordeno pelo ID. Respostas sem marcas ficam fora do ranking.

No POST, uma resposta nova retorna `201`; repetir exatamente um registro retorna `200`; reutilizar um ID com outro conteudo retorna `409`; dados invalidos retornam `422`.

## Testes

Comecei pela limpeza por causa do ID duplicado e das datas variadas. Os testes cobrem validacao, datas, nulos, duplicatas e deteccao. Para a persistencia e a API, uso bancos SQLite temporarios, assim nao altero o banco local ao testar. Tambem testo percentuais, ordenacao, validacao e codigos HTTP.

Uso `unittest`, que faz parte do Python, e executo a suite com `python -m unittest discover -v`. Adicionei `httpx2` porque a versao atual do Starlette usa esse pacote no cliente de testes HTTP.
