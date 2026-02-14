"""
Módulo 01 - Estrutura a Termo de Taxas de Juros
Laboratório de Mercado Financeiro
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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


@st.cache_data(ttl=3600)
def contar_dias_uteis(data_inicio, data_fim):
    """
    Conta dias úteis entre duas datas usando pyield
    """
    try:
        bdays = yd.count_bdays(
            start=data_inicio.strftime("%Y-%m-%d"),
            end=data_fim.strftime("%Y-%m-%d")
        )
        # Converter para int caso venha como outro tipo
        return int(bdays)
    except Exception:
        return None


# =============================================================================
# FUNÇÕES DE INTERPOLAÇÃO / SUAVIZAÇÃO
# =============================================================================

def flat_forward_interpolation(x, y, x_new):
    """
    Interpolação Flat Forward (padrão de mercado brasileiro).
    
    Assume taxa forward constante entre cada par de vértices conhecidos.
    Convenção: capitalização composta, base 252 dias úteis.
    
    (1 + r_d)^(d/252) = (1 + r_i)^(d_i/252) * (1 + f_{i,i+1})^((d - d_i)/252)
    
    onde f_{i,i+1} é a taxa forward implícita entre os vértices i e i+1.
    """
    # Garantir ordenação
    sort_idx = np.argsort(x)
    x_sorted = x[sort_idx]
    y_sorted = y[sort_idx]
    
    # Fatores de capitalização nos vértices conhecidos: (1 + r)^(d/252)
    cap_factors = (1 + y_sorted) ** (x_sorted / 252.0)
    
    # Resultado
    y_result = np.zeros_like(x_new, dtype=float)
    
    for i, d in enumerate(x_new):
        if d <= x_sorted[0]:
            # Antes do primeiro vértice: usar a taxa do primeiro vértice (flat)
            y_result[i] = y_sorted[0]
        elif d >= x_sorted[-1]:
            # Após o último vértice: usar a taxa do último vértice (flat)
            y_result[i] = y_sorted[-1]
        else:
            # Encontrar o segmento: x_sorted[k] <= d < x_sorted[k+1]
            k = np.searchsorted(x_sorted, d, side='right') - 1
            
            # Se d coincide exatamente com um vértice
            if np.isclose(d, x_sorted[k]):
                y_result[i] = y_sorted[k]
            else:
                # Taxa forward implícita no segmento [k, k+1]
                # f = ( cap_factors[k+1] / cap_factors[k] )^(252 / (d_{k+1} - d_k)) - 1
                delta_seg = x_sorted[k + 1] - x_sorted[k]
                fwd_rate = (cap_factors[k + 1] / cap_factors[k]) ** (252.0 / delta_seg) - 1
                
                # Fator de capitalização até d:
                # cap_d = cap_factors[k] * (1 + fwd_rate)^((d - d_k) / 252)
                delta_d = d - x_sorted[k]
                cap_d = cap_factors[k] * (1 + fwd_rate) ** (delta_d / 252.0)
                
                # Recuperar taxa spot: r_d = cap_d^(252/d) - 1
                y_result[i] = cap_d ** (252.0 / d) - 1
    
    return y_result


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
# FUNÇÃO PARA APLICAR MÉTODO DE INTERPOLAÇÃO
# =============================================================================

def aplicar_metodo(metodo, x_data, y_data, x_target, smoothing_factor=None):
    """
    Aplica o método de interpolação selecionado.
    Retorna: (y_interpolado, params_dict ou None)
    params_dict contém parâmetros estimados para NS/NSS.
    """
    params_info = None
    
    if metodo == "Flat Forward":
        y_result = flat_forward_interpolation(x_data, y_data, x_target)
    
    elif metodo == "Interpolação Linear":
        y_result = linear_interpolation(x_data, y_data, x_target)
    
    elif metodo == "Cubic Spline":
        y_result = cubic_spline(x_data, y_data, x_target)
    
    elif metodo == "PCHIP (Monotônica)":
        y_result = pchip_interpolation(x_data, y_data, x_target)
    
    elif metodo == "Akima Spline":
        y_result = akima_interpolation(x_data, y_data, x_target)
    
    elif metodo == "Smoothing Spline":
        y_result = smoothing_spline(x_data, y_data, x_target, smoothing_factor)
    
    elif metodo == "Nelson-Siegel":
        params_ns = fit_nelson_siegel(x_data, y_data)
        y_result = nelson_siegel(params_ns, x_target)
        params_info = {
            'tipo': 'NS',
            'params': params_ns,
            'labels': ['β₀', 'β₁', 'β₂', 'λ'],
            'formats': ['.6f', '.6f', '.6f', '.2f']
        }
    
    elif metodo == "Nelson-Siegel-Svensson":
        params_nss = fit_nelson_siegel_svensson(x_data, y_data)
        y_result = nelson_siegel_svensson(params_nss, x_target)
        params_info = {
            'tipo': 'NSS',
            'params': params_nss,
            'labels': ['β₀', 'β₁', 'β₂', 'β₃', 'λ₁', 'λ₂'],
            'formats': ['.6f', '.6f', '.6f', '.6f', '.2f', '.2f']
        }
    
    return y_result, params_info


# =============================================================================
# FUNÇÃO PARA EXIBIR EQUAÇÃO DO MÉTODO
# =============================================================================

def exibir_equacao_metodo(metodo, smoothing_factor=None):
    """Exibe a equação e explicação do método selecionado"""
    
    if metodo == "Flat Forward":
        st.markdown("""
        **Equação (capitalização composta, base 252 d.u.):**
        
        A taxa forward implícita entre os vértices $i$ e $i+1$:
        
        $$f_{i,i+1} = \\left(\\frac{(1+r_{i+1})^{d_{i+1}/252}}{(1+r_i)^{d_i/252}}\\right)^{\\frac{252}{d_{i+1}-d_i}} - 1$$
        
        Para um ponto intermediário $d$ onde $d_i \\leq d \\leq d_{i+1}$:
        
        $$(1+r_d)^{d/252} = (1+r_i)^{d_i/252} \\cdot (1+f_{i,i+1})^{(d-d_i)/252}$$
        
        **Descrição:** Assume taxa forward constante entre vértices adjacentes. 
        Padrão de mercado no Brasil (B3/ANBIMA). Respeita a convenção de capitalização 
        composta em base 252 dias úteis e garante não-arbitragem entre vértices.
        """)
    
    elif metodo == "Interpolação Linear":
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
        sf_display = smoothing_factor if smoothing_factor is not None else "N"
        st.markdown(f"""
        **Equação de Otimização:**
        
        $$\\min_f \\sum_{{i=1}}^n (y_i - f(x_i))^2 + \\lambda \\int (f''(x))^2 dx$$
        
        **Parâmetros:**
        - **λ (fator de suavização):** {sf_display:.1f}
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


