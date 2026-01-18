import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def run():
    st.title("📊 Módulo 1: Simulador de Viabilidade Econômica")
    st.markdown("### O Breakeven: Por que FIDCs pequenos são inviáveis?")
    
    st.markdown("""
    Este módulo demonstra matematicamente a estrutura de custos de um FIDC e identifica 
    o **ponto de equilíbrio** (breakeven) mínimo para que a estrutura seja economicamente viável.
    """)
    
    # Divisão em colunas
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Parâmetros da Simulação")
        
        # Inputs do usuário
        pl_alvo = st.slider(
            "Patrimônio Líquido (PL) Alvo do FIDC (R$ milhões)",
            min_value=5.0,
            max_value=100.0,
            value=20.0,
            step=5.0,
            help="Tamanho do fundo que você deseja estruturar"
        )
        
        yield_carteira = st.slider(
            "Taxa Média de Cessão / Yield da Carteira (% a.a.)",
            min_value=8.0,
            max_value=25.0,
            value=20.0,
            step=0.5,
            help="Rentabilidade bruta que os ativos geram"
        )
        
        st.markdown("---")
        
        # Custos Fixos (baseados na Tabela 1 do PDF)
        st.markdown("#### 💰 Custos Fixos Anuais")
        
        with st.expander("🔧 Ajustar Custos Fixos"):
            custo_auditoria = st.number_input(
                "Auditoria Externa (R$ mil/ano)",
                value=45.0,
                step=5.0
            )
            
            custo_rating = st.number_input(
                "Rating (R$ mil/ano)",
                value=35.0,
                step=5.0,
                help="Obrigatório para acesso ao varejo"
            )
            
            custo_cvm_anbima = st.number_input(
                "Taxa CVM + Anbima (R$ mil/ano)",
                value=15.0,
                step=2.0
            )
            
            custo_setup_juridico = st.number_input(
                "Setup Jurídico Inicial (R$ mil)",
                value=80.0,
                step=10.0,
                help="Amortizado em 3 anos"
            )
            
            custo_outros = st.number_input(
                "Outros Custos Fixos (R$ mil/ano)",
                value=25.0,
                step=5.0
            )
        
        # Custos Variáveis (% do PL)
        st.markdown("#### 📈 Custos Variáveis (% a.a. do PL)")
        
        taxa_gestao = st.slider(
            "Taxa de Gestão (% a.a.)",
            min_value=0.5,
            max_value=3.0,
            value=1.5,
            step=0.1
        )
        
        taxa_administracao = st.slider(
            "Taxa de Administração (% a.a.)",
            min_value=0.1,
            max_value=1.0,
            value=0.20,
            step=0.05
        )
    
    with col2:
        st.markdown("### 📊 Análise de Viabilidade")
        
        # Cálculos
        receita_bruta = (pl_alvo * 1_000_000 * yield_carteira / 100)  # Converter para R$
        
        # Custos fixos totais (setup amortizado em 3 anos)
        custos_fixos_total = (
            custo_auditoria * 1_000 +
            custo_rating * 1_000 +
            custo_cvm_anbima * 1_000 +
            (custo_setup_juridico * 1_000 / 3) +  # Amortização
            custo_outros * 1_000
        )
        
        # Custos variáveis
        custo_gestao = pl_alvo * 1_000_000 * taxa_gestao / 100
        custo_admin = pl_alvo * 1_000_000 * taxa_administracao / 100
        custos_variaveis_total = custo_gestao + custo_admin
        
        # Resultado
        custos_totais = custos_fixos_total + custos_variaveis_total
        resultado_liquido = receita_bruta - custos_totais
        margem_liquida = (resultado_liquido / receita_bruta * 100) if receita_bruta > 0 else 0
        
        # Gráfico Waterfall
        fig = go.Figure(go.Waterfall(
            name="Estrutura de Custos",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "total"],
            x=[
                "Receita Bruta<br>(Yield)",
                "Auditoria +<br>Rating + CVM",
                "Setup Jurídico<br>(amortizado)",
                "Taxa de<br>Gestão",
                "Taxa de<br>Administração",
                "Resultado<br>Líquido"
            ],
            textposition="outside",
            text=[
                f"R$ {receita_bruta/1_000_000:.2f}M",
                f"-R$ {(custo_auditoria + custo_rating + custo_cvm_anbima + custo_outros)/1000:.0f}k",
                f"-R$ {(custo_setup_juridico/3):.0f}k",
                f"-R$ {custo_gestao/1_000_000:.2f}M",
                f"-R$ {custo_admin/1_000_000:.2f}M",
                f"R$ {resultado_liquido/1_000_000:.2f}M"
            ],
            y=[
                receita_bruta,
                -(custo_auditoria + custo_rating + custo_cvm_anbima + custo_outros) * 1_000,
                -(custo_setup_juridico * 1_000 / 3),
                -custo_gestao,
                -custo_admin,
                resultado_liquido
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#ff6b6b"}},
            increasing={"marker": {"color": "#51cf66"}},
            totals={"marker": {"color": "#1f77b4"}}
        ))
        
        fig.update_layout(
            title=f"Análise de Waterfall - FIDC de R$ {pl_alvo:.0f} milhões",
            height=500,
            showlegend=False,
            yaxis_title="Valor (R$)",
            xaxis_title=""
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas principais
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric(
                "Receita Bruta Anual",
                f"R$ {receita_bruta/1_000_000:.2f}M"
            )
        
        with col_m2:
            st.metric(
                "Custos Totais",
                f"R$ {custos_totais/1_000_000:.2f}M"
            )
        
        with col_m3:
            delta_color = "normal" if resultado_liquido > 0 else "inverse"
            st.metric(
                "Resultado Líquido",
                f"R$ {resultado_liquido/1_000_000:.2f}M",
                f"{margem_liquida:.1f}% margem",
                delta_color=delta_color
            )
        
        # Análise de viabilidade
        st.markdown("---")
        st.markdown("### 💡 Análise de Viabilidade")
        
        if resultado_liquido < 0:
            st.markdown(f"""
            <div class="error-box">
            <h4>🚨 ESTRUTURA INVIÁVEL</h4>
            <p>Com um PL de <strong>R$ {pl_alvo:.0f} milhões</strong>, o FIDC apresenta 
            <strong>prejuízo de R$ {abs(resultado_liquido/1_000_000):.2f} milhões</strong> por ano.</p>
            <p>Os custos fixos regulatórios (auditoria, rating, CVM) representam uma barreira 
            significativa para fundos pequenos.</p>
            <p><strong>Recomendação:</strong> Considere entrar como cotista em um FIDC multi-cedente 
            existente ou aumente o tamanho da estrutura para diluir os custos fixos.</p>
            </div>
            """, unsafe_allow_html=True)
        elif margem_liquida < 5:
            st.markdown(f"""
            <div class="warning-box">
            <h4>⚠️ MARGEM APERTADA</h4>
            <p>A estrutura é tecnicamente viável, mas a margem líquida de 
            <strong>{margem_liquida:.1f}%</strong> é muito baixa.</p>
            <p>Qualquer aumento de custos ou inadimplência pode tornar o fundo deficitário.</p>
            <p><strong>Recomendação:</strong> Aumente o PL para pelo menos R$ {pl_alvo * 1.5:.0f} milhões 
            ou busque ativos com yield mais elevado.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="success-box">
            <h4>✅ ESTRUTURA VIÁVEL</h4>
            <p>Com margem líquida de <strong>{margem_liquida:.1f}%</strong>, esta estrutura 
            apresenta viabilidade econômica adequada.</p>
            <p>O tamanho do fundo permite diluir os custos fixos de forma satisfatória.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Análise de sensibilidade
    st.markdown("---")
    st.markdown("## 🎯 Análise de Sensibilidade: Encontrando o Breakeven")
    
    st.write("""
    O gráfico abaixo mostra como a margem líquida varia com diferentes tamanhos de PL, 
    mantendo os demais parâmetros constantes. Identifique o **ponto de equilíbrio** onde a estrutura 
    começa a ser viável.
    """)
    
    # Calcular cenários
    pls_simulacao = list(range(5, 105, 5))
    resultados_simulacao = []
    
    for pl_sim in pls_simulacao:
        receita_sim = pl_sim * 1_000_000 * yield_carteira / 100
        custo_var_sim = pl_sim * 1_000_000 * (taxa_gestao + taxa_administracao) / 100
        resultado_sim = receita_sim - custos_fixos_total - custo_var_sim
        margem_sim = (resultado_sim / receita_sim * 100) if receita_sim > 0 else -100
        
        resultados_simulacao.append({
            'PL (R$ milhões)': pl_sim,
            'Margem Líquida (%)': margem_sim,
            'Resultado (R$ milhões)': resultado_sim / 1_000_000
        })
    
    df_sensibilidade = pd.DataFrame(resultados_simulacao)
    
    # Encontrar breakeven
    df_positivo = df_sensibilidade[df_sensibilidade['Margem Líquida (%)'] > 0]
    pl_breakeven = df_positivo['PL (R$ milhões)'].min() if len(df_positivo) > 0 else None
    
    # Gráfico de sensibilidade
    fig2 = go.Figure()
    
    # Linha de margem
    fig2.add_trace(go.Scatter(
        x=df_sensibilidade['PL (R$ milhões)'],
        y=df_sensibilidade['Margem Líquida (%)'],
        mode='lines+markers',
        name='Margem Líquida',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Linha de breakeven (margem = 0)
    fig2.add_hline(
        y=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Breakeven (Margem = 0%)",
        annotation_position="right"
    )
    
    # Destacar o PL atual
    margem_atual = df_sensibilidade[df_sensibilidade['PL (R$ milhões)'] == pl_alvo]['Margem Líquida (%)'].values[0]
    fig2.add_trace(go.Scatter(
        x=[pl_alvo],
        y=[margem_atual],
        mode='markers',
        name='PL Atual',
        marker=dict(size=15, color='red', symbol='star')
    ))
    
    if pl_breakeven:
        fig2.add_vline(
            x=pl_breakeven,
            line_dash="dot",
            line_color="green",
            annotation_text=f"Breakeven: R$ {pl_breakeven:.0f}M",
            annotation_position="top"
        )
    
    fig2.update_layout(
        title="Sensibilidade da Margem Líquida ao Tamanho do PL",
        xaxis_title="Patrimônio Líquido (R$ milhões)",
        yaxis_title="Margem Líquida (%)",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    if pl_breakeven:
        st.info(f"""
        📍 **Ponto de Equilíbrio Identificado:** R$ {pl_breakeven:.0f} milhões
        
        Este é o tamanho mínimo de PL necessário para que a estrutura não opere com prejuízo, 
        considerando os parâmetros atuais de yield ({yield_carteira:.1f}% a.a.) e estrutura de custos.
        
        **Importante:** Na prática, recomenda-se operar com margem de segurança de pelo menos 5% 
        para absorver variações e imprevistos.
        """)
    else:
        st.warning("⚠️ Nenhum ponto de equilíbrio encontrado no range simulado. A estrutura pode ser inviável.")
    
    # Tabela de decomposição de custos
    st.markdown("---")
    st.markdown("### 📋 Decomposição Detalhada de Custos")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("#### Custos Fixos Anuais")
        df_fixos = pd.DataFrame({
            'Item': [
                'Auditoria Externa',
                'Rating',
                'Taxa CVM + Anbima',
                'Setup Jurídico (amortizado)',
                'Outros Custos Fixos'
            ],
            'Valor (R$ mil)': [
                custo_auditoria,
                custo_rating,
                custo_cvm_anbima,
                custo_setup_juridico / 3,
                custo_outros
            ]
        })
        df_fixos['% do Total Fixo'] = (df_fixos['Valor (R$ mil)'] / df_fixos['Valor (R$ mil)'].sum() * 100).round(1)
        st.dataframe(df_fixos, hide_index=True)
        st.metric("Total Fixo", f"R$ {custos_fixos_total/1_000:.0f} mil/ano")
    
    with col_t2:
        st.markdown("#### Custos Variáveis Anuais")
        df_variaveis = pd.DataFrame({
            'Item': [
                f'Taxa de Gestão ({taxa_gestao:.1f}% a.a.)',
                f'Taxa de Administração ({taxa_administracao:.2f}% a.a.)'
            ],
            'Valor (R$ mil)': [
                custo_gestao / 1_000,
                custo_admin / 1_000
            ]
        })
        df_variaveis['% do PL'] = [taxa_gestao, taxa_administracao]
        st.dataframe(df_variaveis, hide_index=True)
        st.metric("Total Variável", f"R$ {custos_variaveis_total/1_000:.0f} mil/ano")
    
    # Insights pedagógicos
    st.markdown("---")
    st.markdown("### 🎓 Conceitos-Chave")
    
    with st.expander("📚 Por que FIDCs pequenos são desafiadores?"):
        st.write("""
        **Custos Fixos Indivisíveis:**
        
        Independentemente do tamanho do fundo, certos custos regulatórios são obrigatórios:
        - Auditoria externa anual (exigência CVM)
        - Rating (obrigatório para acesso ao varejo)
        - Taxas de fiscalização (CVM e Anbima)
        - Estruturação jurídica
        
        Para um FIDC de R$ 10 milhões, esses custos podem representar 2-3% do PL.
        Para um FIDC de R$ 100 milhões, representam apenas 0,2-0,3% do PL.
        
        **Economia de Escala:**
        
        FIDCs maiores conseguem diluir os custos fixos entre mais cotistas, tornando a 
        estrutura mais eficiente. Por isso, a consolidação via FIDCs multi-cedentes 
        tem crescido no mercado.
        """)
    
    with st.expander("💼 Alternativas para Estruturas Pequenas"):
        st.write("""
        Se sua operação não atinge o ponto de equilíbrio:
        
        1. **FIDC Multi-cedente:** Entre como cedente em um fundo existente que já possui 
           a estrutura montada. Você compartilha os custos fixos com outros cedentes.
        
        2. **Cessão Direta:** Para volumes muito pequenos, considere a cessão direta de 
           recebíveis para bancos ou securitizadoras.
        
        3. **Aguarde Crescimento:** Acumule recebíveis até atingir massa crítica para 
           estruturar um FIDC próprio de forma viável.
        
        4. **Consórcio de Cedentes:** Agrupe-se com outras empresas de perfil similar 
           para criar um FIDC compartilhado desde o início.
        """)
