import streamlit as st
import graphviz

def run():
    st.title("🏗️ Módulo 2: Arquiteto de Classes")
    st.markdown("### Entendendo a Segregação Patrimonial (Resolução CVM 175/2022)")
    
    st.markdown("""
    A **Resolução CVM 175/2022** trouxe uma das mudanças mais significativas na estrutura 
    dos FIDCs: a possibilidade de criar **múltiplas classes** dentro de um único CNPJ, 
    cada uma com **patrimônio segregado**.
    """)
    
    # Explicação conceitual
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📖 Conceitos Fundamentais")
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **CLASSE:**
        - Patrimônio completamente segregado
        - Ativos e passivos independentes
        - Tipos diferentes de recebíveis
        - "Blindagem" entre classes
        
        **SUBCLASSE:**
        - Divisão dentro de uma classe
        - Compartilham o mesmo patrimônio
        - Diferença está na **subordinação**
        - Exemplo: Sênior vs. Júnior
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🆚 Antes vs. Depois da CVM 175")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("""
        **ANTES (CVM 356):**
        - 1 CNPJ = 1 tipo de ativo
        - Para diversificar: múltiplos CNPJs
        - Gestão fragmentada
        - Custos multiplicados
        
        **DEPOIS (CVM 175):**
        - 1 CNPJ = várias classes
        - Segregação patrimonial automática
        - Gestão centralizada
        - Economia de escala
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Construtor interativo
    st.markdown("## 🎨 Monte seu FIDC Personalizado")
    
    st.write("""
    Use os controles abaixo para construir a estrutura do seu FIDC. O diagrama será 
    atualizado automaticamente mostrando a hierarquia de classes e subclasses.
    """)
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.markdown("### 📦 Classes de Ativos")
        
        # Nome do fundo
        nome_fundo = st.text_input(
            "Nome do FIDC",
            value="FIDC Exemplo S.A.",
            help="Nome fantasia do fundo"
        )
        
        cnpj_raiz = st.text_input(
            "CNPJ do Fundo",
            value="12.345.678/0001-90",
            help="CNPJ único registrado na CVM"
        )
        
        st.markdown("#### Adicionar Classes:")
        
        classe_corporativo = st.checkbox(
            "✅ Classe de Crédito Corporativo",
            value=True,
            help="Recebíveis de empresas (duplicatas, cheques, contratos)"
        )
        
        classe_cartao = st.checkbox(
            "💳 Classe de Cartão de Crédito",
            value=False,
            help="Recebíveis de cartão de crédito (bandeiras)"
        )
        
        classe_agro = st.checkbox(
            "🌾 Classe de Crédito Agrícola",
            value=False,
            help="CPR, LCA, recebíveis do agronegócio"
        )
        
        classe_imobiliario = st.checkbox(
            "🏠 Classe de Crédito Imobiliário",
            value=False,
            help="CCB imobiliários, CRI, financiamentos"
        )
        
        classe_veiculos = st.checkbox(
            "🚗 Classe de Financiamento de Veículos",
            value=False,
            help="CDC de veículos, leasing"
        )
        
        classe_consignado = st.checkbox(
            "👔 Classe de Crédito Consignado",
            value=False,
            help="Empréstimos consignados (INSS, servidores)"
        )
    
    with col_config2:
        st.markdown("### 🎯 Configuração de Subclasses")
        
        st.info("""
        **Subclasses** representam diferentes níveis de risco dentro da mesma classe.
        
        - **Sênior:** Recebe pagamentos primeiro, menor risco
        - **Mezanino:** Risco intermediário (opcional)
        - **Subordinada (Júnior):** Absorve perdas primeiro, maior risco
        """)
        
        # Configuração de subordinação
        usar_mezanino = st.checkbox(
            "Incluir Subclasse Mezanino",
            value=False,
            help="Adiciona uma camada intermediária de risco"
        )
        
        # Mostrar índices de subordinação se houver classes
        classes_ativas = []
        if classe_corporativo:
            classes_ativas.append("Corporativo")
        if classe_cartao:
            classes_ativas.append("Cartão")
        if classe_agro:
            classes_ativas.append("Agrícola")
        if classe_imobiliario:
            classes_ativas.append("Imobiliário")
        if classe_veiculos:
            classes_ativas.append("Veículos")
        if classe_consignado:
            classes_ativas.append("Consignado")
        
        if len(classes_ativas) > 0:
            st.markdown("#### Índices de Subordinação:")
            subordinacao_config = {}
            
            for classe in classes_ativas:
                subordinacao_config[classe] = st.slider(
                    f"Subordinação {classe} (%)",
                    min_value=10,
                    max_value=50,
                    value=20,
                    step=5,
                    help=f"Percentual de cotas subordinadas na classe {classe}"
                )
    
    # Criar o diagrama
    st.markdown("---")
    st.markdown("## 🗺️ Estrutura Hierárquica do FIDC")
    
    if len(classes_ativas) == 0:
        st.warning("⚠️ Selecione pelo menos uma classe de ativos para visualizar a estrutura.")
    else:
        # Criar diagrama usando Graphviz
        dot = graphviz.Digraph(comment='Estrutura FIDC')
        dot.attr(rankdir='TB', splines='ortho')
        dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
        
        # Nó raiz (Fundo)
        dot.node('raiz', f'{nome_fundo}\nCNPJ: {cnpj_raiz}', 
                fillcolor='#1f77b4', fontcolor='white', penwidth='3')
        
        # Definir cores para as classes
        cores_classes = {
            'Corporativo': '#ff7f0e',
            'Cartão': '#2ca02c',
            'Agrícola': '#d62728',
            'Imobiliário': '#9467bd',
            'Veículos': '#8c564b',
            'Consignado': '#e377c2'
        }
        
        # Adicionar classes
        for i, classe in enumerate(classes_ativas):
            classe_id = f'classe_{i}'
            cor_classe = cores_classes.get(classe, '#bcbd22')
            
            dot.node(classe_id, f'CLASSE {i+1}\n{classe}\n(Patrimônio Segregado)', 
                    fillcolor=cor_classe, fontcolor='white', penwidth='2')
            dot.edge('raiz', classe_id, penwidth='2')
            
            # Adicionar subclasses
            subordinacao = subordinacao_config.get(classe, 20)
            senior_pct = 100 - subordinacao
            
            # Subclasse Sênior
            senior_id = f'senior_{i}'
            dot.node(senior_id, f'Subclasse SÊNIOR\n{senior_pct}% do patrimônio\nMenor risco', 
                    fillcolor='#51cf66', fontcolor='black', shape='box')
            dot.edge(classe_id, senior_id, label='prioridade 1°', penwidth='1.5')
            
            # Subclasse Mezanino (se habilitada)
            if usar_mezanino:
                mezanino_pct = subordinacao / 2
                mezanino_id = f'mezanino_{i}'
                dot.node(mezanino_id, f'Subclasse MEZANINO\n{mezanino_pct:.0f}% do patrimônio\nRisco médio', 
                        fillcolor='#ffd43b', fontcolor='black', shape='box')
                dot.edge(classe_id, mezanino_id, label='prioridade 2°', penwidth='1.5')
            
            # Subclasse Subordinada
            junior_pct = subordinacao if not usar_mezanino else subordinacao / 2
            junior_id = f'junior_{i}'
            prioridade_junior = '3°' if usar_mezanino else '2°'
            dot.node(junior_id, f'Subclasse SUBORDINADA\n{junior_pct:.0f}% do patrimônio\nMaior risco', 
                    fillcolor='#ff6b6b', fontcolor='white', shape='box')
            dot.edge(classe_id, junior_id, label=f'prioridade {prioridade_junior}', penwidth='1.5')
        
        # Renderizar o diagrama
        st.graphviz_chart(dot)
        
        # Explicação da estrutura criada
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"""
        ### ✅ Estrutura Criada com Sucesso!
        
        **Seu FIDC possui:**
        - **1 CNPJ único:** {cnpj_raiz}
        - **{len(classes_ativas)} classe(s) segregada(s):** {', '.join(classes_ativas)}
        - **Subclasses por classe:** {'Sênior, Mezanino e Subordinada' if usar_mezanino else 'Sênior e Subordinada'}
        
        **Vantagens desta estrutura:**
        1. ✅ Um único relatório consolidado para a CVM
        2. ✅ Redução de custos administrativos
        3. ✅ Flexibilidade para adicionar/remover classes
        4. ✅ Patrimônios blindados entre classes (sem contaminação)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção comparativa
    st.markdown("---")
    st.markdown("## 🔍 Entendendo a Blindagem Patrimonial")
    
    col_blindagem1, col_blindagem2 = st.columns(2)
    
    with col_blindagem1:
        st.markdown("### ❌ Sem Segregação (Risco)")
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown("""
        **Cenário:** Todas as classes em um único patrimônio
        
        ```
        FIDC Único
        ├── Cartão de Crédito: R$ 50M
        └── Crédito Imobiliário: R$ 50M
        ```
        
        **Problema:**
        - Inadimplência no cartão: -R$ 20M
        - **CONTAMINA o imobiliário!**
        - Ambas as carteiras prejudicadas
        - Cotistas de imóveis sofrem por culpa do cartão
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_blindagem2:
        st.markdown("### ✅ Com Segregação (Proteção)")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("""
        **Cenário:** Classes segregadas (CVM 175)
        
        ```
        FIDC com Classes
        ├── CLASSE A (Cartão): R$ 50M
        └── CLASSE B (Imobiliário): R$ 50M
        ```
        
        **Proteção:**
        - Inadimplência no cartão: -R$ 20M
        - **NÃO AFETA o imobiliário!**
        - Patrimônios independentes
        - Cotistas de imóveis protegidos
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Casos de uso
    st.markdown("---")
    st.markdown("## 💼 Casos de Uso Práticos")
    
    casos = {
        "Varejista Multi-Segmento": {
            "Situação": "Empresa com operações de varejo físico e e-commerce",
            "Classes Sugeridas": [
                "Classe A: Recebíveis de cartão (lojas físicas)",
                "Classe B: Recebíveis de e-commerce (marketplace)"
            ],
            "Benefício": "Permite tratar cada canal com política de crédito específica"
        },
        "Banco Regional": {
            "Situação": "Banco com múltiplas linhas de crédito",
            "Classes Sugeridas": [
                "Classe A: CDC Veículos",
                "Classe B: Crédito Consignado",
                "Classe C: Capital de Giro Empresas"
            ],
            "Benefício": "Atende diferentes perfis de investidores com um único fundo"
        },
        "Fintech de Crédito": {
            "Situação": "Startup que opera em nicho específico mas quer expandir",
            "Classes Sugeridas": [
                "Classe A: Produto atual consolidado (menor risco)",
                "Classe B: Novos produtos em teste (maior risco)"
            ],
            "Benefício": "Flexibilidade para inovar sem contaminar carteira principal"
        }
    }
    
    caso_selecionado = st.selectbox(
        "Selecione um caso de uso:",
        list(casos.keys())
    )
    
    caso = casos[caso_selecionado]
    
    st.markdown(f"### 📋 {caso_selecionado}")
    
    col_caso1, col_caso2 = st.columns([1, 1])
    
    with col_caso1:
        st.markdown("**Situação:**")
        st.write(caso["Situação"])
        
        st.markdown("**Classes Sugeridas:**")
        for classe in caso["Classes Sugeridas"]:
            st.write(f"- {classe}")
    
    with col_caso2:
        st.markdown("**Benefício Principal:**")
        st.info(caso["Benefício"])
    
    # Conceitos pedagógicos
    st.markdown("---")
    st.markdown("### 🎓 Conceitos-Chave")
    
    with st.expander("📚 Por que a segregação patrimonial é revolucionária?"):
        st.write("""
        **Contexto Histórico:**
        
        Antes da CVM 175, empresas que queriam securitizar diferentes tipos de recebíveis 
        precisavam criar múltiplos FIDCs, cada um com:
        - CNPJ próprio
        - Auditoria separada
        - Rating individual
        - Assembleia de cotistas própria
        - Custos administrativos multiplicados
        
        **Mudança de Paradigma:**
        
        A segregação patrimonial permite que um único FIDC opere como um "condomínio de carteiras", 
        onde cada classe é uma "torre" independente com:
        - Ativos e passivos próprios
        - Performance isolada
        - Política de investimento específica
        - Mas compartilhando: gestão, custódia, auditoria, registro CVM
        
        **Analogia:**
        
        Pense em um shopping center (CNPJ único) com diferentes lojas (classes). 
        Se uma loja falir, não afeta as outras. Mas todas compartilham segurança, 
        limpeza e administração central.
        """)
    
    with st.expander("⚖️ Diferença entre Classe e Subclasse"):
        st.write("""
        **CLASSE = Tipo de Ativo (Segregação Patrimonial)**
        - Carteiras completamente diferentes
        - Exemplos: Cartão vs. Imobiliário vs. Veículos
        - Patrimônios não se comunicam
        - Inadimplência em uma não afeta outra
        
        **SUBCLASSE = Nível de Risco (Subordinação)**
        - Mesma carteira de ativos
        - Exemplos: Sênior vs. Júnior
        - Compartilham o patrimônio da classe
        - Diferença está na ordem de pagamento (waterfall)
        
        **Exemplo Prático:**
        ```
        FIDC XYZ
        │
        ├── CLASSE A (Cartão de Crédito) ← Patrimônio segregado
        │   ├── Subclasse Sênior (80%) ← Mesma carteira, prioridade 1°
        │   └── Subclasse Júnior (20%) ← Mesma carteira, prioridade 2°
        │
        └── CLASSE B (Veículos) ← Outro patrimônio segregado
            ├── Subclasse Sênior (70%) ← Carteira diferente, prioridade 1°
            └── Subclasse Júnior (30%) ← Carteira diferente, prioridade 2°
        ```
        """)
    
    with st.expander("🚀 Impacto da CVM 175 no Mercado"):
        st.write("""
        A flexibilização trazida pela Resolução 175 tem impulsionado:
        
        **1. Crescimento de FIDCs Multi-Cedentes:**
        - Pequenas empresas agora conseguem participar de estruturas robustas
        - Custos compartilhados entre múltiplos originadores
        - Classes dedicadas para cada cedente
        
        **2. Produtos Mais Sofisticados:**
        - FIDCs que oferecem diferentes perfis de risco/retorno
        - Melhor casamento entre apetite do investidor e carteira
        - Estruturas que "crescem" conforme demanda
        
        **3. Redução de Custos:**
        - Eliminação de redundâncias administrativas
        - Uma única auditoria para múltiplas classes
        - Economia pode chegar a 30-40% em estruturas complexas
        
        **4. Maior Acessibilidade:**
        - Empresas médias conseguem estruturar FIDCs viáveis
        - Barreira de entrada reduzida
        - Democratização do mercado de capitais
        """)
