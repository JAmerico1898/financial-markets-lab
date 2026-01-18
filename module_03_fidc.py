"""
Módulo 03 - Fundos de Investimento em Direitos Creditórios (FIDC)
Laboratório de Mercado Financeiro
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path


# =============================================================================
# FUNÇÃO RENDER - PONTO DE ENTRADA DO MÓDULO
# =============================================================================

def render():
    """Função principal que renderiza o módulo FIDC Builder 175"""
    
    # CSS customizado
    st.markdown("""
        <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: #1f77b4;
            margin-bottom: 1rem;
        }
        .subtitle {
            font-size: 1.5rem;
            text-align: center;
            color: #555;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #e7f3ff;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #ffc107;
            margin: 1rem 0;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #dc3545;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d4edda;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #28a745;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Título principal
    st.markdown('<div class="main-title">🏦 FIDC Builder 175</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Jornada de Estruturação de Fundos de Investimento em Direitos Creditórios</div>', unsafe_allow_html=True)

    # Sidebar com navegação
    st.sidebar.title("📚 Navegação")
    st.sidebar.markdown("---")

    # Informações sobre o app
    with st.sidebar.expander("ℹ️ Sobre o Aplicativo"):
        st.write("""
        Este aplicativo educacional simula o processo completo de estruturação 
        de um FIDC, incorporando as mudanças da Resolução CVM 175/2022.
        
        **Público-Alvo:**
        - Executivos de finanças
        - Advogados
        - Gestores em formação
        """)

    # Menu de navegação
    pagina = st.sidebar.radio(
        "Escolha o módulo:",
        [
            "🏠 Início",
            "📊 Módulo 1: Viabilidade Econômica",
            "🗂️ Módulo 2: Arquiteto de Classes",
            "🛡️ Módulo 3: Subordinação e Risco",
            "✅ Módulo 4: Checklist Regulatório",
            "✨ Módulo 5: Animação"
        ],
        key="m03_pagina"
    )

    # Página Inicial
    if pagina == "🏠 Início":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## 🎯 Objetivo do Aplicativo")
            st.write("""
            Este simulador interativo foi desenvolvido para ensinar os conceitos fundamentais 
            da estruturação de FIDCs (Fundos de Investimento em Direitos Creditórios), 
            com foco especial nas inovações trazidas pela **Resolução CVM 175/2022**.
            """)
            
            st.markdown("## 📖 O que você vai aprender:")
            
            st.markdown("""
            ### 1️⃣ Viabilidade Econômica
            - Por que FIDCs pequenos são inviáveis economicamente
            - Cálculo do ponto de equilíbrio (breakeven)
            - Estrutura de custos fixos e variáveis
            
            ### 2️⃣ Arquitetura de Classes (Novidade CVM 175)
            - Conceito de segregação patrimonial
            - Diferença entre Classes e Subclasses
            - Estrutura de CNPJ único com múltiplas classes
            
            ### 3️⃣ Subordinação e Proteção de Risco
            - Como a cota subordinada protege a cota sênior
            - Simulação de cenários de inadimplência
            - Conceito de desenquadramento
            
            ### 4️⃣ Rito de Registro na CVM
            - Regras de acesso ao varejo
            - Diferença entre ativos padronizados e não-padronizados
            - Requisitos para registro automático

            ### 5️⃣ Animação - FIDC Monocedente
            - Passo-a-passo do funcionamento

            """)
        
        with col2:
            st.markdown("## 🎓 Contexto Regulatório")
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("""
            **Resolução CVM 175/2022**
            
            Trouxe mudanças significativas:
            
            - ✅ Segregação patrimonial por classes
            - ✅ CNPJ único para o fundo
            - ✅ Maior flexibilidade operacional
            - ✅ Regras mais claras para varejo
            - ✅ Simplificação de processos
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("## 🚀 Como usar")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.write("""
            1. **Navegue** pelos módulos usando o menu lateral
            2. **Interaja** com os controles (sliders, checkboxes)
            3. **Observe** os gráficos e alertas gerados
            4. **Aprenda** com os insights pedagógicos
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("👈 Comece selecionando o **Módulo 1** no menu lateral para iniciar sua jornada!")

    # Importar e executar os módulos
    elif pagina == "📊 Módulo 1: Viabilidade Econômica":
        from modulos import modulo1_viabilidade
        modulo1_viabilidade.run()

    elif pagina == "🗂️ Módulo 2: Arquiteto de Classes":
        from modulos import modulo2_classes
        modulo2_classes.run()

    elif pagina == "🛡️ Módulo 3: Subordinação e Risco":
        from modulos import modulo3_subordinacao
        modulo3_subordinacao.run()

    elif pagina == "✅ Módulo 4: Checklist Regulatório":
        from modulos import modulo4_checklist
        modulo4_checklist.run()
        
    elif pagina == "✨ Módulo 5: Animação":
        st.title("✨ Visualização 3D Interativa - FIDC Varejo")
        st.markdown("### Animação do Fluxo Operacional")
        
        # Ler o arquivo HTML que está dentro da pasta modulos
        html_file = Path("modulos/modulo5_animação.html")
        
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Renderizar o HTML com altura ajustável
            components.html(html_content, height=700, scrolling=False)
                    
            st.markdown("---")
            st.info("💡 **Instruções:** Use os botões 'Anterior' e 'Próximo' na parte inferior para navegar pelos 7 passos do FIDC.")
            
        else:
            st.error(f"❌ Arquivo 'modulo5_animacao.html' não encontrado na pasta modulos.")
            st.write(f"Caminho esperado: {html_file.absolute()}")

# =============================================================================
# EXECUÇÃO STANDALONE (para testes)
# =============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="FIDC Builder 175",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()