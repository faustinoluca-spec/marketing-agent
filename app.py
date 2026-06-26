import streamlit as st
import os
import requests
import re
import io
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
from reportlab.lib.units import cm

try:
    GROQ_KEY = st.secrets["GROQ_KEY"]
    SERPER_KEY = st.secrets["SERPER_KEY"]
except:
    GROQ_KEY = os.environ.get("GROQ_KEY")
    SERPER_KEY = os.environ.get("SERPER_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_KEY)

def buscar(query):
    r = requests.post("https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_KEY},
        json={"q": query, "num": 6})
    return "\n".join([f"- {x['title']}: {x.get('snippet','')}"
                      for x in r.json().get("organic", [])[:5]])

def ia(sistema, conteudo):
    prompt = ChatPromptTemplate.from_messages([
        ("system", sistema), ("human", conteudo)
    ])
    return (prompt | llm).invoke({}).content

def limpar(texto):
    texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    texto = texto.replace('&', '&amp;')
    texto = re.sub(r'<br\s*/?>', ' ', texto)
    texto = re.sub(r'<(?!b>|/b>)[^>]+>', '', texto)
    return texto

def gerar_pdf(estrategia, conteudo, empresa, produto, objetivo, orcamento, prazo, cores_marca):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    cor_primaria = HexColor('#6366f1')
    cor_secundaria = HexColor('#a855f7')
    cor_escura = HexColor('#0f0f1a')
    cor_texto = HexColor('#1e293b')
    cor_subtexto = HexColor('#64748b')
    capa_titulo = ParagraphStyle('capa_titulo', fontSize=36, textColor=white,
        fontName='Helvetica-Bold', spaceAfter=8, leading=42)
    capa_sub = ParagraphStyle('capa_sub', fontSize=14, textColor=HexColor('#a5b4fc'),
        fontName='Helvetica', spaceAfter=4, leading=20)
    capa_info = ParagraphStyle('capa_info', fontSize=10, textColor=HexColor('#94a3b8'),
        fontName='Helvetica', spaceAfter=4)
    section_title = ParagraphStyle('section_title', fontSize=18, textColor=cor_primaria,
        fontName='Helvetica-Bold', spaceAfter=12, spaceBefore=24)
    subsection_title = ParagraphStyle('subsection_title', fontSize=13, textColor=cor_secundaria,
        fontName='Helvetica-Bold', spaceAfter=8, spaceBefore=16)
    body = ParagraphStyle('body', fontSize=10, textColor=cor_texto,
        fontName='Helvetica', spaceAfter=6, leading=16)
    footer_style = ParagraphStyle('footer', fontSize=8, textColor=cor_subtexto,
        fontName='Helvetica', alignment=1)
    story = []
    story.append(Table(
        [[Paragraph("APEX Marketing Intelligence", capa_titulo)],
         [Paragraph(empresa, ParagraphStyle('emp', fontSize=28,
             textColor=HexColor('#e2e8f0'), fontName='Helvetica-Bold', spaceAfter=4))],
         [Paragraph(produto, capa_sub)],
         [Spacer(1, 20)],
         [HRFlowable(width="100%", thickness=1, color=cor_primaria)],
         [Spacer(1, 16)],
        ],
        colWidths=[18*cm],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), cor_escura),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 20),
            ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ])
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Table of Contents", section_title))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#e2e8f0')))
    story.append(Spacer(1, 12))
    fases = [
        "Phase 1: Business Intelligence & Audit",
        "Phase 2: Positioning & Irresistible Offer",
        "Phase 3: Traffic & Acquisition Strategy",
        "Phase 4: Conversion Infrastructure",
        "Phase 5: Retention & Automation",
        "Phase 6: Performance Dashboard",
        "Phase 7: Legal & Compliance",
        "Phase 8: Brand Equity & Awareness",
        "Phase 9: Omnichannel & Trade Marketing",
        "Phase 10: MarTech Stack & Data Intelligence",
        "Budget Allocation & ROI Projection",
        "Ready-to-Use Content Package",
    ]
    for i, fase in enumerate(fases, 1):
        story.append(Paragraph(f"{i:02d}. {fase}", body))
    story.append(PageBreak())

    def processar(texto):
        for linha in texto.split('\n'):
            linha = linha.strip()
            if not linha:
                story.append(Spacer(1, 4))
            elif linha.startswith('## '):
                story.append(HRFlowable(width="100%", thickness=0.5,
                    color=HexColor('#e2e8f0'), spaceAfter=8))
                story.append(Paragraph(limpar(linha[3:]), section_title))
            elif linha.startswith('### '):
                story.append(Paragraph(limpar(linha[4:]), subsection_title))
            elif linha.startswith('- ') or linha.startswith('* '):
                try:
                    story.append(Paragraph(f"• {limpar(linha[2:])}", body))
                except:
                    story.append(Paragraph(f"• {linha[2:]}", body))
            else:
                try:
                    story.append(Paragraph(limpar(linha), body))
                except:
                    story.append(Paragraph(re.sub(r'<[^>]+>', '', linha), body))

    processar(estrategia)
    story.append(PageBreak())
    story.append(Paragraph("READY-TO-USE CONTENT PACKAGE", section_title))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#e2e8f0')))
    processar(conteudo)
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=cor_primaria))
    story.append(Paragraph(
        "Generated by APEX Marketing Intelligence — AI-powered campaigns",
        footer_style
    ))
    doc.build(story)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="APEX Marketing Intelligence", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #08080f; }
