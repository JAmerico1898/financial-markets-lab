import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def run():
    st.title("✅ Módulo 4: Checklist Regulatório Inteligente")
    st.markdown("### Navegando pelas Regras de Registro na CVM")
    
    st.markdown("""
    O processo de registro de um FIDC na CVM possui **requisitos específicos** que variam conforme:
    - O **público-alvo** (investidores profissionais vs. varejo)
    - A **padronização dos ativos** (padronizados vs. não-padronizados)
    - O **tipo de registro** (automático vs. análise prévia)
    
    Este módulo te guiará pelas regras e identificará o caminho mais adequado para sua estrutura.
    """)
    
    st.markdown("---")
    
    # Seção 1: Definições básicas
    st.markdown("## 📋 Etapa 1: Defina o Perfil da Estrutura")
    
    col_def1, col_def2 = st.columns(2)
    
    with col_def1:
        st.markdown("### 👥 Público-Alvo")
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Investidor Profissional:**
        - Possui mais de R$ 10 milhões em investimentos
        - Instituições financeiras, fundos de pensão, seguradoras
        - Assina termo de profissionalidade
        - **Vantagem:** Menos restrições regulatórias
        
        **Investidor de Varejo:**
        - Investidor qualificado (>R$ 1 milhão) ou público geral
        - Pessoa física, pequenas empresas
        - **Restrições:** Mais exigências para proteção
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        publico_alvo = st.radio(
            "Qual será o público-alvo do FIDC?",
            ["Investidores Profissionais", "Investidores de Varejo"],
            help="Esta escolha afeta significativamente os requisitos"
        )
    
    with col_def2:
        st.markdown("### 📄 Tipo de Ativo")
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Direitos Creditórios Padronizados (DCP):**
        - Características homogêneas e previsíveis
        - Exemplos: cartão de crédito, consignado, aluguel
        - Histórico estatístico robusto
        - **Vantagem:** Acesso ao varejo facilitado
        
        **Direitos Creditórios Não-Padronizados (DCNP):**
        - Características heterogêneas ou únicas
        - Exemplos: contratos corporativos específicos, duplicatas
        - Análise caso a caso
        - **Restrição:** Vedado para varejo
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        tipo_ativo = st.radio(
            "Qual o tipo de ativo do FIDC?",
            ["Direitos Creditórios Padronizados (DCP)", 
             "Direitos Creditórios Não-Padronizados (DCNP)"],
            help="Determina elegibilidade para varejo"
        )
    
    # Validação da combinação
    st.markdown("---")
    st.markdown("## 🔍 Etapa 2: Validação de Elegibilidade")
    
    # Lógica de validação
    eh_varejo = publico_alvo == "Investidores de Varejo"
    eh_nao_padronizado = tipo_ativo == "Direitos Creditórios Não-Padronizados (DCNP)"
    
    if eh_varejo and eh_nao_padronizado:
        # Combinação proibida
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown("""
        ### ❌ COMBINAÇÃO PROIBIDA PELA CVM 175
        
        **Ativos Não-Padronizados** não podem ser oferecidos ao **público de varejo**.
        
        **Fundamento Legal:**
        A Resolução CVM 175/2022 estabelece que FIDCs com ativos não-padronizados 
        são destinados **exclusivamente a investidores profissionais**.
        
        **Suas Opções:**
        1. **Alterar o público-alvo** para Investidores Profissionais
        2. **Alterar os ativos** para Direitos Creditórios Padronizados
        3. **Estruturar um FIDC Multi-classe** com DCP separados para varejo
        
        **Por que essa restrição existe?**
        Ativos não-padronizados exigem análise sofisticada de risco que a CVM considera 
        inadequada para investidores de varejo, mesmo que qualificados.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.stop()  # Interrompe a execução se combinação inválida
    
    else:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"""
        ### ✅ Combinação Válida
        
        - **Público:** {publico_alvo}
        - **Ativos:** {tipo_ativo.split('(')[0].strip()}
        
        Esta estrutura está em conformidade com a CVM 175. Prossiga para o checklist detalhado.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção 3: Checklist detalhado para varejo
    if eh_varejo:
        st.markdown("---")
        st.markdown("## 📝 Etapa 3: Checklist Obrigatório para Acesso ao Varejo")
        
        st.write("""
        Para oferecer cotas de FIDC ao público de varejo, você deve cumprir **todos** os requisitos abaixo.
        Marque cada item conforme implementado em sua estrutura.
        """)
        
        st.markdown("### 🎯 Requisitos Obrigatórios")
        
        # Rating
        col_check1, col_check2 = st.columns([3, 1])
        with col_check1:
            st.markdown("#### 1. Rating Contratado")
            st.write("""
            Agência de rating registrada na CVM deve atribuir classificação de risco 
            às cotas sênior destinadas ao varejo. Rating mínimo recomendado: **A** ou superior.
            """)
        with col_check2:
            rating_ok = st.checkbox("✓ Contratado", key="rating", value=False)
        
        if rating_ok:
            rating_agencia = st.selectbox(
                "Agência de Rating",
                ["Fitch Ratings", "Moody's", "S&P Global", "Austin Rating", "Liberum Ratings"],
                help="Selecione a agência contratada"
            )
            rating_nota = st.selectbox(
                "Rating Atribuído",
                ["AAA(bra)", "AA+(bra)", "AA(bra)", "AA-(bra)", 
                 "A+(bra)", "A(bra)", "A-(bra)", 
                 "BBB+(bra)", "BBB(bra)", "BBB-(bra)"],
                index=5,  # A(bra) como padrão
                help="Rating na escala nacional brasileira"
            )
            
            # Avaliar se rating é adequado
            ratings_aceitaveis = ["AAA(bra)", "AA+(bra)", "AA(bra)", "AA-(bra)", "A+(bra)", "A(bra)"]
            if rating_nota in ratings_aceitaveis:
                st.success(f"✅ Rating {rating_nota} é adequado para varejo.")
            else:
                st.warning(f"⚠️ Rating {rating_nota} pode dificultar a distribuição no varejo.")
        
        st.markdown("---")
        
        # Cota Sênior
        col_check3, col_check4 = st.columns([3, 1])
        with col_check3:
            st.markdown("#### 2. Oferta Restrita a Cotas Sênior")
            st.write("""
            Apenas cotas com **primeira prioridade de pagamento** (sênior) podem ser 
            distribuídas ao público de varejo. Cotas subordinadas são vedadas.
            """)
        with col_check4:
            senior_ok = st.checkbox("✓ Apenas Sênior", key="senior", value=False)
        
        if senior_ok:
            subordinacao_varejo = st.slider(
                "Índice de Subordinação (%)",
                min_value=10,
                max_value=50,
                value=20,
                step=5,
                help="Percentual de cotas subordinadas que protegem a sênior"
            )
            st.info(f"📊 Com {subordinacao_varejo}% de subordinação, as cotas sênior ({100-subordinacao_varejo}%) têm proteção adequada.")
        
        st.markdown("---")
        
        # Liquidez
        col_check5, col_check6 = st.columns([3, 1])
        with col_check5:
            st.markdown("#### 3. Prazo Médio de Vencimento")
            st.write("""
            A carteira deve ter prazo médio de vencimento de até **365 dias** para 
            fundos abertos ou **até 5 anos** para fundos fechados destinados ao varejo.
            """)
        with col_check6:
            liquidez_ok = st.checkbox("✓ Dentro do Prazo", key="liquidez", value=False)
        
        if liquidez_ok:
            tipo_fundo_varejo = st.radio(
                "Tipo de Fundo",
                ["Aberto (resgate a qualquer tempo)", "Fechado (prazo determinado)"],
                help="Afeta requisitos de liquidez"
            )
            
            if tipo_fundo_varejo == "Aberto (resgate a qualquer tempo)":
                prazo_medio = st.slider(
                    "Prazo Médio de Vencimento da Carteira (dias)",
                    min_value=30,
                    max_value=365,
                    value=180,
                    step=5
                )
                
                if prazo_medio <= 365:
                    st.success(f"✅ Prazo de {prazo_medio} dias está dentro do limite para fundos abertos.")
                else:
                    st.error(f"❌ Prazo de {prazo_medio} dias excede o limite de 365 dias para fundos abertos.")
            else:
                prazo_medio_anos = st.slider(
                    "Prazo Médio de Vencimento da Carteira (anos)",
                    min_value=1.0,
                    max_value=5.0,
                    value=3.0,
                    step=0.5
                )
                
                if prazo_medio_anos <= 5.0:
                    st.success(f"✅ Prazo de {prazo_medio_anos} anos está dentro do limite para fundos fechados.")
                else:
                    st.error(f"❌ Prazo de {prazo_medio_anos} anos excede o limite de 5 anos para fundos fechados.")
        
        st.markdown("---")
        
        # Diversificação
        col_check7, col_check8 = st.columns([3, 1])
        with col_check7:
            st.markdown("#### 4. Diversificação da Carteira")
            st.write("""
            Limites de concentração devem ser respeitados para mitigar risco de crédito:
            - Máximo 20% do PL em um único devedor (pessoas jurídicas)
            - Para pessoas físicas, limite agregado por faixa de renda
            """)
        with col_check8:
            diversificacao_ok = st.checkbox("✓ Diversificada", key="diversificacao", value=False)
        
        if diversificacao_ok:
            maior_exposicao = st.slider(
                "Maior Exposição a um Único Devedor (% do PL)",
                min_value=1,
                max_value=25,
                value=10,
                step=1
            )
            
            if maior_exposicao <= 20:
                st.success(f"✅ Exposição de {maior_exposicao}% respeita o limite de 20%.")
            else:
                st.warning(f"⚠️ Exposição de {maior_exposicao}% excede o limite regulatório de 20%.")
        
        st.markdown("---")
        
        # Transparência
        col_check9, col_check10 = st.columns([3, 1])
        with col_check9:
            st.markdown("#### 5. Regime de Informações Periódicas")
            st.write("""
            Demonstrações financeiras auditadas anuais e relatórios gerenciais mensais 
            devem ser disponibilizados aos cotistas e ao mercado.
            """)
        with col_check10:
            info_ok = st.checkbox("✓ Implementado", key="info", value=False)
        
        st.markdown("---")
        
        # Distribuição
        col_check11, col_check12 = st.columns([3, 1])
        with col_check11:
            st.markdown("#### 6. Distribuição por Instituição Habilitada")
            st.write("""
            As cotas devem ser distribuídas por intermediário autorizado pela CVM 
            (corretoras, distribuidoras, bancos de investimento).
            """)
        with col_check12:
            distribuidor_ok = st.checkbox("✓ Contratado", key="distribuidor", value=False)
        
        if distribuidor_ok:
            distribuidor_nome = st.text_input(
                "Nome do Distribuidor",
                placeholder="Ex: XP Investimentos, BTG Pactual, etc."
            )
        
        # Análise de Conformidade
        st.markdown("---")
        st.markdown("## 📊 Análise de Conformidade")
        
        requisitos_atendidos = sum([
            rating_ok, senior_ok, liquidez_ok, 
            diversificacao_ok, info_ok, distribuidor_ok
        ])
        total_requisitos = 6
        conformidade_pct = (requisitos_atendidos / total_requisitos) * 100
        
        col_conf1, col_conf2, col_conf3 = st.columns(3)
        
        with col_conf1:
            st.metric("Requisitos Atendidos", f"{requisitos_atendidos}/{total_requisitos}")
        
        with col_conf2:
            st.metric("Conformidade", f"{conformidade_pct:.0f}%")
        
        with col_conf3:
            if conformidade_pct == 100:
                st.metric("Status", "✅ APROVADO")
            elif conformidade_pct >= 80:
                st.metric("Status", "⚠️ QUASE LÁ")
            else:
                st.metric("Status", "❌ PENDENTE")
        
        # Mensagem final
        if conformidade_pct == 100:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("""
            ### 🎉 Estrutura Completa para Varejo!
            
            Todos os requisitos foram atendidos. Sua estrutura está pronta para:
            1. Submeter o registro na CVM
            2. Iniciar o processo de distribuição
            3. Captar recursos do público de varejo
            
            **Próximos Passos:**
            - Finalizar documentação (Regulamento, Prospecto)
            - Protocolar via sistema CVMWeb
            - Aguardar análise (se registro ordinário) ou confirmação (se automático)
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown(f"""
            ### ⚠️ Estrutura Incompleta
            
            Ainda faltam **{total_requisitos - requisitos_atendidos} requisito(s)** para conformidade total.
            
            **Requisitos Pendentes:**
            """)
            if not rating_ok:
                st.write("- ❌ Contratar agência de rating")
            if not senior_ok:
                st.write("- ❌ Restringir oferta a cotas sênior")
            if not liquidez_ok:
                st.write("- ❌ Adequar prazo de vencimento")
            if not diversificacao_ok:
                st.write("- ❌ Garantir diversificação mínima")
            if not info_ok:
                st.write("- ❌ Implementar regime de transparência")
            if not distribuidor_ok:
                st.write("- ❌ Contratar distribuidor autorizado")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção 4: Definir tipo de registro
    st.markdown("---")
    st.markdown("## 🚦 Etapa 4: Tipo de Registro e Prazo Estimado")
    
    st.write("""
    A CVM oferece diferentes ritos de registro. O prazo e complexidade variam conforme 
    o tipo de estrutura e convênios firmados.
    """)
    
    # Perguntar sobre convênio ANBIMA
    convenio_anbima = st.radio(
        "O gestor e administrador possuem convênio com a ANBIMA?",
        ["Sim", "Não"],
        help="Convênio permite registro automático sem análise prévia da CVM"
    )
    
    # Determinar tipo de registro
    if eh_varejo:
        if convenio_anbima == "Sim":
            tipo_registro = "Registro Automático via Convênio ANBIMA"
            prazo_estimado = "3 a 4 meses"
            prazo_dias = 90
            cor_status = "success"
            explicacao = """
            **Registro Automático (CVM 175, Art. 16):**
            
            Por meio do convênio com a ANBIMA, o fundo é registrado automaticamente 
            após protocolo na CVM, desde que atenda todos os requisitos. Não há análise prévia.
            
            **Fluxo:**
            1. Protocolo via CVMWeb (dia 0)
            2. ANBIMA valida documentação (10 dias)
            3. CVM emite registro automático (20 dias)
            4. Início da distribuição (possível em ~30 dias)
            
            **Vantagens:**
            - Prazo previsível
            - Menor custo (sem taxa de análise)
            - Processo padronizado
            """
        else:
            tipo_registro = "Registro Ordinário com Análise CVM"
            prazo_estimado = "4 a 6 meses"
            prazo_dias = 150
            cor_status = "warning"
            explicacao = """
            **Registro Ordinário (CVM 175, Art. 15):**
            
            A CVM realiza análise detalhada da documentação antes de conceder o registro.
            Pode haver rodadas de perguntas e adequações.
            
            **Fluxo:**
            1. Protocolo via CVMWeb (dia 0)
            2. CVM inicia análise (15 dias para primeira manifestação)
            3. Rodada de perguntas (comum: 1-2 rodadas)
            4. Análise final e decisão (até 90 dias desde protocolo)
            5. Início da distribuição (após concessão)
            
            **Desafios:**
            - Prazo variável
            - Custos de análise
            - Possíveis adequações
            """
    else:  # Investidores Profissionais
        tipo_registro = "Registro Simplificado"
        prazo_estimado = "2 a 3 meses"
        prazo_dias = 60
        cor_status = "success"
        explicacao = """
        **Registro Simplificado para Profissionais:**
        
        FIDCs destinados exclusivamente a investidores profissionais têm 
        processo de registro mais ágil e com menos requisitos.
        
        **Fluxo:**
        1. Protocolo via CVMWeb (dia 0)
        2. Análise simplificada CVM (até 20 dias)
        3. Registro concedido (até 30 dias)
        4. Início da captação imediata
        
        **Vantagens:**
        - Menor burocracia
        - Dispensa rating
        - Maior flexibilidade na estrutura
        - Custos reduzidos
        """
    
    # Exibir resultado
    if cor_status == "success":
        st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warning-box">', unsafe_allow_html=True)
    
    st.markdown(f"""
    ### {tipo_registro}
    
    **Prazo Estimado:** {prazo_estimado}
    
    {explicacao}
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Timeline visual
    st.markdown("### 📅 Timeline Estimado")
    
    hoje = datetime.now()
    
    if eh_varejo and convenio_anbima == "Sim":
        marcos = [
            {"evento": "Protocolo CVMWeb", "dias": 0},
            {"evento": "Validação ANBIMA", "dias": 10},
            {"evento": "Registro Automático CVM", "dias": 30},
            {"evento": "Início Distribuição", "dias": 35},
            {"evento": "Captação Completa (est.)", "dias": 90}
        ]
    elif eh_varejo and convenio_anbima == "Não":
        marcos = [
            {"evento": "Protocolo CVMWeb", "dias": 0},
            {"evento": "1ª Manifestação CVM", "dias": 15},
            {"evento": "Rodada de Perguntas", "dias": 45},
            {"evento": "Análise Final", "dias": 90},
            {"evento": "Registro Concedido", "dias": 120},
            {"evento": "Início Distribuição", "dias": 125}
        ]
    else:
        marcos = [
            {"evento": "Protocolo CVMWeb", "dias": 0},
            {"evento": "Análise CVM", "dias": 10},
            {"evento": "Registro Concedido", "dias": 30},
            {"evento": "Início Captação", "dias": 32},
            {"evento": "Primeira Cessão", "dias": 60}
        ]
    
    df_timeline = pd.DataFrame(marcos)
    df_timeline['Data Estimada'] = df_timeline['dias'].apply(lambda x: (hoje + timedelta(days=x)).strftime('%d/%m/%Y'))
    
    st.dataframe(
        df_timeline[['Data Estimada', 'evento']].rename(columns={'evento': 'Marco'}),
        hide_index=True,
        use_container_width=True
    )
    
    # Gráfico de Gantt simplificado
    fig_timeline = go.Figure()
    
    for i, marco in enumerate(marcos):
        fig_timeline.add_trace(go.Scatter(
            x=[marco['dias']],
            y=[i],
            mode='markers+text',
            marker=dict(size=20, color='#1f77b4'),
            text=[marco['evento']],
            textposition='middle right',
            textfont=dict(size=10),
            hovertemplate=f"<b>{marco['evento']}</b><br>Dia {marco['dias']}<extra></extra>",
            showlegend=False
        ))
    
    fig_timeline.update_layout(
        title="Linha do Tempo do Processo de Registro",
        xaxis_title="Dias desde o Protocolo",
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        height=300,
        margin=dict(l=20, r=200, t=50, b=50)
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Custos estimados
    st.markdown("---")
    st.markdown("## 💰 Custos Estimados do Processo")
    
    col_custo1, col_custo2 = st.columns(2)
    
    with col_custo1:
        st.markdown("### Custos Fixos de Estruturação")
        
        custos_estruturacao = {
            "Assessoria Jurídica": 80000,
            "Regulamento e Prospecto": 30000,
            "Taxa de Registro CVM": 8000,
            "Due Diligence Inicial": 25000,
        }
        
        if eh_varejo:
            custos_estruturacao["Rating Inicial"] = 35000
            custos_estruturacao["Estudo de Viabilidade"] = 15000
        
        df_custos = pd.DataFrame({
            'Item': list(custos_estruturacao.keys()),
            'Valor (R$)': list(custos_estruturacao.values())
        })
        
        total_estruturacao = sum(custos_estruturacao.values())
        
        st.dataframe(df_custos, hide_index=True)
        st.metric("Total de Estruturação", f"R$ {total_estruturacao:,.0f}")
    
    with col_custo2:
        st.markdown("### Custos Recorrentes (Anuais)")
        
        custos_recorrentes = {
            "Administração (0.2% a.a.)": "% do PL",
            "Gestão (1.5% a.a.)": "% do PL",
            "Auditoria": "R$ 45.000",
            "Custódia": "R$ 20.000",
        }
        
        if eh_varejo:
            custos_recorrentes["Rating Anual"] = "R$ 35.000"
            custos_recorrentes["Distribuição (comissão)"] = "0.5-1% captado"
        
        st.write("**Custos Variáveis (sobre o PL):**")
        for item, valor in custos_recorrentes.items():
            st.write(f"- {item}: {valor}")
        
        st.info("""
        💡 **Exemplo para FIDC de R$ 50M:**
        - Administração: R$ 100k/ano
        - Gestão: R$ 750k/ano
        - Custos fixos: ~R$ 100k/ano
        - **Total:** ~R$ 950k/ano (~1.9% do PL)
        """)
    
    # Conceitos pedagógicos
    st.markdown("---")
    st.markdown("### 🎓 Conceitos-Chave")
    
    with st.expander("📚 Por que tantas exigências para o varejo?"):
        st.write("""
        **Filosofia Regulatória da CVM:**
        
        A CVM adota o princípio da **proteção assimétrica** - quanto menos sofisticado 
        o investidor, maior a proteção regulatória necessária.
        
        **Racional:**
        
        1. **Assimetria de Informação:** Investidores de varejo têm menos acesso a 
        análises profundas sobre qualidade de crédito dos ativos.
        
        2. **Capacidade de Absorção de Perdas:** Perdas em FIDC podem ser substanciais 
        e irreversíveis. Investidores de varejo têm menor capacidade de recuperação.
        
        3. **Histórico de Mercado:** FIDCs mal estruturados causaram prejuízos 
        significativos ao varejo no passado (ex: crise de 2008).
        
        4. **Alinhamento com Basel III:** Bancos e seguradoras têm requisitos de 
        capital mais baixos para investir em FIDCs bem classificados, incentivando 
        estruturas de qualidade.
        
        **Comparação Internacional:**
        
        - EUA: Apenas investidores acreditados (>US$ 1M em ativos) acessam CLOs
        - Europa: Regras similares em securitizações (EU 2402/2017)
        - Brasil: CVM 175 é considerada relativamente flexível internacionalmente
        """)
    
    with st.expander("⚖️ Diferenças entre Registro Automático vs. Ordinário"):
        st.write("""
        **Registro Automático (Convênio ANBIMA):**
        
        **Requisitos:**
        - Gestor e administrador certificados pela ANBIMA
        - Estrutura 100% padronizada (sem exceções)
        - Ativos homologados pela ANBIMA
        - Rating obrigatório de agência certificada
        
        **Vantagens:**
        - Prazo curto e previsível (~30 dias)
        - Sem rodadas de perguntas da CVM
        - Menor custo (não há taxa de análise)
        - Processo 100% digital
        
        **Limitações:**
        - Zero flexibilidade na estrutura
        - Não aceita inovações ou peculiaridades
        - Restrito a tipos de ativos pré-aprovados
        
        ---
        
        **Registro Ordinário (Análise CVM):**
        
        **Quando Necessário:**
        - Estruturas inovadoras ou complexas
        - Ativos não padronizados (mesmo para profissionais)
        - Cláusulas especiais no regulamento
        - Primeira oferta de gestores novos
        
        **Vantagens:**
        - Permite inovação e customização
        - CVM pode aprovar exceções fundamentadas
        - Aceita estruturas híbridas
        
        **Desafios:**
        - Prazo variável (60-180 dias)
        - Rodadas de perguntas (média 2 rodadas)
        - Custo maior (taxa + honorários advocatícios)
        - Risco de exigências não previstas
        
        **Dica Prática:**
        
        Se sua estrutura é simples e se enquadra nos padrões ANBIMA, escolha o registro 
        automático. Só vá para o ordinário se realmente precisar de flexibilidade.
        """)
    
    with st.expander("🚀 Tendências Pós-CVM 175"):
        st.write("""
        A Resolução 175 tem impulsionado mudanças significativas no mercado:
        
        **1. Democratização do Acesso**
        - Antes: FIDCs eram essencialmente wholesale (institucionais)
        - Depois: Crescimento de 400% na oferta para varejo (2022-2024)
        - Plataformas digitais facilitam distribuição
        
        **2. Inovação em Estruturas**
        - FIDCs de precatórios
        - FIDCs de royalties (propriedade intelectual)
        - FIDCs verdes (financiamento sustentável)
        - FIDCs tokenizados (blockchain)
        
        **3. Competição com Renda Fixa**
        - FIDCs competem com CDBs, LCIs, LCAs
        - Spread atrativo vs. Tesouro Direto
        - Diversificação de portfólio
        
        **4. Consolidação via Multi-Cedentes**
        - Pequenas empresas se unem em FIDCs compartilhados
        - Redução de custos por economia de escala
        - Aumento de liquidez secundária
        
        **5. Regulação Tecnológica**
        - CVM estuda permitir smart contracts
        - Integração com Open Banking
        - Cessão digital de recebíveis (Lemon, Pipefy, etc.)
        
        **Expectativa para 2025-2030:**
        
        - Mercado pode triplicar de tamanho
        - FIDCs retail se tornarão mainstream
        - Maior integração com fintechs
        - Regulação se adaptará à tokenização
        """)
