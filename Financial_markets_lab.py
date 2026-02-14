"""
Laboratório de Mercado Financeiro - Aplicativo Principal
"""

import streamlit as st

# Configuração da página (deve ser a primeira chamada Streamlit)
st.set_page_config(
    page_title="Laboratório de Mercado Financeiro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Importação dos módulos
import module_01_ettj
import module_02_credit_risk
import module_03_fidc
import module_04_baas
import module_05_tokenization
import module_06_financial_regulation
import module_07_suggestions

# =============================================================================
# DEFINIÇÃO DOS MÓDULOS
# =============================================================================

MODULES = [
    {"key": "M1", "icon": "📈", "title": "Estrutura a Termo de Taxas de Juros",
     "render": module_01_ettj.render},
    {"key": "M2", "icon": "🧪", "title": "Modelagem de Risco de Crédito",
     "render": module_02_credit_risk.render},
    {"key": "M3", "icon": "⚖️", "title": "Fundos de Investimento em Direitos Creditórios",
     "render": module_03_fidc.render},
    {"key": "M4", "icon": "🏛️", "title": "Banking as a Service",
     "render": module_04_baas.render},
    {"key": "M5", "icon": "📊", "title": "Tokenização de Ativos",
     "render": module_05_tokenization.render},
    {"key": "M6", "icon": "🏦", "title": "Regulação Bancária",
     "render": module_06_financial_regulation.render},
    {"key": "SUG", "icon": "💬", "title": "Sugestões e Dúvidas  Fale com o Professor",
     "render": module_07_suggestions.render},
]

# =============================================================================
# SESSION STATE
# =============================================================================

if "selected_module" not in st.session_state:
    st.session_state.selected_module = None


def go_to_module(key):
    st.session_state.selected_module = key


def go_to_hub():
    st.session_state.selected_module = None


# =============================================================================
# HUB
# =============================================================================

def render_hub():
    """Renderiza a página principal com cards de módulos."""

    # CSS para cards e layout
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');

        .main {
            background-color: #f8fafc;
            font-family: 'Montserrat', sans-serif;
        }

        /* ========== HEADER ========== */
        .hub-header {
            text-align: center;
            padding: 2rem 0 1rem 0;
        }
        .hub-header h1 {
            font-size: 2rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.3rem;
        }
        .hub-header p {
            font-size: 1rem;
            color: #888;
        }

        /* ========== CARD BUTTONS ========== */
        .stButton > button {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            padding: 18px 12px !important;
            min-height: 110px !important;
            width: 100% !important;
            color: #1e293b !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            line-height: 1.4 !important;
            white-space: pre-wrap !important;
            text-align: center !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
            border-color: #c0392b !important;
            color: #c0392b !important;
        }

        .stButton > button:active {
            transform: translateY(0px) !important;
        }

        .stButton > button:focus:not(:active) {
            border-color: #c0392b !important;
            box-shadow: 0 0 0 3px rgba(192,57,43,0.12) !important;
        }

        /* ========== FOOTER ========== */
        .hub-footer {
            text-align: center;
            color: #999;
            font-size: 0.85em;
            padding: 1rem 0 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="hub-header">
        <h1>📊 Laboratório de Mercado Financeiro</h1>
        <p>Selecione um módulo para começar</p>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: M1, M2, M3
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            mod = MODULES[i]
            if st.button(
                f"{mod['icon']}\n\n{mod['title']}",
                key=f"btn_{mod['key']}",
                use_container_width=True,
                on_click=go_to_module,
                args=(mod["key"],)
            ):
                pass

    # Row 2: M4, M5, M6
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            mod = MODULES[i + 3]
            if st.button(
                f"{mod['icon']}\n\n{mod['title']}",
                key=f"btn_{mod['key']}",
                use_container_width=True,
                on_click=go_to_module,
                args=(mod["key"],)
            ):
                pass

    # Row 3: Sugestões (centralizada)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        mod = MODULES[6]
        if st.button(
            f"{mod['icon']}\n\n{mod['title']}",
            key=f"btn_{mod['key']}",
            use_container_width=True,
            on_click=go_to_module,
            args=(mod["key"],)
        ):
            pass


# =============================================================================
# MODULE PAGE
# =============================================================================

def render_module_page(module_info):
    """Renderiza um módulo como página independente."""

    # Override do CSS dos cards para não afetar botões internos do módulo
    st.markdown("""
    <style>
        /* Reset: botões dentro de módulos voltam ao estilo padrão Streamlit */
        .stButton > button {
            background: #f0f2f6 !important;
            border: 1px solid #d2d6dd !important;
            border-radius: 0.5rem !important;
            box-shadow: none !important;
            padding: 0.4rem 1rem !important;
            min-height: 0 !important;
            white-space: normal !important;
            text-align: center !important;
            color: #31333F !important;
            font-size: 0.875rem !important;
            font-weight: 400 !important;
            transform: none !important;
            transition: none !important;
        }
        .stButton > button:hover {
            border-color: #c0392b !important;
            color: #c0392b !important;
            transform: none !important;
            box-shadow: none !important;
        }
        
        /* Botão voltar: estilo especial */
        div[data-testid="stVerticalBlock"] > div:first-child .stButton > button {
            background: transparent !important;
            border: 1.2px solid #ddd !important;
            color: #777 !important;
            font-size: 0.85rem !important;
            padding: 0.35rem 1.2rem !important;
            border-radius: 8px !important;
        }
        div[data-testid="stVerticalBlock"] > div:first-child .stButton > button:hover {
            background: #fafafa !important;
            border-color: #c0392b !important;
            color: #c0392b !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Botão voltar
    st.button("← Voltar ao Menu Principal", key="btn_voltar", on_click=go_to_hub)

    st.markdown("")

    # Renderizar módulo
    module_info["render"]()


# =============================================================================
# FLUXO PRINCIPAL
# =============================================================================

if st.session_state.selected_module is None:
    # HUB
    render_hub()

    st.markdown("<hr style='border:0.5px solid #eee;'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="hub-footer">
        📊 © 2026 Laboratório de Mercado Financeiro | Desenvolvido para fins educacionais<br>
        Prof. José Américo — Coppead - FGV - UCAM
    </div>
    """, unsafe_allow_html=True)

else:
    selected = next(
        (m for m in MODULES if m["key"] == st.session_state.selected_module),
        None
    )
    if selected:
        render_module_page(selected)
    else:
        st.error("Módulo não encontrado.")
        go_to_hub()
        st.rerun()