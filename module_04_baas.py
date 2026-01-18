"""
Módulo 04 - Banking as a Service (BaaS)
Laboratório de Mercado Financeiro
Baseado na Consulta Pública BCB 108/2024 e 115/2025
"""

import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components


# =============================================================================
# FUNÇÕES AUXILIARES (fora do render)
# =============================================================================

def inject_custom_css():
    """Injeta CSS customizado para o tema dark"""
    st.markdown("""
    <style>
        /* --- RESET GERAL E FUNDO --- */
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #020617 !important;
            border-right: 1px solid #1e293b;
        }

        h1, h2, h3, h4, h5, h6 { color: #f8fafc !important; }
        p, li, label { color: #cbd5e1 !important; }
        
        .block-container { 
            padding-top: 2rem; 
            padding-bottom: 3rem; 
            max-width: 1400px; 
        }

        /* --- CARDS E CONTAINERS --- */
        .metric-card { 
            background-color: #1e293b !important;
            border: 1px solid #334155; 
            border-radius: 12px; 
            padding: 20px; 
            margin: 10px 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: #38bdf8;
        }

        .highlight-card { 
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); 
            border: 1px solid #0ea5e9;
            border-radius: 16px; 
            padding: 24px; 
            margin: 12px 0; 
        }
        
        .highlight-card-green { 
            background: linear-gradient(145deg, #064e3b 0%, #022c22 100%);
            border: 1px solid #10b981; 
            border-radius: 16px; padding: 24px; margin: 12px 0;
        }
        
        .highlight-card-amber { 
            background: linear-gradient(145deg, #451a03 0%, #431407 100%);
            border: 1px solid #f59e0b; 
            border-radius: 16px; padding: 24px; margin: 12px 0;
        }

        /* --- COMPONENTES STREAMLIT --- */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="base-input"] {
            background-color: #1e293b !important;
            border-color: #475569 !important;
            color: white !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1e293b;
            padding: 10px;
            border-radius: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #3b82f6 !important;
            color: white !important;
        }

        /* Métricas Nativas */
        [data-testid="stMetric"] {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #334155;
        }
        [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
        [data-testid="stMetricValue"] { color: #f8fafc !important; }

        /* Badges */
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
        .badge-cyan { background: rgba(14, 165, 233, 0.2); color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.4); }
        .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
        .badge-amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
        .badge-violet { background: rgba(139, 92, 246, 0.2); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.4); }

        /* Utilitários */
        hr { border: none; height: 1px; background: #334155; margin: 2rem 0; }
        .main-title { font-size: 2.5rem; font-weight: 700; color: #f8fafc; text-align: center; margin-bottom: 0.5rem; }
        .subtitle { color: #94a3b8; text-align: center; font-size: 1.1rem; margin-bottom: 2rem; }
        .section-title { font-size: 1.5rem; font-weight: 600; color: #f8fafc; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid #334155; }
        
        /* Caixas de Texto */
        .info-box { background: rgba(14, 165, 233, 0.15); border-left: 4px solid #0ea5e9; padding: 16px; border-radius: 4px; margin: 16px 0; color: #e0f2fe; }
        .warning-box { background: rgba(245, 158, 11, 0.15); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 4px; margin: 16px 0; color: #fef3c7; }
        .danger-box { background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 16px; border-radius: 4px; margin: 16px 0; color: #fee2e2; }

        .main .block-container {
            padding-top: 1rem !important;
        }

        [data-testid="collapsedControl"] {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: fixed !important;
            left: 10px !important;
            top: 10px !important;
            z-index: 9999 !important;
            background-color: #020617 !important;
            border: 2px solid #0ea5e9 !important;
            border-radius: 5px !important;
            padding: 5px !important;
            width: 40px !important;
            height: 40px !important;
        }

        [data-testid="collapsedControl"]:hover {
            background-color: #1e293b !important;
            border-color: #38bdf8 !important;
        }

        [data-testid="collapsedControl"] svg {
            fill: #f8fafc !important;
            color: #f8fafc !important;
        }

    </style>
    """, unsafe_allow_html=True)


