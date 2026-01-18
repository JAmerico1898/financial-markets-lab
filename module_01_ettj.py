"""
Módulo 01 - Estrutura a Termo de Taxas de Juros
Laboratório de Mercado Financeiro
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.interpolate import (
    interp1d, 
    UnivariateSpline, 
    CubicSpline,
    PchipInterpolator,
    Akima1DInterpolator
)
from scipy.optimize import minimize
import pyield as yd


# =============================================================================
# FUNÇÕES AUXILIARES (fora do render para permitir caching)
# =============================================================================

@st.cache_data(ttl=3600)
def buscar_dados_di1(data_referencia):
    """
    Busca dados DI1 para uma data específica
    Se não houver dados, tenta dias anteriores até encontrar
    """
    tentativas = 0
    max_tentativas = 10
    data_atual = data_referencia
    
    while tentativas < max_tentativas:
        try:
            # Formatar data no formato YYYY-MM-DD
            data_str = data_atual.strftime("%Y-%m-%d")
            
            # Buscar dados
            df_polars = yd.futures(contract_code="DI1", date=data_str)
            
            # Converter para pandas
            df = df_polars.to_pandas(use_pyarrow_extension_array=True)
            
            # Verificar se há dados
            if df is not None and len(df) > 0:
                return df, data_atual
            
        except Exception as e:
            st.warning(f"Erro ao buscar dados para {data_str}: {str(e)}")
        
        # Tentar dia anterior
        data_atual = data_atual - timedelta(days=1)
        tentativas += 1
    
    return None, None


def filtrar_dados_5anos(df, data_referencia):
    """
    Filtra contratos DI1 até 5 anos (1260 dias úteis) a partir da data de referência
    """
    # 5 anos = 252 dias úteis/ano * 5 = 1260 dias úteis
    max_dias_uteis = 1260
    
    # Converter para pandas nativo se necessário (lidar com PyArrow)
    df_filtrado = df.copy()
    if hasattr(df_filtrado['BDaysToExp'], 'to_numpy'):
        df_filtrado['BDaysToExp'] = df_filtrado['BDaysToExp'].to_numpy()
    
    df_filtrado = df_filtrado[df_filtrado['BDaysToExp'] <= max_dias_uteis].copy()
    
    # Ordenar por dias úteis
    df_filtrado = df_filtrado.sort_values('BDaysToExp')
    
    return df_filtrado


# Funções de interpolação/suavização
def linear_interpolation(x, y, x_new):
    """Interpolação Linear"""
    f = interp1d(x, y, kind='linear', fill_value='extrapolate')
    return f(x_new)


def cubic_spline(x, y, x_new):
    """Cubic Spline"""
    cs = CubicSpline(x, y)
    return cs(x_new)


def pchip_interpolation(x, y, x_new):
    """PCHIP - Preserva monotonicidade"""
    pchip = PchipInterpolator(x, y)
    return pchip(x_new)


def akima_interpolation(x, y, x_new):
    """Akima Spline - Menos oscilações"""
    akima = Akima1DInterpolator(x, y)
    return akima(x_new)


def smoothing_spline(x, y, x_new, smoothing_factor=None):
    """Smoothing Spline com fator de suavização"""
    if smoothing_factor is None:
        smoothing_factor = len(x)
    
    spl = UnivariateSpline(x, y, s=smoothing_factor)
    return spl(x_new)


def nelson_siegel(params, tau):
    """
    Modelo Nelson-Siegel
    r(tau) = beta0 + beta1 * ((1 - exp(-tau/lambda)) / (tau/lambda)) 
           + beta2 * (((1 - exp(-tau/lambda)) / (tau/lambda)) - exp(-tau/lambda))
    """
    beta0, beta1, beta2, lambda_param = params
    
    if lambda_param <= 0:
        lambda_param = 0.0001
    
    term1 = (1 - np.exp(-tau / lambda_param)) / (tau / lambda_param + 1e-10)
    term2 = term1 - np.exp(-tau / lambda_param)
    
    return beta0 + beta1 * term1 + beta2 * term2


def fit_nelson_siegel(x, y):
    """Ajuste do modelo Nelson-Siegel aos dados"""
    
    def objective(params):
        predicted = nelson_siegel(params, x)
        return np.sum((y - predicted) ** 2)
    
    # Valores iniciais
    initial_params = [np.mean(y), -0.02, -0.02, 500]
    
    # Limites para os parâmetros
    bounds = [
        (y.min() - 0.05, y.max() + 0.05),  # beta0
        (-0.1, 0.1),                        # beta1
        (-0.1, 0.1),                        # beta2
        (1, 2000)                           # lambda
    ]
    
    result = minimize(objective, initial_params, method='L-BFGS-B', bounds=bounds)
    
    return result.x


def nelson_siegel_svensson(params, tau):
    """
    Modelo Nelson-Siegel-Svensson (extensão do NS com 2 parâmetros adicionais)
    """
    beta0, beta1, beta2, beta3, lambda1, lambda2 = params
    
    if lambda1 <= 0:
        lambda1 = 0.0001
    if lambda2 <= 0:
        lambda2 = 0.0001
    
    term1 = (1 - np.exp(-tau / lambda1)) / (tau / lambda1 + 1e-10)
    term2 = term1 - np.exp(-tau / lambda1)
    term3 = (1 - np.exp(-tau / lambda2)) / (tau / lambda2 + 1e-10) - np.exp(-tau / lambda2)
    
    return beta0 + beta1 * term1 + beta2 * term2 + beta3 * term3


def fit_nelson_siegel_svensson(x, y):
    """Ajuste do modelo Nelson-Siegel-Svensson aos dados"""
    
    def objective(params):
        predicted = nelson_siegel_svensson(params, x)
        return np.sum((y - predicted) ** 2)
    
    # Valores iniciais
    initial_params = [np.mean(y), -0.02, -0.02, 0.01, 500, 1000]
    
    # Limites para os parâmetros
    bounds = [
        (y.min() - 0.05, y.max() + 0.05),  # beta0
        (-0.1, 0.1),                        # beta1
        (-0.1, 0.1),                        # beta2
        (-0.1, 0.1),                        # beta3
        (1, 2000),                          # lambda1
        (1, 3000)                           # lambda2
    ]
    
    result = minimize(objective, initial_params, method='L-BFGS-B', bounds=bounds)
    
    return result.x


# =============================================================================
# FUNÇÃO RENDER - PONTO DE ENTRADA DO MÓDULO
# =============================================================================

def render():
    """Função principal que renderiza o módulo"""
    
    # Título e descrição
    st.title("📈 Modelagem da Estrutura a Termo - Taxa DI (CDI)")
    st.markdown("""
    Esta aplicação modela a estrutura a termo das taxas de juros brasileiras usando dados de contratos futuros DI1 da B3.
    Os contratos DI1 são derivativos da taxa DI (CDI) pós-fixada, essencialmente taxas zero-cupom com capitalização de 252 dias úteis.
    """)

    # Sidebar para controles
    st.sidebar.header("⚙️ Configurações")

    # Data de referência
    data_hoje = datetime.now().date()
    data_referencia = st.sidebar.date_input(
        "Data de Referência",
        value=data_hoje - timedelta(days=1),
        max_value=data_hoje,
        key="ettj_data_ref"
    )

    # Botão para carregar dados
    if st.sidebar.button("🔄 Carregar Dados", type="primary", key="ettj_btn_carregar"):
        st.cache_data.clear()

    # Carregar dados
    with st.spinner("Carregando dados DI1..."):
        df_original, data_encontrada = buscar_dados_di1(data_referencia)

    if df_original is None:
        st.error("❌ Não foi possível carregar os dados. Verifique sua conexão e tente novamente.")
        st.stop()

    # Exibir data dos dados
    if data_encontrada != data_referencia:
        st.info(f"ℹ️ Dados não disponíveis para {data_referencia}. Usando dados de **{data_encontrada.strftime('%d/%m/%Y')}**")
    else:
        st.success(f"✅ Dados carregados para **{data_encontrada.strftime('%d/%m/%Y')}**")

    # Filtrar dados até 5 anos
    df_filtrado = filtrar_dados_5anos(df_original, data_encontrada)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Estatísticas dos Dados")
    st.sidebar.metric("Total de Contratos", len(df_original))
    st.sidebar.metric("Contratos até 5 anos", len(df_filtrado))
    # Converter para numpy para evitar problemas com PyArrow
    prazo_max = int(df_filtrado['BDaysToExp'].to_numpy().max())
    st.sidebar.metric("Prazo Máximo (dias úteis)", prazo_max)

    # Preparar dados para modelagem
    # Converter de PyArrow para numpy para evitar erros com .min() e .max()
    x_data = df_filtrado['BDaysToExp'].to_numpy(dtype='float64')
    y_data = df_filtrado['SettlementRate'].to_numpy(dtype='float64')

    # Sidebar - Seleção do método de suavização
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Método de Suavização")

    metodo = st.sidebar.selectbox(
        "Escolha o método:",
        [
            "Nelson-Siegel-Svensson",
            "Nelson-Siegel",
            "Smoothing Spline",
            "Akima Spline",
            "PCHIP (Monotônica)",
            "Cubic Spline",
            "Interpolação Linear",
        ],
        key="ettj_metodo"
    )

    # Parâmetros específicos para alguns métodos
    smoothing_factor = None
    if metodo == "Smoothing Spline":
        smoothing_factor = st.sidebar.slider(
            "Fator de Suavização",
            min_value=0.0,
            max_value=float(len(x_data) * 2),
            value=float(len(x_data)),
            step=10.0,
            help="Valores maiores = mais suavização",
            key="ettj_smoothing"
        )

    # Gerar pontos para a curva suavizada
    x_smooth = np.linspace(x_data.min(), x_data.max(), 500)

    # Aplicar método selecionado
    try:
        if metodo == "Interpolação Linear":
            y_smooth = linear_interpolation(x_data, y_data, x_smooth)
        
        elif metodo == "Cubic Spline":
            y_smooth = cubic_spline(x_data, y_data, x_smooth)
        
        elif metodo == "PCHIP (Monotônica)":
            y_smooth = pchip_interpolation(x_data, y_data, x_smooth)
        
        elif metodo == "Akima Spline":
            y_smooth = akima_interpolation(x_data, y_data, x_smooth)
        
        elif metodo == "Smoothing Spline":
            y_smooth = smoothing_spline(x_data, y_data, x_smooth, smoothing_factor)
        
        elif metodo == "Nelson-Siegel":
            params_ns = fit_nelson_siegel(x_data, y_data)
            y_smooth = nelson_siegel(params_ns, x_smooth)
            
            # Exibir parâmetros estimados
            st.sidebar.markdown("**Parâmetros Estimados:**")
            st.sidebar.text(f"β₀ = {params_ns[0]:.6f}")
            st.sidebar.text(f"β₁ = {params_ns[1]:.6f}")
            st.sidebar.text(f"β₂ = {params_ns[2]:.6f}")
            st.sidebar.text(f"λ = {params_ns[3]:.2f}")
        
        elif metodo == "Nelson-Siegel-Svensson":
            params_nss = fit_nelson_siegel_svensson(x_data, y_data)
            y_smooth = nelson_siegel_svensson(params_nss, x_smooth)
            
            # Exibir parâmetros estimados
            st.sidebar.markdown("**Parâmetros Estimados:**")
            st.sidebar.text(f"β₀ = {params_nss[0]:.6f}")
            st.sidebar.text(f"β₁ = {params_nss[1]:.6f}")
            st.sidebar.text(f"β₂ = {params_nss[2]:.6f}")
            st.sidebar.text(f"β₃ = {params_nss[3]:.6f}")
            st.sidebar.text(f"λ₁ = {params_nss[4]:.2f}")
            st.sidebar.text(f"λ₂ = {params_nss[5]:.2f}")
        
        # Converter para percentual
        y_data_pct = y_data * 100
        y_smooth_pct = y_smooth * 100
        
        # Criar gráfico principal
        fig = go.Figure()
        
        # Adicionar pontos observados
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data_pct,
            mode='markers',
            name='Taxas Observadas',
            marker=dict(size=8, color='royalblue', symbol='circle'),
            hovertemplate='<b>Dias Úteis:</b> %{x}<br><b>Taxa:</b> %{y:.4f}%<extra></extra>'
        ))
        
        # Adicionar curva suavizada
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=y_smooth_pct,
            mode='lines',
            name=f'Curva Ajustada ({metodo})',
            line=dict(color='crimson', width=3),
            hovertemplate='<b>Dias Úteis:</b> %{x:.0f}<br><b>Taxa:</b> %{y:.4f}%<extra></extra>'
        ))
        
        # Layout do gráfico
        fig.update_layout(
            title=f"Estrutura a Termo da Taxa DI - {data_encontrada.strftime('%d/%m/%Y')}",
            xaxis_title="Dias Úteis até o Vencimento",
            yaxis_title="Taxa de Juros (%)",
            hovermode='closest',
            template='plotly_white',
            height=600,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Exibir gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas de qualidade do ajuste
        col1, col2, col3, col4 = st.columns(4)
        
        # Calcular valores ajustados nos pontos observados
        if metodo == "Nelson-Siegel":
            y_fitted = nelson_siegel(params_ns, x_data)
        elif metodo == "Nelson-Siegel-Svensson":
            y_fitted = nelson_siegel_svensson(params_nss, x_data)
        elif metodo == "Smoothing Spline":
            y_fitted = smoothing_spline(x_data, y_data, x_data, smoothing_factor)
        elif metodo == "Interpolação Linear":
            y_fitted = linear_interpolation(x_data, y_data, x_data)
        elif metodo == "Cubic Spline":
            y_fitted = cubic_spline(x_data, y_data, x_data)
        elif metodo == "PCHIP (Monotônica)":
            y_fitted = pchip_interpolation(x_data, y_data, x_data)
        elif metodo == "Akima Spline":
            y_fitted = akima_interpolation(x_data, y_data, x_data)
        
        # Calcular métricas
        residuos = y_data - y_fitted
        rmse = np.sqrt(np.mean(residuos ** 2))
        mae = np.mean(np.abs(residuos))
        r2 = 1 - (np.sum(residuos ** 2) / np.sum((y_data - np.mean(y_data)) ** 2))
        max_erro = np.max(np.abs(residuos))
        
        with col1:
            st.metric("RMSE", f"{rmse*100:.2f}%")
        with col2:
            st.metric("MAE", f"{mae*100:.2f}%")
        with col3:
            st.metric("R²", f"{r2:.2f}")
        with col4:
            st.metric("Erro Máximo", f"{max_erro*100:.2f}%")

        # Seção de análise adicional
        st.markdown("---")
        
        # Expander com explicação das métricas
        with st.expander("ℹ️ O que significam essas métricas?", expanded=False):
            st.markdown("""
            **RMSE (Root Mean Square Error - Erro Quadrático Médio):**
            
            $$RMSE = \\sqrt{\\frac{1}{n}\\sum_{i=1}^n (y_i - \\hat{y}_i)^2}$$
            
            - Mede a raiz da média dos erros ao quadrado
            - Penaliza mais fortemente erros grandes
            - **Quanto menor, melhor o ajuste**
            - Unidade: mesma das taxas (pontos percentuais)
            
            ---
            
            **MAE (Mean Absolute Error - Erro Absoluto Médio):**
            
            $$MAE = \\frac{1}{n}\\sum_{i=1}^n |y_i - \\hat{y}_i|$$
            
            - Mede a média dos erros em valor absoluto
            - Menos sensível a outliers que RMSE
            - **Quanto menor, melhor o ajuste**
            - Unidade: mesma das taxas (pontos percentuais)
            
            ---
            
            **R² (Coeficiente de Determinação):**
            
            $$R^2 = 1 - \\frac{\\sum_{i=1}^n (y_i - \\hat{y}_i)^2}{\\sum_{i=1}^n (y_i - \\bar{y})^2}$$
            
            - Mede a proporção da variância explicada pelo modelo
            - Varia entre 0 e 1 (ou negativo se o modelo for muito ruim)
            - **Quanto mais próximo de 1, melhor o ajuste**
            - R² = 1: ajuste perfeito
            - R² = 0: modelo não explica nada
            
            ---
            
            **Erro Máximo:**
            
            $$\\text{Erro Máximo} = \\max_i |y_i - \\hat{y}_i|$$
            
            - Maior desvio (em valor absoluto) entre observado e ajustado
            - Identifica o pior ponto de ajuste
            - **Quanto menor, melhor**
            - Útil para detectar outliers ou problemas pontuais
            
            ---
            
            **Interpretação Prática:**
            
            - Para taxas DI, erros típicos de bons modelos ficam abaixo de 0.10% (10 bps)
            - Compare diferentes métodos usando essas métricas
            - Um R² > 0.99 indica excelente ajuste para estruturas a termo
            """)
        
        
        # Expander com equação e explicação do método
        with st.expander("📐 Equação do Método", expanded=False):
            if metodo == "Interpolação Linear":
                st.markdown("""
                **Equação:**
                
                $$y = y_i + \\frac{y_{i+1} - y_i}{x_{i+1} - x_i}(x - x_i)$$
                
                Para $x_i \\leq x \\leq x_{i+1}$
                
                **Descrição:** Conecta pontos adjacentes com segmentos de reta.
                """)
            
            elif metodo == "Cubic Spline":
                st.markdown("""
                **Equação:**
                
                $$S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3$$
                
                Para $x_i \\leq x \\leq x_{i+1}$
                
                **Descrição:** Polinômios cúbicos conectados com continuidade até a segunda derivada.
                """)
            
            elif metodo == "PCHIP (Monotônica)":
                st.markdown("""
                **Equação:** Interpolação cúbica por partes com derivadas $m_i$ que preservam monotonicidade.
                
                **Descrição:** Garante que não haja overshoots ou oscilações espúrias entre os pontos.
                """)
            
            elif metodo == "Akima Spline":
                st.markdown("""
                **Equação:** Spline cúbica com ponderação robusta para cálculo de derivadas.
                
                **Descrição:** Menos sensível a outliers, produz curvas mais naturais que cubic spline.
                """)
            
            elif metodo == "Smoothing Spline":
                st.markdown(f"""
                **Equação de Otimização:**
                
                $$\\min_f \\sum_{{i=1}}^n (y_i - f(x_i))^2 + \\lambda \\int (f''(x))^2 dx$$
                
                **Parâmetros:**
                - **λ (fator de suavização):** {smoothing_factor:.1f}
                - Valores maiores → mais suavização
                - Valores menores → mais fidelidade aos dados
                
                **Descrição:** Balanceia o ajuste aos dados com a suavidade da curva.
                """)
            
            elif metodo == "Nelson-Siegel":
                st.markdown("""
                **Equação:**
                
                $$r(\\tau) = \\beta_0 + \\beta_1 \\frac{1 - e^{-\\tau/\\lambda}}{\\tau/\\lambda} + \\beta_2 \\left(\\frac{1 - e^{-\\tau/\\lambda}}{\\tau/\\lambda} - e^{-\\tau/\\lambda}\\right)$$
                
                **Parâmetros:**
                - **β₀:** Nível de longo prazo (taxa assintótica)
                - **β₁:** Componente de curto prazo
                - **β₂:** Componente de médio prazo (curvatura)
                - **λ:** Parâmetro de decaimento (controla onde ocorre a curvatura máxima)
                
                **Descrição:** Modelo paramétrico clássico para estrutura a termo.
                """)
            
            elif metodo == "Nelson-Siegel-Svensson":
                st.markdown("""
                **Equação:**
                
                $$r(\\tau) = \\beta_0 + \\beta_1 \\frac{1 - e^{-\\tau/\\lambda_1}}{\\tau/\\lambda_1} + \\beta_2 \\left(\\frac{1 - e^{-\\tau/\\lambda_1}}{\\tau/\\lambda_1} - e^{-\\tau/\\lambda_1}\\right)$$
                $$+ \\beta_3 \\left(\\frac{1 - e^{-\\tau/\\lambda_2}}{\\tau/\\lambda_2} - e^{-\\tau/\\lambda_2}\\right)$$
                
                **Parâmetros:**
                - **β₀:** Nível de longo prazo
                - **β₁:** Componente de curto prazo
                - **β₂:** Primeira componente de curvatura
                - **β₃:** Segunda componente de curvatura
                - **λ₁:** Primeiro parâmetro de decaimento
                - **λ₂:** Segundo parâmetro de decaimento
                
                **Descrição:** Extensão do NS com maior flexibilidade para capturar formas complexas.
                """)

        # Seção de análise adicional
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📋 Dados Utilizados", "📊 Análise de Resíduos", "💾 Download"])
        
        with tab1:
            with st.expander("📋 Dados dos Contratos DI1 (até 5 anos)", expanded=False):
                # Preparar DataFrame para exibição
                df_display = df_filtrado[['TickerSymbol', 'ExpirationDate', 'BDaysToExp', 'SettlementRate']].copy()
                df_display['SettlementRate'] = df_display['SettlementRate'] * 100
                df_display.columns = ['Contrato', 'Vencimento', 'Dias Úteis', 'Taxa (%)']
                
                st.dataframe(
                    df_display,
                    use_container_width=True,
                    hide_index=True
                )
                
        with tab2:
            st.subheader("Análise de Resíduos")
            
            # Gráfico de resíduos
            fig_residuos = go.Figure()
            
            fig_residuos.add_trace(go.Scatter(
                x=x_data,
                y=residuos * 100,
                mode='markers',
                name='Resíduos',
                marker=dict(size=8, color='orange'),
                hovertemplate='<b>Dias Úteis:</b> %{x}<br><b>Resíduo:</b> %{y:.4f}%<extra></extra>'
            ))
            
            fig_residuos.add_hline(
                y=0, 
                line_dash="dash", 
                line_color="gray",
                annotation_text="Zero"
            )
            
            fig_residuos.update_layout(
                title="Resíduos do Ajuste",
                xaxis_title="Dias Úteis até o Vencimento",
                yaxis_title="Resíduo (%)",
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_residuos, use_container_width=True)
            
            # Estatísticas dos resíduos
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Média dos Resíduos", f"{np.mean(residuos)*100:.6f}%")
                st.metric("Desvio Padrão", f"{np.std(residuos)*100:.3f}%")
            with col2:
                st.metric("Resíduo Mínimo", f"{np.min(residuos)*100:.3f}%")
                st.metric("Resíduo Máximo", f"{np.max(residuos)*100:.3f}%")

            # Expander com explicação sobre resíduos
            with st.expander("ℹ️ O que são resíduos?", expanded=False):
                st.markdown("""
                **Resíduos** são as diferenças entre os valores observados e os valores ajustados pelo modelo:
                
                $$\\text{Resíduo}_i = y_i^{\\text{observado}} - y_i^{\\text{ajustado}}$$
                
                **Interpretação:**
                
                - **Resíduos próximos de zero:** O modelo ajusta bem os dados
                - **Resíduos aleatórios em torno de zero:** Bom ajuste, sem viés sistemático
                - **Padrões nos resíduos:** Indicam que o modelo pode não capturar toda a estrutura dos dados
                
                **O que observar:**
                
                - ✅ **Ideal:** Resíduos distribuídos aleatoriamente em torno de zero, sem padrões claros
                - ⚠️ **Atenção:** Resíduos com tendência crescente/decrescente ou padrões sistemáticos
                - ⚠️ **Atenção:** Resíduos muito grandes em pontos específicos (outliers)
                
                **Métricas:**
                
                - **Média dos Resíduos:** Deve estar próxima de zero (modelo sem viés)
                - **Desvio Padrão:** Mede a dispersão dos erros
                - **Resíduo Mínimo/Máximo:** Identificam os maiores desvios
                """)
            
        with tab3:
            st.subheader("Download dos Resultados")
            
            # Preparar DataFrame com resultados
            df_resultados = pd.DataFrame({
                'DiasUteis': x_smooth,
                'TaxaAjustada_pct': y_smooth_pct
            })
            
            # Converter para CSV
            csv = df_resultados.to_csv(index=False, decimal=',', sep=';')
            
            st.download_button(
                label="📥 Download Curva Ajustada (CSV)",
                data=csv,
                file_name=f"curva_di_{data_encontrada.strftime('%Y%m%d')}_{metodo.replace(' ', '_')}.csv",
                mime="text/csv",
                key="ettj_download_curva"
            )
            
            # Download dos dados originais
            csv_original = df_filtrado.to_csv(index=False, decimal=',', sep=';')
            
            st.download_button(
                label="📥 Download Dados Originais (CSV)",
                data=csv_original,
                file_name=f"dados_di1_{data_encontrada.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="ettj_download_dados"
            )

    except Exception as e:
        st.error(f"❌ Erro ao processar dados: {str(e)}")
        st.exception(e)

    # Informações no rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        <p><strong>Fonte de Dados:</strong> B3 (Brasil, Bolsa, Balcão) via pyield</p>
        <p><strong>Nota:</strong> Os contratos DI1 são essencialmente taxas zero-cupom com capitalização de 252 dias úteis</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# EXECUÇÃO STANDALONE (para testes)
# =============================================================================
if __name__ == "__main__":
    # Configuração da página para execução standalone
    st.set_page_config(
        page_title="Estrutura a Termo - Taxa DI",
        page_icon="📈",
        layout="wide"
    )
    render()