import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def run():
    st.title("🛡️ Módulo 3: Laboratório de Subordinação e Risco")
    st.markdown("### Como a Cota Subordinada Protege a Cota Sênior")
    
    st.markdown("""
    A **subordinação** é o mecanismo de proteção mais importante em um FIDC estruturado. 
    Este módulo simula como as perdas são absorvidas pelas diferentes camadas de cotas.
    """)
    
    # Explicação conceitual
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 💡 Como Funciona a Subordinação?
    
    **Princípio do "Escudo de Proteção":**
    
    Imagine um castelo com múltiplas muralhas. A cota **Subordinada (Júnior)** é a primeira 
    linha de defesa - absorve todas as perdas antes que qualquer dano chegue à cota **Sênior**.
    
    **Ordem de Absorção de Prejuízos (Waterfall de Perdas):**
    1. 🔴 **Júnior absorve primeiro** - até sua eliminação total
    2. 🟡 **Mezanino absorve** (se houver) - após Júnior zerada
    3. 🔵 **Sênior absorve por último** - apenas se todas as outras foram eliminadas
    
    Por isso, a cota Sênior é considerada de **baixo risco** e oferece menor retorno,
    enquanto a Júnior tem **alto risco** mas potencial de retorno muito maior.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interface de simulação
    col_inputs, col_visual = st.columns([1, 2])
    
    with col_inputs:
        st.markdown("### ⚙️ Parâmetros da Simulação")
        
        # Base para cálculos
        st.markdown("#### 📊 Estrutura do Fundo")
        
        pl_total = st.number_input(
            "Patrimônio Líquido Total (R$ milhões)",
            min_value=10.0,
            max_value=500.0,
            value=100.0,
            step=10.0,
            help="Tamanho total do fundo"
        )
        
        # Índice de subordinação
        subordinacao_pct = st.slider(
            "Índice de Subordinação (%)",
            min_value=10,
            max_value=50,
            value=20,
            step=5,
            help="Percentual da cota subordinada que protege a sênior"
        )
        
        # Opção de mezanino
        incluir_mezanino = st.checkbox(
            "Incluir Cota Mezanino",
            value=False,
            help="Adiciona uma camada intermediária de risco"
        )
        
        st.markdown("---")
        st.markdown("#### 📉 Cenário de Stress")
        
        # Simular perda
        perda_carteira = st.slider(
            "Perda Simulada na Carteira (R$ milhões)",
            min_value=0.0,
            max_value=float(pl_total * 0.6),
            value=float(pl_total * 0.05),
            step=float(pl_total * 0.01),
            help="Valor de inadimplência ou perdas na carteira"
        )
        
        perda_pct = (perda_carteira / pl_total * 100) if pl_total > 0 else 0
        
        st.metric(
            "Perda em % do PL",
            f"{perda_pct:.1f}%",
            delta=f"{perda_pct - subordinacao_pct:.1f}pp vs subordinação",
            delta_color="inverse"
        )
        
        st.markdown("---")
        
    
    with col_visual:
        st.markdown("### 📊 Visualização da Estrutura de Capital")
        
        # Cálculos
        if not incluir_mezanino:
            # Estrutura simples: Sênior + Júnior
            senior_inicial = pl_total * (1 - subordinacao_pct/100)
            junior_inicial = pl_total * (subordinacao_pct/100)
            mezanino_inicial = 0
            
            # Lógica de absorção de prejuízo
            if perda_carteira <= junior_inicial:
                junior_final = junior_inicial - perda_carteira
                senior_final = senior_inicial
                mezanino_final = 0
                status = "✅ Cota Sênior Intacta"
                status_cor = "success"
                explicacao = f"A perda de R$ {perda_carteira:.1f}M foi completamente absorvida pela cota Júnior (R$ {junior_inicial:.1f}M). O 'escudo' funcionou perfeitamente."
            else:
                # Perda consumiu toda a Júnior e atingiu a Sênior
                junior_final = 0
                dano_na_senior = perda_carteira - junior_inicial
                senior_final = senior_inicial - dano_na_senior
                mezanino_final = 0
                status = "🚨 PERDA NA SÊNIOR - Desenquadramento Crítico"
                status_cor = "error"
                explicacao = f"A perda de R$ {perda_carteira:.1f}M excedeu a proteção da Júnior (R$ {junior_inicial:.1f}M). A Sênior sofreu prejuízo de R$ {dano_na_senior:.1f}M."
        
        else:
            # Estrutura com Mezanino: Sênior + Mezanino + Júnior
            subordinacao_total = subordinacao_pct
            junior_pct = subordinacao_total / 2
            mezanino_pct = subordinacao_total / 2
            senior_pct = 100 - subordinacao_total
            
            senior_inicial = pl_total * (senior_pct/100)
            mezanino_inicial = pl_total * (mezanino_pct/100)
            junior_inicial = pl_total * (junior_pct/100)
            
            # Lógica de absorção em três camadas
            if perda_carteira <= junior_inicial:
                # Perda absorvida apenas pela Júnior
                junior_final = junior_inicial - perda_carteira
                mezanino_final = mezanino_inicial
                senior_final = senior_inicial
                status = "✅ Cotas Sênior e Mezanino Intactas"
                status_cor = "success"
                explicacao = f"A perda de R$ {perda_carteira:.1f}M foi absorvida pela Júnior. Mezanino e Sênior protegidos."
            
            elif perda_carteira <= (junior_inicial + mezanino_inicial):
                # Júnior zerada, Mezanino parcialmente atingida
                junior_final = 0
                dano_no_mezanino = perda_carteira - junior_inicial
                mezanino_final = mezanino_inicial - dano_no_mezanino
                senior_final = senior_inicial
                status = "⚠️ Júnior Eliminada, Mezanino Atingido, Sênior Protegida"
                status_cor = "warning"
                explicacao = f"Júnior (R$ {junior_inicial:.1f}M) totalmente consumida. Mezanino perdeu R$ {dano_no_mezanino:.1f}M. Sênior permanece intacta."
            
            else:
                # Júnior e Mezanino zeradas, Sênior atingida
                junior_final = 0
                mezanino_final = 0
                dano_na_senior = perda_carteira - junior_inicial - mezanino_inicial
                senior_final = senior_inicial - dano_na_senior
                status = "🚨 PERDA NA SÊNIOR - Desenquadramento Crítico"
                status_cor = "error"
                explicacao = f"Júnior e Mezanino eliminadas. Sênior sofreu prejuízo de R$ {dano_na_senior:.1f}M."
        
        # Exibir status
        if status_cor == "success":
            st.markdown(f'<div class="success-box"><h3>{status}</h3><p>{explicacao}</p></div>', unsafe_allow_html=True)
        elif status_cor == "warning":
            st.markdown(f'<div class="warning-box"><h3>{status}</h3><p>{explicacao}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box"><h3>{status}</h3><p>{explicacao}</p></div>', unsafe_allow_html=True)
        
        # Gráfico de barras empilhadas
        fig = go.Figure()
        
        # Estado inicial
        if incluir_mezanino:
            fig.add_trace(go.Bar(
                name='Júnior',
                x=['Estado Inicial', 'Após Perda'],
                y=[junior_inicial, junior_final],
                marker_color='#ff6b6b',
                text=[f'R$ {junior_inicial:.1f}M<br>({junior_inicial/pl_total*100:.0f}%)', 
                      f'R$ {junior_final:.1f}M<br>({junior_final/pl_total*100:.0f}%)'],
                textposition='inside',
                hovertemplate='<b>Júnior</b><br>Valor: R$ %{y:.1f}M<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Mezanino',
                x=['Estado Inicial', 'Após Perda'],
                y=[mezanino_inicial, mezanino_final],
                marker_color='#ffd43b',
                text=[f'R$ {mezanino_inicial:.1f}M<br>({mezanino_inicial/pl_total*100:.0f}%)', 
                      f'R$ {mezanino_final:.1f}M<br>({mezanino_final/pl_total*100:.0f}%)'],
                textposition='inside',
                hovertemplate='<b>Mezanino</b><br>Valor: R$ %{y:.1f}M<extra></extra>'
            ))
        else:
            fig.add_trace(go.Bar(
                name='Subordinada (Júnior)',
                x=['Estado Inicial', 'Após Perda'],
                y=[junior_inicial, junior_final],
                marker_color='#ff6b6b',
                text=[f'R$ {junior_inicial:.1f}M<br>({subordinacao_pct:.0f}%)', 
                      f'R$ {junior_final:.1f}M<br>({junior_final/pl_total*100:.0f}%)'],
                textposition='inside',
                hovertemplate='<b>Subordinada</b><br>Valor: R$ %{y:.1f}M<extra></extra>'
            ))
        
        fig.add_trace(go.Bar(
            name='Sênior',
            x=['Estado Inicial', 'Após Perda'],
            y=[senior_inicial, senior_final],
            marker_color='#51cf66',
            text=[f'R$ {senior_inicial:.1f}M<br>({senior_inicial/pl_total*100:.0f}%)', 
                  f'R$ {senior_final:.1f}M<br>({senior_final/pl_total*100:.0f}%)'],
            textposition='inside',
            hovertemplate='<b>Sênior</b><br>Valor: R$ %{y:.1f}M<extra></extra>'
        ))
        
        fig.update_layout(
            barmode='stack',
            title=f'Impacto de Perda de R$ {perda_carteira:.1f}M ({perda_pct:.1f}% do PL)',
            height=500,
            yaxis_title='Patrimônio (R$ milhões)',
            xaxis_title='',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de resumo
        st.markdown("#### 📋 Resumo Quantitativo")
        
        if incluir_mezanino:
            df_resumo = pd.DataFrame({
                'Cota': ['Sênior', 'Mezanino', 'Júnior', 'TOTAL'],
                'Inicial (R$ M)': [senior_inicial, mezanino_inicial, junior_inicial, pl_total],
                'Perda (R$ M)': [
                    senior_inicial - senior_final,
                    mezanino_inicial - mezanino_final,
                    junior_inicial - junior_final,
                    perda_carteira
                ],
                'Final (R$ M)': [senior_final, mezanino_final, junior_final, pl_total - perda_carteira],
                'Perda (%)': [
                    (senior_inicial - senior_final) / senior_inicial * 100 if senior_inicial > 0 else 0,
                    (mezanino_inicial - mezanino_final) / mezanino_inicial * 100 if mezanino_inicial > 0 else 0,
                    (junior_inicial - junior_final) / junior_inicial * 100 if junior_inicial > 0 else 0,
                    perda_pct
                ]
            })
        else:
            df_resumo = pd.DataFrame({
                'Cota': ['Sênior', 'Subordinada', 'TOTAL'],
                'Inicial (R$ M)': [senior_inicial, junior_inicial, pl_total],
                'Perda (R$ M)': [
                    senior_inicial - senior_final,
                    junior_inicial - junior_final,
                    perda_carteira
                ],
                'Final (R$ M)': [senior_final, junior_final, pl_total - perda_carteira],
                'Perda (%)': [
                    (senior_inicial - senior_final) / senior_inicial * 100 if senior_inicial > 0 else 0,
                    (junior_inicial - junior_final) / junior_inicial * 100 if junior_inicial > 0 else 0,
                    perda_pct
                ]
            })
        
        # Formatar valores
        df_resumo['Inicial (R$ M)'] = df_resumo['Inicial (R$ M)'].apply(lambda x: f'{x:.1f}')
        df_resumo['Perda (R$ M)'] = df_resumo['Perda (R$ M)'].apply(lambda x: f'{x:.1f}')
        df_resumo['Final (R$ M)'] = df_resumo['Final (R$ M)'].apply(lambda x: f'{x:.1f}')
        df_resumo['Perda (%)'] = df_resumo['Perda (%)'].apply(lambda x: f'{x:.1f}%')
        
        st.dataframe(df_resumo, hide_index=True, use_container_width=True)
    
    # Análise de desenquadramento
    st.markdown("---")
    st.markdown("## ⚠️ Conceito de Desenquadramento")
    
    col_des1, col_des2 = st.columns([1, 1])
    
    with col_des1:
        st.markdown("### O que é Desenquadramento?")
        st.write("""
        Ocorre quando o **índice de subordinação efetivo** cai abaixo do **índice mínimo** 
        estabelecido no regulamento do fundo.
        
        **Exemplo:**
        - Subordinação contratual: 20%
        - Após perdas: subordinação efetiva cai para 15%
        - **Resultado:** Fundo desenquadrado
        
        **Consequências:**
        - Suspensão de pagamentos à Júnior
        - Retenção obrigatória de receitas
        - Necessidade de aporte adicional
        - Possível amortização extraordinária de Sênior
        """)
    
    with col_des2:
        st.markdown("### Índice Atual do Fundo")
        
        patrimonio_pos_perda = pl_total - perda_carteira
        
        if incluir_mezanino:
            subordinacao_efetiva = ((mezanino_final + junior_final) / patrimonio_pos_perda * 100) if patrimonio_pos_perda > 0 else 0
        else:
            subordinacao_efetiva = (junior_final / patrimonio_pos_perda * 100) if patrimonio_pos_perda > 0 else 0
        
        desenquadrado = subordinacao_efetiva < subordinacao_pct
        
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.metric(
                "Subordinação Contratual",
                f"{subordinacao_pct}%",
                help="Índice mínimo estabelecido no regulamento"
            )
        
        with col_metric2:
            delta_sub = subordinacao_efetiva - subordinacao_pct
            st.metric(
                "Subordinação Efetiva",
                f"{subordinacao_efetiva:.1f}%",
                f"{delta_sub:+.1f}pp",
                delta_color="inverse" if delta_sub < 0 else "normal",
                help="Índice atual após as perdas"
            )
        
        if desenquadrado:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("""
            ### 🚨 FUNDO DESENQUADRADO
            
            O índice de subordinação efetivo está **abaixo** do mínimo contratual.
            
            **Ações Necessárias:**
            1. Suspender distribuição de rendimentos à Júnior
            2. Reter receitas para recompor subordinação
            3. Convocar assembleia de cotistas
            4. Avaliar necessidade de aporte ou resgate antecipado
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("""
            ### ✅ FUNDO ENQUADRADO
            
            O índice de subordinação permanece **acima** do mínimo estabelecido.
            
            O fundo pode continuar operando normalmente.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Análise de sensibilidade
    st.markdown("---")
    st.markdown("## 📈 Análise de Sensibilidade: Testando Diferentes Cenários")
    
    st.write("""
    O gráfico abaixo mostra como diferentes níveis de perda afetam cada camada de cotas.
    Identifique os **pontos de ruptura** onde cada cota é eliminada.
    """)
    
    # Gerar cenários de 0% a 60% de perda
    perdas_simuladas = np.linspace(0, pl_total * 0.6, 50)
    
    senior_valores = []
    mezanino_valores = []
    junior_valores = []
    
    for perda_sim in perdas_simuladas:
        if not incluir_mezanino:
            if perda_sim <= junior_inicial:
                senior_valores.append(senior_inicial)
                junior_valores.append(junior_inicial - perda_sim)
                mezanino_valores.append(0)
            else:
                dano_senior = perda_sim - junior_inicial
                senior_valores.append(max(0, senior_inicial - dano_senior))
                junior_valores.append(0)
                mezanino_valores.append(0)
        else:
            if perda_sim <= junior_inicial:
                senior_valores.append(senior_inicial)
                mezanino_valores.append(mezanino_inicial)
                junior_valores.append(junior_inicial - perda_sim)
            elif perda_sim <= (junior_inicial + mezanino_inicial):
                dano_mezanino = perda_sim - junior_inicial
                senior_valores.append(senior_inicial)
                mezanino_valores.append(mezanino_inicial - dano_mezanino)
                junior_valores.append(0)
            else:
                dano_senior = perda_sim - junior_inicial - mezanino_inicial
                senior_valores.append(max(0, senior_inicial - dano_senior))
                mezanino_valores.append(0)
                junior_valores.append(0)
    
    # Gráfico de área empilhada
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=perdas_simuladas / pl_total * 100,
        y=np.array(junior_valores),
        mode='lines',
        name='Júnior',
        fill='tozeroy',
        line=dict(color='#ff6b6b', width=0),
        fillcolor='rgba(255, 107, 107, 0.7)',
        hovertemplate='Júnior: R$ %{y:.1f}M<extra></extra>'
    ))
    
    if incluir_mezanino:
        fig2.add_trace(go.Scatter(
            x=perdas_simuladas / pl_total * 100,
            y=np.array(mezanino_valores) + np.array(junior_valores),
            mode='lines',
            name='Mezanino',
            fill='tonexty',
            line=dict(color='#ffd43b', width=0),
            fillcolor='rgba(255, 212, 59, 0.7)',
            hovertemplate='Mezanino: R$ %{y:.1f}M<extra></extra>'
        ))
    
    fig2.add_trace(go.Scatter(
        x=perdas_simuladas / pl_total * 100,
        y=np.array(senior_valores) + np.array(mezanino_valores) + np.array(junior_valores),
        mode='lines',
        name='Sênior',
        fill='tonexty',
        line=dict(color='#51cf66', width=0),
        fillcolor='rgba(81, 207, 102, 0.7)',
        hovertemplate='Sênior: R$ %{y:.1f}M<extra></extra>'
    ))
    
    # Marcar perda atual
    fig2.add_vline(
        x=perda_pct,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Perda Atual: {perda_pct:.1f}%",
        annotation_position="top"
    )
    
    fig2.update_layout(
        title="Resiliência das Cotas a Diferentes Níveis de Perda",
        xaxis_title="Perda na Carteira (% do PL)",
        yaxis_title="Patrimônio Remanescente (R$ milhões)",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Identificar pontos de ruptura
    st.markdown("### 🎯 Pontos de Ruptura Identificados")
    
    col_rupt1, col_rupt2, col_rupt3 = st.columns(3)
    
    with col_rupt1:
        st.metric(
            "Júnior Eliminada em:",
            f"{junior_inicial / pl_total * 100:.1f}% de perda",
            help="Ponto onde a cota Júnior é totalmente consumida"
        )
    
    with col_rupt2:
        if incluir_mezanino:
            st.metric(
                "Mezanino Eliminado em:",
                f"{(junior_inicial + mezanino_inicial) / pl_total * 100:.1f}% de perda",
                help="Ponto onde a cota Mezanino é totalmente consumida"
            )
        else:
            st.metric(
                "Sênior Atingida em:",
                f"{junior_inicial / pl_total * 100:.1f}% de perda",
                help="Ponto onde perdas começam a afetar a Sênior"
            )
    
    with col_rupt3:
        limite_total = junior_inicial + mezanino_inicial + senior_inicial
        st.metric(
            "Fundo Eliminado em:",
            f"{limite_total / pl_total * 100:.0f}% de perda",
            help="Perda que zeraria todo o patrimônio"
        )
    
    # Conceitos pedagógicos
    st.markdown("---")
    st.markdown("### 🎓 Conceitos-Chave")
    
    with st.expander("📚 Por que a subordinação é essencial?"):
        st.write("""
        **Função de Proteção (Credit Enhancement):**
        
        A subordinação não é apenas um mecanismo de distribuição de riscos - é o que permite 
        que um FIDC acesse o mercado de varejo. Sem subordinação adequada, seria impossível 
        obter rating investment grade para a cota sênior.
        
        **Analogia com Seguros:**
        
        Pense na cota subordinada como uma "franquia" ou "seguro de primeira perda":
        - O cotista júnior aceita perdas até R$ X (a franquia)
        - Em troca, recebe retorno muito superior
        - O cotista sênior só perde se as perdas excederem R$ X
        - Por isso, aceita retorno menor
        
        **Alinhamento de Incentivos:**
        
        Tipicamente, o originador (empresa que cede os recebíveis) mantém a cota subordinada.
        Isso garante "skin in the game" - se a qualidade da carteira deteriorar, o originador 
        perde primeiro. Isso protege os investidores sênior de seleção adversa.
        
        **Dimensionamento:**
        
        O índice de subordinação ideal depende de:
        - Histórico de inadimplência da carteira (PDD - Provisão para Devedores Duvidosos)
        - Volatilidade das perdas
        - Rating desejado para a cota sênior
        - Apetite de risco do mercado
        
        Carteiras mais arriscadas (ex: cartão de crédito) tipicamente exigem subordinação de 30-40%.
        Carteiras seguras (ex: recebíveis de empresas blue chip) podem operar com 10-15%.
        """)
    
    with st.expander("⚖️ Recomposição de Subordinação"):
        st.write("""
        **Quando o índice cai abaixo do mínimo, o fundo deve agir:**
        
        **Opção 1: Retenção de Receitas (Automática)**
        - Suspende distribuição de rendimentos à Júnior
        - Receitas retidas aumentam o patrimônio da Júnior
        - Processo pode levar meses para recompor
        
        **Opção 2: Aporte de Capital**
        - Originador injeta recursos na Júnior
        - Recomposição imediata
        - Mais custoso, mas evita desenquadramento prolongado
        
        **Opção 3: Amortização Extraordinária de Sênior**
        - Reduz a base de cálculo da subordinação
        - Aumenta o índice percentual
        - Pode frustrar investidores sênior (saída antecipada)
        
        **Opção 4: Substituição de Ativos**
        - Troca recebíveis ruins por bons (se permitido pelo regulamento)
        - Melhora qualidade e restaura subordinação
        - Requer aprovação de assembleia
        
        **Prevenção:**
        
        Fundos bem geridos mantêm margem de segurança. Se a subordinação contratual é 20%, 
        operam com 25-30% para absorver volatilidade sem desenquadrar.
        """)
    
    with st.expander("💰 Remuneração: Por que Júnior ganha mais?"):
        st.write("""
        **Estrutura Típica de Remuneração:**
        
        **Cota Sênior:**
        - Retorno: CDI + 1% a 3% a.a.
        - Risco: Baixo (primeira a receber, última a perder)
        - Perfil: Investidores conservadores, fundos de pensão, seguradoras
        
        **Cota Mezanino (se houver):**
        - Retorno: CDI + 4% a 7% a.a.
        - Risco: Médio (segunda na fila de pagamentos)
        - Perfil: Fundos de crédito, family offices
        
        **Cota Subordinada:**
        - Retorno: CDI + 8% a 15% a.a. (ou mais)
        - Risco: Alto (última a receber, primeira a perder)
        - Perfil: Originador, fundos especializados em high yield
        
        **Retorno Residual:**
        
        Além do yield contratado, a Júnior pode ter direito ao "excesso de spread" - 
        ou seja, se a carteira performar melhor que o esperado, a diferença vai para a Júnior.
        
        Exemplo:
        - Carteira rende: 18% a.a.
        - Custos + Sênior: 12% a.a.
        - Excesso: 6% a.a. → vai para a Júnior
        
        Isso cria um retorno "assimétrico" - perdas limitadas (no máximo 100% do investimento), 
        mas potencial de ganho ilimitado.
        """)