def render_baas_animation():
    """Renderiza a animação BaaS a partir do arquivo JSX"""
    try:
        jsx_path = 'BaaSAnimation.jsx'
        with open(jsx_path, 'r', encoding='utf-8') as f:
            jsx_code = f.read()
        
        jsx_lines = jsx_code.split('\n')
        jsx_code_clean = []
        
        for line in jsx_lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('export default'):
                continue
            jsx_code_clean.append(line)
        
        jsx_code_final = '\n'.join(jsx_code_clean)
        
        html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
            <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
            <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
            
            <style>
                * {{
                    box-sizing: border-box;
                }}
                html, body {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    overflow-x: hidden;
                }}
                body {{ 
                    background-color: #0f172a;
                    font-family: 'Outfit', 'Inter', system-ui, sans-serif;
                }}
                #root {{
                    width: 100%;
                    height: 100%;
                    min-height: 100vh;
                }}
            </style>
        </head>
        <body>
            <div id="root"></div>

            <script type="text/babel">
                const {{ useState, useEffect, useRef }} = React;
                
                {jsx_code_final}
                
                const rootElement = document.getElementById('root');
                if (rootElement) {{
                    const root = ReactDOM.createRoot(rootElement);
                    root.render(<BaaSAnimation />);
                }}
            </script>
        </body>
        </html>
        """
        
        components.html(html_code, height=1200, scrolling=True)
        
    except FileNotFoundError:
        st.error("❌ Arquivo 'BaaSAnimation.jsx' não encontrado")
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")


def create_metric_card(icon, title, value, description, color="cyan"):
    """Cria um card de métrica estilizado"""
    colors = {"cyan": ("#0ea5e9", "rgba(14, 165, 233, 0.2)"), "violet": ("#8b5cf6", "rgba(139, 92, 246, 0.2)"), "emerald": ("#10b981", "rgba(16, 185, 129, 0.2)"), "amber": ("#f59e0b", "rgba(245, 158, 11, 0.2)"), "rose": ("#f43f5e", "rgba(244, 63, 94, 0.2)")}
    primary, bg = colors.get(color, colors["cyan"])
    return f'<div class="metric-card"><div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;"><div style="width: 48px; height: 48px; background: {bg}; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">{icon}</div><div><div style="color: {primary}; font-size: 1.5rem; font-weight: 700;">{value}</div><div style="color: #94a3b8; font-size: 0.85rem;">{title}</div></div></div><p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">{description}</p></div>'


def create_participant_card(icon, name, subtitle, responsibilities, color):
    """Cria um card de participante"""
    resp_html = "".join([f'<li style="color: #cbd5e1; margin: 4px 0;">{r}</li>' for r in responsibilities])
    return f'<div style="background: linear-gradient(145deg, {color}15 0%, {color}08 100%); border: 1px solid {color}40; border-radius: 16px; padding: 20px; height: 100%;"><div style="font-size: 2.5rem; margin-bottom: 12px;">{icon}</div><h4 style="color: #f8fafc; font-size: 1.1rem; margin: 0 0 4px 0;">{name}</h4><p style="color: {color}; font-size: 0.8rem; margin: 0 0 12px 0;">{subtitle}</p><ul style="margin: 0; padding-left: 18px; font-size: 0.85rem;">{resp_html}</ul></div>'


def create_flow_diagram():
    """Cria diagrama de fluxo do ecossistema BaaS"""
    fig = go.Figure()
    nodes = {'BCB': (0.1, 0.5), 'Banco': (0.35, 0.8), 'Middleware': (0.5, 0.5), 'Tomador': (0.65, 0.2), 'Cliente': (0.9, 0.5)}
    edges = [('BCB', 'Banco', 'Regulação'), ('Banco', 'Middleware', 'APIs'), ('Middleware', 'Tomador', 'Serviços'), ('Tomador', 'Cliente', 'UX'), ('Banco', 'Tomador', 'Supervisão')]
    for start, end, label in edges:
        x0, y0 = nodes[start]; x1, y1 = nodes[end]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', line=dict(color='rgba(100, 116, 139, 0.4)', width=2, dash='dot'), hoverinfo='skip', showlegend=False))
        fig.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2, text=label, showarrow=False, font=dict(size=10, color='#64748b'), bgcolor='rgba(15, 23, 42, 0.8)', borderpad=4)
    node_styles = {'BCB': ('#10b981', '⚖️', 'Banco Central'), 'Banco': ('#0ea5e9', '🏛️', 'Instituição Prestadora'), 'Middleware': ('#f59e0b', '🔌', 'Middleware'), 'Tomador': ('#8b5cf6', '📱', 'Tomador de Serviços'), 'Cliente': ('#ec4899', '👤', 'Cliente Final')}
    for name, (x, y) in nodes.items():
        color, icon, label = node_styles[name]
        fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers+text', marker=dict(size=60, color=color, opacity=0.2), text=f"{icon}<br><b>{label}</b>", textposition='middle center', textfont=dict(size=10, color='#f8fafc'), showlegend=False))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1, 1.1]), margin=dict(l=20, r=20, t=20, b=20), height=350)
    return fig


def create_risk_radar():
    """Cria gráfico radar de riscos"""
    categories = ['Regulatório', 'Operacional', 'Reputacional', 'Econômico', 'Cibernético', 'Conformidade']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[5, 4, 3, 4, 5, 5], theta=categories, fill='toself', name='Nível de Risco', fillcolor='rgba(239, 68, 68, 0.3)', line=dict(color='#ef4444', width=2)))
    fig.add_trace(go.Scatterpolar(r=[3, 3, 2, 3, 3, 4], theta=categories, fill='toself', name='Após Mitigação', fillcolor='rgba(16, 185, 129, 0.3)', line=dict(color='#10b981', width=2)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(color='#64748b'), gridcolor='rgba(100, 116, 139, 0.2)'), angularaxis=dict(tickfont=dict(color='#94a3b8', size=11), gridcolor='rgba(100, 116, 139, 0.2)'), bgcolor='rgba(0,0,0,0)'), showlegend=True, legend=dict(font=dict(color='#94a3b8'), bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=60, r=60, t=40, b=40), height=400)
    return fig


def create_global_comparison():
    """Cria gráfico de comparação global"""
    regions = ['EUA', 'UK', 'UE', 'Brasil', 'APAC', 'África']
    metrics = {'Maturidade Reg.': [4, 5, 5, 4, 3, 2], 'Adoção BaaS': [5, 4, 4, 3, 4, 2], 'Infra Tech': [5, 5, 4, 4, 4, 2], 'Inclusão Fin.': [3, 4, 4, 3, 3, 4]}
    fig = go.Figure()
    colors = ['#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b']
    for i, (metric, values) in enumerate(metrics.items()):
        fig.add_trace(go.Bar(name=metric, x=regions, y=values, marker_color=colors[i], opacity=0.8))
    fig.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(tickfont=dict(color='#94a3b8')), yaxis=dict(tickfont=dict(color='#94a3b8'), range=[0, 6]), legend=dict(font=dict(color='#94a3b8'), bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1), margin=dict(l=40, r=40, t=60, b=40), height=400)
    return fig


def create_timeline():
    """Cria timeline regulatória"""
    events = [('Out 2024', 'CP 108/2024', 'done'), ('Jan 2025', 'Prazo Original', 'done'), ('Fev 2025', 'CP 115/2025', 'current'), ('2025', 'Análise', 'pending'), ('2025', 'Resolução', 'pending')]
    fig = go.Figure()
    for i, (date, title, status) in enumerate(events):
        color = '#10b981' if status == 'done' else '#0ea5e9' if status == 'current' else '#64748b'
        size = 20 if status == 'current' else 15
        fig.add_trace(go.Scatter(x=[i], y=[0], mode='markers+text', marker=dict(size=size, color=color), text=[f"<b>{date}</b><br>{title}"], textposition='top center', textfont=dict(size=10, color='#f8fafc' if status != 'pending' else '#64748b'), showlegend=False))
    fig.add_trace(go.Scatter(x=list(range(len(events))), y=[0]*len(events), mode='lines', line=dict(color='rgba(100, 116, 139, 0.4)', width=2, dash='dot'), showlegend=False))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 1]), margin=dict(l=20, r=20, t=80, b=20), height=200)
    return fig


# =============================================================================
# FUNÇÃO RENDER - PONTO DE ENTRADA DO MÓDULO
# =============================================================================

def render():
    """Função principal que renderiza o módulo BaaS"""
    
    # SIDEBAR
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 20px 0;"><div style="font-size: 3rem; margin-bottom: 10px;">🏦</div><h2 style="color: #f8fafc; margin: 0; font-size: 1.3rem;">Banking as a Service</h2><p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">Aplicação Pedagógica MBA</p></div>', unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("📚 Navegação", ["🏠 Introdução", "🔄 Ecossistema BaaS", "💼 Modelos de Negócio", "⚙️ Serviços", "📋 Regulação BCB", "⚠️ Riscos", "🚀 Oportunidades", "🌍 Cenário Global", "📊 Simulador", "📊 Animação", "📝 Quiz"], label_visibility="collapsed", key="m04_page")
        st.markdown("---")
        st.markdown('<div style="padding: 15px; background: rgba(14, 165, 233, 0.1); border-radius: 12px; border: 1px solid rgba(14, 165, 233, 0.2);"><p style="color: #0ea5e9; font-size: 0.75rem; margin: 0 0 8px 0; font-weight: 600;">📌 REFERÊNCIA</p><p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">CP BCB 108/2024 e 115/2025</p></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #475569; font-size: 0.7rem; margin-top: 20px;"><p>COPPEAD/UFRJ</p></div>', unsafe_allow_html=True)

    # CSS
    inject_custom_css()

    # PÁGINAS
    if page == "🏠 Introdução":
        st.markdown('<h1 class="main-title">Banking as a Service</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">A Transformação Digital dos Serviços Financeiros</p>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; margin-bottom: 2rem;"><span class="badge badge-cyan">Consulta Pública BCB nº 108/2024</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="highlight-card"><div style="display: flex; align-items: flex-start; gap: 16px;"><div style="font-size: 2.5rem;">💡</div><div><h3 style="color: #f8fafc; margin: 0 0 8px 0;">O que é Banking as a Service?</h3><p style="color: #cbd5e1; line-height: 1.7; margin: 0;"><strong style="color: #0ea5e9;">Banking as a Service (BaaS)</strong> é um modelo onde instituições financeiras autorizadas pelo BCB disponibilizam sua <strong style="color: #8b5cf6;">infraestrutura regulamentada</strong> para que entidades terceiras (fintechs, varejistas, plataformas digitais) possam oferecer <strong style="color: #10b981;">produtos e serviços financeiros</strong> aos seus clientes.</p></div></div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(create_metric_card("🏛️", "Instituições Prestadoras", "Bancos, IPs, SCDs", "Entidades autorizadas pelo BCB que fornecem a infraestrutura regulamentada.", "cyan"), unsafe_allow_html=True)
        with col2: st.markdown(create_metric_card("📱", "Tomadores de Serviços", "Fintechs, Varejo", "Entidades que utilizam a infraestrutura BaaS para oferecer serviços.", "violet"), unsafe_allow_html=True)
        with col3: st.markdown(create_metric_card("👤", "Clientes Finais", "PF e PJ", "Consumidores que acessam serviços financeiros através da experiência integrada.", "emerald"), unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h2 class="section-title">📌 Por que Regular o BaaS?</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.markdown('<div class="metric-card"><h3>🔍 Contexto</h3><p>Crescimento relevante no volume de serviços financeiros via BaaS, estruturados por contratos privados com diversidade de regras. O BCB identificou necessidade de disciplinar para mitigar riscos ao SFN e SPB.</p></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="metric-card"><h3>🎯 Objetivos</h3><ul style="color: #cbd5e1; line-height: 2;"><li>Segurança e solidez do sistema</li><li>Eficiência e competitividade</li><li>Inovação e livre concorrência</li><li>Inclusão financeira</li><li>Proteção ao consumidor</li></ul></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="highlight-card-green"><h3 style="color: #10b981; margin: 0 0 12px 0;">💻 Analogia: BaaS é o "SaaS" do Setor Bancário</h3><p style="color: #cbd5e1; line-height: 1.7; margin: 0;">Assim como empresas de tecnologia consomem capacidades de computação em nuvem <strong>sob demanda</strong> (Software as a Service), o BaaS permite que empresas não-bancárias consumam <strong>capacidades bancárias via APIs</strong>, sem precisar construir ou licenciar toda a infraestrutura por conta própria.</p></div>', unsafe_allow_html=True)

    elif page == "🔄 Ecossistema BaaS":
        st.markdown('<h1 class="main-title">Ecossistema BaaS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Participantes, Fluxos e Responsabilidades</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">🔄 Fluxo do Ecossistema</h2>', unsafe_allow_html=True)
        st.plotly_chart(create_flow_diagram(), use_container_width=True, config={'displayModeBar': False})
        st.markdown("---")
        st.markdown('<h2 class="section-title">👥 Participantes</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(create_participant_card("🏛️", "Instituição Prestadora", "Banco, IP, SCD autorizado pelo BCB", ["Licença regulatória", "Gestão de balanço", "Conformidade PLD/FT", "Supervisão de riscos", "Reporte ao BCB"], "#0ea5e9"), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(create_participant_card("📱", "Tomador de Serviços", "Fintech, Varejo, Plataforma Digital", ["Tecnologia e UX", "Marketing e aquisição", "Design de produto", "Relacionamento com cliente"], "#8b5cf6"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_participant_card("🔌", "Middleware (Opcional)", "Plataforma de integração técnica", ["Simplificação via APIs", "Camada de abstração", "Gestão de programa", "Suporte operacional"], "#f59e0b"), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(create_participant_card("⚖️", "Banco Central do Brasil", "Regulador e Supervisor", ["Autorização de instituições", "Regulação do modelo BaaS", "Supervisão e fiscalização", "Proteção do SFN"], "#10b981"), unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="warning-box"><strong>⚠️ Ponto Crítico:</strong> A instituição prestadora é a <strong>responsável final</strong> perante o BCB pela conformidade de toda a cadeia.</div>', unsafe_allow_html=True)

    elif page == "💼 Modelos de Negócio":
        st.markdown('<h1 class="main-title">Modelos de Negócio</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Estruturas Operacionais e Modelos de Receita</p>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🤝 Estruturas Operacionais", "💰 Modelos de Receita"])
        with tab1:
            st.markdown('<h2 class="section-title">Estruturas de Parceria</h2>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown('<div class="metric-card"><div style="text-align: center; margin-bottom: 16px;"><div style="font-size: 3rem;">🤝</div><h3 style="color: #0ea5e9;">Parceria Direta</h3></div><p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px;">Integração direta entre instituição e tomador.</p><p style="color: #10b981; font-size: 0.8rem; margin: 4px 0;">✓ Maior controle e flexibilidade</p><p style="color: #f43f5e; font-size: 0.8rem; margin: 4px 0;">✗ Maior complexidade técnica</p></div>', unsafe_allow_html=True)
            with col2: st.markdown('<div class="metric-card"><div style="text-align: center; margin-bottom: 16px;"><div style="font-size: 3rem;">🔗</div><h3 style="color: #8b5cf6;">Via Middleware</h3></div><p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px;">Plataforma intermediária facilita a integração.</p><p style="color: #10b981; font-size: 0.8rem; margin: 4px 0;">✓ Integração simplificada</p><p style="color: #f43f5e; font-size: 0.8rem; margin: 4px 0;">✗ Dependência do intermediário</p></div>', unsafe_allow_html=True)
            with col3: st.markdown('<div class="metric-card"><div style="text-align: center; margin-bottom: 16px;"><div style="font-size: 3rem;">⚡</div><h3 style="color: #10b981;">Banco Nativo API</h3></div><p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px;">Bancos construídos com tecnologia moderna.</p><p style="color: #10b981; font-size: 0.8rem; margin: 4px 0;">✓ Alta performance/escala</p><p style="color: #f43f5e; font-size: 0.8rem; margin: 4px 0;">✗ Poucos players</p></div>', unsafe_allow_html=True)
        with tab2:
            st.markdown('<h2 class="section-title">Modelos de Monetização</h2>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="highlight-card"><h4 style="color: #0ea5e9; margin: 0 0 12px 0;">💳 Orientado por Intercâmbio</h4><p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.7;">Receita gerada a cada transação com cartão. Nos EUA, Emenda Durbin criou arbitragem favorecendo bancos menores.</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="highlight-card-green"><h4 style="color: #10b981; margin: 0 0 12px 0;">💰 Captação de Depósitos</h4><p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.7;">Fintechs como canal de aquisição de depósitos de baixo custo. Banco compartilha margem de juros líquida.</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="highlight-card-amber"><h4 style="color: #f59e0b; margin: 0 0 12px 0;">📈 Originação de Crédito</h4><p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.7;">Banco origina empréstimos usando sua licença, vende para fintech ou investidores.</p><p style="color: #f59e0b; font-size: 0.8rem; margin-top: 8px;">⚠️ Atenção ao risco de "True Lender"</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-card"><h4 style="color: #8b5cf6; margin: 0 0 12px 0;">🔧 Taxas de Plataforma</h4><p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.7;">Modelo de middlewares: taxas fixas, percentual sobre volume, ou compartilhamento de receita.</p></div>', unsafe_allow_html=True)

    elif page == "⚙️ Serviços":
        st.markdown('<h1 class="main-title">Serviços BaaS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Escopo de Serviços conforme CP BCB 108/2024</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📋 Detalhamento dos Serviços</h2>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        services_data = [("💳", "Contas de Pagamento", "emerald", "Previsto", "Contas correntes, poupança e pré-pagas."), ("⚡", "Pix", "emerald", "Previsto", "Pagamento instantâneo: QR Code, Saque, Troco."), ("💎", "Cartões", "emerald", "Previsto", "Débito, crédito e pré-pagos."), ("📤", "TED/TEF", "emerald", "Previsto", "Transferências bancárias tradicionais."), ("📈", "Crédito", "amber", "Em Discussão", "Oferta e contratação de empréstimos."), ("🏪", "Credenciamento", "amber", "Em Discussão", "Aceitação de pagamentos. Subcredenciadores."), ("🔄", "ITP", "cyan", "Em Avaliação", "Iniciação via Open Finance."), ("🌎", "eFX", "cyan", "Em Avaliação", "Pagamentos internacionais."), ("📊", "Investimentos", "violet", "Futuro", "CDBs, fundos e previdência.")]
        for i, (icon, name, color, status, desc) in enumerate(services_data):
            col = [col1, col2, col3][i % 3]
            with col: st.markdown(f'<div class="metric-card"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;"><span style="font-size: 2rem;">{icon}</span><span class="badge badge-{color}">{status}</span></div><h4 style="color: #f8fafc; margin: 0 0 8px 0;">{name}</h4><p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">{desc}</p></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h2 class="section-title">💬 Temas em Discussão</h2>', unsafe_allow_html=True)
        with st.expander("🏪 Subcredenciamento via BaaS"): st.markdown("O BCB propõe que subcredenciadores atuem exclusivamente como tomadores de BaaS, operando através de credenciadores autorizados.")
        with st.expander("🔄 Inclusão de ITP"): st.markdown("Avaliação de condicionantes para Iniciação de Transação de Pagamento: limitação de volume, portes de prestador e tomador.")
        with st.expander("🌎 Inclusão de eFX"): st.markdown("Discussão sobre câmbio internacional: montante máximo, tipo de instituição, obrigatoriedade de conta na mesma instituição.")

    elif page == "📋 Regulação BCB":
        st.markdown('<h1 class="main-title">Regulação BCB</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Consulta Pública 108/2024 e 115/2025</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📅 Cronograma Regulatório</h2>', unsafe_allow_html=True)
        st.plotly_chart(create_timeline(), use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div class="info-box"><strong>📌 Status Atual:</strong> Consulta Pública prorrogada até <strong>28 de fevereiro de 2025</strong> (Edital 115/2025).</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h2 class="section-title">⚖️ Princípios da Regulação</h2>', unsafe_allow_html=True)
        principles = [("🔍", "Transparência", "Clareza nas informações ao cliente"), ("⚖️", "Conduta", "Proteção do consumidor financeiro"), ("🛡️", "PLD/FT", "Prevenção à lavagem de dinheiro"), ("🔒", "Controles Internos", "Gestão de riscos"), ("📋", "Responsabilização", "Definição clara de responsabilidades"), ("📊", "Prudencial", "Requerimentos de capital em avaliação")]
        col1, col2 = st.columns(2)
        for i, (icon, title, desc) in enumerate(principles):
            col = col1 if i % 2 == 0 else col2
            with col: st.markdown(f'<div class="metric-card"><div style="display: flex; align-items: center; gap: 12px;"><span style="font-size: 1.8rem;">{icon}</span><div><h4 style="color: #f8fafc; margin: 0;">{title}</h4><p style="color: #94a3b8; font-size: 0.85rem; margin: 4px 0 0 0;">{desc}</p></div></div></div>', unsafe_allow_html=True)

    elif page == "⚠️ Riscos":
        st.markdown('<h1 class="main-title">Riscos do BaaS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Mapeamento e Estratégias de Mitigação</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📊 Radar de Riscos</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1: st.plotly_chart(create_risk_radar(), use_container_width=True, config={'displayModeBar': False})
        with col2: st.markdown('<div class="metric-card"><h4 style="color: #f8fafc; margin: 0 0 12px 0;">Legenda</h4><div style="display: flex; align-items: center; gap: 8px; margin: 8px 0;"><div style="width: 16px; height: 16px; background: rgba(239, 68, 68, 0.5); border-radius: 4px;"></div><span style="color: #94a3b8; font-size: 0.85rem;">Risco Inerente</span></div><div style="display: flex; align-items: center; gap: 8px; margin: 8px 0;"><div style="width: 16px; height: 16px; background: rgba(16, 185, 129, 0.5); border-radius: 4px;"></div><span style="color: #94a3b8; font-size: 0.85rem;">Após Mitigação</span></div><hr style="margin: 16px 0; border-color: rgba(100,116,139,0.2);"><p style="color: #64748b; font-size: 0.8rem; margin: 0;">Escala de 1 (baixo) a 5 (crítico)</p></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<h2 class="section-title">⚠️ Caso Synapse (2024)</h2>', unsafe_allow_html=True)
        st.markdown('<div class="danger-box"><h4 style="color: #ef4444; margin: 0 0 12px 0;">A Falência que Abalou o Mercado BaaS</h4><p style="color: #cbd5e1; line-height: 1.7;">A Synapse, middleware de BaaS nos EUA, deixou centenas de milhares de clientes sem acesso aos fundos. Problemas: falhas de reconciliação em contas FBO, supervisão inadequada, complexidade de resolução.</p><p style="color: #f59e0b; font-size: 0.9rem; margin-top: 12px;"><strong>Lição:</strong> Dependência de middleware adiciona camada de risco que bancos parceiros precisam supervisionar.</p></div>', unsafe_allow_html=True)

    elif page == "🚀 Oportunidades":
        st.markdown('<h1 class="main-title">Oportunidades do BaaS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Benefícios para o Sistema Financeiro e a Sociedade</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">🎯 Principais Oportunidades</h2>', unsafe_allow_html=True)
        opportunities = [("🚀", "Inclusão Financeira", "#10b981", "Ampliação do acesso a serviços financeiros para populações desbancarizadas."), ("💡", "Inovação", "#8b5cf6", "Novos produtos e experiências financeiras integradas."), ("📈", "Novos Mercados", "#0ea5e9", "Acesso a segmentos antes inviáveis economicamente."), ("💰", "Diversificação", "#f59e0b", "Novas fontes de receita para bancos e fintechs."), ("⚡", "Eficiência", "#ec4899", "Otimização via especialização de cada participante."), ("🤝", "Competitividade", "#06b6d4", "Democratização da infraestrutura bancária.")]
        col1, col2, col3 = st.columns(3)
        for i, (icon, title, color, desc) in enumerate(opportunities):
            col = [col1, col2, col3][i % 3]
            with col: st.markdown(f'<div class="metric-card" style="border-color: {color}30;"><div style="font-size: 2.5rem; margin-bottom: 12px;">{icon}</div><h4 style="color: {color}; margin: 0 0 8px 0;">{title}</h4><p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.6;">{desc}</p></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="highlight-card"><div style="display: flex; align-items: flex-start; gap: 20px;"><div style="font-size: 4rem;">🔮</div><div><h3 style="color: #f8fafc; margin: 0 0 12px 0;">Embedded Finance - O Futuro</h3><p style="color: #cbd5e1; line-height: 1.8;">Serviços financeiros integrados de forma invisível em plataformas não-financeiras. E-commerce, mobilidade, SaaS B2B e Gig Economy oferecendo conta, pagamentos, crédito e seguros na jornada do usuário.</p></div></div></div>', unsafe_allow_html=True)

    elif page == "🌍 Cenário Global":
        st.markdown('<h1 class="main-title">Cenário Global</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Comparativo Internacional de Modelos BaaS</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📊 Comparativo por Região</h2>', unsafe_allow_html=True)
        st.plotly_chart(create_global_comparison(), use_container_width=True, config={'displayModeBar': False})
        st.markdown("---")
        st.markdown('<h2 class="section-title">🇧🇷 Brasil: Pioneiro em Infraestrutura</h2>', unsafe_allow_html=True)
        st.markdown('<div class="highlight-card-green"><div style="display: flex; align-items: flex-start; gap: 20px;"><div style="font-size: 4rem;">🇧🇷</div><div style="flex: 1;"><h3 style="color: #f8fafc; margin: 0 0 12px 0;">Posição de Destaque Global</h3><p style="color: #cbd5e1; line-height: 1.7;">O Brasil possui uma das infraestruturas de pagamentos mais avançadas do mundo. <span style="color: #10b981; font-weight: 600;">Pix</span>, <span style="color: #0ea5e9; font-weight: 600;">Open Finance</span> e <span style="color: #8b5cf6; font-weight: 600;">Open Banking</span> posicionam o país na vanguarda.</p></div></div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        for col, (label, value, desc, color) in zip([col1, col2, col3], [("Pix", "150M+", "usuários", "#10b981"), ("Open Finance", "45M+", "consentimentos", "#0ea5e9"), ("Fintechs", "1.500+", "ativas", "#8b5cf6")]):
            with col: st.markdown(f'<div class="metric-card" style="text-align: center;"><div style="font-size: 1.8rem; font-weight: 700; color: {color};">{value}</div><div style="color: #f8fafc; font-size: 0.9rem; font-weight: 500;">{label}</div><div style="color: #64748b; font-size: 0.75rem;">{desc}</div></div>', unsafe_allow_html=True)

    elif page == "📊 Simulador":
        st.markdown('<h1 class="main-title">Simulador BaaS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Explore Cenários e Modelos de Negócio</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### ⚙️ Parâmetros")
            tipo_entidade = st.selectbox("Tipo de Tomador", ["Fintech (Neobank)", "Varejista", "Marketplace", "SaaS B2B", "Gig Economy"], key="m04_tipo_entidade")
            modelo_estrutura = st.selectbox("Estrutura de Parceria", ["Parceria Direta", "Via Middleware", "Banco Nativo API"], key="m04_modelo_estrutura")
            servicos = st.multiselect("Serviços Desejados", ["Conta de Pagamento", "Pix", "Cartão de Débito", "Cartão de Crédito", "Crédito/Empréstimo", "Câmbio (eFX)"], default=["Conta de Pagamento", "Pix", "Cartão de Débito"], key="m04_servicos")
            volume_clientes = st.slider("Volume de Clientes (milhares)", min_value=10, max_value=1000, value=100, step=10, key="m04_volume_clientes")
            ticket_medio = st.slider("Ticket Médio Mensal (R$)", min_value=50, max_value=5000, value=500, step=50, key="m04_ticket_medio")
        with col2:
            st.markdown("### 📊 Análise do Modelo")
            base_custo = {"Parceria Direta": 500000, "Via Middleware": 150000, "Banco Nativo API": 300000}
            base_tempo = {"Parceria Direta": 12, "Via Middleware": 4, "Banco Nativo API": 6}
            risco_score = {"Parceria Direta": 2, "Via Middleware": 4, "Banco Nativo API": 2}
            custo_total = base_custo[modelo_estrutura] + len(servicos) * 50000
            tempo_impl = base_tempo[modelo_estrutura] + len(servicos)
            clientes = volume_clientes * 1000
            receita_interchange = clientes * 0.015 * ticket_medio * 0.5 if "Cartão de Débito" in servicos else 0
            receita_float = clientes * ticket_medio * 0.3 * 0.01 if "Conta de Pagamento" in servicos else 0
            receita_credito = clientes * 0.1 * 2000 * 0.03 if "Crédito/Empréstimo" in servicos else 0
            receita_total_mensal = receita_interchange + receita_float + receita_credito
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.metric("💰 Investimento Inicial", f"R$ {custo_total:,.0f}".replace(",", "."))
                st.metric("⏱️ Time to Market", f"{tempo_impl} meses")
            with col_r2:
                st.metric("📈 Receita Mensal Est.", f"R$ {receita_total_mensal:,.0f}".replace(",", "."))
                st.metric("⚠️ Score de Risco", f"{risco_score[modelo_estrutura]}/5")
            if receita_total_mensal > 0:
                fig = go.Figure(data=[go.Pie(labels=['Intercâmbio', 'Float', 'Crédito'], values=[receita_interchange, receita_float, receita_credito], hole=0.6, marker_colors=['#0ea5e9', '#10b981', '#f59e0b'])])
                fig.update_layout(showlegend=True, legend=dict(font=dict(color='#94a3b8')), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20), height=250, annotations=[dict(text='Receita', x=0.5, y=0.5, font_size=14, font_color='#f8fafc', showarrow=False)])
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown("### 💡 Recomendações")
            if modelo_estrutura == "Via Middleware" and len(servicos) > 4: st.warning("⚠️ Com muitos serviços, considere parceria direta.")
            if "Crédito/Empréstimo" in servicos: st.info("📋 Operações de crédito exigem atenção à regulação de correspondentes.")
            if volume_clientes > 500: st.success("✅ Volume alto justifica investimento em infraestrutura própria.")

    elif page == "📊 Animação":
        st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
        render_baas_animation()
                
    elif page == "📝 Quiz":
        st.markdown('<h1 class="main-title">Quiz BaaS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Teste seus Conhecimentos</p>', unsafe_allow_html=True)
        questions = [{"q": "1. Qual é a principal responsabilidade da instituição prestadora no BaaS?", "options": ["Marketing", "Licença regulatória e conformidade perante o BCB", "Desenvolvimento de APIs", "Design de UX"], "correct": 1}, {"q": "2. O que a Emenda Durbin nos EUA criou em relação ao BaaS?", "options": ["Obrigação de oferecer BaaS", "Arbitragem regulatória favorecendo bancos menores", "Proibição de middlewares", "Limite de clientes"], "correct": 1}, {"q": "3. Qual o principal risco demonstrado pelo caso Synapse?", "options": ["Custos baixos", "Falta de inovação", "Dependência e complexidade em múltiplas camadas", "Excesso de regulação"], "correct": 2}, {"q": "4. Qual prazo foi estabelecido pela CP 115/2025 para contribuições?", "options": ["31/01/2025", "28/02/2025", "31/03/2025", "30/04/2025"], "correct": 1}, {"q": "5. O que é 'Embedded Finance'?", "options": ["Financiamento de startups", "Serviços financeiros integrados em plataformas não-financeiras", "Banco digital tradicional", "Regulação de fintechs"], "correct": 1}]
        with st.form("m04_quiz_form"):
            answers = {}
            for i, q in enumerate(questions):
                st.markdown(f'<div class="metric-card"><h4 style="color: #f8fafc; margin: 0 0 16px 0;">{q["q"]}</h4></div>', unsafe_allow_html=True)
                answers[i] = st.radio(f"Selecione:", q["options"], key=f"m04_q_{i}", label_visibility="collapsed")
                st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("📊 Ver Resultado", use_container_width=True)
            if submitted:
                score = sum(1 for i, q in enumerate(questions) if q["options"].index(answers[i]) == q["correct"])
                percentage = (score / len(questions)) * 100
                color = "#10b981" if percentage >= 80 else "#f59e0b" if percentage >= 60 else "#ef4444"
                message = "🎉 Excelente!" if percentage >= 80 else "👍 Bom trabalho!" if percentage >= 60 else "📚 Continue estudando!"
                st.markdown(f'<div class="highlight-card" style="text-align: center; margin-top: 24px;"><div style="font-size: 4rem; color: {color}; font-weight: 700;">{score}/{len(questions)}</div><div style="color: #94a3b8; font-size: 1.2rem; margin: 8px 0;">{percentage:.0f}% de acertos</div><p style="color: #f8fafc; font-size: 1.1rem; margin-top: 16px;">{message}</p></div>', unsafe_allow_html=True)


# =============================================================================
# EXECUÇÃO STANDALONE (para testes)
# =============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="BaaS - Banking as a Service", 
        page_icon="🏦", 
        layout="wide", 
        initial_sidebar_state="expanded"
    )
    render()