# =============================================================================
# FUNÇÕES DE RENDERIZAÇÃO DOS MODOS
# =============================================================================

def render_modo_unico(df_filtrado, data_encontrada, metodo, smoothing_factor):
    """Renderiza o modo de curva única com consulta de taxa"""
    
    # Preparar dados para modelagem
    x_data = df_filtrado['BDaysToExp'].to_numpy(dtype='float64')
    y_data = df_filtrado['SettlementRate'].to_numpy(dtype='float64')
    
    # Gerar pontos para a curva suavizada
    x_smooth = np.linspace(x_data.min(), x_data.max(), 500)
    
    # Aplicar método selecionado
    try:
        y_smooth, params_info = aplicar_metodo(metodo, x_data, y_data, x_smooth, smoothing_factor)
        
        # Exibir parâmetros estimados na sidebar (NS e NSS)
        if params_info is not None:
            st.sidebar.markdown("**Parâmetros Estimados:**")
            for label, val, fmt in zip(params_info['labels'], params_info['params'], params_info['formats']):
                st.sidebar.text(f"{label} = {val:{fmt}}")
        
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
        
        # =====================================================================
        # CONSULTA DE TAXA (Issue 2)
        # =====================================================================
        st.markdown("---")
        st.subheader("🔍 Consulta de Taxa na Curva")
        
        col_consulta1, col_consulta2 = st.columns(2)
        
        with col_consulta1:
            # Calcular datas limites para o date_input
            from datetime import date
            min_bdays = int(x_data.min())
            max_bdays = int(x_data.max())
            
            # Opção 1: por data
            st.markdown("**Consultar por data:**")
            
            # Estimar datas-calendário aproximadas para os limites
            data_ref = data_encontrada
            data_min_aprox = data_ref + timedelta(days=int(min_bdays * 1.45))
            data_max_aprox = data_ref + timedelta(days=int(max_bdays * 1.45))
            
            data_consulta = st.date_input(
                "Data de vencimento desejada",
                value=data_ref + timedelta(days=int(252 * 1.45)),  # ~1 ano
                min_value=data_min_aprox,
                max_value=data_max_aprox,
                key="ettj_data_consulta"
            )
            
            # Converter data para dias úteis
            bdays_consulta = contar_dias_uteis(data_ref, data_consulta)
            
            if bdays_consulta is not None:
                st.caption(f"≈ {bdays_consulta} dias úteis a partir de {data_ref.strftime('%d/%m/%Y')}")
        
        with col_consulta2:
            # Opção 2: por dias úteis direto
            st.markdown("**Consultar por dias úteis:**")
            du_consulta = st.number_input(
                "Dias úteis até o vencimento",
                min_value=min_bdays,
                max_value=max_bdays,
                value=252,
                step=1,
                key="ettj_du_consulta"
            )
        
        # Calcular e exibir a taxa
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            if bdays_consulta is not None and min_bdays <= bdays_consulta <= max_bdays:
                taxa_data, _ = aplicar_metodo(
                    metodo, x_data, y_data, 
                    np.array([float(bdays_consulta)]), smoothing_factor
                )
                st.metric(
                    f"Taxa para {data_consulta.strftime('%d/%m/%Y')}",
                    f"{taxa_data[0] * 100:.4f}%",
                    help=f"{bdays_consulta} dias úteis"
                )
            elif bdays_consulta is not None:
                st.warning("Data fora do intervalo da curva.")
        
        with col_res2:
            taxa_du, _ = aplicar_metodo(
                metodo, x_data, y_data, 
                np.array([float(du_consulta)]), smoothing_factor
            )
            st.metric(
                f"Taxa para {du_consulta} dias úteis",
                f"{taxa_du[0] * 100:.4f}%"
            )
        
        # =====================================================================
        # MÉTRICAS DE QUALIDADE
        # =====================================================================
        st.markdown("---")
        
        # Calcular valores ajustados nos pontos observados
        y_fitted, _ = aplicar_metodo(metodo, x_data, y_data, x_data, smoothing_factor)
        
        # Calcular métricas
        residuos = y_data - y_fitted
        rmse = np.sqrt(np.mean(residuos ** 2))
        mae = np.mean(np.abs(residuos))
        r2 = 1 - (np.sum(residuos ** 2) / np.sum((y_data - np.mean(y_data)) ** 2))
        max_erro = np.max(np.abs(residuos))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("RMSE", f"{rmse*100:.2f}%")
        with col2:
            st.metric("MAE", f"{mae*100:.2f}%")
        with col3:
            st.metric("R²", f"{r2:.2f}")
        with col4:
            st.metric("Erro Máximo", f"{max_erro*100:.2f}%")
        
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
        
        # Expander com equação do método
        with st.expander("📐 Equação do Método", expanded=False):
            exibir_equacao_metodo(metodo, smoothing_factor)
        
        # =====================================================================
        # ABAS: DADOS, RESÍDUOS, DOWNLOAD
        # =====================================================================
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📋 Dados Utilizados", "📊 Análise de Resíduos", "💾 Download"])
        
        with tab1:
            with st.expander("📋 Dados dos Contratos DI1 (até 5 anos)", expanded=False):
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
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Média dos Resíduos", f"{np.mean(residuos)*100:.6f}%")
                st.metric("Desvio Padrão", f"{np.std(residuos)*100:.3f}%")
            with col2:
                st.metric("Resíduo Mínimo", f"{np.min(residuos)*100:.3f}%")
                st.metric("Resíduo Máximo", f"{np.max(residuos)*100:.3f}%")

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
            
            df_resultados = pd.DataFrame({
                'DiasUteis': x_smooth,
                'TaxaAjustada_pct': y_smooth_pct
            })
            
            csv = df_resultados.to_csv(index=False, decimal=',', sep=';')
            
            st.download_button(
                label="📥 Download Curva Ajustada (CSV)",
                data=csv,
                file_name=f"curva_di_{data_encontrada.strftime('%Y%m%d')}_{metodo.replace(' ', '_')}.csv",
                mime="text/csv",
                key="ettj_download_curva"
            )
            
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


