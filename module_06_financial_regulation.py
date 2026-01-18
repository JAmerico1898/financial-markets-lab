# module_06_financial_regulation.py
# Explorador Pedagógico dos Acordos de Basileia
# Laboratório de Mercado Financeiro

"""
Módulo 06 - Regulação Financeira (Acordos de Basileia)
Laboratório de Mercado Financeiro
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from datetime import datetime
import streamlit.components.v1 as components

# =============================================================================
# FUNÇÃO RENDER - PONTO DE ENTRADA DO MÓDULO
# =============================================================================

def render():
    """Função principal que renderiza o módulo de Regulação Financeira"""
    
    # Inicialização do session_state para simulação
    if 'ano_atual' not in st.session_state:
        st.session_state.ano_atual = 2025
        st.session_state.capital = 150.0
        st.session_state.ativos = 1000.0
        st.session_state.rwa_percent = 70
        st.session_state.historico = []
    
    # ==================== ESTILOS PERSONALIZADOS ====================
    st.markdown("""
    <style>
        .big-font {font-size: 50px !important; font-weight: bold; text-align: center; color: #1E90FF;}
        .medium-font {font-size: 28px !important; font-weight: bold;}
        .success-box {padding: 15px; border-radius: 10px; background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724;}
        .warning-box {padding: 15px; border-radius: 10px; background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404;}
        .danger-box {padding: 15px; border-radius: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24;}
        .info-box {padding: 15px; border-radius: 10px; background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460;}
    </style>
    """, unsafe_allow_html=True)

    # ==================== SIDEBAR COM NAVEGAÇÃO ====================
    with st.sidebar:
        st.image("https://www.bis.org/img/bislogo_og.jpg", width=200)
        st.title("🏦 Navegação")
        
        modulo = st.radio("Escolha o módulo:",
            ["🏠 Introdução", 
             "1️⃣ Ativos Ponderados por Risco (RWA)", 
             "2️⃣ Simulador de Risco de Crédito", 
             "3️⃣ Alavancagem x Capital Baseado em Risco",
             "4️⃣ Simulação Integrada - Construa seu Banco",
             "5️⃣ Animação - Regulação Prudencial",
             "🧠 Quiz & Recursos"],
            key="m06_modulo"
        )
    
    # ==================== MÓDULO: INTRODUÇÃO ====================
    if modulo == "🏠 Introdução":
        st.markdown('<p class="big-font">Acordos de Basileia</p>', unsafe_allow_html=True)
        st.markdown('<p class="medium-font" style="text-align:center;">Entendendo os Requisitos de Capital Bancário</p>', unsafe_allow_html=True)
    
        col1, col2 = st.columns([1,1])
        with col1:
            st.image("https://www.datocms-assets.com/17507/1606822567-balancopatrimonialestruturaeelementos.png", 
                            caption="Balanço Patrimonial Simplificado", use_container_width=True)    
        with col2:
            st.markdown("""
            ### Por que os bancos precisam de capital?
        
            O capital próprio funciona como um **amortecedor** contra perdas inesperadas.
        
            Em 2008, muitos bancos tinham capital insuficiente para absorver as perdas com hipotecas subprime → **crise financeira global**.
        
            Os **Acordos de Basileia** (I, II, III e IV) foram criados pelo Comitê de Basileia para:
            - Garantir que os bancos tenham capital suficiente
            - Reduzir o risco de falências bancárias
            - Proteger depositantes e a economia
        
            Neste app você vai **aprender fazendo**: construindo portfólios, simulando crises e gerenciando bancos virtuais.
            """)
    
        st.divider()
        st.success("Navegue pelos módulos no menu lateral para começar sua jornada!")

    # ==================== MÓDULO 1: RWA PLAYGROUND ====================
    elif modulo == "1️⃣ Ativos Ponderados por Risco (RWA)":
        st.header("Módulo 1: Ativos Ponderados por Risco (RWA)")
        st.markdown("### Aprenda como a composição do portfólio afeta o capital exigido")
    
        with st.expander("🎯 Objetivos de aprendizagem"):
            st.write("- Entender pesos de risco de crédito por classe de ativo\n- Ver como o RWA impacta o capital mínimo exigido (10,5%)\n- Comparar estratégias conservadoras vs. agressivas")
    
        col1, col2 = st.columns([1, 1])
    
        with col1:
            st.subheader("Monte seu Banco")
            st.latex("(Ativos, $100 milhões; Capital, $12 milhões)")
            st.latex("")
        
            cash = st.slider("Caixa e títulos públicos (0%)", 0, 100, 20, key="m06_cash")
            gov_bonds = st.slider("Títulos soberanos AAA (0-20%)", 0, 100-cash, 15, key="m06_gov_bonds")
            mortgages = st.slider("Hipotecas residenciais (35-75%)", 0, 100-cash-gov_bonds, 30, key="m06_mortgages")
            corp_loans = st.slider("Empréstimos corporativos investment grade (100%)", 0, 100-cash-gov_bonds-mortgages, 20, key="m06_corp_loans")
            high_yield = st.slider("High-yield / Subinvestment (100-150%)", 0, 100-cash-gov_bonds-mortgages-corp_loans, 10, key="m06_high_yield")
            unrated = st.slider("Não classificados (150%)", 0, 100-cash-gov_bonds-mortgages-corp_loans-high_yield, 5, key="m06_unrated")
        
            total_assets = cash + gov_bonds + mortgages + corp_loans + high_yield + unrated
            if total_assets != 100:
                st.warning(f"Total: ${total_assets}M (ajuste para $100M)")
                total_assets = 100
        
            # Pesos médios simplificados (Basel III padronizado)
            rwa = (cash * 0 + gov_bonds * 0.1 + mortgages * 0.5 + corp_loans * 1.0 + high_yield * 1.2 + unrated * 1.5) * 1e6
            required_capital = rwa * 0.105
            car = (10.5e6 / rwa) * 100 if rwa > 0 else 100  # Supondo capital inicial de $10,5M
        
            df = pd.DataFrame({
                "Classe de Ativo": ["Caixa", "Títulos Públicos", "Hipotecas", "Corp. IG", "High-Yield", "Não Classificado"],
                "Alocação ($M)": [cash, gov_bonds, mortgages, corp_loans, high_yield, unrated],
                "Peso de Risco": [0, 0.1, 0.5, 1.0, 1.2, 1.5],
                "RWA Contribuição ($M)": [0, gov_bonds*0.1, mortgages*0.5, corp_loans*1.0, high_yield*1.2, unrated*1.5]
            })
        
            st.dataframe(df, use_container_width=True)

            st.metric("Ativos Totais", f"${total_assets}M")
            st.metric("RWA Total", f"${rwa/1e6:.1f}M")
            st.metric("Capital Mínimo Exigido (10,5%)", f"${required_capital/1e6:.2f}M")
    
        with col2:
            st.subheader("Dashboard em Tempo Real")
        
            fig_pie = px.pie(df, values="Alocação ($M)", names="Classe de Ativo", title="Composição do Portfólio")
            st.plotly_chart(fig_pie, use_container_width=True)
        
            fig_bar = px.bar(df, x="Classe de Ativo", y="RWA Contribuição ($M)", title="Contribuição para RWA")
            st.plotly_chart(fig_bar, use_container_width=True)
        
            st.metric("Patrimônio Regulatório", f"${10.5:.1f}M")
            st.metric("Índice de Basileia (CAR, Patrimônio Regulatório/RWA)", f"{car:.2f}%")
            st.metric("Buffer de Capital (Índice de Basileia - Mínimo Exigido (10,5%))", f"{(car-10.5):.2f}%")

        col3, col4, col5 = st.columns([1,4,1])
        with col4:
          fig_gauge = go.Figure(go.Indicator(
          mode = "gauge+number+delta",
          value = car,
          domain = {'x': [0, 1], 'y': [0, 1]},
          title = {'text': "Índice de Basileia (CAR, Capital Adequacy Ratio) (em %)"},
          delta = {'reference': 10.5},
          gauge = {
              'axis': {'range': [None, 25]},
              'bar': {'color': "darkblue"},
              'steps': [
                  {'range': [0, 8], 'color': "red"},
                  {'range': [8, 10.5], 'color': "orange"},
                  {'range': [10.5, 25], 'color': "green"}
              ],
              'threshold': {
                  'line': {'color': "red", 'width': 4},
                  'thickness': 0.75,
                  'value': 8}}))
          st.plotly_chart(fig_gauge)

          if car >= 10.5:
              st.success("✅ Banco bem capitalizado!")
          elif car >= 8:
              st.warning("⚠️ Acima do mínimo, mas abaixo do buffer recomendado")
          else:
              st.error("❌ Ratio abaixo do mínimo regulatório!")

    # ==================== MÓDULO 2: SIMULADOR DE RISCO DE CRÉDITO ====================
    elif modulo == "2️⃣ Simulador de Risco de Crédito":
        st.header("Módulo 2: Provisões e Ciclo de Crédito")
        st.markdown("**Objetivo**: ver na prática por que a Res 4966 reduz a prociclicidade e cria colchão antes da crise")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Configuração Inicial")
            carteira = st.number_input("Carteira de empréstimos ($M)", 100, 2000, 500, key="m06_carteira")
            taxa_juros = st.slider("Taxa média de juros anual (%)", 10.0, 25.0, 15.0, key="m06_taxa_juros")
            cenario = st.selectbox("Cenário econômico", ["Boom", "Normal", "Recessão"], key="m06_cenario")
            modelo = st.radio("Modelo de provisionamento", ["Res 2682 (perda incorrida)", "Res 4966 (perda esperada)"], key="m06_modelo")

        # Taxas de inadimplência (PD) por cenário
        if cenario == "Boom":
            pd_rates = [0.5, 0.4, 0.3, 0.4, 0.5]
        elif cenario == "Normal":
            pd_rates = [1.0, 1.2, 1.5, 1.8, 1.6]
        else:  # Recessão
            pd_rates = [2.0, 3.5, 6.0, 12.0, 8.0]  # pico de 12 %

        anos = [2025, 2026, 2027, 2028, 2029]
        lgd = 0.5
        realized_loss = [carteira * (pd / 100) * lgd for pd in pd_rates]
        total_realized = sum(realized_loss)

        # Provisão base (12-month ECL ≈ 1 % da carteira para Res 4966 mesmo em bons tempos)
        base_ifrs9 = carteira * 0.01  # 1 % ao ano (ajuste se quiser mais/menos dramático)

        if cenario == "Recessão":
            front_proportions = [0.35, 0.30, 0.20, 0.10, 0.05]  # Res 4966 antecipa forte
            back_proportions = [0.00, 0.05, 0.15, 0.35, 0.45]   # Res 2682 “cliff” no final

            if modelo == "Res 4966 (perda esperada)":
                provisao = [round(base_ifrs9 + total_realized * p, 1) for p in front_proportions]
            else:
                provisao = [round(0 + total_realized * p, 1) for p in back_proportions]
        else:
            # Em Boom/Normal o Res 4966 sempre provisiona mais (conservadorismo)
            if modelo == "Res 4966 (perda esperada)":
                provisao = [round(base_ifrs9, 1) for _ in anos]
            else:
                provisao = [0.0 for _ in anos]  # Res 2682 quase nada em bons tempos

        juros_anual = carteira * (taxa_juros / 100)
        juros = [round(juros_anual, 1) for _ in anos]

        lucro = [round(j - p, 1) for j, p in zip(juros, provisao)]

        df_sim = pd.DataFrame({
            "Ano": anos,
            "Juros ($M)": juros,
            "Provisões ($M)": provisao,
            "Lucro Líquido ($M)": lucro
        })
    
        st.subheader("Simulação 5 anos")
        st.dataframe(df_sim, use_container_width=True)
    
        fig = go.Figure()
        fig.add_trace(go.Bar(x=anos, y=juros, name="Receita de Juros", marker_color="#00cc96"))
        fig.add_trace(go.Bar(x=anos, y=[-p for p in provisao], name="Provisões", marker_color="#ff4444"))
        fig.update_layout(barmode="relative", title="Receita de Juros × Provisões", yaxis_title="$ milhões")
        st.plotly_chart(fig, use_container_width=True)
    
        st.metric("Provisões Cumulativas", f"${sum(provisao):.1f}M")
        st.metric("Lucro Acumulado", f"${sum(lucro):.1f}M")
    
        if cenario != "Recessão":
            if modelo == "Res 4966 (perda esperada)":
                st.info("💡 Em tempos bons a Res 4966 já provisiona mais que a Res 2682 → constrói colchão antecipado")
            else:
                st.info("📌 Res 2682 praticamente não provisiona em bons tempos (só quando a perda já ocorreu)")
        else:
            if modelo == "Res 4966 (perda esperada)":
                st.success("✅ Res 4966 antecipa a perda esperada → cria colchão antes da recessão e estabiliza lucro")
            else:
                st.warning("⚠️ Res 2682: “cliff effect” → lucro inflado no início, depois colapso (crise 2008)")

    # ==================== MÓDULO 3: ALAVANCAGEM ====================
    elif modulo == "3️⃣ Alavancagem x Capital Baseado em Risco":
        st.header("Módulo 3: As Duas Restrições Simultâneas")
        st.markdown("Todo banco enfrenta **dois limites**: Capital baseado em risco (CAR, ou Índice de Basileia) e Índice de Alavancagem (contábil)")
    
        capital = st.number_input("Capital próprio ($M)", 50, 300, 100, key="m06_capital")
        ativos_totais = st.slider("Ativos totais ($M)", 500, 5000, 1500, key="m06_ativos_totais")
        rwa_percent = st.slider("RWA médio (%) dos ativos", 40, 100, 70, key="m06_rwa_percent")
        rwa = ativos_totais * (rwa_percent / 100)
        car = (capital / rwa) * 100 if rwa > 0 else 0
        leverage = (capital / (ativos_totais)) * 100

        col1, col2, col3 = st.columns([3, 3, 3])
        with col1:
          st.metric("Ativos Ponderados pelo Risco (RWA)", f"${rwa:.0f}M")
        with col2:
          st.metric("Índice de Basileia", f"${car:.2f}%")
        with col3:
          st.metric("Índice de Alavancagem", f"${leverage:.2f}%")
   
        col4, col5 = st.columns(2)
        with col4:
            fig1 = go.Figure(go.Indicator(mode="gauge+number", value=car, title={'text': "CAR, Índice de Basileia (%)"}, 
                                         gauge={'axis': {'range': [0, 25]}, 'threshold': {'value': 10.5}}))
            st.plotly_chart(fig1)
        with col5:
            fig2 = go.Figure(go.Indicator(mode="gauge+number", value=leverage, title={'text': "Índice de Alavancagem (%)"}, 
                                         gauge={'axis': {'range': [0, 15]}, 'threshold': {'value': 3}}))
            st.plotly_chart(fig2)
    
        if car < 10.5 and leverage >= 3:
            st.error("Banco em situação crítica - viola ambas as regras!")
        elif leverage < 3 and car < 10.5:
            st.error("Restrição ativa: Requerimento Mínimo de Capital não satisfeito")
        elif car >= 10.5 and leverage >= 3:
            st.error("Restrição ativa: Índice de Alavancagem (ex: bancos com ativos em excesso, mas de baixo risco)")
        else:
            st.success("Banco cumpre ambas as exigências!")

    # ==================== MÓDULO 4: SIMULAÇÃO INTEGRADA ====================
    elif modulo == "4️⃣ Simulação Integrada - Construa seu Banco":
        st.header("Módulo 4: Construa seu Banco!")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader(f"Ano {st.session_state.ano_atual}")
            crescimento = st.slider("Crescimento anual dos ativos (%)", -20, 60, 12, 1, key="m06_crescimento")
            roa = st.slider("ROA esperado (retorno sobre ativos %)", 0.0, 8.0, 4.0, 0.1, key="m06_roa") / 100
            provisao_stress = st.checkbox("Evento de stress/recessão neste ano?", key="m06_provisao_stress")

        # Cálculos do ano - usar valores ATUAIS antes de incrementar
        ano_calculado = st.session_state.ano_atual
        capital_inicial = st.session_state.capital
        ativos_iniciais = st.session_state.ativos

        novo_ativo = round(ativos_iniciais * (1 + crescimento / 100), 1)
        lucro_bruto = round(novo_ativo * roa, 1)
        payout = 0.5  # 50% do lucro é distribuído como dividendo

        if provisao_stress:
            provisao = round(novo_ativo * 0.04, 1)  # stress forte
        else:
            provisao = round(novo_ativo * 0.008, 1)  # normal

        dividendos = round((lucro_bruto - provisao) * payout, 1)
                      
        delta_capital = lucro_bruto - provisao - dividendos
        capital_final = round(capital_inicial + delta_capital, 1)

        rwa_ratio = st.session_state.rwa_percent / 100
        car = round(capital_final / (novo_ativo * rwa_ratio) * 100, 1)
        leverage = round(capital_final / novo_ativo * 100, 1)

        # Dashboard do ano corrente
        colm1, colm2, colm3 = st.columns(3)
        colm1.metric("Capital", f"${capital_final:.0f}M", f"{delta_capital:+.0f}M")
        colm2.metric("Ativos Totais", f"${novo_ativo:.0f}M")
        colm3.metric("RWA / Ativos", f"{st.session_state.rwa_percent}%")

        colm1, colm2, colm3 = st.columns(3)
        colm1.metric("CAR (Capital Adequacy Ratio)", f"{car}%", 
                    "🟢 OK" if car >= 10.5 else "🔴 Abaixo do requerido")
        colm2.metric("Leverage Ratio", f"{leverage}%", 
                    "🟢 OK" if leverage >= 3 else "🔴 Abaixo do requerido")
        colm3.metric("ROA realizado", f"{roa*100:.1f}%")

        st.metric("Dividendos pagos", f"50% do lucro → ${dividendos}M")

        # Botão de avanço - AGORA sim atualiza o session_state
        if st.button("➡️ Avançar para o próximo ano", type="primary", key="m06_btn_avancar"):
            st.session_state.historico.append({
                "Ano": ano_calculado,
                "Capital": capital_final,
                "Ativos": novo_ativo,
                "CAR": car,
                "Leverage": leverage,
                "RWA %": st.session_state.rwa_percent
            })
        
            # Atualiza o estado APENAS quando o botão é clicado
            st.session_state.capital = capital_final
            st.session_state.ativos = novo_ativo
            st.session_state.ano_atual += 1

            if st.session_state.ano_atual > 2027:
                st.success("🎉 Simulação de 3 anos concluída!")
                st.balloons()
                if car >= 10.5 and leverage >= 3:
                    st.success("🏦 Seu banco sobreviveu e está bem capitalizado!")
                else:
                    st.error("💥 Seu banco violou requisitos regulatórios – intervenção regulatória")
            st.rerun()
            
        # Gráfico histórico
        if st.session_state.historico:
            df_hist = pd.DataFrame(st.session_state.historico)
            fig = px.line(df_hist, x="Ano", y="CAR", markers=True, title="Evolução do CAR")
            fig.add_hline(y=10.5, line_dash="dash", line_color="orange", annotation_text="Mínimo 10.5%")
            fig.add_hline(y=8.0, line_dash="dash", line_color="red", annotation_text="Mínimo regulatório")
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Botão de reinício (sempre visível no final da página)
        if st.button("🔄 Reiniciar Simulação Completa", type="secondary", key="m06_btn_reiniciar"):
            keys_to_del = ['ano_atual', 'capital', 'ativos', 'rwa_percent', 'historico']
            for k in keys_to_del:
                st.session_state.pop(k, None)
            st.success("Simulação reiniciada!")
            st.rerun()

    # ==================== CÓDIGO ATUALIZADO PARA INTEGRAÇÃO DA ANIMAÇÃO ====================

    elif modulo == "5️⃣ Animação - Regulação Prudencial":
        st.header("🎬 Módulo 5: Animação Interativa - Regulação Prudencial")
    
        st.markdown("""
        Esta animação interativa apresenta uma jornada completa pelos **Acordos de Basileia**, 
        desde a crise de 2008 até as regulamentações mais recentes.
    
        **Controles:**
        - Use os botões **← Anterior** e **Próximo →** para navegar
        - Clique em **▶ Reproduzir** para modo automático
        - Clique nos pontos na parte inferior para ir direto a um módulo
        """)
    
        st.markdown("---")
    
        # HTML que carrega React e renderiza o componente JSX
        react_animation_html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Acordos de Basileia - Animação React</title>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'DM Sans', sans-serif; }
            #root { min-height: 700px; }
        </style>
    </head>
    <body>
        <div id="root"></div>
    
        <script type="text/babel">
            // Professional Basel Accords Financial Regulation Animation
            // Designed for integration with Streamlit pedagogical application
            // Author: Prof. José Américo - Coppead/UFRJ

            const BaselAccordsAnimation = () => {
              const [currentStage, setCurrentStage] = React.useState(0);
              const [isPlaying, setIsPlaying] = React.useState(false);
              const [bankMetrics, setBankMetrics] = React.useState({
                capital: 150,
                assets: 1000,
                rwa: 600,
                provisions: 20,
                car: 25,
                leverage: 15
              });
              const [animationPhase, setAnimationPhase] = React.useState('idle');
              const [particlePositions, setParticlePositions] = React.useState([]);
          
              const stages = [
                {
                  id: 'intro',
                  title: 'Regulação Prudencial Bancária',
                  subtitle: 'Os Acordos de Basileia',
                  description: 'Uma jornada pelos pilares que sustentam a estabilidade financeira global. Os Acordos de Basileia representam o padrão internacional para regulação bancária, estabelecendo requisitos de capital que protegem depositantes e a estabilidade financeira.',
                  icon: '🏛️'
                },
                {
                  id: 'crisis',
                  title: 'A Crise de 2008',
                  subtitle: 'Por que precisamos de regulação?',
                  description: 'Bancos operavam com índices de capital menores que 4%. Hipotecas subprime e produtos estruturados sem buffers adequados levaram ao colapso sistêmico. A crise demonstrou a necessidade de regulação prudencial mais rigorosa.',
                  icon: '📉'
                },
                {
                  id: 'basel1',
                  title: 'Basileia I (1988)',
                  subtitle: 'O Nascimento da Regulação de Capital',
                  description: 'Introduziu o conceito revolucionário de capital mínimo de 8% sobre ativos ponderados pelo risco. Pela primeira vez, bancos internacionais seguiriam padrões uniformes de capitalização.',
                  icon: '📜'
                },
                {
                  id: 'rwa',
                  title: 'Ativos Ponderados pelo Risco',
                  subtitle: 'RWA - Risk-Weighted Assets',
                  description: 'Diferentes classes de ativos carregam diferentes pesos de risco. Caixa = 0%, Títulos Soberanos = 0-20%, Hipotecas = 35-75%, Corporativo = 100%. Este conceito é o coração da regulação bancária.',
                  icon: '⚖️'
                },
                {
                  id: 'basel2',
                  title: 'Basileia II (2004)',
                  subtitle: 'Os Três Pilares',
                  description: 'Pilar 1: Requerimentos Mínimos de Capital | Pilar 2: Revisão Supervisória | Pilar 3: Disciplina de Mercado. Uma estrutura mais sofisticada que reconhece a complexidade do risco bancário moderno.',
                  icon: '🏗️'
                },
                {
                  id: 'basel3',
                  title: 'Basileia III (2010)',
                  subtitle: 'Resposta à Crise Financeira',
                  description: 'Exigência de capital aumenta para mínimo de 10,5% total. Introdução do Índice de Alavancagem de 3%. Requisitos mais rigorosos para garantir a resiliência do sistema bancário.',
                  icon: '🛡️'
                },
                {
                  id: 'car',
                  title: 'Índice de Adequação de Capital',
                  subtitle: 'CAR - Capital Adequacy Ratio',
                  description: 'CAR = Capital Total / RWA × 100%. Mínimo regulatório: 10,5%. Bancos bem capitalizados superam 15%.',
                  icon: '📊'
                },
                {
                  id: 'leverage',
                  title: 'Índice de Alavancagem',
                  subtitle: 'Restrição Dupla',
                  description: 'Leverage Ratio = Tier 1 Capital / Ativos Totais × 100%. Mínimo: 3%. Complementa o CAR para evitar arbitragem regulatória e acúmulo excessivo de ativos de baixo risco.',
                  icon: '🔒'
                },
                {
                  id: 'ifrs9',
                  title: 'IFRS 9 vs IAS 39',
                  subtitle: 'Provisão para Perdas Esperadas',
                  description: 'IAS 39: Perda Incorrida (reativo) - reconhece perdas apenas quando ocorrem. IFRS 9: Perda Esperada (prospectivo) - provisiona antecipadamente. Modelo de 3 estágios reduz a prociclicalidade.',
                  icon: '📈'
                },
                {
                  id: 'basel4',
                  title: 'Basileia IV (2023)',
                  subtitle: 'Refinamentos Finais',
                  description: 'Revisão dos pesos de risco padronizados, piso de output de 72,5% para modelos internos, e tratamento revisado de risco operacional. O framework continua evoluindo.',
                  icon: '🔧'
                },
                {
                  id: 'simulation',
                  title: 'Simulação Integrada',
                  subtitle: 'Gestão Estratégica de Capital',
                  description: 'Equilibre crescimento, rentabilidade e conformidade regulatória. Um CFO bancário enfrenta decisões complexas: expandir ativos, reter lucros, pagar dividendos - tudo mantendo os índices adequados.',
                  icon: '🎮'
                },
                {
                  id: 'conclusion',
                  title: 'Estabilidade Financeira',
                  subtitle: 'O Objetivo Final',
                  description: 'Regulação prudencial protege depositantes, previne crises sistêmicas e garante a resiliência do sistema financeiro global. Os Acordos de Basileia são fundamentais para um sistema bancário saudável.',
                  icon: '🌍'
                }
              ];

              // Animation particles for visual effect
              React.useEffect(() => {
                const particles = Array.from({ length: 20 }, (_, i) => ({
                  id: i,
                  x: Math.random() * 100,
                  y: Math.random() * 100,
                  size: Math.random() * 4 + 2,
                  speed: Math.random() * 0.5 + 0.2,
                  opacity: Math.random() * 0.3 + 0.1
                }));
                setParticlePositions(particles);
              }, []);

              // Auto-play functionality
              React.useEffect(() => {
                let interval;
                if (isPlaying && currentStage < stages.length - 1) {
                  interval = setInterval(() => {
                    setCurrentStage(prev => {
                      if (prev < stages.length - 1) return prev + 1;
                      setIsPlaying(false);
                      return prev;
                    });
                  }, 5000);
                }
                return () => clearInterval(interval);
              }, [isPlaying, currentStage]);

              // Update bank metrics based on stage
              React.useEffect(() => {
                const metricsMap = {
                  0: { capital: 150, assets: 1000, rwa: 600, provisions: 20, car: 25, leverage: 15 },
                  1: { capital: 30, assets: 1000, rwa: 800, provisions: 5, car: 3.75, leverage: 3 },
                  2: { capital: 80, assets: 1000, rwa: 600, provisions: 15, car: 13.3, leverage: 8 },
                  3: { capital: 100, assets: 1000, rwa: 500, provisions: 18, car: 20, leverage: 10 },
                  4: { capital: 100, assets: 1000, rwa: 550, provisions: 20, car: 18.2, leverage: 10 },
                  5: { capital: 120, assets: 1000, rwa: 600, provisions: 25, car: 20, leverage: 12 },
                  6: { capital: 105, assets: 1000, rwa: 600, provisions: 22, car: 17.5, leverage: 10.5 },
                  7: { capital: 105, assets: 1000, rwa: 400, provisions: 22, car: 26.25, leverage: 10.5 },
                  8: { capital: 110, assets: 1000, rwa: 580, provisions: 35, car: 19, leverage: 11 },
                  9: { capital: 115, assets: 1000, rwa: 620, provisions: 30, car: 18.5, leverage: 11.5 },
                  10: { capital: 125, assets: 1200, rwa: 700, provisions: 28, car: 17.9, leverage: 10.4 },
                  11: { capital: 150, assets: 1000, rwa: 600, provisions: 25, car: 25, leverage: 15 }
                };
                setBankMetrics(metricsMap[currentStage] || metricsMap[0]);
                setAnimationPhase('entering');
                setTimeout(() => setAnimationPhase('active'), 100);
              }, [currentStage]);

              const getStatusColor = (value, min, target) => {
                if (value >= target) return '#10B981';
                if (value >= min) return '#F59E0B';
                return '#EF4444';
              };

              const renderGauge = (value, min, target, label, unit = '%') => {
                const percentage = Math.min((value / (target * 1.5)) * 100, 100);
                const statusColor = getStatusColor(value, min, target);
            
                return (
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '8px'
                  }}>
                    <div style={{
                      position: 'relative',
                      width: '100px',
                      height: '100px'
                    }}>
                      <svg viewBox="0 0 100 100" style={{ transform: 'rotate(-90deg)' }}>
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          fill="none"
                          stroke="rgba(255,255,255,0.1)"
                          strokeWidth="8"
                        />
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          fill="none"
                          stroke={statusColor}
                          strokeWidth="8"
                          strokeDasharray={`${percentage * 2.51} 251`}
                          style={{
                            transition: 'stroke-dasharray 1s ease-out, stroke 0.5s ease'
                          }}
                        />
                      </svg>
                      <div style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        textAlign: 'center'
                      }}>
                        <div style={{
                          fontSize: '18px',
                          fontWeight: '700',
                          color: statusColor,
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          {value.toFixed(1)}{unit}
                        </div>
                      </div>
                    </div>
                    <div style={{
                      fontSize: '11px',
                      color: 'rgba(255,255,255,0.7)',
                      textTransform: 'uppercase',
                      letterSpacing: '1px',
                      fontFamily: "'DM Sans', sans-serif"
                    }}>
                      {label}
                    </div>
                    <div style={{
                      fontSize: '9px',
                      color: 'rgba(255,255,255,0.4)',
                      fontFamily: "'DM Sans', sans-serif"
                    }}>
                      Min: {min}%
                    </div>
                  </div>
                );
              };

              const renderAssetBar = (label, value, maxValue, color, riskWeight) => {
                const width = (value / maxValue) * 100;
                return (
                  <div style={{ marginBottom: '12px' }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      marginBottom: '4px',
                      fontSize: '11px',
                      color: 'rgba(255,255,255,0.8)',
                      fontFamily: "'DM Sans', sans-serif"
                    }}>
                      <span>{label}</span>
                      <span style={{ color: 'rgba(255,255,255,0.5)' }}>
                        Peso: {riskWeight}% | R$ {value}M
                      </span>
                    </div>
                    <div style={{
                      height: '8px',
                      background: 'rgba(255,255,255,0.1)',
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        height: '100%',
                        width: `${width}%`,
                        background: `linear-gradient(90deg, ${color}, ${color}88)`,
                        borderRadius: '4px',
                        transition: 'width 0.8s ease-out'
                      }} />
                    </div>
                  </div>
                );
              };

              const renderRWAVisualization = () => {
                const assets = [
                  { label: 'Caixa', value: 100, riskWeight: 0, color: '#10B981' },
                  { label: 'Títulos Soberanos', value: 200, riskWeight: 20, color: '#3B82F6' },
                  { label: 'Hipotecas', value: 250, riskWeight: 50, color: '#8B5CF6' },
                  { label: 'Corporativo', value: 300, riskWeight: 100, color: '#F59E0B' },
                  { label: 'Alto Risco', value: 100, riskWeight: 150, color: '#EF4444' },
                  { label: 'Sem Rating', value: 50, riskWeight: 150, color: '#DC2626' }
                ];

                return (
                  <div style={{
                    background: 'rgba(0,0,0,0.3)',
                    borderRadius: '16px',
                    padding: '20px',
                    marginTop: '20px'
                  }}>
                    <h4 style={{
                      margin: '0 0 16px 0',
                      fontSize: '14px',
                      color: 'rgba(255,255,255,0.9)',
                      fontFamily: "'DM Sans', sans-serif",
                      fontWeight: '600'
                    }}>
                      Composição de Ativos e Pesos de Risco
                    </h4>
                    {assets.map((asset, i) => (
                      <div key={i} style={{
                        animation: `fadeSlideIn 0.5s ease-out ${i * 0.1}s both`
                      }}>
                        {renderAssetBar(asset.label, asset.value, 400, asset.color, asset.riskWeight)}
                      </div>
                    ))}
                  </div>
                );
              };

              const renderIFRS9Comparison = () => {
                const scenarios = [
                  { period: 'Expansão', ias39: 10, ifrs9: 25 },
                  { period: 'Normal', ias39: 15, ifrs9: 30 },
                  { period: 'Recessão', ias39: 80, ifrs9: 45 }
                ];

                return (
                  <div style={{
                    background: 'rgba(0,0,0,0.3)',
                    borderRadius: '16px',
                    padding: '20px',
                    marginTop: '20px'
                  }}>
                    <h4 style={{
                      margin: '0 0 16px 0',
                      fontSize: '14px',
                      color: 'rgba(255,255,255,0.9)',
                      fontFamily: "'DM Sans', sans-serif",
                      fontWeight: '600'
                    }}>
                      Comparação de Provisões (R$ milhões)
                    </h4>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-around',
                      alignItems: 'flex-end',
                      height: '120px',
                      borderBottom: '1px solid rgba(255,255,255,0.2)',
                      paddingBottom: '8px'
                    }}>
                      {scenarios.map((s, i) => (
                        <div key={i} style={{
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center',
                          gap: '4px'
                        }}>
                          <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end' }}>
                            <div style={{
                              width: '24px',
                              height: `${s.ias39}px`,
                              background: 'linear-gradient(180deg, #F59E0B, #D97706)',
                              borderRadius: '4px 4px 0 0',
                              transition: 'height 0.8s ease-out'
                            }} />
                            <div style={{
                              width: '24px',
                              height: `${s.ifrs9}px`,
                              background: 'linear-gradient(180deg, #10B981, #059669)',
                              borderRadius: '4px 4px 0 0',
                              transition: 'height 0.8s ease-out'
                            }} />
                          </div>
                          <span style={{
                            fontSize: '10px',
                            color: 'rgba(255,255,255,0.7)',
                            marginTop: '8px',
                            fontFamily: "'DM Sans', sans-serif"
                          }}>
                            {s.period}
                          </span>
                        </div>
                      ))}
                    </div>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'center',
                      gap: '24px',
                      marginTop: '12px'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <div style={{ width: '12px', height: '12px', background: '#F59E0B', borderRadius: '2px' }} />
                        <span style={{ fontSize: '10px', color: 'rgba(255,255,255,0.7)', fontFamily: "'DM Sans', sans-serif" }}>IAS 39</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <div style={{ width: '12px', height: '12px', background: '#10B981', borderRadius: '2px' }} />
                        <span style={{ fontSize: '10px', color: 'rgba(255,255,255,0.7)', fontFamily: "'DM Sans', sans-serif" }}>IFRS 9</span>
                      </div>
                    </div>
                  </div>
                );
              };

              const renderThreePillars = () => {
                const pillars = [
                  { number: 1, title: 'Capital Mínimo', desc: 'Requerimentos quantitativos', color: '#3B82F6' },
                  { number: 2, title: 'Revisão Supervisória', desc: 'Avaliação qualitativa', color: '#8B5CF6' },
                  { number: 3, title: 'Disciplina de Mercado', desc: 'Transparência e divulgação', color: '#10B981' }
                ];

                return (
                  <div style={{
                    display: 'flex',
                    gap: '16px',
                    marginTop: '20px',
                    justifyContent: 'center'
                  }}>
                    {pillars.map((p, i) => (
                      <div key={i} style={{
                        flex: 1,
                        maxWidth: '140px',
                        background: `linear-gradient(180deg, ${p.color}22, ${p.color}11)`,
                        border: `1px solid ${p.color}44`,
                        borderRadius: '12px',
                        padding: '16px',
                        textAlign: 'center'
                      }}>
                        <div style={{
                          width: '40px',
                          height: '40px',
                          background: p.color,
                          borderRadius: '50%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          margin: '0 auto 12px',
                          fontSize: '18px',
                          fontWeight: '700',
                          color: 'white',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          {p.number}
                        </div>
                        <div style={{
                          fontSize: '13px',
                          fontWeight: '600',
                          color: 'white',
                          marginBottom: '4px',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          {p.title}
                        </div>
                        <div style={{
                          fontSize: '10px',
                          color: 'rgba(255,255,255,0.6)',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          {p.desc}
                        </div>
                      </div>
                    ))}
                  </div>
                );
              };

              const renderDualConstraint = () => {
                return (
                  <div style={{
                    background: 'rgba(0,0,0,0.3)',
                    borderRadius: '16px',
                    padding: '20px',
                    marginTop: '20px'
                  }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-around',
                      gap: '20px'
                    }}>
                      <div style={{
                        flex: 1,
                        textAlign: 'center',
                        padding: '16px',
                        background: 'rgba(59,130,246,0.15)',
                        borderRadius: '12px',
                        border: '1px solid rgba(59,130,246,0.3)'
                      }}>
                        <div style={{ fontSize: '24px', marginBottom: '8px' }}>📊</div>
                        <div style={{
                          fontSize: '13px',
                          fontWeight: '600',
                          color: '#3B82F6',
                          marginBottom: '4px',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          CAR (Ponderado)
                        </div>
                        <div style={{
                          fontSize: '11px',
                          color: 'rgba(255,255,255,0.7)',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          Capital / RWA
                        </div>
                        <div style={{
                          fontSize: '18px',
                          fontWeight: '700',
                          color: '#3B82F6',
                          marginTop: '8px',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          ≥ 10,5%
                        </div>
                      </div>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        fontSize: '24px',
                        color: 'rgba(255,255,255,0.5)'
                      }}>
                        +
                      </div>
                      <div style={{
                        flex: 1,
                        textAlign: 'center',
                        padding: '16px',
                        background: 'rgba(139,92,246,0.15)',
                        borderRadius: '12px',
                        border: '1px solid rgba(139,92,246,0.3)'
                      }}>
                        <div style={{ fontSize: '24px', marginBottom: '8px' }}>🔒</div>
                        <div style={{
                          fontSize: '13px',
                          fontWeight: '600',
                          color: '#8B5CF6',
                          marginBottom: '4px',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          Alavancagem
                        </div>
                        <div style={{
                          fontSize: '11px',
                          color: 'rgba(255,255,255,0.7)',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          Tier 1 / Ativos
                        </div>
                        <div style={{
                          fontSize: '18px',
                          fontWeight: '700',
                          color: '#8B5CF6',
                          marginTop: '8px',
                          fontFamily: "'DM Sans', sans-serif"
                        }}>
                          ≥ 3%
                        </div>
                      </div>
                    </div>
                  </div>
                );
              };

              const renderTimeline = () => {
                const events = [
                  { year: '1988', label: 'Basileia I', color: '#3B82F6' },
                  { year: '2004', label: 'Basileia II', color: '#8B5CF6' },
                  { year: '2008', label: 'Crise', color: '#EF4444' },
                  { year: '2010', label: 'Basileia III', color: '#10B981' },
                  { year: '2018', label: 'IFRS 9', color: '#F59E0B' },
                  { year: '2023', label: 'Basileia IV', color: '#06B6D4' }
                ];

                return (
                  <div style={{
                    position: 'relative',
                    padding: '20px 0',
                    marginTop: '20px'
                  }}>
                    <div style={{
                      position: 'absolute',
                      top: '50%',
                      left: '5%',
                      right: '5%',
                      height: '2px',
                      background: 'rgba(255,255,255,0.2)'
                    }} />
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      position: 'relative',
                      padding: '0 5%'
                    }}>
                      {events.map((e, i) => (
                        <div key={i} style={{
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center'
                        }}>
                          <div style={{
                            width: '14px',
                            height: '14px',
                            background: e.color,
                            borderRadius: '50%',
                            border: '3px solid #0f172a',
                            marginBottom: '8px',
                            boxShadow: `0 0 12px ${e.color}66`
                          }} />
                          <span style={{
                            fontSize: '11px',
                            fontWeight: '600',
                            color: e.color,
                            fontFamily: "'DM Sans', sans-serif"
                          }}>
                            {e.year}
                          </span>
                          <span style={{
                            fontSize: '9px',
                            color: 'rgba(255,255,255,0.6)',
                            fontFamily: "'DM Sans', sans-serif",
                            marginTop: '2px'
                          }}>
                            {e.label}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              };

              const renderStageContent = () => {
                const stage = stages[currentStage];
            
                let additionalContent = null;
            
                switch(stage.id) {
                  case 'rwa':
                    additionalContent = renderRWAVisualization();
                    break;
                  case 'basel2':
                    additionalContent = renderThreePillars();
                    break;
                  case 'leverage':
                  case 'car':
                    additionalContent = renderDualConstraint();
                    break;
                  case 'ifrs9':
                    additionalContent = renderIFRS9Comparison();
                    break;
                  case 'intro':
                  case 'crisis':
                  case 'basel1':
                  case 'basel3':
                  case 'basel4':
                    additionalContent = renderTimeline();
                    break;
                  default:
                    break;
                }

                return additionalContent;
              };

              const containerStyle = {
                minHeight: '700px',
                background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
                fontFamily: "'DM Sans', sans-serif",
                color: 'white',
                position: 'relative',
                overflow: 'hidden',
                borderRadius: '24px',
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)'
              };

              return (
                <div style={containerStyle}>
                  {/* CSS Animations */}
                  <style>{`
                    @keyframes fadeSlideIn {
                      from { opacity: 0; transform: translateX(-20px); }
                      to { opacity: 1; transform: translateX(0); }
                    }
                    @keyframes fadeSlideUp {
                      from { opacity: 0; transform: translateY(20px); }
                      to { opacity: 1; transform: translateY(0); }
                    }
                    @keyframes pulse {
                      0%, 100% { opacity: 0.1; transform: scale(1); }
                      50% { opacity: 0.3; transform: scale(1.1); }
                    }
                    @keyframes float {
                      0%, 100% { transform: translateY(0px); }
                      50% { transform: translateY(-10px); }
                    }
                    @keyframes glow {
                      0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
                      50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.6); }
                    }
                  `}</style>

                  {/* Background Gradient */}
                  <div style={{
                    position: 'absolute',
                    top: 0, left: 0, right: 0, bottom: 0,
                    background: 'radial-gradient(ellipse at 30% 20%, rgba(59,130,246,0.15) 0%, transparent 50%), radial-gradient(ellipse at 70% 80%, rgba(139,92,246,0.15) 0%, transparent 50%)',
                    pointerEvents: 'none'
                  }} />

                  {/* Particles */}
                  {particlePositions.map(p => (
                    <div key={p.id} style={{
                      position: 'absolute',
                      left: `${p.x}%`,
                      top: `${p.y}%`,
                      width: `${p.size}px`,
                      height: `${p.size}px`,
                      background: 'rgba(59, 130, 246, 0.3)',
                      borderRadius: '50%',
                      animation: `pulse ${3 / p.speed}s ease-in-out infinite`,
                      pointerEvents: 'none'
                    }} />
                  ))}

                  {/* Header */}
                  <div style={{
                    padding: '24px 32px',
                    borderBottom: '1px solid rgba(255,255,255,0.1)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    position: 'relative',
                    zIndex: 10
                  }}>
                    <div>
                      <h1 style={{
                        margin: 0,
                        fontSize: '24px',
                        fontWeight: '600',
                        background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        fontFamily: "'Playfair Display', serif"
                      }}>
                        Acordos de Basileia
                      </h1>
                      <p style={{
                        margin: '4px 0 0 0',
                        fontSize: '12px',
                        color: 'rgba(255,255,255,0.5)',
                        letterSpacing: '2px',
                        textTransform: 'uppercase'
                      }}>
                        Regulação Prudencial Bancária
                      </p>
                    </div>
                    <span style={{
                      fontSize: '11px',
                      color: 'rgba(255,255,255,0.5)',
                      padding: '6px 12px',
                      background: 'rgba(255,255,255,0.05)',
                      borderRadius: '20px'
                    }}>
                      Coppead/UFRJ
                    </span>
                  </div>

                  {/* Main Content */}
                  <div style={{
                    display: 'flex',
                    padding: '24px 32px',
                    gap: '32px',
                    position: 'relative',
                    zIndex: 10
                  }}>
                    {/* Left Panel */}
                    <div style={{ flex: '1.2', display: 'flex', flexDirection: 'column' }}>
                      {/* Progress */}
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        marginBottom: '20px'
                      }}>
                        <div style={{
                          background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)',
                          padding: '8px 16px',
                          borderRadius: '20px',
                          fontSize: '12px',
                          fontWeight: '600'
                        }}>
                          Módulo {currentStage + 1} de {stages.length}
                        </div>
                        <div style={{
                          flex: 1,
                          height: '4px',
                          background: 'rgba(255,255,255,0.1)',
                          borderRadius: '2px',
                          overflow: 'hidden'
                        }}>
                          <div style={{
                            height: '100%',
                            width: `${((currentStage + 1) / stages.length) * 100}%`,
                            background: 'linear-gradient(90deg, #3B82F6, #8B5CF6)',
                            borderRadius: '2px',
                            transition: 'width 0.5s ease-out'
                          }} />
                        </div>
                      </div>

                      {/* Stage Card */}
                      <div style={{
                        background: 'rgba(255,255,255,0.03)',
                        borderRadius: '20px',
                        padding: '32px',
                        border: '1px solid rgba(255,255,255,0.08)',
                        animation: animationPhase === 'entering' ? 'fadeSlideUp 0.5s ease-out' : 'none'
                      }}>
                        <div style={{
                          fontSize: '48px',
                          marginBottom: '16px',
                          animation: 'float 3s ease-in-out infinite'
                        }}>
                          {stages[currentStage].icon}
                        </div>
                        <h2 style={{
                          margin: '0 0 8px 0',
                          fontSize: '28px',
                          fontWeight: '700',
                          fontFamily: "'Playfair Display', serif",
                          lineHeight: 1.2
                        }}>
                          {stages[currentStage].title}
                        </h2>
                        <p style={{
                          margin: '0 0 20px 0',
                          fontSize: '16px',
                          color: '#3B82F6',
                          fontWeight: '500'
                        }}>
                          {stages[currentStage].subtitle}
                        </p>
                        <p style={{
                          margin: 0,
                          fontSize: '14px',
                          lineHeight: 1.7,
                          color: 'rgba(255,255,255,0.8)'
                        }}>
                          {stages[currentStage].description}
                        </p>
                        {renderStageContent()}
                      </div>

                      {/* Navigation */}
                      <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginTop: '20px',
                        gap: '12px'
                      }}>
                        <button
                          onClick={() => setCurrentStage(Math.max(0, currentStage - 1))}
                          disabled={currentStage === 0}
                          style={{
                            padding: '12px 24px',
                            background: currentStage === 0 ? 'rgba(255,255,255,0.05)' : 'rgba(255,255,255,0.1)',
                            border: 'none',
                            borderRadius: '12px',
                            color: currentStage === 0 ? 'rgba(255,255,255,0.3)' : 'white',
                            cursor: currentStage === 0 ? 'not-allowed' : 'pointer',
                            fontSize: '13px',
                            fontWeight: '500',
                            transition: 'all 0.2s ease',
                            fontFamily: "'DM Sans', sans-serif"
                          }}
                        >
                          ← Anterior
                        </button>

                        <button
                          onClick={() => setIsPlaying(!isPlaying)}
                          style={{
                            padding: '12px 32px',
                            background: isPlaying 
                              ? 'linear-gradient(135deg, #EF4444, #DC2626)' 
                              : 'linear-gradient(135deg, #3B82F6, #8B5CF6)',
                            border: 'none',
                            borderRadius: '12px',
                            color: 'white',
                            cursor: 'pointer',
                            fontSize: '13px',
                            fontWeight: '600',
                            transition: 'all 0.2s ease',
                            animation: 'glow 2s ease-in-out infinite',
                            fontFamily: "'DM Sans', sans-serif"
                          }}
                        >
                          {isPlaying ? '⏸ Pausar' : '▶ Reproduzir'}
                        </button>

                        <button
                          onClick={() => setCurrentStage(Math.min(stages.length - 1, currentStage + 1))}
                          disabled={currentStage === stages.length - 1}
                          style={{
                            padding: '12px 24px',
                            background: currentStage === stages.length - 1 ? 'rgba(255,255,255,0.05)' : 'rgba(255,255,255,0.1)',
                            border: 'none',
                            borderRadius: '12px',
                            color: currentStage === stages.length - 1 ? 'rgba(255,255,255,0.3)' : 'white',
                            cursor: currentStage === stages.length - 1 ? 'not-allowed' : 'pointer',
                            fontSize: '13px',
                            fontWeight: '500',
                            transition: 'all 0.2s ease',
                            fontFamily: "'DM Sans', sans-serif"
                          }}
                        >
                          Próximo →
                        </button>
                      </div>
                    </div>

                    {/* Right Panel - Dashboard */}
                    <div style={{
                      width: '300px',
                      background: 'rgba(0,0,0,0.2)',
                      borderRadius: '20px',
                      padding: '24px',
                      border: '1px solid rgba(255,255,255,0.08)'
                    }}>
                      <h3 style={{
                        margin: '0 0 20px 0',
                        fontSize: '14px',
                        fontWeight: '600',
                        color: 'rgba(255,255,255,0.9)',
                        textTransform: 'uppercase',
                        letterSpacing: '1px'
                      }}>
                        📊 Painel do Banco
                      </h3>

                      {/* Gauges */}
                      <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(2, 1fr)',
                        gap: '20px',
                        marginBottom: '24px'
                      }}>
                        {renderGauge(bankMetrics.car, 10.5, 'CAR')}
                        {renderGauge(bankMetrics.leverage, 3, 'Alavancagem')}
                      </div>

                      {/* Metrics */}
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {[
                          { label: 'Capital Total', value: `R$ ${bankMetrics.capital}M`, color: '#10B981' },
                          { label: 'Ativos Totais', value: `R$ ${bankMetrics.assets}M`, color: '#3B82F6' },
                          { label: 'RWA', value: `R$ ${bankMetrics.rwa}M`, color: '#8B5CF6' },
                          { label: 'Provisões', value: `R$ ${bankMetrics.provisions}M`, color: '#F59E0B' }
                        ].map((m, i) => (
                          <div key={i} style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            padding: '12px 16px',
                            background: 'rgba(255,255,255,0.03)',
                            borderRadius: '10px',
                            border: '1px solid rgba(255,255,255,0.05)'
                          }}>
                            <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.7)' }}>{m.label}</span>
                            <span style={{ fontSize: '14px', fontWeight: '600', color: m.color }}>{m.value}</span>
                          </div>
                        ))}
                      </div>

                      {/* Status */}
                      <div style={{
                        marginTop: '20px',
                        padding: '16px',
                        background: bankMetrics.car >= 10.5 && bankMetrics.leverage >= 3 
                          ? 'rgba(16,185,129,0.15)'
                          : 'rgba(239,68,68,0.15)',
                        borderRadius: '12px',
                        border: bankMetrics.car >= 10.5 && bankMetrics.leverage >= 3
                          ? '1px solid rgba(16,185,129,0.3)'
                          : '1px solid rgba(239,68,68,0.3)',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontSize: '20px', marginBottom: '8px' }}>
                          {bankMetrics.car >= 10.5 && bankMetrics.leverage >= 3 ? '✅' : '⚠️'}
                        </div>
                        <div style={{
                          fontSize: '12px',
                          fontWeight: '600',
                          color: bankMetrics.car >= 10.5 && bankMetrics.leverage >= 3 ? '#10B981' : '#EF4444'
                        }}>
                          {bankMetrics.car >= 10.5 && bankMetrics.leverage >= 3 ? 'Em Conformidade' : 'Atenção Regulatória'}
                        </div>
                        <div style={{
                          fontSize: '10px',
                          color: 'rgba(255,255,255,0.5)',
                          marginTop: '4px'
                        }}>
                          {bankMetrics.car >= 10.5 
                            ? 'Acima do mínimo regulatório'
                            : 'Abaixo do mínimo regulatório'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Stage Dots */}
                  <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    gap: '8px',
                    padding: '20px',
                    position: 'relative',
                    zIndex: 10
                  }}>
                    {stages.map((_, i) => (
                      <button
                        key={i}
                        onClick={() => setCurrentStage(i)}
                        style={{
                          width: currentStage === i ? '24px' : '8px',
                          height: '8px',
                          borderRadius: '4px',
                          background: currentStage === i 
                            ? 'linear-gradient(90deg, #3B82F6, #8B5CF6)' 
                            : 'rgba(255,255,255,0.2)',
                          border: 'none',
                          cursor: 'pointer',
                          transition: 'all 0.3s ease'
                        }}
                      />
                    ))}
                  </div>

                  {/* Footer */}
                  <div style={{
                    padding: '16px 32px',
                    borderTop: '1px solid rgba(255,255,255,0.1)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    position: 'relative',
                    zIndex: 10
                  }}>
                    <p style={{ margin: 0, fontSize: '11px', color: 'rgba(255,255,255,0.4)' }}>
                      © 2025 Prof. José Américo | Coppead - UFRJ Business School
                    </p>
                    <p style={{ margin: 0, fontSize: '11px', color: 'rgba(255,255,255,0.4)' }}>
                      Ferramenta Pedagógica para Educação Financeira
                    </p>
                  </div>
                </div>
              );
            };

            // Render the React component
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<BaselAccordsAnimation />);
        </script>
    </body>
    </html>
    '''
    
        # Renderizar a animação React usando st.components.v1.html
        import streamlit.components.v1 as components
        components.html(react_animation_html, height=900, scrolling=False)
    
        # Informações adicionais abaixo da animação
        with st.expander("ℹ️ Sobre esta Animação"):
            st.markdown("""
            ### Módulos da Animação (React Component)
        
            Esta animação foi construída usando **React 18** e renderiza um componente funcional
            com hooks (`useState`, `useEffect`) para gerenciar estado e efeitos.
        
            | # | Módulo | Descrição |
            |---|--------|-----------|
            | 1 | 🏛️ Introdução | Visão geral da regulação prudencial |
            | 2 | 📉 Crise de 2008 | Motivação para a regulação |
            | 3 | 📜 Basileia I | Capital mínimo de 8% sobre RWA |
            | 4 | ⚖️ RWA | Ativos ponderados pelo risco |
            | 5 | 🏗️ Basileia II | Os Três Pilares |
            | 6 | 🛡️ Basileia III | Resposta à crise financeira |
            | 7 | 📊 CAR | Índice de Adequação de Capital |
            | 8 | 🔒 Alavancagem | Sistema de restrição dupla |
            | 9 | 📈 IFRS 9 | Provisão para perdas esperadas |
            | 10 | 🔧 Basileia IV | Refinamentos de 2023 |
            | 11 | 🎮 Simulação | Gestão estratégica de capital |
            | 12 | 🌍 Conclusão | Estabilidade financeira global |
                    """)
        
    # ==================== QUIZ & RECURSOS ====================
    else:
        st.header("🧠 Quiz Final & Recursos")
    
        st.success("Parabéns por chegar até aqui! Teste seu conhecimento:")
    
        with st.form("m06_quiz"):
            q1 = st.radio("Qual o capital mínimo exigido pelo Basel III (Pilar 1)?", ["4%", "8%", "10.5%"], key="m06_q1")
            q2 = st.radio("O que o Leverage Ratio tenta evitar?", ["Risco de crédito", "Alavancagem excessiva independentemente do risco dos ativos", "Risco operacional"], key="m06_q2")
            q3 = st.checkbox("Res 4966 é mais conservadora que Res 2682 em recessões", key="m06_q3")
        
            if st.form_submit_button("Ver resultado"):
                pontos = 0
                if q1 == "10.5%": pontos += 1
                if q2 == "Alavancagem excessiva independentemente do risco dos ativos": pontos += 1
                if q3: pontos += 1
            
                st.write(f"Você acertou {pontos}/3!")
    
        st.markdown("### 📚 Recursos Adicionais")
        st.markdown("- [Site oficial do BIS](https://www.bis.org/bcbs/basel3.htm)")
        st.markdown("- [Resumo Basel III - BCB](https://www.bcb.gov.br/estabilidadefinanceira/basileia3)")
        st.markdown("- Glossário completo de termos regulatórios")


# =============================================================================
# EXECUÇÃO STANDALONE (para testes)
# =============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="Acordos de Basileia - Explorador Pedagógico",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()