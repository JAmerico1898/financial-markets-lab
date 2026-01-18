"""
Módulo 02 - Modelagem de Risco de Crédito
Laboratório de Mercado Financeiro
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# CONSTANTES E CONFIGURAÇÕES
# =============================================================================

# Dicionário de variáveis e suas descrições
variable_descriptions = {
    'unnamed:0': 'Index',
    'id': 'Identificação da operação de crédito',
    'acc_open_past_24mths': 'Número de tentativas de empréstimo nos últimos 24 meses',
    'addr_state': 'Estado de residência indicado pelo tomador de crédito no momento do pleito',
    'application_type':	'Informa se o empréstimo é individual ou conjunto para dois co-tomadores',
    'avg_cur_bal': 'Saldo corrente médio de todos os empréstimos',
    'bc_open_to_buy': 'Limite total disponível para utilização em cartões de crédito rotativos (revolving)',
    'bc_util': 'Relação entre o saldo total atual e o limite máximo de crédito em todas as contas de cartão de crédito',
    'dti': 'Razão entre os pagamentos mensais de operações de crédito pelo devedor da operação de crédito e a renda do devedor da operação de crédito',
    'earliest_cr_line': 'Mês de abertura da linha de crédito mais antiga registrada do tomador',
    'fico_score': 'Credit scoring do devedor da operação de crédito no momento da originação da operação de crédito',
    'funded_amnt': 'Valor total comprometido (ou financiado) naquele empréstimo até aquele momento',
    'grade': 'Grau de risco atribuído pelo Lending Club ao empréstimo',
    'home_ownership': 'Situação de propriedade do domicílio informada pelo tomador no momento do cadastro ou obtida do relatório de crédito. Os valores possíveis são: ALUGADO, PRÓPRIO, FINANCIADO, OUTROS.',
    'initial_list_status': 'Status inicial de listagem do empréstimo. Valores possíveis: W (em espera) e F (financiado)',
    'installment': 'Valor da prestação mensal devida pelo tomador caso o empréstimo seja efetivamente originado',
    'int_rate': 'Taxa de juros da operação de crédito',
    'loan_amnt': 'Valor da operação de crédito',
    'log_annual_inc': 'Logaritmo natural da renda anual informada pelo tomador de crédito no momento do pleito',
    'mo_sin_old_rev_tl_op': 'Número de meses desde a abertura da conta rotativa mais antiga do tomador',
    'mo_sin_rcnt_rev_tl_op': 'Número de meses desde a abertura da conta rotativa mais recente do tomador',             
    'mort_acc': 'Número de contas de financiamento imobiliário (hipotecas) mantidas pelo tomador',
    'num_actv_rev_tl': 'Número de contas rotativas atualmente ativas',
    'purpose': 'Categoria informada pelo tomador para justificar o propósito do empréstimo',    
    'revol_util': 'Taxa de utilização de crédito rotativo, ou seja, a proporção do crédito disponível que o tomador está efetivamente utilizando',
    'loan_status': 'Status atual da operação de crédito: operação de crédito em dia (loan_status = 0); operação de crédito em atraso (loan_status = 1)'
}


# =============================================================================
# FUNÇÕES AUXILIARES (fora do render para permitir caching)
# =============================================================================

@st.cache_data
def load_data():
    try:
        training_data = pd.read_csv('training_sample.csv')
        production_data = pd.read_csv('testing_sample_true.csv')
        return training_data, production_data
    except FileNotFoundError:
        st.error("Arquivos CSV não encontrados. Certifique-se de que 'training_sample.csv' e 'testing_sample_true.csv' estão no diretório correto.")
        return None, None


def plot_sigmoid_curve(model, X_train, y_train, selected_features):
    """Função para plotar a curva S da regressão logística"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Curva S Teórica da Regressão Logística', 'Distribuição de Probabilidades por Classe'],
        column_widths=[0.5, 0.5]
    )
    
    # Gráfico 1: Curva S teórica
    X_scaled = (X_train - X_train.mean()) / X_train.std()
    linear_combination = np.dot(X_scaled, model.coef_.T) + model.intercept_
    
    min_val = linear_combination.min() - 2
    max_val = linear_combination.max() + 2
    x_range = np.linspace(min_val, max_val, 300)
    
    y_sigmoid = 1 / (1 + np.exp(-x_range))
    
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=y_sigmoid,
            mode='lines',
            name='Curva Sigmóide',
            line=dict(color='blue', width=3),
            showlegend=False
        ),
        row=1, col=1
    )
    
    real_probabilities = 1 / (1 + np.exp(-linear_combination.flatten()))
    
    sample_size = min(1000, len(linear_combination))
    indices = np.random.choice(len(linear_combination), sample_size, replace=False)
    
    fig.add_trace(
        go.Scatter(
            x=linear_combination.flatten()[indices],
            y=real_probabilities[indices],
            mode='markers',
            name='Dados do Modelo',
            marker=dict(
                color=y_train.iloc[indices], 
                colorscale=[[0, 'green'], [1, 'red']], 
                size=4, 
                opacity=0.6,
            ),
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Gráfico 2: Distribuição de probabilidades por classe
    y_pred_proba = model.predict_proba(X_train)[:, 1]
    
    prob_class_0 = y_pred_proba[y_train == 0]
    prob_class_1 = y_pred_proba[y_train == 1]
    
    fig.add_trace(
        go.Histogram(
            x=prob_class_0,
            name='Bons Pagadores (Classe 0)',
            opacity=0.7,
            nbinsx=30,
            marker_color='green',
            showlegend=True
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Histogram(
            x=prob_class_1,
            name='Inadimplentes (Classe 1)',
            opacity=0.7,
            nbinsx=30,
            marker_color='red',
            showlegend=True
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Combinação Linear (β₀ + β₁X₁ + β₂X₂ + ...)", row=1, col=1)
    fig.update_yaxes(title_text="Probabilidade de Inadimplência", row=1, col=1)
    fig.update_xaxes(title_text="Probabilidade Predita", row=1, col=2)
    fig.update_yaxes(title_text="Frequência", row=1, col=2)
    
    fig.update_layout(
        title_text="Análise da Função Sigmóide do Modelo de Regressão Logística",
        height=500,
        barmode='overlay'
    )
    
    return fig


def plot_roc_curve(y_true, y_pred_proba):
    """Função para plotar curva ROC"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {roc_auc:.3f})',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Classificador Aleatório',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title='Curva ROC',
        xaxis_title='Taxa de Falsos Positivos (1 - Especificidade)',
        yaxis_title='Taxa de Verdadeiros Positivos (Sensibilidade)',
        height=400,
        showlegend=True
    )
    
    return fig, roc_auc


def plot_confusion_matrix(y_true, y_pred, title="Matriz de Confusão"):
    """Função para plotar matriz de confusão"""
    cm = confusion_matrix(y_true, y_pred)
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predito: Bom Pagador', 'Predito: Inadimplente'],
        y=['Real: Bom Pagador', 'Real: Inadimplente'],
        colorscale='Blues',
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        xaxis_title="Predição",
        yaxis_title="Valor Real"
    )
    
    return fig


def display_model_statistics(model, X_train, y_train, X_test, y_test, cutoff=0.5):
    """Função para exibir estatísticas do modelo"""
    st.subheader("📊 Estatísticas do Modelo de Regressão Logística")
    
    def apply_custom_cutoff(probabilities, cutoff_value):
        return (probabilities > cutoff_value).astype(int)
    
    y_pred_proba_train = model.predict_proba(X_train)[:, 1]
    y_pred_proba_test = model.predict_proba(X_test)[:, 1]
    
    y_pred_train = apply_custom_cutoff(y_pred_proba_train, cutoff)
    y_pred_test = apply_custom_cutoff(y_pred_proba_test, cutoff)
    
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Acurácia no Treinamento", f"{train_accuracy:.4f}")
        st.metric("Acurácia no Teste", f"{test_accuracy:.4f}")
    
    with col2:
        st.metric("Número de Observações (Treino)", len(y_train))
        st.metric("Número de Observações (Teste)", len(y_test))
    
    with col3:
        st.metric("Cut-off Utilizado", f"{cutoff:.2%}")
        negadas_pct = (y_pred_test.sum() / len(y_pred_test)) * 100
        st.metric("% Operações Negadas", f"{negadas_pct:.1f}%")
    
    st.subheader("📋 Relatório de Classificação")
    report = classification_report(y_test, y_pred_test, output_dict=True)
    
    report_data = {
        'Métrica': ['Precisão', 'Recall (Sensibilidade)', 'F1-Score', 'Support (Qtd)'],
        'Bons Pagadores (Classe 0)': [
            f"{report['0']['precision']:.4f}",
            f"{report['0']['recall']:.4f}", 
            f"{report['0']['f1-score']:.4f}",
            f"{int(report['0']['support'])}"
        ],
        'Inadimplentes (Classe 1)': [
            f"{report['1']['precision']:.4f}",
            f"{report['1']['recall']:.4f}",
            f"{report['1']['f1-score']:.4f}", 
            f"{int(report['1']['support'])}"
        ]
    }
    
    report_df = pd.DataFrame(report_data)
    st.dataframe(report_df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📊 Acurácia Geral", 
            f"{report['accuracy']:.4f}",
            help="Proporção total de predições corretas"
        )
    
    with col2:
        st.metric(
            "⚖️ F1-Score Médio", 
            f"{report['macro avg']['f1-score']:.4f}",
            help="Média harmônica entre precisão e recall"
        )
    
    with col3:
        st.metric(
            "🎯 F1-Score Ponderado", 
            f"{report['weighted avg']['f1-score']:.4f}",
            help="F1-Score considerando o desbalanceamento das classes"
        )
    
    with st.expander("💡 Explicação das Estatísticas"):
        st.markdown(f"""
        **Cut-off Atual**: {cutoff:.2%} - Operações com probabilidade de inadimplência MAIOR que {cutoff:.2%} são NEGADAS.
        
        **Acurácia**: Proporção de predições corretas em relação ao total de predições.
        
        **Precisão**: Proporção de verdadeiros positivos em relação ao total de positivos preditos.
        
        **Recall (Sensibilidade)**: Proporção de verdadeiros positivos em relação ao total de positivos reais.
        
        **F1-Score**: Média harmônica entre precisão e recall.
        
        **Support**: Número de observações reais de cada classe.
        
        **Impacto do Cut-off**:
        - Cut-off mais baixo: Mais aprovações, menos conservador
        - Cut-off mais alto: Menos aprovações, mais conservador
        - Cut-off padrão: 0.50 (50%)
        """)


def display_regression_equation(model, selected_features):
    """Função para exibir equação da regressão"""
    st.subheader("🔢 Equação da Regressão Logística")
    
    coef = model.coef_[0]
    intercept = model.intercept_[0]
    
    coef_df = pd.DataFrame({
        'Variável': selected_features,
        'Coeficiente': coef,
        'Exp(Coeficiente)': np.exp(coef)
    })
    
    st.dataframe(coef_df.round(4))
    
    st.markdown("### Equação Logística:")
    equation = f"logit(p) = {intercept:.4f}"
    
    for i, feature in enumerate(selected_features):
        sign = "+" if coef[i] >= 0 else ""
        equation += f" {sign} {coef[i]:.4f} * {feature}"
    
    st.code(equation)
    
    st.markdown("### Probabilidade:")
    st.latex(r"p = \frac{1}{1 + e^{-logit(p)}}")
    
    with st.expander("💡 Interpretação dos Coeficientes"):
        st.markdown("""
        **Coeficiente**: Representa a mudança no log-odds (logit) para uma mudança unitária na variável independente.
        
        **Exp(Coeficiente)**: Representa o odds ratio. 
        - Se > 1: A variável aumenta a chance de inadimplência
        - Se < 1: A variável diminui a chance de inadimplência
        - Se = 1: A variável não afeta a chance de inadimplência
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Interpretação Específica por Variável:")
        
        for i, feature in enumerate(selected_features):
            coef_val = coef[i]
            exp_coef = np.exp(coef_val)
            
            if coef_val > 0:
                effect_icon = "📈"
                effect_text = "AUMENTA"
                risk_color = "red"
            elif coef_val < 0:
                effect_icon = "📉"
                effect_text = "DIMINUI"
                risk_color = "green"
            else:
                effect_icon = "➡️"
                effect_text = "NÃO AFETA"
                risk_color = "gray"
            
            if abs(coef_val) > 1:
                magnitude = "FORTE"
            elif abs(coef_val) > 0.5:
                magnitude = "MODERADO"
            elif abs(coef_val) > 0.1:
                magnitude = "FRACO"
            else:
                magnitude = "MUITO FRACO"
            
            if coef_val != 0:
                change_pct = (exp_coef - 1) * 100
                if coef_val > 0:
                    interpretation = f"Cada aumento unitário em **{feature}** multiplica as chances de inadimplência por **{exp_coef:.4f}**, representando um aumento de **{change_pct:+.1f}%** nas odds"
                else:
                    interpretation = f"Cada aumento unitário em **{feature}** multiplica as chances de inadimplência por **{exp_coef:.4f}**, representando uma redução de **{abs(change_pct):.1f}%** nas odds"
            else:
                interpretation = f"**{feature}** não tem impacto significativo na probabilidade de inadimplência"
                            
            st.markdown(f"""
            **{effect_icon} {feature}**
            - **Efeito**: <span style="color:{risk_color}">**{effect_text}**</span> o risco de inadimplência
            - **Magnitude**: {magnitude} (coeficiente: {coef_val:.4f})
            - **Interpretação**: {interpretation}
            """, unsafe_allow_html=True)
            
            st.markdown("---")


# =============================================================================
# FUNÇÃO RENDER - PONTO DE ENTRADA DO MÓDULO
# =============================================================================

def render():
    """Função principal que renderiza o módulo de risco de crédito"""
    
    # Título principal
    st.title("🏦 Sistema de Modelagem de Risco de Crédito")
    st.markdown("---")
    
    # Carregar dados
    training_data, production_data = load_data()
    
    if training_data is None or production_data is None:
        st.stop()
    
    # Seção de configuração do modelo na página principal
    st.header("🔧 Configuração do Modelo")
    
    # Listar variáveis disponíveis (excluindo target e id)
    available_features = [col for col in training_data.columns 
                         if col not in ['loan_status', 'id', 'Unnamed: 0']]
    
    # Seleção de variáveis
    selected_features = st.multiselect(
        "Selecione as variáveis para o modelo:",
        available_features,
        default=['loan_amnt', 'int_rate', 'log_annual_inc', 'fico_score', 'funded_amnt'],
        help="Selecione as variáveis que serão utilizadas no modelo de regressão logística",
        key="m02_selected_features"
    )
    
    # Exibir descrições das variáveis em um expander
    with st.expander("📝 Ver Descrição das Variáveis"):
        st.markdown("### Descrição de Todas as Variáveis Disponíveis")
        for feature in available_features:
            st.write(f"**{feature}**: {variable_descriptions.get(feature, 'Descrição não disponível')}")
        
        if selected_features:
            st.markdown("---")
            st.markdown("### Variáveis Selecionadas no Modelo Atual")
            for feature in selected_features:
                st.write(f"**{feature}**: {variable_descriptions.get(feature, 'Descrição não disponível')}")
    
    st.markdown("---")
    
    # Botão para executar o modelo
    if not selected_features:
        st.warning("⚠️ Selecione pelo menos uma variável para continuar!")
        st.button("🚀 Executar Modelo de Regressão Logística", disabled=True, key="m02_btn_disabled")
        return
    
    # Mostrar resumo das variáveis selecionadas
    st.info(f"📊 Variáveis selecionadas: {', '.join(selected_features)}")
    
    # Configuração do cut-off ANTES do treinamento
    st.subheader("⚖️ Configuração do Ponto de Cut-off")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        cutoff = st.slider(
            "Selecione o ponto de cut-off (probabilidade mínima para NEGAR o crédito):",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            format="%.2f",
            help="Operações com probabilidade de inadimplência MAIOR que este valor serão NEGADAS. Este cut-off será usado para avaliar o modelo.",
            key="m02_cutoff"
        )
    
    with col2:
        st.metric("Cut-off Selecionado", f"{cutoff:.2%}")
        if cutoff < 0.3:
            st.warning("⚠️ Cut-off baixo: Muitas negações")
        elif cutoff > 0.7:
            st.warning("⚠️ Cut-off alto: Muitas aprovações")
        else:
            st.success("✅ Cut-off equilibrado")
    
    # Função para aplicar cut-off personalizado
    def apply_custom_cutoff(probabilities, cutoff_value):
        return (probabilities > cutoff_value).astype(int)
    
    # Botão para executar o modelo
    run_model = st.button("🚀 Executar Modelo de Regressão Logística", type="primary", key="m02_btn_run")
    
    if not run_model:
        st.info("👆 Clique no botão acima para treinar o modelo com as variáveis selecionadas.")
        return
    
    # Mostrar progresso
    with st.spinner('🔄 Treinando modelo de regressão logística...'):
        # Preparar dados
        X = training_data[selected_features]
        y = training_data['loan_status']
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        # Criar e treinar modelo
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
    
    st.success("✅ Modelo treinado com sucesso!")
    st.info(f"🎯 Cut-off aplicado: {cutoff:.2%} - Todas as análises usarão este ponto de corte.")
    
    st.markdown("---")
    
    # Tabs para organizar o conteúdo
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Análise do Modelo", 
        "🎯 Aplicação em Produção", 
        "📈 Comparação com Produção",
        "📋 Dados", 
        "ℹ️ Informações"
    ])
    
    with tab1:
        st.header("📊 Análise do Modelo de Treinamento")
        
        # Gráfico S da regressão logística
        st.subheader("📈 Curva S da Regressão Logística")
        sigmoid_fig = plot_sigmoid_curve(model, X_train, y_train, selected_features)
        st.plotly_chart(sigmoid_fig, use_container_width=True)
        
        # Curva ROC
        st.subheader("📊 Curva ROC")
        y_pred_proba_test = model.predict_proba(X_test)[:, 1]
        roc_fig, roc_auc = plot_roc_curve(y_test, y_pred_proba_test)
        st.plotly_chart(roc_fig, use_container_width=True)
        
        # Matriz de confusão
        st.subheader("🔍 Matriz de Confusão")
        y_pred_proba_test = model.predict_proba(X_test)[:, 1]
        y_pred_test_custom = apply_custom_cutoff(y_pred_proba_test, cutoff)
        cm_fig = plot_confusion_matrix(y_test, y_pred_test_custom, f"Matriz de Confusão (Cut-off: {cutoff:.2%})")
        st.plotly_chart(cm_fig, use_container_width=True)
        
        # Mostrar impacto do cut-off selecionado
        with st.expander("📊 Comparação com Cut-off Padrão (50%)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                y_pred_test_default = apply_custom_cutoff(y_pred_proba_test, 0.5)
                acc_default = accuracy_score(y_test, y_pred_test_default)
                st.metric("Acurácia (Cut-off 50%)", f"{acc_default:.3f}")
            
            with col2:
                acc_custom = accuracy_score(y_test, y_pred_test_custom)
                st.metric(f"Acurácia (Cut-off {cutoff:.0%})", f"{acc_custom:.3f}")
            
            with col3:
                diff = acc_custom - acc_default
                st.metric("Diferença", f"{diff:+.3f}")
        
        # Estatísticas do modelo
        display_model_statistics(model, X_train, y_train, X_test, y_test, cutoff)
        
        # Equação da regressão
        display_regression_equation(model, selected_features)
    
    with tab2:
        st.header("🎯 Aplicação do Modelo em Produção")
        
        # Aplicar modelo nos dados de produção
        X_production = production_data[selected_features]
        y_pred_proba_production = model.predict_proba(X_production)[:, 1]
        y_pred_production = apply_custom_cutoff(y_pred_proba_production, cutoff)
        
        # Criar DataFrame com resultados
        results_df = production_data.copy()
        results_df['probabilidade_inadimplencia'] = y_pred_proba_production
        results_df['decisao_credito'] = ['NEGAR' if pred == 1 else 'APROVAR' for pred in y_pred_production]
        
        # Estatísticas de decisão
        st.subheader("📊 Estatísticas de Decisão")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            aprovadas = sum(y_pred_production == 0)
            st.metric("Operações Aprovadas", aprovadas)
        
        with col2:
            negadas = sum(y_pred_production == 1)
            st.metric("Operações Negadas", negadas)
        
        with col3:
            taxa_aprovacao = (aprovadas / len(y_pred_production)) * 100
            st.metric("Taxa de Aprovação", f"{taxa_aprovacao:.1f}%")
        
        with col4:
            st.metric("Cut-off Aplicado", f"{cutoff:.2%}")
        
        # Distribuição de probabilidades com linha de cut-off
        st.subheader("📈 Distribuição de Probabilidades de Inadimplência")
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=y_pred_proba_production,
            nbinsx=50,
            name='Distribuição de Probabilidades',
            opacity=0.7,
            marker_color='lightblue'
        ))
        
        fig.add_vline(
            x=cutoff, 
            line_dash="dash", 
            line_color="red",
            line_width=3,
            annotation_text=f"Cut-off: {cutoff:.2%}"
        )
        
        fig.add_vrect(
            x0=0, x1=cutoff,
            fillcolor="green", opacity=0.2,
            annotation_text="APROVAR", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=cutoff, x1=1,
            fillcolor="red", opacity=0.2,
            annotation_text="NEGAR", annotation_position="top right"
        )
        
        fig.update_layout(
            title='Distribuição de Probabilidades de Inadimplência com Cut-off',
            xaxis_title='Probabilidade de Inadimplência',
            yaxis_title='Frequência',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise por faixas de probabilidade
        st.subheader("📊 Análise por Faixas de Probabilidade")
        
        bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
        results_df['faixa_probabilidade'] = pd.cut(results_df['probabilidade_inadimplencia'], bins=bins, labels=labels, include_lowest=True)
        
        faixa_counts = results_df['faixa_probabilidade'].value_counts().sort_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Distribuição por Faixa de Risco:**")
            for faixa, count in faixa_counts.items():
                pct = (count / len(results_df)) * 100
                st.write(f"• {faixa}: {count} operações ({pct:.1f}%)")
        
        with col2:
            fig_pie = go.Figure(data=[go.Pie(
                labels=faixa_counts.index,
                values=faixa_counts.values,
                hole=0.3
            )])
            fig_pie.update_layout(title="Distribuição por Faixa de Risco", height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Exibir resultados
        st.subheader("📋 Resultados das Decisões")
        display_cols = ['id', 'probabilidade_inadimplencia', 'decisao_credito', 'faixa_probabilidade']
        st.dataframe(results_df[display_cols].round(4))
    
    with tab3:
        st.header("📈 Comparação com Dados de Produção")
        
        if 'loan_status' in production_data.columns:
            y_true_production = production_data['loan_status']
            
            X_production = production_data[selected_features]
            y_pred_proba_production = model.predict_proba(X_production)[:, 1]
            y_pred_production = apply_custom_cutoff(y_pred_proba_production, cutoff)
            
            st.subheader("🔄 Comparação de Performance por Cut-off")
            
            cutoffs_comparison = [0.3, 0.4, 0.5, 0.6, 0.7]
            comparison_results = []
            
            for co in cutoffs_comparison:
                y_pred_co = apply_custom_cutoff(y_pred_proba_production, co)
                acc = accuracy_score(y_true_production, y_pred_co)
                
                from sklearn.metrics import precision_score, recall_score, f1_score
                precision = precision_score(y_true_production, y_pred_co, zero_division=0)
                recall = recall_score(y_true_production, y_pred_co, zero_division=0)
                f1 = f1_score(y_true_production, y_pred_co, zero_division=0)
                
                aprovacao_rate = (1 - y_pred_co.mean()) * 100
                
                comparison_results.append({
                    'Cut-off': f"{co:.1%}",
                    'Acurácia': f"{acc:.3f}",
                    'Precisão': f"{precision:.3f}",
                    'Recall': f"{recall:.3f}",
                    'F1-Score': f"{f1:.3f}",
                    'Taxa Aprovação': f"{aprovacao_rate:.1f}%"
                })
            
            comparison_df = pd.DataFrame(comparison_results)
            
            current_cutoff_str = f"{cutoff:.1%}"
            
            st.write("**Comparação de Performance com Diferentes Cut-offs:**")
            
            def highlight_current_cutoff(row):
                if row['Cut-off'] == current_cutoff_str:
                    return ['background-color: lightgreen'] * len(row)
                return [''] * len(row)
            
            styled_df = comparison_df.style.apply(highlight_current_cutoff, axis=1)
            st.dataframe(styled_df)
            
            st.info(f"💡 Cut-off atual ({current_cutoff_str}) destacado em verde na tabela acima.")
            
            st.subheader("🔍 Matriz de Confusão - Produção")
            cm_prod_fig = plot_confusion_matrix(
                y_true_production, 
                y_pred_production, 
                f"Matriz de Confusão - Produção (Cut-off: {cutoff:.2%})"
            )
            st.plotly_chart(cm_prod_fig, use_container_width=True)
            
            st.subheader("📊 Métricas de Produção")
            
            accuracy_prod = accuracy_score(y_true_production, y_pred_production)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Acurácia em Produção", f"{accuracy_prod:.4f}")
            
            with col2:
                roc_auc_prod = auc(*roc_curve(y_true_production, y_pred_proba_production)[:2])
                st.metric("AUC em Produção", f"{roc_auc_prod:.4f}")
            
            with col3:
                st.metric("Cut-off Aplicado", f"{cutoff:.2%}")
            
            st.subheader("📋 Relatório de Classificação - Produção")
            report_prod = classification_report(y_true_production, y_pred_production, output_dict=True)
            report_prod_df = pd.DataFrame(report_prod).transpose()
            st.dataframe(report_prod_df.round(4))
            
            st.subheader("📊 Curva ROC - Produção")
            roc_prod_fig, _ = plot_roc_curve(y_true_production, y_pred_proba_production)
            st.plotly_chart(roc_prod_fig, use_container_width=True)
            
        else:
            st.info("⚠️ Os dados de produção não contêm a variável 'loan_status' para comparação.")
    
    with tab4:
        st.header("📋 Visualização dos Dados")
        
        st.subheader("🔧 Dados de Treinamento")
        st.write(f"Shape: {training_data.shape}")
        st.dataframe(training_data.head())
        
        st.subheader("🎯 Dados de Produção")
        st.write(f"Shape: {production_data.shape}")
        st.dataframe(production_data.head())
        
        st.subheader("📊 Estatísticas Descritivas")
        st.write("**Dados de Treinamento:**")
        st.dataframe(training_data[selected_features].describe())
    
    with tab5:
        st.header("ℹ️ Informações sobre o Sistema")
        
        st.markdown("""
        ### 🎯 Objetivo
        Este sistema foi desenvolvido para ensinar aos estagiários como funciona a modelagem de risco de crédito utilizando regressão logística.
        
        ### 📊 Funcionalidades
        1. **Seleção de Variáveis**: Permite escolher quais variáveis usar no modelo
        2. **Treinamento do Modelo**: Treina um modelo de regressão logística com divisão 70/30
        3. **Visualizações**: Gera gráficos da curva S, ROC e matriz de confusão
        4. **Estatísticas**: Exibe métricas detalhadas do modelo
        5. **Aplicação em Produção**: Aplica o modelo em novos dados
        6. **Comparação**: Compara resultados com dados reais (quando disponíveis)
        
        ### 🔧 Tecnologias Utilizadas
        - **Streamlit**: Interface web interativa
        - **Scikit-learn**: Algoritmos de machine learning
        - **Plotly**: Visualizações interativas
        - **Pandas**: Manipulação de dados
        
        ### 📈 Interpretação dos Resultados
        - **AUC > 0.8**: Modelo excelente
        - **AUC 0.7-0.8**: Modelo bom
        - **AUC 0.6-0.7**: Modelo regular
        - **AUC < 0.6**: Modelo ruim
        
        """)


# =============================================================================
# EXECUÇÃO STANDALONE (para testes)
# =============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sistema de Modelagem de Risco de Crédito",
        page_icon="💳",
        layout="wide"
    )
    render()