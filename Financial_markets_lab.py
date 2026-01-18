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

# CABEÇALHO DO FORM
st.markdown("<h2 style='text-align: center;'>Laboratório de Mercado Financeiro</h2>", unsafe_allow_html=True)

st.markdown("<hr style='border:0.5px solid black;'>", unsafe_allow_html=True)

# Define your options (7 módulos)
options = [
    "M1 - Estrutura a Termo de Taxas de Juros",
    "M2 - Modelagem de Risco de Crédito",
    "M3 - Fundos de Investimento em Direitos Creditórios", 
    "M4 - Banking as a Service",
    "M5 - Tokenização de Ativos",
    "M6 - Regulação Bancária",
    "Caixa de Sugestões, Dúvidas...!"
]

# Initialize session state variables if they don't exist
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
    st.session_state.should_scroll = False

# Define button click handlers for each option
def select_option(option):
    st.session_state.selected_option = option

# Define custom CSS for button styling
st.markdown("""
<style>
    /* Default button style (light gray) */
    .stButton > button {
        background-color: #f0f2f6 !important;
        color: #31333F !important;
        border-color: #d2d6dd !important;
        width: 100%;
    }
    
    /* Selected button style (red) */
    .selected-button {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF0000 !important;
        width: 100%;
        padding: 0.5rem;
        font-weight: 400;
        border-radius: 0.25rem;
        cursor: default;
        text-align: center;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# GRID DE BOTÕES (3 colunas x 3 linhas = 9 posições para 7 módulos)
# =============================================================================

# Row 1 (Módulos 1, 2, 3)
col1, col2, col3 = st.columns([3, 3, 3])

with col1:
    if st.session_state.selected_option == options[0]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[0]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[0], key="btn0", use_container_width=True, on_click=select_option, args=(options[0],))

with col2:
    if st.session_state.selected_option == options[1]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[1]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[1], key="btn1", use_container_width=True, on_click=select_option, args=(options[1],))

with col3:
    if st.session_state.selected_option == options[2]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[2]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[2], key="btn2", use_container_width=True, on_click=select_option, args=(options[2],))

# Row 2 (Módulos 4, 5, 6)
col4, col5, col6 = st.columns([3, 3, 3])

with col4:
    if st.session_state.selected_option == options[3]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[3]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[3], key="btn3", use_container_width=True, on_click=select_option, args=(options[3],))

with col5:
    if st.session_state.selected_option == options[4]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[4]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[4], key="btn4", use_container_width=True, on_click=select_option, args=(options[4],))

with col6:
    if st.session_state.selected_option == options[5]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[5]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[5], key="btn5", use_container_width=True, on_click=select_option, args=(options[5],))

# Row 3 (Caixa de Sugestões centralizada)
col7, col8, col9 = st.columns([3, 3, 3])

with col7:
    pass  # Vazio para centralizar

with col8:
    if st.session_state.selected_option == options[6]:
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[6]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.button(options[6], key="btn6", use_container_width=True, on_click=select_option, args=(options[6],))

with col9:
    pass  # Vazio para centralizar

st.markdown("<hr style='border:0.5px solid black;'>", unsafe_allow_html=True)


# =============================================================================
# RENDERIZAÇÃO DOS MÓDULOS
# =============================================================================

if st.session_state.selected_option == "M1 - Estrutura a Termo de Taxas de Juros":
    module_01_ettj.render()

elif st.session_state.selected_option == "M2 - Modelagem de Risco de Crédito":
    module_02_credit_risk.render()
    
elif st.session_state.selected_option == "M3 - Fundos de Investimento em Direitos Creditórios":
    module_03_fidc.render()

elif st.session_state.selected_option == "M4 - Banking as a Service":
    module_04_baas.render()

elif st.session_state.selected_option == "M5 - Tokenização de Ativos":
    module_05_tokenization.render()

elif st.session_state.selected_option == "M6 - Regulação Bancária":
    module_06_financial_regulation.render()

elif st.session_state.selected_option == "Caixa de Sugestões, Dúvidas...!":
    module_07_suggestions.render()

else:
    # Nenhum módulo selecionado - mostrar mensagem de boas-vindas
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <h3>👆 Selecione um módulo acima para começar</h3>
        <p>Clique em um dos botões para acessar o conteúdo interativo.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RODAPÉ
# -----------------------------------------------------------------------------
st.divider()

st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    📊 © 2026 Laboratório de Mercado Financeiro | Desenvolvido para fins educacionais<br>
    Prof. José Américo – Coppead - FGV - UCAM
</div>
""", unsafe_allow_html=True)