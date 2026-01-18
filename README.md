# FIDC Builder 175 - Jornada de Estruturação

Aplicativo educacional interativo para ensinar os conceitos fundamentais da estruturação de FIDCs (Fundos de Investimento em Direitos Creditórios), com foco nas inovações da Resolução CVM 175/2022.

## 🎯 Objetivo

Este simulador foi desenvolvido para executivos de finanças, advogados e gestores em formação que desejam compreender o processo completo de criação de um FIDC, desde a análise de viabilidade econômica até o registro na CVM.

## 📚 Módulos do Aplicativo

### Módulo 1: Simulador de Viabilidade Econômica
- Demonstra matematicamente por que FIDCs pequenos são inviáveis
- Calcula o ponto de equilíbrio (breakeven)
- Analisa estrutura de custos fixos e variáveis
- Gera análise de sensibilidade

### Módulo 2: Arquiteto de Classes (CVM 175)
- Ensina o conceito de segregação patrimonial
- Demonstra diferença entre Classes e Subclasses
- Permite construir estruturas personalizadas interativamente
- Visualiza a hierarquia com diagramas dinâmicos

### Módulo 3: Laboratório de Subordinação e Risco
- Simula como a cota subordinada protege a cota sênior
- Demonstra absorção de perdas em diferentes cenários
- Analisa o conceito de desenquadramento
- Gera análises de sensibilidade a stress

### Módulo 4: Checklist Regulatório Inteligente
- Guia pelas regras de acesso ao varejo
- Valida elegibilidade da estrutura
- Identifica tipo de registro adequado
- Estima prazos e custos do processo

## 🚀 Como Executar

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Executar o Aplicativo

```bash
streamlit run fidc_builder.py
```

O aplicativo será aberto automaticamente no navegador em `http://localhost:8501`

## 📦 Estrutura de Arquivos

```
.
├── fidc_builder.py          # Arquivo principal do aplicativo
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
└── modulos/                # Pasta com os módulos
    ├── __init__.py
    ├── modulo1_viabilidade.py
    ├── modulo2_classes.py
    ├── modulo3_subordinacao.py
    └── modulo4_checklist.py
```

## 🎓 Público-Alvo

- **Executivos de Finanças:** CFOs e tesoureiros avaliando estruturação de FIDC
- **Advogados:** Profissionais especializados em direito do mercado de capitais
- **Gestores em Formação:** Profissionais em cursos de MBA e pós-graduação
- **Analistas de Crédito:** Profissionais analisando investimentos em FIDCs

## 📖 Conceitos Abordados

- Viabilidade econômica e breakeven
- Resolução CVM 175/2022
- Segregação patrimonial por classes
- Subordinação de cotas
- Direitos creditórios padronizados vs. não-padronizados
- Requisitos para acesso ao varejo
- Processo de registro na CVM
- Rating de crédito
- Desenquadramento e recomposição

## 💡 Características Pedagógicas

- **Interatividade:** Controles deslizantes, checkboxes e formulários
- **Visualizações:** Gráficos Plotly interativos e diagramas hierárquicos
- **Feedback Imediato:** Alertas e insights baseados nas escolhas do usuário
- **Cenários Práticos:** Casos de uso reais do mercado
- **Explicações Detalhadas:** Expanders com conceitos aprofundados

## 🔧 Tecnologias Utilizadas

- **Streamlit:** Framework para aplicações web em Python
- **Plotly:** Biblioteca para gráficos interativos
- **Graphviz:** Geração de diagramas hierárquicos
- **Pandas:** Manipulação de dados tabulares
- **NumPy:** Cálculos numéricos

## 📝 Notas Importantes

- Este aplicativo é desenvolvido **exclusivamente para fins educacionais**
- Não constitui assessoria jurídica, financeira ou de investimentos
- Baseado na Resolução CVM 175/2022 e melhores práticas de mercado
- Os valores e prazos são estimativas para fins didáticos

## 🤝 Contribuições

Este é um projeto educacional. Sugestões de melhorias são bem-vindas!

## 📄 Licença

Desenvolvido para fins pedagógicos no contexto acadêmico.

---

**Desenvolvido por:** Prof. José Américo  
**Instituição:** Coppead/UFRJ  
**Ano:** 2025
