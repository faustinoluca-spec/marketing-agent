import streamlit as st
import os
import requests
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

try:
    GROQ_KEY = st.secrets["GROQ_KEY"]
    SERPER_KEY = st.secrets["SERPER_KEY"]
except:
    GROQ_KEY = os.environ.get("GROQ_KEY")
    SERPER_KEY = os.environ.get("SERPER_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_KEY)

def buscar_web(query):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_KEY}
    payload = {"q": query, "gl": "br", "hl": "pt-br", "num": 5}
    resposta = requests.post(url, headers=headers, json=payload)
    dados = resposta.json()
    resultados = dados.get("organic", [])
    texto = ""
    for r in resultados:
        texto += f"- {r['title']}: {r.get('snippet', '')}\n"
    return texto

def chamar_ia(sistema, conteudo):
    prompt = ChatPromptTemplate.from_messages([
        ("system", sistema),
        ("human", conteudo)
    ])
    chain = prompt | llm
    return chain.invoke({}).content

st.set_page_config(page_title="Marketing Agent", page_icon="🎯", layout="wide")
st.title("🎯 Marketing Agent")
st.subheader("Gere campanhas completas com IA em segundos")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Sobre o produto")
    produto = st.text_input("Nome do produto ou empresa", placeholder="Ex: Nike Air Max")
    publico = st.text_input("Publico-alvo", placeholder="Ex: jovens 18-30 anos")
    tom = st.selectbox("Tom da campanha", ["Moderno e jovem", "Profissional", "Divertido", "Luxuoso", "Minimalista"])
    gerar = st.button("Gerar campanha", type="primary", use_container_width=True)

with col2:
    if gerar:
        if not produto:
            st.warning("Digite o nome do produto!")
        else:
            st.write("Iniciando geracao da campanha...")
            with st.spinner("Pesquisando o mercado..."):
                pesquisa = buscar_web(f"{produto} marketing trends 2026 Brazil")
            with st.spinner("Criando sua campanha..."):
                campanha = chamar_ia(
                    f"Voce e um especialista em marketing digital com 20 anos de experiencia. Tom da campanha: {tom}.",
                    f"""Com base na pesquisa de mercado abaixo, crie uma campanha completa para {produto} direcionada para {publico}.

Pesquisa de mercado:
{pesquisa}

Crie exatamente nessa estrutura:

## Slogan
[um slogan impactante]

## Conceito da campanha
[2-3 paragrafos explicando a ideia central]

## Instagram (3 posts)
[3 posts completos com caption e hashtags]

## LinkedIn (1 post)
[post profissional completo]

## Twitter/X (3 tweets)
[3 tweets prontos para publicar]

## Email marketing
[assunto + corpo do email completo]

## Sugestao de anuncio pago
[descricao do anuncio para Google/Meta Ads]"""
                )
            st.markdown(campanha)
            st.download_button(
                label="Baixar campanha",
                data=campanha,
                file_name=f"campanha_{produto.replace(' ', '_')}.md",
                mime="text/markdown"
            )
    else:
        st.info("Preencha os campos e clique em Gerar campanha!")