# Brand Monitor

Servico para analisar mencoes de marcas em respostas de ferramentas de IA. O projeto tem ingestao, validacao, deteccao de marcas, persistencia SQLite e endpoints HTTP.

## Estrutura

- `app/api`: recebe requisicoes HTTP e chama as regras do produto.
- `app/domain`: define o formato dos registros.
- `app/services`: valida dados, detecta marcas e calcula metricas.
- `app/infrastructure`: configura o SQLite e salva/consulta respostas.
- `app/scripts`: executa tarefas como a ingestao inicial.
- `tests`: verifica regras e endpoints.

Separei essas partes para testar as regras sem depender diretamente da API ou do banco.

## Dados

`respostas-exemplo.json` e a fonte da ingestao. Contem dados coletados com variacoes de data, valores nulos, uma resposta vazia e um ID duplicado.

## API

- `GET /share-of-voice?marca=Acme`: percentual de respostas com mencao, no geral e por plataforma.
- `GET /top-citacoes?n=5`: respostas ordenadas pela quantidade de marcas distintas citadas.
- `POST /respostas`: valida e salva uma nova resposta.

## Desenvolvimento

No PowerShell, ative o ambiente virtual e instale as dependencias:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Execute a ingestao com `python -m app.scripts.ingest`, rode os testes com `python -m unittest discover -v` e inicie a API com `uvicorn app.main:app --reload`.

As decisoes e dificuldades do desenvolvimento estao em [DOCUMENTACAO.md](DOCUMENTACAO.md).