.hero {
    text-align: center; padding: 60px 20px 50px;
    background: linear-gradient(180deg, rgba(99,102,241,0.08) 0%, transparent 100%);
    border-radius: 24px; margin-bottom: 40px;
    border: 1px solid rgba(99,102,241,0.15);
}
.hero-badge {
    display: inline-block; background: rgba(99,102,241,0.12); color: #818cf8;
    padding: 6px 18px; border-radius: 100px; font-size: 11px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 24px;
    border: 1px solid rgba(99,102,241,0.25);
}
.hero h1 { font-size: 54px; font-weight: 900; color: #fff; line-height: 1.1; margin: 0 0 16px; }
.hero h1 span { background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: #64748b; font-size: 17px; max-width: 560px; margin: 0 auto; line-height: 1.7; }
.card { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 24px; margin-bottom: 16px; }
.card-label { color: #6366f1; font-size: 10px; font-weight: 800;
    letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; }
.stTextInput > label, .stTextArea > label,
.stSelectbox > label, .stMultiSelect > label {
    color: #64748b !important; font-size: 12px !important; font-weight: 500 !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important; color: #e2e8f0 !important; font-size: 13px !important; }
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important; color: #e2e8f0 !important; }
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-size: 15px !important; font-weight: 700 !important; padding: 16px !important; width: 100% !important; }
.stMarkdown h2 { color: #818cf8 !important; font-size: 18px !important;
    border-bottom: 1px solid rgba(99,102,241,0.2) !important;
    padding-bottom: 10px !important; margin-top: 28px !important; }
.stMarkdown h3 { color: #a78bfa !important; font-size: 15px !important; }
p, li { color: #94a3b8 !important; }
strong { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI Marketing Intelligence</div>
    <h1>The <span>Full-Stack</span><br>Marketing Machine</h1>
    <p>10-phase campaigns that top agencies charge $50,000+ for.<br>Generated in minutes. Built on real market data.</p>
</div>
""", unsafe_allow_html=True)

col_form, col_result = st.columns([1, 1.6], gap="large")

with col_form:
    st.markdown('<div class="card"><div class="card-label">01 — Business Profile</div>', unsafe_allow_html=True)
    empresa = st.text_input("Company / Brand Name", placeholder="Nike, Tesla, Your Startup")
    produto = st.text_input("Product / Service", placeholder="Air Max 2026, SaaS Platform")
    segmento = st.selectbox("Business Model", ["B2C","B2B","B2B2C","D2C","Marketplace","SaaS","E-commerce"])
    setor = st.text_input("Industry / Niche", placeholder="Sportswear, FinTech, Health")
    faturamento = st.text_input("Current Monthly Revenue (optional)", placeholder="$50k/mo, Pre-revenue")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">02 — Target & Market</div>', unsafe_allow_html=True)
    publico = st.text_area("Target Audience", placeholder="Gen Z males 18-25, urban, sneaker culture", height=80)
    ticket = st.text_input("Price Point", placeholder="$180 one-time, $97/month")
    concorrentes = st.text_input("Main Competitors", placeholder="Adidas, New Balance, On Running")
    diferenciais = st.text_area("Unique Advantages", placeholder="Proprietary tech, brand legacy", height=60)
    objecoes = st.text_area("Customer Objections", placeholder="Too expensive, competitor is trendier", height=60)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">03 — Campaign Setup</div>', unsafe_allow_html=True)
    objetivo = st.selectbox("Primary Objective", [
        "Product Launch — New market entry",
        "Lead Generation — Fill the sales pipeline",
        "Brand Awareness — Category dominance",
        "Sales Conversion — Revenue acceleration",
        "Customer Retention — Reduce churn & increase LTV",
    ])
    orcamento = st.selectbox("Monthly Budget", [
        "Seed ($1k-$5k/mo)", "Growth ($5k-$20k/mo)",
        "Scale ($20k-$100k/mo)", "Enterprise ($100k+/mo)"
    ])
    prazo = st.selectbox("Campaign Duration", ["30 days","60 days","90 days","6 months","12 months"])
    canais = st.multiselect("Priority Channels", [
        "Instagram","TikTok","LinkedIn","Twitter/X",
        "YouTube","Google Ads","Meta Ads","Email","WhatsApp","SEO"
    ], default=["Instagram","Meta Ads","Google Ads","Email"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">04 — Brand Identity</div>', unsafe_allow_html=True)
    tom = st.selectbox("Brand Tone", [
        "Bold & Disruptive", "Premium & Sophisticated",
        "Human & Authentic", "Technical & Authoritative",
        "Fun & Energetic", "Minimalist & Clean"
    ])
    cores = st.text_input("Brand Colors", placeholder="Black, White, Volt Green")
    referencias = st.text_area("Visual References", placeholder="Supreme hype culture meets Apple minimalism", height=60)
    st.markdown('</div>', unsafe_allow_html=True)

    gerar = st.button("⚡ Generate Full 10-Phase Campaign", use_container_width=True)

with col_result:
    if gerar:
        if not empresa or not produto:
            st.warning("Please fill in Company and Product!")
        else:
            progress = st.progress(0)
            status = st.empty()

            status.markdown("**🔍 Researching market...**")
            m1 = buscar(f"{produto} {setor} market trends 2026 strategy")
            progress.progress(10)

            status.markdown("**🔍 Analyzing competitors...**")
            m2 = buscar(f"{concorrentes} {setor} marketing advertising 2026")
            progress.progress(20)

            status.markdown("**🔍 Profiling audience...**")
            m3 = buscar(f"{publico} {setor} consumer behavior 2026")
            progress.progress(30)

            canais_str = ", ".join(canais) if canais else "Instagram, Meta Ads, Google Ads, Email"

            sistema_base = f"""You are the Chief Strategy Officer of the world's #1 marketing agency.
You've built campaigns for Nike, Apple, Tesla, and Airbnb.
Brand tone: {tom}. Model: {segmento}. Budget: {orcamento}. Duration: {prazo}.
Channels: {canais_str}. Colors: {cores}. References: {referencias}.
IMPORTANT: Never use HTML tags like <br>, <p>, <div> in your response. Use plain text only."""

            contexto = f"""Company: {empresa} | Product: {produto} | Industry: {setor}
Target: {publico} | Price: {ticket} | Revenue: {faturamento}
Competitors: {concorrentes} | Differentiators: {diferenciais} | Objections: {objecoes}
Objective: {objetivo}
Market: {m1}
Competitors: {m2}
Audience: {m3}"""

            status.markdown("**⚡ Building 10-phase strategy...**")
            estrategia = ia(sistema_base, f"""{contexto}

Generate a COMPLETE 10-phase strategy for {empresa}. Be extremely specific — real numbers, real tactics.
Use ## for main sections and ### for subsections. No HTML tags.

## PHASE 1: BUSINESS INTELLIGENCE & AUDIT
## PHASE 2: POSITIONING & IRRESISTIBLE OFFER
## PHASE 3: TRAFFIC & ACQUISITION STRATEGY
## PHASE 4: CONVERSION INFRASTRUCTURE
## PHASE 5: RETENTION & AUTOMATION
## PHASE 6: PERFORMANCE DASHBOARD
## PHASE 7: LEGAL & COMPLIANCE
## PHASE 8: BRAND EQUITY & AWARENESS
## PHASE 9: OMNICHANNEL & TRADE MARKETING
## PHASE 10: MARTECH STACK & DATA INTELLIGENCE
## BUDGET ALLOCATION & ROI PROJECTION""")
            progress.progress(60)

            status.markdown("**✍️ Creating content package...**")
            conteudo = ia(sistema_base, f"""{contexto}

Write a COMPLETE ready-to-use content package. Every piece must be fully written.
Use ## for sections and ### for subsections. No HTML tags. No placeholders.

## INSTAGRAM — 5 COMPLETE POSTS
## TIKTOK — 3 VIDEO SCRIPTS
## LINKEDIN — 3 PROFESSIONAL POSTS
## TWITTER/X — 7 TWEETS
## EMAIL SEQUENCE 1: WELCOME/LAUNCH
## EMAIL SEQUENCE 2: ABANDONED CART
## GOOGLE ADS — 5 COMPLETE ADS
## META ADS — 5 COMPLETE CONCEPTS
## 4-WEEK EDITORIAL CALENDAR""")
            progress.progress(85)

            status.markdown("**📄 Generating PDF...**")
            pdf = gerar_pdf(estrategia, conteudo, empresa, produto, objetivo, orcamento, prazo, cores)
            progress.progress(100)
            status.empty()

            tab1, tab2, tab3 = st.tabs(["📋 10-Phase Strategy", "✍️ Content Package", "📊 Visual Summary"])

            with tab1:
                st.markdown(estrategia)

            with tab2:
                st.markdown(conteudo)

            with tab3:
                st.markdown("### Campaign Overview")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Budget", orcamento.split("(")[1].replace(")", "") if "(" in orcamento else orcamento)
                    st.metric("Duration", prazo)
                with col_b:
                    st.metric("Channels", str(len(canais)))
                    st.metric("Content Pieces", "23+")
                with col_c:
                    st.metric("Strategy Phases", "10")
                    st.metric("Ads Created", "10")

                st.markdown("### Campaign Brief")
                st.markdown(f"""
| Field | Details |
|-------|---------|
| Company | {empresa} |
| Product | {produto} |
| Objective | {objetivo} |
| Target | {publico[:80]}... |
| Price Point | {ticket} |
| Brand Tone | {tom} |
| Competitors | {concorrentes} |
""")

            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 Download PDF Report", data=pdf,
                    file_name=f"APEX_Campaign_{empresa.replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)
            with col2:
                full = f"# {empresa} — {produto}\n\n{estrategia}\n\n---\n\n{conteudo}"
                st.download_button("📝 Download Markdown", data=full,
                    file_name=f"APEX_Campaign_{empresa.replace(' ','_')}.md",
                    mime="text/markdown", use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:100px 40px;">
            <div style="font-size:72px;margin-bottom:24px;">⚡</div>
            <h3 style="color:#334155;font-size:22px;font-weight:700;margin-bottom:12px;">Fill in your brief</h3>
            <p style="color:#475569;font-size:14px;line-height:1.8;">
                Complete 10-phase strategy + full content package<br>
                + professional PDF report in under 3 minutes.<br><br>
                <strong style="color:#6366f1;">Strategy · Content · PDF · Visual Summary</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)