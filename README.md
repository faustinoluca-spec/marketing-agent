# 🎯 Marketing Agent

Agente de IA que gera campanhas de marketing completas em segundos.

## Demo
🔗 [Acesse o app ao vivo](https://marketing-agent-foqkvcvkhtw7fcpbtclsry.streamlit.app)

## O que faz
- Pesquisa tendências de mercado em tempo real
- Gera slogan, conceito e estratégia da campanha
- Cria posts prontos para Instagram, LinkedIn e Twitter/X
- Escreve email marketing completo
- Sugere briefing para anúncios pagos (Google/Meta Ads)
- Exporta a campanha em arquivo markdown

## Stack
- Python
- Streamlit (interface web)
- LangChain + Groq (LLM)
- Serper API (busca web em tempo real)

## Como rodar localmente

1. Clone o repositório
2. Instale as dependências: pip install -r requirements.txt
3. Crie um arquivo .env com suas chaves:
   GROQ_KEY=sua_chave
   SERPER_KEY=sua_chave
4. Rode: streamlit run app.py

## Arquitetura
O agente segue um pipeline de 2 etapas:
1. Pesquisa - busca tendências de mercado em tempo real via Serper
2. Geração - envia os dados para o LLM que cria a campanha estruturada

## Autor
Luca Faustino - GitHub: https://github.com/faustinoluca-spec