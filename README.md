# Assistente de Cardápio

> Chat que recomenda pratos de restaurantes fictícios. Combina busca semântica com embeddings (RAG) e um agente que chama um LLM via API compatível com a OpenAI (Groq por padrão).

## Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas para as seguintes tarefas:

- [x] Dados dos cardápios e leitura dos pratos
- [ ] Busca semântica com filtros de preço e restrições
- [ ] Agente com ferramentas
- [ ] Interface em Gradio
- [ ] Testes

## 💻 Pré-requisitos

- Python 3.10+
- Linux, macOS ou WSL
- Uma chave de API do [Groq](https://console.groq.com) ou de outro provedor compatível com a OpenAI

## 🚀 Instalando

```bash
python -m venv .venv
source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

Crie um `.env` na raiz:

```
LLM_API_KEY=sua_chave
LLM_MODEL=nome_do_modelo
LLM_BASE_URL=https://api.groq.com/openai/v1   # opcional
```

## ☕ Usando

```bash
python app.py      # abre em http://127.0.0.1:7860
python -m pytest   # roda os testes
```
