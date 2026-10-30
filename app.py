import streamlit as st
import pandas as pd
import altair as alt
import json
import re

from security_utils import anonimizar_nome, sanitizar_texto_lgpd, html_seguro
from workflow_engine import executar_workflow_demo

# Configuração da Página
st.set_page_config(
    page_title="FoodDesk AI | Assistente operacional com IA",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= ESTADO INICIAL DE NAVEGAÇÃO E TEMA =================
if "pagina_ativa" not in st.session_state:
    st.session_state.pagina_ativa = "Home"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ================= PALETA DINÂMICA (LIGHT MODE vs DARK MODE) =================
if st.session_state.dark_mode:
    bg_app = "#0E1117"
    bg_card = "#1A1C24"
    text_main = "#F3F4F6"
    text_muted = "#9CA3AF"
    border_col = "#2D313E"
else:
    bg_app = "#F7F7F7"
    bg_card = "#FFFFFF"
    text_main = "#3E3E3E"
    text_muted = "#6B7280"
    border_col = "#EAEAEA"

# ================= CSS DINÂMICO E CORREÇÃO DO TOPO =================
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_app};
        color: {text_main};
    }}

    /* Padding superior ajustado para NÃO cortar a barra vinho no topo */
    .block-container {{
        padding-top: 3.2rem !important;
        padding-bottom: 3rem !important;
    }}

    /* Barra de Acessibilidade Superior (Vinho Escuro) */
    .top-bar {{
        background-color: #9E0B16;
        color: white;
        padding: 10px 24px;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 10px 10px 0 0;
        line-height: 1.4;
    }}

    /* Header / Logo Container */
    .brand-bar {{
        background-color: {bg_card};
        padding: 16px 28px;
        border: 1px solid {border_col};
        border-top: none;
        border-radius: 0 0 12px 12px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }}
    .fooddesk-logo {{
        color: #EA1D2C;
        font-size: 2.1rem;
        font-weight: 900;
        letter-spacing: -1px;
        font-style: italic;
        line-height: 1;
    }}

    /* Títulos Estilo Página Oficial */
    .hero-title {{
        color: #EA1D2C;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }}
    .hero-subtitle {{
        color: {text_muted};
        font-size: 1.55rem;
        font-weight: 600;
        margin-bottom: 18px;
    }}
    .section-red-title {{
        color: #EA1D2C;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 14px;
    }}

    /* Cards Customizados */
    .custom-card {{
        background-color: {bg_card};
        color: {text_main};
        padding: 24px 26px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid {border_col};
        margin-bottom: 18px;
    }}
    .ai-first-header {{
        color: {text_muted};
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }}
    .card-body-text {{
        color: {text_main};
        font-size: 0.96rem;
        line-height: 1.65;
    }}

    /* Cards de resultado com borda lateral */
    .agent-box {{
        background-color: {bg_card};
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        border: 1px solid {border_col};
        border-left: 6px solid #EA1D2C;
    }}
    .agent-label {{
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        color: {text_muted};
        margin-bottom: 6px;
    }}
    .agent-text {{
        font-size: 1rem;
        color: {text_main};
        font-weight: 500;
        line-height: 1.5;
    }}

    /* Botões em Pílula */
    .stButton>button {{
        background-color: #EA1D2C;
        color: white !important;
        font-weight: 700;
        border-radius: 50px;
        border: none;
        padding: 0.55rem 1.2rem;
        transition: 0.2s all;
        box-shadow: 0 3px 8px rgba(234, 29, 44, 0.2);
    }}
    .stButton>button:hover {{
        background-color: #B81420;
        transform: translateY(-1px);
    }}

    /* Badges */
    .pill-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 8px;
    }}
    .badge-red {{ background-color: rgba(220, 38, 38, 0.15); color: #EF4444; border: 1px solid #EF4444; }}
    .badge-green {{ background-color: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid #10B981; }}
    .badge-gray {{ background-color: rgba(107, 114, 128, 0.15); color: {text_main}; border: 1px solid {border_col}; }}

    /* Métricas Padronizadas com espaçamento inferior */
    div[data-testid="stMetric"] {{
        background-color: {bg_card};
        border: 1px solid {border_col};
        padding: 18px 22px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
        border-top: 4px solid #EA1D2C;
        margin-bottom: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# ================= BARRA LATERAL: SEGURANÇA E CONTRASTE =================
st.sidebar.markdown(f"<h2 style='color:#EA1D2C; margin-bottom:0;'>FoodDesk AI <span style='color:{text_main}; font-weight:400;'>| Segurança</span></h2>", unsafe_allow_html=True)
st.sidebar.caption("Protótipo Independente · Governança e Acessibilidade")
st.sidebar.markdown("---")

modo_escuro = st.sidebar.toggle("🌗 Tema escuro", value=st.session_state.dark_mode)
if modo_escuro != st.session_state.dark_mode:
    st.session_state.dark_mode = modo_escuro
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Ambiente demonstrativo")
st.sidebar.success("Modo Demo ativo · sem chamadas externas")
st.sidebar.caption(
    "A análise generativa é simulada por regras locais. Nenhuma chave de API, "
    "webhook ou serviço de terceiros é utilizado nesta versão pública."
)
st.sidebar.markdown("---")
st.sidebar.subheader("🛡️ Camada de Proteção")
st.sidebar.caption(
    "A sanitização mascara alguns padrões comuns de dados pessoais. "
    "Não garante anonimização completa nem conformidade integral com a LGPD."
)

if "workflow_resultado" not in st.session_state:
    st.session_state.workflow_resultado = None
if "diagnostico_executivo" not in st.session_state:
    st.session_state.diagnostico_executivo = None

# ================= DADOS INICIAIS NA SESSÃO (100% FICTÍCIOS E ANONIMIZADOS) =================
if "avaliacoes" not in st.session_state:
    st.session_state.avaliacoes = [
        {"Cliente": "Lucas M***", "Pedido": "#4092", "Nota": 1, "Comentario": "Meu lanche chegou completamente frio e o refrigerante veio errado. Demorou 1h30!", "Categoria": "Logística / Atraso", "Sentimento": "Crítico", "Acao": "Cupom R$15 + Alerta Gerente"},
        {"Cliente": "Fernanda S***", "Pedido": "#4095", "Nota": 5, "Comentario": "Hambúrguer sensacional, chegou super rápido e quentinho!", "Categoria": "Elogio", "Sentimento": "Positivo", "Acao": "Agradecimento Padrão"},
        {"Cliente": "Marcos T***", "Pedido": "#4102", "Nota": 2, "Comentario": "Faltou a batata frita que eu paguei a mais. Meu tel é [TELEFONE OCULTO - LGPD].", "Categoria": "Item Faltante", "Sentimento": "Negativo", "Acao": "Estorno Parcial"},
        {"Cliente": "Beatriz R***", "Pedido": "#4115", "Nota": 1, "Comentario": "A embalagem veio rasgada e o açaí derramou todo na sacola.", "Categoria": "Embalagem", "Sentimento": "Crítico", "Acao": "Reembolso Integral"},
        {"Cliente": "Roberto A***", "Pedido": "#4130", "Nota": 1, "Comentario": "Pedido atrasou mais de 1 hora e chegou gelado.", "Categoria": "Logística / Atraso", "Sentimento": "Crítico", "Acao": "Cupom R$15 + Alerta Logística"}
    ]

if "cenario_cliente" not in st.session_state:
    st.session_state.cenario_cliente = "Mariana Costa"
    st.session_state.cenario_pedido = "#4188"
    st.session_state.cenario_nota = 1
    st.session_state.cenario_comentario = "O motoboy entregou o pedido todo revirado e atrasou 45 min! Meu CPF é 123.456.789-01 e meu zap é (11) 91234-5678, quero estorno!"

# ================= TOP BAR & MENU DE NAVEGAÇÃO INTERATIVO =================
status_contraste = "⚫ MODO ESCURO ATIVO" if st.session_state.dark_mode else "⚪ MODO CLARO ATIVO"
st.markdown(f"""
    <div class="top-bar">
        <div>FoodDesk AI &nbsp;|&nbsp; <b>Protótipo demonstrativo</b></div>
        <div>INTERFACE EXPERIMENTAL &nbsp;|&nbsp; TEMA: {status_contraste} &nbsp;|&nbsp; PT-BR</div>
    </div>
    <div class="brand-bar">
        <div class="fooddesk-logo">FoodDesk AI</div>
        <div style="font-size: 0.9rem; font-weight: 600; color: {text_muted};">
            Protótipo Independente · Operações com IA &nbsp;|&nbsp; Página Atual: <b style="color:#EA1D2C;">{st.session_state.pagina_ativa}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5 = st.columns(5)
if nav1.button("🏠 Home (App IA)", use_container_width=True):
    st.session_state.pagina_ativa = "Home"
    st.rerun()
if nav2.button("❤️ Cultura AI First", use_container_width=True):
    st.session_state.pagina_ativa = "Cultura"
    st.rerun()
if nav3.button("🎓 Programas GenAI", use_container_width=True):
    st.session_state.pagina_ativa = "Programas"
    st.rerun()
if nav4.button("📈 Simulador de impacto", use_container_width=True):
    st.session_state.pagina_ativa = "Efeito"
    st.rerun()
if nav5.button("🛡️ Segurança & LGPD", use_container_width=True):
    st.session_state.pagina_ativa = "Seguranca"
    st.rerun()

st.markdown("<hr style='margin-top: 8px; margin-bottom: 24px; opacity: 0.2;'>", unsafe_allow_html=True)

# ==============================================================================
# PÁGINA 1: HOME (O PRODUTO PRINCIPAL + DASHBOARD ALINHADO)
# ==============================================================================
if st.session_state.pagina_ativa == "Home":
    h_col1, h_col2 = st.columns([1.35, 1], gap="large")

    with h_col1:
        st.markdown(f"""
            <div class="hero-title">FoodDesk AI -<br>GenAI</div>
            <div class="hero-subtitle">Brasil · Operações & CX</div>
            <div class="section-red-title">Nosso modo de fazer no time</div>
            <p class="card-body-text">
                Protótipo Independente na linha de <b>AI Builder</b>: explora como IA generativa pode apoiar a triagem de avaliações, recomendações operacionais e automações, com atenção à proteção de dados.
            </p>
        """, unsafe_allow_html=True)

    with h_col2:
        st.markdown("""
            <div class="custom-card">
                <div class="ai-first-header">INTELIGÊNCIA EM AÇÃO</div>
                <div class="card-body-text">
                    Este protótipo explora IA como multiplicador de força: um fluxo assistido classifica avaliações e gera diagnósticos. As recomendações são sugestões e não executam ações reais.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    aba1, aba2 = st.tabs(["🧪 Workflow Demonstrativo", "📊 Dashboard Executivo & Analytics"])

    # --- ABA 1: WORKFLOW DEMONSTRATIVO ---
    with aba1:
        st.info(
            "Demonstração transparente: entrada, sanitização, validação e apresentação "
            "são executadas localmente. A análise que seria feita pelo Gemini é representada "
            "por uma saída determinística, sem chamada a modelo."
        )
        col1, col2 = st.columns([1, 1.05], gap="large")

        with col1:
            st.markdown('<div class="section-red-title">Entrada de avaliação</div>', unsafe_allow_html=True)
            st.caption("Escolha um cenário fictício ou edite os campos.")

            b1, b2, b3 = st.columns(3)
            if b1.button("🚨 Atraso + CPF", use_container_width=True):
                st.session_state.cenario_cliente = "Mariana Costa"
                st.session_state.cenario_pedido = "#4188"
                st.session_state.cenario_nota = 1
                st.session_state.cenario_comentario = "O motoboy entregou o pedido todo revirado e atrasou 45 min! Meu CPF é 123.456.789-01 e meu zap é (11) 91234-5678, quero estorno!"
                st.session_state.cliente_input = st.session_state.cenario_cliente
                st.session_state.pedido_input = st.session_state.cenario_pedido
                st.session_state.nota_input = st.session_state.cenario_nota
                st.session_state.comentario_input = st.session_state.cenario_comentario
                st.session_state.pop("workflow_resultado", None)
                st.rerun()
            if b2.button("🍟 Item Faltando", use_container_width=True):
                st.session_state.cenario_cliente = "Rafael Souza"
                st.session_state.cenario_pedido = "#4201"
                st.session_state.cenario_nota = 2
                st.session_state.cenario_comentario = "Pedi dois combos e faltou a batata. Meu email é cliente.ficticio@exemplo.com, aguardo retorno."
                st.session_state.cliente_input = st.session_state.cenario_cliente
                st.session_state.pedido_input = st.session_state.cenario_pedido
                st.session_state.nota_input = st.session_state.cenario_nota
                st.session_state.comentario_input = st.session_state.cenario_comentario
                st.session_state.pop("workflow_resultado", None)
                st.rerun()
            if b3.button("😍 Elogio Nota 5", use_container_width=True):
                st.session_state.cenario_cliente = "Juliana Lima"
                st.session_state.cenario_pedido = "#4210"
                st.session_state.cenario_nota = 5
                st.session_state.cenario_comentario = "Simplesmente perfeito! Chegou 15 minutos antes do prazo, lanche super quente!"
                st.session_state.cliente_input = st.session_state.cenario_cliente
                st.session_state.pedido_input = st.session_state.cenario_pedido
                st.session_state.nota_input = st.session_state.cenario_nota
                st.session_state.comentario_input = st.session_state.cenario_comentario
                st.session_state.pop("workflow_resultado", None)
                st.rerun()

            # Valores dos widgets são inicializados uma vez e atualizados pelos cenários rápidos.
            for chave, valor in {
                "cliente_input": st.session_state.cenario_cliente,
                "pedido_input": st.session_state.cenario_pedido,
                "nota_input": st.session_state.cenario_nota,
                "comentario_input": st.session_state.cenario_comentario,
            }.items():
                if chave not in st.session_state:
                    st.session_state[chave] = valor

            cliente_bruto = st.text_input("Nome fictício do cliente", key="cliente_input")
            pedido_bruto = st.text_input("Identificador fictício do pedido", max_chars=30, key="pedido_input")
            pedido = re.sub(r"[^A-Za-z0-9#_-]", "", pedido_bruto)[:30]
            nota = st.slider("Nota da avaliação", 1, 5, key="nota_input")
            comentario_bruto = st.text_area(
                "Comentário do cliente",
                height=110,
                max_chars=1000,
                key="comentario_input",
                help="Use apenas dados fictícios. O texto é processado localmente nesta demonstração."
            )
            executar = st.button("▶ Executar workflow demonstrativo", use_container_width=True)

        with col2:
            st.markdown('<div class="section-red-title">Execução do workflow</div>', unsafe_allow_html=True)

            if executar:
                try:
                    with st.spinner("Executando etapas locais e preparando a demonstração..."):
                        resultado_workflow = executar_workflow_demo(int(nota), comentario_bruto)
                    st.session_state.workflow_resultado = resultado_workflow
                    st.session_state.avaliacoes.append({
                        "Cliente": anonimizar_nome(cliente_bruto),
                        "Pedido": pedido,
                        "Nota": int(nota),
                        "Comentario": resultado_workflow["comentario_sanitizado"],
                        "Categoria": resultado_workflow["resultado"]["categoria"],
                        "Sentimento": resultado_workflow["resultado"]["sentimento"],
                        "Acao": resultado_workflow["resultado"]["acao_operacional"],
                    })
                    st.success("Workflow demonstrativo concluído.")
                except (TypeError, ValueError) as erro:
                    st.error(f"Não foi possível executar a demonstração: {erro}")

            resultado_workflow = st.session_state.get("workflow_resultado")
            if not resultado_workflow:
                st.markdown("""
                    <div class="agent-box" style="border-left-color: #9CA3AF;">
                        <div class="agent-label">Status do pipeline</div>
                        <div class="agent-text">
                            Aguardando uma avaliação. Escolha um cenário e execute o workflow
                            para visualizar as cinco etapas.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("Resumo de execução · 0 chamadas externas · sem persistência em banco de dados")
                for indice, etapa in enumerate(resultado_workflow["etapas"], start=1):
                    status_label = "SIMULADA" if etapa["status"] == "simulada" else "EXECUTADA LOCALMENTE"
                    status_icon = "🧪" if etapa["status"] == "simulada" else "✓"
                    with st.expander(f"{status_icon} Etapa {indice} — {etapa['titulo']} · {status_label}", expanded=(indice == 3)):
                        st.write(etapa["descricao"])
                        st.caption(etapa["detalhe"])

                dados_analise = resultado_workflow["resultado"]
                cor_badge = "badge-red" if dados_analise["sentimento"] in ["Crítico", "Negativo"] else "badge-green"
                st.markdown(f"""
                    <div class="agent-box">
                        <div class="agent-label">Classificação demonstrativa</div>
                        <div class="agent-text">
                            <span class="pill-badge {cor_badge}">{html_seguro(dados_analise['sentimento'])}</span>
                            <span class="pill-badge badge-gray">{html_seguro(dados_analise['categoria'])}</span>
                            <div style="margin-top:8px;"><b>Síntese:</b> {html_seguro(dados_analise['resumo_causa'])}</div>
                        </div>
                    </div>
                    <div class="agent-box" style="border-left-color: #F59E0B;">
                        <div class="agent-label">Recomendação operacional (não executada)</div>
                        <div class="agent-text">{html_seguro(dados_analise['acao_operacional'])}</div>
                    </div>
                    <div class="agent-box" style="border-left-color: #10B981;">
                        <div class="agent-label">Resposta sugerida (não enviada)</div>
                        <div class="agent-text"><i>"{html_seguro(dados_analise['resposta_cliente'])}"</i></div>
                    </div>
                """, unsafe_allow_html=True)

                with st.expander("🔍 Por dentro da IA: prompt e contrato de dados"):
                    st.markdown("**Prompt de referência para uma futura integração com Gemini**")
                    st.code(resultado_workflow["prompt_referencia"], language="text")
                    st.markdown("**JSON de saída esperado**")
                    st.json(dados_analise)
                    st.caption(
                        "O prompt é exibido para fins didáticos e não foi enviado a nenhum modelo. "
                        "A saída acima foi produzida por regras locais determinísticas."
                    )
                st.warning(resultado_workflow["aviso"])

    # --- ABA 2: DASHBOARD EXECUTIVO COM GRÁFICOS ALINHADOS ---
    with aba2:
        df = pd.DataFrame(st.session_state.avaliacoes)

        st.markdown('<div class="section-red-title">Indicadores da Operação</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Avaliações Analisadas", len(df))
        k2.metric("Nota Média", f"{df['Nota'].mean():.1f} ⭐")
        k3.metric("Casos Críticos", len(df[df['Nota'] <= 2]))
        k4.metric("Proteção de dados", "Sanitização demonstrativa")

        st.markdown("<br>", unsafe_allow_html=True)

        g1, g2 = st.columns(2, gap="large")
        with g1:
            st.markdown("**📊 Ocorrências por Categoria**")
            df_cat = df["Categoria"].value_counts().reset_index()
            df_cat.columns = ["Categoria", "Quantidade"]
            chart_cat = alt.Chart(df_cat).mark_bar(
                color="#EA1D2C",
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6,
                size=42
            ).encode(
                x=alt.X("Categoria:N", sort="-y", title=None, axis=alt.Axis(labelAngle=0, labelFontSize=12)),
                y=alt.Y("Quantidade:Q", title="Total de Casos", axis=alt.Axis(tickMinStep=1)),
                tooltip=["Categoria", "Quantidade"]
            ).properties(height=280)
            st.altair_chart(chart_cat, use_container_width=True)

        with g2:
            st.markdown("**🎯 Volume por Sentimento**")
            df_sent = df["Sentimento"].value_counts().reset_index()
            df_sent.columns = ["Sentimento", "Quantidade"]
            chart_sent = alt.Chart(df_sent).mark_bar(
                color="#9E0B16",
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6,
                size=48
            ).encode(
                x=alt.X("Sentimento:N", sort="-y", title=None, axis=alt.Axis(labelAngle=0, labelFontSize=12)),
                y=alt.Y("Quantidade:Q", title="Total de Avaliações", axis=alt.Axis(tickMinStep=1)),
                tooltip=["Sentimento", "Quantidade"]
            ).properties(height=280)
            st.altair_chart(chart_sent, use_container_width=True)

        st.markdown("**📋 Histórico de Avaliações (Dados de demonstração sanitizados)**")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-red-title">Diagnóstico executivo demonstrativo</div>', unsafe_allow_html=True)
        st.caption(
            "Os indicadores são calculados localmente com Python e Pandas. "
            "A interpretação abaixo usa regras fixas, não um modelo generativo."
        )
        if st.button("📊 Gerar diagnóstico operacional demonstrativo"):
            if df.empty:
                st.warning("Ainda não existem avaliações para analisar.")
            else:
                total_avaliacoes = len(df)
                nota_media = float(df["Nota"].mean())
                casos_criticos = int((df["Nota"] <= 2).sum())
                percentual_criticos = (casos_criticos / total_avaliacoes) * 100
                distribuicao = df["Categoria"].value_counts()
                categoria_principal = str(distribuicao.index[0])

                categorias_permitidas = {
                    "Logística / Atraso",
                    "Item Faltante",
                    "Qualidade da Comida",
                    "Embalagem",
                    "Elogio",
                }

                if categoria_principal not in categorias_permitidas:
                    categoria_principal = "Outros"
                quantidade_principal = int(distribuicao.iloc[0])
                percentual_negativos = (
                    df["Sentimento"].isin(["Crítico", "Negativo"]).sum()
                    / total_avaliacoes
                ) * 100

                if percentual_criticos >= 40:
                    leitura = "A amostra apresenta proporção relevante de avaliações com notas baixas. Recomenda-se priorizar a investigação dos casos críticos."
                elif nota_media >= 4:
                    leitura = "A nota média da amostra é positiva. Vale identificar práticas associadas às boas experiências e acompanhar recorrências negativas."
                else:
                    leitura = "Os indicadores sugerem oportunidades de melhoria. Recomenda-se investigar os temas mais recorrentes antes de definir ações."

                diagnostico = f"""
**1. Principal ocorrência**

A categoria mais frequente é **{categoria_principal}**, com {quantidade_principal} registro(s) ({quantidade_principal / total_avaliacoes:.1%} da amostra).

**2. Satisfação observada**

A nota média é **{nota_media:.2f}/5**. Existem **{casos_criticos} avaliações com nota até 2** ({percentual_criticos:.1f}%). Avaliações classificadas como negativas ou críticas representam **{percentual_negativos:.1f}%** da amostra.

**3. Ações para investigação**

- Investigar os registros associados à categoria mais frequente.
- Revisar os casos de nota baixa e acompanhar se o problema se repete.

**Leitura demonstrativa:** {leitura}

*Análise descritiva da amostra fictícia da sessão. Não comprova causas nem impacto financeiro.*
"""
                st.session_state.diagnostico_executivo = diagnostico

        if st.session_state.get("diagnostico_executivo"):
            st.markdown(st.session_state.diagnostico_executivo)

# ==============================================================================
# PÁGINA 2: PRINCÍPIOS DE CONSTRUÇÃO COM IA
# ==============================================================================
elif st.session_state.pagina_ativa == "Cultura":
    st.markdown('<div class="hero-title">Construção AI First</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Princípios de construção responsável com IA</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
            <div class="custom-card">
                <div class="section-red-title">🚀 1. IA como Multiplicador de Força (IA como ferramenta de trabalho)</div>
                <p class="card-body-text">
                    O <b>FoodDesk AI</b> explora como uma esteira assistida por IA pode classificar avaliações e sugerir respostas, reduzindo trabalho repetitivo. O impacto real precisa ser medido em testes com usuários.
                </p>
            </div>
            <div class="custom-card">
                <div class="section-red-title">⚡ 2. Vibe Coding & Velocidade de Entrega</div>
                <p class="card-body-text">
                    Construído com foco em geração de valor imediato: partimos de um problema operacional hipotético — priorizar avaliações e identificar padrões — para um protótipo demonstrativo com interface executiva, workflow local simulado e análise de dados.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
            <div class="custom-card">
                <div class="section-red-title">🎯 3. Obsessão pelo Cliente e pelo Parceiro</div>
                <p class="card-body-text">
                    Avaliações negativas podem indicar problemas que merecem investigação; a relação com retenção precisa ser validada com dados reais. O prompt foi elaborado com <i>Prompt Engineering</i> focado em empatia e sugestões de investigação da causa raiz.
                </p>
            </div>
            <div class="custom-card">
                <div class="section-red-title">🛡️ 4. Inovação com Responsabilidade (Privacy by Design)</div>
                <p class="card-body-text">
                    Velocidade não significa abrir mão de governança. O fluxo demonstrativo aplica sanitização local antes da etapa simulada, reduzindo a exposição de alguns padrões de dados, sem garantir anonimização completa ou conformidade integral.
                </p>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PÁGINA 3: PROGRAMAS (ADEQUAÇÃO À VAGA REF. 100233)
# ==============================================================================
elif st.session_state.pagina_ativa == "Programas":
    st.markdown('<div class="hero-title">Competências AI Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Como o protótipo demonstra competências de AI Builder</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="custom-card">
            <div class="section-red-title">Como o FoodDesk AI se relaciona com competências da trilha AI Builder</div>
            <p class="card-body-text">
                A tabela relaciona competências mencionadas na descrição da vaga com aspectos demonstráveis neste protótipo independente. Ela não representa avaliação ou endosso do iFood.
            </p>
        </div>
    """, unsafe_allow_html=True)

    df_requisitos = pd.DataFrame([
        {"Requisito da Vaga (AI Builder)": "Prompt engineering", "Implementação no FoodDesk AI": "Prompt com instruções de saída JSON e validação dos campos retornados; o modelo ainda pode falhar.", "Status": "🧪 Protótipo demonstrativo"},
        {"Requisito da Vaga (AI Builder)": "Fluxo assistido por IA", "Implementação no FoodDesk AI": "A simulação representa a saída que poderia ser produzida por uma chamada ao modelo; não há LLM nem agentes independentes ativos nesta versão.", "Status": "🧪 Protótipo demonstrativo"},
        {"Requisito da Vaga (AI Builder)": "Automações (n8n, Make, Zapier)", "Implementação no FoodDesk AI": "Arquitetura preparada conceitualmente para futura integração com Make ou n8n; webhooks estão desabilitados nesta versão pública.", "Status": "🧪 Protótipo demonstrativo"},
        {"Requisito da Vaga (AI Builder)": "Vibe Coding & Prototipação Rápida", "Implementação no FoodDesk AI": "Protótipo desenvolvido com apoio de ferramentas de IA e identidade visual própria, sem afiliação oficial.", "Status": "🧪 Protótipo demonstrativo"},
        {"Requisito da Vaga (AI Builder)": "Análise de Dados com IA & Dashboards", "Implementação no FoodDesk AI": "Indicadores e gráficos sobre o histórico fictício da sessão e diagnóstico executivo calculado localmente.", "Status": "🧪 Protótipo demonstrativo"}
    ])
    st.dataframe(df_requisitos, use_container_width=True, hide_index=True)

# ==============================================================================
# PÁGINA 4: SIMULADOR DE IMPACTO OPERACIONAL
# ==============================================================================
elif st.session_state.pagina_ativa == "Efeito":
    st.markdown('<div class="hero-title">Simulador de impacto</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Simulador Interativo de Impacto Operacional e Economia de Horas</div>', unsafe_allow_html=True)

    col_sim, col_res = st.columns([1, 1.2], gap="large")
    with col_sim:
        st.markdown('<div class="section-red-title">Parâmetros do Restaurante Parceiro</div>', unsafe_allow_html=True)
        pedidos_mes = st.slider("Volume de Pedidos por Mês", 500, 20000, 3500, step=500)
        taxa_avaliacao = st.slider("% de Pedidos com Comentários/Avaliações", 5, 40, 15)
        tempo_humano_min = st.slider("Tempo Médio Humano por Triagem/Resposta (minutos)", 2, 15, 6)
        ticket_medio = st.number_input("Ticket Médio do Restaurante (R$)", value=65.0, step=5.0)

    with col_res:
        st.markdown('<div class="section-red-title">Simulação hipotética de impacto mensal</div>', unsafe_allow_html=True)
        total_avaliacoes = int(pedidos_mes * (taxa_avaliacao / 100))
        horas_economizadas = (total_avaliacoes * tempo_humano_min) / 60
        clientes_recuperados = int(total_avaliacoes * 0.18)
        receita_protegida = clientes_recuperados * ticket_medio * 2.5

        r1, r2 = st.columns(2)
        r1.metric("Avaliações que poderiam ser triadas / Mês", f"{total_avaliacoes}")
        r2.metric("Horas Humanas Economizadas", f"{horas_economizadas:.1f} h/mês")

        r3, r4 = st.columns(2)
        r3.metric("Clientes potencialmente retidos*", f"{clientes_recuperados} clientes")
        r4.metric("Receita potencial estimada*", f"R$ {receita_protegida:,.2f}")

        st.markdown(f"""
            <div class="custom-card" style="margin-top: 8px;">
                <div class="ai-first-header">RESUMO DE IMPACTO</div>
                <p class="card-body-text">
                    Em uma operação com <b>{pedidos_mes} pedidos/mês</b>, o <b>FoodDesk AI</b> poderia liberar cerca de <b>{horas_economizadas:.0f} horas mensais</b> sob as premissas informadas. O valor de <b>R$ {receita_protegida:,.2f}</b> é uma estimativa hipotética, não um resultado medido.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.caption("*Estimativas ilustrativas, não resultados medidos. O simulador assume que 18% das avaliações representam clientes potencialmente recuperáveis e multiplica esse número pelo ticket médio e por 2,5 compras hipotéticas. Altere as premissas com cautela.")

# ==============================================================================
# PÁGINA 5: SEGURANÇA & IA (LABORATÓRIO DEMONSTRATIVO)
# ==============================================================================
elif st.session_state.pagina_ativa == "Seguranca":
    st.markdown('<div class="hero-title">Segurança & IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Arquitetura de Privacidade (LGPD) e Proteção de Credenciais</div>', unsafe_allow_html=True)

    s1, s2 = st.columns([1.1, 1], gap="large")
    with s1:
        st.markdown('<div class="section-red-title">🧪 Testador de sanitização (DLP demonstrativo)</div>', unsafe_allow_html=True)
        st.caption("Simulação com números sequenciais fictícios para demonstrar a interceptação de dados sensíveis antes de uma eventual integração externa:")

        # Nome, CPF e Telefone 100% fictícios e sequenciais
        nome_teste = st.text_input("Nome Completo Fictício", "Cliente Teste Silva")
        texto_teste = st.text_area(
            "Texto com Dados Sensíveis Sequenciais (PII Fictício)",
            "Olá, meu pedido atrasou! Meu CPF é 123.456.789-01, meu telefone é (11) 91234-5678 e meu e-mail é cliente.ficticio@exemplo.com.br.",
            height=110
        )

        st.markdown("**🔒 Exemplo de payload após sanitização (não representa garantia de anonimização):**")
        st.code(json.dumps({
            "cliente_anonimizado": anonimizar_nome(nome_teste),
            "comentario_sanitizado": sanitizar_texto_lgpd(texto_teste),
            "observacao": "Sanitização demonstrativa; não garante anonimização completa"
        }, indent=4, ensure_ascii=False), language="json")

    with s2:
        st.markdown('<div class="section-red-title">🛡️ Controles demonstrativos e limitações</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="custom-card">
                <b>1. Gestão de credenciais</b>
                <p class="card-body-text" style="margin-top:4px;">
                    A versão pública demonstrativa não solicita nem utiliza chave de API. Uma futura integração local com Gemini deverá ler a credencial fora do código-fonte. O <code>.gitignore</code> ajuda, mas não impede sozinho que um segredo já rastreado seja publicado.
                </p>
                <hr style="opacity:0.2;">
                <b>2. Filtro Regex DLP Pré-Inferência (CPF, Tel, Email, Cartão)</b>
                <p class="card-body-text" style="margin-top:4px;">
                    Na demonstração, expressões regulares varrem o texto e substituem alguns padrões comuns por tags de proteção, limitando também o tamanho do comentário. Nenhum modelo é invocado.
                </p>
                <hr style="opacity:0.2;">
                <b>3. Integrações externas desabilitadas</b>
                <p class="card-body-text" style="margin-top:4px;">
                    Esta versão pública não realiza chamadas de webhook nem envia dados a serviços externos. Uma futura integração deverá incluir autenticação, limites de uso e validação de destinos.
                </p>
                <hr style="opacity:0.2;">
                <b>4. Minimização de dados e mensagens de erro genéricas</b>
                <p class="card-body-text" style="margin-top:4px;">
                    O histórico da demonstração fica na sessão do Streamlit. Isso não é uma garantia de não retenção por provedores externos; erros técnicos são exibidos de forma genérica.
                </p>
            </div>
        """, unsafe_allow_html=True)