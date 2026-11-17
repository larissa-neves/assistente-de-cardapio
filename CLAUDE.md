# Assistente de Cardápio

Chat em Gradio que recomenda pratos de restaurantes fictícios. Combina busca semântica com embeddings (RAG) e um agente com tool use que chama um LLM via API compatível com a OpenAI (Groq por padrão).

## Stack

- Python 3.10+, ambiente virtual em `.venv`
- `gradio`: interface de chat (`gr.ChatInterface`)
- `openai`: cliente do LLM, apontando para o Groq via `base_url`
- `sentence-transformers` + `numpy`: embeddings e similaridade de cosseno
- `python-dotenv`: leitura do `.env`
- `pytest`: testes
- PyTorch instalado na versão só para CPU (fora do `requirements.txt`)

## Estrutura

```
dados/cardapios.json   # 6 restaurantes, 5 pratos cada
busca.py               # Prato (dataclass), carregar_pratos, BuscaCardapio
agente.py              # ferramentas, prompt de sistema, ciclo do agente
app.py                 # interface Gradio; cria busca e agente uma vez
tests/                 # testes com pytest, sem internet e sem chave
requirements.txt       # só dependências diretas
.env                   # chaves (fora do Git)
```

## Comandos

```bash
source .venv/bin/activate                                          # ativar o ambiente
pip install torch --index-url https://download.pytorch.org/whl/cpu # antes do requirements
pip install -r requirements.txt                                    # instalar dependências
python app.py                                                      # rodar (http://127.0.0.1:7860)
python -m pytest                                                   # rodar os testes
```

Ambiente: Ubuntu no WSL. O projeto fica em `~/projetos/assistente-cardapio`, não em `/mnt/c`.

## Variáveis de ambiente

| Variável | Uso | Padrão |
|---|---|---|
| `LLM_API_KEY` | Chave do provedor do LLM | obrigatória |
| `LLM_BASE_URL` | Endereço da API compatível com a OpenAI | `https://api.groq.com/openai/v1` |
| `LLM_MODEL` | Nome do modelo | definido no `.env` |

## Dados

Cada restaurante tem `restaurante`, `culinaria` e `pratos`. Cada prato tem `nome`, `descricao`, `preco` (float, em reais), `categoria` e `tags`. Tags permitidas: `vegano`, `vegetariano`, `sem glúten`.

## Regras de arquitetura

- **Filtros por código, nunca por similaridade.** Preço máximo e restrições alimentares são aplicados em Python depois da busca. A similaridade só ordena.
- **Vegano conta como vegetariano** no filtro de restrições.
- **Embeddings normalizados** (`normalize_embeddings=True`), para que o produto escalar seja a similaridade de cosseno. Busca com NumPy, sem banco vetorial.
- **Vetores dos pratos calculados uma vez**, na criação da `BuscaCardapio`.
- **Dependências injetadas.** `BuscaCardapio` recebe a função de embeddings; `Agente` recebe o cliente do LLM. Nunca instanciar modelo ou cliente dentro dessas classes.
- **Ferramentas do agente:** `buscar_pratos(consulta, preco_maximo?, restricoes?)` e `ver_cardapio(restaurante)`. Resultados devolvidos como JSON com `ensure_ascii=False`.
- **Ciclo do agente:** no máximo 5 passos. Cada resultado de ferramenta volta como mensagem `tool` com o `tool_call_id` do pedido. Argumentos JSON inválidos viram mensagem de erro para o modelo, nunca exceção.
- **Prompt de sistema** proíbe inventar pratos, preços ou restaurantes e limita a 3 recomendações.
- **Gradio:** modelo, busca e agente criados fora da função de resposta. Erros do LLM aparecem no chat via `try/except`. O histórico do Gradio é convertido para mensagens `{role, content}` de texto antes de ir ao LLM.

## Testes

- Nenhum teste chama a API do LLM nem baixa o modelo de embeddings.
- Embeddings substituídos por uma função falsa determinística; cliente do LLM por um objeto falso com respostas programadas.
- Cobrir: filtro de preço, filtro de restrições, vegano como vegetariano, ciclo com chamada de ferramenta, limite de passos e argumentos inválidos.

## Segurança

- Nunca escrever chaves no código, em testes ou no README. Ler sempre de `os.environ`.
- `.env`, `.venv` e `__pycache__` ficam no `.gitignore`. Conferir com `git status` antes de qualquer push.
- Conferir a grafia de pacotes antes de instalar (typosquatting).

## Convenções

- Código simples e legível, sem abstrações desnecessárias.
- Nomes de variáveis, funções e comentários em português.
- Mudanças pequenas, uma etapa por vez. Explicar o plano antes de editar e não avançar de etapa sem pedido.