def render_modo_comparacao(metodo, smoothing_factor):
    """Renderiza o modo de comparação de duas curvas"""
    
    st.subheader("📅 Selecione as duas datas de referência")
    
    data_hoje = datetime.now().date()
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        data_ref_a = st.date_input(
            "📌 Data A (referência)",
            value=data_hoje - timedelta(days=30),
            max_value=data_hoje,
            key="ettj_comp_data_a"
        )
    
    with col_d2:
        data_ref_b = st.date_input(
            "📌 Data B (referência)",
            value=data_hoje - timedelta(days=1),
            max_value=data_hoje,
            key="ettj_comp_data_b"
        )
    
    if data_ref_a == data_ref_b:
        st.warning("⚠️ Selecione duas datas diferentes para comparação.")
        st.stop()
    
    # Carregar dados para ambas as datas
    with st.spinner("Carregando dados para Data A..."):
        df_a, data_enc_a = buscar_dados_di1(data_ref_a)
    
    with st.spinner("Carregando dados para Data B..."):
        df_b, data_enc_b = buscar_dados_di1(data_ref_b)
    
    if df_a is None or df_b is None:
        st.error("❌ Não foi possível carregar dados para uma ou ambas as datas.")
        st.stop()
    
    # Informar datas efetivas
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        if data_enc_a != data_ref_a:
            st.info(f"Data A: usando dados de **{data_enc_a.strftime('%d/%m/%Y')}**")
        else:
            st.success(f"Data A: **{data_enc_a.strftime('%d/%m/%Y')}**")
    with col_info2:
        if data_enc_b != data_ref_b:
            st.info(f"Data B: usando dados de **{data_enc_b.strftime('%d/%m/%Y')}**")
        else:
            st.success(f"Data B: **{data_enc_b.strftime('%d/%m/%Y')}**")
    
    # Filtrar dados
    df_filt_a = filtrar_dados_5anos(df_a, data_enc_a)
    df_filt_b = filtrar_dados_5anos(df_b, data_enc_b)
    
    # Preparar dados
    x_a = df_filt_a['BDaysToExp'].to_numpy(dtype='float64')
    y_a = df_filt_a['SettlementRate'].to_numpy(dtype='float64')
    x_b = df_filt_b['BDaysToExp'].to_numpy(dtype='float64')
    y_b = df_filt_b['SettlementRate'].to_numpy(dtype='float64')
    
    # Intervalo comum (interseção dos ranges)
    x_min_comum = max(x_a.min(), x_b.min())
    x_max_comum = min(x_a.max(), x_b.max())
    
    if x_min_comum >= x_max_comum:
        st.error("❌ Não há interseção de prazos entre as duas datas.")
        st.stop()
    
    # Gerar pontos comuns para interpolação
    x_smooth = np.linspace(x_min_comum, x_max_comum, 500)
    
    try:
        # Aplicar método para ambas as curvas
        y_smooth_a, params_a = aplicar_metodo(metodo, x_a, y_a, x_smooth, smoothing_factor)
        y_smooth_b, params_b = aplicar_metodo(metodo, x_b, y_b, x_smooth, smoothing_factor)
        
        # Exibir parâmetros na sidebar se NS/NSS
        if params_a is not None:
            st.sidebar.markdown(f"**Parâmetros Data A ({data_enc_a.strftime('%d/%m/%Y')}):**")
            for label, val, fmt in zip(params_a['labels'], params_a['params'], params_a['formats']):
                st.sidebar.text(f"{label} = {val:{fmt}}")
        if params_b is not None:
            st.sidebar.markdown(f"**Parâmetros Data B ({data_enc_b.strftime('%d/%m/%Y')}):**")
            for label, val, fmt in zip(params_b['labels'], params_b['params'], params_b['formats']):
                st.sidebar.text(f"{label} = {val:{fmt}}")
        
        # Converter para percentual
        y_smooth_a_pct = y_smooth_a * 100
        y_smooth_b_pct = y_smooth_b * 100
        diff_pct = y_smooth_b_pct - y_smooth_a_pct  # B - A
        
        # =================================================================
        # GRÁFICO 1: COMPARAÇÃO DAS CURVAS
        # =================================================================
        fig_comp = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.65, 0.35],
            subplot_titles=[
                f"Comparação de Curvas ETTJ ({metodo})",
                f"Diferença (Data B − Data A) em pontos percentuais"
            ]
        )
        
        # Curva A - pontos observados
        fig_comp.add_trace(go.Scatter(
            x=x_a,
            y=y_a * 100,
            mode='markers',
            name=f'Observado A ({data_enc_a.strftime("%d/%m/%Y")})',
            marker=dict(size=6, color='royalblue', symbol='circle', opacity=0.5),
            hovertemplate='<b>DU:</b> %{x}<br><b>Taxa:</b> %{y:.4f}%<extra></extra>',
            legendgroup='A'
        ), row=1, col=1)
        
        # Curva A - interpolada
        fig_comp.add_trace(go.Scatter(
            x=x_smooth,
            y=y_smooth_a_pct,
            mode='lines',
            name=f'Curva A ({data_enc_a.strftime("%d/%m/%Y")})',
            line=dict(color='royalblue', width=3),
            hovertemplate='<b>DU:</b> %{x:.0f}<br><b>Taxa A:</b> %{y:.4f}%<extra></extra>',
            legendgroup='A'
        ), row=1, col=1)
        
        # Curva B - pontos observados
        fig_comp.add_trace(go.Scatter(
            x=x_b,
            y=y_b * 100,
            mode='markers',
            name=f'Observado B ({data_enc_b.strftime("%d/%m/%Y")})',
            marker=dict(size=6, color='crimson', symbol='diamond', opacity=0.5),
            hovertemplate='<b>DU:</b> %{x}<br><b>Taxa:</b> %{y:.4f}%<extra></extra>',
            legendgroup='B'
        ), row=1, col=1)
        
        # Curva B - interpolada
        fig_comp.add_trace(go.Scatter(
            x=x_smooth,
            y=y_smooth_b_pct,
            mode='lines',
            name=f'Curva B ({data_enc_b.strftime("%d/%m/%Y")})',
            line=dict(color='crimson', width=3),
            hovertemplate='<b>DU:</b> %{x:.0f}<br><b>Taxa B:</b> %{y:.4f}%<extra></extra>',
            legendgroup='B'
        ), row=1, col=1)
        
        # =================================================================
        # GRÁFICO 2: DIFERENÇA (B - A)
        # =================================================================
        # Colorir diferença: verde se B > A, vermelho se B < A
        fig_comp.add_trace(go.Scatter(
            x=x_smooth,
            y=diff_pct,
            mode='lines',
            name='Diferença (B − A)',
            line=dict(color='darkorange', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(255, 165, 0, 0.15)',
            hovertemplate='<b>DU:</b> %{x:.0f}<br><b>Δ Taxa:</b> %{y:.4f} p.p.<extra></extra>'
        ), row=2, col=1)
        
        fig_comp.add_hline(
            y=0, line_dash="dash", line_color="gray", row=2, col=1
        )
        
        # Layout
        fig_comp.update_layout(
            template='plotly_white',
            height=850,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified'
        )
        
        fig_comp.update_xaxes(title_text="Dias Úteis a partir da Data de Referência", row=2, col=1)
        fig_comp.update_yaxes(title_text="Taxa de Juros (%)", row=1, col=1)
        fig_comp.update_yaxes(title_text="Diferença (p.p.)", row=2, col=1)
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # =================================================================
        # ESTATÍSTICAS DA COMPARAÇÃO
        # =================================================================
        st.markdown("---")
        st.subheader("📊 Estatísticas da Comparação")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Diferença Média",
                f"{np.mean(diff_pct):.2f} p.p.",
                help="Média da diferença (B − A) ao longo da curva"
            )
        with col2:
            st.metric(
                "Diferença Máxima",
                f"{np.max(diff_pct):.2f} p.p.",
                help="Maior diferença positiva (B acima de A)"
            )
        with col3:
            st.metric(
                "Diferença Mínima",
                f"{np.min(diff_pct):.2f} p.p.",
                help="Maior diferença negativa (A acima de B)"
            )
        with col4:
            # Prazo onde a diferença é máxima em valor absoluto
            idx_max_abs = np.argmax(np.abs(diff_pct))
            du_max_diff = int(x_smooth[idx_max_abs])
            st.metric(
                "DU Maior Divergência",
                f"{du_max_diff} d.u.",
                help="Prazo (dias úteis) onde a diferença absoluta é máxima"
            )
        
        # Tabela resumo em prazos-chave
        st.markdown("**Comparação em prazos-chave:**")
        prazos_chave = [21, 63, 126, 252, 504, 756, 1008, 1260]
        prazos_validos = [p for p in prazos_chave if x_min_comum <= p <= x_max_comum]
        
        if prazos_validos:
            prazos_np = np.array(prazos_validos, dtype=float)
            taxas_a_chave, _ = aplicar_metodo(metodo, x_a, y_a, prazos_np, smoothing_factor)
            taxas_b_chave, _ = aplicar_metodo(metodo, x_b, y_b, prazos_np, smoothing_factor)
            
            prazo_labels = {
                21: "1M", 63: "3M", 126: "6M", 252: "1A",
                504: "2A", 756: "3A", 1008: "4A", 1260: "5A"
            }
            
            df_comp = pd.DataFrame({
                'Prazo': [prazo_labels.get(p, f"{p} DU") for p in prazos_validos],
                'Dias Úteis': prazos_validos,
                f'Taxa A ({data_enc_a.strftime("%d/%m/%Y")})': [f"{t*100:.4f}%" for t in taxas_a_chave],
                f'Taxa B ({data_enc_b.strftime("%d/%m/%Y")})': [f"{t*100:.4f}%" for t in taxas_b_chave],
                'Diferença (p.p.)': [f"{(b-a)*100:.4f}" for a, b in zip(taxas_a_chave, taxas_b_chave)]
            })
            
            st.dataframe(df_comp, use_container_width=True, hide_index=True)
        
        # Equação do método
        with st.expander("📐 Equação do Método", expanded=False):
            exibir_equacao_metodo(metodo, smoothing_factor)
        
        # Download
        with st.expander("💾 Download dos Resultados", expanded=False):
            df_download = pd.DataFrame({
                'DiasUteis': x_smooth,
                f'Taxa_A_{data_enc_a.strftime("%Y%m%d")}_pct': y_smooth_a_pct,
                f'Taxa_B_{data_enc_b.strftime("%Y%m%d")}_pct': y_smooth_b_pct,
                'Diferenca_pp': diff_pct
            })
            
            csv_comp = df_download.to_csv(index=False, decimal=',', sep=';')
            
            st.download_button(
                label="📥 Download Comparação (CSV)",
                data=csv_comp,
                file_name=f"comparacao_ettj_{data_enc_a.strftime('%Y%m%d')}_vs_{data_enc_b.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="ettj_download_comparacao"
            )
    
    except Exception as e:
        st.error(f"❌ Erro ao processar comparação: {str(e)}")
        st.exception(e)


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

    # =========================================================================
    # SIDEBAR - CONTROLES
    # =========================================================================
    st.sidebar.header("⚙️ Configurações")
    
    # Modo de operação
    modo = st.sidebar.radio(
        "🔀 Modo de Operação",
        ["Curva Única", "Comparação de Curvas"],
        key="ettj_modo",
        help="Curva Única: análise detalhada de uma data. Comparação: sobreposição de duas datas."
    )
    
    st.sidebar.markdown("---")
    
    # Método de interpolação (comum a ambos os modos)
    st.sidebar.subheader("🎯 Método de Interpolação")
    
    metodo = st.sidebar.selectbox(
        "Escolha o método:",
        [
            "Flat Forward",
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
    
    # Parâmetro específico do Smoothing Spline
    smoothing_factor = None
    if metodo == "Smoothing Spline":
        smoothing_factor = st.sidebar.slider(
            "Fator de Suavização",
            min_value=0.0,
            max_value=200.0,
            value=50.0,
            step=10.0,
            help="Valores maiores = mais suavização",
            key="ettj_smoothing"
        )
    
    # =========================================================================
    # MODO CURVA ÚNICA
    # =========================================================================
    if modo == "Curva Única":
        st.sidebar.markdown("---")
        st.sidebar.subheader("📅 Data de Referência")
        
        data_hoje = datetime.now().date()
        data_referencia = st.sidebar.date_input(
            "Data de Referência",
            value=data_hoje - timedelta(days=1),
            max_value=data_hoje,
            key="ettj_data_ref"
        )
        
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
        
        # Estatísticas na sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Estatísticas dos Dados")
        st.sidebar.metric("Total de Contratos", len(df_original))
        st.sidebar.metric("Contratos até 5 anos", len(df_filtrado))
        prazo_max = int(df_filtrado['BDaysToExp'].to_numpy().max())
        st.sidebar.metric("Prazo Máximo (dias úteis)", prazo_max)
        
        # Renderizar modo único
        render_modo_unico(df_filtrado, data_encontrada, metodo, smoothing_factor)
    
    # =========================================================================
    # MODO COMPARAÇÃO
    # =========================================================================
    else:
        if st.sidebar.button("🔄 Recarregar Dados", type="primary", key="ettj_btn_recarregar"):
            st.cache_data.clear()
        
        render_modo_comparacao(metodo, smoothing_factor)

    # =========================================================================
    # RODAPÉ
    # =========================================================================
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